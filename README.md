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
- GitHub Pages: static learner interface plus public concept/worked-example media.
- Supabase Auth/Postgres: learner login, cloud sync, protected content, attempts and exam records.
- Supabase Edge Functions: server-side challenge grading/solution unlocks and exam grading.
- Protected AMC archive text/answers are not stored in the public Pages branch.
- Every challenge solution video is attempt-gated. Final challenge MP4s use private Supabase Storage signed URLs; if a protected final is unavailable, Kokoro is generated on the signed-in learner's device and cached locally.

## Assessment truth
AMC Upper Primary rehearsal uses 30 questions in 60 minutes with 25 multiple-choice and 5 integer-answer questions, including explicit Save behaviour for integer responses. Summit One authored mocks are not official AMT papers. Award bands shown without a verified WA paper-year table are clearly labelled practice estimates.

## Costs
Current architecture is designed to operate within free GitHub Pages/Release hosting and the connected Supabase Free project for one learner. Usage limits of those third-party free services still apply.

## Release status
The authenticated AMC Test Centre is live with complete 30-question / 135-mark Upper Primary papers for 2007, 2008, 2023 and 2024, alongside 25 original Summit One AMC-format mocks and 11 original Rossmoyne-style papers. A full 2025 Upper Primary paper is not installed because the current project source bank contains verified 2025 final-five material but not a recoverable complete 30-question source.

The 266-video visual library is complete. Narration is now verified complete at **266/266 Kokoro tracks**, using Kokoro `af_heart` at generation speed `0.88`. The former HeyGen tracks are no longer counted as final narration. Final MP4 post-production is the active media stage. The 72 concept/worked-example videos are public-safe media. All 194 challenge-solution videos are stored only in the private `summit-one-protected-video` bucket and are served by short-lived signed URLs after the server has verified an independent attempt.

Post-production tooling under `postproduction/` pairs the verified Kokoro narration with the correct visual master, preserves Kokoro pitch, applies bounded visual retiming and pitch-preserving tempo correction only when needed, produces H.264/AAC MP4s plus VTT/checksums/QA, and hard-fails if protected AMC media is placed in a public release bundle. A001 and A049 use their separately approved polished visual sources rather than the superseded archive masters.

## Media quality tiers
High-quality final MP4s remain the archival/source-of-truth copies in the AMC Training Library. The protected challenge library is projected to exceed the Supabase Free plan's 1 GB Storage quota if those masters are uploaded unchanged. `postproduction/make_protected_delivery.py` therefore creates separate 720p H.264/AAC streaming copies for the private bucket and hard-fails above a 900 MiB safety ceiling. This delivery step never replaces or recompresses the archived masters.
