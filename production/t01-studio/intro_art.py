"""Composition helpers for the Summit One lesson introductions."""

from stage import BLUE, GOLD, MINT, MUTED, PANEL, RED, RIM, WHITE, between, blend
from studio_diagrams import fit, wrapped_text


def header(stage, slot, section, title, subtitle=None):
    fit(stage, f"SUMMIT ONE  /  LESSON {slot:02}", 229, 35, 22, 305, BLUE)
    stage.text(section.upper(), 1200, 35, 21, MUTED, bold=True, align="right")
    stage.line(((79, 60), (1201, 60)), RIM, 1)
    fit(stage, title, 640, 111, 50, 1110, WHITE)
    if subtitle:
        fit(stage, subtitle, 640, 162, 32, 1100, MUTED, bold=False)


def card(stage, x, y, text, colour=BLUE, *, w=122, h=80, opacity=1, size=46):
    """A matte tile with a lit face and a shallow visual edge."""
    stage.box(x - w / 2, y - h / 2 + 8, w, h, radius=17, fill="#090e15", opacity=opacity)
    stage.box(x - w / 2, y - h / 2, w, h, radius=17, fill=blend(PANEL, colour, .12),
              edge=colour, opacity=opacity)
    stage.line(((x - w / 2 + 18, y + h / 2 - 7), (x + w / 2 - 18, y + h / 2 - 7)),
               colour, 2, opacity * .3)
    fit(stage, str(text), x, y, size, w - 17, colour, opacity)


def prompt(stage, moment, slot, level, title, lines):
    header(stage, slot, level, title)
    for index, (cue, text) in enumerate(lines):
        p = moment.reveal(cue, .65)
        y = 248 + index * 65
        fit(stage, text, 640, y + (1 - p) * 12, 43, 1120, WHITE, p, bold=False)


def applications(stage, moment, slot, title, exams):
    header(stage, slot, "Where it shows up", title)
    for index, (cue, exam, line1, line2) in enumerate(exams):
        p = moment.reveal(cue, .65)
        y = 277 + index * 185 + (1 - p) * 15
        colour = (BLUE, GOLD)[index]
        stage.box(112, y - 62, 1056, 139, radius=25, fill=PANEL, edge=RIM, opacity=p)
        stage.line(((139, y - 37), (139, y + 50)), colour, 5, p)
        stage.text(exam, 178, y - 17, 32, colour, bold=True, align="left", opacity=p)
        stage.text(line1, 178, y + 23, 34, WHITE, align="left", opacity=p)
        if line2:
            stage.text(line2, 178, y + 59, 29, MUTED, align="left", opacity=p)


def steps(stage, moment, slot, title, items):
    header(stage, slot, "Your exam checklist", title)
    for index, (cue, label, detail) in enumerate(items):
        p = moment.reveal(cue, .75)
        y = 239 + 100 * index + (1 - p) * 11
        stage.box(97, y - 39, 1086, 78, radius=18, edge=RIM, opacity=p)
        stage.dot(144, y, 25, "#23483e", p)
        stage.line(((132, y), (142, y + 9), (157, y - 10)), MINT, 4, p)
        stage.text(label, 195, y - 13, 33, WHITE, bold=True, align="left", opacity=p)
        stage.text(detail, 195, y + 19, 28, MUTED, align="left", opacity=p)


def mistakes(stage, moment, slot, title, pairs):
    header(stage, slot, "Common mistakes", title)
    for index, (cue, error, fix) in enumerate(pairs):
        p = moment.reveal(cue, .6)
        y = 266 + index * 133 + (1 - p) * 13
        stage.box(79, y - 42, 524, 84, edge=blend(RIM, RED, .48), radius=19, opacity=p)
        stage.box(677, y - 42, 524, 84, edge=blend(RIM, MINT, .48), radius=19, opacity=p)
        wrapped_text(stage, error, 341, y, 30, 474, RED, p, bold=True)
        wrapped_text(stage, fix, 939, y, 30, 474, MINT, p, bold=True)
        stage.arrow((617, y), (663, y), MINT, p, 3)


def stagger(moment, phrase, index, *, delay=.12, speed=.55):
    return between(moment.t, moment.at(phrase) + index * delay, speed)
