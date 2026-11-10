const RELEASE_BASE="https://github.com/SimonRJ/-summit-one-narrator/releases/download/summit-one-audio-v1";

function esc(s){return String(s??"").replace(/[&<>"']/g,m=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[m]))}
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
