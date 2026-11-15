"""Visual models and worked examples for T01.2."""

import math

from stage import BLUE, GOLD, MINT, MUTED, RED, RIM, WHITE
from stage import between, blend, mix


PANEL_LENGTH = 128
POSTS = tuple((256 + PANEL_LENGTH * i, 350) for i in range(7))


def model_cards(stage, reveals, fade=1.0):
    for i, (name, color, p) in enumerate(zip(
        ("Line", "Table", "Sketch", "Equation"), (BLUE, GOLD, MINT, WHITE), reveals
    )):
        x = 250 + i * 260
        p *= fade
        stage.box(x - 112, 229, 224, 201, edge=RIM, radius=24, opacity=p)
        if i == 0:
            stage.line([(x - 70, 314), (x + 70, 314)], color, 3, p)
            for dx in (-70, -35, 0, 35, 70):
                stage.dot(x + dx, 314, 5, color, p)
        elif i == 1:
            stage.box(x - 59, 271, 118, 86, radius=9, fill=None, edge=color, opacity=p)
            stage.line([(x, 271), (x, 357)], color, 2, p)
            for y in (299, 328):
                stage.line([(x - 59, y), (x + 59, y)], color, 2, p)
        elif i == 2:
            stage.line([(x - 62, 356), (x - 62, 280), (x + 12, 280),
                        (x + 12, 302), (x + 60, 302), (x + 60, 356), (x - 62, 356)], color, 3, p)
        else:
            stage.text("a + b = c", x, 314, 32, color, bold=True, opacity=p)
        stage.text(name, x, 396, 28, color, bold=True, opacity=p)


def select_model(stage, s):
    stage.heading("Make the relationship visible")
    cues = ("a line shows order", "a table sets comparisons", "a sketch makes shapes", "an equation holds")
    model_cards(stage, [s.reveal(cue) for cue in cues])
    stage.text("Choose the model that answers the question.", 640, 524, 36, MINT,
               opacity=s.reveal("choose the one"))


def post(stage, x, y, hue=BLUE, opacity=1.0, size=10):
    stage.dot(x, y + 3, size + 4, "#121b24", opacity)
    stage.dot(x, y, size, hue, opacity)
    stage.dot(x - size / 4, y - size / 4, size / 3, blend(hue, WHITE, 0.35), opacity)


def interval_intro(stage, s):
    stage.heading("A fence makes two counts visible")
    posts = s.reveal("follow every post")
    panels = s.reveal("every panel between two posts")
    ends = s.reveal("mark those ends first")
    coordinates = [320, 640, 960]
    for i in range(2):
        x0, x1 = coordinates[i:i + 2]
        stage.line([(x0, 338), (mix(x0, x1, panels), 338)], GOLD, 9, panels)
        stage.text("panel", (x0 + x1) / 2, 383, 28, GOLD, opacity=panels)
    for x in coordinates:
        stage.line([(x, 285), (x, 359)], BLUE, 4, posts)
        post(stage, x, 338, BLUE, posts, 12)
    stage.text("left end", 320, 262, 26, MINT, bold=True, opacity=ends)
    stage.text("right end", 960, 262, 26, MINT, bold=True, opacity=ends)
    stage.text("Posts are points. Panels span the gaps.", 640, 512, 39, WHITE, bold=True,
               opacity=s.reveal("a sketch gives both counts"))


def open_fence(stage, s):
    stage.heading("Posts along a straight fence")
    full = s.reveal("thirty metres long")
    mark = s.at("mark off spaces of five metres")
    endposts = s.reveal("post at each end")
    stage.line([POSTS[0], (mix(POSTS[0][0], POSTS[-1][0], full), 350)], RIM, 6)
    stage.bracket(256, 1024, 281, "30 m", MINT, full)
    for i, (x, y) in enumerate(POSTS):
        opacity = endposts if i in (0, 6) else between(s.t, mark + (i - 1) * 0.18)
        post(stage, x, y, BLUE, opacity)
        stage.text(str(5 * i), x, 398, 24, MUTED, opacity=opacity)
    stage.text("How many posts are there?", 640, 512, 44, WHITE, bold=True,
               opacity=s.reveal("how many posts are there"))
    stage.text("5 m between successive posts", 640, 454, 26, GOLD, opacity=between(s.t, mark))


