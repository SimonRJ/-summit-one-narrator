"""Verify a reviewed film on its public, active and completed learner routes."""
import argparse
import asyncio
import hashlib
import json
import re
from pathlib import Path
from urllib.request import urlopen
from urllib.parse import urljoin

from playwright.async_api import async_playwright, expect

from browser_lesson_fixed import MOCK

ROOT = Path(__file__).resolve().parents[1]
PROFILES = {
    'iphone-portrait': ('iPhone 13', False),
    'iphone-landscape': ('iPhone 13', True),
    'ipad-portrait': ('iPad (gen 7)', False),
    'ipad-landscape': ('iPad (gen 7)', True),
    'pc': ('Desktop Chrome', False),
}


async def fits(page):
    dims = await page.evaluate("""() => {
      const el = document.querySelector('.lesson-screen-stage');
      const footer = document.querySelector('.lesson-screen-footer');
      const r = footer?.getBoundingClientRect();
      return {overflow: document.documentElement.scrollWidth - innerWidth,
        stageOverflow: el ? el.scrollWidth - el.clientWidth : 0,
        footerBottom: r ? r.bottom : 0, footerTop: r ? r.top : 0, height: innerHeight};
    }""")
    assert dims['overflow'] <= 2 and dims['stageOverflow'] <= 2, dims
    assert dims['footerTop'] >= -2 and dims['footerBottom'] <= dims['height'] + 2, dims


async def verify_media(page, player, movie, seconds):
    await player.wait_for()
    await page.wait_for_function("""([id, url]) => {
      const v = document.getElementById(id);
      return v?.currentSrc === url && !v.error && v.readyState >= 1;
    }""", arg=[await player.get_attribute('id'), movie], timeout=60000)
    actual = await player.evaluate('v => [v.videoWidth, v.videoHeight, v.duration, v.controls]')
    assert actual[:2] == [1920, 1080] and abs(actual[2] - seconds) < .15 and actual[3], actual


async def verify_progress(page, player, start):
    await page.wait_for_function("""([id, t]) => {
      const v = document.getElementById(id);
      return !v.error && !v.paused && !v.seeking && v.readyState >= 2
        && v.currentTime > t + .65 && v.currentTime < t + 5;
    }""", arg=[await player.get_attribute('id'), start], timeout=30000)


async def play_inline(page, player):
    await player.evaluate('async v => { v.muted = true; await v.play(); }')
    await verify_progress(page, player, 0)
    await player.evaluate('v => v.pause()')


