"""Responsive one-viewport lesson regression on iPhone, iPad, laptop and desktop.
Uses the trusted local mock from the older comprehensive browser test; no user secrets.
"""
import ast,asyncio,json,os,shutil
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[1]
SCREENSHOTS=Path(os.environ.get('SUMMIT_SCREENSHOT_DIR', ROOT/'docs'))
SCREENSHOTS.mkdir(parents=True, exist_ok=True)
tree=ast.parse((ROOT/'tools/browser_checks.py').read_text())
MOCK=next(node.value.value for node in tree.body if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='MOCK' for t in node.targets))
async def verify_course_restart(browser):
 """A course restart isolates unsynced lesson work and revision practice on the same device."""
 for review in (False,True):
  ctx=await browser.new_context(service_workers='block')
  await ctx.route('**/supabase-client.js*',lambda route:route.fulfill(content_type='application/javascript',body=MOCK))
  await ctx.add_init_script("""
   const review=new URLSearchParams(location.search).has('view');
   const run=sessionStorage.getItem('fixture-run');
   const record={session_number:1,immutable:true,completed_at:'2026-01-01T00:00:00Z',answers:{},evidence:{},working:{},summary:{}};
   window.fixture={records:review?[record]:[],attempts:[],exams:[],writes:[],fail:false,
    progress:{completed_sessions:review?1:0,current_session:review?2:1,xp:0,rank:0,state:run?{course_run_id:run}:{}}};
  """)
  page=await ctx.new_page()
  page.on('dialog',lambda d:d.accept())
  url='http://127.0.0.1:8765/'+('?view=review' if review else '')
  await page.goto(url)
  cases=[(None,'','original work'),(None,'original work','legacy edit'),
         ('restart-1','','new work'),('restart-1','new work','new edit'),('restart-2','','')]
  for index,(run,expected,entry) in enumerate(cases):
   if index:
    if run:await page.evaluate("run=>sessionStorage.setItem('fixture-run',run)",run)
    await page.reload()
   if review:
    await page.locator('[data-review-session="1"] summary').click()
    await page.locator('[data-revised-copy="1"]').click()
   else:
    await page.locator('#continue').click()
   await page.locator('.rwl').wait_for()
   if review or not expected:
    await page.locator('.rwl-example').wait_for()
    await page.locator('[data-screen-next]').click()
    await page.locator('[data-screen-next]').click()
   field=page.locator('.rwl-form input')
   assert await field.input_value()==expected,(review,run,expected)
   # Leave a real unsynced working answer on this browser across reloads.
   await page.evaluate('fixture.fail=true')
   if entry:await field.fill(entry)
  await ctx.close()
 print('PASS: legacy and current-run lesson drafts and revision copies resume; successive resets start blank.',flush=True)


