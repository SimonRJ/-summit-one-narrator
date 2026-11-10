import { supabase, loadProgress, saveProgress, signOut, currentUser, upsertSession, recordAttempt } from "./supabase-client.js";

const app=document.getElementById("app");
const problemTemplate=document.getElementById("problemTemplate");
let course=[], teaching=[], mawa=[], rossMap=[], problemIndex=[], progress=null, user=null, activeView="home", activeStage=0;
let currentProblems=[], currentMawa=null, sessionDraft={answers:{},working:{},evidence:{},summary:{}};

const esc=s=>String(s??"").replace(/[&<>"']/g,m=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[m]));
const pct=n=>Math.max(0,Math.min(100,Number(n)||0));
const hash=s=>{let h=2166136261;for(const c of String(s)){h^=c.charCodeAt(0);h=Math.imul(h,16777619)}return h>>>0};
const normalize=s=>String(s??"").toLowerCase().replace(/\s+/g,"").replace(/[×·]/g,"*").replace(/[²]/g,"^2").replace(/[³]/g,"^3").replace(/[.,;:]$/g,"");
const rankNames=["Pathfinder","Pattern Scout","Model Builder","Logic Ranger","Number Navigator","Geometry Pilot","Counting Specialist","Invariant Hunter","Transfer Thinker","Proof Builder","Problem Solver","Strategy Captain","Olympiad Explorer","Insight Engineer","Reasoning Commander","AMC Specialist","MAWA Specialist","Rossmoyne Specialist","Summit Elite","135 Master"];

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
function currentRank(){return Math.max(1,Math.min(20,Math.ceil(Math.max(0.0001,overall())/5)))}
function problemKeywords(focus){
  return focus.toLowerCase().split(/[^a-z0-9]+/).filter(w=>w.length>4&&!["including","through","under","using","simple","reasoning"].includes(w));
}
function chooseProblems(session){
  const words=problemKeywords(session.focus);
  const scored=problemIndex.map(p=>{
    const hay=(p.title+" "+p.category+" "+p.source_label).toLowerCase();
    let score=words.reduce((n,w)=>n+(hay.includes(w)?4:0),0);
    if(session.phase.includes("AMC")&&p.source_type==="authentic_amc")score+=2;
    if(session.type==="MAWA"&&p.source_type==="original_authored")score+=3;
    return {...p,_score:score,_tie:hash(session.slot+"|"+p.id)};
  }).sort((a,b)=>b._score-a._score||a._tie-b._tie);
  const chosen=[];
  for(const p of scored){if(!chosen.some(x=>x.id===p.id)){chosen.push(p);if(chosen.length===2)break}}
  return chosen;
}
function teachingFor(session){
  const chapter=chapterFor(session.focus);
  const arr=teaching.filter(x=>x.id.startsWith(chapter+"."));
  if(!arr.length)return [];
  const concept=arr.filter(x=>x.type==="concept");
  const pick=concept[(session.slot-1)%Math.max(1,concept.length)];
  const example=arr.find(x=>x.type==="worked_example");
  return [pick,example].filter(Boolean);
}
async function boot(){
  try{
    user=await currentUser();
    if(!user){location.href="login.html";return}
    const [c,t,m,h]=await Promise.all([fetch("data/sessions-372.json").then(r=>r.json()),fetch("data/teaching-72.json").then(r=>r.json()),fetch("data/mawa-investigations-20.json").then(r=>r.json()),fetch("data/rossmoyne-h23.json").then(r=>r.json())]);
    course=c.sessions; teaching=t.items; mawa=m.items; rossMap=h.items;
    const {data:problems,error}=await supabase.from("content_problems").select("id,source_type,title,source_label,category,difficulty,prompt,unit").order("id");
    if(error)throw error; problemIndex=problems||[];
    progress=await loadProgress();
    if(!progress)progress=await saveProgress({current_session:0,completed_sessions:0,xp:0,rank:1,overall_percent:0,state:{}});
    wireNav(); renderHome();
  }catch(e){app.innerHTML='<section class="panel hero-panel"><h1>Unable to load Summit One</h1><p class="muted">'+esc(e.message)+'</p></section>'}
}
function wireNav(){
  document.querySelectorAll("[data-view]").forEach(b=>b.onclick=()=>{document.querySelectorAll(".nav-btn").forEach(x=>x.classList.remove("active"));b.classList.add("active");activeView=b.dataset.view;if(activeView==="home")renderHome();if(activeView==="review")renderReview();if(activeView==="profile")renderProfile()})
}
function renderHome(){
  const s=courseSession(),done=progress.completed_sessions||0,amc=nextSlot("AMC MOCK"),mawa=nextSlot("MAWA");
  app.innerHTML=`
  <section class="dashboard-grid">
    <article class="panel mission-card">
      <div class="session-kicker">SESSION ${s.slot} / 372</div>
      <h1>${esc(s.focus)}</h1>
      <div><span class="type-chip">${esc(s.type)}</span><span class="phase-chip">${esc(s.phase)}</span></div>
      <p class="muted">Remember → Discover → Try → Transfer → Check. Work carefully; there is no calendar streak and no penalty for taking the time you need.</p>
      <button id="continue" class="primary cta">${done>=372?"Course complete":"Continue Session "+s.slot}</button>
      <div class="sync-line"><span class="dot"></span> Cloud progress synced</div>
      <div class="quick-links"><a class="secondary" href="tests.html">AMC Test Centre</a><button id="reviewQuick" class="ghost">Review completed sessions</button></div>
    </article>
    <aside class="side-stack">
      <article class="panel stat-card"><div class="eyebrow">COURSE PROGRESS</div><div class="stat-value">${done} / 372</div><div class="progress-track"><div class="progress-fill" style="width:${overall().toFixed(2)}%"></div></div><div class="stat-label">${overall().toFixed(1)}% complete · Rank ${currentRank()} / 20</div></article>
      <article class="panel stat-card"><div class="eyebrow">NEXT PRACTICE</div><div class="stat-value">${amc??"—"}</div><div class="stat-label">completed session${amc===1?"":"s"} until next AMC-format mock</div></article>
      <article class="panel stat-card"><div class="eyebrow">NEXT MAWA INVESTIGATION</div><div class="stat-value">${mawa??"—"}</div><div class="stat-label">completed session${mawa===1?"":"s"} away</div></article>
    </aside>
  </section>
  <p class="footer-note">The course follows the canonical 372-session Summit One plan: 283 teaching/transfer sessions, 53 MAWA investigations, 25 AMC mock positions and 11 Rossmoyne-style mock positions. Full authentic AMC papers live separately in the Test Centre and never replace the teaching sequence.</p>`;
  document.getElementById("continue").onclick=()=>done<372?startSession(s):renderProfile();
  document.getElementById("reviewQuick").onclick=()=>renderReview();
}
async function startSession(s){
  activeStage=0;currentProblems=chooseProblems(s);currentMawa=s.type==="MAWA"?mawa[(Math.floor(s.slot/7)-1)%mawa.length]:null;sessionDraft={answers:{},working:{},evidence:{},summary:{}};
  const {data:existing}=await supabase.from("session_records").select("*").eq("user_id",user.id).eq("session_number",s.slot).maybeSingle();
  if(existing){sessionDraft={answers:existing.answers||{},working:existing.working||{},evidence:existing.evidence||{},summary:existing.summary||{}}}
  else await upsertSession({session_number:s.slot,session_key:`S${String(s.slot).padStart(3,"0")}`,answers:{},working:{},evidence:{},summary:{}});
  if(s.type==="MAWA"){renderMawaSession(s);return}
  renderSession(s);
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
    <nav class="stage-nav" aria-label="MAWA stages">${["Remember","Discover","Try","Transfer","Check"].map((x,i)=>`<button data-stage="${i}" class="${i===activeStage?"active":""}">${i+1}. ${x}</button>`).join("")}</nav>
    <section id="stage" class="panel stage"></section>
  </section>`;
  document.querySelectorAll("[data-stage]").forEach(b=>b.onclick=()=>{activeStage=Number(b.dataset.stage);renderMawaSession(s)});
  const el=document.getElementById("stage"), item=currentMawa;
  if(activeStage===0){
    const prevSlot=s.slot-7,prev=prevSlot>=7?mawa[(Math.floor(prevSlot/7)-1)%mawa.length]:null;
    el.innerHTML=`<div class="stage-number">STAGE 1 · RETRIEVAL</div><h2>Remember</h2><p class="muted">MAWA-style work rewards systematic thinking and clear justification, not speed alone.</p><div class="teaching-item"><h3>${prev?esc(prev.title):"Proof habit"}</h3><p class="math-copy">${prev?"Without reopening the old solution, write one sentence about what made the previous investigation complete.":"Write the difference between finding an example and proving a maximum, minimum or impossibility."}</p></div><div class="complete-row"><span></span><button id="nextStage" class="primary">Discover</button></div>`;
  }
  if(activeStage===1){
    el.innerHTML=`<div class="stage-number">STAGE 2 · INVESTIGATION SETUP</div><h2>Discover</h2><p class="muted">Read the problem slowly. Decide what evidence would count as a proof before calculating.</p><div class="problem-card"><div class="problem-meta">${esc(item.topic)}</div><h3 class="problem-title">${esc(item.title)}</h3><div class="problem-prompt math-copy">${esc(item.prompt)}</div><details style="margin-top:14px"><summary>First hint — use only if you are genuinely stuck</summary><p class="math-copy">${esc(item.hint)}</p></details></div><div class="complete-row"><span class="muted">Plan cases, a diagram, a table or an invariant.</span><button id="nextStage" class="primary">Try the investigation</button></div>`;
  }
  if(activeStage===2){
    const saved=sessionDraft.working.mawa_base||"";
    el.innerHTML=`<div class="stage-number">STAGE 3 · INDEPENDENT WORK</div><h2>Try</h2><p class="muted">Use paper, a notebook or this box. A correct number without justification is not complete evidence.</p><div class="problem-card"><div class="math-copy">${esc(item.prompt)}</div><label class="answer-label">Your organised reasoning<textarea id="mawaBase" class="answer-box" rows="12">${esc(saved)}</textarea></label><button id="recordMawa" class="primary">Record investigation work</button><div id="mawaMsg" class="attempt-feedback" hidden></div></div><div class="complete-row"><button id="backStage" class="ghost">Back</button><button id="nextStage" class="primary">Transfer</button></div>`;
    document.getElementById("recordMawa").onclick=async()=>{const v=document.getElementById("mawaBase").value.trim();if(v.length<20){alert("Record enough working to show the method, not only an answer.");return}sessionDraft.working.mawa_base=v;sessionDraft.evidence.mawa_base={status:"proof_evidence_unreviewed",recorded_at:new Date().toISOString()};await upsertSession({session_number:s.slot,session_key:`S${String(s.slot).padStart(3,"0")}`,answers:sessionDraft.answers,working:sessionDraft.working,evidence:sessionDraft.evidence,summary:sessionDraft.summary});const m=document.getElementById("mawaMsg");m.hidden=false;m.textContent="Work saved. Proof evidence remains unreviewed until you compare/check it."};
  }
  if(activeStage===3){
    const ext=mawaExtension(s,item),saved=sessionDraft.working.mawa_extension||"";
    el.innerHTML=`<div class="stage-number">STAGE 4 · GENERALISE</div><h2>Transfer</h2><p class="muted">${esc(ext)}</p><label class="answer-label">Extension reasoning<textarea id="mawaExt" class="answer-box" rows="10">${esc(saved)}</textarea></label><button id="recordExt" class="primary">Record extension</button><div class="complete-row"><button id="backStage" class="ghost">Back</button><button id="nextStage" class="primary">Check</button></div>`;
    document.getElementById("recordExt").onclick=async()=>{const v=document.getElementById("mawaExt").value.trim();if(v.length<20){alert("Give a mathematical reason, example, diagram description or proof step.");return}sessionDraft.working.mawa_extension=v;await upsertSession({session_number:s.slot,session_key:`S${String(s.slot).padStart(3,"0")}`,answers:sessionDraft.answers,working:sessionDraft.working,evidence:sessionDraft.evidence,summary:sessionDraft.summary});};
  }
  if(activeStage===4){
    const ready=sessionDraft.working.mawa_base&&sessionDraft.working.mawa_extension;
    el.innerHTML=`<div class="stage-number">STAGE 5 · PROOF CHECK</div><h2>Check</h2><p class="muted">Score the evidence, not confidence. This is a practice rubric, not an official MAWA admissions score.</p><div class="problem-card"><details><summary>Compare with model reasoning</summary><p class="solution-panel" style="display:block">${esc(item.solution)}</p><p class="muted"><b>Common trap:</b> ${esc(item.trap)}</p></details><div class="check-grid"><label class="answer-label">Result 0–3<input id="rResult" type="number" min="0" max="3" value="3"></label><label class="answer-label">Method 0–3<input id="rMethod" type="number" min="0" max="3" value="2"></label><label class="answer-label">Proof / completeness 0–3<input id="rProof" type="number" min="0" max="3" value="2"></label><label class="answer-label">Clarity 0–1<input id="rClarity" type="number" min="0" max="1" value="1"></label></div></div><div class="complete-row"><span class="muted">${ready?"Investigation and extension recorded.":"Record both the investigation and extension before completion."}</span><button id="completeMawa" class="primary" ${ready?"":"disabled"}>Complete and lock Session ${s.slot}</button></div>`;
    if(ready)document.getElementById("completeMawa").onclick=async()=>{const rubric={result:Number(document.getElementById("rResult").value),method:Number(document.getElementById("rMethod").value),proof:Number(document.getElementById("rProof").value),clarity:Number(document.getElementById("rClarity").value)};sessionDraft.summary={focus:item.title,type:"MAWA",phase:s.phase,investigation_id:item.id,rubric,total:rubric.result+rubric.method+rubric.proof+rubric.clarity};await completeSpecialSession(s)};
  }
  const next=document.getElementById("nextStage");if(next)next.onclick=()=>{activeStage=Math.min(4,activeStage+1);renderMawaSession(s)};
  const back=document.getElementById("backStage");if(back)back.onclick=()=>{activeStage=Math.max(0,activeStage-1);renderMawaSession(s)};
}
async function completeSpecialSession(s){
  await upsertSession({session_number:s.slot,session_key:`S${String(s.slot).padStart(3,"0")}`,completed_at:new Date().toISOString(),immutable:true,answers:sessionDraft.answers,working:sessionDraft.working,evidence:sessionDraft.evidence,summary:sessionDraft.summary});
  const done=Math.max(progress.completed_sessions||0,s.slot),p=done/372*100,r=Math.max(1,Math.min(20,Math.ceil(Math.max(.0001,p)/5)));
  progress=await saveProgress({completed_sessions:done,current_session:Math.min(372,done+1),xp:done*100,rank:r,overall_percent:Number(p.toFixed(2)),next_practice_exam_in:(course.find(x=>x.slot>done&&(x.type==="AMC MOCK"||x.type==="ROSSMOYNE MOCK"))?.slot??done)-done});
  renderHome();
}

function renderSession(s){
  app.innerHTML=`
  <section class="session-page">
    <header class="panel session-header"><div class="eyebrow">SESSION ${s.slot} / 372 · ${esc(s.phase)}</div><h1>${esc(s.focus)}</h1><div><span class="type-chip">${esc(s.type)}</span></div></header>
    <nav class="stage-nav" aria-label="Session stages">
      ${["Remember","Discover","Try","Transfer","Check"].map((x,i)=>`<button data-stage="${i}" class="${i===activeStage?"active":""}">${i+1}. ${x}</button>`).join("")}
    </nav>
    <section id="stage" class="panel stage"></section>
  </section>`;
  document.querySelectorAll("[data-stage]").forEach(b=>b.onclick=()=>{activeStage=Number(b.dataset.stage);renderSession(s)});
  const target=document.getElementById("stage");
  if(activeStage===0)renderRemember(target,s);
  if(activeStage===1)renderDiscover(target,s);
  if(activeStage===2)renderChallenge(target,s,currentProblems[0],"try");
  if(activeStage===3)renderChallenge(target,s,currentProblems[1],"transfer");
  if(activeStage===4)renderCheck(target,s);
}
function renderRemember(el,s){
  const prev=course[s.slot-2];
  el.innerHTML=`<div class="stage-number">STAGE 1 · RETRIEVAL</div><h2>Remember</h2><p class="muted">Start without notes. Retrieval is meant to feel effortful.</p>
  <div class="teaching-item"><h3>${prev?esc(prev.focus):"Mathematical habits"}</h3><p class="math-copy">${prev?`In your notebook, write one idea you remember from <b>Session ${prev.slot}</b>. Then make a tiny example that would prove you understand it rather than merely recognise the words.`:"Write three things that make a mathematical answer trustworthy: a clear model, valid operations and a check against the original conditions."}</p></div>
  <div class="complete-row"><span class="muted">When you have written something from memory, continue.</span><button class="primary" id="nextStage">Discover</button></div>`;
  document.getElementById("nextStage").onclick=()=>{activeStage=1;renderSession(s)};
}
function renderDiscover(el,s){
  const items=teachingFor(s);
  el.innerHTML=`<div class="stage-number">STAGE 2 · EXPLANATION</div><h2>Discover</h2><p class="muted">Read, sketch and listen. The goal is to see why the method works, not memorise a slogan.</p>
  <div class="teaching-box">${items.map(t=>`<article class="teaching-item"><div class="eyebrow">${esc(t.type==="worked_example"?"WORKED EXAMPLE":"CONCEPT")}</div><h3>${esc(t.title)}</h3><details><summary>Read explanation</summary><p class="math-copy">${esc(t.transcript)}</p></details><div class="audio-row"><audio controls preload="none" src="${esc(t.audio_url)}"></audio><span class="muted">Narrated explanation</span></div></article>`).join("")||'<p class="muted">Teaching explanation is being selected from the course library.</p>'}</div>
  <div class="complete-row"><span class="muted">Make one note or diagram before moving on.</span><button class="primary" id="nextStage">Try independently</button></div>`;
  document.getElementById("nextStage").onclick=()=>{activeStage=2;renderSession(s)};
}
async function loadProblemDetail(id){
  const {data,error}=await supabase.from("content_problems").select("*").eq("id",id).single();
  if(error)throw error;return data;
}
function renderChallenge(el,s,p,mode){
  if(!p){el.innerHTML='<div class="empty">No challenge available.</div>';return}
  el.innerHTML=`<div class="stage-number">STAGE ${mode==="try"?3:4} · ${mode==="try"?"INDEPENDENT ATTEMPT":"TRANSFER"}</div><h2>${mode==="try"?"Try":"Transfer"}</h2><p class="muted">${mode==="try"?"Solve before opening any explanation.":"Use the idea in a different setting. Decide the strategy yourself."}</p>`;
  const node=problemTemplate.content.firstElementChild.cloneNode(true);
  node.querySelector(".problem-meta").textContent=`${p.source_type==="authentic_amc"?"AMC ARCHIVE":"ORIGINAL CHALLENGE"} · ${p.source_label||""}`;
  node.querySelector(".problem-title").textContent=p.title||p.id;
  node.querySelector(".problem-prompt").textContent=p.prompt;
  const box=node.querySelector(".answer-box"),submit=node.querySelector(".submit-answer"),reveal=node.querySelector(".reveal-solution"),feedback=node.querySelector(".attempt-feedback"),solution=node.querySelector(".solution-panel");
  const saved=sessionDraft.answers[p.id];
  if(saved){box.value=saved.response||"";box.disabled=true;submit.hidden=true;reveal.hidden=false;feedback.hidden=false;feedback.textContent=saved.correct===true?"Recorded as correct independent work.":saved.correct===false?"Attempt recorded. Compare your reasoning, then revisit the method.":"Attempt recorded. This problem needs reasoning rather than a simple exact-answer check."}
  submit.onclick=async()=>{
    const response=box.value.trim();if(!response){feedback.hidden=false;feedback.textContent="Write an answer or reasoning first.";return}
    submit.disabled=true;feedback.hidden=false;feedback.textContent="Recording independent attempt…";
    try{
      const detail=await loadProblemDetail(p.id);
      let correct=null;
      const expected=detail.answer;
      if(typeof expected==="number") correct=Number(response.replace(/[^0-9.+-]/g,""))===expected;
      else if(typeof expected==="string"&&expected.length<40) correct=normalize(response)===normalize(expected);
      await recordAttempt({problem_id:p.id,session_number:s.slot,answer_text:response,is_correct:correct,evidence_level:"independent",solution_video_opened:false,independent_credit:correct===true,elapsed_seconds:null});
      sessionDraft.answers[p.id]={response,correct,attempted_at:new Date().toISOString()};
      await upsertSession({session_number:s.slot,session_key:`S${String(s.slot).padStart(3,"0")}`,answers:sessionDraft.answers,working:sessionDraft.working,evidence:sessionDraft.evidence,summary:sessionDraft.summary});
      box.disabled=true;submit.hidden=true;reveal.hidden=false;feedback.textContent=correct===true?"Correct — and recorded as independent evidence.":correct===false?"Attempt recorded. Now compare methods and find the exact point to improve.":"Attempt recorded. Compare the proof/reasoning rather than relying on exact text matching.";
    }catch(e){feedback.textContent=e.message;submit.disabled=false}
  };
  reveal.onclick=async()=>{
    try{
      const d=await loadProblemDetail(p.id);
      await recordAttempt({problem_id:p.id,session_number:s.slot,answer_text:null,is_correct:null,evidence_level:"viewed",solution_video_opened:true,independent_credit:false,elapsed_seconds:null});
      solution.hidden=false;solution.innerHTML=`<b>Compare reasoning</b>\n\n${esc(d.solution_text||d.spoken_script||"Solution unavailable.")}
      <div class="audio-row"><audio controls preload="none" src="https://github.com/SimonRJ/-summit-one-narrator/releases/download/summit-one-audio-v1/${encodeURIComponent(p.id)}_narration.wav"></audio><span class="muted">Narrated solution when media is available</span></div>`;
      reveal.disabled=true;
    }catch(e){solution.hidden=false;solution.textContent=e.message}
  };
  el.appendChild(node);
  const footer=document.createElement("div");footer.className="complete-row";footer.innerHTML=`<button class="ghost" id="prevStage">Back</button><button class="primary" id="nextStage">${mode==="try"?"Transfer":"Check"}</button>`;el.appendChild(footer);
  footer.querySelector("#prevStage").onclick=()=>{activeStage=mode==="try"?1:2;renderSession(s)};
  footer.querySelector("#nextStage").onclick=()=>{activeStage=mode==="try"?3:4;renderSession(s)};
}
function renderCheck(el,s){
  const attempted=currentProblems.filter(p=>sessionDraft.answers[p?.id]).length;
  el.innerHTML=`<div class="stage-number">STAGE 5 · METACOGNITION</div><h2>Check</h2><p class="muted">Make the learning reusable. A short accurate reflection is better than a long vague one.</p>
  <div class="check-grid"><label class="answer-label">What was the key idea?<textarea id="takeaway" class="answer-box" placeholder="The move that made the problem smaller was…">${esc(sessionDraft.summary.takeaway||"")}</textarea></label>
  <label class="answer-label">What will you watch for next time?<textarea id="watch" class="answer-box" placeholder="A mistake I want to avoid is…">${esc(sessionDraft.summary.watch||"")}</textarea></label></div>
  <div class="complete-row"><span class="muted">${attempted}/2 challenge attempts recorded.</span><button id="completeSession" class="primary" ${attempted<2?"disabled":""}>Complete and lock Session ${s.slot}</button></div>`;
  document.getElementById("completeSession").onclick=async()=>{
    const take=document.getElementById("takeaway").value.trim(),watch=document.getElementById("watch").value.trim();
    if(!take||!watch){alert("Write both short reflections before completing the session.");return}
    const btn=document.getElementById("completeSession");btn.disabled=true;btn.textContent="Locking session…";
    try{
      sessionDraft.summary={takeaway:take,watch,focus:s.focus,type:s.type,phase:s.phase,problems:currentProblems.map(x=>x.id)};
      await upsertSession({session_number:s.slot,session_key:`S${String(s.slot).padStart(3,"0")}`,completed_at:new Date().toISOString(),immutable:true,answers:sessionDraft.answers,working:sessionDraft.working,evidence:sessionDraft.evidence,summary:sessionDraft.summary});
      const done=Math.max(progress.completed_sessions||0,s.slot),p=done/372*100,r=Math.max(1,Math.min(20,Math.ceil(Math.max(.0001,p)/5)));
      progress=await saveProgress({completed_sessions:done,current_session:Math.min(372,done+1),xp:done*100,rank:r,overall_percent:Number(p.toFixed(2)),next_practice_exam_in:(course.find(x=>x.slot>done&&x.type==="AMC MOCK")?.slot??done)-done});
      renderHome();
    }catch(e){alert(e.message);btn.disabled=false;btn.textContent=`Complete and lock Session ${s.slot}`}
  };
}
async function renderReview(){
  activeView="review";app.innerHTML='<section class="panel hero-panel"><div class="eyebrow">ARCHIVE</div><h1>Completed sessions</h1><p class="muted">Finished sessions are preserved as read-only evidence.</p><div id="reviewList" class="review-list"><div class="empty">Loading…</div></div></section>';
  const {data,error}=await supabase.from("session_records").select("session_number,completed_at,summary,answers").eq("user_id",user.id).not("completed_at","is",null).order("session_number",{ascending:false});
  const list=document.getElementById("reviewList");if(error){list.textContent=error.message;return}
  list.innerHTML=(data||[]).map(x=>`<article class="review-item"><div><b>Session ${x.session_number} · ${esc(x.summary?.focus||course[x.session_number-1]?.focus||"")}</b><small>${new Date(x.completed_at).toLocaleDateString()} · ${Object.keys(x.answers||{}).length} recorded attempts</small></div><span class="type-chip">LOCKED</span></article>`).join("")||'<div class="empty">No completed sessions yet.</div>';
}
async function renderProfile(){
  activeView="profile";const r=currentRank();
  app.innerHTML=`<section class="panel hero-panel"><div class="eyebrow">LEARNER PROFILE</div><h1>Summit progress</h1>
  <div class="profile-grid"><div class="panel profile-stat"><b>${(progress.completed_sessions||0)}</b><span>sessions complete</span></div><div class="panel profile-stat"><b>${overall().toFixed(1)}%</b><span>course complete</span></div><div class="panel profile-stat"><b>${r}</b><span>current rank</span></div><div class="panel profile-stat"><b>${progress.xp||0}</b><span>XP</span></div></div>
  <h2 style="margin-top:28px">20 explorer ranks</h2><div class="rank-grid">${rankNames.map((n,i)=>`<div class="rank ${i+1>r?"locked":""}"><span class="rnum">RANK ${i+1}</span><b>${esc(n)}</b><small class="muted">${Math.ceil(372*(i+1)/20)} sessions</small></div>`).join("")}</div>
  <div class="complete-row"><a class="secondary" href="tests.html">Open AMC Test Centre</a><button id="logout" class="danger">Sign out</button></div>
  <p class="footer-note">Ranks recognise course completion; they do not replace evidence of independent mathematical mastery.</p></section>`;
  document.getElementById("logout").onclick=async()=>{await signOut();location.href="login.html"};
}
boot();
