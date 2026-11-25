# Catalogue fixture repair after S102 publication

The first live correction release passed Pages, release QA, all lesson-opening profiles, teaching behavior and split-exam QA. Recorded playback stopped before decoding because the availability test still treated S102 as a synthetic external-only film. The actual recorded S102 guide correctly took precedence. Both engine failures are retained at workflow 45528347868.

The test now chooses its external verified and pending fixtures from unrecorded teaching lessons. A separate conflicting external entry explicitly verifies that the recorded guide title and immutable movie retain precedence. Existing offline/retry, pending/unavailable, separate-release, first-six redirect and layout checks remain.

The repaired fixture passed Chromium and WebKit at 320, 390 and 1024 pixels. All outside-origin requests were fulfilled from the synthetic catalogue or aborted; no learner backend or real learner state was used. The complete raw local log and structured results are retained. This changes the checker only, with no editorial credit.
