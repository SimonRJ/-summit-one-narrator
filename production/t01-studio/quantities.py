"""Visual proofs and worked examples for T01.1."""

import math

from stage import BG, BLUE, GOLD, MINT, MUTED, PANEL, RED, RIM, WHITE
from stage import between, blend, mix


PACKETS = (238, 446, 654, 862)
LOOSE = (1057, 1121)
GRID = (542, 640, 738)
COLORS = (MINT, GOLD, BLUE)


def overview(stage, s):
    stage.heading("Give every quantity a job")
    labels = ("packets", "counters per packet", "loose counters")
    cues = ("one might count packets", "another might tell you", "the third might count")
    for i, (number, label, color, cue) in enumerate(zip((4, 3, 2), labels, COLORS, cues)):
        x = 292 + 348 * i
        stage.box(x - 140, 216, 280, 218, edge=RIM, radius=26)
        stage.text(str(number), x, 286, 82, WHITE, bold=True)
        reveal = s.reveal(cue)
        stage.line([(x - 90, 350), (x + 90, 350)], color, 3, reveal)
        stage.text(label, x, 391 + 12 * (1 - reveal), 26, color, bold=True, opacity=reveal)
    stage.text("What does each number count?", 640, 515, 35, MINT, opacity=s.reveal("give every number"))


def units(stage, s):
    stage.heading("Read the final question", "How many counters altogether?")
    p = s.reveal("four plus three plus two")
    stage.terms([("4", MINT, p), ("+", WHITE, p), ("3", GOLD, p), ("+", WHITE, p),
                 ("2", BLUE, p), ("=", WHITE, p), ("9", WHITE, p)], 273, 65)
    mismatched = s.reveal("we would be adding")
    stage.line([(463, 315), (817, 315)], RED, 3, mismatched)
    for x, label, color in zip((373, 640, 907), ("packets", "counters per packet", "loose counters"), COLORS):
        stage.box(x - 123, 372, 246, 71, radius=17, edge=color, fill=PANEL, opacity=mismatched)
        stage.text(label, x, 408, 24, color, bold=True, opacity=mismatched)
    stage.text("Convert to a count of counters", 640, 531, 38, WHITE, bold=True,
               opacity=s.reveal("get everything into counters", offset=-0.28))


def packet(stage, x, y, opacity=1.0, lift=0.0):
    if opacity <= 0:
        return
    stage.box(x - 88, y - 42, 176, 95, radius=20, fill="#101820", opacity=opacity)
    stage.box(x - 88, y - 48, 176, 92, radius=20, fill="#283746", edge="#536478", opacity=opacity)
    stage.box(x - 76, y - 28, 152, 56, radius=13, fill="#192530", edge="#3f5265", opacity=opacity)
    stage.box(x - 88, y - 50 - lift, 176, 14, radius=7, fill="#516477", opacity=opacity)


def puzzle(stage, s):
    stage.heading("Mia’s counters")
    group_start = s.at("four packets of counters")
    count = s.reveal("each packet contains three counters")
    for i, x in enumerate(PACKETS):
        opacity = between(s.t, group_start + 0.24 * i)
        y = 317 + 16 * (1 - opacity)
        packet(stage, x, y, opacity)
        for dx in (-47, 0, 47):
            stage.coin(x + dx, y, width=41, opacity=opacity * count)
    blue = s.reveal("two loose counters")
    for x in LOOSE:
        stage.coin(x + 42 * (1 - blue), 317, "blue", 49, blue)
    stage.bracket(145, 955, 425, "4 packets · 3 counters in each", GOLD, count)
    stage.bracket(1026, 1153, 425, "2 loose", BLUE, blue)
    stage.text("How many counters altogether?", 640, 532, 43, WHITE, bold=True,
               opacity=s.reveal("how many counters does"))


def unpack(stage, s):
    stage.heading("Open the packets", "Count the same-sized groups")
    first = s.at("open the first packet")
    others = s.at("open the others")
    for i, x in enumerate(PACKETS):
        start = first if not i else others + 0.58 * (i - 1)
        u = between(s.t, start, 1.0)
        packet(stage, x, 317, 1 - u, 25 * u)
        for k in range(3):
            tx, ty = GRID[k], 243 + 67 * i
            stage.coin(mix(x + (k - 1) * 47, tx, u),
                       mix(317, ty, u) - 17 * math.sin(math.pi * u),
                       width=round(mix(41, 50, u)))
    for x in LOOSE:
        stage.coin(x, 317, "blue", 49)
    p = s.reveal("four groups of three")
    q = s.reveal("give twelve counters", offset=0.28)
    stage.terms([("4 packets", MINT, p), ("×", WHITE, p), ("3 per packet", GOLD, p),
                 ("=", WHITE, q), ("12 counters", GOLD, q)], 551, 39)


def total(stage, s):
    stage.heading("Add quantities with a common unit")
    result = s.reveal("fourteen counters", offset=0.22)
    move = s.reveal("slide them into the collection", 1.1)
    stage.box(491, 198, 429, 279, radius=25, fill=None, edge=MINT, opacity=result)
    for row in range(4):
        for x in GRID:
            stage.coin(x, 243 + 67 * row, width=50)
    for i, x in enumerate(LOOSE):
        stage.coin(mix(x, 814 + 64 * i, move), mix(317, 444, move) - 29 * math.sin(math.pi * move),
                   "blue", 49)
    p = s.reveal("adding twelve counters and two counters")
    stage.terms([("12 counters", GOLD, p), ("+", WHITE, p), ("2 counters", BLUE, p),
                 ("=", WHITE, result), ("14 counters", MINT, result)], 551, 43)


