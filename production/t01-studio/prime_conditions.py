"""Compare and pair copies of primes to prove divisibility and minimality."""

from stage import BLUE, GOLD, MINT, MUTED, RED, RIM, WHITE, mix
from studio_diagrams import PRIME_COLOURS, fit, join, prime, rail, tile


PRIMES = (2, 3)
ORIGINAL = ((2, 1), (1, 2))
COLUMNS = (557, 902)


def row(stage, counts, y, label, opacity=1.0, *, selection=None, columns=COLUMNS):
    fit(stage, label, 234, y, 40, 310, WHITE, opacity)
    for i, (x, value, count) in enumerate(zip(columns, PRIMES, counts)):
        for j in range(count):
            selected = selection[i] if selection is not None else count
            prime(stage, x + 39 * (2 * j - 1), y, value,
                  opacity * (1 if j < selected else 0.23), 66)


def headers(stage, opacity=1):
    for x, p in zip(COLUMNS, PRIMES):
        fit(stage, "Twos" if p == 2 else "Threes", x, 188, 31, 265, PRIME_COLOURS[p], opacity)
    stage.line([(730, 170), (730, 498)], RIM, 2, opacity)


def source_rows(stage, top=1, bottom=1, *, selection=None, ys=(281, 402)):
    row(stage, ORIGINAL[0], ys[0], "12", top, selection=selection)
    row(stage, ORIGINAL[1], ys[1], "18", bottom, selection=selection)
    stage.line([(156, sum(ys) / 2), (1076, sum(ys) / 2)], RIM, 2, bottom)


def sort_copies(stage, s):
    stage.heading("Group copies of the same prime")
    align = s.reveal("group copies of the same prime", 1.05)
    headers(stage, align)
    origins = (504, 642, 780)
    for i, (label, y, values, xs, cue) in enumerate((
            ("12", 281, (2, 2, 3), (518, 596, 863), "write twelve"),
            ("18", 402, (2, 3, 3), (518, 863, 941), "write eighteen"))):
        arrive = s.reveal(cue)
        fit(stage, label, 234, y, 48, 190, WHITE, arrive)
        for j, (value, x) in enumerate(zip(values, xs)):
            prime(stage, mix(origins[j], x, align), y, value, s.reveal(cue, offset=0.35 + j * 0.21), 66)
    fit(stage, "Count each column separately", 640, 542, 36, 1000, MINT,
        s.reveal("how many of each prime"))


def condition_preview(stage, s):
    stage.heading("Three questions, two prime columns")
    headers(stage)
    source_rows(stage, ys=(246, 320))
    for i, (label, sub, colour, cue) in enumerate((
            ("Common factor", "Fits inside both rows", BLUE, "to divide into both"),
            ("Common multiple", "Has enough for either row", GOLD, "a common multiple"),
            ("Square", "Two matching sets", MINT, "for a square"))):
        x = 315 + i * 325
        show = s.reveal(cue)
        tile(stage, x, 459, label, colour, 299, 73, show, size=28)
        fit(stage, sub, x, 532, 26, 299, colour, show, False)


def hcf_lcm_problem(stage, s):
    stage.heading("Compare 12 and 18")
    headers(stage)
    source_rows(stage, ys=(255, 331))
    for y, question, colour, cue in (
            (454, "Largest number that divides both?", BLUE, "find the largest"),
            (530, "Smallest positive multiple of both?", GOLD, "then find the smallest")):
        fit(stage, question, 640, y, 36, 1120, colour, s.reveal(cue))


