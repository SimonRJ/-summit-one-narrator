"""A scale that unrolls, two interval gauges, and a cropped-chart reconstruction."""

from fractions import Fraction
from math import floor
from stage import between, blend, clamp, ease, mix

BACKGROUND = ("#112b34", "#10232a")
PAPER = "#e3eee5"
MINT = "#88d7bd"
AZURE = "#77cce3"
BLUE = "#579ab9"
GOLD = "#ffd27c"
MUTED = "#a0bbb7"
GRID = "#436269"
INK = "#132f36"
WHITE = "#ebf4eb"
BRIDGE = "Read the first number on the vertical axis. Then watch what changes when the chart reveals the rest of each bar."


def poster(draw):
    return draw(9.38, 1.5)


def check_maths():
    assert (36 - 30, 42 - 30) == (6, 12) and 42 - 36 == 6
    assert Fraction(42, 36) == Fraction(7, 6) and Fraction(42 - 30, 36 - 30) == 2
    assert (12 + 3 * 2, 12 + 7 * 2) == (18, 26) and Fraction(26, 18) == Fraction(13, 9)
    assert [b for b in range(36) if 48 - b == 3 * (36 - b)] == [30]
    for crop in range(36):
        assert (48 - crop) - (36 - crop) == 12


def heading(a, main, unit):
    a.label("READING THE SCALE", 74, 51, 21, MINT, bold=True)
    a.label(main, 72, 102, 45, WHITE, bold=True)
    a.label(unit, 1175, 61, 23, MUTED, align="right")


def plot(
    a,
    start,
    values,
    tick,
    unit,
    names,
    show=(True, True),
    grow=(1, 1),
    baseline=True,
    ticks=True,
    opacity=1,
):
    bottom = 494
    max_value = max(values)
    scale = 270 / (max_value - start)

    def y(v):
        return bottom - (v - start) * scale

    a.label(unit, 98, 169, 24, MINT, bold=True)
    a.line([(166, 206), (166, bottom), (735, bottom)], MUTED, 3)
    if ticks:
        for raw in range(0, int(max_value + tick) + 1, tick):
            yy = y(raw)
            if yy > bottom + 0.01 or yy < 192:
                continue
            a.line([(166, yy), (735, yy)], GRID, 1.2)
            a.line([(155, yy), (166, yy)], MUTED, 2)
            a.label(
                str(raw),
                145,
                yy,
                27,
                PAPER,
                align="right",
                bold=abs(raw - start) < 0.01,
            )
    elif baseline:
        a.label(str(int(start)), 145, bottom, 23, PAPER, align="right", bold=True)
    xs = (303, 539)
    cols = (BLUE, AZURE)
    for x, v, col, name, op, p in zip(xs, values, cols, names, show, grow):
        top = mix(bottom, y(v), clamp(p))
        ht = bottom - top
        if ht > 1:
            a.box(x, top, 105, ht, radius=0, fill=col)
            a.line([(x, top), (x + 105, top)], "#c1edee", 3)
        if op:
            a.text(str(v), x + 52, y(v) - 22, 28, WHITE, bold=True, opacity=op)
        a.text(name, x + 52, bottom + 35, 27, PAPER, bold=True)
    if start > 0 and baseline:
        a.line(
            [
                (154, bottom + 8),
                (174, bottom - 4),
                (156, bottom + 10),
                (175, bottom + 0),
            ],
            GOLD,
            2.5,
        )
    return y, xs


def annotation(a, label, value, top, alpha=1):
    a.label(label, 816, top, 25, MUTED, alpha)
    a.label(value, 812, top + 50, 42, WHITE, alpha, bold=True)


def mystery_graph(
    a, division=0, prior=0, baseline_label=None, tops=(True, True), grow=(1, 1)
):
    y0 = 503
    unit = 14
    short = 6 * unit
    left = 285
    right = 545
    w = 96
    a.line([(182, 183), (182, y0), (714, y0)], MUTED, 3)
    for x, v, annot, p in zip((left, right), (36, 48), tops, grow):
        height = (v - 30) * unit
        a.box(
            x,
            y0 - height * p,
            w,
            height * p,
            radius=0,
            fill=BLUE if x == left else AZURE,
        )
        if annot:
            a.text(
                str(v), x + w / 2, y0 - height - 29, 34, WHITE, bold=True, opacity=annot
            )
    a.text("A", left + w / 2, 538, 23, MUTED, bold=True)
    a.text("B", right + w / 2, 538, 23, MUTED, bold=True)
    if baseline_label is None:
        a.box(95, 481, 67, 45, radius=4, fill="#284b52", edge=GRID)
        a.text("?", 128, 503, 29, GOLD, bold=True)
    else:
        a.text(str(baseline_label), 140, 503, 30, GOLD, bold=True)
    if prior > 0:
        x = mix(left, right - 106, prior)
        a.box(
            x,
            y0 - short,
            w,
            short,
            radius=0,
            fill=None,
            edge=GOLD,
            stroke=4,
            opacity=prior,
        )
        a.dashed(
            (x + w, y0 - short), (right + w + 25, y0 - short), GOLD, fraction=prior
        )
    for i in (1, 2):
        a.line([(right, y0 - i * short), (right + w, y0 - i * short)], INK, 4, division)
    return y0, short, right, w


