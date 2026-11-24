"""Re-stage the restricted-number and reversible-seating films using their approved audio."""

from bisect import bisect_right
import argparse
import hashlib
from itertools import permutations
import json
from math import ceil
from pathlib import Path
import re
import subprocess
from PIL import Image, ImageDraw
from finish_tickets import txt, box, line, pt, ease, mix, font, caption_time

ROOT = Path(__file__).resolve().parents[2]
EDITIONS = {
    "T05.2": (
        "number-press",
        "319b5d1491e4f7a122ff9247f57672cbff6d77a9677211a6a550c9d78c8f20ba",
    ),
    "T05.3": (
        "seat-bookings",
        "a06c2e4f882687fd5030f1075031d4864b40eb19ed7760d6926cc7f18a147656",
    ),
}
INK, STEEL, CREAM, GREEN, AMBER, RUST = (
    "#16333d",
    "#30808c",
    "#fff4d4",
    "#12634d",
    "#ffce71",
    "#ad432c",
)
PINK, LIGHT, PLUM, TEAL = "#eed1bd", "#fffbf1", "#473445", "#256460"


def middle(d, x, y, s, size=30, colour=INK, face="b"):
    txt(d, x, y, s, size, colour, face, "mm")


def press(d, x, y, values, w=490):
    """A fixed point of registration sits in front of three removable type drums."""
    h = w * 0.53
    box(d, x, y, w, h, INK, "#51777a", 20)
    gap = w * 0.035
    slot = (w - 4 * gap) / 3
    for i, val in enumerate(values):
        xx = x + gap + i * (slot + gap)
        box(d, xx, y + h * 0.19, slot, h * 0.64, CREAM, "#a88d50", 7)
        line(d, xx + 4, y + h * 0.29, xx + slot - 4, y + h * 0.29, "#c5b69c")
        line(d, xx + 4, y + h * 0.72, xx + slot - 4, y + h * 0.72, "#c5b69c")
        middle(
            d, xx + slot / 2, y + h * 0.49, val, w * 0.13, RUST if val == "0" else INK
        )
    for xx in (x + gap / 2, x + w - gap / 2):
        for yy in (y + h * 0.12, y + h * 0.88):
            d.ellipse(pt(xx - 3, yy - 3, xx + 3, yy + 3), fill=AMBER)
    middle(
        d,
        x + w / 2,
        y + h * 0.92,
        "HUNDREDS      TENS      ONES",
        w * 0.033,
        CREAM,
        "m",
    )


def number_heading(d, title):
    txt(d, 58, 51, "TYPE ROOM   /   RESTRICTED NUMBERS", 23, STEEL, "b")
    txt(d, 58, 115, title, 53, INK, "s")
    line(d, 60, 162, 1220, 162, STEEL, 4)


def tray(d, x, y, label, items, active):
    box(d, x, y, 520, 110, "#e1dec2", "#757b67", 5)
    txt(d, x + 18, y + 29, label, 22, INK, "b")
    for j, item in enumerate(items):
        if active > j:
            middle(
                d,
                x + 70 + 130 * j,
                y + 76 - 32 * (1 - ease(active - j, 0, 0.75)),
                item,
                39,
                INK,
                "m",
            )


def circuit(d, x, y, one, two, cross):
    box(d, x, y, 234, 174, "#26414a", "#7ca2a2", 13)
    for i, on in enumerate((one, two)):
        xx = x + 67 + i * 100
        box(d, xx - 24, y + 25, 48, 80, "#101f28", None, 22)
        d.ellipse(
            pt(xx - 17, y + (31 if on else 66), xx + 17, y + (65 if on else 100)),
            fill=AMBER if on else "#879693",
        )
        middle(d, xx, y + 133, "ON" if on else "OFF", 20, LIGHT, "m")
    if cross:
        line(d, x + 12, y + 156, x + 223, y + 14, "#ff9273", 7)


