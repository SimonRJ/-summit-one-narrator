"""Score ledger and centre-of-a-list diagrams for T16.3."""

from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont

PAPER = "#fffaf3"
INK = "#292238"
PURPLE = "#58397d"
PLUM = "#974978"
CYAN = "#126775"
PALE = "#e4d8e7"
GOLD = "#e4ad44"
DIMS = (1920, 1080)


@lru_cache(None)
def font(n, f):
    name = {"r": "DejaVuSans", "b": "DejaVuSans-Bold", "s": "DejaVuSerif", "i": "DejaVuSerif-Italic"}[f]
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/" + name + ".ttf", round(n * 1.5))


def point(*coords):
    return tuple(round(v * 1.5) for v in coords)


def text(d, x, y, s, size=28, colour=INK, face="r", anchor="lm"):
    d.text(point(x, y), str(s), font=font(size, face), fill=colour, anchor=anchor)


def rect(d, x, y, w, h, fill, border=None):
    d.rounded_rectangle(point(x, y, x + w, y + h), radius=13, fill=fill, outline=border, width=3)


def line(d, coords, colour=PALE, width=2):
    d.line(point(*coords), fill=colour, width=round(width * 1.5))


def ease(t, a, b):
    n = min(1, max(0, (t - a) / (b - a)))
    return n * n * (3 - 2 * n)


def pile(d, x, y, count, hue):
    for j in range(count):
        d.rounded_rectangle(point(x - 18, y - j * 14 - 11, x + 18, y - j * 14 + 1), radius=4, fill=hue)


def slip(d, x, y, w, label, value, hue=PURPLE):
    rect(d, x, y, w, 133, "#fffdf8", PALE)
    text(d, x + 19, y + 31, label, 20, hue, "b")
    text(d, x + 19, y + 89, value, 37, INK, "s")


def scores(d, values, middle, y=328, *, xs=None):
    coords = []
    for i, num in enumerate(values):
        x = xs[i] if xs is not None else 640 + (i - (len(values) - 1) / 2) * 150
        coords.append(x)
        rect(
            d,
            x - 52,
            y - 40,
            104,
            84,
            "#dcefe6" if i in middle else "#f4eff4",
            CYAN if i in middle else PALE,
        )
        text(d, x, y, str(num), 40, CYAN if i in middle else INK, "b", "mm")
    return coords


@lru_cache(None)
def station():
    im = Image.new("RGB", DIMS, PAPER)
    d = ImageDraw.Draw(im)
    d.rectangle(point(0, 0, 24, 720), fill=PURPLE)
    for y in range(192, 605, 36):
        line(d, (54, y, 1224, y), "#eee5eb", 1)
    text(d, 73, 63, "THE SCORE NOTEBOOK", 22, PURPLE, "b")
    return im


