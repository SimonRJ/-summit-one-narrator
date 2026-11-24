"""A verified six-singer block design counted through pair appearances."""

from itertools import combinations
from collections import Counter

BACKGROUND = ("#2b2537", "#3d3444")
INK, RULE, TEAL, GOLD, RED = "#f8eee3", "#9b8a9c", "#93dacb", "#f8ca88", "#f0a5a1"
BRIDGE = "On the ten-card roster, how many times does the pair Ada and Ben appear? Decide when your unit is a pair, an appearance of a pair, or a whole soundcheck."
HEAD = (
    "One trio, three pairs",
    "List each pair once",
    "Fix the pair first",
    "Which number repeats?",
    "Audit a six singer roster",
    "Start with all pairs",
    "Count inside the rehearsals",
    "Read the units",
)
ROSTER = ("ABF", "BCF", "CDF", "DEF", "EAF", "ABD", "BCE", "CDA", "DEB", "EAC")


def check_maths():
    counts = Counter(tuple(sorted(p)) for trio in ROSTER for p in combinations(trio, 2))
    assert len(counts) == 15 and set(counts.values()) == {2}
    assert len([t for t in ROSTER if "A" in t and "B" in t]) == 2 and 10 * 3 == 15 * 2


def singer(a, x, y, name, active=True):
    col = TEAL if active else RULE
    a.dot(x, y, 30, col)
    a.text(name, x, y + 1, 27, "#302a39", bold=True)


def draw(a, n, c):
    a.text(HEAD[n - 1], 63, 70, 46, INK, bold=True, align="left")
    a.line([(63, 123), (1216, 123)], RULE, 3)
    if n <= 2:
        positions = ((352, 217), (162, 459), (544, 459))
        pairs = ((0, 1), (0, 2), (1, 2))
        for i, (j, k) in enumerate(pairs):
            a.line([positions[j], positions[k]], GOLD, 5, 1 if n == 2 else 0.5)
        for nm, pt in zip("ABC", positions):
            singer(a, *pt, nm)
        for i, lab in enumerate(("Ada + Ben", "Ada + Cora", "Ben + Cora")):
            a.text(lab, 769, 231 + i * 77, 31, INK, align="left", opacity=1 if n == 2 else 0.4)
        a.text(
            "6 reports ÷ 2 = 3 pairs" if n == 2 else "Count each pair once",
            733,
            512,
            32,
            GOLD,
            bold=True,
            align="left",
        )
    elif n in (3, 4):
        for i, nm in enumerate("ABCDE"):
            singer(a, 243 + i * 197, 223, nm, i < 2)
        for i, third in enumerate("CDE"):
            x = 223 + 300 * i
            a.box(x, 360, 236, 74, fill="#493f54", edge=TEAL, stroke=3, radius=9)
            a.text(f"A  B  {third}", x + 118, 398, 33, INK, bold=True)
        a.text(
            (
                "Fix A and B; choose the third singer."
                if n == 3
                else "One distinct pair, three trio appearances."
            ),
            640,
            517,
            32,
            GOLD,
            bold=True,
        )
    elif n == 5:
        for i, initial in enumerate("ABCDEF"):
            singer(a, 196 + 176 * i, 248, initial)
        a.text("Three singers per soundcheck", 640, 386, 34, INK, bold=True)
        a.text("Each unordered pair shares exactly two soundchecks.", 640, 469, 32, GOLD, bold=True)
    elif n == 7:
        for i, trio in enumerate(ROSTER):
            x = 89 + (i % 5) * 229
            y = 231 + (i // 5) * 122
            contains = "A" in trio and "B" in trio
            col = GOLD if contains and n == 7 else RULE
            a.box(
                x,
                y,
                190,
                80,
                fill="#4c4054",
                edge=col,
                radius=10,
                stroke=4 if contains and n == 7 else 2,
            )
            a.text(
                "  ".join(trio), x + 95, y + 42, 32, col if n == 7 and contains else INK, bold=True
            )
        a.text(
            (
                "Every pair shares exactly two soundchecks."
                if n == 5
                else "ABF and ABD each contain the pair AB."
            ),
            640,
            528,
            32,
            GOLD,
            bold=True,
            opacity=c.reveal("with Fay once") if n == 7 else 1,
        )
    else:
        values = (
            ("6 singers", "Each names 5 partners"),
            ("15 different pairs", "6 × 5 ÷ 2"),
            ("30 pair appearances", "15 × 2 rehearsals per pair"),
            ("10 soundchecks", "30 ÷ 3 pairs per trio"),
        )
        for i, (l, r) in enumerate(values[:3] if n == 6 else values):
            y = 207 + i * 88
            a.text(l, 136, y, 31, TEAL, bold=True, align="left")
            a.text(r, 666, y, 29, INK, align="left")
        if n == 6:
            a.text(
                "How many pair appearances fit on one trio’s card?", 640, 528, 30, GOLD, bold=True
            )


def poster(draw):
    return draw(7, 1)
