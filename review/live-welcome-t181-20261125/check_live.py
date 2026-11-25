"""Bounded public-route smoke check; run only after the Pages-success handoff.

Uses a new iPhone WebKit context for each public watch page. It does not visit
the signed-in app, replay an entire film, or change any learner record.
"""
import argparse
import asyncio
import datetime
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
from urllib.parse import urlparse

from playwright.async_api import async_playwright


SOURCE = "e287b9102574b8a6cbc29beba97ccc9a7dc569fe"
TREE = "de6b0b43b98bba31a2a6ec3cf633210c1c2b3bdf"
SITE = "https://simonrj.github.io/-summit-one-narrator/"
CASES = [
    dict(name="welcome", page="welcome.html", chapters=18,
         html_sha256="4ac46b6820394da64fafa7c483af688bc4418515e4dd8a28ebea7780409ac1a4",
         media="AMCIntroduction.mp4?v=course-films-target-clock-20261125",
         duration=260.533333, repaired_start=228.42, inspect_at=243.7,
         transcript_summary="Read the introduction", transcript=".transcript",
         expected_text="The clock counts up from zero."),
    dict(name="t181", page="watch-t18-1.html", chapters=8,
         html_sha256="98616e777d4b455d4d0ed793c43953ab010141ac1807e82085abbd9d6e96a88d",
         media="T18.1.mp4?v=thirteen-search", duration=117.433333,
         repaired_start=61.4, inspect_at=79.9,
         transcript_summary="Read the transcript", transcript="details.transcript",
         expected_text="Their perimeters are fifty, twenty-eight, twenty-two and twenty."),
]

FONT_CHECK = """async () => {
  const rows=[];
  for (const specification of [
    '400 18px "Source Sans 3"',
    '500 18px "Source Serif 4"',
    '500 18px "Source Code Pro"'
  ]) {
    const faces=await document.fonts.load(specification, 'Summit One 123');
    rows.push({specification, loaded:faces.length>0 && faces.every(f=>f.status==='loaded')});
  }
  await document.fonts.ready;
  return {faces:rows, body_family:getComputedStyle(document.body).fontFamily,
    heading_family:getComputedStyle(document.querySelector('h1')).fontFamily,
    overflow:document.documentElement.scrollWidth-innerWidth};
}"""

FRAME_TRACE = """() => {
  const video=document.querySelector('video');
  window.__smokeFrames={count:0,mediaTime:-1};
  window.__smokeEvents=[];
  window.__smokeState=()=>({time:video.currentTime,paused:video.paused,
    seeking:video.seeking,readyState:video.readyState,networkState:video.networkState,
    error:video.error?.code||null,frames:window.__smokeFrames,
    muted:video.muted,volume:video.volume,playbackRate:video.playbackRate,
    visibility:document.visibilityState});
  for(const type of ['play','playing','pause','seeking','seeked','waiting','stalled','error'])
    video.addEventListener(type,()=>window.__smokeEvents.push({type,...window.__smokeState()}));
  function frame(now,metadata){
    window.__smokeFrames={count:window.__smokeFrames.count+1,mediaTime:metadata.mediaTime};
    video.requestVideoFrameCallback(frame);
  }
  video.requestVideoFrameCallback(frame);
}"""


