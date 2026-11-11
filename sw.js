const CACHE="summit-one-amc-interface-20261112";
const STATIC=["./","./index.html","./main.css?v=journey-20261112","./app-main.js?v=journey-20261112","./lesson-player.js","./curriculum.js?v=journey-20261112","./learning-ui.js?v=journey-20261112","./session-intros.js?v=journey-20261112","./lesson-journeys.js?v=journey-20261112","./problem-figures.js","./login.html","./login.js?v=auth-20261112","./supabase-client.js?v=auth-20261112","./tests.html","./tests.js?v=amc-interface-20261112","./exam.css?v=amc-interface-20261112","./manifest.webmanifest","./icon.svg","./robots.txt","./data/sessions-372.json","./data/teaching-72.json","./data/mawa-investigations-20.json","./data/rossmoyne-h23.json","./data/taxonomy-52.json","./data/amc-awards.json","./data/milestones.json"];
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
