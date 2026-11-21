"""A sail slides on its rail, a fence divides a field, and a rectangle pairs areas."""

from fractions import Fraction
from math import pi, sin
from stage import between, blend, clamp, ease, mix

BACKGROUND = ("#29263a", "#202431")
LINE = "#565369"
LILAC = "#cfb4ec"
AQUA = "#95dad0"
GOLD = "#f4c780"
CORAL = "#e99593"
WHITE = "#f4f0e9"
MUTED = "#c0bccb"
TEAL_FILL = "#396163"
PLUM_FILL = "#665377"
BRIDGE = "Follow the perpendicular line from the moving corner to the base. Use that distance to compare the areas."


def poster(draw):
    return draw(10.75, 1.5)


def check_maths():
    def area(vertices):
        (x0, y0), (x1, y1), (x2, y2) = vertices
        return Fraction(abs((x1 - x0) * (y2 - y0) - (x2 - x0) * (y1 - y0)), 2)

    for x in range(-5, 13):
        assert area([(0, 0), (6, 0), (x, 4)]) == 12
    for x in range(10):
        assert area([(0, 0), (4, 0), (x, 8)]) == 16
        assert area([(4, 0), (9, 0), (x, 8)]) == 20
    for x in range(1, 12):
        assert area([(0, 0), (12, 0), (x, 3)]) == 18
        assert area([(0, 8), (12, 8), (x, 3)]) == 30


def title(a, name):
    a.label("AREA CONSTRUCTIONS", 74, 53, 21, LILAC, bold=True)
    a.label(name, 72, 107, 45, WHITE, bold=True)


def right_angle(a, x, y, up=True, q=1):
    s = -1 if up else 1
    a.line([(x - 16, y), (x - 16, y + s * 16), (x, y + s * 16)], GOLD, 2.4, q)


def height(a, x, y_top, y_base, op=1, tag=None):
    a.dashed((x, y_top), (x, y_base), GOLD, 3, 8, 6, op)
    right_angle(a, x, y_base, up=y_top < y_base, q=op)
    if tag:
        a.label(tag, x + 12, (y_top + y_base) / 2, 26, GOLD, op, bold=True)


def panel(a, note, line, y, op=1):
    a.label(note, 822, y, 24, MUTED, op)
    a.label(line, 817, y + 53, 40, WHITE, op, bold=True)


def sail(a, x, ruler=0, base_label=0, extend=0):
    left, right, base, rail = 213, 549, 491, 267
    a.line([(110, rail), (733, rail)], LILAC, 4)
    for end in (110, 733):
        a.dot(end, rail, 5, LILAC)
    a.polygon([(left, base), (right, base), (x, rail)], TEAL_FILL, AQUA, 3)
    a.line([(left, base), (right, base)], AQUA, 5)
    if x > right:
        a.dashed((right, base), (x + 26, base), MUTED, 2.3, 8, 6, extend)
    if x < left:
        a.dashed((left, base), (x - 28, base), MUTED, 2.3, 8, 6, extend)
    if ruler:
        height(a, x, rail, base, ruler, "4 cm" if ruler > 0.8 else None)
    for px, py, col in ((left, base, AQUA), (right, base, AQUA), (x, rail, GOLD)):
        a.dot(px, py, 7, col)
    a.text(
        "6 cm", (left + right) / 2, base + 36, 29, AQUA, bold=True, opacity=base_label
    )


