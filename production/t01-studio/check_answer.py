"""T01.3, from a sensible prediction to a checked minimum."""

import math

from stage import BG, BLUE, GOLD, MINT, MUTED, PANEL, RED, RIM, WHITE
from stage import between, blend, mix


STUDENTS = 130
SEATS = 40
FULL, WAITING = divmod(STUDENTS, SEATS)
CAPACITY = SEATS * (FULL + 1)
COACH_X = (250, 510, 770, 1030)
COACH_Y = 232


def board_position(center, seat):
    row, column = divmod(seat, 10)
    return center - 83 + column * 16, COACH_Y - 27 + row * 20


def waiting_position(student):
    column, row = divmod(student, 10)
    return 250 + 65 * column, 364 + 11.5 * row


def passenger(stage, x, y, colour=BLUE, opacity=1.0):
    stage.dot(x, y + 1.7, 5.1, "#111922", opacity)
    stage.dot(x, y, 4.1, colour, opacity)
    stage.dot(x - 1, y - 1.2, 1.35, blend(colour, WHITE, 0.44), opacity)


def coach(stage, x, *, occupants=0, colour=BLUE, emphasis=0.0, opacity=1.0):
    y = COACH_Y
    for cx in (x - 59, x + 57):
        stage.box(cx - 14, y - 60, 28, 15, radius=5, fill="#121820", opacity=opacity)
        stage.box(cx - 14, y + 48, 28, 15, radius=5, fill="#121820", opacity=opacity)
    stage.box(x - 109, y - 51, 218, 108, radius=23, fill="#111820", opacity=opacity)
    stage.box(x - 107, y - 54, 214, 107, radius=23, fill="#263848",
              edge=blend("#556777", MINT, emphasis), stroke=2.5, opacity=opacity)
    stage.box(x - 98, y - 39, 182, 84, radius=13, fill="#172530", opacity=opacity)
    stage.box(x + 86, y - 31, 10, 62, radius=5, fill="#667e93", opacity=0.75 * opacity)
    for seat in range(SEATS):
        px, py = board_position(x, seat)
        stage.dot(px, py, 4.5, "#3b4f61", opacity)
        if seat < occupants:
            passenger(stage, px, py, colour, opacity)


def sensible_answer(stage, s):
    stage.heading("Use the model to check the answer")
    cue = s.at("seven and a half people")
    whole = s.reveal("a headcount has to be a whole number")
    for i in range(7):
        x = 275 + 95 * i
        p = between(s.t, cue + 0.09 * i)
        stage.dot(x, 284, 18, BLUE, p)
        stage.box(x - 26, 315, 52, 51, radius=17, fill=BLUE, opacity=p)
    fraction = between(s.t, cue + 0.65)
    stage.box(908, 279, 70, 86, radius=16, edge=RED, fill=PANEL, opacity=fraction)
    stage.text("½", 943, 320, 47, RED, bold=True, opacity=fraction)
    stage.text("7.5 people?", 640, 434, 50, RED, bold=True, opacity=fraction * (1 - whole))
    stage.text("A headcount is a whole number.", 640, 454, 41, MINT, bold=True, opacity=whole)
    stage.text("What kind of answer would make sense?", 640, 540, 29, MUTED,
               opacity=s.reveal("what a sensible answer could look like"))


def kinds_of_answer(stage, s):
    stage.heading("Predict the kind of answer")
    options = (
        ("Count", BLUE, "a count of buses"),
        ("Probability", GOLD, "a probability is between"),
        ("Area", MINT, "an area has square units"),
    )
    for i, (name, colour, cue) in enumerate(options):
        x = 280 + 360 * i
        opacity = s.reveal(cue)
        stage.box(x - 143, 212, 286, 260, radius=23, edge=RIM, opacity=opacity)
        stage.text(name, x, 250, 30, colour, bold=True, opacity=opacity)
        if i == 0:
            for j in range(3):
                left = x - 93 + 63 * j
                stage.box(left, 303, 58, 37, radius=9, fill="#273d50", edge=BLUE, opacity=opacity)
                stage.dot(left + 12, 344, 5, BLUE, opacity)
                stage.dot(left + 46, 344, 5, BLUE, opacity)
            stage.text("Whole buses", x, 405, 27, WHITE, opacity=opacity)
        elif i == 1:
            stage.line([(x - 87, 333), (x + 87, 333)], GOLD, 5, opacity)
            for side, value in ((-1, "0"), (1, "1")):
                stage.dot(x + side * 87, 333, 7, GOLD, opacity)
                stage.text(value, x + side * 87, 365, 24, GOLD, opacity=opacity)
            stage.text("0 to 1", x, 411, 27, WHITE, opacity=opacity)
        else:
            tiles = s.reveal("three metres along each side")
            for row in range(3):
                for col in range(3):
                    stage.box(x - 60 + col * 39, 278 + row * 39, 36, 36, radius=5,
                              fill="#2d554c", edge=MINT, opacity=tiles)
            stage.text("3 m", x - 97, 333, 20, MINT, opacity=tiles)
            stage.text("9 m²", x, 422, 27, WHITE, opacity=s.reveal("nine square metres"))
    stage.text("Which unit and how large?", 640, 552, 36, MINT, bold=True,
               opacity=s.reveal("predict its size", offset=-0.3))


