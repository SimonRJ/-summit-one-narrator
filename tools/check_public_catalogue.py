"""Verify catalogue availability, direct links and recovery at touch and desktop widths."""
import argparse
import asyncio
import json
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from urllib.parse import urlparse

from playwright.async_api import async_playwright, expect


ROOT = Path(__file__).resolve().parents[1]
CATALOGUE = json.loads((ROOT / 'data/recorded-studies.json').read_text())
GUIDES = CATALOGUE['lessons']
ALTERNATE = 'https://github.com/SimonRJ/-summit-one-narrator/releases/download/test-edition/'


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


async def exercise(page, base):
    mode = 'healthy'
    loads = []
    gallery = page.locator('#introGallery')
    film = page.locator('#introFilm')
    status = page.locator('#introStatus')
    retry = page.get_by_role('button', name='Reload lesson')
    async def fixture(route):
        req = route.request
        url = urlparse(req.url)
        if url.path.endswith('/data/recorded-studies.json') and mode == 'separate-release':
            guides = {**GUIDES, 'S137': {**GUIDES['S137'], 'release': ALTERNATE}}
            return await route.fulfill(json={**CATALOGUE, 'lessons': guides})
        if url.hostname == 'raw.githubusercontent.com':
            if mode == 'offline' or not url.path.endswith('/lesson-intros-live.json'):
                return await route.abort()
            return await route.fulfill(json={'version':1, 'entries':[
                {'id':'S101','title':'Under review','seconds':80,'status':'checking'},
                {'id':'S102','title':'Verified example','seconds':125,'status':'verified'}
            ]})
        if req.resource_type == 'media':
            loads.append(url.path)
            return await route.abort()
        if url.hostname != '127.0.0.1':
            return await route.abort()
        await route.continue_()

    async def visit(path):
        await page.goto(base+path, wait_until='domcontentloaded')
    async def fits():
        assert await page.evaluate('document.documentElement.scrollWidth <= window.innerWidth + 1')
        for rect in await page.locator('main a:visible, main button:visible, summary:visible').evaluate_all(
                'elements => elements.map(e=>[e.getBoundingClientRect().left,e.getBoundingClientRect().right])'):
            assert -1 <= rect[0] and rect[1] <= page.viewport_size['width']+1, rect
    await page.route('**/*',fixture)
    await visit('lesson-introduction-videos.html')
    await expect(gallery.locator('li[data-intro-slot="102"]')).to_contain_text('Verified example')
    await expect(gallery.locator('li[data-intro-slot="101"]')).to_have_count(0)
    await expect(page.locator('#introProgress')).to_have_text(f'{len(GUIDES)+7} of 283 lesson introductions available')
    await fits()
    await visit('watch-lesson-intro.html?slot=101')
    await expect(status).to_contain_text('No lesson introduction is published')
    await expect(film).to_be_hidden()
    await expect(retry).to_be_hidden()
    assert not any('S101' in url for url in loads)
    await visit('watch-lesson-intro.html?slot=102')
    await expect(page.locator('#introTitle')).to_have_text('Verified example')
    await expect(page.locator('#introGuideStatus')).to_be_visible()
    await expect(retry).to_be_visible()
    mode='offline'
    await visit('lesson-introduction-videos.html')
    await expect(page.locator('#introProgress')).to_contain_text('The full catalogue could not be loaded.')
    await expect(gallery.locator('li')).to_have_count(len(GUIDES)+6)
    await visit('watch-lesson-intro.html?slot=102')
    await expect(status).to_contain_text('Reconnect')
    await expect(film).to_be_hidden()
    await expect(retry).to_be_visible()
    await fits()
    mode='healthy'
    await retry.click()
    await expect(page.locator('#introTitle')).to_have_text('Verified example')
    mode = 'separate-release'
    for slot, release in [(137, ALTERNATE), (138, GUIDES['S138'].get('release') or CATALOGUE['release'])]:
        await visit(f'watch-lesson-intro.html?slot={slot}')
        await expect(film.locator('source')).to_have_attribute('src', f'{release}S{slot}.mp4')
        await expect(film).to_have_attribute('poster', f'{release}S{slot}-poster.jpg')
    await visit('watch-lesson-intro.html?slot=0')
    await expect(status).to_contain_text('Choose a lesson')
    for slot in range(1,7):
        # Allow the module to replace this entry before the initial DOM has loaded.
        await page.goto(base+f'watch-lesson-intro.html?slot={slot:03}', wait_until='commit')
        await expect(page).to_have_url(base+f'watch-intro-s{slot:03}.html')
        await expect(page.locator('button[data-time]')).to_have_count(7)
        await expect(page.locator('video[controls][playsinline]')).to_be_visible()
        await page.locator('.transcript summary').click()
        await expect(page.locator('.transcript p').first).to_be_visible()
        await fits()

async def main(engine):
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=ROOT))
    Thread(target=server.serve_forever,daemon=True).start()
    try:
        async with async_playwright() as playwright:
            browser=await (playwright.chromium.launch(channel='chrome') if engine=='chromium' else playwright.webkit.launch())
            try:
                for width,height in ((320,720),(390,844),(1024,768)):
                    page=await browser.new_page(viewport={'width':width,'height':height},has_touch=True)
                    await exercise(page,f'http://127.0.0.1:{server.server_port}/')
                    await page.close()
                    print(engine,width,'catalogue and player recovery passed',flush=True)
            finally:
                await browser.close()
    finally:
        server.shutdown()
        server.server_close()

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--engine',choices=['chromium','webkit'],required=True)
    asyncio.run(main(parser.parse_args().engine))
