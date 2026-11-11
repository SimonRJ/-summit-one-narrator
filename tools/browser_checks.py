import asyncio,json,shutil
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[1]
MOCK=r'''
const state=window.fixture=window.fixture||{records:[],attempts:[],exams:[],progress:{completed_sessions:0,current_session:1,xp:0,rank:0,state:{}},writes:[],fail:false};
const problems=[{id:'TEST1',title:'A test problem',prompt:'What is 6 plus 6?',source_type:'original',category:'digits',difficulty:2},{id:'TEST2',title:'A transfer problem',prompt:'What is 3 times 4?',source_type:'original',category:'digits',difficulty:2}];
function query(table){let filters=[],payload=null,kind='read',single=false;
const q={select(){return q},eq(k,v){filters.push([k,v]);return q},not(){return q},order(){return q},limit(){return q},maybeSingle(){single=true;return q},single(){single=true;return q},insert(v){payload=v;kind='insert';return q},update(v){payload=v;kind='update';return q},upsert(v){payload=v;kind='upsert';return q},then(resolve,reject){try{let rows=table==='content_problems_student'?problems:table==='session_records'?state.records:table==='problem_attempts'?state.attempts:table==='exam_sittings'?state.exams:table==='exam_catalog'?[{id:'fixture-paper',year:2025,session_slot:16,title:'Fixture paper',max_score:135,duration_minutes:60,question_count:30,source_type:'authentic_amc_past_paper',active:true}]:table==='exam_questions_student'?Array.from({length:30},(_,i)=>({exam_id:'fixture-paper',question_number:i+1,question_type:i<25?'multiple_choice':'integer',stem:'Fixture question '+(i+1),choices:['one','two','three','four','five'],marks:i<10?3:i<20?4:i<25?5:i-19})):[];
 if(kind!=='read'){if(state.fail)return resolve({error:{message:'Simulated connection failure'}});if(kind==='insert'){payload={id:'sitting1',...payload};rows.push(payload)}else{const found=rows.find(r=>filters.every(([k,v])=>r[k]===v));if(found)Object.assign(found,payload);payload=found||payload}return resolve({data:payload,error:null})}
 rows=rows.filter(r=>filters.every(([k,v])=>k==='user_id'||r[k]===v));resolve({data:single?rows[0]||null:rows,error:null})}catch(e){reject(e)}}};return q}
export const supabase={from:query,auth:{getSession:async()=>({data:{session:{access_token:'fixture'}}})},functions:{invoke:async(name,{body})=>({data:name==='submit-problem-attempt'?{correct:true,independent_credit:true}:{solution_text:'Six plus six is twelve.'},error:null})}};
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
  await page.locator('[data-stage="2"]').click();assert not await page.locator('.problem-card').is_visible();await page.locator('.mini-check input').fill('1');await page.locator('.mini-check button.primary').click();await page.locator('.problem-card').wait_for();await page.locator('.working-box').fill('My reasoning survives changing stages.')
  await page.locator('[data-stage="3"]').click();await page.locator('[data-stage="2"]').click()
  assert await page.locator('.working-box').input_value()=='My reasoning survives changing stages.'
  await page.locator('.problem-card .answer-box:not(.working-box)').fill('12');await page.locator('.submit-answer').click();await page.locator('.submit-answer').wait_for(state='hidden')
  await page.locator('[data-stage="4"]').click();assert await page.locator('.mini-check').count()==0;await page.locator('[data-stage="1"]').click()
  assert await page.evaluate("Object.values(fixture.records[0].evidence).find(e=>e.kind==='guided').independent===false")
  await page.evaluate('window.scrollTo(0,0)');await page.screenshot(path=str(ROOT/'docs/teaching-desktop.png'),full_page=True)
  await page.set_viewport_size({'width':390,'height':844});await page.screenshot(path=str(ROOT/'docs/teaching-mobile.png'),full_page=True)
  assert await page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
  await page.goto('http://127.0.0.1:8765/tests.html');await page.locator('.startExam').first.click();await page.locator('[data-choice="B"]').click()
  assert await page.evaluate("fixture.exams[0].responses['1']==='B'")
  await page.evaluate('fixture.fail=true');await page.locator('[data-choice="C"]').click()
  assert await page.locator('[data-choice="B"]').get_attribute('class')=='choice selected'
  await page.evaluate('fixture.fail=false');await page.locator('[data-q="25"]').click();await page.locator('#integerInput').fill('12');await page.locator('#saveInteger').click();await page.locator('#saveState').wait_for()
  assert await page.evaluate("fixture.exams[0].responses['26']==='12'")
  await page.locator('#integerInput').fill('13');await page.locator('[data-q="26"]').click();await page.locator('[data-q="25"]').click();assert await page.locator('#saveState').inner_text()=='Not saved'
  await page.screenshot(path=str(ROOT/'docs/exam-mobile.png'),full_page=True)
  assert not errors,errors
  print('PASS: desktop/mobile lesson navigation, hint persistence, working save, strict practice evidence, exam save failure rollback, unsaved integer status; no browser errors.')

  # All session types get an opening, including investigation and timed rehearsal.
  for completed in [6,15,360]:
   special=await browser.new_context(viewport={'width':390,'height':844},service_workers='block')
   await special.route('**/supabase-client.js*',lambda route:route.fulfill(content_type='application/javascript',body=MOCK))
   await special.add_init_script("window.fixture={records:[],attempts:[],exams:[],progress:{completed_sessions:"+str(completed)+",xp:0,rank:0,state:{}},writes:[],fail:false}")
   sp=await special.new_page();await sp.goto('http://127.0.0.1:8765/');await sp.locator('#continue').click()
   await sp.locator('.session-intro').wait_for()
   assert await sp.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
   if completed in [6,360]:
    await sp.locator('[data-stage="1"]').click();await sp.locator('.gentle-example').wait_for()
   else: await sp.locator('#startCourseExam').wait_for()
   await special.close()
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
