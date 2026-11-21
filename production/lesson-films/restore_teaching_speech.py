"""Render the cube workshop or score notebook with its approved Voice C corrections.

Inputs are the public prerevision MP4/WebVTT/QA files, corrected WAVs with their
Voice C provenance JSON, and a local Whisper model. The original PCM outside
the specified sentence boundaries is retained. All new caption times come from
the corrected voice. A speech mismatch stops the build for listening review.

For example, from the repository root, pass the source media and original QA
from Git revision ef01dbf7, then the checked recordings, script and local ASR:

    python production/lesson-films/restore_teaching_speech.py T13.3 \
        ORIGINAL/media ORIGINAL/review/T13.3-studio-qa.json \
        production/lesson-films/voice-c-repairs \
        production/lesson-films/voice-c-repairs/requests.json \
        LOCAL_WHISPER_SMALL_MODEL OUTPUT_DIRECTORY

"""

import argparse
import bisect
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

import numpy as np
from PIL import ImageDraw
import soundfile as sf

from cube_workshop import region as cube_frame
from score_notebook import region as scores_frame

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "production/t01-studio"))
from prepare_audio import align, caption_cues, stamp, transcribe
from synth import RATE, VOICE_SHA, MODEL_REVISION
from finish_tickets import caption_time, font

EDITIONS = {
    "T13.3": {
        "source": "84b56ff9e8acc7501953df44028715cb06863ff632eb82e526de7d9f64ec507d",
        "captions": "fa4ca7ffb5316c53503f98d9b2dbbc97dea5a9a53045756f7281529122456231",
        "version": "cube-workshop",
        "renderer": cube_frame,
        "changes": [(74.34, 76.84, "T13.3-face-centres")],
    },
    "T16.3": {
        "source": "9e074ff4aefda57cce35853860f12ae782dc3ad1892425c5e5229b4744d2efda",
        "captions": "add31dba21612970505675fb4a690a63784ac147f41eeffa79e3f0a4b4e63701",
        "version": "score-notebook",
        "renderer": scores_frame,
        "changes": [(77.32, 95.35, "T16.3-four-values"), (95.37, 103.13, "T16.3-median-recap")],
    },
}


def digest(path):
    with path.open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def read_cues(path):
    rows = []
    for block in re.split(r"\n\s*\n", path.read_text().strip())[1:]:
        timer, *text = block.splitlines()
        start, end = map(caption_time, timer.split(" --> "))
        rows.append({"start": start, "end": end, "text": " ".join(text)})
    return rows


def change_voice(lesson, source, recordings, qa, model, plan):
    cfg = EDITIONS[lesson]
    old = source / (lesson + ".mp4")
    vtt = source / (lesson + ".vtt")
    if digest(old) != cfg["source"] or digest(vtt) != cfg["captions"]:
        raise ValueError("Unexpected original film or captions")
    raw = subprocess.check_output(
        [
            "ffmpeg",
            "-v",
            "error",
            "-i",
            str(old),
            "-map",
            "0:a",
            "-f",
            "s16le",
            "-ar",
            str(RATE),
            "-ac",
            "1",
            "-",
        ]
    )
    original = np.frombuffer(raw, np.int16)
    cue = read_cues(vtt)
    new = []
    pieces = []
    marks = {}
    cursor = 0.0
    delta = 0.0
    adjusted = []

    def oldpart(lo, hi):
        pieces.append(original[round(lo * RATE) : round(hi * RATE)])
        for line in cue:
            if lo <= line["start"] < hi:
                if line["end"] > hi:
                    raise ValueError("Cut crosses a caption")
                new.append(
                    {"start": line["start"] + delta, "end": line["end"] + delta, "text": line["text"]}
                )

    for a, b, key in cfg["changes"]:
        oldpart(cursor, a)
        metadata = json.loads((recordings / (key + ".json")).read_text())
        sample, rate = sf.read(recordings / (key + ".wav"), dtype="int16")
        text = plan[key]
        if (
            rate != RATE
            or metadata["reference_sha256"] != VOICE_SHA
            or metadata["model_revision"] != MODEL_REVISION
            or metadata["narration_sha256"] != hashlib.sha256(text.encode()).hexdigest()
        ):
            raise ValueError("Incorrect correction waveform or source text")
        rec = transcribe(model, sample.astype(np.float32) / 32768.0)
        words, match = align(text, rec, 0, len(sample) / RATE)
        if match < 99.99:
            raise ValueError(
                f"{key}: verify spoken words ({match}% match): " + " ".join(w.word.strip() for w in rec)
            )
        pad = round(0.14 * RATE)
        pieces.extend((np.zeros(pad, np.int16), sample, np.zeros(pad, np.int16)))
        base = a + delta + pad / RATE
        for word in words:
            marks.setdefault(key, []).append({"start": word["start"] + base, "text": word["text"]})
        for line in caption_cues(words):
            new.append(dict(start=line["start"] + base, end=line["end"] + base, text=line["text"]))
        tracks = len(sample) / RATE + 2 * pad / RATE
        adjusted.append((a, b, base, tracks - (b - a)))
        delta += tracks - (b - a)
        cursor = b
    oldpart(cursor, len(original) / RATE)

    def mapped(t):
        d = 0.0
        for a, b, base, duration_delta in adjusted:
            if a <= t < b:
                return base
            if t >= b:
                d += duration_delta
        return t + d

    new_starts = [mapped(row["start"]) for row in qa["scenes"]]
    for at, key in [(6, "T16.3-four-values"), (7, "T16.3-median-recap")]:
        if key in marks:
            new_starts[at] = marks[key][0]["start"]
    return np.concatenate(pieces), new, new_starts, marks, mapped


