# Missing rung, mail train and tile frame — 25 November 2026

The three early replacements now have their authored scripts and distinctive
drawing sources in the main renderer registry. S012 and S015 also have checked
guides, transcripts, timed captions and exact-candidate evidence. This source
integration does not assign an unpublished movie to a learner or award final
editorial credit.

| Study | Candidate status | Exact master SHA-256 |
| --- | --- | --- |
| S012, The missing rung | CI render, five browser profiles and immutable release passed; all six returned assets verified | `87e71ca9ae8e3355f9f092f05a7e4c0678313aa569bbc3b4cc63a200ff2cedd7` |
| S015, Two stamps for the mail train | Local master and seven learner-route/profile combinations passed; original CI stopped before encoding | `67fdcbc472137a9deba2873a23a0e0785ccdd2dc76939534161638545b8adce0` |
| S017, A frame around two tiles | Authored source and mathematics checked; existing voice scenes 7 and 8 queued | No completed master yet |

## What was verified

Both completed movies were decoded again against their exact approved Voice C
recordings and integrated drawing sources. The 294 whole-second drawing/caption
comparisons passed. All sixteen complete-scene audio correlations exceed
0.9995. The archived recording scripts equal their authored scripts byte for
byte. The rendering implementation is unchanged apart from the lesson registry,
so the new entries preserve the original artwork and caption behavior.

Independent enumeration gives the missing-rung counts
`1, 1, 2, 0, 2, 2, 4, 6, 10` from ground through rung 8, with exactly six routes
visiting the compulsory bell at rung 5. The mail-train labels passing both
divisibility tests are 324 and 384. Shifting the inclusive interval 23–59 by one
gives four common multiples, 24, 36, 48 and 60; undoing the shift gives
23, 35, 47 and 59. Enumerating all 60 contiguous rectangles in the tile wall
gives 24 containing A, eight containing both marks and sixteen containing A
without B.

Each script has eight new scenes. Comparing against the other available guide
editions found no repeated complete scene. S012 and S015 were compared with
1,952 other scenes; S017 with 1,949. Their longest shared passages are respectively
five, four and four words. Arithmetic phrases remain arithmetic phrases; this
is evidence against recycled sections, not a claim of universal originality.

The decoded S015 contact sheet covers the parcels, separate stamps, movement of
both interval endpoints, common multiples and the return to original loads.
The actual inline iPad worked example agrees with the four numeric pairs. The
S012 iPhone worked example shows its two distinct beginnings paired with all
three endings. Complete source correspondence is covered by the encoded
comparisons; sampled visual inspection does not claim every frame was viewed.

### Browser evidence

The five S012 CI result archives were downloaded and checked against their
GitHub artifact digests. Every result identifies the master above. The five
canonical S015 profiles were run locally against the current app source, and
the later technique consumer at slot 260 additionally passed on PC and iPad
portrait. Gallery chapters, the active Read → Watch → Practise flow, correct
and incorrect fixture grading, and immutable completed-lesson replay passed.
The iPhone portrait profile played each whole film unmuted at normal speed.

These are emulated browser profiles on candidate sites with an isolated fake
backend. They are neither physical-device certification nor final deployed-site
checks. Audio correlation, recognition and an automated unmuted player are not
a separate human listening signoff. In S015, the final listener should inspect
the end of scene 7 and the opening “A tempting” in scene 8; those recognition
scores are 96.84%, with the consequential numeric answers retained.

The exact records are:

- `review/S012-missing-rung-candidate-qa.json`
- `review/S015-mail-train-candidate-qa.json`
- `review/S017-tile-framer-source-qa.json`

All retain `final_editorial_credit: false`.

## S012 publication gate

