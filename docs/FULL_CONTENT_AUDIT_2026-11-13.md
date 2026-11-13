# Summit One — full-content audit register
**Audit date:** 13 November 2026  
**Focus:** AMC-aligned mathematics, accurate problems and worked solutions, visual presentation, originality, accessibility and reproducible checks

## Scope and inventory

The Supabase content database contains **3,233 stored question records** in two independently sourced areas:

| Area | Records | Status and use |
|---|---:|---|
| `content_problems` | 760 | 608 original authored and 152 authentic AMC-linked |
| Standard lesson problems `O###T/X` (subset above) | 566 | Two protected questions in each of 283 lesson sessions |
| Other original authored content (subset above) | 42 | Separately structured challenge/research problems |
| `exam_questions` | 2,473 | Across 100 stored exam catalog entries |
| **Active exam questions** (subset of exam bank) | **860** | Across 33 active exams |
| Active AMC past papers | 570 | 19 Upper Primary papers, 2007–2025 |
| Active Summit-authored mock questions | 267 | 207 in nine authored full practice papers and 60 in active AMC split sets |
| Active user-supplied original sample | 23 | Separate paper and its source-specific layout |
| Inactive exam questions | 1,613 | Archived/retired banks, deliberately not treated as active practice material |

There are also **52 technique families**, **20 MAWA investigation themes**, flash-choice decks, short practice questions, original teaching examples, and advanced mathematical connection pages. These must be reviewed as pedagogical content in addition to the stored question tables.

## Changes applied and verified

1. The entire protected lesson bank of 566 questions has had the repeated typed-reasoning/reflection instructions removed. The final answer remains assessed, and the original recorded attempts and scoring IDs are preserved.
2. All 554 generic "Workshop problem" / "A new setting" lesson titles were replaced with meaningful technique-specific titles. The resulting 566-question bank has 115 distinct titles, including prior bespoke corrections.
3. All 566 standard lesson solutions retain a final answer and their mathematical steps, but no longer carry the repeated "Recognise / Step 1 / Step 2 / Check" labels.
4. Thirteen explanations that referred to source-code variables not defined in the question were rewritten with the actual numerical dimensions and a check of the result.
5. Artificial or misleading recurring scenarios were rewritten, including meters adding unnamed units, robots spending money, badge machines, complete batches with leftovers, odometer logs and purposeless flashing lamps. Later-visit variants were included. The generator was updated so old wording cannot be restored by a rebuild.
6. Student-facing failures loading protected worked solutions now give clear feedback and a retry path, without bypassing the requirement for a recorded final answer.
7. Authentic AMC questions supplied as images now present one clean answer-letter strip instead of repeating "Option A", "Option B" and so on beneath the original printed choices. The image and official wording remain unchanged.
8. Sixty-five unnecessarily templated explanations in active archived AMC papers were edited to remove generic coaching paragraphs while preserving their mathematical steps, specific warnings, checks and final answers.
9. The 2025 Upper Primary paper's **30 stored answer keys matched all 30 entries** in a published copy of the 2025 AMC solution-book answer table. This is an answer-key comparison, *not* a guarantee that every explanatory argument and image crop has completed manual proof/visual review.
10. The short flash/practice pages now use less artificial wording, and the place-value drill rotates between several believable contexts. Required written-reflection wording has been removed from the optional bridge.
11. The full authored question generator is again capable of producing all 566 protected questions; a missing revisit counter was detected and corrected by the new whole-course test. Digit generators are constrained to actual decimal digits for all nine parameter visits.

## Automated QA now in the repository

**Lesson-bank audit:** `tools/content/audit_all_lessons.py` rebuilds all 566 questions using canonical session/technique mappings and checks question completeness, spelling-independent identity, prompt/answer/solution structure, uniqueness of IDs, title coverage, deprecated wording and numeric-structure repetition. It runs as part of Teaching behavior checks.

