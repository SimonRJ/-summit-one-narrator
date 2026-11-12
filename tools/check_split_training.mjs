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

const src=await readFile(new URL("../tests.js",import.meta.url),"utf8");
const app=await readFile(new URL("../app-main.js",import.meta.url),"utf8");
const index=await readFile(new URL("../index.html",import.meta.url),"utf8");
const testsPage=await readFile(new URL("../tests.html",import.meta.url),"utf8");
const examStyle=await readFile(new URL("../exam.css",import.meta.url),"utf8");
const sw=await readFile(new URL("../sw.js",import.meta.url),"utf8");

assert.doesNotThrow(()=>new Function(src.replace(/^import .*$/gm,"")),"exam UI syntax");
assert.doesNotThrow(()=>new Function(app.replace(/^import .*$/gm,"")),"learning UI syntax");
for(const section of ['speed','depth','amc','practice','rossmoyne','mawa']){
 assert(src.includes('id:"'+section+'"')||src.includes("id:\""+section+"\""),"hub card present: "+section);
}
for(const phrase of ["formatElapsedSeconds","first","Fastest perfect","time_used_seconds","elapsedClock","case","split familiarisation"]){
 assert(src.toLowerCase().includes(phrase.toLowerCase()),"expected split support phrase "+phrase);
}
assert(src.includes("save_exam_response"),"response RPC still used");
assert(src.includes("/functions/v1/grade-exam"),"secure grading function still used");
assert(src.includes("answerGaps"),"end confirmation still checks missing and unsaved");
assert(src.includes("Q21–25")&&src.includes("Q26–30"),"depth mark legend present");
assert(src.includes("20 / 20")&&src.includes("65 available marks"),"targets and marks present");
assert(index.includes('data-view="home"')&&index.includes('href="tests.html"'),"Learning and Exams top-level routes");
assert(testsPage.includes("tests.js?v=split-20261113"),"tests bundle cache-busted");
assert(examStyle.includes(".exam-mode .exam-main"),"existing exam interaction styling retained");
assert(sw.includes("split-20261113"),"service worker cache version updated");
assert(app.includes("Continue Session"),"single-path teaching action unchanged");
console.log("AMC split-mode structural, timing and navigation QA passed.");
