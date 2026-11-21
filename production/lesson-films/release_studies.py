"""Prepare one film from its public, word-aligned Voice C recording."""
import argparse
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
GROUPS = {
    "three": ("S137", "S141", "S149"),
    "four": ("S138", "S150", "S152", "S155"),
}
RECORDINGS = {
    "three": "e3f0ef4e55231e00513f18da44d12c4194a59d9e",
    "four": "04713c9f10da1db43f58f5927df96769d7d3db6b",
}


def prepare(lesson, destination):
    group = next(name for name, ids in GROUPS.items() if lesson in ids)
    ref = RECORDINGS[group]
    subprocess.run(["git", "fetch", "--quiet", "--depth=1", "origin", ref], cwd=ROOT, check=True)
    destination.mkdir(parents=True, exist_ok=True)
    folder = f"review/{group}-original-films/{lesson}"
    inputs = {
        "script.json": f"production/scripts/{lesson}.json",
        "timeline.json": f"{folder}/timeline.json",
        "narration.flac": f"{folder}/narration.flac",
        "captions.vtt": f"{folder}/captions.vtt",
    }
    for name, source in inputs.items():
        with (destination / name).open("wb") as output:
            subprocess.run(["git", "show", f"{ref}:{source}"], cwd=ROOT, stdout=output, check=True)


def build(lesson, out):
    recording = ROOT / "build" / "course-studies" / lesson
    prepare(lesson, recording)
    for utility in ("render_recorded.py", "verify_recorded.py"):
        subprocess.run([sys.executable, str(Path(__file__).with_name(utility)), lesson, str(recording)], check=True)
    out.mkdir(parents=True, exist_ok=True)
    media = ROOT / "media" / "lesson-films"
    guides = ROOT / "production" / "lesson-films" / lesson
    for suffix, source in {
        ".mp4": media / f"{lesson}.mp4", "-poster.jpg": media / f"{lesson}-poster.jpg",
        ".vtt": guides / "captions.vtt", "-guide.json": guides / "guide.json", "-qa.json": guides / "qa.json",
    }.items():
        shutil.copyfile(source, out / (lesson + suffix))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("lesson", choices=sorted(i for ids in GROUPS.values() for i in ids))
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    build(args.lesson, args.output)