def common_factor(stage, s):
    stage.heading("Keep only the copies they share")
    headers(stage)
    twos = s.reveal("eighteen can supply one two")
    threes = s.reveal("twelve can supply one three")
    for counts, yy, label in zip(ORIGINAL, (254, 332), ("12", "18")):
        fit(stage, label, 234, yy, 39, 270)
        for i, (p, x, count) in enumerate(zip(PRIMES, COLUMNS, counts)):
            for j in range(count):
                fade = twos if p == 2 else threes
                prime(stage, x + 39 * (2 * j - 1), yy, p, 1 if j == 0 else 1 - 0.78 * fade, 64)
    for x, p, present in zip((518, 863), PRIMES, (twos, threes)):
        join(stage, x, 282, 305, PRIME_COLOURS[p], present)
        slide = s.reveal("the smaller counts", 0.84, 0.15 if p == 3 else 0)
        if slide > 0:
            prime(stage, mix(x, 535 if p == 2 else 745, slide), mix(362, 464, slide), p, slide, 71)
    fit(stage, "2 × 3 = 6", 640, 560, 48, 800, MINT, s.reveal("which is six"))


def common_multiple(stage, s):
    stage.heading("Use enough copies for each row")
    headers(stage)
    source_rows(stage, ys=(249, 328))
    for i, (x, p, words, source_y) in enumerate(
            zip(COLUMNS, PRIMES, ("twelve needs two twos", "eighteen needs two threes"), (249, 328))):
        show = s.reveal(words)
        stage.box(x - 86, source_y - 34, 172, 68, fill=None, edge=PRIME_COLOURS[p], opacity=show)
        move = s.reveal("take the larger count", 0.9, i * 0.14)
        for j in range(2):
            original = x + 39 * (2 * j - 1)
            final = 463 + 114 * (2 * i + j)
            prime(stage, mix(original, final, move), mix(source_y, 459, move), p, move, 70)
    fit(stage, "2² × 3² = 36", 640, 556, 49, 1010, MINT, s.reveal("multiply to thirty-six"))


def same_total(stage, s):
    stage.heading("The total prime counts stay fixed")
    colours = (BLUE, GOLD)
    new = s.reveal("so the factors of six")
    for i, (x, p, original) in enumerate(zip((419, 862), PRIMES, ("2 + 1", "1 + 2"))):
        prime(stage, x, 208, p, width=70)
        fit(stage, original, x, 307, 42, 335, colours[i])
        stage.arrow((x, 340), (x, 401), MUTED, new, 3)
        fit(stage, "1 + 2", x, 451, 44, 335, MINT, new)
    fit(stage, "12 × 18  =  6 × 36  =  216", 640, 560, 47, 1090, MINT,
        s.reveal("both products are"))


def paired_square(stage, s):
    change = s.reveal("forty-eight has four twos")
    if change < 0.5:
        stage.heading("36 has two matching groups")
        for i, value in enumerate((2, 3)):
            x = 555 + 180 * i
            for y in (266, 423):
                prime(stage, x, y, value, width=90)
            join(stage, x, 305, 385, PRIME_COLOURS[value])
        for y in (266, 423):
            fit(stage, "6", 886, y, 43, 210, MINT, s.reveal("two sixes"))
        fit(stage, "6 × 6 = 36", 640, 568, 44, 800, MINT, s.reveal("two sixes"))
        return
    stage.heading("48 needs another three", opacity=change)
    fit(stage, "48 = 2⁴ × 3", 640, 183, 37, 850, WHITE, change)
    filled = s.reveal("multiply by another three", 0.95)
    for i, value in enumerate((2, 2, 3)):
        x = 462 + 174 * i
        prime(stage, x, 276, value, change, 75)
        join(stage, x, 308, 390, PRIME_COLOURS[value], change if value == 2 else max(0.25, filled))
        if value == 2:
            prime(stage, x, 419, value, change, 75)
        else:
            stage.box(x - 38, 389, 76, 60, fill=None, edge=GOLD, opacity=change * (1 - filled))
            prime(stage, mix(1060, x, filled), 419, 3, filled, 75)
    fit(stage, "48 × 3 = 144 = 12²", 640, 561, 48, 1090, MINT,
        s.reveal("one hundred and forty-four"))


