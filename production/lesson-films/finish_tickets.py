"""Render T05.1 from its approved podium-and-teams master and matching WebVTT.

Run: python production/lesson-films/finish_tickets.py OLD_MP4 OLD_VTT OUTPUT_DIRECTORY
The original is stored at Git revision ef01dbf7. Timing and intact utterances come
from that edition. Everything drawn here was composed for the finish order problem.
"""

import argparse
import bisect
import hashlib
import itertools
import math
import re
import subprocess
import wave
from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ORIGINAL = "1c0ca597aa6f9f5821b3c9b2bba42799749b28af36be5de3fab26d05806b62d6"
CAPTION_HASH = "72f0e6a58fb83b85a27d67a6bef7a0e3d0ccfeae2c60b972dfdbbea78127c894"
SCENES = [0, 16.28, 27, 41.85, 50.98, 64.10, 83.77, 94.82]
SCALE, FPS, FRAMES = 1.5, 30, 3532
PAPER, DARK, TEAL, GOLD, ORANGE = "#f5eedc", "#172f36", "#07665e", "#f0c159", "#c04b32"
OFFWHITE, MUTE, LINE = "#fffcf1", "#3d5756", "#a8b5a1"
NAMES = {"A": "Ava", "B": "Ben", "C": "Cal", "D": "Dee", "E": "Eli", "F": "Fox"}
COLOURS = {
    "A": "#f8c462",
    "B": "#89c4b1",
    "C": "#ef9c7e",
    "D": "#b4bfdf",
    "E": "#d4b4ce",
    "F": "#cfceb1",
}
TITLES = [
    "What changes when two runners swap?",
    "Two tickets, one team",
    "The starter’s question",
    "Fill the finish log",
    "File the finishes as teams",
    "Three names on one roster",
    "Now the jobs are different",
    "Pick the players",
]
FONTROOT = Path("/usr/share/fonts/truetype/dejavu")


@lru_cache(None)
def font(size, family):
    name = {"r": "DejaVuSans", "b": "DejaVuSans-Bold", "s": "DejaVuSerif-Bold", "m": "DejaVuSansMono"}[
        family
    ]
    return ImageFont.truetype(str(FONTROOT / (name + ".ttf")), round(size * SCALE))


def pt(*v):
    return tuple(round(value * SCALE) for value in v)


def txt(draw, x, y, value, size=28, colour=DARK, family="r", anchor="lm"):
    draw.text(pt(x, y), str(value), font=font(size, family), fill=colour, anchor=anchor)


def line(draw, x1, y1, x2, y2, colour=LINE, width=2):
    draw.line(pt(x1, y1, x2, y2), fill=colour, width=max(1, round(width * SCALE)))


def box(draw, x, y, w, h, background=OFFWHITE, edge=None, r=12):
    draw.rounded_rectangle(
        pt(x, y, x + w, y + h),
        radius=round(r * SCALE),
        fill=background,
        outline=edge,
        width=round(2 * SCALE),
    )


def ease(t, a, b):
    v = max(0, min(1, (t - a) / (b - a)))
    return v * v * (3 - 2 * v)


def mix(a, b, x):
    return a + (b - a) * x


def bib(draw, x, y, letter, diameter=64):
    draw.ellipse(
        pt(x - diameter / 2, y - diameter / 2, x + diameter / 2, y + diameter / 2),
        fill=COLOURS[letter],
        outline=DARK,
        width=round(2 * SCALE),
    )
    txt(draw, x, y, letter, diameter * 0.5, DARK, "b", "mm")


def caption_time(raw):
    h, m, s = raw.split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)


def stamp(t):
    ms = round(t * 1000)
    s, ms = divmod(ms, 1000)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return f"{h:02}:{m:02}:{s:02}.{ms:03}"


def captions(src):
    rows = []
    for block in re.split(r"\n\s*\n", src.strip())[1:]:
        timer, *text = block.splitlines()
        a, b = map(caption_time, timer.split(" --> "))
        if 16.28 <= a < 27:
            continue
        if 59.42 <= a < 63:
            a, b = a - 43.14, b - 43.14
        elif 78.84 <= a < 83:
            a, b = a - 58.31, b - 58.31
        rows.append((round(a, 3), round(b, 3), " ".join(text)))
    return sorted(rows)


