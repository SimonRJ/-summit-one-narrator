"""Isometric cube workshop for T13.3. Coordinates are unit-cube centres."""

from itertools import product
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont

BG = "#191d35"
INK = "#f8f2e6"
SOFT = "#aebbd0"
RIM = "#27364a"
WARM = ("#ffd187", "#e5a24e", "#bd703f")
COOL = ("#b7d7ec", "#70a3c4", "#4b7299")
MINT = ("#c6f2de", "#7fcab0", "#479d8d")
DIM = ("#5f6582", "#434a69", "#323a57")


@lru_cache(None)
def font(size, bold=False):
    return ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans" + ("-Bold" if bold else "") + ".ttf",
        round(size * 1.5),
    )


def text(d, x, y, words, size=28, colour=INK, bold=False, anchor="lm"):
    d.text((round(1.5 * x), round(1.5 * y)), words, font=font(size, bold), fill=colour, anchor=anchor)


def poly(d, points, fill):
    pts = [(round(x * 1.5), round(y * 1.5)) for x, y in points]
    d.polygon(pts, fill=fill)
    d.line(pts + [pts[0]], fill=RIM, width=3, joint="curve")


def progress(t, lo, hi):
    x = min(1, max(0, (t - lo) / (hi - lo)))
    return x * x * (3 - 2 * x)


def cube(d, origin, xyz, width, colours, lift=0):
    x, y, z = xyz
    cx = origin[0] + width * (x - y)
    cy = origin[1] + width * 0.48 * (x + y) - width * 1.00 * z - lift
    w, h, v = width, width * 0.48, width
    top = (cx, cy - h)
    left = (cx - w, cy)
    mid = (cx, cy + h)
    right = (cx + w, cy)
    poly(d, [left, mid, (cx, cy + h + v), (cx - w, cy + v)], colours[1])
    poly(d, [mid, right, (cx + w, cy + v), (cx, cy + h + v)], colours[2])
    poly(d, [top, right, mid, left], colours[0])


def solid(d, coords, origin=(390, 277), size=50, palette=lambda x, y, z: COOL, lift=lambda z: 0):
    for c in sorted(coords, key=lambda k: (k[2], k[0] + k[1], k[0])):
        cube(d, origin, c, size, palette(*c), lift(c[2]))


def block(x, y, z):
    return product(range(x), range(y), range(z))


def panel(d, x, y, value, detail, colour=WARM[0]):
    text(d, x, y, value, 40, colour, True)
    text(d, x, y + 49, detail, 23, INK)


