"""Remainder classes, repeating beads and two flash schedules."""

import math

from stage import BLUE, GOLD, MINT, MUTED, RED, RIM, WHITE, between, blend, mix
from studio_diagrams import BEAD_COLOURS, bead, fit, join, rail, recap, tile


def groups_of_five(stage, s):
    stage.heading("Seventeen counters in groups of five")
    start = s.at("seventeen counters")
    group = s.at("make three full groups of five")
    extra = s.reveal("with two left over")
    for row, x in enumerate((281, 520, 759)):
        p = between(s.t, group + row * 0.19, 0.8)
        stage.box(x - 99, 349, 198, 100, radius=17, fill=None, edge=BLUE, opacity=p)
        for col in range(5):
            i = 5 * row + col
            visible = between(s.t, start + 0.025 * i)
            old_x = 163 + i * 59
            bead(stage, mix(old_x, x - 68 + 34 * col, p), mix(259, 399, p), BLUE, visible, 13)
        fit(stage, "5", x, 482, 25, colour=BLUE, opacity=p)
    for col in range(2):
        bead(stage, mix(1048 + 59 * col, 1023 + 47 * col, extra), mix(259, 399, extra),
             blend(BLUE, GOLD, extra), between(s.t, start + 0.3 + 0.15 * col), 15)
    fit(stage, "2 left over", 1047, 482, 26, colour=GOLD, opacity=extra)
    show = s.reveal("how far seventeen is past")
    stage.terms([("17", WHITE, show), ("=", WHITE, show), ("3 × 5", BLUE, show),
                 ("+", WHITE, show), ("2", GOLD, show)], 567, 50)


def five_classes(stage, s):
    stage.heading("Only five remainders are possible")
    start = s.at("the possible remainders are zero")
    for i in range(5):
        x = 232 + 204 * i
        p = between(s.t, start + i * 0.21)
        stage.box(x - 84, 249, 168, 161, radius=21, edge=RIM, opacity=p)
        fit(stage, str(i), x, 374, 38, colour=MINT, opacity=p)
        for j in range(i):
            bead(stage, x + (j - (i - 1) / 2) * 27, 303, GOLD, p, 10)
    full = s.reveal("a leftover of five")
    for j in range(5):
        bead(stage, 331 + j * 31, 514, GOLD, full, 11)
    stage.arrow((502, 514), (595, 514), MINT, full, 3)
    stage.box(633, 476, 335, 75, radius=15, fill=None, edge=BLUE, opacity=full)
    fit(stage, "One complete group", 800, 514, 30, colour=BLUE, opacity=full)


def bead_strip(stage, start, n, y, *, opacity=1.0, focus=None, x=201, step=78):
    for i in range(n):
        index = start + i
        px = x + i * step
        a = opacity(i) if callable(opacity) else opacity
        if index == focus:
            stage.dot(px, y, 27, "#234c42", a)
        bead(stage, px, y, BEAD_COLOURS[(index - 1) % 4], a, 17)
        fit(stage, str(index), px, y + 45, 23, colour=WHITE if index == focus else MUTED, opacity=a)


def necklace(stage, s):
    stage.heading("What colour is bead 50?")
    show = s.at("repeats red, blue, green and yellow")
    bead_strip(stage, 1, 12, 316, opacity=lambda i: between(s.t, show + 0.13 * i))
    covered = s.reveal("boundaries between the repeating groups")
    for i in range(3):
        x = 201 + i * 312
        stage.bracket(x - 23, x + 3 * 78 + 23, 412, "4 beads", BLUE, covered)
    fit(stage, "The first bead is red.", 640, 534, 33, colour=WHITE,
        opacity=s.reveal("the first bead is red"))


