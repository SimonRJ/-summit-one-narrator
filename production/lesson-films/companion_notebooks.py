"""Nineteen illustrated notebook prompts. Each drawing follows its own problem."""

from math import cos, sin, pi
from PIL import Image, ImageDraw
from finish_tickets import box, line, txt, pt, ease, mix

INK = "#242d3b"
WHITE = "#fffaf0"
BLUE = "#28718b"
TEAL = "#35735c"
RED = "#a54b40"
GOLD = "#e9ae51"
PURPLE = "#67517d"
NAVY = "#25394a"
MINT = "#a4cbb0"
OCHRE = "#ba7439"
LINE = "#b8b5a6"
THEMES = {
    14: ("#f1f2e9", BLUE),
    15: ("#fbefe0", PURPLE),
    16: ("#eff2e8", TEAL),
    17: ("#f0ecf5", PURPLE),
    18: ("#faefdd", RED),
}


def center(d, x, y, value, size=31, colour=INK, face="b"):
    txt(d, x, y, value, size, colour, face, "mm")


def dot(d, x, y, r, colour, edge=None):
    d.ellipse(pt(x - r, y - r, x + r, y + r), fill=colour, outline=edge, width=3)


def polygon(d, points, fill, edge=None):
    coords = [pt(x, y) for x, y in points]
    d.polygon(coords, fill=fill)
    if edge:
        d.line(coords + [coords[0]], fill=edge, width=4)


def notes(d, x, y, rows):
    for j, (s, sz, col) in enumerate(rows):
        txt(d, x, y + 73 * j, s, sz, col, "s" if j == 0 else "r")


def pad(d, title, rubric, accent):
    txt(d, 65, 51, rubric.upper(), 23, accent, "b")
    txt(d, 65, 114, title, 48, INK, "s")
    line(d, 65, 162, 1215, 162, accent, 3)


def route_grid(d, p, answer):
    pad(d, "Count routes across three blocks", "street map", BLUE)
    for y in range(3):
        line(d, 119, 256 + y * 120, 677, 256 + y * 120, LINE, 6)
    for x in range(4):
        line(d, 119 + x * 186, 256, 119 + x * 186, 496, LINE, 6)
    values = ((1, 3, 6, 10), (1, 2, 3, 4), (1, 1, 1, 1))
    for y in range(3):
        for x in range(4):
            xx, yy = 119 + x * 186, 256 + y * 120
            dot(d, xx, yy, 23, BLUE if (x, y) in ((0, 2), (3, 0)) else "#e4ded0", INK)
            if answer and x + 2 - y <= p * 5:
                center(
                    d,
                    xx,
                    yy,
                    values[y][x],
                    22,
                    WHITE if (x, y) in ((0, 2), (3, 0)) else INK,
                )
    txt(d, 76, 550, "Start", 25, TEAL, "b")
    txt(d, 646, 201, "Finish", 25, RED, "b")
    notes(
        d,
        785,
        245,
        [
            ("Right or up", 38, INK),
            ("Five steps in each route.", 25, BLUE),
            ("Where can the two up steps go?", 23, INK),
        ],
    )
    if answer:
        txt(d, 785, 506, "Choose 2 of 5 positions: 10 routes.", 24, TEAL, "b")


def same_colour(d, p, answer):
    pad(d, "Can both top corners be endpoints?", "checkerboard route", BLUE)
    for j in range(2):
        for i in range(3):
            x, y = 130 + 180 * i, 277 + j * 180
            if i < 2:
                line(d, x, y, x + 180, y, LINE, 6)
            if j == 0:
                line(d, x, y, x, y + 180, LINE, 6)
    for j in range(2):
        for i in range(3):
            x, y = 130 + 180 * i, 277 + j * 180
            dot(d, x, y, 31, INK if (i + j) % 2 == 0 else GOLD, PURPLE)
            if j == 0 and i != 1:
                center(d, x, y - 63, "start" if i == 0 else "finish", 24, RED)
    notes(
        d,
        672,
        237,
        [
            ("Six places", 37, INK),
            ("Each step changes colour.", 29, BLUE),
            ("A six-dot route uses five steps.", 25, INK),
        ],
    )
    if answer:
        for j in range(6):
            dot(d, 700 + j * 72, 485, 21, INK if j % 2 == 0 else GOLD)
        txt(d, 673, 554, "Five changes mean different endpoint colours.", 23, RED, "b")


