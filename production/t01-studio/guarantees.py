"""Chapter 3 guarantees, with colour boxes, pairs and residue classes."""

import math

from stage import BLUE, GOLD, MINT, MUTED, PANEL, RED, RIM, WHITE, between, blend, mix
from studio_diagrams import BEAD_COLOURS, bead, fit, join, recap, tile


CENTRES = (290, 640, 990)


def bin_outline(stage, x, y, width, label, *, edge=RIM, opacity=1.0):
    stage.box(x - width / 2, y - 62, width, 124, radius=19,
              fill=None, edge=edge, opacity=opacity)
    fit(stage, label, x, y + 97, 25, width - 8, edge if edge != RIM else MUTED, opacity)


def four_counters(stage, s):
    stage.heading("Four counters and three boxes")
    show = s.reveal("put four counters")
    fill = s.at("place the first three")
    fourth = s.reveal("the fourth has to join", 0.85)
    for i, x in enumerate(CENTRES):
        bin_outline(stage, x, 395, 238, f"Box {i + 1}",
                    edge=blend(RIM, MINT, fourth if i == 0 else 0.0), opacity=show)
        motion = between(s.t, fill + 0.19 * i, 0.7)
        bead(stage, mix(416 + 148 * i, x - 27 * fourth if i == 0 else x, motion),
             mix(229, 394, motion), BLUE, show, 23)
    bead(stage, mix(860, CENTRES[0] + 27, fourth), mix(229, 394, fourth) - 35 * math.sin(math.pi * fourth),
         GOLD, show, 23)
    fit(stage, "Some box contains at least 2.", 640, 572, 40, colour=MINT,
        opacity=s.reveal("the claim already holds"))


def strongest_delay(stage, s):
    stage.heading("Find the largest arrangement without a match")
    limit = s.reveal("the arrangement that delays")
    force = s.reveal("smallest count that will force")
    for i, x in enumerate(CENTRES):
        bin_outline(stage, x, 350, 235, f"Box {i + 1}", opacity=limit)
        bead(stage, x - (32 * force if i == 2 else 0), 350, BLUE, limit, 24)
    bead(stage, mix(642, 1022, force), mix(222, 350, force), GOLD, force, 24)
    fit(stage, "One per box fills only 3 places.", 640, 546, 37, colour=WHITE, opacity=limit)
    fit(stage, "The fourth forces a match.", 640, 587, 30, colour=MINT, opacity=force)


def sock(stage, x, y, colour, opacity=1.0):
    stage.box(x - 20, y - 39, 43, 75, radius=10,
              fill=blend(PANEL, colour, 0.65), edge=colour, opacity=opacity)
    stage.box(x - 20, y + 11, 69, 30, radius=10,
              fill=blend(PANEL, colour, 0.65), edge=colour, opacity=opacity)
    stage.box(x - 21, y - 42, 45, 16, radius=6, fill=colour, opacity=opacity)


SOCK_X = (246, 509, 772, 1035)
COLOUR_NAMES = ("Red", "Blue", "Green", "Yellow")


def blind_draw(stage, s):
    stage.heading("How many socks guarantee a colour match?")
    start = s.at("a drawer contains many socks")
    for i, (x, colour, label) in enumerate(zip(SOCK_X, BEAD_COLOURS, COLOUR_NAMES)):
        p = between(s.t, start + 0.20 * i)
        sock(stage, x - 12, 312, colour, p)
        fit(stage, label, x, 405, 31, colour=colour, opacity=p)
    fit(stage, "Draw without looking.", 640, 533, 41, colour=WHITE,
        opacity=s.reveal("you take socks without looking"))


def fifth_sock(stage, s):
    stage.heading("Fill one box per colour")
    bins = s.reveal("use one box for each colour")
    start = s.at("begin with one sock in each box")
    fifth = s.reveal("the fifth sock has to go", 0.90)
    result = s.reveal("five is sufficient")
    for i, (x, colour, label) in enumerate(zip(SOCK_X, BEAD_COLOURS, COLOUR_NAMES)):
        edge = blend(colour, MINT, fifth if i == 1 else 0)
        bin_outline(stage, x, 398, 218, label, edge=edge, opacity=bins)
        move = between(s.t, start + 0.17 * i, 0.70)
        sock(stage, x - 12 - (30 * fifth if i == 1 else 0), mix(224, 398, move), colour, bins)
    ask = s.reveal("a possible draw of four socks")
    if fifth < 0.999:
        for x in SOCK_X:
            stage.arrow((640, 258), (x, 333), RIM, ask * (1 - fifth), 1.5)
    sock(stage, mix(640, SOCK_X[1] + 32, fifth), mix(214, 398, fifth),
         blend(WHITE, BEAD_COLOURS[1], fifth), ask)
    fit(stage, "4 can miss. 5 guarantees a pair.", 640, 571, 42, colour=MINT, opacity=result)