async def verify_revised_lessons(browser):
 """Exercise the published S001/002 route using a synthetic learner and grading service."""
 ctx=await browser.new_context(viewport={'width':390,'height':844}, service_workers='block')
 calls=[]
 async def mock_api(route):
  await route.fulfill(content_type='application/javascript', body=MOCK.replace('correct:true,independent_credit:',"correct:body.answer_text!=='fixture-miss',independent_credit:").replace(
   'functions:{invoke:async(name,{body})=>({data:',
   'functions:{invoke:async(name,{body})=>(await window.fixtureInvoke(name,body),{data:'))
 await ctx.expose_function('fixtureInvoke', lambda name,body: calls.append((name,body)))
 await ctx.route('**/supabase-client.js*', mock_api)
 page=await ctx.new_page()
 errors=[]
 page.on('pageerror',lambda err: errors.append(str(err)))
 await page.goto('http://127.0.0.1:8765/')
 await page.locator('#continue').click()
 read=page.locator('.rwl-example')
 await read.wait_for()
 assert await read.locator('li').count()>=2
 assert await page.locator('.rwl-bridge').is_visible()
 assert not await page.locator('#openingVideo,.rwl-form').count()
 async def fits():
  box=await page.evaluate("""() => {
   const el=document.querySelector('.lesson-screen-stage'), f=document.querySelector('.lesson-screen-footer').getBoundingClientRect();
   return {windowX:document.documentElement.scrollWidth-innerWidth, stageX:el.scrollWidth-el.clientWidth,
     footerTop:f.top, footerBottom:f.bottom, height:innerHeight};
  }""")
  assert box['windowX']<=2 and box['stageX']<=2 and 0<=box['footerTop']<box['footerBottom']<=box['height']+2, box
 await fits()
 await page.screenshot(path=str(SCREENSHOTS/'read-session-1-iphone.png'))
 first=read.locator('.rwl-first-step')
 full=read.locator('.rwl-full-example')
 assert not await first.locator('p').is_visible()
 assert not await full.locator('ol').is_visible()
 # Full working is available immediately and both disclosures work from the keyboard.
 await full.locator(':scope > summary').press('Enter')
 assert await full.locator('ol').is_visible()
 await first.locator('summary').press('Space')
 assert await first.locator('p').is_visible()
 assert not await full.locator('ol').is_visible()
 await full.locator(':scope > summary').click()
 assert await full.locator('ol').is_visible() and not await first.locator('p').is_visible()
 await fits()
 assert not any(name in ('submit-problem-attempt','get-problem-solution') for name,_ in calls)
 # Check the shared renderer against every authored example, including symbols and figures.
 count=await page.evaluate("""async () => {
   const {readCard}=await import('./reviewed-lesson.js');
   const volumes=await Promise.all(['read-watch-practise','read-watch-practise-later']
     .map(async name=>(await fetch('./data/'+name+'.json')).json()));
   const lessons=volumes.flatMap(volume=>volume.lessons);
   const template=document.createElement('template');
   for(const lesson of lessons){
     template.innerHTML=readCard(lesson);
     const card=template.content.querySelector('.rwl-example'), example=lesson.example;
     const first=card.querySelector('.rwl-first-step p'), full=card.querySelector('.rwl-full-example');
     const steps=Array.from(full.querySelectorAll(':scope > ol > li'),item=>item.textContent);
     if(card.querySelector('details[open]') || card.querySelector('p').textContent!==example.prompt
        || first.textContent!==example.steps[0] || JSON.stringify(steps)!==JSON.stringify(example.steps)
        || card.querySelector('img')?.getAttribute('alt')!==example.figure?.alt){
       throw Error('Worked example changed in session '+lesson.slot);
     }
   }
   return lessons.length;
 }""")
 assert count==283,count
 next_button=page.locator('[data-screen-next]')
 back=page.locator('[data-screen-back]')
 async def play_phase(slot):
  await next_button.click()
  video=page.locator('#openingVideo')
  await video.wait_for()
  assert f'S{slot:03}-Intro.mp4' in await video.get_attribute('src')
  assert await video.get_attribute('controls') is not None
  assert 'Watch' in await page.locator('[aria-current="step"]').inner_text()
  await fits()
 await play_phase(1)
 await next_button.click()
 await page.locator('.rwl-form').wait_for()
 assert 'Practise' in await page.locator('[aria-current="step"]').inner_text()
 question_ids=await page.evaluate('fixture.records[0].summary.problems')
 assert len(question_ids)>=4 and len(set(question_ids))==len(question_ids)
 for index,qid in enumerate(question_ids):
  await page.locator('.rwl-form').wait_for()
  assert not await page.locator('.rwl-solution').is_visible()
  assert await next_button.is_disabled()
  assert not await page.locator('.rwl-problem textarea').count()
  if index==0:
   await page.locator('.rwl-hint summary').click()
   await page.locator('.rwl-hint p').wait_for()
   await page.locator('.rwl-hint summary').click()
  if index==len(question_ids)-1:
   assert await page.get_by_text('UNFAMILIAR CHALLENGE',exact=True).is_visible()
  await page.locator('.rwl-form input').fill('fixture-miss' if index in (1,2) else '12')
  await page.locator('.rwl-form button').click()
  await page.wait_for_function("!document.querySelector('[data-screen-next]').disabled")
  assert calls[-1][0]=='submit-problem-attempt' and calls[-1][1]['problem_id']==qid
  if index in (1,2):
   rethink=page.locator('.rwl-rethink')
   await rethink.locator('summary').click()
   assert (await rethink.locator('p').inner_text()).strip()
   assert await page.locator('.rwl-solution').is_visible()
   assert await page.locator('.rwl-form input').is_disabled()
   assert calls[-1][0]=='submit-problem-attempt'
  if index==0:
   assert calls[-1][1]['used_help'] is True
   await page.locator('.rwl-solution').click()
   await page.locator('.rwl-steps').wait_for()
   assert calls[-1][0]=='get-problem-solution' and calls[-1][1]['problem_id']==qid
   assert 'Six plus six' in await page.locator('.rwl-steps').inner_text()
   await fits()
   await back.click()
   await next_button.click()
   assert await page.locator('.rwl-form input').is_disabled()
   assert await page.locator('.rwl-form input').input_value()=='12'
  await next_button.click()
 await page.locator('.rwl-results').wait_for()
 assert await page.locator('[data-revisit]').count()==len(question_ids)
 assert await page.locator('[data-revisit] b').all_text_contents()==['Correct with support','Try again on paper','Try again on paper',*['Correct']*(len(question_ids)-3)]
 await fits()
 await next_button.click()
 await page.locator('#continue').wait_for()
 assert await page.evaluate('fixture.records[0].immutable && fixture.progress.completed_sessions===1')
 snapshot=await page.evaluate('JSON.stringify(fixture.records[0])')
 await page.locator('#menuToggle').click()
 await page.locator('[data-menu-action="review"]').click()
 await page.locator('[data-review-session="1"] summary').click()
 await page.locator('[data-revised-copy="1"]').click()
 await read.wait_for()
 assert await page.locator('.rwl-review-note').is_visible()
 await back.click()
 assert snapshot==await page.evaluate('JSON.stringify(fixture.records[0])')
 await page.locator('#menuToggle').click()
 await page.locator('[data-menu-action="continue"]').click()
 await read.wait_for()
 second_method=read.locator('.rwl-second-method')
 assert not await second_method.is_visible()
 await read.locator('.rwl-full-example > summary').click()
 assert await second_method.is_visible() and not await second_method.locator('p').first.is_visible()
 await second_method.locator('summary').press('Enter')
 assert '248' in await second_method.locator('p').first.inner_text()
 comparison=second_method.locator('p').last
 assert 'Which would you try' in await comparison.inner_text()
 assert await comparison.evaluate("""p => p.textContent.includes('47 × 8') ||
   Boolean(p.querySelector('[data-math-source="47 × 8"]'))""")
 await fits()
 await play_phase(2)
 await back.click()
 assert await read.is_visible()
 for width,height in [(320,568),(390,844),(820,1180),(1024,768),(1366,768)]:
  await page.set_viewport_size({'width':width,'height':height})
  await fits()
 await ctx.close()
 assert not errors,errors
 print(f'PASS: revised S001 Read → Watch → Practise through all {len(question_ids)} attempts, gated solutions, saved results, lock and S002 opening.',flush=True)

