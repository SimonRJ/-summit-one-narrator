"""Compile original introduction storyboards for the canonical course lessons."""

import argparse
from collections import Counter
import json
from pathlib import Path

from number_topics import cryptarithms, cycles, divisibility, multiples, parity, primes, repunits
from story import Lesson, film


ROOT = Path(__file__).resolve().parents[3]
BESPOKE = {f"S{slot:03}" for slot in range(1,7)}
TOPICS = {
    "Repeated digits, palindromes and repunits": repunits,
    "Cryptarithms and symbol-to-digit arithmetic": cryptarithms,
    "Primes, factors and factorisation": primes,
    "Multiples, HCF and LCM": multiples,
    "Divisibility tests and modular remainders": divisibility,
    "Parity and odd/even structure": parity,
    "Last-digit, clock and repeating-cycle reasoning": cycles,
}


def lessons():
    sessions = json.loads((ROOT / "data/sessions-372.json").read_text())["sessions"]
    visits = Counter()
    for item in sessions:
        if item["type"] != "LESSON":
            continue
        title = item["focus"]
        yield Lesson(item["slot"], title, item["phase"], visits[title])
        visits[title] += 1


def ready(lesson):
    return lesson.id in BESPOKE or lesson.title in TOPICS


def compile_lesson(lesson):
    path = ROOT / "production/scripts" / f"{lesson.id}.json"
    if lesson.id in BESPOKE:
        return json.loads(path.read_text())
    data = film(lesson, TOPICS[lesson.title](lesson))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, separators=(",",":")) + "\n")
    return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ids", nargs="*")
    parser.add_argument("--list-ready", action="store_true")
    parser.add_argument("--all", action="store_true", help="Validate and compile all ready lessons.")
    args = parser.parse_args()
    course = dict((lesson.id, lesson) for lesson in lessons())
    if args.list_ready:
        print(json.dumps([lesson.id for lesson in course.values() if ready(lesson)]))
    else:
        names = [lesson.id for lesson in course.values() if ready(lesson)] if args.all else args.ids
        assert names, "Specify the lesson IDs or --all."
        for id in names:
            result = compile_lesson(course[id])
            print(f"{id} | {result['title']} | {len(result['scenes'])} scenes")
