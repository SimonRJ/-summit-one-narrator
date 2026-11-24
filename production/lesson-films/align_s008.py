"""Apply the reviewed speech boundaries to the exact S008 Voice C master."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "t01-studio"))
from prepare_audio import stamp


def prepare(source, target):
    timing = json.loads((HERE / "s008-word-times.json").read_text())
    if source.resolve() == target.resolve():
        raise ValueError("Use a separate folder for the corrected timing.")
    for filename, expected in timing["input_sha256"].items():
        with (source / filename).open("rb") as handle:
            if hashlib.file_digest(handle, "sha256").hexdigest() != expected:
                raise ValueError(f"The recorded edition differs: {filename}")

    timeline = json.loads((source / "timeline.json").read_text())
    script = json.loads((source / "script.json").read_text())
    captions = []
    for scene, chapter, positions, groups in zip(
        timeline["scenes"], script["scenes"], timing["word_times"], timing["caption_word_counts"], strict=True
    ):
        # Scene one includes 600 ms of opening silence before the recording.
        origin = scene["start"] if scene["n"] != 1 else 0.6
        previous = origin
        for word, text, (left, right) in zip(
            scene["words"], chapter["narration"].split(), positions, strict=True
        ):
            start, end = round(origin + left / 100, 2), round(origin + right / 100, 2)
            if word["text"] != text or not previous <= start < end <= round(scene["speech_end"], 2):
                raise ValueError(f"Invalid reviewed boundary for scene {scene['n']}: {text}")
            word.update(start=start, end=end)
            previous = end

        # The authored phrase breaks keep each mathematical value together.
        cues = []
        offset = 0
        for count in groups:
            group = scene["words"][offset:offset + count]
            offset += count
            until = group[-1]["end"] + 0.13
            if offset < len(scene["words"]):
                until = min(until, scene["words"][offset]["start"])
            cues.append({"start": group[0]["start"], "end": until, "text": " ".join(w["text"] for w in group)})

        if " ".join(cue["text"] for cue in cues) != chapter["narration"]:
            raise ValueError(f"Caption words missing in scene {scene['n']}")
        captions.extend(cues)

    timeline["captions"] = captions
    timeline["word_timing_method"] = "Reviewed acoustic alignment of all eight final scene recordings"
    target.mkdir(parents=True, exist_ok=True)
    for filename in ("narration.flac", "script.json"):
        shutil.copyfile(source / filename, target / filename)
    (target / "timeline.json").write_text(json.dumps(timeline, indent=2) + "\n")
    (target / "captions.vtt").write_text("WEBVTT\n\n" + "\n\n".join(
        f"{stamp(cue['start'])} --> {stamp(cue['end'])}\n{cue['text']}" for cue in captions
    ) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("target", type=Path)
    args = parser.parse_args()
    prepare(args.source, args.target)