async def verify_later_lessons(browser):
 """Cover a dedicated introduction, a shared technique film and the last capstone."""
 import json
 volume=json.loads((ROOT/'data/read-watch-practise-later.json').read_text())
 lessons={l['slot']:l for l in volume['lessons']}
 for slot in (69,158,318,333,370):
  lesson=lessons[slot]
  ctx=await browser.new_context(viewport={'width':390,'height':844},service_workers='block')
  await ctx.add_init_script(f"""window.fixture={{records:[],attempts:[],exams:[],
   progress:{{completed_sessions:{slot-1},current_session:{slot},xp:0,rank:0,state:{{}}}},writes:[],fail:false}}""")
  await ctx.route('**/supabase-client.js*',lambda route: route.fulfill(content_type='application/javascript',body=MOCK))
  page=await ctx.new_page()
  await page.goto('http://127.0.0.1:8765/')
  await page.locator('#continue').click()
  await page.locator('.rwl-example').wait_for()
  assert lesson['headline']==await page.locator('.rwl-copy h2').inner_text()
  if slot==318:
   model=page.locator('.route-model')
   await model.locator(':scope > summary').click()
   await model.locator('select').select_option('edge')
   await model.locator('.rm-proof > summary').press('Enter')
   assert '7 routes' in await model.locator('.rm-total').inner_text()
   assert await page.evaluate('fixture.attempts.length === 0')
  if slot==333:
   model=page.locator('.domino-model')
   await model.locator(':scope > summary').press('Enter')
   await model.locator('[data-action="impossible"]').click()
   assert 'A1 and A3' in await model.locator('.dm-message').inner_text()
   assert await page.evaluate('fixture.attempts.length === 0')
  forward=page.locator('[data-screen-next]')
  await forward.click()
  assert await page.locator('#openingVideo').get_attribute('src')==lesson['movie']
  if lesson['filmUse']=='technique':
   assert await page.get_by_text('Technique film from lesson '+lesson['videoId']+'.',exact=True).is_visible()
  await forward.click()
  await page.locator('.rwl-form').wait_for()
  assert (await page.locator('.problem-prompt').inner_text()).strip()
  assert await forward.is_disabled()
  await page.locator('.rwl-form input').fill('12')
  await page.locator('.rwl-form button').click()
  await page.locator('.rwl-solution').click()
  assert await page.locator('.rwl-steps').is_visible()
  await ctx.close()
 print('PASS: dedicated, technique-film and final capstone lessons on a phone viewport.',flush=True)


