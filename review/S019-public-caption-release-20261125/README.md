# S019 actual public caption release and strict integration plan

The actual public master is **5455c0c0119bedd897ddda6feb41002cf215575c8f8839565661674c42ad712c**,
6,751,206 bytes, from completed production run **45524933207** at source
`ac244dec713654fa7fb47693c8c179d9fb436479`. Its exact release is
[`s019-stable-captions-20261125-ac244dec7136`](https://github.com/SimonRJ/-summit-one-narrator/releases/tag/s019-stable-captions-20261125-ac244dec7136).
The render, all five browser-profile jobs and release completed successfully.

This commit admits only that returned public edition to the preparation helper.
It does not assign S019, edit route/data files, change learner state, publish a
branch or award editorial credit. The held public `51545b1b…` and unpublished
local `4a549a8c…` masters remain explicitly rejected.

## Independent returned-byte and media verification

All **six public assets / 17,487,486 bytes** were downloaded from their actual
public release URLs and matched their GitHub sizes and SHA-256 digests.
`returned-byte-check.json` records the result. The guide and QA both identify
the exact returned movie; the guide differs from the held source only in its
movie SHA. The API records in `run.json`, `release.json` and `jobs.json` were
saved from the actual successful run, not synthetic positive fixtures.

The returned movie retains all **6,673 original AAC packet records**, including
payload hashes, side data and timing, as well as identical extracted AAC ADTS
bytes. Its **4,269 video frames** retain the original presentation times,
durations and decode timestamps. The original VTT, complete recording ZIP,
script, timeline, lossless recording and poster are byte-identical. Exact
properties and member hashes appear in `preservation-and-caption-check.json`.

The actual public movie was independently checked at all **143 whole-second
samples**: 129 against the original retained scenes and 14 against the stable
scene-five renderer. Its maximum picture/caption mean differences are
**1.895295 / 1.987654** out of 255; the retained-scene maxima are
**0.116388 / 0.349267**. Those reproduce the public QA measurements and remain
below the existing threshold of 5. See `actual-public-picture-comparisons.json`.

Exact public decoded frames **1481 / 1501** (**49.366667 / 50.033333 seconds**)
were inspected alongside the held frames. Both returned frames have one stable
bold caption layer; the first keeps the leftmost top-row pair visibly crossed
out. The four full-size PNGs retain that observation.

The returned container is **not** assumed identical to the local candidate.
Their encoded video records differ, and 25 of 4,269 full decoded-frame hash
records differ. `decoded-public-local-identity.json` preserves that distinction.
The public master was independently checked as described above; the local
candidate's SHA is never substituted for its identity.

## Strict gate and exact proposed changes

`tools/prepare_spoken_film_release.py` now pins the successful run, source,
workflow, tag and exact public movie. It requires the original ZIP/VTT hashes,
AAC/timeline/frame-count preservation, the scoped fifth scene, all 143 picture
comparisons with their 129/14 split, and the established difference bounds.
Both saved lesson bridges remain unchanged.

`integration-plan.json` was produced from the actual successful API payloads and
all six actual downloaded assets. It proposes these field changes:

| Slot | Actual changed fields | Existing bridge |
| --- | --- | --- |
| 19 | Movie URL, video title, dedicated-film marker | Preserved exactly |
| 333 | Movie URL and video title | Preserved exactly |

The canonical generator bridge already matches and is also preserved. Root can
apply only these route fields and the supplied catalogue entry, then refresh
matching catalogue/app/service-worker versions in the next release.

The focused `check_policy.py` regression uses the actual public package for its
positive case and isolated temporary copies for **18 rejected negative cases**:
wrong run/source/digest, queued completion, both disallowed masters, altered
archive/VTT, missing preservation, new synthesis, wrong scene, incomplete or
out-of-bound picture evidence and a rewritten canonical lesson bridge.
`policy-regressions.json` records each exact rejection. All source route/data
hashes were unchanged after the checks.

## Remaining acceptance

Root still owns integration, publication and verification of the deployed
application's canonical/technique learner routes. Browser-emulation production
checks and targeted decoded frames are technical evidence; complete independent
moving-picture and audible editorial approval remains pending.
