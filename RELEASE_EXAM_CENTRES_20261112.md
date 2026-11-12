# Exam centres and learning repairs

The 36 previous embedded mock slots are now untimed strategy workshops. Stable session numbers, the 372-session path, 53 investigations (every seventh completed session), and existing learner records are preserved. Full exams are accessed through their own tabs.

- AMC past papers: 19 authentic Upper Primary papers, 2007–2025; one attempt, permanent review.
- AMC practice: 10 new 30-question, 135-mark papers; unlimited separately saved attempts, first/best scores and full history.
- Rossmoyne honours: nine new 23-question mocks plus the uploaded original sample transcription, with its four-section, 100-mark structure. Navy/gold presentation. One attempt per paper. The 60-minute limit is a home-practice setting, not verified official timing; the sample is not represented as the actual 2028 paper.
- All 530 questions in the new exam set and all 570 authentic AMC questions have written explanations. Existing approved video links remain; no new solution videos were produced.
- A second worked bridge and partially completed practice support all 52 techniques. Later lessons include mixed-method transfer; 36 workshops replace the old exam sessions. Original lesson challenges remain.
- Wrong answers create saved repair items: identify the cause, explain the correction, use support, solve changed values independently, then check after three further completed sessions.
- Completed investigations accept separate parent/tutor rubric reviews without altering learner work. Reviewer names are self-declared.
- The 3/4/5-star feature and its increment RPC are removed. Legacy fields are retained inertly to avoid destroying historical data.

## Corrections and integrity

Six older AMC mock keys and 2020 Q2–Q5 keys were corrected. 2007 Q25's transcription now correctly states that Ace, rather than Bea, is older than Geo. The verified 2008 Q2 number line is restored. Twelve lesson prompts and eleven retired Rossmoyne painted-block questions have explicit wording/orientation. Historical submissions and scores are not overwritten; reviews can show corrected-key scores separately.

The new backend enforces one open attempt, allowed repeatability, immutable completed sittings, server expiry, question-level response saves, private answer keys and atomic result sealing. Retired papers remain reviewable. Completed results store a snapshot.

## Validation

- Transactional database fixtures passed: repeat attempts, one-attempt lock, open-attempt uniqueness, expiry/immutable-response guards, strict numerical responses, grading, idempotent snapshots and user isolation. Fixtures were rolled back.
- JavaScript/data/media checks passed; 2,704 practice variants were checked, including independent combinatorial, remainder, geometry and route calculations.
- Desktop and 390px mobile browser checks passed for exam start, answer save, missing-answer warning, submission, solution review, retry, Rossmoyne styling, lesson bridge, the complete repair/delayed-check cycle and adult review. No page errors or horizontal overflow.
- Authored diagrams were rendered and inspected. These checks do not amount to formal psychometric calibration or a guarantee of an exam result.

## Deployment order

1. Apply `supabase/changes/exam_centres_v2.sql` and deploy `grade-exam`.
2. Import the twenty new private paper documents while inactive, including written solutions and figures. Apply documented archive corrections and technique mappings.
3. Publish the tested frontend to GitHub Pages.
4. Run `supabase/changes/activate_exam_centres_v2.sql`. It validates the replacement set before activating it and retires, without deleting, the old 36 mocks.
5. Verify the live authenticated catalog and navigation without consuming any learner's one-attempt papers.

Authoring sources are under `tools/papers/` and `tools/solutions/`; generated private exam JSON is not bundled into the student frontend. For rollback, restore the previous frontend and catalog activation flags; keep the backwards-compatible schema and saved learner records.
