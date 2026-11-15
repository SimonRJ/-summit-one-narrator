"""Record one lesson with Voice C, then render and check the timed movie."""

import argparse
from hashlib import sha256
import json
import shutil
import subprocess
import sys

from compile_intros import ROOT, compile_lesson, lessons


STUDIO = ROOT / "production/t01-studio"
BUILD = ROOT / "build/t01-studio"
SHARED_VOICE = BUILD / "shared-voice"
TEACHING_STAGES = {"INTRO", "EXAM", "MISTAKES", "RECAP"}


def run(name, *args, **kwargs):
    return subprocess.run([sys.executable, str(STUDIO / name), *args], cwd=ROOT, **kwargs)


def record(lesson, scenes, seed):
    directory = BUILD / lesson
    directory.mkdir(parents=True, exist_ok=True)
    sequence = directory / "requested-scenes.json"
    sequence.write_text(json.dumps([{"lesson": lesson, "scene": number} for number in scenes]))
    return run("synth.py", "--sequence", str(sequence), "--threads", "4", "--seed-offset", str(seed))


def narration_hash(scene):
    return sha256(scene["narration"].encode()).hexdigest()


def has_recording(stem, scene):
    try:
        metadata = json.loads(stem.with_suffix(".json").read_text())
    except (OSError, json.JSONDecodeError):
        return False
    return stem.with_suffix(".wav").is_file() and metadata.get("narration_sha256") == narration_hash(scene)


def teaching_scenes(script):
    return [scene for scene in script["scenes"] if scene["stage"] in TEACHING_STAGES]


def voice_cache_key(script):
    phrases = [narration_hash(scene) for scene in teaching_scenes(script)]
    synth_revision = sha256((STUDIO / "synth.py").read_bytes()).hexdigest()
    return sha256("\n".join([synth_revision, *phrases]).encode()).hexdigest()


def transfer_recording(source, target, scene, lesson):
    if has_recording(source, scene):
        metadata = json.loads(source.with_suffix(".json").read_text())
        metadata.update(lesson=lesson, scene=scene["n"])
        shutil.copyfile(source.with_suffix(".wav"), target.with_suffix(".wav"))
        target.with_suffix(".json").write_text(json.dumps(metadata) + "\n")


def produce(id, script, attempt):
    BUILD.mkdir(parents=True, exist_ok=True)
    shared = teaching_scenes(script)
    for scene in shared:
        destination = BUILD / f"{id}-{scene['n']:02}"
        if not has_recording(destination, scene):
            transfer_recording(SHARED_VOICE / narration_hash(scene), destination, scene, id)
    seed_base = attempt * 269
    for seed in (0, 19, 73, 155):
        incomplete = [scene["n"] for scene in script["scenes"]
                      if not has_recording(BUILD / f"{id}-{scene['n']:02}", scene)]
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
    SHARED_VOICE.mkdir(parents=True, exist_ok=True)
    for scene in shared:
        transfer_recording(BUILD / f"{id}-{scene['n']:02}", SHARED_VOICE / narration_hash(scene), scene, id)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("id")
    parser.add_argument("--cache-key", action="store_true")
    parser.add_argument("--attempt", type=int, choices=(0, 1, 2), default=0)
    args = parser.parse_args()
    script = compile_lesson(next(item for item in lessons() if item.id == args.id))
    if args.cache_key:
        print(voice_cache_key(script))
    else:
        produce(args.id, script, args.attempt)
