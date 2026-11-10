import { loadCourse,getProfile,requireUser,challengePair,teachingSet,answerMatches,recordAttempt,finishSession } from "./course-engine.js";
import { renderNarratedLesson } from "./media-player.js";

const root=document.getElementById("sessionApp"),esc=s=>String(s??"").replace(/[&<>"']/g,m=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[m]));
const qs=new URLSearchParams(location.search);const requested=Number(qs.get("session")||0);
let state={tryAttempted:false,transferAttempted:false,tryCorrect:false,transferCorrect:false,remember:"",takeaway:""};

function solutionMedia(p){
 return {...p,spoken_script:p.spoken_script||[p.prompt,...(p.solution_steps||[])].join("\n\n"),transcript:p.spoken_script||[p.prompt,...(p.solution_steps||[])].join("\n\n")};
}
function challengeBlock(id,label,p){
 const hints=(p.hints||[]).map(h=>`<li>${esc(h)}</li>`).join("");
 return `<div class="stage" id="${id}Stage"><h3><span class="stage-index">${label}</span>${esc(p.title)}</h3>
 <div class="prompt">${esc(p.prompt)}</div>
 <textarea id="${id}Working" placeholder="Write your reasoning here. A calculation without an explanation is not the whole solution."></textarea>
 <input class="input" id="${id}Answer" placeholder="Your final answer">
 <div class="btnrow"><button class="primary" id="${id}Check">Check answer</button>${hints?`<button id="${id}Hint">Hint</button>`:""}<button id="${id}Solution" disabled>Watch solution</button></div>
 <div id="${id}Feedback" class="mini" style="margin-top:10px"></div>
 ${hints?`<div id="${id}Hints" class="mini" hidden><ul>${hints}</ul></div>`:""}
 <div id="${id}Media" style="margin-top:14px" hidden></div></div>`;
}
async function bindChallenge(id,p,slot){
 const check=document.getElementById(id+"Check"),answer=document.getElementById(id+"Answer"),working=document.getElementById(id+"Working"),feedback=document.getElementById(id+"Feedback"),solution=document.getElementById(id+"Solution"),media=document.getElementById(id+"Media");
 document.getElementById(id+"Hint")?.addEventListener("click",()=>{document.getElementById(id+"Hints").hidden=false});
 check.onclick=async()=>{
  check.disabled=true;
  const correct=answerMatches(answer.value,p.answer);
  state[id+"Attempted"]=true;state[id+"Correct"]=correct;
  feedback.innerHTML=correct?`<span class="correct"><b>Correct.</b> Now make sure your reasoning explains why.</span>`:`<span class="wrong"><b>Not yet.</b> Re-read the exact question and check each condition. You can revise before opening the solution.</span>`;
  solution.disabled=false;
  try{await recordAttempt(p,slot,answer.value,correct,false,"independent")}catch(e){feedback.innerHTML+=` <span class="mini">Sync retry will occur later.</span>`}
  check.disabled=false;
 };
 solution.onclick=async()=>{
  if(!state[id+"Attempted"])return;
  media.hidden=false;renderNarratedLesson(media,solutionMedia(p),{label:"Solution explanation"});
  solution.disabled=true;
  try{await recordAttempt(p,slot,answer.value,state[id+"Correct"],true,"guided")}catch{}
  media.scrollIntoView({behavior:"smooth",block:"start"});
 };
 return {answer,working};
}
async function render(){
 await requireUser();
 const [course,pack]=await Promise.all([loadCourse(),getProfile()]);
 const slot=requested||Math.min(372,(pack.progress.completed_sessions||0)+1);
 const session=course.sessions[slot-1];if(!session)throw new Error("Unknown session");
 if(session.type==="AMC MOCK"){
   root.innerHTML=`<div class="card"><div class="eyebrow">Session ${slot} · AMC mock</div><h1>${esc(session.focus)}</h1><p class="lead">This is a formal 60-minute, 30-question, 135-mark training mock. Teaching aids are disabled during the sitting.</p><a class="cta" href="exam.html?practiceSession=${slot}&mode=amc">Begin mock →</a></div>`;return;
 }
 if(session.type==="ROSSMOYNE MOCK"){
   root.innerHTML=`<div class="card"><div class="eyebrow">Session ${slot} · Rossmoyne-style mock</div><h1>${esc(session.focus)}</h1><p class="lead">Independent school-style reasoning practice. Results are stored separately from lesson progress.</p><a class="cta" href="exam.html?practiceSession=${slot}&mode=ross">Begin practice paper →</a></div>`;return;
 }
 const [tryP,transferP]=challengePair(course,session),teach=teachingSet(course,session),isMawa=session.type==="MAWA";
 root.innerHTML=`
 <div class="card"><div class="eyebrow">${esc(session.phase)} · ${esc(session.type)} · Session ${slot}/372</div><h1 style="font-size:clamp(2rem,5vw,3.6rem);margin:.35em 0">${esc(session.focus)}</h1><p class="lead">${isMawa?"Investigation day: make a conjecture, test it, prove what you can, and explain the argument so another mathematician could follow it.":"Complete the five stages in order. The solution explanations stay locked until you make a genuine attempt."}</p></div>
 <div class="stage-list section">
  <div class="stage"><h3><span class="stage-index">1 · Remember</span>Retrieve before you re-learn</h3><p class="prompt">${isMawa?"Without notes, write two proof moves you could use when a pattern seems true.":"Without notes, write what you already know about: "+esc(session.focus)+". Include one fact, one representation, and one possible trap."}</p><textarea id="remember" placeholder="Your retrieval notes"></textarea></div>
  <div class="stage"><h3><span class="stage-index">2 · Discover</span>${esc(teach.concept?.title||teach.chapter)}</h3><p class="mini">Read, watch and pause. The goal is to understand the structure, not memorise a trick.</p><div id="discoverMedia"></div></div>
  ${challengeBlock("try","3 · Try",tryP)}
  ${challengeBlock("transfer","4 · Transfer",transferP)}
  <div class="stage"><h3><span class="stage-index">5 · Check</span>Make the learning explicit</h3><p class="prompt">In one or two sentences: what clue should make you recognise this idea next time, and what mistake will you avoid?</p><textarea id="takeaway" placeholder="My recognition clue and check…"></textarea><div class="btnrow"><button class="primary" id="completeSession">Complete and lock Session ${slot}</button></div><div id="completeMsg" class="mini" style="margin-top:10px"></div></div>
 </div>`;
 renderNarratedLesson(document.getElementById("discoverMedia"),teach.concept,{label:"Concept explanation"});
 const tryBind=await bindChallenge("try",tryP,slot),transferBind=await bindChallenge("transfer",transferP,slot);
 document.getElementById("completeSession").onclick=async e=>{
  const btn=e.currentTarget,msg=document.getElementById("completeMsg");
  state.remember=document.getElementById("remember").value.trim();state.takeaway=document.getElementById("takeaway").value.trim();
  if(!state.tryAttempted||!state.transferAttempted){msg.textContent="Make an attempt on both Try and Transfer before completing the session.";return}
  if(!state.takeaway){msg.textContent="Add your final recognition clue before completing.";return}
  btn.disabled=true;msg.textContent="Sealing and syncing your session…";
  try{
   const payload={answers:{try:{problem_id:tryP.id,answer:tryBind.answer.value,correct:state.tryCorrect},transfer:{problem_id:transferP.id,answer:transferBind.answer.value,correct:state.transferCorrect}},
    working:{remember:state.remember,try:tryBind.working.value,transfer:transferBind.working.value,takeaway:state.takeaway},
    evidence:{try:state.tryCorrect?"independent":"attempted",transfer:state.transferCorrect?"independent":"attempted"},
    summary:{focus:session.focus,type:session.type,phase:session.phase}};
   await finishSession(slot,`session-${slot}`,payload);
   msg.innerHTML=`<span class="correct"><b>Session ${slot} complete.</b> Your record is now read-only and synced.</span>`;
   setTimeout(()=>location.replace("./"),700);
  }catch(err){msg.textContent="Could not seal the session: "+err.message;btn.disabled=false}
 };
}
render().catch(e=>root.innerHTML=`<div class="card"><h2>Session could not load</h2><p class="mini">${esc(e.message)}</p><a class="cta" href="./">Return to mission</a></div>`);