def residue_bins(stage, values, t, start, *, focus=None, opacity=1.0, accent=0.0):
    counts = {0: 0, 1: 0, 2: 0}
    for r, x in enumerate(CENTRES):
        edge = blend(RIM, MINT, accent if r == focus else 0)
        bin_outline(stage, x, 398, 259, f"Remainder {r}", edge=edge, opacity=opacity)
    for i, value in enumerate(values):
        label, remainder = value
        tx = CENTRES[remainder] - 53 + 105 * counts[remainder]
        counts[remainder] += 1
        p = between(t, start + 0.13 * i, 0.75)
        x = 640 + (i - (len(values) - 1) / 2) * 174
        tile(stage, mix(x, tx, p), mix(229, 398, p) - 16 * math.sin(math.pi * p),
             label, blend(BLUE, MINT, accent if remainder == focus else 0), 82, 62, opacity)


def whole_numbers(stage, s):
    stage.heading("Use the remainder as the box", "Example with 1, 4, 5 and 9")
    p = s.reveal("take any four different whole numbers")
    values = tuple((n, n % 3) for n in (1, 4, 5, 9))
    start = s.at("the possibilities are zero, one and two")
    match = s.reveal("two of the four numbers share a remainder")
    residue_bins(stage, values, s.t, start, focus=1, opacity=p, accent=match)
    proof = s.reveal("take their difference")
    fit(stage, "4 − 1 = 3", 640, 567, 43, colour=MINT, opacity=proof)


def pairs_of_eleven(stage, s):
    stage.heading("The boxes can be pairs")
    group = s.reveal("group the ten numbers")
    chosen = s.at("a choice of six")
    complete = s.reveal("both members of that pair")
    for i in range(5):
        x = 231 + 205 * i
        first = between(s.t, chosen + i * 0.15)
        second = between(s.t, chosen + 0.8) if i == 0 else 0
        box = blend(RIM, MINT, complete if i == 0 else 0)
        bin_outline(stage, x, 354, 170, "Sum 11", edge=box, opacity=group)
        tile(stage, x - 43, 354, i + 1, GOLD, 68, 63, group * (0.38 + 0.62 * first))
        tile(stage, x + 43, 354, 10 - i, GOLD, 68, 63, group * (0.38 + 0.62 * second))
    fit(stage, "6 choices in 5 pair boxes", 640, 542, 39, colour=MINT,
        opacity=s.reveal("puts two numbers in one"))


