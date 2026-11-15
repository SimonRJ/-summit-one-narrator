"""Verify the teaching examples independently of their recorded solutions."""

from itertools import permutations
import json
from math import lcm
from pathlib import Path


def as_numbers(cards):
    return [int("".join(order)) for order in permutations(cards) if order[0] != "0"]


def check_examples():
    assert divmod(38, 6) == (6, 2)
    choices = (124, 142, 212, 221)
    assert [number for number in choices if number % 4 == 0 and number % 3 == 2] == [212]
    meetings = sorted(set(range(2, 200, 6)) & set(range(5, 200, 9)))
    assert meetings[0] == 14 and lcm(6, 9) == 18
    assert [minute for minute in meetings if minute > 100] == [104, 122, 140, 158, 176, 194]
    assert [minute for minute in meetings if minute > 100 and minute % 5 == 0] == [140]

    assert 3986 + 2047 == 6000 - 14 + 47 == 6033
    assert 49 * 28 == 50 * 28 - 28 == 1372
    assert 39 * 52 - 37 * 48 == 37 * 4 + 2 * 52 == 252
    assert 252 - 250 == 2

    assert 6 * 4 + 7 == 31
    assert 27 - 27 // 3 + 7 == 25
    tickets = [68]
    for _ in range(3):
        assert tickets[-1] % 2 == 0
        tickets.append(tickets[-1] // 2 - 2)
    assert tickets == [68, 32, 14, 5]

    assert min(as_numbers("047")) == 407
    assert sorted(number for number in as_numbers("025") if number % 2 == 0) == [250, 502, 520]
    valid = [number for number in as_numbers("01246") if number > 40000 and number % 4 == 0]
    assert len(valid) == 18 and 61204 in valid
    assert sum(number // 10000 == 4 for number in valid) == 8

    assert 5724 % 9 == 0 and sum(map(int, str(5724))) == 18
    assert sum(str(number).count("4") for number in range(1, 66)) == 17
    allowed = [number for number in range(1, 251) if number % 9 == 0]
    assert [[number for number in allowed if number // place % 10 == 2] for place in (1, 10, 100)] == [
        [72, 162], [27, 126, 225], [207, 216, 225, 234, 243],
    ]
    assert sum(str(number).count("2") for number in allowed) == 10

    assert 3 * 2 * 2 == 12
    heights = (1, 3, 2, 4, 1, 3)
    assert [sum(height >= level for height in heights) for level in range(1, 5)] == [6, 4, 3, 1]
    assert sum(heights) == 14
    original = {(x, y, z) for x in range(4) for y in range(4) for z in range(3)}
    remaining = {p for p in original if not (p[:2] == (1, 2) or p[1:] == (2, 1))}
    assert [sum(p[2] == z for p in remaining) for z in range(3)] == [15, 12, 15]
    assert len(remaining) == 42


def check_course_order():
    root = Path(__file__).resolve().parents[2]
    course = json.loads((root / "data/sessions-372.json").read_text())
    for lesson in course["sessions"][:6]:
        slot = lesson["slot"]
        code = f"S{slot:03}"
        script = json.loads((root / f"production/scripts/{code}.json").read_text())
        assert lesson["type"] == "LESSON" and lesson["focus"] == script["title"]
        assert slot == script["course_slot"] and code == script["id"]
        stages = [scene["stage"] for scene in script["scenes"]]
        assert stages[:7] == ["INTRO", "EXAM", "PUZZLE", "BASIC", "PUZZLE", "MEDIUM", "PUZZLE"]
        assert all(stage == "HARD" for stage in stages[7:-2])
        assert stages[-2:] == ["MISTAKES", "RECAP"]


if __name__ == "__main__":
    check_examples()
    check_course_order()
    print("Verified the six original introductions and their course placements.")
