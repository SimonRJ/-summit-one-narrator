# Temporary S102 wording correction: UI evidence

Both consumers now explicitly correct the published film's phrase “two end digits”: keep hundreds fixed and swap tens and units, so **153 becomes 135**. Session 102 keeps its separate-column counting prompt. Session 296 keeps its multiples-of-nine and missing-digit prompt. The existing public-guide note map adds the same correction only for the old `S102-Intro.mp4` filename.

The iPhone-width check passed in WebKit 26.0 at **390 × 664 CSS pixels** using the existing isolated learner fixture and an S102 catalogue fixture based on the original public guide. Each lesson was checked on **Read, Watch, and locked completed replay**, including the Chapters and transcript link. The correction text, headings, video rectangles, footer and replay controls fit without horizontal or vertical clipping. The saved completed record, progress and fixture writes were unchanged by replay. The public guide displayed its correction below the current video.

The browser loaded metadata from the existing exact original master, SHA-256 `538f9142a5113e5d14d3a35b6a7851e8dd331e16aba7d98224a7d0c294601612`. **No video was played**; the check recorded zero play events. This is UI evidence, not film acceptance or physical-device certification.

`iphone-fixture.json` records the source hashes, text, measured bounds and assertions. The seven screenshots show the six learner views and public-guide correction. Static comparison against the base commit confirmed that only the two intended public `bridge` fields and matching generator revision entries changed; all questions, other lesson fields and movie URLs remain the same.

Remove or replace these temporary bridge cues and their generator entries when the verified S102 replacement is mounted for both consumers. Remove the old-file public-guide note as part of that integration; it is already scoped so it will not appear for the replacement `S102.mp4` filename. The repair lifecycle is documented in `docs/S102_DIGIT_SWAP_REPAIR_20261125.md`.
