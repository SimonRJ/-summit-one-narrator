
/** Original, non-assessable advanced-competition enrichment.
 * One substantive, student-readable worked connection for every technique.
 * Never scores, records evidence, or gates a lesson.
 */
import {advancedNumber} from "./advanced-number.js?v=technique-transfers-20261121";
import {advancedCounting} from "./advanced-counting.js?v=technique-transfers-20261121";
import {advancedGeometry} from "./advanced-geometry.js?v=technique-transfers-20261121";

const rows=[...advancedNumber,...advancedCounting,...advancedGeometry];
export const advancedConnections=Object.freeze(Object.fromEntries(rows.map(
 ([id,title,bridge,problem,steps,horizon,question,peek])=>[id,{title,bridge,problem,steps,horizon,question,peek}]
)));
const esc=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));

export function advancedConnectionHTML(skillId,{visit=1}={}){
 const item=advancedConnections[skillId];
 if(!item)return '<p class="muted">The deeper connection for this lesson is being prepared.</p>';
 const stepHTML=item.steps.map((step,index)=>
  `<li><span class="advanced-step-number">${index+1}</span><span class="advanced-step-text">${esc(step)}</span></li>`).join("");
 const revisit=Math.max(1,Number(visit)||1);
 return `<article class="advanced-path" aria-label="Optional advanced mathematics: ${esc(item.title)}">
    <header class="advanced-path-header">
      <div class="eyebrow">FURTHER CHALLENGE</div>
      <h3>${esc(item.title)}</h3>
      <p class="advanced-path-disclaimer">Optional practice · not assessed</p>
    </header>
    <section class="advanced-path-bridge">
      <h4>The idea</h4>
      <p>${esc(item.bridge)}</p>
    </section>
    <section class="advanced-path-example">
      <div class="eyebrow">WORKED EXAMPLE</div>
      <h4>${esc(item.problem)}</h4>
      <ol class="advanced-solution-steps">${stepHTML}</ol>
    </section>
    <section class="advanced-path-horizon">
      <h4>Try this on paper</h4>
      <p>${esc(item.question)}</p>
      <details class="advanced-path-curiosity">
        <summary>Show one solution</summary>
        <div class="advanced-path-curiosity-body"><p>${esc(item.peek)}</p></div>
      </details>
    </section>
    <p class="advanced-path-footnote">${revisit>1?"When revisiting this technique, remember this. ":""}${esc(item.horizon)}</p>
  </article>`;
}
