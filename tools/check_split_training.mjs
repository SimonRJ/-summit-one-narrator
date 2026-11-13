import assert from "node:assert/strict";
import {readFile} from "node:fs/promises";
import {examClock,elapsedClock,answerGaps} from "../exam-rules.js";

const start=Date.parse("2026-11-13T07:00:00.000Z");
const speedEnd=new Date(start+20*60_000).toISOString();
const depthEnd=new Date(start+40*60_000).toISOString();
const started=new Date(start).toISOString();

assert.equal(elapsedClock(started,speedEnd,start).label,"00:00","count-up begins at zero");
assert.equal(elapsedClock(started,speedEnd,start+6*60_000+23_000).label,"06:23");
assert.equal(elapsedClock(started,speedEnd,start+20*60_000).label,"20:00");
assert.equal(elapsedClock(started,speedEnd,start+25*60_000).label,"20:00","count-up capped after expiry");
assert.equal(elapsedClock(started,depthEnd,start+39*60_000+59_000).label,"39:59");
assert.equal(elapsedClock(started,depthEnd,start+40*60_000).label,"40:00");
assert.equal(examClock(speedEnd,start+20*60_000).seconds,0,"expiry remains authoritative");
assert.equal(examClock(speedEnd,start+3*60_000).label,"17:00","existing countdown unchanged");

const q=[{question_number:21},{question_number:25},{question_number:26}];
assert.deepEqual(answerGaps(q,{"21":"A","26":"314"},{"26":"315"}),{missing:[25],unsaved:[26]});


const read=async path=>readFile(new URL(path,import.meta.url),"utf8");
const src=await read("../tests.js"),app=await read("../app-main.js"),index=await read("../index.html");
const testsPage=await read("../tests.html"),style=await read("../exam.css"),worker=await read("../sw.js");
const map=JSON.parse(await read("../data/skill-session-links.json"));
const sessions=JSON.parse(await read("../data/sessions-372.json")).sessions;

assert.doesNotThrow(()=>new Function(src.replace(/^import .*$/gm,"")),"AMC UI must parse");
assert.doesNotThrow(()=>new Function(app.replace(/^import .*$/gm,"")),"Learning UI must parse");

for(const id of ["speed","depth","amc","rossmoyne","mawa"])
 assert(src.includes('id:"'+id+'"'),"Hub entry "+id);
assert(!src.includes('id:"practice"'),"The extra full-mock category must not be visible");
assert(!src.includes('["practice","Full mocks"]'),"The old AMC full-mock navigation must be absent");
assert(src.includes("plannedSets=isPart?Array.from({length:30}"),"Thirty reserved slots in each part");
assert(src.includes("one scored attempt")||src.includes("One scored attempt"),"Attempts are single-sitting");
assert(!src.includes("Start another practice attempt"),"No repeat prompt in final review");
assert(src.includes("lessonLinksHTML(r)"),"Every result has an associated review-link section");
assert(app.includes("function renderTechniqueRefresher()"),"Read-only lesson review route exists");
assert(app.includes('requestedView==="technique"'),"Deep link to technique route exists");
assert(src.includes("save_exam_response")&&src.includes("/functions/v1/grade-exam"),"Existing protected grading still used");
assert(src.includes("answerGaps"),"Submission confirmation must catch missing/unsaved responses");
assert(src.includes("elapsedClock"),"Count-up clock retained");

assert.equal(Object.keys(map.skills).length,52,"All mathematical skills have mapped lessons");
for(const [skill,entry] of Object.entries(map.skills)){
 assert(entry.sessions.length>0,"Missing learning path for "+skill);
 for(const item of entry.sessions){
  const actual=sessions.find(s=>s.slot===item.slot&&s.type==="LESSON");
  assert(actual&&actual.focus===item.focus,"Incorrect lesson mapping "+skill+" @ "+item.slot);
 }
}
assert(index.includes("main.css?v=menu-20261113-v2"));
assert(testsPage.includes("tests.js?v=curated-20261113"));
assert(style.includes(".amc-pending-sets"));
assert(worker.includes("summit-one-course-drawer-20261113-v2"));
assert(worker.includes("skill-session-links.json"));
console.log("PASS: curated AMC A/B split, 30-slot plans, one-attempt UI, 52 links and countdown boundaries.");