def six_schedule(d, p, answer):
    pad(d, "Six players, three courts", "the match secretary", BLUE)
    slots = [
        ("AF", "BE", "CD"),
        ("BF", "AC", "DE"),
        ("CF", "BD", "AE"),
        ("DF", "CE", "AB"),
        ("EF", "AD", "BC"),
    ]
    for col in range(3):
        x = 82 + 230 * col
        box(d, x, 208, 190, 78, "#d8e4cf", TEAL, 8)
        line(d, x + 95, 213, x + 95, 280, TEAL, 3)
        center(d, x + 95, 252, "Court " + str(col + 1), 23, INK)
    for j, row in enumerate(slots):
        y = 318 + 53 * j
        if answer and j < max(1, int(p * 6)):
            for col, game in enumerate(row):
                center(d, 178 + 230 * col, y, game, 29, BLUE, "m")
    notes(
        d,
        817,
        246,
        [
            ("15 games", 36, INK),
            ("At most 3 per round.", 26, BLUE),
            ("15 ÷ 3 gives a lower bound.", 22, INK),
        ],
    )
    if answer:
        txt(d, 817, 508, "Five rounds attain it.", 30, TEAL, "s")


def six_meetings(d, p, answer):
    pad(d, "Fit the extra meeting into three slots", "meeting planner", BLUE)
    for j, name in enumerate(("A", "E")):
        x = 144 + j * 328
        dot(d, x, 377, 47, BLUE if j == 0 else TEAL)
        center(d, x, 377, name, 42, WHITE)
        for yy, n in [(245, "B"), (377, "C"), (509, "D")]:
            target = 310
            line(d, x + (32 if j == 0 else -32), 377, target, yy, LINE, 3)
    for yy, n in [(245, "B"), (377, "C"), (509, "D")]:
        dot(d, 310, yy, 30, GOLD)
        center(d, 310, yy, n, 28)
    rows = [("1", "AB  +  DE"), ("2", "AC  +  BE"), ("3", "AD  +  CE")]
    txt(d, 657, 243, "A and E each require three slots.", 29, BLUE, "s")
    for j, (slot, pairs) in enumerate(rows):
        yy = 326 + 70 * j
        txt(d, 655, yy, "Slot " + slot, 23, INK, "b")
        line(d, 780, yy + 20, 1160, yy + 20, LINE, 2)
        if answer and j <= p * 3:
            txt(d, 813, yy, pairs, 35, TEAL, "m")


def tile(d, x, y, side, white_at):
    for j in range(2):
        for i in range(2):
            c = WHITE if 2 * j + i == white_at else NAVY
            s = side / 2
            d.rectangle(
                pt(x + i * s, y + j * s, x + (i + 1) * s, y + (j + 1) * s),
                fill=c,
                outline=GOLD,
                width=3,
            )


def shaded_tile(d, p, answer):
    pad(d, "Turn the one unshaded corner", "tile workshop", PURPLE)
    for j, corner in enumerate((0, 1, 3, 2)):
        if j == 0 or p > j / 5:
            x = 81 + j * 285
            tile(d, x, 269, 201, corner)
            center(
                d, x + 100, 514, ("Start", "¼ turn", "½ turn", "¾ turn")[j], 25, PURPLE
            )
    if answer:
        center(
            d,
            640,
            580,
            "Every position of the light corner belongs to one rotation class.",
            27,
            TEAL,
        )


