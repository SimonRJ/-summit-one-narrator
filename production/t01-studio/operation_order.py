"""Chapter 2 films about how operation order changes the output."""

import math

from order_bars import compare_orders, double_sum

from stage import BLUE, GOLD, MINT, MUTED, RED, RIM, WHITE, between, blend, mix
from studio_diagrams import fit, join, rail, recap, table, tile


def machine(stage, y, label, nodes, cues):
    xs = (230, 430, 630, 830, 1030)
    fit(stage, label, 109, y, 22, 140, MUTED, cues[0])
    for i, (x, node, opacity) in enumerate(zip(xs, nodes, cues)):
        colour = GOLD if node.startswith(("+", "−")) else MINT if node.startswith("×") else BLUE
        tile(stage, x, y, node, colour, 112, 63, opacity)
        if i:
            stage.arrow((xs[i - 1] + 63, y), (x - 63, y), RIM, opacity, 2.3)


def start_three(stage, s):
    stage.heading("The order can change the output")
    a = s.reveal("start with three")
    add = s.reveal("add two and then double")
    first = s.reveal("five becomes ten", 0.54)
    b = s.reveal("try the same start")
    twice = s.reveal("double three first")
    last = s.reveal("six becomes eight")
    machine(stage, 274, "Add first", ("3", "+2", "5", "×2", "10"), (a, add, add, first, first))
    machine(stage, 420, "Double first", ("3", "×2", "6", "+2", "8"), (b, twice, twice, last, last))
    fit(stage, "Same start. Different results.", 640, 550, 37, colour=MINT,
        opacity=s.reveal("the same steps can give"))


def every_input(stage, s):
    stage.heading("One model for every starting number")
    testing = s.reveal("testing more starting numbers")
    general = s.reveal("a letter lets us explain", 0.85)
    compare = s.reveal("we'll compare the two operation orders")
    for i, n in enumerate(("0", "4", "10")):
        x = 307 + 333 * i
        tile(stage, mix(x, 640, general), mix(274, 320, general), n, BLUE,
             126, 79, testing * (1 - general))
    tile(stage, 640, 320, "x", MINT, 126, 88, general, size=48)
    for x, name in ((408, "Order A"), (872, "Order B")):
        stage.arrow((640, 374), (x, 445), RIM, compare, 3)
        fit(stage, name, x, 482, 30, colour=WHITE, opacity=compare)


def question(stage, s, *, add, multiply, word):
    stage.heading("Which gives the greater result?")
    intro = between(s.t, s.start + 0.25)
    a = s.reveal(f"{word} a adds")
    b = s.reveal(f"{word} b multiplies" if word == "rule" else "order b doubles")
    a_nodes = ("x", f"+{add}", "x + " + str(add), f"×{multiply}", "?")
    b_nodes = ("x", f"×{multiply}", f"{multiply}x", f"+{add}", "?")
    machine(stage, 259, f"{word.title()} A", a_nodes, (intro, a, a, a, a))
    machine(stage, 405, f"{word.title()} B", b_nodes, (intro, b, b, b, b))
    fit(stage, "How much greater?", 640, 540, 40, colour=MINT,
        opacity=s.reveal("which output is larger" if word == "rule" else "which order gives"))


def question_five(stage, s):
    question(stage, s, add=5, multiply=2, word="order")


def question_three(stage, s):
    question(stage, s, add=3, multiply=4, word="rule")


def copy_total(stage, s, *, copies, added, first_cue, copy_cue, total_cue, word):
    stage.heading(f"{word} A scales the added amount")
    first = s.reveal(first_cue)
    start = s.at(copy_cue)
    stage.text("One whole input bar", 640, 197, 25, MUTED, opacity=first)
    tile(stage, 591, 253, "x", BLUE, 118, 69, first)
    tile(stage, 691, 253, added, GOLD, 70, 69, first)
    for i in range(copies):
        x = 640 + (i - (copies - 1) / 2) * 236
        p = between(s.t, start + i * 0.22, 0.72)
        y = mix(253, 397, p) - 13 * math.sin(math.pi * p)
        tile(stage, mix(591, x - 39, p), y, "x", BLUE, 118, 67, p)
        tile(stage, mix(691, x + 61, p), y, added, GOLD, 70, 67, p)
    result = s.reveal(total_cue)
    stage.terms([(f"{copies}x", BLUE, result), ("+", WHITE, result),
                 (str(copies * added), GOLD, result)], 540, 57)


def copy_five(stage, s):
    double_sum(stage, s)


def copy_three(stage, s):
    copy_total(stage, s, copies=4, added=3, first_cue="rule a forms x plus three",
               copy_cue="makes four copies", total_cue="so the result is four x", word="Rule")


def copy_start_only(stage, s):
    stage.heading("Rule B scales the starting value")
    start = s.at("make four copies of x")
    added = s.reveal("now add the three")
    for i in range(4):
        p = between(s.t, start + i * 0.18, 0.7)
        x = 333 + i * 154
        tile(stage, mix(640, x, p), mix(237, 380, p), "x", BLUE, 124, 72, p)
    tile(stage, 1003, mix(238, 380, added), 3, GOLD, 85, 72, added)
    result = s.reveal("the result is four x plus three")
    stage.terms([("4x", BLUE, result), ("+", WHITE, result), ("3", GOLD, result)], 542, 58)


