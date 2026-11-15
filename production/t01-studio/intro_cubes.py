"""Layer counts with isometric cubes and explicit cells for overlapping cuts."""

from itertools import product

from intro_art import applications, card, header, mistakes, prompt, stagger, steps
from stage import BG, BLUE, GOLD, MINT, MUTED, RED, RIM, WHITE, blend, mix
from studio_diagrams import fit


SLOT = 6
LAYERS = (BLUE, GOLD, MINT, "#c2b0f5")
BLOCK = frozenset(product(range(3), range(2), range(2)))
HEIGHTS = ((4, 1, 3), (1, 3, 2))
STACKS = frozenset((x, y, z) for y, row in enumerate(HEIGHTS)
                   for x, height in enumerate(row) for z in range(height))
WHOLE = frozenset(product(range(4), range(4), range(3)))
COLUMN = frozenset((1, 2, z) for z in range(3))
TUNNEL = frozenset((x, 2, 1) for x in range(4))
MISSING = COLUMN | TUNNEL


def solids(stage, cells, x0, y0, *, zoom=1, spread=0, opacity=1, monochrome=False, painted=None):
    """Draw only exposed faces with a fixed isometric camera and colour by level."""
    if opacity <= 0:
        return
    face_defs = (
        ((1, 0, 0), ((1, 0, 0), (1, 1, 0), (1, 1, 1), (1, 0, 1)), .52),
        ((0, 1, 0), ((0, 1, 0), (1, 1, 0), (1, 1, 1), (0, 1, 1)), .72),
        ((0, 0, 1), ((0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1)), .96),
    )
    draw_order = sorted(cells, key=lambda xyz: (sum(xyz), xyz[2], xyz[1], xyz[0]))
    for x, y, z in draw_order:
        level_colour = BLUE if monochrome else LAYERS[z % len(LAYERS)]
        for (dx, dy, dz), vertices, shade in face_defs:
            if (x + dx, y + dy, z + dz) in cells and (dz == 0 or spread < 2):
                continue
            tone = level_colour if painted is None else (GOLD if (x, y, z, dx, dy, dz) in painted else BLUE)
            points = [(x0 + (x + vx - y - vy) * 39 * zoom,
                       y0 + (x + vx + y + vy) * 20 * zoom
                       - (z + vz) * 48 * zoom - spread * z)
                      for vx, vy, vz in vertices]
            px = [(stage.px(xp), stage.px(yp)) for xp, yp in points]
            stage.draw.polygon(px, fill=blend(BG, tone, opacity * shade))
            stage.line((*points, points[0]), blend(tone, WHITE, .15), 2, opacity * .72)


def map_layer(stage, *, left, top, width, depth, cells, colour, opacity=1, size=38):
    for row, col in product(range(depth), range(width)):
        x, y = left + col * size, top + row * size
        occupied = (col, row) in cells
        stage.box(x, y, size - 4, size - 4, radius=6, fill=blend(BG, colour, .55) if occupied else None,
                  edge=colour if occupied else RIM, opacity=opacity * (1 if occupied else .8))
        if not occupied:
            stage.line(((x + 7, y + size - 11), (x + size - 11, y + 7)), RIM, 2, opacity)


def introduction(stage, s):
    header(stage, SLOT, "The idea", "Unit-cube counting and layered solids")
    p = s.reveal("build a solid", .8)
    split = s.reveal("lifting one level", 1)
    solids(stage, BLOCK, mix(580, 552, split), 413, zoom=1.5, spread=90 * split, opacity=p,
           monochrome=split <= .01)
    q = s.reveal("the layers give you")
    fit(stage, "Count one layer at a time", 640, 587, 43, 1050, MINT, q)


def exam(stage, s):
    applications(stage, s, SLOT, "Count hidden cubes systematically", (
        ("in amc upper primary", "AMC Upper Primary",
         "A solid can hide cubes behind its front face.", "Sketch the footprint and count each level."),
        ("in a rossmoyne style", "Rossmoyne-style practice",
         "Holes and channels change which cells are filled.", "Keep the layer sketches aligned."),
    ))


def basic_prompt(stage, s):
    header(stage, SLOT, "Basic example", "Count a 3 × 2 × 2 block")
    solids(stage, BLOCK, 546, 388, zoom=1.5, opacity=s.reveal("this block is"))
    p = s.reveal("how many unit cubes")
    card(stage, 931, 356, "How many cubes?", GOLD, w=330, h=93, size=45, opacity=p)


def basic(stage, s):
    header(stage, SLOT, "Basic example", "Copy the footprint to the next layer")
    p = s.reveal("one layer has")
    q = s.reveal("the upper layer", .75)
    solids(stage, BLOCK, 414, 390, zoom=1.5, spread=q * 73, opacity=p)
    fit(stage, "2 rows × 3 per row = 6", 872, 292, 43, 562, GOLD, s.reveal("that gives six"))
    fit(stage, "Another 6 on top", 872, 384, 43, 562, BLUE, q)
    fit(stage, "6 + 6 = 12", 872, 477, 63, 484, MINT, s.reveal("there are twelve"))


