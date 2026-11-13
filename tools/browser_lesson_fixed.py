"""Responsive one-viewport lesson regression on iPhone, iPad, laptop and desktop.
Uses the trusted local mock from the older comprehensive browser test; no user secrets.
"""
import ast,asyncio,shutil
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[1]
tree=ast.parse((ROOT/'tools/browser_checks.py').read_text())
MOCK=next(node.value.value for node in tree.body if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='MOCK' for t in node.targets))
async def main():
 async with async_playwright() as p:
  browser=await p.chromium.launch(headless=True,executable_path=shutil.which('google-chrome'),args=['--no-sandbox'])
  ctx=await browser.new_context(viewport={'width':390,'height':844},service_workers='block')
  await ctx.route('**/supabase-client.js*',lambda route:route.fulfill(content_type='application/javascript',body=MOCK))
  page=await ctx.new_page(); errors=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.on('dialog',lambda d:d.accept())
  async def fits():
   result=await page.evaluate("""() => {
    const stage=document.querySelector('.lesson-screen-stage');
    const excess=stage?stage.scrollHeight-stage.clientHeight:999;
    if(stage)stage.scrollTop=excess;
    const canScroll=stage&&(excess<=5||stage.scrollTop>5);
    if(stage)stage.scrollTop=0;
    return {body:getComputedStyle(document.body).overflow,windowScroll:document.documentElement.scrollHeight-innerHeight,
       horizontal:document.documentElement.scrollWidth-innerWidth,stageOverflow:excess,
       stageOverflowY:stage?getComputedStyle(stage).overflowY:'missing',canScroll};
   }""")
   assert result['body']=='hidden',result
   assert result['windowScroll']<=4 and result['horizontal']<=4,result
   assert result['stageOverflowY'] in ('auto','scroll') and result['canScroll'],result
  async def scroll_probe():
   result=await page.evaluate("""() => {
    const stage=document.querySelector('.lesson-screen-stage'),footer=document.querySelector('.lesson-screen-footer');
    const probe=document.createElement('div');
    probe.style.height=(stage.clientHeight+320)+'px';
    probe.setAttribute('data-overflow-probe','');
    stage.append(probe);
    stage.scrollTop=stage.scrollHeight;
    const scrollable=stage.scrollTop>100;
    const box=footer.getBoundingClientRect();
    const navVisible=box.top>=0&&box.bottom<=innerHeight+2;
    const horizontal=document.documentElement.scrollWidth-innerWidth;
    probe.remove();
    stage.scrollTop=0;
    return {scrollable,navVisible,horizontal};
   }""")
   assert result['scrollable'] and result['navVisible'] and result['horizontal']<=4,result
  async def next_page():
   await page.locator('[data-screen-next]').click();await page.wait_for_timeout(65)
  async def until_visible(selector,max_steps=18):
   for _ in range(max_steps):
    if await page.locator(selector).first.is_visible():return
    await next_page()
   debug=await page.evaluate("""() => ({
      stage:document.querySelector('.lesson-stage-track .here')?.textContent,
      root:[...document.querySelector('#stage').children].map(e=>({tag:e.tagName,cls:e.className,unit:e.getAttribute('data-lesson-unit'),style:e.style.display})),
      flash:document.querySelector('.flash-quiz')?.outerHTML.slice(0,300),
      flashStyle:document.querySelector('.flash-quiz')&&getComputedStyle(document.querySelector('.flash-quiz')).display,
      quick:document.querySelector('#quickCards')?.innerHTML.slice(0,260)
   })""")
   print('SCREENFLOW DEBUG',debug,flush=True)
   raise AssertionError(f'Could not reach {selector}: '+await page.locator('.lesson-screen-progress').inner_text())
  await page.goto('http://127.0.0.1:8765/')
  await page.locator('#continue').wait_for()
  assert await page.locator('.learning-focus .focus-session-card').count()==1
  assert await page.locator('.learning-note,.side-stack,.learning-to-exams,.quick-links').count()==0
  assert await page.evaluate("document.documentElement.scrollHeight<=innerHeight+4 && document.documentElement.scrollWidth<=innerWidth+4"), 'Learning home must fit on iPhone without scrolling'
  assert await page.locator('.topnav,.nav-more').count()==0, 'No horizontal tabs or extra menu row'
  # Editorial typeface and the loading-screen summit emblem remain consistent.
  branding=await page.evaluate("""() => ({
    ui:getComputedStyle(document.body).fontFamily,
    heading:getComputedStyle(document.querySelector('.focus-session-card h1')).fontFamily,
    mark:document.querySelector('.topbar .brand-mark img')?.getAttribute('src'),
    markWidth:document.querySelector('.topbar .brand-mark img')?.getBoundingClientRect().width
  })""")
  assert 'Source Sans 3' in branding['ui'] and 'Source Serif 4' in branding['heading'],branding
  assert branding['mark']=='summit-mark.svg' and branding['markWidth']>=28,branding

  await page.screenshot(path=str(ROOT/'docs/focus-learning-home-iphone.png'))
  await page.locator('#menuToggle').click()
  assert await page.locator('#courseMenu').evaluate('(node)=>node.open')
  assert (await page.locator('#navProgress').inner_text()).strip()=='0 / 372'
  await page.locator('#courseMenuContent [data-menu-screen="lessons"]').click()
  assert await page.locator('[data-menu-group]').count()==13
  await page.locator('[data-menu-group="DIV"]').click()
  assert await page.locator('.course-menu-session').count()==24
  assert await page.locator('.course-menu-session.is-current[data-menu-slot="1"]').count()==1
  assert await page.locator('.course-menu-status.current').count()==1
  assert await page.locator('.course-menu-session.is-completed').count()==0
  assert await page.locator('.course-menu-session.is-locked').count()==23
  slots=await page.locator('.course-menu-session .course-menu-number').all_text_contents()
  assert [int(n) for n in slots]==sorted(int(n) for n in slots)
  await page.screenshot(path=str(ROOT/'docs/lesson-menu-iphone.png'))
  await page.locator('[data-menu-back="sections"]').click()
  await page.locator('[data-menu-group="DIG"]').click()
  assert await page.locator('.course-menu-session.is-locked').count()==26
  assert await page.locator('[data-menu-slot="2"]').count()==0, 'Future lesson must stay locked'
  await page.locator('#menuClose').click()
  assert not await page.locator('#courseMenu').evaluate('(node)=>node.open')
  await page.locator('#menuToggle').click()
  await page.locator('#courseMenuContent [data-menu-action="profile"]').click()
  await page.get_by_role('heading',name='Summit progress').wait_for()
  assert await page.get_by_text('sessions remaining').count()==1
  await page.locator('.profile-upcoming summary').click()
  assert await page.get_by_text('Next strategy workshop').count()==1
  await page.locator('#menuToggle').click()
  await page.locator('#courseMenuContent [data-menu-action="review"]').click()
  await page.get_by_role('heading',name='Completed sessions').wait_for()
  assert not await page.locator('#courseMenu').evaluate('(node)=>node.open')
  await page.locator('#menuToggle').click()
  await page.locator('#courseMenuContent [data-menu-action="continue"]').click()
  await page.locator('.opening-film').wait_for()
  # Confirm ordinary arithmetic becomes semantic TeX without changing saved data.
  await page.locator('#stage').evaluate("""stage => {
    const p=document.createElement('p');
    p.id='summit-math-probe';p.className='math-copy';
    p.textContent='3/4 + 1/2 = 5/4 and a² + b² = c²';
    stage.append(p);
  }""")
  await page.wait_for_function("document.querySelectorAll('#summit-math-probe .math-inline[data-tex]').length >= 2")
  maths=await page.locator('#summit-math-probe .math-inline').evaluate_all(
   "(nodes)=>nodes.map(n=>({source:n.dataset.mathSource,tex:n.dataset.tex,rendered:!!n.querySelector('.katex')||n.classList.contains('math-fallback')}))")
  assert all(m['rendered'] for m in maths) and any('frac' in m['tex'] for m in maths),maths
  await page.locator('#summit-math-probe').evaluate('(node)=>node.remove()')
  # Regression for the reported iPhone issue: inline equations must sit on
  # the same baseline as the sentence, not float above it as scrollable inline-blocks.
  await page.locator('#stage').evaluate("""stage => {
    const p=document.createElement('p');
    p.id='math-baseline-probe';p.className='math-copy';
    p.textContent='Replace each 99 by 100 − 1.';
    stage.append(p);
  }""")
  await page.locator('#math-baseline-probe .math-inline').wait_for()
  await page.wait_for_timeout(120)
  alignment=await page.locator('#math-baseline-probe').evaluate("""p => {
    const math=p.querySelector('.math-inline'),style=getComputedStyle(math);
    const before=p.firstChild,after=p.lastChild,first=document.createRange(),last=document.createRange();
    first.selectNodeContents(before);last.selectNodeContents(after);
    const left=first.getBoundingClientRect(),right=last.getBoundingClientRect();
    const formula=math.getBoundingClientRect();
    return {
      display:style.display,overflowX:style.overflowX,verticalAlign:style.verticalAlign,
      fontSize:style.fontSize,mathTop:formula.top,leftTop:left.top,rightTop:right.top,
      punctuation:after.textContent,wrapped:Math.abs(left.top-right.top)>5,
      mathSource:math.dataset.mathSource
    };
  }""")
  assert alignment['display']=='inline' and alignment['overflowX']=='visible',alignment
  assert alignment['verticalAlign']=='baseline',alignment
  assert not alignment['wrapped'] and abs(alignment['mathTop']-alignment['leftTop'])<14,alignment
  assert alignment['mathSource']=='100 − 1' and alignment['punctuation']=='.',alignment
  await page.screenshot(path=str(ROOT/'docs/math-inline-baseline-iphone.png'))
  await page.locator('#math-baseline-probe').evaluate('(node)=>node.remove()')

  assert await page.locator('#openingVideo').count()==1
  assert 'S001-Intro.mp4' in await page.locator('#openingVideo').get_attribute('src')
  assert 'Video' in await page.locator('.lesson-stage-track .here').inner_text()
  await fits()
  await scroll_probe()  # Taller-than-screen lesson content must scroll; Back/Next stays fixed.
  await page.screenshot(path=str(ROOT/'docs/video-first-session-1-iphone.png'))
  await next_page()
  assert 'Remember' in await page.locator('.lesson-stage-track .here').inner_text()
  await fits()
  await next_page()
  await page.locator('#retrievalChecks').wait_for()
  await next_page()
  assert 'Discover' in await page.locator('.lesson-stage-track .here').inner_text()
  await until_visible('.flash-quiz')
  await fits()
  await page.screenshot(path=str(ROOT/'docs/lesson-flash-iphone.png'))
  for k in range(5):
   choice=await page.evaluate(f"import('./flash-cards.js?v=recognition-20261113').then(m=>m.flashDeck('DIV-03',1,1)[{k}].answer)")
   await page.locator('.flash-option').nth(choice).click()
   await page.locator('.flash-next').click()
  await page.locator('.flash-summary').wait_for()
  await fits()
  # New teaching cards start at the top even when the previous card was scrolled.
  scrolled=await page.evaluate("""() => {
    const stage=document.querySelector('.lesson-screen-stage');
    const spacer=document.createElement('div');
    spacer.dataset.scrollTest='yes';
    spacer.style.height='1300px';
    document.querySelector('.flash-quiz').append(spacer);
    stage.scrollTop=stage.scrollHeight;
    return stage.scrollTop;
  }""")
  assert scrolled>100,scrolled
  await next_page()
  assert await page.locator('.lesson-screen-stage').evaluate('(stage)=>stage.scrollTop')==0
  await page.evaluate("document.querySelector('[data-scroll-test]')?.remove()")
  await page.locator('#guidedCheck .mini-check').wait_for()
  await page.locator('#guidedCheck .short-answer').fill('123')
  await page.locator('#guidedCheck button.primary').click()
  await next_page();await next_page()
  assert 'Try' in await page.locator('.lesson-stage-track .here').inner_text()
  # The partial example, six extra numerical problems and two original problems
  # require only final answers; no clue/plan/working/reflection text fields exist.
  assert await page.locator('.lesson-fade-unit .method').count()==0
  val=await page.evaluate("import('./transfer-practice.js?v=recognition-20261113').then(m=>String(m.practice('DIV-03',9).value))")
  await page.locator('.lesson-fade-unit .response').fill(val)
  await page.locator('.lesson-fade-unit').get_by_role('button',name='Check answer').click()
  await next_page()
  await page.locator('.lesson-prep-unit .short-answer').fill('4')
  await page.locator('.lesson-prep-unit button.primary').click()
  await next_page()
  for k in range(3):
   input_sel=f'.lesson-extra-unit [data-extra-question="{k}"] .response'
   await until_visible(input_sel)
   seed=12+k
   answer=await page.evaluate(f"import('./transfer-practice.js?v=recognition-20261113').then(m=>String(m.practice('DIV-03',{seed}).value))")
   await page.locator(input_sel).fill(answer)
   await page.locator(f'.lesson-extra-unit [data-extra-question="{k}"]').get_by_role('button',name='Check answer').click()
   await next_page()
  await until_visible('.lesson-problem-unit .final-answer-input')
  assert await page.locator('[data-reason="clue"],[data-reason="plan"],.working-box').count()==0
  await page.locator('.lesson-problem-unit .final-answer-input').fill('12')
  await page.locator('.lesson-problem-unit .submit-answer').click()
  await page.locator('.lesson-problem-unit .submit-answer').wait_for(state='hidden')
  await fits()
  await page.locator('[data-screen-back]').click()
  await page.locator('[data-screen-next]').click()
  assert await page.locator('.lesson-problem-unit .final-answer-input').input_value()=='12'
  await next_page()
  await next_page()
  assert 'Transfer' in await page.locator('.lesson-stage-track .here').inner_text()
  # Regression for iPhone screenshot: the blue transfer heading must stay ordinary
  # Source Sans text, not be transformed into overlapping italic TeX glyphs.
  await until_visible('.lesson-extra-unit [data-extra-question="0"] .eyebrow')
  await page.wait_for_timeout(150)
  heading=await page.locator('.lesson-extra-unit [data-extra-question="0"] .eyebrow').evaluate("""el=>({
    text:el.textContent.trim(),
    mathNodes:el.querySelectorAll('.katex,.math-inline').length,
    italic:getComputedStyle(el).fontStyle,
    family:getComputedStyle(el).fontFamily,
    width:el.clientWidth,scrollWidth:el.scrollWidth
  })""")
  assert heading['text']=='TRANSFER · PROBLEM 1 OF 3',heading
  assert heading['mathNodes']==0 and heading['italic']=='normal',heading
  assert 'Source Sans 3' in heading['family'] and heading['scrollWidth']<=heading['width']+2,heading
  await page.screenshot(path=str(ROOT/'docs/transfer-label-iphone.png'))
  for k in range(3):
   input_sel=f'.lesson-extra-unit [data-extra-question="{k}"] .response'
   await until_visible(input_sel)
   seed=15+k
   answer=await page.evaluate(f"import('./transfer-practice.js?v=recognition-20261113').then(m=>String(m.practice('DIV-03',{seed}).value))")
   await page.locator(input_sel).fill(answer)
   await page.locator(f'.lesson-extra-unit [data-extra-question="{k}"]').get_by_role('button',name='Check answer').click()
   await next_page()
  await until_visible('.lesson-problem-unit .final-answer-input')
  await page.locator('.lesson-problem-unit .final-answer-input').fill('12')
  await page.locator('.lesson-problem-unit .submit-answer').click()
  await page.locator('.lesson-problem-unit .submit-answer').wait_for(state='hidden')
  await next_page()
  await next_page()
  assert 'Check' in await page.locator('.lesson-stage-track .here').inner_text()
  assert await page.locator('#takeaway,#watch,[data-final-check],#transferConfidence').count()==0
  assert await page.locator('.lesson-check-summary').count()==1
  assert '6 / 6' in await page.locator('.lesson-check-summary').inner_text()
  await fits()
  await page.screenshot(path=str(ROOT/'docs/lesson-final-iphone.png'))
  await next_page()
  await page.locator('#continue').wait_for()
  assert await page.evaluate('fixture.records[0].immutable===true && fixture.progress.completed_sessions===1')
  await page.locator('#menuToggle').click()
  assert (await page.locator('#navProgress').inner_text()).strip()=='1 / 372'
  await page.locator('#courseMenuContent [data-menu-screen="lessons"]').click()
  await page.locator('[data-menu-group="DIV"]').click()
  completed=page.locator('.course-menu-session.is-completed[data-menu-slot="1"]')
  assert await completed.count()==1, 'Finished lesson must get a green completion status'
  assert (await completed.locator('.course-menu-status.completed').inner_text()).strip()=='✓'
  completed_colour=await completed.locator('.course-menu-status.completed').evaluate('(el)=>getComputedStyle(el).color')
  assert completed_colour!='rgb(255, 255, 255)',completed_colour
  # Completed lesson has both a saved-work entry and a direct video replay action.
  assert await completed.locator('[data-menu-intro-slot="1"]').count()==1
  snapshot=await page.evaluate("""() => ({writes:fixture.writes.length,done:fixture.progress.completed_sessions,
    answer:fixture.records[0].answers,working:fixture.records[0].working,immutable:fixture.records[0].immutable})""")
  await completed.locator('[data-menu-intro-slot="1"]').click()
  await page.locator('#replayIntroVideo').wait_for()
  assert await page.locator('#replayIntroVideo').get_attribute('controls') is not None
  assert 'media/S001-Intro.mp4' in await page.locator('#replayIntroVideo').get_attribute('src')
  assert await page.locator('.lesson-replay-note').get_by_text('cannot restart',exact=False).count()==1
  assert await page.locator('[data-screen-next],.submit-answer').count()==0
  await page.wait_for_timeout(200)
  now=await page.evaluate("""() => ({writes:fixture.writes.length,done:fixture.progress.completed_sessions,
    answer:fixture.records[0].answers,working:fixture.records[0].working,immutable:fixture.records[0].immutable})""")
  assert now==snapshot,('Video replay must be completely read-only',snapshot,now)
  await page.screenshot(path=str(ROOT/'docs/completed-lesson-intro-iphone.png'))
  await page.locator('#replayBack').click()
  await page.locator('.review-detail[data-review-session="1"][open]').wait_for()
  assert await page.locator('.saved-intro[data-video-session="1"]').count()==1
  await page.locator('.saved-intro[data-video-session="1"]').click()
  await page.locator('#replayIntroVideo').wait_for()
  await page.locator('#replayHome').click()
  await page.locator('#menuToggle').click()
  await page.locator('#courseMenuContent [data-menu-action="continue"]').click()
  assert 'S002-Intro.mp4' in await page.locator('#openingVideo').get_attribute('src')
  await fits()
  await page.screenshot(path=str(ROOT/'docs/video-first-session-2-iphone.png'))
  for viewport in [
   {'width':820,'height':1180},  # iPad portrait
   {'width':1024,'height':768},  # iPad landscape
   {'width':1366,'height':768},  # Laptop
   {'width':1920,'height':1080}, # Desktop
   {'width':1280,'height':900}
  ]:
   await page.set_viewport_size(viewport)
   await fits()
   await scroll_probe()
  await page.screenshot(path=str(ROOT/'docs/video-first-session-2-desktop.png'))
  await page.locator('[data-screen-back]').click()
  await page.locator('#continue').wait_for()
  assert not errors,errors
  await browser.close()
 print('PASS: responsive scrolling lessons with fixed navigation, six answer-only practice problems, read-only replay, and immutable completion.')
asyncio.run(main())
