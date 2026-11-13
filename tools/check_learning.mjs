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
 }else if(s.type==='MIXED'){html='<p>Success today: choose a method independently.</p>';}else{html=mockIntroductionHTML({max_score:s.type==='AMC MOCK'?135:100});assert(html.includes('timer has not started'));}
 assert(html.includes('Success today'));assert(!html.includes('undefined'));covered++;
}
assert.equal(covered,372);
assert.equal(new Set(Object.values(journeys).map(j=>j.hook)).size,52);
console.log('PASS: 372 tailored session openings; 52 technique starters; 20 investigation warm-ups; revisit purposes; rehearsal preparation.');

const {selectOriginalProblems,familySeen,reasoningReady,applicationStatus}=await import('../original-learning.js');
const manifest=JSON.parse(fs.readFileSync(new URL('../data/lesson-challenges.json',import.meta.url))).items;
assert.equal(manifest.length,566);assert.equal(new Set(manifest.map(p=>p.id)).size,566);
const fixtureBank=manifest.map(x=>({id:x.id,source_type:'original_authored',prompt:'Original fixture'}));
for(const s of sessions){
 const pair=selectOriginalProblems(s,fixtureBank,manifest);
 if(s.type==='LESSON'){
  assert.equal(pair.length,2);assert.equal(pair[0].learning.skill,skillFor(s,taxonomy));assert.equal(pair[1].learning.skill,skillFor(s,taxonomy));assert.notEqual(pair[0].learning.family,pair[1].learning.family);
 }else assert.equal(pair.length,0);
}
assert.throws(()=>selectOriginalProblems(sessions[0],[{id:manifest[0].id,source_type:'authentic_amc'}],manifest),/Original lesson content/);
assert.throws(()=>selectOriginalProblems(sessions[0],[],manifest),/Original lesson content/);
assert(!familySeen([], 'x'));assert(familySeen([{evidence:{a:{kind:'application',family:'x'}}}], 'x'));
assert(!reasoningReady({evidence:{}},'x'));
assert(!reasoningReady({evidence:{'reasoning:x':{clue:'The clue is a total.',plan:'Use an equation.',check:'Substitute into both conditions.'}}},'x'));
assert(reasoningReady({answers:{x:{response:'12'}},evidence:{}},'x'));
assert.equal(applicationStatus({correct:true,used_help:true}),'Solved with support');
assert.match(applicationStatus({correct:true,used_help:false,familiar_family:true}),/familiar pattern/);
assert.equal(attempt.independentCredit(true,true,false,false),true);
for(const args of [[true,true,true,false],[true,true,false,true],[true,false,false,false],[false,true,false,false]])assert.equal(attempt.independentCredit(...args),false);
assert(investigations.every(x=>x.transfer_prompt.length>70&&x.transfer_solution.length>100));
console.log('PASS: all 283 lesson pairs explicitly mapped; real papers and missing originals fail closed; familiar or supported work cannot earn new-transfer credit; 20 changed-situation investigations.');

const {techniqueCards,investigationCards,flashDeck}=await import('../flash-cards.js');
const {flashReviewed,flashKey}=await import('../flash-ui.js');
let decks=0;
for(const s of sessions){
 if(s.type==='MIXED')continue;
 const inv=s.type==='MAWA',id=inv?investigations[(Math.floor(s.slot/7)-1)%20].id:skillFor(s,taxonomy);
 const visit=inv?1+Math.floor((Math.floor(s.slot/7)-1)/20):lessonPlan(s,sessions,taxonomy).visit;
 const cards=flashDeck(id,visit,s.slot,inv);assert.equal(cards.length,5);
 assert.equal(new Set(cards.map(c=>c.id)).size,5);
 const a=cards.filter(c=>c.answer===0).length;assert(a===2||a===3);
 for(const c of cards){assert(c.q.length>15&&c.why.length>20);assert.notEqual(c.yes,c.no);assert.equal(c.options[c.answer],c.yes);assert(!/undefined|NaN/.test(JSON.stringify(c)));}
 assert.deepEqual(cards,flashDeck(id,visit,s.slot,inv));decks++;
}
assert.equal(decks,336);
assert.throws(()=>techniqueCards('unknown'),/Missing/);assert.throws(()=>investigationCards('unknown'),/Missing/);
assert(!flashReviewed({evidence:{}},'DIV-03'));
assert(!flashReviewed({evidence:{[flashKey('DIV-03')]:{responses:Array(5).fill({}),reviewed:false}}},'DIV-03'));
assert(flashReviewed({evidence:{[flashKey('DIV-03')]:{responses:Array(5).fill({correct:false}),reviewed:true}}},'DIV-03'));
assert(!recallState([{session_number:1,evidence:{f:{kind:'recognition_practice',skill_id:'DIV-03',correct:true,independent_credit:false}}}],'DIV-03').retained);
for(let visit=1;visit<=9;visit++){
 const n=3+(visit-1)%7;
 assert.equal(techniqueCards('DIG-03',visit)[1].yes,String(Array.from({length:10*n+10},(_,i)=>i).filter(i=>i>=10*n).length));
 assert.equal(techniqueCards('RATE-01',visit)[0].yes,String(n+1));
 assert.equal(techniqueCards('FRAC-01',visit)[1].yes,String((12*n/3)*2));
 assert.equal(techniqueCards('SEQ-02',visit)[1].yes,String(n*2**3));
}
console.log('PASS: five balanced, deterministic A/B cards for every teaching/investigation session (336); no timed-exam insertion; wrong choices allow completion; no mastery credit.');

const {examClock,answerGaps}=await import('../exam-rules.js');
for(const [seconds,prominent,urgent] of [[181,false,false],[180,true,false],[61,true,false],[60,true,true],[1,true,true],[0,true,true]]){
 const c=examClock(new Date(seconds*1000).toISOString(),0);assert.equal(c.seconds,seconds);assert.equal(c.prominent,prominent);assert.equal(c.urgent,urgent);
}
assert.equal(examClock(new Date(0).toISOString(),1000).label,'00:00');
assert.equal(examClock(new Date(180001).toISOString(),0).label,'03:01');
assert.deepEqual(answerGaps([{question_number:1},{question_number:2},{question_number:26},{question_number:27}],{1:'A',26:'0'},{26:'1',27:'2'}),{missing:[2,27],unsaved:[26,27]});
console.log('PASS: countdown thresholds and missing/unsaved answer distinctions.');
