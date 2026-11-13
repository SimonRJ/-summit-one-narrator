"""Video-first one-viewport lesson regression on iPhone and desktop.
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
    return {body:getComputedStyle(document.body).overflow,windowScroll:document.documentElement.scrollHeight-innerHeight,
       horizontal:document.documentElement.scrollWidth-innerWidth,stageOverflow:stage?stage.scrollHeight-stage.clientHeight:999};
   }""")
   assert result['body']=='hidden',result
   assert result['windowScroll']<=4 and result['horizontal']<=4,result
   assert result['stageOverflow']<=5,result
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
  assert (await page.locator('#navProgress').inner_text()).strip()=='0 / 372'
  assert await page.evaluate("document.documentElement.scrollHeight<=innerHeight+4 && document.documentElement.scrollWidth<=innerWidth+4"), 'Learning home must fit on the iPhone without scrolling'
  await page.screenshot(path=str(ROOT/'docs/focus-learning-home-iphone.png'))
  await page.locator('[data-view="profile"]').click()
  await page.get_by_role('heading',name='Summit progress').wait_for()
  assert await page.get_by_text('sessions remaining').count()==1
  await page.locator('.profile-upcoming summary').click()
  assert await page.get_by_text('Next strategy workshop').count()==1
  assert await page.get_by_text('Next MAWA investigation').count()==1
  await page.locator('[data-view="home"]').click()
  await page.locator('#continue').wait_for()
  await page.locator('#navMore summary').click()
  await page.get_by_role('button',name='Completed sessions').click()
  await page.get_by_role('heading',name='Completed sessions').wait_for()
  assert not await page.locator('#navMore').evaluate('(node)=>node.open')
  await page.locator('[data-view="home"]').click()
  await page.locator('#continue').wait_for()
  await page.locator('#continue').click()
  await page.locator('.opening-film').wait_for()
  assert await page.locator('#openingVideo').count()==1
  assert 'S001-Intro.mp4' in await page.locator('#openingVideo').get_attribute('src')
  assert 'Video' in await page.locator('.lesson-stage-track .here').inner_text()
  await fits()
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
  await next_page()
  await page.locator('#guidedCheck .mini-check').wait_for()
  await page.locator('#guidedCheck .short-answer').fill('123')
  await page.locator('#guidedCheck button.primary').click()
  await next_page();await next_page()
  assert 'Try' in await page.locator('.lesson-stage-track .here').inner_text()
  await page.locator('.lesson-fade-unit .method').fill('Keep the remainder, check it, then explain every step clearly.')
  val=await page.evaluate("import('./transfer-practice.js?v=recognition-20261113').then(m=>String(m.practice('DIV-03',9).value))")
  await page.locator('.lesson-fade-unit .response').fill(val)
  await page.locator('.lesson-fade-unit').get_by_role('button',name='Record and check').click()
  await next_page()
  await page.locator('.lesson-prep-unit .short-answer').fill('4')
  await page.locator('.lesson-prep-unit button.primary').click()
  await page.locator('.lesson-problem-unit .problem-prompt').wait_for(state='visible')
  assert 'Read your new problem' in await page.locator('.lesson-screen-progress').inner_text()
  await next_page()
  await page.locator('[data-reason="clue"]').fill('This problem uses a remainder to capture the repeating structure.')
  await next_page()
  await page.locator('[data-reason="plan"]').fill('I will calculate a remainder and check the original question.')
  await next_page()
  await page.locator('.lesson-problem-unit .working-box').fill('I wrote clear mathematical working in my notebook.')
  await page.locator('.lesson-problem-unit .answer-box:not(.working-box)').fill('12')
  await page.locator('.lesson-problem-unit .submit-answer').click()
  await page.locator('.lesson-problem-unit .submit-answer').wait_for(state='hidden')
  await fits()
  await page.locator('[data-screen-back]').click()
  await page.locator('[data-screen-next]').click()
  assert await page.locator('.lesson-problem-unit .answer-box:not(.working-box)').input_value()=='12'
  await next_page()
  await next_page()
  assert 'Transfer' in await page.locator('.lesson-stage-track .here').inner_text()
  await next_page()
  await page.locator('[data-reason="clue"]').fill('The change is governed by the same remainder structure.')
  await next_page()
  await page.locator('[data-reason="plan"]').fill('I will use a quotient and remainder, then substitute.')
  await next_page()
  await page.locator('.lesson-problem-unit .answer-box:not(.working-box)').fill('12')
  await page.locator('.lesson-problem-unit .submit-answer').click()
  await page.locator('.lesson-problem-unit .submit-answer').wait_for(state='hidden')
  await next_page()
  await next_page()
  assert 'Check' in await page.locator('.lesson-stage-track .here').inner_text()
  await page.locator('#takeaway').fill('The invariant is the remainder, not the total quotient.')
  await next_page();await page.locator('#watch').fill('Check each original condition at the end.')
  await next_page()
  for k in range(2):
   await page.locator('[data-final-check]').nth(k).fill('I substituted back and checked all the possible cases.')
   await next_page()
  await page.locator('#transferConfidence').select_option('practice')
  await fits()
  await page.screenshot(path=str(ROOT/'docs/lesson-final-iphone.png'))
  await next_page()
  await page.locator('#continue').wait_for()
  assert await page.evaluate('fixture.records[0].immutable===true && fixture.progress.completed_sessions===1')
  await page.locator('#continue').click()
  assert 'S002-Intro.mp4' in await page.locator('#openingVideo').get_attribute('src')
  await fits()
  await page.screenshot(path=str(ROOT/'docs/video-first-session-2-iphone.png'))
  await page.set_viewport_size({'width':1280,'height':900})
  await fits()
  await page.screenshot(path=str(ROOT/'docs/video-first-session-2-desktop.png'))
  await page.locator('[data-screen-back]').click()
  await page.locator('#continue').wait_for()
  assert not errors,errors
  await browser.close()
 print('PASS: no-scroll video-first lessons 1 & 2, single-screen Back/Next, saved answers, flash practice, and course completion.')
asyncio.run(main())
