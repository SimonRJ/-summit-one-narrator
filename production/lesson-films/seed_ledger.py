"""Pod frequencies, a genuine zero observation and deviations from a target mean."""

from fractions import Fraction

BACKGROUND = ("#233c31", "#354936")
INK, RULE, GOLD, LEAF, PINK = "#f5eedb", "#8aa28b", "#f0c16b", "#acd59e", "#f5a28b"
BRIDGE = "Put the empty pod in the count of observations. In the tray with a missing frequency, how much surplus does one five-seed pod contribute above the required mean?"
HEAD = (
    "A pod that holds nothing",
    "Make every copy visible",
    "What the row label misses",
    "Give the pod its vote",
    "The missing frequency",
    "Measure a shortfall",
    "Balance the surplus",
    "Check the ledger",
)


def check_maths():
    assert Fraction(0 + 3 * 2 + 2 * 5, 1 + 3 + 2) == Fraction(8, 3)
    assert [k for k in range(20) if Fraction(10 + 5 * k, 6 + k) == Fraction(5, 2)] == [2]


def table(a, counts, show_total):
    xs = (172, 354, 552)
    for x, title in zip(xs, ("Seeds/pod", "Pods", "Total seeds")):
        a.text(title, x, 192, 24, INK, bold=True)
    for i, (v, count) in enumerate(zip((0, 2, 5), counts)):
        y = 243 + 78 * i
        a.line([(86, y - 23), (639, y - 23)], RULE, 2)
        for j, t in enumerate(
            (
                str(v),
                str(count),
                (
                    str(v * count)
                    if show_total and isinstance(count, int)
                    else "?" if count == "?" else "—"
                ),
            )
        ):
            a.text(t, xs[j], y + 14, 34, LEAF if j == 1 else GOLD if j == 2 else INK, bold=True)


def draw(a, n, c):
    a.text(HEAD[n - 1], 62, 72, 46, INK, bold=True, align="left")
    a.line([(62, 122), (1217, 122)], RULE, 3)
    counts = (1, 3, 2) if n <= 4 else (1, 5, 2) if n >= 7 else (1, 5, "?")
    table(a, counts, n in (2, 4, 7, 8))
    if n == 1:
        rows = (("An empty pod", "0 seeds"), ("What does it add?", "One observation"))
    elif n == 2:
        rows = (("Seeds", "0 + 6 + 10 = 16"), ("Pods", "1 + 3 + 2 = 6"), ("Mean", "16 ÷ 6 = 2⅔"))
    elif n == 3:
        rows = (("Three labels", "(0 + 2 + 5) ÷ 3"), ("Which tray?", "One copy of each"))
    elif n == 4:
        rows = (
            ("Value × frequency", "Counts all the seeds"),
            ("Sum of frequencies", "Counts all the pods"),
        )
    elif n == 5:
        rows = (
            ("Target mean", "2½ seeds per pod"),
            ("Missing frequency", "How many five-seed pods?"),
        )
    elif n == 6:
        rows = (
            ("One empty pod", "Shortfall 2½"),
            ("Five two-seed pods", "5 × ½ = 2½"),
            ("Total shortfall", "5 seeds"),
        )
    elif n == 7:
        rows = (
            ("Surplus per five-seed pod", "5 − 2½ = 2½"),
            ("Pods needed", "5 ÷ 2½ = 2"),
            ("Ordinary check", "20 seeds, 8 pods"),
        )
    else:
        rows = (
            ("Total seeds", "0 + 10 + 10 = 20"),
            ("Number of pods", "1 + 5 + 2 = 8"),
            ("Mean", "20 ÷ 8 = 2½"),
        )
    timed = {
        (1, 1): "number of pods",
        (2, 2): "two and two thirds",
        (6, 2): "combined shortfall",
        (7, 1): "missing frequency is two",
        (7, 2): "total is twenty",
        (8, 2): "two and a half",
    }
    for i, (lab, val) in enumerate(rows):
        y = 190 + i * (115 if len(rows) == 3 else 160)
        cue = timed.get((n, i))
        a.text(lab, 716, y, 25, INK, align="left")
        a.text(
            val,
            716,
            y + 51,
            34,
            PINK if n == 6 else GOLD,
            bold=True,
            align="left",
            opacity=c.reveal(cue) if cue else 1,
        )


def poster(draw):
    return draw(6, 1)
