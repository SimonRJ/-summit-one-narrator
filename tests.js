import {mountExamDiagnostics} from './exam-diagnostics.js?v=recognition-20261113';
import {examClock,elapsedClock,answerGaps} from './exam-rules.js?v=split-20261113';

if("serviceWorker" in navigator){window.addEventListener("load",()=>navigator.serviceWorker.register("./sw.js").catch(()=>{}));}
import { supabase, currentUser } from "./supabase-client.js?v=auth-20261112";

const app=document.getElementById("examApp");
let user, catalog=[], awards, activeExam=null, questions=[], sitting=null, qIndex=0, responses={}, typedInteger={}, timerHandle=null, saveQueue=Promise.resolve(), finishing=false, saving=false, starting=false;
let sittingsByExam=new Map(), allSittings=[], resultMeta={};
let awardYear=Number(localStorage.getItem("summitSchoolYear")||5);
const params=new URLSearchParams(location.search);
const centre=["hub","speed","depth","amc","practice","rossmoyne","mawa"].includes(params.get("section"))?params.get("section"):"hub";
const EXAM_SECTIONS=[["hub","All exams"],["speed","Q1–20"],["depth","Q21–30"],["practice","Full mocks"],["amc","Past papers"],["mawa","MAWA"],["rossmoyne","Rossmoyne"]];
function belongs(exam,section=centre){
 const part=exam.metadata?.amc_part;
 if(section==="speed")return part==="speed";
 if(section==="depth")return part==="depth";
 if(section==="rossmoyne")return exam.max_score===100;
 if(section==="practice")return exam.max_score===135&&exam.source_type!=="authentic_amc_past_paper";
 if(section==="amc")return exam.source_type==="authentic_amc_past_paper";
 return false;
}
function theme(exam=null){
 const section=exam?.metadata?.amc_part|| (exam?.max_score===100?"rossmoyne":centre);
 const label={hub:"EXAMS",speed:"AMC FLUENCY",depth:"AMC CHALLENGE",practice:"AMC FULL MOCKS",amc:"AMC PAST PAPERS",rossmoyne:"HONOURS MATHEMATICS",mawa:"MAWA INVESTIGATIONS"}[section]||"EXAMS";
 document.body.classList.toggle("rossmoyne-theme",section==="rossmoyne");
 document.body.classList.toggle("split-training",section==="speed"||section==="depth");
 document.querySelector(".brand small").textContent=label;
}
const esc=s=>String(s??"").replace(/[&<>"']/g,m=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[m]));
const norm=s=>String(s??"").trim().toLowerCase().replace(/\s+/g,"").replace(/[.,;:]$/g,"");

async function boot(){
  user=await currentUser();if(!user){location.replace("login.html?next="+encodeURIComponent("tests.html"+location.search));return}
  awards=await fetch("data/amc-awards.json").then(r=>r.json());
  const {data,error}=await supabase.from("exam_catalog").select("*").eq("active",true).order("year",{ascending:false});
  if(error)throw error;catalog=data||[];
  await loadSittings();
  const open=await loadOpenSitting();
  if(open){await resumeSitting(open);return}
  renderLibrary();
}
async function loadSittings(){
  allSittings=[];
  for(let start=0;;start+=500){const {data,error}=await supabase.from('exam_sittings').select('*').eq('user_id',user.id).order('started_at',{ascending:false}).order('id').range(start,start+499);if(error)throw error;allSittings.push(...data);if(data.length<500)break;}
  sittingsByExam=new Map();
  for(const row of allSittings)if(!sittingsByExam.has(row.exam_id))sittingsByExam.set(row.exam_id,row);
}
async function existingSitting(id){
  const exam=catalog.find(e=>e.id===id);
  let request=supabase.from("exam_sittings").select("*").eq("user_id",user.id).eq("exam_id",id).order("started_at",{ascending:false}).limit(1);
  if(exam?.repeatable)request=request.eq("completed",false);
  const {data,error}=await request.maybeSingle();if(error)throw error;return data;
}
function showExamError(error){alert(error.message||"Could not open this paper. Please try again.")}
async function loadOpenSitting(){
  return allSittings.find(row=>!row.completed&&catalog.some(e=>e.id===row.exam_id))||null;
}
async function openSavedSitting(row){
  if(!row.completed){await resumeSitting(row);return}
  clearInterval(timerHandle);sitting=row;
  const {data,error}=await supabase.from("exam_catalog").select("*").eq("id",row.exam_id).single();
  if(error)throw error;activeExam=data;await finishExam(false);
}
function formatElapsedSeconds(s){
 const value=Math.max(0,Number(s||0));
 return `${Math.floor(value/60)}:${String(Math.floor(value)%60).padStart(2,"0")}`;
}
function sittingElapsed(row){
 return row.metadata?.time_used_seconds??Math.max(0,Math.round((new Date(row.submitted_at||row.expires_at).getTime()-new Date(row.started_at).getTime())/1000));
}
function paperAction(exam){
 const attempts=allSittings.filter(r=>r.exam_id===exam.id),open=attempts.find(r=>!r.completed),finished=attempts.filter(r=>r.completed);
 const best=finished.length?Math.max(...finished.map(r=>r.score)):null;
 const perfect=finished.filter(r=>r.score===exam.max_score);
 const bestPerfect=perfect.length?Math.min(...perfect.map(sittingElapsed)):null;
 const first=finished.at(-1);
 const label=open?`Resume attempt ${open.attempt_number}`:exam.repeatable?`Start attempt ${attempts.length+1}`:finished.length?"Review locked paper":"Prepare to start";
 const isSplit=Boolean(exam.metadata?.amc_part);
 return `<div class="paper-actions"><button class="primary startExam" data-id="${esc(exam.id)}">${label}</button>${exam.repeatable&&finished.length?`<button class="ghost" data-review="${esc(finished[0].id)}">Review latest</button>`:""}</div>${finished.length?`<p class="attempt-summary">${finished.length} completed · First ${first.score}/${exam.max_score} in ${formatElapsedSeconds(sittingElapsed(first))} · Best ${best}/${exam.max_score}${bestPerfect!==null?` · Fastest perfect ${formatElapsedSeconds(bestPerfect)}`:""}</p>`:""}<p class="paper-locked">${isSplit&&exam.metadata?.originality==="reused_from_existing_full_mock"?"Familiarisation: these questions also appear in an existing full mock. First-attempt scores are the fairest benchmark.":exam.repeatable?"Every attempt, score and elapsed time is saved.":finished.length?"Submitted · permanent review available.":"One attempt · permanent review after submission."}</p>`;
}
function examMarkGuide(exam){
 if(exam.metadata?.amc_part==="speed")return "Q1–10: 3 marks each · Q11–20: 4 marks each · Maximum 70 marks. The timer counts up to 20:00.";
 if(exam.metadata?.amc_part==="depth")return "Q21–25: 5 marks each · Q26–30: 6, 7, 8, 9, 10 marks. Maximum 65 marks. The timer counts up to 40:00.";
 if(exam.max_score===100)return "Sections 1–4: 7 × 3 marks, 6 × 4 marks, 5 × 5 marks and 5 × 6 marks. The final section needs numerical answers.";
 return "Q1–10: 3 marks each · Q11–20: 4 each · Q21–25: 5 each · Q26–30: 6, 7, 8, 9, 10 marks.";
}
function clockForDisplay(){
 const clock=examClock(sitting.expires_at);
 if(!activeExam?.metadata?.amc_part)return clock;
 const elapsed=elapsedClock(sitting.started_at,sitting.expires_at);
 return {...clock,label:elapsed.label};
}
function reportSections(maxScore){
 if(activeExam?.metadata?.amc_part==="speed")return [[1,10,"Questions 1–10"],[11,20,"Questions 11–20"]];
 if(activeExam?.metadata?.amc_part==="depth")return [[21,25,"Five multiple choice"],[26,30,"Five integer answers"]];
 return maxScore===135?[[1,10,"Questions 1–10"],[11,20,"Questions 11–20"],[21,25,"Questions 21–25"],[26,30,"Final five · Q26–Q30"]]:[[1,7,"Section 1"],[8,13,"Section 2"],[14,18,"Section 3"],[19,23,"Section 4"]];
}
function partReport(rows,timeSeconds){
 const part=activeExam?.metadata?.amc_part;
 if(!part)return "";
 const choices=rows.filter(r=>r.question_number<=25),integers=rows.filter(r=>r.question_number>=26);
 const mc=choices.filter(r=>r.correct).length,ic=integers.filter(r=>r.correct).length,total=mc+ic;
 const perfect=total===20;
 const depthBenchmark=part==="depth"&&mc===5&&ic>=1;
 const target=part==="speed"?`${perfect?"Perfect accuracy · ":""}${total}/20 correct`:`${total}/10 correct · ${mc}/5 multiple choice · ${ic}/5 integer`;
 const info=part==="speed"?(perfect?`All 20 correct in ${formatElapsedSeconds(timeSeconds)}. The first-attempt result is the meaningful speed benchmark.`:"Accuracy comes first. Review any missed ideas before trying a faster time on new questions."):(depthBenchmark?"Initial benchmark achieved: all five choices and at least one integer answer correct.":"An initial goal is all five multiple-choice answers plus one integer answer. Check each method carefully.");
 return `<section class="panel exam-part-report"><span class="eyebrow">${part==="speed"?"FLUENCY REPORT":"CHALLENGE REPORT"}</span><h2>${target}</h2><p>${info}</p><p class="muted">Elapsed time: ${formatElapsedSeconds(timeSeconds)} · Limit: ${activeExam.duration_minutes}:00 · This part result is not an official AMC award.</p></section>`;
}
function renderExamHub(){
 const count=id=>catalog.filter(e=>belongs(e,id)).length;
 const last=allSittings.filter(r=>r.completed).slice(0,5);
 const cards=[
  {id:"speed",num:"01",title:"AMC · Fluency",tag:"Q1–20",time:"20-minute limit",summary:"Twenty multiple-choice questions. Aim for 20 correct, then improve the time. Clock counts up from zero.",count:count("speed"),target:"20 / 20 · 70 marks",featured:true},
  {id:"depth",num:"02",title:"AMC · Challenge",tag:"Q21–30",time:"40-minute limit",summary:"Five multiple-choice and five integer-answer problems. An excellent first benchmark is all five choices plus one integer.",count:count("depth"),target:"First benchmark · 6 / 10",featured:true},
  {id:"practice",num:"03",title:"Full AMC mocks",tag:"Q1–30",time:"60 minutes",summary:"Original authored full-length papers. Combine pace and deeper reasoning under complete competition conditions.",count:count("practice"),target:"135 marks"},
  {id:"amc",num:"04",title:"Real AMC papers",tag:"Upper Primary",time:"60 minutes",summary:"Authentic historical papers. One sitting per paper; reserve some for unseen progress checks.",count:count("amc"),target:"Official-format questions"},
  {id:"rossmoyne",num:"05",title:"Rossmoyne Honours",tag:"School entry",time:"Practice setting",summary:"Four-section specialist mathematics practice papers with written solutions and a permanent record.",count:count("rossmoyne"),target:"100 marks"},
  {id:"mawa",num:"06",title:"MAWA investigations",tag:"Mathematical reasoning",time:"Work at your own pace",summary:"Structured investigations and proofs. Every seventh learning session includes one; these are not timed AMC-style tests.",count:null,target:"53 scheduled investigations"}
 ];
 app.innerHTML=`<section class="panel exam-hub-intro"><div class="eyebrow">SUMMIT ONE · ASSESSMENT AND PRACTICE</div><h1>Exams</h1><p>Practise accuracy, speed and unfamiliar problem solving separately—then test the complete skill in full-length exams. Your score and time history remains attached to every sitting.</p><div class="exam-hub-metrics"><span>${allSittings.filter(x=>x.completed).length} completed sittings</span><span>Progress saved to your account</span><span>Full reports after submission</span></div></section>
 <section class="exam-hub-heading"><div><h2>Choose a training mode</h2><p class="muted">The first two modes isolate the skills needed for an efficient AMC sitting.</p></div></section>
 <div class="exam-hub-grid">${cards.map(c=>`<a href="tests.html?section=${c.id}" class="panel exam-hub-card ${c.featured?"exam-hub-featured":""}"><span class="exam-hub-number">${c.num} / TRAINING</span><div class="exam-hub-card-title"><h3>${c.title}</h3><span class="exam-hub-chevron" aria-hidden="true">↗</span></div><div class="exam-hub-labels"><span class="phase-chip">${c.tag}</span><span class="phase-chip">${c.time}</span></div><p>${c.summary}</p><div class="exam-hub-foot"><b>${c.target}</b><span>${c.count===null?"Learning pathway":`${c.count} available sets`}</span></div></a>`).join("")}</div>
 <section class="panel result-card exam-hub-history"><h2>Recent exam results</h2><p class="muted">First-attempt accuracy on new material matters most. Repeated papers are useful for fluency but may become familiar.</p><div id="savedSittings" class="history-list"></div></section>`;
 loadResultHistory().catch(showExamError);
}
function renderMawaHub(){
 app.innerHTML=`<section class="panel test-hero"><div class="eyebrow">MAWA · MATHEMATICAL PROBLEM SOLVING</div><h1>MAWA investigations</h1><p class="muted">These sessions assess the quality of a mathematical explanation, not just a selected answer. They are untimed investigations, not official MAWA exam papers.</p><nav class="exam-centre-tabs" aria-label="Exam sections">${EXAM_SECTIONS.map(([id,label])=>`<a href="tests.html${id==="hub"?"":`?section=${id}`}" ${centre===id?'aria-current="page"':""}>${label}</a>`).join("")}</nav></section>
 <section class="exam-hub-grid"><article class="panel exam-hub-card"><div class="eyebrow">IN THE LEARNING PATHWAY</div><h2>Every seven completed sessions</h2><p>There are 53 investigation slots built into the 372-session course, drawing on twenty detailed investigation themes. Work, reasoning and adult rubric feedback remain part of the learner's saved session record.</p><p>Continue your current session; the next MAWA investigation appears automatically at the correct point in the pathway.</p><a class="primary" href="./">Continue Learning</a></article><article class="panel exam-hub-card"><div class="eyebrow">WHAT COUNTS AS SUCCESS</div><h2>Explain and prove</h2><p>Define the problem clearly, test cases systematically, develop a convincing method, and justify the conclusion. The initial focus is independent reasoning rather than speed.</p><a class="secondary" href="index.html?view=roadmap">View the mathematics roadmap</a></article></section>`;
}
async function prepareExam(id){
  const exam=catalog.find(x=>x.id===id);if(!exam)return;
  const existing=await existingSitting(id);if(existing){await openSavedSitting(existing);return}
  document.body.classList.remove('exam-mode');theme(exam);
  const startLabel=exam.repeatable?'Start this practice attempt':'Start my only attempt';
  app.innerHTML=`<section class="panel test-hero exam-start-warning"><div class="eyebrow">${exam.max_score===100?'ROSSMOYNE HONOURS · ':''}BEFORE YOU START · ${exam.repeatable?'REPEATABLE PRACTICE':'ONE ATTEMPT ONLY'}</div><h1>${esc(exam.title)}</h1><p class="muted">${exam.question_count} questions · ${exam.duration_minutes} minutes · ${exam.max_score} marks</p>
  <div class="notice-box"><h2>${exam.repeatable?'A fresh attempt, with its own saved result':'This is your only attempt at this paper'}</h2><p>When you click <b>${startLabel}</b>, the timer begins and keeps running if you close the page. You can return to the same attempt while time remains.</p><p>Final submission permanently locks <b>this attempt</b>. At zero, saved answers are locked and submitted when connected. ${exam.repeatable?'You may start another attempt afterwards. All attempts, scores and reviews remain in your history.':'You cannot restart or redo this paper. Your completed review remains available afterwards.'}</p></div>
  <div class="exam-section-key">${esc(examMarkGuide(exam))}</div>
  <p>Have paper and a pencil ready. Work without a calculator, notes or solution pages. Multiple-choice answers save when selected; numerical answers count after you press <b>Save</b>.</p>
  ${exam.max_score===100?'<p class="muted">A 60-minute Summit One practice setting. The uploaded sample supplies the question and section format; future school test instructions take precedence.</p>':''}
  ${exam.repeatable?'<p class="muted">Repeat scores show improvement on this paper. Your first attempt is recorded separately because later attempts may benefit from memory.</p>':''}
  <p class="muted">The timer has not started. A computer or tablet is best for a full sitting.</p><div class="complete-row"><button id="cancelStart" class="ghost">Not yet — go back</button><button id="confirmStart" class="primary cta">${startLabel}</button></div></section>`;
  document.getElementById('cancelStart').onclick=()=>renderLibrary();document.getElementById('confirmStart').onclick=()=>startExam(id);window.scrollTo({top:0,behavior:'instant'});
}
function practicePerformanceHTML(part){
 const getExam=id=>catalog.find(e=>e.id===id);
 const original=e=>e?.source_type==="summit_amc_split_original";
 const rows=allSittings.filter(row=>row.completed&&row.attempt_number===1&&getExam(row.exam_id)?.metadata?.amc_part===part&&original(getExam(row.exam_id)));
 const perfect=rows.filter(row=>row.score===row.max_score);
 const avg=rows.length?Math.round(rows.reduce((n,row)=>n+(row.score||0)/row.max_score,0)*100/rows.length):null;
 const fastest=perfect.length?Math.min(...perfect.map(sittingElapsed)):null;
 const recent=rows[0];
 const value=recent?((recent.score||0)+"/"+recent.max_score+" · "+formatElapsedSeconds(sittingElapsed(recent))):"No first sitting yet";
 return `<section class="exam-performance" aria-label="First attempt results on new original papers">
 <div class="exam-performance-card"><span class="eyebrow">NEW-QUESTION ACCURACY</span><strong>${avg===null?"—":avg+"%"}</strong><small>Average first-sitting accuracy across ${rows.length} original ${rows.length===1?"paper":"papers"}</small></div>
 <div class="exam-performance-card"><span class="eyebrow">FASTEST FIRST-TRY PERFECT</span><strong>${fastest===null?"—":formatElapsedSeconds(fastest)}</strong><small>Only ${part==="speed"?"20/20":"10/10"} scores on unseen original sets count</small></div>
 <div class="exam-performance-card"><span class="eyebrow">MOST RECENT ORIGINAL</span><strong class="exam-performance-recent">${value}</strong><small>First submissions only · no result from replaying a memorised set</small></div>
 </section>`;
}
function renderLibrary(){
 document.body.classList.remove("exam-mode");theme();
 if(centre==="hub"){renderExamHub();return;}
 if(centre==="mawa"){renderMawaHub();return;}
 const papers=catalog.filter(e=>belongs(e)).sort((a,b)=>centre==="amc"?b.year-a.year:(Number(b.source_type==="summit_amc_split_original")-Number(a.source_type==="summit_amc_split_original"))||a.id.localeCompare(b.id));
 const titles={speed:"AMC Fluency · Q1–20",depth:"AMC Challenge · Q21–30",amc:"Real AMC past papers",practice:"AMC practice exams",rossmoyne:"Rossmoyne Honours Mathematics"};
 const introductions={
   speed:"Twenty multiple-choice questions, 70 marks and a 20-minute limit. The timer counts up. Aim for 20/20; among perfect first attempts, a time below 20 minutes is excellent. Ten familiarisation sets reuse existing authored full mocks, and one newly authored original set has separate checking. Select an original set for the strongest unseen-problem benchmark.",
   depth:"Ten difficult questions: Q21–25 multiple choice; Q26–30 integer answer. The timer counts up to the 40-minute limit. Six correct—including all five multiple choice and one integer—is an excellent early benchmark. Ten familiarisation sets reuse existing full mocks; an additional newly authored challenge set has been checked independently and is labelled.",
   amc:"Authentic Upper Primary papers from 2007–2025, where available. Keep some unopened for later independent checks. Each authentic paper has one attempt and permanent written-solution review.",
   practice:"Ten original full-length 30-question papers. These combine the easier twenty with the final ten, so they are the most faithful rehearsal of a complete sitting.",
   rossmoyne:"The uploaded original sample and nine authored practice papers, with the same four-section, 100-mark structure. Each paper has one attempt and a permanent review."
 };
 const isPart=centre==="speed"||centre==="depth";
 app.innerHTML=`<section class="panel test-hero"><div class="eyebrow">${centre==="rossmoyne"?"HONOURS MATHEMATICS":"SUMMIT ONE · EXAMS"}</div><h1>${titles[centre]}</h1><p class="muted">${introductions[centre]}</p><nav class="exam-centre-tabs" aria-label="Exam sections">${EXAM_SECTIONS.map(([id,label])=>`<a href="tests.html${id==="hub"?"":`?section=${id}`}" ${centre===id?'aria-current="page"':""}>${label}</a>`).join("")}</nav>${centre==="amc"?`<label class="year-select">School year for estimated award bands <select id="awardYear"><option value="5" ${awardYear===5?"selected":""}>Year 5</option><option value="6" ${awardYear===6?"selected":""}>Year 6</option></select></label>`:""}</section>
 ${isPart?`<section class="exam-benchmark-row"><div><span class="eyebrow">BENCHMARK</span><strong>${centre==="speed"?"20 / 20 correct":"5 / 5 multiple choice + 1 integer"}</strong></div><div><span class="eyebrow">TIME LIMIT</span><strong>${centre==="speed"?"20:00":"40:00"} · counting up</strong></div><div><span class="eyebrow">SCORING</span><strong>${centre==="speed"?"70 available marks":"65 available marks"}</strong></div></section>`:""}
 ${isPart?practicePerformanceHTML(centre):""}
 <div class="test-grid">${papers.map(exam=>`<article class="panel test-card"><div class="eyebrow">${exam.metadata?.originality==="reused_from_existing_full_mock"?"EXISTING MOCK · SPLIT FAMILIARISATION":exam.source_type==="authentic_amc_past_paper"?"AUTHENTIC AMC PAST PAPER":exam.source_type==="summit_amc_split_original"?"NEW ORIGINAL · INDEPENDENTLY CHECKED":exam.metadata?.original_sample?"UPLOADED ORIGINAL SAMPLE · TRANSCRIBED":"SUMMIT ONE AUTHORED PRACTICE"}</div><h2>${esc(exam.title)}</h2><div class="test-meta"><span class="phase-chip">${exam.question_count} questions</span><span class="phase-chip">${exam.duration_minutes} min</span><span class="phase-chip">${exam.max_score} marks</span></div><p class="muted">${esc(exam.metadata?.card_summary||"Full written solutions available after submission.")}</p>${paperAction(exam)}</article>`).join("")}</div>
 <section class="panel result-card"><h2>Your ${isPart?centre==="speed"?"fluency":"challenge":"exam"} history</h2><p class="muted">Every completed attempt and elapsed time remains recorded. A review cannot change a submitted result.</p><div id="savedSittings" class="history-list"></div></section><p class="footer-note">Summit One is an independent study app. Authored mocks are not official AMT or Rossmoyne papers.</p>`;
 document.getElementById("awardYear")?.addEventListener("change",e=>{awardYear=Number(e.target.value);localStorage.setItem("summitSchoolYear",String(awardYear))});
 document.querySelectorAll(".startExam").forEach(b=>b.onclick=()=>prepareExam(b.dataset.id).catch(showExamError));
 document.querySelectorAll("[data-review]").forEach(b=>b.onclick=()=>openSavedSitting(allSittings.find(r=>r.id===b.dataset.review)).catch(showExamError));
 loadResultHistory().catch(showExamError);
}
async function startExam(id){
  if(starting)return;starting=true;
  const button=document.getElementById("confirmStart");if(button){button.disabled=true;button.textContent="Opening your attempt…"}
  try{
    activeExam=catalog.find(x=>x.id===id);if(!activeExam)return;
    const existing=await existingSitting(id);
    if(existing){await openSavedSitting(existing);return}
    const {data:q,error}=await supabase.from("exam_questions_student").select("*").eq("exam_id",id).order("question_number");
    if(error)throw error;if((q||[]).length!==(activeExam.question_count||30))throw new Error("This paper is not complete yet. Your attempt has not started.");
    questions=q;responses={};typedInteger={};qIndex=0;
    const start=new Date(),expires=new Date(start.getTime()+activeExam.duration_minutes*60000);
    const {data:s,error:e}=await supabase.from("exam_sittings").insert({
      user_id:user.id,exam_id:id,exam_year:activeExam.year,started_at:start.toISOString(),expires_at:expires.toISOString(),completed:false,max_score:activeExam.max_score,responses:{},integer_save_times:{},metadata:{title:activeExam.title,student_year:activeExam.source_type==="authentic_amc_past_paper"?awardYear:(activeExam.student_year||awardYear),centre,course_mode:false}
    }).select().single();
    if(e){const concurrent=await existingSitting(id);if(concurrent){await openSavedSitting(concurrent);return}throw e}
    sitting=s;sittingsByExam.set(id,s);renderOverview();startTimer();
  }catch(e){showExamError(e)}finally{starting=false;if(button?.isConnected){button.disabled=false;button.textContent=activeExam?.repeatable?"Start this practice attempt":"Start my only attempt"}}
}
async function resumeSitting(s){
  const {data:exam,error:examError}=await supabase.from("exam_catalog").select("*").eq("id",s.exam_id).single();if(examError)throw examError;activeExam=exam;
  const {data:q,error:questionError}=await supabase.from("exam_questions_student").select("*").eq("exam_id",s.exam_id).order("question_number");if(questionError)throw questionError;questions=q||[];
  sitting=s;sittingsByExam.set(s.exam_id,s);responses=s.responses||{};typedInteger={};qIndex=0;
  if(new Date(s.expires_at)<=new Date()){await finishExam(true);return}
  renderOverview();startTimer();
}
function updateTimer(){
  const clock=clockForDisplay();
  document.querySelectorAll("[data-exam-countdown]").forEach(el=>{
    el.textContent=clock.label;el.classList.toggle("timer-prominent",clock.prominent);el.classList.toggle("timer-urgent",clock.urgent);
  });
  return clock;
}
function startTimer(){
  clearInterval(timerHandle);
  const tick=()=>{if(updateTimer().seconds===0){clearInterval(timerHandle);finishExam(true)}};
  timerHandle=setInterval(tick,500);tick();
}
function wireQuestionZoom(){
 document.querySelectorAll('.exam-visual img').forEach(img=>{
  const button=document.createElement('button');button.type='button';button.className='ghost question-zoom';button.textContent='Enlarge original question';img.after(button);
  button.onclick=()=>{
   const dialog=document.createElement('dialog');dialog.className='question-dialog';
   const close=document.createElement('button');close.className='primary';close.textContent='Close enlarged question';
   const copy=img.cloneNode();copy.className='enlarged-question';
   dialog.append(close,copy);document.body.append(dialog);close.onclick=()=>dialog.close();
   dialog.addEventListener('close',()=>dialog.remove());dialog.showModal();close.focus();
  };
 });
}
function timeRemaining(){return examClock(sitting.expires_at).label}
function countdownHTML(id,extra=""){
  const clock=clockForDisplay();
  return `<b id="${id}" data-exam-countdown class="timer ${extra} ${clock.prominent?"timer-prominent":""} ${clock.urgent?"timer-urgent":""}" aria-live="off">${clock.label}</b>`;
}
function isAnswered(n){return responses[n]!==undefined&&responses[n]!==null&&responses[n]!==""}
function examFrame(content,overview=false){
  document.body.classList.add("exam-mode");theme(activeExam);
  app.innerHTML=`<div class="practice-label">${activeExam.max_score===100?'SUMMIT ONE · ROSSMOYNE HONOURS PRACTICE · FOUR SECTIONS · 100 MARKS':activeExam.metadata?.amc_part?"SUMMIT ONE · AMC "+(activeExam.metadata.amc_part==="speed"?"Q1–20 FLUENCY":"Q21–30 CHALLENGE")+" · INDEPENDENT TRAINING":"SUMMIT ONE PRACTICE · Navigation modelled on AMT\'s public online demonstration"}</div><section class="exam-shell">
  <aside class="exam-sidebar"><button id="menuToggle" class="menu-toggle" aria-expanded="false" aria-controls="questionMenu">Question menu ▾</button><nav id="questionMenu" class="question-menu" aria-label="Exam questions"><button id="overview" class="exam-name ${overview?"current":""}">${esc(activeExam.title)}</button><div class="qnav">${questions.map((q,i)=>`<button data-q="${i}" class="${!overview&&i===qIndex?"current":""} ${isAnswered(q.question_number)?"answered":""}" ${!overview&&i===qIndex?'aria-current="step"':''}><span>Question ${q.question_number}</span><span class="answer-marker" aria-label="${isAnswered(q.question_number)?"Answered":"Not answered"}"></span></button>`).join("")}</div><button id="finish" class="end-menu">End competition</button></nav></aside>
  <article class="exam-main">${content}</article></section>`;
  document.getElementById("menuToggle").onclick=()=>{const menu=document.getElementById("questionMenu"),open=menu.classList.toggle("open");document.getElementById("menuToggle").setAttribute("aria-expanded",String(open))};
  document.querySelectorAll("[data-q]").forEach(b=>b.onclick=()=>{if(finishing)return;qIndex=Number(b.dataset.q);renderExam()});
  document.getElementById("overview").onclick=()=>{if(!finishing)renderOverview()};
  document.getElementById("finish").onclick=()=>{if(!finishing)renderOverview(true)};
  window.scrollTo({top:0,behavior:"instant"});
  const current=document.querySelector("#questionMenu .qnav .current"),sidebar=document.querySelector(".exam-sidebar");
  if(current&&innerWidth>760)sidebar.scrollTop=Math.max(0,current.offsetTop-sidebar.clientHeight/2);
}
function timerHTML(){return `<div class="time-box"><span>${activeExam?.metadata?.amc_part?`Elapsed · ${activeExam.duration_minutes}:00 limit`:"Time remaining"}</span>${countdownHTML("timer")}</div>`}
function renderOverview(ending=false){
  const {missing,unsaved}=answerGaps(questions,responses,typedInteger);
  const questionLinks=numbers=>numbers.map(n=>`<button class="exam-text-link" data-q="${questions.findIndex(q=>q.question_number===n)}">Q${n}</button>`).join(", ");
  examFrame(`<div class="qhead"><h1>${ending?"End competition":esc(activeExam.title)}</h1>${timerHTML()}</div>
  ${ending?`<section class="end-confirm" aria-labelledby="endPrompt"><h2 id="endPrompt">Ready to submit and lock your exam?</h2><p class="submission-countdown">${activeExam?.metadata?.amc_part?"Elapsed time:":"You have"} ${countdownHTML("submitCountdown","submit-time")} ${activeExam?.metadata?.amc_part?"(the limit is "+activeExam.duration_minutes+":00).":"left."}</p><p>Have you given a response for every question and checked all your answers?</p>
  ${missing.length?`<div id="missingAnswers" class="missing-answers"><b>${missing.length} unanswered ${missing.length===1?"question":"questions"}:</b> ${questionLinks(missing)}<p>These questions have no saved response and will receive no marks. Select a question above to return to it.</p></div>`:'<p id="allAnswered"><b>Every question has a saved response.</b></p>'}
  ${unsaved.length?`<div id="unsavedAnswers" class="missing-answers"><b>Unsaved integer answers: ${unsaved.map(esc).join(", ")}.</b> ${questionLinks(unsaved)}<p>Return and press <b>Save</b> if you want the changed answer marked. Otherwise, only the previously saved answer counts.</p></div>`:""}
  <p>Submitting now permanently locks this attempt. ${activeExam.repeatable?"You may start a new practice attempt afterwards; this result remains saved.":"You can review it at any time, but cannot change answers or attempt this paper again."}</p><div class="confirm-actions"><button id="cancelFinish">Go back and check</button><button id="confirmFinish">Submit and lock exam</button></div></section>`:`<p class="overview-help">The table lists all questions, their value and whether you have answered them. It does not show whether answers are correct.</p><button id="firstQuestion" class="exam-text-link">CLICK HERE TO GO TO FIRST QUESTION</button>`}
  <p class="answer-count">${questions.filter(q=>isAnswered(q.question_number)).length} answered · ${questions.filter(q=>!isAnswered(q.question_number)).length} not answered</p>
  <table class="exam-summary"><thead><tr><th>Question</th><th>Value</th><th>Status</th></tr></thead><tbody>${questions.map((q,i)=>`<tr><td><button data-q="${i}" class="exam-text-link">Question ${q.question_number}</button></td><td>${q.marks}</td><td>${isAnswered(q.question_number)?"Answered":"Not answered"}</td></tr>`).join("")}</tbody></table>
  ${ending?"":'<button id="endParticipation" class="exam-text-link end-link">End participation</button>'}`,true);
  const first=document.getElementById("firstQuestion");if(first)first.onclick=()=>{qIndex=0;renderExam()};
  const end=document.getElementById("endParticipation");if(end)end.onclick=()=>renderOverview(true);
  const yes=document.getElementById("confirmFinish");if(yes)yes.onclick=()=>{yes.disabled=true;finishExam(false)};
  const no=document.getElementById("cancelFinish");if(no)no.onclick=()=>renderOverview();
}
function renderExam(){
  const q=questions[qIndex];if(!q)return;
  examFrame(`<div class="qhead"><h1>Question ${q.question_number}</h1><div class="exam-actions"><button id="prev" ${qIndex===0?"disabled":""}>Previous</button><button id="next">Next</button></div>${timerHTML()}</div><div class="stem">${esc(q.stem)}</div>${q.image_ref||q.figure_svg?`<div class="exam-visual">${q.image_ref||q.figure_svg}</div>`:""}<div id="answerArea"></div>`);
  renderAnswer(q);wireQuestionZoom();
  document.getElementById("prev").onclick=()=>{if(!finishing&&qIndex>0){qIndex--;renderExam()}};
  document.getElementById("next").onclick=()=>{if(finishing)return;if(qIndex<questions.length-1){qIndex++;renderExam()}else renderOverview()};
}
function canAnswer(){return !finishing&&!saving&&!sitting?.completed&&Date.now()<new Date(sitting.expires_at).getTime()}
function renderAnswer(q){
  const area=document.getElementById("answerArea"),saved=responses[q.question_number];
  if(q.question_type==="multiple_choice"){
    const choices=Array.isArray(q.choices)?q.choices:[];
    area.innerHTML='<div class="choices">'+choices.map((c,i)=>`<button class="choice ${saved===String.fromCharCode(65+i)?"selected":""}" data-choice="${String.fromCharCode(65+i)}" aria-pressed="${saved===String.fromCharCode(65+i)}"><span class="choice-letter">${String.fromCharCode(65+i)}</span><span class="choice-content">${typeof c==="string"?esc(c):`${c.visual_html||""}${c.text?`<span>${esc(c.text)}</span>`:""}`}</span></button>`).join("")+'</div>';
    area.querySelectorAll("[data-choice]").forEach(b=>b.onclick=async()=>{if(!canAnswer())return;saving=true;const previous=responses[q.question_number];responses[q.question_number]=b.dataset.choice;area.querySelectorAll("button").forEach(x=>x.disabled=true);try{await persistResponses(false,q.question_number);renderExam()}catch(e){if(previous===undefined)delete responses[q.question_number];else responses[q.question_number]=previous;renderExam();alert("Answer not saved: "+e.message)}finally{saving=false}});
  }else{
    const typed=typedInteger[q.question_number]??(saved??"");
    area.innerHTML=`<div class="integer-row"><label>Your integer answer<br><input id="integerInput" inputmode="numeric" pattern="[0-9]*" value="${esc(typed)}"></label><div class="integer-controls"><button id="saveInteger" class="primary">Save</button><span id="saveState" class="${saved!==undefined&&String(typed)===String(saved)?"saved":"unsaved"}">${saved!==undefined&&String(typed)===String(saved)?"Saved":"Not saved"}</span></div></div><p class="muted" style="margin-top:10px">Typing is not enough. Press <b>Save</b> before leaving the question.</p>`;
    const inp=document.getElementById("integerInput");inp.oninput=()=>{typedInteger[q.question_number]=inp.value;document.getElementById("saveState").className="unsaved";document.getElementById("saveState").textContent="Not saved"};
    document.getElementById("saveInteger").onclick=async()=>{if(!canAnswer())return;const v=inp.value.trim();if(!((activeExam.max_score===135||activeExam.metadata?.amc_part)?/^\d{1,3}$/:/^\d{1,6}$/).test(v)){alert((activeExam.max_score===135||activeExam.metadata?.amc_part)?"Enter a whole-number answer from 0 to 999.":"Enter a whole-number answer from 0 to 999999.");return}saving=true;const previous=responses[q.question_number];responses[q.question_number]=v;typedInteger[q.question_number]=v;try{await persistResponses(true,q.question_number);renderExam()}catch(e){if(previous===undefined)delete responses[q.question_number];else responses[q.question_number]=previous;document.getElementById("saveState").textContent="Not saved — retry";alert(e.message)}finally{saving=false}};
  }
  const erase=document.createElement("button");erase.id="eraseAnswer";erase.className="erase-answer";erase.textContent="Erase";
  const integerControls=area.querySelector(".integer-controls");
  if(integerControls)integerControls.insertBefore(erase,document.getElementById("saveState"));else area.append(erase);
  erase.onclick=async()=>{
    if(!canAnswer())return;saving=true;const previous=responses[q.question_number],previousTyped=typedInteger[q.question_number];
    delete responses[q.question_number];delete typedInteger[q.question_number];erase.disabled=true;
    try{await persistResponses(false,q.question_number);renderExam()}catch(e){if(previous!==undefined)responses[q.question_number]=previous;if(previousTyped!==undefined)typedInteger[q.question_number]=previousTyped;renderExam();alert("Answer could not be erased: "+e.message)}finally{saving=false}
  };
}
async function persistResponses(integerSave=false,qnum=null){
  if(qnum===null)return saveQueue;
  const id=sitting.id,value=responses[qnum]??null;
  const task=saveQueue.catch(()=>{}).then(async()=>{const {data,error}=await supabase.rpc('save_exam_response',{p_sitting_id:id,p_question:qnum,p_response:value===null?null:String(value)});if(error)throw error;sitting=Array.isArray(data)?data[0]:data;responses={...sitting.responses};});
  saveQueue=task;return task;
}
async function finishExam(auto){
  if(finishing)return;finishing=true;clearInterval(timerHandle);
  await saveQueue.catch(()=>{});
  try{
    if(!sitting.completed&&Date.now()<new Date(sitting.expires_at).getTime())await persistResponses();
    const {data:session,error:sessionError}=await supabase.auth.getSession();
    if(sessionError) throw sessionError;
    const token=session?.session?.access_token;
    if(!token) throw new Error("Your sign-in session expired. Sign in again.");
    const response=await fetch("https://dyidjdagwdvsczudkryt.supabase.co/functions/v1/grade-exam",{
      method:"POST",
      headers:{
        "Content-Type":"application/json",
        "apikey":"sb_publishable_rz3w3N3QxfgLZjTa6xb-hg_mTv9YM-y",
        "Authorization":"Bearer "+token
      },
      body:JSON.stringify({sitting_id:sitting.id,auto_submitted:Boolean(auto)})
    });
    const result=await response.json();
    if(!response.ok) throw new Error(result.error||"Grading failed.");
    resultMeta=result;sitting={...sitting,completed:true,score:result.original_score??result.score,submitted_at:result.submitted_at||sitting.submitted_at||new Date().toISOString()};
    await loadSittings();
    sittingsByExam.set(sitting.exam_id,sitting);
    renderResults(result.score,result.rows,result.award,auto,result.max_score||135);
  }catch(e){
    alert(e.message||"Could not finish the paper.");
    const host=document.querySelector(".exam-main")||app;
    const retry=document.createElement("div");retry.className="end-confirm";retry.setAttribute("role","alert");retry.innerHTML='<p>Submission has not completed. Your saved answers are retained.</p><button id="retrySubmission">Retry submission</button>';host.prepend(retry);
    document.getElementById("retrySubmission").onclick=()=>finishExam(auto);
    const yes=document.getElementById("confirmFinish");if(yes)yes.disabled=false;
    if(Date.now()<new Date(sitting.expires_at).getTime())startTimer();
  }finally{finishing=false}
}
async function loadResultHistory(){
 const el=document.getElementById("savedSittings");if(!el)return;
 const sorted=allSittings.filter(e=>{
  if(centre==="hub")return true;
  if(centre==="mawa")return false;
  return belongs(catalog.find(x=>x.id===e.exam_id)||{id:e.exam_id,max_score:e.max_score,source_type:e.exam_id.startsWith("amc-up-")?"authentic_amc_past_paper":"legacy",metadata:{amc_part:e.exam_id.includes("-speed-")?"speed":e.exam_id.includes("-depth-")?"depth":null}},centre);
 });
 el.innerHTML=sorted.slice(0,centre==="hub"?30:150).map(e=>`<div class="history-row"><span>${esc(e.metadata?.title||e.exam_id)} · Attempt ${e.attempt_number||1} · ${e.completed?`${e.score}/${e.max_score} · ${formatElapsedSeconds(sittingElapsed(e))} · ${new Date(e.submitted_at).toLocaleDateString("en-AU")}`:"Open attempt · resume to finish"}</span><button class="ghost" data-result="${esc(e.id)}">${e.completed?"Review":"Resume"}</button></div>`).join("")||'<p class="muted">No sittings recorded here yet.</p>';
 el.querySelectorAll("[data-result]").forEach(b=>b.onclick=async()=>{b.disabled=true;try{const {data:row,error}=await supabase.from("exam_sittings").select("*").eq("id",b.dataset.result).single();if(error)throw error;await openSavedSitting(row)}catch(e){alert(e.message);b.disabled=false}});
}
function solutionVideo(r){
  return activeExam?.id==="amc-up-2025"&&r.question_number===17?{url:"watch-amc-2025-q17.html",title:"Watch the number-pyramid solution · under 1 minute"}:null;
}
function resultLabel(r){return r.correct?"Correct":(r.response===null||r.response===undefined||r.response==="")?"Not answered":"Incorrect"}
function renderResults(score,rows,award,auto,maxScore=135){
  document.body.classList.remove("exam-mode");
  const correctCount=rows.filter(r=>r.correct).length;
  const unanswered=rows.filter(r=>r.response===null||r.response===undefined||r.response==="").length;
  const timeSeconds=resultMeta.time_used_seconds??Math.max(0,Math.min(activeExam.duration_minutes*60,Math.round((new Date(sitting.submitted_at||Date.now()).getTime()-new Date(sitting.started_at).getTime())/1000)));
  const timeUsed=`${Math.floor(timeSeconds/60)}:${String(timeSeconds%60).padStart(2,"0")}`;
  const sectionDefs=reportSections(maxScore);
  const sectionStats=sectionDefs.map(([a,b,label])=>{const rr=rows.filter(r=>r.question_number>=a&&r.question_number<=b);return{label,earned:rr.reduce((s,r)=>s+r.earned,0),max:rr.reduce((s,r)=>s+r.marks,0),correct:rr.filter(r=>r.correct).length,count:rr.length}});
  const finalFive=maxScore===135||activeExam?.metadata?.amc_part==="depth"?rows.filter(r=>r.question_number>=26&&r.question_number<=30):[];
  const finalFiveCorrect=finalFive.filter(r=>r.correct).length;
  const finalFiveEarned=finalFive.reduce((s,r)=>s+r.earned,0);
  const finalFiveMax=finalFive.reduce((s,r)=>s+r.marks,0);

  const awardNote=maxScore===135
    ? (award.estimated
        ? esc(awards.practice_estimate_wa.label)+". Official AMT cut-offs vary by year and WA cohort; a verified paper-year WA cutoff will replace this estimate whenever available."
        : "This paper uses a verified award-cutoff table stored with the exam.")
    : activeExam?.metadata?.amc_part?"Split AMC practice results are scores and times, not official AMC award bands. A full sitting is needed to estimate an award.":"This selective-maths practice paper is reported as a raw score only; no official Rossmoyne award bands are invented.";
  const courseSlot=0;theme(activeExam);const partMarkup=partReport(rows,timeSeconds);
  app.innerHTML=`${partMarkup}<section class="panel result-hero"><div class="eyebrow">${auto?"TIME EXPIRED · ":""}${activeExam?.metadata?.amc_part?"TRAINING COMPLETE":"PAPER COMPLETE"}</div><div class="score-big">${score}<span class="muted" style="font-size:.25em"> / ${maxScore}</span></div><div class="award-badge">${esc(award?.label|| (activeExam?.metadata?.amc_part?"Timed part recorded":"Practice paper complete"))}</div><p class="paper-locked">Attempt ${sitting.attempt_number||1} submitted and locked · review available anytime ${activeExam.repeatable?"· new attempts allowed":"· no further attempts"}</p>${resultMeta.review_corrected?`<p class="notice-box">Answer-key correction: your original recorded score was ${resultMeta.original_score}/${maxScore}. This review uses the corrected keys and shows ${score}/${maxScore}. Your original answers and submission are preserved.</p>`:""}<p class="estimate-note">${awardNote}</p></section>
  <section class="profile-grid" style="margin-top:18px"><div class="panel profile-stat"><b>${correctCount}</b><span>questions correct</span></div><div class="panel profile-stat"><b>${unanswered}</b><span>unanswered</span></div><div class="panel profile-stat"><b>${timeUsed}</b><span>time used</span></div><div class="panel profile-stat"><b>${Math.round(score/maxScore*100)}%</b><span>raw mark percentage</span></div></section>
  <section class="panel result-card"><h2>Paper sections</h2>${(maxScore===135||activeExam?.metadata?.amc_part==="depth")?`<div class="final-five-result"><div><span class="eyebrow">AMC FINAL FIVE</span><b>${finalFiveCorrect} / 5 correct</b></div><div><span class="muted">Q26–Q30 marks</span><b>${finalFiveEarned} / ${finalFiveMax}</b></div></div>`:""}<table class="result-table"><thead><tr><th>Section</th><th>Correct</th><th>Marks</th></tr></thead><tbody>${sectionStats.map(s=>`<tr><td>${esc(s.label)}</td><td>${s.correct} / ${s.count}</td><td>${s.earned} / ${s.max}</td></tr>`).join("")}</tbody></table></section>
  <section class="panel result-card" id="examDiagnostics"></section><section class="panel result-card"><h2>Question-by-question results</h2><table class="result-table"><thead><tr><th>Q</th><th>Your answer</th><th>Result</th><th>Marks</th><th>Learn</th></tr></thead><tbody>${rows.map(r=>`<tr><td>${r.question_number}</td><td>${esc(r.response??"—")}</td><td class="${r.correct?"ok":"bad"}">${resultLabel(r)}</td><td>${r.earned} / ${r.marks}</td><td><button class="solution-link" data-solution="${r.question_number}">Show solution</button>${solutionVideo(r)?`<a class="solution-link" href="${solutionVideo(r).url}" target="_blank" rel="noopener">Watch video ↗</a>`:""}</td></tr>`).join("")}</tbody></table></section>
  <section class="panel result-card"><h2>Turn the result into learning</h2><p>Your missed skills are saved to your repair queue. Identify what went wrong, work through a supported correction, then solve a fresh problem independently. A changed example returns after three more completed sessions.</p><a class="primary" href="index.html?view=repairs">Open my repair queue</a><h2>Review each problem</h2>${rows.map(r=>`<details id="solution-${r.question_number}" class="question-review"><summary>Question ${r.question_number} · ${resultLabel(r)} · ${r.earned}/${r.marks}</summary><p><b>Problem</b><br>${esc(r.stem)}</p>${r.image_ref||r.figure_svg?`<div class="exam-visual">${r.image_ref||r.figure_svg}</div>`:""}${!r.image_ref&&r.choices?.length?`<ol class="review-choices" type="A">${r.choices.map(c=>`<li>${typeof c==='string'?esc(c):`${c.visual_html||''}${esc(c.text||'')}`}</li>`).join('')}</ol>`:""}<p><b>Your answer:</b> ${esc(r.response??"—")}<br><b>Correct answer:</b> ${esc(typeof r.correct_answer==="object"?JSON.stringify(r.correct_answer):r.correct_answer)}</p>${r.explanation?`<p class="math-copy"><b>Worked explanation</b><br>${esc(r.explanation)}</p>`:`<p class="muted">The source answer key is verified. A worked explanation for this question has not yet been added.</p>`}${solutionVideo(r)?`<a class="solution-video-link" href="${solutionVideo(r).url}" target="_blank" rel="noopener">▶ ${solutionVideo(r).title}</a>`:""}</details>`).join("")}
  <div class="complete-row"><a class="secondary" href="./">Return to Summit One</a>${activeExam.repeatable?`<button id="retryPaper" class="secondary">Start another practice attempt</button>`:""}<button id="backTests" class="primary">Back to exam section</button></div></section>`;
  const diagnosticsEl=document.getElementById("examDiagnostics");
  mountExamDiagnostics(diagnosticsEl,{rows,user,sitting,exam:activeExam}).catch(e=>{diagnosticsEl.textContent="Learning report unavailable: "+e.message});
  wireQuestionZoom();
  document.querySelectorAll("[data-solution]").forEach(button=>button.onclick=()=>{const detail=document.getElementById("solution-"+button.dataset.solution);detail.open=true;detail.scrollIntoView({behavior:"smooth",block:"start"});detail.querySelector("summary").focus()});
  const back=document.getElementById("backTests");
  if(back)back.onclick=()=>{sitting=null;activeExam=null;questions=[];responses={};renderLibrary()};
  const retry=document.getElementById('retryPaper');if(retry)retry.onclick=()=>prepareExam(activeExam.id).catch(showExamError);

}
boot().catch(e=>{app.innerHTML='<section class="panel hero-panel"><h1>Test Centre error</h1><p class="muted">'+esc(e.message)+'</p></section>'});