def field(a, gate, split, units=0, guides=0):
    x0, x1 = 194, 608
    ybase, ytop = 540, 172
    unit = 46
    mid = x0 + 4 * unit
    peak = 418
    a.polygon([(x0, ybase), (x1, ybase), (peak, ytop)], TEAL_FILL, AQUA, 3)
    if split:
        a.polygon(
            [(mid, ybase), (x1, ybase), (peak, ytop)],
            blend(TEAL_FILL, PLUM_FILL, split),
            None,
        )
        a.line(
            [(mid, ybase), (mix(mid, peak, split), mix(ybase, ytop, split))], WHITE, 3
        )
    for i in range(1, 9):
        if i == 4:
            continue
        g = ease(clamp(units * 9 - i + 0.8))
        x = x0 + i * unit
        if g:
            a.line(
                [(x, ybase), (mix(x, peak, g), mix(ybase, ytop, g))],
                blend(TEAL_FILL, "#beaeb6", g * 0.7),
                1.55,
            )
    a.line([(x0, ybase), (x1, ybase)], GOLD, 4)
    for i in range(10):
        x = x0 + i * unit
        a.line([(x, ybase - 6), (x, ybase + 6)], GOLD, 2.1)
    if guides:
        height(a, peak, ytop, ybase, guides)
    a.dot(peak, ytop, 6, LILAC)
    a.dot(mid, ybase, 8, GOLD, gate)
    a.text("4 m", (x0 + mid) / 2, ybase + 39, 27, AQUA, bold=True, opacity=gate)
    a.text("5 m", (mid + x1) / 2, ybase + 39, 27, LILAC, bold=True, opacity=gate)
    if gate < 0.4:
        a.text(
            "9 m",
            (x0 + x1) / 2,
            ybase + 35,
            27,
            GOLD,
            bold=True,
            opacity=1 - gate / 0.4,
        )


def rect(
    a, x, connect=1, lower=1, upper=1, lower_height=0, upper_height=0, marked=False
):
    x0, x1, y0, y1 = 170, 674, 180, 516
    yp = y1 - 3 * 42
    a.box(x0, y0, x1 - x0, y1 - y0, radius=0, fill="#302c42")
    if lower:
        a.polygon([(x0, y1), (x1, y1), (x, yp)], blend("#302c42", TEAL_FILL, lower))
    if upper:
        a.polygon([(x0, y0), (x1, y0), (x, yp)], blend("#302c42", PLUM_FILL, upper))
    a.line([(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)], MUTED, 3)
    for xx, yy in [(x0, y0), (x1, y0), (x0, y1), (x1, y1)]:
        a.line([(x, yp), (mix(x, xx, connect), mix(yp, yy, connect))], WHITE, 2.5)
    a.line([(x0, y1), (x1, y1)], AQUA, 4, lower)
    a.line([(x0, y0), (x1, y0)], LILAC, 4, upper)
    if lower_height:
        height(a, x, yp, y1, lower_height, "3 m" if marked else None)
    if upper_height:
        height(a, x, yp, y0, upper_height, "5 m" if marked else None)
    a.dot(x, yp, 8, GOLD)
    a.text("12 m", (x0 + x1) / 2, 558, 28, AQUA, bold=True)
    a.label("8 m", x0 - 22, (y0 + y1) / 2, 28, LILAC, align="right", bold=True)