async def inspect_case(browser, pw, case, output):
    device = dict(pw.devices["iPhone 13"])
    device.pop("default_browser_type")
    context = await browser.new_context(
        **device, service_workers="block",
        ignore_https_errors=bool(os.environ.get("HTTPS_PROXY")))
    context.set_default_timeout(15000)
    context.set_default_navigation_timeout(45000)
    result = dict(name=case["name"], url=SITE+case["page"], viewport=device["viewport"],
                  page_errors=[], blocked_supabase=[], blocked_writes=[],
                  external_font_attempts=[], font_responses=[], failed_requests=[],
                  http_errors=[], chapters_checked=[], passed=False)

    async def guard(route):
        request = route.request
        host = (urlparse(request.url).hostname or "").lower()
        if host == "supabase.co" or host.endswith(".supabase.co") or host.endswith(".supabase.com"):
            result["blocked_supabase"].append(request.url)
            await route.abort()
        elif request.method not in ("GET", "HEAD"):
            result["blocked_writes"].append(dict(method=request.method, url=request.url))
            await route.abort()
        elif host in ("fonts.googleapis.com", "fonts.gstatic.com"):
            result["external_font_attempts"].append(request.url)
            await route.abort()
        else:
            await route.continue_()

    await context.route("**/*", guard)
    page = await asyncio.wait_for(context.new_page(),20)
    page.on("pageerror", lambda e: result["page_errors"].append(str(e)))
    page.on("requestfailed", lambda req: result["failed_requests"].append(
        dict(url=req.url, failure=req.failure)))

    def response_seen(response):
        if "/fonts/" in response.url:
            result["font_responses"].append(dict(url=response.url, status=response.status))
        if response.status >= 400:
            result["http_errors"].append(dict(url=response.url, status=response.status))
    page.on("response", response_seen)

    try:
        print("Opening live page",case["name"],flush=True)
        response = await page.goto(result["url"], wait_until="domcontentloaded")
        assert response and response.status == 200
        result["html_sha256"] = hashlib.sha256(await response.body()).hexdigest()
        assert result["html_sha256"] == case["html_sha256"], "Live page differs from frozen source"
        buttons = page.locator("button[data-time]")
        assert await buttons.count() == case["chapters"]
        result["font_faces_before_registration_wait"] = await page.evaluate(
            "Array.from(document.fonts).map(f=>({family:f.family,status:f.status}))")
        await page.wait_for_function("""() => {
          const families=Array.from(document.fonts,f=>f.family.replaceAll('"','').replaceAll("'",''));
          return ['Source Sans 3','Source Serif 4','Source Code Pro'].every(f=>families.includes(f));
        }""", timeout=20000)
        result["registered_font_face_count"] = await page.evaluate("document.fonts.size")
        result["fonts"] = await asyncio.wait_for(page.evaluate(FONT_CHECK), 30)
        assert all(face["loaded"] for face in result["fonts"]["faces"])
        assert result["fonts"]["overflow"] <= 2
        assert result["font_responses"] and all(r["status"] < 400 for r in result["font_responses"])
        assert not result["external_font_attempts"]
        await page.screenshot(path=output/f"{case['name']}-initial.png", timeout=15000)
        result["initial_storage"] = await page.evaluate(
            "({local:Object.keys(localStorage),session:Object.keys(sessionStorage)})")
        assert result["initial_storage"] == dict(local=[], session=[])
        result["initial_title"] = await page.title()
        result["initial_media_source"] = await page.locator("video").evaluate(
            "v=>v.currentSrc||v.src||v.querySelector('source')?.src")
        assert result["initial_media_source"] == SITE+"media/"+case["media"]
        (output/f"{case['name']}-initial.json").write_text(json.dumps(result,indent=2)+"\n")
        print(json.dumps(dict(name=case["name"],checkpoint="live DOM, source and fonts",
                              title=result["initial_title"],overflow=result["fonts"]["overflow"],
                              local_fonts_loaded=True)),flush=True)
        await page.evaluate(FRAME_TRACE)
        video = page.locator("video")

        for target in (0.0, case["repaired_start"]):
            # Select the real chapter by its existing exact numeric data-time.
            index = next(i for i, value in enumerate(await buttons.evaluate_all(
                "buttons=>buttons.map(b=>Number(b.dataset.time))")) if abs(value-target)<.001)
            button = buttons.nth(index)
            before = await page.evaluate("window.__smokeFrames.count")
            await button.click()
            await asyncio.wait_for(page.wait_for_function("""([target,before])=>{
              const v=document.querySelector('video'),f=window.__smokeFrames;
              return !v.error&&!v.paused&&!v.seeking&&v.readyState>=2&&f.count>before&&
                f.mediaTime>=target+.2&&f.mediaTime<target+4&&
                v.currentTime>=target+.2&&v.currentTime<target+4;
            }""", arg=[target,before], timeout=30000), 35)
            sample = await page.evaluate("window.__smokeState()")
            assert not sample["muted"] and sample["volume"] == 1 and sample["playbackRate"] == 1
            result["chapters_checked"].append(dict(target=target, label=await button.inner_text(), **sample))
            if target == 0:
                result["metadata"] = await video.evaluate(
                    "v=>({width:v.videoWidth,height:v.videoHeight,duration:v.duration,source:v.currentSrc,controls:v.controls,inline:v.playsInline})")
                assert result["metadata"]["source"] == SITE+"media/"+case["media"]
                assert [result["metadata"][k] for k in ("width","height")] == [1920,1080]
                assert abs(result["metadata"]["duration"]-case["duration"]) < .01

        await asyncio.wait_for(page.wait_for_function(
            "t=>window.__smokeFrames.mediaTime>=t&&window.__smokeFrames.mediaTime<t+1",
            arg=case["inspect_at"], timeout=25000), 30)
        await video.evaluate("v=>v.pause()")
        result["repaired_frame"] = await page.evaluate("window.__smokeState()")
        result["video_bounds"] = await video.bounding_box()
        rect = result["video_bounds"]
        assert rect["x"] >= -1 and rect["y"] >= -1
        assert rect["x"]+rect["width"] <= device["viewport"]["width"]+1
        assert rect["y"]+rect["height"] <= device["viewport"]["height"]+1
        await page.screenshot(path=output/f"{case['name']}-repaired-chapter.png", timeout=15000)
        await page.get_by_text(case["transcript_summary"], exact=True).click()
        assert case["expected_text"] in await page.locator(case["transcript"]).inner_text()
        result["transcript_opens"] = True
        result["final_overflow"] = await page.evaluate("document.documentElement.scrollWidth-innerWidth")
        assert result["final_overflow"] <= 2
        result["final_storage"] = await page.evaluate(
            "({local:Object.keys(localStorage),session:Object.keys(sessionStorage)})")
        assert result["final_storage"] == result["initial_storage"]
        assert not result["page_errors"]
        assert not result["blocked_writes"]
        assert not result["blocked_supabase"]
        assert not result["http_errors"]
        result["passed"] = True
    except Exception as error:
        result["failure"] = type(error).__name__+": "+str(error)
        try:
            result["failure_state"] = await asyncio.wait_for(page.evaluate(
                "window.__smokeState?window.__smokeState():null"), 5)
            await asyncio.wait_for(page.screenshot(path=output/f"{case['name']}-failure.png", timeout=5000), 7)
        except Exception:
            pass
    finally:
        try:
            result["media_events"] = await asyncio.wait_for(page.evaluate("window.__smokeEvents||[]"), 5)
        except Exception:
            pass
        (output/f"{case['name']}.json").write_text(json.dumps(result,indent=2)+"\n")
        await asyncio.wait_for(context.close(),15)
    print(json.dumps(dict(name=case["name"],passed=result["passed"],failure=result.get("failure"))),flush=True)
    return result


