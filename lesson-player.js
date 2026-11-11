const LOCAL_TTS_MODEL="onnx-community/Kokoro-82M-v1.0-ONNX";
const LOCAL_VOICE="af_heart", LOCAL_SPEED=0.88, LOCAL_DB="summit-one-secure-audio-v1";
let localTtsPromise=null;
function audioDB(){return new Promise((res,rej)=>{const r=indexedDB.open(LOCAL_DB,1);r.onupgradeneeded=()=>r.result.createObjectStore("audio");r.onsuccess=()=>res(r.result);r.onerror=()=>rej(r.error)});}
async function cachedAudio(key){if(!key)return null;const db=await audioDB();return new Promise((res,rej)=>{const r=db.transaction("audio").objectStore("audio").get(key);r.onsuccess=()=>res(r.result||null);r.onerror=()=>rej(r.error)});}
async function cacheAudio(key,blob){if(!key)return;const db=await audioDB();return new Promise((res,rej)=>{const tx=db.transaction("audio","readwrite");tx.objectStore("audio").put(blob,key);tx.oncomplete=res;tx.onerror=()=>rej(tx.error)});}
async function localTts(){
  if(!localTtsPromise)localTtsPromise=(async()=>{const {KokoroTTS}=await import("https://esm.run/kokoro-js@1.2.1");let last;for(const dtype of ["q8","q4"]){try{return await KokoroTTS.from_pretrained(LOCAL_TTS_MODEL,{dtype,device:"wasm"})}catch(e){last=e}}throw last||new Error("Local narration model could not load")})();
  return localTtsPromise;
}
function chunks(text,max=82){const words=String(text||"").trim().split(/\s+/);const out=[];for(let i=0;i<words.length;i+=max)out.push(words.slice(i,i+max).join(" "));return out;}
function concatFloat(arrays,rate,gap=.22){const gapN=Math.floor(rate*gap),n=arrays.reduce((s,a)=>s+a.length,0)+Math.max(0,arrays.length-1)*gapN,out=new Float32Array(n);let p=0;arrays.forEach((a,i)=>{out.set(a,p);p+=a.length;if(i<arrays.length-1)p+=gapN});return out;}
function wavBlob(samples,rate=24000){const b=new ArrayBuffer(44+samples.length*2),v=new DataView(b);const w=(o,s)=>{for(let i=0;i<s.length;i++)v.setUint8(o+i,s.charCodeAt(i))};w(0,"RIFF");v.setUint32(4,36+samples.length*2,true);w(8,"WAVE");w(12,"fmt ");v.setUint32(16,16,true);v.setUint16(20,1,true);v.setUint16(22,1,true);v.setUint32(24,rate,true);v.setUint32(28,rate*2,true);v.setUint16(32,2,true);v.setUint16(34,16,true);w(36,"data");v.setUint32(40,samples.length*2,true);let o=44;for(const x0 of samples){const x=Math.max(-1,Math.min(1,x0));v.setInt16(o,Math.round(x<0?x*32768:x*32767),true);o+=2}return new Blob([b],{type:"audio/wav"});}
async function synthesizeLocal(text,key,status){
  const cached=await cachedAudio(key);if(cached)return cached;
  status.textContent="Preparing secure narration on this device…";
  const tts=await localTts(),parts=[];let rate=24000;
  for(const part of chunks(text)){const r=await tts.generate(part,{voice:LOCAL_VOICE,speed:LOCAL_SPEED});const samples=r.audio??r.data;if(!samples?.length)throw new Error("Narration model returned no waveform");parts.push(samples);rate=r.sampling_rate||24000;}
  const blob=wavBlob(concatFloat(parts,rate),rate);await cacheAudio(key,blob);return blob;
}

