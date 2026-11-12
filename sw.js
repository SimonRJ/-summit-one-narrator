const CACHE="summit-one-recognition-20261113";
const STATIC=["./coverage.html","./coverage.js?v=recognition-20261113","./data/amc-coverage.json?v=recognition-20261113","./recognition.js?v=recognition-20261113","./exam-diagnostics.js?v=recognition-20261113","./welcome.html","./welcome.js?v=welcome-voice-c-20261112","./welcome.css?v=welcome-20261112","./transfer-practice.js?v=recognition-20261113","./learning-support.js?v=recognition-20261113","./exam-rules.js?v=recognition-20261113","./flash-cards.js?v=recognition-20261113","./flash-ui.js?v=recognition-20261113","./original-learning.js?v=recognition-20261113","./data/lesson-challenges.json?v=recognition-20261113","./","./index.html","./main.css?v=recognition-20261113","./app-main.js?v=recognition-20261113","./lesson-player.js","./curriculum.js?v=recognition-20261113","./learning-ui.js?v=recognition-20261113","./session-intros.js?v=recognition-20261113","./lesson-journeys.js?v=recognition-20261113","./problem-figures.js","./login.html","./login.js?v=welcome-20261112","./supabase-client.js?v=auth-20261112","./tests.html","./tests.js?v=recognition-20261113","./exam.css?v=recognition-20261113","./manifest.webmanifest","./icon.svg","./robots.txt","./data/sessions-372.json","./data/teaching-72.json","./data/mawa-investigations-20.json","./data/rossmoyne-h23.json","./data/taxonomy-52.json","./data/amc-awards.json","./data/milestones.json"];
self.addEventListener("install",e=>{self.skipWaiting();e.waitUntil(caches.open(CACHE).then(c=>c.addAll(STATIC).catch(()=>{})))});
self.addEventListener("activate",e=>e.waitUntil(Promise.all([caches.keys().then(keys=>Promise.all(keys.filter(k=>k!==CACHE).map(k=>caches.delete(k)))),self.clients.claim()])));
self.addEventListener("fetch",e=>{
  if(e.request.method!=="GET")return;
  const u=new URL(e.request.url);
  if(u.origin!==location.origin||u.pathname.includes("/media/"))return;
  const isPage=e.request.mode==="navigate"||u.pathname.endsWith(".html")||u.pathname.endsWith("/");
  if(isPage){
    e.respondWith(fetch(e.request).then(r=>{const copy=r.clone();caches.open(CACHE).then(c=>c.put(e.request,copy));return r}).catch(()=>caches.match(e.request)));
  }else{
    e.respondWith(caches.match(e.request).then(cached=>cached||fetch(e.request).then(r=>{const copy=r.clone();caches.open(CACHE).then(c=>c.put(e.request,copy));return r})));
  }
});
