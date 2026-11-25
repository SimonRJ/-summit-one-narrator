# Four recorded films: stable caption refresh

The exact encoded S009, S010, S012 and S017 movies show overlapping regular and bold letter outlines while word emphasis changes. The shared renderer now draws one stable bold phrase. This source package prepares one picture refresh for each film using its existing approved performance.

This is a production handoff, not a new accepted movie. No replacement was encoded or published while preparing it. Final audible editorial credit remains false.

## Pinned inputs

The [manifest](../tools/video/stable-caption-refresh-20261125.json) contains every source asset's byte count and SHA-256, all four recording-archive member hashes, the source artwork and renderer hashes, both lesson bridges, and the exact bad transition frames.

| Film | Input | Canonical / technique consumer | Scenes / words |
|---|---|---|---|
| S009 | Public release carry-reversal-reviewed-20261125-bcbd31159202 | 9 / 228 | 7 / 326 |
| S010 | Same immutable public release | 10 / 319 | 7 / 357 |
| S012 | Public release s012-missing-rung-20261125-b46d28d6d374 | 12 / 248 | 8 / 351 |
| S017 | Successful renderer 138891222565 in run 45520621017; candidate artifact 14981085029 and provenance artifact 14978649628 | 17 / 300 | 8 / 370 |

S017's input commit is 5794566847ce5fd47037f0377c424bc631ac0271 on production/s017-recorded-recovery-20261125. The candidate ZIP is 18,758,988 bytes, SHA-256 44c934edc5358fff7a87be8ef64ccda0190ced77ccf4bc102859d246ac851c7d; its movie is 3ceff0f24ada60db2d09d9900658eed406c8b1666eee85603af57b430a2fc7d7.

The S017 run completed successfully and published its original edition at 01:10:00 UTC on 25 November. The six release asset metadata digests agree with the downloaded candidate bytes. The old edition remains held because the actual movie visibly doubles “Twenty / four” at frame 2006, “rectangles” at frame 2017, and “the / twenty” at frame 3538. Those frames and the exact original provenance are retained in [the S017 evidence](../review/stable-caption-refresh-20261125/S017/).

The recovery keeps S017's eight approved takes. All sixteen returned WAV/JSON provenance hashes were checked against the saved takes. Its corrected scene-four word intervals are Twenty 66.70–66.86, four 66.86–67.22 and rectangles 67.22–67.76 seconds. The source-bound scene-seven intervals remain twenty 117.92–118.10, four 118.10–118.52 and that 118.52–118.66 seconds. The complete returned timeline is pinned; the refresh does not run recognition or adjust these values.

## One production branch and workflow

The only push trigger is production/stable-recorded-captions-20261125, restricted to the new workflow and its manifest. Main pushes are inert. There is no automatic cancellation.

The [workflow](../.github/workflows/stable-recorded-captions.yml) has four independent lesson jobs, ordered S017, S009, S010 and S012. Each job performs the following work:

1. Restore its exact source assets. The Actions source must match the pinned repository, branch, commit, workflow and successful render job. Both artifact ZIP digests and every extracted member are checked. Public sources must use their exact pinned repository release URLs.
2. Validate the recording's script, complete timeline, VTT and FLAC before writing. Different existing outputs are rejected. Shared renderer, artwork and audio-preservation helper hashes are also checked.
3. Render the stable caption pictures once. Copy the original movie's AAC stream into the result and verify all audio packet bytes and timestamps, as well as unchanged newly rendered picture packets.
4. Compare the entire encoded film with its drawing reference at each second, and compare source audio scene by scene. Check the specific subsecond transitions that exposed the defect.
5. Save the candidate artifact before browser checks, so a later route failure does not require another encode to recover it.
6. Exercise five browser profiles, plus the technique consumer on PC and iPad portrait. The fixture backend checks Read, Watch, exact decoded worked frames, practice grading and immutable notebook replay. The canonical iPhone portrait case also runs normal-speed unmuted playback to the end.

There are 28 route cases across the four films. The preview overlay changes only the film fields for slots 9/228, 10/319, 12/248 and 17/300. All eight original bridges are asserted unchanged. No production catalogue or lesson-assignment file is modified by this source commit.

One release job runs only after all four lesson jobs succeed. It requires exactly 24 assets, checks each guide and QA digest against its movie, publishes a new immutable bundle and compares every returned byte. The old source editions remain available. Live assignment and final public-route review are separate root-owned steps.

## Focused caption proof

Whole-frame averages can hide doubled lettering because most pixels belong to the background. The [caption verifier](../tools/video/verify_caption_refresh.py) checks the visible letter pixels at the exact reported frames, while independently comparing the mathematics artwork above the caption band.

| Film | Original frame numbers | Held letter-pixel mean error, 0–255 |
|---|---|---|
| S009 | 43, 153 | 27.70, 20.07 |
| S010 | 31, 272 | 161.69, 159.38 |
| S012 | 224, 1176 | 159.02, 141.49 |
| S017 | 2006, 2017, 3538 | 146.81, 149.01, 157.35 |

All nine original frames reject the stable-letter requirement. Their mathematics artwork matches the unchanged drawing reference with mean error 1.19–1.45. The candidate letter-pixel threshold is 12. A read-only calibration against the already encoded stable S015 movie gave 4.82 and 5.34 at its two former problem frames; no calibration encode was made.

The checked-in reference PNGs are drawings from the pinned recordings. They are clearly labelled as source references and their encoded-acceptance flags are false. During production, the same gate must compare actual frames decoded from the new movie and prove exact original AAC packet preservation.

## Completed preparation checks

- Four complete source packages restored locally and verified: 42 files including the recording members and S017 provenance.
- Eight provenance and nonreplacement tests passed; the two shared stable-caption pixel tests passed.
- Five shell blocks and five embedded Python blocks parsed successfully.
- All four preview overlays preserved their bridges and all unrelated lesson rows.
- Sparse checkout includes the required production/data/tools/figures paths, 34 local JavaScript imports and all 28 locally hosted WOFF2 files. The source includes font commit 03dadd5 so the browser gates do not depend on Google Fonts.
- All nine held movie frames fail the targeted letter-pixel gate while their artwork matches. S017's original transition frames and stable drawing examples for all four films were visually inspected.

The exact local results, source hashes, S017 job/release snapshot, calibration and images are in [the evidence folder](../review/stable-caption-refresh-20261125/). The earlier 21 deployed functional passes for S009/S010/S012 remain a separate record for their original movies.

## Remaining acceptance

Root can publish the reviewed source tree once on the dedicated production branch. The new encodes, exact AAC proof, 28 browser cases and returned-asset comparison must succeed before live assignment. The resulting public URLs then need their own deployed route checks and audible editorial review. This preparation does not change completion counts, learner records or final editorial credit.