def count_fence(stage, s):
    stage.heading("Each gap leads to a post")
    gap_start = s.at("gives six gaps")
    mapping = s.at("follow each gap to its right-hand end")
    first = s.reveal("the post at zero")
    result = s.reveal("makes seven posts", offset=0.28)
    for i, (left, right) in enumerate(zip(POSTS, POSTS[1:])):
        g = between(s.t, gap_start + i * 0.12, 0.4)
        a = between(s.t, mapping + i * 0.13, 0.52)
        stage.line([left, right], RIM, 5)
        stage.line([left, (mix(left[0], right[0], g), 350)], GOLD, 6, g)
        stage.text(str(i + 1), (left[0] + right[0]) / 2, 322, 26, GOLD,
                   bold=True, opacity=g)
        stage.arrow((right[0] - 39, 305), (right[0] - 3, 338), BLUE, a, 2)
        stage.text(str(i + 1), right[0], 400, 25, BLUE, bold=True, opacity=a)
    for i, (x, y) in enumerate(POSTS):
        post(stage, x, y, blend(BLUE, MINT, first) if i == 0 else BLUE)
    stage.text("start", 256, 400, 25, MINT, bold=True, opacity=first)
    stage.terms([("6 right-end posts", BLUE, s.reveal("accounts for six posts")),
                 ("+", WHITE, first), ("1 starting post", MINT, first),
                 ("=", WHITE, result), ("7 posts", MINT, result)], 530, 37)


def loop_points(progress):
    """Rotate the six equal segments at their joints, preserving each panel length."""
    points = [(0.0, 0.0)]
    for index in range(6):
        angle = (index - 2.5) * math.pi / 3 * progress
        x, y = points[-1]
        points.append((x + PANEL_LENGTH * math.cos(angle), y + PANEL_LENGTH * math.sin(angle)))
    mid_x = (max(x for x, _ in points) + min(x for x, _ in points)) / 2
    mid_y = (max(y for _, y in points) + min(y for _, y in points)) / 2
    return [(x - mid_x + 640, y - mid_y + 338) for x, y in points]


def close_fence(stage, s):
    stage.heading("Join the ends into a loop")
    joined = s.at("they meet at a single corner")
    fold_start = s.at("watch the last post come back")
    fold = between(s.t, fold_start, max(0.5, joined - fold_start))
    points = loop_points(fold)
    mapping = s.at("each panel now ends")
    result = s.reveal("that makes six gaps and six posts", offset=0.35)
    for i, (left, right) in enumerate(zip(points, points[1:])):
        stage.line([left, right], GOLD, 6)
        m = between(s.t, mapping + i * 0.22)
        a = (mix(left[0], right[0], 0.35), mix(left[1], right[1], 0.35))
        b = (mix(left[0], right[0], 0.82), mix(left[1], right[1], 0.82))
        stage.arrow(a, b, WHITE, m, 2)
    for i, (x, y) in enumerate(points[:-1]):
        post(stage, x, y, MINT if i == 0 else BLUE)
    ex, ey = points[-1]
    post(stage, ex, ey, BLUE, 1 - between(s.t, joined - 0.12, 0.38))
    stage.text("Shared starting corner", 640, 483, 27, MINT, opacity=between(s.t, joined) * (1 - result))
    stage.terms([("6 gaps", GOLD, result), ("·", WHITE, result), ("6 posts", MINT, result)], 529, 47)


def person(stage, x, color, opacity):
    stage.dot(x, 348, 12, color, opacity)
    stage.box(x - 19, 367, 38, 33, radius=11, fill=color, opacity=opacity)


def queue(stage, s):
    stage.heading("A line keeps each person in one place")
    start = s.at("sam is ninth from the front")
    front = between(s.t, start, 0.75)
    back = s.reveal("sixth from the back")
    front_group = s.reveal("eight stand in front of sam")
    back_group = s.reveal("five stand behind")
    result = s.reveal("makes fourteen", offset=0.23)
    xs = [150 + 75 * i for i in range(14)]
    stage.arrow((xs[0], 242), (xs[8], 242), BLUE, front, 3)
    stage.text("9th from the front", 415, 214, 27, BLUE, bold=True, opacity=front)
    stage.arrow((xs[-1], 288), (xs[8], 288), GOLD, back, 3)
    stage.text("6th from the back", 940, 261, 27, GOLD, bold=True, opacity=back)
    for i, x in enumerate(xs):
        p = between(s.t, start + 0.10 * i)
        color = blend(RIM, BLUE, front_group) if i < 8 else MINT if i == 8 else blend(RIM, GOLD, back_group)
        person(stage, x, color, p)
    stage.bracket(xs[0] - 20, xs[7] + 20, 426, "8 in front", BLUE, front_group)
    stage.bracket(xs[9] - 20, xs[13] + 20, 426, "5 behind", GOLD, back_group)
    stage.text("Sam", xs[8], 446, 25, MINT, bold=True, opacity=front)
    stage.terms([("8", BLUE, result), ("+", WHITE, result), ("1", MINT, result),
                 ("+", WHITE, result), ("5", GOLD, result), ("=", WHITE, result),
                 ("14 people", MINT, result)], 550, 50)


