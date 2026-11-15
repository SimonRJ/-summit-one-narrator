"""Render Summit One teaching films from their aligned narration."""

import argparse
from bisect import bisect_right
import hashlib
from importlib import import_module
import json
import math
from pathlib import Path
import subprocess

from PIL import Image, ImageDraw

import check_answer
from chapter_films import COURSE_FILMS
import guarantees
import introduction_films
import measure_interval
import operation_order
import prime_conditions
import prime_factors
import quantities
import remainder_patterns
import representations
from stage import HEIGHT, ROOT, WIDTH, Moment, Stage


BUILD = ROOT / "build/t01-studio"
FPS = 30
LESSONS = {
    "T01.1": quantities.SCENES,
    "T01.2": representations.SCENES,
    "T01.3": check_answer.SCENES,
    "T01.E": measure_interval.SCENES,
    **operation_order.SCENES,
    **remainder_patterns.SCENES,
    **guarantees.SCENES,
    **prime_factors.SCENES,
    **prime_conditions.SCENES,
}
CHAPTERS = {
    "T01.1": ((1, "Give numbers meaning"), (3, "Mia’s counters"),
              (6, "Convert units"), (7, "Count written nines"), (9, "Your turn")),
    "T01.2": ((1, "Choose a model"), (3, "The fence problem"), (5, "Close the loop"),
              (6, "Count a queue"), (7, "Compare prices"), (8, "Trace a boundary"), (9, "Your turn")),
    "T01.3": ((1, "Predict the answer"), (3, "The school trip"), (4, "Fill the buses"),
              (6, "Prove the minimum"), (7, "Buses completely full"), (8, "Your turn")),
    "T01.E": ((1, "The ribbon problem"), (3, "Count the gaps"), (4, "Subtract the start"),
              (5, "Slide the ribbon"), (6, "The film problem"), (8, "Your turn")),
    "T02.3": ((1, "Compare two orders"), (3, "Find the gap"), (4, "Build both outputs"),
              (5, "Prove the gap is fixed"), (7, "When can steps swap?"), (8, "Your turn")),
    "T02.E": ((1, "The two rules"), (2, "Copy the whole sum"), (4, "Compare the extras"),
              (5, "Test different inputs"), (6, "Your turn")),
    "T03.1": ((1, "Groups and leftovers"), (3, "The bead puzzle"), (4, "Find bead 50"),
              (5, "Remainder zero"), (6, "Same remainder"), (8, "Your turn")),
    "T03.2": ((1, "Two flashing lights"), (3, "Start together"), (4, "Find the period"),
              (5, "Shift one start"), (6, "When clocks never meet"), (7, "Your turn")),
    "T03.3": ((1, "More counters than boxes"), (3, "The sock puzzle"), (5, "Remainder boxes"),
              (6, "Pairs that sum to 11"), (7, "Your turn")),
    "T03.E": ((1, "The four-number problem"), (2, "Sort by remainder"), (4, "Cancel the leftovers"),
              (5, "Check the bound"), (6, "Your turn")),
    "T04.1": ((1, "Build two factor trees"), (3, "Is 91 prime?"), (4, "Test small primes"),
              (5, "Stop at the square root"), (6, "Three factors of 66"), (7, "Your turn")),
    "T04.2": ((1, "Pair factors of 12"), (3, "Count prime choices"), (4, "Fill the grid"),
              (5, "Count factors of 72 and 360"), (6, "Why squares have odd counts"), (7, "Your turn")),
    "T04.3": ((1, "Sort prime copies"), (3, "Compare 12 and 18"), (4, "Highest common factor"),
              (5, "Lowest common multiple"), (7, "Make a square"), (8, "Your turn")),
    "T04.E": ((1, "The perfect square problem"), (2, "Find unpaired primes"),
              (4, "Check the square"), (5, "Prove the multiplier is smallest"), (6, "Your turn")),
}


