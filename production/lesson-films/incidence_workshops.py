"""Animate the two incidence lessons using a check-in desk and a fixture board."""

from functools import lru_cache
from itertools import combinations
from math import cos, sin, pi
from PIL import Image, ImageDraw
from finish_tickets import box, line, txt, pt, ease, mix, font

CHECKS = {
    "T06.1": (
        "paired-receipts",
        "9d7a37ccf5ae5baf483cb67e2adc8e1190bf1e6efae984ede85e3a77beea7e36",
    ),
    "T06.3": (
        "fixture-board",
        "71a3647b9e99730939b430bb6c676148203f4772098a798e239245c07c019719",
    ),
}
CREAM = "#fbf0d7"
INK = "#242d31"
CLAY = "#a14736"
MOSS = "#436957"
NAVY = "#21344f"
GOLD = "#eebf62"
WHITE = "#fff9e8"
FIXTURES = (
    ("AB", "CD", "E"),
    ("AC", "BE", "D"),
    ("AD", "CE", "B"),
    ("AE", "BD", "C"),
    ("BC", "DE", "A"),
)
SIX = (
    ("AF", "BE", "CD"),
    ("BF", "AC", "DE"),
    ("CF", "BD", "AE"),
    ("DF", "CE", "AB"),
    ("EF", "AD", "BC"),
)


def center(d, x, y, label, size=30, colour=INK, style="b"):
    txt(d, x, y, label, size, colour, style, "mm")


def label(d, x, y, s, sz=23, col=INK):
    txt(d, x, y, s, sz, col, "b")


def circle(d, x, y, r, fill, edge=None):
    d.ellipse(pt(x - r, y - r, x + r, y + r), fill=fill, outline=edge, width=3)


def poly(d, points, fill, edge=None):
    p = [pt(x, y) for x, y in points]
    d.polygon(p, fill=fill)
    if edge:
        d.line(p + [p[0]], fill=edge, width=4)


def slip(d, x, y, who, other, colour, w=370):
    h = 0.44 * w
    box(d, x + 3, y + 6, w, h, "#b2a18c", None, 3)
    box(d, x, y, w, h, WHITE, "#a89779", 3)
    line(d, x + 20, y + h * 0.3, x + w - 20, y + h * 0.3, "#c6b9a3")
    label(d, x + 19, y + h * 0.15, "MEETING REPORT", max(15, w * 0.052), colour)
    txt(d, x + 22, y + h * 0.60, who + " met " + other, w * 0.105, INK, "s")
    for j in range(11):
        lx = x + 14 + j * (w - 40) / 11
        line(d, lx, y + h * 0.87, lx + 8, y + h * 0.87, colour, 2)


def check_header(d, title):
    label(d, 64, 52, "THE CHECK-IN DESK", 24, MOSS)
    txt(d, 63, 113, title, 50, INK, "s")
    line(d, 65, 155, 1212, 155, "#85795f", 2)


def registry(d, x, y, count, mode):
    box(d, x, y, 520, 310, "#f9f6e7", "#9a8b72", 7)
    label(d, x + 22, y + 28, "ATTENDANCE REGISTER", 22, MOSS)
    for j, n in enumerate("ABCDEF"):
        yy = y + 68 + j * 38
        line(d, x + 23, yy + 15, x + 490, yy + 15, "#d6cab4", 1)
        txt(d, x + 28, yy, n, 25, INK, "b")
        if mode == "partners":
            txt(
                d,
                x + 91,
                yy,
                " ".join(c for c in "ABCDEF" if c != n) if j < count else "—",
                22,
                INK,
                "m",
            )
        elif mode == "tally" and j < count:
            for k in range(4):
                line(d, x + 102 + k * 14, yy - 9, x + 102 + k * 14, yy + 9, CLAY, 3)
            line(d, x + 94, yy + 9, x + 154, yy - 9, CLAY, 3)
            txt(d, x + 202, yy, "5 reports", 21, INK)
        else:
            txt(d, x + 92, yy, "checked in", 21, MOSS)


def cube_faces(d, t):
    a = (268, 251)
    b = (441, 189)
    c = (607, 261)
    e = (430, 332)
    dy = 161
    bl = (b[0], b[1] + dy)
    el = (e[0], e[1] + dy)
    cl = (c[0], c[1] + dy)
    al = (a[0], a[1] + dy)
    poly(d, [a, b, c, e], "#f4d38d", INK)
    poly(d, [a, e, el, al], "#c7765e", INK)
    poly(d, [e, c, cl, el], "#8bb5a0", INK)
    if t >= 77:
        line(d, *a, *e, WHITE, 8)
        label(d, 71, 548, "The light edge borders the gold and red faces.", 24, MOSS)
    label(d, 734, 236, "Count each face’s four edges.", 28, INK)
    if t >= 77:
        txt(d, 734, 335, "6 faces × 4 = 24 reports", 36, CLAY, "s")
    if t >= 81:
        txt(d, 734, 426, "24 ÷ 2 = 12 edges", 38, MOSS, "s")


