# AMC split-training release · 13 November 2026

## Learner-centred architecture

The student sees only two primary top-level destinations: **Learning** (372 sessions, including 53 MAWA investigation slots) and **Exams** (six clear types). All exams use the existing separate, authenticated simulator and its permanent submission records. Solving mistakes routes back to Learning's repairs. Previously completed lessons, papers, attempt history, account, and existing video access are unaffected.

### AMC Q1–20: fluency

* Original AMC question numbers 1–20, all multiple choice.
* 20 questions, 70 marks: Q1–10 3 marks; Q11–20 4 marks.
* Count-up clock; 20-minute maximum, automatically seals at the cap.
* Accuracy first. First-attempt **20/20** is the standard. Fastest perfect time on a *new* paper is the useful pace comparison; an identical repeat is mainly memorisation/fluency rehearsal.
* Preserve first/best score, elapsed time per sitting, incomplete attempts, permanent review and individual corrections.

### AMC Q21–30: reasoning

* Original AMC numbers 21–30; Q21–25 five-choice MC; Q26–30 integer answers with explicit Save.
* 10 questions, 65 marks: five × 5, then 6, 7, 8, 9 and 10.
* Count-up clock; 40-minute maximum, automatically seals at cap.
* Aim to secure five MC questions and one integer as an excellent **early benchmark**, while gradually reaching 10/10; do not suggest six questions guarantee any award.
* Track MC and integer accuracy distinctly, as well as raw marks/time and problem type.

### Full AMC and other assessments

* Keep 30Q/135 marks/60-minute full AMC papers intact and still available: 10 repeatable authored full mocks and 19 authentic Upper Primary papers (one attempt each).
* Keep 9 Rossmoyne authored mocks + uploaded original sample, 100 marks, unchanged.
* MAWA is linked from the Exam hub but the current 53 investigations remain untimed in the Learning path: do not falsely present them as official timed MAWA tests.
* All modes preserve formal navigation, saved answers, integer Save semantics, one-attempt rules for authentic exams, end confirmation, gap/unsaved warnings, immutable result snapshots and post-exam explanations. Nothing leaks answers or hints during a sitting.

## Current question-bank provenance and status

On 13 November, **20 split familiarisation sets** were constructed using the 10 already-authored, active full AMC mocks:

* 10 Q1–20 sets = 200 questions shown; reused from the full papers.
* 10 Q21–30 sets = 100 questions shown; reused from the full papers.
* They are labelled **REUSED FAMILIARISATION**, not counted as new problems, and have stable source references.
* Each reuse is intentionally visible to the student, as returning to a remembered problem is not evidence of transfer to unseen mathematics.
* Both parts were validated against live catalog counts, question counts, original question numbers, marks, answer types and populated explanations.
* The older 25 retired AMC mocks include routine and repeated formats and **must not** be passed off as fresh elite-level material.

## Independently checked new split sets (verified 13 November 2026)

Three distinct active original sets now supplement the twenty reused familiarisation sets:

* **Original Fluency · Set 01 (pilot):** 20 original multiple-choice problems, 70 marks, 20 minutes; saved in protected database as `summit-amc-speed-original-pilot-01`.
* **Original AMC Fluency 01:** a further 20 original multiple-choice problems, 70 marks, 20 minutes; `summit-amc-speed-original-01` (v2 after removing a structural duplicate corner-perimeter problem).
* **Original AMC Challenge 01:** ten original difficult problems with 5 MC and 5 integer answers, 65 marks, 40 minutes; `summit-amc-depth-original-01`. Four newly drawn instructional *question* diagrams accompany these problems; detailed fully worked explanations and independent enumeration checks confirm the answer keys.
* The **active split bank is 23 sets**: 12 fluency and 11 challenge. Of these, 20 reuse the 10 existing full mocks and 3 are new original sets containing 50 new questions altogether.
* A previous exploratory challenge pilot, `summit-amc-depth-original-pilot-01`, was held back after calibration: it contains several patterns too easy for the final AMC positions, and its Catalan-path problem overlapped mathematically with the stronger independent challenge set. It remains in database history but is not active.
* The count of original exam-quality papers requested by the parent is **not yet met**. Do not label reused familiarisation sets as new or count inactive pilots as complete.

