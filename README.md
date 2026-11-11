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
The full authentic-past-paper engine is implemented. The first family-supplied AMC Upper Primary PDF is the remaining source-content import before the authentic-paper section contains a live paper.