def receipt_scene(d, i, t):
    titles = [
        "One meeting leaves two reports",
        "Read a join from both sides",
        "Open the six-person register",
        "The register counts thirty reports",
        "Match each pair of slips",
        "Can an odd pile be paired?",
        "Two faces share each cube edge",
        "Transfer the count to games",
    ]
    check_header(d, titles[i])
    if i == 0:
        k = ease(t, 5.8, 8.5)
        slip(d, mix(98, 185, k), 218, "A", "B", CLAY, 360)
        slip(d, mix(800, 735, k), 218, "B", "A", MOSS, 360)
        if t > 8.8:
            center(d, 640, 498, "2 reports for 1 handshake", 40, MOSS, "s")
    elif i == 1:
        line(d, 214, 320, 632, 320, CLAY, 11)
        circle(d, 214, 320, 17, MOSS)
        circle(d, 632, 320, 17, MOSS)
        center(d, 214, 397, "one end", 29)
        center(d, 632, 397, "other end", 29)
        txt(d, 804, 291, "1 line", 42, INK, "s")
        txt(d, 804, 390, "2 end reports", 40, MOSS, "s")
        if t >= 21:
            center(
                d,
                640,
                550,
                "Choose the object and count how often it reports.",
                29,
                INK,
            )
    elif i == 2:
        registry(d, 75, 204, 0, "attendance")
        txt(d, 683, 244, "Six visitors", 41, INK, "s")
        txt(d, 683, 335, "One handshake per pair.", 29, CLAY)
        if t >= 29.8:
            txt(d, 683, 440, "What will each visitor report?", 27, MOSS)
    elif i == 3:
        registry(d, 73, 199, int(max(0, (t - 38) * 2)) + 1, "tally")
        label(d, 693, 247, "A shakes hands with", 28, MOSS)
        txt(d, 693, 322, "B   C   D   E   F", 38, INK, "m")
        if t > 42.3:
            txt(d, 693, 434, "6 × 5 = 30 reports", 34, CLAY, "s")
    elif i == 4:
        p = ease(t, 47.5, 50.0)
        slip(d, mix(80, 287, p), 211, "A", "B", CLAY, 320)
        slip(d, mix(880, 622, p), 229, "B", "A", MOSS, 320)
        if t > 50.7:
            center(d, 640, 470, "30 reports ÷ 2 per handshake = 15", 37, MOSS, "s")
        if t > 54.1:
            center(
                d,
                640,
                557,
                "Reverse the names and you find the matching slip.",
                25,
                INK,
            )
    elif i == 5:
        for j in range(21):
            x = 101 + (j // 2) % 5 * 198
            y = 221 + (j // 2) // 5 * 117
            if j < 20:
                if j % 2:
                    x += 55
                box(d, x, y, 50, 65, WHITE, CLAY if j % 2 == 0 else MOSS, 3)
                if j % 2 == 1:
                    line(d, x - 8, y + 31, x + 3, y + 31, MOSS, 3)
            elif t >= 63:
                box(d, 1055, 288, 67, 91, WHITE, CLAY, 4)
                center(d, 1088, 335, "?", 38, CLAY)
        center(d, 640, 519, "7 visitors × 3 reports = 21", 36, INK, "s")
        if t >= 65:
            center(
                d,
                640,
                576,
                "Ten pairs use twenty slips. One slip has no partner.",
                27,
                CLAY,
            )
    elif i == 6:
        cube_faces(d, t)
    else:
        if t < 93.2:
            slip(d, 83, 220, "A", "B", CLAY, 355)
            slip(d, 472, 220, "B", "A", MOSS, 355)
            label(d, 897, 290, "Two reports", 27, MOSS)
            label(d, 897, 366, "one meeting", 27, CLAY)
        else:
            label(d, 89, 226, "TEAM A’S OPPONENTS", 25, MOSS)
            for j, n in enumerate("BCDEFGH"):
                x = 101 + j * 158
                poly(
                    d,
                    [(x, 299), (x + 114, 299), (x + 72, 372), (x + 51, 386), (x, 344)],
                    "#c9ddbb" if j % 2 else "#efc285",
                    INK,
                )
                center(d, x + 51, 330, n, 37, INK, "s")
            center(d, 640, 485, "Eight teams each have seven games to report.", 30, INK)
            if t >= 100.5:
                center(d, 640, 558, "Which two teams report the same game?", 27, CLAY)


def fixture_header(d, title):
    label(d, 64, 53, "THE CLUB FIXTURE ROOM", 24, GOLD)
    txt(d, 63, 116, title, 50, WHITE, "s")
    line(d, 65, 162, 1212, 162, "#8da8a7", 2)


def pin(d, x, y, v, colour=GOLD, r=26):
    circle(d, x, y, r, colour)
    center(d, x, y, v, r * 1.1, NAVY, "b")


def tokens(d, t):
    for j in range(12):
        g = j // 3
        within = j % 3
        p = ease(t, 5.8 + g * 0.42, 8.7 + g * 0.42)
        xx = mix(96 + j * 97, 115 + g * 287 + within * 55, p)
        yy = mix(325, 353, p)
        circle(d, xx, yy, 20, GOLD if j % 3 else "#c8ded5", WHITE)
    if t >= 7.3:
        for g in range(4):
            line(d, 82 + g * 287, 405, 259 + g * 287, 405, "#96c9b1", 5)
        center(d, 640, 534, "12 tokens ÷ 3 per group = 4 groups", 37, WHITE)


def bench(d, x, y, pair):
    box(d, x, y, 233, 102, "#e7d7ae", "#d6be82", 14)
    for j, player in enumerate(pair):
        pin(d, x + 68 + j * 95, y + 48, player, "#90c3b2", 27)
    line(d, x + 14, y + 114, x + 212, y + 114, GOLD, 5)


def chalk(d, x, y, text, size=29):
    txt(d, x, y, text, size, WHITE, "s")


def board(d, t):
    left = 87
    top = 214
    for x, val in [(left, "DAY"), (340, "PAIR 1"), (605, "PAIR 2"), (938, "RESTS")]:
        label(d, x, top, val, 22, GOLD)
    starts = [55.88, 58.98, 62.1, 65.1, 67.9]
    for i, (a, b, rest) in enumerate(FIXTURES):
        yy = 262 + i * 63
        line(d, left, yy + 31, 1160, yy + 31, "#547271", 2)
        chalk(d, left + 10, yy, str(i + 1), 29)
        if t >= starts[i]:
            for x, val in ((338, a), (600, b), (945, rest)):
                txt(d, x, yy, val, 33, WHITE, "m")
    if t > 70.55:
        center(d, 640, 596, "Every one of the ten combinations appears once.", 25, GOLD)


def triple_test(d, t):
    # The two translucent rehearsal circles overlap only at E.
    d.ellipse(pt(92, 219, 508, 470), fill="#32645c", outline="#a4cfbb", width=4)
    d.ellipse(pt(410, 219, 826, 470), fill="#495b79", outline="#a9bdcf", width=4)
    for x, y, person in [
        (188, 337, "A"),
        (302, 375, "B"),
        (457, 332, "E"),
        (624, 374, "C"),
        (739, 332, "D"),
    ]:
        pin(d, x, y, person, GOLD if person == "E" else "#dce5d8", 25)
    label(d, 877, 245, "FIRST TRIPLE", 20, GOLD)
    chalk(d, 877, 290, "A  B  E", 36)
    label(d, 877, 365, "SECOND TRIPLE", 20, GOLD)
    chalk(d, 877, 410, "E  C  D", 36)
    if t < 79:
        msg = "A triple uses three different pairs."
    elif t < 89.37:
        msg = "The two triples meet only at E."
    elif t < 93.85:
        msg = "With E, every possible partner is already used."
    else:
        msg = "Without E, picking three must take both A and B or both C and D."
    center(d, 640, 543, msg, 26, WHITE)
    if t >= 99.4:
        center(d, 640, 596, "Maximum: 2 triples.", 27, GOLD)


def chessboards(d):
    for g in range(3):
        x = 116 + g * 392
        y = 224
        s = 20
        box(d, x - 13, y - 13, s * 8 + 26, s * 8 + 26, "#c3ad85", None, 3)
        for a in range(8):
            for b in range(8):
                d.rectangle(
                    pt(x + s * a, y + s * b, x + s * (a + 1), y + s * (b + 1)),
                    fill=WHITE if (a + b) % 2 == 0 else "#527771",
                )
        for a, b, co in [(0, 0, NAVY), (7, 7, GOLD)]:
            circle(d, x + (a + 0.5) * s, y + (b + 0.45) * s, 10, co)
            poly(
                d,
                [
                    (x + (a + 0.5) * s, y + (b + 0.45) * s),
                    (x + (a + 0.79) * s, y + (b + 0.86) * s),
                    (x + (a + 0.21) * s, y + (b + 0.86) * s),
                ],
                co,
            )
        center(d, x + 4 * s, 444, "Board " + str(g + 1), 26, WHITE)


def fixture_scene(d, i, t):
    title = [
        "Sort the club’s supply",
        "Prove the ceiling can be reached",
        "Two pairs work while one rests",
        "Spend two new pairings each day",
        "Post the five-day fixture list",
        "Can a third triple rehearse?",
        "Take the count to three chessboards",
    ][i]
    fixture_header(d, title)
    if i == 0:
        tokens(d, t)
    elif i == 1:
        label(d, 126, 247, "THE LIMIT", 26, GOLD)
        chalk(d, 126, 329, "No more than four.", 39)
        if t > 17.8:
            label(d, 705, 247, "THE CONSTRUCTION", 26, GOLD)
            chalk(d, 705, 329, "Make four groups.", 39)
            for i in range(4):
                for j in range(3):
                    circle(d, 730 + 90 * i + 22 * j, 409, 9, "#b2d1be")
        if t > 20.7:
            center(
                d,
                640,
                555,
                "A ceiling and a working arrangement prove a maximum.",
                28,
                WHITE,
            )
    elif i == 2:
        bench(d, 112, 267, "AB")
        bench(d, 522, 267, "CD")
        pin(d, 1059, 316, "E", "#b8bdcc", 36)
        center(d, 228, 447, "Work together", 25, WHITE)
        center(d, 638, 447, "Work together", 25, WHITE)
        center(d, 1059, 447, "Rests", 25, WHITE)
        if t > 30.1:
            center(d, 640, 555, "Use two new pairs each day.", 32, GOLD)
    elif i == 3:
        for j, pair in enumerate("AB AC AD AE BC BD BE CD CE DE".split()):
            x = 122 + j % 5 * 229
            y = 234 + j // 5 * 102
            box(d, x - 21, y - 26, 161, 70, "#dde3cc", None, 3)
            center(d, x + 59, y + 10, pair, 36, NAVY, "m")
        if t >= 47.4:
            center(d, 640, 509, "10 possible pairs ÷ 2 new pairs each day", 33, WHITE)
        if t >= 49.4:
            center(d, 640, 568, "At most 5 days", 33, GOLD)
    elif i == 4:
        board(d, t)
    elif i == 5:
        triple_test(d, t)
    elif t < 111.35:
        label(d, 95, 242, "1   COUNT THE AVAILABLE PAIRS", 25, GOLD)
        chalk(d, 95, 321, "2   Find a ceiling.", 32)
        chalk(d, 95, 411, "3   Construct a schedule or prove the ceiling fails.", 32)
    else:
        chessboards(d)
        center(
            d,
            640,
            535,
            "Six students • three games per day • no repeated pair",
            28,
            WHITE,
        )
        if t >= 119.5:
            center(
                d,
                640,
                593,
                "How many different pairs must the fixture list contain?",
                24,
                GOLD,
            )


def make_picture(lesson, index, t, caption):
    background = CREAM if lesson == "T06.1" else "#203b40"
    im = Image.new("RGB", (1920, 1080), background)
    d = ImageDraw.Draw(im)
    (receipt_scene if lesson == "T06.1" else fixture_scene)(d, index, t)
    d.rectangle((0, 930, 1919, 1079), fill=INK if lesson == "T06.1" else "#13282f")
    if caption:
        size = 39
        while d.textlength(caption, font=font(size, "r")) > 1825:
            size -= 1
        d.text((960, 1004), caption, anchor="mm", font=font(size, "r"), fill=WHITE)
    return im


def prove():
    assert len(list(combinations("ABCDEF", 2))) == 15
    all_pairs = {"".join(p) for p in combinations("ABCDE", 2)}
    assert {p for a, b, _ in FIXTURES for p in (a, b)} == all_pairs
    assert all(len(set(a + b + r)) == 5 for a, b, r in FIXTURES)
    trios = [set(t) for t in combinations("ABCDE", 3)]
    assert any(len(a & b) == 1 for a, b in combinations(trios, 2))
    assert all(
        any(len(a & b) > 1 for a, b in combinations(group, 2))
        for group in combinations(trios, 3)
    )
    assert len({tuple(sorted(p)) for day in SIX for p in day}) == 15
    assert all(len(set("".join(day))) == 6 for day in SIX)


if __name__ == "__main__":
    import argparse
    from pathlib import Path
    from counting_workshops import render_visual

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("lesson", choices=CHECKS)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    prove()
    render_visual(args.lesson, args.output, CHECKS[args.lesson][1], make_picture)