def table_orders(d, p, answer):
    pad(d, "Seat four people around one table", "round-table seating", PURPLE)
    circle = (338, 367)
    dot(d, *circle, 105, "#a27750", "#6e5744")
    for j, n in enumerate("ABCD"):
        angle = -pi / 2 + j * pi / 2
        x = circle[0] + 150 * cos(angle)
        y = circle[1] + 150 * sin(angle)
        dot(d, x, y, 33, GOLD if n == "A" else MINT, NAVY)
        center(d, x, y, n, 34)
    notes(
        d,
        663,
        239,
        [
            ("Keep A at the top.", 37, INK),
            ("Arrange the other three clockwise.", 26, PURPLE),
        ],
    )
    if answer:
        for j, s in enumerate(("BCD", "BDC", "CBD", "CDB", "DBC", "DCB")):
            if j <= max(1, p * 6):
                center(d, 746 + (j % 3) * 150, 408 + (j // 3) * 63, s, 31, TEAL, "m")
        txt(d, 664, 553, "3 × 2 × 1 = 6 seatings", 28, INK, "b")


def forty_pairs(d, p, answer):
    pad(d, "Fold the sum from 1 to 40", "adding tape", PURPLE)
    tops = [1, 2, 3, 4, 5, 19, 20]
    bottoms = [40, 39, 38, 37, 36, 22, 21]
    for j, (a, b) in enumerate(zip(tops, bottoms)):
        x = 97 + j * 164
        if j == 5:
            txt(d, x - 85, 386, "…", 35, INK)
        box(d, x, 249, 108, 75, "#fae2b4", OCHRE, 3)
        center(d, x + 54, 286, a, 33)
        if p > 0.18:
            box(d, x, mix(490, 393, p), 108, 75, "#dce8db", TEAL, 3)
            center(d, x + 54, mix(527, 430, p), b, 33)
    if answer:
        center(d, 640, 554, "20 pairs × 41 in each pair = 820", 37, TEAL, "s")


def subset_pair(d, p, answer):
    pad(d, "Make a partner by toggling A", "collection drawer", PURPLE)
    for row, pieces in enumerate(("BD", "ABD")):
        y = 227 + row * 166
        box(d, 85, y, 563, 123, "#f4d8b5", OCHRE, 5)
        for j, n in enumerate("ABCDE"):
            x = 142 + j * 100
            dot(d, x, y + 62, 33, PURPLE if n in pieces else "#dbcbb5")
            center(d, x, y + 62, n, 27, WHITE if n in pieces else INK)
    notes(
        d,
        732,
        251,
        [
            ("A changes sides.", 37, INK),
            ("The other four choices stay fixed.", 25, PURPLE),
            ("Each pair has one odd-sized subset.", 24, INK),
        ],
    )
    if answer:
        txt(d, 732, 524, "32 subsets ÷ 2 = 16 odd subsets", 24, TEAL, "b")


def bead_difference(d, p, answer):
    pad(d, "Measure the extra two bead parts", "bead counter", TEAL)
    for row, n in enumerate([5, 3]):
        y = 278 + row * 145
        line(d, 93, y, 96 + 5 * 112, y, "#a59a82", 4)
        for j in range(n):
            x = 153 + j * 110
            dot(d, x, y, 37, RED if row == 0 else BLUE, INK)
            dot(d, x - 10, y - 13, 6, "#f5dbc6")
    line(d, 448, 357, 647, 357, RED, 4)
    center(d, 550, 338, "16 beads", 23, RED)
    notes(
        d,
        759,
        232,
        [
            ("5 red parts", 34, RED),
            ("3 blue parts", 31, BLUE),
            ("Find the size of one part.", 26, INK),
        ],
    )
    if answer:
        txt(d, 758, 502, "8 parts × 8 beads = 64", 28, TEAL, "b")


def painted_fence(d, p, answer):
    pad(d, "Combine two painters’ rates", "fence workshop", TEAL)
    for j in range(12):
        x = 74 + j * 88
        y = 257
        fill = (
            (BLUE if j < 3 else OCHRE if j == 3 else "#e2d9c3")
            if p > 0.15
            else "#e2d9c3"
        )
        polygon(
            d,
            [
                (x, y + 27),
                (x + 34, y),
                (x + 68, y + 27),
                (x + 68, y + 199),
                (x, y + 199),
            ],
            fill,
            INK,
        )
    center(d, 640, 519, "One hour: 3 blue twelfths + 1 gold twelfth", 29, INK)
    if answer:
        center(
            d,
            640,
            585,
            "Four twelfths per hour complete the whole fence in 3 hours.",
            26,
            TEAL,
        )


def share_scores(d, p, answer):
    pad(d, "Share out four fives and one ten", "score desk", TEAL)
    for j, n in enumerate((5, 5, 5, 5, 10)):
        x = 116 + j * 133
        shown = round(mix(n, 6, p)) if answer else n
        for z in range(shown):
            box(d, x, 482 - z * 22, 77, 17, TEAL if j < 4 else OCHRE, None, 4)
        center(d, x + 38, 533, "Pupil " + str(j + 1), 19)
    notes(
        d, 831, 245, [("Five learners", 36, INK), ("4 × 5 + 10 = 30 points", 26, TEAL)]
    )
    if answer:
        txt(d, 829, 449, "30 ÷ 5 = 6 each", 32, INK, "s")


def odd_groups(d, p, answer):
    pad(d, "Add three odd numbers", "pair-making table", PURPLE)
    for j, n in enumerate((3, 5, 7)):
        x = 116 + j * 381
        for i in range(n // 2):
            box(d, x + i * 79, 250, 68, 125, "#dad4e5", PURPLE, 12)
            for row in range(2):
                dot(d, x + 34 + i * 79, 284 + row * 54, 17, PURPLE)
        finalx = (455 + 65 * j if j < 2 else 741) if answer else x + 24
        finaly = 496 if answer else 431
        dot(d, mix(x + 24, finalx, p), mix(431, finaly, p), 21, GOLD, INK)
    if answer:
        line(d, 428, 536, 540, 536, TEAL, 4)
        center(
            d, 670, 593, "Two leftovers make a pair. One leftover remains.", 28, TEAL
        )
    else:
        center(d, 640, 560, "Each odd group contributes one leftover.", 30, INK)


def cups(d, p, answer):
    pad(d, "Turn two of seven cups", "cup-flipping bench", PURPLE)
    for j in range(7):
        x = 96 + 159 * j
        up = j not in (1, 4) or p < 0.35
        shift = 30 * sin(min(1, p * 1.3) * pi) if j in (1, 4) else 0
        top, bottom = (63, 42) if up else (42, 63)
        cy = 343 - shift
        polygon(
            d,
            [
                (x - top, cy - 59),
                (x + top, cy - 59),
                (x + bottom, cy + 64),
                (x - bottom, cy + 64),
            ],
            MINT if up else GOLD,
            INK,
        )
        line(d, x - top, cy - 59, x + top, cy - 59, INK, 6)
    center(
        d,
        640,
        497,
        "Turning exactly two changes the upright count by −2, 0 or +2.",
        26,
        INK,
    )
    if answer:
        center(
            d,
            640,
            569,
            "Seven starts odd. Zero is even. All seven cannot end upside down.",
            27,
            PURPLE,
        )


def stamps(d, p, answer):
    pad(d, "Find the last gap in the postage", "stamp album", PURPLE)
    rows = [(12, "4 + 4 + 4"), (13, "4 + 4 + 5"), (14, "4 + 5 + 5"), (15, "5 + 5 + 5")]
    for j, (n, total) in enumerate(rows):
        yy = 221 + j * 80
        box(d, 77, yy, 155, 63, "#e5d7e5", PURPLE, 4)
        center(d, 154, yy + 30, str(n) + "¢", 30, PURPLE)
        if p > j * 0.14:
            txt(d, 285, yy + 29, total, 30, INK, "m")
    notes(
        d,
        692,
        235,
        [
            ("Check 11¢.", 34, RED),
            ("After 0, 1 or 2 five-cent stamps,", 24, INK),
            ("the amounts left are 11, 6 and 1.", 24, INK),
        ],
    )
    if answer:
        txt(d, 690, 499, "None is a multiple of 4.", 27, RED, "b")
        txt(d, 690, 563, "Adding 4 carries 12–15 forward.", 25, TEAL)


def triples(d, p, answer):
    pad(d, "Slide a window of three neighbours", "number-line proof", PURPLE)
    for j in range(10):
        x = 98 + j * 119
        if j < 9:
            line(d, x, 359, x + 119, 359, LINE, 3)
        dot(d, x, 359, 31, TEAL if j % 3 == 0 else "#ddd4df", INK)
        center(d, x, 359, j, 26, WHITE if j % 3 == 0 else INK)
    k = min(6, int(p * 7))
    box(d, 65 + k * 119, 423, 300, 24, "#e4c071", None, 4)
    center(
        d,
        640,
        502,
        "Any three consecutive numbers cover one of each remainder modulo 3.",
        25,
        INK,
    )
    if answer:
        center(
            d,
            640,
            571,
            "One factor is divisible by 3, so the product is too.",
            28,
            TEAL,
        )


def odd_thirteens(d, p, answer):
    pad(d, "Mark the multiples of thirteen", "number search", RED)
    line(d, 85, 365, 1190, 365, INK, 4)
    for n in range(50, 101, 5):
        x = 85 + (n - 50) * 22
        line(d, x, 356, x, 378, INK, 3)
        center(d, x, 412, n, 21)
    for j, n in enumerate((52, 65, 78, 91)):
        if j <= p * 4:
            x = 85 + (n - 50) * 22
            dot(d, x, 329, 24, RED if n % 2 else BLUE)
            center(d, x, 329, n, 20, WHITE)
    center(
        d,
        640,
        515,
        "Count by 13 inside the interval. Then apply the odd-number condition.",
        24,
        INK,
    )
    if answer:
        center(d, 640, 581, "65 and 91 survive both checks.", 29, TEAL)


def border(d, p, answer):
    pad(d, "Count a seven-by-seven border twice", "tile inspector", RED)
    for y in range(7):
        for x in range(7):
            xx = 109 + x * 54
            yy = 197 + y * 54
            border = x in (0, 6) or y in (0, 6)
            fill = (BLUE if y in (0, 6) else GOLD) if border else "#e4dfd1"
            d.rectangle(pt(xx, yy, xx + 51, yy + 51), fill=fill, outline=INK, width=2)
    notes(
        d,
        640,
        239,
        [
            ("Outside minus inside", 35, INK),
            ("49 squares − 25 interior squares", 26, BLUE),
            ("Whole rows plus side pieces", 30, INK),
        ],
    )
    if answer:
        txt(d, 640, 473, "7 + 7 + 5 + 5 = 24", 33, TEAL, "b")
        txt(d, 640, 552, "Both methods give 24 border squares.", 24, RED)


def option_test(d, p, answer):
    pad(d, "Which ticket passes both tests?", "divisibility check", RED)
    for j, n in enumerate((45, 60, 75, 90)):
        x = 90 + j * 290
        box(d, x, 244, 231, 173, "#f4ddad", OCHRE, 9)
        center(d, x + 115, 303, n, 45, INK, "s")
        center(d, x + 115, 378, "passes 5", 23, TEAL)
        if p > 0.42 and n != 60:
            line(d, x + 37, 262, x + 194, 342, RED, 5)
    center(
        d, 640, 499, "All four end in 0 or 5. Which one is a multiple of 4?", 28, INK
    )
    if answer:
        center(d, 640, 571, "60 = 4 × 15 = 5 × 12", 32, TEAL)


def pair_grid(d, p, answer):
    pad(d, "Find the pairs with a small enough sum", "pair-sum table", RED)
    for j in range(1, 7):
        x = 124 + (j - 1) * 64
        center(d, x, 203, j, 22, INK)
        for i in range(1, 7):
            y = 251 + (i - 1) * 55
            if j == 1:
                center(d, 62, y, i, 21, INK)
            if i < j:
                yes = i + j <= 5
                color = TEAL if yes and p > 0.32 else "#e1d7bf"
                box(d, x - 24, y - 20, 48, 40, color, None, 4)
                if p > 0.18:
                    center(d, x, y, i + j, 21, WHITE if yes and p > 0.32 else INK)
    notes(
        d,
        634,
        230,
        [
            ("Smaller number = row", 31, INK),
            ("Larger number = column", 27, BLUE),
            ("Keep each sum at most 5.", 27, RED),
        ],
    )
    if answer:
        txt(d, 634, 495, "(1,2), (1,3), (1,4), (2,3)", 27, TEAL, "m")
        txt(d, 634, 562, "Four unordered pairs.", 29, INK, "s")


ART = {
    "T14.1": ("street-map-ten", route_grid),
    "T14.2": ("endpoint-colours", same_colour),
    "T14.3": ("three-court-fixtures", six_schedule),
    "T14.E": ("meeting-planner", six_meetings),
    "T15.1": ("four-tile-turns", shaded_tile),
    "T15.2": ("fixed-table-seat", table_orders),
    "T15.3": ("folded-adding-tape", forty_pairs),
    "T15.E": ("subset-drawer", subset_pair),
    "T16.1": ("bead-difference", bead_difference),
    "T16.2": ("painter-fence", painted_fence),
    "T16.E": ("five-score-stacks", share_scores),
    "T17.1": ("three-odd-piles", odd_groups),
    "T17.2": ("cup-flip-bench", cups),
    "T17.3": ("postage-album", stamps),
    "T17.E": ("three-number-window", triples),
    "T18.1": ("thirteen-search", odd_thirteens),
    "T18.2": ("seven-tile-border", border),
    "T18.3": ("option-tickets", option_test),
    "T18.E": ("triangular-pair-table", pair_grid),
}


def picture(lesson, time_from_prompt, spoken_span, silent_span):
    if silent_span < 0.6:
        raise ValueError("A notebook answer needs a genuine thinking pause.")
    after = max(0, time_from_prompt - spoken_span)
    pause = min(2.4, silent_span * 0.48)
    show_answer = after >= pause
    progress = ease(time_from_prompt, 0, max(1, spoken_span * 0.78))
    if show_answer and lesson in {"T14.1", "T14.3", "T14.E", "T15.2", "T16.E", "T17.1"}:
        progress = ease(after, pause, pause + min(0.8, (silent_span - pause) * 0.4))
    chapter = int(lesson[1:3])
    bg, accent = THEMES[chapter]
    im = Image.new("RGB", (1920, 930), bg)
    d = ImageDraw.Draw(im)
    ART[lesson][1](d, progress, show_answer)
    return im