def find_word(words, target):
    selected = [w["start"] for w in words if w["text"].lower().strip(".,?!:") == target]
    if not selected:
        raise ValueError("Missing animation cue: " + target)
    return selected[0]


def render(lesson, source, original_report, recordings, out, model, plan):
    from faster_whisper import WhisperModel

    cfg = EDITIONS[lesson]
    out.mkdir(parents=True, exist_ok=True)
    qa = json.loads(original_report.read_text())
    audio, cues, starts, marks, remap = change_voice(
        lesson,
        source,
        recordings,
        qa,
        WhisperModel(str(model), device="cpu", compute_type="int8", cpu_threads=3),
        plan,
    )
    duration = remap(qa["duration_seconds"])
    frames = round(duration * 30)
    sf.write(out / "voice.wav", audio, RATE, subtype="PCM_16")
    (out / (lesson + ".vtt")).write_text(
        "WEBVTT\n\n"
        + "\n\n".join(f"{stamp(r['start'])} --> {stamp(r['end'])}\n{r['text']}" for r in cues)
        + "\n"
    )
    texts = [r["start"] for r in cues]
    bounds = starts + [frames / 30]
    signals = {}
    if lesson == "T13.3":
        signals["edges"] = remap(72.02) - starts[5]
        signals["centres"] = marks["T13.3-face-centres"][0]["start"] - starts[5]
        signals["hidden"] = remap(77.10) - starts[5]
    else:
        w = marks["T16.3-four-values"]
        signals.update(
            remove=find_word(w, "now") - starts[6],
            mean=find_word(w, "sum") - starts[6],
            average=find_word(w, "average") - starts[6],
            notebook=remap(103.35) - starts[7],
        )

    def paint(t):
        n = max(0, bisect.bisect_right(starts, t) - 1)
        im = cfg["renderer"](n, t - starts[n], bounds[n + 1] - starts[n], signals)
        d = ImageDraw.Draw(im)
        dark = "#15182c" if lesson == "T13.3" else "#332740"
        d.rectangle((0, 938, 1920, 1080), fill=dark)
        idx = bisect.bisect_right(texts, t) - 1
        if idx >= 0 and t < cues[idx]["end"]:
            value = cues[idx]["text"]
            size = 39
            while d.textlength(value, font(size, "r")) > 1820:
                size -= 1
            d.text((960, 1008), value, anchor="mm", font=font(size, "r"), fill="#fffdf1")
        return im

    paint(8).save(out / (lesson + "-studio-poster.jpg"), quality=92)
    final = out / (lesson + ".mp4")
    cmd = [
        "ffmpeg",
        "-v",
        "error",
        "-y",
        "-f",
        "rawvideo",
        "-pix_fmt",
        "rgb24",
        "-s",
        "1920x1080",
        "-r",
        "30",
        "-i",
        "-",
        "-i",
        str(out / "voice.wav"),
        "-map",
        "0:v",
        "-map",
        "1:a",
        "-vf",
        "format=yuv420p",
        "-c:v",
        "libx264",
        "-threads",
        "3",
        "-preset",
        "veryfast",
        "-crf",
        "18",
        "-c:a",
        "aac",
        "-b:a",
        "144k",
        "-movflags",
        "+faststart",
        "-t",
        str(frames / 30),
        str(final),
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(frames):
        proc.stdin.write(paint(i / 30).tobytes())
    proc.stdin.close()
    if proc.wait():
        raise RuntimeError("Film encoding failed")
    (out / "measured.json").write_text(
        json.dumps(
            dict(
                sha256=digest(final),
                source_sha256=cfg["source"],
                version=cfg["version"],
                frames=frames,
                duration_seconds=frames / 30,
                scene_starts=starts,
                spoken_cues=signals,
            ),
            indent=2,
        )
        + "\n"
    )


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("lesson", choices=EDITIONS)
    ap.add_argument("original_media", type=Path)
    ap.add_argument("original_report", type=Path)
    ap.add_argument("recordings", type=Path)
    ap.add_argument("request", type=Path)
    ap.add_argument("whisper_model", type=Path)
    ap.add_argument("output", type=Path)
    args = ap.parse_args()
    plan = {r["id"]: r["text"] for r in json.loads(args.request.read_text())}
    render(
        args.lesson,
        args.original_media,
        args.original_report,
        args.recordings,
        args.output,
        args.whisper_model,
        plan,
    )
