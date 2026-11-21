import {chromium} from 'playwright';
import fs from 'node:fs';import path from 'node:path';import http from 'node:http';import assert from 'node:assert/strict';
const root=process.cwd();fs.mkdirSync('qa-screenshots',{recursive:true});
const mimeTypes={'.js':'application/javascript','.css':'text/css','.json':'application/json','.svg':'image/svg+xml','.jpg':'image/jpeg','.png':'image/png','.mp4':'video/mp4'};
const server=http.createServer((req,res)=>{let name=decodeURIComponent(new URL(req.url,'http://localhost').pathname);if(name==='/')name='/index.html';const file=path.resolve(root,'.'+name);if(!file.startsWith(root+path.sep)){res.writeHead(403);res.end();return}try{res.setHeader('Content-Type',mimeTypes[path.extname(file)]||'text/html');res.end(fs.readFileSync(file))}catch{res.writeHead(404);res.end()}});await new Promise(r=>server.listen(4173,'127.0.0.1',r));
const manifest=JSON.parse(fs.readFileSync('data/lesson-challenges.json')).items;
const fixtures=()=>{
 const exam=(id,title,part)=>({id,title,active:true,year:part==="ross"?2028:2027,source_type:part==="ross"?'original_authored_mock':'summit_amc_split_original',question_count:part==="speed"?20:part==="depth"?10:23,duration_minutes:part==="speed"?20:part==="depth"?40:60,max_score:part==="speed"?70:part==="depth"?65:100,repeatable:false,metadata:part==="ross"?{}:{amc_part:part,plan_index:1,quality_gate:"reviewed"},student_year:6});
 const catalog=[exam('amc-fixture-a','AMC Part A · Set 01','speed'),exam('amc-fixture-b','AMC Part B · Set 01','depth'),exam('ross-fixture','Rossmoyne Honours Practice 01','ross')];
 const questions=catalog.flatMap(e=>Array.from({length:e.question_count},(_,i)=>{const n=e.metadata?.amc_part==='depth'?i+21:i+1;const mc=e.metadata?.amc_part==='speed'||e.metadata?.amc_part==='depth'&&n<=25||e.max_score===100&&i<18;return {exam_id:e.id,question_number:n,question_type:mc?'multiple_choice':'integer',category:'ALG-01',metadata:{skill_id:'ALG-01',learning_map:{topic:'Algebra and equations',strategy:'Represent an unknown with a bar or equation'}},stem:'A training fixture asks for the missing total. Use the stated relationship.',choices:mc?['First','Second','Third','Fourth','Fifth']:[],marks:e.max_score===100?(i<7?3:i<13?4:i<18?5:6):e.max_score===70?(n<=10?3:4):(n<=25?5:n-20),figure_svg:i===0?'<svg viewBox="0 0 400 140"><rect x="30" y="20" width="340" height="100" fill="#b6dcd6"/></svg>':''}}));
 return {counter:0,exam_catalog:catalog,exam_questions_student:questions,exam_sittings:[],progress_state:[{user_id:'fixture-learner',completed_sessions:0,rank:0,xp:0}],session_records:[],problem_attempts:[],learning_repairs:[],investigation_reviews:[],content_problems_student:manifest.map(x=>({id:x.id,source_type:'original_authored',title:'An original learning challenge',prompt:'A test fixture asks you to recognise a useful structure and explain a method.'}))};
};
const browser=await chromium.launch({headless:true,...(process.env.CHROMIUM_PATH?{executablePath:process.env.CHROMIUM_PATH}:{})});let failures=[];
try{
 for(const mobile of [false,true]){
 const context=await browser.newContext({viewport:mobile?{width:390,height:844}:{width:1440,height:1000},serviceWorkers:'block'});const page=await context.newPage();page.on('pageerror',e=>failures.push(e.message));
 await page.addInitScript(db=>{globalThis.__fixture=JSON.parse(sessionStorage.getItem('qa-repair-state')||'null')||db},fixtures());
 await page.route('**/supabase-client.js*',route=>route.fulfill({contentType:'application/javascript',body:fs.readFileSync('tools/browser_fixture.js','utf8')}));
 await page.route('**/functions/v1/grade-exam',async route=>{
 const input=route.request().postDataJSON();const result=await page.evaluate(id=>{const d=globalThis.__fixture,s=d.exam_sittings.find(x=>x.id===id),e=d.exam_catalog.find(x=>x.id===s.exam_id);const rows=d.exam_questions_student.filter(q=>q.exam_id===e.id).map(q=>{const correct_answer=q.question_type==='integer'?'12':'B',response=s.responses[q.question_number]??null,correct=response===correct_answer||q.question_type==='integer'&&Number(response)===12;return {...q,response,correct,correct_answer,earned:correct?q.marks:0,explanation:'First identify the total and the missing part. Subtract the known amount. Finally substitute the result to check the relationship.'}});s.completed=true;s.score=rows.reduce((n,q)=>n+q.earned,0);s.submitted_at=new Date().toISOString();return {exam:e,rows,score:s.score,original_score:s.score,max_score:e.max_score,submitted_at:s.submitted_at,award:{label:e.max_score===135?'Participation':null,estimated:true},time_used_seconds:90}},input.sitting_id);await route.fulfill({contentType:'application/json',body:JSON.stringify(result)});
 });
 const prefix=mobile?'mobile':'desktop';
  await page.goto('http://127.0.0.1:4173/tests.html?section=depth');await page.getByRole('heading',{name:'AMC Practice · Part B (Q21–30)',exact:true}).waitFor();
  await page.getByRole('button',{name:'Prepare to start',exact:true}).click();await page.getByRole('button',{name:'Start my only attempt',exact:true}).click();await page.getByRole('button',{name:'CLICK HERE TO GO TO FIRST QUESTION'}).click();await page.locator('[data-choice="B"]').click();
 await page.screenshot({path:`qa-screenshots/${prefix}-amc-question.png`,fullPage:true});
  if(mobile)await page.locator('#menuToggle').click();await page.locator('#questionMenu [data-q="5"]').click();await page.locator('#integerInput').fill('12');await page.locator('#saveInteger').click();
  if(mobile)await page.locator('#menuToggle').click();await page.locator('#finish').click();await page.locator('#missingAnswers').waitFor();assert.match(await page.locator('#missingAnswers').innerText(),/8 unanswered/);
 await page.screenshot({path:`qa-screenshots/${prefix}-submit-warning.png`,fullPage:true});await page.locator('#confirmFinish').click();await page.getByRole('heading',{name:'Question-by-question results'}).waitFor();await page.locator('[data-solution="26"]').click();await page.locator('#solution-26[open]').waitFor();await page.screenshot({path:`qa-screenshots/${prefix}-exam-review.png`,fullPage:true});
 // Preserve an existing repair's independent evidence while saving a diagnosis.
 await page.locator('.diagnostic-detail-list>summary').click();await page.locator('.diagnostic-question').first().waitFor();
 await page.evaluate(()=>{const d=globalThis.__fixture,s=d.exam_sittings[0];d.learning_repairs.push({id:'preserved-repair',user_id:'fixture-learner',source_type:'exam',source_ref:s.id+':22',source_label:'Practice Q22',skill_id:'ALG-01',stage:3,due_after_session:3,evidence:{correction:'Existing correction',history:[{correct:true}]},updated_at:'2026-11-12T00:00:00Z'});});
 const diagnostic=page.locator('.diagnostic-question').first();await diagnostic.locator('summary').click();await diagnostic.locator('select').selectOption('choosing a method');await diagnostic.locator('button').click();await diagnostic.getByText('Saved. Your repair progress and exam answers are unchanged.').waitFor();
 assert.deepEqual(await page.evaluate(()=>{const r=globalThis.__fixture.learning_repairs.find(r=>r.id==='preserved-repair');return {stage:r.stage,history:r.evidence.history.length,cause:r.classification}}),{stage:3,history:1,cause:'choosing a method'});
 await page.screenshot({path:`qa-screenshots/${prefix}-exam-diagnosis.png`,fullPage:true});
  await page.locator('#backTests').click();await page.getByRole('button',{name:'Review locked paper',exact:true}).click();await page.locator('.score-big').waitFor();assert.equal(await page.evaluate(()=>globalThis.__fixture.exam_sittings.filter(x=>x.exam_id==='amc-fixture-b').length),1,'locked practice paper cannot be sat again');await page.screenshot({path:`qa-screenshots/${prefix}-locked-amc-review.png`,fullPage:true});await page.locator('[data-solution="26"]').click();await page.locator('#solution-26[open]').waitFor();await page.locator('#solution-26 .exam-lesson-links a').first().click();await page.locator('.technique-review').waitFor();assert.equal(await page.evaluate(()=>globalThis.__fixture.progress_state[0].completed_sessions),0,'exam-driven revision must not advance course');
 await page.goto('http://127.0.0.1:4173/tests.html?section=rossmoyne');await page.getByRole('heading',{name:'Rossmoyne Honours Mathematics',exact:true}).waitFor();assert(await page.locator('body').evaluate(e=>e.classList.contains('rossmoyne-theme')));await page.screenshot({path:`qa-screenshots/${prefix}-rossmoyne-centre.png`,fullPage:true});
 await page.goto('http://127.0.0.1:4173/');
 await page.locator('#continue').click();
 const phase=page.locator('.rwl-track [aria-current="step"]');
 await page.locator('.rwl-example').waitFor();
 assert.equal(await phase.innerText(),'1. Read');
 assert(await page.locator('.rwl-bridge').isVisible());
 assert.equal(await page.locator('#openingVideo,.rwl-form').count(),0);
 await page.screenshot({path:`qa-screenshots/${prefix}-lesson-bridge.png`,fullPage:true});
 await page.getByRole('button',{name:'Watch video',exact:true}).click();
 await page.locator('#openingVideo').waitFor();
 assert.equal(await phase.innerText(),'2. Watch');
 assert.match(await page.locator('#openingVideo').getAttribute('src'),/S001-Intro\.mp4/);
 await page.getByRole('button',{name:'Start practice',exact:true}).click();
 await page.locator('.rwl-form').waitFor();
 assert.equal(await phase.innerText(),'3. Practise');
 assert(await page.locator('[data-screen-next]').isDisabled());
 assert.equal(await page.locator('.rwl-solution').isVisible(),false);
 await page.locator('.rwl-form input').fill('12');
 await page.getByRole('button',{name:'Check answer',exact:true}).click();
 await page.getByRole('button',{name:'See worked solution',exact:true}).click();
 await page.locator('.rwl-steps').waitFor();
 assert.match(await page.locator('.rwl-steps').innerText(),/check the original conditions/);
 assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+2),false);
 // Exercise the repair link and hard reload using a synthetic exam or lesson record.
 await page.evaluate(mobile=>{
  const d=globalThis.__fixture;
  d.learning_repairs=[{id:'repair-one',user_id:'fixture-learner',source_type:mobile?'lesson':'exam',
   source_ref:mobile?'12:application:fixture':'exam:26',source_label:mobile?'Session 12 · Practice':'Paper 01 · Q26',
   skill_id:'ALG-01',stage:0,due_after_session:0,evidence:{},updated_at:'2026-11-12T00:00:00Z'}];
  sessionStorage.setItem('qa-repair-state',JSON.stringify(d));
 },mobile);
 await page.goto('http://127.0.0.1:4173/?view=repairs');
 const content=page.locator('#repairList .repair-content');
 const openRepair=async()=>{
  await page.locator('#repairList details:not([open]) > summary').click();
  // Browsers deliver the native details toggle after its click. Wait for that handler to render the stage.
  await content.locator(':scope > :first-child').waitFor();
 };
 const reopenRepair=async done=>{
  await page.evaluate(done=>{
   const db=globalThis.__fixture;
   if(done!==null)db.progress_state[0].completed_sessions=done;
   sessionStorage.setItem('qa-repair-state',JSON.stringify(db));
  },done??null);
  await page.reload();
  await openRepair();
 };
 const getRepair=()=>page.evaluate(()=>globalThis.__fixture.learning_repairs[0]);
 const submitRepair=async wrong=>{
  const prompt=await content.locator('.mini-check > p').first().textContent();
  const parcel=/A parcel weighs (\d+) grams/.exec(prompt);
  const notebooks=/notebooks and a \$4 pen cost \$(\d+)/.exec(prompt);
  assert.ok(parcel||notebooks,'Unrecognised ALG-01 prompt: '+prompt);
  const answer=parcel?(Number(parcel[1])-7)/5:(Number(notebooks[1])-4)/3;
  await content.locator('.response').fill(wrong?'100000':String(answer));
  await content.getByRole('button',{name:'Check answer',exact:true}).click();
  await content.getByRole('button',{name:'Save repair step'}).waitFor();
  return prompt;
 };
 const advanceRepair=async stage=>{
  await content.getByRole('button',{name:'Save repair step'}).click();
  await page.waitForFunction(s=>globalThis.__fixture.learning_repairs[0].stage===s &&
   !globalThis.__fixture.learning_repairs[0].evidence.pending_recall,stage);
  await openRepair();
 };
 const noCoaching=async()=>{
  await content.locator('.mini-check .response:enabled').waitFor();
  assert.equal(await content.getByText('The idea:',{exact:true}).count(),0);
  assert.equal(await content.getByText('Your next step:',{exact:true}).count(),0);
  assert.equal(await content.getByText('Saved correction:',{exact:true}).count(),0);
 };
 await openRepair();
 await page.locator('[name=cause]').selectOption('choosing a model');
 await page.getByRole('button',{name:'Start practice'}).click();
 await page.waitForFunction(()=>globalThis.__fixture.learning_repairs[0].stage===1);
 await openRepair();
 await content.getByText('The idea:',{exact:true}).waitFor();
 const supportedPrompt=await submitRepair(false);
 await advanceRepair(2);
 await noCoaching();
 // Reject an obsolete hint write; no clue is exposed until it can be recorded.
 await page.evaluate(()=>globalThis.__fixture.learning_repairs[0].updated_at='2026-11-13T00:00:00Z');
 await content.locator('.hint').click();
 await content.getByText(/The hint could not be saved/).waitFor();
 assert.equal((await getRepair()).evidence.pending_recall,undefined);
 await reopenRepair();
 await content.locator('.hint').click();
 await page.waitForFunction(()=>globalThis.__fixture.learning_repairs[0].evidence.pending_recall?.helped);
 await reopenRepair();
 await noCoaching();
 const assistedPrompt=await submitRepair(false);
 assert.notEqual(assistedPrompt,supportedPrompt);
 assert.equal((await getRepair()).evidence.pending_recall.result.used_help,true);
 await reopenRepair();
 await content.locator('.response:disabled').waitFor();
 await content.getByText('The idea:',{exact:true}).waitFor();
 await advanceRepair(2);
 assert.ok((await getRepair()).evidence.history.at(-1).used_help);
 await noCoaching();
 const lostPrompt=await submitRepair(true);
 await reopenRepair();
 await content.locator('.response:disabled').waitFor();
 assert.equal((await getRepair()).evidence.pending_recall.result.correct,false);
 await advanceRepair(2);
 const independentPrompt=await submitRepair(false);
 assert.notEqual(independentPrompt,lostPrompt);
 await advanceRepair(3);
 await page.getByText('Continue learning. This check unlocks after 3 more completed sessions; calendar days do not matter.').waitFor();
 await page.screenshot({path:`qa-screenshots/${prefix}-repair-delay.png`,fullPage:true});
 await reopenRepair(3);
 await noCoaching();
 await content.locator('.hint').click();
 await page.waitForFunction(()=>globalThis.__fixture.learning_repairs[0].evidence.pending_recall?.helped);
 await reopenRepair();
 await submitRepair(false);
 await advanceRepair(2);
 assert.equal((await getRepair()).evidence.history.at(-1).used_help,true);
 await submitRepair(false);
 await advanceRepair(3);
 assert.equal((await getRepair()).due_after_session,6);
 await reopenRepair(6);
 await noCoaching();
 await submitRepair(false);
 await advanceRepair(4);
 const finished=await getRepair();
 assert.ok(finished.evidence.history.at(-1).correct&&!finished.evidence.history.at(-1).used_help);
 assert.equal(finished.evidence.pending_recall,undefined);
 await page.evaluate(()=>sessionStorage.removeItem('qa-repair-state'));
 await page.evaluate(async()=>{const m=await import('/learning-support.js?v=recognition-20261113');await m.mountInvestigationReview(document.querySelector('#app'),{user:{id:'fixture-learner'},record:{session_number:7},item:{solution:'A complete model argument.',transfer_solution:'Test the general rule in a new setting.'}});});
 await page.locator('[name=reviewer]').fill('QA Parent');for(const k of ['result','method','proof'])await page.locator(`[name=${k}]`).selectOption('2');await page.locator('[name=clarity]').selectOption('1');await page.locator('[name=notes]').fill('The pattern is clear. Next, explain why the missing cases cannot occur.');await page.getByRole('button',{name:'Save adult review'}).click();await page.getByText('QA Parent · parent').waitFor();assert.equal(await page.evaluate(()=>globalThis.__fixture.investigation_reviews.length),1);await page.screenshot({path:`qa-screenshots/${prefix}-adult-review.png`,fullPage:true});
 await page.goto('http://127.0.0.1:4173/coverage.html');await page.getByRole('heading',{name:'Coverage across the complete archive'}).waitFor();assert.equal(await page.locator('.coverage-table tbody tr').count(),13);await page.screenshot({path:`qa-screenshots/${prefix}-coverage.png`,fullPage:true});
 assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+2),false,'horizontal overflow');
 await page.goto('http://127.0.0.1:4173/');await page.locator('#continue').waitFor();
 await page.evaluate(async()=>{const {mountPractice}=await import('/transfer-practice.js?v=recognition-20261113');mountPractice(document.querySelector('#app'),{id:'ALG-01',seed:2,key:'independent',draft:{evidence:{},working:{}},save:async()=>{}});});assert.equal(await page.locator('.mini-check svg').count(),0,'independent diagram must not reveal worked steps');
 const value=await page.evaluate(async()=>(await import('/transfer-practice.js?v=recognition-20261113')).practice('ALG-01',2).value);await page.locator('.response').fill(String(value));await page.getByRole('button',{name:'Check answer',exact:true}).click();await page.locator('.feedback ol').waitFor();
 await context.close();
 }
 // Render every authored paper diagram at normal reading size for visual review.
 if(fs.existsSync('/tmp/summit-papers')){
 const figs=fs.readdirSync('/tmp/summit-papers').filter(f=>f.endsWith('.json')).sort().flatMap(f=>{const p=JSON.parse(fs.readFileSync('/tmp/summit-papers/'+f));return p.questions.filter(q=>q.figure_svg).map(q=>({title:p.exam.title+' · '+q.question_number,figure:q.figure_svg}));});
 const context=await browser.newContext({viewport:{width:1200,height:1000}}),p=await context.newPage();
 for(let i=0;i<figs.length;i+=12){await p.setContent('<style>body{font:16px Arial;background:#e8edf2}main{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}article{background:white;padding:10px}svg{width:100%;height:220px}h3{font-size:16px}</style><main>'+figs.slice(i,i+12).map(f=>'<article><h3>'+f.title+'</h3>'+f.figure+'</article>').join('')+'</main>');await p.screenshot({path:`qa-screenshots/figures-${String(i/12+1).padStart(2,'0')}.png`,fullPage:true});}
 await context.close();
 }
 assert.deepEqual(failures,[]);console.log('PASS: desktop/mobile exams, repair cycle, delayed check, adult reviews and lesson bridge; no page errors or horizontal overflow.');
}finally{await browser.close();server.close()}

await import('./check_lesson_models.mjs');
