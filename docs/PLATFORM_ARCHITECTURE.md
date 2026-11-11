# Summit One Platform Architecture

## Mission

Build a world-class mathematics training platform for a gifted 10-year-old working above year level, with a single guided path toward:

1. AMC Upper Primary mastery, including a target of a perfect 135/135.
2. Rossmoyne Senior High School Specialist (Honours) Mathematics entrance readiness.
3. MAWA Problem Solving Program / primary extension problem-solving readiness.
4. Deep, transferable mathematical reasoning rather than answer-pattern memorisation.

The platform should combine reading mathematics, writing mathematics, seeing mathematics, hearing mathematics and deliberately practising retrieval/transfer.

## Hosting architecture

### Static application
- Host the Summit One front end on GitHub Pages.
- Keep HTML/CSS/JS, lightweight diagrams, manifests, route data and small JSON content in the Pages repository.
- Do not place the full video library directly in the Pages site because Pages has site-size and bandwidth limits.

### Large media
- Only the 72 concept/worked-example final MP4s may be stored as public GitHub Release assets.
- All 194 challenge/problem explanation MP4s—both authentic AMC and original K/N challenges—must remain private in the Supabase Storage bucket `summit-one-protected-video`.
- The authenticated solution Edge Function may issue a short-lived signed URL for a challenge MP4 only after confirming a recorded independent attempt.
- Use stable release URLs for public-safe media and signed URLs for protected media.
- Preserve high-quality source/master archives separately in the AMC Training Library.
- The release packager must fail if any challenge ID (`A…`, `K…` or `N…`) is found in a public bundle.

### Authentication and progress
Use Supabase Auth/Postgres for learner authentication, immutable session evidence, problem attempts, exam sittings, progress and protected-content gating.

Student-facing login presents:
- learner name / alias
- PIN/password

The browser uses only the publishable client credential. Service-role credentials remain server-side in Supabase Edge Functions or protected CI secrets and must never be committed to the public repository.

Public student-facing database views use `security_invoker=true` and expose only safe columns. Answer/solution columns are not granted to the browser role. Challenge solutions are returned by authenticated Edge Functions only after the server verifies an independent attempt.

Progress syncs across devices through Supabase. Completed session records remain immutable. Video-view evidence is stored separately from independent mathematical evidence.

## Course structure

Sessions are completion-based, not calendar-day based.

Standard session:
1. Remember
2. Discover
3. Try
4. Transfer
5. Check

Typical session duration: 30–60 minutes.

Student may complete:
- zero sessions on a day,
- one session,
- or multiple sessions.

MAWA-style investigation frequency:
- one investigation every 7 completed sessions.

Completed sessions are immutable as evidence:
- answers preserved,
- working/reasoning preserved where entered,
- videos watched preserved separately,
- independent solution credit cannot be awarded from simply watching a solution.

## Video rules

Total course video registry: 266.

Video categories:
- 54 concept explanations
- 18 worked examples
- 194 challenge/problem explanations

Challenge solution video unlock rule:
- locked until the student has made a genuine attempt.

Watching a solution:
- never counts as independent solving,
- may move evidence to viewed/guided,
- never increments independent-correct tally.

Player:
- transcript
- replay
- speed controls
- gentle letter glow -> whole-word glow -> fade
- stable viewport size
- high-quality audio
- no forced tiny text

Final delivery videos should preserve the approved production quality rather than lowering bitrate or resolution merely to fit Pages.

## Mastery and evidence

Track evidence separately:
- viewed
- guided
- independent

Track:
- technique mastery
- Rossmoyne problem families
- AMC Q26–Q30 performance
- MAWA investigation performance
- retrieval success
- transfer success
- timed-exam success

Only correct timed-exam problems contribute to the 3-star / 4-star / 5-star solved counts.

Do not count:
- attempts,
- incorrect answers,
- solution-video views
as solved problems.

## Motivation and ranks

20 ranks across the entire program.

Award next rank every 5% of true overall completion.

Profile shows:
- overall percentage complete
- current rank
- all 20 ranks
- locked ranks greyed out
- XP/progress needed to next rank
- 3-star correct count
- 4-star correct count
- 5-star correct count
- sessions until next practice exam

Motivation should support competence rather than distract from mathematics.

## AMC real-exam simulator

Use genuine past AMC papers supplied/licensed by the user only.

Current official Upper Primary competition structure:
- 30 questions
- 60 minutes
- questions 1–25 multiple choice
- questions 26–30 integer answer
- no penalty for incorrect answers
- scoring: Q1–10 = 3 each, Q11–20 = 4 each, Q21–25 = 5 each, Q26–30 = 6,7,8,9,10
- maximum = 135

Competition-mode behaviour to reproduce:
- explicit Start action begins timer
- visible competition timer
- menu allows skipping and returning to earlier questions
- multiple-choice selection
- integer-entry response
- integer answers require explicit Save
- automatic finish when time expires
- submitted answers retained at expiry
- no coaching, hints, solution videos or correctness feedback during exam
- one complete sitting record
- post-exam review only after completion

The training simulator should reproduce behaviour and pressure profile without copying AMT branding, logos or a pixel-identical proprietary interface.

Official AMT practice/navigation test should be used as the behavioural reference when validating simulator interaction.

AMT states official online competitions must not be sat on mobile phones. Simulator may remain responsive for practice, but desktop/iPad exam mode is the target rehearsal layout.

## Rossmoyne pathway

Training must include:
- advanced curriculum fluency
- unfamiliar-context problem solving
- competition reasoning
- critical thinking
- concise written reasoning
- multi-step arithmetic/algebra
- geometry
- number structure
- combinatorics
- logical deduction
- strategy selection under time pressure

Rossmoyne reports its specialist program attracts hundreds of applications for around 25 Year 7 places and expects exceptional mathematical ability and passion.

Include their official sample entrance-test style as a calibration source where permitted.

## MAWA pathway

MAWA PSP emphasis:
- mathematical problem solving
- persistence with challenge
- logical and effective presentation of solutions
- mathematical enrichment

Maintain a MAWA-style investigation every 7 completed sessions.

## Quality gates before release

### Content
- no duplicate IDs
- no missing routes
- no broken question/video mapping
- no answer leakage before attempt
- no incorrect worked solution
- no ambiguous unit/answer display
- no accidental use of copyrighted material beyond supplied/licensed content

### Video
- playable MP4
- audio stream present
- sync checked
- no truncated narration
- no blank/black frames
- readable text on target devices
- consistent loudness
- captions/transcript linked
- high-resolution master retained

### App
- login persists
- progress sync works across devices
- offline/poor-network failure is graceful
- refresh does not lose answers
- completed session cannot silently mutate
- timer cannot be reset by ordinary refresh during a real practice exam
- exam completion record is immutable
- solution video cannot grant independent credit

### Accessibility and child UX
- large touch targets
- readable typography
- no cluttered dashboard
- minimal navigation choices
- no manipulative engagement loops
- clear next action
- explicit feedback
- diagrams where they genuinely help
- language appropriate for a gifted 10-year-old without being babyish

## Full release review

Before calling the platform complete, conduct:
1. Registry integrity audit.
2. Every route/link audit.
3. Every video playback/audio audit.
4. Cross-device login/progress audit.
5. Session progression audit.
6. MAWA cadence audit.
7. Rank/XP calculation audit.
8. Timed AMC simulator audit.
9. Rossmoyne coverage audit.
10. MAWA coverage audit.
11. Pedagogy review for explanation depth and pacing.
12. Child-UX review.
13. Security/privacy review.
14. Copyright/branding review.
15. Final end-to-end learner journey test from first login through exam review.
