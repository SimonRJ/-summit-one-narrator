/* Summit One cinematic boot + restrained asynchronous transition loader. */
(function makeSummitBootLoader(){
  "use strict";
  const root=document.getElementById("summitBoot");
  if(!root)return;
  const prefersReduced=window.matchMedia?.("(prefers-reduced-motion: reduce)")?.matches===true;
  const kind=root.getAttribute("data-mode")==="compact"?"compact":"main";
  let previouslyShown=false;
  try{previouslyShown=sessionStorage.getItem("summit-one:cinematic-boot:v1")==="1"}catch{}
  const cinematic=kind==="main"&&!previouslyShown&&!prefersReduced;
  const started=performance.now();
  let isReady=false,skipped=false,closed=false;
  const miniSessions=new Map();
  let nextMiniId=1,miniShownAt=0,miniHideTimer=null;
  const logo=`
    <svg class="sb-summit-gem" viewBox="0 0 284 266" aria-hidden="true" focusable="false">
      <defs>
        <linearGradient id="sbFacetLeft" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" stop-color="#f1fbff"/><stop offset=".38" stop-color="#a8d7ec"/>
          <stop offset="1" stop-color="#1b456b"/>
        </linearGradient>
        <linearGradient id="sbFacetRight" x1=".2" y1="0" x2=".95" y2="1">
          <stop offset="0" stop-color="#d9f6ff"/><stop offset=".52" stop-color="#5aa3d6"/>
          <stop offset="1" stop-color="#12304c"/>
        </linearGradient>
        <linearGradient id="sbFacetBase" x1=".2" y1=".1" x2=".7" y2=".95">
          <stop offset="0" stop-color="#224e76"/><stop offset=".7" stop-color="#0c2a4a"/>
          <stop offset="1" stop-color="#06172e"/>
        </linearGradient>
        <linearGradient id="sbEdge" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#effaff"/><stop offset="1" stop-color="#6acdf7"/></linearGradient>
        <filter id="sbBlur"><feGaussianBlur stdDeviation="6"/></filter>
      </defs>
      <g class="sb-gem-glow" filter="url(#sbBlur)" opacity=".65">
        <path d="M142 19 259 232H25Z" stroke="#6edfff" stroke-width="6" fill="none"/>
      </g>
      <path class="sb-facet sb-facet--left" d="M142 19 25 232 142 157Z" fill="url(#sbFacetLeft)"/>
      <path class="sb-facet sb-facet--right" d="M142 19 259 232 142 157Z" fill="url(#sbFacetRight)"/>
      <path class="sb-facet sb-facet--base" d="M25 232 142 157 259 232Z" fill="url(#sbFacetBase)"/>
      <path class="sb-gem-outline" d="M142 19 25 232 259 232Z M142 19 142 157 25 232 M142 157 259 232" stroke="url(#sbEdge)" stroke-width="1.8" fill="none" stroke-linejoin="round"/>
      <path d="M142 19 142 157" stroke="#f8fdff" stroke-width="1.3" opacity=".7"/>
    </svg>`;
  const logoTiny=`<svg viewBox="0 0 70 70" aria-hidden="true" focusable="false">
      <path d="M35 5 63 59H7Z" fill="#0c253e" stroke="#76dafe" stroke-width="1.8"/>
      <path d="M35 5 7 59 35 42Z" fill="#9bcde5"/>
      <path d="M35 5 63 59 35 42Z" fill="#4c96bc"/>
      <path d="M7 59 35 42 63 59Z" fill="#133c59"/>
    </svg>`;
  root.innerHTML=`
    <div class="sb-aura sb-aura-one" aria-hidden="true"></div>
    <div class="sb-aura sb-aura-two" aria-hidden="true"></div>
    <div class="sb-grid" aria-hidden="true"></div>
    <div class="sb-stars" aria-hidden="true"></div>
    <div class="sb-math sb-math-left" aria-hidden="true">a² + b² = c²</div>
    <div class="sb-math sb-math-right" aria-hidden="true">∑ n</div>
    <div class="sb-math sb-math-bottom" aria-hidden="true">π &nbsp; · &nbsp; ∞ &nbsp; · &nbsp; φ</div>
    <div class="sb-stage">
      <div class="sb-logo-frame" aria-hidden="true">
        <div class="sb-ring sb-ring-outer"></div>
        <div class="sb-ring sb-ring-inner"></div>
        <div class="sb-gem">${logo}</div>
        <div class="sb-gem-sweep"></div>
        <div class="sb-logo-light"></div>
      </div>
      <div class="sb-type">
        <div class="sb-wordmark"><span>SUMMIT</span><span class="sb-one"> ONE</span></div>
        <div class="sb-subtitle">MATHEMATICS TRAINING</div>
      </div>
      <div class="sb-status" id="sbStatus">Preparing your learning experience<span class="sb-ellipsis" aria-hidden="true"></span></div>
      <div class="sb-progress-line" aria-hidden="true"><span></span></div>
    </div>
    <div class="sb-controls">
      <button type="button" class="sb-sound" id="sbSound" aria-label="Play the Summit One opening sound">♪ <span>Play sound</span></button>
      <button type="button" class="sb-skip" id="sbSkip">Skip animation</button>
    </div>`;
  root.classList.add(cinematic?"sb-cinematic":"sb-brief");
  document.body.classList.add("summit-splash-active");
  if(prefersReduced)root.classList.add("sb-motion-reduced");
  const stars=root.querySelector(".sb-stars");
  for(let i=0;i<26;i++){
    const span=document.createElement("i");
    const n=(i*73+29)%101, m=(i*39+13)%97;
    span.style.setProperty("--star-x",n+"%");
    span.style.setProperty("--star-y",m+"%");
    span.style.setProperty("--star-d",(i%9)*.32+"s");
    span.style.setProperty("--star-size",i%6===0?"3px":i%3===0?"2px":"1px");
    stars.append(span);
  }
  const status=root.querySelector("#sbStatus"), sound=root.querySelector("#sbSound");
  const skipButton=root.querySelector("#sbSkip");
  if(!cinematic){sound.hidden=true;skipButton.hidden=true;}
  function originalSignatureSound(){
    const AC=window.AudioContext||window.webkitAudioContext;
    if(!AC||prefersReduced)return false;
    const ctx=new AC(), master=ctx.createGain();
    master.gain.value=.32;
    master.connect(ctx.destination);
    const at=ctx.currentTime+.03;
    for(const [freq,delay,duration,volume] of [[130.81,.02,.8,.08],[196,.15,.85,.05],[261.63,.28,1,.055],[392,.47,.68,.025]]){
      const os=ctx.createOscillator(),g=ctx.createGain(),f=ctx.createBiquadFilter();
      os.type="sine";os.frequency.setValueAtTime(freq,at+delay);
      f.type="lowpass";f.frequency.value=1800;
      g.gain.setValueAtTime(0,at+delay);
      g.gain.linearRampToValueAtTime(volume,at+delay+.07);
      g.gain.exponentialRampToValueAtTime(.001,at+delay+duration);
      os.connect(f);f.connect(g);g.connect(master);
      os.start(at+delay);os.stop(at+delay+duration+.05);
    }
    const length=Math.round(ctx.sampleRate*.6);
    const noise=ctx.createBuffer(1,length,ctx.sampleRate),data=noise.getChannelData(0);
    for(let i=0;i<length;i++)data[i]=(Math.random()*2-1)*.14;
    const src=ctx.createBufferSource(),filter=ctx.createBiquadFilter(),gain=ctx.createGain();
    src.buffer=noise;filter.type="bandpass";filter.frequency.setValueAtTime(340,at);
    filter.frequency.exponentialRampToValueAtTime(1900,at+.49);
    filter.Q.value=.5;gain.gain.setValueAtTime(.001,at);
    gain.gain.linearRampToValueAtTime(.055,at+.24);
    gain.gain.exponentialRampToValueAtTime(.001,at+.55);
    src.connect(filter);filter.connect(gain);gain.connect(master);src.start(at);src.stop(at+.57);
    ctx.resume().catch(()=>{});
    setTimeout(()=>ctx.close().catch(()=>{}),1800);
    return true;
  }
  sound.addEventListener("click",()=>{
    try{
      if(originalSignatureSound()){
        sound.innerHTML="♫ <span>Sound played</span>";
        sound.setAttribute("aria-label","Replay the Summit One opening sound");
      }
    }catch{
      sound.innerHTML="♪ <span>Sound unavailable</span>";
    }
  });
  function finish(){
    if(closed)return;
    closed=true;
    root.classList.add("sb-leaving");
    document.body.classList.remove("summit-splash-active");
    try{sessionStorage.setItem("summit-one:cinematic-boot:v1","1")}catch{}
    setTimeout(()=>{root.hidden=true;root.setAttribute("aria-hidden","true");},530);
  }
  function ready(){
    if(isReady)return;
    isReady=true;
    clearTimeout(safetyTimeout);
    if(status)status.textContent="Ready";
    const minimum=skipped||prefersReduced?0:cinematic?2700:kind==="compact"?0:140;
    setTimeout(finish,Math.max(0,minimum-(performance.now()-started)));
  }
  skipButton.addEventListener("click",()=>{
    skipped=true;
    if(isReady)finish();
    else{
      skipButton.textContent="Almost ready…";
      if(status)status.textContent="Preparing your course";
    }
  });
  const safetyTimeout=setTimeout(ready,13000);
  const mini=document.createElement("div");
  mini.id="summitMini";
  mini.className="summit-mini";
  mini.hidden=true;
  mini.setAttribute("role","status");
  mini.setAttribute("aria-live","polite");
  mini.innerHTML=`<div class="sm-card"><div class="sm-mark">${logoTiny}</div><div class="sm-wordmark">SUMMIT <span>ONE</span></div><div class="sm-caption" id="smCaption">Loading</div><div class="sm-dots" aria-hidden="true"><span></span><span></span><span></span></div></div>`;
  document.body.append(mini);
  function renderMini(){
    if(!miniSessions.size||!root.hidden)return;
    const latest=[...miniSessions.values()].at(-1);
    if(!latest||latest.timer!==null)return;
    clearTimeout(miniHideTimer);
    mini.querySelector("#smCaption").textContent=latest.label||"Loading";
    mini.hidden=false;
    miniShownAt=performance.now();
  }
  function beginSmall(label="Opening lesson",delay=190){
    const id=nextMiniId++;
    const item={id,label,timer:null};
    item.timer=setTimeout(()=>{item.timer=null;renderMini()},delay);
    miniSessions.set(id,item);
    return id;
  }
  function endSmall(id){
    const item=miniSessions.get(id);
    if(!item)return;
    if(item.timer!==null)clearTimeout(item.timer);
    miniSessions.delete(id);
    if(!miniSessions.size){
      clearTimeout(miniHideTimer);
      const delay=mini.hidden?0:Math.max(0,300-(performance.now()-miniShownAt));
      miniHideTimer=setTimeout(()=>{if(!miniSessions.size)mini.hidden=true},delay);
    }else{
      const latest=[...miniSessions.values()].at(-1);
      if(latest&&!mini.hidden)mini.querySelector("#smCaption").textContent=latest.label;
    }
  }
  async function withSmallLoading(job,label="Loading"){
    const token=beginSmall(label);
    try{return await job()}
    finally{endSmall(token)}
  }
  window.SummitLoader={ready,beginSmall,endSmall,withSmallLoading,skip:()=>{skipped=true;if(isReady)finish()},get mode(){return cinematic?"cinematic":"compact"}};
})();
