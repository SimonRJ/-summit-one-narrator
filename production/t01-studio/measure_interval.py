"""T01.E, a worked example in measuring between two positions."""

from stage import BG, BLUE, GOLD, MINT, MUTED, RED, RIM, WHITE
from stage import between, blend, mix


RULER_X = 184
CENTIMETRE = 76
RULER_Y = 376
RIBBON_START = 2
RIBBON_END = 9
LENGTH = RIBBON_END - RIBBON_START
CLOCK = (0, 45, 105, 110)
CLOCK_Y = 364


def cm(position):
    return RULER_X + position * CENTIMETRE


def minutes(position):
    return 228 + position * 7.4


def ruler(stage, opacity=1.0):
    x, y = cm(0), RULER_Y
    width = cm(12) - x
    stage.box(x - 29, y - 10, width + 58, 80, radius=15, fill="#111820", opacity=opacity)
    stage.box(x - 29, y - 15, width + 58, 80, radius=15, fill="#263747", edge="#556879", opacity=opacity)
    stage.line([(x - 15, y - 8), (x + width + 15, y - 8)], "#697e91", 2, 0.78 * opacity)
    for tick in range(13):
        left = cm(tick)
        stage.line([(left, y - 3), (left, y + 19)], WHITE, 2, opacity)
        stage.text(str(tick), left, y + 43, 23, WHITE, opacity=opacity)
        if tick < 12:
            mid = cm(tick + 0.5)
            stage.line([(mid, y - 3), (mid, y + 10)], MUTED, 1.5, opacity)
    stage.text("cm", cm(12) + 56, y + 42, 22, MUTED, opacity=opacity)


def ribbon(stage, start=RIBBON_START, *, opacity=1.0, guides=1.0):
    x, y = cm(start), 296
    width = LENGTH * CENTIMETRE
    stage.box(x, y + 5, width, 36, radius=3, fill="#282520", opacity=opacity)
    stage.box(x, y, width, 36, radius=3, fill="#a9773c", edge=GOLD, opacity=opacity)
    stage.line([(x + 3, y + 6), (x + width - 3, y + 6)], "#f2ca88", 2, opacity)
    for position, colour in ((x, BLUE), (x + width, GOLD)):
        stage.line([(position, y + 35), (position, RULER_Y + 15)], colour, 2, opacity * guides)


def ribbon_problem(stage, s):
    stage.heading("How long is the ribbon?")
    ruler(stage, s.reveal("a ribbon lies along a centimetre ruler"))
    ribbon(stage, opacity=s.reveal("its left edge lines up with two"), guides=0)
    first = s.reveal("its left edge lines up with two")
    last = s.reveal("its right edge lines up with nine")
    stage.line([(cm(2), 333), (cm(2), RULER_Y + 10)], BLUE, 3, first)
    stage.line([(cm(9), 333), (cm(9), RULER_Y + 10)], GOLD, 3, last)
    stage.text("Start at 2", cm(2), 260, 28, BLUE, bold=True, opacity=first)
    stage.text("End at 9", cm(9), 260, 28, GOLD, bold=True, opacity=last)
    stage.text("What can you measure from those two marks?", 640, 521, 37, WHITE,
               bold=True, opacity=s.reveal("how long is the ribbon"))


def positions(stage, s):
    stage.heading("Read the two positions")
    ruler(stage)
    ribbon(stage)
    chosen = s.reveal("the distance from the first position")
    a = s.reveal("a position two centimetres from zero")
    b = s.reveal("a position nine centimetres from zero")
    stage.arrow((cm(0), 210), (cm(2), 210), BLUE, a, 3)
    stage.text("2 cm from zero", (cm(0) + cm(2)) / 2 + 8, 188, 24, BLUE, opacity=a)
    stage.arrow((cm(0), 253), (cm(9), 253), GOLD, b, 3)
    stage.text("9 cm from zero", (cm(0) + cm(9)) / 2, 230, 24, GOLD, opacity=b)
    stage.bracket(cm(2), cm(9), 483, "Distance between the two marks", MINT, chosen)


