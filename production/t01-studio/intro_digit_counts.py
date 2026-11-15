"""Lesson 5. Digit sums and position-by-position counting."""

from intro_art import applications, card, header, mistakes, prompt, stagger, steps
from stage import BLUE, GOLD, MINT, MUTED, RED, RIM, WHITE, blend
from studio_diagrams import fit


SLOT = 5
PLACES = ("Thousands", "Hundreds", "Tens", "Units")
VALUES = ("1,000", "100", "10", "1")


def digit_value(stage, p):
    for n, digit in enumerate("5724"):
        x = 227 + 275 * n
        fit(stage, PLACES[n], x, 214, 37, 239, BLUE, p)
        card(stage, x, 333, digit, GOLD if digit == "4" else WHITE, w=183, h=108, opacity=p, size=70)
        fit(stage, VALUES[n], x, 439, 43, 224, BLUE, p)


def introduction(stage, s):
    header(stage, SLOT, "The idea", "Digit sums and counting digits")
    p = s.reveal("a place-value column")
    digit_value(stage, p)
    fit(stage, "Value changes with position.", 350, 554, 36, 610, BLUE,
        s.reveal("the value of a digit"))
    fit(stage, "Count where a digit appears.", 940, 554, 36, 602, GOLD,
        s.reveal("a position where a digit can appear"))


def exam(stage, s):
    applications(stage, s, SLOT, "Read exactly what the question counts", (
        ("in amc practice", "AMC Upper Primary",
         "Count written digits or test divisibility.", "A digit can contribute in more than one position."),
        ("a mawa style investigation", "MAWA-style investigation",
         "Move the end of the range and predict the change.", "Track units, tens and hundreds separately."),
    ))


def basic_prompt(stage, s):
    header(stage, SLOT, "Basic example", "Is 5,724 divisible by 9?")
    digit_value(stage, s.reveal("five thousand seven hundred"))
    fit(stage, "Why should the sum of the digits help?", 640, 550, 40, 1110, WHITE,
        s.reveal("think about why"))


def basic(stage, s):
    header(stage, SLOT, "Basic example", "Keep the remainder from each place")
    for i, (left, right, cue) in enumerate((
        ("10", "9 + 1", "ten, one hundred"),
        ("100", "99 + 1", "one hundred and one thousand"),
        ("1,000", "999 + 1", "one thousand"),
    )):
        x = 227 + 413 * i
        p = s.reveal(cue)
        card(stage, x, 276, left, BLUE, w=232, h=91, size=57, opacity=p)
        fit(stage, f"= {right}", x, 366, 46, 360, GOLD, s.reveal("one more than") * p)
    total = s.reveal("five plus seven plus two plus four")
    stage.terms((("5 + 7 + 2 + 4", BLUE, total), ("=", WHITE, total),
                 ("18", GOLD, s.reveal("is eighteen"))), 470, 62)
    fit(stage, "18 is divisible by 9, so 5,724 is too.", 640, 570, 44, 1110, MINT,
        s.reveal("so the original number is too"))


def medium_prompt(stage, s):
    header(stage, SLOT, "Medium example", "How many fours do you write?")
    p = s.reveal("from one through sixty-five")
    card(stage, 640, 327, "1, 2, 3, …, 65", BLUE, w=767, h=121, size=67, opacity=p)
    fit(stage, "Count the written 4s.", 640, 499, 44, 1120, GOLD,
        s.reveal("how many times would you write"))


def written_marks(stage, x, y, number, digit, position, opacity, *, w=77, size=38):
    """Colour only the counted occurrence, retaining the other digits for context."""
    digits = str(number)
    edge = GOLD if int(digits.count(digit)) >= 2 else RIM
    stage.box(x - w / 2, y - 33, w, 66, radius=12, edge=edge, opacity=opacity)
    for i, symbol in enumerate(digits):
        px = x + (i - (len(digits) - 1) / 2) * (size * .56)
        active = len(digits) - 1 - i == position
        if active:
            assert symbol == digit
        fit(stage, symbol, px, y, size, size, GOLD if active else WHITE, opacity)


def medium(stage, s):
    header(stage, SLOT, "Medium example", "Count the units and tens separately")
    for index, (marks, title, cue, count_cue, colour) in enumerate((
        (range(4, 65, 10), "Units", "first watch the units column", "give seven marks", BLUE),
        (range(40, 50), "Tens", "in the tens column", "give ten more", MINT),
    )):
        y, x0 = 277 + 145 * index, 219
        fit(stage, title, 114, y, 31, 124, colour, s.reveal(cue))
        for i, value in enumerate(marks):
            written_marks(stage, x0 + i * 91, y, value, "4", index,
                          stagger(s, cue, i, delay=.22), size=35, w=76)
        fit(stage, f"{len(marks)} marks", 1151, y, 28, 145, colour, s.reveal(count_cue))
    fit(stage, "7 + 10 = 17 written fours", 640, 560, 52, 1110, MINT,
        s.reveal("seven plus ten is seventeen"))