def guarantee_recap(stage, s):
    if s.t < s.at("in your notebook"):
        stage.heading("How long can a pair be delayed?")
        boxes = s.reveal("choose the boxes")
        counts = s.reveal("compare their counts")
        fewer = s.reveal("one fewer could fail")
        for i, (x, colour, label) in enumerate(zip(SOCK_X, BEAD_COLOURS, COLOUR_NAMES)):
            bin_outline(stage, x, 365, 201, label, edge=colour, opacity=boxes)
            sock(stage, x, 365, colour, counts)
        fit(stage, "4 colours", 640, 500, 32, colour=WHITE, opacity=counts)
        fit(stage, "One of each colour: four draws can miss.", 640, 560, 30,
            colour=MINT, opacity=fewer)
        return

    stage.heading("Birthdays in the same month")
    months = ("Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
    begin = s.at("how many people")
    for i, month in enumerate(months):
        x = 208 + 172 * (i % 6)
        y = 250 + 142 * (i // 6)
        box = between(s.t, begin + i * .045, .42)
        stage.box(x - 66, y - 48, 132, 106, radius=12, fill=None, edge=BLUE, opacity=box)
        fit(stage, month, x, y - 22, 23, colour=WHITE, opacity=box)
        bead(stage, x, y + 23, GOLD, between(s.t, s.at("two birthdays") + i * .1, .42), 12)
    fit(stage, "One person per month delays a match.", 640, 505, 30, colour=GOLD,
        opacity=s.reveal("in the same month"))
    fit(stage, "How many people force a shared month?", 640, 565, 34, colour=WHITE,
        opacity=s.reveal("in the same month"))


def difference_claim(stage, s):
    stage.heading("Prove a difference is a multiple of three")
    p = s.reveal("choose any four different whole numbers")
    for i in range(4):
        tile(stage, 281 + 239 * i, 304, f"Number {i + 1}", BLUE, 194, 78,
             p, size=25)
    fit(stage, "How can we prove a pair always exists?", 640, 505, 39, colour=WHITE,
        opacity=s.reveal("two of them always have"))


def three_boxes(stage, s):
    stage.heading("There are three remainder boxes")
    start = s.at("the remainder can be zero")
    for r, x in enumerate(CENTRES):
        p = between(s.t, start + r * 0.22)
        bin_outline(stage, x, 355, 244, f"Remainder {r}", opacity=p)
        for k in range(r):
            bead(stage, x + (k - (r - 1) / 2) * 52, 354, GOLD, p, 18)
    group = s.reveal("a leftover of three")
    stage.terms([("3", GOLD, group), ("=", WHITE, group), ("1 full group", BLUE, group),
                 ("+", WHITE, group), ("0 left over", MINT, group)], 545, 37)


def guarantee_pair(stage, s):
    stage.heading("A shared box is unavoidable", "One possible placement")
    start = s.at("four numbers and three boxes")
    focus = s.reveal("those two numbers have the same remainder")
    residue_bins(stage, (("A", 0), ("B", 1), ("C", 2), ("D", 1)), s.t, start,
                 focus=1, opacity=s.reveal("every chosen number"), accent=focus)
    fit(stage, "At least two have the same remainder.", 640, 567, 37, colour=MINT, opacity=focus)


def subtract_leftovers(stage, s):
    stage.heading("Subtract the equal leftovers")
    a = s.reveal("the larger number as three a")
    b = s.reveal("the smaller as three b")
    cancel = s.reveal("the two r terms cancel", 0.72)
    finish = s.reveal("three times the difference")
    for row, part, p, label in ((275, "3a", a, "Larger"), (410, "3b", b, "Smaller")):
        fit(stage, label, 277, row, 26, colour=MUTED, opacity=p)
        tile(stage, 511, row, part, BLUE, 160, 69, p)
        fit(stage, "+", 624, row, 40, colour=WHITE, opacity=p * (1 - cancel))
        tile(stage, 736, mix(row, 344, cancel), "r", GOLD, 122, 69, p * (1 - cancel))
    join(stage, 736, 311, 376, GOLD, cancel * (1 - cancel) * 4)
    stage.terms([("3a", BLUE, finish), ("−", WHITE, finish), ("3b", BLUE, finish),
                 ("=", WHITE, finish), ("3(a − b)", MINT, finish)], 545, 44)


def examples_of_difference(stage, s):
    stage.heading("Check the example and the minimum")
    fewer = s.at("could three numbers guarantee")
    transition = between(s.t, fewer, 0.55)
    first_opacity = max(0.0, 1 - 2 * transition)
    next_opacity = max(0.0, 2 * transition - 1)
    display = s.reveal("try two, six, ten and thirteen")
    focus = s.reveal("ten and thirteen both leave remainder one")
    residue_bins(stage, tuple((n, n % 3) for n in (2, 6, 10, 13)), s.t,
                 s.at("try two, six, ten and thirteen") + 0.35, focus=1,
                 opacity=display * first_opacity, accent=focus)
    fit(stage, "13 − 10 = 3", 640, 560, 43, colour=MINT,
        opacity=s.reveal("their difference is three") * first_opacity)
    residue_bins(stage, tuple((n, n % 3) for n in (1, 2, 3)), s.t,
                 s.at("with one, two and three") + 0.25, opacity=next_opacity)
    fit(stage, "1, 2 and 3 all have different remainders.", 640, 553, 36, colour=WHITE,
        opacity=s.reveal("the remainders all differ"))
    fit(stage, "Four is the minimum guarantee.", 640, 599, 30, colour=MINT,
        opacity=s.reveal("four is the smallest"))


def difference_recap(stage, s):
    if s.t < s.at("now increase the divisor to ten"):
        stage.heading("Subtract two numbers from the same box")
        group = s.reveal("a box for each remainder")
        cancel = s.reveal("use subtraction")
        for y, n in ((278, 10), (410, 13)):
            fit(stage, str(n), 255, y, 36, colour=WHITE, opacity=group)
            for i in range(n):
                x = 350 + 133 * (i // 3) + 31 * (i % 3) if i < n - 1 else 1015
                colour = GOLD if i == n - 1 else MINT if i >= 9 else BLUE
                keep = n == 13 and 9 <= i < 12
                bead(stage, x, y, colour, group * (1 if keep else 1 - .66 * cancel), 12)
            for i in range(n // 3):
                stage.box(329 + 133 * i, y - 27, 106, 54, radius=9, fill=None, edge=BLUE, opacity=group)
        fit(stage, "13 − 10 = one group of 3", 640, 545, 34, colour=MINT, opacity=cancel)
        return

    stage.heading("Change the divisor to ten")
    start = s.at("increase the divisor to ten")
    witness = s.at("one fewer choice")
    for r in range(10):
        x = 245 + (r % 5) * 197
        y = 268 + (r // 5) * 135
        appear = between(s.t, start + r * .07, .45)
        stage.box(x - 73, y - 56, 146, 110, radius=11, fill=None, edge=BLUE, opacity=appear)
        fit(stage, f"Rem. {r}", x, y - 27, 23, colour=WHITE, opacity=appear)
        tile(stage, x, y + 16, str(r), GOLD, 56, 42,
             between(s.t, witness + r * .07, .42), size=24)
    fit(stage, "How many choices guarantee a shared remainder?", 640, 515, 32, colour=WHITE,
        opacity=s.reveal("how many different whole numbers"))
    fit(stage, "0 through 9: one number per box", 640, 574, 27, colour=GOLD,
        opacity=s.reveal("one fewer choice"))


SCENES = {
    "T03.3": (four_counters, strongest_delay, blind_draw, fifth_sock, whole_numbers,
              pairs_of_eleven, guarantee_recap),
    "T03.E": (difference_claim, three_boxes, guarantee_pair, subtract_leftovers,
              examples_of_difference, difference_recap),
}
