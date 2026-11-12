import {journeys,investigationOpeners} from './lesson-journeys.js?v=centres-20261112';
import {skillFor,methods,exercise,capstoneSkills} from './curriculum.js?v=centres-20261112';
const esc=s=>String(s??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
export function lessonPlan(s,course,taxonomy){
 const id=skillFor(s,taxonomy),j=journeys[id];
 if(!j)throw Error('Missing lesson introduction: '+s.slot+' '+s.focus);
 const visit=course.filter(x=>x.slot<=s.slot&&x.type==='LESSON'&&skillFor(x,taxonomy)===id).length;
 const missions=[
  ['Meet the idea','Explain each step of a small example, then use the method with support.'],
  ['Make it your own','Recall the method, solve a changed example, and explain why its key step works.'],
  ['Spot the disguise','Identify the useful structure when the story looks different; explain the clue you used.'],
  ['Choose and justify','Compare your method with another approach and explain why this one fits.'],
  ['Test the limits','Change a condition, predict what changes, and find when the method needs adjusting.']
 ];
 const mission=missions[Math.min(visit-1,4)];
 const secondary=capstoneSkills[s.slot]?.[1];
 return {...j,visit,mission:secondary?'Combine two tools':mission[0],target:secondary?'Explain which part of a problem each tool can handle, and justify the connection between them.':mission[1],secondary:secondary?journeys[secondary]:null,bridge:exercise(id,(visit-1)%7)};
}
export function workedSteps(j,label='Start small · watch the thinking'){
 return `<article class="worked-example gentle-example"><div class="eyebrow">${esc(label)}</div><h3>${esc(j.starter)}</h3><ol class="reasoning-steps">${j.steps.map(x=>`<li>${esc(x)}</li>`).join('')}</ol><p class="muted">Pause: explain why the final step follows. You can use counters, a sketch or your own words.</p></article>`;
}
export function introductionHTML(s,course,taxonomy){
 const p=lessonPlan(s,course,taxonomy);
 return `<section class="session-intro" aria-label="Session introduction"><div class="eyebrow">BEFORE WE BEGIN · ${esc(p.mission)}</div><h2>${esc(p.hook)}</h2><p class="intro-goal">Today you will learn to <strong>${esc(p.goal.charAt(0).toLowerCase()+p.goal.slice(1))}</strong></p><div class="intro-grid"><div><h3>Why and when this helps</h3><p>${esc(p.when)}</p></div><div><h3>Start with what you know</h3><p>${esc(p.prerequisite)}</p></div></div>${p.secondary?`<p><b>Your second tool:</b> ${esc(p.secondary.goal)} ${esc(p.secondary.when)}</p>`:''}<p><b>Your mission${p.visit>1?' · return '+p.visit:''}:</b> ${esc(p.target)}</p><p class="muted">First see a tiny example explained → work through a second example → five quick A/B decisions → try with a hint available → solve independently → tackle a transfer challenge. About 30–60 minutes; take a break when you need one.</p><div class="success-note"><b>Success today:</b> You can name the clue, choose a method, explain the important step and check your answer. A difficult question is a place to investigate, not a signal to rush.</div></section>`;
}
export function investigationIntroHTML(s,item){
 const j=investigationOpeners[item.id];if(!j)throw Error('Missing investigation opener '+item.id);
 const visit=1+Math.floor((Math.floor(s.slot/7)-1)/20);
 return `<section class="session-intro" aria-label="Investigation introduction"><div class="eyebrow">BEFORE WE BEGIN · MATHEMATICAL DETECTIVE</div><h2>${esc(j.hook)}</h2><p class="intro-goal">Your task: <strong>${esc(j.goal)}</strong></p><div class="intro-grid"><div><h3>Why this matters</h3><p>Investigations ask not only “what is the answer?” but “how do you know?”. Today’s focus is ${esc(item.topic.toLowerCase())}. You will turn small examples into organised evidence.</p></div><div><h3>Tools you already have</h3><p>${esc(journeys[j.skill].prerequisite)} You can draw, list cases and check a smaller version before using symbols.</p></div></div><p><b>Today’s route:</b> A small worked investigation → five quick decisions → the main question → your reasoning → a changed case → a proof check. Allow 30–60 minutes, or split the investigation across sittings.</p><p><b>Success today:</b> ${visit===1?'Find an answer and explain why your cases cover all possibilities.':visit===2?'Change a condition and explain which parts of your old reasoning still work.':'State a general claim, test a boundary case and justify when the claim holds.'}</p></section>`;
}
export function investigationWarmupHTML(item){return workedSteps(investigationOpeners[item.id],'A smaller investigation · learn the first move');}
export function mockIntroductionHTML(exam){
 const amc=exam.max_score===135;
 return `<section class="session-intro" aria-label="Rehearsal introduction"><h2>Today, practise choosing your own tools</h2><p>You have learnt methods one at a time. This rehearsal practises deciding which method fits when nobody names it for you.</p><div class="intro-grid"><div><h3>What you are learning</h3><p>${amc?'Read accurately, secure approachable marks, and leave time for the multi-step problems.':'Turn unfamiliar wording into a diagram, organised list or equation, and check each conclusion.'}</p></div><div><h3>When it helps</h3><p>In a mixed test, recognising a useful idea and managing time matter alongside calculating. This is practice evidence, not a prediction of an admission outcome.</p></div></div><ol><li>Before starting: prepare paper and pencil, clear distractions and close notes.</li><li>During the paper: try approachable questions first; move on when stuck and return with fresh eyes. Save each numeric answer.</li><li>Afterwards: choose one error, explain its cause, and solve a changed example in a later session.</li></ol><p><b>Success today:</b> An honest independent attempt and a clear next learning step. The timer has not started yet.</p></section>`;
}