def challenge_prompt(stage, s):
    prompt(stage, s, SLOT, "Exam-style challenge", "Count the twos in multiples of 9", (
        ("now write only the multiples", "Write the multiples of 9 from 1 through 250."),
        ("how many times", "How many times does the digit 2 appear?"),
        ("keep the columns separate", "Check units, tens and hundreds separately."),
    ))


def counted_units(stage, s):
    header(stage, SLOT, "Exam-style challenge", "Units column", "9, 18, 27, … cycle through all ten final digits.")
    p = s.reveal("the units cycle repeats")
    for i, digit in enumerate("9876543210"):
        card(stage, 160 + 106 * i, 280, digit, GOLD if digit == "2" else BLUE,
             w=81, h=78, size=49,
             opacity=stagger(s, "the units cycle repeats", i, delay=.064))
    for i, (number, cue) in enumerate(((72, "is seventy-two"), (162, "gives one hundred and sixty-two"),
                                       (252, "the next is two hundred and fifty-two"))):
        x = 357 + i * 283
        show = s.reveal(cue)
        written_marks(stage, x, 453, number, "2", 0, show, w=155, size=43)
        if i:
            stage.arrow((x - 186, 453), (x - 92, 453), BLUE, p * show, 3)
            fit(stage, "+90", x - 139, 406, 27, 105, BLUE, p * show)
        if number == 252:
            fit(stage, "Outside the range", x, 519, 28, 253, RED, s.reveal("outside our range"))
            stage.line(((x - 55, 477), (x + 55, 429)), RED, 3, s.reveal("outside our range"))
    fit(stage, "2 units marks", 640, 578, 43, 1070, MINT, s.reveal("that is two marks"))


def counted_tens(stage, s):
    header(stage, SLOT, "Exam-style challenge", "Tens column", "Choose the units digit that makes the sum a multiple of 9.")
    for i, (prefix, number, clue, cue, result) in enumerate((
        ("2▯", 27, "2 + 7 = 9", "check the twenties", "give twenty-seven"),
        ("12▯", 126, "1 + 2 + 6 = 9", "the one hundred and twenties", "one hundred and twenty-six"),
        ("22▯", 225, "2 + 2 + 5 = 9", "the two hundred and twenties", "two hundred and twenty-five"),
    )):
        x, p = 293 + i * 347, s.reveal(cue)
        card(stage, x, 247, prefix, BLUE, w=226, h=81, opacity=p, size=47)
        show = s.reveal(result)
        stage.arrow((x, 301), (x, 345), GOLD, show, 3)
        written_marks(stage, x, 405, number, "2", 1, show, w=226, size=55)
        fit(stage, clue, x, 487, 38, 297, GOLD, show)
    fit(stage, "3 tens marks", 640, 578, 43, 1070, MINT, s.reveal("three tens marks"))


def counted_hundreds(stage, s):
    header(stage, SLOT, "Exam-style challenge", "Hundreds column", "Start at the first multiple of 9 at or above 200.")
    for i, (number, cue) in enumerate(zip((207, 216, 225, 234, 243), (
        "two hundred and seven", "two hundred and sixteen", "two hundred and twenty-five",
        "two hundred and thirty-four", "two hundred and forty-three"
    ))):
        x = 197 + i * 221
        p = s.reveal(cue)
        written_marks(stage, x, 334, number, "2", 2, p, w=146, size=48)
        if i:
            stage.arrow((x - 140, 334), (x - 80, 334), BLUE, p, 3)
            fit(stage, "+9", x - 111, 289, 26, 75, BLUE, p)
    p = s.reveal("five hundreds marks")
    fit(stage, "5 hundreds marks", 640, 454, 45, 1100, GOLD, p)
    p = s.reveal("two plus three plus five")
    fit(stage, "2 + 3 + 5 = 10 written twos", 640, 559, 54, 1100, MINT, p)


def common_errors(stage, s):
    mistakes(stage, s, SLOT, "Count appearances inside the range", (
        ("contributes once in the tens", "225 contributes once", "225 contributes twice"),
        ("including two hundred and fifty-two", "Count 252", "Stop at 250"),
    ))


def takeaway(stage, s):
    steps(stage, s, SLOT, "Use a tally for each position", (
        ("underline times the digit is written", "Underline what you count", "Distinguish written digits from distinct numbers."),
        ("draw one tally line", "Split the positions", "Give units, tens and hundreds a separate tally."),
        ("write the range endpoints", "Mark the range and filter", "Only tally entries satisfying both."),
        ("check one number", "Check a repeat digit", "Each qualifying occurrence gets its own mark."),
    ))


SCENES = (introduction, exam, basic_prompt, basic, medium_prompt, medium, challenge_prompt,
          counted_units, counted_tens, counted_hundreds, common_errors, takeaway)