def number_scene(d, i, t):
    titles = [
        "Sort by the final digit",
        "What changes the choices?",
        "Set the number press",
        "Zero has a special job",
        "Count each print run",
        "Combine the print runs",
        "Switch off one setting",
        "Try a two-digit print run",
    ]
    number_heading(d, titles[i])
    if i == 0:
        press(d, 70, 205, ("1", "2", "0"), 415)
        for j, (label, items) in enumerate(
            [
                ("ENDS IN ZERO", ["120", "310", "420"]),
                ("ENDS IN TWO OR FOUR", ["102", "134", "402"]),
            ]
        ):
            tray(d, 665, 210 + 154 * j, label, items, max(0, (t - 3 - j) * 0.8))
        if t > 7:
            txt(d, 70, 505, "Each number has one final digit.", 32, INK, "s")
    elif i == 1:
        for j, (end, leading) in enumerate([("0", "1  2  3  4"), ("2", "1  3  4")]):
            x = 92 + j * 610
            press(d, x, 196, ("?", "?", end), 440)
            txt(d, x, 475, "Hundreds digit", 26, STEEL, "b")
            if t > 14:
                txt(d, x, 536, leading, 45, INK, "m")
        if t > 20:
            middle(d, 640, 597, "The number of legal first digits changes.", 29, RUST)
    elif i == 2:
        press(d, 86, 220, ("?", "?", "?"), 570)
        txt(d, 775, 241, "Type available", 28, STEEL, "b")
        txt(d, 775, 317, "0 1 2 3 4", 48, INK, "m")
        txt(d, 775, 404, "Three digits", 31, INK, "s")
        txt(d, 775, 452, "Even • no repeats", 31, INK, "s")
        if t > 34:
            txt(d, 86, 563, "Which drum would you set first?", 32, RUST, "s")
    elif i == 3:
        press(
            d,
            74,
            235,
            ("?", "?", ("0", "2", "4")[min(2, int(max(0, t - 40) / 1.25))]),
            490,
        )
        tray(d, 655, 209, "ENDS IN ZERO", ["120"], 1)
        tray(d, 655, 361, "ENDS IN TWO OR FOUR", ["132", "304"], 2)
        if t > 45:
            txt(d, 74, 557, "Zero cannot lead a three-digit number.", 30, RUST, "s")
    elif i == 4:
        last = "0" if t < 61.31 else ("2" if t < 68 else "4")
        press(d, 72, 206, ("?", "?", last), 470)
        txt(d, 655, 227, "Last digit fixed at " + last, 31, STEEL, "b")
        txt(d, 655, 301, "Hundreds digit", 25, INK, "b")
        legal = {"0": "1  2  3  4", "2": "1  3  4", "4": "1  2  3"}[last]
        txt(d, 655, 363, legal, 44, INK, "m")
        if t > 57.35:
            txt(d, 655, 441, "Tens digit: 3 remaining digits", 29, INK)
        if 58.15 < t < 61.31:
            middle(
                d,
                640,
                557,
                "1 ending × 4 first digits × 3 middle digits = 12",
                34,
                GREEN,
            )
        if t > 69.8:
            middle(
                d,
                640,
                557,
                "2 endings × 3 first digits × 3 middle digits = 18",
                34,
                GREEN,
            )
    elif i == 5:
        tray(d, 70, 224, "ENDS IN ZERO", ["120", "130", "140"], 3)
        tray(d, 680, 224, "ENDS IN TWO OR FOUR", ["102", "104", "132"], 3)
        middle(d, 330, 406, "12 numbers", 41, INK)
        middle(d, 940, 406, "18 numbers", 41, INK)
        if t > 78.36:
            middle(d, 640, 552, "12 + 18 = 30 even numbers", 44, GREEN)
    elif i == 6:
        for j, (a, b) in enumerate(
            [(False, False), (False, True), (True, False), (True, True)]
        ):
            circuit(d, 71 + j * 303, 248, a, b, j == 3 and t >= 87.75)
        if t > 89.45:
            middle(d, 640, 529, "4 settings − 1 forbidden setting = 3", 39, GREEN)
    else:
        if t < 103.1:
            txt(d, 90, 250, "1    Split by the ending.", 38, INK, "s")
            if t > 99.6:
                txt(d, 90, 349, "2    Multiply inside each case.", 38, STEEL, "s")
            if t > 101.9:
                txt(d, 90, 449, "3    Add the case totals.", 38, GREEN, "s")
        else:
            for j, n in enumerate(("TENS", "ONES")):
                x = 105 + j * 319
                box(d, x, 211, 249, 210, INK, None, 12)
                middle(d, x + 124, 298, "?", 80, CREAM)
                middle(d, x + 124, 384, n, 25, AMBER, "m")
            txt(d, 783, 254, "Use two different digits.", 32, INK, "s")
            txt(d, 783, 354, "Can zero be first?", 29, RUST)
            if t > 108:
                txt(d, 783, 441, "Try 9 × 9 in your notebook.", 27, STEEL)


