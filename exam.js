import { supabase } from "./supabase-client.js";
import { requireUser,loadCourse,getProfile,finishSession } from "./course-engine.js";
import { practicePaper,createSitting,updateSitting,completeSitting,awardFor } from "./exam-engine.js";

const root=document.getElementById("examApp"),qs=new URLSearchParams(location.search),esc=s=>String(s??"").replace(/[&<>"']/g,m=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[m]));
let paper=null,sitting=null,responses={},saveTimes={},current=1,timerHandle=null,drafts={},finished=false;

const ACTIVE_KEY="summit-one-active-exam-v1";
async function loadPaper(){
 const practice=Number(qs.get("practiceSession")||0),mode=qs.get("mode")||"amc",paperId=qs.get("paper");
 if(practice){
   const {progress}=await getProfile();
   const allowed=Math.min(372,(progress.completed_sessions||0)+1);
   if(practice!==allowed)throw new Error("That practice assessment is locked until you reach its session in the learning path.");
   const course=await loadCourse(),slot=course.sessions[practice-1];
   if(mode==="amc"&&slot?.type!=="AMC MOCK")throw new Error("This session is not an AMC mock.");
   if(mode==="ross"&&slot?.type!=="ROSSMOYNE MOCK")throw new Error("This session is not a Rossmoyne mock.");
   return practicePaper(practice,mode);
 }
 if(!paperId)throw new Error("No paper selected.");
 const [{data:entry,error:paperError},{data:questions,error:qError}]=await Promise.all([
   supabase.from("exam_catalog").select("*").eq("id",paperId).eq("active",true).maybeSingle(),
   supabase.from("exam_questions").select("*").eq("exam_id",paperId).order("question_number",{ascending:true})
 ]);
 if(paperError)throw paperError;if(qError)throw qError;if(!entry)throw new Error("Paper not found.");
 if((questions||[]).length!==30)throw new Error("This paper is not yet fully imported.");
 const normalized=(questions||[]).map(q=>{
   let choices=q.choices;
   if(Array.isArray(choices))choices=choices.map((x,i)=>typeof x==="object"?x:{label:String.fromCharCode(65+i),value:String(x)});
   const answer=(q.answer&&typeof q.answer==="object"&&"value" in q.answer)?q.answer.value:q.answer;
   return {number:q.question_number,prompt:q.stem,prompt_html:null,figure_svg:q.figure_svg||null,answer:String(answer??""),type:q.question_type,choices,marks:q.marks,category:q.category||"reasoning"};
 });
 return {id:entry.id,title:entry.title,year:entry.year,division:entry.division,year_level:entry.student_year,duration_minutes:entry.duration_minutes,max_score:entry.max_score,kind:"official_past_paper",award_cutoffs_wa:entry.award_cutoffs||null,questions:normalized};
}
function formatTime(ms){const s=Math.max(0,Math.ceil(ms/1000)),m=Math.floor(s/60),x=s%60;return `${String(m).padStart(2,"0")}:${String(x).padStart(2,"0")}`}
function remaining(){return sitting?new Date(sitting.expires_at).getTime()-Date.now():paper.duration_minutes*60000}
function answerCount(){return Object.keys(responses).filter(k=>responses[k]?.value!==undefined&&responses[k]?.value!=="").length}
function storeActive(){if(sitting)localStorage.setItem(ACTIVE_KEY,JSON.stringify({id:sitting.id,exam_id:paper.id}))}
function clearActive(){try{localStorage.removeItem(ACTIVE_KEY)}catch{}}
async function persist(){if(sitting&&!finished)try{sitting=await updateSitting(sitting,responses,saveTimes);storeActive()}catch{}}
async function resumeOpenSitting(){
 const user=await requireUser();
 let candidate=null;
 try{
   const local=JSON.parse(localStorage.getItem(ACTIVE_KEY)||"null");
   if(local?.id){
     const {data}=await supabase.from("exam_sittings").select("*").eq("id",local.id).eq("user_id",user.id).eq("completed",false).maybeSingle();
     if(data&&data.exam_id===paper.id)candidate=data;
   }
 }catch{}
 if(!candidate){
   const {data}=await supabase.from("exam_sittings").select("*").eq("user_id",user.id).eq("exam_id",paper.id).eq("completed",false).order("started_at",{ascending:false}).limit(1);
   candidate=data?.[0]||null;
 }
 if(candidate){
   sitting=candidate;responses=candidate.responses||{};saveTimes=candidate.integer_save_times||{};storeActive();
   if(remaining()<=0){await finish(true);return true}
   renderExam();startTimer();return true;
 }
 return false;
}
function renderStart(){
 root.innerHTML=`<div class="card"><div class="eyebrow">${esc(paper.kind==="practice"?"Summit One training assessment":"Past-paper rehearsal")}</div><h1 style="font-size:clamp(2rem,5vw,3.4rem);margin:.35em 0">${esc(paper.title)}</h1>
 <p class="lead">${paper.division?esc(paper.division)+" · ":""}${paper.questions.length} questions · ${paper.duration_minutes} minutes · ${paper.max_score} marks.</p>
 <div class="grid3"><div class="kpi"><strong>${paper.duration_minutes}</strong><span>minutes</span></div><div class="kpi"><strong>${paper.questions.length}</strong><span>questions</span></div><div class="kpi"><strong>${paper.max_score}</strong><span>marks</span></div></div>
 <p class="mini" style="margin-top:18px">Once you press Start, the timer continues even if the page is refreshed. Q1–Q25 multiple-choice selections save immediately. Q26–Q30 integer answers count only after you press Save. No hints or solution feedback appear during the sitting.</p>
 <div id="phoneWarning" class="mini" style="display:none;color:#ffd166;margin-top:12px"><b>Rehearsal note:</b> use a tablet or computer for the closest match to the official online AMC environment. Phone access remains available for convenience.</div>
 <button class="cta" id="startExam">Start assessment</button> <a class="ghost" href="exams.html">Cancel</a></div>`;
 document.getElementById("phoneWarning").style.display=matchMedia("(max-width: 600px)").matches?"block":"none";
 document.getElementById("startExam").onclick=async e=>{e.currentTarget.disabled=true;sitting=await createSitting(paper);responses=sitting.responses||{};saveTimes=sitting.integer_save_times||{};storeActive();renderExam();startTimer()};
}
function nav(){
 return paper.questions.map(q=>`<button data-q="${q.number}" class="${responses[String(q.number)]?.value!==undefined?"answered":""} ${q.number===current?"current":""}">${q.number}</button>`).join("");
}
function renderExam(){
 const q=paper.questions[current-1],saved=responses[String(q.number)]?.value??"",draft=drafts[q.number]??saved;
 root.innerHTML=`<header class="exam-head"><div><b>Summit One</b><div class="mini">${esc(paper.title)}</div></div><div><span id="answeredCount">${answerCount()}</span>/${paper.questions.length} answered · <span class="timer" id="timer">${formatTime(remaining())}</span></div></header>
 <div class="qnav" id="qnav">${nav()}</div>
 <main class="card question"><div class="eyebrow">Question ${q.number} · ${q.marks} marks</div><h2 style="line-height:1.45">${esc(q.prompt)}</h2>${q.figure_svg?`<div style="max-width:620px;margin:18px auto">${q.figure_svg}</div>`:""}
 ${q.type==="multiple_choice"?`<div id="choices">${(q.choices||[]).map(c=>`<button class="choice ${saved===c.value?"selected":""}" data-value="${esc(c.value)}"><b>${esc(c.label)}.</b> ${esc(c.value)}</button>`).join("")}</div>`:
 `<label class="mini">Integer answer</label><input class="input" id="integerDraft" inputmode="numeric" value="${esc(draft)}" placeholder="Type your integer answer"><div class="btnrow"><button id="saveInteger" class="primary">Save answer</button><span id="saveState" class="${saved!==""?"saved":"unsaved"}">${saved!==""?"Saved: "+esc(saved):"Not saved"}</span></div>`}
 </main>
 <div class="btnrow" style="justify-content:space-between"><button id="prev" ${current===1?"disabled":""}>← Previous</button><button id="submitExam" class="danger">Finish & submit</button><button id="next" ${current===paper.questions.length?"disabled":""}>Next →</button></div>`;
 document.querySelectorAll("#qnav button").forEach(b=>b.onclick=()=>{current=Number(b.dataset.q);renderExam()});
 document.getElementById("prev").onclick=()=>{if(current>1){current--;renderExam()}};
 document.getElementById("next").onclick=()=>{if(current<paper.questions.length){current++;renderExam()}};
 document.getElementById("submitExam").onclick=()=>{if(confirm("Finish and submit this assessment? You will not be able to change answers afterwards."))finish(false)};
 if(q.type==="multiple_choice")document.querySelectorAll(".choice").forEach(b=>b.onclick=async()=>{
   responses[String(q.number)]={value:b.dataset.value,saved_at:new Date().toISOString()};await persist();renderExam()
 });
 else{
   const input=document.getElementById("integerDraft");input.oninput=()=>{drafts[q.number]=input.value;document.getElementById("saveState").className="unsaved";document.getElementById("saveState").textContent="Changed — press Save"};
   document.getElementById("saveInteger").onclick=async()=>{responses[String(q.number)]={value:input.value,saved_at:new Date().toISOString()};saveTimes[String(q.number)]=new Date().toISOString();drafts[q.number]=input.value;await persist();renderExam()};
 }
}
function startTimer(){clearInterval(timerHandle);timerHandle=setInterval(()=>{const el=document.getElementById("timer");if(el)el.textContent=formatTime(remaining());if(remaining()<=0)finish(true)},500)}
async function updateStarCounts(result){
 const user=await requireUser();const {data:p}=await supabase.from("progress_state").select("*").eq("user_id",user.id).maybeSingle();if(!p)return;
 let s3=0,s4=0,s5=0;for(const r of result.rows.filter(x=>x.correct)){const src=(await loadCourse()).challenges.find(c=>c.id===r.source_id);const d=Number(src?.difficulty||r.star||0);if(d===3)s3++;if(d===4)s4++;if(d>=5)s5++}
 await supabase.from("progress_state").update({star3_correct:(p.star3_correct||0)+s3,star4_correct:(p.star4_correct||0)+s4,star5_correct:(p.star5_correct||0)+s5,updated_at:new Date().toISOString()}).eq("user_id",user.id);
}
async function finish(auto){
 if(finished||!sitting)return;finished=true;clearInterval(timerHandle);
 const {result}=await completeSitting(sitting,paper,responses,saveTimes);clearActive();await updateStarCounts(result).catch(()=>{});
 const practice=Number(qs.get("practiceSession")||0);if(practice)await finishSession(practice,`assessment-${practice}`,{answers:responses,working:{},evidence:{exam:true},summary:{type:qs.get("mode")||"amc",score:result.score,max:result.max,auto_submitted:auto}}).catch(()=>{});
 const awards=(await loadCourse()).awards,yearLevel=paper.year_level||5,award=paper.max_score===135?awardFor(result.score,awards,yearLevel,paper.award_cutoffs_wa||null):{name:"Training result",label:"Rossmoyne-style practice",official:false};
 renderResults(result,award,auto);
}
function renderResults(result,award,auto){
 const byCat={};for(const r of result.rows){const k=r.category||"reasoning";byCat[k]??={correct:0,total:0};byCat[k].total++;if(r.correct)byCat[k].correct++}
 root.innerHTML=`<div class="card"><div class="eyebrow">${auto?"Time expired — automatically submitted":"Assessment complete"}</div><h1 style="font-size:clamp(2.5rem,8vw,5rem);margin:.2em 0">${result.score}<span style="color:#8297aa;font-size:.45em"> / ${result.max}</span></h1>
 <div class="award ${/High/.test(award.name)?"hd":award.name==="Distinction"?"d":award.name==="Credit"?"c":""}">${esc(award.name)}</div><p class="mini">${esc(award.label)}${award.official?"":" · not an official AMT award determination"}</p>
 <a class="cta" href="exams.html">Return to test centre</a> <a class="ghost" href="./">Back to mission</a></div>
 <section class="section card"><h2>Question-by-question results</h2>
 <div class="result-grid">${result.rows.map(r=>`<div class="result-cell ${r.correct?"ok":"no"}"><b>Q${r.number}</b><br><span>${r.earned}/${r.marks}</span><br><small>${r.correct?"Correct":"Review"}</small></div>`).join("")}</div>
 <div style="display:grid;gap:10px;margin-top:18px">${result.rows.map(r=>`<details class="stage"><summary><b>Q${r.number} · ${r.correct?"Correct":"Incorrect"} · ${r.earned}/${r.marks}</b></summary><div class="prompt" style="margin-top:12px">${esc(r.prompt)}</div><p class="mini"><b>Your answer:</b> ${esc(r.response||"Unanswered")}<br><b>Correct answer:</b> ${esc(r.answer)}<br><b>Problem family:</b> ${esc(r.category||"reasoning")}</p></details>`).join("")}</div></section>
 <section class="section card"><h2>Performance by problem family</h2>${Object.entries(byCat).map(([k,v])=>`<div style="margin:10px 0"><b>${esc(k)}</b><span class="mini"> · ${v.correct}/${v.total} correct</span><div class="progress"><span style="width:${v.correct/v.total*100}%"></span></div></div>`).join("")}</section>`;
}
async function init(){await requireUser();paper=await loadPaper();if(!(await resumeOpenSitting()))renderStart()}
init().catch(e=>root.innerHTML=`<div class="card"><h2>Assessment could not load</h2><p class="mini">${esc(e.message)}</p><a class="cta" href="exams.html">Return to test centre</a></div>`);
