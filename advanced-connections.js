
/** Original, non-assessable advanced-competition enrichment.
 * One substantive, student-readable worked connection for every technique.
 * Never scores, records evidence, or gates a lesson.
 */
import {advancedNumber} from "./advanced-number.js?v=adv-enrichment-20261113";
import {advancedCounting} from "./advanced-counting.js?v=adv-enrichment-20261113";
import {advancedGeometry} from "./advanced-geometry.js?v=adv-enrichment-20261113";

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
      <div class="eyebrow">LOOKING AHEAD · ORIGINAL MATHEMATICS</div>
      <h3>${esc(item.title)}</h3>
      <p class="advanced-path-disclaimer">An optional glimpse of higher-level problem solving — not assessed, no written answer and no effect on progress.</p>
    </header>
    <section class="advanced-path-bridge">
      <h4>From today's idea to a bigger one</h4>
      <p>${esc(item.bridge)}</p>
    </section>
    <section class="advanced-path-example">
      <div class="eyebrow">FOLLOW A MORE ADVANCED EXAMPLE</div>
      <h4>${esc(item.problem)}</h4>
      <ol class="advanced-solution-steps">${stepHTML}</ol>
    </section>
    <section class="advanced-path-horizon">
      <h4>Where this can lead</h4>
      <p>${esc(item.horizon)}</p>
      <p class="advanced-path-context">The ideas connect to styles of problems encountered later in AMC Junior / Intermediate, WAJO and mathematics enrichment. This is an original illustration, not an official past-paper question.</p>
    </section>
    <details class="advanced-path-curiosity">
      <summary>One more thing to wonder about</summary>
      <div class="advanced-path-curiosity-body">
        <p>${esc(item.question)}</p>
        <p><strong>One way to see it:</strong> ${esc(item.peek)}</p>
      </div>
    </details>
    <p class="advanced-path-footnote">${revisit>1?"You are revisiting this technique; look for the principle behind the example rather than just the calculation.":"You do not need to master this yet — it is a preview of what your current technique can unlock."} Move on whenever you are ready.</p>
  </article>`;
}
