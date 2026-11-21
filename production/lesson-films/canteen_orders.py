"""Draw T05.E as a lunch counter with food trays and a closing clothes rail.

The only inputs are the published lunch-and-outfit-grids MP4 and matching VTT.
The H.264 video is new. The original approved AAC packets pass through unchanged.
"""

import argparse
from bisect import bisect_right
from functools import lru_cache
import hashlib
from pathlib import Path
import re
import subprocess

from PIL import Image, ImageDraw, ImageFont
from finish_tickets import caption_time

BASE = "#faf1dd"
INK = "#263f37"
RED = "#9f3b2d"
GREEN = "#326951"
WHITE = "#fffbee"
BLUE = "#528293"
PALETTE = {"apple": "#c64733", "pear": "#8cae3d", "plum": "#81466e"}
STARTS = [0, 13.54, 23.15, 32.76, 40.29, 52.61]
SOURCE = "c74b76ab2ad1e2d56c8feb484ea4d52a046c8d2e047fa22d44fb97bf73e43bc5"


def pt(*v):
    return tuple(round(t * 1.5) for t in v)


@lru_cache(None)
def face(size, kind):
    family = {"title": "DejaVuSerif-Bold", "label": "DejaVuSans-Bold", "copy": "DejaVuSans"}[kind]
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/" + family + ".ttf", round(size * 1.5))


def words(d, x, y, value, size=24, color=INK, kind="copy", anchor="lm"):
    d.text(pt(x, y), value, anchor=anchor, font=face(size, kind), fill=color)


def line(d, coords, colour, width=3):
    d.line(pt(*coords), fill=colour, width=max(1, round(width * 1.5)), joint="curve")


def rounded(d, box, r, fill, edge=None, width=2):
    d.rounded_rectangle(pt(*box), round(r * 1.5), fill=fill, outline=edge, width=round(width * 1.5))


def ellipse(d, box, fill, edge=None, width=2):
    d.ellipse(pt(*box), fill=fill, outline=edge, width=round(width * 1.5))


def poly(d, points, fill, edge=None, width=2):
    d.polygon([pt(*p) for p in points], fill=fill)
    if edge:
        line(d, [v for p in points + [points[0]] for v in p], edge, width)


def phase(t, a, b):
    x = min(1, max(0, (t - a) / (b - a)))
    return x * x * (3 - 2 * x)


def sandwich(d, x, y, kind, scale=1):
    def pos(points):
        return [(x + a * scale, y + b * scale) for a, b in points]

    lower = [(-60, 12), (-5, -48), (61, 10), (61, 23), (-60, 23)]
    poly(d, pos(lower), "#ce9655", "#775233", 2)
    if kind == "cheese":
        poly(
            d,
            pos([(-52, 9), (48, 1), (47, 17), (20, 23), (10, 16), (-14, 26), (-52, 19)]),
            "#e1aa28",
            "#8f6a24",
            2,
        )
    else:
        for dx, dy in [(-37, 15), (-15, 16), (7, 17), (29, 15), (45, 13)]:
            ellipse(
                d,
                (
                    x + (dx - 10) * scale,
                    y + (dy - 5) * scale,
                    x + (dx + 10) * scale,
                    y + (dy + 5) * scale,
                ),
                "#9b5540",
                "#75432d",
                1,
            )
    poly(d, pos([(-60, 9), (-2, -54), (60, 2), (56, 10), (-56, 15)]), "#f9d699", "#9d6c42", 2)
    for k in range(3):
        line(
            d,
            [
                x + (-30 + k * 17) * scale,
                y + (-11 - k * 6) * scale,
                x + (-20 + k * 17) * scale,
                y + (-15 - k * 6) * scale,
            ],
            "#b98651",
            2,
        )