def coach(d):
    box(d, 55, 186, 1170, 284, "#286468", "#194647", 38)
    for i in range(5):
        x = 102 + i * 223
        box(d, x, 207, 187, 113, "#cee3db", "#e2be81", 9)
        line(d, x + 90, 212, x + 90, 313, "#98b8b5", 3)
    line(d, 79, 447, 1200, 447, "#e9be79", 7)
    for xx in (141, 1150):
        d.ellipse(pt(xx - 21, 447, xx + 21, 489), fill="#29383a")
        d.ellipse(pt(xx - 8, 461, xx + 8, 477), fill="#a99f89")


def passenger(d, x, y, n):
    fill = "#e8b87b" if n in "ABC" else "#b9d9db"
    box(d, x - 43, y - 41, 86, 79, fill, PLUM, 14)
    middle(d, x, y, n, 47, PLUM, "s")


def seat_row(d, order, y=378, enter=1):
    coach(d)
    for i, n in enumerate(order):
        x = 195 + i * 223
        box(d, x - 63, y + 20, 126, 22, "#ead6aa", "#704c38", 8)
        if n != " " and enter > i / 8:
            progress = ease(enter, i / 8, i / 8 + 0.40)
            passenger(d, x, y - 14 - 78 * (1 - progress), n)


def rail_heading(d, title):
    txt(d, 60, 49, "CARRIAGE RESERVATIONS   /   FIVE PASSENGERS", 22, TEAL, "b")
    txt(d, 60, 113, title, 52, PLUM, "s")
    line(d, 62, 158, 1217, 158, "#bf956c", 3)


def girls_gaps(d, shown, boys=()):
    for j, s in enumerate("ABC"):
        x = 320 + j * 320
        box(d, x - 65, 341, 130, 24, "#86583d", None, 8)
        passenger(d, x, 299, s)
    positions = (160, 480, 800, 1120)
    for j, x in enumerate(positions):
        if shown:
            line(d, x, 355, x, 401, "#9b734f", 4)
            middle(d, x, 429, "gap " + str(j + 1), 26, TEAL)
    for symbol, gap, y in boys:
        passenger(d, positions[gap - 1], y, symbol)


def spine(d, x, y, w, h, letter, colour):
    box(d, x, y, w, h, colour, PLUM, 6)
    for k in (18, h - 20):
        line(d, x + 5, y + k, x + w - 5, y + k, "#f0d397", 2)
    middle(d, x + w / 2, y + h / 2, letter, 42, LIGHT, "s")


