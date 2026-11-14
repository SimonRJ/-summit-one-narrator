# Summit One current status

**14 November 2026.** The repository, public site and live database are verified separately. See [the lesson audit register](CONTENT_AUDIT_REGISTER.md) for the editorial checks and [the continuation](CHATGPT_CONTINUATION.md) for the release procedure.

## Content inventory

| Item | Count |
|---|---:|
| Course sessions | 372, comprising 283 lessons, 53 investigation visits and 36 mock slots |
| Techniques | 52 |
| Standard Try and Transfer problems | 566 |
| `content_problems` rows | 760, comprising 608 original and 152 authentic-linked |
| Learner attempts at the start of the audit | 7 on O001T, O001X, O002T and O002X |
| Exam sittings at the start of the audit | 0 |

## Standard lesson bank

| Check | Result |
|---|---:|
| Prompts and worked solutions individually reviewed | 566 of 566 |
| Answers checked by a separate calculation or enumeration | 566 of 566 |
| Revised in the full-bank audit | 469 |
| Retained after an earlier individual review | 93 |
| Retained as saved, with learner attempts | 4 |
| Distinct titles and number-normalised stems | 566 each |
| Repeated number-normalised stems beyond the first occurrence | 0 |
| Figures, charts and tables rendered at 320 and 390 CSS pixels | 113 |

The audit began after the earlier spatial and data-reading batches, when 286 problems still shared an earlier number-normalised stem. This pass reviewed the remaining 464 problems and followed up on nine from earlier batches. The originality screen used the installed 19-paper archive, including OCR for 447 image-backed questions, and manual comparison of the closest matches. The difficulty bands in the register are estimates of the reasoning demanded by Upper Primary questions at those positions.

| Estimated AMC Upper Primary band | Problems |
|---|---:|
| Q1–10 | 2 |
| Q11–20 | 204 |
| Q21–25 | 302 |
| Q26–30 | 58 |

The checks cover the 566 standard lesson problems. Retrieval cards, extra technique drills, MAWA investigations, original practice papers and Rossmoyne mocks have their own content and release status.

### Release verification

The revised lesson data and diagrams are prepared for release. The final live database and Pages verification is tracked separately from repository checks. The learner's account is left untouched during browser testing. A fixture account exercises answer submission, diagram rendering, solution reveal, locked review and navigation.

## Examination papers

| Category | Active | Inactive | Notes |
|---|---|---|---|
| Authentic AMC past papers | 19 papers, 570 questions | none | Frozen. See [authentic AMC freeze](AUTHENTIC_AMC_FREEZE.md). |
| Original AMC Part A / Part B split papers | 4 entries, 60 questions | 1 entry, 10 questions | Earlier plan called for about 30 sets per part. |
| AMC split familiarisation sets | none | 20 entries, 300 questions | Uses earlier questions. |
| Original authored mocks | 9 Rossmoyne-style papers, 207 questions | 10 AMC-style papers, 300 questions | |
| Earlier Summit-authored mocks | none | 25 papers, 750 questions | Retired. |
| Earlier Rossmoyne-authored mocks | none | 11 papers, 253 questions | Retired. |
| User-supplied original sample | 1 paper, 23 questions | none | |

## Videos and guides

| Item | Status |
|---|---|
| Teaching videos | 72 planned, with T02.1 and T02.2 finished and approved |
| Teaching scripts | 70 drafts |
| Other finished public videos | AMC introduction, welcome, two session introductions and one AMC solution pilot |
| Guides | [Student guide](STUDENT_GUIDE.md) and [parent guide](PARENT_GUIDE.md) |

## Verification commands

| Command | Checks |
|---|---|
| `tools/content/audit_all_lessons.py` | Canonical IDs, title and stem uniqueness, wording and required answer format |
| `tools/content/check_reviewed_lessons.py` | Answer calculations, fingerprints of checked prompts and exact agreement with the public diagram manifest |
| Both commands with `--solutions PATH` | Comparison of all 566 private answer keys to the calculations and consistency of final-answer lines |
| `tools/content/check_curated_{batch2,spatial,data}.py` | Independent checks for the earlier three releases |
| `tools/browser_lesson_fixed.py` | Layout of every prompt and figure at 320 and 390 CSS pixels and the lesson flow across phones, tablets and desktop |
| The browser test with `SUMMIT_ONE_LESSON_SOLUTIONS` set | Layout of all 566 worked solutions at both phone widths |
| `tools/check_learning.mjs`, `tools/check_fixed_lesson.mjs`, `tools/check_split_training.mjs` | Course mapping, lesson behaviour and AMC split structure |
| `tools/check_amc_freeze.sql` | Read-only fingerprints of the authentic archive and recorded attempts |
