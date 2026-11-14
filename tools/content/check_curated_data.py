"""Recompute each chart and table answer and verify the published lesson mapping."""
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
from statistics import mean, median
import json
import tempfile

from audit_all_lessons import map_course
from build_original_lessons import build
from curated_data import DATA_REVISITS


def main():
    choice_totals = [(apple, pear, both) for apple, pear, both in product(range(31), repeat=3)
                     if apple + pear + both == 30 and apple + both == 24 and pear + both == 16]
    assert len(choice_totals) == 1
    totals = (6, 4, 7, 5)
    pairs = [pair for pair in combinations(range(4), 2)
             if sum(totals[i] for i in pair) == sum(totals[i] for i in range(4) if i not in pair)]
    readings = [0, 9, 13, 25, 30]
    expected = {
        (2, 'try'): sum((a+b)//2 for a,b in [(20,24),(32,36)]),
        (2, 'transfer'): abs(Fraction(9,2)*6 - Fraction(9,2)*8),
        (3, 'try'): next(n for n in range(81) if 16+12+20+n+14 == 80),
        (3, 'transfer'): abs((35+2*5)-(20+2*5)),
        (4, 'try'): sum(choice_totals[0][:2]),
        (4, 'transfer'): max(range(1,len(readings)), key=lambda i: readings[i]-readings[i-1]),
        (5, 'try'): Fraction(70,1) / (Fraction(5,2)+Fraction(9,2)),
        (5, 'transfer'): mean((7,8,15,10)),
        (6, 'try'): len(pairs),
        (6, 'transfer'): median((4,)*3+(6,)*5+(8,)+(10,)*3),
        (7, 'try'): 5*32-5*20,
        (7, 'transfer'): str(Fraction(24,20)),
    }
    assert expected == {key:q['answer'] for key,q in DATA_REVISITS.items()}, expected
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp)
        build(map_course(), out)
        manifest = json.loads((out/'lesson-manifest.json').read_text())['items']
        published = json.loads((Path(__file__).resolve().parents[2]/'data/lesson-challenges.json').read_text())['items']
        assert [m for m in manifest if m['skill']=='DATA-03'] == [m for m in published if m['skill']=='DATA-03']
    print('PASS: 12 data-reading answers independently recomputed and matched to the published displays.')


if __name__ == '__main__':
    main()
