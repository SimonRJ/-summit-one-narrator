"""Compile original introduction storyboards for the canonical course lessons."""

import argparse
from collections import Counter
import json
from pathlib import Path

from algebra_topics import backwards, differences, margins, part_whole, recurrence, simultaneous, word_equations
from count_topics import restricted_arrangements
from counting_cases import complement, double_counting, enumeration, partition_cases, selections
from deduction_topics import deduction, exhaustiveness, magic_grid
from spatial_topics import crossings, layered_cubes, optimise, perimeter, shaded_area, tiling
from quantity_topics import averages, distance_speed, percentages, ratios, relative_motion, unit_rates, weighted_fractions, work_rates
from logic_topics import graphs, truth_liars
from number_topics import arithmetic_sequence, cryptarithms, cycles, divisibility, doubling, finite_state, multiples, parity, primes, repunits
from story import Lesson, film


ROOT = Path(__file__).resolve().parents[3]
BESPOKE = {f"S{slot:03}" for slot in range(1,7)}
TOPICS = {
    "Constraint elimination and logical deduction": deduction,
    "Magic grids, symbolic rules and consistency": magic_grid,
    "Proving all cases and unique solutions": exhaustiveness,
    "Systematic enumeration without missing cases": enumeration,
    "Multiplication principle and combinations": selections,
    "Complement counting and inclusion–exclusion": complement,
    "Double-counting and shared objects": double_counting,
    "Partitioning into non-overlapping cases": partition_cases,
    "One- and two-variable word equations": word_equations,
    "Simultaneous and total-sum constraints": simultaneous,
    "Eliminating an unknown by differences": differences,
    "Winner margins, shared totals and linear rules": margins,
    "Reading and reasoning from graphs/tables": graphs,
    "Arithmetic sequences and fixed increments": arithmetic_sequence,
    "Doubling, geometric growth and finite sums": doubling,
    "Repeating transformations and finite-state patterns": finite_state,
    "Optimising areas and lengths under constraints": optimise,
    "Area decomposition and shaded complements": shaded_area,
    "Unit-cube counting and layered solids": layered_cubes,
    "Combined work rates": work_rates,
    "Truth-tellers, liars and contradiction": truth_liars,
    "Distance–speed–time reasoning": distance_speed,
    "Relative speeds, timed movement and meetings": relative_motion,
    "Polyominoes, tiling and shape assembly": tiling,
    "Perimeter, shared edges and boundary effects": perimeter,
    "Averages, weighted means and simple distributions": averages,
    "Fractions, percentages and proportional comparisons": percentages,
    "Ratio and scale factors": ratios,
    "Unit conversion and repeated-event rates": unit_rates,
    "Grouped fractions and weighted totals": weighted_fractions,
    "Working backwards through operations": backwards,
    "Recurrence relations, steps and branching": recurrence,
    "Parts and wholes, including remaining fractions": part_whole,
    "Restricted arrangements and neighbour rules": restricted_arrangements,
    "Grid lines, crossings and coordinates": crossings,
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