def steps(stage, s):
    stage.heading("Count the centimetre intervals")
    ruler(stage)
    ribbon(stage, opacity=0.58)
    first = s.at("move from two to three")
    second = s.at("from three to four")
    repeated = s.at("keep going until you reach nine")
    total = s.at("there are seven gaps")
    starts = (first, second, *(mix(repeated, total - 0.36, i / 4) for i in range(5)))
    for interval, start in enumerate(starts):
        position = RIBBON_START + interval
        progress = between(s.t, start, 0.38)
        if progress > 0.01:
            stage.box(cm(position) + 2, 282, (CENTIMETRE - 4) * progress, 64, radius=5,
                      fill="#42412e", edge=GOLD, opacity=progress)
            stage.text(str(interval + 1), cm(position + 0.5), 313, 28, GOLD,
                       bold=True, opacity=progress)
    complete = s.reveal("the ribbon is seven centimetres long", offset=0.35)
    gap_count = s.reveal("there are seven gaps")
    stage.terms([("7 gaps", GOLD, gap_count), ("×", WHITE, gap_count), ("1 cm", GOLD, gap_count),
                 ("=", WHITE, complete), ("7 cm", MINT, complete)], 533, 45)


def subtraction(stage, s):
    stage.heading("Remove what comes before the ribbon")
    ruler(stage)
    total = s.reveal("the nine centimetres from zero to the end")
    before = s.reveal("two centimetres before the ribbon begins")
    remove = s.reveal("remove those two centimetres", 0.85)
    solve = s.reveal("nine minus two leaves seven", offset=0.22)
    marks_start = s.at("eight marked points across the ribbon")
    gaps = s.reveal("in the space between two marks")
    for index in range(RIBBON_END):
        colour = blend(GOLD, RED, before) if index < RIBBON_START else GOLD
        opacity = total * (1 - remove) if index < RIBBON_START else total
        y = 290 - (55 * remove if index < RIBBON_START else 0)
        stage.box(cm(index) + 2, y, CENTIMETRE - 4, 54, radius=5,
                  fill=blend(BG, colour, 0.63), edge=colour, opacity=opacity)
        if index >= RIBBON_START:
            stage.text(str(index - RIBBON_START + 1), cm(index + 0.5), y + 26,
                       25, GOLD, bold=True, opacity=gaps)
    for index in range(RIBBON_START, RIBBON_END + 1):
        stage.dot(cm(index), 356, 5, BLUE,
                  between(s.t, marks_start + 0.10 * (index - RIBBON_START)))
    stage.text("8 marked points", cm(5.5), 247, 27, BLUE, bold=True,
               opacity=between(s.t, marks_start))
    stage.terms([("9 cm", GOLD, solve), ("−", WHITE, solve), ("2 cm", RED, solve),
                 ("=", WHITE, solve), ("7 cm", MINT, solve)], 533, 49)
    stage.text("7 spaces between the marks", 640, 595, 28, MINT,
               opacity=gaps)


def slide_check(stage, s):
    stage.heading("Slide the ribbon to check")
    ruler(stage)
    moves = s.at("slide the ribbon two centimetres to the left")
    reaches = s.at("it starts at zero and reaches seven")
    travel = between(s.t, moves, max(0.8, reaches - moves))
    start = mix(RIBBON_START, 0, travel)
    for pos in (RIBBON_START, RIBBON_END):
        for y in range(237, 279, 10):
            stage.line([(cm(pos), y), (cm(pos), y + 5)], MUTED, 2, travel * 0.7)
    stage.arrow((cm(5.5), 250), (cm(3.5), 250), BLUE, travel, 3)
    ribbon(stage, start)
    stage.bracket(cm(start), cm(start + LENGTH), 487, "7 cm", MINT,
                  s.reveal("the span stayed seven centimetres", offset=-0.15))
    stage.text("Both ends move 2 cm.", 640, 557, 34, WHITE,
               opacity=s.reveal("watch both ends move the same distance"))


def time_marks(stage, shown):
    for i, (point, label, opacity) in enumerate(zip(CLOCK, ("7:15 pm", "8:00", "9:00", "9:05 pm"), shown)):
        x = minutes(point)
        colour = MINT if i in (0, 3) else BLUE
        if i == 3:
            stage.line([(x, CLOCK_Y), (x, CLOCK_Y - 50)], colour, 2, opacity)
            stage.text(label, x + 11, CLOCK_Y - 70, 26, colour, bold=True, opacity=opacity)
        else:
            stage.line([(x, CLOCK_Y), (x, CLOCK_Y + 19)], colour, 2, opacity)
            stage.text(label, x, CLOCK_Y + 49, 26, colour, bold=True, opacity=opacity)
        stage.dot(x, CLOCK_Y, 6, colour, opacity)