async def main(args):
    output=args.output.resolve()
    output.mkdir(parents=True,exist_ok=True)
    report=dict(source_commit=SOURCE,source_tree=TREE,pages_commit=args.pages_commit,
                pages_run=args.pages_run,profile="iPhone 13 portrait WebKit emulation",
                checked_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                playwright=importlib.metadata.version("playwright"),
                service_workers="blocked",fresh_context_per_page=True,
                supabase_blocked=True,non_read_requests_blocked=True,
                physical_device=False,human_listening=False,full_replay=False,
                final_editorial_acceptance=False,results=[])
    assert report["playwright"] == "1.58.0", "Use the existing 1.58 client with WebKit build 2248"
    (output/"result.json").write_text(json.dumps(report,indent=2)+"\n")
    async with async_playwright() as pw:
        launch=dict(executable_path=args.webkit)
        if os.environ.get("HTTPS_PROXY"):
            launch["proxy"]={"server":os.environ["HTTPS_PROXY"],"bypass":"localhost,127.0.0.1"}
        browser=await asyncio.wait_for(pw.webkit.launch(**launch),35)
        report["browser_version"]=browser.version
        try:
            for case in [case for case in CASES if case["name"] in args.cases]:
                try:
                    result=await asyncio.wait_for(inspect_case(browser,pw,case,output),120)
                except Exception as error:
                    result=dict(name=case["name"],passed=False,failure=type(error).__name__+": "+str(error))
                report["results"].append(result)
                (output/"result.json").write_text(json.dumps(report,indent=2)+"\n")
        finally:
            await asyncio.wait_for(browser.close(),15)
    report["passed"]=all(r["passed"] for r in report["results"]) and len(report["results"])==len(args.cases)
    (output/"result.json").write_text(json.dumps(report,indent=2)+"\n")
    if not report["passed"]:
        raise SystemExit(1)


if __name__=="__main__":
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--pages-commit",required=True)
    cli.add_argument("--pages-run",required=True,type=int)
    cli.add_argument("--webkit",default="/tmp/amc-intros/device/webkit.sh")
    cli.add_argument("--output",required=True,type=Path)
    cli.add_argument("--cases",nargs="+",choices=("welcome","t181"),default=["welcome","t181"])
    asyncio.run(main(cli.parse_args()))
