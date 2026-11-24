import {enableFigureViewing} from './figure-viewer.js?v=deeper-20261121';
import {exampleMethods} from './example-methods.js?v=course-review-20261122-a';
import {mountLessonModel} from './lesson-models.js?v=powers-20261122';
// The published lesson text and hints are public. Answers and worked solutions are
// versioned in content_problems and are requested only through the signed-in learner.
export const edition='read-watch-practise-1';
const escape=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
// Only public lesson numbers are kept on this device for the offline reading list.
export function readingAvailable(slot) {
 if(slot === 1)return true;
 try { return localStorage.getItem('summit-one-reading:'+slot) === '1'; } catch { return false; }
}
function rememberReading(slot) {
 try {
  localStorage.setItem('summit-one-reading:'+slot, '1');
  localStorage.setItem('summit-one-reading:last', String(slot));
 } catch { /* The signed-in lesson remains usable with storage disabled. */ }
}
export function readCard(lesson) {
 const { example } = lesson;
 const group = 'rwl-example-' + escape(lesson.slot);
 const figure = example.figure
  ? `<img class="rwl-opening-figure" src="${escape(example.figure.src)}" alt="${escape(example.figure.alt)}">`
  : '';
 const alternative = exampleMethods.get(example.prompt);
 const secondMethod = alternative ? `<details class="rwl-second-method">
  <summary>Another way — ${escape(alternative.method)}</summary>
  <p class="math-copy">${escape(alternative.working)}</p>
  <p class="math-copy">${escape(alternative.comparison)}</p>
 </details>` : '';
 const steps = example.steps.map(step => `<li class="math-copy">${escape(step)}</li>`).join('');
 return `<article class="rwl-copy">
  <div class="eyebrow">THE IDEA</div>
  <h2>${escape(lesson.headline)}</h2>
  <p class="math-copy">${escape(lesson.intro)}</p>
  <section class="rwl-example">
   <h3>A small example</h3>
   <p class="math-copy">${escape(example.prompt)}</p>
   ${figure}
   ${example.prediction ? `<p class="rwl-predict math-copy">${escape(example.prediction)}</p>` : ''}
   <details name="${group}" class="rwl-first-step">
    <summary>Show the first step</summary>
    <p class="math-copy">${escape(example.steps[0])}</p>
   </details>
   <details name="${group}" class="rwl-full-example">
    <summary>Show all steps</summary>
    <ol>${steps}</ol>
    ${secondMethod}
   </details>
  </section>
  <div data-lesson-model></div>
  <p class="rwl-bridge math-copy"><b>As you watch:</b> ${escape(lesson.bridge)}</p>
 </article>`;
}
export function questionOrder(l,bank,manifest){
 const legacy=id=>{const p=bank.find(x=>x.id===id),m=manifest.find(x=>x.id===id);if(!p||!m||m.session!==l.slot||p.source_type!=='original_authored')throw Error('The lesson challenges did not load. Reopen the lesson to try again.');return {...p,learning:m,hint:null}};
 const [a,b,c,d]=l.questions;
 return [a,b,...l.retained.filter(id=>id.endsWith('T')).map(legacy),c,...l.retained.filter(id=>id.endsWith('X')).map(legacy),d];
}
function feedbackFamily(lesson, question) {
 return question.learning?.family || question.family || lesson.skill + ':' + question.id;
}
function evidenceFor(lesson, question, last, answer, usedHelp, familiar) {
 return {kind:'application', role:last?'transfer':question.learning?.role||'practice',
  skill_id:lesson.skill, family:feedbackFamily(lesson, question), problem_id:question.id,
  correct:answer.correct, used_help:usedHelp, familiar_family:familiar, recorded_at:answer.attempted_at};
}
function recordedResult(answer, evidence) {
 if (answer?.correct === true) return evidence?.used_help ? 'Correct with support' : 'Correct';
 return answer?.correct === false ? 'Try again on paper' : 'Recorded';
}
function offerNextStep(container, question, lesson, sawHint) {
 const cue = !sawHint && question.hint ? question.hint : lesson.recap;
 if (!cue) return;
 container.querySelector('p').textContent = cue;
 container.hidden = false;
}
// The server may have recorded an answer just before a network interruption.
// Reuse that first attempt instead of making the student submit the same question again.
export function restoreGradedAnswers(lesson, questions, draft, history, wasSeen) {
 const byId=new Map(questions.map(q=>[q.id,q]));
 for(const row of history) {
  const q=byId.get(row.problem_id);
  if(!q || row.session_number!==lesson.slot || draft.answers[q.id] || !String(row.answer_text??'').trim())continue;
  const a={response:row.answer_text, correct:row.is_correct, independent_credit:row.independent_credit===true, attempted_at:row.created_at};
  draft.answers[q.id]=a;
  const family=feedbackFamily(lesson,q);
  draft.evidence['application:'+q.id]??=evidenceFor(lesson,q,q.id===questions.at(-1).id,a,row.evidence_level==='guided',wasSeen(family)||(!a.independent_credit&&a.correct===true&&row.evidence_level==='independent'));
 }
}
export function phaseFor(page){return page===0?'Read':page===1?'Watch':'Practise'}
export function renderReviewedLesson({app,s,l,questions,draft,locked=false,video,filmGuide,companionGuide,extension,recordWatch,figure,attempt,getSolution,showSolution,save,markLocal,complete,home,wasSeen,trackChange=fn=>fn(),changedSize}){
 rememberReading(l.slot);
 const savedPage=Number(draft.summary.read_practice_page);
 const first=Number.isInteger(savedPage)?savedPage:0;
 let page=Math.max(0,Math.min(questions.length+2,first)),busy=false;
 app.innerHTML=`<section class="session-page lesson-screen-page rwl" aria-label="Session ${s.slot}"><header class="panel lesson-screen-header"><div class="eyebrow">LEARNING SESSION ${s.slot}</div><h1>${escape(s.focus)}</h1></header><div class="lesson-stage-track rwl-track" aria-label="Lesson order"></div><section id="stage" class="panel stage lesson-screen-stage" aria-live="off"></section><footer class="lesson-screen-footer"><button type="button" class="ghost" data-screen-back>Back</button><div class="lesson-screen-progress"><strong data-screen-name></strong><span data-screen-count></span></div><button type="button" class="primary" data-screen-next>Next</button></footer></section>`;
 const stage=app.querySelector('#stage'),track=app.querySelector('.rwl-track'),next=app.querySelector('[data-screen-next]'),back=app.querySelector('[data-screen-back]');let generation=0;
 function locate(){draft.summary.read_practice_page=page;markLocal()}
 function syncNav(){const q=questions[page-2];next.disabled=busy||(q?!draft.answers[q.id]:page===questions.length+2&&!questions.every(x=>draft.answers[x.id]));back.disabled=busy}
 function show(){
  generation++;const phase=phaseFor(page);track.innerHTML=['Read','Watch','Practise'].map((p,i)=>`<span class="${p===phase?'here':i<['Read','Watch','Practise'].indexOf(phase)?'visited':''}" ${p===phase?'aria-current="step"':''}>${i+1}. ${p}</span>`).join('');
  app.querySelector('[data-screen-name]').textContent=page===0?'Meet the idea':page===1?'Lesson video':page<=questions.length+1?`Problem ${page-1} of ${questions.length}`:'Take it with you';
  app.querySelector('[data-screen-count]').textContent=`${page+1} / ${questions.length+3}`;back.textContent=page===0?(locked?'Saved lesson':'Home'):'Back';next.textContent=page===0?'Watch video':page===1?'Start practice':page===questions.length+2?(locked?'Saved lesson':'Finish lesson'):page===questions.length+1?'Recap':'Next';
  if(page===0) {
   stage.innerHTML=(locked?'<p class="rwl-review-note" role="note">Revision practice. Your original answers, score and completion stay locked.</p>':'')+readCard(l);
   enableFigureViewing(stage);
   mountLessonModel(stage.querySelector('[data-lesson-model]'), l);
  }
  else if(page===1){stage.innerHTML=`<article class="opening-film rwl-film"><div class="eyebrow">WATCH THE IDEA IN ACTION</div><h2>${escape(l.videoTitle||s.focus)}</h2>${l.filmUse==="technique"?`<p class="muted">Technique film from lesson ${escape(l.videoId)}.</p>`:""}<div class="opening-video-wrap">${video()}</div><p class="muted rwl-video-note">${escape(l.bridge)}${filmGuide ? ` <a target="_blank" rel="noopener" href="${escape(filmGuide)}" aria-label="Chapters and transcript (opens in a new tab)">Chapters and transcript</a>` : ''}</p>${companionGuide ? `<p>${companionGuide}</p>` : ''}</article>`;const film=stage.querySelector('video');if(film){let watched=0,last=null,marked=false;film.addEventListener('timeupdate',()=>{const t=film.currentTime;if(!film.paused&&last!==null&&t>=last&&t-last<2)watched+=t-last;last=t;if(!marked&&film.duration>0&&watched>=.8*film.duration){marked=true;recordWatch({position_seconds:t,duration_seconds:film.duration,completed_80_percent:true,media_mode:'finished_video'})}});film.addEventListener('error',()=>{if(!stage.contains(film))return;stage.querySelector('.rwl-video-note').textContent='The film could not be loaded. Check your connection and reopen this screen to retry.'})}}
  else if(page===questions.length+2){const correct=questions.filter(x=>draft.answers[x.id]?.correct===true).length;stage.innerHTML=`<article class="rwl-copy"><div class="eyebrow">TAKE IT WITH YOU</div><h2>For the next unfamiliar problem</h2><p class="rwl-bridge math-copy">${escape(l.recap)}</p><p><strong>${correct} of ${questions.length} correct</strong> on your recorded answers.</p><p class="muted">Choose a question to revisit your method and compare it with the worked solution.</p><div class="rwl-results">${questions.map((q,i)=>`<button class="ghost" data-revisit="${i+2}"><span>${i+1}. ${escape(q.title)}</span><b>${recordedResult(draft.answers[q.id],draft.evidence['application:'+q.id])}</b></button>`).join('')}</div>${extension ? '<details class="rwl-extension"><summary>Try a further challenge</summary>'+extension()+'</details>' : ''}</article>`;stage.querySelectorAll('[data-revisit]').forEach(b=>b.onclick=()=>move(Number(b.dataset.revisit)))}
  else mountProblem(questions[page-2]);
  stage.scrollTop=0;syncNav();changedSize?.();
 }
 function mountProblem(q){
  const i=page-2,last=i===questions.length-1,key='rwl-hint:'+q.id,answer=draft.answers[q.id],prompt=q.prompt,stamp=generation;
  const hint=q.hint;stage.innerHTML=`<article class="rwl-copy rwl-problem"><div class="eyebrow">${i===0?'FIRST PRACTICE':last?'UNFAMILIAR CHALLENGE':'YOUR TURN'}</div><h2>${escape(q.title)}</h2>${q.learning?figure(q):''}<p class="problem-prompt math-copy">${escape(prompt)}</p>${q.figure?`<img class="rwl-opening-figure" src="${escape(q.figure.src)}" alt="${escape(q.figure.alt)}">`:''}<form class="rwl-form"><label class="answer-label">Final answer<input type="text" class="final-answer-input" maxlength="90" autocomplete="off" autocapitalize="none" spellcheck="false" required></label><button type="submit" class="primary">Check answer</button></form><label class="support-choice rwl-help"><input type="checkbox"> I used help with this question</label>${hint?`<details class="rwl-hint"><summary>A first hint</summary><p class="math-copy">${escape(hint)}</p></details>`:''}<p class="rwl-feedback" role="status"></p><details class="rwl-rethink" hidden><summary>Try a next step on paper</summary><p class="math-copy"></p></details><button class="secondary rwl-solution" type="button" hidden>See worked solution</button><div class="rwl-steps math-copy" hidden></div></article>`;
  enableFigureViewing(stage);
  const form=stage.querySelector('form'),field=form.querySelector('input'),check=form.querySelector('button'),feedback=stage.querySelector('.rwl-feedback'),reveal=stage.querySelector('.rwl-solution'),solution=stage.querySelector('.rwl-steps'),details=stage.querySelector('.rwl-hint'),helpLabel=stage.querySelector('.rwl-help'),helpBox=helpLabel.querySelector('input');
  const keep='draft-answer:'+q.id;field.value=answer?.response||draft.working[keep]||'';field.oninput=()=>{draft.working[keep]=field.value;markLocal()};
  const displayAnswer = a => {
   field.value = a.response ?? a;
   field.disabled = true;
   check.hidden = true;
   helpLabel.hidden = true;
   if (details) details.hidden = true;
   reveal.hidden = false;
   const evidence = draft.evidence['application:'+q.id];
   if (a.correct === false) {
    feedback.textContent = 'That answer does not match. You can try another step on paper or open the worked solution.';
    offerNextStep(stage.querySelector('.rwl-rethink'), q, l, draft.evidence[key]?.seen === true);
   } else {
    feedback.textContent = a.correct === true ? recordedResult(a, evidence) + '.' : 'Your answer was recorded. Compare it with the worked solution.';
   }
   syncNav();
  };
  const previousHelp=draft.evidence['reasoning:'+q.id]?.used_help===true;
  const setHelp=()=>{
   const irreversible=previousHelp || draft.evidence[key]?.seen===true;
   helpBox.checked=irreversible || draft.evidence[key]?.otherHelp===true;
   helpBox.disabled=irreversible;
  };
  setHelp();
  helpBox.onchange=()=>{draft.evidence[key]={...draft.evidence[key],otherHelp:helpBox.checked};setHelp();markLocal()};
  if(details){
   details.open=draft.evidence[key]?.seen===true;
   const recordHint=()=>{if(!draft.evidence[key]?.seen){draft.evidence[key]={...draft.evidence[key],seen:true};setHelp();markLocal()}};
   details.querySelector('summary').addEventListener('click',()=>{if(!details.open)recordHint()});
   details.ontoggle=()=>{if(details.open)recordHint()};
  }
  form.onsubmit=async e=>{e.preventDefault();if(draft.answers[q.id]||busy||!field.value.trim())return;return trackChange(async()=>{busy=true;syncNav();check.disabled=true;const response=field.value.trim(),help=Boolean(details?.open||draft.evidence[key]?.seen||helpBox.checked);const family=feedbackFamily(l,q);const familiar=wasSeen(family);feedback.textContent='Checking…';try{
    const g=await attempt(q.id,response,help,familiar);const a={response,correct:g.correct,independent_credit:g.independent_credit===true,attempted_at:new Date().toISOString()};draft.answers[q.id]=a;draft.evidence['application:'+q.id]=evidenceFor(l,q,last,a,help,
     familiar || (g.first_attempt===false && !a.independent_credit));
    // The video and worked example have just taught this skill. This question
    // measures application; it cannot establish delayed independent retrieval.
    markLocal();if(stamp===generation)displayAnswer(a);try{await save()}catch{if(stamp===generation)feedback.textContent+=' Your answer is saved on this device; cloud sync is pending.'}
   }catch(err){feedback.textContent=err.message||'Could not check your answer. Try again.';check.disabled=false}finally{busy=false;syncNav()}})};
  reveal.onclick=async()=>{reveal.disabled=true;try{const d=await getSolution(q.id);if(stamp!==generation||!stage.isConnected)return;solution.hidden=false;showSolution(solution,d,q.id);reveal.hidden=true;solution.tabIndex=-1;solution.focus({preventScroll:true});draft.evidence['solution:'+q.id]={seen:true,recorded_at:new Date().toISOString()};markLocal()}catch(err){if(stamp!==generation)return;feedback.textContent=err.message;reveal.disabled=false}};
  if(answer)displayAnswer(answer);
 }
 function move(to){if(busy)return;stage.querySelector('video')?.pause();page=to;locate();show();const heading=stage.querySelector('h2');if(heading){heading.tabIndex=-1;heading.focus({preventScroll:true})}}
 back.onclick=async()=>{if(busy)return;if(page>0)return move(page-1);busy=true;syncNav();try{await home()}catch(err){alert(err.message)}finally{busy=false;syncNav()}};
 next.onclick=async()=>{if(busy||next.disabled)return;if(page<questions.length+2)return move(page+1);busy=true;syncNav();try{await complete()}catch(err){alert('Could not finish saving: '+err.message)}finally{busy=false;syncNav()}};
 show();
}