def time_problem(stage, s):
    stage.heading("Measure the time between two readings")
    start = s.reveal("a film starts at seven fifteen")
    finish = s.reveal("ends at nine oh five")
    stage.text("Start 7:15 pm", 418, 219, 36, BLUE, bold=True, opacity=start)
    stage.arrow((561, 219), (700, 219), RIM, finish, 3)
    stage.text("Finish 9:05 pm", 868, 219, 36, MINT, bold=True, opacity=finish)
    track = s.reveal("draw a timeline", 0.76)
    stage.line([(minutes(0), CLOCK_Y), (mix(minutes(0), minutes(110), track), CLOCK_Y)], RIM, 5, track)
    shown = (
        s.reveal("put seven fifteen on the left"),
        s.reveal("mark eight o'clock"),
        s.reveal("and nine o'clock along the way"),
        s.reveal("stop at nine oh five"),
    )
    time_marks(stage, shown)
    stage.text("How many minutes pass?", 640, 523, 42, WHITE, bold=True,
               opacity=s.reveal("how many minutes pass"))


def elapsed_time(stage, s):
    stage.heading("Add the minutes across the hour marks")
    stage.line([(minutes(0), CLOCK_Y), (minutes(CLOCK[-1]), CLOCK_Y)], RIM, 5)
    cues = ("is forty-five minutes", "the next hour gives sixty minutes", "five more")
    intervals = tuple((a, b, s.reveal(cue, 0.75), colour) for a, b, cue, colour in zip(
        CLOCK, CLOCK[1:], cues, (GOLD, BLUE, MINT)
    ))
    for i, (left, right, opacity, colour) in enumerate(intervals):
        x1, x2 = minutes(left), minutes(right)
        span = x2 - x1
        if opacity > 0.01:
            stage.box(x1 + 1, CLOCK_Y - 13, (span - 2) * opacity, 26, radius=4,
                      fill=blend(BG, colour, 0.68), edge=colour, opacity=opacity)
        if i < 2:
            stage.text(f"{right - left} min", (x1 + x2) / 2, 316, 32,
                       colour, bold=True, opacity=opacity)
        else:
            stage.line([((x1 + x2) / 2, CLOCK_Y - 18), (x2 + 92, 330)], MINT, 2, opacity)
            stage.text("5 min", x2 + 94, 313, 25, MINT, bold=True, opacity=opacity)
    time_marks(stage, (1.0, 1.0, 1.0, 1.0))
    total = s.reveal("the total is one hundred and ten minutes", offset=0.45)
    p = s.reveal("add forty-five, sixty and five")
    stage.terms([("45", GOLD, p), ("+", WHITE, p), ("60", BLUE, p), ("+", WHITE, p),
                 ("5", MINT, p), ("=", WHITE, total), ("110 minutes", MINT, total)], 520, 48)
    stage.text("1 hour 50 minutes", 640, 580, 28, MUTED,
               opacity=s.reveal("one hour and fifty minutes"))


def recap(stage, s):
    challenge = s.reveal("now try your own timeline")
    stage.heading("Measure between two positions", opacity=1 - challenge)
    show = s.reveal("label the two positions") * (1 - challenge)
    stage.line([(299, 327), (981, 327)], RIM, 4, show)
    for x, title, colour in ((299, "Start", BLUE), (981, "End", GOLD)):
        stage.dot(x, 327, 8, colour, show)
        stage.text(title, x, 285, 30, colour, bold=True, opacity=show)
    stage.bracket(299, 981, 399, "Length or elapsed time", MINT,
                  (1 - challenge) * s.reveal("between them"))
    stage.text("Use equal steps. Check the units.", 640, 517, 32, WHITE,
               opacity=(1 - challenge) * s.reveal("use equal steps"))

    stage.heading("Your turn", opacity=challenge)
    first = s.reveal("ten forty-seven in the morning")
    last = s.reveal("stops at twelve oh six")
    stage.line([(259, 334), (1021, 334)], RIM, 4, first)
    stage.dot(259, 334, 8, BLUE, first)
    stage.dot(1021, 334, 8, GOLD, last)
    stage.text("10:47 am", 259, 284, 35, BLUE, bold=True, opacity=first)
    stage.text("12:06 pm", 1021, 284, 35, GOLD, bold=True, opacity=last)
    stage.text("How many minutes does the camera record?", 640, 507, 39, WHITE, bold=True,
               opacity=s.reveal("how many minutes does it record"))
    stage.text("Draw the timeline, then count the minutes.", 640, 559, 27, MINT,
               opacity=s.reveal("how many minutes does it record", offset=0.2))


SCENES = (ribbon_problem, positions, steps, subtraction, slide_check,
          time_problem, elapsed_time, recap)