## New original bank: editorial release specification

The next content milestone is 20–50 **additional** genuinely new, independently verified papers, not 20–50 number substitutions or rearrangements. Target at least 30 independent Q1–20 fluency sets and at least 30 independent Q21–30 challenge sets, staged in small audited batches. Each new exam must remain hidden/inactive until it passes all checks.

Every question record must have:
- a unique stable source ID, paper, exact AMC question number and score;
- topic and skill-family tags; prerequisite and strategy demands; a precise independent solution;
- five plausible, distinct, *diagnostic* MC distractors, or correct 0–999 integer answer;
- diagrams when reasoning genuinely depends on spatial relationships;
- provenance (original / user-supplied reference inspiration), structural-originality reasoning, solution verification method, reviewer sign-off;
- a fully worked solution explaining the idea, checking steps, and common pitfalls.

**Originality gate:** classify the mathematical mechanism (e.g. lattice walk, digit invariant, adversarial game, non-obvious colouring), not just noun changes. Compare new tasks against all existing AMC and authored mocks, the APSMO pages, the George Lenchner contest collection, and the AMT problem-solving book. Near-duplicates, cloned solutions with relabelled variables, answer leakage, or ambiguity remain quarantined. A claimed “new” question must have a genuinely different path of insight or combination of ideas.

**Difficulty gate:** use authentic Upper Primary year-by-year calibration: 1–10 approachable, 11–20 fluency with some reasoning, 21–25 multi-step unfamiliar MC, 26–30 harder insight requiring structured reasoning rather than brute-force calculation. AMC authenticity is judged by strategy selection, cognitive demand, diagram clarity, and distractors—not by artificially large numbers.

**Math validation:** solve every newly authored question independently of the keyed answer; check all answer choices, numerical conditions, alternate readings and all diagrams. For finite constructions use a second programmatic enumeration when appropriate. Add a problem-specific explanation of why tempting wrong choices fail. Do not publish until both solution and independent QA pass.

**Rights:** user-uploaded photos of *Building Confidence in Maths Problem Solving*, Volume 1 (APSMO/Pauline Kohlhoff), the George Lenchner *Math Olympiad Contest Problems for Elementary and Middle Schools*, and AMT *Methods of Problem Solving Book 3* may inform topics and teaching techniques. Do not copy entire questions, solutions, photographs, book diagrams or published test material into the publicly accessible site without permission. Reference books are not a free question bank.

## Design standard

* Serious, calm, academically ambitious visual hierarchy—not cartoon themes, high-score confetti or daily streak pressure.
* Clear mobile-first Reading / Thinking / Responding affordances. Keep current authorised login and progress intact.
* Two unmistakable destinations; a single primary action (“Continue session”), with clear but subordinate paths to exams.
* Show scores and elapsed times honestly; distinguish *first attempt on unseen problem* from replay.
* Existing high-quality T02.1-style concept films remain the video benchmark: visual and spoken mathematics perfectly aligned, polished progressive diagrams, slow explanatory steps, accessible captions. No videos were modified by this release.

## Acceptance tests

- [ ] 20-minute Q1–20 starts at 00:00 and rises; server deadline still ends at 20:00.
- [ ] 40-minute Q21–30 starts at 00:00 and rises; server deadline still ends at 40:00.
- [ ] Both sections show original AMC question numbers and correct 70/65 mark totals.
- [ ] Result summary shows score, correct count, split MC/integer breakdown and elapsed time; first, best and fastest-perfect history are visible.
- [ ] End prompt accurately says “elapsed” rather than “time left” where count-up is displayed.
- [ ] Refreshed/reopened exam cannot reset countdown/deadline; submitted answers locked.
- [ ] Existing full authentic and original AMC and Rossmoyne functionality unchanged.
- [ ] MAWA entry links back to investigation learning, and does not invent an official MAWA test.
- [ ] All saved user progress and prior exam results remain available.
- [ ] Written solutions remain hidden until submission; protected-video gating retained.
- [ ] iPhone-responsive browse/learn and keyboard accessible navigation; tablet/desktop target for official-like exam rehearsal.
- [ ] 20–50 **new** papers may be labelled new only after distinct question creation, source checks and independent grading validation (not completed in this release).
