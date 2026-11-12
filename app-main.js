import {selectOriginalProblems,familySeen,reasoningReady,applicationStatus,mountReasoning,originalFigure,LEARNING_VERSION} from './original-learning.js?v=original-transfer-20261112';
import {introductionHTML,lessonPlan,investigationIntroHTML,investigationWarmupHTML} from './session-intros.js?v=original-transfer-20261112';

if("serviceWorker" in navigator){window.addEventListener("load",()=>navigator.serviceWorker.register("./sw.js").catch(()=>{}));}
import { supabase, loadProgress, saveProgress, signOut, currentUser, upsertSession } from "./supabase-client.js?v=auth-20261112";
import { mountNarratedPlayer } from "./lesson-player.js";
import {methods,skillFor,recallState} from "./curriculum.js?v=original-transfer-20261112";
import {lessonCard,mountCheck,mountRetrieval,readinessHTML} from "./learning-ui.js?v=original-transfer-20261112";
import { problemFigure } from "./problem-figures.js";

const app=document.getElementById("app");
const problemTemplate=document.getElementById("problemTemplate");
let course=[], teaching=[], mawa=[], rossMap=[], taxonomy=null, milestones=null, problemIndex=[], progress=null, user=null, activeView="home", activeStage=0;
let lessonManifest=[];
let currentProblems=[], currentMawa=null, sessionDraft={answers:{},working:{},evidence:{},summary:{}};
let attemptedProblemIds=new Set();
let completedRecords=[],attemptHistory=[],recentExams=[];
let editingSession=null,autosaveTimer=null,draftDirty=false;
const draftKey=s=>`summit-draft:${user.id}:${s.slot}`;
function rememberDraft(){
 if(!editingSession)return;
 draftDirty=true;saveStatus="Changes saved on this device; syncing…";refreshSyncIndicator();
 localStorage.setItem(draftKey(editingSession),JSON.stringify({updated_at:new Date().toISOString(),draft:sessionDraft}));
 clearTimeout(autosaveTimer);const session=editingSession;
 autosaveTimer=setTimeout(()=>saveDraft(session).catch(()=>{}),700);
}
document.addEventListener('input',()=>{if(editingSession&&document.querySelector('.session-page'))rememberDraft()});
window.addEventListener('beforeunload',e=>{if(draftDirty){e.preventDefault();e.returnValue=''}});


