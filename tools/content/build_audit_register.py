"""Build the per-problem audit register for the 566 standard lesson problems.

Writes docs/content-audit-register.csv. The register contains no prompts, answers or
solutions: only identifiers, a short content fingerprint and review status, so it is
safe in the public repository.

It deliberately separates three levels of assurance:
  * structural      - passes tools/content/audit_all_lessons.py
  * family_check    - its generator family is recomputed by check_original_lessons.py
  * independent     - this exact problem is recomputed by check_curated_batch2.py

Run: python tools/content/build_audit_register.py
"""
import csv, hashlib, json, sys, tempfile
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from audit_all_lessons import map_course, numeric_skeleton
from build_original_lessons import build
from curated_batch2 import B as BATCH2
ROOT = Path(__file__).resolve().parents[2]
BATCH1 = ('DIV-03', 'ALG-04', 'DATA-02', 'DIG-03', 'SOLID-01')
ATTEMPTED = {'O001T', 'O001X', 'O002T', 'O002X'}  # recorded attempts at the 2026-11-14 database check

def main():
    with tempfile.TemporaryDirectory() as t:
        build(map_course(), Path(t))
        rows = json.loads((Path(t) / 'original-problems.json').read_text())
        manifest = {m['id']: m for m in json.loads((Path(t) / 'lesson-manifest.json').read_text())['items']}
    shape = Counter(numeric_skeleton(r['prompt']) for r in rows)
    out, tally = [], Counter()
    for r in rows:
        m = manifest[r['id']]
        key = (r['category'], m['role'], m['visit'])
        shared = shape[numeric_skeleton(r['prompt'])] - 1
        if key in BATCH2:
            level, method, reviewed, status = 'independent', 'brute-force recomputation (check_curated_batch2.py)', 'authored and read individually 2026-11-14', 'Verified and suitable'
        elif r['category'] in BATCH1 and m['visit'] >= 2:
            level, method, reviewed, status = 'family_check', 'curated rewrite asserted equal to generator key (curated_revisits.py)', 'reauthored 2026-11-13; not re-read in this audit', 'Correct by family check; awaiting individual review'
        else:
            level, method, reviewed = 'family_check', 'generator family recomputed (check_original_lessons.py)', 'not individually reviewed'
            status = 'Repetitive and requires redesign' if shared else 'Correct by family check; awaiting individual review'
        tally[status] += 1
        out.append(dict(id=r['id'], session=m['session'], technique=r['category'], role=m['role'], visit=m['visit'],
                        difficulty=r['difficulty'], content_fingerprint=hashlib.md5(r['prompt'].encode()).hexdigest()[:10],
                        assurance_level=level, verification_method=method, same_structure_elsewhere=shared,
                        individually_reviewed=reviewed, has_recorded_attempts='yes - frozen' if r['id'] in ATTEMPTED else 'no',
                        diagram='none (text only)', status=status))
    path = ROOT / 'docs/content-audit-register.csv'
    with path.open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
    distinct = len(shape)
    print(json.dumps(dict(problems=len(out), distinct_structures=distinct, repeated_occurrences=len(out) - distinct,
                          independently_recomputed=sum(o['assurance_level'] == 'independent' for o in out), status=tally), indent=1))

if __name__ == '__main__':
    main()