def conditions_recap(stage, s):
    if s.reveal("in your notebook"):
        stage.heading("Compare 20 and 30")
        for i, (value, factors) in enumerate(((20, (2, 2, 5)), (30, (2, 3, 5)))):
            y = 258 + i*109
            fit(stage, str(value), 326, y, 50, 200)
            for j, p in enumerate(factors):
                prime(stage, 525+j*139, y, p, s.reveal("twenty and thirty", offset=i*.22+j*.15), 79)
        fit(stage, "Which copies fit both rows? Which cover both?", 640, 541, 34, 1120, MINT,
            s.reveal("twenty and thirty"))
        return
    stage.heading("Compare the copies prime by prime")
    headers(stage)
    source_rows(stage, ys=(247, 333))
    smaller = s.reveal("use the smaller")
    larger = s.reveal("use the larger")
    fit(stage, "HCF   2 × 3 = 6", 365, 469, 37, 520, BLUE, smaller)
    fit(stage, "LCM   2² × 3² = 36", 887, 469, 37, 535, GOLD, larger)
    fit(stage, "36 = (2 × 3) × (2 × 3)", 640, 552, 37, 960, MINT,
        s.reveal("a square has even counts"))


def missing_number(stage, s):
    stage.heading("Make 90 into a perfect square")
    tile(stage, 360, 325, 90, WHITE, 155, 105, size=58)
    fit(stage, "×", 513, 325, 49, 100, MUTED)
    tile(stage, 652, 325, "?", GOLD, 153, 105, size=57)
    fit(stage, "=", 784, 325, 49, 100, MUTED)
    stage.box(886, 230, 190, 190, fill="#24383d", edge=MINT, radius=8, stroke=3)
    fit(stage, "square", 981, 325, 38, 170, MINT)
    fit(stage, "What is the smallest positive multiplier?", 640, 554, 37, 1080, WHITE)


def ninety_pairs(stage, s):
    stage.heading("Give every prime a partner")
    fit(stage, "90 = 2 × 3 × 3 × 5", 640, 180, 40, 980, WHITE, s.reveal("ninety factorises"))
    grouped = s.reveal("each prime needs an even number")
    for i, value in enumerate((2, 3, 5)):
        x = 401 + 239 * i
        prime(stage, x, 303, value, s.reveal("two times three", offset=i * 0.29), 90)
        joined = s.reveal("the threes already make") if value == 3 else 0.29 * grouped
        join(stage, x, 339, 418, PRIME_COLOURS[value], joined)
        if value == 3:
            prime(stage, x, 454, value, joined, 90)
        else:
            show = s.reveal("put a space")
            stage.box(x - 45, 418, 90, 72, fill=None, edge=PRIME_COLOURS[value], opacity=show, stroke=3)
            fit(stage, "?", x, 454, 35, 70, PRIME_COLOURS[value], show)
    fit(stage, "The 2 and the 5 are unpaired", 640, 570, 37, 1050, GOLD,
        s.reveal("the two and the five each appear"))


def add_missing_partners(stage, s):
    stage.heading("Add just the two missing tiles")
    for i, value in enumerate((2, 3, 5)):
        x = 398 + 240 * i
        colour = PRIME_COLOURS[value]
        prime(stage, x, 272, value, width=80)
        join(stage, x, 305, 388, colour)
        if value == 3:
            prime(stage, x, 420, value, width=80)
        else:
            move = s.reveal("supply one more two" if value == 2 else "and one more five", 1.0)
            stage.box(x - 40, 388, 80, 64, edge=colour, fill=None, opacity=1 - move)
            prime(stage, mix(174 if value == 2 else 1106, x, move),
                  mix(449, 420, move), value, move, 80)
    fit(stage, "New tiles give 2 × 5 = 10", 640, 560, 44, 1080, MINT,
        s.reveal("their product is ten"))


