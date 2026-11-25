"""Finish only the remaining consumer replay after the bounded full route run."""
import asyncio, importlib.util, json, os, sys
from pathlib import Path
from urllib.parse import urljoin
from aiohttp import web
from playwright.async_api import async_playwright

ROOT=Path('/workspace/scratch/2fdd119b5e17/amc-priority-release')
OUTPUT=Path('/workspace/scratch/2fdd119b5e17/s020-consumer-replay-completion')
sys.path.insert(0,str(ROOT/'tools'))
spec=importlib.util.spec_from_file_location('check_routes',ROOT/'tools/check_lesson_film_routes.py')
check=importlib.util.module_from_spec(spec);spec.loader.exec_module(check)

async def main():
 OUTPUT.mkdir(exist_ok=True)
 guide=json.loads((ROOT/'data/recorded-studies.json').read_text())['lessons']['S020']
 assert guide['sha256']=='5308674d7d66dee6545d05699311a192b13e2fce2d48b6d2f560ec35ce1e57f3'
 async def serve(request):
  target=(ROOT/(request.match_info['path'] or 'index.html')).resolve()
  if ROOT not in target.parents or not target.is_file():raise web.HTTPNotFound()
  return web.FileResponse(target)
 app=web.Application();app.router.add_get('/{path:.*}',serve)
 runner=web.AppRunner(app);await runner.setup();server=web.TCPSite(runner,'127.0.0.1',0);await server.start()
 site=f'http://127.0.0.1:{server._server.sockets[0].getsockname()[1]}/'
 movie=urljoin(site,guide['release']+'S020.mp4');poster=urljoin(site,guide['release']+'S020-poster.jpg')
 result={'slot':283,'profile':'ipad-portrait','engine':'webkit','site':site,'film':movie,'sha256':guide['sha256'],'scope':'Remaining completed-notebook replay only. Public MP4 hash, gallery, active lesson and practice already completed in the preserved bounded run.'}
 try:
  async with async_playwright() as pw:
   launch={'executable_path':'/tmp/amc-intros/device/webkit.sh'}
   if os.environ.get('HTTPS_PROXY'):launch['proxy']={'server':os.environ['HTTPS_PROXY'],'bypass':'localhost,127.0.0.1'}
   browser=await pw.webkit.launch(**launch)
   device=dict(pw.devices['iPad (gen 7)']);device.pop('default_browser_type')
   context=await browser.new_context(**device,service_workers='block',ignore_https_errors=bool(os.environ.get('HTTPS_PROXY')))
   context.set_default_navigation_timeout(60000)
   fixture=check.MOCK.replace("correct:true,independent_credit:","correct:body.answer_text!=='fixture-miss',independent_credit:")
   assert fixture!=check.MOCK
   await context.route('**/supabase-client.js*',lambda r:r.fulfill(body=fixture,content_type='application/javascript'))
   await context.route('https://*.supabase.co/**',lambda r:r.abort())
   await context.add_init_script("""window.fixture={records:[{session_number:283,immutable:true,completed_at:'2026-01-01T00:00:00Z',answers:{},evidence:{},working:{},summary:{}}],attempts:[],exams:[],writes:[],fail:false,progress:{completed_sessions:283,current_session:284,xp:0,rank:0,state:{}}};""")
   page=await context.new_page()
   try:
    print('Load completed notebook',flush=True)
    await page.goto(site+'?fixtureSlot=283&view=review',wait_until='domcontentloaded')
    row=page.locator('[data-review-session="283"]')
    await row.locator(':scope > summary').click()
    before=await page.evaluate('JSON.stringify([fixture.records,fixture.progress,fixture.writes])')
    await row.locator('button[data-video-session="283"]').click()
    player=page.locator('#replayIntroVideo')
    print('Check exact public media metadata',flush=True)
    await check.verify_media(page,player,movie,guide['seconds'])
    assert await player.evaluate('v=>v.poster')==poster
    result['notebook_frame_css_pixels']=await check.full_frame(player)
    print('Check advancing replay',flush=True)
    await check.play_inline(page,player)
    assert await page.evaluate('JSON.stringify([fixture.records,fixture.progress,fixture.writes])')==before
    result.update(immutable_replay=True,practice_grading='isolated fixture',video=await player.evaluate('v=>({source:v.currentSrc,time:v.currentTime,ready:v.readyState,paused:v.paused,error:v.error?.code||null})'),passed=True)
    await page.screenshot(path=OUTPUT/'replay.png')
    print('PASS completed replay',flush=True)
   except Exception as error:
    result['failure']={'type':type(error).__name__,'message':str(error)}
    try:result['video']=await asyncio.wait_for(page.locator('video').evaluate_all('list=>list.map(v=>({source:v.currentSrc,time:v.currentTime,ready:v.readyState,error:v.error?.code||null}))'),5)
    except Exception:pass
    raise
   finally:
    (OUTPUT/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    await asyncio.wait_for(browser.close(),15)
 finally:await runner.cleanup()

asyncio.run(asyncio.wait_for(main(),150))