The existing run is
[45487384299](https://github.com/SimonRJ/-summit-one-narrator/actions/runs/45487384299),
source `b46d28d6d37434c91c164a74005e1a9ec8b5a21f`. Release job `138851167593`
succeeded and published `s012-missing-rung-20261125-b46d28d6d374` at 07:47 AWST
on 25 November. All six returned assets, 18,199,837 bytes in total, match their
published digests. The returned movie and guide also match the verified
candidate. See `review/S012-public-release-20261125.json`.

This revision installs the returned guide in `data/recorded-studies.json` and
updates dedicated slot 12 plus technique slot 248. Both original bridges,
all questions and grading editions remain unchanged.
Five integrated public-media route checks also pass: the canonical lesson on
PC, iPhone portrait and iPad portrait, plus consumer 248 on PC and iPad
portrait. The whole public film reached its end unmuted at normal speed on
iPhone emulation. Both iPad pairing frames show the two arrivals and all three
endings, with six dots and no player clipping. These checks used local app
pages and an isolated learner fixture; see
`review/S012-public-routes-20261125.json`.
Check final deployed gallery, active lesson and notebook routes on all five
profiles, plus consumer 248 on PC/iPad portrait. Complete final audible/editorial
acceptance before updating the review register.

## S015 recovery gate

The checked recovery source has now been published once on
`production/s015-recorded-recovery-20261125`, commit
`8fb7e5e6e3fbe8923c9c5152368b89efdeadef9b`. Its tree exactly matches the reviewed
local source. Run
[45512588528](https://github.com/SimonRJ/-summit-one-narrator/actions/runs/45512588528)
is queued. Leave that existing run intact; no second dispatch or new voice
recording is needed. This does not yet establish a completed CI master or live
film assignment.

The approved source run is
[45487547111](https://github.com/SimonRJ/-summit-one-narrator/actions/runs/45487547111),
commit `c873621cd8988d3862563a0668e500bcb94614c9`. The actual voice-source
branch is `production/s012-missing-rung`; the subsequent render source was on
`production/original-studies-s015-s017`. Do not assume these branches are equal.

Every S015 voice scene succeeded and all eight existing ZIPs were recovered
without re-recording. The original S015 renderer,
[45488080273](https://github.com/SimonRJ/-summit-one-narrator/actions/runs/45488080273),
failed after waiting 100 × 45 seconds for the entire S015/S017 voice matrix.
The workflow's alignment job depends on that whole matrix, so a completed
S015 recording cannot progress while S017 scenes 7/8 are still queued.

A separate recovery is prepared in
`.github/workflows/s015-recorded-recovery.yml`. It downloads the eight exact
artifact IDs/digests in `tools/video/s015-recorded-takes.json`, confirms each
corresponding successful source job, verifies the source commit, branch and
workflow, and rejects an active or successful original renderer. It validates
the archive bytes, narration hash, Voice C reference, model revision and natural
speed before assembling the already recorded audio. It performs no synthesis,
job cancellation or rerun.

The recovery then aligns, draws, encodes, compares the exact result, and runs
five candidate profiles plus consumer 260 on PC/iPad portrait. Only after all
those gates pass does its release job publish an immutable candidate and
compare every returned asset. The future CI hash may differ from this local
export because of alignment or encoder environment; retain that returned CI
hash and its own evidence.

Choose one rendering path before dispatching: the new per-lesson recovery or
the existing paired-run resumer on `production/park-stalled-voice-waits`
(`66dffb5814eedd463a7ca5517e16025e8890bd29`). Publishing the workflow on
main is inert. Its push trigger is restricted to the one-purpose branch
`production/s015-recorded-recovery-20261125` and changes to the workflow or
`tools/video/s015-recorded-takes.json`. Publishing the complete checked source
to that branch once starts recovery without a workflow-dispatch API. If a
workflow-dispatch client is available, the alternative invocation is:

```sh
gh workflow run s015-recorded-recovery.yml \
  --repo SimonRJ/-summit-one-narrator \
  --ref main
```

The existing broader resumer needs a correction before it can handle this pair:
its `pinned` check applies the same configured branch to both voice and render
runs, but their actual branches differ as recorded above. It would reject voice
run `45487547111`. The new per-lesson recovery already pins its actual branch. The latest broader
resumer run `45497757032` is completed with failure; its only job `138841846200`
failed at 23:31:47 UTC with `Run 45487547111 does not match its pinned production.`
It reached that source gate before iterating S015’s renderer. The S015 original
renderer remains failed with playback/release skipped. No resumer or renderer
job was cancelled for this handoff.

The recovery manifest and helper were checked against the current GitHub API
responses and all eight actual archived ZIPs. Six regression tests cover the
completed-lesson/queued-sibling case, incomplete own takes, an already active
renderer, wrong source commit, expired artifacts, changed ZIP/script, wrong
voice and unexpected archive members. The workflow's shell and embedded Python
syntax checks pass. The workflow itself has not run yet.

The checkout audit covers all twelve rendering/recording dependencies and 45
playback paths, including the 34-file local app/gallery JavaScript import
closure. Render checks out `production`, `data` and `tools/video`; playback
checks out `data`, `tools` and `figures`. Cone-mode checkout retains their root
HTML, JavaScript and stylesheet dependencies. The candidate MP4/poster are
supplied by the previous job’s artifact. Release uses its downloaded artifact
and repository/token environment only. The exact audit and latest run states
are in `review/S015-mail-train-recovery-handoff-20261125.json`.

For eventual installation, use dedicated slot 15 and technique consumer 260.
Consumer 260 needs the checked mail-train stamp bridge from the QA record;
its old wording describes a different film. Then run deployed-route checks
and final audible/editorial acceptance before giving completion credit.

## S017 next step

Keep the existing voice jobs intact: scene 7 is `138776830497` and scene 8 is
`138776830534`. The old renderer `45488080237` also failed at the matrix wait
before drawing. The source is ready for its final approved audio, followed by
encoded verification, visual/listening review, five browser profiles and
immutable release. Eventual consumers are dedicated slot 17 and technique
slot 300. No S017 candidate or playback pass is asserted here.

## Protected state

S012's published replacement changes its guide and the film-routing fields for
slots 12 and 248. The S015/S017 source work does not yet change their public
film assignments. Question IDs, grading, review counts, authentic exam material
and saved learner history remain unchanged. The two completed source
comparisons can be rerun with `verify_recorded.py` using each exact master and
archived recording.
