const {chromium, webkit, devices} = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs/promises');
const root = 'https://simonrj.github.io/-summit-one-narrator/';
const registry = 'https://raw.githubusercontent.com/SimonRJ/-summit-one-narrator/refs/heads/lesson-intro-catalog/data/lesson-intros-live.json';

async function publicJson(url) {
  const response = await fetch(url, {signal: AbortSignal.timeout(30000)});
  if (!response.ok) throw Error('Could not read '+url+' ('+response.status+')');
  return response.json();
}
async function course() {
  const [catalogue, teaching] = await Promise.all([publicJson(registry+'?review='+Date.now()),publicJson(root+'data/teaching-72.json')]);
  const films = [];
  for (let slot=1;slot<=6;slot++) {
    const id='S'+String(slot).padStart(3,'0');
    films.push({id,page:'watch-intro-'+id.toLowerCase()+'.html',asset:id+'-Intro.mp4'});
  }
  for (const row of catalogue.entries.filter(r=>r.status==='verified')) {
    const suffix=row.illustration===2 || row.illustration===1 && row.illustratedRevision===2 ? '-Illustrated-v2' : row.illustration===1 ? '-Illustrated' : '';
    films.push({id:row.id,page:'watch-lesson-intro.html?slot='+Number(row.id.slice(1)),asset:row.id+'-Intro'+suffix+'.mp4'});
  }
  for (const {id} of teaching.items) {
    films.push({id,page:'watch-'+id.toLowerCase().replace('.','-')+'.html',asset:id+'.mp4'});
  }
  assert.equal(new Set(films.map(f=>f.id)).size,films.length);
  return films;
}
async function check(context,film,orientation,engine) {
  const {id,asset}=film;
  const page=await context.newPage();
  try {
    await page.addInitScript(()=>{
      window.__chapterEvents=[];
      for(const type of ['click','seeking','seeked','canplay','play','pause']) {
        document.addEventListener(type,e=>{
          const v=document.querySelector('video');
          if(v)window.__chapterEvents.push([type,e.target.tagName,e.target.dataset?.time,v.currentTime,v.readyState,[...Array(v.seekable.length)].map((_,i)=>[v.seekable.start(i),v.seekable.end(i)])]);
        },true);
      }
    });
    await page.goto(root+film.page,{waitUntil:'domcontentloaded',timeout:45000});
    const video=page.locator('video');
    await video.waitFor({state:'visible',timeout:25000});
    await page.waitForFunction(()=>document.querySelector('video')?.readyState>=1,null,{timeout:45000});
    const source=await video.evaluate(v=>v.currentSrc);
    assert.equal(new URL(source).pathname.split('/').pop(),asset);
    if (id==='T02.3') assert.match(source,/variable-bars/);
    if (id==='T13.1') assert.match(source,/moving-area/);
    if (id==='T13.2') assert.match(source,/cut-and-scale/);
    if (id==='T12.3') assert.match(source,/construction-notebook/);
    if (id==='T12.1') assert.match(source,/angle-tracing/);
    if ((process.env.ILLUSTRATED || '').split(/\s+/).includes(id)) assert.match(source,/-Intro-Illustrated(?:-v2)?\.mp4(?:[?#]|$)/);
    await video.evaluate(v=>{v.muted=true;return v.play()});
    await page.waitForFunction(()=>document.querySelector('video').currentTime>.15,null,{timeout:20000});
    let target,method;
    if (id==='T02.1') {
      // This approved film uses native controls and has no chapter buttons.
      target=await video.evaluate(v=>{const t=v.duration*.53;v.currentTime=t;return t});
      method='native seek';
    } else {
      const chapters=page.locator('[data-time]');
      await chapters.first().waitFor({timeout:18000});
      const chapter=chapters.nth(Math.min(id.startsWith('S')?4:3,await chapters.count()-1));
      target=Number(await chapter.getAttribute('data-time'));
      assert.ok(target>0);
      await chapter.tap();method='chapter button';
    }
    await page.waitForFunction(t=>{const v=document.querySelector('video');return !v.seeking&&v.readyState>=2&&Math.abs(v.currentTime-t)<2},target,{timeout:25000});
    const afterSeek=await video.evaluate(v=>v.currentTime);
    await page.waitForFunction(([t,after])=>{const v=document.querySelector('video');return v.currentTime>Math.max(t+.75,after+.12)&&v.currentTime<t+4},[target,afterSeek],{timeout:15000});
    const result=await video.evaluate(v=>({time:v.currentTime,seconds:v.duration,width:v.videoWidth,height:v.videoHeight,visibleWidth:v.getBoundingClientRect().width,source:v.currentSrc,error:v.error?.code||0,overflow:document.documentElement.scrollWidth>innerWidth+1}));
    assert.equal(result.width,1920);assert.equal(result.height,1080);assert.equal(result.error,0);assert.equal(result.overflow,false);
    if (orientation==='landscape'&&['T13.1','T13.2','T16.E','T17.2'].includes(id)) {
      assert.ok(await video.evaluate(v=>v.getBoundingClientRect().height<=innerHeight));
    }
    const file='build/phone/'+id+'-'+engine+'-'+orientation;
    await video.screenshot({path:file+'.png',timeout:15000});
    await fs.writeFile(file+'.json',JSON.stringify({id,engine,orientation,method,target,page:root+film.page,...result},null,2));
    console.log(id,engine,orientation,method,result.time.toFixed(2));
  } catch(error) {
    const state=await page.locator('video').evaluate(v=>({time:v.currentTime,seeking:v.seeking,paused:v.paused,ready:v.readyState,network:v.networkState,events:window.__chapterEvents?.slice(-15),seekable:[...Array(v.seekable.length)].map((_,i)=>[v.seekable.start(i),v.seekable.end(i)]),buffered:[...Array(v.buffered.length)].map((_,i)=>[v.buffered.start(i),v.buffered.end(i)]),pageWidth:innerWidth,visible:v.getBoundingClientRect().toJSON(),error:v.error?.message})).catch(()=>({}));
    throw Error(String(error)+' '+JSON.stringify(state));
  } finally {await page.close();}
}
(async()=>{
  const args=process.argv.slice(2);
  const all=await course();
  const requested=new Set(args);
  let films;
  if (args[0]==='--shard') {
    const shard=Number(args[1]),total=Number(args[2]);
    assert.ok(Number.isInteger(shard)&&shard>=0&&shard<total);
    films=all.filter((_,i)=>i%total===shard);
  } else {
    films=all.filter(f=>requested.has(f.id));
    assert.equal(films.length,requested.size);
  }
  const engine=process.env.ENGINE||'webkit';
  const browser=engine==='webkit'?await webkit.launch():await chromium.launch({channel:'chrome'});
  let failed=false;
  try {
    await fs.mkdir('build/phone',{recursive:true});
    for(const [orientation,width,height] of [['portrait',390,844],['landscape',844,390]]) {
      const context=await browser.newContext({...devices['iPhone 13'],defaultBrowserType:undefined,viewport:{width,height},screen:{width,height},deviceScaleFactor:2});
      for(const film of films) {
        try{await check(context,film,orientation,engine);}
        catch(first){
          console.error(film.id,engine,orientation,'retry:',String(first));
          try{await check(context,film,orientation,engine);}
          catch(err){
            failed=true;
            await fs.writeFile('build/phone/'+film.id+'-'+engine+'-'+orientation+'-failure.json',JSON.stringify({id:film.id,engine,orientation,page:root+film.page,error:String(err)}));
          }
        }
      }
      await context.close();
    }
  } finally {await browser.close();}
  if(failed)process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1});