def count_fifty(stage, s):
    stage.heading("Count full cycles, then the remainder")
    start = s.at("twelve groups of four")
    for i in range(12):
        x = 215 + 77 * i
        p = between(s.t, start + 0.10 * i)
        stage.box(x - 26, 232, 52, 66, radius=11, edge=RIM, opacity=p)
        for j, colour in enumerate(BEAD_COLOURS):
            bead(stage, x - 15 + 10 * j, 254, colour, p, 4.2)
        fit(stage, str(i + 1), x, 281, 17, colour=MUTED, opacity=p, bold=False)
    groups = s.reveal("take us to bead forty-eight")
    stage.bracket(188, 1088, 323, "12 full cycles = 48 beads", BLUE, groups)
    steps = s.reveal("count two beads into", 0.70)
    bead_strip(stage, 49, 4, 440, x=523, step=78, focus=50,
               opacity=lambda i: steps * (1.0 if i < 2 else 0.26))
    fit(stage, "Bead 50 is blue.", 640, 568, 43, colour=BLUE, opacity=s.reveal("bead fifty is blue"))


def remainder_zero(stage, s):
    stage.heading("Remainder zero lands at the boundary")
    result = s.reveal("bead forty-eight is yellow")
    mark = s.reveal("a complete group boundary")
    bead_strip(stage, 41, 8, 312, x=290, step=95, focus=48)
    stage.bracket(261, 604, 412, "One complete cycle", BLUE, mark)
    stage.bracket(643, 984, 412, "One complete cycle", BLUE, mark)
    join(stage, 987, 247, 418, GOLD, mark)
    fit(stage, "48 = 12 × 4", 438, 540, 45, colour=WHITE,
        opacity=s.reveal("remainder zero when divided by four"))
    fit(stage, "Bead 48 is yellow.", 799, 540, 39, colour=GOLD, opacity=result)


def equal_remainders(stage, s):
    stage.heading("The shared remainder cancels")
    a = s.reveal("twenty-three is four groups")
    b = s.reveal("thirty-eight is seven groups")
    cancel = s.reveal("the two leftovers cancel")
    count = s.reveal("give fifteen", offset=-0.28)
    fit(stage, "23", 154, 274, 40, colour=WHITE, opacity=a)
    fit(stage, "38", 154, 415, 40, colour=WHITE, opacity=b)
    for i in range(7):
        x = 282 + 96 * i
        if i < 4:
            tile(stage, x, 274, 5, BLUE, 72, 60, a * (1 - 0.62 * cancel))
            join(stage, x, 311, 381, BLUE, cancel)
        tile(stage, x, 415, 5, BLUE if i < 4 else MINT, 72, 60,
             b * (1 - 0.62 * cancel if i < 4 else 1))
    for y, p in ((274, a), (415, b)):
        tile(stage, 1050, y, "+3", GOLD, 99, 60, p * (1 - 0.73 * cancel))
    join(stage, 1050, 311, 381, GOLD, cancel)
    stage.bracket(635, 897, 475, "3 extra groups of 5", MINT, count)
    fit(stage, "38 − 23 = 15", 640, 575, 46, colour=MINT, opacity=count)


def two_conditions(stage, s):
    stage.heading("Use both remainder conditions", "Sort the candidates by their remainder on division by 3.")
    start = s.at("are three, eight, thirteen")
    send = s.at("now test them for remainder one")
    answer = s.reveal("only thirteen and twenty-eight")
    candidates = (3, 8, 13, 18, 23, 28)
    picked = {0: 0, 1: 0, 2: 0}
    for r in range(3):
        x = 285 + 355 * r
        stage.box(x - 131, 357, 262, 120, radius=18, fill=None,
                  edge=blend(RIM, MINT, answer if r == 1 else 0), opacity=between(s.t, send))
        fit(stage, f"Remainder {r}", x, 516, 25, colour=MINT if r == 1 else MUTED,
            opacity=between(s.t, send))
    for i, n in enumerate(candidates):
        r = n % 3
        end_x = 285 + 355 * r + (picked[r] - 0.5) * 96
        picked[r] += 1
        p = between(s.t, send + i * 0.13, 0.65)
        colour = blend(BLUE, MINT, answer) if r == 1 else BLUE
        tile(stage, mix(232 + 163 * i, end_x, p), mix(246, 413, p), n,
             colour, 82, 68, between(s.t, start + 0.10 * i))
    fit(stage, "13 and 28 satisfy both conditions.", 640, 582, 36, colour=MINT, opacity=answer)


