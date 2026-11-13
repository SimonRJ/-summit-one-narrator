import {mixedFlashDeck} from './flash-cards.js?v=recognition-20261113';
import {wordingHTML} from './recognition.js?v=recognition-20261113';
import {bridgeHTML,mountPractice} from './transfer-practice.js?v=cinematic-practice-20261113';
import {allRows,queueLessonRepairs,renderRepairs,mountInvestigationReview,rubricHTML} from './learning-support.js?v=recognition-20261113';
import {mountFlashCards,flashReviewed} from './flash-ui.js?v=recognition-20261113';
import {selectOriginalProblems,familySeen,reasoningReady,applicationStatus,mountReasoning,originalFigure,LEARNING_VERSION} from './original-learning.js?v=cinematic-practice-20261113';
import {introductionHTML,lessonPlan,investigationIntroHTML,investigationWarmupHTML} from './session-intros.js?v=recognition-20261113';

if("serviceWorker" in navigator){window.addEventListener("load",()=>navigator.serviceWorker.register("./sw.js").catch(()=>{}));}
import { supabase, loadProgress, saveProgress, signOut, currentUser, upsertSession } from "./supabase-client.js?v=auth-20261112";
import { mountNarratedPlayer } from "./lesson-player.js";
import {methods,skillFor,recallState} from "./curriculum.js?v=recognition-20261113";
import {lessonCard,mountCheck,mountRetrieval,readinessHTML} from "./learning-ui.js?v=recognition-20261113";
import { problemFigure } from "./problem-figures.js";
import {mountLessonPager} from "./lesson-pager.js?v=cinema-20261113";
import {learningScreens} from "./lesson-screenflow.js?v=cinematic-practice-20261113";
import {buildCourseNavigation} from "./course-menu.js?v=menu-20261113";
import {mountCourseMenu} from "./course-menu-ui.js?v=lesson-replay-20261113";

const app=document.getElementById("app");
const problemTemplate=document.getElementById("problemTemplate");
let course=[], teaching=[], mawa=[], rossMap=[], taxonomy=null, milestones=null, problemIndex=[], progress=null, user=null, activeView="home", activeStage=-1, activeLessonPanel=0, lessonPager=null;
let lessonManifest=[];
let courseNavigation=null,mainMenu=null;
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
const rankNames=["Pathfinder","Pattern Scout","Model Builder","Logic Ranger","Number Navigator","Geometry Pilot","Counting Specialist","Invariant Hunter","Transfer Thinker","Proof Builder","Problem Solver","Strategy Captain","Olympiad Explorer","Insight Engineer","Reasoning Commander","AMC Specialist","MAWA Specialist","Rossmoyne Specialist","Summit Elite","Summit Scholar"];
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
 const [records,exams]=await Promise.all([
 allRows(()=>supabase.from('session_records').select('session_number,completed_at,summary,answers,working,evidence').eq('user_id',user.id).not('completed_at','is',null).order('session_number')),
 allRows(()=>supabase.from('exam_sittings').select('id,exam_id,score,max_score,submitted_at,metadata').eq('user_id',user.id).eq('completed',true).order('submitted_at',{ascending:false}).order('id'))]);
 completedRecords=records.map(r=>({...r,summary:{...r.summary,skill_id:r.summary?.skill_id||skillFor(course[r.session_number-1]||{},taxonomy)}}));recentExams=exams;
}
async function openRepairs(){document.body.classList.remove("home-focus");await refreshEvidence();await renderRepairs(app,{user,done:progress.completed_sessions||0,records:completedRecords});}
async function renderRoadmap(){document.body.classList.remove("home-focus");await refreshEvidence();app.innerHTML=readinessHTML({records:completedRecords,taxonomy,progress,milestones,exams:recentExams});}
async function boot(){
  try{
    user=await currentUser();
    if(!user){location.href="login.html";return}
    const [c,t,m,h,tax,ms,lm]=await Promise.all([fetch("data/sessions-372.json").then(r=>r.json()),fetch("data/teaching-72.json").then(r=>r.json()),fetch("data/mawa-investigations-20.json").then(r=>r.json()),fetch("data/rossmoyne-h23.json").then(r=>r.json()),fetch("data/taxonomy-52.json").then(r=>r.json()),fetch("data/milestones.json").then(r=>r.json()),fetch("data/lesson-challenges.json?v=recognition-20261113").then(r=>r.json())]);
    course=c.sessions; teaching=t.items; mawa=m.items; rossMap=h.items; taxonomy=tax; milestones=ms;lessonManifest=lm.items;courseNavigation=buildCourseNavigation(course,taxonomy);
    const {data:problems,error}=await supabase.from("content_problems_student").select("id,source_type,title,source_label,category,difficulty,prompt,unit").eq("source_type","original_authored").order("id");
    if(error)throw error; problemIndex=problems||[];
    attemptHistory=await allRows(()=>supabase.from('problem_attempts').select('problem_id,independent_credit,is_correct,created_at').eq('user_id',user.id).not('answer_text','is',null).order('created_at').order('id'));
    attemptedProblemIds=new Set(attemptHistory.map(x=>x.problem_id));
    progress=await loadProgress();
    if(!progress)progress=await saveProgress({current_session:0,completed_sessions:0,xp:0,rank:0,overall_percent:0,state:{}});
    await refreshEvidence();
    // Recover a completed session if the separate progress write lost its connection.
    let contiguous=0;while(completedRecords.some(r=>r.session_number===contiguous+1))contiguous++;
    if(contiguous>(progress.completed_sessions||0))progress=await saveProgress({completed_sessions:contiguous,current_session:Math.min(372,contiguous+1),xp:contiguous*100,rank:earnedRankBySessions(contiguous),overall_percent:contiguous/372*100});
    wireNav();updateNavProgress(); const requestedView=new URLSearchParams(location.search).get("view");if(location.hash==="#repairs"||requestedView==="repairs")await openRepairs();else if(requestedView==="roadmap")await renderRoadmap();else if(requestedView==="review")await renderReview();else if(requestedView==="profile")await renderProfile();else if(requestedView==="technique")renderTechniqueRefresher();else renderHome();
  }catch(e){app.innerHTML='<section class="panel hero-panel"><h1>Unable to load Summit One</h1><p class="muted">'+esc(e.message)+'</p></section>'}
}

