"""Play the published maths films through the same gallery, chapter and transcript controls as a learner."""
import argparse
import asyncio
import json
from pathlib import Path

from playwright.async_api import async_playwright, expect

from browser_lesson_fixed import MOCK


ROOT = Path(__file__).resolve().parents[1]


async def check_course_players(browser, site, lesson, guide, release):
    """Use the course and the immutable notebook with the same published movie."""
    slot = int(lesson[1:])
    context = await browser.new_context(viewport={'width':390, 'height':844}, has_touch=True,
                                        is_mobile=True, service_workers='block')
    try:
        await context.route('**/supabase-client.js*',
                            lambda route: route.fulfill(content_type='application/javascript', body=MOCK))
        await context.route('https://raw.githubusercontent.com/**', lambda route: route.abort())
        await context.add_init_script("""
            const route = new URLSearchParams(location.search);
            const slot = Number(route.get('fixtureSlot'));
            const replay = route.get('view') === 'review';
            const completed = replay ? slot : slot - 1;
            window.fixture = {
                records: replay ? [{session_number:slot, immutable:true, completed_at:'2026-01-01T00:00:00Z',
                          answers:{}, evidence:{}, working:{}, summary:{}}] : [],
                attempts:[], exams:[], writes:[], fail:false,
                progress:{completed_sessions:completed, current_session:completed+1, xp:0, rank:0, state:{}}
            };
        """)
        page = await context.new_page()
        for replay in (False, True):
            path = f'?fixtureSlot={slot}' + ('&view=review' if replay else '')
            await page.goto(site + path, wait_until='domcontentloaded')
            if replay:
                await page.locator(f'[data-review-session="{slot}"] > summary').tap()
                before = await page.evaluate('JSON.stringify(window.fixture.records)')
                await page.locator(f'button[data-video-session="{slot}"]').tap()
                player = page.locator('#replayIntroVideo')
            else:
                await page.locator('#continue').tap()
                await expect(page.locator('.rwl-bridge')).to_contain_text(guide['bridge'])
                await page.locator('[data-screen-next]').tap()
                player = page.locator('#openingVideo')
            await expect(player).to_have_attribute('src', release + lesson + '.mp4')
            await expect(player).to_have_attribute('poster', release + lesson + '-poster.jpg')
            await player.evaluate('async video => { video.muted = true; await video.play(); }')
            await page.wait_for_function("""id => {
                const v = document.getElementById(id);
                return !v.error && v.videoWidth === 1920 && !v.paused && v.currentTime > .2;
            }""", arg=await player.get_attribute('id'), timeout=35000)
            await player.evaluate('video => video.pause()')
            if replay:
                assert await page.evaluate('JSON.stringify(window.fixture.records)') == before
                assert await page.evaluate('window.fixture.progress.completed_sessions') == slot
    finally:
        await context.close()


async def run(site, engine):
    catalogue = json.loads((ROOT / 'data/recorded-studies.json').read_text())
    async with async_playwright() as playwright:
        browser = await (playwright.webkit.launch() if engine == 'webkit'
                         else playwright.chromium.launch(channel='chrome'))
        try:
            context = await browser.new_context(viewport={'width': 390, 'height': 844},
                                                is_mobile=True, has_touch=True)
            page = await context.new_page()
            # These lesson records and complete chapters belong to this edition even
            # if the separately maintained older catalogue is unavailable.
            await page.route('https://raw.githubusercontent.com/**', lambda route: route.abort())
            await page.goto(site + 'lesson-introduction-videos.html', wait_until='domcontentloaded')
            for lesson, guide in catalogue['lessons'].items():
                slot = int(lesson[1:])
                await expect(page.locator(f'li[data-intro-slot="{slot}"] a')).to_contain_text(guide['title'])

            for index, (lesson, guide) in enumerate(catalogue['lessons'].items()):
                slot = int(lesson[1:])
                await page.goto(site + f'watch-lesson-intro.html?slot={slot}', wait_until='domcontentloaded')
                await expect(page.locator('#introTitle')).to_have_text(guide['title'])
                await expect(page.locator('#introTranscript p')).to_have_text(guide['transcript'])
                buttons = page.locator('#introChapters button')
                await expect(buttons).to_have_count(len(guide['chapters']))
                film = page.locator('#introFilm')
                release = guide.get('release') or catalogue['release']
                await expect(film.locator('source')).to_have_attribute('src', release + lesson + '.mp4')
                await expect(film).to_have_attribute('poster', release + lesson + '-poster.jpg')
                await film.evaluate('v => { v.muted = true; }')
                await page.wait_for_function("""() => {
                    const v = document.getElementById('introFilm');
                    return v.videoWidth === 1920 && v.videoHeight === 1080 && v.readyState >= 1;
                }""", timeout=50000)
                duration = await film.evaluate('v => v.duration')
                assert abs(duration - guide['seconds']) < 0.15, (lesson, duration, guide['seconds'])
                chapter = max(1, (len(guide['chapters']) - 1) // 2)
                await buttons.nth(chapter).tap()
                await page.wait_for_function("""t => {
                    const v = document.getElementById('introFilm');
                    return !v.error && !v.paused && !v.seeking && v.currentTime > t + 0.2 && v.currentTime < t + 9;
                }""", arg=guide['chapters'][chapter]['start'], timeout=30000)
                await film.evaluate('v => v.pause()')
                width = await page.evaluate('document.documentElement.scrollWidth - innerWidth')
                assert width <= 1, (lesson, width)
                await check_course_players(browser, site, lesson, guide, release)
                print(lesson, engine, 'played and sought to', guide['chapters'][chapter]['title'], flush=True)
                await page.set_viewport_size({'width': 844, 'height': 390} if index % 2 == 0
                                             else {'width': 390, 'height': 844})
        finally:
            await browser.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--site', default='http://127.0.0.1:8765/')
    parser.add_argument('--engine', choices=['chromium', 'webkit'], required=True)
    args = parser.parse_args()
    asyncio.run(run(args.site.rstrip('/') + '/', args.engine))
