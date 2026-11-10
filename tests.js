import { supabase, currentUser } from "./supabase-client.js";

const app=document.getElementById("examApp");
let user, catalog=[], awards, activeExam=null, questions=[], sitting=null, qIndex=0, responses={}, typedInteger={}, timerHandle=null;
const esc=s=>String(s??"").replace(/[&<>"']/g,m=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[m]));
const norm=s=>String(s??"").trim().toLowerCase().replace(/\s+/g,"").replace(/[.,;:]$/g,"");

async function boot(){
  user=await currentUser();if(!user){location.href="login.html";return}
  awards=await fetch("data/amc-awards.json").then(r=>r.json());
  const {data,error}=await supabase.from("exam_catalog").select("*").eq("active",true).order("year",{ascending:false});
  if(error)throw error;catalog=data||[];
  const open=await loadOpenSitting();
  if(open){await resumeSitting(open);return}
  renderLibrary();
}
async function loadOpenSitting(){
  const {data}=await supabase.from("exam_sittings").select("*").eq("user_id",user.id).eq("completed",false).order("started_at",{ascending:false}).limit(1).maybeSingle();
  return data;
}
function renderLibrary(){
  app.innerHTML=`<section class="panel test-hero"><div class="eyebrow">SEPARATE EXAM MODE</div><h1>AMC Test Centre</h1><p class="muted">Sit a complete paper only when you choose. Exam mode has no hints, no solution videos and no correctness feedback until the sitting ends.</p>
  <div class="notice-box"><b>Official format:</b> Upper Primary is 30 questions in 60 minutes: Questions 1–25 multiple choice; Questions 26–30 integer answer. The practice interface reproduces the timing, navigation and save behaviour without copying AMT branding.</div>
  <div class="test-grid">${catalog.map(exam=>`<article class="panel test-card"><div class="eyebrow">${esc(exam.source_type.replaceAll("_"," "))}</div><h3>${esc(exam.title)}</h3><div class="test-meta"><span class="phase-chip">${esc(exam.division)}</span><span class="phase-chip">${exam.duration_minutes} min</span><span class="phase-chip">135 marks</span></div><button class="primary startExam" data-id="${esc(exam.id)}">Start paper</button></article>`).join("")||`<article class="panel test-card"><div class="eyebrow">ENGINE READY</div><h3>Your first full AMC paper goes here</h3><p class="muted">The timer, navigation, autosave, scoring, per-question results and award calculation are already built. No full past paper has been installed yet.</p><span class="type-chip">Awaiting PDF</span></article>`}</div>
  <p class="footer-note">Official AMC award cut-offs are region/year specific and vary with paper difficulty. When a verified WA cutoff is available for an installed paper, that cutoff is used. Otherwise results show a clearly labelled WA practice estimate.</p></section>`;
  document.querySelectorAll(".startExam").forEach(b=>b.onclick=()=>startExam(b.dataset.id));
}
async function startExam(id){
  activeExam=catalog.find(x=>x.id===id);if(!activeExam)return;
  if(innerWidth<650&&!confirm("The official AMC is not intended for a phone-sized screen. You can practise here, but an iPad or computer is better for realistic rehearsal. Continue?"))return;
  const {data:q,error}=await supabase.from("exam_questions_student").select("*").eq("exam_id",id).order("question_number");
  if(error)throw error;if((q||[]).length!==30){alert("This paper is not complete yet.");return}
  questions=q;responses={};typedInteger={};qIndex=0;
  const start=new Date(),expires=new Date(start.getTime()+activeExam.duration_minutes*60000);
  const {data:s,error:e}=await supabase.from("exam_sittings").insert({
    user_id:user.id,exam_id:id,exam_year:activeExam.year,started_at:start.toISOString(),expires_at:expires.toISOString(),completed:false,max_score:activeExam.max_score,responses:{},integer_save_times:{},metadata:{title:activeExam.title,student_year:activeExam.student_year}
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
  <article class="panel exam-main"><div class="qhead"><div class="qnum">QUESTION ${q.question_number} / 30</div><div class="marks">${q.marks} mark${q.marks===1?"":"s"}</div></div><div class="stem">${esc(q.stem)}</div><div id="answerArea"></div>
  <div class="exam-actions"><button id="prev" class="ghost" ${qIndex===0?"disabled":""}>Previous</button><button id="next" class="primary">${qIndex===29?"Review menu":"Next"}</button></div></article></section>`;
  renderAnswer(q);
  document.querySelectorAll("[data-q]").forEach(b=>b.onclick=()=>{qIndex=Number(b.dataset.q);renderExam()});
  document.getElementById("prev").onclick=()=>{if(qIndex>0){qIndex--;renderExam()}};
  document.getElementById("next").onclick=()=>{if(qIndex<29){qIndex++;renderExam()}};
  document.getElementById("finish").onclick=()=>{if(confirm("Finish this paper? You will not be able to change answers afterwards."))finishExam(false)};
}
function renderAnswer(q){
  const area=document.getElementById("answerArea"),saved=responses[q.question_number];
  if(q.question_type==="multiple_choice"){
    const choices=Array.isArray(q.choices)?q.choices:[];
    area.innerHTML='<div class="choices">'+choices.map((c,i)=>`<button class="choice ${saved===String.fromCharCode(65+i)?"selected":""}" data-choice="${String.fromCharCode(65+i)}"><span class="choice-letter">${String.fromCharCode(65+i)}</span><span>${esc(typeof c==="string"?c:c.text||"")}</span></button>`).join("")+'</div>';
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
  app.innerHTML=`<section class="panel result-hero"><div class="eyebrow">${auto?"TIME EXPIRED · ":""}PAPER COMPLETE</div><div class="score-big">${score}<span class="muted" style="font-size:.25em"> / ${maxScore}</span></div><div class="award-badge">${esc(award.label)}</div><p class="estimate-note">${award.estimated?esc(awards.practice_estimate_wa.label)+". Official AMT cut-offs vary by year and WA cohort; a verified paper-year WA cutoff will replace this estimate whenever available.":"This paper uses a verified award-cutoff table stored with the exam."}</p></section>
  <section class="panel result-card"><h2>Question-by-question results</h2><table class="result-table"><thead><tr><th>Q</th><th>Your answer</th><th>Result</th><th>Marks</th></tr></thead><tbody>${rows.map(r=>`<tr><td>${r.question_number}</td><td>${esc(r.response??"—")}</td><td class="${r.correct?"ok":"bad"}">${r.correct?"Correct":"Incorrect"}</td><td>${r.earned} / ${r.marks}</td></tr>`).join("")}</tbody></table></section>
  <section class="panel result-card"><h2>Review each problem</h2>${rows.map(r=>`<details class="question-review"><summary>Question ${r.question_number} · ${r.correct?"✓ Correct":"Review"} · ${r.earned}/${r.marks}</summary><p><b>Problem</b><br>${esc(r.stem)}</p><p><b>Your answer:</b> ${esc(r.response??"—")}<br><b>Correct answer:</b> ${esc(typeof r.correct_answer==="object"?JSON.stringify(r.correct_answer):r.correct_answer)}</p>${r.explanation?`<p><b>Worked explanation</b><br>${esc(r.explanation)}</p>`:""}</details>`).join("")}<div class="complete-row"><a class="secondary" href="./">Return to Summit One</a><button id="backTests" class="primary">Test Centre</button></div></section>`;
  document.getElementById("backTests").onclick=()=>{sitting=null;activeExam=null;questions=[];responses={};renderLibrary()};
}
boot().catch(e=>{app.innerHTML='<section class="panel hero-panel"><h1>Test Centre error</h1><p class="muted">'+esc(e.message)+'</p></section>'});
