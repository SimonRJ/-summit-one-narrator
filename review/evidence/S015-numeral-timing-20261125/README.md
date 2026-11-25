# S015 — measured numeral timing and stable captions

The final **local candidate**, not an immutable release or deployed movie, is
`3a54e336d09eb2f1e9e5fcf50253c6cea5ddf58ed96bf468a300316754c2cfd2`.
Its source is the held returned CI movie
`f4bb4b7e43d5d0037680d07ff8b65a375fd552f865406657d7e2b259604eca52`.
Do not mount that held movie if its independent browser/release jobs finish.

## What changed

The audit covered all eight saved Voice C takes. The correction measures all
21 compound-number groups in scenes 2–8, changes 54 numeral-word timings and
eight immediately adjoining words, and preserves 318 other word timings.
All 21 groups stay in one complete caption through the measured last word.
The saved timeline and VTT are under
`production/lesson-films/voice-c-repairs/S015-numeral-*`.
The full measurements, old/new intervals, archive identities and group checks
are in `review/S015-numeral-timing-correction-20261125.json`.

The shared renderer now uses one stable bold phrase. Its old regular/bold
cross-fade produced doubled outlines during word emphasis; the intermediate
timing-only comparison in `intermediate-caption-ghosting.jpg` preserves that
observation. It identifies superseded movie `bcb9e0b9…`, not the final master.

`caption-comparison.jpg` shows ten exact decoded frame pairs. The left column
is the held movie and the right is the final local candidate. `frames.json`
binds each full-size JPEG to its frame index at 30 fps and both movie hashes.
The selected times show 324/344/354/384, 24/54, the shifted 24, the complete
common-multiple phrase, 59, and the later 23. The final pairs were visually
inspected: the missing/truncated phrases remain visible and the letter
outlines stay single. These samples do not claim every frame was viewed.

## What was verified

- `encoded-verification.json`: full decode, 156 whole-second comparisons,
  maximum picture/caption errors 2.081/1.757 out of 255, eight complete-scene
  audio comparisons with correlation at least 0.999754.
- `audio-preservation.json`: all 7,280 original AAC packet payload hashes and
  timestamps are identical; all 4,659 newly drawn picture packets survive the
  audio-copy step unchanged. The original lossless FLAC is also byte-identical.
- `timing-application.json`: the exact source ZIP, archived recording, script,
  core drawing/timing files and saved patch pass their pinned hash and content
  checks. A changed candidate ZIP was rejected before extraction or writes.
- `candidate-assets.json`: hashes and byte lengths of all six local candidate
  assets. The parent owns CI publication and must verify its returned master.

The production workflow is `.github/workflows/s015-numeral-timing.yml`, on the
isolated branch `production/s015-numeral-timing`. It applies this saved patch
without another ASR pass, model download or voice recording, then runs encoded
comparisons, five canonical profiles and consumer 260 on PC/iPad portrait.
Eleven numeral tests and two caption pixel tests pass locally.

## Open acceptance

No corrected CI master, corrected-candidate browser pass, immutable release,
deployed-route result or final audible/editorial credit is asserted here.
The nonnumeric word “Check” retains its zero-width anchor at 125.02 seconds.
Scene 7 and scene 8 retain source recognition scores of 97.87% and 96.84%;
“Check” and “A tempting” remain explicit listening checkpoints.

The earlier `67fdcbc4…` local master, `bcb9e0b9…` timing-only proof and
`ea6186de…` incomplete stable-caption render are superseded. Historical
comparisons for other released films retain their original pinned source.
