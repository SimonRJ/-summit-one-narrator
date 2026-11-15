"""Speech-timed mathematical marks for the Summit One teaching series."""

import math

from stage import BG, BLUE, GOLD, MINT, MUTED, PANEL, RED, RIM, WHITE, blend, mix
from studio_diagrams import bead, fit, recap, tile


def cue(s, words, *, delay=0, duration=0.55):
    return s.reveal(words, duration, delay) if words else 1


def scene(title, *layers, subtitle=None):
    def draw(stage, s):
        fit(stage,title,640,87,48 if len(title)<41 else 43,1170,WHITE)
        if subtitle:
            fit(stage,subtitle,640,143,26,1100,MUTED,bold=False)
        for layer in layers:
            layer(stage, s)
    draw.chapter = title
    return draw


def steps(stage, s, layers):
    for layer in layers:
        layer(stage, s)


def change(words, before, after):
    def draw(stage, s):
        steps(stage, s, after if s.t >= s.at(words) else before)
    return draw


def note(text, words=None, *, x=640, y=550, size=39, colour=MINT, width=1100):
    return lambda stage, s: fit(stage, text, x, y, size, width, colour, cue(s, words))


def equation(*terms, y=551, size=47):
    """Keep each term in a fixed position as the equation is built."""
    def draw(stage, s):
        stage.terms([(text, colour, cue(s, words)) for text, colour, words in terms], y, size)
    return draw


def cards(items, y=333, *, words=None, x=640, width=124, gap=142, face=BLUE, size=33,
          delay=0.13, rise=35, height=67):
    def draw(stage, s):
        for i, item in enumerate(items):
            if isinstance(item, tuple):
                label, colour = item
            else:
                label, colour = item, face
            opacity = cue(s, words, delay=i * delay)
            tile(stage, x + (i - (len(items) - 1) / 2) * gap, y - rise * (1 - opacity),
                 label, colour, width, height, opacity, size)
    return draw


def move(label, start, finish, words, *, colour=BLUE, width=108, height=64, delay=0, duration=0.8):
    def draw(stage, s):
        p = cue(s, words, delay=delay, duration=duration)
        tile(stage, mix(start[0], finish[0], p), mix(start[1], finish[1], p) - 17 * math.sin(math.pi * p),
             label, colour, width, height, size=30)
    return draw


def outline(x, y, width, height, words=None, *, colour=RIM, radius=13):
    return lambda stage, s: stage.box(x, y, width, height, fill=None, edge=colour, radius=radius,
                                      opacity=cue(s, words), stroke=2)


def link(start, end, words=None, *, colour=RIM, arrow=False, width=3, delay=0):
    def draw(stage, s):
        p = cue(s, words, delay=delay, duration=0.65)
        if arrow:
            stage.arrow(start, end, colour, p, width)
        elif p > 0:
            stage.line((start, (mix(start[0], end[0], p), mix(start[1], end[1], p))), colour, width, p)
    return draw


def chart(headings, rows, *, x=640, y=227, row_height=68, width=980, highlight=(), font=31):
    """Each row supplies its own spoken cue for revealing actual counted outcomes."""
    left = x - width / 2
    w = width / len(headings)
    xs = [left + w * (i + 0.5) for i in range(len(headings))]

    def draw(stage, s):
        stage.box(left, y - 31, width, row_height * (len(rows) + 1) - 2, fill=None, edge=RIM)
        for i, (label, x) in enumerate(zip(headings, xs)):
            fit(stage, label, x, y, 24, w - 12, MUTED)
            if i:
                stage.line([(left + w * i, y - 30), (left + w * i, y + (len(rows) + 0.5) * row_height - 1)], RIM, 1)
        for j, (values, words) in enumerate(rows, 1):
            p = cue(s, words)
            yy = y + row_height * j
            stage.line([(left, yy - row_height / 2), (left + width, yy - row_height / 2)], RIM, 1)
            for k, (value, x) in enumerate(zip(values, xs)):
                colour = MINT if (j - 1, k) in highlight else WHITE
                if isinstance(value, tuple):
                    value, colour = value
                fit(stage, str(value), x, yy, font, w - 15, colour, p)
    return draw


def board(rows, cols, *, width=64, x=640, y=350, cells=(), marks=(), grid=RIM, tint=PANEL):
    """A grid with independently revealed coloured cells and labelled occupants."""
    left, top = x - cols * width / 2, y - rows * width / 2

    def draw(stage, s):
        stage.box(left, top, cols * width, rows * width, fill=tint, edge=grid, radius=2)
        for r, c, colour, words in cells:
            stage.box(left + c * width + 1, top + r * width + 1, width - 2, width - 2, radius=3,
                      fill=blend(PANEL, colour, 0.32), edge=colour, opacity=cue(s, words), stroke=2)
        for k in range(1, cols):
            stage.line([(left + k * width, top), (left + k * width, top + rows * width)], grid, 2)
        for k in range(1, rows):
            stage.line([(left, top + k * width), (left + cols * width, top + k * width)], grid, 2)
        for r, c, label, colour, words in marks:
            xx, yy = left + (c + 0.5) * width, top + (r + 0.5) * width
            p = cue(s, words)
            if label == "•":
                bead(stage, xx, yy, colour, p, min(23, width * 0.24))
            else:
                fit(stage, label, xx, yy, min(38, round(width * 0.57)), width - 6, colour, p)
    return draw


def ring(n, *, x=640, y=347, radius=138):
    return [(x + radius * math.sin(i * 2 * math.pi / n), y - radius * math.cos(i * 2 * math.pi / n))
            for i in range(n)]


def network(positions, labels, edges=(), *, node_colour=BLUE, radius=23, stage_words=None):
    """Draw edges before nodes, keeping the identities of all vertices visible."""
    def draw(stage, s):
        p = cue(s, stage_words)
        for i, j, colour, words in edges:
            a, b = positions[i], positions[j]
            progress = cue(s, words, duration=0.75)
            if progress:
                stage.line((a, (mix(a[0], b[0], progress), mix(a[1], b[1], progress))),
                           colour, 4 if colour != RIM else 2, progress * p)
        for point, label in zip(positions, labels):
            bead(stage, *point, node_colour, p, radius)
            fit(stage, str(label), *point, min(35, radius), radius * 1.65, BG, p)
    return draw


def balance(left, right, *, words=None, y=347, x=640):
    def draw(stage, s):
        p = cue(s, words)
        stage.line([(x - 396, y + 36), (x + 396, y + 36)], MINT, 5, p)
        stage.line([(x - 39, y + 117), (x, y + 39), (x + 39, y + 117), (x - 39, y + 117)], RIM, 4, p)
        for xx, label in ((x - 218, left), (x + 218, right)):
            tile(stage, xx, y - 6, label, BLUE, 335, 69, p, 36)
    return draw


def blocks(parts, *, x=640, y=335, width=810, height=70, words=None, gap=4):
    """Area models and number bars preserve the relative size of every part."""
    total = sum(part[0] for part in parts)
    inner = width - gap * (len(parts) - 1)

    def draw(stage, s):
        left = x - width / 2
        for weight, label, colour, when in parts:
            w = weight * inner / total
            p = cue(s, when or words)
            tile(stage, left + w / 2, y, label, colour, w, height, p, min(34, round(w * 0.42)))
            left += w + gap
    return draw


def exercise(method, words, question, *, sub=None):
    def draw(stage, s):
        recap(stage, s, method, words, question, sub=sub)
    draw.chapter = "Your turn"
    return draw
