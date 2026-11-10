import { supabase } from "./supabase-client.js";
import { requireUser,loadCourse,getProfile,sessionNumber,rankForCompleted,RANK_NAMES,nextSlot,countBefore,tagClass } from "./course-engine.js";

const app=document.getElementById("app");
const esc=s=>String(s??"").replace(/[&<>"']/g,m=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[m]));
function node(s,current,completed){
 const cls=s.slot===current?"current":s.slot<=completed?"done":"";
 const type=s.type==="LESSON"?"Lesson":s.type.replace(" MOCK"," mock");
 return `<div class="path-node ${cls}"><div class="num">Session ${s.slot}</div><div class="tag ${tagClass(s.type)}">${esc(type)}</div><div style="margin-top:8px;font-weight:750">${esc(s.focus)}</div></div>`;
}
async function render(){
 await requireUser();
 const [course,profilePack]=await Promise.all([loadCourse(),getProfile()]);
 const {profile,progress}=profilePack;
 const completed=progress.completed_sessions||0,current=sessionNumber(progress);
 const s=course.sessions[current-1],pct=Math.min(100,completed/372*100),rank=rankForCompleted(completed);
 const nextAMC=nextSlot(course.sessions,current,["AMC MOCK"]),nextMAWA=nextSlot(course.sessions,current,["MAWA"]);
 const nextPractice=nextSlot(course.sessions,current,["AMC MOCK","ROSSMOYNE MOCK"]);
 const nearby=course.sessions.slice(Math.max(0,current-2),Math.min(372,current+5));
 const completedBeforeAMC=countBefore(nextAMC,current),completedBeforeMAWA=countBefore(nextMAWA,current);
 app.innerHTML=`
 <section class="hero">
  <div class="card">
   <div class="eyebrow">${esc(s.phase)} · Session ${current} of 372</div>
   <h2 class="mission-title">${esc(s.focus)}</h2>
   <p class="lead">${s.type==="LESSON"?"Remember → Discover → Try → Transfer → Check. One focused session, then your progress is sealed and synced.":s.type==="MAWA"?"Today is a deep proof-and-investigation session. Explain why, test cases, generalise, and communicate the reasoning clearly.":s.type==="AMC MOCK"?"A formal AMC-format practice slot: 30 questions, 60 minutes, 135 marks.":"A Rossmoyne-style independent practice assessment."}</p>
   <a class="cta" href="session.html?session=${current}">${s.type==="LESSON"?"Continue Session":s.type==="MAWA"?"Begin Investigation":"Open Practice Assessment"} ${current} →</a>
  </div>
  <aside class="card">
   <div class="eyebrow">Synced progress</div>
   <div style="font-size:2rem;font-weight:950;margin:10px 0">${pct.toFixed(1)}%</div>
   <div class="progress"><span style="width:${pct}%"></span></div>
   <p class="mini">${completed} completed · archived and locked</p>
   <div class="kpis">
    <div class="kpi"><strong>${RANK_NAMES[rank-1]}</strong><span>Rank ${rank}/20</span></div>
    <div class="kpi"><strong>${progress.xp||0}</strong><span>XP</span></div>
    <div class="kpi"><strong>${completedBeforeAMC??"—"}</strong><span>sessions before next AMC mock</span></div>
    <div class="kpi"><strong>${completedBeforeMAWA??"—"}</strong><span>sessions before next MAWA investigation</span></div>
   </div>
  </aside>
 </section>
 <section class="grid3">
  <a class="card" href="exams.html" style="text-decoration:none"><div class="eyebrow">Separate test centre</div><h2>AMC Past Papers</h2><p class="mini">Sit a complete 60-minute paper when you decide you are ready. Results and award estimate appear immediately after submission.</p></a>
  <a class="card" href="review.html" style="text-decoration:none"><div class="eyebrow">Evidence</div><h2>Review completed sessions</h2><p class="mini">Your completed answers and reasoning remain read-only. Solution watching never becomes independent credit.</p></a>
  <a class="card" href="profile.html" style="text-decoration:none"><div class="eyebrow">Explorer profile</div><h2>${esc(profile?.display_name||profile?.learner_name||"Learner")}</h2><p class="mini">20 ranks · ${progress.star3_correct||0} three-star · ${progress.star4_correct||0} four-star · ${progress.star5_correct||0} five-star correct.</p></a>
 </section>
 <section class="section"><h2>Your path</h2><div class="path-row">${nearby.map(x=>node(x,current,completed)).join("")}</div></section>
 <section class="section card"><div class="exam-card"><div><div class="eyebrow">Next formal checkpoint</div><h2 style="margin:7px 0 4px">${nextPractice?"Session "+nextPractice:"All scheduled checkpoints completed"}</h2><p class="mini">Practice exams are part of the training path, while the AMC Past Papers section remains available separately for full official-paper rehearsals whenever you choose.</p></div><a class="ghost" href="exams.html">Open test centre</a></div></section>
 `;
}
document.getElementById("signOut").onclick=async()=>{await supabase.auth.signOut();location.replace("login.html")};
render().catch(e=>app.innerHTML=`<div class="card"><h2>Could not load Summit One</h2><p class="mini">${esc(e.message)}</p><a class="cta" href="login.html">Return to login</a></div>`);
