# Paused draft — 11 November 2026

User requested a pause for the night. Do not deploy this branch without resuming the task and completing validation.
Main remains 0b77194f20e2286ff6a09ef040ce9c2b6788c5a7; no app changes or exam imports have been published.
Supabase project dyidjdagwdvsczudkryt. Temporary import-archive-20261111 endpoint has been disabled (JWT required, always 410, no write code).
Do not restore its old credential.

## Draft changes
- Explicit method teaching for all 52 techniques, each with a small worked example, trap, guided check and parameterised recall check.
- Delayed recall by completed sessions; two revision questions at most.
- Goal/readiness and parent guidance view for AMC August 2027, MAWA 2027 application for 2028, Rossmoyne Year 6 test 2028 for Year 7 entry 2029.
- Pin unfinished session challenges; separate final answers from working; readable immutable session archive.
- Safe numerical/fraction grading draft; no first-number extraction; repeated problems do not earn fresh independent credit.
- Exam save queue, saved results review, original diagrams in results, honest missing-source/explanation labels.
- Quiet audio fallback; preserve approved T02.1/T02.2 masters; no guessed video URLs.

## Exam audit
Live database contains 4 authentic complete papers: 2007, 2008, 2023, 2024; 25 authored AMC mocks and 11 Rossmoyne mocks.
User supplied AMC upper Exams PDF has 2007–2022 and answer keys on PDF pages 157–158.
Prepared 14 additional 30-question/135-mark import payloads, 2009–2022 (420 questions), but NOT imported.
The file labelled AMC 2025 is the 2013 Upper Primary paper (all 30 questions match the 2013 archive); do not publish it as 2025.
2014 scan ends at Q27; Q28–30 recovered from existing authenticated bank A061–A063 and checked against archive key.
Only available worked solutions are attached; most new earlier questions have verified answer keys but no worked explanations yet.

Local working directory: /workspace/scratch/2c6b7aa92624/summit-audit.
Source PDFs: sibling upload/.
Archive work: sibling archive-build/ (import-2009.json through import-2022.json, crops, keys, contact sheets, OCR 2014).
Archive payloads and source PDFs must remain protected and must NOT be committed to the public repository.
tools/build_archive.py is a checkpoint of the extraction process and currently uses those local paths.
private-content-audit.json is local authenticated source content; do not commit it.

## Validation still required
Only JS syntax checks have run. No browser or behavior tests, deployment or full mathematical review yet.
Review all 52 exercise variants independently; constant-answer exercises should not be mistaken for varied mastery evidence.
Recheck cropped diagrams: initial text-anchor cropping clipped figures beginning above their question numbers; the final builder now chooses full-width whitespace boundaries, but final images still need visual verification.
Review curriculum progression and difficulty: current draft selection still uses category/keywords, prioritises all unseen questions, and its history needs updating after new attempts.
Check all stage navigation and unsaved work, MAWA saves, hint persistence, session completion failures, exam save failures, replay/reload behavior.
Fix service-worker cache (not updated yet), version URLs, include new modules in release QA.
Confirm no unsupported claims: retained checks are not exam mastery; repeated perfect papers must not inflate distinct-paper readiness.
Current challenge solutions K001/K007/K015/K022 contain lost exponent notation; fix verified formula text and spoken scripts before publishing.
Exam server award fallback differs from data config in main; draft aligns it, but verify source cutoff config before deployment.
Validate backend functions with authenticated fixture tests without changing the real learner’s records.
Publish only after passing tests; then import protected questions, verify 18 genuine papers 2007–2024, and disclose genuine 2025 source still needed.

## Official sources checked
https://amt.edu.au/competitions — AMC 3–5 August 2027.
https://amt.edu.au/amc — primary 60 minutes, 30 questions, 135 marks.
https://mawainc.org.au/mawapsp/ — primary entry by application problems; future 2028 application dates not verified.
https://www.rossmoyne.wa.edu.au/enrolment/specialist-programs/specialist-mathematics-program/ — Year 6 applications, current published schedule is 2026 test for 2027 entry; future 2028 test date unverified.