def region(n, t, span, voice_at):
    im = station().copy()
    d = ImageDraw.Draw(im)
    title = [
        "Put the points back into a pile",
        "How much does each group contribute?",
        "A fifth score changes the mean",
        "Keep both totals on the page",
        "What did the fifth score add?",
        "Combine people, not just group means",
        "Which scores sit in the middle?",
        "Recover the missing score",
    ][n]
    text(d, 72, 133, title, 48, INK, "s")
    if n == 0:
        p = ease(t, 2.0, 5.0)
        for i, raw in enumerate((2, 4, 6, 8)):
            x = 222 + i * 174
            count = round(raw * (1 - p) + 5 * p)
            pile(d, x, 468, count, CYAN)
            text(d, x, 508, count, 27, INK, "b", "mm")
        text(d, 883, 317, "20 points", 40, PURPLE, "s")
        text(d, 883, 383, "4 people", 36, INK, "s")
        text(d, 881, 455, "20 ÷ 4 = 5", 30, CYAN, "b")
        text(d, 74, 568, "Redistribute the points without changing the total.", 27, INK)
    elif n == 1:
        for i, (count, hue) in enumerate([(6, PURPLE), (6, PURPLE), (10, CYAN), (10, CYAN), (10, CYAN)]):
            pile(d, 210 + i * 190, 448, count, hue)
        text(d, 303, 503, "2 people", 30, PURPLE, "b", "mm")
        text(d, 788, 503, "3 people", 30, CYAN, "b", "mm")
        text(d, 74, 572, "Each person contributes once. A larger group gets more weight.", 26, INK)
    elif n == 2:
        slip(d, 83, 240, 504, "BEFORE", "4 scores, mean 7")
        slip(d, 683, 240, 504, "AFTER", "5 scores, mean 8", CYAN)
        text(d, 79, 466, "What changed between the two totals?", 35, PURPLE, "s")
        if t > 7:
            text(d, 82, 565, "Pause and write down both totals.", 27, INK)
    elif n == 3:
        slip(d, 82, 238, 509, "FOUR SCORES", "4 × 7 = 28")
        if t > 2:
            slip(d, 677, 238, 509, "FIVE SCORES", "5 × 8 = 40", CYAN)
        for i in range(5):
            cx = 217 + i * 199
            d.ellipse(point(cx - 19, 471, cx + 19, 509), fill=CYAN if i == 4 else PURPLE)
        text(d, 81, 565, "The fifth score accounts for the difference.", 27)
    elif n == 4:
        slip(d, 82, 228, 509, "DIFFERENCE OF TOTALS", "40 − 28 = 12")
        if t > 4:
            slip(d, 677, 228, 509, "ANOTHER WAY TO SEE IT", "32 − 28 = 4", CYAN)
            for i in range(12):
                x = 142 + i * 77
                rect(d, x, 437, 57, 59, PURPLE if i < 8 else CYAN)
            text(d, 142, 548, "8 for the new learner", 27, PURPLE, "b")
            text(d, 757, 548, "4 to fill the shortfall", 26, CYAN, "b")
    elif n == 5:
        slip(d, 77, 223, 505, "FIRST GROUP", "2 × 6 = 12")
        slip(d, 673, 223, 505, "SECOND GROUP", "3 × 10 = 30", CYAN)
        if t > 5:
            text(d, 75, 446, "42 points across 5 people", 41, INK, "s")
        if t > 9.8:
            text(d, 75, 558, "42 ÷ 5 = 8.4", 35, CYAN, "b")
    elif n == 6:
        remove_at = voice_at.get("remove", span * 0.48)
        text(d, 640, 218, "Ordered scores", 25, PURPLE, "b", "mm")
        if t < remove_at:
            scores(d, [2, 3, 5, 9, 31], [2])
            text(d, 640, 435, "Median = 5", 34, CYAN, "b", "mm")
            if t >= voice_at.get("mean", 4):
                text(d, 640, 536, "Mean = (2 + 3 + 5 + 9 + 31) ÷ 5 = 10", 29, INK, "r", "mm")
        else:
            # Pull the fifth-point slip downward, then let the four other slips close the gap.
            travel = ease(t - remove_at, 0, 1.0)
            settle = ease(t - remove_at, 0.3, 1.4)
            xs = [340 + 75 * settle, 490 + 75 * settle, 790 - 75 * settle, 940 - 75 * settle]
            scores(d, [2, 3, 9, 31], [1, 2] if settle > 0.95 else [], xs=xs)
            if travel < 1:
                rect(d, 588, 288 + 185 * travel, 104, 84, "#f4eff4", PALE)
                text(d, 640, 328 + 185 * travel, "5", 40, PLUM, "b", "mm")
            if settle < 1:
                return im
            left, right = xs[1:3]
            line(d, (left, 385, left, 410, right, 410, right, 385), CYAN, 4)
            text(d, 640, 466, "Two middle scores: 3 and 9", 35, CYAN, "b", "mm")
            if t >= voice_at.get("average", span * 0.74):
                text(d, 640, 552, "Median = (3 + 9) ÷ 2 = 6", 35, INK, "s", "mm")
    else:
        if t < voice_at.get("notebook", span * 0.46):
            text(d, 80, 270, "Mean", 39, PURPLE, "s")
            text(d, 85, 332, "Use the total and the number of scores.", 29)
            text(d, 80, 430, "Median", 39, CYAN, "s")
            text(d, 85, 492, "Order the scores. Use one centre value or average the two.", 29)
        else:
            slip(d, 80, 232, 502, "BEFORE REMOVAL", "6 scores, mean 9")
            slip(d, 680, 232, 502, "AFTER REMOVAL", "5 scores, mean 8", CYAN)
            text(d, 80, 460, "Which score was removed?", 42, INK, "s")
            if t > span - 3.5:
                text(d, 80, 565, "Check: 6 × 9 − 5 × 8 = 14", 31, CYAN, "b")
    return im
