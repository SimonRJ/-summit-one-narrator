function splitSentences(text){
  return String(text||"").replace(/\s+/g," ").trim().match(/[^.!?]+[.!?]+|[^.!?]+$/g)||[];
}
function motifKind(text){
  const s=text.toLowerCase();
  if(/area|perimeter|triangle|square|polygon|geometry|angle/.test(s))return"geometry";
  if(/grid|path|route|coordinate|row|column|table/.test(s))return"grid";
  if(/ratio|fraction|percentage|rate|average|part|whole/.test(s))return"bars";
  if(/cube|solid|volume|painted|3d/.test(s))return"cube";
  if(/digit|number|remainder|factor|multiple|prime|divisib/.test(s))return"number";
  return"network";
}
function motifSvg(kind){
  if(kind==="geometry")return `<svg viewBox="0 0 360 210" aria-hidden="true"><rect x="70" y="25" width="210" height="160" rx="5"/><path d="M70 25L175 105L280 25M70 185L175 105L280 185"/><circle cx="175" cy="105" r="7"/><path class="accent" d="M70 25L175 105L70 185Z"/></svg>`;
  if(kind==="grid")return `<svg viewBox="0 0 360 210" aria-hidden="true"><g class="thin">${Array.from({length:7},(_,i)=>`<path d="M60 ${30+i*25}H310"/>`).join("")}${Array.from({length:11},(_,i)=>`<path d="M60+${i*25} 30V180"/>`.replace("60+",""+(60+i*25)+" ").replace(" "+(60+i*25)+" ",""))}</g><path class="accent" d="M60 180H110V155H160V130H210V105H260V80H310"/><circle cx="60" cy="180" r="7"/><circle cx="310" cy="80" r="7"/></svg>`;
  if(kind==="bars")return `<svg viewBox="0 0 360 210" aria-hidden="true"><rect x="55" y="55" width="250" height="35" rx="8"/><rect class="accent" x="55" y="55" width="100" height="35" rx="8"/><rect x="55" y="125" width="190" height="35" rx="8"/><path class="thin" d="M105 50V95M155 50V95M205 50V95M255 50V95"/></svg>`;
  if(kind==="cube")return `<svg viewBox="0 0 360 210" aria-hidden="true"><path d="M125 70l70-35 70 35-70 35z"/><path d="M125 70v75l70 35v-75z"/><path class="accent" d="M265 70v75l-70 35v-75z"/><path class="thin" d="M148 58l70 35M172 46l70 35M148 82l70-35M172 94l70-35"/></svg>`;
  if(kind==="number")return `<svg viewBox="0 0 360 210" aria-hidden="true"><path d="M45 120H315"/>${[60,100,140,180,220,260,300].map((x,i)=>`<path class="thin" d="M${x} 108V132"/><text x="${x}" y="155">${i}</text>`).join("")}<circle class="accent-fill" cx="220" cy="120" r="10"/><path class="accent" d="M100 90Q160 35 220 90"/></svg>`;
  return `<svg viewBox="0 0 360 210" aria-hidden="true"><g class="thin"><path d="M75 115L145 55L220 90L290 45M75 115L155 165L220 90L290 155M145 55L155 165"/></g>${[[75,115],[145,55],[155,165],[220,90],[290,45],[290,155]].map(([x,y],i)=>`<circle class="${i===3?"accent-fill":""}" cx="${x}" cy="${y}" r="10"/>`).join("")}</svg>`;
}
export function mountNarratedPlayer(host,{title="",transcript="",audioUrl=""}={}){
  if(!host)return;
  const sentences=splitSentences(transcript);
  const words=String(transcript||"").replace(/\s+/g," ").trim().split(" ").filter(Boolean);
  const kind=motifKind(title+" "+transcript.slice(0,500));
  host.className="narrated-player";
  host.innerHTML=`
    <div class="np-screen">
      <div class="np-visual"><div class="np-label">${title}</div>${motifSvg(kind)}</div>
      <div class="np-caption"><div class="np-sentence"></div><div class="np-glowword" aria-hidden="true"></div></div>
    </div>
    <div class="np-controls">
      <button class="np-play primary">Play</button><button class="np-replay ghost">Replay</button>
      <label>Speed <select class="np-speed"><option value=".75">0.75×</option><option value="1" selected>1×</option><option value="1.25">1.25×</option><option value="1.5">1.5×</option></select></label>
      <span class="np-time">0:00</span>
    </div>
    <audio class="np-audio" preload="metadata" src="${audioUrl}"></audio>
    <details class="np-transcript"><summary>Transcript</summary><p>${transcript}</p></details>
    <div class="np-status"></div>`;
  const audio=host.querySelector(".np-audio"),play=host.querySelector(".np-play"),replay=host.querySelector(".np-replay"),speed=host.querySelector(".np-speed"),sent=host.querySelector(".np-sentence"),glow=host.querySelector(".np-glowword"),time=host.querySelector(".np-time"),status=host.querySelector(".np-status");
  const sentenceStarts=[];let k=0;for(const s of sentences){sentenceStarts.push(k);k+=s.trim().split(/\s+/).length}
  const render=()=>{
    const dur=Number.isFinite(audio.duration)&&audio.duration>0?audio.duration:Math.max(1,words.length/2.4);
    const wi=Math.min(words.length-1,Math.floor((audio.currentTime/dur)*words.length));
    let si=0;for(let i=0;i<sentenceStarts.length;i++){if(sentenceStarts[i]<=wi)si=i;else break}
    sent.textContent=sentences[si]?.trim()||"";
    const w=words[wi]||"";glow.innerHTML=[...w].map(ch=>`<span class="np-letter">${ch}</span>`).join("");
    const m=Math.floor(audio.currentTime/60),s=Math.floor(audio.currentTime%60);time.textContent=`${m}:${String(s).padStart(2,"0")}`;
    play.textContent=audio.paused?"Play":"Pause";
  };
  play.onclick=()=>audio.paused?audio.play().catch(e=>status.textContent=e.message):audio.pause();
  replay.onclick=()=>{audio.currentTime=0;audio.play().catch(e=>status.textContent=e.message)};
  speed.onchange=()=>audio.playbackRate=Number(speed.value);
  audio.addEventListener("timeupdate",render);audio.addEventListener("loadedmetadata",render);audio.addEventListener("play",render);audio.addEventListener("pause",render);
  audio.addEventListener("error",()=>{status.textContent="Narration media is still being published. The written explanation remains available.";play.disabled=true;replay.disabled=true});
  render();
}
