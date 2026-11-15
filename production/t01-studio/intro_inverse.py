"""Lesson 3. Reverse a machine, a fraction of a whole and repeated changes."""

from intro_art import applications, card, header, mistakes, prompt, steps
from stage import BLUE, GOLD, MINT, MUTED, PANEL, RED, RIM, WHITE, blend
from studio_diagrams import bead, fit


SLOT = 3


def number_machine(stage, forward=(1, 1), values=("?", "", "31"), back=(0, 0)):
    for i, (x, value) in enumerate(zip((196, 640, 1084), values)):
        card(stage, x, 338, value, (MINT, BLUE, WHITE)[i], w=168, h=112, size=60)
    for i, (colour, direct, inverse) in enumerate(((BLUE, "×4", "÷4"), (GOLD, "+7", "−7"))):
        x = 330 + i * 444
        f, b = forward[i], back[i]
        stage.arrow((x, 309), (x + 172, 309), colour, f, 4)
        fit(stage, direct, x + 86, 262, 42, 185, colour, f)
        stage.arrow((x + 172, 386), (x, 386), colour, b, 4)
        fit(stage, inverse, x + 86, 447, 42, 185, colour, b)


def introduction(stage, s):
    header(stage, SLOT, "The idea", "Working backwards through operations")
    a = s.reveal("how a value changed")
    end = s.reveal("where the story ends")
    p = s.reveal("walk back along its steps")
    card(stage, 242, 335, "START", MINT, w=255, h=107, opacity=a)
    card(stage, 1038, 335, "FINISH", WHITE, w=255, h=107, opacity=end)
    stage.arrow((401, 313), (879, 313), BLUE, a, 4)
    fit(stage, "A change", 640, 263, 43, 375, BLUE, a)
    stage.arrow((879, 377), (401, 377), GOLD, p, 4)
    fit(stage, "Undo the change", 640, 430, 43, 459, GOLD, p)


def exam(stage, s):
    applications(stage, s, SLOT, "Start with the quantity you know", (
        ("an amc question", "AMC Upper Primary",
         "A number machine or a shrinking pile hides its start.", "Work back from the final amount."),
        ("a rossmoyne style puzzle", "Rossmoyne-style practice",
         "Show why the starting amount is forced.", "Use one inverse step for every forward step."),
    ))


def basic_prompt(stage, s):
    header(stage, SLOT, "Basic example", "Find the number machine’s input")
    number_machine(stage, (s.reveal("multiplies the input"), s.reveal("adds seven")),
                   ("?", "", "31" if s.reveal("output is thirty-one") > .35 else "?"))
    fit(stage, "Which operation happened last?", 640, 554, 43, 1085, WHITE,
        s.reveal("which step touched"))


def basic(stage, s):
    header(stage, SLOT, "Basic example", "Undo the last step first")
    a = s.reveal("thirty-one minus seven")
    b = s.reveal("by dividing by four")
    replay = s.reveal("run six forward", 1)
    number_machine(stage, (replay, replay),
                   ("6" if b > .55 else "?", "24" if a > .55 else "", "31"), (b, a))
    p = s.reveal("the input is six")
    fit(stage, "(31 − 7) ÷ 4 = 6", 640, 549, 56, 1080, MINT, p)