async def verify_mawa_visits(browser):
 """Open actual MAWA screens with isolated signed-in fixture records and notebook work."""
 service=(ROOT/'tools/browser_fixture.js').read_text()
 async def scenario(records,local_draft=None):
  ctx=await browser.new_context(viewport={'width':390,'height':844},service_workers='block')
  await ctx.route('**/supabase-client.js*',lambda r:r.fulfill(content_type='application/javascript',body=service))
  state={'counter':0,'session_records':records,'progress_state':[{'user_id':'fixture-learner','completed_sessions':146,'state':{}}]}
  script='globalThis.__fixture = JSON.parse(sessionStorage.getItem("mawa-db") || "null") || '+json.dumps(state)+';'
  if local_draft:
   script+='localStorage.setItem("summit-draft:fixture-learner:147",'+json.dumps(json.dumps({'updated_at':'2099-01-01T00:00:00Z','draft':local_draft}))+');'
  await ctx.add_init_script(script)
  page=await ctx.new_page()
  await page.goto('http://127.0.0.1:8765/')
  await page.locator('#continue').click()
  return ctx,page

 def record(**fields):
  return dict(user_id='fixture-learner',session_number=147,answers={},evidence={},**fields)
 # Both cloud and newer local drafts predate the version field.
 working={'mawa_base':'My original working'}
 for local in [False,True]:
  draft={'working':working,'answers':{},'evidence':{},'summary':{}}
  ctx,page=await scenario([] if local else [record(working=working,summary={})],draft if local else None)
  await page.get_by_role('heading',name='The reverse-number detective').wait_for()
  await page.locator('[data-stage="3"]').click()
  assert 'Then change a condition' in await page.locator('#stage').inner_text()
  stored=await page.evaluate('__fixture.session_records[0]')
  assert stored['summary']['investigation_edition']=='mawa-20-v1' and stored['working']==working
  await ctx.close()

 ctx,page=await scenario([])
 await page.get_by_role('heading',name='A number filed back to front').wait_for()
 await page.locator('[data-stage="1"]').click()
 await page.get_by_role('heading',name='What changes when 62 becomes 26?').wait_for()
 for _ in range(5):
  await page.locator('.flash-option').first.click()
  await page.locator('.flash-next').click()
 await page.locator('#nextStage').click()
 await page.locator('#recordMawa').click()
 await page.locator('#nextStage').click()
 assert 'Erase the sum clue' in await page.locator('#stage').inner_text()
 await page.locator('#recordExt').click()
 await page.locator('#nextStage').click()
 await page.get_by_text('Compare with model reasoning').click()
 model=await page.locator('.solution-panel').evaluate("""panel => {
  const copy = panel.cloneNode(true);
  for (const math of copy.querySelectorAll('[data-math-source]')) math.replaceWith(math.dataset.mathSource);
  return copy.textContent;
 }""")
 assert '73 + 37 = 110' in model and 'The equations force both digits' in model,model
 for name,value in [('rResult','0'),('rMethod','2'),('rProof','1'),('rClarity','1')]:
  await page.locator('#'+name).fill(value)
 await page.locator('#completeMawa').click()
 await page.locator('#continue').wait_for()
 await page.evaluate('sessionStorage.setItem("mawa-db", JSON.stringify(__fixture))')
 await page.goto('http://127.0.0.1:8765/?view=review')
 await page.locator('[data-review-session="147"] > summary').click()
 await page.get_by_text('Your recorded self-assessment').wait_for()
 assert 'Result 0/3' in await page.locator('.saved-investigation').inner_text()
 await page.get_by_text('Open worked investigation solution').click()
 assert '73 + 37 = 110' in await page.locator('[data-adult-review]').inner_text()
 form=page.locator('.adult-review')
 await form.locator('[name=reviewer]').fill('Fixture reviewer')
 for key,value in [('result','1'),('method','2'),('proof','1'),('clarity','1')]:
  await form.locator('[name='+key+']').select_option(value)
 await form.locator('[name=notes]').fill('Recheck the final digit against the sum.')
 await form.get_by_role('button').click()
 await page.get_by_text('Fixture reviewer · parent').wait_for()
 assert await page.evaluate('__fixture.investigation_reviews.length===1 && __fixture.session_records[0].summary.rubric.result===0')
 assert await page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
 await ctx.close()