def region(n, t, span, voice_at):
    im = Image.new("RGB", (1920, 1080), BG)
    d = ImageDraw.Draw(im)
    for y in range(176, 608, 32):
        for x in range(52, 1285, 36):
            d.ellipse(
                (round(x * 1.5), round(y * 1.5), round(x * 1.5) + 3, round(y * 1.5) + 3), fill="#353d55"
            )
    title = [
        "Which cubes are hidden?",
        "See the cubes behind the drawing",
        "Build a 4 × 3 × 2 block",
        "Lift the upper layer",
        "Peel a painted cube",
        "Sort by painted faces",
        "Read a staircase by levels",
        "Find the core of a 4 × 4 × 4 cube",
    ][n]
    text(d, 53, 48, "SOLID GEOMETRY   /   THE CUBE WORKSHOP", 19, MINT[0], True)
    text(d, 50, 114, title, 52, INK, True)
    if n in (0, 1, 2, 3):
        lift_distance = (45 if n == 0 else 58) * progress(t, 1.8, 6)
        if n == 2:
            lift_distance = 0
        solid(
            d,
            block(4, 3, 2),
            (310, 319),
            51,
            lambda x, y, z: WARM if not z else COOL,
            lambda z: z * lift_distance,
        )
        if n == 0:
            panel(d, 745, 278, "One level at a time", "Slide the top layer away.")
            text(d, 745, 410, "Count a layer, then the layers.", 26, MINT[0])
        elif n == 1:
            panel(d, 737, 265, "Look under the top", "Every cube uses a place in a layer.")
            text(d, 737, 402, "A face you cannot see still counts.", 24, MINT[0])
        elif n == 2:
            panel(d, 737, 264, "4 long   3 wide   2 high", "How many unit cubes fill the block?")
            if t > 6:
                text(d, 737, 400, "Sketch one 4 × 3 layer.", 28, MINT[0])
        else:
            panel(d, 737, 248, "4 × 3 = 12", "Twelve cubes in one level.")
            if t > 3.4:
                panel(d, 737, 395, "12 × 2 = 24", "Two complete layers.", MINT[0])
    elif n == 4:
        peel = progress(t, 10.4, 16.4)
        if peel < 1:
            for x, y, z in sorted(block(3, 3, 3), key=lambda k: (k[2], k[0] + k[1], k[0])):
                if (x, y, z) == (1, 1, 1):
                    cube(d, (380, 377), (x, y, z), 44, MINT)
                    continue
                if peel > 0.04 and ((x + y + z) % 3) / 3 < peel - 0.30:
                    continue
                ox = (x - 1) * peel * 38
                oy = (y - 1) * peel * 38
                cube(
                    d, (380 + ox - oy, 377 + (ox + oy) * 0.48), (x, y, z), 44, WARM, (z - 1) * peel * 26
                )
        else:
            solid(d, [(1, 1, 1)], (380, 377), 44, lambda *c: MINT)
        panel(d, 742, 265, "Paint the outside", "The original block has 27 small cubes.")
        if t > 12.4:
            panel(d, 742, 415, "1 unpainted", "The cube in the very centre.", MINT[0])
    elif n == 5:
        # Every face has one unique centre. Bring those six forward as an unfolded net.
        phase = (
            0
            if t < voice_at["edges"]
            else 1
            if t < voice_at["centres"]
            else 2
            if t < voice_at["hidden"]
            else 3
        )
        group = [(8, "corner cubes"), (12, "edge middles"), (6, "face centres"), (1, "interior cube")]
        cells = list(block(3, 3, 3))

        def shade(x, y, z):
            boundary = sum(v in (0, 2) for v in (x, y, z))
            return [MINT, MINT, COOL, WARM][boundary] if boundary == 3 - phase else DIM

        solid(d, [(1, 1, 1)] if phase == 3 else cells, (260, 315), 41, shade)
        if phase == 2:
            face_net = [(1, 0), (0, 1), (1, 1), (2, 1), (3, 1), (1, 2)]
            for col, row in face_net:
                left = 511 + col * 70
                top = 223 + row * 70
                for i, j in product(range(3), repeat=2):
                    d.rectangle(
                        (
                            round((left + i * 21) * 1.5),
                            round((top + j * 21) * 1.5),
                            round((left + (i + 1) * 21 - 2) * 1.5),
                            round((top + (j + 1) * 21 - 2) * 1.5),
                        ),
                        fill=MINT[0] if i == j == 1 else DIM[0],
                    )
            text(d, 651, 477, "Six faces unfolded", 24, MINT[0], True, "mm")
        for i, (qty, desc) in enumerate(group):
            text(d, 840, 228 + i * 77, str(qty), 43, MINT[0] if i == phase else SOFT, True)
            text(d, 910, 228 + i * 77, desc, 26, INK if i == phase else SOFT)
        if phase == 3:
            text(d, 77, 562, "8 + 12 + 6 + 1 = 27", 31, MINT[0], True)
    elif n == 6:
        staircase = [(x, y, z) for z in range(3) for x in range(3 - z) for y in range(3 - z)]
        solid(
            d,
            staircase,
            (350, 414),
            57,
            lambda x, y, z: [WARM, COOL, MINT][z],
            lambda z: z * 42 * progress(t, 1, 7),
        )
        for i, (v, why) in enumerate(
            [("9", "3 × 3 on the bottom"), ("4", "2 × 2 in the middle"), ("1", "1 × 1 on top")]
        ):
            text(d, 741, 248 + i * 76, v, 42, [WARM, COOL, MINT][i][0], True)
            text(d, 812, 248 + i * 76, why, 28)
        if t > 6.5:
            text(d, 739, 501, "9 + 4 + 1 = 14", 35, INK, True)
    else:
        show = t > span - 4.3
        solid(
            d,
            [(x, y, z) for x, y, z in block(4, 4, 4) if not show or all(v in (1, 2) for v in (x, y, z))],
            (355, 319),
            42,
            lambda x, y, z: MINT if all(v in (1, 2) for v in (x, y, z)) else COOL,
        )
        panel(d, 742, 269, "Paint, cut, then count", "Which cubes touch none of the six faces?")
        if show:
            panel(d, 742, 432, "2 × 2 × 2 = 8", "Two interior cubes in each direction.", MINT[0])
    return im