def stamp_bar(stage, x, y, opacity, restored=0):
    for i in range(3):
        left = x + i * 230
        colour = GOLD if i == 0 else BLUE
        fade = .34 if i == 0 else 1
        p = opacity * fade
        if i == 0:
            p = max(p, restored)
        stage.box(left, y, 220, 96, radius=16, fill=blend(PANEL, colour, .18), edge=colour,
                  opacity=p)
        for dot in range(9):
            bead(stage, left + 48 + (dot % 3) * 62, y + 23 + (dot // 3) * 25, colour, p, 7)


def medium_prompt(stage, s):
    header(stage, SLOT, "Medium example", "What was Sam’s starting pile?")
    p = s.reveal("sam gives away one third")
    for i in range(3):
        x = 397 + i * 230
        card(stage, x, 313, "1/3", GOLD if i == 0 else BLUE, w=212, h=100, opacity=p)
    fit(stage, "Gives away ⅓ of her original stamps", 640, 408, 41, 1080, WHITE, p)
    b = s.reveal("she receives seven stamps")
    stage.terms((("+7 stamps", GOLD, b), ("→", MUTED, b), ("25 at the end", WHITE, b)), 522, 48)


def medium(stage, s):
    header(stage, SLOT, "Medium example", "Restore one part, then the whole")
    start = s.reveal("eighteen stamps")
    stage.terms((("25", WHITE, start), ("−", WHITE, start), ("7", GOLD, start),
                 ("=", WHITE, start), ("18", BLUE, start)), 230, 51)
    p = s.reveal("two of the original three equal parts")
    original = s.reveal("three parts is twenty-seven")
    units = s.reveal("nine stamps per part")
    stamp_bar(stage, 300, 340, p, restored=original)
    stage.bracket(530, 980, 456, "2 parts = 18", BLUE, p * (1 - units))
    for n in range(3):
        fit(stage, "9", 410 + n * 230, 477, 39, 210, GOLD if n == 0 else BLUE,
            units * (original if n == 0 else 1))
    fit(stage, "3 × 9 = 27 stamps", 640, 573, 50, 1090, MINT, original)


def challenge_prompt(stage, s):
    prompt(stage, s, SLOT, "Exam-style challenge", "Reverse three ticket stations", (
        ("a player stops at three stations", "A player visits 3 stations."),
        ("at each station", "At each station, hand over half the current tickets,"),
        ("and then two more", "then hand over 2 more."),
        ("after the third station", "After the third stop, 5 remain. How many at the start?"),
    ))


def reverse_station(stage, s):
    header(stage, SLOT, "Exam-style challenge", "Walk back through station 3")
    add = s.reveal("add back the last two", .85)
    half = s.reveal("double seven", .85)
    card(stage, 1064, 357, "5", WHITE, w=144, h=108, size=60)
    card(stage, 640, 357, "7", GOLD, w=144, h=108, opacity=add, size=60)
    card(stage, 216, 357, "14", BLUE, w=144, h=108, opacity=half, size=60)
    for a, b, sign, p, colour in ((969, 738, "+2", add, GOLD), (546, 311, "×2", half, BLUE)):
        stage.arrow((a, 357), (b, 357), colour, p, 5)
        fit(stage, sign, (a + b) / 2, 298, 54, 185, colour, p)
    fit(stage, "Before station 3", 216, 453, 34, 274, BLUE, half)
    fit(stage, "After station 3", 1064, 453, 34, 274, WHITE)
    fit(stage, "Reverse rule: add 2, then double.", 640, 564, 46, 1105, MINT,
        s.reveal("the same reverse rule"))


def rewind(stage, s):
    header(stage, SLOT, "Exam-style challenge", "Restore the first two stations")
    stages = ((178, "68", "START", s.reveal("sixty-eight")),
              (487, "32", "AFTER 1", s.reveal("thirty-two")),
              (796, "14", "AFTER 2", 1),
              (1105, "5", "AFTER 3", 1))
    for x, value, label, p in stages:
        card(stage, x, 362, value, MINT if value == "68" else BLUE, w=127, h=98, size=57, opacity=p)
        fit(stage, label, x, 449, 26, 161, MUTED, p)
    for x, p in ((487, s.reveal("fourteen plus two")), (178, s.reveal("thirty-two plus two")), (796, 1)):
        stage.arrow((x + 230, 329), (x + 76, 329), GOLD, p, 4)
        fit(stage, "+2, then ×2", x + 154, 280, 27, 192, GOLD, p)
    p = s.reveal("halve and subtract")
    for x, target in ((178, 487), (487, 796), (796, 1105)):
        stage.arrow((x + 70, 397), (target - 70, 397), BLUE, p, 3)
    fit(stage, "Forward check:  halve, then subtract 2.", 640, 566, 43, 1100, MINT, p)


def common_errors(stage, s):
    mistakes(stage, s, SLOT, "Undo in the reverse order", (
        ("doubling five and then adding two", "5 × 2 + 2 = 12", "(5 + 2) × 2 = 14"),
        ("watch what the fraction", "Half the starting pile", "Half the current pile"),
    ))


def takeaway(stage, s):
    steps(stage, s, SLOT, "Make the whole story reversible", (
        ("circle what you know", "Start at the known endpoint", "Circle the final amount."),
        ("draw the forward arrows", "Reverse the order", "Write the inverse of each forward step."),
        ("label what each fraction", "Name the whole", "Say what the fraction is taken from."),
        ("run your starting value forward", "Check with the forward rule", "You should land on the stated final amount."),
    ))


SCENES = (introduction, exam, basic_prompt, basic, medium_prompt, medium, challenge_prompt,
          reverse_station, rewind, common_errors, takeaway)
