"""Check the shared figure viewer through a lesson, offline reader and resumed exam."""
import argparse
import asyncio
import json
import shutil
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.async_api import async_playwright, expect
from browser_lesson_fixed import MOCK

ROOT = Path(__file__).resolve().parents[1]


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass


async def check_viewer(page, label, source, touch):
    opener = page.get_by_role('button', name=label, exact=True).first
    await (opener.tap() if touch else opener.click())
    viewer = page.get_by_role('dialog')
    await expect(viewer.get_by_role('button', name='Close')).to_be_focused()
    await expect(viewer.locator(source)).to_be_visible()
    fit = viewer.get_by_role('button', name='Fit')
    await fit.click()
    port = viewer.locator('.fv-window')
    assert await port.evaluate('el => el.scrollWidth <= el.clientWidth + 1')
    initial = await viewer.locator(source).evaluate('el => el.getBoundingClientRect().width')
    zoom = viewer.get_by_role('button', name='3×')
    await (zoom.tap() if touch else zoom.click())
    await expect(viewer.get_by_role('button', name='3×')).to_have_attribute('aria-pressed', 'true')
    width = await viewer.locator(source).evaluate('el => el.getBoundingClientRect().width')
    assert abs(width - initial * 3) < 2, (initial, width)
    assert await port.evaluate('el => {el.scrollLeft = el.scrollWidth; return el.scrollLeft > 0;}')
    assert await page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1')
    if touch:
        await viewer.get_by_role('button', name='Close').tap()
    else:
        await page.keyboard.press('Escape')
    await expect(viewer).to_have_count(0)
    await expect(opener).to_be_focused()


async def check_lessons(browser, base, device):
    context = await browser.new_context(**{**device, 'viewport': {'width': 320, 'height': 620}}, service_workers='block')
    try:
        await context.route('https://**/*', lambda route: route.abort())
        await context.route('**/supabase-client.js*', lambda route: route.fulfill(content_type='application/javascript', body=MOCK))
        await context.add_init_script("""window.fixture={records:[],attempts:[],exams:[],writes:[],fail:false,
          progress:{completed_sessions:5,current_session:6,xp:0,rank:0,state:{}}};""")
        page = await context.new_page()
        await page.goto(base)
        await page.locator('#continue').click()
        image = page.locator('img.rwl-opening-figure')
        alt = await image.get_attribute('alt')
        assert alt
        await check_viewer(page, 'Enlarge diagram', 'img', bool(device))
        await expect(image).to_have_attribute('alt', alt)
        assert await page.evaluate('fixture.attempts.length === 0')
        # Check an actual retained practice diagram whose description is the adjacent caption.
        authored = next(item for item in json.loads((ROOT / 'tools/content/reviewed/geo.json').read_text())
                        if item['id'] == 'O043T')
        await page.evaluate("""async item => {
            const {originalFigure} = await import('./original-learning.js');
            const {enableFigureViewing} = await import('./figure-viewer.js?v=deeper-20261121');
            const {items} = await (await fetch('./data/lesson-challenges.json')).json();
            const host = document.querySelector('#stage');
            host.innerHTML = originalFigure({...item, learning:items.find(entry=>entry.id===item.id)});
            enableFigureViewing(host);
        }""", authored)
        caption = await page.locator('.original-figure figcaption').inner_text()
        await page.get_by_role('button', name='Enlarge diagram').click()
        authored_view = page.get_by_role('dialog')
        await expect(authored_view).to_have_accessible_description(caption)
        await expect(authored_view.locator('.fv-caption')).to_have_text(caption)
        assert await authored_view.locator('.fv-window').evaluate(
            "el => getComputedStyle(el).backgroundColor === 'rgb(16, 35, 50)'")
        await authored_view.get_by_role('button', name='Close').click()
        await expect(page.locator('.original-figure figcaption')).to_have_text(caption)
        await page.goto(base + 'offline-reader.html?slot=6')
        await expect(page.locator('#readerLesson')).to_have_value('6')
        await check_viewer(page, 'Enlarge diagram', 'img', bool(device))
        await expect(page.locator('img.rwl-opening-figure')).to_have_attribute('alt', alt)
    finally:
        await context.close()


