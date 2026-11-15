"""Lesson 4. Position and casework with fixed digit cards."""

from intro_art import applications, card, header, mistakes, prompt, stagger, steps
from stage import BLUE, GOLD, MINT, MUTED, RED, RIM, WHITE, blend, mix
from studio_diagrams import fit


SLOT = 4
ENDINGS = (("20", "40", "60"), ("12",), ("04", "24", "64"), ("16",))


def three_slots(stage, values, y, *, x=435, colour=BLUE, opacity=1, labels=True):
    for index, value in enumerate(values):
        left = x + 205 * index
        card(stage, left, y, value, colour, w=158, h=112, size=74, opacity=opacity)
        if labels:
            fit(stage, ("Hundreds", "Tens", "Units")[index], left, y + 91, 30, 167, MUTED, opacity)


def introduction(stage, s):
    header(stage, SLOT, "The idea", "Digits, zero and positional constraints")
    p = s.reveal("moving just one card")
    q = s.reveal("whether it passes a rule", duration=1)
    for i, x in enumerate((435, 640, 845)):
        stage.box(x - 89, 260, 178, 162, radius=20, fill=None, edge=RIM, opacity=p)
        fit(stage, ("Hundreds", "Tens", "Units")[i], x, 456, 29, 169, MUTED, p)
    card(stage, 435, 341, "4", BLUE, w=142, h=108, size=77, opacity=p)
    card(stage, mix(640, 845, q), 341 - 39 * (4 * q * (1 - q)), "0", GOLD,
         w=142, h=108, size=77, opacity=p)
    card(stage, mix(845, 640, q), 341 + 39 * (4 * q * (1 - q)), "7", BLUE,
         w=142, h=108, size=77, opacity=p)
    fit(stage, "407 is odd.  470 is even.", 640, 563, 46, 1110, MINT,
        s.reveal("the places as separate slots"))


def exam(stage, s):
    applications(stage, s, SLOT, "Let the places organise your search", (
        ("look for clues about the first digit", "AMC Upper Primary",
         "Look for leading digits, endings and repeat rules.", "Begin with the place that has the fewest choices."),
        ("in a rossmoyne style counting puzzle", "Rossmoyne-style practice",
         "Explain why the cases cover every possibility.", "Keep the cases separate so each number is counted once."),
    ))


def basic_prompt(stage, s):
    header(stage, SLOT, "Basic example", "Make the smallest three-digit number")
    for n, digit in enumerate("047"):
        card(stage, 435 + n * 205, 349, digit, GOLD if digit == "0" else BLUE, w=142, h=111,
             size=80, opacity=stagger(s, "use the digit cards", n))
    fit(stage, "Use each card exactly once.", 640, 514, 43, 1100, WHITE, s.reveal("once each"))


def basic(stage, s):
    header(stage, SLOT, "Basic example", "Put the smallest legal digit first")
    for n, (digit, cue) in enumerate(zip("407", ("four is our smallest choice", "put zero in the tens", "seven in the units"))):
        x = 435 + n * 205
        stage.box(x - 89, 257, 178, 147, radius=19, fill=None,
                  edge=GOLD if n == 0 else RIM, opacity=s.reveal("the hundreds place"))
        card(stage, x, 330, digit, GOLD if digit == "0" else BLUE, w=143, h=110, size=79,
             opacity=s.reveal(cue))
        fit(stage, ("Hundreds", "Tens", "Units")[n], x, 444, 30, 175, MUTED,
            s.reveal("the hundreds place"))
    fit(stage, "407", 410, 551, 59, 320, MINT, s.reveal("the number is four hundred and seven"))
    fit(stage, "047 represents 47", 813, 551, 41, 548, RED, s.reveal("putting zero first"))


def medium_prompt(stage, s):
    header(stage, SLOT, "Medium example", "Count the three-digit even numbers")
    three_slots(stage, "025", 306, labels=False, opacity=s.reveal("use zero, two and five"))
    start = s.reveal("the units place")
    fit(stage, "Use each card once.", 403, 483, 40, 560, WHITE, start)
    fit(stage, "Units digit: 0 or 2", 862, 483, 43, 568, GOLD, start)


def medium(stage, s):
    header(stage, SLOT, "Medium example", "Split by the last card")
    for n, (ending, result, cue, colour) in enumerate((
        ("0", ("250", "520"), "a final zero", BLUE),
        ("2", ("502",), "a final two", GOLD),
    )):
        y = 274 + 160 * n
        p = s.reveal(cue)
        v = s.reveal("making two hundred and fifty" if n == 0 else "giving five hundred and two")
        card(stage, 283, y, f"Ends in {ending}", colour, w=284, h=91, size=37, opacity=p)
        for j, value in enumerate(result):
            card(stage, 666 + 261 * j, y, value, MINT, w=186, h=88, opacity=v, size=58)
        if n == 1:
            card(stage, 927, y, "052", RED, w=186, h=88, opacity=p * (1 - .45 * v), size=58)
            stage.line(((870, y + 28), (985, y - 28)), RED, 4, v)
    fit(stage, "2 + 1 = 3 numbers", 640, 566, 51, 1100, MINT, s.reveal("three numbers altogether"))