function updateNavProgress(){mainMenu?.refreshProgress()}
async function navigateMenuView(view){
 const loadToken=window.SummitLoader?.beginSmall("Opening "+({home:"Learning",profile:"Progress",review:"Completed sessions",repairs:"Repairs",roadmap:"Readiness"}[view]||"section"));
 try{
 if(editingSession){
  await saveDraft(editingSession);
  editingSession=null;
 }
 document.body.classList.remove("lesson-fullscreen","home-focus","lesson-video-review");
 activeView=view;
 if(view==="home"){renderHome();return}
 if(view==="profile"){await renderProfile();return}
 if(view==="review"){await renderReview();return}
 if(view==="repairs"){await openRepairs();return}
 if(view==="roadmap"){await renderRoadmap();return}
 throw new Error("Unknown menu destination");
 }finally{window.SummitLoader?.endSmall(loadToken)}
}
async function continueFromMenu(){
 const done=Number(progress?.completed_sessions)||0;
 if(done>=372){await navigateMenuView("profile");return}
 const session=courseSession();
 if(editingSession?.slot===session.slot)return;
 if(editingSession){await saveDraft(editingSession);editingSession=null}
 await startSession(session);
}
async function openCompletedFromMenu(slot){
 if(!Number.isInteger(slot)||slot>(Number(progress?.completed_sessions)||0))throw new Error("This session has not been completed");
 await navigateMenuView("review");
 const details=app.querySelector('[data-review-session="'+slot+'"]');
 if(details){details.open=true;details.scrollIntoView({behavior:"auto",block:"start"})}
}
async function openLessonIntroductionFromMenu(slot){
 const loadToken=window.SummitLoader?.beginSmall("Preparing lesson video");
 try{
 const item=course.find(s=>s.slot===slot&&s.type==="LESSON");
 const done=Number(progress?.completed_sessions)||0;
 const isComplete=slot<=done;
 const isCurrent=slot===courseSession()?.slot&&done<372;
 if(!item||(!isComplete&&!isCurrent))throw new Error("This lesson is not available for review yet.");
 if(editingSession){
  await saveDraft(editingSession);
  editingSession=null;
 }
 document.body.classList.remove("home-focus","lesson-fullscreen");
 document.body.classList.add("lesson-video-review");
 setLessonScreenTopbar();
 activeView="lesson-intro-review";
 const introId=item.slot===1?"S001":item.slot===2?"S002":null;
 const teaching=teachingFor(item)[0]||null;
 const media=introId?`<div class="lesson-replay-video"><video id="replayIntroVideo" controls playsinline preload="metadata" poster="media/${introId}-Intro-poster.jpg?v=cinema-20261113" src="media/${introId}-Intro.mp4?v=cinema-20261113" aria-label="${esc(item.focus)} · animated introduction"><track kind="captions" srclang="en" label="English captions" src="media/${introId}-Intro.vtt?v=cinema-20261113"></video></div>`:
  teaching?`<div id="replayNarratedTeaching" class="lesson-replay-narration"></div>`:
  '<p class="muted">An animated introduction has not yet been published for this lesson. The original lesson and written explanations remain available.</p>';
 app.innerHTML=`<section class="panel lesson-replay-page" aria-label="Read-only lesson video review">
   <div class="eyebrow">LESSON ${item.slot} · ${isComplete?"COMPLETED — REPLAY ONLY":"CURRENT — REVIEW"}</div>
   <h1>${esc(item.focus)}</h1>
   <p class="muted">${introId?"Replay the original easy, medium and hard worked examples.":teaching?"Review the available narrated concept teaching. A dedicated three-level introduction has not yet been published for this lesson.":"The video for this lesson is not yet published."}</p>
   ${media}
   <p class="lesson-replay-note">${isComplete?"Your original answers, score and completion status stay locked. Replaying this video cannot restart the lesson.":"This is an optional teaching review. Your current answers and lesson position remain saved."}</p>
   <div class="lesson-replay-actions"><button type="button" id="replayBack" class="secondary">${isComplete?"Back to saved lesson":"Return to current lesson"}</button><button type="button" id="replayHome" class="ghost">Learning home</button></div>
 </section>`;
 if(!introId&&teaching){
  mountNarratedPlayer(document.getElementById("replayNarratedTeaching"),{
   title:teaching.title,transcript:teaching.transcript,audioUrl:teaching.audio_url,
   videoUrl:finalVideoUrl(teaching.id),cacheKey:"read-only-lesson:"+item.slot
   // Deliberately no onWatch callback and no session-record mutation.
  });
 }
 document.getElementById("replayBack").onclick=async()=>{document.body.classList.remove("lesson-video-review");if(isComplete)await openCompletedFromMenu(slot);else await continueFromMenu()};
 document.getElementById("replayHome").onclick=()=>{document.body.classList.remove("lesson-video-review");renderHome()};
 }finally{window.SummitLoader?.endSmall(loadToken)}
}
function wireNav(){
 mainMenu=mountCourseMenu({
  navigation:courseNavigation,
  getDone:()=>Number(progress?.completed_sessions)||0,
  getCurrent:()=>courseSession(),
  onContinue:continueFromMenu,
  onCompleted:openCompletedFromMenu,
  onIntroduction:openLessonIntroductionFromMenu,
  onView:navigateMenuView
 });
}
function renderTechniqueRefresher(){
 document.body.classList.remove("home-focus");
 activeView="technique";
 const p=new URLSearchParams(location.search);
 const slot=Number(p.get("slot"));
 const session=course.find(x=>x.slot===slot&&x.type==="LESSON");
 const skill=String(p.get("skill")||"").replace(/^LOG-(\d{2})$/,"LOGIC-$1");
 const valid=Object.values(taxonomy?.categories||[]).some(c=>(c.subskills||[]).some(x=>x.id===skill));
 if(!session||!valid){app.innerHTML='<section class="panel hero-panel"><h1>Learning review unavailable</h1><p>This session reference could not be matched.</p><a class="secondary" href="./">Return to Learning</a></section>';return;}
 const m=methods[skill]||{};
 const videos=teachingFor(session).slice(0,2);
 const previouslyCompleted=completedRecords.some(r=>r.session_number===slot);
 app.innerHTML=`<section class="panel hero-panel technique-review"><div class="eyebrow">POST-EXAM LEARNING REVIEW · SESSION ${slot}</div><h1>${esc(session.focus)}</h1><p>Revisit the mathematical idea behind this problem, without using the original exam answer as a template.</p><p class="muted">${previouslyCompleted?"This session has previously been completed; your original records remain locked.":"This session lies in the learning pathway. Viewing this explanation does not skip ahead or mark it completed."}</p><div class="complete-row"><a class="ghost" href="tests.html">Back to Exams</a><a class="secondary" href="index.html?view=review">My completed-session notebook</a><a class="secondary" href="./">Continue the learning pathway</a></div></section>
 <section class="panel learning-refresher"><div class="eyebrow">WHAT, WHY AND WHERE</div>${introductionHTML(session,course,taxonomy)}</section>
 <section class="panel learning-refresher"><div class="eyebrow">THE RELEVANT TECHNIQUE</div>${lessonCard(skill,lessonPlan(session,course,taxonomy))}<h3>Key reasoning</h3><p class="math-copy">${esc(m.idea||"Represent the situation, identify the key constraint, and explain why your method covers every case.")}</p><h3>What to watch for</h3><p class="math-copy">${esc(m.trap||"Check the original conditions and validate your answer another way.")}</p></section>
 <section class="panel learning-refresher"><h2>Related teaching and worked examples</h2><div class="technique-review-videos">${videos.map((t,i)=>`<article class="teaching-item"><h3>${esc(t.title)}</h3><div id="techniqueVideo${i}" class="lesson-player-slot"></div><details><summary>Read the full explanation</summary><p class="math-copy">${esc(t.transcript)}</p></details></article>`).join("")||'<p class="muted">The written technique above is available for this session.</p>'}</div></section>
 <section class="panel learning-refresher"><h2>Transfer to a fresh problem</h2><p>In your notebook, write the clue that suggests this method, the mathematical argument, and a check that would catch a mistake. Then work on an unfamiliar problem in the next scheduled session.</p><a class="primary" href="./">Return to current session</a></section>`;
 videos.forEach((t,i)=>mountNarratedPlayer(document.getElementById("techniqueVideo"+i),{title:t.title,transcript:t.transcript,audioUrl:t.audio_url,videoUrl:finalVideoUrl(t.id),cacheKey:t.id}));
}
function renderHome(){
 document.body.classList.remove("lesson-fullscreen","lesson-video-review");
 document.body.classList.add("home-focus");
 setLessonScreenTopbar();
 activeView="home";
 updateNavProgress();
 const session=courseSession(),done=Number(progress?.completed_sessions)||0,finished=done>=372;
 app.innerHTML=`<section class="learning-focus" aria-label="Continue mathematics learning">
   <article class="panel focus-session-card">
     <div class="eyebrow">YOUR LEARNING PATH</div>
     <span class="session-kicker">${finished?"ALL SESSIONS COMPLETE":`SESSION ${session.slot}`}</span>
     <h1>${finished?"Course completed":esc(session.focus)}</h1>
     <p class="muted">${finished?"Review your progress and completed work.":"Continue with the next part of your lesson."}</p>
     <button id="continue" type="button" class="primary cta">${finished?"View progress":`Continue Session ${session.slot}`}</button>
   </article>
 </section>`;
 document.getElementById("continue").onclick=()=>finished?renderProfile():startSession(session);
}
async function startSession(s){
 document.body.classList.remove("home-focus");
 const loadToken=window.SummitLoader?.beginSmall("Opening Session "+s.slot);
 try{
  await refreshEvidence();
  activeStage=0;currentMawa=s.type==="MAWA"?mawa[(Math.floor(s.slot/7)-1)%mawa.length]:null;
  const {data:existing,error}=await supabase.from("session_records").select("*").eq("user_id",user.id).eq("session_number",s.slot).maybeSingle();if(error)throw error;
  if(existing?.immutable){await refreshEvidence();renderReview();return}
  sessionDraft={answers:existing?.answers||{},working:existing?.working||{},evidence:existing?.evidence||{},summary:existing?.summary||{}};
  const local=JSON.parse(localStorage.getItem(draftKey(s))||'null');
  if(local?.draft&&(!existing?.updated_at||local.updated_at>existing.updated_at))sessionDraft=local.draft;
  if(s.type==="LESSON"){
    const stage=Number(sessionDraft.summary.lesson_stage);
    activeStage=Number.isInteger(stage)&&stage>=-1&&stage<=4?stage:-1;
    activeLessonPanel=Math.max(0,Number(sessionDraft.summary.lesson_panel)||0);
  }else{activeStage=0;activeLessonPanel=0;}
  editingSession=s;
  const previous=sessionDraft.summary.problems||[];
  currentProblems=chooseProblems(s);
  // Preserve saved answers and working, including legacy drafts, but replace the active tasks.
  const retired=previous.filter(id=>!currentProblems.some(p=>p.id===id));
  sessionDraft.summary={...sessionDraft.summary,previous_problem_ids:[...new Set([...(sessionDraft.summary.previous_problem_ids||[]),...retired])],learning_version:LEARNING_VERSION,problems:currentProblems.map(p=>p.id),skill_id:skillFor(s,taxonomy),focus:s.focus,type:s.type,phase:s.phase};
  await saveDraft(s);
  if(s.type==="MAWA"){renderMawaSession(s);return}if(s.type==="MIXED"){renderWorkshop(s);return}renderSession(s);
 }catch(e){alert("Could not open this session: "+e.message)}
 finally{window.SummitLoader?.endSmall(loadToken)}
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
    el.innerHTML=`${investigationIntroHTML(s,item)}<div class="stage-number">NOW REMEMBER · A USEFUL HABIT</div><h2>Bring back an idea</h2><p class="muted">Try small cases and build a mathematical solution in your notebook.</p><div class="teaching-item"><h3>${prev?esc(prev.title):"Proof habit"}</h3><p class="math-copy">${prev?"Try a smaller version of today’s problem before attempting the full challenge.":"Test a few examples and look for the most important condition."}</p></div><div class="complete-row"><span></span><button id="nextStage" class="primary">Discover</button></div>`;
  }
  if(activeStage===1){
    el.innerHTML=`<div class="stage-number">STAGE 2 · INVESTIGATION SETUP</div><h2>Discover</h2>${investigationWarmupHTML(item)}<div id="investigationCards"></div><h3>Now grow the investigation</h3><p class="muted">Read the problem slowly. Decide what evidence would count as a proof before calculating.</p><div class="problem-card"><div class="problem-meta">${esc(item.topic)}</div><h3 class="problem-title">${esc(item.title)}</h3><div class="problem-prompt math-copy">${esc(item.prompt)}</div><details style="margin-top:14px"><summary>First hint — use only if you are genuinely stuck</summary><p class="math-copy">${esc(item.hint)}</p></details></div><div class="complete-row"><span class="muted">Plan cases, a diagram, a table or an invariant.</span><button id="nextStage" class="primary">Try the investigation</button></div>`;
  }
  if(activeStage===1)mountFlashCards(el.querySelector('#investigationCards'),{id:item.id,visit:1+Math.floor((Math.floor(s.slot/7)-1)/20),slot:s.slot,investigation:true,draft:sessionDraft,save:()=>saveDraft(s)});
  if(activeStage===2){
    const recorded=Boolean(sessionDraft.evidence.mawa_base?.status);
    el.innerHTML=`<div class="stage-number">STAGE 3 · INDEPENDENT INVESTIGATION</div><h2>Solve the investigation</h2>
      <p class="muted">Work on paper or in a maths notebook. Use a table, diagram, calculation or proof as needed. There is no written response to type into the app.</p>
      <div class="problem-card"><div class="math-copy">${esc(item.prompt)}</div>
      <details class="mawa-paper-hint"><summary>Show a hint if you are stuck</summary><p class="math-copy">${esc(item.hint)}</p></details>
      <button id="recordMawa" class="primary" ${recorded?"disabled":""}>${recorded?"Attempt recorded":"I have attempted this problem on paper"}</button>
      <div id="mawaMsg" class="attempt-feedback" ${recorded?"":"hidden"}>Notebook attempt recorded; check your mathematical work against the model in the last stage.</div></div>
      <div class="complete-row"><button id="backStage" class="ghost">Back</button><button id="nextStage" class="primary">Transfer</button></div>`;
    document.getElementById("recordMawa").onclick=async event=>{
      event.target.disabled=true;
      sessionDraft.evidence.mawa_base={status:"attempted_on_paper_unreviewed",recorded_at:new Date().toISOString()};
      try{await saveDraft(s);const note=document.getElementById("mawaMsg");note.hidden=false;note.textContent="Notebook attempt saved. The proof has not been independently assessed."}
      catch(error){event.target.disabled=false;alert("Could not save your attempt: "+error.message)}
    };
  }
  if(activeStage===3){
    const ext=(item.transfer_prompt||mawaExtension(s,item))+(Math.floor(s.slot/7)>20?" Then change a condition, predict the effect, and test a general rule or counterexample.":""),recorded=Boolean(sessionDraft.evidence.mawa_extension?.status);
    el.innerHTML=`<div class="stage-number">STAGE 4 · TRANSFER TO A NEW CASE</div><h2>Solve the extension</h2>
      <p class="muted">${esc(ext)}</p><p>Solve this new mathematical problem in your notebook. No typed explanation is needed.</p>
      <button id="recordExt" class="primary" ${recorded?"disabled":""}>${recorded?"Extension attempt recorded":"I have attempted the extension on paper"}</button>
      <div id="mawaExtMsg" class="attempt-feedback" ${recorded?"":"hidden"}>Extension attempted on paper.</div>
      <div class="complete-row"><button id="backStage" class="ghost">Back</button><button id="nextStage" class="primary">Check</button></div>`;
    document.getElementById("recordExt").onclick=async event=>{
      event.target.disabled=true;
      sessionDraft.evidence.mawa_extension={status:"attempted_on_paper_unreviewed",recorded_at:new Date().toISOString()};
      try{await saveDraft(s);const note=document.getElementById("mawaExtMsg");note.hidden=false;note.textContent="Notebook extension saved."}
      catch(error){event.target.disabled=false;alert("Could not save the extension attempt: "+error.message)}
    };
  }
  if(activeStage===4){
    const ready=Boolean(sessionDraft.evidence.mawa_base?.status&&sessionDraft.evidence.mawa_extension?.status);
    el.innerHTML=`<div class="stage-number">STAGE 5 · PROOF CHECK</div><h2>Check</h2><p class="muted">Score the evidence, not confidence. This is a practice rubric, not an official MAWA admissions score.</p><div class="problem-card"><details ${ready?"":"hidden"}><summary>Compare with model reasoning</summary><p class="solution-panel" style="display:block">${esc(item.solution)}</p>${item.transfer_solution?`<h4>Check the new setting</h4><p class="math-copy">${esc(item.transfer_solution)}</p>`:""}<p class="muted"><b>Common trap:</b> ${esc(item.trap)}</p></details>${rubricHTML()}<div class="check-grid"><label class="answer-label">Result 0–3<input id="rResult" type="number" min="0" max="3" value="" required></label><label class="answer-label">Method 0–3<input id="rMethod" type="number" min="0" max="3" value="" required></label><label class="answer-label">Proof / completeness 0–3<input id="rProof" type="number" min="0" max="3" value="" required></label><label class="answer-label">Clarity 0–1<input id="rClarity" type="number" min="0" max="1" value="" required></label></div></div><div class="complete-row"><span class="muted">${ready?"Investigation and extension recorded.":"Record both the investigation and extension before completion."}</span><button id="completeMawa" class="primary" ${ready?"":"disabled"}>Complete and lock Session ${s.slot}</button></div>`;
    if(ready)document.getElementById("completeMawa").onclick=async()=>{if(!["rResult","rMethod","rProof","rClarity"].every(id=>{const x=document.getElementById(id);return x.value!==""&&x.checkValidity()})){alert("Enter each rubric score after comparing the reasoning.");return}const rubric={result:Number(document.getElementById("rResult").value),method:Number(document.getElementById("rMethod").value),proof:Number(document.getElementById("rProof").value),clarity:Number(document.getElementById("rClarity").value)};sessionDraft.summary={...sessionDraft.summary,review_status:"self_reviewed_not_independently_verified",focus:item.title,type:"MAWA",phase:s.phase,investigation_id:item.id,rubric,total:rubric.result+rubric.method+rubric.proof+rubric.clarity};const button=document.getElementById("completeMawa");button.disabled=true;try{await completeSpecialSession(s)}catch(e){alert("Could not finish saving: "+e.message);button.disabled=false}};
  }
  const next=document.getElementById("nextStage");if(next)next.onclick=async()=>{if(activeStage===1&&!flashReviewed(sessionDraft,item.id)){alert("Finish the five quick decisions and read the recap, then grow the investigation.");return}await saveDraft(s);activeStage=Math.min(4,activeStage+1);renderMawaSession(s)};
  const back=document.getElementById("backStage");if(back)back.onclick=async()=>{try{await saveDraft(s);activeStage=Math.max(0,activeStage-1);renderMawaSession(s)}catch(e){alert(e.message)}};
}
async function completeSpecialSession(s){
 clearTimeout(autosaveTimer);await queueLessonRepairs(user.id,s.slot,sessionDraft,progress.completed_sessions||0);
  await upsertSession({session_number:s.slot,session_key:`S${String(s.slot).padStart(3,"0")}`,completed_at:new Date().toISOString(),immutable:true,answers:sessionDraft.answers,working:sessionDraft.working,evidence:sessionDraft.evidence,summary:sessionDraft.summary});
  const done=Math.max(progress.completed_sessions||0,s.slot),p=done/372*100,r=Math.max(Number(progress.rank||0),Math.max(0,Math.min(20,Math.floor(done*20/372))));
  progress=await saveProgress({completed_sessions:done,current_session:Math.min(372,done+1),xp:done*100,rank:r,overall_percent:Number(p.toFixed(2)),next_practice_exam_in:(course.find(x=>x.slot>done&&(x.type==="MIXED"))?.slot??done)-done});
  localStorage.removeItem(draftKey(s));editingSession=null;draftDirty=false;await refreshEvidence();renderHome();
}

