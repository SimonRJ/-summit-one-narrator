import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import {stripTypeScriptTypes} from 'node:module';
import {methods,exercise,checkAnswer,recallState,skillFor} from '../curriculum.js';
const taxonomy=JSON.parse(fs.readFileSync(new URL('../data/taxonomy-52.json',import.meta.url)));
const sessions=JSON.parse(fs.readFileSync(new URL('../data/sessions-372.json',import.meta.url))).sessions;
assert.equal(Object.keys(methods).length,52);
for(const id of Object.keys(methods))for(let seed=0;seed<7;seed++){
 const q=exercise(id,seed);assert(q.prompt&&q.reason);assert(checkAnswer(q.value,String(q.value)),id);assert(!checkAnswer(q.value,'I think '+q.value),id);
}
assert.equal(new Set(sessions.filter(s=>s.slot<=104).map(s=>skillFor(s,taxonomy)).filter(Boolean)).size,52);
for(let k=7;k<=371;k+=7)assert.equal(sessions[k-1].type,'MAWA');
assert(checkAnswer('1/2','2/4'));assert(!checkAnswer('1/2','1/0'));assert(!checkAnswer(12,'12 or 13'));
const rec=(session,seed,independent=true,correct=true,expected=String(seed))=>({session_number:session,evidence:{a:{kind:'retrieval',skill_id:'ALG-01',seed,question_id:'q'+seed,expected,correct,independent}}});
assert(!recallState([rec(1,2),rec(3,3)],'ALG-01').retained);
assert(!recallState([rec(1,2),rec(5,3,false)],'ALG-01').retained);
assert(!recallState([rec(1,2,true,true,'5'),rec(5,3,true,true,'5')],'ALG-01').retained);
assert(recallState([rec(1,2),rec(5,3)],'ALG-01').retained);
assert(!recallState([rec(1,2),rec(5,3),rec(8,4,true,false)],'ALG-01').retained);
for(let seed=0;seed<7;seed++){
 const n=2+seed;
 const digits=Array.from({length:n+1},(_,i)=>i);
 let count=0;for(const a of digits)for(const b of digits)for(const c of digits)if(a&&a!==b&&b!==c&&a!==c)count++;
 assert.equal(exercise('DIG-02',seed).value,count);
 assert.equal(exercise('DIG-03',seed).value,Array.from({length:n*10+9},(_,i)=>String(i+1)).join('').split('1').length-1);
 const N=2**n*9;let divisors=0;for(let d=1;d<=N;d++)if(N%d===0)divisors++;assert.equal(exercise('DIV-01',seed).value,divisors);
 let maxArea=0;for(let a=1;a<2*n;a++)maxArea=Math.max(maxArea,a*(2*n-a));assert.equal(exercise('GEO-05',seed).value,maxArea);
}
const loadBackend=name=>{
 let source=fs.readFileSync(new URL('../supabase/functions/'+name+'/index.ts',import.meta.url),'utf8').replace(/^import .*;\n/m,'').replace(/export /g,'');
 source=stripTypeScriptTypes(source);const ctx={Deno:{env:{get:()=>''},serve:()=>{}},Response,console};vm.createContext(ctx);vm.runInContext(source,ctx);return ctx;
};
const attempt=loadBackend('submit-problem-attempt');assert.equal(attempt.grade(12,'12'),true);assert.equal(attempt.grade(12,'120'),false);assert.equal(attempt.grade(12,'12 or 15'),null);assert.equal(attempt.grade('1/2','2/4'),true);assert.equal(attempt.grade('a long proof answer','12'),null);
const exam=loadBackend('grade-exam');assert(exam.correctFor({question_type:'integer',answer:'12'},'012'));assert(!exam.correctFor({question_type:'integer',answer:'12'},'12abc'));assert.equal(exam.awardFor(83,{max_score:135},{metadata:{student_year:5}}).label,'High Distinction');assert.equal(exam.awardFor(83,{max_score:135},{metadata:{student_year:6}}).label,'Distinction');
console.log('PASS: 364 exercise variants; 52-technique coverage; 53 seventh-session investigations; delayed evidence, strict answers and exam grading.');

const clientSource=fs.readFileSync(new URL('../supabase-client.js',import.meta.url),'utf8');
const currentUserBody=clientSource.match(/export async function currentUser\(\) \{([\s\S]*?)\n\}/)[1];
const runAuth=async(result)=>new Function('supabase','return (async()=>{'+currentUserBody+'})()')({auth:{getUser:async()=>result}});
assert.equal(await runAuth({data:{user:null},error:{name:'AuthSessionMissingError'}}),null);
assert.equal(await runAuth({data:null,error:{code:'session_not_found'}}),null);
assert.equal((await runAuth({data:{user:{id:'test'}}})).id,'test');
await assert.rejects(()=>runAuth({error:new Error('Network unavailable')}),/Network unavailable/);
console.log('PASS: signed-out and expired sessions, authenticated user, and genuine network error handling.');

const {journeys,investigationOpeners}=await import('../lesson-journeys.js');
const {lessonPlan,introductionHTML,investigationIntroHTML,investigationWarmupHTML,mockIntroductionHTML}=await import('../session-intros.js');
const investigations=JSON.parse(fs.readFileSync(new URL('../data/mawa-investigations-20.json',import.meta.url))).items;
assert.equal(Object.keys(journeys).length,52);
assert.equal(Object.keys(investigationOpeners).length,20);
let covered=0;
for(const s of sessions){
 let html;
 if(s.type==='LESSON'){
  const p=lessonPlan(s,sessions,taxonomy);
  assert.equal(p.id,skillFor(s,taxonomy));assert(p.visit>=1);
  for(const key of ['hook','goal','when','prerequisite','starter','target'])assert(p[key]?.length>15,s.slot+' '+key);
  assert.equal(p.steps.length,3);assert(p.steps.every(x=>x.length>5));
  assert(p.bridge.prompt&&p.bridge.reason);
  html=introductionHTML(s,sessions,taxonomy);
 }else if(s.type==='MAWA'){
  const item=investigations[(Math.floor(s.slot/7)-1)%20];
  html=investigationIntroHTML(s,item);assert(investigationWarmupHTML(item).includes('reasoning-steps'));
 }else{html=mockIntroductionHTML({max_score:s.type==='AMC MOCK'?135:100});assert(html.includes('timer has not started'));}
 assert(html.includes('Success today'));assert(!html.includes('undefined'));covered++;
}
assert.equal(covered,372);
assert.equal(new Set(Object.values(journeys).map(j=>j.hook)).size,52);
console.log('PASS: 372 tailored session openings; 52 technique starters; 20 investigation warm-ups; revisit purposes; rehearsal preparation.');
