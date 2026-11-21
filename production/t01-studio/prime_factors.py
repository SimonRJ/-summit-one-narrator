"""Build and count prime factorizations using trees, factor pairs and choice grids."""

from stage import BLUE, GOLD, MINT, MUTED, RED, RIM, WHITE, mix
from studio_diagrams import fit, prime, tile


def branch(stage, x, y, xs, lower, amount):
    for i, child in enumerate(xs):
        stage.arrow((x + (i * 2 - 1) * 12, y + 28), (child, lower - 35), RIM, amount)


def tree(stage, center, middle, factors, ends, arranged=0.0, *, top=208):
    branches = (center - 137, center + 137)
    leaves = [x + delta for x in branches for delta in (-56, 56)]
    ys = (top, top + 116, top + 249)
    tile(stage, center, ys[0], 60, WHITE, 98, 57, size=33)
    branch(stage, center, ys[0], branches, ys[1], middle)
    for x, factor in zip(branches, factors):
        tile(stage, x, ys[1], factor, MUTED, 83, 57, middle)
    for group, amount in enumerate(ends):
        branch(stage, branches[group], ys[1], leaves[2 * group:2 * group + 2], ys[2],
               amount * (1 - arranged))
    values = {6: (2, 3), 10: (2, 5), 4: (2, 2), 15: (3, 5)}
    numbers = [p for factor in factors for p in values[factor]]
    order = sorted(range(4), key=lambda i: numbers[i])
    for i, (x, value) in enumerate(zip(leaves, numbers)):
        target = center + (order.index(i) - 1.5) * 82
        prime(stage, mix(x, target, arranged), ys[2] + arranged * 29, value, ends[i // 2], 65)


def first_tree(stage, s):
    stage.heading("Break a number into primes")
    start = s.reveal("take sixty")
    definition = (1 - start) * s.reveal("a prime has exactly two")
    for x, name in ((491, "1"), (789, "itself")):
        tile(stage, x, 370, name, BLUE, 218, 89, definition, size=40)
    fit(stage, "The two positive factors of a prime", 640, 270, 38, 1000, WHITE, definition)
    if start:
        middle = s.reveal("split it into six")
        bottom = s.reveal("then split those again")
        # The first tree enters after the definition clears.
        if start > 0.2:
            tree(stage, 640, middle, (6, 10), (bottom, bottom), top=210)
        fit(stage, "2 × 3 × 2 × 5", 640, 555, 48, 680, MINT, s.reveal("two and five"))


def same_primes(stage, s):
    stage.heading("Different starts, same primes")
    arrange = s.reveal("rearrange the pieces", 0.95)
    tree(stage, 327, 1, (6, 10), (1, 1), arrange, top=197)
    tree(stage, 953, s.reveal("four times fifteen"), (4, 15),
         (s.reveal("four gives two twos"), s.reveal("fifteen gives")), arrange, top=197)
    stage.line([(640, 196), (640, 525)], RIM, 2)
    fit(stage, "2² × 3 × 5", 640, 572, 42, 600, MINT, s.reveal("the same list"))


def prime_question(stage, s):
    stage.heading("Is 91 prime?")
    stage.box(388, 219, 504, 256, edge=RIM, fill=None, stroke=3)
    for x, y in ((640, 190), (934, 348)):
        tile(stage, x, y, "?", GOLD, 70, 57, size=34)
    fit(stage, "91", 640, 346, 86, 250)
    fit(stage, "How far do you need to check?", 640, 537, 35, 910, BLUE,
        s.reveal("how far the search"))


def prime_tests(stage, s):
    stage.heading("Test small primes for 91")
    lines = (
        (2, "91 is odd", "ninety-one is odd"),
        (3, "9 + 1 = 10", "its digits add to ten"),
        (5, "Ends in 1", "its last digit"),
        (7, "7 × 13 = 91", "try seven"),
    )
    for i, (value, reason, cue) in enumerate(lines):
        y = 227 + i * 93
        visible = s.reveal(cue)
        prime(stage, 175, y, value, visible, 66)
        fit(stage, reason, 355, y, 33, 265, MINT if i == 3 else MUTED, visible)
        stage.line([(113, y + 42), (481, y + 42)], RIM, 2, visible)
        if i < 3:
            fit(stage, "×", 462, y, 36, 35, RED, visible)
    build = s.reveal("seven times thirteen", 1.15)
    for row in range(7):
        for col in range(13):
            opacity = max(0.0, min(1.0, build * 7.8 - row))
            x, y = 594 + 43 * col, 244 + 40 * row
            stage.box(x, y, 35, 32, fill="#284b49", edge=MINT, radius=4, opacity=opacity)
    stage.bracket(594, 1145, 523, "13 columns", MINT, build)
    fit(stage, "7 rows", 873, 204, 29, 260, MINT, build)
    fit(stage, "91 is composite", 872, 581, 36, 600, MINT, s.reveal("ninety-one is composite"))


def square_root_limit(stage, s):
    stage.heading("Stop at the square root")
    over = 1 - s.reveal("for ninety-seven")
    fit(stage, "Both factors > √n", 640, 235, 49, 1020, GOLD, over)
    draw = s.reveal("multiplying them would give too much")
    tile(stage, 478, 342, "> √n", GOLD, 233, 81, over * draw)
    tile(stage, 805, 342, "> √n", GOLD, 233, 81, over * draw)
    fit(stage, "×", 640, 342, 42, 85, WHITE, over * draw)
    fit(stage, "Product > n", 640, 448, 45, 800, RED, over * draw)
    fit(stage, "A composite number has a prime factor ≤ √n", 640, 545, 35, 1060, MINT,
        over * s.reveal("a composite number has a prime factor"))
    show = 1 - over
    fit(stage, "9² = 81     <     97     <     100 = 10²", 640, 233, 44, 1110, BLUE, show)
    fit(stage, "Prime candidates up to √97", 640, 320, 30, 930, MUTED, show)
    test = s.reveal("try two three five and seven", 1.3)
    remains = s.reveal("all leave a remainder")
    for i, (value, left) in enumerate(((2, 1), (3, 1), (5, 2), (7, 6))):
        x = 314 + 217 * i
        prime(stage, x, 410, value, max(0.0, min(1.0, test * 4.5 - i)), 76)
        fit(stage, f"Remainder {left}", x, 482, 27, 205, GOLD, remains)
    fit(stage, "97 is prime", 640, 568, 45, 720, MINT, s.reveal("ninety-seven is prime"))


def distribute_sixty_six(stage, s):
    stage.heading("Three distinct numbers multiply to 66")
    fit(stage, "Each number is greater than 1", 640, 157, 30, 1000, MUTED)
    show = s.reveal("sixty-six has exactly three")
    fit(stage, "66 = 2 × 3 × 11", 640, 233, 45, 900, WHITE, show)
    for i, value in enumerate((2, 3, 11)):
        x = 350 + 290 * i
        stage.box(x - 105, 385, 210, 130, edge=RIM, fill=None, stroke=3)
        arrow = s.reveal("each of the three numbers needs a piece", 1.1, i * 0.14)
        stage.arrow((x, 348), (x, 388), MINT, arrow)
        slide = s.reveal("each gets exactly one", 0.8, i * 0.12)
        prime(stage, x, mix(321, 451, slide), value, show, 81)
    fit(stage, "One prime per number", 640, 570, 35, 890, MINT, s.reveal("those three primes"))


def factor_recap(stage, s):
    if s.reveal("in your notebook"):
        stage.heading("Build a factor tree for 84")
        tile(stage, 640, 205, 84, WHITE, 120, 66, size=40)
        show = s.reveal("write eighty-four")
        branch(stage, 640, 205, (463, 817), 365, show)
        for x in (463, 817):
            tile(stage, x, 365, "?", GOLD, 115, 65, show)
        fit(stage, "Keep splitting until every leaf is prime.", 640, 535, 38, 1060,
            MINT, s.reveal("as a product of primes"))
        return
    stage.heading("Prime pieces and prime tests")
    tree(stage, 335, 1, (6, 10), (1, 1), top=177)
    test = s.reveal("when you test")
    fit(stage, "97", 924, 199, 54, 280, WHITE, test)
    fit(stage, "9² < 97 < 10²", 924, 275, 37, 475, BLUE, test)
    limit = s.reveal("up to its square root", 0.8)
    for i, value in enumerate((2, 3, 5, 7)):
        prime(stage, 763+i*107, 371, value, min(1, max(0, limit*4-i)), 73)
    fit(stage, "1 has just one positive factor.", 640, 557, 34, 1050,
        GOLD, s.reveal("one has only one"))


def pair_chart(stage, s, pairs, cues, *, y=243, step=81, x=640):
    for i, ((first, second), cue) in enumerate(zip(pairs, cues)):
        opacity = s.reveal(cue)
        yy = y + step * i
        highlight = first == second
        colour = MINT if highlight else BLUE
        if highlight:
            tile(stage, x, yy, first, MINT, 84, 57, opacity)
        else:
            for shift, value in ((-144, first), (144, second)):
                tile(stage, x + shift, yy, value, colour, 88, 57, opacity)
            fit(stage, "×", x, yy, 34, 80, MUTED, opacity)


def twelve_pairs(stage, s):
    stage.heading("How many factors does 12 have?")
    for i, (val, cue) in enumerate(((1, "one two three four"), (2, "two three four six"),
                                    (3, "three four six and twelve"), (4, "four six and twelve"),
                                    (6, "six and twelve"), (12, "and twelve"))):
        tile(stage, 315 + 130 * i, 204, val, MINT, 98, 59, s.reveal(cue))
    pair_chart(stage, s, ((1, 12), (2, 6), (3, 4)),
               ("finding the products", "finding the products", "finding the products"), y=323, step=80)
    fit(stage, "Each pair multiplies to 12", 640, 584, 33, 920, BLUE, s.reveal("products that make twelve"))


def preview_360(stage, s):
    stage.heading("Count with prime powers")
    fit(stage, "360 = 2³ × 3² × 5", 640, 240, 62, 1030, WHITE, s.reveal("two cubed"))
    for i, (label, colour) in enumerate((("Copies of 2", BLUE), ("Copies of 3", GOLD), ("Copies of 5", MINT))):
        tile(stage, 325 + i * 315, 387, label, colour, 270, 81, s.reveal("three small counts", offset=i * 0.24))
    fit(stage, "24 positive factors", 640, 531, 41, 980, MINT, s.reveal("twenty-four entries"))


def twelve_choices(stage, s):
    stage.heading("Build factors of 12")
    for i, value in enumerate((2, 2, 3)):
        prime(stage, 458 + i * 182, 307, value, s.reveal("two times two times three", offset=i * 0.27), 112)
    stage.bracket(402, 694, 397, "How many twos?", BLUE, s.reveal("how many twos"))
    stage.bracket(764, 880, 397, "And threes?", GOLD, s.reveal("choices for the three"))
    fit(stage, "How many different products?", 640, 550, 39, 1050, MINT,
        s.reveal("how many different products"))


def choice_grid(stage, two_max, three_max, two, three, fill, *, emphasis=None, y=277):
    row_height = 64
    col_width = 171
    xs = [707 + (j - three_max / 2) * col_width for j in range(three_max + 1)]
    left = xs[0] - 81
    fit(stage, "Number of threes", 707, y - 103, 28, 530, GOLD, three)
    fit(stage, "Twos", left - 106, y - 50, 29, 140, BLUE, two)
    for j, x in enumerate(xs):
        fit(stage, str(j), x, y - 49, 35, 150, GOLD, three)
    for i in range(two_max + 1):
        yy = y + row_height * i
        opacity = max(0.0, min(1.0, two * (two_max + 1.6) - i))
        fit(stage, str(i), left - 106, yy, 36, 110, BLUE, opacity)
        for j, x in enumerate(xs):
            appear = max(0.0, min(1.0, fill * (two_max + 1.7) - i))
            accent = emphasis == (i, j)
            stage.box(x - 77, yy - 27, 154, 54, fill=None, edge=MINT if accent else RIM, opacity=three * opacity)
            fit(stage, str(2 ** i * 3 ** j), x, yy, 33, 150, MINT if accent else WHITE, appear)


def twelve_grid(stage, s):
    stage.heading("One product in every cell")
    use_none = s.reveal("taking no tiles")
    use_all = s.reveal("taking all the tiles")
    emphasis = (2, 1) if use_all > 0.5 else (0, 0) if use_none > 0.5 else None
    choice_grid(stage, 2, 1, s.reveal("use zero one or two twos", 1.0),
                s.reveal("either include the three"), s.reveal("three times two", 1.25), emphasis=emphasis)
    fit(stage, "3 × 2 = 6 factors", 640, 550, 49, 970, MINT, s.reveal("six products"))


def seventy_two_grid(stage, s):
    change = s.reveal("for three hundred and sixty", 0.68)
    if change < 0.5:
        stage.heading("72 = 2³ × 3²")
        choice_grid(stage, 3, 2, s.reveal("choose zero one two or three twos", 1.25),
                    s.reveal("three possibilities"), s.reveal("four times three", 1.4), y=265)
        fit(stage, "4 × 3 = 12 factors", 640, 566, 45, 950, MINT, s.reveal("twelve factors"))
    else:
        stage.heading("360 = 2³ × 3² × 5")
        tile(stage, 416, 329, "12 without 5", BLUE, 335, 96, change, size=40)
        tile(stage, 862, 329, "12 with 5", GOLD, 335, 96, change, size=40)
        fit(stage, "12 × 2 = 24 factors", 640, 522, 52, 1030, MINT, s.reveal("doubles that count"))


def square_pairs(stage, s):
    stage.heading("Why a square has an odd factor count")
    cues = ("one and thirty-six", "two and eighteen", "three and twelve", "four and nine", "six pairs with itself")
    pair_chart(stage, s, ((1, 36), (2, 18), (3, 12), (4, 9), (6, 6)), cues, y=207, step=75, x=374)
    self_pair = s.reveal("six pairs with itself")
    for i in range(6):
        for j in range(6):
            stage.box(725 + 43 * j, 239 + 43 * i, 38, 38, radius=4, edge=MINT,
                      fill="#284b49", opacity=self_pair)
    stage.bracket(725, 978, 517, "6 columns", MINT, self_pair)
    fit(stage, "6 rows", 1054, 361, 30, 143, MINT, self_pair)
    fit(stage, "2 × 4 + 1 = 9 factors", 640, 596, 37, 1040, MINT,
        s.reveal("an odd count"))


def count_recap(stage, s):
    if s.reveal("in your notebook"):
        stage.heading("How many factors does 200 have?")
        fit(stage, "200 = 2³ × 5²", 640, 199, 48, 880, WHITE,
            s.reveal("two hundred"))
        show = s.reveal("then explain why")
        fit(stage, "Copies of 5", 755, 276, 29, 445, GOLD, show)
        fit(stage, "Copies of 2", 420, 364, 26, 205, BLUE, show)
        for row in range(4):
            fit(stage, str(row), 552, 362+48*row, 28, 64, BLUE, show)
            for col in range(3):
                x = 590+112*col
                stage.box(x, 340+48*row, 101, 42, fill=None, edge=RIM, opacity=show)
                if not row:
                    fit(stage, str(col), x+50, 315, 27, 60, GOLD, show)
        fit(stage, "Fill one product in each cell.", 640, 577, 32, 990, MINT, show)
        return
    stage.heading("Two independent prime choices")
    fit(stage, "12 = 2² × 3", 640, 185, 43, 850)
    choice_grid(stage, 2, 1, s.reveal("for each prime"), s.reveal("zero copies"),
                s.reveal("multiply the resulting"), y=340)
    fit(stage, "(2 + 1) × (1 + 1) = 6", 640, 554, 40, 990, MINT,
        s.reveal("multiply the resulting"))


SCENES = {
    "T04.1": (first_tree, same_primes, prime_question, prime_tests, square_root_limit,
              distribute_sixty_six, factor_recap),
    "T04.2": (twelve_pairs, preview_360, twelve_choices, twelve_grid, seventy_two_grid,
              square_pairs, count_recap),
}