async def verify(site, lesson, profile, digest, output):
    slot = int(lesson[1:])
    catalog = json.loads((ROOT / 'data/recorded-studies.json').read_text())
    guide = catalog['lessons'][lesson]
    base = guide.get('release') or catalog['release']
    movie = urljoin(site, base + lesson + '.mp4')
    poster = urljoin(site, base + lesson + '-poster.jpg')
    digest = digest or guide.get('sha256')
    assert digest and re.fullmatch('[0-9a-f]{64}', digest), 'Supply the exact SHA-256 of the reviewed master'
    with urlopen(movie, timeout=90) as response:
        delivered = hashlib.file_digest(response, 'sha256').hexdigest()
    assert delivered == digest, (delivered, digest)
    output.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as pw:
        name, landscape = PROFILES[profile]
        device = dict(pw.devices[name])
        engine = device.pop('default_browser_type')
        if profile == 'pc':
            device['viewport'] = {'width': 1440, 'height': 900}
            device['screen'] = dict(device['viewport'])
        if landscape:
            for key in ('viewport', 'screen'):
                if key in device:
                    rect = device[key]
                    device[key] = {'width': rect['height'], 'height': rect['width']}
        browser = await (pw.webkit.launch() if engine == 'webkit' else pw.chromium.launch(channel='chrome'))
        context = await browser.new_context(**device, service_workers='block')
        # Use the existing in-memory course backend. Test both outcomes using dummy responses.
        fixture = MOCK.replace("correct:true,independent_credit:", "correct:body.answer_text!=='fixture-miss',independent_credit:")
        assert fixture != MOCK
        await context.route('**/supabase-client.js*', lambda r: r.fulfill(body=fixture, content_type='application/javascript'))
        await context.route('https://*.supabase.co/**', lambda r: r.abort())
        await context.add_init_script("""
          const args = new URLSearchParams(location.search);
          const slot = Number(args.get('fixtureSlot') || 1);
          const replay = args.get('view') === 'review';
          const done = replay ? slot : slot-1;
          window.fixture = {
            records: replay ? [{session_number:slot, immutable:true, completed_at:'2026-01-01T00:00:00Z',
              answers:{}, evidence:{}, working:{}, summary:{}}] : [], attempts:[], exams:[], writes:[], fail:false,
            progress:{completed_sessions:done, current_session:done+1, xp:0, rank:0, state:{}}
          };
        """)
        page = await context.new_page()
        try:
            await page.goto(site + 'lesson-introduction-videos.html', wait_until='domcontentloaded')
            row = page.locator(f'li[data-intro-slot="{slot}"] a')
            await expect(row).to_contain_text(guide['title'], timeout=20000)
            await row.click()
            await expect(page.locator('#introTitle')).to_have_text(guide['title'], timeout=20000)
            await expect(page.locator('#introTranscript p')).to_have_text(guide['transcript'])
            player = page.locator('#introFilm')
            assert await player.evaluate('v=>v.poster') == poster
            await verify_media(page, player, movie, guide['seconds'])
            chapters = page.locator('#introChapters button')
            await expect(chapters).to_have_count(len(guide['chapters']))
            await fits(page)
            for i, chapter in enumerate(guide['chapters']):
                button = chapters.nth(i)
                await expect(button).to_contain_text(chapter['title'])
                await button.click()
                await verify_progress(page, player, chapter['start'])
            full = profile == 'iphone-portrait'
            if full:
                await chapters.first.click()
                await verify_progress(page, player, 0)
                assert await player.evaluate('v => !v.muted && v.volume > 0 && v.playbackRate === 1')
                await page.wait_for_function("document.getElementById('introFilm').ended",
                                             timeout=(guide['seconds'] + 40) * 1000)
            await page.goto(site + f'?fixtureSlot={slot}', wait_until='domcontentloaded')
            await page.locator('#continue').click()
            await expect(page.locator('.rwl-bridge')).to_contain_text(guide['bridge'], timeout=20000)
            await fits(page)
            await page.screenshot(path=output / 'read.png')
            forward = page.locator('[data-screen-next]')
            await forward.click()
            player = page.locator('#openingVideo')
            await verify_media(page, player, movie, guide['seconds'])
            assert await player.evaluate('v=>v.poster') == poster
            await play_inline(page, player)
            await fits(page)
            await page.screenshot(path=output / 'watch.png')
            await forward.click()
            for answer, correct in [('fixture-answer', True), ('fixture-miss', False)]:
                form = page.locator('.rwl-form')
                await form.wait_for()
                await expect(page.locator('.rwl-solution')).to_be_hidden()
                await expect(forward).to_be_disabled()
                await form.locator('input').fill(answer)
                await form.locator('button').click()
                await expect(forward).to_be_enabled()
                await expect(form.locator('input')).to_be_disabled()
                saved = await page.evaluate("Object.values(fixture.records[0].answers).at(-1).correct")
                assert saved == correct, (answer, saved)
                if not correct:
                    await page.locator('.rwl-rethink summary').click()
                    await expect(page.locator('.rwl-rethink p')).to_be_visible()
                await fits(page)
                if correct:
                    await forward.click()
            await page.screenshot(path=output / 'practice.png')
            await page.goto(site + f'?fixtureSlot={slot}&view=review', wait_until='domcontentloaded')
            row = page.locator(f'[data-review-session="{slot}"]')
            await row.locator(':scope > summary').click()
            before = await page.evaluate('JSON.stringify([fixture.records, fixture.progress, fixture.writes])')
            await row.locator(f'button[data-video-session="{slot}"]').click()
            player = page.locator('#replayIntroVideo')
            await verify_media(page, player, movie, guide['seconds'])
            assert await player.evaluate('v=>v.poster') == poster
            await play_inline(page, player)
            assert await page.evaluate('JSON.stringify([fixture.records, fixture.progress, fixture.writes])') == before
            await page.screenshot(path=output / 'replay.png')
            result = {'profile':profile, 'engine':engine, 'viewport':device['viewport'], 'site':site,
                      'sha256':digest, 'film':movie, 'duration':guide['seconds'], 'chapters':len(guide['chapters']),
                      'normal_speed_unmuted_to_ended':full, 'practice_grading':'isolated fixture',
                      'immutable_replay':True}
            (output / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
            print(json.dumps(result), flush=True)
        except Exception:
            print('Stopped at', page.url, await page.locator('video').evaluate_all(
                'videos => videos.map(v => ({src: v.currentSrc, time: v.currentTime, ready: v.readyState, error: v.error?.code}))'
            ), flush=True)
            await page.screenshot(path=output / 'failure.png', timeout=5000)
            raise
        finally:
            await browser.close()


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--lesson', required=True)
    p.add_argument('--site', required=True)
    p.add_argument('--profile', required=True, choices=PROFILES)
    p.add_argument('--sha256')
    p.add_argument('--output', required=True, type=Path)
    args = p.parse_args()
    asyncio.run(verify(args.site.rstrip('/') + '/', args.lesson, args.profile, args.sha256, args.output))
