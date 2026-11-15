"""Install verified teaching films and generate their review pages."""

from html import escape
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil

from chapter_films import CHAPTER_FILMS

ROOT = Path(__file__).resolve().parents[2]
BUILD = ROOT / "build/t01-studio"
IDS = ("T01.1", "T01.2")
CHAPTER_IDS = (*IDS, "T01.3", "T01.E", *CHAPTER_FILMS)
TEACHING_SEQUENCE = (*IDS, "T01.3", "T01.E", "T02.1", "T02.2", *CHAPTER_FILMS)
VERSION = "t01-studio-v1"
CHAPTER_VERSION = "studio-chapters-02-04-v1"
VOICE_SHA = "0f3304a393ee504e9fa22537267ac03f150569a5fab0859616f261d009513362"


def revise(path, old, new):
    file = ROOT / path
    content = file.read_text()
    if new in content:
        return
    if content.count(old) != 1:
        raise ValueError(f"{path}: expected one matching source section")
    file.write_text(content.replace(old, new, 1))


def clock(seconds):
    seconds = int(seconds)
    return f"{seconds // 60}:{seconds % 60:02}"


def watch_path(lesson):
    return f"watch-{lesson.lower().replace('.', '-')}.html"


def make_watch_page(lesson, source, report):
    next_lesson = {
        "T01.1": ("watch-t01-2.html", "Next · Choose a representation"),
        "T01.2": ("watch-t01-3.html", "Next · Check the answer"),
        "T01.3": ("watch-t01-e.html", "Next · Worked example"),
        "T01.E": ("watch-t02-1.html", "Next · Find an invariant"),
    }
    chapter_link = ""
    version = VERSION
    if lesson in CHAPTER_FILMS:
        version = CHAPTER_VERSION
        chapter_link = '<a href="teaching-videos.html">Teaching videos</a>'
        index = CHAPTER_FILMS.index(lesson)
        if index + 1 < len(CHAPTER_FILMS):
            following = CHAPTER_FILMS[index + 1]
            title = json.loads((ROOT / f"production/scripts/{following}.json").read_text())["title"]
            next_link = f'<a href="{watch_path(following)}">Next · {escape(title)} →</a>'
        else:
            next_link = ""
    else:
        next_href, next_title = next_lesson[lesson]
        next_link = f'<a href="{next_href}">{next_title} →</a>'
    chapter_buttons = "\n".join(
        f'<button type="button" data-time="{chapter["start"]:.3f}">'
        f'{clock(chapter["start"])} · {escape(chapter["title"])}</button>'
        for chapter in report["chapters"]
    )
    title = escape(source["title"])
    label = f"{lesson} · Worked example" if source.get("type") == "worked_example" else lesson
    transcript = "\n".join(f'<p>{escape(scene["narration"])}</p>' for scene in source["scenes"])
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#10151d">
<link rel="icon" href="icon.svg">
<title>{lesson} · {title} · Summit One</title>
<style>
:root {{ color-scheme: dark; }}
* {{ box-sizing: border-box; }}
body {{
  margin: 0; min-height: 100vh;
  background: radial-gradient(ellipse at 50% 25%, #192631, #0c121a 75%);
  color: #f2f1ed; font: 1rem/1.55 system-ui, sans-serif;
}}
main {{ max-width: 1120px; margin: auto; padding: clamp(18px, 4vw, 48px); }}
nav {{ display: flex; flex-wrap: wrap; gap: 8px; }}
.back {{ justify-content: space-between; gap: 8px 20px; }}
a {{ color: #9cdbbc; }}
h1 {{ max-width: 880px; margin: .25em 0 .45em; font-size: clamp(1.95rem, 5vw, 3.45rem); line-height: 1.12; }}
h2 {{ margin: 0; font-size: 1.2rem; }}
p {{ max-width: 55rem; color: #bac4cf; }}
.lesson {{ color: #9cdbbc; margin: 2rem 0 0; font-size: .88rem; font-weight: 700; }}
video {{ display: block; width: 100%; aspect-ratio: 16 / 9; background: #10151d; border: 1px solid #354652; border-radius: 14px; }}
.meta {{ color: #bac4cf; margin: .65rem 0 0; }}
.chapters {{ margin: 1.2rem 0 1.6rem; }}
button {{
  cursor: pointer; min-height: 44px; border: 1px solid #405463; border-radius: 12px;
  background: #1b2834; color: #eef2f4; font: inherit; padding: .5rem .8rem;
}}
.exercise {{ background: #18232e; border: 1px solid #364756; border-radius: 16px; padding: 1.15rem; }}
summary {{ cursor: pointer; color: #9cdbbc; padding-block: .4rem; }}
.transcript {{ margin-top: 1rem; }}
button:focus-visible, a:focus-visible, summary:focus-visible {{ outline: 2px solid #9cdbbc; outline-offset: 4px; }}
</style>
</head>
<body>
<main>
<nav class="back" aria-label="Lesson navigation">
<a href="./">← Summit One</a>{chapter_link}{next_link}
</nav>
<p class="lesson">{label}</p>
<h1>{title}</h1>
<p>{escape(source["goal"])}</p>
<video id="lesson" controls playsinline preload="metadata" aria-label="{title}"
  poster="media/{lesson}-studio-poster.jpg?v={version}">
  <source src="media/{lesson}.mp4?v={version}" type="video/mp4">
</video>
<p class="meta">{clock(report["duration_seconds"])} · Full HD</p>
<nav class="chapters" aria-label="Video chapters">{chapter_buttons}</nav>
<section class="exercise">
<h2>Try it in your notebook</h2>
<p>{escape(source["notebook_exercise"])}</p>
<details><summary>Check your reasoning</summary><p>{escape(source["notebook_answer"])}</p></details>
</section>
<details class="transcript"><summary>Read the transcript</summary>{transcript}</details>
<p><a href="media/{lesson}.mp4?v={version}">Open the MP4 directly</a></p>
</main>
<script>
const video = document.querySelector("#lesson");
for (const button of document.querySelectorAll("[data-time]")) {{
  button.addEventListener("click", () => {{
    video.currentTime = Number(button.dataset.time);
    video.play().catch(() => {{}});
    video.scrollIntoView({{block: "center"}});
  }});
}}
</script>
</body>
</html>
"""


def make_video_index(teaching):
    videos = {item["id"]: item for item in teaching["items"]}
    sections = []
    for number in range(1, 5):
        rows = []
        for lesson in TEACHING_SEQUENCE:
            if not lesson.startswith(f"T{number:02}."):
                continue
            title = escape(videos[lesson]["title"])
            kind = "Worked example" if videos[lesson]["type"] == "worked_example" else "Concept"
            rows.append(f'<li><a href="{watch_path(lesson)}"><span>{title}</span>'
                        f'<small>{lesson} · {kind}</small></a></li>')
        heading = escape(videos[f"T{number:02}.1"]["chapter"])
        sections.append(f'<section><h2>{heading}</h2><ol>{"".join(rows)}</ol></section>')
    blocks = "\n".join(sections)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#10151d">
<link rel="icon" href="icon.svg">
<title>Teaching videos · Summit One</title>
<style>
:root {{ color-scheme: dark; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; min-height: 100vh; color: #f2f1ed; background: radial-gradient(ellipse at 50% 20%, #192631, #0c121a 75%); font: 1rem/1.5 system-ui, sans-serif; }}
main {{ max-width: 1040px; margin: auto; padding: clamp(18px, 4vw, 48px); }}
a {{ color: #9cdbbc; }}
h1 {{ font-size: clamp(2.15rem, 6vw, 3.65rem); line-height: 1.08; margin: .85em 0 .75em; }}
h2 {{ margin: 0 0 14px; font-size: 1.14rem; line-height: 1.3; }}
.chapters {{ display: grid; gap: 18px; grid-template-columns: repeat(auto-fit, minmax(min(100%, 350px), 1fr)); }}
section {{ background: #17232e; border: 1px solid #354652; border-radius: 14px; padding: 17px; }}
ol {{ list-style: none; margin: 0; padding: 0; }}
li + li {{ border-top: 1px solid #354652; }}
li a {{ display: block; min-height: 44px; padding: .7rem .3rem; text-decoration: none; }}
li a:hover span {{ text-decoration: underline; }}
small {{ display: block; color: #bac4cf; margin-top: .16rem; }}
a:focus-visible {{ outline: 2px solid #9cdbbc; outline-offset: 3px; }}
</style>
</head>
<body>
<main>
<a href="./">← Summit One</a>
<h1>Teaching videos</h1>
<div class="chapters">
{blocks}
</div>
</main>
</body>
</html>
"""


def install(lessons=IDS):
    verified = {}
    for lesson in lessons:
        folder = BUILD / lesson
        source = json.loads((ROOT / f"production/scripts/{lesson}.json").read_text())
        report = json.loads((folder / "qa.json").read_text())
        if (report["id"] != lesson or not report["decoded_successfully"]
                or report["reference_sha256"] != VOICE_SHA or report["caption_layers"] != 1
                or report["match_percent"] < 90
                or hashlib.sha256((folder / "final.mp4").read_bytes()).hexdigest() != report["sha256"]):
            raise ValueError(f"{lesson}: a verified render with Voice C is required")
        if lesson in CHAPTER_FILMS:
            timeline = json.loads((folder / "timeline.json").read_text())
            recorded = [" ".join(word["text"] for word in scene["words"]) for scene in timeline["scenes"]]
            if recorded != [scene["narration"] for scene in source["scenes"]]:
                raise ValueError(f"{lesson}: the verified export must match the lesson script")
        verified[lesson] = (folder, source, report)

    teaching_file = ROOT / "data/teaching-72.json"
    teaching = json.loads(teaching_file.read_text())
    for lesson, (folder, source, report) in verified.items():
        for src, dest in (("final.mp4", f"{lesson}.mp4"),
                          ("poster.jpg", f"{lesson}-studio-poster.jpg")):
            shutil.copyfile(folder / src, ROOT / "media" / dest)
        captions = (folder / "captions.vtt").read_text().rstrip("\n")
        (ROOT / "media" / f"{lesson}.vtt").write_text(captions + "\n")
        shutil.copyfile(folder / "qa.json", ROOT / f"review/{lesson}-studio-qa.json")
        page = ROOT / watch_path(lesson)
        page.write_text(make_watch_page(lesson, source, report))
        row = next(item for item in teaching["items"] if item["id"] == lesson)
        row["transcript"] = " ".join(scene["narration"] for scene in source["scenes"])
    teaching_file.write_text(json.dumps(teaching, ensure_ascii=False, indent=2) + "\n")
    if set(CHAPTER_FILMS) <= verified.keys():
        (ROOT / "teaching-videos.html").write_text(make_video_index(teaching))

    if tuple(lessons) == IDS and "const openingFilmIds=" not in (ROOT / "app-main.js").read_text():
        install_first_lesson_routes()


def install_first_lesson_routes():
    revise("app-main.js",
           '  if(id==="T01.2")return ""; // George retired; use natural on-device narration until new T01.2 master is approved.',
           f'  if(id==="T01.1"||id==="T01.2")return "media/"+id+".mp4?v={VERSION}";')
    revise("app-main.js", "function teachingFor(session){",
           f"""function openingConceptFilm(slot){{
 const id=slot===1?"T01.1":slot===2?"T01.2":null;
 if(!id)return "";
 const film=teaching.find(item=>item.id===id);
 if(!film)return "";
 return `<details class="opening-fallback"><summary>Watch ${{esc(film.title)}}</summary>
   <div class="opening-video-wrap"><video controls playsinline preload="none"
     src="${{finalVideoUrl(id)}}" poster="media/${{id}}-studio-poster.jpg?v={VERSION}" aria-label="${{esc(film.title)}}"></video></div>
 </details>`;
}}
function teachingFor(session){{""")
    revise("app-main.js", '   ${media}\n   <p class="lesson-replay-note">',
           '   ${media}\n   ${openingConceptFilm(item.slot)}\n   <p class="lesson-replay-note">')
    revise("app-main.js", '   <p class="opening-coda">',
           '   ${openingConceptFilm(s.slot)}\n   <p class="opening-coda">')

    # These versions let iPhone and installed PWA clients pick up the new routes.
    for relative in ("index.html", "sw.js"):
        path = ROOT / relative
        html = path.read_text()
        html, count = re.subn(r"app-main\.js\?v=[^\s\"']+", f"app-main.js?v={VERSION}", html)
        if count != 1:
            raise ValueError(f"{relative}: missing app cache revision")
        if relative == "sw.js":
            html = re.sub(r'const CACHE="[^"]+";', f'const CACHE="summit-one-{VERSION}";', html, count=1)
        path.write_text(html)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lessons", choices=CHAPTER_IDS, nargs="+", default=IDS)
    install(parser.parse_args().lessons)
