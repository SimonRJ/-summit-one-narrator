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


async def check_domino_pages(page):
    # The published lesson page must expose the board independently of film availability.
    await page.goto(BASE + '/watch-lesson-intro.html?slot=36#lessonModel', wait_until='domcontentloaded')
    model = page.locator('#lessonModel .domino-model')
    await model.locator(':scope > summary').tap()
    board = model.locator('.dm-board')
    cell = lambda index: board.locator(f'[data-cell="{index}"]')
    status = model.get_by_role('status')
    await expect(board.get_by_role('button')).to_have_count(6)
    for width in (320, 390):
        await page.set_viewport_size({'width': width, 'height': 780})
        assert await board.evaluate("""el => {
            const max = document.documentElement.clientWidth;
            return document.documentElement.scrollWidth <= max + 1 &&
                [...el.querySelectorAll('button')].every(button => {
                    const r = button.getBoundingClientRect();
                    return r.width >= 44 && r.height >= 44 && r.left >= 0 && r.right <= max + 1;
                });
        }"""), width
    # A diagonal tap is rejected. The original corner stays selected for the next valid tap.
    await cell(0).tap()
    await cell(4).tap()
    await expect(status).to_contain_text('do not share an edge')
    await expect(cell(0)).to_have_attribute('aria-pressed', 'true')
    await cell(1).tap()
    await expect(cell(0)).to_have_attribute('data-mate', 'right')
    await expect(cell(1)).to_have_attribute('data-mate', 'left')
    assert await cell(0).evaluate("el => getComputedStyle(el, '::after').width") == '3px'
    await model.get_by_role('button', name='Undo last domino').tap()
    await expect(board.locator('[data-mate]')).to_have_count(0)
    for top, bottom in ((0, 3), (1, 4), (2, 5)):
        await cell(top).tap()
        await cell(bottom).tap()
        await expect(cell(top)).to_have_attribute('data-mate', 'below')
        await expect(cell(bottom)).to_have_attribute('data-mate', 'above')
    await expect(status).to_contain_text('cover every square')
    await model.get_by_role('button', name='Start over').tap()
    await expect(board.locator('[data-mate]')).to_have_count(0)
    await expect(model.get_by_role('button', name='Undo last domino')).to_be_disabled()

    await page.goto(BASE + '/watch-lesson-intro.html?slot=333#lessonModel', wait_until='domcontentloaded')
    await model.locator(':scope > summary').tap()
    await expect(board.get_by_role('button')).to_have_count(8)
    await expect(model.locator('select')).to_have_value('2')
    await model.get_by_label('Show checkerboard colours').tap()
    await expect(model.locator('.dm-count')).to_contain_text('4 dark (●) and 4 light (○)')
    await model.get_by_role('button', name='No', exact=True).tap()
    await expect(status).to_contain_text('only with A2')


async def check_route_page(page):
    await page.goto(BASE + '/watch-lesson-intro.html?slot=318#lessonModel', wait_until='domcontentloaded')
    model = page.locator('#lessonModel .route-model')
    await model.locator(':scope > summary').tap()
    rule = model.get_by_role('combobox')
    right = model.locator('[data-move="R"]')
    up = model.locator('[data-move="U"]')
    status = model.get_by_role('status')
    await expect(rule).to_have_value('point')
    await right.tap()
    await up.tap()
    await expect(status).to_contain_text('B2 is closed')
    await expect(model.locator('svg')).to_have_attribute('aria-label', 'Route grid from A1 to D3. Close the junction B2. Current junction B1. Moves R.')

    await rule.select_option('edge')
    await up.tap()
    await right.tap()
    await expect(status).to_contain_text('street from A2 to B2 is closed')
    await model.get_by_role('button', name='Undo step').tap()
    await right.tap()
    await up.tap()
    await expect(status).to_contain_text('At B2')
    await model.locator('.rm-proof > summary').tap()
    await expect(model.locator('.rm-total')).to_have_text('7 routes from A1 to D3.')

    await rule.select_option('checkpoint')
    for step in (right, up, right, right, up):
        await step.tap()
    await expect(status).to_contain_text('A new route')
    await model.locator('.rm-saved > summary').tap()
    await expect(model.locator('.rm-saved li')).to_have_text('RURRU')
    await model.get_by_role('button', name='New route').tap()
    for step in (right, up, right, right, up):
        await step.tap()
    await expect(status).to_contain_text('already found')
    await expect(model.locator('.rm-saved li')).to_have_count(1)
    for width in (320, 390):
        await page.set_viewport_size({'width': width, 'height': 780})
        assert await model.evaluate("""el => document.documentElement.scrollWidth <= innerWidth + 1 &&
            [...el.querySelectorAll('button,select')].every(node => {
                const box=node.getBoundingClientRect();
                return box.width >= 44 && box.height >= 44 && box.left >= 0 && box.right <= innerWidth + 1;
            })"""), width


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
            await check_domino_pages(page)
            await check_route_page(page)
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
        print('PASS: iPhone WebKit cube taps, domino tilings, route counting, rotation, worked steps and draft recovery.')


if __name__ == '__main__':
    asyncio.run(main())
