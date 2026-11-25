# S019 caption-only refresh evidence

Local candidate:
`4a549a8cdb160102a38b9e9e63c409188f41406c300c05f2041694a3348d7a16`.
Held source:
`51545b1baf76d155f052fdcedc6bfde126e45c63845e97468166c0e069bc365f`.

- `caption-comparison.jpg` compares the exact 49.366667- and 50.033333-second
  frames. “Farthest” has doubled outlines in the held movie and one stable
  outline in the corrected candidate. Both final samples were inspected.
- `frames.json` identifies all six full-size decoded frame pairs. The four
  additional pairs straddle the start and end of scene 5.
- `boundary-comparison.json` checks those four boundary pairs. Their mean
  channel differences are all below 0.096 out of 255.
- `stream-preservation.json` records both streams' exact identities, hashes
  the original audio packet records and video timestamps, and confirms the
  preserved 6,673 audio packets and 4,269 video frames.
- `encoded-verification.json` records 143 source comparisons, including
  129 checks against the retained original scenes outside scene 5.
- `candidate-assets.json` hashes all six final local assets.
- `S020-compatibility.json` verifies the already returned S020 stable CI movie
  against its original source using the stricter preservation checks. It is a
  read-only compatibility check, not a new S020 encode or workflow run.

The source lossless audio, script, timeline, VTT and whole recording ZIP are
unchanged. The other ten scenes retain their original decoded content; their
H.264 packets are re-encoded, so picture packet identity is not claimed.
The final MP4 has not been published or mounted by this task. CI, browser,
immutable-release, deployed-route and final audible/editorial gates remain
open. See `docs/S019_CAPTION_REFRESH_20261125.md` and
`review/S019-stable-captions-candidate-20261125.json`.