def draw(a, scene, c):
    if scene == 1:
        title(a, "A sail on a rail")
        x = mix(307, 646, c.reveal("sliding the top corner", 4.8))
        sail(a, x)
        a.label(
            "The base stays put.",
            821,
            283,
            31,
            AQUA,
            c.reveal("while the base"),
            bold=True,
        )
        a.label(
            "What about the area?",
            819,
            371,
            31,
            GOLD,
            c.reveal("can its area change"),
            bold=True,
        )
    elif scene == 2:
        title(a, "Measure at a right angle")
        travel = c.reveal("as the peg travels", 3.5)
        x = mix(311, 665, travel)
        sail(
            a,
            x,
            c.reveal("four centimetres above", 1.1),
            c.reveal("six centimetres"),
            1,
        )
        panel(
            a, "Area of the sail", "½ × 6 × 4", 239, c.reveal("half of six times four")
        )
        a.label("= 12 cm²", 818, 370, 50, AQUA, c.reveal("is twelve"), bold=True)
        a.label(
            "Height to the base line",
            821,
            468,
            26,
            GOLD,
            c.reveal("beyond the end"),
            bold=True,
        )
    elif scene == 3:
        title(a, "Two plots share a fence")
        g = c.reveal("a gate splits", 0.9)
        field(a, g, c.reveal("divide the field", 1.4))
        panel(a, "Whole field", "36 m²", 245, c.reveal("thirty six square metres"))
        a.label(
            "Area beside the 5 m fence?",
            822,
            415,
            28,
            LILAC,
            c.reveal("area beside the longer"),
            bold=True,
        )
    elif scene == 4:
        title(a, "Divide by fence length")
        u = c.reveal("nine equal parts", 1.9)
        field(a, 1, 1, u, c.reveal("same perpendicular height", 0.9))
        panel(a, "Area ratio", "4 : 5", 211, c.reveal("ratio four to five"))
        panel(a, "One part", "36 ÷ 9 = 4 m²", 333, c.reveal("each part is four"))
        a.label(
            "5 × 4 = 20 m²",
            816,
            505,
            42,
            LILAC,
            c.reveal("twenty square metres"),
            bold=True,
        )
    elif scene == 5:
        title(a, "A point inside a rectangle")
        q = c.reveal("draw a line to each corner", 1.5)
        lo = c.reveal("triangle along the bottom", 1)
        up = c.reveal("triangle along the top", 0.9)
        rect(a, 374, q, lo, up)
        panel(a, "Area along the bottom", "18 m²", 242, lo)
        panel(a, "Area along the top", "?", 392, up)
    elif scene == 6:
        title(a, "Pair the opposite bases")
        left = c.reveal("sideways the point moves", 1.7)
        x = 374 + 145 * left
        hr = c.reveal("perpendicular heights", 1)
        rect(a, x, 1, 1, 1, hr, hr)
        panel(
            a, "The two heights", "Together 8 m", 226, c.reveal("heights add to eight")
        )
        panel(
            a,
            "Combined area",
            "½ × 12 × 8",
            367,
            c.reveal("half of twelve times eight"),
        )
        a.label("= 48 m²", 817, 498, 44, GOLD, c.reveal("forty eight"), bold=True)
    elif scene == 7:
        title(a, "Check by measuring both heights")
        low = c.reveal("bottom height must be three", 0.8)
        up = c.reveal("height left for the top", 0.8)
        rect(a, 519, 1, 1, 1, low, up, True)
        panel(
            a,
            "Area along the top",
            "48 − 18 = 30 m²",
            230,
            c.reveal("top area is thirty"),
        )
        a.label("Bottom  ½ × 12 × 3 = 18", 813, 384, 30, AQUA, low, bold=True)
        a.label("Top  ½ × 12 × 5 = 30", 813, 466, 30, LILAC, up, bold=True)
    else:
        title(a, "Three marks to make on paper")
        cols = (101, 501, 901)
        # Each thumbnail is a distinct geometric construction, revealed by its own spoken cue.
        p = c.reveal("mark the base", 0.8)
        x = cols[0]
        a.line(
            [(x + 10, 430), (x + 206, 430), (x + 246, 280), (x + 10, 430)], AQUA, 3, p
        )
        a.dashed(
            (x + 206, 430),
            (x + 271, 430),
            MUTED,
            fraction=c.reveal("extending the base line"),
        )
        h = c.reveal("height at a right angle", 0.8)
        a.dashed((x + 246, 280), (x + 246, 430), GOLD, 3, fraction=h)
        right_angle(a, x + 246, 430, q=h)
        a.text("Perpendicular height", x + 130, 510, 28, WHITE, bold=True, opacity=p)
        p = c.reveal("shared height", 1)
        x = cols[1]
        pts = [(x, 430), (x + 226, 430), (x + 141, 280)]
        a.line(pts + [pts[0]], LILAC, 3, p)
        a.line([(x + 83, 430), pts[-1]], AQUA, 3, p)
        a.text("Shared height", x + 118, 510, 28, WHITE, bold=True, opacity=p)
        p = c.reveal("equal parallel bases", 1)
        x = cols[2]
        top, bot = 282, 430
        px, py = x + 129, 385
        box = [(x, top), (x + 223, top), (x + 223, bot), (x, bot), (x, top)]
        a.line(box, MUTED, 3, p)
        for pt in box[:-1]:
            a.line([pt, (px, py)], LILAC, 2, p)
        a.dashed((px, top), (px, bot), GOLD, 3, fraction=p)
        a.text("Opposite bases", x + 112, 510, 28, WHITE, bold=True, opacity=p)
