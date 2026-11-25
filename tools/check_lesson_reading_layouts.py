"""Exercise all 283 authored lesson openings inside the student reader on one device profile."""
import argparse
import asyncio
import json
from pathlib import Path

from playwright.async_api import async_playwright
from browser_lesson_fixed import MOCK
from check_lesson_film_routes import PROFILES

MEASURE = """async () => {
  const {renderReviewedLesson} = await import('./reviewed-lesson.js');
  const {typesetMath} = await import('./math-typography.js?v=advanced-20261113');
  const volumes = await Promise.all(['read-watch-practise','read-watch-practise-later']
    .map(async f => (await fetch('data/'+f+'.json')).json()));
  const lessons = volumes.flatMap(v => v.lessons);
  const app = document.querySelector('#app');
  const readings = [];
  const authoredText = node => {
    const copy = node.cloneNode(true);
    for (const math of copy.querySelectorAll('[data-math-source]')) {
      const source = math.dataset.mathSource;
      const annotation = math.querySelector('.katex-mathml annotation[encoding="application/x-tex"]');
      if (math.getAttribute('aria-label') !== source ||
          (annotation ? annotation.textContent !== math.dataset.tex :
            !math.classList.contains('math-fallback') || math.textContent !== source))
        throw Error('Rendered mathematics differs from its preserved source');
      // KaTeX contains both accessible MathML and visual HTML. Compare the one
      // exact authored expression, rather than their combined textContent.
      math.replaceWith(document.createTextNode(source));
    }
    return copy.textContent;
  };
  for (const lesson of lessons) {
    const session = {slot:lesson.slot, focus:lesson.headline};
    const draft = {summary:{}, answers:{}, working:{}, evidence:{}};
    renderReviewedLesson({app, s:session, l:lesson, questions:lesson.questions, draft,
      markLocal:()=>{}, save:()=>{}, changedSize:()=>{}, video:()=>'<video controls></video>'});
    const stage = app.querySelector('#stage'), card = stage.querySelector('.rwl-example');
    const figure = card.querySelector('.rwl-opening-figure');
    if (figure) await figure.decode();
    // The live observer runs on animation frames. Typeset explicitly so neither
    // authored-text assertions nor geometry depend on image/network scheduling.
    typesetMath(app);
    await document.fonts.ready;
    await new Promise(requestAnimationFrame);
    if (!card.isConnected || app.querySelector('.session-page').getAttribute('aria-label') !== 'Session '+lesson.slot)
      throw Error('Another lesson replaced the measured reader in lesson '+lesson.slot);
    const next = app.querySelector('[data-screen-next]').getBoundingClientRect();
    const prompt = authoredText(card.querySelector(':scope > p'));
    const prediction = authoredText(card.querySelector('.rwl-predict'));
    const first = authoredText(card.querySelector('.rwl-first-step p'));
    const scroll = stage.scrollHeight-stage.clientHeight;
    const horizontal = Math.max(document.documentElement.scrollWidth-innerWidth, stage.scrollWidth-stage.clientWidth);
    card.querySelector('.rwl-full-example').open = true;
    const full = [...card.querySelectorAll('.rwl-full-example > ol > li')].map(authoredText);
    if (prompt!==lesson.example.prompt || prediction!==lesson.example.prediction ||
        first!==lesson.example.steps[0] || JSON.stringify(full)!==JSON.stringify(lesson.example.steps))
      throw Error('Different prompt or working in lesson '+lesson.slot);
    readings.push({slot:lesson.slot, horizontal, scroll, footer:next.bottom-innerHeight,
      authored_text_preserved:true, typeset_expressions:card.querySelectorAll('[data-math-source]').length});
  }
  return readings;
}"""


async def run(args):
    async with async_playwright() as pw:
        name, landscape = PROFILES[args.profile]
        device = dict(pw.devices[name])
        engine = device.pop('default_browser_type')
        if landscape:
            for key in ('viewport', 'screen'):
                if key in device:
                    w, h = device[key]['width'], device[key]['height']
                    device[key] = {'width':h, 'height':w}
        if args.viewport is not None or args.profile == 'pc':
            width, height = args.viewport or (1440, 900)
            size = {'width':width, 'height':height}
            device.update(viewport=size, screen=size.copy())
        browser = await (pw.webkit.launch() if engine == 'webkit' else pw.chromium.launch(channel='chrome'))
        context = await browser.new_context(**device, service_workers='block')
        await context.route('**/supabase-client.js*',
                            lambda route: route.fulfill(content_type='application/javascript',body=MOCK))
        await context.route('https://*.supabase.co/**', lambda route: route.abort())
        try:
            page = await context.new_page()
            await page.goto(args.site,wait_until='domcontentloaded')
            await page.locator('#continue').click()
            await page.locator('.rwl-example').wait_for()
            await page.wait_for_function("typeof window.katex?.render === 'function'")
            await page.evaluate('document.fonts.ready')
            rows = await page.evaluate(MEASURE)
            assert len(rows) == len({row['slot'] for row in rows}) == 283
            args.output.write_text(json.dumps(rows,indent=2)+'\n')
            failures = [r for r in rows if r['horizontal']>2 or r['footer']>2 or (
                        args.profile in ('ipad-portrait','ipad-landscape','pc') and r['scroll']>2)]
            assert not failures, failures
            print('283 lesson openings fit',args.profile)
        finally:
            await browser.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--profile',choices=PROFILES,required=True)
    parser.add_argument('--site',default='http://127.0.0.1:8765/')
    parser.add_argument('--viewport',type=int,nargs=2,metavar=('WIDTH','HEIGHT'))
    parser.add_argument('--output',type=Path,required=True)
    asyncio.run(run(parser.parse_args()))
