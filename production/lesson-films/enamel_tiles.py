"""Invoices split into colour-coded enamel tiles and a fixed eight-place tray."""
from itertools import product

BACKGROUND = ("#343d3c", "#232e30")
PAPER, INK, BLUE, GOLD, LINE = "#f3eed9", "#253536", "#9ad4de", "#f2c782", "#82908d"
BRIDGE = "Compare the two repair slips. Which tiles can you lift from both? When the bench changes to an eight-space tray, explain why the gold count must be eight minus the blue count."
HEADINGS = (
    "Two tiles for a mosaic", "Read two repair slips", "Lift off the matching tiles",
    "Price the remaining group", "A tray with a fixed length", "Give each term its units",
    "Start with eight gold tiles", "Try naming the other count",
)


def check_maths():
    prices = [(b, g) for b, g in product(range(80), repeat=2)
              if 4*b + 3*g == 58 and 7*b + 3*g == 79]
    assert prices == [(7, 10)]
    assert [(b, 8-b) for b in range(9) if 7*b + 10*(8-b) == 65] == [(5, 3)]
    assert 80 - 5*3 == 65 == 56 + 3*3


def label(board, value, x, y, size, colour=PAPER, opacity=1):
    board.text(str(value), x, y, size, colour, bold=True, opacity=opacity)


def tile(board, x, y, size, kind):
    half = size / 2
    colour = {"blue": BLUE, "gold": GOLD, "space": "#455454"}[kind]
    board.box(x-half, y-half, size, size, fill=colour, edge=LINE, stroke=2, radius=4)
    if kind == "blue":
        board.dot(x, y, size * .20, INK)
    elif kind == "gold":
        r = size * .23
        board.polygon([(x, y-r), (x+r, y), (x, y+r), (x-r, y)], INK)


def tile_row(board, x, y, size, kinds):
    for index, kind in enumerate(kinds):
        tile(board, x + index*(size+8), y, size, kind)


def invoice(board, x, label_text, blue_count, gold_count, price):
    board.box(x, 170, 508, 301, fill="#324142", edge=LINE, stroke=3, radius=10)
    label(board, label_text, x+254, 206, 32)
    tile_row(board, x+54, 270, 46, ["blue"] * blue_count)
    tile_row(board, x+54, 337, 46, ["gold"] * gold_count)
    label(board, f"Total  ${price}", x+254, 419, 38, PAPER)


def tray(board, y, kinds):
    board.box(208, y-48, 863, 96, fill="#253334", edge=LINE, stroke=3, radius=12)
    tile_row(board, 283, y, 90, kinds)


def draw(board, scene, cue):
    board.label(HEADINGS[scene-1], 64, 70, 42, PAPER, bold=True)
    board.line([(64,124),(1216,124)], LINE, 3)
    if scene == 1:
        tile(board, 371, 294, 143, "blue")
        tile(board, 897, 294, 143, "gold")
        label(board, "One blue tile", 371, 437, 38, BLUE)
        label(board, "One gold tile", 897, 437, 38, GOLD)
        label(board, "Which price does the letter mean?", 640, 554, 35, PAPER, cue.reveal("a letter stands for a price"))
    elif scene == 2:
        invoice(board, 98, "Delivery one", 4, 3, 58)
        invoice(board, 674, "Delivery two", 7, 3, 79)
        label(board, "What stayed the same?", 640, 549, 39, GOLD, cue.reveal("side by side"))
    elif scene == 3:
        label(board, "Extra tiles on the second slip", 640, 218, 36)
        tile_row(board, 501, 337, 119, ["blue"]*3)
        label(board, "$79 − $58 = $21", 640, 457, 42, BLUE, cue.reveal("twenty one dollars higher"))
        label(board, "One blue tile costs $7.", 640, 554, 37, PAPER, cue.reveal("one blue tile costs"))
    elif scene == 4:
        tile_row(board, 173, 286, 65, ["blue"] * 4)
        tile_row(board, 767, 286, 65, ["gold"] * 3)
        label(board, "4 × $7 = $28", 284, 393, 36, BLUE)
        label(board, "$58 − $28 = $30", 850, 393, 36, GOLD, cue.reveal("Subtract twenty eight"))
        label(board, "One gold tile costs $10.", 640, 525, 40, GOLD, cue.reveal("one gold tile costs"))
    elif scene == 5:
        tray(board, 310, ["space"]*8)
        label(board, "8 tiles together are worth $65.", 640, 205, 37)
        label(board, "x = number of blue tiles", 640, 468, 38, BLUE, cue.reveal("number of blue tiles"))
        label(board, "How many are gold?", 640, 553, 32, GOLD, cue.reveal("number of gold tiles"))
    elif scene == 6:
        label(board, "Blue count: x", 334, 243, 40, BLUE)
        label(board, "Gold count: 8 − x", 918, 243, 40, GOLD, cue.reveal("eight minus x"))
        label(board, "Blue dollars: 7x", 334, 367, 37, BLUE, cue.reveal("dollars for the blue"))
        label(board, "Gold dollars: 10(8 − x)", 918, 367, 37, GOLD, cue.reveal("dollars for the gold"))
        label(board, "7x + 10(8 − x) = 65", 640, 523, 46, PAPER, cue.reveal("Their sum"))
    elif scene == 7:
        blue = 5 if cue.reveal("make five exchanges") > .1 else 0
        tray(board, 304, ["blue"]*blue + ["gold"]*(8-blue))
        label(board, "$80 − $65 = $15", 640, 424, 39, GOLD, cue.reveal("lose fifteen dollars"))
        label(board, "5 exchanges lower the bill by $15.", 640, 534, 35, BLUE, cue.reveal("make five exchanges"))
    else:
        gold = 3 if cue.reveal("takes three changes") > .1 else 0
        tray(board, 304, ["blue"]*(8-gold) + ["gold"]*gold)
        label(board, "y = number of gold tiles", 640, 207, 37, GOLD)
        label(board, "$56 + 3 × $3 = $65", 640, 453, 41, BLUE, cue.reveal("takes three changes"))
        label(board, "x = 5 blue tiles     y = 3 gold tiles", 640, 552, 35, PAPER, cue.reveal("same tray"))


def poster(draw_frame):
    return draw_frame(8, 1)