const esc=s=>String(s??"").replace(/[&<>"']/g,m=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[m]));
const pct=n=>Math.max(0,Math.min(100,Number(n)||0));
const hash=s=>{let h=2166136261;for(const c of String(s)){h^=c.charCodeAt(0);h=Math.imul(h,16777619)}return h>>>0};
const normalize=s=>String(s??"").toLowerCase().replace(/\s+/g,"").replace(/[×·]/g,"*").replace(/[²]/g,"^2").replace(/[³]/g,"^3").replace(/[.,;:]$/g,"");
const rankNames=["Pathfinder","Pattern Scout","Model Builder","Logic Ranger","Number Navigator","Geometry Pilot","Counting Specialist","Invariant Hunter","Transfer Thinker","Proof Builder","Problem Solver","Strategy Captain","Olympiad Explorer","Insight Engineer","Reasoning Commander","AMC Specialist","MAWA Specialist","Rossmoyne Specialist","Summit Elite","135 Master"];
function finalVideoUrl(videoId){
  const id=String(videoId||"");
  // Only concept/worked-example T videos are public. Every challenge solution is attempt-gated.
  if(!/^T\d{2}\.(?:1|2|3|E)$/.test(id))return "";
  if(id==="T01.2")return ""; // George retired; use natural on-device narration until new T01.2 master is approved.
  if(id==="T02.1")return "media/T02.1.mp4?v=studio-v4";
  if(id==="T02.2")return "media/T02.2.mp4?v=studio-v1";
  return ""; // Only verified published masters are offered; other lessons use their written/audio teaching.
}
async function recordVideoEvidence(sessionNumber,videoId,kind,detail={}){
  if(!sessionNumber||!videoId)return;
  const key=`video:${videoId}`;
  const prev=sessionDraft.evidence?.[key]||{};
  sessionDraft.evidence={...(sessionDraft.evidence||{}),[key]:{...prev,kind,status:"viewed",independent_credit:false,last_viewed_at:new Date().toISOString(),...detail}};
  try{
    await upsertSession({session_number:sessionNumber,session_key:`S${String(sessionNumber).padStart(3,"0")}`,answers:sessionDraft.answers,working:sessionDraft.working,evidence:sessionDraft.evidence,summary:sessionDraft.summary});
  }catch(e){console.warn("Video evidence save failed",e)}
}
let saveStatus="Loaded from cloud";
window.addEventListener("summit-save",e=>{saveStatus=e.detail;refreshSyncIndicator()});
function syncStatusText(){return navigator.onLine?saveStatus:"Offline — changes are not yet saved"}
function refreshSyncIndicator(){const el=document.getElementById("syncStatus");if(el){el.textContent=syncStatusText();el.parentElement.style.color=navigator.onLine?"var(--green)":"var(--gold)"}}
window.addEventListener("online",refreshSyncIndicator);window.addEventListener("offline",refreshSyncIndicator);

const chapterRules=[
  [/digit|place-value|cryptarithm|palindrome|repunits?/i,"T11"],
  [/divisib|remainder|last-digit|clock|cycle|multiple|hcf|lcm/i,"T03"],
  [/prime|factor/i,"T04"],
  [/probab/i,"T08"],
  [/angle|polygon/i,"T12"],
  [/area|perimeter|cube|solid|surface|volume|painted|net/i,"T13"],
  [/symmetry|transform|tessell/i,"T15"],
  [/route|adjacency|grid lines|crossings|coordinates/i,"T14"],
  [/ratio|rate|speed|average|weighted|fraction|percentage|proportion/i,"T16"],
  [/count|arrangement|combination|enumeration|partition|inclusion|paths/i,"T05"],
  [/double-count|shared objects/i,"T06"],
  [/optimis|maximum|minimum/i,"T07"],
  [/recurrence|sequence|growth|increment|pattern/i,"T10"],
  [/proof|truth-teller|liar|contradiction|unique solution/i,"T17"],
  [/working backwards|difference|simultaneous|equation|total-sum|unknown/i,"T02"],
  [/reading|graph|table|model|estimate|parts and wholes/i,"T01"]
];

function chapterFor(focus){
  for(const [re,id] of chapterRules) if(re.test(focus)) return id;
  return "T18";
}
function courseSession(){return course[Math.min((progress?.completed_sessions||0),371)]||course[0]}
function nextSlot(type){
  const done=progress?.completed_sessions||0;
  const next=course.find(s=>s.slot>done&&s.type===type);
  return next?next.slot-done:null;
}
function overall(){
  const done=progress?.completed_sessions||0;
  return done/372*100;
}
function earnedRankBySessions(done=progress?.completed_sessions||0){return Math.max(0,Math.min(20,Math.floor(Number(done||0)*20/372)))}
function currentRank(){return Math.max(Number(progress?.rank||0),earnedRankBySessions())}
function currentRankLabel(){const r=currentRank();return r===0?"Cadet":`Rank ${r} · ${rankNames[r-1]}`}
function problemKeywords(focus){
  return focus.toLowerCase().split(/[^a-z0-9]+/).filter(w=>w.length>4&&!["including","through","under","using","simple","reasoning"].includes(w));
}
function chooseProblems(session){return selectOriginalProblems(session,problemIndex,lessonManifest);}
function teachingFor(session){
 const m=methods[skillFor(session,taxonomy)];
 return m?teaching.filter(t=>t.id===m.video):[];
}
async function saveDraft(s){
 clearTimeout(autosaveTimer);const snapshot=JSON.stringify(sessionDraft);
 localStorage.setItem(draftKey(s),JSON.stringify({updated_at:new Date().toISOString(),draft:sessionDraft}));
 await upsertSession({session_number:s.slot,session_key:`S${String(s.slot).padStart(3,"0")}`,answers:sessionDraft.answers,working:sessionDraft.working,evidence:sessionDraft.evidence,summary:sessionDraft.summary});
 if(JSON.stringify(sessionDraft)===snapshot){draftDirty=false;localStorage.removeItem(draftKey(s));}
}
async function refreshEvidence(){
 const [{data,error},{data:exams,error:ee}]=await Promise.all([
  supabase.from("session_records").select("session_number,completed_at,summary,answers,working,evidence").eq("user_id",user.id).not("completed_at","is",null).order("session_number"),
  supabase.from("exam_sittings").select("id,exam_id,score,max_score,submitted_at,metadata").eq("user_id",user.id).eq("completed",true).order("submitted_at",{ascending:false}).limit(30)
 ]);if(error||ee)throw error||ee;completedRecords=(data||[]).map(r=>({...r,summary:{...r.summary,skill_id:r.summary?.skill_id||skillFor(course[r.session_number-1]||{},taxonomy)}}));recentExams=exams||[];
}
async function renderRoadmap(){await refreshEvidence();app.innerHTML=readinessHTML({records:completedRecords,taxonomy,progress,milestones,exams:recentExams});}
async function boot(){
  try{
    user=await currentUser();
    if(!user){location.href="login.html";return}
    const [c,t,m,h,tax,ms,lm]=await Promise.all([fetch("data/sessions-372.json").then(r=>r.json()),fetch("data/teaching-72.json").then(r=>r.json()),fetch("data/mawa-investigations-20.json").then(r=>r.json()),fetch("data/rossmoyne-h23.json").then(r=>r.json()),fetch("data/taxonomy-52.json").then(r=>r.json()),fetch("data/milestones.json").then(r=>r.json()),fetch("data/lesson-challenges.json?v=original-transfer-20261112").then(r=>r.json())]);
    course=c.sessions; teaching=t.items; mawa=m.items; rossMap=h.items; taxonomy=tax; milestones=ms;lessonManifest=lm.items;
    const {data:problems,error}=await supabase.from("content_problems_student").select("id,source_type,title,source_label,category,difficulty,prompt,unit").eq("source_type","original_authored").order("id");
    if(error)throw error; problemIndex=problems||[];
    const {data:attemptRows,error:attemptError}=await supabase.from("problem_attempts").select("problem_id,independent_credit,is_correct,created_at").eq("user_id",user.id).not("answer_text","is",null).order("created_at");
    if(attemptError)throw attemptError; attemptHistory=attemptRows||[]; attemptedProblemIds=new Set(attemptHistory.map(x=>x.problem_id));
    progress=await loadProgress();
    if(!progress)progress=await saveProgress({current_session:0,completed_sessions:0,xp:0,rank:0,overall_percent:0,state:{}});
    await refreshEvidence();
    // Recover a completed session if the separate progress write lost its connection.
    let contiguous=0;while(completedRecords.some(r=>r.session_number===contiguous+1))contiguous++;
    if(contiguous>(progress.completed_sessions||0))progress=await saveProgress({completed_sessions:contiguous,current_session:Math.min(372,contiguous+1),xp:contiguous*100,rank:earnedRankBySessions(contiguous),overall_percent:contiguous/372*100});
    wireNav(); renderHome();
  }catch(e){app.innerHTML='<section class="panel hero-panel"><h1>Unable to load Summit One</h1><p class="muted">'+esc(e.message)+'</p></section>'}
}
function wireNav(){
  document.querySelectorAll("[data-view]").forEach(b=>b.onclick=async()=>{if(editingSession){try{await saveDraft(editingSession);editingSession=null}catch(e){alert("Please retry saving before leaving: "+e.message);return}}document.querySelectorAll(".nav-btn").forEach(x=>x.classList.remove("active"));b.classList.add("active");activeView=b.dataset.view;if(activeView==="home")renderHome();if(activeView==="review")renderReview();if(activeView==="profile")renderProfile();if(activeView==="roadmap")renderRoadmap().catch(e=>alert(e.message))})
}
function renderHome(){
  const s=courseSession(),done=progress.completed_sessions||0,amc=nextSlot("AMC MOCK"),mawa=nextSlot("MAWA");
  const nextPractice=course.find(x=>x.slot>done&&(x.type==="AMC MOCK"||x.type==="ROSSMOYNE MOCK"));
  const practiceGap=nextPractice?nextPractice.slot-done:null;
  const milestone=done<152?{target:152,label:"2027 AMC readiness"}:done<176?{target:176,label:"MAWA application readiness"}:done<360?{target:360,label:"2028 AMC readiness"}:{target:372,label:"Rossmoyne capstone"};
  const milestoneDone=Math.min(done,milestone.target);
  app.innerHTML=`
  <section class="dashboard-grid">
    <article class="panel mission-card">
      <div class="session-kicker">SESSION ${s.slot} / 372</div>
      <h1>${esc(s.focus)}</h1>
      <div><span class="type-chip">${esc(s.type)}</span><span class="phase-chip">${esc(s.phase)}</span></div>
      <p class="muted">Remember → Discover → Try → Transfer → Check. Work carefully; there is no calendar streak and no penalty for taking the time you need.</p>
      <button id="continue" class="primary cta">${done>=372?"Course complete":"Continue Session "+s.slot}</button>
      <div class="sync-line"><span class="dot"></span> Cloud progress: <span id="syncStatus">${syncStatusText()}</span></div>
      <div class="quick-links"><a class="secondary" href="tests.html">AMC Test Centre</a><button id="reviewQuick" class="ghost">Review completed sessions</button></div>
    </article>
    <aside class="side-stack">
      <article class="panel stat-card"><div class="eyebrow">COURSE PROGRESS</div><div class="stat-value">${done} / 372</div><div class="progress-track"><div class="progress-fill" style="width:${overall().toFixed(2)}%"></div></div><div class="stat-label">${overall().toFixed(1)}% complete · ${esc(currentRankLabel())}</div></article>
      <article class="panel stat-card"><div class="eyebrow">NEXT PRACTICE EXAM</div><div class="stat-value">${practiceGap??"—"}</div><div class="stat-label">${nextPractice?`${esc(nextPractice.type)} · Session ${nextPractice.slot}`:"All scheduled mocks complete"}</div></article>
      <article class="panel stat-card"><div class="eyebrow">NEXT MAWA INVESTIGATION</div><div class="stat-value">${mawa??"—"}</div><div class="stat-label">${mawa===1?"Next session":mawa===null?"All scheduled investigations complete":mawa+" completed sessions away"}</div></article>
      <article class="panel stat-card"><div class="eyebrow">CURRENT MILESTONE</div><div class="stat-value">${milestoneDone} / ${milestone.target}</div><div class="progress-track"><div class="progress-fill" style="width:${(milestoneDone/milestone.target*100).toFixed(1)}%"></div></div><div class="stat-label">${esc(milestone.label)}</div></article>
    </aside>
  </section>
  <section class="panel learning-note"><h2>Today’s rhythm</h2><p>3–5 minutes meeting the idea and remembering · 10–15 minutes with worked examples and supported practice · 15–25 minutes applying and transferring · 5–10 minutes checking. Stop for a short break if concentration drops; unfinished work stays in this session.</p><button id="planQuick" class="secondary">Goals and readiness</button></section>
  <p class="footer-note">The course follows the canonical 372-session Summit One plan: 283 teaching/transfer sessions, 53 MAWA investigations, 25 AMC mock positions and 11 Rossmoyne-style mock positions. Full authentic AMC papers live separately in the Test Centre and never replace the teaching sequence.</p>`;
  document.getElementById("continue").onclick=()=>done<372?startSession(s):renderProfile();
  document.getElementById("reviewQuick").onclick=()=>renderReview();
  document.getElementById("planQuick").onclick=()=>renderRoadmap().catch(e=>alert(e.message));
}
async function startSession(s){
 try{
  if(s.type==="AMC MOCK"||s.type==="ROSSMOYNE MOCK"){location.href=`tests.html?slot=${s.slot}&course=1`;return}
  await refreshEvidence();
  activeStage=0;currentMawa=s.type==="MAWA"?mawa[(Math.floor(s.slot/7)-1)%mawa.length]:null;
  const {data:existing,error}=await supabase.from("session_records").select("*").eq("user_id",user.id).eq("session_number",s.slot).maybeSingle();if(error)throw error;
  if(existing?.immutable){await refreshEvidence();renderReview();return}
  sessionDraft={answers:existing?.answers||{},working:existing?.working||{},evidence:existing?.evidence||{},summary:existing?.summary||{}};
  const local=JSON.parse(localStorage.getItem(draftKey(s))||'null');
  if(local?.draft&&(!existing?.updated_at||local.updated_at>existing.updated_at))sessionDraft=local.draft;
  editingSession=s;
  const previous=sessionDraft.summary.problems||[];
  currentProblems=chooseProblems(s);
  // Preserve saved answers and working, including legacy drafts, but replace the active tasks.
  const retired=previous.filter(id=>!currentProblems.some(p=>p.id===id));
  sessionDraft.summary={...sessionDraft.summary,previous_problem_ids:[...new Set([...(sessionDraft.summary.previous_problem_ids||[]),...retired])],learning_version:LEARNING_VERSION,problems:currentProblems.map(p=>p.id),skill_id:skillFor(s,taxonomy),focus:s.focus,type:s.type,phase:s.phase};
  await saveDraft(s);
  if(s.type==="MAWA"){renderMawaSession(s);return}renderSession(s);
 }catch(e){alert("Could not open this session: "+e.message)}
}

function mawaExtension(s,item){
  const ordinal=Math.floor(s.slot/7);
  const cycle=Math.floor((ordinal-1)/20);
  if(cycle===0)return "Base investigation: solve every part and justify the general or optimal claim.";
  if(cycle===1)return "Extension: change one numerical condition in a sensible way. Predict what changes before calculating, solve the new case, then state which part of the original reasoning still works.";
  return "Deep extension: write a variable/general version of the problem. State a conjecture, test boundary cases or a counterexample, and give an argument for when the rule is true.";
}
function renderMawaSession(s){
  app.innerHTML=`
  <section class="session-page">
    <header class="panel session-header"><div class="eyebrow">SESSION ${s.slot} / 372 · MAWA INVESTIGATION</div><h1>${esc(currentMawa.title)}</h1><div><span class="type-chip">PROOF & INVESTIGATION</span><span class="phase-chip">${esc(s.phase)}</span></div></header>
    <nav class="stage-nav" aria-label="MAWA stages">${["Start","Discover","Try","Transfer","Check"].map((x,i)=>`<button data-stage="${i}" class="${i===activeStage?"active":""}">${i+1}. ${x}</button>`).join("")}</nav>
    <section id="stage" class="panel stage"></section>
  </section>`;
  document.querySelectorAll("[data-stage]").forEach(b=>b.onclick=async()=>{try{await saveDraft(s);activeStage=Number(b.dataset.stage);renderMawaSession(s)}catch(e){alert(e.message)}});
  const el=document.getElementById("stage"), item=currentMawa;
  if(activeStage===0){
    const prevSlot=s.slot-7,prev=prevSlot>=7?mawa[(Math.floor(prevSlot/7)-1)%mawa.length]:null;
    el.innerHTML=`${investigationIntroHTML(s,item)}<div class="stage-number">NOW REMEMBER · A USEFUL HABIT</div><h2>Bring back an idea</h2><p class="muted">MAWA-style work rewards systematic thinking and clear justification, not speed alone.</p><div class="teaching-item"><h3>${prev?esc(prev.title):"Proof habit"}</h3><p class="math-copy">${prev?"Without reopening the old solution, write one sentence about what made the previous investigation complete.":"Write the difference between finding an example and proving a maximum, minimum or impossibility."}</p></div><div class="complete-row"><span></span><button id="nextStage" class="primary">Discover</button></div>`;
  }
  if(activeStage===1){
    el.innerHTML=`<div class="stage-number">STAGE 2 · INVESTIGATION SETUP</div><h2>Discover</h2>${investigationWarmupHTML(item)}<h3>Now grow the investigation</h3><p class="muted">Read the problem slowly. Decide what evidence would count as a proof before calculating.</p><div class="problem-card"><div class="problem-meta">${esc(item.topic)}</div><h3 class="problem-title">${esc(item.title)}</h3><div class="problem-prompt math-copy">${esc(item.prompt)}</div><details style="margin-top:14px"><summary>First hint — use only if you are genuinely stuck</summary><p class="math-copy">${esc(item.hint)}</p></details></div><div class="complete-row"><span class="muted">Plan cases, a diagram, a table or an invariant.</span><button id="nextStage" class="primary">Try the investigation</button></div>`;
  }
  if(activeStage===2){
    const saved=sessionDraft.working.mawa_base||"";
    el.innerHTML=`<div class="stage-number">STAGE 3 · INDEPENDENT WORK</div><h2>Try</h2><p class="muted">Use paper, a notebook or this box. A correct number without justification is not complete evidence.</p><div class="problem-card"><div class="math-copy">${esc(item.prompt)}</div><label class="answer-label">Your organised reasoning<textarea id="mawaBase" class="answer-box" rows="12">${esc(saved)}</textarea></label><button id="recordMawa" class="primary">Record investigation work</button><div id="mawaMsg" class="attempt-feedback" hidden></div></div><div class="complete-row"><button id="backStage" class="ghost">Back</button><button id="nextStage" class="primary">Transfer</button></div>`;
    document.getElementById("mawaBase").oninput=e=>{sessionDraft.working.mawa_base=e.target.value};
    document.getElementById("recordMawa").onclick=async()=>{const v=document.getElementById("mawaBase").value.trim();if(v.length<20){alert("Record enough working to show the method, not only an answer.");return}sessionDraft.working.mawa_base=v;sessionDraft.evidence.mawa_base={status:"proof_evidence_unreviewed",recorded_at:new Date().toISOString()};await upsertSession({session_number:s.slot,session_key:`S${String(s.slot).padStart(3,"0")}`,answers:sessionDraft.answers,working:sessionDraft.working,evidence:sessionDraft.evidence,summary:sessionDraft.summary});const m=document.getElementById("mawaMsg");m.hidden=false;m.textContent="Work saved. Proof evidence remains unreviewed until you compare/check it."};
  }
  if(activeStage===3){
    const ext=(item.transfer_prompt||mawaExtension(s,item))+(Math.floor(s.slot/7)>20?" Then change a condition, predict the effect, and justify a general rule or counterexample.":""),saved=sessionDraft.working.mawa_extension||"";
    el.innerHTML=`<div class="stage-number">STAGE 4 · GENERALISE</div><h2>Transfer</h2><p class="muted">${esc(ext)}</p><label class="answer-label">Extension reasoning<textarea id="mawaExt" class="answer-box" rows="10">${esc(saved)}</textarea></label><button id="recordExt" class="primary">Record extension</button><div class="complete-row"><button id="backStage" class="ghost">Back</button><button id="nextStage" class="primary">Check</button></div>`;
    document.getElementById("mawaExt").oninput=e=>{sessionDraft.working.mawa_extension=e.target.value};
    document.getElementById("recordExt").onclick=async()=>{const v=document.getElementById("mawaExt").value.trim();if(v.length<20){alert("Give a mathematical reason, example, diagram description or proof step.");return}sessionDraft.working.mawa_extension=v;await upsertSession({session_number:s.slot,session_key:`S${String(s.slot).padStart(3,"0")}`,answers:sessionDraft.answers,working:sessionDraft.working,evidence:sessionDraft.evidence,summary:sessionDraft.summary});};
  }
  if(activeStage===4){
    const ready=(sessionDraft.working.mawa_base||"").trim().length>=20&&(sessionDraft.working.mawa_extension||"").trim().length>=20;
    el.innerHTML=`<div class="stage-number">STAGE 5 · PROOF CHECK</div><h2>Check</h2><p class="muted">Score the evidence, not confidence. This is a practice rubric, not an official MAWA admissions score.</p><div class="problem-card"><details ${ready?"":"hidden"}><summary>Compare with model reasoning</summary><p class="solution-panel" style="display:block">${esc(item.solution)}</p>${item.transfer_solution?`<h4>Check the new setting</h4><p class="math-copy">${esc(item.transfer_solution)}</p>`:""}<p class="muted"><b>Common trap:</b> ${esc(item.trap)}</p></details><div class="check-grid"><label class="answer-label">Result 0–3<input id="rResult" type="number" min="0" max="3" value="" required></label><label class="answer-label">Method 0–3<input id="rMethod" type="number" min="0" max="3" value="" required></label><label class="answer-label">Proof / completeness 0–3<input id="rProof" type="number" min="0" max="3" value="" required></label><label class="answer-label">Clarity 0–1<input id="rClarity" type="number" min="0" max="1" value="" required></label></div></div><div class="complete-row"><span class="muted">${ready?"Investigation and extension recorded.":"Record both the investigation and extension before completion."}</span><button id="completeMawa" class="primary" ${ready?"":"disabled"}>Complete and lock Session ${s.slot}</button></div>`;
    if(ready)document.getElementById("completeMawa").onclick=async()=>{if(!["rResult","rMethod","rProof","rClarity"].every(id=>{const x=document.getElementById(id);return x.value!==""&&x.checkValidity()})){alert("Enter each rubric score after comparing the reasoning.");return}const rubric={result:Number(document.getElementById("rResult").value),method:Number(document.getElementById("rMethod").value),proof:Number(document.getElementById("rProof").value),clarity:Number(document.getElementById("rClarity").value)};sessionDraft.summary={...sessionDraft.summary,review_status:"self_reviewed_not_independently_verified",focus:item.title,type:"MAWA",phase:s.phase,investigation_id:item.id,rubric,total:rubric.result+rubric.method+rubric.proof+rubric.clarity};const button=document.getElementById("completeMawa");button.disabled=true;try{await completeSpecialSession(s)}catch(e){alert("Could not finish saving: "+e.message);button.disabled=false}};
  }
  const next=document.getElementById("nextStage");if(next)next.onclick=async()=>{await saveDraft(s);activeStage=Math.min(4,activeStage+1);renderMawaSession(s)};
  const back=document.getElementById("backStage");if(back)back.onclick=async()=>{try{await saveDraft(s);activeStage=Math.max(0,activeStage-1);renderMawaSession(s)}catch(e){alert(e.message)}};
}
async function completeSpecialSession(s){
 clearTimeout(autosaveTimer);
  await upsertSession({session_number:s.slot,session_key:`S${String(s.slot).padStart(3,"0")}`,completed_at:new Date().toISOString(),immutable:true,answers:sessionDraft.answers,working:sessionDraft.working,evidence:sessionDraft.evidence,summary:sessionDraft.summary});
  const done=Math.max(progress.completed_sessions||0,s.slot),p=done/372*100,r=Math.max(Number(progress.rank||0),Math.max(0,Math.min(20,Math.floor(done*20/372))));
  progress=await saveProgress({completed_sessions:done,current_session:Math.min(372,done+1),xp:done*100,rank:r,overall_percent:Number(p.toFixed(2)),next_practice_exam_in:(course.find(x=>x.slot>done&&(x.type==="AMC MOCK"||x.type==="ROSSMOYNE MOCK"))?.slot??done)-done});
  localStorage.removeItem(draftKey(s));editingSession=null;draftDirty=false;await refreshEvidence();renderHome();
}

function renderSession(s){
  app.innerHTML=`
  <section class="session-page">
    <header class="panel session-header"><div class="eyebrow">SESSION ${s.slot} / 372 · ${esc(s.phase)}</div><h1>${esc(s.focus)}</h1><div><span class="type-chip">${esc(s.type)}</span></div></header>
    <nav class="stage-nav" aria-label="Session stages">
      ${["Start","Discover","Try","Transfer","Check"].map((x,i)=>`<button data-stage="${i}" class="${i===activeStage?"active":""}">${i+1}. ${x}</button>`).join("")}
    </nav>
    <section id="stage" class="panel stage"></section>
  </section>`;
  document.querySelectorAll("[data-stage]").forEach(b=>b.onclick=async()=>{try{await saveDraft(s);activeStage=Number(b.dataset.stage);renderSession(s)}catch(e){alert("Your work is still here. Could not save: "+e.message)}});
  const target=document.getElementById("stage");
  if(activeStage===0)renderRemember(target,s);
  if(activeStage===1)renderDiscover(target,s);
  if(activeStage===2)renderChallenge(target,s,currentProblems[0],"try");
  if(activeStage===3)renderChallenge(target,s,currentProblems[1],"transfer");
  if(activeStage===4)renderCheck(target,s);
}
function renderRemember(el,s){
 el.innerHTML=`${introductionHTML(s,course,taxonomy)}<div class="stage-number">NOW REMEMBER · ABOUT 5 MINUTES</div><h2>Warm up what you know</h2><p class="muted">Start without notes. Getting stuck shows us what to revisit.</p><div id="retrievalChecks"></div><div class="complete-row"><span class="muted">Try the due checks before continuing.</span><button class="primary" id="nextStage">Discover</button></div>`;
 mountRetrieval(el.querySelector('#retrievalChecks'),{records:completedRecords,slot:s.slot,currentId:skillFor(s,taxonomy),draft:sessionDraft,save:()=>saveDraft(s)});
 document.getElementById('nextStage').onclick=async()=>{if((sessionDraft.summary.retrieval_ids||[]).some(id=>!sessionDraft.evidence['retrieval:'+id])){alert('Try each short revision check. Use a hint if needed.');return}await saveDraft(s);activeStage=1;renderSession(s)};
}

function renderDiscover(el,s){
  const items=teachingFor(s);
  el.innerHTML=`<div class="stage-number">STAGE 2 · EXPLANATION</div><h2>Discover</h2><p class="muted">Read, sketch and listen. The goal is to see why the method works, not memorise a slogan.</p>
  ${lessonCard(skillFor(s,taxonomy),lessonPlan(s,course,taxonomy))}<div id="guidedCheck"></div><details class="optional-lesson"><summary>Optional deeper connection · related video or reading</summary><div class="teaching-box">${items.map((t,i)=>`<article class="teaching-item"><div class="eyebrow">${esc(t.type==="worked_example"?"WORKED EXAMPLE":"CONCEPT")}</div><h3>${esc(t.title)}</h3><div class="lesson-player-slot" id="lessonPlayer${i}"></div><details><summary>Read explanation</summary><p class="math-copy">${esc(t.transcript)}</p>${t.extended_reading?`<h4>Further mathematical connections</h4><p class="math-copy">${esc(t.extended_reading)}</p>`:""}</details></article>`).join("")||'<p class="muted">Teaching explanation is being selected from the course library.</p>'}</div></details>
  <div class="complete-row"><span class="muted">Try the supported question first. A hint is part of learning.</span><button class="primary" id="nextStage">Try independently</button></div>`;
  if(skillFor(s,taxonomy))mountCheck(el.querySelector("#guidedCheck"),{id:skillFor(s,taxonomy),slot:s.slot,records:completedRecords,draft:sessionDraft,kind:"guided",seedOverride:lessonPlan(s,course,taxonomy).visit%7,save:()=>saveDraft(s)});
  items.forEach((t,i)=>mountNarratedPlayer(document.getElementById("lessonPlayer"+i),{
    title:t.title,
    transcript:t.transcript,
    audioUrl:t.audio_url,
    videoUrl:finalVideoUrl(t.id),
    cacheKey:t.id,
    onWatch:detail=>recordVideoEvidence(s.slot,t.id,t.type,detail)
  }));
  document.getElementById("nextStage").onclick=async()=>{try{if(!sessionDraft.evidence["guided:"+skillFor(s,taxonomy)]){alert("Try the supported question first. Use the hint or worked example if needed.");return}await saveDraft(s);activeStage=2;renderSession(s)}catch(e){alert(e.message)}};
}
function renderChallenge(el,s,p,mode){
  const sid=skillFor(s,taxonomy), guided=sessionDraft.evidence['guided:'+sid], core=sessionDraft.evidence['retrieval:'+sid];
  if(!guided||(mode==='transfer'&&!core)){
    el.innerHTML=`<h2>Build the method first</h2><p>Before the stretch questions, try the supported example in Discover, then the short independent check in Try. You do not have to get everything right to continue; use the explanation to repair a mistake.</p><button id="prepareMethod" class="primary">${!guided?'Go to Discover':'Go to Try'}</button>`;
    el.querySelector('#prepareMethod').onclick=()=>{activeStage=!guided?1:2;renderSession(s)};return;
  }
  if(!p){el.innerHTML='<div class="empty">No challenge available.</div>';return}
  el.innerHTML=`<div class="stage-number">STAGE ${mode==="try"?3:4} · ${mode==="try"?"INDEPENDENT ATTEMPT":"TRANSFER"}</div><h2>${mode==="try"?"Try":"Transfer"}</h2><p class="muted">${mode==="try"?"First check the method on a manageable question. Then open the stretch problem.":"Choose a method from the clues, before looking at a hint. Explain how this setting connects to an idea you know."}</p>`;
  const node=problemTemplate.content.firstElementChild.cloneNode(true);
  node.querySelector(".problem-meta").textContent=`ORIGINAL LEARNING PROBLEM · ${mode==="try"?"APPLY THE IDEA":"CHOOSE YOUR METHOD"}`;
  node.querySelector(".problem-title").textContent=p.title||p.id;
  const promptEl=node.querySelector(".problem-prompt"); promptEl.textContent=p.prompt; const figure=originalFigure(p)||problemFigure(p.id); if(figure)promptEl.insertAdjacentHTML("beforebegin",figure);
  const box=node.querySelector(".answer-box"),submit=node.querySelector(".submit-answer"),reveal=node.querySelector(".reveal-solution"),feedback=node.querySelector(".attempt-feedback"),solution=node.querySelector(".solution-panel");
  const familiar=familySeen(completedRecords,p.learning.family);
  const reason=mountReasoning(node,{p,draft:sessionDraft,save:()=>saveDraft(s),showHint:()=>methods[p.learning.skill].idea});
  const saved=sessionDraft.answers[p.id];
  const working=node.querySelector(".working-box");working.value=sessionDraft.working[p.id]||"";working.oninput=()=>{sessionDraft.working[p.id]=working.value};
  box.value=sessionDraft.working["draft-answer:"+p.id]||"";box.oninput=()=>{sessionDraft.working["draft-answer:"+p.id]=box.value};
  if(saved){box.value=saved.response||"";box.disabled=true;submit.hidden=true;reveal.hidden=false;feedback.hidden=false;feedback.textContent=applicationStatus(sessionDraft.evidence["application:"+p.id])+". Check the reasoning, not only the final answer."}
  submit.onclick=async()=>{
    const response=box.value.trim();if(!response){feedback.hidden=false;feedback.textContent="Write an answer or reasoning first.";return}
    if(!['clue','plan'].every(k=>String(reason[k]||'').trim().length>=8)){feedback.hidden=false;feedback.textContent="Before submitting, record the clue you noticed and why your first step fits. Use the help button if you need a starting point.";return}
    submit.disabled=true;feedback.hidden=false;feedback.textContent="Recording your attempt…";
    try{
      const {data:graded,error:gradeError}=await supabase.functions.invoke("submit-problem-attempt",{body:{problem_id:p.id,session_number:s.slot,answer_text:response,used_help:reason.used_help===true,familiar_family:familiar}});
      if(gradeError)throw gradeError;
      if(graded?.error)throw new Error(graded.error);
      const correct=graded?.correct??null;
      sessionDraft.evidence['application:'+p.id]={kind:'application',role:p.learning.role,skill_id:p.learning.skill,family:p.learning.family,problem_id:p.id,correct,used_help:reason.used_help===true,familiar_family:familiar,explanation_status:'saved_for_review_not_automatically_verified',recorded_at:new Date().toISOString()};
      attemptedProblemIds.add(p.id);
      attemptHistory.push({problem_id:p.id,is_correct:correct,independent_credit:graded?.independent_credit===true,created_at:new Date().toISOString()});
      sessionDraft.answers[p.id]={response,correct,independent_credit:graded?.independent_credit===true,attempted_at:new Date().toISOString()};
      await upsertSession({session_number:s.slot,session_key:`S${String(s.slot).padStart(3,"0")}`,answers:sessionDraft.answers,working:sessionDraft.working,evidence:sessionDraft.evidence,summary:sessionDraft.summary});
      box.disabled=true;submit.hidden=true;reveal.hidden=false;feedback.textContent=applicationStatus(sessionDraft.evidence["application:"+p.id])+". Now check your reasoning against the original conditions.";
    }catch(e){feedback.textContent=e.message;submit.disabled=false}
  };
  reveal.onclick=async()=>{
    try{
      const {data:d,error:solutionError}=await supabase.functions.invoke("get-problem-solution",{body:{problem_id:p.id,session_number:s.slot}});
      if(solutionError)throw solutionError;
      if(d?.error)throw new Error(d.error);
      const transcript=d.spoken_script||d.solution_text||"Solution unavailable.";
      const writtenSolution=d.solution_text||transcript;
      solution.hidden=false;solution.innerHTML=`<b>Compare reasoning</b><div id="solutionPlayer-${p.id.replace(/[^A-Za-z0-9]/g,"_")}"></div><details style="margin-top:12px"><summary>Read full worked solution</summary><p class="math-copy">${esc(writtenSolution)}</p></details>`;
      const protectedAudio="";
      mountNarratedPlayer(document.getElementById("solutionPlayer-"+p.id.replace(/[^A-Za-z0-9]/g,"_")),{
        title:p.title||p.id,
        transcript,
        audioUrl:protectedAudio,
        videoUrl:["K001","K007","K015","K022"].includes(p.id)?"":d.video_url||finalVideoUrl(p.id),
        cacheKey:p.id,
        onWatch:detail=>recordVideoEvidence(s.slot,p.id,"challenge_solution",detail)
      });
      sessionDraft.evidence['solution:'+p.id]={seen:true,recorded_at:new Date().toISOString()};
      await saveDraft(s);reveal.disabled=true;
    }catch(e){solution.hidden=false;solution.textContent=e.message}
  };
  if(mode==='try'){
    const prep=document.createElement('div');el.appendChild(prep);
    node.hidden=!core;
    const unlock=e=>{node.hidden=false;node.scrollIntoView({behavior:'smooth',block:'start'});};
    mountCheck(prep,{id:sid,slot:s.slot,records:completedRecords,draft:sessionDraft,save:()=>saveDraft(s),label:'YOUR TURN · INDEPENDENT BASICS CHECK',seedOverride:(lessonPlan(s,course,taxonomy).visit+1)%7,onDone:unlock});
  }
  const bridge=document.createElement('div');bridge.className='challenge-bridge';
  bridge.innerHTML=`<h3>${mode==='try'?'Next: apply the idea':familiar?'Transfer: practise a variation':'Transfer: choose your tools'}</h3><p>This is a challenge, not the first explanation. Read for the requested quantity, sketch or list what is known, and decide which tool fits. If today’s method does not fit on its own, combine it with an older one.</p><details><summary>A starting plan, without the answer</summary><ol><li>Restate the question in your own words.</li><li>Test a smaller case or draw the quantities.</li><li>Look for a connection to the worked examples. Explain why it applies before calculating.</li></ol></details>`;
  node.prepend(bridge);el.appendChild(node);
  const footer=document.createElement("div");footer.className="complete-row";footer.innerHTML=`<button class="ghost" id="prevStage">Back</button><button class="primary" id="nextStage">${mode==="try"?"Transfer":"Check"}</button>`;el.appendChild(footer);
  footer.querySelector("#prevStage").onclick=async()=>{await saveDraft(s);activeStage=mode==="try"?1:2;renderSession(s)};
  footer.querySelector("#nextStage").onclick=async()=>{await saveDraft(s);activeStage=mode==="try"?3:4;renderSession(s)};
}
function renderCheck(el,s){
  const attempted=currentProblems.filter(p=>sessionDraft.answers[p?.id]).length;
  el.innerHTML=`<div class="stage-number">STAGE 5 · METACOGNITION</div><h2>Check</h2><p class="muted">Make the learning reusable. A short accurate reflection is better than a long vague one.</p>
  <p class="success-note">You have already checked the basic method before the challenges. Finish by explaining what you learnt, checking your reasoning and choosing a useful next step.</p><div class="check-grid"><label class="answer-label">What was the key idea?<textarea id="takeaway" class="answer-box" placeholder="I would use this when… because… The important step is…">${esc(sessionDraft.summary.takeaway||"")}</textarea></label>
  <label class="answer-label">What will you watch for next time?<textarea id="watch" class="answer-box" placeholder="A mistake I want to avoid is…">${esc(sessionDraft.summary.watch||"")}</textarea></label></div>
  <div class="complete-row"><span class="muted">${attempted}/2 challenge attempts recorded.</span><button id="completeSession" class="primary" ${attempted<2?"disabled":""}>Complete and lock Session ${s.slot}</button></div>`;
  const checks=document.createElement('section');checks.className='transfer-checks';
  checks.innerHTML=`<h3>Check, repair, then decide</h3>${currentProblems.map(p=>{const e=sessionDraft.evidence['reasoning:'+p.id]||{};return `<article class="check-status"><h4>${p.learning.role==='transfer'?'Transfer problem':'Practice problem'}</h4><p>${esc(applicationStatus(sessionDraft.evidence['application:'+p.id]))}</p><label class="answer-label">How did you check the result? If it was wrong, where did the reasoning change?<textarea class="reason-input" data-final-check="${p.id}" placeholder="I substituted back / listed the cases / used a different method…">${esc(e.check||'')}</textarea></label></article>`}).join('')}<label class="answer-label">How ready do you feel for another problem with this idea?<select id="transferConfidence" class="answer-box"><option value="">Choose after checking your work</option><option value="ready">Ready to try another independently</option><option value="practice">I need more practice</option><option value="explanation">I need the idea explained again</option></select></label><p class="muted">This is your reflection, not an automatic mastery award. Explanations are saved for you and a parent to review. Mistakes do not block progress once you have attempted, checked and reflected.</p>`;
  el.querySelector('.complete-row').before(checks);
  checks.querySelectorAll('[data-final-check]').forEach(input=>input.oninput=()=>{const key='reasoning:'+input.dataset.finalCheck;sessionDraft.evidence[key]||={};sessionDraft.evidence[key].check=input.value});
  checks.querySelector('#transferConfidence').value=sessionDraft.summary.transfer_confidence||'';
  checks.querySelector('#transferConfidence').onchange=e=>{sessionDraft.summary.transfer_confidence=e.target.value};
  const sid=skillFor(s,taxonomy);
  document.getElementById("takeaway").oninput=e=>{sessionDraft.summary.takeaway=e.target.value};
  document.getElementById("watch").oninput=e=>{sessionDraft.summary.watch=e.target.value};
  document.getElementById("completeSession").onclick=async()=>{
    if(sid&&!sessionDraft.evidence["retrieval:"+sid]){alert("Complete the independent basics check in Try first. Use a hint if needed.");return}
    if((sessionDraft.summary.retrieval_ids||[]).some(id=>!sessionDraft.evidence["retrieval:"+id])){alert("Finish the due Remember checks first.");return}
    if(!currentProblems.every(p=>reasoningReady(sessionDraft,p.id))||!sessionDraft.summary.transfer_confidence){alert("Record a check or correction for each problem, then choose how ready you feel. A mistake is useful evidence; it does not prevent completion.");return}
    const take=document.getElementById("takeaway").value.trim(),watch=document.getElementById("watch").value.trim();
    if(!take||!watch){alert("Write both short reflections before completing the session.");return}
    clearTimeout(autosaveTimer);const btn=document.getElementById("completeSession");btn.disabled=true;btn.textContent="Locking session…";
    try{
      sessionDraft.summary={...sessionDraft.summary,takeaway:take,watch,focus:s.focus,type:s.type,phase:s.phase,problems:currentProblems.map(x=>x.id)};
      await upsertSession({session_number:s.slot,session_key:`S${String(s.slot).padStart(3,"0")}`,completed_at:new Date().toISOString(),immutable:true,answers:sessionDraft.answers,working:sessionDraft.working,evidence:sessionDraft.evidence,summary:sessionDraft.summary});
      const done=Math.max(progress.completed_sessions||0,s.slot),p=done/372*100,r=Math.max(Number(progress.rank||0),Math.max(0,Math.min(20,Math.floor(done*20/372))));
      progress=await saveProgress({completed_sessions:done,current_session:Math.min(372,done+1),xp:done*100,rank:r,overall_percent:Number(p.toFixed(2)),next_practice_exam_in:(course.find(x=>x.slot>done&&x.type==="AMC MOCK")?.slot??done)-done});
      localStorage.removeItem(draftKey(s));editingSession=null;draftDirty=false;await refreshEvidence();renderHome();
    }catch(e){alert(e.message);btn.disabled=false;btn.textContent=`Complete and lock Session ${s.slot}`}
  };
}
async function renderReview(){
 activeView="review";await refreshEvidence();
 app.innerHTML=`<section class="panel hero-panel"><div class="eyebrow">YOUR MATHEMATICAL NOTEBOOK</div><h1>Completed sessions</h1><p class="muted">The original answers and working are locked. Use a fresh session to show new learning.</p>${[...completedRecords].reverse().map(r=>`<details class="review-detail"><summary>Session ${r.session_number} · ${esc(r.summary?.focus||course[r.session_number-1]?.focus||'')} <span class="type-chip">LOCKED</span></summary><p><b>Key idea:</b> ${esc(r.summary?.takeaway||'—')}</p><p><b>Next time:</b> ${esc(r.summary?.watch||'—')}</p>${Object.entries(r.answers||{}).map(([id,a])=>`<article><h3>${esc(problemIndex.find(p=>p.id===id)?.title||id)}</h3><p class="math-copy">${esc(problemIndex.find(p=>p.id===id)?.prompt||'')}</p><p><b>Recorded answer:</b> ${esc(a?.response??a)}</p><p class="math-copy">${esc(r.working?.[id]||'')}</p></article>`).join('')}${r.working?.mawa_base?`<h3>Investigation</h3><p class="math-copy">${esc(r.working.mawa_base)}</p><h3>Extension</h3><p class="math-copy">${esc(r.working.mawa_extension||'')}</p>`:''}</details>`).join('')||'<p>No completed sessions yet.</p>'}</section>`;
}

async function exportProgressBackup(){
  const tables=["profiles","progress_state","session_records","problem_attempts","exam_sittings"];
  const out={schema_version:"summit-one-progress-export-v1",exported_at:new Date().toISOString(),user_id:user.id,data:{}};
  for(const table of tables){
    let q=supabase.from(table).select("*");
    if(table==="profiles")q=q.eq("id",user.id);else q=q.eq("user_id",user.id);
    const {data,error}=await q;if(error)throw error;out.data[table]=data||[];
  }
  const blob=new Blob([JSON.stringify(out,null,2)],{type:"application/json"});
  const a=document.createElement("a");a.href=URL.createObjectURL(blob);a.download="Summit-One-progress-"+new Date().toISOString().slice(0,10)+".json";document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(a.href),1000);
}
async function renderProfile(){
  activeView="profile";await refreshEvidence();const r=currentRank();
  const done=progress.completed_sessions||0,currentXp=progress.xp??done*100;
  const nextRankSession=r>=20?null:Math.ceil(372*(r+1)/20);
  const nextRankXp=nextRankSession===null?0:Math.max(0,nextRankSession*100-currentXp);
  const [{data:completed},{data:exams}]=await Promise.all([supabase.from("session_records").select("session_number,summary,evidence").eq("user_id",user.id).not("completed_at","is",null),supabase.from("exam_sittings").select("exam_id,score,max_score,submitted_at,metadata").eq("user_id",user.id).eq("completed",true).order("submitted_at",{ascending:false}).limit(12)]);
  const focusCounts=new Map();
  for(const row of completed||[]){
    const focus=String(row.summary?.focus||course[row.session_number-1]?.focus||"").toLowerCase();
    for(const cat of taxonomy?.categories||[])for(const skill of cat.subskills||[]){
      const key=skill.name.toLowerCase();
      if(focus && (focus===key||focus.includes(key)||key.includes(focus)))focusCounts.set(skill.id,(focusCounts.get(skill.id)||0)+1);
    }
  }
  const covered=[...focusCounts.values()].filter(x=>x>0).length;
  app.innerHTML=`<section class="panel hero-panel"><div class="eyebrow">LEARNER PROFILE</div><h1>Summit progress</h1>
  <div class="profile-grid"><div class="panel profile-stat"><b>${progress.completed_sessions||0}</b><span>sessions complete</span></div><div class="panel profile-stat"><b>${overall().toFixed(1)}%</b><span>course complete</span></div><div class="panel profile-stat"><b>${r===0?"Cadet":r}</b><span>${r===0?"starting rank":"current rank"}</span></div><div class="panel profile-stat"><b>${nextRankSession===null?"MAX":nextRankXp}</b><span>${nextRankSession===null?"all 20 ranks unlocked":"XP to Rank "+(r+1)}</span></div></div><div class="profile-grid" style="margin-top:12px"><div class="panel profile-stat"><b>${progress.star3_correct||0}</b><span>3-star timed problems correct</span></div><div class="panel profile-stat"><b>${progress.star4_correct||0}</b><span>4-star timed problems correct</span></div><div class="panel profile-stat"><b>${progress.star5_correct||0}</b><span>5-star timed problems correct</span></div><div class="panel profile-stat"><b>${exams?.length||0}</b><span>recent exams in history</span></div></div>
  <h2 style="margin-top:28px">Technique evidence map</h2><p class="muted">A check means the technique has appeared in a completed session. It does <b>not</b> automatically mean independent mastery; timed and transfer evidence remains separate.</p>
  <div class="technique-map">${(taxonomy?.categories||[]).map(cat=>`<article class="tech-category"><div class="eyebrow">${esc(cat.id)}</div><h3>${esc(cat.name)}</h3><div class="tech-list">${cat.subskills.map(sk=>{const n=focusCounts.get(sk.id)||0,recall=recallState(completedRecords,sk.id);return `<div class="tech ${n?"covered":""}"><span>${n?"✓":"○"}</span><div><b>${esc(sk.name)}</b><small>${esc(sk.id)} · ${recall.retained?"retained on delayed checks · ":""}${n?n+" completed-session exposure"+(n===1?"":"s"):"not yet completed"}</small></div></div>`}).join("")}</div></article>`).join("")}</div>
  <h2 style="margin-top:28px">Recent timed assessments</h2><div class="history-list">${(exams||[]).map(e=>`<div class="history-row"><div><b>${esc(e.metadata?.title||e.exam_id)}</b><small>${e.submitted_at?new Date(e.submitted_at).toLocaleDateString():""}</small></div><div class="history-score">${e.score??"—"} / ${e.max_score}</div><div class="history-award">${esc(e.metadata?.award||"")}</div></div>`).join("")||'<div class="empty">No timed assessments completed yet.</div>'}</div><h2 style="margin-top:28px">20 explorer ranks</h2><div class="rank-grid">${rankNames.map((n,i)=>`<div class="rank ${i+1>r?"locked":""}"><span class="rank-emblem" aria-hidden="true">${i+1}</span><div><span class="rnum">RANK ${i+1}</span><b>${esc(n)}</b><small class="muted">${Math.ceil(372*(i+1)/20)} sessions</small></div></div>`).join("")}</div>
  <div class="complete-row"><a class="secondary" href="tests.html">Open AMC Test Centre</a><button id="exportProgress" class="ghost">Export progress backup</button><button id="logout" class="danger">Sign out</button></div>
  <p class="footer-note">Ranks recognise course completion; they do not replace evidence of independent mathematical mastery.</p></section>`;
  document.getElementById("exportProgress").onclick=async()=>{const b=document.getElementById("exportProgress");b.disabled=true;try{await exportProgressBackup()}catch(e){alert(e.message)}finally{b.disabled=false}};
  document.getElementById("logout").onclick=async()=>{await signOut();location.href="login.html"};
}
boot();