def draw(a, scene, c):
    if scene == 1:
        heading(a, "The creek after rain", "Depth in centimetres")
        y, x = plot(
            a,
            30,
            (36, 42),
            3,
            "cm",
            ("Monday", "Tuesday"),
            show=(False, False),
            grow=(between(c.local, 0, 1.5), between(c.local, 0.55, 1.7)),
        )
        annotation(a, "Visible height", "6 and 12", 244, c.reveal("twice as tall"))
        a.label(
            "Where does zero sit?",
            808,
            460,
            31,
            GOLD,
            c.reveal("bottom of the scale"),
            bold=True,
        )
    elif scene == 2:
        heading(a, "Restore the missing scale", "Depth in centimetres")
        r = c.reveal("restoring the missing thirty", 2.35)
        start = 30 * (1 - r)
        y, _ = plot(
            a,
            start,
            (36, 42),
            6,
            "cm",
            ("Monday", "Tuesday"),
            show=(c.reveal("thirty six"), c.reveal("forty two")),
        )
        a.dashed((648, y(36)), (703, y(36)), GOLD)
        a.line([(688, y(36)), (688, y(42))], GOLD, 3)
        a.line([(677, y(42)), (699, y(42))], GOLD, 3)
        annotation(a, "Rise", "42 − 36 = 6 cm", 222, c.reveal("rise is six"))
        annotation(a, "Whole depths", "42 ÷ 36 = 7/6", 369, c.reveal("seven sixths"))
    elif scene == 3:
        heading(a, "Two tank gauges", "Litres")
        y, x = plot(
            a,
            12,
            (18, 26),
            2,
            "L",
            ("Tank A", "Tank B"),
            show=(False, False),
            grow=(c.reveal("one bar rises", 1.15), c.reveal("other rises seven", 1.8)),
        )
        annotation(a, "Starting level", "12 L", 214, c.reveal("twelve litres"))
        annotation(a, "One interval", "+2 L", 330, c.reveal("two litres"))
        a.label(
            "Fuller : other = ?",
            811,
            481,
            35,
            GOLD,
            c.reveal("ratio of the fuller"),
            bold=True,
        )
    elif scene == 4:
        heading(a, "Count from twelve", "Litres")
        p, q = c.reveal("eighteen"), c.reveal("twenty six")
        y, x = plot(a, 12, (18, 26), 2, "L", ("Tank A", "Tank B"), show=(p, q))
        for x0, v, when in zip(x, (18, 26), ("three intervals", "seven intervals")):
            g = c.reveal(when, 1.4)
            for k, val in enumerate(range(14, v + 1, 2)):
                a.line(
                    [(x0, y(val)), (x0 + 105, y(val))],
                    INK,
                    2,
                    clamp(g * ((v - 12) / 2) - k),
                )
        annotation(a, "Tank A", "12 + 6 = 18", 211, p)
        annotation(a, "Tank B", "12 + 14 = 26", 330, q)
        a.label(
            "26 : 18 = 13 : 9",
            809,
            483,
            36,
            GOLD,
            c.reveal("thirteen to nine"),
            bold=True,
        )
    elif scene == 5:
        heading(a, "Recover an erased label", "Unknown baseline")
        mystery_graph(
            a,
            tops=(c.reveal("thirty six"), c.reveal("forty eight")),
            grow=(between(c.local, 0, 0.8), between(c.local, 0.4, 0.9)),
        )
        annotation(a, "Visible lengths", "1 to 3", 257, c.reveal("three times as tall"))
        a.label(
            "Find the missing number.",
            810,
            437,
            26,
            GOLD,
            c.reveal("what number"),
            bold=True,
        )
    elif scene == 6:
        heading(a, "Slide a copy of the short bar", "Two equal gaps")
        slide = c.reveal("sliding the short bar", 1.9)
        divide = c.reveal("gap is two short bars", 1.3)
        y0, short, x, w = mystery_graph(a, divide, slide)
        mark = c.reveal("twelve units apart")
        a.line([(x + w + 48, y0 - short), (x + w + 48, y0 - 3 * short)], GOLD, 3, mark)
        for top in (y0 - short, y0 - 3 * short):
            a.line([(x + w + 38, top), (x + w + 58, top)], GOLD, 3, mark)
        annotation(a, "Difference of the tops", "48 − 36 = 12", 225, mark)
        annotation(a, "One short bar", "12 ÷ 2 = 6", 392, c.reveal("six units"))
    elif scene == 7:
        heading(a, "Put the baseline back", "Reconstruct the readings")
        show = c.reveal("must be thirty")
        mystery_graph(a, 1, 0, 30 if show > 0.3 else None)
        annotation(a, "Step down from A", "36 − 6 = 30", 227, c.reveal("step down six"))
        annotation(a, "Check B", "48 − 30 = 18", 365, c.reveal("minus thirty"))
        a.label(
            "18 = 3 × 6", 812, 512, 35, GOLD, c.reveal("three times six"), bold=True
        )
    else:
        heading(a, "What the crop preserves", "Changing the baseline")
        crop = c.reveal("cropping the same amount", 2.3)
        uncrop = c.reveal("whole readings", 2.2)
        start = 30 * crop * (1 - uncrop)
        y, _ = plot(a, start, (36, 48), 6, "units", ("A", "B"), show=(True, True))
        a.line([(679, y(36)), (679, y(48))], GOLD, 3)
        for top in (y(36), y(48)):
            a.line([(669, top), (689, top)], GOLD, 3)
        annotation(
            a, "Difference", "48 − 36 = 12", 216, c.reveal("preserves the difference")
        )
        annotation(
            a,
            "Ratio of the readings",
            "48 : 36 = 4 : 3",
            368,
            c.reveal("whole readings"),
        )
