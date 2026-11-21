import {transferEvidenceHTML} from './original-learning.js?v=geometry-r2-20261114';
import {workedSteps} from './session-intros.js?v=recognition-20261113';
import {methods,exercise,checkAnswer,recallState,dueSkills} from './curriculum.js?v=recognition-20261113';
const esc=s=>String(s??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
export function lessonCard(id,plan){
 const m=methods[id];if(!m||!plan)return '';
 const q=plan.bridge;
 const notation=(q.reason.includes('!')?' The symbol ! means multiply the positive whole numbers down to 1: 3! = 3 × 2 × 1.':'')+(q.reason.includes('^')||q.prompt.includes('^')?' A power counts repeated factors: 2^3 means 2 × 2 × 2.':'')+(q.reason.includes('f(')?' Here f(k) means the number of routes to step k. It is a label for a count.':'')+(q.reason.includes('n²')?' The letter n names a side length; n² means n multiplied by itself.':'');
 return `${workedSteps(plan)}${plan.secondary?workedSteps(plan.secondary,"Second tool · recall before combining"):""}<article class="method-card"><div class="eyebrow">NAME THE IDEA · ${esc(id)}</div><h3>What made that work?</h3><p>${esc(m.idea)}</p><div class="worked-example"><div class="eyebrow">BUILD ON IT · A SECOND WORKED EXAMPLE</div><h3>${esc(q.prompt)}</h3><p><b>First move:</b> ${esc(plan.goal)}</p>${notation?`<p class="notation-note">${esc(notation)}</p>`:''}<p class="math-copy">${esc(q.reason)}</p><p><b>Connect the examples:</b> What stayed the same in the method, even though the numbers or setting changed?</p></div><p class="trap-note"><b>Watch for:</b> ${esc(m.trap)}</p></article>`;
}
export function mountCheck(el,{id,slot,records,draft,save,kind='retrieval',label='',seedOverride=null,onDone=()=>{}}){
 const key=`${kind}:${id}`;
 const old=draft.evidence[key];
 const seed=old?.seed??seedOverride??(kind==='guided'?1:2+((slot+id.charCodeAt(0))%5));
 const q=exercise(id,seed);
 el.innerHTML=`<article class="mini-check"><div class="eyebrow">${esc(label||(kind==='guided'?'YOUR TURN · SUPPORT AVAILABLE':'FROM MEMORY · '+id))}</div><p>${esc(q.prompt)}</p><form><label class="answer-label">${typeof q.value==='number'?'Your final answer':'Your answer'}<input class="answer-box short-answer" autocomplete="off" value="${esc(old?.response||'')}" ${old?'disabled':''}></label><div class="problem-actions"><button class="primary" ${old?'disabled':''}>Check my answer</button><button type="button" class="ghost hint" ${old?'disabled':''}>I need a hint</button></div></form><div class="check-feedback" role="status"></div></article>`;
 let helped=old?.independent===false||draft.evidence['hint:'+key]===true;
 const feedback=el.querySelector('.check-feedback');
 const explain=e=>{feedback.innerHTML=`<p><b>${e.correct?'Correct.':'Not quite yet — let’s repair the method.'}</b> ${e.independent?'First response recorded.':'Recorded with support.'}</p><p>${esc(q.reason)}</p>${!e.correct?'<p>Cover the explanation and solve it again in your notebook. This skill will return in revision.</p>':''}`;};
 if(old)explain(old);
 el.querySelector('.hint').onclick=async()=>{helped=true;draft.evidence['hint:'+key]=true;feedback.textContent=methods[id].idea;try{await save()}catch(err){feedback.textContent+=' Hint use is recorded locally; cloud save failed: '+err.message}};
 el.querySelector('form').onsubmit=async event=>{
  event.preventDefault();const input=el.querySelector('input'),response=input.value.trim();if(!response)return;
  const e={kind,skill_id:id,seed,question_id:q.prompt,expected:String(q.value),response,correct:checkAnswer(q.value,response),independent:kind==='retrieval'&&!helped,recorded_at:new Date().toISOString()};
  const buttons=el.querySelectorAll('button');buttons.forEach(b=>b.disabled=true);draft.evidence[key]=e;
  try{await save();input.disabled=true;explain(e);onDone(e);}catch(err){delete draft.evidence[key];buttons.forEach(b=>b.disabled=false);feedback.textContent='Not saved: '+err.message;}
 };
}
export function mountRetrieval(el,options){
 const {records,slot,currentId,draft}=options;
 const ids=draft.summary.retrieval_ids||(draft.summary.retrieval_ids=dueSkills(records,slot,currentId));
 el.innerHTML=ids.length?`<h3>Bring back an older idea</h3><p class="muted">Two short checks at most. These return after completed sessions, so taking a day off never creates a penalty.</p>${ids.map((id,i)=>`<div id="recall-${i}"></div>`).join('')}`:'<p class="muted">No older checks are due. Sketch what you already know about today’s idea, then continue.</p>';
 ids.forEach((id,i)=>mountCheck(el.querySelector('#recall-'+i),{...options,id}));
}
export function readinessHTML({records,taxonomy,progress,milestones,exams=[]}){
 const done=progress.completed_sessions||0,skills=taxonomy.categories.flatMap(c=>c.subskills),retained=skills.filter(s=>recallState(records,s.id).retained),taught=new Set(records.map(r=>r.summary?.skill_id).filter(Boolean));
 const startDate=milestones?.amc_2027?.start_date || '2027-08-03';
 const weeks=Math.max(0,(Date.parse(startDate+'T00:00:00+08:00')-Date.now())/604800000);
 const remaining=Math.max(0,152-done);
 const availableSlots=Math.floor(weeks*3);
 const projectedSlot=Math.min(372,done+availableSlots);
 const pace=weeks>0?(remaining/weeks).toFixed(1):null;
 const amc=exams.filter(e=>/^amc-up-\d{4}$/.test(e.exam_id) && e.max_score===135 && (e.attempt_number??1)===1);
 const perfect=new Set(amc.filter(e=>e.score===135).map(e=>e.exam_id));
 const practicePlan=weeks>0
  ? `At three study sessions a week, there is time for about ${availableSlots} more before the AMC. If each one completes a course session, that would take you to session ${projectedSlot}. Allow time for practice papers and for lessons that need a second sitting.`
  : 'The scheduled 2027 AMC window has started or passed. Check the organiser’s calendar for your next sitting.';
 const recent=amc.slice(0,3);
 return `<section class="panel roadmap"><div class="eyebrow">THE THREE GOALS</div><h1>Build the evidence, one session at a time</h1><p class="muted">Aim for complete understanding and 135/135. Course progress records effort; independent checks and unfamiliar papers show what is secure.</p>
 <div class="goal-grid"><article><span class="type-chip">AUGUST 2027</span><h2>AMC Upper Primary</h2><p><b>3–5 August 2027</b> · 30 questions · 60 minutes · 135 marks.</p><p>Build accuracy across Q1–25 as well as the insight needed for Q26–30. Practise skipping a stuck question, returning to it, and checking the requested quantity.</p><a href="https://amt.edu.au/competitions" target="_blank" rel="noopener">AMT dates and entry information ↗</a></article>
 <article><span class="type-chip">2027 APPLICATION GOAL</span><h2>MAWA Problem Solving Program</h2><p>Prepare for the 2028 program by writing investigations. MAWA published application problems for its 2027 intake. Check the instructions for your own intake.</p><p>Show organised cases, a reason for every step, and why the conclusion covers every possibility. Every seventh completed session is an investigation.</p><a href="https://mawainc.org.au/mawapsp/" target="_blank" rel="noopener">MAWA application requirements ↗</a></article>
 <article><span class="type-chip">2028 PREPARATION GOAL</span><h2>Rossmoyne Honours Mathematics</h2><p>Rossmoyne assesses Year 6 applicants for its Year 7 Specialist Mathematics Program. Use the school’s notice for the application and test dates that match your intake.</p><p>Practise unfamiliar problems, precise explanations and discussing a solution aloud. The school’s own sample test is the best format check.</p><a href="https://www.rossmoyne.wa.edu.au/enrolment/specialist-programs/specialist-mathematics-program/" target="_blank" rel="noopener">School requirements and sample test ↗</a></article></div>
 <h2>Your study plan before the AMC</h2><p>By session 104 you will have met all 52 techniques. Sessions 105–152 use them again in harder and mixed problems. Later sessions extend the course through the MAWA and Rossmoyne goals.</p><p>${practicePlan}</p><div class="profile-grid"><div class="panel profile-stat"><b>${remaining}</b><span>sessions to the first AMC milestone</span></div><div class="panel profile-stat"><b>${pace??'—'}</b><span>average sessions/week needed by 3 August</span></div><div class="panel profile-stat"><b>${retained.length} / 52</b><span>techniques retained on delayed checks</span></div><div class="panel profile-stat"><b>${perfect.size}</b><span>different authentic AMC papers with a perfect first sitting</span></div></div><p class="muted">A technique counts as retained after correct, unassisted answers on changed examples at least four completed sessions apart. Use that evidence to decide which methods to practise next.</p>
 ${transferEvidenceHTML(records)}<h2>What to work on next</h2><div class="readiness-list">${skills.filter(s=>taught.has(s.id)&&!recallState(records,s.id).retained).slice(0,6).map(s=>`<p><b>${esc(s.name)}</b><br><span class="muted">${recallState(records,s.id).last?.correct===false?'Rebuild the method, then try a fresh example.':'Needs successful delayed recall.'}</span></p>`).join('')||(taught.size?'<p>Your introduced techniques have evidence of delayed recall. Try using them on an unfamiliar problem.</p>':'<p>Complete the opening lessons to start building a personal revision queue.</p>')}</div>
 <p>For a 20-minute speed check, choose an unopened <a href="tests.html?section=speed">Part A set</a>. For a 40-minute challenge, try <a href="tests.html?section=depth">Part B</a>. Save a full paper for a separate 60-minute sitting.</p><p><a class="secondary" href="coverage.html">Explore the 570-question coverage map</a></p><h2>Parent check-in · about ten minutes each week</h2><ol><li>Ask the learner to explain one solution without reading it. Ask “why does that step work?” and “how do you know you found all cases?”</li><li>Choose one mistake to repair. Classify it as reading, modelling, method, calculation or checking. Solve a changed example later.</li><li>Look for success on unfamiliar problems, including the easier questions. Repeated high marks on a remembered paper are useful practice but weaker readiness evidence.</li><li>Keep a fresh recent paper for a supervised 60-minute rehearsal nearer the AMC. Aim for three different perfect papers, with complete reasoning, as a long-term practice goal.</li></ol>
 <p class="muted">${recent.length?'Recent AMC papers: '+recent.map(e=>`${esc(e.metadata?.title||e.exam_id)} ${e.score}/135`).join(' · '):'No completed AMC papers in recent history yet.'}</p><p class="footer-note">Use the organisers’ linked pages for dates and entry arrangements for your intake.</p></section>`;
}
