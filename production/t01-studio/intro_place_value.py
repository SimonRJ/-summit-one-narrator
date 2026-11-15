"""Lesson 2. Compensation and area models for exact calculations."""

from functools import lru_cache
from PIL import Image, ImageDraw

from intro_art import applications, card, header, mistakes, prompt, steps
from stage import BLUE, GOLD, MINT, MUTED, RED, RIM, WHITE, blend
from studio_diagrams import fit


SLOT = 2


def introduction(stage, s):
    header(stage, SLOT, "The idea", "Place-value decomposition and estimation")
    p = s.reveal("close to a round number")
    card(stage, 251, 330, "3,986", WHITE, w=258, h=140, opacity=p, size=68)
    part = s.reveal("work with the round part first")
    stage.arrow((409, 330), (502, 330), BLUE, part, 4)
    card(stage, 668, 330, "4,000", BLUE, w=254, h=140, opacity=part, size=68)
    change = s.reveal("account for the difference")
    fit(stage, "−", 838, 330, 66, 85, GOLD, change)
    card(stage, 987, 330, "14", GOLD, w=216, h=140, opacity=change, size=68)
    fit(stage, "Estimate the scale. Keep the exact difference.", 640, 526, 42, 1120, MINT,
        s.reveal("keep an estimate"))


def exam(stage, s):
    applications(stage, s, SLOT, "Estimate and calculate on purpose", (
        ("in amc upper primary practice", "AMC Upper Primary",
         "Estimate to eliminate options far from the right size.", "Look for measurements or awkward numbers close to round ones."),
        ("when a rossmoyne style problem asks", "Rossmoyne-style practice",
         "An exact difference needs every adjustment.", "Use a diagram if pieces of a length or area change."),
    ))


def basic_prompt(stage, s):
    header(stage, SLOT, "Basic example", "From estimate to exact answer")
    p = s.reveal("add three thousand")
    stage.terms((("3,986", BLUE, p), ("+", WHITE, p), ("2,047", GOLD, p)), 331, 86)
    fit(stage, "Estimate to the nearest thousand, then find the exact sum.", 640, 494, 38, 1110, WHITE,
        s.reveal("first think about the total"))


def basic(stage, s):
    header(stage, SLOT, "Basic example", "Balance the adjustments")
    near = s.reveal("the nearby thousands")
    card(stage, 640, 237, "4,000 + 2,000 = 6,000", BLUE, w=741, h=79, opacity=near, size=52)
    for x, y, cue, round_value, delta, original, colour in (
        (374, 389, "fourteen below", "4,000", "−14", "3,986", BLUE),
        (906, 389, "forty-seven above", "2,000", "+47", "2,047", GOLD),
    ):
        p = s.reveal(cue, .8)
        fit(stage, round_value, x - 156, y, 47, 168, colour, p)
        stage.arrow((x - 62, y), (x + 55, y), colour, p, 4)
        fit(stage, delta, x, y - 46, 38, 124, colour, p)
        fit(stage, original, x + 153, y, 47, 167, WHITE, p)
    net = s.reveal("thirty-three above")
    exact = s.reveal("giving six thousand")
    stage.terms((("6,000", BLUE, net), ("+", WHITE, net), ("33", GOLD, net),
                 ("=", WHITE, exact), ("6,033", MINT, exact)), 542, 62)


@lru_cache(maxsize=22)
def seat_grid(scale, columns, rows, x_step, y_step, slant, colour):
    """Render an exact count of small, softly lit seats for repeated frames."""
    image = Image.new("RGBA", (round((columns * x_step + rows * slant + 12) * scale),
                               round((rows * y_step + 12) * scale)))
    draw = ImageDraw.Draw(image)
    shade = (*blend(colour, "#09111b", .50), 255)
    lit = (*blend(colour, WHITE, .23), 255)
    for row in range(rows):
        for col in range(columns):
            x = round((col * x_step + row * slant + 1) * scale)
            y = round((row * y_step + 1) * scale)
            width = round(x_step * .69 * scale)
            height = round(y_step * .69 * scale)
            draw.rounded_rectangle((x, y, x + width, y + height), radius=max(1, round(scale)),
                                   fill=shade)
            draw.line(((x + 1, y), (x + width - 1, y)), fill=lit, width=max(1, round(scale)))
    return image


def seat_block(stage, x, y, cols, rows, colour, *, opacity=1, dx=13.4, dy=7.2, skew=1.1):
    tile = seat_grid(stage.scale, cols, rows, dx, dy, skew, colour)
    stage.paste(tile, stage.px(x), stage.px(y), opacity)


def product_grid(stage, reveal, extra=0):
    seat_block(stage, 267, 204, 28, 49, BLUE, opacity=reveal, dx=23, dy=5.7, skew=1.15)
    seat_block(stage, 267 + 49 * 1.15, 204 + 49 * 5.7 + 14 * (1 - extra),
               28, 1, GOLD, opacity=extra, dx=23, dy=5.7, skew=1.15)
    fit(stage, "49 rows", 137, 339, 32, 145, BLUE, reveal)
    fit(stage, "28 per row", 1054, 340, 31, 177, BLUE, reveal)


