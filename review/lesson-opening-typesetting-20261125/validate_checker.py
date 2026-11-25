"""Run the repaired reader check with existing browsers and a local file server."""
import argparse
import asyncio
import hashlib
import importlib.util
import json
import os
from pathlib import Path
from types import SimpleNamespace
import sys

from aiohttp import web
from playwright.async_api import async_playwright


async def main(args):
    root, output = args.root.resolve(), args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    sys.path.insert(0, str(root / "tools"))
    spec = importlib.util.spec_from_file_location("reader_check", root / "tools/check_lesson_reading_layouts.py")
    checker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(checker)

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
    proxy = os.environ.get("HTTPS_PROXY")
    os.environ["PLAYWRIGHT_DISABLE_FORCED_CHROMIUM_PROXIED_LOOPBACK"] = "1"

    class PinnedBrowsers:
        async def __aenter__(self):
            self.driver = async_playwright()
            pw = await self.driver.__aenter__()
            for name, executable in (("chromium", args.chromium), ("webkit", args.webkit)):
                original = getattr(pw, name).launch

                async def launch(*, _original=original, _name=name, _executable=executable, **options):
                    options.pop("channel", None)
                    options["executable_path"] = _executable
                    if _name == "chromium":
                        options["args"] = json.loads(args.chromium_args)
                    if proxy:
                        options["proxy"] = {"server": proxy, "bypass": "localhost,127.0.0.1"}
                    browser = await _original(**options)
                    original_context = browser.new_context

                    async def context(**config):
                        if proxy:
                            config["ignore_https_errors"] = True
                        return await original_context(**config)

                    browser.new_context = context
                    return browser

                getattr(pw, name).launch = launch
            return pw

        async def __aexit__(self, *error):
            return await self.driver.__aexit__(*error)

    checker.async_playwright = PinnedBrowsers
    report = {"app_renderer_data_commit": "585081646578fe8b0020d2dee831a8f853eb3bca",
              "checker_sha256": hashlib.sha256((root / "tools/check_lesson_reading_layouts.py").read_bytes()).hexdigest(),
              "font_overlay_css_sha256": hashlib.sha256((args.font_overlay / "design-system.css").read_bytes()).hexdigest() if args.font_overlay else None,
              "positive_cases": [], "negative_cases": []}
    try:
        for profile in args.profiles:
            viewports = [None]
            if args.short_screens and profile == "pc":
                viewports += [(1366, 768), (1280, 720)]
            if args.short_screens and profile == "ipad-landscape":
                viewports += [(1024, 768)]
            for viewport in viewports:
                name = profile + ("-" + "x".join(map(str, viewport)) if viewport else "")
                path = output / (name + ".json")
                print("Checking", name, flush=True)
                await checker.run(SimpleNamespace(profile=profile, viewport=viewport, site=site, output=path))
                rows = json.loads(path.read_text())
                report["positive_cases"].append({"name": name, "lessons": len(rows),
                    "authored_text_preserved": all(r["authored_text_preserved"] for r in rows),
                    "typeset_expressions": sum(r["typeset_expressions"] for r in rows),
                    "max_horizontal_overflow": max(r["horizontal"] for r in rows),
                    "max_stage_scroll": max(r["scroll"] for r in rows),
                    "max_footer_overflow": max(r["footer"] for r in rows)})
                (output / "validation-summary.json").write_text(json.dumps(report, indent=2) + "\n")

        if args.negative:
            async with PinnedBrowsers() as pw:
                browser = await pw.chromium.launch()
                context = await browser.new_context(viewport={"width": 1440, "height": 900}, service_workers="block")
                await context.route("**/supabase-client.js*", lambda route: route.fulfill(content_type="application/javascript", body=checker.MOCK))
                await context.route("https://*.supabase.co/**", lambda route: route.abort())
                page = await context.new_page()
                try:
                    await page.goto(site, wait_until="domcontentloaded")
                    await page.locator("#continue").click()
                    await page.locator(".rwl-example").wait_for()
                    await page.wait_for_function("typeof window.katex?.render === 'function'")
                    one = checker.MEASURE.replace("volumes.flatMap(v => v.lessons);", "volumes.flatMap(v => v.lessons).filter(l=>l.slot===2);")
                    cases = {
                        "changed_authored_number": "const m=card.querySelector('[data-math-source]');m.dataset.mathSource='31 × 9';m.setAttribute('aria-label','31 × 9');",
                        "added_working_text": "card.querySelector('.rwl-full-example > ol > li').append(' Incorrect extra sentence.');",
                        "changed_rendered_annotation": "card.querySelector('.katex-mathml annotation').textContent='1+1=3';",
                    }
                    for name, mutation in cases.items():
                        code = one.replace("typesetMath(app);", "typesetMath(app);\n    " + mutation)
                        try:
                            await page.evaluate(code)
                        except Exception as error:
                            message = str(error)
                            assert "Different prompt or working" in message or "Rendered mathematics differs" in message, message
                            report["negative_cases"].append({"name": name, "rejected": True, "error": message})
                            print("Rejected", name, flush=True)
                        else:
                            raise AssertionError("Corrupted content was accepted: " + name)
                finally:
                    await context.close()
                    await browser.close()
        (output / "validation-summary.json").write_text(json.dumps(report, indent=2) + "\n")
    finally:
        await runner.cleanup()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--font-overlay", type=Path)
    parser.add_argument("--chromium", required=True)
    parser.add_argument("--chromium-args", required=True)
    parser.add_argument("--webkit", required=True)
    parser.add_argument("--profiles", nargs="*", default=["pc", "iphone-portrait", "iphone-landscape", "ipad-portrait", "ipad-landscape"])
    parser.add_argument("--short-screens", action="store_true")
    parser.add_argument("--negative", action="store_true")
    asyncio.run(main(parser.parse_args()))
