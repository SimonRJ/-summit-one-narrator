import { requireUser } from "./course-engine.js";
const root=document.getElementById("examCentre"),esc=s=>String(s??"").replace(/[&<>"']/g,m=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[m]));
async function render(){
 await requireUser();
 const index=await fetch("./data/exams/index.json",{cache:"no-store"}).then(r=>r.json());
 const papers=index.papers||[];
 root.innerHTML=`
 <div class="card"><div class="eyebrow">Separate assessment section</div><h1 style="font-size:clamp(2rem,5vw,3.6rem);margin:.35em 0">AMC Past Papers</h1>
 <p class="lead">Use this area only when you feel ready for a full sitting. Each paper runs for 60 minutes with 30 questions and a 135-mark score. During the sitting there are no hints, solution videos, technique labels or correctness indicators.</p>
 <div class="grid3" style="margin-top:18px"><div class="kpi"><strong>60</strong><span>minutes</span></div><div class="kpi"><strong>30</strong><span>questions</span></div><div class="kpi"><strong>135</strong><span>maximum marks</span></div></div></div>
 <section class="section"><h2>Available official past-paper rehearsals</h2>
 ${papers.length?papers.map(p=>`<div class="card exam-card" style="margin-bottom:12px"><div><div class="eyebrow">${esc(p.division||"Upper Primary")}</div><h2>${esc(p.title)}</h2><p class="mini">${esc(p.year)} · 60 minutes · 30 questions · Results and award band shown only after submission.</p></div><a class="cta" href="exam.html?paper=${encodeURIComponent(p.id)}">Sit paper →</a></div>`).join(""):`
 <div class="card"><h2>Paper import slot ready</h2><p class="mini">The exam engine is complete and waiting for the first full Upper Primary AMC PDF. Once a paper is imported here, it becomes a separate selectable 60-minute rehearsal without changing the 372-session learning path.</p></div>`}
 </section>
 <section class="section card"><div class="eyebrow">How results work</div><h2>Immediate post-exam report</h2><p class="mini">After submission you see the score out of 135, every question’s answer/correctness/marks, unanswered questions, performance by topic, and an award band. Official WA paper-year cutoffs are used when verifiable; otherwise the app clearly labels the band as a WA practice estimate.</p></section>
 `;
}
render().catch(e=>root.innerHTML=`<div class="card"><h2>Could not load test centre</h2><p class="mini">${esc(e.message)}</p></div>`);