function splitSentences(text){
  return String(text||"").replace(/\s+/g," ").trim().match(/[^.!?]+[.!?]+|[^.!?]+$/g)||[];
}
function motifKind(text){
  const s=text.toLowerCase();
  if(/facing page|next page|maths book|page numbers/.test(s))return"book";
  if(/area|perimeter|triangle|square|polygon|geometry|angle/.test(s))return"geometry";
  if(/grid|path|route|coordinate|row|column|table/.test(s))return"grid";
  if(/ratio|fraction|percentage|rate|average|part|whole/.test(s))return"bars";
  if(/cube|solid|volume|painted|3d/.test(s))return"cube";
  if(/digit|number|remainder|factor|multiple|prime|divisib/.test(s))return"number";
  return"network";
}
function motifSvg(kind){
  if(kind==="book")return `<svg viewBox="0 0 360 210" aria-hidden="true"><path d="M42 52Q96 34 168 58V178Q100 154 42 172Z"/><path d="M318 52Q264 34 192 58V178Q260 154 318 172Z"/><path class="accent" d="M180 58V180"/><path class="thin" d="M66 78Q111 68 151 79M66 100Q111 90 151 101M209 79Q252 68 294 78M209 101Q252 90 294 100"/><text x="132" y="146">158</text><text x="228" y="146">159</text><path class="accent" d="M275 155Q312 133 306 95"/><path d="M294 91l13 4-4 13" class="accent"/></svg>`;
  if(kind==="geometry")return `<svg viewBox="0 0 360 210" aria-hidden="true"><rect x="70" y="25" width="210" height="160" rx="5"/><path d="M70 25L175 105L280 25M70 185L175 105L280 185"/><circle cx="175" cy="105" r="7"/><path class="accent" d="M70 25L175 105L70 185Z"/></svg>`;
  if(kind==="grid")return `<svg viewBox="0 0 360 210" aria-hidden="true"><g class="thin">${Array.from({length:7},(_,i)=>`<path d="M60 ${30+i*25}H310"/>`).join("")}${Array.from({length:11},(_,i)=>`<path d="M${60+i*25} 30V180"/>`).join("")}</g><path class="accent" d="M60 180H110V155H160V130H210V105H260V80H310"/><circle cx="60" cy="180" r="7"/><circle cx="310" cy="80" r="7"/></svg>`;
  if(kind==="bars")return `<svg viewBox="0 0 360 210" aria-hidden="true"><rect x="55" y="55" width="250" height="35" rx="8"/><rect class="accent" x="55" y="55" width="100" height="35" rx="8"/><rect x="55" y="125" width="190" height="35" rx="8"/><path class="thin" d="M105 50V95M155 50V95M205 50V95M255 50V95"/></svg>`;
  if(kind==="cube")return `<svg viewBox="0 0 360 210" aria-hidden="true"><path d="M125 70l70-35 70 35-70 35z"/><path d="M125 70v75l70 35v-75z"/><path class="accent" d="M265 70v75l-70 35v-75z"/><path class="thin" d="M148 58l70 35M172 46l70 35M148 82l70-35M172 94l70-35"/></svg>`;
  if(kind==="number")return `<svg viewBox="0 0 360 210" aria-hidden="true"><path d="M45 120H315"/>${[60,100,140,180,220,260,300].map((x,i)=>`<path class="thin" d="M${x} 108V132"/><text x="${x}" y="155">${i}</text>`).join("")}<circle class="accent-fill" cx="220" cy="120" r="10"/><path class="accent" d="M100 90Q160 35 220 90"/></svg>`;
  return `<svg viewBox="0 0 360 210" aria-hidden="true"><g class="thin"><path d="M75 115L145 55L220 90L290 45M75 115L155 165L220 90L290 155M145 55L155 165"/></g>${[[75,115],[145,55],[155,165],[220,90],[290,45],[290,155]].map(([x,y],i)=>`<circle class="${i===3?"accent-fill":""}" cx="${x}" cy="${y}" r="10"/>`).join("")}</svg>`;
}
export function mountNarratedPlayer(host,{title="",transcript="",audioUrl="",videoUrl="",cacheKey="",onWatch=null}={}){
  if(!host)return;
  const sentences=splitSentences(transcript);
  const words=String(transcript||"").replace(/\s+/g," ").trim().split(" ").filter(Boolean);
  const kind=motifKind(title+" "+transcript.slice(0,500));
  const resumeKey="summit-one-media-position:"+String(cacheKey||title);
  host.className="narrated-player";
  host.innerHTML=`
    <div class="np-screen">
      <video class="np-video" playsinline preload="metadata" ${videoUrl?`src="${videoUrl}"`:""} ${videoUrl?"":"hidden"}></video>
      <div class="np-fallback" ${videoUrl?"hidden":""}>
        <div class="np-visual"><div class="np-label">${title}</div>${motifSvg(kind)}</div>
        <div class="np-caption"><div class="np-sentence"></div><div class="np-glowword" aria-hidden="true"></div></div>
      </div>
    </div>
    <div class="np-controls">
      <button class="np-play primary">Play</button><button class="np-replay ghost">Replay</button>
      <label>Speed <select class="np-speed"><option value=".75">0.75×</option><option value="1" selected>1×</option><option value="1.25">1.25×</option><option value="1.5">1.5×</option></select></label>
      <span class="np-time">0:00</span>
    </div>
    <audio class="np-audio" preload="metadata" ${audioUrl?`src="${audioUrl}"`:""}></audio>
    <details class="np-transcript"><summary>Transcript</summary><p>${transcript}</p></details>
    <div class="np-status"></div>`;
  const video=host.querySelector(".np-video"),fallback=host.querySelector(".np-fallback"),audio=host.querySelector(".np-audio");
  const play=host.querySelector(".np-play"),replay=host.querySelector(".np-replay"),speed=host.querySelector(".np-speed");
  const sent=host.querySelector(".np-sentence"),glow=host.querySelector(".np-glowword"),time=host.querySelector(".np-time"),status=host.querySelector(".np-status");
  const sentenceStarts=[];let k=0;for(const s of sentences){sentenceStarts.push(k);k+=s.trim().split(/\s+/).length}
  let media=videoUrl?video:audio,localNeeded=!videoUrl&&!audioUrl,localLoading=false,watchMarked=false,lastPersist=0,resumeApplied=false;

  function activateFallback(message){
    video.pause();video.hidden=true;fallback.hidden=false;media=audio;
    if(!audio.src)localNeeded=true;
    status.textContent=message||"Secure Kokoro narration will be prepared on this device.";
    render();
  }
  function durationOf(){return Number.isFinite(media.duration)&&media.duration>0?media.duration:Math.max(1,words.length/2.4)}
  function persistPosition(){
    if(!cacheKey||!Number.isFinite(media.currentTime))return;
    const d=durationOf();
    if(d>0&&media.currentTime/d>.92)localStorage.removeItem(resumeKey);
    else localStorage.setItem(resumeKey,String(media.currentTime));
  }
  function applyResume(){
    if(resumeApplied||!cacheKey)return;resumeApplied=true;
    const saved=Number(localStorage.getItem(resumeKey)||0),d=durationOf();
    if(Number.isFinite(saved)&&saved>2&&saved<d-8)media.currentTime=saved;
  }
  function render(){
    const dur=durationOf(),current=Number.isFinite(media.currentTime)?media.currentTime:0;
    if(media===audio){
      const wi=words.length?Math.min(words.length-1,Math.floor((current/dur)*words.length)):0;
      let si=0;for(let i=0;i<sentenceStarts.length;i++){if(sentenceStarts[i]<=wi)si=i;else break}
      sent.textContent=sentences[si]?.trim()||"";
      const w=words[wi]||"";glow.innerHTML=[...w].map(ch=>`<span class="np-letter">${ch}</span>`).join("");
    }
    const m=Math.floor(current/60),s=Math.floor(current%60);time.textContent=`${m}:${String(s).padStart(2,"0")}`;
    play.textContent=media.paused?"Play":"Pause";
    if(!watchMarked&&dur>0&&current/dur>=.8){
      watchMarked=true;
      try{onWatch?.({completed_80_percent:true,position_seconds:Number(current.toFixed(1)),duration_seconds:Number(dur.toFixed(1)),media_mode:media===video?"finished_video":"kokoro_fallback"})}catch{}
    }
    if(current-lastPersist>=5){lastPersist=current;persistPosition()}
  }
  async function ensureAudio(){
    if(media===video&&video.src)return;
    if(!localNeeded&&audio.src){media=audio;return}
    if(localLoading)return;
    localLoading=true;play.disabled=true;replay.disabled=true;
    try{
      const blob=await synthesizeLocal(transcript,cacheKey||title+"|"+transcript.length,status);
      audio.src=URL.createObjectURL(blob);audio.load();media=audio;localNeeded=false;
      status.textContent="Secure Kokoro narration cached on this device.";
    }catch(e){status.textContent="Narration could not be prepared: "+e.message;throw e}
    finally{localLoading=false;play.disabled=false;replay.disabled=false}
  }
  async function ensureMedia(){
    if(media===video&&video.src)return;
    await ensureAudio();
  }
  play.onclick=async()=>{try{await ensureMedia();media.paused?await media.play():media.pause()}catch{}};
  replay.onclick=async()=>{try{await ensureMedia();media.currentTime=0;await media.play()}catch{}};
  speed.onchange=()=>{const v=Number(speed.value);video.playbackRate=v;audio.playbackRate=v};
  for(const el of [video,audio]){
    el.addEventListener("timeupdate",render);
    el.addEventListener("loadedmetadata",()=>{if(el===media){applyResume();render()}});
    el.addEventListener("play",render);el.addEventListener("pause",()=>{persistPosition();render()});
    el.addEventListener("ended",()=>{localStorage.removeItem(resumeKey);render()});
  }
  video.addEventListener("error",()=>activateFallback("Finished lesson video is not available yet. Using the secure Kokoro fallback."));
  audio.addEventListener("error",()=>{if(media!==audio)return;localNeeded=true;audio.removeAttribute("src");audio.load();status.textContent="Audio asset unavailable; press Play to prepare secure Kokoro narration on this device.";play.disabled=false;replay.disabled=false});
  if(videoUrl)status.textContent="Finished lesson video.";
  else status.textContent=audioUrl?"Narrated lesson audio.":"Press Play to prepare secure Kokoro narration on this device.";
  render();
}
