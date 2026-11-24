"""Reflection orbits in a glazed 3-by-5 window and a constrained count of amber panes."""

from collections import Counter
from itertools import combinations

BACKGROUND = ("#18283a", "#273b49")
INK, BAR, AMBER, BLUE, FRAME = "#fff1ce", "#c8c9b4", "#ffc87a", "#69a6c6", "#243544"
BRIDGE = "In the three-by-five window, why does an order for five amber panes force the centre to be amber? Find two different ways the remaining four panes can be grouped."
HEAD = (
    "A strip in the mirror",
    "One choice per group",
    "Two mirrors in one window",
    "Find all the groups",
    "An exact colour order",
    "Spend the odd pane",
    "Count the two routes",
    "Check the actual glass",
)
GROUP = (("A", "B", "C", "B", "A"), ("D", "E", "F", "E", "D"), ("A", "B", "C", "B", "A"))
ACCENTS = dict(A="#9ecddb", B="#b7b3d2", C="#cfb3a3", D="#98c3a0", E="#c4c58f", F="#e5d8b9")


def check_maths():
    orbits = Counter(cell for row in GROUP for cell in row)
    assert sorted(orbits.values()) == [1, 2, 2, 2, 4, 4]
    orders = [
        keys
        for n in range(7)
        for keys in combinations(orbits, n)
        if sum(orbits[k] for k in keys) == 5
    ]
    assert len(orders) == 5 and all("F" in keys for keys in orders)
    assert all(
        GROUP[y][x] == GROUP[2 - y][x] == GROUP[y][4 - x] for x in range(5) for y in range(3)
    )


def pane(a, x, y, size, fill, label=""):
    a.box(x, y, size - 3, size - 3, fill=fill, edge=FRAME, stroke=3, radius=8)
    a.line([(x + 7, y + size * 0.42), (x + size * 0.38, y + 8)], "#d9e6dd", 2)
    if label:
        a.text(label, x + size * 0.63, y + size * 0.67, 23, FRAME, bold=True)


def window(a, x, y, size, mode, amber=()):
    for row, line in enumerate(GROUP):
        for col, k in enumerate(line):
            fill = (
                ACCENTS[k]
                if mode == "groups"
                else AMBER if k in amber else "#b5b8ac" if mode == "undecided" else BLUE
            )
            pane(a, x + col * size, y + row * size, size, fill, k if mode == "groups" else "")
    if mode in ("groups", "corner"):
        a.dashed((x + 2.5 * size, y - 17), (x + 2.5 * size, y + 3 * size + 17), INK, 3, 9, 8)
        a.dashed((x - 15, y + 1.5 * size), (x + 5 * size + 15, y + 1.5 * size), INK, 3, 9, 8)


def draw(a, n, c):
    a.text(HEAD[n - 1], 62, 69, 46, INK, bold=True, align="left")
    a.line([(62, 124), (1218, 124)], BAR, 3)
    if n <= 2:
        for i in range(7):
            pane(
                a,
                135 + 146 * i,
                260,
                117,
                (AMBER if i == 0 else "#b5b8ac") if n == 1 else AMBER if i in (0, 6) else BLUE,
                str(min(i, 6 - i) + 1) if n == 2 else "",
            )
            a.text(str(i + 1), 193 + 146 * i, 408, 27, INK)
        a.dashed((631, 200), (631, 396), INK, 4)
        a.text(
            (
                "Seven panes; one vertical mirror"
                if n == 1
                else "Three pairs + one centre = 4 choices of colour"
            ),
            640,
            493,
            32,
            INK,
            bold=True,
        )
        if n == 2:
            a.text(
                "16 with no preset pane; 8 with the first fixed",
                640,
                552,
                30,
                AMBER,
                bold=True,
                opacity=c.reveal("eight strips"),
            )
        return
    if n in (3, 4, 5, 6):
        mode = "corner" if n == 3 else "groups" if n in (4, 5) else "undecided"
        window(a, 112, 247, 86, mode, ("A",) if n == 3 else ("F",) if n == 6 else ())
        if n == 3:
            lines = (
                ("The top left pane", INK),
                ("Reflect left to right.", BAR),
                ("Reflect top to bottom.", BAR),
            )
        elif n == 4:
            lines = (
                ("A and B: four panes each", INK),
                ("C, D and E: two panes each", INK),
                ("F: the centre only", AMBER),
            )
        elif n == 5:
            lines = (
                ("Order: exactly 5 amber", AMBER),
                ("4, 4, 2, 2, 2, 1", INK),
                ("Can the centre stay blue?", INK),
            )
        else:
            lines = (
                ("The centre supplies 1.", AMBER),
                ("Four panes still needed", INK),
                ("One 4 or two 2s", INK),
            )
        for i, (s, col) in enumerate(lines):
            a.text(s, 637, 249 + 99 * i, 31, col, bold=i == 0, align="left")
        return
    for i, (groups, desc) in enumerate(
        ((("A", "F"), "Centre + one group of four"), (("C", "E", "F"), "Centre + two pairs"))
    ):
        x = 171 + i * 610
        window(a, x, 214, 65, "order", groups)
        a.text(desc, x + 161, 443, 27, INK, bold=True)
        if n == 7:
            a.text(
                "2 choices" if i == 0 else "3 choices",
                x + 161,
                493,
                29,
                AMBER,
                bold=True,
                opacity=c.reveal("two choices" if i == 0 else "three choices"),
            )
    a.text(
        (
            "2 + 3 = 5 different windows"
            if n == 7
            else "Each sample has 5 amber panes and both mirror lines."
        ),
        640,
        564,
        31,
        INK,
        bold=True,
        opacity=c.reveal("five orders") if n == 7 else 1,
    )


def poster(draw):
    return draw(7, 1)
