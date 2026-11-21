"""A travelling ticket, a sorting rack, and a three-wheel combination lock."""

from itertools import product
from math import sin, pi
from stage import between, blend, clamp, ease, mix

BACKGROUND = ("#191e24", "#252630")
PAPER = "#eadbc0"
INK = "#26272b"
OCHRE = "#edb867"
INKBLUE = "#294c67"
CORAL = "#f19c83"
GREY = "#b8b8b5"
LIGHT = "#fff1dc"
LINE = "#59606b"
BRIDGE = "Watch what each digit gains or loses when it moves one place. In the lock, look for the digit that stays put."


def poster(draw):
    return draw(6.17, 1.5)


def check_maths():
    for a in range(1, 10):
        for b in range(10):
            assert (10 * a + b) - (10 * b + a) == 9 * (a - b)
    assert 73 - 37 == 36
    assert [
        n
        for n in range(10, 100)
        if sum(divmod(n, 10)) == 11 and n - int(str(n)[::-1]) == 27
    ] == [74]
    assert [
        (a, b, c)
        for a, b, c in product(range(1, 10), range(10), range(10))
        if 99 * (a - c) == 396 and b == 2 * c and a + b + c == 16
    ] == [(7, 6, 3)]


def ticket(a, x=100, y=168, w=690, h=360):
    a.box(x + 5, y + 9, w, h, radius=20, fill="#12181e")
    a.box(x, y, w, h, radius=20, fill=PAPER, edge="#e1c59a")
    for q in range(12):
        px = x + 28 + q * (w - 55) / 11
        a.line([(px, y + 21), (px + 6, y + 21)], "#bfa882", 2)
    a.label("PLACE VALUE  /  TICKET", x + 32, y + 49, 20, INK, bold=True)
    a.line([(x + 30, y + 76), (x + w - 30, y + 76)], "#bfa882", 2)
    for cy in (y + h * 0.47, y + h * 0.61):
        a.dot(x, cy, 9, "#22262d")
        a.dot(x + w, cy, 9, "#22262d")


def card(a, x, y, value, ink=INK, scale=1, op=1):
    w, h = 110 * scale, 128 * scale
    a.box(x - w / 2 + 2, y - h / 2 + 4, w, h, radius=8, fill="#af9b80", opacity=op)
    a.box(
        x - w / 2, y - h / 2, w, h, radius=8, fill="#fcf3dd", edge="#bdac93", opacity=op
    )
    a.text(str(value), x, y, 78 * scale, ink, bold=True, opacity=op)


def heading(a, title, note):
    a.label("DIGIT DETECTIVES", 80, 58, 21, OCHRE, bold=True)
    a.label(title, 80, 108, 44, LIGHT, bold=True)
    a.label(note, 1194, 65, 22, GREY, align="right")


def marker(a, x, y, text, op):
    a.label(text, x, y, 34, LIGHT, op, bold=True)


def two_cards(a, A, B, p=0):
    x1, x2 = 332, 558
    y = 347
    arch = 77 * sin(pi * p)
    a.label("TENS", x1, 483, 22, INK, align="center", bold=True)
    a.label("ONES", x2, 483, 22, INK, align="center", bold=True)
    card(a, mix(x1, x2, p), y - arch, A, INKBLUE)
    card(a, mix(x2, x1, p), y + arch, B, "#8a3c30")


def lock(a, labels=("?", "?", "?"), highlight=None):
    a.box(100, 194, 645, 292, radius=30, fill="#504435", edge="#c09762", stroke=4)
    a.box(122, 216, 600, 248, radius=20, fill="#231f20", edge="#6e5c48")
    for x in (117, 727):
        for y in (210, 470):
            a.dot(x, y, 4, "#dac196")
    for i, (v, c) in enumerate(zip(labels, (INKBLUE, "#664f84", "#95452e"))):
        x = 220 + i * 201
        card(a, x, 329, v, c, 0.96)
        a.text(
            ("hundreds", "tens", "ones")[i], x, 420, 23, "#edd9b4", bold=i == highlight
        )


