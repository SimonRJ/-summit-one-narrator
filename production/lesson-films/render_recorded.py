"""Render a word-cued lesson using its recorded Voice C master and studio captions.

The pinned public recordings and scripts are listed in release_studies.py.
Pass a recording directory containing its timeline, script, captions and audio master.
"""

import argparse
import bisect
from functools import lru_cache
import hashlib
import importlib
import json
import math
from pathlib import Path
import shutil
import subprocess
import sys

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "production/t01-studio"))
from stage import Stage, Moment, WHITE, between, blend, clamp, ease, lettering, mix, rgb

LESSONS = {
    "S137": "digit_detectives",
    "S138": "flow_bench",
    "S141": "creek_readings",
    "S149": "area_atelier",
    "S150": "sun_lamp",
    "S152": "counter_exchange",
    "S155": "palindrome_odometer",
    "S156": "beacon_tape",
}
VOICE = "0f3304a393ee504e9fa22537267ac03f150569a5fab0859616f261d009513362"


class Board(Stage):
    def __init__(self, background, scale):
        self.scale = scale
        self.image = background.copy()
        self.draw = ImageDraw.Draw(self.image)

    def polygon(self, points, fill, outline=None, width=2):
        points = [(self.px(x), self.px(y)) for x, y in points]
        self.draw.polygon(points, fill=fill)
        if outline:
            self.draw.line(
                points + [points[0]], fill=outline, width=self.px(width), joint="curve"
            )

    def dashed(self, start, end, color, width=2, dash=9, gap=7, fraction=1):
        x, y = start
        dx, dy = end[0] - x, end[1] - y
        length = math.hypot(dx, dy)
        if length < 1:
            return
        stop = clamp(fraction) * length
        for d in range(0, math.ceil(stop), dash + gap):
            finish = min(d + dash, stop)
            self.line(
                [
                    (x + dx * d / length, y + dy * d / length),
                    (x + dx * finish / length, y + dy * finish / length),
                ],
                color,
                width,
            )

    def label(
        self, text, x, y, size, color=WHITE, alpha=1, *, align="left", bold=False
    ):
        self.text(str(text), x, y, size, color, bold=bold, opacity=alpha, align=align)


@lru_cache(maxsize=12)
def background(top, bottom, scale):
    width, height = round(1280 * scale), round(720 * scale)
    image = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(image)
    for y in range(height):
        draw.line((0, y, width, y), fill=blend(top, bottom, y / height))
    return image


def caption(art, cue, words, t):
    """One phrase band, with smoothly moving word-weight emphasis in its final recording."""
    all_words = cue["text"].split()
    # Use the printed spelling and measured words in order, including split captions.
    word_starts = [w["start"] for w in words]
    i = bisect.bisect_left(word_starts, cue["start"] - 0.055)
    positions = words[i : i + len(all_words)]
    if " ".join(w["text"] for w in positions).casefold() != cue["text"].casefold():
        for k in range(max(0, i - 3), min(i + 4, len(words))):
            sub = words[k : k + len(all_words)]
            if " ".join(w["text"] for w in sub).casefold() == cue["text"].casefold():
                positions = sub
                break
    if len(positions) != len(all_words):
        positions = []
    size = 38
    gap = art.px(10)

    def widths():
        return [
            max(lettering(w, art.px(size), WHITE, b).width for b in (False, True))
            for w in all_words
        ]

    ws = widths()
    while sum(ws) + gap * (len(ws) - 1) > art.px(1200) and size > 28:
        size -= 1
        ws = widths()
    total = sum(ws) + gap * (len(ws) - 1)
    x = (art.image.width - total) // 2
    opacity = min(ease((t - cue["start"]) / 0.08), ease((cue["end"] - t) / 0.11))
    if opacity <= 0:
        return
    art.box(
        (1280 - total / art.scale) / 2 - 18,
        631,
        total / art.scale + 36,
        66,
        fill="#101820",
        radius=15,
        opacity=opacity,
    )
    for idx, (w, width) in enumerate(zip(all_words, ws)):
        emphasis = 0
        if positions:
            pos = positions[idx]
            emphasis = min(
                ease((t - pos["start"] + 0.06) / 0.15),
                ease((pos["end"] - t + 0.13) / 0.18),
            )
        # A thin regular glyph plus a soft overlay of its heavier counterpart produces
        # one legible word throughout; both layers share the reserved advance width.
        light = lettering(w, art.px(size), WHITE, False)
        bold = lettering(w, art.px(size), WHITE, True)
        if emphasis < 1:
            art.paste(
                light,
                x + (width - light.width) // 2,
                art.px(664) - light.height // 2,
                opacity * (1 - emphasis),
            )
        if emphasis > 0:
            art.paste(
                bold,
                x + (width - bold.width) // 2,
                art.px(664) - bold.height // 2,
                opacity * emphasis,
            )
        x += width + gap