def estimated_timeline(lesson):
    """Supply temporary cue positions to inspect artwork before the recording is ready."""
    script = json.loads((ROOT / f"production/scripts/{lesson}.json").read_text())
    cursor = 0.6
    scenes = []
    captions = []
    for scene in script["scenes"]:
        start = cursor
        words = []
        for token in scene["narration"].split():
            duration = 0.29 + len(token) * 0.024
            words.append({"text": token, "start": cursor, "end": cursor + duration})
            cursor += duration + (0.27 if token.endswith((".", "?")) else 0.0)
        finish = cursor
        cursor += 0.9
        scenes.append({"n": scene["n"], "start": 0.0 if scene["n"] == 1 else start,
                       "end": cursor, "speech_end": finish, "words": words})
        captions.append({
            "start": start + 0.2,
            "end": finish,
            "text": " ".join(word["text"] for word in words[:8]),
        })
    return {"id": lesson, "duration": cursor, "scenes": scenes, "captions": captions}


def film_scenes(lesson):
    if lesson in introduction_films.FILMS:
        return introduction_films.FILMS[lesson], introduction_films.chapters(lesson)
    if lesson in LESSONS:
        return LESSONS[lesson], CHAPTERS[lesson]
    module = import_module(f"series_{lesson[1:3]}")
    scenes = module.FILMS[lesson]
    return scenes, tuple((number, draw.chapter) for number, draw in enumerate(scenes, 1))