def seat_scene(d, i, t):
    titles = [
        "Give a row a return address",
        "Read the booking record",
        "Find a legal seating",
        "Reserve the girls’ order first",
        "Two bookings in different gaps",
        "Read the seats backwards",
        "Count the adjacent bookings",
        "Transfer the idea to a bookshelf",
    ]
    rail_heading(d, titles[i])
    if i in (0, 1, 2):
        order = (
            "ADBCE"
            if i != 2
            else ("     " if t < 28 else ("ABCDE" if t < 33 else "ADBCE"))
        )
        seat_row(
            d,
            order,
            enter=ease(t, 0.5, 4.6)
            if i == 0
            else (ease(t, 27.9, 30.3) if i == 2 and t < 33 else 1),
        )
        if i == 0:
            middle(
                d,
                640,
                543,
                "Row A D B C E   ↔   A B C  •  D in gap 2  •  E in gap 4",
                30,
                TEAL,
            )
        if i == 1:
            labels = (
                "Read the row from left to right.",
                "First record the girls’ order: A B C.",
                "Then record the two gaps: D in 2, E in 4.",
            )
            middle(
                d, 640, 543, labels[0 if t < 18.7 else (1 if t < 21 else 2)], 32, TEAL
            )
            if t > 18.7:
                for j in (0, 2, 3) if t < 21 else (1, 4):
                    x = 195 + j * 223
                    line(d, x - 38, 417, x + 38, 417, "#f6d084", 5)
        if i == 2:
            if 30.3 <= t < 33:
                line(d, 826, 415, 1142, 415, "#f6d084", 7)
            msg = (
                "Girls  A, B, C      Boys  D, E"
                if t < 30.3
                else (
                    "Adjacent D and E break the rule."
                    if t < 33
                    else "A legal row. How many legal rows are there?"
                )
            )
            middle(d, 640, 543, msg, 31, PLUM)
    elif i == 3:
        girls_gaps(d, t >= 47.7)
        if t >= 44.8:
            middle(d, 640, 543, "ABC   ACB   BAC   BCA   CAB   CBA", 35, PLUM, "m")
    elif i == 4:
        boys = []
        if t > 54.55:
            boys.append(("D", 2, mix(200, 299, ease(t, 54.55, 55.6))))
        if t > 57.05:
            boys.append(("E", 4, mix(200, 299, ease(t, 57.05, 58.1))))
        girls_gaps(d, True, boys)
        middle(
            d,
            640,
            542,
            "6 girl orders × 4 first gaps × 3 remaining gaps = 72"
            if t > 59.4
            else "The second boy needs a different gap.",
            32,
            TEAL,
        )
    elif i == 5:
        if t < 67.25:
            seat_row(d, "ADBCE")
        else:
            a = ease(t, 67.25, 69.15)
            girls_gaps(
                d, True, [("D", 2, mix(299, 211, a)), ("E", 4, mix(299, 211, a))]
            )
        middle(
            d,
            640,
            536,
            "A B C   •   D in gap 2   •   E in gap 4"
            if t > 69.6
            else "Start with one complete legal row.",
            33,
            TEAL,
        )
    elif i == 6:
        seat_row(d, "ABCED" if t > 88.29 else "ABCDE")
        if t > 85:
            x = 195 + 3 * 223
            box(d, x - 62, 409, 350, 25, "#e8b87b", None, 3)
            middle(d, x + 111, 421, "ONE ATTACHED PAIR", 15, PLUM)
        msg = (
            "5! = 120 possible rows"
            if t < 85
            else (
                "4! × 2 = 48 adjacent rows" if t < 94.8 else "120 − 48 = 72 legal rows"
            )
        )
        middle(d, 640, 543, msg, 41, TEAL)
    else:
        if t < 107.48:
            girls_gaps(d, True, [("D", 2, 299), ("E", 4, 299)])
            middle(
                d,
                640,
                552,
                "Can you rebuild the row from its booking record?",
                33,
                TEAL,
            )
        else:
            for j, (letter, co, h) in enumerate(
                [
                    ("A", "#754c56", 188),
                    ("C", "#327778", 171),
                    ("B", "#97542e", 208),
                    ("D", "#515b81", 185),
                ]
            ):
                spine(d, 151 + j * 94, 438 - h, 82, h, letter, co)
            box(d, 112, 439, 450, 19, "#8b5e43", None, 4)
            txt(d, 665, 256, "Four different books", 36, PLUM, "s")
            txt(d, 665, 345, "Keep A and B apart.", 33, TEAL, "b")
            txt(d, 665, 437, "How many shelf orders work?", 30, PLUM)
            if t > 116:
                txt(d, 665, 520, "Check all orders minus adjacent orders.", 23, TEAL)


