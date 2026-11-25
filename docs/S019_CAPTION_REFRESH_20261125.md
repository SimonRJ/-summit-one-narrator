# S019 — stable captions for the approved domino condition

The prepared local candidate is
`4a549a8cdb160102a38b9e9e63c409188f41406c300c05f2041694a3348d7a16`.
It replaces only the caption treatment in scene 5 of the returned
`51545b1baf76d155f052fdcedc6bfde126e45c63845e97468166c0e069bc365f`
edition. That earlier movie remains held for doubled caption glyphs and must
not be installed merely because its route and public-byte gates passed.

The condition remains exactly the approved one: cross out columns 1 and 2 of
the top row. One domino covers columns 3 and 4, and two horizontal dominoes
cover each lower row. The seven dominoes cover all fourteen remaining squares
without overlap, seven of each colour. The narration, transcript, bridge,
chapter starts and mathematical drawing are unchanged.

## Exact preservation and checks

Scene 5 occupies frames 1,348 through 1,767 at 30 fps. It now uses the same
single bold phrase treatment as S020. The ten other scenes come from the
original decoded movie; the combined picture is re-encoded, so their original
H.264 packet bytes are not claimed to be identical.

| Check | Result |
| --- | --- |
| Original AAC packet payloads and timestamps | All 6,673 identical |
| Video presentation and decode timestamps | Identical |
| Video frames | Exactly 4,269, preserved from the source |
| Video / audio / container durations | 142.30 / 142.33 / 142.33 seconds, unchanged |
| VTT and complete recording ZIP | Byte-identical |
| Timeline, script and lossless narration inside the ZIP | Byte-identical |
| Guide fields other than movie hash | Unchanged |
| Decoded comparisons | 143 whole-second checks passed |
| Maximum picture / caption difference | 1.895 / 1.988 out of 255 |
| Other ten scenes | 129 comparisons; maximum differences 0.116 / 0.349 |
| Scene boundaries | Four adjacent frame pairs checked; mean differences below 0.096 |

The source has slightly less video than audio. The refresh preserves the
measured 4,269-frame stream; it does not add a frame by rounding the container
duration. Four regression tests cover that case, changed audio timing,
the approved leftmost-pair condition and default S020 compatibility.
The two shared caption pixel tests also pass.

The exact decoded 49.366667-second frame shows “farthest” with a single
outline, where the held movie visibly blends two outlines. The frame at
50.033333 seconds is also clean. The frame pairs, stream identities, asset
hashes and encoded report are in
`review/evidence/S019-stable-captions-20261125`. The complete handoff record is
`review/S019-stable-captions-candidate-20261125.json`.

## Isolated production path

The new workflow `.github/workflows/s019-caption-stability.yml` is restricted
to `production/s019-caption-stability` or manual dispatch. It retrieves the
exact six assets from release `s019-domino-condition-20261125-3d94f6856b47`,
verifies the release identity and asset hashes, refreshes scene 5, checks all
preserved stream timestamps, and compares the encoded pictures. It performs
no speech recognition, model download, synthesis or timeline realignment.

The candidate then needs five canonical browser profiles plus technique
consumer 333 on PC and iPad portrait. Only after those gates pass does the
workflow publish a separate immutable edition and compare the returned bytes.
The eventual installation remains dedicated slot 19 and technique slot 333;
the technique bridge comparing adjacent removals with opposite corners is
preserved in the candidate fixture. No learner state or live routing was
changed by this local work.

`recaption_spoken_condition.py` still defaults to S020 and keeps its original
input pins. The existing returned S020 stable CI movie passed the new stream
identity checks against its held source without another render. S020's push
trigger is now limited to its production branch, so this shared source change
cannot launch another S020 job when main is published. Manual dispatch and
the existing run are unaffected.

## Acceptance still open

This local candidate has no claimed new CI, browser, immutable-release or
deployed-route result. The parent owns publication and must verify the exact
returned master, whose encoding hash may differ from this local one.
Final audible/editorial acceptance remains separate. The inherited scene-5
recognition score is 96.2%; preserving its audio is not a new human listening
signoff. Every new review record retains `final_editorial_credit: false`.