def compare_outputs(stage, s, *, copies, added, match, result, b=1.0, added_b=1.0, word="Order"):
    stage.heading("Match the common parts")
    if copies == 2:
        x_parts = (359, 500)
        add_parts = (700, 851)
    else:
        x_parts = (284, 411, 538, 665)
        add_parts = (796, 895, 994, 1093)
    fading = 1 - 0.70 * match
    fit(stage, word + " A", 133, 268, 26, 150, MUTED)
    fit(stage, word + " B", 133, 416, 26, 150, MUTED, b)
    for x in x_parts:
        tile(stage, x, 268, "x", BLUE, 110, 66, fading)
        tile(stage, x, 416, "x", BLUE, 110, 66, b * fading)
        join(stage, x, 309, 378, BLUE, match * 0.75)
    for i, x in enumerate(add_parts):
        tile(stage, x, 268, added, GOLD, 80, 66, fading if i == 0 else 1.0)
    tile(stage, add_parts[0], 416, added, GOLD, 80, 66, added_b * fading)
    join(stage, add_parts[0], 309, 378, GOLD, match * 0.72)
    stage.bracket(add_parts[1] - 42, add_parts[-1] + 42, 336, f"{(copies - 1) * added} extra", MINT, result)
    fit(stage, f"{word} A is greater by {(copies - 1) * added}.", 640, 550, 43, colour=MINT,
        opacity=result)


def compare_five(stage, s):
    compare_orders(stage, s)


def compare_three(stage, s):
    compare_outputs(stage, s, copies=4, added=3, match=s.reveal("pair those tiles"),
                    result=s.reveal("their total is nine"), word="Rule")


def negative(stage, s):
    stage.heading("Change the multiplier to negative two")
    first = s.reveal("its contribution is negative ten")
    second = s.reveal("order b still adds positive five")
    same = s.reveal("the common part is negative two x")
    difference = s.reveal("positive five is fifteen more")
    fit(stage, "Order A", 268, 234, 27, colour=MUTED, opacity=first)
    fit(stage, "Order B", 268, 322, 27, colour=MUTED, opacity=second)
    tile(stage, 492, 234, "−2x", BLUE, 151, 61, first * (1 - 0.62 * same))
    tile(stage, 492, 322, "−2x", BLUE, 151, 61, second * (1 - 0.62 * same))
    join(stage, 492, 269, 290, BLUE, same)
    tile(stage, 742, 234, "−10", RED, 145, 61, first)
    tile(stage, 742, 322, "+5", GOLD, 145, 61, second)
    x = [326 + i * 42 for i in range(16)]
    rail(stage, x, 461, ["−10", *[""] * 9, "0", *[""] * 4, "+5"], opacity=difference)
    stage.arrow((x[0], 438), (x[-1], 438), MINT, difference, 4)
    fit(stage, "Order B is greater by 15.", 640, 572, 42, colour=MINT, opacity=difference)


def reorder(stage, s):
    stage.heading("When can the steps swap?")
    variants = (
        (268, "+2", "+5", "+7", "two additions can swap", "we still add the same total", GOLD),
        (413, "×2", "×3", "×6", "two multiplications can swap", "their combined scale", MINT),
    )
    for y, left, right, result, intro, done, colour in variants:
        p = s.reveal(intro)
        u = s.reveal(done, 0.92)
        for a, b, lift, label in ((385, 606, -27, left), (606, 385, 27, right)):
            tile(stage, mix(a, b, u), y + lift * math.sin(math.pi * u), label, colour,
                 130, 65, p)
        stage.arrow((704, y), (825, y), RIM, u, 3)
        tile(stage, 946, y, result, colour, 148, 75, u)
    fit(stage, "Track what the multiplication scales.", 640, 554, 37, colour=WHITE,
        opacity=s.reveal("when you mix the two types"))


def recap_five(stage, s):
    recap(stage, s, (("Label the start", "give the start a letter"),
                     ("Write both orders", "write the two orders"),
                     ("Compare the parts", "compare the parts")),
          "in your notebook",
          ("Subtract 4, then multiply by 3.", "Multiply by 3, then subtract 4.",
           "Which is greater, and by how much?"), sub="Use the same starting number for both.")


def examples_three(stage, s):
    stage.heading("Check two different inputs")
    zero = s.reveal("starting from zero gives")
    ten = s.reveal("starting from ten gives")
    gap = s.reveal("each difference is nine")
    rows = (("Start", "Rule A", "Rule B", "Difference"),
            tuple(v if p > 0.5 else "" for v, p in zip(("0", "12", "3", "9"), (zero, zero, zero, gap))),
            tuple(v if p > 0.5 else "" for v, p in zip(("10", "52", "43", "9"), (ten, ten, ten, gap))))
    table(stage, (280, 516, 760, 998), (229, 325, 421), rows, highlighted=(1, 2) if gap > 0.7 else ())
    fit(stage, "Both outputs move by the same amount.", 640, 539, 37, colour=MINT,
        opacity=s.reveal("the starting amount changes"))


def recap_three(stage, s):
    stage.heading("Find the extra copies")
    wait = s.reveal("use that observation", 0.65)
    for i in range(4):
        tile(stage, 423 + 144 * i, 292, 3, GOLD, 82, 69,
             between(s.t, s.start + 0.36 + 0.14 * i) * (1 - wait))
    fit(stage, "Multiply the whole input bar.", 640, 397, 35, colour=MINT, opacity=1 - wait)
    a = s.reveal("one adds two")
    b = s.reveal("the other multiplies by six")
    for y, intro, values, p in ((289, "Rule A", ("x", "+2", "x + 2", "×6", "?"), a),
                                (415, "Rule B", ("x", "×6", "6x", "+2", "?"), b)):
        machine(stage, y, intro, values, (p,) * 5)
    fit(stage, "Draw the matching pieces and find the gap.", 640, 543, 37, colour=WHITE,
        opacity=s.reveal("draw the matching pieces"))


SCENES = {
    "T02.3": (start_three, every_input, question_five, copy_five, compare_five, negative, reorder, recap_five),
    "T02.E": (question_three, copy_three, copy_start_only, compare_three, examples_three, recap_three),
}
