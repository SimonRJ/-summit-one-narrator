const CACHE="summit-one-course-v6";
const CORE=["./","./index.html","./app.css","./main.js","./course-engine.js","./supabase-client.js","./login.html","./login.js","./session.html","./session.js","./media-player.js","./exams.html","./exams.js","./exam.html","./exam.js","./exam-engine.js","./profile.html","./profile.js","./review.html","./review.js"];
self.addEventListener("install",e=>{self.skipWaiting();e.waitUntil(caches.open(CACHE).then(c=>c.addAll(CORE)))});
self.addEventListener("activate",e=>e.waitUntil(Promise.all([caches.keys().then(keys=>Promise.all(keys.filter(k=>k!==CACHE).map(k=>caches.delete(k)))),self.clients.claim()])));
self.addEventListener("fetch",e=>{
 if(e.request.method!=="GET"||new URL(e.request.url).origin!==location.origin)return;
 e.respondWith((async()=>{
   try{
     const fresh=await fetch(e.request);
     if(fresh.ok){const c=await caches.open(CACHE);c.put(e.request,fresh.clone())}
     return fresh;
   }catch{
     return (await caches.match(e.request))||new Response("Offline",{status:503});
   }
 })());
});
