"""Record an authored scene with Summit One's approved synthetic Voice C."""

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

import numpy as np
import soundfile as sf

from chapter_films import CHAPTER_FILMS, COURSE_FILMS


ROOT = Path(__file__).resolve().parents[2]
BUILD = ROOT / "build/t01-studio"
OPENING_IDS = ("T01.1", "T01.2")
IDS = (*OPENING_IDS, "T01.3", "T01.E", *CHAPTER_FILMS, *COURSE_FILMS)
REFERENCE = ROOT / "media/voice-audition/vox-australian-male-c.mp3"
VOICE_SHA = "0f3304a393ee504e9fa22537267ac03f150569a5fab0859616f261d009513362"
MODEL_REVISION = "7936080b41163874f38610f46f438e2c0757f9fd"
RATE = 48000


def passages(text):
    groups = []
    for sentence in re.split(r"(?<=[.!?])\s+", text):
        if groups and len((groups[-1] + " " + sentence).split()) <= 28:
            groups[-1] += " " + sentence
        else:
            groups.append(sentence)
    return groups


def record_scenes(requests, threads=2, *, seed_offset=0):
    import torch
    from huggingface_hub import snapshot_download
    from voxcpm import VoxCPM

    if hashlib.sha256(REFERENCE.read_bytes()).hexdigest() != VOICE_SHA:
        raise ValueError("The saved Voice C reference has changed")
    scripts = {
        lesson: json.loads((ROOT / f"production/scripts/{lesson}.json").read_text())
        for lesson in dict.fromkeys(lesson for lesson, _ in requests)
    }
    for lesson, number in requests:
        if not 1 <= number <= len(scripts[lesson]["scenes"]):
            raise ValueError(f"{lesson}: scene {number} is not in the script")
    BUILD.mkdir(parents=True, exist_ok=True)
    reference_wav = BUILD / "reference.wav"
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-i", str(REFERENCE),
         "-ar", str(RATE), "-ac", "1", str(reference_wav)],
        check=True,
    )

    torch.set_num_threads(threads)
    torch.set_num_interop_threads(1)
    model_path = snapshot_download(
        "openbmb/VoxCPM2",
        revision=MODEL_REVISION,
        allow_patterns=["*.json", "*.safetensors", "audiovae.pth", "*.model", "*.txt"],
    )
    model = VoxCPM.from_pretrained(
        model_path, load_denoiser=False, optimize=False, device="cpu"
    )
    prompt = json.loads((ROOT / "production/voice-audition/brief.json").read_text())["text"]
    for lesson, scene_number in requests:
        scene = scripts[lesson]["scenes"][scene_number - 1]
        narration = scene["narration"]
        short_passages = lesson not in OPENING_IDS
        chunks = passages(narration) if short_passages else [narration]
        clips = []
        for index, chunk in enumerate(chunks):
            seed = 432 + 13 * scene_number + index if short_passages else 125 + scene_number
            clip = np.asarray(
                model.generate(
                    text=chunk,
                    prompt_wav_path=str(reference_wav),
                    reference_wav_path=str(reference_wav),
                    prompt_text=prompt,
                    seed=seed + seed_offset,
                    cfg_value=2.0,
                    inference_timesteps=10,
                    normalize=False,
                    denoise=False,
                    max_len=375 if short_passages else 650,
                    retry_badcase=True,
                    retry_badcase_max_times=1,
                ),
                dtype=np.float32,
            ).reshape(-1)
            seconds = len(clip) / RATE
            if not np.isfinite(clip).all() or not 0.5 < seconds < 48:
                raise ValueError(f"{lesson} scene {scene_number} passage {index + 1}: invalid {seconds:.2f}s")
            if float(np.sqrt(np.mean(clip**2))) < 0.005:
                raise ValueError(f"{lesson} scene {scene_number} passage {index + 1}: narration too quiet")
            if index:
                clips.append(np.zeros(round(0.15 * RATE), dtype=np.float32))
            clips.append(clip)
        samples = np.concatenate(clips)
        seconds = len(samples) / RATE
        if not 4 < seconds < 48:
            raise ValueError(f"{lesson} scene {scene_number}: invalid {seconds:.2f}s of assembled audio")

        filename = f"{lesson}-{scene_number:02}.wav"
        sf.write(BUILD / filename, samples, RATE, subtype="PCM_16")
        metadata = {
            "lesson": lesson,
            "scene": scene_number,
            "narration_sha256": hashlib.sha256(narration.encode()).hexdigest(),
            "reference_sha256": VOICE_SHA,
            "model_revision": MODEL_REVISION,
            "natural_speed": True,
            "sample_rate_hz": RATE,
            "duration_seconds": seconds,
        }
        (BUILD / filename.replace(".wav", ".json")).write_text(json.dumps(metadata) + "\n")
        print(f"{lesson} scene {scene_number}: {seconds:.2f}s from Voice C", flush=True)


def record(scene_number, selected_lesson=None):
    lessons = (selected_lesson,) if selected_lesson else OPENING_IDS
    record_scenes([(lesson, scene_number) for lesson in lessons])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument("--scene", type=int)
    selection.add_argument("--sequence", type=Path)
    parser.add_argument("--lesson", choices=IDS)
    parser.add_argument("--threads", type=int, choices=(2, 4), default=2)
    parser.add_argument("--seed-offset", type=int, default=0, help="Resample a scene in the same voice")
    args = parser.parse_args()
    if not 0 <= args.seed_offset < 10000:
        parser.error("The seed offset must be between 0 and 9999")
    if args.sequence:
        requests = [(item["lesson"], item["scene"]) for item in json.loads(args.sequence.read_text())]
        if not requests or len(requests) != len(set(requests)) or any(lesson not in IDS for lesson, _ in requests):
            parser.error("The sequence must list distinct teaching scenes")
    else:
        requests = [(lesson, args.scene) for lesson in ((args.lesson,) if args.lesson else OPENING_IDS)]
    record_scenes(requests, args.threads, seed_offset=args.seed_offset)
