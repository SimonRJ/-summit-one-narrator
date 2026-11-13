# Summit One — curated AMC practice audit
Reviewed 13 November 2026.

## Intended learner experience
AMC has exactly three student-facing options: **Practice Part A (Q1–20)**, **Practice Part B (Q21–30)**, **Real AMC past papers**. Rossmoyne Honours and MAWA continue in the Exams hub as distinct mathematics pathways. The old full-length authored AMC mock centre is retired from active selection; historical saved sittings remain accessible.

Each Part A/B paper allows **one timed and scored attempt**. The database guard uses the authenticated user and paper ID to prevent a second sitting. A completed result snapshot retains answers, grades, time, full written solutions, and question metadata. Practice countdown uses a count-up clock while the server enforces the fixed expiry. Review-only lesson links cannot create progress or unlock future sessions.

| Mode | Target | Released original sets | Verified questions | Unreleased original sets |
|---|---|---|---|---|
| AMC Part A Q1–20 | 30 sets = 600 questions | 2 | 40 | 28 |
| AMC Part B Q21–30 | 30 sets = 300 questions | 1 | 10 | 29 |
| **Total** | **60 sets = 900 questions** | **3** | **50** | **57 sets / 850 questions** |

Do not represent unreleased sets as complete or repeatable. The ten familiarisation sets copied from prior authored full mocks in each part, and the older structurally repeated mocks, are inactive and do not count toward the 60 unique papers.

## Mathematical and editorial checks carried out
- 40 original Part A multiple-choice answer keys checked independently against the actual selected choice and a separately computed result.
- Ten original Part B keys checked independently using enumeration or a second method. Methods included restricted unequal-step walks, digit-swap constraints, axis-aligned lattice triangles, consecutive-square totals, nonadjacent circular seats, multiset-first-occurrence orders, row/column parity masks, nonattacking queens, strict lattice paths, and modular sliding-window arrangements.
- Question numbers and mark weights preserved: Part A Q1–10 ×3 and Q11–20 ×4 (70 total); Part B Q21–25 ×5 and Q26–30 worth 6,7,8,9,10 (65 total).
- Q14 of the second original Part A set had stray surrounding quotation marks corrected in the secure database before any attempt.
- Eleven question-to-technique categories were corrected so exam reviews link to the *mathematical method* (for example constrained grid paths, toggle parity and restricted circular arrangements), not merely the problem's wording.
- Original Part B stems and Part A questions 11–20 were edited toward concise, unambiguous AMC style without changing answers. New version identifiers mark those editorial reviews.
- Lexical comparison checked all 50 active original questions against the 570 authentic Upper Primary questions from 2007–2025 in the private database. A near-overlapping digit extremisation problem was replaced with a structurally different pairwise-difference/gap invariant before release. Automated similarity is a screening step, not a guarantee against every possible mathematical resemblance.
- A 52-skill course map links graded questions to canonical session numbers and relevant written or narrated teaching. Viewing a refresher neither changes exam scores nor grants session completion.

## Calibration to real Upper Primary AMC papers
Historical corpus: 19 real past papers (570 questions), inspected by bands Q1–10, Q11–20, Q21–25 and Q26–30. The current question bank contains more words per difficult question than the authentic median and needs continued careful editorial trimming. Diagrams are important particularly in middle and later questions; a topic label alone must never substitute for inspecting what mathematical insight a question actually needs.

### Release gate for *each* new question
1. Novel wording, diagram and genuine mathematical strategy: comparison against authentic years, existing practice, contest references, APSMO photographs and all already released new sets. Number-only substitutions and identical solution mechanisms are rejected.
2. Exact, unambiguous conditions. Five distinct plausible multiple-choice options or a single valid 0–999 integer answer; correct original slot and mark weight.
3. Independently derived and checked answer; second method or small program where applicable. For multi-case tasks prove that all possibilities are counted exactly once.
4. Written solution explains the idea, efficient path, alternative representation or check, and a tempting failure mode. For 2027/2028 preparation teach transfer, not recognition of memorised source questions.
5. Accurate diagram for any geometric, spatial, route or visual-constraint question. Colours and labels must match the wording.
6. Primary skill and relevant refresher sessions checked against the 372-session canonical course; link at least one exact lesson, without unlocking it.
7. Entire 20/10-question paper reviewed for difficulty progression, **variety** across mathematical domains, duplicates across its own questions, and total score. Keep inactive until every check passes.
8. Confirm one-attempt lock, saved time, missing/unsaved warning, all written solutions and owner-only historical review. No answer keys in public Pages assets.

Reference textbooks are learning-method references only. The APSMO photographed pages, the George Lenchner Olympiad volume and AMT Methods of Problem Solving Book 3 must not be copied verbatim into a publicly accessible app. No author can know the unseen 2027/2028 AMC questions; the aim is maximum transferable reasoning and speed, not a guarantee of a future score.

## Regression tests
- GitHub Actions **AMC split training QA** checks clock bounds, one-attempt UI, navigation and all 52 skill-to-lesson mappings.
- GitHub Actions **Teaching behavior checks** cover learning, saved progress and review.
- **Summit One release QA** runs desktop/mobile browser workflow, locked-paper report, solution links, no-repeat semantics, repair classification preservation and course navigation.
