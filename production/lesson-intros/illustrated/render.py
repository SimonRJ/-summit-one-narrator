"""Render a lesson-specific animation against the unchanged published Voice C soundtrack."""
import argparse
from bisect import bisect_right
from hashlib import sha256
import json
from math import ceil
from pathlib import Path
import subprocess
from urllib.request import Request, urlopen

from PIL import Image, ImageDraw

import area
import fraction_art
import perimeter
import palindrome
import remainders
import place_value
import reverse_steps
import digit_slots
import digit_tallies
import cube_layers
import cryptarithm
import reversed_digits
import prime_pairs
import ladder_recurrence
import common_factor
import shifted_remainders
import grid_rectangles
from visuals import Art, Cues


HERE = Path(__file__).resolve().parent
REPOSITORY = "SimonRJ/-summit-one-narrator"
RELEASE = f"https://github.com/{REPOSITORY}/releases/download/lesson-introductions/"
MOVIES = {"S001": (remainders, "digits"), "S002": (place_value, "area"), "S003": (reverse_steps, "digits"), "S004": (digit_slots, "edge"), "S005": (digit_tallies, "area"), "S006": (cube_layers, "edge"), "S008": (palindrome, "digits"), "S009": (cryptarithm, "fraction"), "S010": (reversed_digits, "area"), "S011": (prime_pairs, "digits"), "S012": (ladder_recurrence, "edge"), "S013": (common_factor, "fraction"), "S015": (shifted_remainders, "digits"), "S017": (grid_rectangles, "edge"), "S078": (area, "area"), "S108": (perimeter, "edge"), "S142": (fraction_art, "fraction")}
FPS = 30


def load(lesson):
    data = json.loads((HERE / f"{lesson}.json").read_text())
    assert len(data["scenes"]) == (9 if lesson in ("S001", "S002") else 12 if lesson in ("S004", "S005") else 11)
    assert all(scene["start"] <= scene["speech_end"] <= scene["end"] for scene in data["scenes"])
    assert all(a["end"] <= b["start"] for a,b in zip(data["captions"],data["captions"][1:]))
    if lesson not in ("S001", "S002"):
        assert all(scene["match"] >= (80 if lesson in ("S010", "S011", "S017") else 90) for scene in data["scenes"])
    return data


