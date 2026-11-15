"""Lesson 1. Group objects, narrow a shortlist and align two periods."""

from intro_art import applications, card, header, mistakes, prompt, stagger, steps
from stage import BLUE, GOLD, MINT, MUTED, RED, RIM, WHITE, blend, mix
from studio_diagrams import bead, fit


SLOT = 1
CHOICES = (124, 142, 212, 221)
MEETINGS = (104, 122, 140, 158, 176, 194)


def packets(stage, fraction, result=0, *, opacity=1):
    for packet in range(6):
        x, y = 173 + packet * 151, 365
        stage.box(x - 62, y - 59, 124, 118, radius=20, fill="#192b3d", edge=BLUE,
                  opacity=fraction * opacity)
        for sticker in range(6):
            index = packet * 6 + sticker
            col, row = sticker % 3, sticker // 3
            bead(stage, mix(121 + (index % 19) * 56, x + (col - 1) * 34, fraction),
                 mix(287 + (index // 19) * 46, y + (row - .5) * 36, fraction),
                 BLUE, opacity, 11)
    for sticker in range(2):
        index = 36 + sticker
        bead(stage, mix(121 + (index % 19) * 56, 1085 + sticker * 42, fraction),
             mix(333, 365, fraction), blend(BLUE, GOLD, fraction), opacity, 13)
    stage.bracket(111, 991, 453, "6 full packets", BLUE, result)
    stage.bracket(1065, 1147, 453, "2 left", GOLD, result)


def introduction(stage, s):
    header(stage, SLOT, "The idea", "Divisibility and remainders")
    p = s.reveal("a remainder is what is left", .8)
    grouped = s.reveal("equal groups", 1.5)
    packets(stage, grouped, grouped, opacity=p)
    fit(stage, "Equal groups + what is left", 640, 552, 43, 1085, MINT,
        s.reveal("that tiny number"))


def exam(stage, s):
    applications(stage, s, SLOT, "Recognise the clue in the question", (
        ("in amc upper primary practice", "AMC Upper Primary",
         "“Divides evenly”  ·  “Left over”  ·  “Repeats every”", "Turn each phrase into a test."),
        ("in a rossmoyne style number puzzle", "Rossmoyne-style practice",
         "Several clues can restrict the same number.", "Keep only the candidates that pass every test."),
    ))


def basic_prompt(stage, s):
    header(stage, SLOT, "Basic example", "Pack 38 stickers")
    packets(stage, 0, opacity=s.reveal("thirty-eight stickers"))
    p = s.reveal("each full packet holds six")
    card(stage, 640, 433, "6 per packet", GOLD, w=320, h=81, opacity=p, size=39)
    fit(stage, "How many full packets?  How many left over?", 640, 549, 42, 1080, WHITE,
        s.reveal("how many full packets"))


def basic(stage, s):
    header(stage, SLOT, "Basic example", "Group the stickers")
    packets(stage, s.reveal("six packets", 1.5), s.reveal("leaving two"))
    p = s.reveal("thirty-eight equals", .7)
    stage.terms((("38", WHITE, p), ("=", WHITE, p), ("6 × 6", BLUE, p),
                 ("+", WHITE, p), ("2", GOLD, p)), 557, 56)


def choices(stage, reveal, shows=(1, 1, 1, 1), results=(0, 0, 0, 0)):
    for i, (number, p, result) in enumerate(zip(CHOICES, shows, results)):
        x = 211 + 286 * i
        colour = BLUE
        if i % 2:
            p *= 1 - .66 * reveal
            colour = blend(BLUE, RED, reveal)
        elif i == 2:
            colour = blend(BLUE, MINT, result)
        card(stage, x, 316, number, colour, w=208, h=112, opacity=p, size=60)
        fit(stage, f"last two: {number % 100:02}", x, 408, 27, 208, colour, reveal * p)
        if i % 2 == 0:
            fit(stage, ("123 + 1" if i == 0 else "210 + 2"), x, 475, 38, 238,
                GOLD if i == 0 else MINT, result)


def medium_prompt(stage, s):
    header(stage, SLOT, "Medium example", "Which number passes both tests?")
    choices(stage, 0, tuple(stagger(s, "these four numbers", i) for i in range(4)))
    fit(stage, "Divisible by 4", 369, 496, 42, 480, BLUE, s.reveal("divisible by four"))
    fit(stage, "Remainder 2 when divided by 3", 875, 496, 38, 630, GOLD,
        s.reveal("leave remainder two"))


def medium(stage, s):
    header(stage, SLOT, "Medium example", "Test the last two digits",
           "100 is a multiple of 4, so only the last two digits affect this test.")
    p = s.reveal("forty-two and twenty-one are out")
    choices(stage, p, results=(s.reveal("one hundred and twenty-four is one past"), 0,
                              s.reveal("two hundred and twelve is two past"), 0))
    fit(stage, "212 passes both tests.", 640, 569, 53, 1070, MINT, s.reveal("so it fits both clues"))


def challenge_prompt(stage, s):
    prompt(stage, s, SLOT, "Exam-style challenge", "When do both beacons flash?", (
        ("a blue beacon flashes", "Blue beacon starts at minute 2, then flashes every 6 minutes."),
        ("a gold beacon flashes", "Gold beacon starts at minute 5, then flashes every 9 minutes."),
        ("when do they flash together", "Find a common flash strictly between minutes 100 and 200."),
        ("at a multiple of five", "The minute must be a multiple of 5."),
    ))


def rendezvous(stage, s):
    header(stage, SLOT, "Exam-style challenge", "Find the first meeting")
    for label, y, colour, times, cue in (
        ("BLUE", 278, BLUE, (2, 8, 14, 20, 26, 32), "blue goes at two"),
        ("GOLD", 426, GOLD, (5, 14, 23, 32), "gold goes at five"),
    ):
        stage.text(label, 87, y, 25, colour, bold=True, align="left")
        stage.line(((192, y), (1150, y)), RIM, 3)
        for i, time in enumerate(times):
            x = 197 + time * 28
            p = stagger(s, cue, i, delay=.2) if time <= 14 else s.reveal("every eighteen minutes")
            bead(stage, x, y, colour, p, 14)
            fit(stage, str(time), x, y + 41, 32, 77, colour, p)
    first = s.reveal("they first meet at fourteen")
    interval = s.reveal("every eighteen minutes")
    for time, p in ((14, first), (32, interval)):
        x = 197 + time * 28
        stage.line(((x, 300), (x, 404)), MINT, 3, p)
    stage.bracket(589, 1093, 503, "18 minutes between meetings", MINT, interval)
    fit(stage, "18 = 3 × 6 = 2 × 9", 330, 541, 38, 483, MINT, interval)


def search_range(stage, s):
    header(stage, SLOT, "Exam-style challenge", "Jump 18 minutes at a time")
    earlier = s.reveal("eighty-six")
    card(stage, 105, 340, "86", MUTED, w=95, h=76, opacity=earlier)
    stage.line(((182, 270), (182, 439)), RIM, 2, earlier)
    stage.line(((1187, 270), (1187, 439)), RIM, 2, earlier)
    fit(stage, "100", 182, 474, 28, 100, MUTED, earlier)
    fit(stage, "200", 1187, 474, 28, 100, MUTED, earlier)
    p = s.reveal("only one ends in zero or five")
    cues = ("one hundred and four", "one hundred and twenty-two", "one hundred and forty",
            "one hundred and fifty-eight", "one hundred and seventy-six", "one hundred and ninety-four")
    for i, (time, cue) in enumerate(zip(MEETINGS, cues)):
        x = 264 + 168 * i
        a = s.reveal(cue)
        mark = time == 140
        colour = blend(BLUE, MINT, p) if mark else BLUE
        card(stage, x, 340, time, colour, w=118, h=86, opacity=a * (1 if mark else 1 - .58 * p))
        if i:
            stage.arrow((x - 106, 338), (x - 67, 338), BLUE, a * (1 - .45 * p))
            fit(stage, "+18", x - 83, 281, 23, 67, BLUE, a * (1 - .45 * p))
    fit(stage, "140 is the shared flash at a multiple of 5.", 640, 554, 41, 1100, MINT,
        s.reveal("one hundred and forty is the answer"))


def checks(stage, s):
    header(stage, SLOT, "Exam-style challenge", "Check the three original clues")
    for i, (cue, label, value, colour) in enumerate((
        ("one hundred and forty minus two", "Blue cycles", "140 − 2 = 138 = 23 × 6", BLUE),
        ("one hundred and forty minus five", "Gold cycles", "140 − 5 = 135 = 15 × 9", GOLD),
        ("twenty-eight times five", "Multiple of 5", "140 = 28 × 5", MINT),
    )):
        y = 242 + i * 132
        p = s.reveal(cue)
        card(stage, 248, y, label, colour, w=310, h=82, size=36, opacity=p)
        fit(stage, value, 745, y, 51, 615, colour, p)


def common_errors(stage, s):
    mistakes(stage, s, SLOT, "Check the period, the test and the range", (
        ("adding the periods", "6 + 9 = 15", "Shared period = 18"),
        ("divisible means remainder zero", "Any leftover still divides", "Divisible means remainder 0"),
        ("keep your search inside", "Check 86", "Search only inside 100–200"),
    ))


def takeaway(stage, s):
    steps(stage, s, SLOT, "Use each clue as a filter", (
        ("write the remainders", "Record the clues", "Keep the divisor beside its remainder."),
        ("combine the clues", "Combine one at a time", "Build a list with the shared period."),
        ("check your answer", "Check against the original question", "Use all conditions and the given range."),
        ("for a mawa style investigation", "Extend the problem", "Change the starting minute and predict what happens."),
    ))


SCENES = (introduction, exam, basic_prompt, basic, medium_prompt, medium, challenge_prompt,
          rendezvous, search_range, checks, common_errors, takeaway)
