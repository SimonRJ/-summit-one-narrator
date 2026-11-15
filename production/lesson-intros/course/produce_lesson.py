"""Record one lesson with Voice C, then render and check the timed movie."""

import argparse
import json
from pathlib import Path
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


def produce(id):
    lesson = next(item for item in lessons() if item.id == id)
    script = compile_lesson(lesson)
    numbers = [scene["n"] for scene in script["scenes"]]
    for seed in (0, 19, 73):
        incomplete = [number for number in numbers if not (BUILD / f"{id}-{number:02}.json").is_file()
                      or not (BUILD / f"{id}-{number:02}.wav").is_file()]
        if not incomplete:
            break
        record(id, incomplete, seed)
    report = BUILD / id / "alignment-failure.json"
    for seed in (71, 137):
        aligned = run("prepare_audio.py", id)
        if aligned.returncode == 0:
            break
        if not report.is_file():
            aligned.check_returncode()
        targets = json.loads(report.read_text())["scenes"]
        record(id, targets, seed).check_returncode()
    else:
        run("prepare_audio.py", id, check=True)
    run("render.py", id, "--preview", check=True)
    run("render.py", id, check=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("id")
    produce(parser.parse_args().id)