def medium_prompt(stage, s):
    header(stage, SLOT, "Medium example", "Six stacks of different heights")
    p = s.reveal("their heights")
    for i, (row, numbers) in enumerate((("FRONT", HEIGHTS[1]), ("BACK", HEIGHTS[0]))):
        y = 290 + 125 * i
        stage.text(row, 185, y, 26, MUTED, bold=True, opacity=p)
        for j, height in enumerate(numbers):
            a = stagger(s, "their heights", i * 3 + j, delay=.23)
            card(stage, 340 + 140 * j, y, height, BLUE, w=114, h=87, opacity=a)
    solids(stage, STACKS, 953, 478, zoom=.96, opacity=s.reveal("all stacks rest"))
    fit(stage, "How many cubes altogether?", 640, 572, 42, 1090, WHITE,
        s.reveal("how many cubes"))


def medium(stage, s):
    header(stage, SLOT, "Medium example", "Check how many stacks reach each level")
    level_cues = ("level one has six", "reach level two", "reach level three", "reaches level four")
    for z, (cue, count) in enumerate(zip(level_cues, (6, 4, 3, 1))):
        x = 167 + z * 276
        p = s.reveal(cue)
        occupied = {(a, b) for a, b, level in STACKS if level == z}
        fit(stage, f"LEVEL {z + 1}", x + 58, 265, 31, 190, LAYERS[z], p)
        map_layer(stage, left=x, top=309, width=3, depth=2, cells=occupied, colour=LAYERS[z], opacity=p)
        fit(stage, str(count), x + 56, 449, 47, 150, LAYERS[z], p)
    fit(stage, "6 + 4 + 3 + 1 = 14", 640, 552, 54, 1060, MINT,
        s.reveal("add six, four"))


def challenge_prompt(stage, s):
    header(stage, SLOT, "Exam-style challenge", "Two cuts cross inside the block")
    solids(stage, WHOLE, 405, 373, zoom=1.21, opacity=s.reveal("start with a solid"))
    for j, (cue, message, colour) in enumerate((
        ("start with a solid", "A solid 4 × 4 × 3 block", BLUE),
        ("remove a vertical column", "Remove one 3-cube column.", GOLD),
        ("also remove a straight tunnel", "Remove 4 across the middle.", BLUE),
        ("the tunnel passes through", "The two cuts share a cell.", MINT),
    )):
        p = s.reveal(cue)
        fit(stage, message, 849, 249 + j * 74, 37, 635, colour, p)
    fit(stage, "How many cubes remain?", 640, 583, 42, 1045, WHITE,
        s.reveal("how many cubes remain"))


def cut_plans(stage, s):
    header(stage, SLOT, "Exam-style challenge", "Update the cut plan for each layer")
    original = s.reveal("each of the three layers")
    column = s.reveal("removing the vertical column")
    tunnel = s.reveal("the tunnel runs through")
    shared = s.reveal("one of them is already empty")
    for z, title in enumerate(("BOTTOM", "MIDDLE", "TOP")):
        left = 179 + 368 * z
        fit(stage, title, left + 100, 231, 37, 235, LAYERS[z], original)
        fog = {(x, y) for x, y, layer in WHOLE if layer == z}
        map_layer(stage, left=left, top=266, width=4, depth=4, colour=LAYERS[z],
                  cells=fog, opacity=original, size=50)
        for x, y, layer in sorted(MISSING):
            if layer == z:
                lx, ly = left + 50 * x, 266 + 50 * y
                p = column if (x, y, layer) in COLUMN else tunnel
                tint = MINT if (x, y, layer) in COLUMN and z == 1 else RED
                stage.box(lx, ly, 46, 46, radius=6, fill=BG, edge=tint, opacity=p)
                stage.line(((lx + 8, ly + 37), (lx + 37, ly + 8)), tint, 3, p)
                if tint == MINT:
                    stage.box(lx - 3, ly - 3, 52, 52, radius=8, fill=None, edge=MINT, stroke=3, opacity=shared)
    fit(stage, "Column removes 3. The tunnel removes 3 more.", 640, 555, 42, 1120, MINT,
        s.reveal("takes only three more"))


def challenge(stage, s):
    header(stage, SLOT, "Exam-style challenge", "Count what remains")
    p = s.reveal("the bottom and top")
    q = s.reveal("the middle has twelve")
    r = s.reveal("is forty-two")
    solids(stage, WHOLE - MISSING, 412, 432, zoom=1.05, spread=40, opacity=p)
    fit(stage, "15   +   12   +   15", 854, 278, 52, 560, WHITE, q)
    fit(stage, "= 42 cubes", 854, 369, 58, 545, MINT, r)
    fit(stage, "Check: 48 − 6 = 42", 854, 486, 43, 550, WHITE,
        s.reveal("as a check"))


def common_errors(stage, s):
    mistakes(stage, s, SLOT, "Keep hidden cells and shared cuts visible", (
        ("a visible cube count", "Count the visible cubes", "Count every position in each layer"),
        ("a second mistake", "Remove 3 + 4 cubes", "Remove 3 + 4 − 1 cubes"),
    ))


def takeaway(stage, s):
    steps(stage, s, SLOT, "One sketch for each level", (
        ("identify the base dimensions", "Name the base and levels", "Label the width, depth and height."),
        ("label hidden positions", "Sketch layers in order", "Include cells behind the visible front."),
        ("mark their common cell", "Mark the shared cell", "Every empty cell is removed once."),
        ("check your count", "Check in a second way", "Compare the layer sum with full volume minus the missing cubes."),
    ))


SCENES = (introduction, exam, basic_prompt, basic, medium_prompt, medium, challenge_prompt,
          cut_plans, challenge, common_errors, takeaway)