def make_picture(k, index, t, caption):
    im = Image.new("RGB", (1920, 1080), "#f3edda" if k == "T05.2" else "#fcf3e6")
    d = ImageDraw.Draw(im)
    (number_scene if k == "T05.2" else seat_scene)(d, index, t)
    d.rectangle((0, 930, 1919, 1079), fill=INK if k == "T05.2" else PLUM)
    if caption:
        size = 39
        while d.textlength(caption, font=font(size, "r")) > 1824:
            size -= 1
        d.text((960, 1004), caption, anchor="mm", font=font(size, "r"), fill=LIGHT)
    return im


def prove():
    nums = [
        100 * a + 10 * b + c
        for a, b, c in permutations(range(5), 3)
        if a and c % 2 == 0
    ]
    assert len([n for n in nums if n % 10 == 0]) == 12 and len(nums) == 30
    seats = [p for p in permutations("ABCDE") if abs(p.index("D") - p.index("E")) > 1]

    def record(p):
        return tuple(n for n in p if n in "ABC"), tuple(
            sum(x in "ABC" for x in p[: p.index(n)]) + 1 for n in "DE"
        )

    assert len(seats) == len(set(map(record, seats))) == 72
    assert (
        len([p for p in permutations("ABCD") if abs(p.index("A") - p.index("B")) > 1])
        == 12
    )


def render_visual(lesson, folder, source_digest, draw):
    k = lesson
    folder.mkdir(parents=True, exist_ok=True)
    original = ROOT / "media" / (k + ".mp4")
    qa = json.loads((ROOT / "review" / (k + "-studio-qa.json")).read_text())
    assert (
        hashlib.file_digest(original.open("rb"), "sha256").hexdigest()
        == qa["sha256"]
        == source_digest
    )
    parts = []
    for block in re.split(
        r"\n\s*\n", (ROOT / "media" / (k + ".vtt")).read_text().strip()
    )[1:]:
        marks, *copy = block.splitlines()
        a, b = map(caption_time, marks.split(" --> "))
        parts.append((a, b, " ".join(copy)))
    starts = [r["start"] for r in qa["scenes"]]
    cue_starts = [row[0] for row in parts]

    def paint(t):
        ix = bisect_right(cue_starts, t) - 1
        caption = parts[ix][2] if ix >= 0 and t < parts[ix][1] else ""
        return draw(k, max(0, bisect_right(starts, t) - 1), t, caption)

    paint(9).save(folder / (k + "-studio-poster.jpg"), quality=90)
    frames = round(qa["duration_seconds"] * 30)
    cmd = [
        "ffmpeg",
        "-nostdin",
        "-loglevel",
        "error",
        "-y",
        "-f",
        "rawvideo",
        "-pix_fmt",
        "rgb24",
        "-s",
        "1920x1080",
        "-r",
        "15",
        "-i",
        "-",
        "-i",
        str(original),
        "-map",
        "0:v",
        "-map",
        "1:a",
        "-vf",
        "fps=30,format=yuv420p",
        "-frames:v",
        str(frames),
        "-c:v",
        "libx264",
        "-threads",
        "3",
        "-preset",
        "veryfast",
        "-crf",
        "19",
        "-c:a",
        "copy",
        "-movflags",
        "+faststart",
        str(folder / (k + ".mp4")),
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for n in range(ceil(frames / 2)):
        proc.stdin.write(paint(n / 15).tobytes())
    proc.stdin.close()
    if proc.wait():
        raise RuntimeError("Could not encode " + k)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("lesson", choices=EDITIONS)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    prove()
    render_visual(args.lesson, args.output, EDITIONS[args.lesson][1], make_picture)
