import {flashDeck,FLASH_VERSION} from './flash-cards.js?v=centres-20261112';
const esc=s=>String(s??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
export const flashKey=id=>`flash:${FLASH_VERSION}:${id}`;
export function flashReviewed(draft,id){const e=draft.evidence?.[flashKey(id)];return !!(e?.reviewed&&e.responses?.length===5);}
export function mountFlashCards(el,{id,visit=1,slot,investigation=false,draft,save,onComplete=()=>{}}){
 const deck=flashDeck(id,visit,slot,investigation),key=flashKey(id);
 const e=draft.evidence[key]||(draft.evidence[key]={kind:'recognition_practice',version:FLASH_VERSION,skill_id:investigation?null:id,investigation_id:investigation?id:null,visit,independent_credit:false,cursor:0,responses:[],reviewed:false});
 let busy=false,saveError='';
 const persist=async()=>{try{await save();saveError='';return true}catch(err){saveError='Your choices are kept on this device. Cloud save failed: '+err.message;return false}};
 function render(focus=false){
  if(!el.isConnected)return;
  const index=Math.min(e.cursor,4),card=deck[index],r=e.responses[index];
  const done=e.reviewed&&e.responses.length===5;
  el.innerHTML=`<section class="flash-quiz" aria-label="Five quick decisions"><div class="flash-top"><span class="eyebrow">QUICK THINKING · 5 CARDS</span><span class="flash-progress">${done?'Reviewed':`${index+1} / 5`}</span></div><h3>Spot it. Choose it. Understand it.</h3><p class="muted flash-intro">About 2–3 minutes. Pick A or B, then read why. Think of your reason before tapping; there is no countdown.</p>${done?summary():`<div class="flash-dots" aria-hidden="true">${deck.map((_,i)=>`<span class="${i<e.responses.length?'answered':i===index?'current':''}"></span>`).join('')}</div><p class="flash-question" tabindex="-1">${esc(card.q)}</p><div class="flash-options">${card.options.map((option,i)=>`<button type="button" class="flash-option ${r?(i===card.answer?'correct':i===r.choice?'chosen-wrong':''):''}" data-choice="${i}" ${r||busy?'disabled':''}><span class="flash-letter">${i?'B':'A'}</span><span>${esc(option)}</span>${r&&i===card.answer?'<span class="flash-mark">✓</span>':''}</button>`).join('')}</div><div class="flash-feedback" role="status" aria-live="polite">${r?`<b>${r.correct?'Correct.':'Here is the useful distinction.'}</b><p>${esc(card.why)}</p><p class="flash-answer">Best choice: ${card.answer?'B':'A'} · ${esc(card.yes)}</p>`:''}</div>${r?`<button class="primary flash-next" type="button" ${busy||saveError?'disabled':''}>${index===4?'See recap and continue':'Next card →'}</button>`:''}`}
  <div class="flash-save-error" role="alert">${saveError?`${esc(saveError)} <button class="ghost flash-retry" type="button">Retry saving</button>`:''}</div><p class="flash-note">This practises quick decisions. The full problems afterwards test whether you can use them.</p></section>`;
  el.querySelectorAll('.flash-option').forEach(button=>button.onclick=async()=>{
   if(busy||e.responses[index])return;busy=true;
   const choice=Number(button.dataset.choice);
   e.responses[index]={question_id:card.id,choice,correct:choice===card.answer,recorded_at:new Date().toISOString()};
   render();await persist();busy=false;render();
  });
  const next=el.querySelector('.flash-next');if(next)next.onclick=async()=>{
   if(busy||saveError)return;busy=true;render();
   if(index===4)e.reviewed=true;else e.cursor=index+1;
   const ok=await persist();busy=false;
   if(!ok){e.cursor=index;e.reviewed=false;}
   render(ok);
  };
  const retry=el.querySelector('.flash-retry');if(retry)retry.onclick=async()=>{if(busy)return;busy=true;retry.disabled=true;await persist();busy=false;render()};
  el.onkeydown=event=>{if(event.ctrlKey||event.altKey||event.metaKey||event.repeat||busy||e.responses[index]||done)return;const choice={a:0,b:1}[event.key.toLowerCase()];if(choice!==undefined){event.preventDefault();el.querySelector(`[data-choice="${choice}"]`)?.click()}};
  if(focus){const target=el.querySelector('.flash-question,.flash-summary-title');target?.focus({preventScroll:true});target?.scrollIntoView({behavior:'smooth',block:'nearest'});}
  if(done)onComplete(e);
 }
 function summary(){
  const correct=e.responses.filter(r=>r.correct).length;
  return `<div class="flash-summary"><h4 class="flash-summary-title" tabindex="-1">Five decisions practised</h4><p>${correct} of 5 first choices matched. ${correct===5?'Now explain the method in your own words and use it.':'The corrections below are your next useful clues.'}</p><details ${correct<5?'open':''}><summary>${correct<5?'Keep these distinctions in mind':'Review the five takeaways'}</summary><ul>${deck.filter((_,i)=>correct===5||!e.responses[i].correct).map(c=>`<li><b>${esc(c.q)}</b><br>${esc(c.why)}</li>`).join('')}</ul></details><p><b>Next:</b> Apply the idea to a full problem. Choose your own first step and check it against the conditions.</p></div>`;
 }
 render();
}