function renderLessonOpening(el,s){
 const id=s.slot===1?"S001":s.slot===2?"S002":null;
 const p=lessonPlan(s,course,taxonomy);
 const title=esc(s.focus);
 const examples=id?'<p class="opening-levels"><span>Easy example</span><span>Medium example</span><span>Hard example</span></p>':'';
 el.innerHTML=`<section class="opening-film" aria-label="Lesson introduction">
   <div class="eyebrow">THE IDEA FIRST · A VISUAL EXPLANATION</div>
   <h2>${title}</h2>
   <p class="muted">Watch how a useful mathematical idea solves progressively harder problems. The problems in this introduction are teaching examples, not practice-test questions.</p>
   ${id?`<div class="opening-video-wrap"><video id="openingVideo" controls playsinline preload="metadata" poster="media/${id}-Intro-poster.jpg?v=cinema-20261113" src="media/${id}-Intro.mp4?v=cinema-20261113" aria-label="${title} — fully worked animated introduction in three difficulty levels"><track kind="captions" srclang="en" label="English captions" src="media/${id}-Intro.vtt?v=cinema-20261113"></video></div>`:
   `<div class="opening-concept-board"><div class="opening-concept-method">${esc(p.hook)}</div><div class="opening-concept-mark">${esc(skillFor(s,taxonomy))}</div><p>${esc(p.goal)}</p></div>`}
   ${examples}
   <div id="openingFallback" class="opening-fallback" ${id?"hidden":""}></div>
   <p class="opening-coda">After watching, press <b>Next</b> and solve fresh problems using the same idea. Bring paper and a pencil.</p>
 </section>`;
 const mountFallback=()=>{
  const host=el.querySelector("#openingFallback");
  if(!host||host.dataset.mounted)return;
  host.hidden=false;host.dataset.mounted="yes";
  const t=teachingFor(s)[0];
  if(t)mountNarratedPlayer(host,{title:t.title,transcript:t.transcript,audioUrl:t.audio_url,videoUrl:finalVideoUrl(t.id),cacheKey:"lesson-opening-"+s.slot,onWatch:d=>recordVideoEvidence(s.slot,t.id,"concept",d)});
  else host.innerHTML='<p class="muted">The short written introduction is available in the next screen.</p>';
 };
 const video=el.querySelector("#openingVideo");
 if(video){
  video.addEventListener("error",()=>{video.hidden=true;mountFallback()});
  let marked=false;
  video.addEventListener("timeupdate",()=>{
   if(marked||!video.duration||video.currentTime/video.duration<.8)return;
   marked=true;recordVideoEvidence(s.slot,id+"-Intro","lesson_intro",{position_seconds:video.currentTime,duration_seconds:video.duration,completed_80_percent:true,media_mode:"finished_video"}).catch(()=>{});
  });
 }else mountFallback();
}
function setLessonScreenTopbar(){
 document.body.style.setProperty("--lesson-topbar",Math.ceil(document.querySelector(".topbar")?.getBoundingClientRect().height||72)+"px");
}
window.addEventListener("resize",()=>{
 if(document.body.classList.contains("lesson-fullscreen")||document.body.classList.contains("home-focus")||document.body.classList.contains("lesson-video-review"))setLessonScreenTopbar();
});
function renderSession(s){
 document.body.classList.remove("home-focus","lesson-video-review");
 document.body.classList.add("lesson-fullscreen");
 setLessonScreenTopbar();
 const stages=["Video","Remember","Discover","Try","Transfer","Check"];
 const stageIndex=activeStage+1;
 app.innerHTML=`<section class="session-page lesson-screen-page" aria-label="Session ${s.slot} screen by screen">
  <header class="panel lesson-screen-header"><div class="eyebrow">LEARNING SESSION ${s.slot} / 372 · ${esc(s.phase)}</div><h1>${esc(s.focus)}</h1></header>
  <div class="lesson-stage-track" aria-label="Your current lesson stage">${stages.map((label,i)=>`<span class="${i===stageIndex?"here":i<stageIndex?"visited":""}">${i+1}. ${label}</span>`).join("")}</div>
  <section id="stage" class="panel stage lesson-screen-stage"></section>
  <footer class="lesson-screen-footer"><button type="button" class="ghost" data-screen-back>Back</button><div class="lesson-screen-progress"><strong data-screen-name>Learning</strong><span data-screen-count>1 / 1</span></div><button type="button" class="primary" data-screen-next>Next</button></footer>
 </section>`;
 const target=document.getElementById("stage"),sid=skillFor(s,taxonomy);
 if(activeStage===-1)renderLessonOpening(target,s);
 if(activeStage===0)renderRemember(target,s);
 if(activeStage===1)renderDiscover(target,s);
 if(activeStage===2)renderChallenge(target,s,currentProblems[0],"try");
 if(activeStage===3)renderChallenge(target,s,currentProblems[1],"transfer");
 if(activeStage===4)renderCheck(target,s);
 const pages=learningScreens(target,activeStage,{draft:sessionDraft,skill:sid,problem:activeStage===2?currentProblems[0]:activeStage===3?currentProblems[1]:null,slot:s.slot,flashDone:()=>flashReviewed(sessionDraft,sid)});
 const footer=app.querySelector(".lesson-screen-footer");
 const persistLocation=index=>{
  activeLessonPanel=index;sessionDraft.summary.lesson_stage=activeStage;sessionDraft.summary.lesson_panel=index;
  rememberDraft();
 };
 const leaveNext=async()=>{
  if(activeStage===-1){activeStage=0;activeLessonPanel=0;await saveDraft(s);renderSession(s);return}
  if(activeStage===4){const finish=target.querySelector("#completeSession");if(finish&&!finish.disabled)finish.click();else alert("Complete both challenge attempts before locking this session.");return}
  const next=target.querySelector("#nextStage");
  if(next){activeLessonPanel=0;next.click();}
 };
 const leaveBack=async()=>{
  if(activeStage===-1){await saveDraft(s);editingSession=null;document.body.classList.remove("lesson-fullscreen");renderHome();return}
  activeStage-=1;activeLessonPanel=999;await saveDraft(s);renderSession(s);
 };
 lessonPager=mountLessonPager({pages,footer,initial:activeLessonPanel,onNext:leaveNext,onBack:leaveBack,onChange:persistLocation});
}
function renderRemember(el,s){
 const p=lessonPlan(s,course,taxonomy);el.innerHTML=`<div class="lesson-recall-brief"><div class="eyebrow">REMEMBER · NO TIMER</div><h2>Bring back one useful idea</h2><p>${esc(p.prerequisite)}</p><p class="muted">A short check strengthens your understanding. It does not change your exam score.</p></div><div id="retrievalChecks"></div><div class="complete-row"><span class="muted">Try any due recall checks before continuing.</span><button class="primary" id="nextStage">Discover</button></div>`;
 mountRetrieval(el.querySelector('#retrievalChecks'),{records:completedRecords,slot:s.slot,currentId:skillFor(s,taxonomy),draft:sessionDraft,save:()=>saveDraft(s)});
 document.getElementById('nextStage').onclick=async()=>{if((sessionDraft.summary.retrieval_ids||[]).some(id=>!sessionDraft.evidence['retrieval:'+id])){alert('Try each short revision check. Use a hint if needed.');return}await saveDraft(s);activeStage=1;renderSession(s)};
}

