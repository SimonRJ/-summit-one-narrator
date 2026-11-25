"""Check the actual local font faces and optional service-worker offline delivery."""
import argparse
import asyncio
import json
from pathlib import Path

from playwright.async_api import async_playwright


FONT_CHECK = """async () => {
  const specifications = [
    ...[400,500,600,700].map(w => `${w} 18px \"Source Sans 3\"`),
    ...[400,500,600].map(w => `italic ${w} 18px \"Source Sans 3\"`),
    ...[400,500,600].map(w => `${w} 18px \"Source Serif 4\"`),
    ...[500,600].map(w => `${w} 18px \"Source Code Pro\"`),
    '400 18px \"STIX Two Math\"'
  ];
  const rows = [];
  for (const specification of specifications) {
    const text = specification.includes('STIX') ? '∑ ∫ ∞ ≤ ≥ ½ → 123' : 'Summit One 123';
    const faces = await document.fonts.load(specification, text);
    rows.push({specification, loaded: faces.length > 0 && faces.every(f => f.status === 'loaded')});
  }
  await document.fonts.ready;
  return {faces:rows, overflow:document.documentElement.scrollWidth-innerWidth,
    body_family:getComputedStyle(document.body).fontFamily};
}"""


async def verify(site, profile, output, offline=False):
    output.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as playwright:
        device = dict(playwright.devices['iPhone 13' if profile == 'iphone' else 'Desktop Chrome'])
        engine = device.pop('default_browser_type')
        browser = await (playwright.webkit.launch() if engine == 'webkit'
                         else playwright.chromium.launch(channel='chrome'))
        context = await browser.new_context(**device)
        context.set_default_navigation_timeout(60000)
        external_fonts = []
        context.on('request', lambda request: external_fonts.append(request.url)
                   if 'fonts.googleapis.com' in request.url or 'fonts.gstatic.com' in request.url else None)
        await context.route('https://*.supabase.co/**', lambda route: route.abort())
        await context.route('https://fonts.googleapis.com/**', lambda route: route.abort())
        await context.route('https://fonts.gstatic.com/**', lambda route: route.abort())
        page = await context.new_page()
        try:
            await page.goto(site + 'lesson-introduction-videos.html', wait_until='domcontentloaded')
            await page.locator('li[data-intro-slot="9"]').wait_for()
            online = await page.evaluate(FONT_CHECK)
            assert all(face['loaded'] for face in online['faces']), online
            assert online['overflow'] <= 2, online
            assert not external_fonts, external_fonts
            await page.screenshot(path=output / 'gallery.png', full_page=False)
            result = {'profile':profile, 'engine':engine, 'site':site, 'online':online,
                      'external_font_requests':external_fonts, 'physical_device':False}
            if offline:
                await page.goto(site + 'offline-reader.html', wait_until='domcontentloaded')
                await page.evaluate('async () => { await navigator.serviceWorker.ready; }')
                await page.wait_for_function('Boolean(navigator.serviceWorker.controller)', timeout=60000)
                cached = await page.evaluate("""async () => {
                  const result=[];
                  for (const name of await caches.keys()) {
                    const cache=await caches.open(name);
                    for (const request of await cache.keys())
                      if (new URL(request.url).pathname.includes('/fonts/')) result.push(request.url);
                  }
                  return [...new Set(result)];
                }""")
                assert len(cached) == 28, cached
                await context.set_offline(True)
                offline_page = await context.new_page()
                await offline_page.goto(site + 'offline-reader.html', wait_until='domcontentloaded')
                await offline_page.locator('#reading .rwl-copy').wait_for()
                reading = await offline_page.evaluate(FONT_CHECK)
                assert all(face['loaded'] for face in reading['faces']), reading
                assert reading['overflow'] <= 2, reading
                assert not external_fonts, external_fonts
                await offline_page.screenshot(path=output / 'offline-reader.png', full_page=False)
                result.update(offline=reading, cached_font_files=len(cached),
                              offline_fresh_document=True)
            (output / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
            print(json.dumps(result), flush=True)
        finally:
            await browser.close()


if __name__ == '__main__':
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--site', required=True)
    cli.add_argument('--profile', choices=('pc', 'iphone'), required=True)
    cli.add_argument('--output', required=True, type=Path)
    cli.add_argument('--offline', action='store_true')
    args = cli.parse_args()
    asyncio.run(verify(args.site.rstrip('/')+'/', args.profile, args.output, args.offline))