class Lesson:
    def __init__(self, lesson, scale=1.5):
        self.id = lesson
        self.data = load(lesson)
        self.artist, self.theme = MOVIES[lesson]
        self.scenes = self.data["scenes"]
        self.captions = self.data["captions"]
        self.scene_starts = [s["start"] for s in self.scenes]
        self.caption_starts = [c["start"] for c in self.captions]
        self.scale = scale

    def frame(self, time, captions=True):
        board = Art(self.scale, self.theme)
        scene = self.scenes[bisect_right(self.scene_starts, time) - 1]
        self.artist.draw(board, Cues(scene,time), scene["n"])
        current = bisect_right(self.caption_starts,time) - 1
        if captions and current >= 0 and time < self.captions[current]["end"]:
            board.caption(self.captions[current],time)
        return board.image

    def preview(self, target):
        contact = Image.new("RGB",(1008, len(self.scenes)*211),"#111925")
        pencil = ImageDraw.Draw(contact)
        for scene in self.scenes:
            index = scene["n"] - 1
            for column, fraction in enumerate((.18,.52,.95)):
                time=scene["start"]+(scene["speech_end"]-scene["start"])*fraction
                frame=self.frame(time)
                thumb=frame.resize((336,189),Image.Resampling.LANCZOS)
                contact.paste(thumb,(column*336,index*211))
                pencil.text((column*336+9,index*211+193),f"Scene {scene['n']:02d}  ·  {time:05.1f}s",fill="#e4edf1")
        contact.save(target / f"{self.id}-contact.jpg",quality=90)

    def render(self, target, source):
        if not source.is_file():
            with urlopen(Request(RELEASE + self.id + "-Intro.mp4",headers={"User-Agent":"Summit-One-illustrated"}),timeout=60) as response:
                source.write_bytes(response.read())
        if sha256(source.read_bytes()).hexdigest() != self.data["legacy_sha256"]:
            raise ValueError(f"{self.id}: source audio must match the reviewed publication")
        file=target/f"{self.id}-Intro-Illustrated.mp4"
        poster=target/f"{self.id}-Intro-Illustrated-poster.jpg"
        width,height=round(1280*self.scale),round(720*self.scale)
        command=["ffmpeg","-nostdin","-v","error","-y","-f","rawvideo","-pixel_format","rgb24",
                 "-video_size",f"{width}x{height}","-framerate",str(FPS),"-i","pipe:0",
                 "-i",str(source),"-map","0:v:0","-map","1:a:0","-c:v","libx264","-crf","20",
                 "-preset","fast","-threads","3","-pix_fmt","yuv420p","-profile:v","high","-level:v","4.1",
                 "-c:a","copy","-movflags","+faststart",str(file)]
        with subprocess.Popen(command,stdin=subprocess.PIPE) as encoder:
            try:
                for frame in range(ceil(self.data["seconds"] * FPS)):
                    encoder.stdin.write(self.frame(frame/FPS).tobytes())
                    if frame and frame%900==0:
                        print(f"{self.id}: {frame//FPS}s rendered",flush=True)
            finally:
                encoder.stdin.close()
            if encoder.wait():
                raise RuntimeError(f"Encoding failed: {self.id}")
        hero = self.scenes[2 if self.id == "S108" else 4]
        moment = Cues(self.scenes[5], self.scenes[5]["start"])
        if self.id == "S142":
            _, word = moment.find("Divide it into three equal parts")
            poster_time = moment.scene["words"][word]["end"] + .35
        else:
            poster_time = hero["speech_end"]-.1
        self.frame(poster_time,False).save(poster,quality=95)
        verified=self.verify(file,source)
        (target/f"{self.id}-qa.json").write_text(json.dumps(verified,indent=2)+"\n")
        print(self.id, "verified H.264 video, source-identical audio and duration",flush=True)

    def verify(self, file, source):
        def audio_hash(media):
            return subprocess.check_output(["ffmpeg","-nostdin","-v","error","-i",str(media),"-map","0:a:0",
                                            "-c:a","copy","-f","hash","-hash","sha256","pipe:"],text=True).strip()

        info=json.loads(subprocess.check_output(["ffprobe","-v","error","-show_streams","-show_format",
                                                "-of","json",str(file)],text=True))
        video,audio=info["streams"]
        assert video["codec_name"]=="h264" and video["pix_fmt"]=="yuv420p"
        assert (video["width"],video["height"],video["avg_frame_rate"])==(1920,1080,"30/1")
        assert audio["codec_name"]=="aac"
        assert abs(float(info["format"]["duration"])-self.data["seconds"])<.08
        assert audio_hash(file)==audio_hash(source)
        subprocess.run(["ffmpeg","-nostdin","-v","error","-xerror","-i",str(file),"-f","null","-"],check=True)
        return {"lesson":self.id,"sha256":sha256(file.read_bytes()).hexdigest(),
                "seconds":self.data["seconds"],"audio_packets":audio_hash(file)}


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("lesson",choices=MOVIES)
    parser.add_argument("--out",type=Path,required=True)
    parser.add_argument("--source",type=Path)
    parser.add_argument("--preview",action="store_true")
    args=parser.parse_args()
    args.out.mkdir(parents=True,exist_ok=True)
    lesson=Lesson(args.lesson,1 if args.preview else 1.5)
    if args.preview:
        lesson.preview(args.out)
    else:
        lesson.render(args.out,args.source or args.out/f"{args.lesson}-original.mp4")
