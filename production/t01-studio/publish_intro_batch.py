"""Install verified introductory films and generate their public review pages."""

import hashlib
from html import escape
import json
from pathlib import Path
import re
import shutil


ROOT = Path(__file__).resolve().parents[2]
PLAN = ROOT / "production/t01-studio/intro_release_plan.json"
VERSION = "lesson-intros-v2"
VOICE_C = "0f3304a393ee504e9fa22537267ac03f150569a5fab0859616f261d009513362"


def watch_page(lesson):
    return f"watch-intro-{lesson.lower()}.html"


def watch_time(seconds):
    minutes, seconds = divmod(int(seconds), 60)
    return f"{minutes}:{seconds:02}"


def html_document(title, body, *, player=False, model_slot=None):
    script = f'<script defer src="lesson-introduction-watch.js?v={VERSION}"></script>' if player else ""
    if model_slot is not None:
        script += f"""
<link rel="stylesheet" href="lesson-models.css?v=guided-20261121">
<script type="module">
import {{mountLessonModel}} from './lesson-models.js?v=guided-20261121';
mountLessonModel(document.getElementById('lessonModel'), {{slot: {int(model_slot)}}});
</script>"""
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#0e1621">
<title>{escape(title)} · Summit One</title>
<link rel="icon" href="icon.svg">
<link rel="stylesheet" href="lesson-introduction-videos.css?v={VERSION}">
{script}
</head>
<body><main>
{body}
</main></body>
</html>
'''


def write_watch(lesson, script, report, following):
    title = escape(script["title"])
    stem = f"media/{lesson}-Intro"
    chapters = "\n".join(
        f'<li><button type="button" data-time="{chapter["start"]:.3f}">'
        f'{escape(chapter["title"])} <span>{watch_time(chapter["start"])}</span></button></li>'
        for chapter in report["chapters"]
    )
    transcript = "\n".join(f'<p>{escape(scene["narration"])}</p>' for scene in script["scenes"])
    next_link = ""
    if following:
        next_link = f'<a rel="next" href="{watch_page(following)}">Next lesson →</a>'
    # The original six local films include one with a companion cube model.
    model_slot = 6 if lesson == 'S006' else None
    model = '<div id="lessonModel"></div>\n' if model_slot else ''
    body = f'''<a href="lesson-introduction-videos.html">← Lesson introduction videos</a>
<p class="lesson-number">Lesson {script["course_slot"]} · {watch_time(report["duration_seconds"])}</p>
<h1>{title}</h1>
<video id="introFilm" controls playsinline preload="metadata"
       poster="{stem}-poster.jpg?v={VERSION}" aria-label="{title} with English captions">
  <source src="{stem}.mp4?v={VERSION}" type="video/mp4">
  <a href="{stem}.mp4?v={VERSION}">Open the video</a>
</video>
{model}<h2>Jump to a chapter</h2>
<ol class="jump">
{chapters}
</ol>
<details class="transcript"><summary>Read the transcript</summary>
{transcript}
</details>
<nav class="next" aria-label="Lesson navigation">
  <a href="./">Summit One app</a>
{next_link}
</nav>'''
    (ROOT / watch_page(lesson)).write_text(html_document(script["title"], body, player=True, model_slot=model_slot))


def write_gallery(lessons, scripts, reports):
    rows = "\n".join(
        f'<li><a href="{watch_page(lesson)}"><span class="number">{scripts[lesson]["course_slot"]:02}</span>'
        f'<strong>{escape(scripts[lesson]["title"])}</strong>'
        f'<small>{watch_time(reports[lesson]["duration_seconds"])}</small></a></li>'
        for lesson in lessons
    )
    body = f'''<a href="./">← Summit One</a>
<h1>Lesson introduction videos</h1>
<p class="intro">Learn the technique, work through three examples and review the mistakes to watch for in exams.</p>
<ol class="gallery">
{rows}
</ol>'''
    (ROOT / "lesson-introduction-videos.html").write_text(
        html_document("Lesson introduction videos", body)
    )


def read_plan():
    plan = json.loads(PLAN.read_text())
    lessons = plan["lessons"]
    if not lessons or sorted(set(lessons)) != lessons or not all(re.fullmatch(r"S[0-9]{3}", code) for code in lessons):
        raise ValueError("The release plan must list unique introductions in course order")
    return plan


def install():
    plan = read_plan()
    lessons = plan["lessons"]
    scripts = {}
    reports = {}
    for lesson in lessons:
        build = ROOT / "build/t01-studio" / lesson
        reports[lesson] = report = json.loads((build / "qa.json").read_text())
        scripts[lesson] = script = json.loads((ROOT / f"production/scripts/{lesson}.json").read_text())
        media = build / "final.mp4"
        assert report["id"] == script["id"] == lesson
        assert report["decoded_successfully"] and report["caption_layers"] == report["audio_streams"] == 1
        assert (report["width"], report["height"], report["fps"]) == (1920, 1080, 30)
        assert report["reference_sha256"] == VOICE_C and report["narration_speed_changed"] is False
        assert report["sha256"] == hashlib.sha256(media.read_bytes()).hexdigest()
        assert report["match_percent"] >= 90 and len(report["chapters"]) == 7
        stem = ROOT / "media" / f"{lesson}-Intro"
        shutil.copyfile(media, stem.with_suffix(".mp4"))
        shutil.copyfile(build / "poster.jpg", stem.with_name(stem.name + "-poster.jpg"))
        shutil.copyfile(build / "captions.vtt", stem.with_suffix(".vtt"))
        shutil.copyfile(build / "qa.json", ROOT / f"review/{lesson}-Intro-qa.json")
        transcript = "\n\n".join(scene["narration"] for scene in script["scenes"])
        stem.with_name(stem.name + "-transcript.txt").write_text(transcript + "\n")
        print(f"{lesson}: verified {watch_time(report['duration_seconds'])} in Full HD with Voice C and captions.")
    published = sorted(path.name[:4] for path in (ROOT / "review").glob("S[0-9][0-9][0-9]-Intro-qa.json"))
    for lesson in published:
        if lesson not in reports:
            reports[lesson] = json.loads((ROOT / f"review/{lesson}-Intro-qa.json").read_text())
            scripts[lesson] = json.loads((ROOT / f"production/scripts/{lesson}.json").read_text())
    for index, lesson in enumerate(published):
        following = published[index + 1] if index + 1 < len(published) else None
        write_watch(lesson, scripts[lesson], reports[lesson], following)
    write_gallery(published, scripts, reports)


if __name__ == "__main__":
    install()
