const {chromium, webkit, devices} = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs/promises');
const root = 'https://simonrj.github.io/-summit-one-narrator/';
const registry = 'https://raw.githubusercontent.com/SimonRJ/-summit-one-narrator/refs/heads/lesson-intro-catalog/data/lesson-intros-live.json';
const teachingRevisions = {
  'T02.3':'variable-bars', 'T03.2':'signal-timetable',
  'T12.1':'angle-tracing', 'T12.2':'clock-arc-proof', 'T12.3':'construction-notebook',
  'T13.1':'moving-area', 'T13.2':'cut-and-scale', 'T13.3':'hidden-cubes',
};

async function publicJson(url) {
  const response = await fetch(url, {signal: AbortSignal.timeout(30000)});
  if (!response.ok) throw Error('Could not read '+url+' ('+response.status+')');
  return response.json();
}
async function course() {
  const [catalogue, teaching] = await Promise.all([publicJson(registry + '?v=' + Math.floor(Date.now() / 20000)),publicJson(root+'data/teaching-72.json')]);
  const films = [];
  for (let slot=1;slot<=6;slot++) {
    const id='S'+String(slot).padStart(3,'0');
    films.push({id,page:'watch-intro-'+id.toLowerCase()+'.html',asset:id+'-Intro.mp4'});
  }
  for (const row of catalogue.entries.filter(r=>r.status==='verified')) {
    const explicitlyRevised=(process.env.ILLUSTRATED || '').split(/\s+/).includes(row.id);
    const suffix=row.illustration===2 || row.illustration===1 && row.illustratedRevision===2 ? '-Illustrated-v2' : (row.illustration===1 || explicitlyRevised) ? '-Illustrated' : '';
    films.push({id:row.id,page:'watch-lesson-intro.html?slot='+Number(row.id.slice(1)),asset:row.id+'-Intro'+suffix+'.mp4'});
  }
  for (const {id,video_url} of teaching.items) {
    films.push({id,page:'watch-'+id.toLowerCase().replace('.','-')+'.html',asset:id+'.mp4',listed:video_url});
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
    const expectedPlayer = process.env.CHAPTER_PLAYER_SHA256;
    const playerResponse = expectedPlayer ? page.waitForResponse(response =>
      new URL(response.url()).pathname.endsWith('/lesson-introduction-watch.js'), {timeout: 45000}) : null;
    await page.goto(root+film.page,{waitUntil:'domcontentloaded',timeout:45000});
    if (playerResponse) {
      const response = await playerResponse;
      const digest = require('node:crypto').createHash('sha256').update(await response.body()).digest('hex');
      assert.equal(digest, expectedPlayer, 'The watch page loaded an earlier chapter player');
    }
    const video=page.locator('video');
    await video.waitFor({state:'visible',timeout:25000});
    await page.waitForFunction(()=>document.querySelector('video')?.readyState>=1,null,{timeout:45000});
    const source=await video.evaluate(v=>v.currentSrc);
    assert.equal(new URL(source).pathname.split('/').pop(),asset);
    if (teachingRevisions[id]) assert.ok(source.includes(teachingRevisions[id]),source);
    if (id==='S054') assert.match(source,/-Intro-Illustrated-v2\.mp4(?:[?#]|$)/);
    if ((process.env.ILLUSTRATED || '').split(/\s+/).includes(id)) assert.match(source,/-Intro-Illustrated(?:-v2)?\.mp4(?:[?#]|$)/);
    // Opening a lesson and replaying it from a completed session share this live resolver.
    // The dedicated player and the app must select the exact same edition.
    let courseSource;
    if (id.startsWith('S')) {
      courseSource=await page.evaluate(async id=>{
        const api=await import('./lesson-introduction-media.js?v=lesson-intros-v16');
        await api.loadIntroductionCatalogue();
        const selected=api.lessonIntroId(Number(id.slice(1)));
        if (selected!==id) throw Error('Lesson missing from the app catalogue: '+id);
        return new URL(api.introMediaSource(selected).movie,location.href).href;
      },id);
    } else {
      courseSource=film.listed ? new URL(film.listed,root).href : source;
    }
    assert.equal(courseSource,source);
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
    await fs.writeFile(file+'.json',JSON.stringify({id,engine,orientation,method,target,page:root+film.page,courseSource,...result},null,2));
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