def remainder_recap(stage, s):
    challenge = s.at("here is your notebook challenge")
    if s.t < challenge:
        stage.heading("What does the remainder measure?")
        groups = s.reveal("how far you are past a multiple")
        for i in range(17):
            x = 235 + (i // 5) * 220 + (i % 5) * 30
            bead(stage, x, 257, BLUE if i < 15 else GOLD, groups, 11)
        for i in range(3):
            x = 215 + i * 220
            stage.box(x, 225, 161, 64, radius=9, fill=None, edge=BLUE, opacity=groups)
        fit(stage, "17 = 3 × 5 + 2", 640, 351, 43, colour=WHITE, opacity=groups)
        bound = s.reveal("smaller than the divisor")
        fit(stage, "2 < 5", 640, 421, 35, colour=GOLD, opacity=bound)
        last = s.reveal("which position sits at remainder zero")
        for i, colour in enumerate(BEAD_COLOURS):
            bead(stage, 393 + i * 86, 528, colour, last, 17)
            fit(stage, str(i + 1), 393 + i * 86, 574, 22, colour=WHITE, opacity=last)
        fit(stage, "4th bead: remainder 0", 905, 529, 27, colour=GOLD, opacity=last)
        return

    stage.heading("Your turn: count whole weeks")
    begin = s.reveal("today is tuesday")
    question = s.reveal("one hundred days", 0.5)
    days = ("Tue", "Wed", "Thu", "Fri", "Sat", "Sun", "Mon", "Tue")
    for i, day in enumerate(days):
        x = 153 + 139 * i
        opacity = begin if i == 0 else question
        tile(stage, x, 345, day, GOLD if i in (0, 7) else BLUE, 106, 72, opacity, size=30)
        fit(stage, f"Day {i}", x, 420, 22, colour=MUTED, opacity=opacity)
    stage.bracket(153, 1126, 467, "7 days return to Tuesday", MINT, question)
    fit(stage, "What day will it be 100 days from now?", 640, 558, 34, colour=WHITE, opacity=question)


FLASH_Y = (296, 420)


def tick(t):
    return 241 + 34.5 * t


def flash_row(stage, index, period, values, *, opacity=1.0, labels=True):
    y, colour = FLASH_Y[index], (BLUE, GOLD)[index]
    fit(stage, f"Every {period} s", 135, y, 22, 155, colour)
    stage.line([(tick(0), y), (tick(24), y)], RIM, 4)
    for i, v in enumerate(values):
        p = opacity(i) if callable(opacity) else opacity
        bead(stage, tick(v), y, colour, p, 10)
        if labels:
            fit(stage, str(round(v)), tick(v), y + 33, 23, 53, colour, p, False)


def meetings(stage, times, opacity):
    for t in times:
        join(stage, tick(t), 312, 408, MINT, opacity)
        stage.box(tick(t) - 31, 214, 62, 41, radius=9, fill=None, edge=MINT, opacity=opacity)
        fit(stage, f"{t} s", tick(t), 235, 21, 54, MINT, opacity)


def flash_question_intro(stage, s):
    stage.heading("Two lights on one timeline")
    a = s.at("one flashes every four seconds")
    b = s.at("the other every six")
    flash_row(stage, 0, 4, (0, 4, 8), opacity=lambda i: between(s.t, a + i * 0.19))
    flash_row(stage, 1, 6, (0, 6), opacity=lambda i: between(s.t, b + i * 0.19))
    fit(stage, "First meeting?", 424, 553, 39, colour=MINT, opacity=s.reveal("when they first flash together"))
    fit(stage, "Time between meetings?", 818, 553, 35, colour=WHITE, opacity=s.reveal("how much time separates"))


def shared_period(stage, s):
    stage.heading("Lay out each period")
    p = s.reveal("twenty-four is a multiple")
    flash_row(stage, 0, 4, (0, 24), opacity=p)
    flash_row(stage, 1, 6, (0, 24), opacity=p)
    starts = s.reveal("first mark where each light starts")
    join(stage, tick(0), 312, 408, MINT, starts)
    step = s.reveal("then add its own period")
    for y, period, colour in ((FLASH_Y[0], 4, BLUE), (FLASH_Y[1], 6, GOLD)):
        stage.arrow((tick(0), y - 22), (tick(period), y - 22), colour, step, 3)
        fit(stage, f"+{period} s", (tick(0) + tick(period)) / 2, y - 47, 21, 92, colour, step)
    fit(stage, "Find the earliest shared mark.", 640, 546, 36, colour=MINT,
        opacity=s.reveal("a smaller common multiple"))


def same_start(stage, s):
    stage.heading("When do they next flash together?")
    start = s.reveal("both lights flash at time zero")
    flash_row(stage, 0, 4, (0,), opacity=start)
    flash_row(stage, 1, 6, (0,), opacity=start)
    join(stage, tick(0), 312, 408, MINT, start)
    prompt = s.reveal("list a few times")
    fit(stage, "Start at 0. List each light’s next few times.", 640, 543, 35, colour=MINT, opacity=prompt)


def common_flashes(stage, s):
    stage.heading("Find the first positive meeting")
    upper = s.at("the first light flashes at four")
    lower = s.at("the second flashes at six")
    more = s.reveal("the next meeting is twelve seconds later")
    flash_row(stage, 0, 4, (0, 4, 8, 12, 16, 20, 24),
              opacity=lambda i: 1.0 if not i else between(s.t, upper + (i - 1) * 0.17) if i < 5 else more)
    flash_row(stage, 1, 6, (0, 6, 12, 18, 24),
              opacity=lambda i: 1.0 if not i else between(s.t, lower + (i - 1) * 0.21) if i < 4 else more)
    both = s.reveal("their first positive meeting")
    meetings(stage, (12,), both)
    meetings(stage, (24,), more)
    stage.bracket(tick(12), tick(24), 498, "12 seconds apart", MINT, more)
    fit(stage, "LCM of 4 and 6 = 12", 640, 582, 34, colour=WHITE,
        opacity=s.reveal("twelve is the lowest common multiple"))


def shifted_start(stage, s):
    stage.heading("Move just the second starting time")
    shift = s.reveal("start at time two", 1.05)
    flash_row(stage, 0, 4, tuple(range(0, 25, 4)))
    flash_row(stage, 1, 6, tuple(v + 2 * shift for v in (0, 6, 12, 18)))
    first = s.reveal("the first meeting moves to eight seconds")
    second = s.reveal("the next is at twenty")
    meetings(stage, (8,), first)
    meetings(stage, (20,), second)
    gap = s.reveal("the twelve-second gap stayed the same")
    stage.bracket(tick(8), tick(20), 497, "Still 12 seconds apart", MINT, gap)


def odd_offset(stage, s):
    stage.heading("Can the two lights always meet?")
    shift = s.reveal("start the second light at time one", 0.75)
    odd = s.reveal("keep all its times odd")
    even = s.reveal("keeps the other times even")
    flash_row(stage, 0, 4, tuple(range(0, 25, 4)))
    flash_row(stage, 1, 6, tuple(v + 2 - shift for v in (0, 6, 12, 18)))
    tile(stage, 1103, 250, "Even", BLUE, 113, 53, even, 24)
    tile(stage, 1103, 491, "Odd", GOLD, 113, 53, odd, 24)
    fit(stage, "Even and odd times never meet.", 640, 570, 40, colour=MINT,
        opacity=s.reveal("an odd time and an even time cannot match"))


def flash_recap(stage, s):
    recap(stage, s, (("Use the LCM for spacing", "the lowest common multiple gives the gap"),
                     ("Check the starts", "the starting positions decide")),
          "in your notebook",
          ("One bus leaves every 8 minutes; another every 12.",
           "Both leave at 9:00. When do they next leave together?"),
          sub="Start both lists at the same time.")


SCENES = {
    "T03.1": (groups_of_five, five_classes, necklace, count_fifty, remainder_zero,
              equal_remainders, two_conditions, remainder_recap),
    "T03.2": (flash_question_intro, shared_period, same_start, common_flashes,
              shifted_start, odd_offset, flash_recap),
}
