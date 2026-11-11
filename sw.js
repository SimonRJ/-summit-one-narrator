const CACHE="summit-one-v17";
const STATIC=["./","./index.html","./main.css?v=3","./app-main.js?v=12","./lesson-player.js","./problem-figures.js","./login.html","./login.js","./supabase-client.js","./tests.html","./tests.js?v=3","./exam.css?v=2","./manifest.webmanifest","./icon.svg","./robots.txt","./data/sessions-372.json","./data/teaching-72.json","./data/mawa-investigations-20.json","./data/rossmoyne-h23.json","./data/taxonomy-52.json","./data/amc-awards.json","./data/milestones.json"];
self.addEventListener("install",e=>{self.skipWaiting();e.waitUntil(caches.open(CACHE).then(c=>c.addAll(STATIC).catch(()=>{})))});
self.addEventListener("activate",e=>e.waitUntil(Promise.all([caches.keys().then(keys=>Promise.all(keys.filter(k=>k!==CACHE).map(k=>caches.delete(k)))),self.clients.claim()])));
self.addEventListener("fetch",e=>{
  if(e.request.method!=="GET")return;
  const u=new URL(e.request.url);
  if(u.origin!==location.origin)return;
  const isPage=e.request.mode==="navigate"||u.pathname.endsWith(".html")||u.pathname.endsWith("/");
  if(isPage){
    e.respondWith(fetch(e.request).then(r=>{const copy=r.clone();caches.open(CACHE).then(c=>c.put(e.request,copy));return r}).catch(()=>caches.match(e.request)));
  }else{
    e.respondWith(caches.match(e.request).then(cached=>cached||fetch(e.request).then(r=>{const copy=r.clone();caches.open(CACHE).then(c=>c.put(e.request,copy));return r})));
  }
});