def make_audio(source, out):
    # Only handle silence and whole utterances. Each boundary includes the
    # surrounding breath/pause, and all other PCM samples are retained exactly.
    cmd = [
        "ffmpeg",
        "-v",
        "error",
        "-i",
        str(source),
        "-map",
        "0:a:0",
        "-f",
        "s16le",
        "-ar",
        "48000",
        "-ac",
        "1",
        "-",
    ]
    raw = subprocess.check_output(cmd)

    def byte(t):
        return 2 * round(t * 48000)

    edited = bytearray(raw)
    for lo, hi in [(15.92, 26.55), (59.18, 63.32), (78.61, 82.94)]:
        edited[byte(lo) : byte(hi)] = bytes(byte(hi) - byte(lo))
    for lo, hi, delta in [(59.18, 63.32, -43.14), (78.61, 82.94, -58.31)]:
        edited[byte(lo + delta) : byte(hi + delta)] = raw[byte(lo) : byte(hi)]
    with wave.open(str(out), "wb") as wav:
        wav.setparams((1, 2, 48000, 0, "NONE", "not compressed"))
        wav.writeframes(edited)


def ticket(draw, x, y, order, width=175):
    box(draw, x, y, width, 62, OFFWHITE, DARK, 5)
    line(draw, x + 13, y + 8, x + 13, y + 54, ORANGE, 3)
    txt(draw, x + 26, y + 32, order[0] + "  →  " + order[1], 25, DARK, "b")


def label(draw, x, y, value):
    txt(draw, x, y, value, 19, TEAL, "b")


def card(draw, x, y, w, h, title):
    box(draw, x, y, w, h, OFFWHITE, LINE)
    label(draw, x + 19, y + 28, title)


def strip(draw, x, y, letters, spacing=72):
    for i, letter in enumerate(letters):
        bib(draw, x + i * spacing, y, letter, 56)


def finals(draw, t):
    card(draw, 65, 201, 553, 297, "FINISH LINE")
    card(draw, 658, 201, 552, 297, "TEAM LIST")
    for i, letter in enumerate("AB"):
        pos = ease(t, 9.3, 11.9)
        x = mix(214 + i * 236, 450 - i * 236, pos)
        bib(draw, x, 325 + (1 if i else -1) * 82 * math.sin(pos * math.pi), letter, 76)
        txt(draw, 214 + i * 236, 417, ["1st", "2nd"][i], 32, DARK, "s", "mm")
    strip(draw, 857, 342, "AB", 138)
    line(draw, 793, 402, 1069, 402, TEAL, 3)
    txt(draw, 931, 438, "Same two runners", 25, DARK, "r", "mm")
    txt(draw, 65, 549, "Read the finish by place. Read the team by its members.", 27, MUTE)


def file_tickets(draw, t):
    label(draw, 65, 199, "FINISH TICKETS")
    label(draw, 692, 199, "TEAM ENVELOPE")
    fold = ease(t, 17.7, 19.8)
    box(draw, 711, 252, 387, 153, TEAL)
    for i, order in enumerate(["AB", "BA"]):
        ticket(draw, mix(77, 726 + 177 * i, fold), mix(244 + 100 * i, 231, fold), order, 165)
    draw.polygon([pt(712, 283), pt(904, 337), pt(1097, 283), pt(1097, 397), pt(712, 397)], fill=TEAL)
    line(draw, 715, 283, 905, 337, "#92c9b4", 4)
    line(draw, 1094, 283, 905, 337, "#92c9b4", 4)
    txt(draw, 907, 375, "AVA  +  BEN", 29, OFFWHITE, "b", "mm")
    if t >= 20.35:
        txt(draw, 72, 479, "Two orders for two distinct runners", 35, DARK, "s")
        txt(draw, 72, 542, "For three distinct runners, try ABC, ACB, BAC, BCA, CAB and CBA.", 25, MUTE)


