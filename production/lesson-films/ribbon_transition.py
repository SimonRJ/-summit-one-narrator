"""Restore a readable handover from the ribbon question to its worked calculation."""

import hashlib
from pathlib import Path
import re
import subprocess
from tempfile import TemporaryDirectory
from PIL import Image

ORIGINAL_SHA = "de26a263cf9c51fa08f8a1ae107ae310baa9572c12a0392c06907d3a2258af14"
Y, HEIGHT = 700, 154
START, END = 96.9, 98.1
FRAMES = 4804


def strip(source, t):
    raw = subprocess.check_output(
        [
            "ffmpeg",
            "-v",
            "error",
            "-ss",
            str(t),
            "-i",
            str(source),
            "-frames:v",
            "1",
            "-vf",
            f"crop=1920:{HEIGHT}:0:{Y},format=rgb24",
            "-f",
            "rawvideo",
            "-",
        ]
    )
    return Image.frombytes("RGB", (1920, HEIGHT), raw)


def ease(v):
    v = max(0, min(1, v))
    return v * v * (3 - 2 * v)


def render(original, final):
    with original.open("rb") as f:
        assert hashlib.file_digest(f, "sha256").hexdigest() == ORIGINAL_SHA
    # Sample the exact public lettering and matte while the cue is held and before it appears.
    plain, question, answer = [strip(original, t) for t in (87.5, 96.50, 98.40)]
    graph = f"[1:v]setpts=PTS-STARTPTS+{START}/TB[band];[0:v][band]overlay=0:{Y}:enable='between(t,{START},{END})':eof_action=repeat,format=yuv420p[film]"
    cmd = [
        "ffmpeg",
        "-v",
        "error",
        "-y",
        "-nostdin",
        "-threads",
        "2",
        "-i",
        str(original),
        "-f",
        "rawvideo",
        "-pix_fmt",
        "rgb24",
        "-s",
        f"1920x{HEIGHT}",
        "-r",
        "30",
        "-i",
        "-",
        "-filter_complex_threads",
        "2",
        "-filter_complex",
        graph,
        "-map",
        "[film]",
        "-map",
        "0:a:0",
        "-frames:v",
        str(FRAMES),
        "-c:v",
        "libx264",
        "-threads",
        "3",
        "-preset",
        "veryfast",
        "-crf",
        "16",
        "-c:a",
        "copy",
        "-movflags",
        "+faststart",
        str(final),
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(round((END - START) * 30) + 1):
        t = START + i / 30
        combined = ease((t - 96.96) / 1.05)
        if combined < 0.5:
            frame = Image.blend(question, plain, ease(2 * combined))
        else:
            frame = Image.blend(plain, answer, ease(2 * combined - 1))
        proc.stdin.write(frame.tobytes())
    proc.stdin.close()
    if proc.wait():
        raise RuntimeError("Ribbon sequence could not be encoded")
    with TemporaryDirectory() as temp:
        stats = Path(temp) / "ssim.log"
        mask = f"drawbox=x=0:y={Y}:w=1920:h={HEIGHT}:color=black:t=fill:enable='between(t,{START - 0.05},{END + 0.05})',scale=256:144,format=gray"
        chk = [
            "ffmpeg",
            "-v",
            "error",
            "-threads",
            "2",
            "-i",
            str(original),
            "-threads",
            "2",
            "-i",
            str(final),
            "-filter_complex_threads",
            "2",
            "-filter_complex",
            f"[0:v]{mask}[original];[1:v]{mask}[corrected];[original][corrected]ssim=stats_file={stats}",
            "-an",
            "-f",
            "null",
            "-",
        ]
        subprocess.run(chk, check=True)
        score = [
            float(re.search(r"All:([.0-9]+)", l)[1])
            for l in stats.read_text().splitlines()
        ]
    assert len(score) == FRAMES and min(score) > 0.975, (len(score), min(score))
    return {
        "original_mp4_sha256": ORIGINAL_SHA,
        "modified_region": {
            "x": 0,
            "y": Y,
            "width": 1920,
            "height": HEIGHT,
            "start": START,
            "end": END,
        },
        "frame_count": len(score),
        "minimum_frame_ssim_outside_patch_at_256x144": min(score),
        "mean_frame_ssim_outside_patch_at_256x144": round(sum(score) / len(score), 7),
        "transition": "The question fades completely before the area is used by the worked 200 cm + 30 cm = 230 cm calculation.",
    }
