
if("serviceWorker" in navigator){window.addEventListener("load",()=>navigator.serviceWorker.register("./sw.js").catch(()=>{}));}
import { supabase, currentUser, loadProgress, saveProgress, upsertSession } from "./supabase-client.js";

const app=document.getElementById("examApp");
let user, catalog=[], awards, activeExam=null, questions=[], sitting=null, qIndex=0, responses={}, typedInteger={}, timerHandle=null;
let awardYear=Number(localStorage.getItem("summitSchoolYear")||5);
const params=new URLSearchParams(location.search); const courseMode=params.get("course")==="1";
const esc=s=>String(s??"").replace(/[&<>"']/g,m=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[m]));
const norm=s=>String(s??"").trim().toLowerCase().replace(/\s+/g,"").replace(/[.,;:]$/g,"");

async function boot(){
  user=await currentUser();if(!user){location.href="login.html";return}
  awards=await fetch("data/amc-awards.json").then(r=>r.json());
  const {data,error}=await supabase.from("exam_catalog").select("*").eq("active",true).order("year",{ascending:false});
  if(error)throw error;catalog=data||[];
  const open=await loadOpenSitting();
  if(open){await resumeSitting(open);return}
  const slot=Number(params.get("slot")||0);
  if(slot){
    const {data:bySlot}=await supabase.from("exam_catalog").select("*").eq("session_slot",slot).maybeSingle();
    if(bySlot){renderCourseExamIntro(bySlot);return}
  }
  renderLibrary();
}
function renderCourseExamIntro(exam){
  const isAMC=exam.max_score===135;
  app.innerHTML=`<section class="panel test-hero"><div class="eyebrow">CANONICAL SESSION ${exam.session_slot}</div><h1>${esc(exam.title)}</h1><p class="muted">${isAMC?"Full AMC-format rehearsal: 30 questions, 60 minutes, 135 marks.":"Original Rossmoyne-style selective-mathematics rehearsal: 23 questions, 100 marks. The 60-minute clock is a Summit One home-practice target, not a claim about the official Rossmoyne entrance-test duration."}</p><div class="notice-box"><b>Before you start:</b> close notes and solution pages. The timer begins only when you press Start. Answers are autosaved where appropriate; numeric AMC answers require the explicit Save answer button.</div><div class="complete-row"><a class="ghost" href="./">Return to mission</a><button id="startCourseExam" class="primary cta">Start timed paper</button></div></section>`;
  document.getElementById("startCourseExam").onclick=()=>{catalog=[exam];startExam(exam.id)};
}
async function loadOpenSitting(){
  const {data}=await supabase.from("exam_sittings").select("*").eq("user_id",user.id).eq("completed",false).order("started_at",{ascending:false}).limit(1).maybeSingle();
  return data;
}
function examCard(exam){
  return `<article class="panel test-card"><div class="eyebrow">${esc(exam.source_type.replaceAll("_"," "))}</div><h3>${esc(exam.title)}</h3><div class="test-meta"><span class="phase-chip">${esc(exam.division)}</span><span class="phase-chip">${exam.duration_minutes} min</span><span class="phase-chip">${exam.max_score} marks</span></div><button class="primary startExam" data-id="${esc(exam.id)}">Start paper</button></article>`;
}
function renderLibrary(){
  const amc=catalog.filter(exam=>exam.max_score===135);
  const official=amc.filter(exam=>exam.source_type==="authentic_amc_past_paper");
  const mocks=amc.filter(exam=>exam.source_type!=="authentic_amc_past_paper");
  const cards=list=>list.map(exam=>`<article class="panel test-card"><div class="eyebrow">${exam.source_type==="authentic_amc_past_paper"?"AUTHENTIC PAST PAPER":"SUMMIT ONE AUTHORED MOCK"}</div><h3>${esc(exam.title)}</h3><div class="test-meta"><span class="phase-chip">${esc(exam.division)}</span><span class="phase-chip">${exam.duration_minutes} min</span><span class="phase-chip">${exam.max_score} marks</span></div><button class="primary startExam" data-id="${esc(exam.id)}">Start paper</button></article>`).join("");
  app.innerHTML=`<section class="panel test-hero"><div class="eyebrow">SEPARATE EXAM MODE</div><h1>AMC Test Centre</h1><p class="muted">Choose a complete paper only when you want a full exam sitting. Exam mode has no hints, no solution videos and no correctness feedback until the sitting is sealed.</p>
  <div class="notice-box"><b>Official Upper Primary workflow:</b> 30 questions in 60 minutes; Questions 1–25 multiple choice and Questions 26–30 integer answer. Use the question menu to skip/backtrack. Integer answers count only after <b>Save answer</b>. Submitted answers are retained when time expires.</div>
  <h2 style="margin-top:24px">Authentic past AMC papers</h2><p class="muted">Full papers supplied by the family are installed here as protected authenticated assessments.</p>
  <div class="complete-row"><label class="answer-label" style="max-width:220px">Award cohort<select id="awardYear" class="np-speed"><option value="5" ${awardYear===5?"selected":""}>Year 5</option><option value="6" ${awardYear===6?"selected":""}>Year 6</option></select></label><span class="muted">Used when an official WA paper-year cutoff cannot be verified.</span></div>
  <div class="test-grid">${official.length?cards(official):`<article class="panel test-card"><div class="eyebrow">READY FOR IMPORT</div><h3>Past-paper engine is ready</h3><p class="muted">No full authentic past paper has been installed yet. The secure timer, navigation, grading and results engine is complete.</p><span class="type-chip">Awaiting first PDF</span></article>`}</div>
  <h2 style="margin-top:30px">Summit One authored mocks</h2><p class="muted">Original 135-mark papers for repeated full-format practice. These are not official AMT papers.</p><div class="test-grid">${cards(mocks)}</div>
  <p class="footer-note">AMT determines official awards by year level and region, and raw-score cutoffs vary with each paper. Authentic papers use verified WA paper-year cutoffs when available. Otherwise the results page labels the displayed band as a WA practice estimate.</p></section>`;
  const yearSelect=document.getElementById("awardYear"); if(yearSelect)yearSelect.onchange=()=>{awardYear=Number(yearSelect.value);localStorage.setItem("summitSchoolYear",String(awardYear))};
  document.querySelectorAll(".startExam").forEach(b=>b.onclick=()=>startExam(b.dataset.id));
}
async function startExam(id){
  activeExam=catalog.find(x=>x.id===id);if(!activeExam)return;
  if(innerWidth<650){const message=activeExam.max_score===135?"The official AMC is not intended for a phone-sized screen. You can practise here, but an iPad or computer is better for realistic rehearsal. Continue?":"A larger screen is recommended for realistic selective-maths rehearsal. Continue on this phone?";if(!confirm(message))return}
  const {data:q,error}=await supabase.from("exam_questions_student").select("*").eq("exam_id",id).order("question_number");
  if(error)throw error;if((q||[]).length!==(activeExam.question_count||30)){alert("This paper is not complete yet.");return}
  questions=q;responses={};typedInteger={};qIndex=0;
  const start=new Date(),expires=new Date(start.getTime()+activeExam.duration_minutes*60000);
  const {data:s,error:e}=await supabase.from("exam_sittings").insert({
    user_id:user.id,exam_id:id,exam_year:activeExam.year,started_at:start.toISOString(),expires_at:expires.toISOString(),completed:false,max_score:activeExam.max_score,responses:{},integer_save_times:{},metadata:{title:activeExam.title,student_year:activeExam.source_type==="authentic_amc_past_paper"?awardYear:(activeExam.student_year||awardYear),course_slot:courseMode?(activeExam.session_slot||null):null,course_mode:courseMode}
  }).select().single();
  if(e)throw e;sitting=s;renderExam();startTimer();
}
async function resumeSitting(s){
  const {data:exam}=await supabase.from("exam_catalog").select("*").eq("id",s.exam_id).single();activeExam=exam;
  const {data:q}=await supabase.from("exam_questions_student").select("*").eq("exam_id",s.exam_id).order("question_number");questions=q||[];
  sitting=s;responses=s.responses||{};typedInteger={};qIndex=0;
  if(new Date(s.expires_at)<=new Date()){await finishExam(true);return}
  renderExam();startTimer();
}
function startTimer(){
  clearInterval(timerHandle);
  const tick=()=>{
    const left=Math.max(0,new Date(sitting.expires_at).getTime()-Date.now());
    const mm=String(Math.floor(left/60000)).padStart(2,"0"),ss=String(Math.floor((left%60000)/1000)).padStart(2,"0");
    const el=document.getElementById("timer");if(el)el.textContent=mm+":"+ss;
    if(left<=0){clearInterval(timerHandle);finishExam(true)}
  };tick();timerHandle=setInterval(tick,500);
}
function renderExam(){
  const q=questions[qIndex];if(!q)return;
  app.innerHTML=`<section class="exam-shell">
  <aside class="panel exam-sidebar"><div class="eyebrow">TIME REMAINING</div><div id="timer" class="timer">60:00</div><div class="qnav">${questions.map((x,i)=>`<button data-q="${i}" class="${i===qIndex?"current":""} ${responses[x.question_number]!==undefined?"answered":""}">${x.question_number}</button>`).join("")}</div><button id="finish" class="danger" style="width:100%;margin-top:15px">Finish paper</button></aside>
  <article class="panel exam-main"><div class="qhead"><div class="qnum">QUESTION ${q.question_number} / ${questions.length}</div><div class="marks">${q.marks} mark${q.marks===1?"":"s"}</div></div><div class="stem">${esc(q.stem)}</div>${q.image_ref?`<div class="exam-visual">${q.image_ref}</div>`:""}<div id="answerArea"></div>
  <div class="exam-actions"><button id="prev" class="ghost" ${qIndex===0?"disabled":""}>Previous</button><button id="next" class="primary">${qIndex===questions.length-1?"Review menu":"Next"}</button></div></article></section>`;
  renderAnswer(q);
  document.querySelectorAll("[data-q]").forEach(b=>b.onclick=()=>{qIndex=Number(b.dataset.q);renderExam()});
  document.getElementById("prev").onclick=()=>{if(qIndex>0){qIndex--;renderExam()}};
  document.getElementById("next").onclick=()=>{if(qIndex<questions.length-1){qIndex++;renderExam()}};
  document.getElementById("finish").onclick=()=>{if(confirm("Finish this paper? You will not be able to change answers afterwards."))finishExam(false)};
}
function renderAnswer(q){
  const area=document.getElementById("answerArea"),saved=responses[q.question_number];
  if(q.question_type==="multiple_choice"){
    const choices=Array.isArray(q.choices)?q.choices:[];
    area.innerHTML='<div class="choices">'+choices.map((c,i)=>`<button class="choice ${saved===String.fromCharCode(65+i)?"selected":""}" data-choice="${String.fromCharCode(65+i)}"><span class="choice-letter">${String.fromCharCode(65+i)}</span><span class="choice-content">${typeof c==="string"?esc(c):`${c.visual_html||""}${c.text?`<span>${esc(c.text)}</span>`:""}`}</span></button>`).join("")+'</div>';
    area.querySelectorAll("[data-choice]").forEach(b=>b.onclick=async()=>{responses[q.question_number]=b.dataset.choice;await persistResponses();renderExam()});
  }else{
    const typed=typedInteger[q.question_number]??(saved??"");
    area.innerHTML=`<div class="integer-row"><label>Your integer answer<br><input id="integerInput" inputmode="numeric" pattern="[0-9]*" value="${esc(typed)}"></label><button id="saveInteger" class="primary">Save answer</button><span id="saveState" class="${saved!==undefined?"saved":"unsaved"}">${saved!==undefined?"Saved":"Not saved"}</span></div><p class="muted" style="margin-top:10px">Typing is not enough. Press <b>Save answer</b> before leaving the question.</p>`;
    const inp=document.getElementById("integerInput");inp.oninput=()=>{typedInteger[q.question_number]=inp.value;document.getElementById("saveState").className="unsaved";document.getElementById("saveState").textContent="Not saved"};
    document.getElementById("saveInteger").onclick=async()=>{const v=inp.value.trim();if(!/^\d+$/.test(v)){alert("Enter a whole-number answer.");return}responses[q.question_number]=v;typedInteger[q.question_number]=v;await persistResponses(true,q.question_number);renderExam()};
  }
}
async function persistResponses(integerSave=false,qnum=null){
  const patch={responses};
  if(integerSave){
    const times={...(sitting.integer_save_times||{})};times[qnum]=new Date().toISOString();patch.integer_save_times=times;sitting.integer_save_times=times;
  }
  const {data,error}=await supabase.from("exam_sittings").update(patch).eq("id",sitting.id).select().single();if(error)throw error;sitting=data;
}
async function finishExam(auto){
  clearInterval(timerHandle);
  try{
    await persistResponses();
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
    sitting={...sitting,completed:true,score:result.score};
    renderResults(result.score,result.rows,result.award,auto,result.max_score||135);
  }catch(e){
    alert(e.message||"Could not finish the paper.");
    startTimer();
  }
}
function renderResults(score,rows,award,auto,maxScore=135){
  const correctCount=rows.filter(r=>r.correct).length;
  const unanswered=rows.filter(r=>r.response===null||r.response===undefined||r.response==="").length;
  const timeSeconds=Math.max(0,Math.round((new Date(sitting.submitted_at||Date.now()).getTime()-new Date(sitting.started_at).getTime())/1000));
  const timeUsed=`${Math.floor(timeSeconds/60)}:${String(timeSeconds%60).padStart(2,"0")}`;
  const sectionDefs=maxScore===135?[[1,10,"Questions 1–10"],[11,20,"Questions 11–20"],[21,30,"Questions 21–30"]]:[[1,7,"Section 1"],[8,13,"Section 2"],[14,18,"Section 3"],[19,23,"Section 4"]];
  const sectionStats=sectionDefs.map(([a,b,label])=>{const rr=rows.filter(r=>r.question_number>=a&&r.question_number<=b);return{label,earned:rr.reduce((s,r)=>s+r.earned,0),max:rr.reduce((s,r)=>s+r.marks,0),correct:rr.filter(r=>r.correct).length,count:rr.length}});

  const awardNote=maxScore===135
    ? (award.estimated
        ? esc(awards.practice_estimate_wa.label)+". Official AMT cut-offs vary by year and WA cohort; a verified paper-year WA cutoff will replace this estimate whenever available."
        : "This paper uses a verified award-cutoff table stored with the exam.")
    : "This selective-maths practice paper is reported as a raw score only; no official Rossmoyne award bands are invented.";
  const courseSlot=sitting?.metadata?.course_mode===true?Number(sitting?.metadata?.course_slot||0):0;
  app.innerHTML=`<section class="panel result-hero"><div class="eyebrow">${auto?"TIME EXPIRED · ":""}PAPER COMPLETE</div><div class="score-big">${score}<span class="muted" style="font-size:.25em"> / ${maxScore}</span></div><div class="award-badge">${esc(award.label||"Practice paper complete")}</div><p class="estimate-note">${awardNote}</p></section>
  <section class="profile-grid" style="margin-top:18px"><div class="panel profile-stat"><b>${correctCount}</b><span>questions correct</span></div><div class="panel profile-stat"><b>${unanswered}</b><span>unanswered</span></div><div class="panel profile-stat"><b>${timeUsed}</b><span>time used</span></div><div class="panel profile-stat"><b>${Math.round(score/maxScore*100)}%</b><span>raw mark percentage</span></div></section>
  <section class="panel result-card"><h2>Paper sections</h2><table class="result-table"><thead><tr><th>Section</th><th>Correct</th><th>Marks</th></tr></thead><tbody>${sectionStats.map(s=>`<tr><td>${esc(s.label)}</td><td>${s.correct} / ${s.count}</td><td>${s.earned} / ${s.max}</td></tr>`).join("")}</tbody></table></section>
  <section class="panel result-card"><h2>Question-by-question results</h2><table class="result-table"><thead><tr><th>Q</th><th>Your answer</th><th>Result</th><th>Marks</th></tr></thead><tbody>${rows.map(r=>`<tr><td>${r.question_number}</td><td>${esc(r.response??"—")}</td><td class="${r.correct?"ok":"bad"}">${r.correct?"Correct":"Incorrect"}</td><td>${r.earned} / ${r.marks}</td></tr>`).join("")}</tbody></table></section>
  <section class="panel result-card"><h2>Review each problem</h2>${rows.map(r=>`<details class="question-review"><summary>Question ${r.question_number} · ${r.correct?"✓ Correct":"Review"} · ${r.earned}/${r.marks}</summary><p><b>Problem</b><br>${esc(r.stem)}</p><p><b>Your answer:</b> ${esc(r.response??"—")}<br><b>Correct answer:</b> ${esc(typeof r.correct_answer==="object"?JSON.stringify(r.correct_answer):r.correct_answer)}</p>${r.explanation?`<p><b>Worked explanation</b><br>${esc(r.explanation)}</p>`:""}</details>`).join("")}
  <div class="complete-row"><a class="secondary" href="./">Return to Summit One</a>${courseSlot?`<button id="completeCourseMock" class="primary">Complete Course Session ${courseSlot}</button>`:`<button id="backTests" class="primary">Test Centre</button>`}</div></section>`;
  const back=document.getElementById("backTests");
  if(back)back.onclick=()=>{sitting=null;activeExam=null;questions=[];responses={};renderLibrary()};
  const complete=document.getElementById("completeCourseMock");
  if(complete)complete.onclick=async()=>{
    complete.disabled=true;complete.textContent="Locking course session…";
    try{
      const p=await loadProgress();
      if((p?.completed_sessions||0)!==courseSlot-1) throw new Error("This result is saved, but it is not the next canonical course session and cannot advance the course.");
      const type=maxScore===135?"AMC MOCK":"ROSSMOYNE MOCK";
      await upsertSession({
        session_number:courseSlot,
        session_key:`S${String(courseSlot).padStart(3,"0")}`,
        completed_at:new Date().toISOString(),
        immutable:true,
        answers:{exam_sitting_id:sitting.id},
        working:{},
        evidence:{timed_exam:{score,max_score:maxScore,independent:true}},
        summary:{focus:activeExam.title,type,exam_id:activeExam.id,score,max_score:maxScore}
      });
      const done=Math.max(p?.completed_sessions||0,courseSlot);
      const percent=done/372*100,rank=Math.max(1,Math.min(20,Math.ceil(Math.max(.0001,percent)/5)));
      await saveProgress({completed_sessions:done,current_session:Math.min(372,done+1),xp:done*100,rank,overall_percent:Number(percent.toFixed(2))});
      location.href="./";
    }catch(e){alert(e.message||"Could not complete the course session.");complete.disabled=false;complete.textContent=`Complete Course Session ${courseSlot}`}
  };
}
boot().catch(e=>{app.innerHTML='<section class="panel hero-panel"><h1>Test Centre error</h1><p class="muted">'+esc(e.message)+'</p></section>'});
