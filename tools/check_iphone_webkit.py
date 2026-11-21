"""Exercise the shipped lesson pages with WebKit, touch input and a synthetic learner."""
import asyncio
from pathlib import Path

from playwright.async_api import async_playwright, expect

from browser_lesson_fixed import MOCK


BASE = 'http://127.0.0.1:8765'
FAILURES = Path('qa-screenshots/iphone-webkit')


async def check_model_layout(model):
    await expect(model.locator('.lm-drawing svg')).to_be_visible()
    await expect(model.locator('.lm-controls input[type=range]')).to_have_count(2)
    bounds = await model.evaluate("""el => {
        const max = document.documentElement.clientWidth;
        const elements = [...el.querySelectorAll(':scope > summary, .lm-controls label, .lm-controls input, .lm-controls select, .lm-drawing svg, .lm-result')];
        return {
            overflow: document.documentElement.scrollWidth - max,
            clipped: elements.filter(node => {
                const box = node.getBoundingClientRect();
                return box.width <= 0 || box.height <= 0 || box.left < -1 || box.right > max + 1;
            }).map(node => node.tagName)
        };
    }""")
    assert bounds['overflow'] <= 1 and not bounds['clipped'], bounds


async def check_cube_page(page, devices):
    await page.goto(BASE + '/watch-intro-s006.html#lessonModel', wait_until='domcontentloaded')
    model = page.locator('#lessonModel .lesson-model')
    await model.locator(':scope > summary').tap()
    slider = model.get_by_role('slider', name='Back-left stack height', exact=False)
    await expect(slider).to_be_visible()
    await check_model_layout(model)

    challenge = model.locator('.lm-claims')
    await challenge.locator(':scope > summary').tap()
    save = challenge.get_by_role('button', name='Use this example')
    for height, left in ((2, 3), (3, 3), (4, 4)):
        box = await slider.bounding_box()
        assert box
        # Tap the interior tick on the native range track, as the learner would.
        await slider.tap(position={'x': box['width'] * (height - 1) / 4, 'y': box['height'] / 2})
        await expect(slider).to_have_value(str(height))
        await expect(model.locator('.lm-result')).to_contain_text(
            f'front outline shows {left} cubes (left) and 4 (right)')
        # Four plan cells come first. The two columns of unit squares form the front view.
        heights = await model.locator('.lm-drawing svg rect').evaluate_all("""rects => {
            const counts = new Map();
            for (const rect of rects.slice(4)) {
                const x = Number(rect.getAttribute('x'));
                counts.set(x, (counts.get(x) || 0) + 1);
            }
            return [...counts].sort((a, b) => a[0] - b[0]).map(entry => entry[1]);
        }""")
        assert heights == [left, 4], (height, heights)
        if height in (2, 4):
            await save.tap()
    await expect(challenge.locator('.lm-cases li')).to_have_count(2)
    await challenge.get_by_role('button', name='Sometimes', exact=True).tap()
    await expect(challenge.get_by_role('status')).to_contain_text('At heights 4 and 5')

    await page.set_viewport_size(devices['iPhone 13 landscape']['viewport'])
    await expect(slider).to_have_value('4')
    await check_model_layout(model)
    await page.set_viewport_size(devices['iPhone 13']['viewport'])


async def check_lesson_resume(page):
    await page.goto(BASE + '/', wait_until='domcontentloaded')
    await page.locator('#continue').tap()
    first = page.locator('.rwl-first-step')
    full = page.locator('.rwl-full-example')
    await expect(full.locator('ol')).to_be_hidden()
    await first.locator('summary').tap()
    await expect(first.locator('p')).to_be_visible()
    await full.locator('summary').tap()
    await expect(full.locator('ol')).to_be_visible()
    await expect(first.locator('p')).to_be_hidden()
    await page.get_by_role('button', name='Watch video', exact=True).tap()
    await expect(page.locator('#openingVideo')).to_be_visible()
    await page.get_by_role('button', name='Start practice', exact=True).tap()
    field = page.locator('.rwl-form input')
    await field.fill('17')
    await expect(page.locator('.rwl-solution')).to_be_hidden()
    await page.reload(wait_until='domcontentloaded')
    await page.locator('#continue').tap()
    await expect(field).to_have_value('17')
    await expect(field).to_be_enabled()
    await expect(page.locator('.rwl-solution')).to_be_hidden()
    assert await page.evaluate('fixture.progress.completed_sessions === 0 && fixture.attempts.length === 0')


async def main():
    async with async_playwright() as playwright:
        browser = await playwright.webkit.launch()
        context = await browser.new_context(**playwright.devices['iPhone 13'], service_workers='block')
        # All assets and the learner fixture come from localhost.
        await context.route('https://**/*', lambda route: route.abort())
        await context.route('**/supabase-client.js*', lambda route: route.fulfill(
            content_type='application/javascript', body=MOCK))
        await context.tracing.start(screenshots=True, snapshots=True, sources=True)
        page = await context.new_page()
        page.on('dialog', lambda dialog: dialog.accept())
        try:
            await check_cube_page(page, playwright.devices)
            await check_lesson_resume(page)
        except Exception:
            FAILURES.mkdir(parents=True, exist_ok=True)
            try:
                await context.tracing.stop(path=FAILURES / 'trace.zip')
            finally:
                await page.screenshot(path=FAILURES / 'screen.png', timeout=5000)
            raise
        else:
            await context.tracing.stop()
        finally:
            await context.close()
            await browser.close()
        print('PASS: iPhone WebKit cube taps, silhouette, rotation, worked steps and draft recovery.')


if __name__ == '__main__':
    asyncio.run(main())