def starter(draw, t):
    card(draw, 65, 196, 402, 357, "START LIST")
    for i, letter in enumerate("ABC"):
        y = 283 + 85 * i
        bib(draw, 128, y, letter, 54)
        txt(draw, 183, y, NAMES[letter], 34, DARK, "s")
    card(draw, 520, 196, 691, 156, "RESULT 1")
    txt(draw, 546, 304, "First place: ____     Second: ____", 28, DARK, "b")
    if t >= 31.2:
        card(draw, 520, 372, 691, 181, "RESULT 2")
        txt(draw, 545, 465, "Team members: ____  and  ____", 29, DARK, "b")
    if t >= 37.9:
        txt(draw, 65, 590, "Try listing the finishes and the teams.", 28, TEAL, "b")


def finish_log(draw, t):
    card(draw, 65, 191, 1143, 360, "FIRST RUNNER")
    label(draw, 438, 219, "POSSIBLE SECOND RUNNERS")
    for row, first in enumerate("ABC"):
        y = 281 + 90 * row
        bib(draw, 178, y + 5, first, 55)
        for col, second in enumerate(c for c in "ABC" if c != first):
            if t >= 42 + row * 0.6 + col * 0.32:
                ticket(draw, 449 + col * 273, y - 21, (first, second), 204)
    if t >= 47.2:
        txt(draw, 65, 590, "3 first-place choices × 2 remaining choices = 6 finishes", 29, TEAL, "b")


def team_files(draw, t):
    for i, pair in enumerate(["AB", "AC", "BC"]):
        x = 66 + 389 * i
        card(draw, x, 203, 357, 323, "TEAM  " + NAMES[pair[0]].upper() + " + " + NAMES[pair[1]].upper())
        p = ease(t, 54 + i * 0.34, 57.7 + i * 0.34)
        ticket(draw, x + 29, 261 + 62 * p, pair, 146)
        ticket(draw, x + 177, 261 + 62 * p, pair[::-1], 146)
        if p > 0.3:
            line(draw, x + 35, 412, x + 322, 412, TEAL, 3)
            txt(draw, x + 180, 461, "One pair", 30, TEAL, "s", "mm")
    txt(
        draw,
        67,
        576,
        (
            "Spot the two finishes in each file."
            if t >= 59
            else "Read one ticket, then reverse the order."
        ),
        27,
        MUTE,
    )


