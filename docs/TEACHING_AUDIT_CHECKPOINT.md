# Summit One teaching audit — 12 November 2026

## Installed assessment archive

All 19 authentic Upper Primary papers from 2007 through 2025 are installed in the protected database. Each has 30 questions and 135 marks: 570 questions total. Existing learner records and the four previously installed papers were preserved.

2009–2022 use the family-supplied archive and its printed answer tables. The 2014 scan ends at Q27; Q28–30 use the previously authenticated transcriptions, checked against the archive key. The file formerly labelled AMC 2025 was a duplicate 2013 paper and was not treated as 2025.

2025 uses the eight newly supplied screenshots (book pages 13–20). All 30 have original worked explanations. Answers were independently solved; an official answer key was not supplied. Counting problems were additionally checked by exhaustive enumeration where suitable. The app labels this distinction. Original question images remain protected database content, not public repository files.

The archive contains 215 worked explanations; 355 earlier questions still have answer keys only. This is an explicit remaining content task, not a complete-solutions claim.

The temporary hash-allowlisted import function was replaced with an inert 410 response after import and JWT verification re-enabled. It has no remaining write capability.

## Teaching and interface release

- 52 explicit method cards, worked examples, guided checks and exit/retrieval questions.
- Delayed recall uses completed-session spacing; hints persist, and repeated identical answers cannot establish varied evidence.
- All 52 techniques appear by session 104; the 372-session plan and every-seventh-session MAWA cadence remain intact.
- Readiness distinguishes course completion from independent evidence and counts distinct perfect papers.
- Challenge selection prioritises topic fit, then novelty/difficulty, and updates recent attempt history immediately.
- Local draft recovery, queued cloud saves, saved work during stage changes, and review of locked completed sessions.
- Separate final answer and working fields; strict server marking does not extract the first number from prose.
- First-attempt independent credit; video viewing remains viewed evidence only.
- Full-paper results history, integer-save status, save-failure rollback and enlarged original question images.
- Smaller headings, quieter background, compact mobile navigation and visible keyboard focus.
- Corrected exponents in K001, K007, K015, K022 and teaching T04.1/T04.2. Those four challenge videos are bypassed in favour of the corrected text/audio. Approved T02.1/T02.2 masters are unchanged.
- Narration cache identity now includes the exact transcript and voice settings.

## Validation

`node tools/check_learning.mjs` checks exercise generation, independent enumerations, technique coverage, investigation cadence, delayed-evidence rules, strict parsing and exam grading.

`tools/browser_checks.py` runs synthetic learner interactions in Chrome without reading or changing a real learner's account. It checks desktop/mobile navigation, hint recording, working persistence, saved/unsaved exam responses and failure rollback. GitHub Actions runs these checks before release; screenshots are retained as workflow artifacts.

Release QA checks canonical counts, JavaScript syntax and public-content/media safety. Database verification checks 19 complete papers, marks, protected answer-column access and required login. Security advisors report only the two existing intentionally policy-less server-only tables.

## Remaining work

- Add the missing 355 worked explanations, carefully verified against source questions.
- Obtain an official 2025 key for independent cross-checking (the current paper is independently solved and labelled).
- Continue the wider video production programme; only approved masters should be offered as finished videos.
- Extend transfer questions and proof review beyond short generated checks; delayed checks are not a claim of exam mastery.
- Future MAWA/Rossmoyne dates must be checked when published. A 2028 Year 6 Rossmoyne test normally targets Year 7 entry in 2029.

No claim of a guaranteed perfect score or a completely finished course is made.

## Session teaching sequence revision — 12 November 2026

All 372 positions now have an explicit opening. The 283 lessons use 52 authored technique introductions with purpose, recognition cues, prerequisites, a small three-step worked example and a larger worked application. Repeated visits have a new purpose (recall, recognise, choose, test limits). The seven mixed capstones explicitly pair methods instead of falling through to an unmapped focus.

The 53 investigations use 20 distinct smaller worked investigations and purpose statements. The 36 scheduled rehearsals introduce strategy selection, preparation and post-test repair before the timer starts.

Lesson order is purpose → small model → worked application → supported attempt → independent basics check → archive stretch → transfer → reflection. The independent basics check moved from the end to before archive challenges. Guided/core attempts unlock challenge work, including when the learner needs support; correctness is not used to block progress. Existing completed records remain unchanged. Archive selections are ordered by stored difficulty, which is an approximation rather than a guarantee of perceived difficulty.

Validation enumerates all 372 openings, technique and investigation coverage, and tests the supported-to-independent-to-stretch route in Chrome, together with MAWA, rehearsal and capstone openings on mobile.
