"""Bind a recorded study to its source and prepare the matching learner routes for QA."""

import argparse
import hashlib
import json
import os
from pathlib import Path
from zipfile import ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[2]
FILES = ("script.json", "timeline.json", "captions.vtt", "narration.flac")


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def bind(lesson, recording, check):
    source = ROOT / "production/scripts" / f"{lesson}.json"
    script = json.loads(source.read_text())
    timeline = json.loads((recording / "timeline.json").read_text())
    assert source.read_bytes() == (recording / "script.json").read_bytes()
    assert [x["n"] for x in script["scenes"]] == [x["n"] for x in timeline["scenes"]]
    assert " ".join(x["narration"] for x in script["scenes"]) == " ".join(
        x["text"] for x in timeline["captions"]
    )
    assert (
        timeline["narration_reference"]
        == "0f3304a393ee504e9fa22537267ac03f150569a5fab0859616f261d009513362"
    )
    binding = {
        "lesson": lesson,
        "commit": os.environ["GITHUB_SHA"],
        "assets": {n: digest(recording / n) for n in FILES},
    }
    manifest = recording / "recording-source.json"
    if check:
        assert (
            json.loads(manifest.read_text()) == binding
        ), "The aligned recording no longer matches its source"
    else:
        manifest.write_text(json.dumps(binding, indent=2) + "\n")


def package(lesson, recording):
    target = ROOT / "build/candidate" / f"{lesson}-recording.zip"
    with ZipFile(target, "w") as archive:
        for name in (*FILES, "recording-source.json"):
            archive.writestr(ZipInfo(name), (recording / name).read_bytes())


def stage(lesson):
    slot = int(lesson[1:])
    guide = json.loads((ROOT / "build/candidate" / f"{lesson}-guide.json").read_text())
    guide["release"] = "http://127.0.0.1:8765/build/candidate/"
    catalog = ROOT / "data/recorded-studies.json"
    data = json.loads(catalog.read_text())
    data["lessons"][lesson] = guide
    catalog.write_text(json.dumps(data))
    covered = []
    for file in ("read-watch-practise.json", "read-watch-practise-later.json"):
        target = ROOT / "data" / file
        rows = json.loads(target.read_text())
        matches = [r for r in rows["lessons"] if r["slot"] == slot]
        if matches:
            assert len(matches) == 1
            matches[0].update(
                videoId=lesson,
                videoTitle=guide["title"],
                movie=guide["release"] + lesson + ".mp4",
                bridge=guide["bridge"],
                filmUse="dedicated",
            )
            target.write_text(json.dumps(rows))
            covered.append(file)
    assert len(covered) == 1, f"Expected one written lesson for {lesson}, found {covered}"


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("action", choices=["seal", "verify", "package", "stage"])
    p.add_argument("lesson")
    p.add_argument("recording", type=Path, nargs="?", default=ROOT / "build/recording")
    a = p.parse_args()
    if a.action == "stage":
        stage(a.lesson)
    elif a.action == "package":
        package(a.lesson, a.recording)
    else:
        bind(a.lesson, a.recording, a.action == "verify")
