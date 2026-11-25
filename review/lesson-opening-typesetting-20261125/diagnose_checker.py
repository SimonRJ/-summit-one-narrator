"""Reproduce the original reader assertion with a local synthetic learner.

No application source is modified. --font-overlay can serve the approved local
font implementation while the app/lesson/renderer files remain at the failed SHA.
"""
import argparse
import ast
import asyncio
import hashlib
import json
import os
from pathlib import Path
import subprocess

from aiohttp import web
from playwright.async_api import async_playwright


async def main(args):
    root, output = args.root.resolve(), args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    tree = ast.parse((root / "tools/browser_checks.py").read_text())
    mock = next(node.value.value for node in tree.body if isinstance(node, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == "MOCK" for t in node.targets))
    baseline = "585081646578fe8b0020d2dee831a8f853eb3bca"
    checker = subprocess.check_output(
        ["git", "show", baseline + ":tools/check_lesson_reading_layouts.py"], cwd=root, text=True)
    for path in ("app-main.js", "reviewed-lesson.js", "math-typography.js",
                 "data/read-watch-practise.json", "data/read-watch-practise-later.json"):
        expected = subprocess.check_output(["git", "show", baseline + ":" + path], cwd=root)
        assert (root / path).read_bytes() == expected, "Diagnostic source changed: " + path
    source = next(node.value.value for node in ast.parse(checker).body if isinstance(node, ast.Assign)
                  and any(isinstance(t, ast.Name) and t.id == "MEASURE" for t in node.targets))
    source = source.replace("const figure = card.querySelector", "window.__beforeText = [...card.querySelectorAll('.rwl-full-example > ol > li')].map(n=>n.textContent);\n    const figure = card.querySelector")
    source = source.replace("throw Error('Different prompt or working in lesson '+lesson.slot);", "{window.__readingDifference={slot:lesson.slot,expected:lesson.example.steps,before:window.__beforeText,after:full,prediction,expectedPrediction:lesson.example.prediction,connected:card.isConnected,session:app.querySelector('.session-page')?.getAttribute('aria-label'),math:[...card.querySelectorAll('[data-math-source]')].map(n=>({source:n.dataset.mathSource,tex:n.dataset.tex,annotation:n.querySelector('annotation')?.textContent}))};throw Error('Different prompt or working in lesson '+lesson.slot);}")

    async def serve(request):
        name = request.match_info["path"] or "index.html"
        folder = args.font_overlay if args.font_overlay and (name == "design-system.css" or name.startswith("fonts/")) else root
        target = (folder / name).resolve()
        if folder.resolve() not in target.parents or not target.is_file():
            raise web.HTTPNotFound()
        return web.FileResponse(target)

    app = web.Application()
    app.router.add_get("/{path:.*}", serve)
    runner = web.AppRunner(app)
    await runner.setup()
    server = web.TCPSite(runner, "127.0.0.1", 0)
    await server.start()
    site = f"http://127.0.0.1:{server._server.sockets[0].getsockname()[1]}/"
    result = {"failed_commit": "585081646578fe8b0020d2dee831a8f853eb3bca",
              "checker_sha256": hashlib.sha256(checker.encode()).hexdigest(),
              "font_overlay": bool(args.font_overlay)}
    if args.font_overlay:
        result["font_overlay_css_sha256"] = hashlib.sha256((args.font_overlay / "design-system.css").read_bytes()).hexdigest()
    try:
        async with async_playwright() as pw:
            launch = {"executable_path": args.chromium, "args": json.loads(args.chromium_args)}
            if os.environ.get("HTTPS_PROXY"):
                launch["proxy"] = {"server": os.environ["HTTPS_PROXY"], "bypass": "localhost,127.0.0.1"}
            browser = await pw.chromium.launch(**launch)
            context = await browser.new_context(viewport={"width": 1440, "height": 900},
                                                service_workers="block", ignore_https_errors=bool(os.environ.get("HTTPS_PROXY")))
            await context.route("**/supabase-client.js*", lambda route: route.fulfill(content_type="application/javascript", body=mock))
            await context.route("https://*.supabase.co/**", lambda route: route.abort())
            page = await context.new_page()
            try:
                await page.goto(site, wait_until="domcontentloaded")
                await page.locator("#continue").click()
                await page.locator(".rwl-example").wait_for()
                await page.wait_for_function("typeof window.katex?.render === 'function'", timeout=30000)
                await page.evaluate("document.fonts.ready")
                try:
                    await page.evaluate(source)
                    result["original_assertion"] = "passed in this scheduling run"
                except Exception as error:
                    result["original_assertion"] = str(error)
                    result["difference"] = await page.evaluate("window.__readingDifference")
                result["controlled_typeset"] = await page.evaluate("""async () => {
                  const {renderReviewedLesson}=await import('./reviewed-lesson.js');
                  const {typesetMath}=await import('./math-typography.js?v=advanced-20261113');
                  const volume=await (await fetch('data/read-watch-practise.json')).json();
                  const lesson=volume.lessons.find(x=>x.slot===2), app=document.querySelector('#app');
                  renderReviewedLesson({app,s:{slot:2,focus:lesson.headline},l:lesson,questions:lesson.questions,
                    draft:{summary:{},answers:{},working:{},evidence:{}},markLocal:()=>{},save:()=>{},changedSize:()=>{},video:()=>'<video controls></video>'});
                  const card=app.querySelector('.rwl-example');
                  const steps=()=>[...card.querySelectorAll('.rwl-full-example > ol > li')].map(n=>n.textContent);
                  const before=steps(); typesetMath(app);
                  const after=steps();
                  const preserved=[...card.querySelectorAll('[data-math-source]')].map(n=>({source:n.dataset.mathSource,tex:n.dataset.tex,annotation:n.querySelector('annotation')?.textContent,aria:n.getAttribute('aria-label')}));
                  card.querySelector('.rwl-full-example').open=true;
                  await document.fonts.ready;
                  return {slot:2,before,after,expected:lesson.example.steps,preserved,connected:card.isConnected,session:app.querySelector('.session-page').getAttribute('aria-label')};
                }""")
                (output / "before-finding.json").write_text(json.dumps(result, indent=2) + "\n")
                print(json.dumps(result), flush=True)
                if args.screenshot:
                    try:
                        await page.screenshot(path=output / "lesson-2-rendered.png", timeout=15000)
                    except Exception as error:
                        result["screenshot_error"] = str(error)
                        (output / "before-finding.json").write_text(json.dumps(result, indent=2) + "\n")
            finally:
                await context.close()
                await browser.close()
    finally:
        await runner.cleanup()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--font-overlay", type=Path)
    parser.add_argument("--chromium", required=True)
    parser.add_argument("--chromium-args", required=True)
    parser.add_argument("--screenshot", action="store_true")
    asyncio.run(main(parser.parse_args()))
