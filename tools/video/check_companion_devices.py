"""Play a public companion film to completion and check its chapters on student devices."""

import argparse
import asyncio
import hashlib
import json
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import urlopen

from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[2]
PROFILES = [
    ("iPhone 13", False),
    ("iPhone 13", True),
    ("iPad (gen 7)", False),
    ("iPad (gen 7)", True),
    ("Desktop Chrome", False),
]


def reported_hash(url):
    with urlopen(url, timeout=90) as response:
        return hashlib.file_digest(response, "sha256").hexdigest()


async def check_device(
    browser, device, landscape, root, lesson, metadata, output, whole
):
    device = dict(device)
    device.pop("default_browser_type", None)
    if landscape:
        for name in ("viewport", "screen"):
            if name not in device:
                continue
            device[name] = {
                "width": device[name]["height"],
                "height": device[name]["width"],
            }
    context = await browser.new_context(**device, service_workers="block")
    page = await context.new_page()
    try:
        page_name = "watch-" + lesson.lower().replace(".", "-") + ".html"
        await page.goto(
            urljoin(root, "teaching-videos.html"), wait_until="domcontentloaded"
        )
        await page.locator(f'a[href^="{page_name}"]').first.click()
        movie = page.locator("video").first
        await movie.evaluate(
            'v => new Promise((ok,fail) => {if(v.readyState) ok(); else {v.addEventListener("loadedmetadata",ok,{once:true});v.addEventListener("error",fail,{once:true})}})'
        )
        actual = await movie.evaluate(
            "v => ({url:v.currentSrc,w:v.videoWidth,h:v.videoHeight,d:v.duration})"
        )
        assert (actual["w"], actual["h"]) == (
            metadata["width"],
            metadata["height"],
        ) and abs(actual["d"] - metadata["duration_seconds"]) < 0.21, actual
        assert actual["url"].split("?")[0].endswith("/" + lesson + ".mp4"), actual
        chapters = page.locator("button[data-time]")
        times = await chapters.evaluate_all("rows=>rows.map(b=>Number(b.dataset.time))")
        assert (
            len(times) > 1
            and times[0] == 0
            and all(a < b for a, b in zip(times, times[1:]))
        ), times
        for index, start in enumerate(times):
            await chapters.nth(index).click()
            await page.wait_for_function(
                't=>{const v=document.querySelector("video"); return !v.error&&!v.paused&&!v.seeking&&v.readyState>=2&&v.currentTime>t+.24&&v.currentTime<t+4}',
                arg=start,
                timeout=35000,
            )
        await movie.evaluate("v=>v.pause()")
        await movie.scroll_into_view_if_needed()
        frame = await movie.bounding_box()
        assert frame and frame["width"] > 100
        assert (
            frame["x"] >= -2
            and frame["x"] + frame["width"] <= device["viewport"]["width"] + 2
        )
        await movie.screenshot(path=output.with_suffix(".jpg"), type="jpeg", quality=78)
        details = page.locator("details.transcript").first
        await details.locator("summary").click()
        assert (await details.inner_text()).strip()
        if whole:
            assert (
                await asyncio.to_thread(reported_hash, actual["url"])
                == metadata["sha256"]
            )
            await chapters.first.click()
            await page.wait_for_function(
                '()=>{const v=document.querySelector("video");return v.currentTime<5&&!v.muted&&!v.paused&&v.volume>0&&v.playbackRate===1}',
                timeout=15000,
            )
            await page.wait_for_function(
                '()=>document.querySelector("video").ended',
                timeout=int((actual["d"] + 60) * 1000),
            )
        return dict(
            viewport=device["viewport"],
            video=actual,
            chapters=len(times),
            complete_playback=whole,
            ended=await movie.evaluate("v=>v.ended"),
        )
    finally:
        await context.close()


async def check(ids, site, output, landscape_only):
    output.mkdir(exist_ok=True, parents=True)
    errors = []
    async with async_playwright() as p:
        engines = {
            "webkit": await p.webkit.launch(),
            "chromium": await p.chromium.launch(channel="chrome"),
        }
        try:
            for lesson in ids:
                report = json.loads(
                    (ROOT / "review" / f"{lesson}-studio-qa.json").read_text()
                )
                result = {}

                async def profile(name, landscape):
                    key = name + ("-landscape" if landscape else "")
                    device = p.devices[name]
                    engine = device["default_browser_type"]
                    whole = name == "iPhone 13" and not landscape
                    try:
                        result[key] = await asyncio.wait_for(
                            check_device(
                                engines[engine],
                                device,
                                landscape,
                                site,
                                lesson,
                                report,
                                output
                                / (lesson + "-" + key.replace(" ", "-") + ".jpg"),
                                whole,
                            ),
                            report["duration_seconds"] + 180,
                        )
                    except Exception as e:
                        result[key] = {"error": str(e)[:1200]}
                        errors.append((lesson, key))
                        print(lesson, key, "failed", str(e)[:360], flush=True)

                await asyncio.gather(
                    *(
                        profile(*pair)
                        for pair in PROFILES
                        if not landscape_only or pair[1]
                    )
                )
                (output / (lesson + ".json")).write_text(
                    json.dumps(
                        dict(id=lesson, sha256=report["sha256"], devices=result),
                        indent=2,
                    )
                    + "\n"
                )
                print(lesson, "done", flush=True)
        finally:
            await asyncio.gather(*(b.close() for b in engines.values()))
    if errors:
        raise SystemExit(f"Failed device checks: {errors}")


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("ids", nargs="+")
    cli.add_argument("--output", type=Path, required=True)
    cli.add_argument(
        "--site", default="https://simonrj.github.io/-summit-one-narrator/"
    )
    cli.add_argument("--landscape-only", action="store_true")
    args = cli.parse_args()
    asyncio.run(check(args.ids, args.site, args.output, args.landscape_only))