function renderDiscover(el,s){
  const items=teachingFor(s);
  el.innerHTML=`<div class="stage-number">STAGE 2 · EXPLANATION</div><h2>Discover</h2><p class="muted">Read, sketch and listen. The goal is to see why the method works, not memorise a slogan.</p>
  <section data-lesson-unit="concept">${lessonCard(skillFor(s,taxonomy),lessonPlan(s,course,taxonomy))}</section><section data-lesson-unit="bridge">${bridgeHTML(skillFor(s,taxonomy),lessonPlan(s,course,taxonomy).visit)}</section><section data-lesson-unit="flash"><div id="quickCards"></div></section><section data-lesson-unit="guided"><div id="guidedCheck"><p class="muted">Work through the five quick decisions above, then try the supported problem.</p></div></section><section data-lesson-unit="more"><details class="optional-lesson"><summary>Optional deeper connection · related video or reading</summary><div class="teaching-box">${items.map((t,i)=>`<article class="teaching-item"><div class="eyebrow">${esc(t.type==="worked_example"?"WORKED EXAMPLE":"CONCEPT")}</div><h3>${esc(t.title)}</h3><div class="lesson-player-slot" id="lessonPlayer${i}"></div><details><summary>Read explanation</summary><p class="math-copy">${esc(t.transcript)}</p>${t.extended_reading?`<h4>Further mathematical connections</h4><p class="math-copy">${esc(t.extended_reading)}</p>`:""}</details></article>`).join("")||'<p class="muted">Teaching explanation is being selected from the course library.</p>'}</div></details></section>
  <div class="complete-row"><span class="muted">Try the supported question first. A hint is part of learning.</span><button class="primary" id="nextStage">Try independently</button></div>`;
  let guidedMounted=false;
  mountFlashCards(el.querySelector('#quickCards'),{id:skillFor(s,taxonomy),visit:lessonPlan(s,course,taxonomy).visit,slot:s.slot,draft:sessionDraft,save:()=>saveDraft(s),onComplete:()=>{
    if(guidedMounted||!el.isConnected)return;guidedMounted=true;
    mountCheck(el.querySelector("#guidedCheck"),{id:skillFor(s,taxonomy),slot:s.slot,records:completedRecords,draft:sessionDraft,kind:"guided",seedOverride:lessonPlan(s,course,taxonomy).visit%7,save:()=>saveDraft(s)});
  }});
  items.forEach((t,i)=>mountNarratedPlayer(document.getElementById("lessonPlayer"+i),{
    title:t.title,
    transcript:t.transcript,
    audioUrl:t.audio_url,
    videoUrl:finalVideoUrl(t.id),
    cacheKey:t.id,
    onWatch:detail=>recordVideoEvidence(s.slot,t.id,t.type,detail)
  }));
  document.getElementById("nextStage").onclick=async()=>{try{if(!flashReviewed(sessionDraft,skillFor(s,taxonomy))){alert("Finish the five quick decisions and read the recap first. Mistakes are part of the warm-up.");return}if(!sessionDraft.evidence["guided:"+skillFor(s,taxonomy)]){alert("Try the supported question first. Use the hint or worked example if needed.");return}await saveDraft(s);activeStage=2;renderSession(s)}catch(e){alert(e.message)}};
}
function renderChallenge(el,s,p,mode){
  const sid=skillFor(s,taxonomy), guided=sessionDraft.evidence['guided:'+sid], core=sessionDraft.evidence['retrieval:'+sid];
  if(!guided||(mode==='transfer'&&!core)){
    el.innerHTML=`<h2>Build the method first</h2><p>Before the stretch questions, try the supported example in Discover, then the short independent check in Try. You do not have to get everything right to continue; use the explanation to repair a mistake.</p><button id="prepareMethod" class="primary">${!guided?'Go to Discover':'Go to Try'}</button>`;
    el.querySelector('#prepareMethod').onclick=()=>{activeStage=!guided?1:2;renderSession(s)};return;
  }
  if(!p){el.innerHTML='<div class="empty">No challenge available.</div>';return}
  el.innerHTML=`<div class="stage-number">STAGE ${mode==="try"?3:4} · ${mode==="try"?"INDEPENDENT ATTEMPT":"TRANSFER"}</div><h2>${mode==="try"?"Try":"Transfer"}</h2><p class="muted">${mode==="try"?"Solve a few fresh problems to build accuracy. Then open the stretch problem.":"Solve unfamiliar problems, using paper for your working. Only enter your final answers here."}</p>`;
  const node=problemTemplate.content.firstElementChild.cloneNode(true);node.classList.add('lesson-problem-unit');
  node.querySelector(".problem-meta").textContent=`ORIGINAL LEARNING PROBLEM · ${mode==="try"?"APPLY THE IDEA":"CHOOSE YOUR METHOD"}`;
  node.querySelector(".problem-title").textContent=p.title||p.id;
  const promptEl=node.querySelector(".problem-prompt"); promptEl.textContent=p.prompt; const figure=originalFigure(p)||problemFigure(p.id); if(figure)promptEl.insertAdjacentHTML("beforebegin",figure);
  const box=node.querySelector(".answer-box"),submit=node.querySelector(".submit-answer"),reveal=node.querySelector(".reveal-solution"),feedback=node.querySelector(".attempt-feedback"),solution=node.querySelector(".solution-panel");
  const familiar=familySeen(completedRecords,p.learning.family);
  const reason=mountReasoning(node,{p,draft:sessionDraft,save:()=>saveDraft(s),showHint:()=>methods[p.learning.skill].idea});
  const saved=sessionDraft.answers[p.id];
  box.value=sessionDraft.working["draft-answer:"+p.id]||"";box.oninput=()=>{sessionDraft.working["draft-answer:"+p.id]=box.value};
  if(saved){box.value=saved.response||"";box.disabled=true;submit.hidden=true;reveal.hidden=false;feedback.hidden=false;feedback.textContent=applicationStatus(sessionDraft.evidence["application:"+p.id])+". Open the worked solution to compare."}
  submit.onclick=async()=>{
    const response=box.value.trim();if(!response){feedback.hidden=false;feedback.textContent="Enter your final answer first.";return}
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
      box.disabled=true;submit.hidden=true;reveal.hidden=false;feedback.textContent=applicationStatus(sessionDraft.evidence["application:"+p.id])+". Open the worked solution to learn the method.";
    }catch(e){feedback.textContent=e.message;submit.disabled=false}
  };
  reveal.onclick=async()=>{
    try{
      const {data:d,error:solutionError}=await supabase.functions.invoke("get-problem-solution",{body:{problem_id:p.id,session_number:s.slot}});
      if(solutionError)throw solutionError;
      if(d?.error)throw new Error(d.error);
      const transcript=d.spoken_script||d.solution_text||"Solution unavailable.";
      const writtenSolution=d.solution_text||transcript;
      solution.hidden=false;solution.innerHTML=`<b>Worked solution</b><div id="solutionPlayer-${p.id.replace(/[^A-Za-z0-9]/g,"_")}"></div><details style="margin-top:12px"><summary>Read full worked solution</summary><p class="math-copy">${esc(writtenSolution)}</p></details>`;
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
    const fade=document.createElement('div');fade.className='lesson-fade-unit';el.append(fade);
    mountPractice(fade,{id:sid,seed:lessonPlan(s,course,taxonomy).visit+8,key:'faded:'+sid,draft:sessionDraft,save:()=>saveDraft(s),supported:true,label:'YOUR TURN · FINISH THE NEXT EXAMPLE'});
    const prep=document.createElement('div');prep.className='lesson-prep-unit';el.appendChild(prep);
    node.hidden=!core;
    const unlock=e=>{node.hidden=false;const targetPage=lessonPager?.count?2:null;if(targetPage!==null)lessonPager.show(targetPage);};
    mountCheck(prep,{id:sid,slot:s.slot,records:completedRecords,draft:sessionDraft,save:()=>saveDraft(s),label:'YOUR TURN · INDEPENDENT BASICS CHECK',seedOverride:(lessonPlan(s,course,taxonomy).visit+1)%7,onDone:unlock});
  }
  if(mode==='transfer'&&s.slot>=16){const mix=document.createElement('div');mix.className='lesson-mix-unit';el.append(mix);mountMixed(mix,s,2);}
  // Six fresh numerical challenges supplement the protected original pair.
  // Only the final answer is typed; each attempt reveals worked mathematical steps.
  const extra=document.createElement('section');extra.className='lesson-extra-unit';extra.setAttribute('aria-label','More problem solving');
  const visit=lessonPlan(s,course,taxonomy).visit;
  for(let i=0;i<3;i++){
    const target=document.createElement('div');
    target.setAttribute('data-extra-question',String(i));
    extra.append(target);
    const key='drill:'+mode+':'+s.slot+':'+i;
    mountPractice(target,{id:sid,seed:s.slot*7+visit*5+(mode==='try'?0:3)+i,
      key,draft:sessionDraft,save:()=>saveDraft(s),
      label:(mode==='try'?'PRACTICE':'TRANSFER')+' · PROBLEM '+(i+1)+' OF 3'});
  }
  el.append(extra);

  const bridge=document.createElement('div');bridge.className='challenge-bridge';
  bridge.innerHTML=`<h3>${mode==='try'?'Next: apply the idea':familiar?'Transfer: practise a variation':'Transfer: choose your tools'}</h3><p>Solve it on paper, check the answer, and compare with the worked solution. Your approach may use more than one idea.</p><details><summary>A starting plan, without the answer</summary><ol><li>Restate the question in your own words.</li><li>Test a smaller case or draw the quantities.</li><li>Choose a useful operation or pattern, then calculate and verify the result.</li></ol></details>`;
  node.prepend(bridge);el.appendChild(node);
  const footer=document.createElement("div");footer.className="complete-row";footer.innerHTML=`<button class="ghost" id="prevStage">Back</button><button class="primary" id="nextStage">${mode==="try"?"Transfer":"Check"}</button>`;el.appendChild(footer);
  footer.querySelector("#prevStage").onclick=async()=>{await saveDraft(s);activeStage=mode==="try"?1:2;renderSession(s)};
  footer.querySelector("#nextStage").onclick=async()=>{await saveDraft(s);activeStage=mode==="try"?3:4;renderSession(s)};
}
function renderCheck(el,s){
  const sid=skillFor(s,taxonomy);
  const attempted=currentProblems.filter(p=>sessionDraft.answers[p?.id]).length;
  const modeKeys=['try','transfer'].flatMap(mode=>[0,1,2].map(i=>'drill:'+mode+':'+s.slot+':'+i));
  const drilled=modeKeys.filter(key=>Boolean(sessionDraft.evidence[key])).length;
  const scores=currentProblems.map((p,i)=>{
    const a=sessionDraft.answers[p?.id],status=applicationStatus(sessionDraft.evidence['application:'+p?.id]);
    return `<div class="lesson-result-line"><span>${i===0?'Practice challenge':'Transfer challenge'}</span><strong>${esc(status)}</strong></div>`;
  }).join('');
  el.innerHTML=`<div class="lesson-check-summary">
    <div class="eyebrow">CHECK · RESULTS</div><h2>Problems solved</h2>
    <p class="muted">No written reflection required. Use your notebook for calculations and review the worked solutions whenever you need them.</p>
    <div class="lesson-check-total"><strong>${attempted} / 2</strong><span>Original challenge attempts</span></div>
    <div class="lesson-check-total"><strong>${drilled} / 6</strong><span>Extra problem-solving checks</span></div>
    <div class="lesson-check-status">${scores}</div>
    <p class="muted">Mistakes are useful information. Your results guide future revision; completing a session does not award automatic mastery.</p>
  </div><div class="complete-row"><button id="completeSession" class="primary" ${attempted<2||drilled<6?"disabled":""}>Complete and lock Session ${s.slot}</button></div>`;
  document.getElementById("completeSession").onclick=async()=>{
    if(sid&&!sessionDraft.evidence['faded:'+sid]){alert('Finish the partly worked problem in Try first.');return}
    if(sid&&!sessionDraft.evidence["retrieval:"+sid]){alert("Attempt the independent basics problem in Try first.");return}
    if((sessionDraft.summary.retrieval_ids||[]).some(id=>!sessionDraft.evidence["retrieval:"+id])){alert("Complete the short revision questions first.");return}
    if(!currentProblems.every(p=>sessionDraft.answers[p.id])){alert("Attempt both original problems before finishing.");return}
    if(!modeKeys.every(key=>sessionDraft.evidence[key])){alert("Finish the six extra practice problems before completing this session.");return}
    if((sessionDraft.summary.mixed_skills||[]).some((id,i)=>!sessionDraft.evidence['mixed:'+i])){alert('Attempt the two mixed-method problems first.');return}
    clearTimeout(autosaveTimer);const btn=document.getElementById("completeSession");btn.disabled=true;btn.textContent="Locking session…";
    try{
      await queueLessonRepairs(user.id,s.slot,sessionDraft,progress.completed_sessions||0);
      sessionDraft.summary={...sessionDraft.summary,focus:s.focus,type:s.type,phase:s.phase,problems:currentProblems.map(x=>x.id)};
      await upsertSession({session_number:s.slot,session_key:`S${String(s.slot).padStart(3,"0")}`,completed_at:new Date().toISOString(),immutable:true,answers:sessionDraft.answers,working:sessionDraft.working,evidence:sessionDraft.evidence,summary:sessionDraft.summary});
      const done=Math.max(progress.completed_sessions||0,s.slot),p=done/372*100,r=Math.max(Number(progress.rank||0),Math.max(0,Math.min(20,Math.floor(done*20/372))));
      progress=await saveProgress({completed_sessions:done,current_session:Math.min(372,done+1),xp:done*100,rank:r,overall_percent:Number(p.toFixed(2)),next_practice_exam_in:(course.find(x=>x.slot>done&&x.type==="MIXED")?.slot??done)-done});
      localStorage.removeItem(draftKey(s));editingSession=null;draftDirty=false;await refreshEvidence();renderHome();
    }catch(e){alert(e.message);btn.disabled=false;btn.textContent=`Complete and lock Session ${s.slot}`}

  };
}
function mixedSkills(s,count){
 const recorded=completedRecords.filter(r=>r.session_number<s.slot).flatMap(r=>[r.summary?.skill_id,...(r.summary?.mixed_skills||[])]);
 // Older records may predate skill tags. Completed path positions still identify
 // the methods already taught; never leave a workshop empty after an upgrade.
 const priorLessons=course.filter(x=>x.type==='LESSON'&&x.slot<s.slot&&x.slot<=(progress.completed_sessions||0)).map(x=>skillFor(x,taxonomy));
 const taught=[...new Set([...recorded,...priorLessons].filter(id=>methods[id]))];
 const candidates=taught.filter(id=>id!==skillFor(s,taxonomy));
 const ids=candidates.length?candidates:taught;
 return Array.from({length:count},(_,i)=>ids[(s.slot*3+i*Math.max(1,Math.floor(ids.length/count)))%ids.length]); // Repeat a taught skill with new numbers if fewer distinct skills are available.
}
function mountMixed(el,s,count){
 const ids=sessionDraft.summary.mixed_skills||(sessionDraft.summary.mixed_skills=mixedSkills(s,count));
 el.innerHTML=`<h3>Which tool fits?</h3><p class="muted">These questions draw on earlier lessons. Choose a method before opening a hint. This is untimed practice with written feedback.</p>${ids.map((id,i)=>`<div data-mixed="${i}"></div>`).join('')}`;
 ids.forEach((id,i)=>mountPractice(el.querySelector(`[data-mixed="${i}"]`),{id,seed:s.slot+i*5,key:'mixed:'+i,draft:sessionDraft,save:()=>saveDraft(s),label:`MIXED QUESTION ${i+1}`}));
}
function renderWorkshop(s){
 app.innerHTML=`<section class="session-page panel stage"><div class="eyebrow">SESSION ${s.slot} · STRATEGY WORKSHOP</div><h1>Mixed problem solving</h1><p>Each question may need a different method. Work out your answer on paper, enter the final result, and study the solution after checking.</p><p class="muted">Six problems plus five quick decisions. No written explanations or reflections required.</p>${wordingHTML(s.slot)}<div id="workshopFlash"></div><div id="workshopQuestions"></div><button id="completeWorkshop" class="primary">Complete and lock workshop</button></section>`;
 const ids=sessionDraft.summary.mixed_skills||(sessionDraft.summary.mixed_skills=mixedSkills(s,6));
 mountFlashCards(app.querySelector('#workshopFlash'),{id:'mixed-'+s.slot,slot:s.slot,deck:mixedFlashDeck(ids,s.slot),draft:sessionDraft,save:()=>saveDraft(s)});
 mountMixed(app.querySelector('#workshopQuestions'),s,6);
 app.querySelector('#completeWorkshop').onclick=async event=>{
  if(!flashReviewed(sessionDraft,'mixed-'+s.slot)){alert('Finish the five quick decisions first.');return}
  if((sessionDraft.summary.mixed_skills||[]).some((id,i)=>!sessionDraft.evidence['mixed:'+i])){alert('Check your answer on each of the six problems first.');return}
  event.target.disabled=true;
  try{sessionDraft.summary.type='MIXED';await completeSpecialSession(s)}
  catch(error){alert(error.message);event.target.disabled=false}
 };
}
async function renderReview(){
 document.body.classList.remove("lesson-fullscreen","home-focus","lesson-video-review");
 activeView="review";await refreshEvidence();
 app.innerHTML=`<section class="panel hero-panel"><div class="eyebrow">YOUR MATHEMATICAL NOTEBOOK</div><h1>Completed sessions</h1><p class="muted">The original answers and working are locked. Use a fresh session to show new learning.</p>${[...completedRecords].reverse().map(r=>`<details class="review-detail" data-review-session="${r.session_number}"><summary>Session ${r.session_number} · ${esc(r.summary?.focus||course[r.session_number-1]?.focus||'')} <span class="type-chip">LOCKED</span></summary>${course[r.session_number-1]?.type==="LESSON"?`<button type="button" class="secondary saved-intro" data-video-session="${r.session_number}">${[1,2].includes(r.session_number)?"Watch introduction video":"Review lesson teaching"}</button>`:""}${r.summary?.takeaway?`<p><b>Key idea:</b> ${esc(r.summary.takeaway)}</p>`:""}${r.summary?.watch?`<p><b>Next time:</b> ${esc(r.summary.watch)}</p>`:""}${r.evidence?.mawa_base?.status?`<p>Mathematical investigation completed in a paper notebook. ${r.evidence.mawa_extension?.status?"Extension completed on paper.":""} Saved rubric scores are available above.</p>`:""}${Object.entries(r.answers||{}).map(([id,a])=>`<article><h3>${esc(problemIndex.find(p=>p.id===id)?.title||id)}</h3><p class="math-copy">${esc(problemIndex.find(p=>p.id===id)?.prompt||'')}</p><p><b>Recorded answer:</b> ${esc(a?.response??a)}</p><p class="math-copy">${esc(r.working?.[id]||'')}</p><button class="ghost saved-solution" data-problem="${esc(id)}" data-session="${r.session_number}">Worked solution</button><div class="saved-solution-content"></div>${r.evidence?.['reasoning:'+id]?`<p><b>Recognition clue:</b> ${esc(r.evidence['reasoning:'+id].clue||'—')}</p><p><b>Plan:</b> ${esc(r.evidence['reasoning:'+id].plan||'—')}</p><p><b>Check or correction:</b> ${esc(r.evidence['reasoning:'+id].check||'—')}</p><p class="muted">${esc(applicationStatus(r.evidence?.['application:'+id]))} · explanation saved for review</p>`:''}</article>`).join('')}${Object.values(r.evidence||{}).filter(e=>e?.kind==='mixed_application').map(e=>`<article><h3>${esc(e.question_id)}</h3>${e.method?`<p><b>Your method:</b> ${esc(e.method)}</p>`:""}<p><b>Recorded answer:</b> ${esc(e.response)} · ${e.correct?'correct':'needs repair'}${e.used_help?' · supported':''}</p></article>`).join('')}${r.working?.mawa_base?`<div data-adult-review="${r.session_number}"></div><h3>Investigation</h3><p class="math-copy">${esc(r.working.mawa_base)}</p><h3>Extension</h3><p class="math-copy">${esc(r.working.mawa_extension||'')}</p>`:''}</details>`).join('')||'<p>No completed sessions yet.</p>'}</section>`;
 app.querySelectorAll('.saved-intro').forEach(button=>button.onclick=()=>openLessonIntroductionFromMenu(Number(button.dataset.videoSession)).catch(error=>alert(error.message)));
 app.querySelectorAll('.saved-solution').forEach(button=>button.onclick=async()=>{button.disabled=true;const target=button.nextElementSibling;try{const {data,error}=await supabase.functions.invoke('get-problem-solution',{body:{problem_id:button.dataset.problem,session_number:Number(button.dataset.session)}});if(error||data?.error)throw error||new Error(data.error);target.className='math-copy';target.textContent=data.solution_text||data.spoken_script||'No written solution returned.'}catch(err){target.textContent=err.message;button.disabled=false}});
 app.querySelectorAll('[data-adult-review]').forEach(target=>{const details=target.closest('details');details.addEventListener('toggle',async()=>{if(!details.open||target.dataset.loaded)return;target.dataset.loaded='1';const record=completedRecords.find(r=>r.session_number===Number(target.dataset.adultReview)),item=mawa.find(x=>x.id===record.summary?.investigation_id)||mawa[(Math.floor(record.session_number/7)-1)%20];try{await mountInvestigationReview(target,{user,record,item})}catch(err){target.textContent=err.message;delete target.dataset.loaded}})});
}

