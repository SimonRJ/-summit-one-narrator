"""After matching common objects, a leftover swap measures a difference of masses."""

BACKGROUND = ("#e9e2d8", "#e7dace")
INK, METAL, GREEN, RED, PAPER, RULE = (
    "#342f32",
    "#627b92",
    "#357764",
    "#9c4e40",
    "#fff8e9",
    "#a49184",
)
BRIDGE = "When the two parcel loads both contain five objects, what stays on each scale after you cancel every exact match? Use the remaining swap to reconstruct a single mass."
HEAD = (
    "An extra foam pad",
    "Lift off matching objects",
    "A different pair of loads",
    "A swap has a price",
    "Trade tins for discs",
    "Recover one mass",
    "Run the scales again",
    "Name the leftover objects",
)


def check_maths():
    assert 300 + 2 * 110 == 520 and 300 + 110 == 410
    assert [
        (t, d)
        for t in range(250)
        for d in range(200)
        if 2 * t + 3 * d == 470 and 3 * t + 2 * d == 530
    ] == [(130, 70)]


def item(a, x, y, kind, dim=False):
    col = (
        RULE
        if dim
        else {"Carrier": METAL, "Pad": GREEN, "Tin": METAL, "Disc": GREEN, "+60": RED}[kind]
    )
    if kind == "Disc":
        a.dot(x, y, 26, col)
        a.dot(x, y, 8, PAPER)
    elif kind == "Pad":
        a.box(x - 31, y - 13, 62, 26, fill=col, radius=8)
    elif kind == "Tin":
        a.box(x - 23, y - 30, 46, 60, fill=col, radius=9)
        a.line([(x - 16, y - 17), (x + 17, y - 17)], PAPER, 3)
    elif kind == "Carrier":
        a.box(x - 33, y - 22, 66, 44, fill=col, radius=6)
        a.line([(x - 19, y - 11), (x + 20, y - 11)], PAPER, 3)
    else:
        a.box(x - 30, y - 24, 60, 48, fill=col, radius=5)
        a.text("60", x, y + 1, 24, PAPER, bold=True)
    if dim:
        a.line([(x - 29, y + 29), (x + 29, y - 29)], RED, 4)


def load(a, y, items, reading, hide=()):
    for i, k in enumerate(items):
        item(a, 162 + i * 91, y, k, i in hide)
    a.line([(99, y + 38), (635, y + 38)], INK, 5)
    a.box(672, y - 30, 157, 71, fill=PAPER, edge=RULE, radius=10, stroke=3)
    a.text(reading, 751, y + 6, 32, INK, bold=True)


def draw(a, n, c):
    a.text(HEAD[n - 1], 63, 70, 46, INK, bold=True, align="left")
    a.line([(62, 123), (1217, 123)], RULE, 3)
    if n <= 2:
        load(a, 252, ("Carrier", "Pad", "Pad"), "520 g", (0, 1) if n == 2 else ())
        load(a, 430, ("Carrier", "Pad"), "410 g", (0, 1) if n == 2 else ())
        a.text("Same carrier", 898, 226, 28, METAL, align="left")
        a.text("Matching pads", 898, 284, 28, GREEN, align="left")
        if n == 2:
            a.text(
                "1 pad = 110 g",
                884,
                434,
                33,
                RED,
                bold=True,
                align="left",
                opacity=c.reveal("one hundred and ten"),
            )
    elif n in (3, 4, 7):
        load(
            a, 252, ("Tin", "Tin", "Disc", "Disc", "Disc"), "470 g", (0, 1, 2, 3) if n == 4 else ()
        )
        load(a, 430, ("Tin", "Tin", "Disc", "Disc", "Tin"), "530 g", (0, 1, 2, 3) if n == 4 else ())
        for y, k in ((235, "Tin"), (302, "Disc")):
            item(a, 909, y, k)
            a.text(k, 961, y, 26, INK, align="left")
        if n == 4:
            a.text(
                "Tin = disc + 60 g",
                863,
                439,
                30,
                RED,
                bold=True,
                align="left",
                opacity=c.reveal("sixty grams more"),
            )
        if n == 7:
            a.text("Tin: 130 g", 887, 425, 30, RED, bold=True, align="left")
            a.text("Disc: 70 g", 887, 474, 30, GREEN, bold=True, align="left")
    elif n <= 6:
        load(a, 246, ("Tin", "Tin", "Disc", "Disc", "Disc"), "470 g")
        load(a, 420, ("Disc",) * 5, "? g" if n == 5 else "350 g")
        item(a, 924, 419, "+60")
        item(a, 1014, 419, "+60")
        a.text("Two excess weights", 965, 486, 22, RED)
        if n == 6:
            a.text(
                "Disc: 350 ÷ 5 = 70 g      Tin: 70 + 60 = 130 g",
                640,
                550,
                34,
                INK,
                bold=True,
                opacity=c.reveal("one hundred and thirty"),
            )
    else:
        for y, title, left, right in (
            (243, "Foam-pad loads", "Pad", "Nothing"),
            (432, "Tin-and-disc loads", "Tin", "Disc"),
        ):
            a.text(title, 110, y, 31, INK, bold=True, align="left")
            item(a, 665, y, left)
            if right != "Nothing":
                item(a, 909, y, right)
            else:
                a.text("Empty", 909, y, 25, RULE)
        a.text("What is the difference measuring?", 640, 553, 32, INK)


def poster(draw):
    return draw(4, 1)
