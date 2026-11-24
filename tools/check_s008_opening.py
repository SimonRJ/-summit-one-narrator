import asyncio, json, os
from pathlib import Path
from playwright.async_api import async_playwright, expect
from browser_lesson_fixed import MOCK
from check_lesson_film_routes import fits,full_frame,PROFILES

async def run():
    profile=os.environ['PROFILE']
    async with async_playwright() as pw:
        name,rotate=PROFILES[profile]; device=dict(pw.devices[name]);engine=device.pop('default_browser_type')
        if profile=='pc':device['viewport']={'width':1440,'height':900}
        if rotate:device['viewport']={'width':device['viewport']['height'],'height':device['viewport']['width']}
        browser=await (pw.webkit.launch() if engine=='webkit' else pw.chromium.launch(channel='chrome'))
        ctx=await browser.new_context(**device,service_workers='block')
        await ctx.route('**/supabase-client.js*',lambda r:r.fulfill(body=MOCK,content_type='application/javascript'))
        await ctx.add_init_script("window.fixture={records:[],attempts:[],exams:[],writes:[],fail:false,progress:{completed_sessions:7,current_session:8,xp:0,rank:0,state:{}}}")
        page=await ctx.new_page();await page.goto('http://127.0.0.1:8765/',wait_until='domcontentloaded')
        await page.locator('#continue').click();cue=page.locator('.rwl-bridge');await expect(cue).to_contain_text('printing press',timeout=20000)
        await page.locator('.rwl-opening-figure').evaluate('v=>v.decode()')
        stage=page.locator('.lesson-screen-stage')
        geom=await stage.evaluate("s=>({stage:s.clientHeight,content:s.scrollHeight,scrollable:getComputedStyle(s).overflowY})")
        print(profile, geom,flush=True)
        await fits(page)
        if profile.startswith('ipad') or profile=='pc':
            print('Default cue:',await full_frame(cue),flush=True)
        else:
            await cue.scroll_into_view_if_needed()
            print('Phone cue:',await full_frame(cue),flush=True)
            await stage.evaluate('s=>s.scrollTo(0,0)')
        output=Path('build/opening');output.mkdir(parents=True,exist_ok=True)
        await page.screenshot(path=output/'collapsed.png')
        await page.locator('.rwl-full-example>summary').click()
        await expect(page.locator('.rwl-full-example ol li')).to_have_count(2)
        await expect(page.locator('.rwl-full-example ol')).to_be_visible()
        await fits(page)
        await page.locator('.rwl-full-example>summary').click()
        await page.locator('.fv-open').first.click()
        await expect(page.locator('dialog.figure-viewer')).to_be_visible()
        await page.locator('dialog.figure-viewer button').first.wait_for()
        await page.keyboard.press('Escape')
        await expect(page.locator('dialog.figure-viewer')).to_be_hidden()
        await browser.close()
asyncio.run(run())