async function exportProgressBackup(){
  const tables=["profiles","progress_state","session_records","problem_attempts","exam_sittings","learning_repairs","investigation_reviews"];
  const out={schema_version:"summit-one-progress-export-v1",exported_at:new Date().toISOString(),user_id:user.id,data:{}};
  for(const table of tables){
    out.data[table]=await allRows(()=>{let q=supabase.from(table).select('*');return table==='profiles'?q.eq('id',user.id).order('id'):q.eq('user_id',user.id).order(table==='progress_state'?'user_id':'id')});
    for(const row of out.data[table])for(const key of Object.keys(row))if(/^star[345]_/.test(key))delete row[key];
  }
  const blob=new Blob([JSON.stringify(out,null,2)],{type:"application/json"});
  const a=document.createElement("a");a.href=URL.createObjectURL(blob);a.download="Summit-One-progress-"+new Date().toISOString().slice(0,10)+".json";document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(a.href),1000);
}
async function renderProfile(){
 document.body.classList.remove("lesson-fullscreen","home-focus","lesson-video-review");
  activeView="profile";await refreshEvidence();updateNavProgress();const r=currentRank();
  const done=progress.completed_sessions||0,currentXp=progress.xp??done*100;
  const nextRankSession=r>=20?null:Math.ceil(372*(r+1)/20);
  const nextRankXp=nextRankSession===null?0:Math.max(0,nextRankSession*100-currentXp);
  const remaining=Math.max(0,372-done);
  const nextPractice=course.find(item=>item.slot>done&&item.type==="MIXED");
  const nextMawa=course.find(item=>item.slot>done&&item.type==="MAWA");
  const milestone=done<152?{target:152,label:"2027 AMC readiness"}:done<176?{target:176,label:"MAWA application readiness"}:done<360?{target:360,label:"2028 AMC readiness"}:{target:372,label:"Rossmoyne capstone"};
  const rankProgress=nextRankSession===null?"All ranks unlocked":nextRankXp+" XP to your next rank";
  const completed=completedRecords,exams=recentExams;
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
  <div class="profile-grid">
    <div class="panel profile-stat"><b>${done} / 372</b><span>sessions completed</span></div>
    <div class="panel profile-stat"><b>${remaining}</b><span>sessions remaining</span></div>
    <div class="panel profile-stat"><b>${overall().toFixed(1)}%</b><span>course completed</span></div>
    <div class="panel profile-stat"><b>${r===0?"Cadet":r}</b><span>${r===0?"starting rank":"current rank"}</span></div>
  </div>
  <p class="muted profile-sync">Cloud progress: <span id="syncStatus">${esc(syncStatusText())}</span> · ${exams.length} completed timed assessments</p>
  <details class="profile-upcoming">
    <summary>Upcoming workshops, investigations and milestones</summary>
    <div class="profile-upcoming-grid">
      <div><span>Next strategy workshop</span><b>${nextPractice?`Session ${nextPractice.slot}`:"Complete"}</b><small>${nextPractice?`${nextPractice.slot-done} sessions away`:"All workshops completed"}</small></div>
      <div><span>Next MAWA investigation</span><b>${nextMawa?`Session ${nextMawa.slot}`:"Complete"}</b><small>${nextMawa?`${nextMawa.slot-done} sessions away`:"All investigations completed"}</small></div>
      <div><span>Current milestone</span><b>${Math.min(done,milestone.target)} / ${milestone.target}</b><small>${esc(milestone.label)}</small></div>
      <div><span>Rank progress</span><b>${r>=20?"All 20 ranks":"Rank "+(r+1)+" next"}</b><small>${rankProgress}</small></div>
    </div>
  </details>
  <h2 style="margin-top:28px">Technique evidence map</h2><p class="muted">A check means the technique has appeared in a completed session. It does <b>not</b> automatically mean independent mastery; timed and transfer evidence remains separate.</p>
  <div class="technique-map">${(taxonomy?.categories||[]).map(cat=>`<article class="tech-category"><div class="eyebrow">${esc(cat.id)}</div><h3>${esc(cat.name)}</h3><div class="tech-list">${cat.subskills.map(sk=>{const n=focusCounts.get(sk.id)||0,recall=recallState(completedRecords,sk.id);return `<div class="tech ${n?"covered":""}"><span>${n?"✓":"○"}</span><div><b>${esc(sk.name)}</b><small>${esc(sk.id)} · ${recall.retained?"retained on delayed checks · ":""}${n?n+" completed-session exposure"+(n===1?"":"s"):"not yet completed"}</small></div></div>`}).join("")}</div></article>`).join("")}</div>
  <h2 style="margin-top:28px">Recent timed assessments</h2><div class="history-list">${(exams||[]).map(e=>`<div class="history-row"><div><b>${esc(e.metadata?.title||e.exam_id)}</b><small>${e.submitted_at?new Date(e.submitted_at).toLocaleDateString():""}</small></div><div class="history-score">${e.score??"—"} / ${e.max_score}</div><div class="history-award">${esc(e.metadata?.award||"")}</div></div>`).join("")||'<div class="empty">No timed assessments completed yet.</div>'}</div><h2 style="margin-top:28px">20 explorer ranks</h2><div class="rank-grid">${rankNames.map((n,i)=>`<div class="rank ${i+1>r?"locked":""}"><span class="rank-emblem" aria-hidden="true">${i+1}</span><div><span class="rnum">RANK ${i+1}</span><b>${esc(n)}</b><small class="muted">${Math.ceil(372*(i+1)/20)} sessions</small></div></div>`).join("")}</div>
  <div class="complete-row"><a class="secondary" href="tests.html">Open AMC Test Centre</a><button id="exportProgress" class="ghost">Export progress backup</button><button id="logout" class="danger">Sign out</button></div>
  <p class="footer-note">Ranks recognise course completion; they do not replace evidence of independent mathematical mastery.</p></section>`;
  document.getElementById("exportProgress").onclick=async()=>{const b=document.getElementById("exportProgress");b.disabled=true;try{await exportProgressBackup()}catch(e){alert(e.message)}finally{b.disabled=false}};
  document.getElementById("logout").onclick=async()=>{await signOut();location.href="login.html"};
}
boot().finally(()=>window.SummitLoader?.ready());

