"""Check the returned T18.1 container and watch page; no learner backend or publication.

Use the existing Playwright installation. Optional executable arguments support a
pinned local browser runtime; otherwise Playwright's installed browsers are used.
"""
import argparse
import asyncio
import hashlib
import json
import os
from pathlib import Path

from aiohttp import web
from playwright.async_api import async_playwright


async def check(args):
    root = args.root.resolve()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    movie = root / "media/T18.1.mp4"
    digest = hashlib.sha256(movie.read_bytes()).hexdigest()
    assert digest == "3527d02410e4b1158af7d42a5d8abce16cb6fed702947b8fa864af25590635ce"
    qa = json.loads((root / "review/T18.1-studio-qa.json").read_text())
    assert digest == qa["sha256"]

    async def serve(request):
        relative = request.match_info["path"] or "index.html"
        target = (root / relative).resolve()
        if root not in target.parents or not target.is_file():
            raise web.HTTPNotFound()
        return web.FileResponse(target)

    app = web.Application()
    app.router.add_get("/{path:.*}", serve)
    runner = web.AppRunner(app)
    await runner.setup()
    server = web.TCPSite(runner, "127.0.0.1", 0)
    await server.start()
    site = f"http://127.0.0.1:{server._server.sockets[0].getsockname()[1]}/"
    results = []
    try:
        async with async_playwright() as pw:
            for profile in args.profiles:
                print("Checking", profile, flush=True)
                engine = "chromium" if profile == "pc" else "webkit"
                launch = {}
                executable = args.chromium if engine == "chromium" else args.webkit
                if executable:
                    launch["executable_path"] = executable
                if engine == "chromium" and args.chromium_args:
                    launch["args"] = json.loads(args.chromium_args)
                if os.environ.get("HTTPS_PROXY"):
                    launch["proxy"] = {"server": os.environ["HTTPS_PROXY"], "bypass": "localhost,127.0.0.1"}
                browser = await getattr(pw, engine).launch(**launch)
                print("Launched", profile, flush=True)
                if profile == "pc":
                    device = {"viewport": {"width": 1440, "height": 900}}
                else:
                    device = dict(pw.devices["iPhone 13" if profile.startswith("iphone") else "iPad (gen 7)"])
                    device.pop("default_browser_type")
                    if profile.endswith("landscape"):
                        for key in ("viewport", "screen"):
                            if key in device:
                                size = device[key]
                                device[key] = {"width": size["height"], "height": size["width"]}
                context = await browser.new_context(**device, service_workers="block",
                                                    ignore_https_errors=bool(os.environ.get("HTTPS_PROXY")))
                await context.route("https://*.supabase.co/**", lambda route: route.abort())
                page = await context.new_page()
                errors = []
                page.on("pageerror", lambda error: errors.append(str(error)))
                result = {"profile": profile, "engine": engine, "browser_version": browser.version,
                          "viewport": device["viewport"], "movie_sha256": digest, "chapters": []}
                try:
                    await page.goto(site + "watch-t18-1.html", wait_until="domcontentloaded")
                    print("Loaded", profile, flush=True)
                    player = page.locator("video")
                    # Start through the actual chapter control. Mobile browsers
                    # may defer metadata until the visible player is requested.
                    await page.locator('button[data-time]').first.click()
                    await asyncio.wait_for(page.wait_for_function(
                        "document.querySelector('video').readyState >= 1", timeout=30000), 35)
                    result["metadata"] = await player.evaluate("v => ({width:v.videoWidth,height:v.videoHeight,duration:v.duration,controls:v.controls,inline:v.playsInline,source:new URL(v.currentSrc).pathname+new URL(v.currentSrc).search})")
                    assert result["metadata"]["source"] == "/media/T18.1.mp4?v=thirteen-search"
                    assert [result["metadata"][key] for key in ("width", "height")] == [1920, 1080]
                    assert abs(result["metadata"]["duration"] - qa["duration_seconds"]) < .01
                    await player.evaluate("""v => {
                      window.__frame = {count:0, mediaTime:-1};
                      function frame(now, metadata) {
                        window.__frame = {count:window.__frame.count+1, mediaTime:metadata.mediaTime};
                        v.requestVideoFrameCallback(frame);
                      }
                      v.requestVideoFrameCallback(frame);
                    }""")
                    buttons = page.locator("button[data-time]")
                    assert await buttons.count() == 8
                    for index, chapter in enumerate(qa["chapters"]):
                        button = buttons.nth(index)
                        target = float(await button.get_attribute("data-time"))
                        assert abs(target - chapter["start"]) < .001
                        before = await page.evaluate("window.__frame.count")
                        await button.click()
                        await page.wait_for_function("""([target, before]) => {
                          const v=document.querySelector('video'), f=window.__frame;
                          return !v.error && !v.paused && !v.seeking && v.readyState>=2 &&
                            f.count>before && f.mediaTime>=target+.2 && f.mediaTime<target+3 &&
                            v.currentTime>=target+.2 && v.currentTime<target+3;
                        }""", arg=[target, before], timeout=30000)
                        result["chapters"].append(await player.evaluate("v => ({time:v.currentTime,decoded:window.__frame.mediaTime,paused:v.paused,seeking:v.seeking,error:v.error?.code||null})"))
                    print("Decoded all eight chapters", profile, flush=True)
                    # Use the learner's existing chapter control for this check too.
                    # The WebKit trace completed every chapter, then hung awaiting
                    # a programmatic play() promise after a paused caption seek.
                    # Play from the preceding chapter into the same strict decoded
                    # caption interval instead; no player behavior is changed.
                    correction_chapter = max(index for index, chapter in enumerate(qa["chapters"])
                                             if chapter["start"] <= 79.6)
                    before = await page.evaluate("window.__frame.count")
                    await buttons.nth(correction_chapter).click()
                    await page.wait_for_function("before => window.__frame.count>before && window.__frame.mediaTime>=79.9 && window.__frame.mediaTime<80.5", arg=before, timeout=30000)
                    await player.evaluate("v => v.pause()")
                    result["correction_frame_seconds"] = await page.evaluate("window.__frame.mediaTime")
                    result["video_bounds"] = await player.bounding_box()
                    rect, viewport = result["video_bounds"], device["viewport"]
                    assert rect["x"] >= -1 and rect["y"] >= -1
                    assert rect["x"] + rect["width"] <= viewport["width"] + 1
                    assert rect["y"] + rect["height"] <= viewport["height"] + 1
                    result["theme"] = await page.evaluate("({scheme:getComputedStyle(document.documentElement).colorScheme,background:getComputedStyle(document.body).backgroundColor,text:getComputedStyle(document.body).color})")
                    print("Decoded all chapters and caption", profile, flush=True)
                    await page.screenshot(path=output / f"{profile}.png", timeout=15000)
                    await page.get_by_text("Read the transcript", exact=True).click()
                    assert "Their perimeters are fifty, twenty-eight, twenty-two and twenty." in await page.locator("details.transcript").inner_text()
                    await page.get_by_text("See the worked answer", exact=True).click()
                    assert "only 14 is divisible by 7" in await page.locator(".companion-variation details").inner_text()
                    assert not errors, errors
                    result.update(transcript_opens=True, variation_opens=True, page_errors=errors, passed=True)
                    results.append(result)
                    (output / "device-results.json").write_text(json.dumps(results, indent=2) + "\n")
                    print("PASS", profile, "8 decoded chapter starts and corrected caption frame", flush=True)
                finally:
                    print("Closing", profile, flush=True)
                    await asyncio.wait_for(context.close(), timeout=15)
                    await asyncio.wait_for(browser.close(), timeout=15)
    finally:
        await runner.cleanup()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--chromium")
    parser.add_argument("--chromium-args")
    parser.add_argument("--webkit")
    parser.add_argument("--profiles", nargs="+", default=["pc", "iphone-portrait", "iphone-landscape", "ipad-portrait", "ipad-landscape"])
    asyncio.run(check(parser.parse_args()))
