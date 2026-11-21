"""Keep the public review list consistent with the two film editorial registers."""
import argparse
import csv
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
WATCH_LIST = ROOT / "lesson-video-review-list.html"
ROW = re.compile(r'<tr><th scope="row">([ST][^<]+)</th>[^\n]*?</tr>\n?')


def approved(name):
    with (ROOT / "docs" / name).open(encoding="utf-8", newline="") as source:
        return {row[0] for row in csv.reader(source) if row[3] == "final editorial review complete"}


def reconcile(page):
    films = approved("teaching-video-review-register-20261116.csv")
    intros = approved("lesson-introduction-review-register-20261116.csv")
    permitted = films | intros
    listed = ROW.findall(page)
    if len(listed) != len(set(listed)):
        raise ValueError("A film appears more than once in the public tables.")
    missing = permitted - set(listed)
    if missing:
        raise ValueError("Add a runtime and verified player URL for: " + ", ".join(sorted(missing)))
    page = ROW.sub(lambda m: m[0] if m[1] in permitted else "", page)
    page = re.sub(r'(href="#revised-teaching-films">)[^<]*',r'\1Teaching films',page)
    page = re.sub(r'(href="#revised-lesson-introductions">)[^<]*',r'\1Lesson introductions',page)
    prior = films.intersection({"T02.1", "T02.2"})
    page = re.sub(r'These \d+ teaching films', f'These {len(films-prior)} teaching films', page)
    page = re.sub(r'\d+ of 283 lesson introductions are reviewed and live',
                  f'{len(intros)} of 283 lesson introductions are reviewed and live', page)
    return page


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    original = WATCH_LIST.read_text(encoding="utf-8")
    updated = reconcile(original)
    if args.write:
        WATCH_LIST.write_text(updated,encoding="utf-8")
    elif original != updated:
        raise SystemExit("Sync the review list after changing a film's editorial status.")