def team_three(draw, t):
    card(draw, 65, 195, 484, 337, "ONE TEAM: AVA, BEN AND CAL")
    for i, perm in enumerate(itertools.permutations("ABC")):
        x = 91 + (i % 2) * 215
        y = 285 + (i // 2) * 73
        strip(draw, x + 18, y, "".join(perm), 50)
    if t >= 68:
        card(draw, 570, 195, 637, 337, "ALL THREE-PERSON TEAMS FROM FIVE RUNNERS")
        for i, team in enumerate(itertools.combinations("ABCDE", 3)):
            if t >= 68 + i * 0.49:
                x = 597 + (i % 5) * 118
                y = 291 + (i // 5) * 95
                box(draw, x, y, 106, 55, "#ddece1", LINE, 5)
                txt(draw, x + 53, y + 28, "".join(team), 25, DARK, "m", "mm")
    if t >= 76.5:
        txt(draw, 65, 582, "60 ordered finishes ÷ 6 orders per team = 10 teams", 30, TEAL, "b")


def roles(draw, t):
    progress = ease(t, 88.3, 90.3)
    for i, role in enumerate(["Captain", "Scorer", "Timekeeper"]):
        x = 65 + 388 * i
        card(draw, x, 216, 356, 262, "JOB " + str(i + 1))
        txt(draw, x + 178, 445, role, 34, DARK, "s", "mm")
    for i, letter in enumerate("ABC"):
        x = 245 + 388 * i
        dest = (633, 245, 1021)[i]
        bib(
            draw,
            mix(x, dest, progress),
            346 + (1 if i == 1 else -1) * 52 * math.sin(progress * math.pi),
            letter,
            79,
        )
    txt(draw, 65, 566, "5 choices × 4 choices × 3 choices = 60 assignments", 29, TEAL, "b")


def selection(draw, t):
    for i, letter in enumerate("ABCDEF"):
        bib(draw, 136 + i * 199, 244, letter, 67)
    card(draw, 65, 317, 544, 190, "CAPTAIN AND VICE-CAPTAIN")
    txt(draw, 89, 415, "Two different jobs", 31, DARK, "s")
    card(draw, 650, 317, 555, 190, "TWO EQUIPMENT CARRIERS")
    txt(draw, 676, 415, "One team of two", 31, DARK, "s")
    if t >= 114.4:
        txt(draw, 65, 574, "Check: 6 × 5 = 30 role assignments.     30 ÷ 2 = 15 teams.", 28, TEAL, "b")
    elif t >= 102.8:
        txt(draw, 65, 574, "Try both counts in your notebook.", 28, TEAL, "b")


RENDERERS = [finals, file_tickets, starter, finish_log, team_files, team_three, roles, selection]


@lru_cache(None)
def background(n):
    im = Image.new("RGB", pt(1280, 720), PAPER)
    draw = ImageDraw.Draw(im)
    draw.rectangle(pt(0, 0, 1280, 20), fill=TEAL)
    for x in range(16, 1280, 56):
        line(draw, x, 2, x + 18, 17, "#80b7a1", 3)
    txt(draw, 65, 66, "FIELD NOTES   /   ATHLETICS", 21, TEAL, "b")
    txt(draw, 1208, 66, "FINISH DESK   •   " + str(n + 1) + " / 8", 20, MUTE, "m", "rm")
    txt(draw, 64, 133, TITLES[n], 46, DARK, "s")
    line(draw, 66, 178, 1209, 178, LINE, 2)
    draw.rectangle(pt(0, 624, 1280, 720), fill=DARK)
    return im


def render(t, cues):
    n = max(0, bisect.bisect_right(SCENES, t) - 1)
    im = background(n).copy()
    draw = ImageDraw.Draw(im)
    RENDERERS[n](draw, t)
    for a, b, words in cues:
        if a <= t < b:
            size = 39
            while draw.textlength(words, font(size, "r")) > 1780:
                size -= 1
            txt(draw, 640, 672, words, size, OFFWHITE, "r", "mm")
            break
    return im


def run():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("original", type=Path)
    parser.add_argument("captions", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--boards", action="store_true", help="Build the poster and scene checks only.")
    args = parser.parse_args()
    if (
        hashlib.sha256(args.original.read_bytes()).hexdigest() != ORIGINAL
        or hashlib.sha256(args.captions.read_bytes()).hexdigest() != CAPTION_HASH
    ):
        raise ValueError("Supply the verified podium-and-teams master and its matching captions")
    out = args.output
    out.mkdir(parents=True, exist_ok=True)
    cues = captions(args.captions.read_text())
    (out / "T05.1.vtt").write_text(
        "WEBVTT\n\n" + "\n\n".join(f"{stamp(a)} --> {stamp(b)}\n{text}" for a, b, text in cues) + "\n"
    )
    render(15.75, cues).save(out / "T05.1-studio-poster.jpg", quality=91)
    if args.boards:
        times = [9.0, 18.5, 34, 48, 59.5, 80, 90, 115.8]
        board = Image.new("RGB", (960, 540), PAPER)
        for i, t in enumerate(times):
            board.paste(
                render(t, cues).resize((240, 135), Image.Resampling.LANCZOS),
                ((i % 4) * 240, (i // 4) * 270 + 65),
            )
        board.save(out / "board.jpg", quality=92)
        return
    make_audio(args.original, out / "voice.wav")
    cmd = [
        "ffmpeg",
        "-v",
        "error",
        "-y",
        "-f",
        "rawvideo",
        "-pix_fmt",
        "rgb24",
        "-s",
        "1920x1080",
        "-r",
        "30",
        "-i",
        "-",
        "-i",
        str(out / "voice.wav"),
        "-map",
        "0:v",
        "-map",
        "1:a",
        "-vf",
        "format=yuv420p",
        "-c:v",
        "libx264",
        "-threads",
        "4",
        "-preset",
        "veryfast",
        "-crf",
        "18",
        "-c:a",
        "aac",
        "-b:a",
        "144k",
        "-movflags",
        "+faststart",
        "-t",
        str(FRAMES / FPS),
        str(out / "T05.1.mp4"),
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for f in range(FRAMES):
        proc.stdin.write(render(f / FPS, cues).tobytes())
    proc.stdin.close()
    if proc.wait():
        raise RuntimeError("Full HD film encoding failed")


if __name__ == "__main__":
    run()
