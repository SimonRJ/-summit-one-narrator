"""Check an actual older worker and HTTP cache while a new release loads.

The server supplies the existing isolated learner fixture. No Playwright routing
is used: routing would disable the browser HTTP cache this test must exercise.
Movies are not played or editorially assessed by this cache test.
"""
import argparse
import ast
import asyncio
import hashlib
import json
import re
import subprocess
from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import urlsplit

from aiohttp import web
from playwright.async_api import async_playwright, expect


def git_bytes(root, ref, path):
    return subprocess.check_output(['git', 'show', f'{ref}:{path}'], cwd=root,
                                   stderr=subprocess.DEVNULL)


def cached_paths(worker):
    body = re.search(r'const staticFiles = (\[.*?\])\.map', worker, re.S).group(1)
    return {urlsplit(url).path.removeprefix('./') or 'index.html'
            for url in json.loads(body)}


async def verify(args):
    root, output = args.root.resolve(), args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    previous_worker = git_bytes(root, args.previous_ref, 'sw.js').decode()
    current_worker = (root / 'sw.js').read_text()
    previous_revision = re.search(r'const CACHE="([^"]+)"', previous_worker).group(1)
    current_revision = re.search(r'const CACHE="([^"]+)"', current_worker).group(1)
    assert previous_revision != current_revision
    paths = cached_paths(previous_worker) | cached_paths(current_worker) | {'sw.js', 'lesson-introduction-videos.css'}
    previous = {p: git_bytes(root, args.previous_ref, p) for p in paths}
    current = {p: (root / p).read_bytes() if (root / p).is_file()
               else git_bytes(root, 'HEAD', p) for p in paths}
    print(f'Snapshotted {len(paths)} real public files from baseline and current release.', flush=True)
    fixture_tree = ast.parse((root / 'tools/browser_checks.py').read_text())
    fixture = next(n.value.value for n in fixture_tree.body if isinstance(n, ast.Assign)
                   and any(isinstance(t, ast.Name) and t.id == 'MOCK' for t in n.targets))
    scope = '/-summit-one-narrator/'
    old_cache, new_cache = scope + ':' + previous_revision, scope + ':' + current_revision
    state = {'current': False, 'held_worker_requests': 0}
    gate = asyncio.Event()
    requests = []

    def record(message):
        report['checks'].append(message)
        print(message, flush=True)

    async def serve(request):
        if not request.path.startswith(scope):
            raise web.HTTPNotFound()
        path = request.path[len(scope):] or 'index.html'
        if '..' in Path(path).parts:
            raise web.HTTPNotFound()
        phase = 'current' if state['current'] else 'previous'
        requests.append({'phase': phase, 'path': path, 'query': request.query_string})
        if state['current'] and path == 'sw.js' and not gate.is_set():
            state['held_worker_requests'] += 1
            await gate.wait()
        content = fixture.encode() if path == 'supabase-client.js' else (current if state['current'] else previous).get(path)
        if content is None:
            raise web.HTTPNotFound()
        mime = {'.js': 'application/javascript', '.json': 'application/json',
                '.html': 'text/html', '.css': 'text/css', '.svg': 'image/svg+xml',
                '.webmanifest': 'application/manifest+json'}.get(Path(path).suffix)
        response = web.Response(body=content, content_type=mime)
        response.headers['Cache-Control'] = 'no-store' if path == 'sw.js' or path.endswith('.html') else 'public, max-age=86400, immutable'
        response.headers['ETag'] = '"' + hashlib.sha256(content).hexdigest() + '"'
        return response

    app = web.Application()
    app.router.add_get('/{path:.*}', serve)
    runner = web.AppRunner(app)
    await runner.setup()
    server = web.TCPSite(runner, '127.0.0.1', 0)
    await server.start()
    site = f'http://127.0.0.1:{server._server.sockets[0].getsockname()[1]}' + scope
    expected_lessons = {row['slot']: row for name in ['read-watch-practise', 'read-watch-practise-later']
                        for row in json.loads(current[f'data/{name}.json'])['lessons']}
    guides = json.loads(current['data/recorded-studies.json'])['lessons']
    old_guides = json.loads(previous['data/recorded-studies.json'])['lessons']
    old_guide_url = re.search(r'"(\./data/recorded-studies\.json\?v=[^"]+)"',
                              previous['lesson-introduction-media.js'].decode()).group(1)
    teaching = {row['id']: row for row in json.loads(current['data/teaching-72.json'])['items']}
    report = {'checked_at_utc': datetime.now(timezone.utc).isoformat(),
              'previous_ref': args.previous_ref, 'previous_cache': old_cache, 'current_cache': new_cache,
              'source_sha256': {p: hashlib.sha256(current[p]).hexdigest() for p in
                                ['app-main.js', 'sw.js', 'lesson-introduction-media.js',
                                 'data/recorded-studies.json', 'data/teaching-72.json',
                                 'data/read-watch-practise.json', 'data/read-watch-practise-later.json',
                                 'index.html', 'course-menu-ui.js', 'lesson-introduction-library.js',
                                 'lesson-introduction-videos.html', 'watch-lesson-intro.html',
                                 'offline-reader.html', 'offline-reader.js']},
              'checks': [], 'scope': 'Real Chromium service worker and browser HTTP-cache upgrade; isolated learner backend; source mappings and offline reader only, not media or editorial acceptance.'}
    browser = None
    try:
        async with async_playwright() as pw:
            options = {'headless': True}
            if args.chromium:
                options['executable_path'] = str(args.chromium)
            if args.browser_flags:
                options['args'] = json.loads(args.browser_flags.read_text().splitlines()[-1])
            browser = await pw.chromium.launch(**options)
            print('Chromium started.', flush=True)
            report['browser_version'] = browser.version
            context = await browser.new_context(viewport={'width': 1440, 'height': 900}, service_workers='allow')
            context.set_default_timeout(30000)
            await context.add_init_script('''
              const slot = Number(new URLSearchParams(location.search).get('fixtureSlot') || 9);
              window.fixture = {records:[], attempts:[], exams:[], writes:[], fail:false,
                progress:{completed_sessions:slot-1,current_session:slot,xp:0,rank:0,state:{}}};
              const originalFetch = window.fetch.bind(window);
              window.fetch = (input, init) => {
                const url = new URL(input instanceof Request ? input.url : input, location.href);
                if (url.hostname.endsWith('.supabase.co')) throw Error('Real backend prohibited in cache fixture');
                if (url.hostname === 'raw.githubusercontent.com' && url.pathname.endsWith('/lesson-intros-live.json')) {
                  return Promise.resolve(new Response(JSON.stringify({version:1,entries:[]}), {headers:{'Content-Type':'application/json'}}));
                }
                return originalFetch(input, init);
              };
            ''')
            page = await context.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            await page.goto(site + '?fixtureSlot=9', wait_until='domcontentloaded')
            await page.locator('#continue').wait_for()
            print('Previous app loaded; installing baseline worker.', flush=True)
            await page.evaluate("async () => { await navigator.serviceWorker.register('./sw.js'); }")
            await page.wait_for_function('() => Boolean(navigator.serviceWorker.controller)')
            await page.wait_for_function('async name => (await caches.keys()).includes(name)', arg=old_cache)
            # Warm the exact unversioned HTTP entry in addition to the worker's old manifests.
            warmed = await page.evaluate("async () => (await (await fetch('data/teaching-72.json')).json()).items.find(x=>x.id==='T16.3').video_url")
            assert warmed != teaching['T16.3']['video_url'], warmed
            report['warmed_t163_url'] = warmed
            record('Previous worker controls the page and its old T16.3 catalogue is warm.')
            state['current'] = True
            await page.evaluate('() => { navigator.serviceWorker.getRegistration().then(r => r.update()).catch(() => {}); }')
            before_probe = len(requests)
            stale = await page.evaluate('''async guideUrl => {
              const teaching = await (await fetch('data/teaching-72.json')).json();
              const guides = await (await fetch(guideUrl)).json();
              return {t163:teaching.items.find(x=>x.id==='T16.3').video_url,
                titles:[guides.lessons.S009?.title ?? null,guides.lessons.S010?.title ?? null]};
            }''', old_guide_url)
            assert stale['t163'] == warmed
            assert stale['titles'] == [old_guides.get(f'S{slot:03}', {}).get('title') for slot in (9, 10)]
            assert stale['titles'] != [guides[f'S{slot:03}']['title'] for slot in (9, 10)]
            assert not any(request['path'] == 'data/teaching-72.json' for request in requests[before_probe:])
            report['stale_control_after_server_flip'] = stale
            record('Old catalogue URLs retain old T16.3 and absent S009/S010 guide entries after the server flips; the HTTP teaching cache bypasses the server.')
            report['current_mappings'] = {}

            for slot in (9, 10):
                await page.goto(site + f'?fixtureSlot={slot}', wait_until='domcontentloaded')
                await page.locator('#continue').click()
                await expect(page.locator('.rwl-bridge')).to_contain_text(expected_lessons[slot]['bridge'])
                await page.locator('[data-screen-next]').click()
                await expect(page.locator('#openingVideo')).to_have_attribute('src', expected_lessons[slot]['movie'])
                report['current_mappings'][f'S{slot:03}'] = {'bridge': expected_lessons[slot]['bridge'],
                    'movie': await page.locator('#openingVideo').get_attribute('src'), 'guide_title':guides[f'S{slot:03}']['title']}
                record(f'S{slot:03} current Read and Watch use the new bridge and movie while the old worker controls.')

            await page.goto(site + '?fixtureSlot=26', wait_until='domcontentloaded')
            await page.locator('#continue').wait_for()
            await page.locator('#menuToggle').click()
            await page.locator('[data-menu-intro-slot="26"]').click()
            await page.locator('#replayCompanion > summary').click()
            await expect(page.locator('#replayNarratedTeaching video')).to_have_attribute('src', teaching['T16.3']['video_url'])
            report['current_mappings']['T16.3'] = await page.locator('#replayNarratedTeaching video').get_attribute('src')
            record('Current T16.3 companion uses the new catalogue declaration under the old controller.')

            await page.goto(site + 'lesson-introduction-videos.html', wait_until='domcontentloaded')
            for slot in (9, 10):
                await expect(page.locator(f'li[data-intro-slot="{slot}"] a')).to_contain_text(guides[f'S{slot:03}']['title'])
            await page.locator('li[data-intro-slot="10"] a').click()
            await expect(page.locator('#introTitle')).to_have_text(guides['S010']['title'])
            await expect(page.locator('#introChapters button')).to_have_count(len(guides['S010']['chapters']))
            await expect(page.locator('#introFilm source')).to_have_attribute('src', expected_lessons[10]['movie'])
            record('Gallery and S010 guide use the current recorded-study catalogue under the old controller.')

            await page.goto(site + 'offline-reader.html?slot=9', wait_until='domcontentloaded')
            await expect(page.locator('#reading .rwl-bridge')).to_contain_text(expected_lessons[9]['bridge'])
            keys = await page.evaluate('caches.keys()')
            assert old_cache in keys and new_cache not in keys, keys
            assert state['held_worker_requests'] > 0
            report['held_worker_requests'] = state['held_worker_requests']
            record('Current reader uses the new manifest before new-worker installation is permitted.')
            gate.set()
            await page.evaluate('navigator.serviceWorker.getRegistration().then(r=>r.update())')
            await page.wait_for_function('''async ([oldName,newName]) => {
              const keys = await caches.keys();
              const registration = await navigator.serviceWorker.getRegistration();
              return keys.includes(newName) && !keys.includes(oldName) && registration.active?.state === 'activated';
            }''', arg=[old_cache, new_cache], timeout=60000)
            # Stop the origin as well as emulating offline, so worker requests cannot escape the check.
            await runner.cleanup()
            await context.set_offline(True)
            await page.close()
            page = await context.new_page()
            page.on('pageerror', lambda e: errors.append(str(e)))
            await page.goto(site + 'offline-reader.html?slot=10', wait_until='domcontentloaded')
            await expect(page.locator('#reading .rwl-bridge')).to_contain_text(expected_lessons[10]['bridge'])
            # The reader intentionally offers session 1 and only the readings opened on this device.
            report['offline_slots'] = await page.locator('#readerLesson option').evaluate_all('(options) => options.map(option => option.value)')
            assert report['offline_slots'] == ['1', '9', '10'], report['offline_slots']
            report['offline_colours'] = await page.evaluate('''() => {
              const describe = node => { const s=getComputedStyle(node); return {background:s.backgroundColor,colour:s.color,colourScheme:s.colorScheme}; };
              return {canvas:describe(document.documentElement),body:describe(document.body),picker:describe(document.querySelector('#readerLesson'))};
            }''')
            assert report['offline_colours']['canvas']['background'] == 'rgb(246, 247, 244)'
            assert report['offline_colours']['canvas']['colourScheme'] == 'light'
            await page.screenshot(path=output / 'offline-reader-upgraded.png', full_page=True)
            record('After activation and origin shutdown, a fresh page reads new S010 offline and preserves the opened-reading list (1, 9, 10).')
            assert not errors, errors
            report['page_errors'] = errors
            report['passed'] = True
            report['current_requested_versions'] = sorted({request['path'] + '?' + request['query'] for request in requests
                if request['phase'] == 'current' and request['query'] and any(term in request['path'] for term in
                ['recorded-studies', 'read-watch-practise', 'teaching-72', 'introduction-media', 'introduction-library', 'offline-reader.js'])})
            print(json.dumps({'passed':True,'checks':report['checks'],'offline_colours':report['offline_colours']}, indent=2), flush=True)
            await context.close()
            await browser.close()
            browser = None
    except Exception as error:
        report['passed'] = False
        report['failure'] = str(error)
        raise
    finally:
        gate.set()
        (output / 'cache-upgrade.json').write_text(json.dumps(report, indent=2) + '\n')
        await runner.cleanup()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--previous-ref', default='2cc35f1')
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--chromium', type=Path)
    parser.add_argument('--browser-flags', type=Path, help='JSON flags, or the existing executable/JSON two-line runtime file')
    options = parser.parse_args()
    asyncio.run(asyncio.wait_for(verify(options), timeout=240))
