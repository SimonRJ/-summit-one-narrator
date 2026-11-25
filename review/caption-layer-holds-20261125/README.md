# Recorded caption quality holds

Actual decoded frames from the immutable public S009, S010, S012 and S019 movies show overlapping regular and bold outlines during word emphasis. The eight unaltered caption crops and their exact movie hashes, measured times and source words are recorded in `frames.json`. They were extracted from the returned movies, not regenerated from drawing code.

| Film | Observed examples | Delivery consequence |
|---|---|---|
| S009 | “counters” at 1.4333 s; “equally” at 5.1 s | Keep technical playback evidence separate; prepare a caption-only refresh. |
| S010 | “printer” at 1.0333 s; “nothing” at 9.0667 s | Keep technical playback evidence separate; prepare a caption-only refresh. |
| S012 | “straight” at 7.4667 s; “unreachable” at 39.2 s | Keep technical playback evidence separate; prepare a caption-only refresh. |
| S019 | “squares” at 49.0 s; “farthest” at 49.3667 s | Withdraw the new catalogue/lesson assignments before publication. The earlier correct written bridge remains. |

The shared renderer now uses the existing single stable bold phrase treatment. Two pixel tests verify that the phrase stays identical while its active word changes and disappears outside its cue. This repairs future encodes only; an already published movie does not change when source code changes.

Any immutable refresh must retain the approved narration, scripts, measured timeline and VTT, compare actual decoded output against its pinned source drawing, and pass playback checks for its own returned bytes. The existing published source must remain available for the old-frame comparison. Re-running a historical source comparison against the changed renderer would invalidate that comparison.

S019's completed production matrix, all six public asset digests and five integrated preview-route passes remain recorded in `../S019-public-release-20261125.json`. Those technical passes do not override this visible caption defect. `tools/prepare_spoken_film_release.py` now refuses the held S019 master, even when given successful production and publication metadata.

No final editorial completion, human listening or physical-device signoff is awarded by these checks. No learner records or practice questions were changed.
