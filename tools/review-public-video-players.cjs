const {chromium, webkit, devices} = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs/promises');
const root = 'https://simonrj.github.io/-summit-one-narrator/';
async function check(context,id,orientation,engine) {
  const page=await context.newPage();
  try {
    const intro=id.startsWith('S');
    const url=root+(intro?'watch-lesson-intro.html?slot='+Number(id.slice(1)):'watch-t02-3.html');
    await page.goto(url,{waitUntil:'domcontentloaded',timeout:60000});
    const video=page.locator('video');
    await video.waitFor({state:'visible',timeout:30000});
    await page.waitForFunction(()=>document.querySelector('video')?.readyState>=1,null,{timeout:60000});
    const source=await video.evaluate(v=>v.currentSrc);
    assert.ok(source.includes(intro?id+'-Intro-Illustrated.mp4':'T02.3.mp4?v=variable-bars'),source);
    await video.evaluate(v=>{v.muted=true;return v.play()});
    await page.waitForFunction(()=>document.querySelector('video').currentTime>.15);
    const chapter=page.locator('[data-time]').nth(intro?4:3);
    await chapter.waitFor({timeout:20000});
    const target=Number(await chapter.getAttribute('data-time'));
    await chapter.click();
    await page.waitForFunction(t=>{const v=document.querySelector('video');return v.readyState>=2&&Math.abs(v.currentTime-t)<2},target,{timeout:30000});
    await page.waitForTimeout(280);
    const result=await video.evaluate(v=>({time:v.currentTime,seconds:v.duration,width:v.videoWidth,height:v.videoHeight,
      visibleWidth:v.getBoundingClientRect().width,source:v.currentSrc,error:v.error?.code||0,overflow:document.documentElement.scrollWidth>innerWidth+1}));
    assert.equal(result.width,1920);assert.equal(result.height,1080);assert.equal(result.error,0);assert.equal(result.overflow,false);
    const file='build/phone/'+id+'-'+engine+'-'+orientation;
    await video.screenshot({path:file+'.png',timeout:20000});
    await fs.writeFile(file+'.json',JSON.stringify({id,engine,orientation,target,...result},null,2));
    console.log(id,engine,orientation,'playing',result.time,'chapter start',target);
  } finally {await page.close();}
}
(async()=>{
  const engine=process.env.ENGINE||'webkit';
  const browser=engine==='webkit'?await webkit.launch():await chromium.launch({channel:'chrome'});
  let failed=false;
  try {
    await fs.mkdir('build/phone',{recursive:true});
    for(const [orientation,width,height] of [['portrait',390,844],['landscape',844,390]]) {
      const context=await browser.newContext({...devices['iPhone 13'],defaultBrowserType:undefined,viewport:{width,height},screen:{width,height},deviceScaleFactor:2});
      for(const id of process.argv.slice(2)){
        try{await check(context,id,orientation,engine);}
        catch(err){console.error(id,engine,orientation,String(err));failed=true;}
      }
      await context.close();
    }
  } finally {await browser.close();}
  if(failed)process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1});
