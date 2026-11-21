"""Exercise the complete workshop path against synthetic records through the real student UI."""
import argparse
import asyncio
import json
import shutil
from pathlib import Path

from playwright.async_api import async_playwright, expect
from browser_lesson_fixed import MOCK


ROOT = Path(__file__).resolve().parents[1]


async def open_fixture(browser, base, slot, records, width):
    context = await browser.new_context(viewport={'width': width, 'height': 844}, service_workers='block',
                                        reduced_motion='reduce')
    await context.route('**/supabase-client.js*', lambda route: route.fulfill(
        content_type='application/javascript', body=MOCK))
    await context.route('https://raw.githubusercontent.com/**', lambda route: route.abort())
    initial = dict(records=records, attempts=[], exams=[], writes=[], fail=False,
                   progress=dict(completed_sessions=slot-1, current_session=slot, xp=0, rank=0, state={}))
    await context.add_init_script('window.fixture=JSON.parse(sessionStorage.getItem("workshop-fixture"))||'
                                  + json.dumps(initial))
    page = await context.new_page()
    page.set_default_timeout(14000)
    await page.goto(base, wait_until='domcontentloaded')
    await page.locator('#continue').click()
    await page.locator('#workshopQuestions .mini-check').first.wait_for()
    return context, page


async def authored_text(locator):
    """Read each typeset expression once, using the source carried by its visual span."""
    return await locator.evaluate("""element => {
        const copy = element.cloneNode(true);
        for (const formula of copy.querySelectorAll('[data-math-source]')) {
            formula.replaceWith(document.createTextNode(formula.dataset.mathSource));
        }
        return copy.textContent.trim();
    }""")


async def solve_visit(browser, base, study, index):
    slot = study['slot']
    earlier = dict(session_number=study['prior'], completed_at='2026-01-01', immutable=True,
                   answers={}, evidence={}, working={}, summary={'skill_id': study['id']})
    context, page = await open_fixture(browser, base, slot, [earlier], (390, 768, 1280)[index % 3])
    try:
        await expect(page.locator('.session-page h1')).to_have_text(study['title'])
        forms = page.locator('#workshopQuestions .mini-check')
        await expect(forms).to_have_count(6)
        await expect(page.locator('#completeWorkshop')).to_be_disabled()
        assert await page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1')
        for i, question in enumerate(study['questions']):
            card = forms.nth(i)
            assert await authored_text(card.locator(':scope > p').first) == question['prompt']
            if i == 5:
                await card.locator('button.hint').click()
                assert await authored_text(card.locator('.feedback')) == study['hint']
            await card.locator('input').fill(str(question['value']))
            await card.locator('form .primary').click()
            await expect(card.locator('.feedback ol li')).to_have_count(3)
            await expect(card.locator('input')).to_be_disabled()
        await expect(page.locator('#completeWorkshop')).to_be_disabled()
        for _ in range(5):
            await page.locator('.flash-option').first.click()
            await page.locator('.flash-next').click()
        await page.locator('#completeWorkshop').click()
        await page.locator('.focus-session-card').wait_for()
        record = await page.evaluate('n => fixture.records.find(r => r.session_number === n)', slot)
        assert record['immutable'] and record['evidence']['mixed:5']['used_help']
        assert all(record['evidence'][f'mixed:{i}']['correct'] for i in range(6))
        assert record['summary']['focus'] == study['title']
        await page.evaluate('sessionStorage.setItem("workshop-fixture",JSON.stringify(fixture))')
        await page.goto(base + '?view=review', wait_until='domcontentloaded')
        notebook = page.locator(f'[data-review-session="{slot}"]')
        await notebook.locator(':scope > summary').click()
        last = notebook.locator('article').filter(has=page.get_by_role('heading',
                                               name=study['questions'][-1]['prompt'], exact=True))
        await last.get_by_text('See the worked solution', exact=True).click()
        await expect(last.locator('li')).to_have_text(study['steps'])
        await last.get_by_role('button', name='Revisit lesson', exact=False).click()
        await expect(page.locator('.rwl-review-note')).to_be_visible()
        untouched = await page.evaluate('n => fixture.records.find(r => r.session_number === n)', slot)
        assert untouched == record
    finally:
        await context.close()


async def run(base, all_visits):
    proc = await asyncio.create_subprocess_exec('node', '--input-type=module', '-e', """
        import {workshopStudies} from './workshop-studies.js';
        import {practice} from './transfer-practice.js';
        import {skillFor} from './curriculum.js';
        import fs from 'node:fs';
        const courses=JSON.parse(fs.readFileSync('data/sessions-372.json')).sessions;
        const taxonomy=JSON.parse(fs.readFileSync('data/taxonomy-52.json'));
        console.log(JSON.stringify([...workshopStudies].map(([slot,q])=>({
          slot,id:q.id,title:q.title,steps:q.steps,hint:q.hint,
          prior:courses.find(s=>s.type==='LESSON'&&skillFor(s,taxonomy)===q.id).slot,
          questions:[...q.recall.map(([id,seed])=>practice(id,seed)),q].map(({prompt,value})=>({prompt,value}))
        }))));
    """, stdout=asyncio.subprocess.PIPE, cwd=ROOT)
    output, _ = await proc.communicate()
    assert proc.returncode == 0
    studies = json.loads(output)
    if not all_visits:
        studies = [studies[0], studies[15], studies[-1]]
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(executable_path=shutil.which('google-chrome') or shutil.which('chromium'))
        try:
            limit = asyncio.Semaphore(3)
            async def visit(i, study):
                async with limit:
                    await solve_visit(browser, base, study, i)
            await asyncio.gather(*(visit(i, study) for i, study in enumerate(studies)))
            # Earlier workshops kept the assigned length, typed work and exact marked prompt.
            record = dict(session_number=16, answers={}, working={'mixed:2:answer': '41'}, evidence={},
                          summary={'mixed_skills':['DIV-03','DIG-01','DIG-02','DIG-03']})
            context, page = await open_fixture(browser, base, 16, [record], 390)
            await expect(page.locator('#workshopQuestions .mini-check')).to_have_count(4)
            await expect(page.locator('[data-mixed="2"] input')).to_have_value('41')
            await expect(page.locator('#workshopStatus')).to_contain_text('0 of 4')
            await context.close()
        finally:
            await browser.close()
    print(f'Passed {len(studies)} workshop completions, saved solutions and return to a studied lesson; legacy draft preserved.')


if __name__ == '__main__':
    args = argparse.ArgumentParser(description=__doc__)
    args.add_argument('--base', default='http://127.0.0.1:8765/')
    args.add_argument('--all', action='store_true')
    options = args.parse_args()
    asyncio.run(run(options.base.rstrip('/')+'/', options.all))
