"""Record an authored scene with Summit One's approved synthetic Voice C."""

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import numpy as np
import soundfile as sf


ROOT = Path(__file__).resolve().parents[2]
BUILD = ROOT / "build/t01-studio"
IDS = ("T01.1", "T01.2")
REFERENCE = ROOT / "media/voice-audition/vox-australian-male-c.mp3"
VOICE_SHA = "0f3304a393ee504e9fa22537267ac03f150569a5fab0859616f261d009513362"
MODEL_REVISION = "7936080b41163874f38610f46f438e2c0757f9fd"
RATE = 48000


def record(scene_number):
    import torch
    from huggingface_hub import snapshot_download
    from voxcpm import VoxCPM

    if hashlib.sha256(REFERENCE.read_bytes()).hexdigest() != VOICE_SHA:
        raise ValueError("The saved Voice C reference has changed")
    if not 1 <= scene_number <= 9:
        raise ValueError("Expected a scene number from 1 to 9")
    BUILD.mkdir(parents=True, exist_ok=True)
    reference_wav = BUILD / "reference.wav"
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-i", str(REFERENCE),
         "-ar", str(RATE), "-ac", "1", str(reference_wav)],
        check=True,
    )

    torch.set_num_threads(2)
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
    for lesson in IDS:
        script = json.loads((ROOT / f"production/scripts/{lesson}.json").read_text())
        scene = script["scenes"][scene_number - 1]
        samples = np.asarray(
            model.generate(
                text=scene["narration"],
                prompt_wav_path=str(reference_wav),
                reference_wav_path=str(reference_wav),
                prompt_text=prompt,
                seed=125 + scene_number,
                cfg_value=2.0,
                inference_timesteps=10,
                normalize=False,
                denoise=False,
                max_len=650,
                retry_badcase=True,
                retry_badcase_max_times=1,
            ),
            dtype=np.float32,
        ).reshape(-1)
        seconds = len(samples) / RATE
        if not np.isfinite(samples).all() or not 4 < seconds < 48:
            raise ValueError(f"{lesson} scene {scene_number}: invalid {seconds:.2f}s of audio")
        if float(np.sqrt(np.mean(samples**2))) < 0.005:
            raise ValueError(f"{lesson} scene {scene_number}: narration too quiet")

        filename = f"{lesson}-{scene_number:02}.wav"
        sf.write(BUILD / filename, samples, RATE, subtype="PCM_16")
        metadata = {
            "lesson": lesson,
            "scene": scene_number,
            "narration_sha256": hashlib.sha256(scene["narration"].encode()).hexdigest(),
            "reference_sha256": VOICE_SHA,
            "model_revision": MODEL_REVISION,
            "natural_speed": True,
            "sample_rate_hz": RATE,
            "duration_seconds": seconds,
        }
        (BUILD / filename.replace(".wav", ".json")).write_text(json.dumps(metadata) + "\n")
        print(f"{lesson} scene {scene_number}: {seconds:.2f}s from Voice C", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scene", type=int, required=True)
    record(parser.parse_args().scene)
