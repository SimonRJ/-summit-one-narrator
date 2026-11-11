# Summit One — The 135 Mission

Private-family mathematics training application deployed with GitHub Pages and Supabase.

## Learner experience
- One canonical path through 372 learner-paced sessions.
- Remember → Discover → Try → Transfer → Check.
- 53 MAWA proof/investigation sessions at every seventh slot.
- 25 full 30-question / 135-mark AMC-format authored mocks.
- 11 original 23-question / 100-mark Rossmoyne-style practice papers.
- Separate AMC Test Centre for authentic past papers supplied by the family.
- Completed session and exam records are immutable.
- Viewed/guided/independent evidence is tracked separately.
- Twenty passive explorer ranks at 5% course increments.

## Platform
- GitHub Pages: static learner interface and original authored narration media.
- Supabase Auth/Postgres: learner login, cloud sync, protected content, attempts and exam records.
- Supabase Edge Functions: server-side challenge grading/solution unlocks and exam grading.
- Protected AMC archive text/answers are not stored in the public Pages branch.
- Authentic AMC narration is generated on the signed-in learner's device and cached locally rather than published as public media.

## Assessment truth
AMC Upper Primary rehearsal uses 30 questions in 60 minutes with 25 multiple-choice and 5 integer-answer questions, including explicit Save behaviour for integer responses. Summit One authored mocks are not official AMT papers. Award bands shown without a verified WA paper-year table are clearly labelled practice estimates.

## Costs
Current architecture is designed to operate within free GitHub Pages/Release hosting and the connected Supabase Free project for one learner. Usage limits of those third-party free services still apply.

## Release status
The authenticated AMC Test Centre is live with complete 30-question / 135-mark Upper Primary papers for 2007, 2008, 2023 and 2024, alongside 25 original Summit One AMC-format mocks and 11 original Rossmoyne-style papers. A full 2025 Upper Primary paper is not installed because the current project source bank contains verified 2025 final-five material but not a recoverable complete 30-question source.

The 266-video visual library is complete. Final narration is being standardized on Kokoro `af_heart` at speed `0.88`. Public-safe teaching/original videos are packaged separately from authentic AMC media. Authentic AMC finished videos are stored only in the private `summit-one-protected-video` bucket and are served by short-lived signed URLs after the server has verified an independent attempt.

Post-production tooling under `postproduction/` retimes visuals to verified narration without time-stretching speech, produces H.264/AAC MP4s plus VTT/checksums/QA, and hard-fails if protected AMC media is placed in a public release bundle.
