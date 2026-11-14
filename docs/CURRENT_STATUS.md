# Summit One: current verified status

**As of 14 November 2026.** Every figure here was read from the live database or produced by a test run on that date. Where something was not checked, it says so.

## Content inventory

| Item | Count | How it was checked |
|---|---:|---|
| Course sessions | 372 (283 lessons, 53 investigation visits, 36 mock slots) | `data/sessions-372.json`, `audit_all_lessons.py` |
| Techniques | 52 | `data/taxonomy-52.json` |
| Standard lesson problems | 566 | generator build; database rows `O###T` / `O###X` |
| `content_problems` rows | 760 = 608 original + 152 authentic-linked | database query |
| Learner problem attempts | 7, all on `O001T`, `O001X`, `O002T`, `O002X` | database query |
| Exam sittings | 0 | database query |

## Examination papers

| Category | Active | Inactive | Notes |
|---|---|---|---|
| Authentic AMC past papers | 19 papers, 570 questions | none | Frozen. See AUTHENTIC_AMC_FREEZE.md. |
| Original AMC Part A / Part B split papers | 4 entries, 60 questions | 1 entry, 10 questions | The earlier planning target was about 30 Part A and 30 Part B sets. That target has not been met. |
| AMC split familiarisation sets | none | 20 entries, 300 questions | Reused questions; not new content. |
| Original authored mocks | 9 papers, 207 questions (Rossmoyne-style) | 10 papers, 300 questions (AMC-style) | |
| Earlier Summit-authored mocks | none | 25 papers, 750 questions | Retired; do not reactivate without review. |
| Earlier Rossmoyne-authored mocks | none | 11 papers, 253 questions | Retired. |
| User-supplied original sample | 1 paper, 23 questions | none | |

## Structural repetition in the lesson bank

A "structure" is a problem statement with its numbers removed. Problems that share a structure differ only in their numbers.

| Date | Distinct structures | Rows sharing an earlier structure |
|---|---:|---:|
| 13 Nov 2026 (historical audit) | 122 | 444 |
| 14 Nov 2026, start of session | 178 | 388 |
| 14 Nov 2026, after batch 2 | 238 | 328 |
| 14 Nov 2026, after the spatial batch | 268 | 298 |

Twelve of the 52 technique families now have no repeated structure at all: DIV-03, ALG-04, DIG-03, DATA-02, SOLID-01 (batch 1) ALG-02, SEQ-04, LOGIC-02, FRAC-02, COUNT-01 (batch 2) and SPATIAL-02, SPATIAL-03 (spatial batch). The other 40 families still need redesign. The highest counts remaining are DATA-03 (12), then SOLID-02, RATE-01, RATE-02, GEO-03, FRAC-01, DIG-04 and COUNT-04 (10 each).

## Levels of assurance for the 566 lesson problems

| Level | Problems | Meaning |
|---|---:|---|
| Independently recomputed and read individually | 90 | Each answer is recalculated by its own brute-force check; each statement and solution was written and read in this batch. |
| Family check only | 476 | The generator formula for the family is recomputed over all visits. The individual statement, wording and solution have not been read one by one. |

"566 problems pass structural checks" is true. "566 problems independently solved and reviewed" is not: the figure is 90.

## Videos

| Item | Count |
|---|---:|
| Teaching videos planned | 72 (54 concept, 18 worked example) |
| Finished and approved | 2 (T02.1, T02.2) |
| Script ready, nothing recorded or animated | 70 |
| Other finished public videos | AMC introduction, welcome, two session introductions, one AMC solution pilot |

## What the tests prove

| Test | Proves | Does not prove |
|---|---|---|
| `check_learning.mjs`, `check_fixed_lesson.mjs`, `check_split_training.mjs` | Course mapping, original-only lesson selection, screen structure, split-paper structure | Mathematical correctness of content |
| `check_original_lessons.py` | Each generator family's answer formula agrees with an independent calculation on every visit | That curated rewrites read well; that solutions explain clearly |
| `check_curated_spatial.py` | All 30 spatial answers match independently enumerated configurations and the generated diagrams match the public lesson manifest | The wording and the written explanation, checked separately |
| `check_curated_batch2.py` | Each of 60 problems has the stated answer, and a unique one where uniqueness is claimed | Wording quality, which was checked by reading |
| `audit_all_lessons.py` | IDs, titles, final-answer lines, banned wording, no repeated structure in the twelve reauthored families | Correctness of answers |
| `audit_generated_papers.py` | Option-to-key mapping, numeric keys, SVG well-formedness in 507 generated mock questions | That diagrams are mathematically right or legible |
| `build_scripts.py --check` | All 70 scripts have the required stages, speech-friendly narration and a notebook exercise | That the mathematics in each script is right; that was checked by reading |
| Browser tests in CI | Lesson navigation and layout at phone, tablet and desktop sizes | Visual quality of every screen |

All of the above passed on 14 November 2026.

## Known limitations

1. There are 298 repeated occurrences beyond the first instance. Including the first instance in each repeated group, 378 lesson problems share a structure.
2. 476 lesson problems have not been individually read and solved by a reviewer.
3. No diagram was visually inspected in this session. Lesson problems in the twelve reauthored families are text only.
4. Original AMC Part A and Part B content is far short of the planned volume.
5. Rossmoyne papers, MAWA investigations, the 52 advanced-connection pages, the interface and the Supabase security rules were not audited in this session.
6. 70 teaching videos exist only as scripts.
7. Student, parent, database, deployment and QA guides are not yet written.
