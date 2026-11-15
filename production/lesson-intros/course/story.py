"""Authorable scenes for the Summit One introduction series."""

from dataclasses import dataclass
from fractions import Fraction


SMALL = (
    "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen "
    "fifteen sixteen seventeen eighteen nineteen"
).split()
TENS = "zero ten twenty thirty forty fifty sixty seventy eighty ninety".split()


def say(n):
    """Speak integers and exact fractions naturally with the saved narrator."""
    if isinstance(n, Fraction):
        if n.denominator == 1:
            return say(n.numerator)
        return f"{say(n.numerator)} over {say(n.denominator)}"
    if n < 0:
        return "minus " + say(-n)
    if n < 20:
        return SMALL[n]
    if n < 100:
        tens, ones = divmod(n, 10)
        return TENS[tens] + ("-" + SMALL[ones] if ones else "")
    if n < 1000:
        hundreds, rest = divmod(n, 100)
        return f"{SMALL[hundreds]} hundred" + (" and " + say(rest) if rest else "")
    for unit, name in ((10**9, "billion"), (10**6, "million"), (1000, "thousand")):
        if n >= unit:
            leading, rest = divmod(n, unit)
            join = " and " if 0 < rest < 100 else " "
            return f"{say(leading)} {name}" + (join + say(rest) if rest else "")
    raise AssertionError(n)


def spoken_list(values):
    seq = [say(v) if isinstance(v, (int, Fraction)) else str(v) for v in values]
    if len(seq) < 2:
        return "".join(seq)
    return ", ".join(seq[:-1]) + " and " + seq[-1]


Beat = tuple[str, str]


@dataclass(frozen=True)
class Example:
    title: str
    prompt: tuple[Beat, ...]
    working: tuple[Beat, ...]
    artwork: dict | None = None
    proof: tuple[Beat, ...] = ()
    worked_art: dict | None = None
    proof_art: dict | None = None


@dataclass(frozen=True)
class Topic:
    opening: tuple[Beat, ...]
    exams: tuple[Beat, ...]
    examples: tuple[Example, Example, Example]
    mistakes: tuple[tuple[str, str, str], ...]
    checklist: tuple[tuple[str, str, str], ...]
    cover: dict | None = None


@dataclass(frozen=True)
class Lesson:
    slot: int
    title: str
    phase: str
    visit: int

    @property
    def id(self):
        return f"S{self.slot:03}"


def scene(stage, title, beats, *, art=None, pairs=None):
    clean = [(said.strip(), shown.strip()) for said, shown in beats]
    assert clean and all(said.endswith((".", "?", "!")) and shown for said, shown in clean)
    narrator = " ".join(said for said, _ in clean)
    assert 18 <= len(narrator.split()) <= 86, (stage, title, len(narrator.split()))
    return {
        "stage": stage, "heading": title, "narration": narrator,
        "beats": [{"cue": said, "line": shown} for said, shown in clean],
        **({"art": art} if art else {}), **({"pairs": pairs} if pairs else {}),
    }


def film(lesson, topic):
    shots = [
        scene("INTRO", lesson.title, topic.opening, art=topic.cover),
        scene("EXAM", "Where this idea helps", topic.exams),
    ]
    for level, example in zip(("BASIC", "MEDIUM", "HARD"), topic.examples, strict=True):
        shots.extend((
            scene("PUZZLE", example.title, example.prompt, art=example.artwork),
            scene(level, example.title, example.working, art=example.worked_art or example.artwork),
        ))
        if level == "HARD" and example.proof:
            shots.append(scene("HARD", "Check the challenge solution", example.proof, art=example.proof_art))
    shots.append(scene("MISTAKES", "Common mistakes", tuple((v, a) for v,a,_ in topic.mistakes),
                      pairs=[b for _,_,b in topic.mistakes]))
    shots.append(scene("RECAP", "Your exam checklist", tuple((v, a) for v,a,_ in topic.checklist),
                      pairs=[b for _,_,b in topic.checklist]))
    return {
        "id": lesson.id, "course_slot": lesson.slot, "title": lesson.title,
        "phase": lesson.phase, "visit": lesson.visit + 1,
        "scenes": [{"n": index, **shot} for index, shot in enumerate(shots, 1)],
    }


def tiles(*values, highlight=()):
    return {"kind": "tiles", "values": list(map(str, values)), "highlight": highlight}


def table(*rows, highlight=()):
    return {"kind": "table", "rows": [[str(value) for value in row] for row in rows],
            "highlight": highlight}


def bars(*rows):
    return {"kind": "bars", "rows": rows}


def grid(*rows, highlight=()):
    return {"kind": "grid", "rows": [[str(value) for value in row] for row in rows],
            "highlight": highlight}


def chain(*values):
    return {"kind": "chain", "values": list(map(str, values))}


def geometry(nodes, segments, *, polygons=(), captions=(), keep_aspect=True):
    return {"kind": "geometry", "nodes": nodes, "segments": segments,
            "polygons": polygons, "labels": captions, "keep_aspect": keep_aspect}


def cubes(cells, *, spread=0):
    return {"kind": "cubes", "cells": sorted(cells), "spread": spread}


def venn(left, right, shared):
    return {"kind": "venn", "values": [str(left), str(right), str(shared)]}