def fruit(d, x, y, kind, scale=1):
    def box(a, b, c, e):
        return (x + a * scale, y + b * scale, x + c * scale, y + e * scale)

    co = PALETTE[kind]
    if kind == "apple":
        outline = [
            (-3, -15),
            (-15, -22),
            (-27, -17),
            (-31, -6),
            (-29, 9),
            (-20, 26),
            (-9, 30),
            (0, 26),
            (10, 29),
            (20, 23),
            (28, 7),
            (30, -6),
            (24, -17),
            (13, -21),
            (2, -16),
        ]
        poly(d, [(x + a * scale, y + b * scale) for a, b in outline], co, "#8a3a2e", 1)
    elif kind == "pear":
        outline = [
            (0, -28),
            (-8, -24),
            (-10, -8),
            (-20, 4),
            (-25, 15),
            (-23, 24),
            (-14, 31),
            (1, 34),
            (14, 31),
            (23, 21),
            (23, 12),
            (17, 2),
            (9, -9),
            (7, -24),
        ]
        poly(d, [(x + a * scale, y + b * scale) for a, b in outline], co, "#66813b", 1)
    else:
        ellipse(d, box(-23, -23, 23, 31), co, "#573453", 2)
        line(
            d,
            [
                x + 8 * scale,
                y - 16 * scale,
                x + 13 * scale,
                y - 3 * scale,
                x + 8 * scale,
                y + 18 * scale,
            ],
            "#aa738e",
            2,
        )
    line(d, [x, y - 18 * scale, x + 5 * scale, y - 35 * scale], "#684930", 3)
    ellipse(d, box(4, -34, 20, -26), "#42754c")


def tray(d, x, y, w, h, sand, fr=None, scale=1):
    rounded(d, (x + 3, y + 5, x + w + 3, y + h + 5), 17, "#ccb79b")
    rounded(d, (x, y, x + w, y + h), 17, BLUE, "#305960", 3)
    rounded(d, (x + 7, y + 7, x + w - 7, y + h - 7), 12, "#f9efcc", "#a4bfb0", 2)
    line(d, [x + w * 0.57, y + 12, x + w * 0.57, y + h - 12], "#c9b995", 3)
    sandwich(d, x + w * 0.29, y + h * 0.56, sand, scale)
    if fr:
        fruit(d, x + w * 0.78, y + h * 0.50, fr, scale * 0.9)


@lru_cache(None)
def counter():
    im = Image.new("RGB", (1920, 1080), BASE)
    d = ImageDraw.Draw(im)
    for x in range(-4, 1285, 45):
        d.rectangle(pt(x, 0, x + 10, 31), fill="#ccd8bc")
    for y in (4, 15):
        d.rectangle(pt(0, y, 1280, y + 5), fill="#d2b581")
    line(d, (52, 139, 1228, 139), "#c69a67", 2)
    words(d, 54, 66, "THE LUNCH COUNTER", 21, GREEN, "label")
    return im


def shirt(d, x, y, colour):
    p = [
        (-16, -25),
        (-31, -24),
        (-57, -6),
        (-43, 14),
        (-31, 7),
        (-31, 53),
        (31, 53),
        (31, 7),
        (43, 14),
        (57, -6),
        (31, -24),
        (16, -25),
        (8, -16),
        (-8, -16),
    ]
    poly(d, [(x + a, y + b) for a, b in p], colour, INK, 2)


def shorts(d, x, y, color, striped=False):
    p = [(-28, -19), (28, -19), (36, 24), (9, 29), (0, 6), (-9, 29), (-36, 24)]
    poly(d, [(x + a, y + b) for a, b in p], color, INK, 2)
    line(d, [x - 27, y - 11, x + 27, y - 11], "#dfd2a7", 2)
    if striped:
        for a, b in [(-24, -8), (-18, 7), (17, -6), (20, 9)]:
            line(d, [x + a - 5, y + b, x + a + 5, y + b + 4], "#fbdf95", 3)