def ribbon(stage, x, y, width, colour, opacity):
    stage.box(x, y, width, 33, radius=8, fill=blend(BG, colour, 0.72), edge=colour, opacity=opacity)
    stage.line([(x + 7, y + 6), (x + width - 7, y + 6)], colour, 2, opacity * 0.75)


def measurements(stage, s):
    stage.heading("Measure in a common unit")
    first = s.reveal("one ribbon is two metres long")
    second = s.reveal("another is thirty centimetres long")
    question = s.reveal("how much ribbon")
    convert = s.reveal("two metres is two hundred centimetres", offset=0.9)
    combine = s.reveal("together they measure", 1.05)
    ribbon(stage, 286, 264, 600, GOLD, first)
    ribbon(stage, mix(286, 886, combine), mix(382, 264, combine), 90, BLUE, second)
    stage.text("2 m", 586, 225, 39, GOLD, bold=True, opacity=first * (1 - convert))
    stage.text("200 cm", 586, 225, 39, GOLD, bold=True, opacity=convert)
    stage.text("30 cm", mix(341, 931, combine), mix(350, 225, combine), 35, BLUE, bold=True, opacity=second)
    stage.line([(286, 314), (886 + 90 * combine, 314)], RIM, 2, first)
    for x in (286, 886, 886 + 90 * combine):
        stage.line([(x, 306), (x, 324)], MINT, 2, first)
    stage.text("How much ribbon altogether?", 640, 516, 40, WHITE, bold=True, opacity=question * (1 - combine))
    stage.terms([("200 cm", GOLD, combine), ("+", WHITE, combine), ("30 cm", BLUE, combine),
                 ("=", WHITE, combine), ("230 cm", MINT, combine)], 520, 48)


def pages(stage, opacity_at, highlight_at=None, nines_at=None):
    for index, page in enumerate(range(95, 106)):
        x = 190 + 90 * index
        opacity = opacity_at(index)
        highlight = (highlight_at(index) if highlight_at and index < 5 else 0) * opacity
        stage.box(x - 38, 254, 76, 81, radius=14, fill=PANEL,
                  edge=blend(RIM, GOLD, highlight), opacity=opacity)
        digits = str(page)
        for d, digit in enumerate(digits):
            color = WHITE
            if digit == "9" and nines_at:
                color = blend(WHITE, GOLD, nines_at(index, d))
            stage.text(digit, x + (d - (len(digits) - 1) / 2) * 22, 296, 32,
                       color, bold=True, opacity=opacity)


def page_puzzle(stage, s):
    stage.heading("Count the printed nines")
    start = s.at("pages numbered ninety-five")
    pages(stage, lambda index: between(s.t, start + 0.15 * index))
    stage.text("Pages 95 to 105", 640, 200, 29, MUTED, opacity=between(s.t, start))
    stage.text("How many times is the digit 9 written?", 640, 482, 41, WHITE, bold=True,
               opacity=s.reveal("how many times is the digit nine written"))


def occurrences(stage, s):
    stage.heading("One job for a page, one job for a digit")
    start = s.at("five page numbers contain a nine")
    move = s.at("its first nine counts once")
    last = s.at("its second nine counts once")
    pages(stage, lambda _: 1.0,
          lambda i: between(s.t, start + 0.21 * i),
          lambda i, d: between(s.t, start + 0.21 * i) if d == 0 else between(s.t, last))
    p = between(s.t, start, 0.7)
    stage.bracket(151, 589, 360, "5 pages containing a 9", GOLD, p)
    for i, (page, digit) in enumerate([(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (4, 1)]):
        start_x = 190 + 90 * page + (digit - 0.5) * 22
        u = between(s.t, move + 0.16 * i if i < 5 else last, 0.72)
        finish_x = 420 + 88 * i
        stage.text("9", mix(start_x, finish_x, u), mix(297, 474, u) - 27 * math.sin(math.pi * u),
                   43, GOLD, bold=True, opacity=u)
    stage.text("6 written nines", 640, 554, 42, MINT, bold=True,
               opacity=s.reveal("there are six written nines"))


def recap(stage, s):
    challenge = s.reveal("here is your notebook challenge")
    stage.heading("Keep the quantities labelled", opacity=1 - challenge)
    for i, (instruction, cue) in enumerate((
        ("Read the question", "read the final question"),
        ("Label each quantity", "label each number"),
        ("Use a common unit", "bring quantities"),
    )):
        x = 299 + 341 * i
        p = s.reveal(cue) * (1 - challenge)
        stage.box(x - 153, 249, 306, 114, radius=21, edge=RIM, opacity=p)
        stage.text(instruction, x, 307, 26, COLORS[i], bold=True, opacity=p)

    stage.heading("Your turn", opacity=challenge)
    boxes = s.reveal("six boxes hold eight pencils each") * challenge
    for i in range(6):
        x = 305 + 134 * i
        stage.box(x - 49, 230, 98, 99, radius=18, edge=GOLD, opacity=boxes)
        stage.text("8", x, 270, 41, GOLD, bold=True, opacity=boxes)
        stage.text("pencils", x, 306, 18, MUTED, opacity=boxes)
    broken = s.reveal("five pencils are broken")
    stage.text("5 pencils are broken.", 640, 398, 33, BLUE, opacity=broken)
    stage.text("How many unbroken pencils are there?", 640, 485, 42, WHITE, bold=True,
               opacity=s.reveal("how many unbroken pencils"))
    stage.text("Label the quantities and show your calculation.", 640, 543, 26, MINT,
               opacity=s.reveal("label the quantities and show"))


SCENES = (overview, units, puzzle, unpack, total, measurements, page_puzzle, occurrences, recap)
