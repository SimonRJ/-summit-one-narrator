import {supabase} from './supabase-client.js?v=auth-20261112';
import {methods,exercise} from './curriculum.js?v=centres-20261112';
import {practice,mountPractice,escapeHTML as esc} from './transfer-practice.js?v=centres-20261112';
export async function allRows(makeQuery){const all=[];for(let start=0;;start+=500){const {data,error}=await makeQuery().range(start,start+499);if(error)throw error;all.push(...data);if(data.length<500)return all;}}
export async function queueRepair({userId,sourceType,sourceRef,sourceLabel,skillId,done=0}){
 if(!methods[skillId])return;
 const {error}=await supabase.from('learning_repairs').upsert({user_id:userId,source_type:sourceType,source_ref:sourceRef,source_label:sourceLabel,skill_id:skillId,due_after_session:done},{onConflict:'user_id,source_type,source_ref,skill_id',ignoreDuplicates:true});if(error)throw error;
}
export async function queueLessonRepairs(userId,slot,draft,done){
 for(const [key,e] of Object.entries(draft.evidence||{}))if(e?.correct===false&&methods[e.skill_id])await queueRepair({userId,sourceType:'lesson',sourceRef:`${slot}:${key}`,sourceLabel:`Session ${slot} · ${e.role||e.kind||'check'}`,skillId:e.skill_id,done});
}
const hash=s=>[...s].reduce((a,c)=>(Math.imul(a,31)+c.charCodeAt(0))>>>0,7);
export async function renderRepairs(el,{user,done,records=[]}){
 // Backfill errors recorded before this feature existed; duplicates never reset progress.
 for(const r of records)await queueLessonRepairs(user.id,r.session_number,r,done);
 const rows=await allRows(()=>supabase.from('learning_repairs').select('*').eq('user_id',user.id).order('created_at'));
 const active=rows.filter(r=>r.stage<4),ready=active.filter(r=>r.stage!==3||done>=r.due_after_session);
 el.innerHTML=`<section class="panel hero-panel"><div class="eyebrow">TURN A MISTAKE INTO A TOOL</div><h1>Repair and remember</h1><p>Identify the cause → explain the correction → use the method with support → try changed values independently → check again after three more completed sessions.</p><p>${ready.length} ready now · ${active.length-ready.length} waiting for a delayed check · ${rows.length-active.length} repair cycles completed.</p><p class="muted">A repaired technique is progress, not a promise of an exam score. These checks use familiar methods with changed values; unfamiliar full papers provide separate evidence.</p><div id="repairList"></div></section>`;
 const list=el.querySelector('#repairList');if(!rows.length){list.innerHTML='<p>No saved repairs yet. Mistakes from lessons and new exam submissions will appear here.</p>';return}
 for(const row of [...active,...rows.filter(r=>r.stage===4)]){
  const card=document.createElement('details');card.className='review-detail';card.innerHTML=`<summary>${esc(row.source_label)} · ${row.stage===4?'repair cycle completed':row.stage===3&&done<row.due_after_session?`return after ${row.due_after_session-done} more sessions`:'ready'}</summary><div class="repair-content"></div>`;list.append(card);
  let loaded=false;card.ontoggle=()=>{if(card.open&&!loaded){loaded=true;renderRepair(card.querySelector('.repair-content'),row,{user,done,reload:()=>renderRepairs(el,{user,done})})}};
 }
}
function renderRepair(el,row,{user,done,reload}){
 const m=methods[row.skill_id];if(!m){el.textContent='This item needs a technique mapping before practice can be shown.';return}
 const save=async patch=>{const {data,error}=await supabase.from('learning_repairs').update({...patch,updated_at:new Date().toISOString()}).eq('id',row.id).eq('user_id',user.id).eq('updated_at',row.updated_at).select('id');if(error)throw error;if(!data?.length)throw Error('This repair changed on another device. Reopen it to load the latest step.');await reload()};
 el.innerHTML=`<p><b>The idea:</b> ${esc(m.idea)}</p><p><b>Common trap:</b> ${esc(m.trap)}</p>`;
 if(row.stage===0){
  el.insertAdjacentHTML('beforeend',`<form class="repair-form"><label class="answer-label">Where did it go wrong?<select name="cause" required><option value="">Choose the main cause</option>${['reading the question','choosing a model','choosing a method','calculation','checking','time management'].map(x=>`<option>${x}</option>`).join('')}</select></label><label class="answer-label">Explain the correction in your own words<textarea name="correction" class="answer-box" required minlength="15" placeholder="I first… The missing clue was… Next time I will…"></textarea></label><button class="primary">Save correction and practise</button><p role="status"></p></form>`);
  el.querySelector('form').onsubmit=async e=>{e.preventDefault();const f=e.currentTarget,b=f.querySelector('button');b.disabled=true;try{await save({classification:f.elements.cause.value,stage:1,evidence:{...row.evidence,correction:f.elements.correction.value}})}catch(err){f.querySelector('[role=status]').textContent=err.message;b.disabled=false}};return;
 }
 el.insertAdjacentHTML('beforeend',`<p><b>Your correction:</b> ${esc(row.evidence.correction)}</p>`);
 if(row.stage===4){el.insertAdjacentHTML('beforeend','<p class="success-note">Supported correction, an independent changed example and a delayed check are recorded. Keep testing the idea in unfamiliar problems.</p>');return}
 if(row.stage===3&&done<row.due_after_session){el.insertAdjacentHTML('beforeend',`<p>Continue learning. This check unlocks after ${row.due_after_session-done} more completed sessions; calendar days do not matter.</p>`);return}
 const history=row.evidence.history||[],seed=(hash(row.id)%52)+history.length+row.stage*7,q=practice(row.skill_id,seed);
 const panel=document.createElement('div');el.append(panel);const draft={evidence:{},working:{}};
 mountPractice(panel,{id:row.skill_id,seed,key:'repair',draft,save:async()=>{},supported:row.stage===1,label:row.stage===1?'FINISH THE WORKED EXAMPLE':row.stage===2?'CHANGED VALUES · WITHOUT NOTES':'DELAYED CHECK · WITHOUT NOTES',onDone:async e=>{
  const success=e.correct&&!e.used_help;
  const next=row.stage===1?2:success?(row.stage===2?3:4):2;
  const message=document.createElement('p');message.textContent=next===3?'Independent answer saved. Return after three more completed sessions.':next===4?'Delayed check passed.':row.stage===1?'Now try changed values without help.':'Read the correction, then try another changed example. Help is useful; an unassisted answer is still needed.';panel.append(message);
  const button=document.createElement('button');button.className='primary';button.textContent='Save repair step';panel.append(button);
  button.onclick=async()=>{button.disabled=true;try{await save({stage:next,due_after_session:next===3?done+3:done,evidence:{...row.evidence,history:[...history,{...e,session:done,prompt:q.prompt}]}})}catch(err){message.textContent=err.message;button.disabled=false}};
 }});
}
export const rubricAnchors={result:['No justified result yet','Some useful cases; major gaps remain','Main result correct; one part incomplete','All requested results correct and checked'],method:['No usable strategy recorded','Relevant idea but incomplete execution','Coherent method with a small gap','Efficient, reproducible method throughout'],proof:['Examples only, or no justification','Some reasons; missing cases or a claim assumed','Nearly complete; one justification needs repair','Every case covered; bound and construction or general claim justified'],clarity:['Reasoning difficult to follow','Labels, order and explanations let another reader follow']};
export function rubricHTML(){return `<details class="rubric-guide"><summary>What each rubric score means</summary>${Object.entries(rubricAnchors).map(([key,anchors])=>`<h4>${esc(key)}</h4><ol start="0">${anchors.map(a=>`<li>${esc(a)}</li>`).join('')}</ol>`).join('')}</details>`;}
export async function mountInvestigationReview(el,{user,record,item}){
 const reviews=await allRows(()=>supabase.from('investigation_reviews').select('*').eq('user_id',user.id).eq('session_number',record.session_number).order('reviewed_at'));
 el.innerHTML=`<h3>Model reasoning and adult review</h3><details><summary>Open worked investigation solution</summary><p class="math-copy">${esc(item?.solution||'Model not available for this archived version.')}</p><h4>Transfer solution</h4><p class="math-copy">${esc(item?.transfer_solution||'')}</p></details>${rubricHTML()}<p class="muted">The learner's original work and self-score remain locked. A parent or tutor can add a separate review here. The entered reviewer name is self-declared; it is not a separately verified account.</p>${reviews.map(r=>`<article class="check-status"><b>${esc(r.reviewer_name)} · ${esc(r.reviewer_role)}</b><p>${Object.entries(r.rubric).map(([k,v])=>`${esc(k)} ${v}`).join(' · ')}</p><p>${esc(r.notes)}</p><small>${new Date(r.reviewed_at).toLocaleDateString()}</small></article>`).join('')}<form class="adult-review"><label class="answer-label">Reviewer name<input name="reviewer" required maxlength="80"></label><label class="answer-label">Role<select name="role"><option value="parent">Parent</option><option value="tutor">Tutor</option></select></label>${Object.entries(rubricAnchors).map(([key,anchors])=>`<label class="answer-label">${esc(key)}<select name="${key}" required><option value="">Choose from the evidence</option>${anchors.map((a,i)=>`<option value="${i}">${i} — ${esc(a)}</option>`).join('')}</select></label>`).join('')}<label class="answer-label">Feedback and one next step<textarea name="notes" class="answer-box" required minlength="15"></textarea></label><button class="primary">Save adult review</button><p role="status"></p></form>`;
 el.querySelector('form').onsubmit=async e=>{e.preventDefault();const f=e.currentTarget,b=f.querySelector('button');b.disabled=true;const rubric=Object.fromEntries(Object.keys(rubricAnchors).map(k=>[k,Number(f.elements[k].value)]));try{const {error}=await supabase.from('investigation_reviews').insert({user_id:user.id,session_number:record.session_number,reviewer_name:f.elements.reviewer.value,reviewer_role:f.elements.role.value,rubric,notes:f.elements.notes.value});if(error)throw error;await mountInvestigationReview(el,{user,record,item})}catch(err){f.querySelector('[role=status]').textContent=err.message;b.disabled=false}};
}