async def check_exam(browser, base, device):
    context = await browser.new_context(**{**device, 'viewport': {'width': 390, 'height': 744}}, service_workers='block')
    exam = {'id': 'figure-paper', 'title': 'Figure practice', 'active': True, 'year': 2026, 'max_score': 65,
            'metadata': {'amc_part': 'depth'}, 'question_count': 2, 'time_limit_minutes': 40}
    question = {'exam_id': exam['id'], 'question_type': 'integer', 'stem': 'Read the figure.', 'marks': 6, 'metadata': {}}
    questions = [
        dict(question, question_number=26, figure_svg='<svg viewBox="0 0 300 160" aria-labelledby="plot-title" role="img"><title id="plot-title">A marked rectangle</title><defs><pattern id="plot-fill" patternUnits="userSpaceOnUse" width="10" height="10"><path d="M0 0L10 10" stroke="black"/></pattern></defs><rect width="300" height="160" fill="url(#plot-fill)"/></svg>'),
        dict(question, question_number=27, image_ref='<img src="figures/read-practice/S141.svg" alt="Original question scan">')
    ]
    db = {'exam_catalog': [exam], 'exam_questions_student': questions, 'exam_sittings': [
        {'id': 'figure-sitting', 'user_id': 'fixture-learner', 'exam_id': exam['id'], 'completed': False,
         'started_at': '2026-01-01T00:00:00Z', 'expires_at': '2099-01-02T00:00:00Z', 'responses': {}}]}
    try:
        await context.add_init_script('window.__fixture=' + json.dumps(db))
        await context.route('https://**/*', lambda route: route.abort())
        await context.route('**/supabase-client.js*', lambda route: route.fulfill(
            content_type='application/javascript', body=(ROOT / 'tools/browser_fixture.js').read_text()))
        page = await context.new_page()
        await page.goto(base + 'tests.html?section=depth')
        await page.locator('#firstQuestion').click()
        await page.locator('#integerInput').fill('7')
        await check_viewer(page, 'Enlarge diagram', 'svg', bool(device))
        await expect(page.locator('#integerInput')).to_have_value('7')
        await expect(page.locator('#plot-fill')).to_have_count(1)
        await page.get_by_role('button', name='Enlarge diagram').click()
        await expect(page.get_by_role('dialog').locator('svg')).to_have_attribute('aria-labelledby', 'plot-title')
        await expect(page.locator('#plot-title')).to_have_count(1)
        # Simulate the change of question that can also happen on expiry with a modal open.
        await page.locator('#next').evaluate('el => el.click()')
        await expect(page.get_by_role('dialog')).to_have_count(0)
        await check_viewer(page, 'Enlarge original question', 'img', bool(device))
        assert await page.evaluate('Object.keys(__fixture.exam_sittings[0].responses).length === 0')
    finally:
        await context.close()


async def main(webkit):
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=str(ROOT)))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f'http://127.0.0.1:{server.server_port}/'
    try:
        async with async_playwright() as p:
            device = p.devices['iPhone 13'] if webkit else {}
            browser = await p.webkit.launch() if webkit else await p.chromium.launch(
                executable_path=shutil.which('google-chrome') or shutil.which('chromium'))
            try:
                await check_lessons(browser, base, device)
                await check_exam(browser, base, device)
            finally:
                await browser.close()
    finally:
        server.shutdown()
        server.server_close()
        thread.join()
    print('PASS: figure fit, zoom, pan, keyboard close, focus return, lesson, reader, exam SVG and scan.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--webkit', action='store_true', help='Run with iPhone touch input in WebKit')
    asyncio.run(main(parser.parse_args().webkit))
