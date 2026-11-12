import asyncio,json,shutil
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[1]
MOCK=r'''
const state=window.fixture=window.fixture||{records:[],attempts:[],exams:[],progress:{completed_sessions:0,current_session:1,xp:0,rank:0,state:{}},writes:[],fail:false};
const mapping=(await (await fetch('data/lesson-challenges.json')).json()).items;
const problems=[{id:'A001',title:'Must never be selected',prompt:'A real exam fixture',source_type:'authentic_amc',category:'digits',difficulty:2},...mapping.map(m=>({id:m.id,title:'Original learning fixture',prompt:'What is 6 plus 6?',source_type:'original_authored',category:m.skill,difficulty:3}))];
function query(table){let filters=[],payload=null,kind='read',single=false;
const q={select(){return q},eq(k,v){filters.push([k,v]);return q},not(){return q},order(){return q},limit(){return q},maybeSingle(){single=true;return q},single(){single=true;return q},insert(v){payload=v;kind='insert';return q},update(v){payload=v;kind='update';return q},upsert(v){payload=v;kind='upsert';return q},then(resolve,reject){try{let rows=table==='content_problems_student'?problems:table==='session_records'?state.records:table==='problem_attempts'?state.attempts:table==='exam_sittings'?state.exams:table==='exam_catalog'?[{id:'amc-up-2025',year:2025,session_slot:16,title:'Fixture paper',max_score:135,duration_minutes:60,question_count:30,source_type:'authentic_amc_past_paper',active:true}]:table==='exam_questions_student'?Array.from({length:30},(_,i)=>({exam_id:'amc-up-2025',question_number:i+1,question_type:i<25?'multiple_choice':'integer',stem:'Fixture question '+(i+1),choices:['one','two','three','four','five'],marks:i<10?3:i<20?4:i<25?5:i-19})):[];
 if(kind!=='read'){if(state.fail)return resolve({error:{message:'Simulated connection failure'}});if(kind==='insert'){payload={id:'sitting1',...payload};rows.push(payload)}else{const found=rows.find(r=>filters.every(([k,v])=>r[k]===v));if(found)Object.assign(found,payload);payload=found||payload}return resolve({data:payload,error:null})}
 rows=rows.filter(r=>filters.every(([k,v])=>k==='user_id'||r[k]===v));resolve({data:single?rows[0]||null:rows,error:null})}catch(e){reject(e)}}};return q}
export const supabase={from:query,auth:{getSession:async()=>({data:{session:{access_token:'fixture'}}})},functions:{invoke:async(name,{body})=>({data:name==='submit-problem-attempt'?{correct:true,independent_credit:!body.used_help&&!body.familiar_family}:{solution_text:'Six plus six is twelve.'},error:null})}};
export async function currentUser(){return {id:'fixture-user'}};
export async function loadProgress(){return state.progress};
export async function saveProgress(p){Object.assign(state.progress,p);return state.progress};
export async function signOut(){};
export async function upsertSession(p){if(state.fail)throw Error('Simulated connection failure');const row=structuredClone(p);state.writes.push(row);const ix=state.records.findIndex(r=>r.session_number===p.session_number);if(ix<0)state.records.push(row);else state.records[ix]=row;return row};
'''
async def main():
 async with async_playwright() as p:
  browser=await p.chromium.launch(headless=True,executable_path=shutil.which('google-chrome'),args=['--no-sandbox'])
  context=await browser.new_context(viewport={'width':1280,'height':900},service_workers='block')
  await context.route('**/supabase-client.js*',lambda route:route.fulfill(content_type='application/javascript',body=MOCK))
  page=await context.new_page();errors=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.on('dialog',lambda d:d.accept())
  await page.goto('http://127.0.0.1:8765/');await page.locator('#continue').wait_for()
  await page.locator('#continue').click();await page.locator('.session-intro').wait_for();assert 'Why and when this helps' in await page.locator('.session-intro').inner_text();await page.set_viewport_size({'width':390,'height':844});await page.screenshot(path=str(ROOT/'docs/session-intro-mobile.png'),full_page=True);await page.set_viewport_size({'width':1280,'height':900});await page.locator('[data-stage="1"]').click();assert await page.locator('.worked-example').count()==2
  await page.locator('.mini-check .hint').click();await page.wait_for_timeout(100)
  assert await page.evaluate("Object.values(fixture.records[0].evidence).includes(true)")
  await page.locator('.mini-check input').fill('123');await page.locator('.mini-check button.primary').click();await page.locator('.check-feedback').get_by_text('Not quite yet',exact=False).wait_for()
  await page.locator('[data-stage="2"]').click();assert not await page.locator('.problem-card').is_visible();await page.locator('.mini-check input').fill('4');await page.locator('.mini-check button.primary').click();await page.locator('.problem-card').wait_for();await page.locator('.working-box').fill('My reasoning survives changing stages.')
  await page.locator('[data-stage="3"]').click();await page.locator('[data-stage="2"]').click()
  assert await page.locator('.working-box').input_value()=='My reasoning survives changing stages.'
  assert 'AMC ARCHIVE' not in await page.locator('.problem-meta').inner_text()
  await page.locator('.problem-card .answer-box:not(.working-box)').fill('12');await page.locator('.submit-answer').click()
  assert 'record the clue' in await page.locator('.attempt-feedback').inner_text()
  await page.locator('[data-reason="clue"]').fill('The useful clue is a remainder.')
  await page.locator('[data-reason="plan"]').fill('I will find the remainder and check the requested amount.')
  await page.locator('.submit-answer').click();await page.locator('.submit-answer').wait_for(state='hidden')
  assert await page.evaluate("fixture.records[0].summary.problems.every(id=>/^O/.test(id))")
  await page.locator('[data-stage="3"]').click()
  await page.locator('[data-reason="clue"]').fill('The change preserves the remainder class.')
  await page.locator('[data-reason="plan"]').fill('I will represent the unknown by a multiple plus its remainder.')
  await page.locator('.method-hint').click()
  await page.locator('.problem-card .answer-box:not(.working-box)').fill('12');await page.locator('.submit-answer').click();await page.locator('.submit-answer').wait_for(state='hidden')
  assert 'Solved with support' in await page.locator('.attempt-feedback').inner_text()
  await page.set_viewport_size({'width':390,'height':844});await page.screenshot(path=str(ROOT/'docs/original-transfer-mobile.png'),full_page=True)
  assert await page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
  await page.locator('[data-stage="4"]').click()
  await page.locator('#takeaway').fill('Look for the structure, not just matching words.')
  await page.locator('#watch').fill('Check the required quantity and all constraints.')
  await page.locator('#completeSession').click()
  assert await page.locator('#completeSession').count()==1
  for field in await page.locator('[data-final-check]').all():await field.fill('I substituted the result into the original conditions and checked every part.')
  await page.locator('#transferConfidence').select_option('practice')
  await page.screenshot(path=str(ROOT/'docs/original-check-mobile.png'),full_page=True)
  await page.set_viewport_size({'width':1280,'height':900})
  await page.locator('[data-stage="4"]').click();assert await page.locator('.mini-check').count()==0;await page.locator('[data-stage="1"]').click()
  assert await page.evaluate("Object.values(fixture.records[0].evidence).find(e=>e.kind==='guided').independent===false")
  await page.evaluate('window.scrollTo(0,0)');await page.screenshot(path=str(ROOT/'docs/teaching-desktop.png'),full_page=True)
  await page.set_viewport_size({'width':390,'height':844});await page.screenshot(path=str(ROOT/'docs/teaching-mobile.png'),full_page=True)
  assert await page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
  await page.goto('http://127.0.0.1:8765/tests.html');await page.locator('.startExam').first.click()
  await page.locator('#firstQuestion').wait_for()
  assert await page.locator('.exam-summary tbody tr').count()==30
  assert '0 answered · 30 not answered' in await page.locator('.answer-count').inner_text()
  await page.locator('#firstQuestion').click();await page.locator('[data-choice="B"]').click()
  assert await page.evaluate("fixture.exams[0].responses['1']==='B'")
  await page.evaluate('fixture.fail=true');await page.locator('[data-choice="C"]').click()
  assert await page.locator('[data-choice="B"]').get_attribute('aria-pressed')=='true'
  await page.evaluate('fixture.fail=false');await page.locator('#eraseAnswer').click()
  assert await page.evaluate("fixture.exams[0].responses['1']===undefined")
  await page.locator('[data-choice="A"]').click()
  async def go_question(index):
   if await page.locator('#menuToggle').is_visible():await page.locator('#menuToggle').click()
   await page.locator('#questionMenu [data-q="'+str(index)+'"]').click()
  await go_question(25);await page.locator('#integerInput').fill('12');await page.locator('#saveInteger').click()
  await page.get_by_text('Saved',exact=True).wait_for()
  assert await page.evaluate("fixture.exams[0].responses['26']==='12'")
  await page.locator('#integerInput').fill('13');await go_question(26);await go_question(25)
  assert await page.locator('#saveState').inner_text()=='Not saved'
  assert await page.evaluate("fixture.exams[0].responses['26']==='12'")
  await page.screenshot(path=str(ROOT/'docs/exam-mobile.png'),full_page=True)
  assert await page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
  await page.locator('#eraseAnswer').click()
  assert await page.evaluate("fixture.exams[0].responses['26']===undefined")
  assert await page.locator('#integerInput').input_value()==''
  await page.locator('#integerInput').fill('14');await page.locator('#saveInteger').click();await page.get_by_text('Saved',exact=True).wait_for()
  await page.locator('#integerInput').fill('15')
  await page.set_viewport_size({'width':1280,'height':900});await page.screenshot(path=str(ROOT/'docs/exam-desktop.png'),full_page=True)
  await go_question(29);await page.locator('#next').click();await page.locator('#firstQuestion').wait_for()
  assert '2 answered · 28 not answered' in await page.locator('.answer-count').inner_text()
  await page.locator('#endParticipation').click();await page.locator('#confirmFinish').wait_for()
  assert 'Unsaved integer answers: 26' in await page.locator('.end-confirm').inner_text()
  assert 'Correct' not in await page.locator('.exam-summary').inner_text()
  await page.screenshot(path=str(ROOT/'docs/exam-confirmation.png'),full_page=True)
  await page.locator('#cancelFinish').click();await page.locator('#firstQuestion').wait_for()
  assert await page.evaluate('fixture.exams[0].completed===false')
  rows=[{'question_number':n,'stem':'Fixture question '+str(n),'correct':n==1,'response':'A' if n==1 else '14' if n==26 else None,'correct_answer':'A' if n<=25 else '12','earned':3 if n==1 else 0,'marks':3 if n<=10 else 4 if n<=20 else 5 if n<=25 else n-20,'explanation':'A complete fixture explanation.' if n in [1,17] else None} for n in range(1,31)]
  await context.route('**/functions/v1/grade-exam',lambda r:r.fulfill(content_type='application/json',body=json.dumps({'score':3,'max_score':135,'rows':rows,'award':{'label':'Practice estimate','estimated':True}})))
  await page.locator('#endParticipation').click();await page.locator('#confirmFinish').click()
  await page.locator('.score-big').wait_for()
  assert await page.locator('.question-review').count()==30
  assert await page.locator('.result-table').nth(1).locator('tbody tr').count()==30
  assert await page.locator('.result-table').nth(1).get_by_text('Not answered',exact=True).count()==28
  await page.locator('[data-solution="17"]').click()
  assert await page.locator('#solution-17').get_attribute('open') is not None
  assert 'watch-amc-2025-q17.html' in await page.locator('#solution-17 .solution-video-link').get_attribute('href')
  await page.evaluate('window.scrollTo(0,0)');await page.screenshot(path=str(ROOT/'docs/exam-results.png'),full_page=True)
  await page.set_viewport_size({'width':390,'height':844})
  assert await page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
  assert not errors,errors
  print('PASS: lesson navigation and saved work; exam overview, question menu, Previous/Next, save rollback, Erase, explicit integer Save, unsaved drafts, final confirmation and result/solution/video links; responsive without browser errors.')

  # All session types get an opening, including investigation and timed rehearsal.
  for completed in [6,15,360]:
   special=await browser.new_context(viewport={'width':390,'height':844},service_workers='block')
   await special.route('**/supabase-client.js*',lambda route:route.fulfill(content_type='application/javascript',body=MOCK))
   await special.add_init_script("window.fixture={records:[],attempts:[],exams:[],progress:{completed_sessions:"+str(completed)+",xp:0,rank:0,state:{}},writes:[],fail:false}")
   sp=await special.new_page();await sp.goto('http://127.0.0.1:8765/');await sp.locator('#continue').click()
   await sp.locator('.session-intro').wait_for()
   assert await sp.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
   if completed in [6,360]:
    await sp.locator('[data-stage="1"]').click();await sp.locator('.gentle-example').first.wait_for()
   else: await sp.locator('#startCourseExam').wait_for()
   await special.close()
  legacy=await browser.new_context(service_workers='block')
  await legacy.route('**/supabase-client.js*',lambda route:route.fulfill(content_type='application/javascript',body=MOCK))
  await legacy.add_init_script("window.fixture={records:[{session_number:1,answers:{A001:{response:'old answer'}},working:{A001:'Preserve my old working'},evidence:{},summary:{problems:['A001']}}],attempts:[],exams:[],progress:{completed_sessions:0,xp:0,rank:0,state:{}},writes:[],fail:false}")
  lp=await legacy.new_page();await lp.goto('http://127.0.0.1:8765/');await lp.locator('#continue').click();await lp.locator('.session-intro').wait_for()
  assert await lp.evaluate("fixture.records[0].working.A001==='Preserve my old working' && fixture.records[0].summary.previous_problem_ids.includes('A001') && fixture.records[0].summary.problems.every(id=>id.startsWith('O'))")
  await legacy.close()
  print('PASS: original-only selection, clue/plan gate, support tracking, check/reflection gate and legacy draft work preservation.')
  # Exercise the REAL shared currentUser and login modules with a simulated SDK.
  auth_context=await browser.new_context(service_workers='block')
  sdk="""export function createClient(){return {auth:{
    getUser:async()=>sessionStorage.getItem('auth-fixture')?{data:{user:{id:'fixture'}}}:{data:{user:null},error:{name:'AuthSessionMissingError',message:'Auth session missing!'}},
    signInWithPassword:async()=>{sessionStorage.setItem('auth-fixture','1');return {error:null}}
  },from:()=>{throw Error('End of authenticated fixture')}}}"""
  await auth_context.route('https://esm.sh/**',lambda r:r.fulfill(content_type='application/javascript',body=sdk))
  auth_page=await auth_context.new_page()
  await auth_page.goto('http://127.0.0.1:8765/tests.html?course=1&slot=7')
  await auth_page.wait_for_url('**/login.html?next=*')
  assert await auth_page.locator('#subtitle').inner_text()=='Sign in to open the AMC Test Centre.'
  await auth_page.locator('#loginName').fill('fixture')
  await auth_page.locator('#password').fill('fixture')
  await auth_page.locator('#signIn').click()
  await auth_page.wait_for_url('**/tests.html?course=1&slot=7')
  await auth_page.evaluate('sessionStorage.clear()')
  await auth_page.goto('http://127.0.0.1:8765/')
  await auth_page.wait_for_url('**/login.html')
  print('PASS: real shared auth handles signed-out Mission and Test Centre; login returns to original exam URL.')
  await browser.close()
asyncio.run(main())