def medium_prompt(stage, s):
    header(stage, SLOT, "Medium example", "Find 49 × 28")
    product_grid(stage, s.reveal("imagine forty-nine rows"))
    fit(stage, "What would make this array easier to count?", 640, 537, 39, 1080, WHITE,
        s.reveal("how could we turn"))


def medium(stage, s):
    header(stage, SLOT, "Medium example", "Add a row, then remove it")
    added = s.reveal("add one row", .75)
    removed = s.reveal("take it away")
    product_grid(stage, 1, added * (1 - .82 * removed))
    fit(stage, "50 × 28 = 1,400", 477, 525, 43, 496, BLUE,
        s.reveal("fifty times twenty-eight"))
    fit(stage, "− 28", 756, 525, 44, 137, GOLD, s.reveal("the extra row contains"))
    fit(stage, "= 1,372", 944, 525, 48, 246, MINT, removed)
    fit(stage, "Estimate: 50 × 30 ≈ 1,500", 640, 588, 31, 1050, MUTED,
        s.reveal("an estimate of about"))


def challenge_prompt(stage, s):
    prompt(stage, s, SLOT, "Exam-style challenge", "How many extra seats are free?", (
        ("a theatre has thirty-seven rows", "A theatre has 37 rows of 48 seats."),
        ("adds four seats", "Add 4 seats to each old row, plus 2 new rows of 52 seats."),
        ("after taking two hundred and fifty", "After 250 more bookings, how many added seats are free?"),
    ))


def theatre(stage, old, side, rear):
    x, y, dx, dy, skew = 132, 207, 14.1, 7.85, 1.3
    seat_block(stage, x, y, 48, 37, BLUE, opacity=old, dx=dx, dy=dy, skew=skew)
    seat_block(stage, x + 48 * dx + (1 - side) * 53, y, 4, 37, GOLD, opacity=side,
               dx=dx, dy=dy, skew=skew)
    seat_block(stage, x + 37 * skew, y + 37 * dy + (1 - rear) * 32, 52, 2, MINT, opacity=rear,
               dx=dx, dy=dy, skew=skew)
    fit(stage, "37 rows × 48 seats", 513, 178, 28, 648, BLUE, old)
    stage.line(((906, 353), (968, 353)), GOLD, 3, side)
    fit(stage, "37 × 4", 1063, 328, 38, 170, GOLD, side)
    stage.line(((897, 513), (968, 513)), MINT, 3, rear)
    fit(stage, "2 × 52", 1063, 485, 38, 170, MINT, rear)


def theatre_strips(stage, s):
    header(stage, SLOT, "Exam-style challenge", "Build only the added seats")
    side = s.reveal("attach four seats", .95)
    rear = s.reveal("now attach the two new rows", .95)
    theatre(stage, s.reveal("the old seating block"), side, rear)
    fit(stage, "= 148", 1063, 378, 40, 170, GOLD, s.reveal("one hundred and forty-eight"))
    fit(stage, "= 104", 1063, 537, 40, 170, MINT, s.reveal("one hundred and four"))
    p = s.reveal("including the corner")
    stage.box(848, 493, 62, 23, radius=5, fill=None, edge=WHITE, opacity=p)
    fit(stage, "Corner is part of the new rows", 640, 585, 36, 1110, WHITE, p)


def free_seats(stage, s):
    header(stage, SLOT, "Exam-style challenge", "Count the added seats")
    p = s.reveal("one hundred and forty-eight")
    added = s.reveal("two hundred and fifty-two")
    stage.terms((("148", GOLD, p), ("+", WHITE, p), ("104", MINT, p),
                 ("=", WHITE, added), ("252 added", WHITE, added)), 264, 56)
    removal = s.reveal("remove two hundred and fifty")
    answer = s.reveal("two seats are free")
    stage.terms((("252", BLUE, removal), ("−", WHITE, removal), ("250", RED, removal),
                 ("=", WHITE, answer), ("2 free", MINT, answer)), 415, 72)
    fit(stage, "Check: 39 × 52 − 37 × 48 = 252", 640, 555, 41, 1100, MUTED,
        s.reveal("subtracting the old total"))


def common_errors(stage, s):
    mistakes(stage, s, SLOT, "Count each change once", (
        ("extend all thirty-nine rows", "39 × 4 + 2 × 52", "37 × 4 + 2 × 52"),
        ("adding an adjustment", "1,400 + 28", "1,400 − 28"),
    ))


def takeaway(stage, s):
    steps(stage, s, SLOT, "Make the exact work easier", (
        ("estimate first", "Estimate first", "Get a sensible scale for the answer."),
        ("split the calculation", "Choose tidy parts", "Label each adjustment with its sign."),
        ("sketch the old block", "Separate regions", "Shade each added part once."),
        ("read the question again", "Answer the question asked", "Use an estimate or an exact amount as requested."),
    ))


SCENES = (introduction, exam, basic_prompt, basic, medium_prompt, medium, challenge_prompt,
          theatre_strips, free_seats, common_errors, takeaway)
