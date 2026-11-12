// A welcome is optional. This page never writes learner evidence or starts an exam.
const video=document.querySelector('#welcomeVideo');
// Keep the poster clean until the learner chooses playback. Native controls stay available afterwards.
video.controls=false;
const watch=document.querySelector('#watchWelcome');
const skip=document.querySelector('#skipWelcome');
const status=document.querySelector('#welcomeStatus');
const replay=new URLSearchParams(location.search).get('from')==='dashboard';
if(replay)skip.textContent='Back to my learning';
function say(message,error=false){status.textContent=message;status.classList.toggle('error',error)}
watch.addEventListener('click',async()=>{
  if(!video.paused){video.pause();say('Paused. Take your time.');return}
  try{
    watch.disabled=true;video.controls=true;say('Opening your welcome…');
    if(video.error)video.load();
    if(video.ended)video.currentTime=0;
    await video.play();
    video.scrollIntoView({block:'center',behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'});
    say('You can pause, use full screen, or skip to learning at any time.');
  }catch{
    say('The video could not start. Try again, open the MP4 below, or continue to learning.',true);
  }finally{watch.disabled=false}
});
video.addEventListener('play',()=>{watch.textContent='Pause welcome'});
video.addEventListener('pause',()=>{if(!video.ended)watch.textContent='Continue watching'});
video.addEventListener('ended',()=>{
  watch.textContent='Watch again';skip.textContent='Start my next step';
  say('Your next discovery starts here, Reef. Continue whenever you’re ready.');
});
video.addEventListener('error',()=>{
  watch.disabled=false;watch.textContent='Try video again';
  say('The video is unavailable right now. You can still go straight to your learning.',true);
});
skip.addEventListener('click',()=>video.pause());
video.addEventListener('loadedmetadata',()=>{
  if(Number.isFinite(video.duration))document.querySelector('#videoDuration').textContent=`${Math.floor(video.duration/60)}:${String(Math.floor(video.duration%60)).padStart(2,'0')} · Full HD · Spoken captions`;
});
fetch('./review/ReefWelcome-qa.json').then(r=>r.ok?r.json():null).then(q=>{
  if(q?.duration_seconds)document.querySelector('#videoDuration').textContent=`${Math.floor(q.duration_seconds/60)}:${String(Math.floor(q.duration_seconds%60)).padStart(2,'0')} · Full HD · Spoken captions`;
}).catch(()=>{});
if('serviceWorker' in navigator)navigator.serviceWorker.register('./sw.js').catch(()=>{});
