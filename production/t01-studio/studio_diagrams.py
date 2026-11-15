"""Shared marks, tiles and number lines for the Summit One films."""

from stage import BG, BLUE, GOLD, MINT, MUTED, PANEL, RED, RIM, WHITE
from stage import between, blend, lettering, mix


PRIME_COLOURS = {2: BLUE, 3: GOLD, 5: MINT, 7: "#c3b0ea", 11: "#f4ab94", 13: "#a4cdd1"}
BEAD_COLOURS = ("#ee6870", "#64a8fc", "#55ca99", "#f6d455")


def fit(stage, text, x, y, size=37, width=1100, colour=WHITE, opacity=1.0, bold=True):
    if opacity <= 0:
        return
    while size > 21 and lettering(text, stage.px(size), colour, bold).width > stage.px(width):
        size -= 1
    stage.text(text, x, y, size, colour, bold=bold, opacity=opacity)


def tile(stage, x, y, label, colour=BLUE, width=105, height=65, opacity=1.0, size=33):
    if opacity <= 0:
        return
    stage.box(x - width / 2, y - height / 2 + 4, width, height, radius=13,
              fill="#0e1820", opacity=opacity)
    fill = blend(PANEL, colour, 0.14)
    stage.box(x - width / 2, y - height / 2, width, height, radius=13, fill=fill,
              edge=colour, opacity=opacity)
    stage.line([(x - width * 0.30, y - height / 2 + 5), (x + width * 0.30, y - height / 2 + 5)],
               colour, 1.5, opacity * 0.46)
    fit(stage, str(label), x, y, size, width - 12, colour, opacity)


def prime(stage, x, y, value, opacity=1.0, width=71):
    tile(stage, x, y, value, PRIME_COLOURS.get(value, WHITE), width, width * 0.8,
         opacity, size=33)


def bead(stage, x, y, colour, opacity=1.0, radius=17):
    if opacity <= 0:
        return
    stage.dot(x, y + 4, radius + 1, "#101921", opacity)
    stage.dot(x, y, radius, colour, opacity)
    stage.dot(x - 4, y - 5, radius * 0.31, blend(colour, WHITE, 0.42), opacity)


def rail(stage, coords, y, labels, colour=MUTED, opacity=1.0):
    stage.line([(coords[0], y), (coords[-1], y)], RIM, 4, opacity)
    for x, label in zip(coords, labels):
        stage.line([(x, y - 7), (x, y + 11)], RIM, 1.6, opacity)
        if label:
            fit(stage, str(label), x, y + 31, 23, 110, colour, opacity, False)


def table(stage, xs, ys, rows, *, opacity=1.0, highlighted=(), width=950, colours=()):
    left = (1280 - width) / 2
    top = ys[0] - 29
    bottom = ys[-1] + 34
    stage.box(left, top, width, bottom - top, radius=20, edge=RIM, opacity=opacity)
    for first, second in zip(ys, ys[1:]):
        y = (first + second) / 2
        stage.line([(left + 10, y), (left + width - 10, y)], RIM, 2, opacity)
    for row, (y, cells) in enumerate(zip(ys, rows)):
        if row in highlighted:
            stage.box(left + 9, y - 24, width - 18, 49, radius=10, fill=None, edge=MINT, opacity=opacity)
        colour = (colours[row] if row < len(colours) else MINT) if row else MUTED
        for x, cell in zip(xs, cells):
            fit(stage, str(cell), x, y, 27 if not row else 34, width / len(xs) - 12,
                colour if row in highlighted or colours else WHITE if row else MUTED, opacity, True)


def recap(stage, s, steps, cue, question, *, sub=None):
    """Reveal a short method, then give the learner a clean problem to try."""
    show = s.reveal(cue)
    stage.heading("Use the method again", opacity=1 - show)
    for i, (label, spoken) in enumerate(steps):
        opacity = s.reveal(spoken) * (1 - show)
        count = len(steps)
        x = 640 + (i - (count - 1) / 2) * 325
        tile(stage, x, 328, label, (BLUE, GOLD, MINT)[i], 300, 88, opacity, size=29)
    stage.heading("Your turn", opacity=show)
    for i, line in enumerate(question):
        fit(stage, line, 640, 263 + 63 * i, 38, 1070, WHITE, show)
    if sub:
        fit(stage, sub, 640, 509, 27, 1070, MINT, show, False)


def join(stage, x, y1, y2, colour, opacity=1.0):
    for y in range(round(y1), round(y2), 9):
        stage.line([(x, y), (x, min(y + 4, y2))], colour, 2, opacity)
