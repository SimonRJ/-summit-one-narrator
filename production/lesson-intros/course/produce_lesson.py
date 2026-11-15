"""Record one lesson with Voice C, then render and check the timed movie."""

import argparse
from hashlib import sha256
import json
import subprocess
import sys

from compile_intros import ROOT, compile_lesson, lessons


STUDIO = ROOT / "production/t01-studio"
BUILD = ROOT / "build/t01-studio"


def run(name, *args, **kwargs):
    return subprocess.run([sys.executable, str(STUDIO / name), *args], cwd=ROOT, **kwargs)


def record(lesson, scenes, seed):
    directory = BUILD / lesson
    directory.mkdir(parents=True, exist_ok=True)
    sequence = directory / "requested-scenes.json"
    sequence.write_text(json.dumps([{"lesson": lesson, "scene": number} for number in scenes]))
    return run("synth.py", "--sequence", str(sequence), "--threads", "4", "--seed-offset", str(seed))


def has_recording(lesson, scene):
    stem = BUILD / f"{lesson}-{scene['n']:02}"
    try:
        metadata = json.loads(stem.with_suffix(".json").read_text())
    except (OSError, json.JSONDecodeError):
        return False
    return (stem.with_suffix(".wav").is_file()
            and metadata.get("narration_sha256") == sha256(scene["narration"].encode()).hexdigest())


def produce(id, attempt):
    lesson = next(item for item in lessons() if item.id == id)
    script = compile_lesson(lesson)
    seed_base = attempt * 269
    for seed in (0, 19, 73, 155):
        incomplete = [scene["n"] for scene in script["scenes"] if not has_recording(id, scene)]
        if not incomplete:
            break
        record(id, incomplete, seed_base + seed)
    report = BUILD / id / "alignment-failure.json"
    for seed in (71, 137, 177, 215):
        aligned = run("prepare_audio.py", id)
        if aligned.returncode == 0:
            break
        if not report.is_file():
            aligned.check_returncode()
        targets = json.loads(report.read_text())["scenes"]
        record(id, targets, seed_base + seed)
    else:
        run("prepare_audio.py", id, check=True)
    run("render.py", id, "--preview", check=True)
    run("render.py", id, check=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("id")
    parser.add_argument("--attempt", type=int, choices=(0, 1, 2), default=0)
    args = parser.parse_args()
    produce(args.id, args.attempt)