def frames_for(id, voice):
    timeline = json.loads((voice / "timeline.json").read_text())
    script = json.loads((voice / "script.json").read_text())
    assert (
        timeline["id"] == script["id"] == id
        and timeline["narration_reference"] == VOICE
    )
    assert len(timeline["scenes"]) == len(script["scenes"])
    for scene, part in zip(timeline["scenes"], script["scenes"]):
        assert " ".join(w["text"] for w in scene["words"]) == part["narration"], (
            id,
            scene["n"],
        )
    film = importlib.import_module(LESSONS[id])
    film.check_maths()
    scenes = timeline["scenes"]
    starts = [s["start"] for s in scenes]
    caps = timeline["captions"]
    capstarts = [c["start"] for c in caps]
    words = [w for s in scenes for w in s["words"]]

    def draw(t, scale):
        i = max(0, bisect.bisect_right(starts, t) - 1)
        art = Board(background(*film.BACKGROUND, scale), scale)
        moment = Moment(scenes[i], t)
        film.draw(art, i + 1, moment)
        k = bisect.bisect_right(capstarts, t) - 1
        if k >= 0 and t <= caps[k]["end"]:
            caption(art, caps[k], words, t)
        return art.image

    return timeline, script, film, draw


def render(id, voice, previews=None):
    t, script, film, draw = frames_for(id, voice)
    if previews:
        previews.mkdir(parents=True, exist_ok=True)
        for scene in t["scenes"]:
            for which, fraction in [("early", 0.30), ("late", 0.85)]:
                s = scene["start"] + (scene["end"] - scene["start"]) * fraction
                draw(s, 0.7).save(
                    previews / f"{id}-{scene['n']:02}-{which}.jpg", quality=91
                )
        return
    out = ROOT / "media/lesson-films"
    out.mkdir(exist_ok=True, parents=True)
    guide = ROOT / "production/lesson-films" / id
    guide.mkdir(exist_ok=True)
    mp4 = out / f"{id}.mp4"
    temp = mp4.with_suffix(".building.mp4")
    fps = 30
    n = math.ceil(t["duration"] * fps)
    cmd = [
        "ffmpeg",
        "-y",
        "-nostdin",
        "-v",
        "error",
        "-f",
        "rawvideo",
        "-pix_fmt",
        "rgb24",
        "-s",
        "1920x1080",
        "-framerate",
        str(fps),
        "-i",
        "pipe:0",
        "-i",
        str(voice / "narration.flac"),
        "-map",
        "0:v:0",
        "-map",
        "1:a:0",
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-crf",
        "20",
        "-threads",
        "2",
        "-filter_threads",
        "1",
        "-pix_fmt",
        "yuv420p",
        "-profile:v",
        "high",
        "-level",
        "4.1",
        "-g",
        "60",
        "-c:a",
        "aac",
        "-b:a",
        "160k",
        "-movflags",
        "+faststart",
        str(temp),
    ]
    with subprocess.Popen(cmd, stdin=subprocess.PIPE) as enc:
        try:
            for frame in range(n):
                enc.stdin.write(draw(frame / fps, 1.5).tobytes())
        finally:
            enc.stdin.close()
        if enc.wait():
            raise RuntimeError(f"{id} could not encode")
    probe = json.loads(
        subprocess.check_output(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_streams",
                "-show_format",
                "-of",
                "json",
                str(temp),
            ]
        )
    )
    video, audio = probe["streams"]
    assert (
        video["width"],
        video["height"],
        video["avg_frame_rate"],
        int(video["nb_frames"]),
    ) == (1920, 1080, "30/1", n)
    assert (
        audio["codec_name"] == "aac"
        and abs(float(audio["duration"]) - t["duration"]) < 0.12
    )
    subprocess.run(
        [
            "ffmpeg",
            "-nostdin",
            "-v",
            "error",
            "-threads",
            "2",
            "-xerror",
            "-i",
            str(temp),
            "-f",
            "null",
            "-",
        ],
        check=True,
    )
    temp.replace(mp4)
    film.poster(draw).save(out / f"{id}-poster.jpg", quality=92, optimize=True)
    shutil.copyfile(voice / "captions.vtt", guide / "captions.vtt")
    meta = {
        "id": id,
        "title": script["title"],
        "seconds": float(probe["format"]["duration"]),
        "chapters": [
            {"title": s["title"], "start": round(c["start"], 3)}
            for s, c in zip(script["scenes"], t["scenes"])
        ],
        "transcript": [s["narration"] for s in script["scenes"]],
        "bridge": film.BRIDGE,
        "sha256": hashlib.file_digest(mp4.open("rb"), "sha256").hexdigest(),
    }
    (guide / "guide.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2) + "\n"
    )
    print(id, n, meta["seconds"], meta["sha256"], flush=True)


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("id", choices=LESSONS)
    cli.add_argument("source", type=Path)
    cli.add_argument("--previews", type=Path)
    args = cli.parse_args()
    render(args.id, args.source, args.previews)
