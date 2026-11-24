"""Two peg rails show the phase, period and parity of the dome projectors."""
from math import lcm

BACKGROUND = ("#29364c", "#172437")
PAPER = "#f3f0de"
GOLD = "#f1ca79"
BLUE = "#a6d9f1"
MUTED = "#728197"
RAIL = "#44566b"
BRIDGE = "Start at the gold peg at minute 3. Inside the audience’s viewing window, which pegs also sit one minute past a multiple of 6? What changes when the blue starting peg moves?"
HEADINGS = (
    "The projector test", "Mark just the gold minutes", "Lay the blue strip underneath",
    "A viewing window opens", "Test the second remainder", "Why the pattern repeats",
    "The technician moves a pin", "The impossible new meeting",
)


def check_maths():
    gold = set(range(3, 500, 8))
    blue = set(range(1, 500, 6))
    assert sorted((gold & blue) & set(range(71))) == [19, 43, 67]
    assert sorted(gold & set(range(30, 71))) == [35, 43, 51, 59, 67]
    assert [value % 6 for value in [35, 43, 51, 59, 67]] == [5, 1, 3, 5, 1]
    assert lcm(8, 6) == 24 and not gold.intersection(range(2, 500, 6))


def label(board, value, x, y, size, colour=PAPER, opacity=1):
    board.text(str(value), x, y, size, colour, bold=True, opacity=opacity)


def peg_rail(board, y, start, finish, values, colour, *, common=()):
    """Draw every physical minute tick. Each raised peg also carries its minute."""
    left, right = 122, 1160
    board.line([(left, y), (right, y)], RAIL, 9)
    for minute in range(start, finish + 1):
        x = left + (minute - start) * (right - left) / (finish - start)
        board.line([(x, y), (x, y + (15 if minute % 5 == 0 else 8))], MUTED, 2)
        if minute in values:
            board.line([(x, y - 22), (x, y)], colour, 4)
            board.dot(x, y - 25, 9, colour)
            if minute in common:
                board.box(x - 18, y - 42, 36, 34, edge=PAPER, stroke=3, radius=12)
            label(board, minute, x, y + 39, 28, colour)


def dome(board, x, tint, phase, period):
    board.box(x - 174, 192, 348, 251, fill="#243447", edge=MUTED, radius=30, stroke=3)
    board.line([(x - 85, 338), (x, 240), (x + 82, 338)], tint, 3)
    board.dot(x, 240, 10, tint)
    board.box(x - 46, 327, 92, 27, fill=tint, radius=6)
    label(board, f"First minute {phase}", x, 382, 31, tint)
    label(board, f"Then every {period} min", x, 419, 25)


def draw(board, scene, cue):
    board.label(HEADINGS[scene - 1], 64, 70, 42, PAPER, bold=True)
    board.line([(64, 124), (1216, 124)], RAIL, 3)
    if scene == 1:
        dome(board, 393, GOLD, 3, 8)
        dome(board, 888, BLUE, 1, 6)
        label(board, "Can the two stars appear together?", 640, 541, 38, PAPER, cue.reveal("Could both stars"))
    elif scene in (2, 3):
        peg_rail(board, 252, 0, 44, range(3, 44, 8), GOLD, common=(19,) if scene == 3 else ())
        if scene == 2:
            label(board, "Gold starts at 3", 640, 392, 39, GOLD)
            label(board, "Add 8 for each new peg.", 640, 509, 36, PAPER, cue.reveal("Count on eight"))
        else:
            peg_rail(board, 416, 0, 44, range(1, 20, 6), BLUE, common=(19,))
            label(board, "First matching minute: 19", 640, 546, 35, PAPER, cue.reveal("first matching pair"))
    elif scene in (4, 5):
        values = (35, 43, 51, 59, 67)
        label(board, "Viewing window: minute 30 through minute 70", 640, 190, 35)
        peg_rail(board, 306, 30, 70, values, GOLD)
        if scene == 4:
            label(board, "Which gold pegs also work for blue?", 640, 516, 35, BLUE, cue.reveal("testing against blue"))
        else:
            for value in values:
                x = 122 + (value - 30) * 1038 / 40
                colour = BLUE if value % 6 == 1 else MUTED
                label(board, f"r {value % 6}", x, 414, 34, colour, cue.reveal("on division by six"))
            label(board, "Remainder 1 at minutes 43 and 67", 640, 537, 38, BLUE, cue.reveal("two viewing times"))
    elif scene == 6:
        label(board, "Minutes elapsed after a meeting", 640, 181, 33)
        peg_rail(board, 281, 0, 24, range(0, 25, 8), GOLD, common=(24,))
        peg_rail(board, 417, 0, 24, range(0, 25, 6), BLUE, common=(24,))
        label(board, "3 × 8 = 4 × 6 = 24 minutes", 640, 548, 38, PAPER, cue.reveal("three times"))
    else:
        label(board, "The blue start has moved to minute 2.", 640, 182, 34, BLUE)
        peg_rail(board, 280, 0, 28, range(3, 29, 8), GOLD)
        peg_rail(board, 415, 0, 28, range(2, 29, 6), BLUE)
        if scene == 7:
            label(board, "Will these pegs ever line up?", 640, 544, 38, PAPER, cue.reveal("line up now"))
        else:
            label(board, "Gold stays odd. Blue stays even.", 640, 544, 38, PAPER, cue.reveal("both even and odd"))


def poster(draw_frame):
    return draw_frame(9, 1)
