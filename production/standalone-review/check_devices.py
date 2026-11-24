"""Exercise each native film and each chapter through its real public player."""
import argparse
import asyncio
import hashlib
import json
from pathlib import Path
import sys
from urllib.request import urlopen

from playwright.async_api import async_playwright

sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools'))
from check_lesson_film_routes import PROFILES


async def validate(site, profile, out):
    out.mkdir(exist_ok=True,parents=True)
    sources=[('welcome.html','AMCIntroduction','AMCIntroduction-qa.json',18),
             ('watch-amc-2025-q17.html','AMC2025Q17-voice-c','AMC2025Q17-edition.json',6)]
    results=[]
    async with async_playwright() as pw:
        name,landscape=PROFILES[profile]
        device=dict(pw.devices[name]);engine=device.pop('default_browser_type')
        if profile=='pc':
            device['viewport']={'width':1440,'height':900};device['screen']=dict(device['viewport'])
        if landscape:
            for key in ('viewport','screen'):
                if key in device:
                    rect=device[key];device[key]={'width':rect['height'],'height':rect['width']}
        browser=await (pw.webkit.launch() if engine=='webkit' else pw.chromium.launch(channel='chrome'))
        context=await browser.new_context(**device,service_workers='block')
        try:
            for route,film,report,count in sources:
                with urlopen(site+'review/'+report) as response: qa=json.load(response)
                with urlopen(site+'media/'+film+'.mp4') as response: assert hashlib.file_digest(response,'sha256').hexdigest()==qa['sha256']
                page=await context.new_page()
                await page.goto(site+route,wait_until='domcontentloaded')
                player=page.locator('video');buttons=page.locator('nav button[data-time]')
                assert await buttons.count()==count
                assert await page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
                assert await player.evaluate('v=>v.paused && v.currentTime===0')
                for index in range(count):
                    b=buttons.nth(index)
                    target=float(await b.get_attribute('data-time'))
                    assert abs(target-qa['chapters'][index]['start'])<.001
                    await b.click()
                    await page.wait_for_function("""t=>{const v=document.querySelector('video');
                      return !v.error && v.readyState>=2 && !v.paused && !v.seeking && v.currentTime>=t+.3 && v.currentTime<=t+4}""",
                      arg=target,timeout=25000)
                    assert await player.evaluate('v=>v.videoWidth===1920&&v.videoHeight===1080 && !v.muted')
                    if index==min(count-1,4): await player.screenshot(path=out/(film+'.png'))
                if film.startswith('AMC2025'):
                    # Exercise the captions toggle and the actual timestamped cue through WebKit/Chromium.
                    await player.evaluate("v=>{[...v.textTracks].find(track=>track.kind==='captions').mode='showing';v.currentTime=45;}")
                    await page.wait_for_function("()=>Array.from([...document.querySelector('video').textTracks].find(track=>track.kind==='captions')?.activeCues||[]).some(c=>c.text.includes('middle sums'))")
                    await page.get_by_text('Check your count',exact=True).click()
                    assert '2 × 2 = 4' in await page.locator('details[open]').inner_text()
                if profile=='iphone-portrait':
                    await buttons.first.click()
                    await page.wait_for_function("()=>document.querySelector('video').ended",timeout=int((qa['duration_seconds']+35)*1000))
                    assert await player.evaluate('v=>!v.error && !v.muted && v.playbackRate===1')
                results.append({'film':film,'sha256':qa['sha256'],'chapter_buttons_checked':count,'full_replay_to_end':profile=='iphone-portrait'})
                await page.close()
        finally:
            await browser.close()
    (out/'result.json').write_text(json.dumps({'profile':profile,'films':results},indent=2)+'\n')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('profile',choices=PROFILES);p.add_argument('--site',default='http://127.0.0.1:8765/')
    p.add_argument('--out',type=Path,default=Path('build/device'))
    args=p.parse_args();asyncio.run(validate(args.site.rstrip('/')+'/',args.profile,args.out))
