"""Correct the caption in lesson 78 and preserve the original Voice C audio packets."""
import argparse
from bisect import bisect_right
from hashlib import sha256
import json
import math
from pathlib import Path
import subprocess
from urllib.request import urlopen

from render import Lesson, RELEASE

SOURCE = "S078-Intro-Illustrated"
EXPECTED = "da573641eae9c2c9ed35e3d75e63226228cd714c1fa753a819e6b4c21b524d7f"
FPS = 30

def call(args):
    return subprocess.check_output(args)

def probe(stream, fields, path):
    return json.loads(call(["ffprobe", "-v", "error", "-select_streams", stream,
                            "-show_entries", fields, "-of", "json", str(path)]))

def audio_hash(path):
    return call(["ffmpeg", "-v", "error", "-i", str(path), "-map", "0:a:0",
                 "-c:a", "copy", "-f", "hash", "-hash", "sha256", "-"])

def render(source, folder):
    folder.mkdir(parents=True, exist_ok=True)
    if not source.exists():
        source.write_bytes(urlopen(RELEASE + SOURCE + ".mp4", timeout=90).read())
    assert sha256(source.read_bytes()).hexdigest() == EXPECTED
    lesson = Lesson("S078")
    cue = next(c for c in lesson.captions if c["start"] == 61.37)
    assert cue["text"] == "An eleven-by-nine rectangle has a right triangle removed"
    packets = probe("v:0", "packet=pts_time,flags:stream=nb_frames,time_base", source)
    frames = int(packets["streams"][0]["nb_frames"])
    keys = sorted(round(float(p["pts_time"]) * FPS) for p in packets["packets"] if "K" in p["flags"])
    start, stop = math.ceil(cue["start"] * FPS), math.ceil(cue["end"] * FPS)
    g0, g1 = keys[bisect_right(keys, start)-1], keys[bisect_right(keys, stop)]
    run = ["ffmpeg", "-v", "error", "-xerror", "-nostdin", "-y"]
    call(run + ["-i", str(source), "-map", "0:v:0", "-c", "copy", "-f", "segment",
                "-segment_frames", f"{g0},{g1}", "-reset_timestamps", "1", "-avoid_negative_ts", "disabled",
                str(folder/"part%d.mp4")])
    counts = [int(probe("v:0", "stream=nb_frames", folder/f"part{n}.mp4")["streams"][0]["nb_frames"]) for n in range(3)]
    assert counts == [g0, g1-g0, frames-g1], (counts, g0, g1)
    # The native caption band is the only layer changed. All other GOPs pass through intact.
    band = folder/"band.rgb"
    with band.open("wb") as output:
        for n in range(start, stop):
            output.write(lesson.frame(n / FPS).crop((0,906,1920,1080)).tobytes())
    edited = folder/"edited.mp4"
    offset = (start-g0)/FPS
    filtergraph = (f"[0:v]setpts=PTS-STARTPTS[original];[1:v]setpts=PTS+{offset:.9f}/TB[caption];"
                   f"[original][caption]overlay=0:906:eof_action=pass:repeatlast=0:"
                   f"enable='gte(n,{start-g0})*lt(n,{stop-g0})'[v]")
    denom = packets["streams"][0]["time_base"].split("/")[1]
    call(run + ["-i",str(folder/"part1.mp4"),"-f","rawvideo","-pix_fmt","rgb24","-s","1920x174",
                "-r",str(FPS),"-i",str(band),"-filter_complex_threads","1","-filter_complex",filtergraph,
                "-map","[v]","-an","-c:v","libx264","-threads","3","-crf","17","-preset","fast",
                "-profile:v","high","-level:v","4.1","-pix_fmt","yuv420p","-video_track_timescale",denom,str(edited)])
    assert int(probe("v:0","stream=nb_frames",edited)["streams"][0]["nb_frames"]) == g1-g0
    join = folder/"parts.txt"
    join.write_text("".join(f"file '{name}'\nduration {length / FPS:.9f}\n"
                            for name,length in zip(("part0.mp4","edited.mp4","part2.mp4"),counts)))
    destination=folder/(SOURCE+"-v2.mp4")
    call(run+["-f","concat","-safe","0","-i",str(join),"-i",str(source),
              "-map","0:v:0","-map","1:a:0","-c","copy","-movflags","+faststart","-video_track_timescale",denom,str(destination)])
    verify = probe("v:0","packet=pts_time:stream=nb_frames,width,height,duration",destination)
    times = sorted(float(p["pts_time"]) for p in verify["packets"])
    assert len(times) == frames and max(abs(t - n / FPS) for n,t in enumerate(times)) < .001, (len(times), times[:4], times[-4:])
    assert audio_hash(source) == audio_hash(destination)
    call(run+["-i",str(destination),"-map","0:v:0","-map","0:a:0","-f","null","-"])
    print(json.dumps(dict(sha256=sha256(destination.read_bytes()).hexdigest(), frames=frames,
                          corrected_caption_frames=stop-start, original_audio_packets=True)),flush=True)

if __name__=="__main__":
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument("source",type=Path)
    cli.add_argument("folder",type=Path)
    args=cli.parse_args()
    render(args.source,args.folder)