def draw(a, scene, c):
    if scene == 1:
        heading(a, "Turn the ticket around", "Two-digit numbers")
        ticket(a)
        p = c.reveal("turn its two digit cards", 1.65)
        two_cards(a, 7, 3, p)
        a.label("Before the swap", 853, 250, 23, GREY)
        a.label("73", 850, 320, 67, OCHRE, bold=True)
        a.label("After the swap", 853, 395, 23, GREY, c.reveal("it reads thirty seven"))
        a.label("37", 850, 465, 67, CORAL, c.reveal("thirty seven"), bold=True)
    elif scene == 2:
        heading(a, "Each move has a value", "Compare both changes")
        ticket(a)
        a.label("Digit", 142, 318, 25, INK)
        a.label("Before", 330, 318, 25, INK)
        a.label("After", 538, 318, 25, INK)
        for i, (digit, before, after, color, cue) in enumerate(
            ((7, 70, 7, INKBLUE, "seven loses"), (3, 3, 30, "#8a3c30", "three gains"))
        ):
            p = c.reveal(cue, 0.7)
            y = 381 + 68 * i
            a.text(str(digit), 173, y, 46, color, bold=True, opacity=p)
            a.text(str(before), 386, y, 44, INK, bold=True, opacity=p)
            a.arrow((460, y), (505, y), "#a68b6d", p)
            a.text(str(after), 575, y, 44, INK, bold=True, opacity=p)
        marker(a, 824, 280, "70 − 7 = 63 lost", c.reveal("tens to ones"))
        marker(a, 824, 360, "30 − 3 = 27 gained", c.reveal("on the return trip"))
        a.label("63 − 27 = 36", 824, 453, 42, OCHRE, c.reveal("thirty six"), bold=True)
    elif scene == 3:
        heading(a, "A ticket with two clues", "Which number fits?")
        ticket(a)
        two_cards(a, "?", "?")
        a.label("Digit sum", 838, 232, 24, GREY, c.reveal("digits add"))
        a.label("11", 834, 297, 62, OCHRE, c.reveal("eleven"), bold=True)
        a.label(
            "Difference after reversal",
            838,
            374,
            24,
            GREY,
            c.reveal("exceeds its reverse"),
        )
        a.label("27", 834, 447, 62, CORAL, c.reveal("twenty seven"), bold=True)
    elif scene == 4:
        heading(a, "Give the clues a shape", "Eleven counters")
        a.label("Tens digit", 94, 265, 26, LIGHT)
        a.label("Ones digit", 94, 408, 26, LIGHT)
        extra = c.reveal("set those three aside", 1.0)
        equal = c.reveal("remaining eight splits equally", 1.4)
        for i in range(11):
            x0 = 300 + 60 * i
            y0 = 337
            if i < 3:
                x, y = mix(x0, 612 + i * 60, extra), mix(y0, 264, extra)
                col = "#b77656"
            else:
                k = i - 3
                x, y = mix(x0, 335 + (k % 4) * 60, equal), mix(
                    y0, 264 if k < 4 else 408, equal
                )
                col = "#71acb6"
            a.dot(x, y, 24, col)
            a.dot(x - 5, y - 6, 5, blend(col, LIGHT, 0.34))
        a.label(
            "27 = 9 × 3", 915, 241, 34, OCHRE, c.reveal("nine times three"), bold=True
        )
        a.label(
            "7 and 4",
            915,
            336,
            41,
            LIGHT,
            c.reveal("digits are seven and four"),
            bold=True,
        )
        a.label(
            "74 − 47 = 27",
            797,
            509,
            42,
            CORAL,
            c.reveal("seventy four minus forty seven"),
            bold=True,
        )
    elif scene == 5:
        heading(a, "A three-wheel lock", "Use all three clues")
        lock(a)
        for i, (t, line) in enumerate(
            [
                ("exceeds its reverse", "Code − reverse = 396"),
                ("middle digit is twice", "Middle = 2 × last"),
                ("add to sixteen", "Digit sum = 16"),
            ]
        ):
            a.label(
                line,
                788,
                267 + 85 * i,
                32,
                (OCHRE, LIGHT, CORAL)[i],
                c.reveal(t),
                bold=True,
            )
    elif scene == 6:
        heading(a, "The middle wheel stays put", "Compare place values")
        ticket(a)
        for row, labels in enumerate((("a", "b", "c"), ("c", "b", "a"))):
            y = 316 + 94 * row
            for i, v in enumerate(labels):
                a.text(
                    v,
                    260 + i * 170,
                    y,
                    57,
                    {"a": INKBLUE, "b": "#664f84", "c": "#95452e"}[v],
                    bold=True,
                )
        cancel = c.reveal("subtracting cancels it", 0.8)
        a.line([(403, 286), (458, 346)], "#755c85", 4, cancel)
        a.line([(403, 380), (458, 440)], "#755c85", 4, cancel)
        a.label(
            "100a − a = 99a", 820, 240, 33, LIGHT, c.reveal("outside digits"), bold=True
        )
        a.label(
            "c − 100c = −99c",
            820,
            304,
            33,
            LIGHT,
            c.reveal("outside digits"),
            bold=True,
        )
        a.label("396 = 99 × 4", 820, 405, 40, OCHRE, c.reveal("four groups"), bold=True)
        a.label(
            "First = last + 4",
            820,
            472,
            32,
            CORAL,
            c.reveal("first digit is four"),
            bold=True,
        )
    elif scene == 7:
        heading(a, "Build the three digits", "Sixteen altogether")
        start_x = 324
        unit = 108
        labels = ("Last digit", "Middle digit", "First digit")
        parts = (1, 2, 1)
        cues = ("last digit one part", "middle takes two parts", "first takes one part")
        reveal_values = c.reveal("last digit is three")
        remove = c.reveal("remove four", 0.9)
        for i, (label, n, when) in enumerate(zip(labels, parts, cues)):
            y = 225 + i * 103
            p = c.reveal(when, 0.7)
            a.label(label, 85, y + 30, 26, LIGHT, p)
            for k in range(n):
                x = start_x + k * (unit + 4)
                a.box(
                    x, y, unit, 60, radius=4, fill="#477180", edge="#b2d8d2", opacity=p
                )
                a.text(
                    "3" if reveal_values > 0.6 else "▢",
                    x + unit / 2,
                    y + 30,
                    34,
                    LIGHT,
                    bold=True,
                    opacity=p,
                )
            if i == 2:
                xx = start_x + unit + 4 + remove * 52
                a.box(xx, y, unit, 60, radius=4, fill="#975d47", edge=CORAL, opacity=p)
                a.text("+4", xx + unit / 2, y + 30, 34, LIGHT, bold=True, opacity=p)
        a.label("16 − 4 = 12", 820, 250, 42, OCHRE, c.reveal("remove four"), bold=True)
        a.label(
            "12 ÷ 4 = 3",
            820,
            336,
            42,
            LIGHT,
            c.reveal("four equal parts share twelve"),
            bold=True,
        )
        a.label(
            "Code  7 6 3", 820, 450, 49, CORAL, c.reveal("code is seven"), bold=True
        )
    else:
        heading(a, "Check every clue", "A code you can prove")
        lock(a, ("7", "6", "3"), 1)
        for i, (line, when, col) in enumerate(
            (
                ("763 − 367 = 396", "three hundred and ninety six", OCHRE),
                ("6 = 2 × 3", "middle digit cancels", LIGHT),
                ("7 + 6 + 3 = 16", "digit sum", CORAL),
            )
        ):
            a.label(line, 787, 257 + 88 * i, 36, col, c.reveal(when), bold=True)
