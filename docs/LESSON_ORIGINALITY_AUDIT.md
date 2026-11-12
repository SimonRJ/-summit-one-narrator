# Original teaching and transfer audit — 12 November 2026

The daily challenge selector previously admitted all 152 authentic AMC challenge records. Teaching sessions now use an explicit, original-only curriculum manifest. There is no fallback to a real paper or a broad category search. Real AMC questions remain in the separate Test Centre and its post-exam solution reviews.

## Coverage and changes

- All 372 course positions checked: 283 teaching lessons, 53 MAWA investigation visits, 25 authored AMC mocks and 11 authored Rossmoyne mocks.
- 566 distinct original problem statements assigned to the 283 teaching lessons, two per lesson. These are variants of 104 technique/application families, with seven additional mixed capstone tasks. A numerical variation is labelled familiar practice after its family has been seen; it is not counted as a newly mastered structure.
- All 52 technique introductions and small worked examples, 364 generated guided/recall variants, 72 teaching transcripts/readings, 20 investigation warm-ups, 20 investigation bases and 20 new changed-situation tasks screened.
- The 1,003 questions in the 36 authored course mocks screened. These remain labelled practice, not official AMC/MAWA/Rossmoyne papers.
- A five-person alternating liar exercise was mathematically the same as archive A002 despite different wording. Replaced the entire LOGIC-01 exercise family with a different truth-constraint problem.
- All 20 MAWA investigations now contain a concrete changed-situation problem and model reasoning. Later visits also require changing a condition and justifying a generalisation or counterexample.
- The seven mixed capstones explicitly combine their two advertised tools.
- Existing narration/videos were retained where their teaching content passed this screening. The approved real AMC solution pilot remains in post-exam review, not daily lessons.

## Source comparison

Comparison corpus: 570 Upper Primary questions from the installed 2007–2025 papers, plus 152 authenticated Middle/Upper Primary archive records (there is overlap between those sources). Text was recovered from source transcriptions, PDF crop text, 2014 OCR and the user's genuine 2025 screenshots. The separately named “AMC 2025” PDF has different questions and was not substituted for those screenshots.

The final screen compared 2,117 teaching/practice entries with 722 source references. It found no exact or contained normalized-text matches. Four-word overlap candidates were reviewed by question meaning, quantities and constraints; ordinary wording such as “sum of the digits” was distinguished from copying a complete exam problem. The truth-and-liars match was changed rather than merely renamed.

This is an audit against the installed archive, not a claim to have searched every AMC paper or every possible diagram worldwide. OCR and textual similarity are imperfect, especially for diagram-only questions. The stronger ongoing protection is provenance: real paper records cannot enter the active lesson selector, and the submission endpoint rejects authentic AMC questions attached to teaching sessions.

## Learning evidence

A lesson follows purpose and recognition clues → two small worked examples → guided practice → independent basics → original application → changed setting → check and reflection.

Before submitting either challenge, the learner records the problem clue and why the plan fits. Notes/help are recorded separately. After attempting, the learner records an independent check or correction and chooses a confidence reflection. A wrong answer does not lock the learner out; checking and repairing it is part of learning.

Answer checking does not claim to verify the quality of a written proof. Explanations remain saved for review. Repeated patterns, supported answers, course completion and watched videos do not earn new-transfer evidence. Existing completed records remain immutable; unfinished legacy work is retained while its active questions are replaced with original tasks.

## Verification

- Node checks cover all lesson mappings, original-only rejection, missing-content rejection, support/familiarity classification, all 372 openings and all 53 seventh-session investigation positions.
- Python independently checks generated answers through enumeration, rational arithmetic, graph/path counts, geometric bounds and the combined capstones.
- Database content hashes checked against all 566 authored records before release. Genuine past-paper records and student progress were not modified.
- Browser checks cover the clue/plan gate, help recording, check/reflection gate, mobile layout, saved working, legacy-draft preservation, existing exam navigation and sign-in.

## Maintenance

`data/lesson-challenges.json` is the answer-free curriculum manifest. `tools/content/build_original_lessons.py` is the original-content authoring source, and `tools/content/check_original_lessons.py` checks its mathematics. Generate protected payloads outside the Pages data directory. The real exam corpus must also stay outside public teaching data. After any new authoring or paper import, rerun the text comparison and review semantic/diagram candidates; do not infer originality just from a new ID or changed character names.