async def main():
 async with async_playwright() as p:
  browser=await p.chromium.launch(headless=True,executable_path=shutil.which('google-chrome') or shutil.which('chromium'),args=['--no-sandbox'])
  await verify_mawa_visits(browser)
  await verify_course_restart(browser)
  await verify_revised_lessons(browser)
  await verify_later_lessons(browser)
  ctx=await browser.new_context(viewport={'width':390,'height':844},service_workers='block')
  # Feed the historical fixture its original lesson edition. Later lessons still
  # use this renderer; the separate S094 case also checks its live manifest route.
  await ctx.route('**/data/read-watch-practise.json*',lambda route:route.fulfill(json={'lessons':[]}))
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

  await page.screenshot(path=str(SCREENSHOTS/'focus-learning-home-iphone.png'))
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
  await page.screenshot(path=str(SCREENSHOTS/'lesson-menu-iphone.png'))
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
  # Public CI exercises every prompt and figure. Private release QA also renders each worked solution.
  private_source=os.environ.get('SUMMIT_ONE_LESSON_SOLUTIONS')
  import json
  import subprocess
  import tempfile
  with tempfile.TemporaryDirectory() as tmp:
   subprocess.run(['python', '-c',
    'import sys; from pathlib import Path; sys.path.insert(0, "tools/content"); '
    'from audit_all_lessons import map_course; from build_original_lessons import build; '
    'build(map_course(), Path(sys.argv[1]), public_only=(sys.argv[2]=="public"))',
    tmp, 'private' if private_source else 'public'], cwd=ROOT, check=True)
   filename='original-problems.json' if private_source else 'lesson-prompts.json'
   authored=json.loads((Path(tmp)/filename).read_text())
  layout_rows=[{key:r.get(key,'') for key in ('id','title','prompt','solution_text')} for r in authored]
  for width in (320,390):
   await page.set_viewport_size({'width':width,'height':844})
   report=await page.evaluate("""async rows=>{
    const {originalFigure}=await import('./original-learning.js?v=upper-primary-audit-20261114');
    const {typesetMath}=await import('./math-typography.js?v=advanced-20261113');
    const {items}=await (await fetch('data/lesson-challenges.json')).json();
    const entries=new Map(items.map(m=>[m.id,m]));
    const stage=document.querySelector('.lesson-screen-stage');
    const template=document.querySelector('#problemTemplate').content.firstElementChild;
    const card=template.cloneNode(true);
    const title=card.querySelector('.problem-title');
    const prompt=card.querySelector('.problem-prompt');
    const solution=card.querySelector('.solution-panel');
    const worked=document.createElement('p');
    worked.className='math-copy';
    solution.append(worked);
    solution.hidden=false;
    stage.append(card);
    const errors=[],counts={cards:0,figures:0,tables:0};
    for(const row of rows){
      const learning=entries.get(row.id);
      if(!learning){errors.push([row.id,'missing manifest entry']);continue;}
      title.textContent=row.title;
      prompt.textContent=row.prompt;
      worked.textContent=row.solution_text;
      solution.hidden=!row.solution_text;
      const html=originalFigure({...row,learning});
      const expectsFigure=Boolean(learning.spatialDiagram||learning.dataDisplay||
        learning.geometryDiagram||learning.cuboidDiagram||learning.pictogram);
      prompt.insertAdjacentHTML('beforebegin',html);
      typesetMath(card);
      counts.cards++;
      for(const el of [card,title,prompt,solution,worked]){
        if(el.scrollWidth>el.clientWidth+2)errors.push([row.id,'horizontal overflow',el.className,el.scrollWidth-el.clientWidth]);
      }
      const figure=card.querySelector('[data-lesson-figure]');
      if(Boolean(figure)!==expectsFigure)errors.push([row.id,'missing figure']);
      if(figure){
        counts.figures++;
        const stale=originalFigure({prompt:'An earlier question.',learning});
        const display=figure.querySelector('table,svg');
        if(stale||display.clientWidth>card.clientWidth||figure.scrollWidth>figure.clientWidth+2)
          errors.push([row.id,'figure overflow or mismatched stem']);
        if(display.localName==='svg'){
          const labels=[...display.querySelectorAll('text')];
          const width=display.getBoundingClientRect().width,view=display.viewBox.baseVal;
          const bounds=labels.map(t=>t.getBBox());
          const boxFits=b=>b.x>=0&&b.y>=0&&b.x+b.width<=view.width+1&&b.y+b.height<=view.height+1;
          const overlaps=(a,b)=>a.x+1<b.x+b.width&&a.x+a.width>b.x+1&&a.y+1<b.y+b.height&&a.y+a.height>b.y+1;
          for(const [index,box] of bounds.entries()){
            const font=Number.parseFloat(getComputedStyle(labels[index]).fontSize);
            if(!boxFits(box)||bounds.slice(index+1).some(other=>overlaps(box,other)))
              errors.push([row.id,'clipped or overlapping label',labels[index].textContent]);
            if(width/view.width*font < 11)errors.push([row.id,'small diagram label',labels[index].textContent,width/view.width*font]);
          }
          if(width<180)errors.push([row.id,'narrow diagram',width]);
        }else{
          counts.tables++;
        }
        figure.remove();
      }
    }
    card.remove();
    return {errors,counts};
   }""",layout_rows)
   counts=report['counts']
   assert counts['cards']==566 and counts['figures']>=100 and counts['tables']>=8,counts
   assert not report['errors'],(width,report['errors'])
   scope='prompts and worked solutions' if private_source else 'prompts'
   print(f"Lesson layouts at {width}px: {counts['cards']} {scope}; {counts['figures']} figures and displays",flush=True)
  await page.set_viewport_size({'width':390,'height':844})
  # Run one spatial question through the real lesson screen and solution reveal.
  authored_mock=MOCK.replace("function query(table)", "const authored="+json.dumps(layout_rows)+";"+
   "for(const row of problems)Object.assign(row,authored.find(a=>a.id===row.id));function query(table)")
  authored_mock=authored_mock.replace("{solution_text:'Six plus six is twelve.'}",
   "{solution_text:authored.find(a=>a.id===body.problem_id)?.solution_text||'Fixture worked solution. Final answer: 42'}")
  spatial_ctx=await browser.new_context(viewport={'width':390,'height':844},service_workers='block')
  await spatial_ctx.route('**/data/read-watch-practise-later.json*',lambda route:route.fulfill(json={'lessons':[]}))
  await spatial_ctx.add_init_script("""window.fixture={records:[{session_number:94,answers:{},working:{},
   evidence:{'guided:SPATIAL-02':{},'retrieval:SPATIAL-02':{}},summary:{lesson_stage:3,lesson_panel:5}}],
   attempts:[],exams:[],progress:{completed_sessions:93,current_session:94,xp:0,rank:0,state:{}},writes:[],fail:false}""")
  await spatial_ctx.route('**/supabase-client.js*',lambda route:route.fulfill(content_type='application/javascript',body=authored_mock))
  spatial_page=await spatial_ctx.new_page()
  await spatial_page.goto('http://127.0.0.1:8765/')
  await spatial_page.locator('#continue').click()
  spatial_card=spatial_page.locator('.lesson-problem-unit')
  await spatial_card.locator('svg').wait_for()
  assert 'missing grid segment' in (await spatial_card.locator('.problem-title').inner_text()).lower()
  await spatial_page.locator('[data-screen-next]').click()
  await spatial_card.locator('.final-answer-input').fill('42')
  await spatial_card.locator('.submit-answer').click()
  await spatial_card.locator('.submit-answer').wait_for(state='hidden')
  await spatial_page.locator('[data-screen-next]').click()
  await spatial_card.locator('.reveal-solution').click()
  await spatial_card.get_by_text('Read full worked solution').click()
  assert await spatial_card.locator('svg').first.is_visible()
  assert 'Final answer: 42' in await spatial_card.locator('.solution-panel details[open] p').text_content()
  assert await spatial_page.evaluate('document.documentElement.scrollWidth <= innerWidth+2')
  await spatial_page.locator('.lesson-screen-stage').evaluate('(stage)=>stage.scrollTop=0')
  await spatial_page.screenshot(path=str(SCREENSHOTS/'spatial-solution-iphone.png'))
  await spatial_ctx.close()

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
  await page.screenshot(path=str(SCREENSHOTS/'math-inline-baseline-iphone.png'))
  await page.locator('#math-baseline-probe').evaluate('(node)=>node.remove()')

  assert await page.locator('#openingVideo').count()==1
  assert 'S001-Intro.mp4' in await page.locator('#openingVideo').get_attribute('src')
  assert 'Video' in await page.locator('.lesson-stage-track .here').inner_text()
  await fits()
  await scroll_probe()  # Taller-than-screen lesson content must scroll; Back/Next stays fixed.
  await page.screenshot(path=str(SCREENSHOTS/'video-first-session-1-iphone.png'))
  await next_page()
  assert 'Remember' in await page.locator('.lesson-stage-track .here').inner_text()
  await fits()
  await next_page()
  await page.locator('#retrievalChecks').wait_for()
  await next_page()
  assert 'Discover' in await page.locator('.lesson-stage-track .here').inner_text()
  await until_visible('.flash-quiz')
  await fits()
  await page.screenshot(path=str(SCREENSHOTS/'lesson-flash-iphone.png'))
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
  await next_page()
  # The optional advanced panel must teach something immediately — no empty
  # accordion, new answer fields, progress write, or new advancement guard.
  await page.locator('.advanced-path-header h3').wait_for()
  assert 'remainder' in (await page.locator('.advanced-path-header h3').inner_text()).lower()
  assert await page.locator('.advanced-solution-steps li').count()==3
  assert await page.locator('.advanced-path input,.advanced-path textarea,.advanced-path form').count()==0
  assert 'not assessed' in (await page.locator('.advanced-path-disclaimer').inner_text()).lower()
  assert 'Where this maths can lead' in await page.locator('.lesson-screen-progress').inner_text()
  await fits()
  await scroll_probe()
  await page.screenshot(path=str(SCREENSHOTS/'advanced-connection-iphone.png'))
  await page.locator('.advanced-path-curiosity summary').click()
  assert await page.locator('.advanced-path-curiosity-body').is_visible()
  # The enrichment screen intentionally contains no video or further-reading
  # accordion; opening and completed-lesson video replay remain elsewhere.
  assert await page.locator('.advanced-media,.advanced-path .lesson-player-slot').count()==0
  assert await page.locator('.advanced-path-header h3').is_visible()
  await next_page()
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
  await page.screenshot(path=str(SCREENSHOTS/'transfer-label-iphone.png'))
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
  await page.screenshot(path=str(SCREENSHOTS/'lesson-final-iphone.png'))
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
  await page.screenshot(path=str(SCREENSHOTS/'completed-lesson-intro-iphone.png'))
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
  await page.screenshot(path=str(SCREENSHOTS/'video-first-session-2-iphone.png'))
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
  await page.screenshot(path=str(SCREENSHOTS/'video-first-session-2-desktop.png'))
  await page.locator('[data-screen-back]').click()
  await page.locator('#continue').wait_for()
  assert not errors,errors
  await browser.close()
 print('PASS: responsive scrolling lessons with fixed navigation, six answer-only practice problems, read-only replay, and immutable completion.')
if __name__=='__main__':
 asyncio.run(main())
