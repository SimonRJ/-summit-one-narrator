import {chromium} from 'playwright';
import fs from 'node:fs';import path from 'node:path';import http from 'node:http';import assert from 'node:assert/strict';
const root=process.cwd();fs.mkdirSync('qa-screenshots',{recursive:true});
const server=http.createServer((req,res)=>{let name=decodeURIComponent(new URL(req.url,'http://localhost').pathname);if(name==='/')name='/index.html';const file=path.resolve(root,'.'+name);if(!file.startsWith(root+path.sep)){res.writeHead(403);res.end();return}try{res.setHeader('Content-Type',file.endsWith('.js')?'application/javascript':file.endsWith('.css')?'text/css':file.endsWith('.json')?'application/json':'text/html');res.end(fs.readFileSync(file))}catch{res.writeHead(404);res.end()}});await new Promise(r=>server.listen(4173,'127.0.0.1',r));
const manifest=JSON.parse(fs.readFileSync('data/lesson-challenges.json')).items;
const fixtures=()=>{
 const exam=(id,title,ross=false)=>({id,title,active:true,year:ross?2028:2027,source_type:'original_authored_mock',question_count:ross?23:30,duration_minutes:60,max_score:ross?100:135,repeatable:!ross,metadata:{},student_year:6});
 const catalog=[exam('amc-fixture','AMC Practice 01'),exam('ross-fixture','Rossmoyne Honours Practice 01',true)];
 const questions=catalog.flatMap(e=>Array.from({length:e.question_count},(_,i)=>({exam_id:e.id,question_number:i+1,question_type:i<(e.max_score===100?18:25)?'multiple_choice':'integer',stem:'A training fixture asks for the missing total. Use the stated relationship.',choices:i<(e.max_score===100?18:25)?['First','Second','Third','Fourth','Fifth']:[],marks:e.max_score===100?(i<7?3:i<13?4:i<18?5:6):(i<10?3:i<20?4:i<25?5:i-19),figure_svg:i===0?'<svg viewBox="0 0 400 140"><rect x="30" y="20" width="340" height="100" fill="#b6dcd6"/></svg>':''})));
 return {counter:0,exam_catalog:catalog,exam_questions_student:questions,exam_sittings:[],progress_state:[{user_id:'fixture-learner',completed_sessions:0,rank:0,xp:0}],session_records:[],problem_attempts:[],learning_repairs:[],investigation_reviews:[],content_problems_student:manifest.map(x=>({id:x.id,source_type:'original_authored',title:'An original learning challenge',prompt:'A test fixture asks you to recognise a useful structure and explain a method.'}))};
};
const browser=await chromium.launch({headless:true});let failures=[];
try{
 for(const mobile of [false,true]){
 const context=await browser.newContext({viewport:mobile?{width:390,height:844}:{width:1440,height:1000},serviceWorkers:'block'});const page=await context.newPage();page.on('pageerror',e=>failures.push(e.message));
 await page.addInitScript(db=>{globalThis.__fixture=db},fixtures());
 await page.route('**/supabase-client.js*',route=>route.fulfill({contentType:'application/javascript',body:fs.readFileSync('tools/browser_fixture.js','utf8')}));
 await page.route('**/functions/v1/grade-exam',async route=>{
 const input=route.request().postDataJSON();const result=await page.evaluate(id=>{const d=globalThis.__fixture,s=d.exam_sittings.find(x=>x.id===id),e=d.exam_catalog.find(x=>x.id===s.exam_id);const rows=d.exam_questions_student.filter(q=>q.exam_id===e.id).map(q=>{const correct_answer=q.question_type==='integer'?'12':'B',response=s.responses[q.question_number]??null,correct=response===correct_answer||q.question_type==='integer'&&Number(response)===12;return {...q,response,correct,correct_answer,earned:correct?q.marks:0,explanation:'First identify the total and the missing part. Subtract the known amount. Finally substitute the result to check the relationship.'}});s.completed=true;s.score=rows.reduce((n,q)=>n+q.earned,0);s.submitted_at=new Date().toISOString();return {exam:e,rows,score:s.score,original_score:s.score,max_score:e.max_score,submitted_at:s.submitted_at,award:{label:e.max_score===135?'Participation':null,estimated:true},time_used_seconds:90}},input.sitting_id);await route.fulfill({contentType:'application/json',body:JSON.stringify(result)});
 });
 const prefix=mobile?'mobile':'desktop';
 await page.goto('http://127.0.0.1:4173/tests.html?section=practice');await page.getByRole('heading',{name:'AMC practice exams',exact:true}).waitFor();
 await page.getByRole('button',{name:'Start attempt 1',exact:true}).click();await page.getByRole('button',{name:'Start this practice attempt',exact:true}).click();await page.getByRole('button',{name:'CLICK HERE TO GO TO FIRST QUESTION'}).click();await page.locator('[data-choice="B"]').click();
 await page.screenshot({path:`qa-screenshots/${prefix}-amc-question.png`,fullPage:true});
 if(mobile)await page.locator('#menuToggle').click();await page.locator('#questionMenu [data-q="25"]').click();await page.locator('#integerInput').fill('12');await page.locator('#saveInteger').click();
 if(mobile)await page.locator('#menuToggle').click();await page.locator('#finish').click();await page.locator('#missingAnswers').waitFor();assert.match(await page.locator('#missingAnswers').innerText(),/28 unanswered/);
 await page.screenshot({path:`qa-screenshots/${prefix}-submit-warning.png`,fullPage:true});await page.locator('#confirmFinish').click();await page.getByRole('heading',{name:'Question-by-question results'}).waitFor();await page.locator('[data-solution="26"]').click();await page.locator('#solution-26[open]').waitFor();await page.screenshot({path:`qa-screenshots/${prefix}-exam-review.png`,fullPage:true});
 await page.locator('#retryPaper').click();await page.getByRole('button',{name:'Start this practice attempt',exact:true}).click();assert.equal(await page.evaluate(()=>globalThis.__fixture.exam_sittings.at(-1).attempt_number),2);
 await page.goto('http://127.0.0.1:4173/tests.html?section=rossmoyne');await page.getByRole('heading',{name:'Rossmoyne Honours Mathematics',exact:true}).waitFor();assert(await page.locator('body').evaluate(e=>e.classList.contains('rossmoyne-theme')));await page.screenshot({path:`qa-screenshots/${prefix}-rossmoyne-centre.png`,fullPage:true});
 await page.goto('http://127.0.0.1:4173/');await page.locator('#continue').click();await page.locator('#nextStage').click();await page.getByRole('heading',{name:'Discover',exact:true}).waitFor();await page.screenshot({path:`qa-screenshots/${prefix}-lesson-bridge.png`,fullPage:true});
 assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+2),false,'horizontal overflow');await context.close();
 }
 assert.deepEqual(failures,[]);console.log('PASS: desktop and mobile exam start/save/submit/review/retry; Rossmoyne theme; lesson bridge; no page errors or horizontal overflow.');
}finally{await browser.close();server.close()}