class Film:
    def __init__(self, timeline, scale):
        self.timeline = timeline
        self.scenes = timeline["scenes"]
        self.captions = timeline["captions"]
        self.functions, self.chapters = film_scenes(timeline["id"])
        if len(self.functions) != len(self.scenes):
            raise ValueError(f"{timeline['id']}: every recorded scene requires its own animation")
        self.scale = scale
        self.scene_starts = [scene["start"] for scene in self.scenes]
        self.caption_starts = [cue["start"] for cue in self.captions]

    def frame(self, t, captions=True):
        stage = Stage(self.scale)
        index = max(0, bisect_right(self.scene_starts, t) - 1)
        self.functions[index](stage, Moment(self.scenes[index], t))
        cue_index = bisect_right(self.caption_starts, t) - 1
        if captions and cue_index >= 0 and t < self.captions[cue_index]["end"]:
            stage.caption(self.captions[cue_index], t)
        return stage.image

    def storyboard(self, out):
        """Render early, middle and late states for every scene."""
        out.mkdir(parents=True, exist_ok=True)
        tile_width, tile_height = 380, 214
        blocks = []
        for index, scene in enumerate(self.scenes):
            if index % 3 == 0:
                sheet = Image.new("RGB", (3 * tile_width, 3 * (tile_height + 23)), "#0f1720")
            for column, fraction in enumerate((0.18, 0.55, 0.97)):
                t = scene["start"] + fraction * (scene["speech_end"] - scene["start"])
                frame = self.frame(t)
                frame.save(out / f"scene-{index + 1:02}-{column + 1}.jpg", quality=90)
                y = index % 3 * (tile_height + 23)
                x = column * tile_width
                thumbnail = frame.resize((tile_width, tile_height), Image.Resampling.LANCZOS)
                sheet.paste(thumbnail, (x, y + 23))
                ImageDraw.Draw(sheet).text((x + 9, y + 5), f"Scene {index + 1}  ·  {t:.1f}s", fill="#d6e4ed")
                blocks.append({"scene": index + 1, "time": round(t, 3)})
            if index % 3 == 2 or index == len(self.scenes) - 1:
                sheet.save(out / f"sheet-{index // 3 + 1}.jpg", quality=91)
        (out / "frames.json").write_text(json.dumps(blocks, indent=2) + "\n")

    def render(self, folder):
        width, height = round(WIDTH * self.scale), round(HEIGHT * self.scale)
        file = folder / "final.mp4"
        frames = math.ceil(self.timeline["duration"] * FPS)
        command = [
            "ffmpeg", "-v", "error", "-y",
            "-f", "rawvideo", "-pixel_format", "rgb24", "-video_size", f"{width}x{height}",
            "-framerate", str(FPS), "-i", "pipe:0", "-i", str(folder / "narration.wav"),
            "-map", "0:v:0", "-map", "1:a:0",
            "-c:v", "libx264", "-preset", "fast", "-crf", "19", "-pix_fmt", "yuv420p",
            "-profile:v", "high", "-level", "4.1", "-threads", "4",
            "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-movflags", "+faststart",
            str(file),
        ]
        with subprocess.Popen(command, stdin=subprocess.PIPE) as ffmpeg:
            try:
                for frame in range(frames):
                    ffmpeg.stdin.write(self.frame(frame / FPS).tobytes())
                    if frame and frame % 900 == 0:
                        print(f"{self.timeline['id']}: {frame / FPS:.0f}s of animation encoded", flush=True)
            finally:
                ffmpeg.stdin.close()
            if ffmpeg.wait():
                raise RuntimeError(f"FFmpeg failed to render {file}")

        poster_scene = self.scenes[0 if self.timeline['id'] in introduction_films.FILMS else 3]
        self.frame(poster_scene["speech_end"] - 0.15, captions=False).save(folder / "poster.jpg", quality=94)
        self.verify(file)

    def verify(self, file):
        probe = json.loads(subprocess.check_output([
            "ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(file),
        ]))
        video = [stream for stream in probe["streams"] if stream["codec_type"] == "video"]
        audio = [stream for stream in probe["streams"] if stream["codec_type"] == "audio"]
        assert len(video) == len(audio) == 1 and len(probe["streams"]) == 2
        assert video[0]["codec_name"] == "h264" and video[0]["pix_fmt"] == "yuv420p"
        assert (video[0]["width"], video[0]["height"], video[0]["avg_frame_rate"]) == (1920, 1080, "30/1")
        assert audio[0]["codec_name"] == "aac" and audio[0]["sample_rate"] == "48000"
        duration = float(probe["format"]["duration"])
        assert abs(self.timeline["duration"] - duration) < 0.08
        assert abs(float(video[0]["duration"]) - float(audio[0]["duration"])) < 0.08
        assert all(a["end"] <= b["start"] + 1e-6 for a, b in zip(self.captions, self.captions[1:]))
        subprocess.run(["ffmpeg", "-xerror", "-v", "error", "-i", str(file), "-f", "null", "-"], check=True)
        lesson = self.timeline["id"]
        report = {
            "id": lesson,
            "duration_seconds": duration,
            "sha256": hashlib.sha256(file.read_bytes()).hexdigest(),
            "width": 1920,
            "height": 1080,
            "fps": FPS,
            "audio_streams": 1,
            "narration": "Approved synthetic Voice C",
            "reference_sha256": self.timeline["narration_reference"],
            "model_revision": self.timeline["model_revision"],
            "narration_speed_changed": False,
            "caption_layers": 1,
            "match_percent": self.timeline["mean_match_percent"],
            "scenes": [{"number": scene["n"], "start": scene["start"],
                        "match_percent": scene["match_percent"]} for scene in self.scenes],
            "chapters": [{"title": title, "start": self.scenes[n - 1]["start"]} for n, title in self.chapters],
            "decoded_successfully": True,
        }
        (file.parent / "qa.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
        print(json.dumps(report, ensure_ascii=False), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("lesson", choices=(*LESSONS, *COURSE_FILMS, *introduction_films.FILMS))
    parser.add_argument("--preview", action="store_true")
    parser.add_argument("--estimate", action="store_true", help="Local storyboard timing only")
    args = parser.parse_args()
    if args.estimate and not args.preview:
        parser.error("Estimated timing is available only for a storyboard")
    folder = BUILD / args.lesson
    timeline = estimated_timeline(args.lesson) if args.estimate else json.loads((folder / "timeline.json").read_text())
    film = Film(timeline, 1.0 if args.preview else 1.5)
    if args.preview:
        film.storyboard(folder / ("estimated-storyboard" if args.estimate else "storyboard"))
    else:
        film.render(folder)


if __name__ == "__main__":
    main()
