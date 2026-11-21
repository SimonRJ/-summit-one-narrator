"""Exercise a real install, a failed update and a cold offline start on a nested Pages path."""
import asyncio
import shutil
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.async_api import async_playwright, expect
from browser_lesson_fixed import MOCK

ROOT = Path(__file__).resolve().parents[1]
PREFIX = '/-summit-one-narrator/'
SIBLING = 'other-project-readings'


class PagesHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        if path.startswith(PREFIX):
            path = '/' + path[len(PREFIX):]
        return super().translate_path(path)

    def do_GET(self):
        if self.server.test_failed_update and self.path == PREFIX + 'sw.js':
            original = (ROOT / 'sw.js').read_text()
            candidate = original.replace('const staticFiles = [', "const staticFiles = [\n  './missing-reading-file.js',")
            candidate = candidate.replace('summit-one-github-20261121', 'summit-one-failed-update')
            content = candidate.encode()
            self.send_response(200)
            self.send_header('Content-Type', 'application/javascript')
            self.send_header('Content-Length', str(len(content)))
            self.end_headers()
            self.wfile.write(content)
            return
        super().do_GET()

    def log_message(self, format, *args):
        pass


async def main():
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(PagesHandler, directory=str(ROOT)))
    server.test_failed_update = False
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f'http://127.0.0.1:{server.server_port}{PREFIX}'
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(executable_path=shutil.which('google-chrome') or shutil.which('chromium'))
            context = await browser.new_context(viewport={'width': 390, 'height': 844})
            try:
                await context.add_init_script("""window.fixture={records:[],attempts:[],exams:[],writes:[],fail:false,
                    progress:{completed_sessions:5,current_session:6,xp:0,rank:0,state:{}}};""")
                await context.route('**/supabase-client.js*', lambda route: route.fulfill(
                    content_type='application/javascript', body=MOCK))
                page = await context.new_page()
                await page.goto(base + 'robots.txt')
                await page.evaluate("async name => {const cache=await caches.open(name); await cache.put('sibling.txt',new Response('keep this'));}", SIBLING)
                await page.goto(base, wait_until='domcontentloaded')
                await page.locator('#continue').click()
                await expect(page.locator('.rwl-example')).to_be_visible()
                await page.goto(base + 'offline-reader.html?slot=6')
                await expect(page.locator('#readerStatus')).to_contain_text('Ready to read offline', timeout=45000)
                await expect(page.locator('#readerLesson')).to_have_value('6')
                assert await page.locator('#readerLesson option').count() == 2
                await page.wait_for_function('Boolean(navigator.serviceWorker.controller)')
                cache_info = await page.evaluate("""async name => {
                    const keys=await caches.keys();
                    const own=keys.find(key=>key.startsWith(location.pathname.replace('offline-reader.html','')+':summit-one-'));
                    const files=await (await caches.open(own)).keys();
                    return { sibling:await (await (await caches.open(name)).match('sibling.txt')).text(),
                        files:files.map(request=>new URL(request.url).pathname) };
                }""", SIBLING)
                assert cache_info['sibling'] == 'keep this'
                assert all(path.startswith(PREFIX) and '/media/' not in path and '/supabase/' not in path
                           for path in cache_info['files'])
                assert PREFIX + 'figures/read-practice/S368.svg' in cache_info['files']

                server.test_failed_update = True
                state = await page.evaluate("""async () => {
                    const registration=await navigator.serviceWorker.getRegistration();
                    const finished=new Promise((resolve,reject)=>{
                        const timeout=setTimeout(()=>reject(Error('Update never finished')),30000);
                        registration.addEventListener('updatefound',()=>{
                            const installing=registration.installing;
                            installing.addEventListener('statechange',()=>{
                                if(['redundant','activated'].includes(installing.state)){
                                    clearTimeout(timeout);resolve(installing.state);
                                }
                            });
                        },{once:true});
                    });
                    await registration.update();
                    return finished;
                }""")
                assert state == 'redundant', state

                # Stop the origin itself so service-worker requests also lose network access.
                server.shutdown()
                server.server_close()
                await page.close()
                offline = await context.new_page()
                await offline.goto(base + 'tests.html?section=depth')
                await expect(offline.get_by_role('heading', name='Offline lesson reader')).to_be_visible()
                await expect(offline.locator('#readerLesson')).to_have_value('6')
                await offline.locator('.rwl-full-example > summary').click()
                await expect(offline.locator('.rwl-full-example ol')).to_be_visible()
                await expect(offline.locator('.rwl-opening-figure')).to_be_visible()
                assert await offline.locator('.rwl-opening-figure').evaluate('img => img.complete && img.naturalWidth>0')
                await offline.locator('.lesson-model > summary').click()
                await expect(offline.locator('.lm-drawing svg')).to_be_visible()
                assert not await offline.locator('video,.rwl-form').count()
                await offline.goto(base + 'offline-reader.html?slot=370')
                await expect(offline.locator('#readerLesson')).to_have_value('6')
                await offline.locator('#readerLesson').select_option('1')
                await expect(offline.locator('.rwl-example')).to_be_visible()
                assert await offline.evaluate('document.documentElement.scrollWidth <= innerWidth')
            finally:
                await context.close()
                await browser.close()
    finally:
        server.shutdown()
        server.server_close()
        thread.join()
    print('PASS: opened readings, scoped cache, failed upgrade, cold offline exam navigation, figure and diagram.')


if __name__ == '__main__':
    asyncio.run(main())
