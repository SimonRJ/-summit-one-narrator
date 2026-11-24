"""A logged cargo height, a stopped interval and a signed descent."""

from fractions import Fraction

BACKGROUND = ("#eae9dc", "#d8e3d9")
INK, GRID, UP, DOWN, FLAT, PAPER = "#22383c", "#879b94", "#167366", "#a64735", "#62597a", "#f7f5e9"
BRIDGE = "The winch’s last segment slopes downward. Which interval is fastest when direction is ignored, and which is fastest upward? Keep the two waiting seconds when you average the whole log."
HEAD = (
    "The winch clock",
    "Level each interval",
    "The largest lift",
    "Compare the climbs",
    "A level line and a drop",
    "Keep the direction",
    "Two averages for one log",
    "Read the question first",
)
T = (0, 3, 9, 11, 15)
H = (2, 14, 32, 32, 12)


def check_maths():
    changes = [b - a for a, b in zip(H, H[1:])]
    rates = [Fraction(v, t - s) for v, s, t in zip(changes, T, T[1:])]
    assert rates == [4, 3, 0, -5] and Fraction(sum(changes), 15) == Fraction(2, 3)
    assert Fraction(sum(abs(v) for v in changes), 15) == Fraction(10, 3)


def height_chart(a, max_i, n, c):
    x0, base = 132, 490
    X = lambda t: x0 + 38 * t
    Y = lambda m: base - 7.6 * m
    for h in (0, 8, 16, 24, 32):
        a.line([(x0, Y(h)), (X(15), Y(h))], GRID, 1)
        a.text(str(h), x0 - 26, Y(h), 19, INK)
    for t in T:
        a.line([(X(t), base), (X(t), base + 8)], INK, 2)
        a.text(str(t), X(t), base + 29, 22, INK)
    a.line([(x0, 213), (x0, base), (X(15), base)], INK, 3)
    a.text("Height above floor (m)", x0, 169, 27, INK, align="left")
    a.text("Time since start (s)", 407, 565, 26, INK)
    segment_cues = {
        1: {0: "At three seconds"},
        3: {1: "At nine seconds"},
        5: {2: "until eleven seconds", 3: "it descends"},
    }
    for i in range(max_i):
        cue = segment_cues.get(n, {}).get(i)
        alpha = c.reveal(cue, duration=0.8) if cue else 1
        col = (UP, UP, FLAT, DOWN)[i]
        a.line([(X(T[i]), Y(H[i])), (X(T[i + 1]), Y(H[i + 1]))], col, 6, alpha)
    for i in range(max_i + 1):
        cue = segment_cues.get(n, {}).get(i - 1)
        a.dot(X(T[i]), Y(H[i]), 7, INK, c.reveal(cue) if cue else 1)


def draw(a, n, c):
    a.text(HEAD[n - 1], 61, 72, 47, INK, bold=True, align="left")
    a.line([(61, 124), (1217, 124)], GRID, 3)
    height_chart(a, 1 if n <= 2 else 2 if n in (3, 4) else 4, n, c)
    if n == 1:
        items = (("At 0 seconds", "2 m"), ("At 3 seconds", "14 m"))
    elif n == 2:
        items = (
            ("Height gained", "14 − 2 = 12 m"),
            ("Time interval", "3 seconds"),
            ("Upward rate", "12 ÷ 3 = 4 m/s"),
        )
    elif n == 3:
        items = (("First rise", "12 m in 3 s"), ("Second rise", "18 m in 6 s"))
    elif n == 4:
        items = (("0–3 seconds", "12 ÷ 3 = 4 m/s"), ("3–9 seconds", "18 ÷ 6 = 3 m/s"))
    elif n == 5:
        items = (("9–11 seconds", "32 m to 32 m"), ("11–15 seconds", "32 m to 12 m"))
    elif n == 6:
        items = (
            ("Holding still", "0 m/s"),
            ("Signed descent", "−20 ÷ 4 = −5 m/s"),
            ("Speed of descent", "5 m/s"),
        )
    elif n == 7:
        items = (
            ("Net change", "12 − 2 = 10 m"),
            ("Total travel", "12 + 18 + 20 = 50 m"),
            ("Whole time", "15 seconds"),
        )
    else:
        items = (
            ("Average height change", "10 ÷ 15 = ⅔ m/s"),
            ("Average speed", "50 ÷ 15 = 3⅓ m/s"),
        )
    for i, (lab, val) in enumerate(items):
        cues = {
            1: ("two metres", "fourteen metres"),
            2: ("twelve metres", "three seconds", "four metres per second"),
            3: ("first rise of twelve", "eighteen metres"),
            4: ("four metres per second", "three metres per second"),
            5: ("until eleven seconds", "twelve metres"),
            6: ("rate zero", "negative five", "speed is five"),
            7: ("ten metres", "fifty metres", "fifteen seconds"),
            8: ("Net height change", "three and one third"),
        }
        alpha = c.reveal(cues[n][i])
        y = 203 + i * (110 if len(items) == 3 else 157)
        a.text(lab, 775, y, 26, INK, align="left")
        a.text(
            val,
            775,
            y + 49,
            33,
            DOWN if n == 6 and i else UP,
            bold=True,
            align="left",
            opacity=alpha,
        )


def poster(draw):
    return draw(6, 1)
