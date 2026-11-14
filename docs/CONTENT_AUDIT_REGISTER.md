# Content audit register

[The per-problem register](content-audit-register.csv) covers the 566 standard Try and Transfer problems across 283 lessons and 52 techniques. Run `python tools/content/build_audit_register.py` to regenerate it.

## 14 November 2026 full-bank audit

| Outcome | Problems |
|---|---:|
| Revised | 469 |
| Retained from earlier individually checked batches | 93 |
| Retained because of saved learner attempts | 4 |
| Individually read and independently recomputed | 566 |
| Repeated number-normalised stems | 0 |
| Figures and displays checked at both phone widths | 113 |

The audit checks each statement, its assumptions, units, requested answer, answer key and worked solution. Revisions range from clarifying a condition to replacing the entire problem. For transfer, the learner must decide how to apply the technique in a fresh setting. The difficulty estimates use [Australian Maths Trust Upper Primary examples](https://amt.edu.au/wp-content/uploads/2019/05/AMC-practice-problems-solutions-Set1-UPR.pdf) and the installed authentic AMC papers as reference. The similarity screen compares against all 570 installed questions, using OCR for image-backed prompts and human review of the closest matches. Number-normalisation can flag repeated templates. Mathematical similarity still requires editorial judgement.

The browser fixtures use the real lesson card and maths typesetter at 320 and 390 CSS pixels. They check prompt and solution overflow, cropped or overlapping diagram labels, mismatched figures and the normal answer-to-solution flow. The revised lessons use short final answers and show their reasoning in the worked solutions.

| Register column | Meaning |
|---|---|
| `id`, `session`, `technique`, `role`, `visit` | Canonical lesson mapping. The role is Try or Transfer. |
| `difficulty` | Existing app field: 3 for Try and 4 for Transfer. |
| `upper_primary_band` | Editorial estimate of where a question of comparable demand might appear on an AMC Upper Primary paper. |
| `content_fingerprint` | First 10 hexadecimal characters of the MD5 of the statement. |
| `assurance_level`, `verification_method` | The separate calculation that verifies the answer. |
| `same_structure_elsewhere` | Number of other prompts with the same stem after numerical wording and punctuation are normalised. |
| `individually_reviewed` | The prompt and worked solution were read individually. |
| `has_recorded_attempts` | Learner attempt state at the start of this audit. |
| `diagram` | Whether the question has a display tested in a phone-width fixture. |
| `status` | What the full-bank audit changed or retained. |

## Change log

### Data-reading batch: 14 November 2026

**Change.** Reauthored the 12 DATA-03 revisits. New problems ask learners to interpolate, combine pictogram keys, find a cumulative change, compare truncated axes, infer overlap and recover a median from frequencies. The first visit is retained. Four problems use bar charts and eight use accessible HTML tables.

**Problem IDs.** O104T O104X O141T O141X O173T O173X O232T O232X O323T O323X O355T O355X.

**Verification.** Independent recomputation checks all 12 answers. The lesson browser verifies that each display fits at 320 and 390 CSS pixels and that older stems never show a mismatched display. The live database matches the 12 generated rows. All authentic AMC fingerprints and the seven recorded attempts matched before and after the update.

### Spatial batch: 14 November 2026

**Change.** Revised all 30 later-visit problems in SPATIAL-02 (16) and SPATIAL-03 (14). Six SPATIAL-03 rows already had different live prompts and keys. Their mathematical ideas and keys were preserved, and their wording and diagrams were brought into the generator. The four first-visit problems remain as introductions. The new problems ask students to reason about missing edges, irregular grids, symmetry, constrained tilings, bounds and overlap. Twenty-nine have diagrams. The inverse square-grid problem leaves the board size for the learner to infer.

**Problem IDs.** O082T O082X O094T O094X O097T O097X O118T O118X O127T O127X O159T O159X O177T O177X O209T O209X O218T O218X O250T O250X O268T O268X O300T O300X O309T O309X O341T O341X O359T O359X.

**Verification.** Independent enumeration checks all 30 answers. Browser fixtures check diagram labels and safe handling of a stale question at 320 and 390 CSS pixels. The live database matches all 30 generated rows. The authentic AMC freeze and the seven recorded learner attempts had identical fingerprints before and after the database update. The Pages release published the client and diagram manifest.

### Batch 2: 14 November 2026

**Defect.** In ALG-02, SEQ-04, LOGIC-02, FRAC-02 and COUNT-01, every visit after the first reused the first-visit problem with different numbers.

**Change.** 60 problems reauthored with different mathematical structures and rising demand: ALG-02 (14), SEQ-04 (12), LOGIC-02 (12), FRAC-02 (12), COUNT-01 (10). First-visit problems were kept.

**Problem IDs.** O075T O075X O095T O095X O107T O107X O120T O120X O124T O124X O135T O135X O139T O139X O148T O148X O152T O152X O167T O167X O180T O180X O183T O183X O198T O198X O211T O211X O215T O215X O226T O226X O230T O230X O239T O239X O243T O243X O258T O258X O271T O271X O274T O274X O289T O289X O302T O302X O306T O306X O317T O317X O321T O321X O330T O330X O334T O334X O349T O349X.

**Files.** `tools/content/curated_batch2.py` (new), `tools/content/check_curated_batch2.py` (new), `tools/content/build_original_lessons.py`, `tools/content/audit_all_lessons.py`.

**Verification.**
- Each answer independently recomputed by brute force; uniqueness confirmed where the problem claims a single answer.
- Before the update, the 60 database rows were confirmed identical to the generator's previous output, so the previous content can be regenerated from Git history.
- None of the 60 had recorded attempts (0 attempts in the five families).
- After the update, the fingerprint of the 60 database rows matched the new generator output exactly.
- Authentic AMC fingerprints were unchanged.

**Not done.** No narration or video refers to these problems (`spoken_script` is empty for all of them), so no video mismatch was created. Wording was reviewed by the author of the batch only, not by a second reader or by the learner.

### Batch 1: 13 November 2026 (recorded from the repository)

DIV-03, ALG-04, DATA-02, DIG-03 and SOLID-01 later visits were reauthored in `curated_revisits.py`, with answers constrained to equal the existing keys.