def challenge_prompt(stage, s):
    prompt(stage, s, SLOT, "Exam-style challenge", "Count numbers that pass both rules", (
        ("make a five-digit number", "Use 0, 1, 2, 4 and 6 exactly once each."),
        ("the number must exceed", "The number must be greater than 40,000."),
        ("be divisible by four", "It must also be divisible by 4."),
        ("how many numbers work", "How many five-digit numbers work?"),
    ))


def possible_endings(stage, s):
    header(stage, SLOT, "Exam-style challenge", "List the possible final pairs")
    p = s.reveal("the first digit is four or six")
    fit(stage, "First digit: 4 or 6", 323, 194, 36, 506, BLUE, p)
    fit(stage, "Final pair: multiple of 4", 902, 194, 36, 623, GOLD,
        s.reveal("depends on the final pair"))
    for i, (last, pairs, cue) in enumerate(zip(
        "0246", ENDINGS, ("ending in zero", "ending in two", "ending in four", "ending in six")
    )):
        x, y = (176 + i * 271, 344)
        p = s.reveal(cue)
        stage.box(x - 103, y - 81, 249, 241, radius=24, fill="#1a2735", edge=RIM, opacity=p)
        fit(stage, f"Last digit {last}", x + 19, y - 39, 30, 229, GOLD, p)
        for j, pair in enumerate(pairs):
            fit(stage, pair, x + 19, y + 19 + j * 51, 47, 199, WHITE, p)


def filter_front(stage, s):
    header(stage, SLOT, "Exam-style challenge", "Each card can be used only once")
    endings = tuple(pair for group in ENDINGS for pair in group)
    for index, (first, cue, colour) in enumerate((
        ("4", "with four first", BLUE), ("6", "with six first", GOLD),
    )):
        y = 280 + 143 * index
        p = s.reveal(cue)
        fade = s.reveal("cross out endings containing four" if index == 0 else
                        "cross out endings containing six")
        card(stage, 145, y, f"{first} first", colour, w=158, h=77, size=36, opacity=p)
        for i, pair in enumerate(endings):
            x = 302 + 106 * i
            bad = first in pair
            card(stage, x, y, pair, blend(WHITE, RED, fade) if bad else blend(WHITE, MINT, fade),
                 w=88, h=73, size=42, opacity=p * (1 - .70 * fade if bad else 1))
            if bad:
                stage.line(((x - 26, y + 19), (x + 26, y - 19)), RED, 3, fade)
        fit(stage, f"{4 if index == 0 else 5} endings", 1147, y + 65, 26, 163, colour, fade)
    fit(stage, "Each valid ending leaves two ways to order the middle.", 640, 572, 38, 1100, MINT,
        s.reveal("they can go in either order"))


def count_numbers(stage, s):
    header(stage, SLOT, "Exam-style challenge", "Count the two cases")
    a = s.reveal("four times two")
    b = s.reveal("five times two")
    result = s.reveal("add them for eighteen")
    for x, eq, colour, p in ((389, "4 × 2 = 8", BLUE, a), (891, "5 × 2 = 10", GOLD, b)):
        card(stage, x, 266, eq, colour, w=390, h=94, size=53, opacity=p)
    fit(stage, "8 + 10 = 18 numbers", 640, 402, 60, 1100, MINT, result)
    p = s.reveal("sixty-one thousand two hundred and four")
    stage.terms((("6", BLUE, p), ("1 2", WHITE, p), ("0 4", GOLD, p)), 520, 49)
    fit(stage, "One legal number is 61,204. The ending 04 passes.", 640, 587, 30, 1110, WHITE, p)


def common_errors(stage, s):
    mistakes(stage, s, SLOT, "Test the position of every card", (
        ("it cannot go at the very start", "06,124", "Zero can go inside: 60,124"),
        ("cross out any ending", "6 at front and in ending", "Use each card once"),
        ("remember to count the ways", "One number per ending", "Two middle orders per ending"),
    ))


def takeaway(stage, s):
    steps(stage, s, SLOT, "Turn restrictions into cases", (
        ("mark the places", "Use the strongest rule first", "Mark a forced first digit or ending."),
        ("case-split once", "Give each number one case", "Use a table to keep the cases separate."),
        ("check that every number", "Check every remaining place", "Count the possible orders of unfilled positions."),
    ))


SCENES = (introduction, exam, basic_prompt, basic, medium_prompt, medium, challenge_prompt,
          possible_endings, filter_front, count_numbers, common_errors, takeaway)