def paint(n, t, cues):
    im = counter().copy()
    d = ImageDraw.Draw(im)
    rel = t - STARTS[n]
    title = [
        "Pack one lunch",
        "Start with the sandwich",
        "Cheese goes with two fruits",
        "Bean goes with all three",
        "Inspect the six possible trays",
        "From lunch orders to outfits",
    ][n]
    words(d, 49, 106, title, 43, INK, "title")
    if n == 0:
        words(d, 110, 210, "Choose a sandwich", 32, GREEN, "title")
        words(d, 728, 210, "Choose a fruit", 32, GREEN, "title")
        for i, s in enumerate(("cheese", "bean")):
            x = 207 + i * 257
            sandwich(d, x - 45 * (1 - phase(rel, 0.45 + i * 0.55, 1.30 + i * 0.55)), 342, s, 1.55)
            words(d, x, 426, s.title(), 28, INK, "label", "mm")
        for i, f in enumerate(PALETTE):
            x = 766 + 162 * i
            fruit(d, x, 337 - 67 * (1 - phase(rel, 2.8 + i * 0.30, 3.65 + i * 0.30)), f, 1.55)
            words(d, x, 426, f.title(), 26, INK, "label", "mm")
        if rel >= 5.9:
            words(d, 640, 536, "Cheese and plum cannot go together.", 32, RED, "title", "mm")
    elif n == 1:
        for i, s in enumerate(("cheese", "bean")):
            x = 118 + 690 * i + (1 if i == 0 else -1) * 86 * (1 - phase(rel, 0.1, 2.2))
            tray(d, x, 275, 370, 170, s, scale=1.24)
            words(d, x + 185, 503, s.title() + " orders", 31, GREEN, "title", "mm")
        words(d, 648, 352, "OR", 32, RED, "label", "mm")
        if rel >= 4.4:
            words(
                d,
                640,
                582,
                "Every lunch goes to exactly one side of the counter.",
                26,
                INK,
                "copy",
                "mm",
            )
    elif n in (2, 3):
        sand = "cheese" if n == 2 else "bean"
        fruits = list(PALETTE)[: 2 if n == 2 else 3]
        xs = [224, 699] if n == 2 else [52, 461, 870]
        for i, (x, f) in enumerate(zip(xs, fruits)):
            w = 360
            into = phase(rel, 0.2 + i * 0.72, 1.25 + i * 0.72)
            y = 298 - 39 * into
            tray(d, x, y, w, 157, sand, scale=1.20)
            fall = phase(rel, 0.18 + i * 0.60, 1.25 + i * 0.60)
            fruit(d, x + w * 0.78, y + 78.5 - 82 * (1 - fall), f, 1.08)
            words(d, x + w / 2, y + 201, f.title(), 28, INK, "label", "mm")
        if n == 2 and rel > 2.3:
            words(d, 642, 548, "Plum stays off this order.", 30, RED, "title", "mm")
        if n == 3 and rel > 3.88:
            words(d, 640, 552, "2 cheese lunches + 3 bean lunches = 5", 34, GREEN, "title", "mm")
    elif n == 4:
        for row, s in enumerate(("cheese", "bean")):
            words(d, 57, 314 + row * 143, s.title(), 26, GREEN, "label")
            for j, f in enumerate(PALETTE):
                x = 223 + j * 327
                y = 249 + row * 143
                offset = 450 * phase(rel, 8.17, 9.04) if row == 0 and j == 2 else 0
                tray(d, x + offset, y, 238, 103, s, f, 0.79)
                if not row:
                    words(d, x + 119, 210, f.title(), 24, INK, "label", "mm")
                if row == 0 and j == 2 and rel >= 4.75:
                    portion = phase(rel, 4.75, 5.2)
                    line(
                        d,
                        [
                            x + offset + 19,
                            y + 88,
                            x + offset + 19 + 201 * portion,
                            y + 88 - 72 * portion,
                        ],
                        RED,
                        7,
                    )
        if rel > 8.2:
            words(d, 640, 561, "6 possible orders − 1 forbidden order = 5", 30, RED, "title", "mm")
    elif rel < 7.55:
        for i, (x, s, f) in enumerate(
            [
                (128, "cheese", "apple"),
                (327, "cheese", "pear"),
                (579, "bean", "apple"),
                (778, "bean", "pear"),
                (977, "bean", "plum"),
            ]
        ):
            tray(d, x, 265, 172, 104, s, f, 0.65)
        for x in (214, 413):
            line(d, [302, 403, x, 374], GREEN, 2)
        for x in (665, 864, 1063):
            line(d, [863, 403, x, 374], GREEN, 2)
        words(d, 302, 429, "2 cheese orders", 30, GREEN, "title", "mm")
        words(d, 863, 429, "3 bean orders", 30, GREEN, "title", "mm")
        words(d, 640, 547, "Different-sized cases add to the total.", 30, INK, "copy", "mm")
    else:
        # The orange pairs are visibly different: one plain, one striped.
        line(d, [74, 225, 1204, 225], INK, 4)
        for j, col in enumerate(("#b84733", "#48738d", "#5d8a62")):
            x = 181 + j * 158
            line(d, [x, 225, x, 265], INK, 2)
            shirt(d, x, 288, col)
        for i, col in enumerate(("#cf7738", "#cf7738", "#3a506b", "#888f8b")):
            x = 699 + i * 130
            line(d, [x, 225, x, 265], INK, 2)
            shorts(d, x, 297, col, i == 1)
        words(d, 332, 404, "3 shirts", 28, GREEN, "title", "mm")
        words(d, 897, 404, "4 pairs of shorts", 28, GREEN, "title", "mm")
        if rel > 10.2:
            line(d, [147, 353, 212, 353], RED, 4)
            line(d, [671, 338, 671, 354, 858, 354, 858, 338], RED, 4)
            words(d, 640, 486, "The red shirt rules out both orange pairs.", 28, RED, "copy", "mm")
        if t > 69.2:
            words(d, 640, 576, "2 + 4 + 4 = 10 outfits", 33, INK, "title", "mm")
    d.rectangle(pt(0, 626, 1280, 720), fill=INK)
    j = bisect_right([c[0] for c in cues], t) - 1
    if j >= 0 and t < cues[j][1]:
        words(d, 640, 673, cues[j][2], 27, WHITE, "copy", "mm")
    return im


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("old_mp4", type=Path)
    ap.add_argument("vtt", type=Path)
    ap.add_argument("out", type=Path)
    a = ap.parse_args()
    if hashlib.sha256(a.old_mp4.read_bytes()).hexdigest() != SOURCE:
        raise ValueError("Unexpected source film")
    if (
        hashlib.sha256(a.vtt.read_bytes()).hexdigest()
        != "ad6bf788f552c2c59facdcb3efac6a7dd840322b0873e1ecb4dfeca556efd1a0"
    ):
        raise ValueError("Unexpected source captions")
    cues = []
    for entry in re.split(r"\n\s*\n", a.vtt.read_text().strip())[1:]:
        stamp, *lines = entry.splitlines()
        start, end = map(caption_time, stamp.split(" --> "))
        cues.append((start, end, " ".join(lines)))
    a.out.mkdir(parents=True, exist_ok=True)
    paint(0, 8.30, cues).save(a.out / "T05.E-studio-poster.jpg", quality=92)
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
        str(a.old_mp4),
        "-map",
        "0:v",
        "-map",
        "1:a",
        "-c:v",
        "libx264",
        "-threads",
        "3",
        "-preset",
        "veryfast",
        "-crf",
        "18",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "copy",
        "-movflags",
        "+faststart",
        str(a.out / "T05.E.mp4"),
    ]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(2203):
        t = i / 30
        p.stdin.write(paint(bisect_right(STARTS, t) - 1, t, cues).tobytes())
    p.stdin.close()
    if p.wait():
        raise RuntimeError("Encoding failed")


if __name__ == "__main__":
    main()
