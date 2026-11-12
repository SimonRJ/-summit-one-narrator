import {chromium} from 'playwright';
import fs from 'node:fs';import path from 'node:path';import http from 'node:http';import assert from 'node:assert/strict';
const root=process.cwd();fs.mkdirSync('qa-screenshots',{recursive:true});
const mime={'.js':'application/javascript','.css':'text/css','.json':'application/json','.mp4':'video/mp4','.jpg':'image/jpeg','.html':'text/html','.svg':'image/svg+xml'};
const server=http.createServer((req,res)=>{
 const url=new URL(req.url,'http://localhost');const file=path.resolve(root,'.'+(url.pathname==='/'?'/index.html':url.pathname));
 if(!file.startsWith(root+path.sep)){res.writeHead(403);res.end();return}
 try{
  const size=fs.statSync(file).size;res.setHeader('Content-Type',mime[path.extname(file)]||'text/plain');res.setHeader('Accept-Ranges','bytes');
  const m=/bytes=(\d+)-(\d*)/.exec(req.headers.range||'');const start=m?Number(m[1]):0,end=m&&m[2]?Math.min(Number(m[2]),size-1):size-1;
  if(m){res.writeHead(206,{'Content-Range':`bytes ${start}-${end}/${size}`,'Content-Length':end-start+1})}else res.setHeader('Content-Length',size);
  fs.createReadStream(file,{start,end}).pipe(res);
 }catch{res.writeHead(404);res.end()}
});await new Promise(r=>server.listen(4181,'127.0.0.1',r));
const browser=await chromium.launch({headless:true});
const sdk=`export function createClient(){return {auth:{getUser:async()=>({data:{user:sessionStorage.getItem('welcome-fixture')?{id:'fixture'}:null}}),signInWithPassword:async()=>{sessionStorage.setItem('welcome-fixture','1');return {error:null}}}}}`;
try{
 for(const mobile of [false,true]){
  const context=await browser.newContext({viewport:mobile?{width:390,height:844}:{width:1440,height:1000},serviceWorkers:'block'}),page=await context.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.route('https://esm.sh/**',r=>r.fulfill({contentType:'application/javascript',body:sdk}));
  await page.route('http://127.0.0.1:4181/',r=>r.fulfill({contentType:'text/html',body:'<h1>Learning destination fixture</h1>'}));
  await page.route('**/tests.html?**',r=>r.fulfill({contentType:'text/html',body:'<h1>Exam destination fixture</h1>'}));
  let videoRequests=0;page.on('request',r=>{if(r.url().includes('AMCIntroduction.mp4'))videoRequests++});
  await page.goto('http://127.0.0.1:4181/welcome.html');await page.locator('#watchWelcome').waitFor();
  assert.equal(await page.locator('#welcomeVideo').evaluate(v=>v.paused),true);assert(!/\breef\b/i.test(await page.locator('body').innerText()),'Introduction must not use a learner name');assert((await page.locator('video').getAttribute('src')).includes('AMCIntroduction.mp4'));await page.getByText('Read the introduction',{exact:true}).click();assert((await page.locator('.transcript').innerText()).includes('sixty minutes'));await page.getByText('Read the introduction',{exact:true}).click();assert.equal(videoRequests,0,'Welcome must not auto-download the video');
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+2),false);
  await page.screenshot({path:`qa-screenshots/${mobile?'mobile':'desktop'}-amc-introduction.png`,fullPage:true});
  await page.locator('#watchWelcome').click();await page.waitForFunction(()=>document.querySelector('video').currentTime>.5);assert.equal(await page.locator('video').evaluate(v=>v.videoWidth),1920);
  await page.locator('#watchWelcome').click();assert.equal(await page.locator('video').evaluate(v=>v.paused),true);
  await page.screenshot({path:`qa-screenshots/${mobile?'mobile':'desktop'}-amc-introduction-playing.png`,fullPage:true});
  await page.locator('#watchWelcome').click();await page.waitForFunction(()=>!document.querySelector('video').paused);
  await page.locator('video').evaluate(v=>v.currentTime=v.duration-.3);await page.waitForFunction(()=>document.querySelector('video').ended);
  assert.equal(await page.locator('#skipWelcome').innerText(),'Start my next step');assert.equal(await page.locator('#watchWelcome').innerText(),'Watch again');
  await page.locator('#watchWelcome').click();await page.waitForFunction(()=>document.querySelector('video').currentTime<5&&!document.querySelector('video').paused);
  await page.locator('#skipWelcome').click();await page.waitForURL('http://127.0.0.1:4181/');
  // Real login module with an isolated SDK stub; no learner credentials or records.
  await page.goto('http://127.0.0.1:4181/login.html');await page.locator('#loginName').fill('fixture');await page.locator('#password').fill('fixture-only');await page.locator('#signIn').click();await page.waitForURL('**/welcome.html?from=login');
  await page.locator('#skipWelcome').click();await page.waitForURL('http://127.0.0.1:4181/');
  await page.goto('http://127.0.0.1:4181/login.html');await page.waitForURL('http://127.0.0.1:4181/');
  await page.evaluate(()=>sessionStorage.clear());await page.goto('http://127.0.0.1:4181/login.html?next=tests.html%3Fsection%3Drossmoyne');await page.locator('#loginName').fill('fixture');await page.locator('#password').fill('fixture-only');await page.locator('#signIn').click();await page.waitForURL('**/tests.html?section=rossmoyne');
  await page.goto('http://127.0.0.1:4181/welcome.html?from=dashboard');assert.equal(await page.locator('#skipWelcome').innerText(),'Back to my learning');
  const broken=await browser.newContext({viewport:mobile?{width:390,height:844}:{width:1440,height:1000},serviceWorkers:'block'}),bp=await broken.newPage();
  await bp.route('**/media/AMCIntroduction.mp4*',r=>r.abort());await bp.route('http://127.0.0.1:4181/',r=>r.fulfill({contentType:'text/html',body:'<h1>Learning destination fixture</h1>'}));
  await bp.goto('http://127.0.0.1:4181/welcome.html');await bp.locator('#watchWelcome').click();await bp.waitForFunction(()=>document.querySelector('#welcomeStatus').classList.contains('error'));assert(await bp.locator('#watchWelcome').isEnabled());await bp.locator('#skipWelcome').click();await bp.waitForURL('http://127.0.0.1:4181/');await broken.close();
  assert.deepEqual(errors,[]);await context.close();
 }
 console.log('PASS: desktop/mobile welcome, no autoplay/download, real video decode/play/pause/replay, new login, existing session, exam return, optional skip, error fallback, no overflow or learner data writes.');
}finally{await browser.close();server.close()}
