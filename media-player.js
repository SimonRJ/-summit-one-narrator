const RELEASE_BASE="https://github.com/SimonRJ/-summit-one-narrator/releases/download/summit-one-audio-v1";

function esc(s){return String(s??"").replace(/[&<>"']/g,m=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[m]))}
function visual(item){
 const key=((item.category||"")+" "+(item.chapter_title||item.source||"")+" "+(item.title||"")).toLowerCase();
 const common='viewBox="0 0 800 450" aria-hidden="true" style="position:absolute;inset:0;width:100%;height:100%;opacity:.28"';
 if(/area|perimeter|angle|geometry|shaded|square|triangle/.test(key))return `<svg ${common}><rect x="120" y="70" width="300" height="300" rx="8" fill="none" stroke="#70dcff" stroke-width="6"/><path d="M120 370L420 70M120 210L420 270M270 70L330 370" fill="none" stroke="#ffd166" stroke-width="5"/><circle cx="291" cy="199" r="9" fill="#7ce0a3"/></svg>`;
 if(/cube|solid|volume|surface/.test(key))return `<svg ${common}><g fill="none" stroke="#70dcff" stroke-width="5"><path d="M250 110l110-55 110 55-110 60z"/><path d="M250 110v120l110 65 110-65V110M360 170v125"/><path d="M360 295l110 60 110-60V175l-110-60M470 355V230"/></g></svg>`;
 if(/digit|place|number|prime|factor|divisib|remainder/.test(key))return `<svg ${common}><g font-family="system-ui" font-weight="900" font-size="52" text-anchor="middle"><rect x="120" y="110" width="100" height="100" rx="18" fill="#70dcff22" stroke="#70dcff"/><text x="170" y="178" fill="#fff">2</text><rect x="250" y="110" width="100" height="100" rx="18" fill="#ffd16622" stroke="#ffd166"/><text x="300" y="178" fill="#fff">3</text><rect x="380" y="110" width="100" height="100" rx="18" fill="#7ce0a322" stroke="#7ce0a3"/><text x="430" y="178" fill="#fff">5</text><path d="M170 245H430" stroke="#ff7aa8" stroke-width="6"/><text x="300" y="315" fill="#70dcff">structure</text></g></svg>`;
 if(/time|rate|before|after|schedule/.test(key))return `<svg ${common}><path d="M100 240H700" stroke="#70dcff" stroke-width="7"/><g fill="#ffd166"><circle cx="180" cy="240" r="15"/><circle cx="390" cy="240" r="15"/><circle cx="620" cy="240" r="15"/></g><g fill="#fff" font-family="system-ui" font-size="28"><text x="150" y="205">start</text><text x="360" y="205">change</text><text x="590" y="205">check</text></g></svg>`;
 if(/count|arrang|case|probability|route|network|path|symmetry/.test(key))return `<svg ${common}><g fill="none" stroke="#70dcff" stroke-width="5"><path d="M170 110L310 200L170 310M310 200L470 110M310 200L470 200M310 200L470 310M470 110L640 160M470 200L640 230M470 310L640 300"/></g><g fill="#ffd166">${[[170,110],[170,310],[310,200],[470,110],[470,200],[470,310],[640,160],[640,230],[640,300]].map(([x,y])=>`<circle cx="${x}" cy="${y}" r="10"/>`).join("")}</g></svg>`;
 return `<svg ${common}><g fill="none" stroke-width="5"><rect x="120" y="130" width="500" height="55" rx="18" stroke="#70dcff"/><rect x="120" y="215" width="340" height="55" rx="18" stroke="#ffd166"/><rect x="120" y="300" width="220" height="55" rx="18" stroke="#7ce0a3"/></g></svg>`;
}
function segments(item){
  if(item.chunks?.length)return item.chunks.map(x=>x.text);
  const s=item.spoken_script||item.transcript||"";
  const p=s.split(/\n\n+/).map(x=>x.trim()).filter(Boolean);
  if(p.length)return p;
  return [s];
}
export function mediaUrl(id){return `${RELEASE_BASE}/${encodeURIComponent(id)}_narration.wav`}
export function renderNarratedLesson(container,item,{label="Video explanation"}={}){
  const seg=segments(item),id=item.id||item.video_id;
  container.innerHTML=`
    <div class="cinema">
      ${visual(item)}
      <div class="frame-content">
        <div class="frame-kicker">${esc(label)} · ${esc(id)}</div>
        <div class="frame-title">${esc(item.title||item.chapter_title||"Mathematical reasoning")}</div>
        <div id="frameText" class="frame-text glow">${esc(seg[0]||"")}</div>
      </div>
    </div>
    <div class="player-controls">
      <audio id="narration" controls preload="metadata" src="${mediaUrl(id)}"></audio>
      <button type="button" id="replayMedia">Replay</button>
      <label class="mini">Speed <select id="mediaSpeed"><option>.75</option><option selected>1</option><option>1.25</option><option>1.5</option></select></label>
    </div>
    <div id="mediaNote" class="mini">Narration and visual explanation stay separate from independent-solve credit.</div>
    <details><summary>Transcript</summary><div class="mini" style="white-space:pre-wrap;margin-top:10px">${esc(seg.join("\n\n"))}</div></details>
  `;
  const audio=container.querySelector("#narration"),text=container.querySelector("#frameText"),note=container.querySelector("#mediaNote");
  let last=-1;
  const update=()=>{
    const ratio=audio.duration?Math.min(0.999,audio.currentTime/audio.duration):0;
    const idx=Math.min(seg.length-1,Math.floor(ratio*seg.length));
    if(idx!==last){last=idx;text.textContent=seg[idx]||"";text.classList.remove("glow");void text.offsetWidth;text.classList.add("glow")}
  };
  audio.addEventListener("timeupdate",update);
  audio.addEventListener("loadedmetadata",update);
  audio.addEventListener("error",()=>note.textContent="Narration media is still publishing. The full transcript remains available here; this does not affect your answer record.");
  container.querySelector("#replayMedia").onclick=()=>{audio.currentTime=0;audio.play().catch(()=>{})};
  container.querySelector("#mediaSpeed").onchange=e=>audio.playbackRate=Number(e.target.value);
  return {audio};
}