**Mathematics-family audit:** `tools/content/check_original_lessons.py` checks all 52 mathematical technique families over nine visit parameters, including independent enumeration for counting, paths, digit configurations, factors, number patterns, geometry, and arithmetic boundary cases.

**Exam/diagram audit:** `tools/papers/audit_generated_papers.py` validates all **507 generated questions** across 19 newer practice-paper builds: MC choices, key-to-choice mapping, numerical answer conventions, unique question text, worked-solution presence, and the XML/ARIA/viewBox structure of **103 embedded SVG diagrams**. Short AMC arithmetic prompts are deliberately permitted. This is **structural/static** QA, not a substitute for proof-reading all 507 solutions or rendering every SVG for human visual inspection.

**Interface tests:** Existing browser tests cover lesson screen navigation, iPhone scrolling, iPad/laptop viewports, maths baseline alignment, exam answer persistence, one-attempt safeguards, progress recording and the source-scan answer selection UI.

## Original AMC fidelity benchmark

Use the user's supplied genuine AMC scans for accurate question statements, exact figures and layouts; use the published 2024 Upper Primary solutions and the 2025 AMC solution-book answer table as independent references. Official-source images must not be silently rewritten. Any mismatch with a genuine paper should be fixed only after verifying its source.

2025 solution-book reference consulted: https://www.studocu.com/en-au/document/methodist-ladies-college/amc-mathematics/2025-amc-junior-questions-comprehensive-solution-guide/175493346

## Remaining quality risks — not certified as complete

**1. Repeated mathematical structures (high priority).** Although all 566 standard lesson questions have unique IDs and distinct exact text, the current live database contains **122 distinct number-normalised stem structures**, with **105 structures appearing multiple times** (444 additional rows using an earlier stem structure). Deliberate revisiting of a mathematical technique is pedagogically useful, but those examples should not be presented as hundreds of wholly different original competition puzzles. Mathematical redesign must account for prior attempts and saved keys; cosmetic word changes alone are not an adequate uniqueness fix.

**2. Human proof review of every stored item.** Auditing generator algebra and stored-answer consistency does **not** prove each of the 3,233 stored problems and solutions is error-free. In particular, advanced multipart problems, archived paper explanations and problem-specific distractors still need exhaustive independent mathematical review rather than trusting a stored `solution_verified` flag.

**3. Diagram/source rendering.** There are **546 active exam visual payloads**: 490 stored as `image_ref` (447 WebP source-question scans plus 43 reconstructed SVG/HTML illustrations) and 56 in `figure_svg`. A separate source-figure checklist should compare every scan crop against the original source and visually inspect the live layout at iPhone, iPad and desktop sizes. Parsing a diagram as valid XML is not equivalent to checking its mathematical accuracy.

**4. Retired mocks and practice-bank provenance.** The 1,613 inactive legacy exam questions are preserved with their inactive status; some contain exact duplicate stems and repetitive templates. Do not reactivate any of those papers without a new fidelity and mathematical-content review.

**5. Narration and lesson-consistency review.** Editing written mathematical explanations does not automatically update previously recorded videos or narration. Narration/visual synchronisation requires separate review before declaring those assets fully aligned.

## Non-destructive change policy

- Never alter a student's submitted response, attempt identity, previous score, rank, or completed lesson.
- Recheck mathematics before changing a graded answer; if a historical key was incorrect, design a migration/regrading policy rather than silently rewriting the source.
- Never publish protected answer keys or protected challenge-video assets into the public GitHub Pages directory.
- Keep AMC genuine-source problems separate from original Summit One practice, and do not imply a new problem is an official past-paper question.
- Treat a test failure as evidence of a real or test-harness defect; fix it and rerun the tests before reporting a successful release.

This is a **continuing audit register**. It records completed, reproducible checks and explicitly separates them from mathematical/visual checks that have not yet been carried out problem by problem.