def two_thirties(stage, s):
    stage.heading("Check that 900 is a square")
    separation = s.reveal("split its tiles", 0.9)
    for i, sign in enumerate((-1, 1)):
        x = 640 + sign * mix(124, 252, separation)
        stage.box(x - 199, 229, 398, 175, fill=None, edge=RIM, opacity=separation)
        for j, value in enumerate((2, 3, 5)):
            prime(stage, x + (j - 1) * 92, 285 + i * 55 * (1 - separation), value,
                  s.reveal("split its tiles"), 75)
        fit(stage, "2 × 3 × 5 = 30", x, 365, 37, 385, MINT, s.reveal("each group multiplies to thirty"))
    fit(stage, "90 × 10 = 900", 640, 180, 39, 980, WHITE, s.reveal("is nine hundred"))
    square = s.reveal("so the new number is a square")
    fit(stage, "30 × 30 = 900", mix(640, 494, square), 535, 53, 820, MINT,
        s.reveal("thirty times thirty"))
    # Each fine interval represents one unit. Heavy lines separate blocks of ten.
    if square:
        left, top, side = 896, 429, 150
        stage.box(left, top, side, side, radius=0, fill="#284b49", edge=MINT, opacity=square)
        for k in range(31):
            delta = k * side / 30
            colour = MINT if k % 10 == 0 else RIM
            width = 2 if k % 10 == 0 else 1
            stage.line([(left+delta, top), (left+delta, top+side)], colour, width, square)
            stage.line([(left, top+delta), (left+side, top+delta)], colour, width, square)
        fit(stage, "30", left+side/2, 604, 27, 140, MINT, square)
        fit(stage, "30", 1092, top+side/2, 27, 80, MINT, square)


def minimum_multiplier(stage, s):
    stage.heading("Why 10 is the smallest")
    xs = [330 + i * 88 for i in range(10)]
    number_line = s.reveal("could a smaller positive multiplier")
    rail(stage, xs, 473, tuple(str(i) for i in range(1, 11)), opacity=number_line)
    for value, y, colour, cue in (
            (2, 293, BLUE, "must supply a two"),
            (5, 381, MINT, "and a five")):
        show = s.reveal(cue)
        fit(stage, f"Multiples of {value}", 178, y, 27, 220, colour, show)
        for n in range(value, 11, value):
            x = xs[n - 1]
            stage.dot(x, y, 18, colour, show)
            join(stage, x, y + 20, 464, colour, 0.47 * show)
    both = s.reveal("ten is the first")
    stage.box(xs[-1] - 30, 255, 60, 269, fill=None, edge=GOLD, opacity=both, stroke=3)
    fit(stage, "The first multiplier in both rows is 10", 640, 584, 33, 1080, GOLD, both)


def partners_recap(stage, s):
    exercise = s.reveal("try the same proof with sixty")
    stage.heading("Which partners does 60 need?" if exercise else "Pair the prime pieces of 90")
    groups = ((2, 2), (3, 1), (5, 1)) if exercise else ((2, 1), (3, 2), (5, 1))
    show = s.reveal("try the same proof with sixty") if exercise else s.reveal("pair every prime")
    for i, (p, count) in enumerate(groups):
        x = 399 + i*241
        prime(stage, x, 269, p, show, 86)
        if count == 2:
            prime(stage, x, 406, p, show, 86)
            join(stage, x, 306, 373, PRIME_COLOURS[p], show)
        else:
            appear = s.reveal("choose one partner") if not exercise else show
            stage.box(x-42, 374, 84, 64, fill=None, edge=GOLD, opacity=appear)
            fit(stage, "?", x, 406, 30, 60, GOLD, appear)
    if exercise:
        fit(stage, "Smallest multiplier for 60?", 640, 542, 41, 1000, WHITE,
            s.reveal("smallest positive whole number"))
    else:
        fit(stage, "Missing partners for 90     2 × 5", 640, 542, 38, 1000, MINT,
            s.reveal("whose count is odd"))


SCENES = {
    "T04.3": (sort_copies, condition_preview, hcf_lcm_problem, common_factor, common_multiple,
              same_total, paired_square, conditions_recap),
    "T04.E": (missing_number, ninety_pairs, add_missing_partners, two_thirties, minimum_multiplier,
              partners_recap),
}