def school_trip(stage, s):
    stage.heading("The school trip")
    group = s.at("one hundred and thirty students")
    capacity = s.reveal("each bus has seats for forty students")
    coach(stage, 640, opacity=capacity)
    stage.text("40 seats per bus", 640, 319, 27, BLUE, bold=True, opacity=capacity)
    for student in range(STUDENTS):
        p = between(s.t, group + (student // 10) * 0.075)
        passenger(stage, *waiting_position(student), opacity=p)
    stage.text("130 students", 640, 501, 27, BLUE, bold=True, opacity=between(s.t, group))
    stage.text("What is the smallest number of buses?", 640, 569, 41, WHITE, bold=True,
               opacity=s.reveal("what is the smallest number of buses"))


def fill_three(stage, s):
    stage.heading("Fill buses in groups of forty")
    load = tuple(s.at(cue) for cue in ("one bus takes forty", "a second takes another forty",
                                      "a third brings the total"))
    remaining = s.reveal("there are still ten students waiting")
    for index, x in enumerate(COACH_X[:FULL]):
        opacity = between(s.t, s.start + 0.15 + 0.15 * index)
        coach(stage, x, opacity=opacity)
        p = between(s.t, load[index] + 1.03, 0.4)
        stage.text("40 aboard", x, 319, 25, BLUE, bold=True, opacity=p)

    for student in range(STUDENTS):
        origin_x, origin_y = waiting_position(student)
        index, seat = divmod(student, SEATS)
        if index < FULL:
            destination_x, destination_y = board_position(COACH_X[index], seat)
            motion = between(s.t, load[index] + 0.023 * (seat % 10), 0.92)
            passenger(stage, mix(origin_x, destination_x, motion),
                      mix(origin_y, destination_y, motion) - 17 * math.sin(math.pi * motion))
        else:
            passenger(stage, origin_x, origin_y, blend(BLUE, GOLD, remaining))
    stage.text("10 waiting", COACH_X[-1], 503, 27, GOLD, bold=True, opacity=remaining)
    equation = s.reveal("write one hundred and thirty")
    stage.terms([("130", WHITE, equation), ("=", WHITE, equation), ("3 × 40", BLUE, equation),
                 ("+", WHITE, equation), ("10", GOLD, equation)], 568, 49)


def last_bus(stage, s):
    stage.heading("Give the last ten a seat")
    arrives = s.reveal("put them in a fourth bus", 0.74)
    fill_start = s.at("put them in a fourth bus") + 0.38
    spare = s.reveal("thirty are spare")
    answer = s.reveal("the answer is four buses", offset=0.45)
    for x in COACH_X[:FULL]:
        coach(stage, x, occupants=SEATS, emphasis=answer)
        stage.text("40 aboard", x, 319, 25, BLUE, bold=True)
    x4 = mix(COACH_X[-1] + 95, COACH_X[-1], arrives)
    coach(stage, x4, emphasis=answer, opacity=arrives)
    for i in range(WAITING):
        x0, y0 = waiting_position(FULL * SEATS + i)
        x1, y1 = board_position(x4, i)
        p = between(s.t, fill_start + i * 0.032, 0.92)
        passenger(stage, mix(x0, x1, p), mix(y0, y1, p) - 17 * math.sin(math.pi * p), GOLD)
    stage.text("10 aboard", COACH_X[-1], 319, 25, GOLD, bold=True, opacity=between(s.t, fill_start + 0.93))
    stage.text("30 spare seats", COACH_X[-1], 371, 27, MUTED, opacity=spare)
    stage.text("Everyone has a seat in 4 buses.", 640, 529, 43, MINT, bold=True, opacity=answer)


def minimum_proof(stage, s):
    stage.heading("Check both sides of the boundary")
    x0, unit = 272, 4.8
    target_x = x0 + STUDENTS * unit
    target = between(s.t, s.start + 0.25)
    above = s.reveal("four buses make one hundred and sixty seats", 1.2)
    below = s.reveal("three buses make one hundred and twenty seats", 1.2)
    short = s.reveal("ten students would be left out")
    least = s.reveal("four is the smallest number that works")
    stage.text("130 students", target_x, 206, 26, GOLD, bold=True, opacity=target)
    for y, buses, opacity in ((285, 4, above), (403, 3, below)):
        colour = MINT if buses == 4 else BLUE
        stage.text(str(buses) + " buses", 174, y + 22, 25, colour, bold=True, opacity=opacity)
        for index in range(buses):
            p = min(1, max(0, opacity * buses - index))
            if p > 0.01:
                stage.box(x0 + SEATS * unit * index, y, (SEATS * unit - 4) * p, 43,
                          radius=10, fill=blend(BG, colour, 0.6), edge=colour)
        total = buses * SEATS
        stage.text(str(total) + " seats", x0 + total * unit, y + 66, 23, colour,
                   bold=True, opacity=opacity)
    for y in range(248, 451, 12):
        stage.line([(target_x, y), (target_x, y + 6)], GOLD, 3, target)
    from_x = x0 + FULL * SEATS * unit - 4
    stage.line([(from_x, 423), (target_x, 423)], RED, 4, short)
    stage.text("10 short", target_x + 62, 420, 26, RED, bold=True, opacity=short)
    stage.terms([("120", BLUE, least), ("<", WHITE, least), ("130", GOLD, least),
                 ("≤", WHITE, least), (str(CAPACITY), MINT, least)], 540, 51)
    stage.text("4 buses is the minimum", 640, 594, 29, MINT, opacity=least)


def full_buses(stage, s):
    stage.heading("How many buses are completely full?")
    first = s.at("each of the first three")
    partial = s.reveal("the fourth has ten")
    count = s.reveal("three buses are full", offset=0.18)
    for index, x in enumerate(COACH_X):
        full = index < FULL
        focus = between(s.t, first + 0.22 * index) if full else 0.0
        coach(stage, x, occupants=SEATS if full else WAITING, colour=BLUE if full else GOLD,
              emphasis=focus, opacity=1.0 if full else 1.0 - 0.26 * count)
        if full:
            stage.text("40 of 40", x, 327, 26, MINT, bold=True, opacity=focus)
        else:
            stage.text("10 of 40", x, 327, 26, GOLD, bold=True, opacity=partial)
    stage.bracket(149, 873, 407, "3 completely full buses", MINT, count)
    stage.text("Read what the question asks you to count.", 640, 545, 33, WHITE,
               opacity=s.reveal("the last sentence of the question"))


def recap(stage, s):
    challenge = s.reveal("here is your notebook challenge")
    stage.heading("Before you finish a problem", opacity=1 - challenge)
    steps = (("Predict", "predict what"), ("Check every condition", "check every condition"),
             ("Reread the question", "then reread"))
    for index, (label, cue) in enumerate(steps):
        p = (1 - challenge) * s.reveal(cue)
        x = 300 + 340 * index
        stage.box(x - 148, 241, 296, 117, radius=21, edge=RIM, opacity=p)
        stage.text(label, x, 299, 26, (BLUE, GOLD, MINT)[index], bold=True, opacity=p)

    stage.heading("Your turn", opacity=challenge)
    eggs = s.reveal("pack one hundred eggs into boxes of twelve")
    stage.text("100 eggs", 380, 293, 54, GOLD, bold=True, opacity=eggs)
    stage.box(680, 218, 321, 151, radius=24, fill="#3b3f43", edge="#6c747a", opacity=eggs)
    for row in range(2):
        for col in range(6):
            x, y = 713 + col * 50, 256 + row * 64
            stage.dot(x, y + 5, 21, "#252b32", eggs)
            stage.dot(x, y, 16, "#dec69b", eggs)
            stage.dot(x - 4, y - 5, 5, "#f3e0bc", eggs)
    stage.text("12 eggs per box", 840, 412, 32, GOLD, bold=True, opacity=eggs)
    stage.text("Fill each box before opening the next.", 640, 477, 29, MUTED,
               opacity=s.reveal("fill each box before"))
    stage.text("How many boxes are needed?", 640, 534, 36, WHITE, bold=True,
               opacity=s.reveal("how many boxes are needed"))
    stage.text("How many eggs go in the last box?", 640, 583, 32, MINT,
               opacity=s.reveal("how many eggs go in the last box"))


SCENES = (sensible_answer, kinds_of_answer, school_trip, fill_three,
          last_bus, minimum_proof, full_buses, recap)