def table(stage, s):
    stage.heading("A table makes the comparison fair")
    a = s.reveal("box a contains eight pencils")
    b = s.reveal("box b contains four pencils")
    unit = s.reveal("add a price per pencil column")
    result = s.reveal("two dollars and three dollars")
    verdict = s.reveal("less for each pencil")
    stage.box(174, 224, 932, 256, radius=23, edge=RIM)
    for x in (337, 558, 766):
        stage.line([(x, 233), (x, 467)], RIM, 2)
    for y in (290, 384):
        stage.line([(185, y), (1095, y)], RIM, 2)
    stage.box(773, 296, 323, 78, radius=9, fill=None, edge=MINT, opacity=verdict)
    for x, name, opacity in ((255, "Box", 1.0), (447, "Pencils", 1.0), (664, "Price ($)", 1.0),
                             (932, "Price per pencil ($)", unit)):
        stage.text(name, x, 256, 26, MINT if x == 932 else MUTED, bold=True, opacity=opacity)
    for (y, key, count, price, cost, p) in ((336, "A", 8, 16, 2, a), (431, "B", 4, 12, 3, b)):
        stage.text(key, 255, y, 38, WHITE, bold=True, opacity=p)
        stage.text(str(count), 447, y, 38, GOLD, bold=True, opacity=p)
        stage.text(str(price), 664, y, 38, BLUE, bold=True, opacity=p)
        stage.text(f"{price} ÷ {count} = {cost}", 932, y, 37, MINT, bold=True, opacity=result)
    stage.text("Box A costs $2 per pencil.", 640, 546, 40, MINT, bold=True, opacity=verdict)


def boundary(stage, s):
    stage.heading("A sketch reveals the outside boundary")
    dims = s.reveal("four metres by three metres")
    question = s.reveal("how much edge is exposed")
    individual = s.reveal("each mat has fourteen metres")
    join = s.reveal("the shared edge removes", 1.05)
    result = s.reveal("twenty-two metres outside", offset=0.3)
    x0, x1 = mix(223, 356, join), mix(773, 640, join)
    width, height, y = 284, 213, 231
    stage.box(x0, y, width, height, radius=3, fill="#253b51", edge=BLUE, stroke=3, opacity=dims)
    stage.box(x1, y, width, height, radius=3, fill="#3d3629", edge=GOLD, stroke=3, opacity=dims)
    stage.text("4 m", x0 + width / 2, 199, 29, BLUE, bold=True, opacity=dims)
    stage.text("4 m", x1 + width / 2, 199, 29, GOLD, bold=True, opacity=dims)
    stage.text("3 m", x0 - 43, y + height / 2, 26, BLUE, bold=True, opacity=dims)
    stage.text("3 m", x1 + width + 42, y + height / 2, 26, GOLD, bold=True, opacity=dims)
    stage.text("14 m", x0 + width / 2, y + height / 2, 37, BLUE, bold=True, opacity=individual * (1 - result))
    stage.text("14 m", x1 + width / 2, y + height / 2, 37, GOLD, bold=True, opacity=individual * (1 - result))
    stage.line([(x0 + width - 3, y + 3), (x0 + width - 3, y + height - 3)], RED, 4, join * (1 - result))
    stage.line([(x1 + 3, y + 3), (x1 + 3, y + height - 3)], RED, 4, join * (1 - result))
    stage.box(x0, y, x1 + width - x0, height, radius=3, fill=None, edge=MINT, stroke=5, opacity=result)
    stage.text("How much edge is exposed?", 640, 517, 34, WHITE, bold=True,
               opacity=question * (1 - individual))
    stage.terms([("14", BLUE, individual), ("+", WHITE, individual), ("14", GOLD, individual),
                 ("− 3", RED, join), ("− 3", RED, join), ("=", WHITE, result),
                 ("22 m outside", MINT, result)], 528, 44)


def recap(stage, s):
    challenge = s.reveal("your turn")
    stage.heading("Choose the model that fits", opacity=1 - challenge)
    cues = ("choose a line", "a table for comparisons", "a sketch for shape", "use an equation")
    model_cards(stage, [s.reveal(cue) for cue in cues], 1 - challenge)
    stage.heading("Your turn", opacity=challenge)
    p = s.reveal("forty-metre path")
    stage.line([(254, 318), (1026, 318)], RIM, 5, p)
    for x in (254, 1026):
        post(stage, x, 318, MINT, p)
    stage.text("40 m path", 640, 265, 35, MINT, bold=True, opacity=p)
    stage.text("Trees every 4 m, including both ends.", 640, 402, 31, MUTED, opacity=p)
    stage.text("How many trees are there?", 640, 490, 46, WHITE, bold=True,
               opacity=s.reveal("how many trees are there"))
    stage.text("Sketch it first.", 640, 551, 27, BLUE, opacity=s.reveal("sketch it first"))


SCENES = (select_model, interval_intro, open_fence, count_fence, close_fence, queue, table, boundary, recap)
