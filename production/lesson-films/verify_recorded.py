"""Compare encoded film artwork at each second and the complete Voice C audio by scene."""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess

import numpy as np
from PIL import Image

from render_recorded import ROOT, frames_for


def decode(args):
    return subprocess.check_output(
        [
            "ffmpeg",
            "-nostdin",
            "-threads",
            "2",
            "-filter_threads",
            "1",
            "-v",
            "error",
            "-xerror",
            *map(str, args),
        ]
    )


def samples(path):
    return np.frombuffer(
        decode(["-i", path, "-vn", "-ac", "1", "-ar", "8000", "-f", "f32le", "pipe:1"]),
        dtype="<f4",
    )


def validate(id, voice):
    file = ROOT / "media/lesson-films" / f"{id}.mp4"
    timeline, script, _, draw = frames_for(id, voice)
    text = " ".join(s["narration"] for s in script["scenes"])
    assert text == " ".join(c["text"] for c in timeline["captions"])
    after = timeline["captions"][-1]["end"]
    assert after < timeline["duration"] + 0.04
    master = samples(voice / "narration.flac")
    encoded = samples(file)
    rates = []
    assert abs(len(master) - len(encoded)) < 1200
    for s in timeline["scenes"]:
        start = round(s["start"] * 8000)
        end = min(len(master), len(encoded), round(s["end"] * 8000))
        rate = np.corrcoef(master[start:end], encoded[start:end])[0, 1]
        if not np.isfinite(rate) or rate < 0.992:
            raise ValueError(
                f"{id} scene {s['n']}: recorded audio could not be matched ({rate})"
            )
        rates.append(float(rate))
    raw = decode(
        [
            "-i",
            file,
            "-an",
            "-vf",
            "select='not(mod(n,30))',scale=320:180:flags=area,format=rgb24",
            "-fps_mode",
            "vfr",
            "-f",
            "rawvideo",
            "pipe:1",
        ]
    )
    frames = np.frombuffer(raw, dtype=np.uint8).reshape(-1, 180, 320, 3)
    errors = []
    for second, actual in enumerate(frames):
        reference = np.asarray(
            draw(second, 1.5).resize((320, 180), Image.Resampling.BOX)
        )
        delta = np.abs(actual.astype("int16") - reference.astype("int16"))
        # The decoded H.264/YUV420 colour conversion and resampling necessarily round.
        errors.append([float(delta[:155].mean()), float(delta[155:].mean())])
    peak = np.max(errors, axis=0)
    if max(peak) > 5:
        raise ValueError(
            f"{id}: decoded artwork differs at whole-second comparisons ({peak})"
        )
    meta = ROOT / "production/lesson-films" / id / "guide.json"
    guide = json.loads(meta.read_text())
    digest = hashlib.file_digest(file.open("rb"), "sha256").hexdigest()
    assert digest == guide["sha256"]
    assert len(timeline["scenes"]) == len(guide["chapters"])
    info = {
        "sha256": digest,
        "decoded_reference_comparisons": len(frames),
        "picture_comparison_period_seconds": 1,
        "maximum_picture_mean_channel_error_0_to_255": round(float(peak[0]), 3),
        "maximum_caption_region_mean_channel_error_0_to_255": round(float(peak[1]), 3),
        "minimum_source_audio_correlation_per_scene": round(min(rates), 6),
        "recorded_scenes_checked": len(rates),
        "timed_caption_phrases": len(timeline["captions"]),
        "spoken_words": len(text.split()),
        "source_voice_reference_sha256": timeline["narration_reference"],
        "source_word_alignment_percent": timeline["mean_match_percent"],
    }
    (meta.parent / "qa.json").write_text(json.dumps(info, indent=2) + "\n")
    return info


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("id")
    cli.add_argument("source", type=Path)
    args = cli.parse_args()
    print(json.dumps(validate(args.id, args.source)))
