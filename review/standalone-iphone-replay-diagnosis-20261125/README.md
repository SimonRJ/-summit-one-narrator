# Standalone iPhone replay timeout

The original failed device job **138873118795** in run **45497911900** reached the final full replay of the **50.8-second pyramid film** and timed out after 85.8 seconds. It had already completed all six chapter checks, the active caption cue, and the expandable counting explanation. Because the harness processes the welcome first, the source control flow and pyramid-specific timeout establish that the corrected welcome completed its 18 chapters, full replay and corrected transcript assertions.

The original job saved only two chapter screenshots. It did not preserve the failed replay's final playhead, paused/seeking state, media error or decoded frame. Its exact failure cause cannot be recovered from that evidence.

## Focused reproduction

The returned players archive and both movie hashes were verified, then the unchanged source player was served locally with the exact pyramid master. One pinned iPhone WebKit run repeated all six chapter selections, the caption cue, the counting explanation and the final replay. It reached `ended` at 50.8 seconds after approximately **50.9 wall seconds**, with continuing decoded frames and no page or media error. The chapter handler correctly brought the player back into view after the explanation had scrolled it offscreen.

This run used a fresh browser and did not repeat the preceding four-minute welcome playback. It supports a narrow non-reproduction finding, not certainty about the original CI cause or a replacement for its gate.

No product or timeout change is supported by these results. Root accepted **one retry of the original failed job**, using the same source and returned artifacts, after the complete original run concluded failure. This does not rerun upstream voice synthesis and preserves the already-generated scene 16 take. The retry result belongs in a later evidence entry.

`diagnosis.json` contains exact identities and the retry rationale. `local-pyramid-replay.json` preserves media events, decoded-frame counts, play promises, buffering and visibility from the focused run. The original failure excerpt and original chapter screenshots are retained. No signed download URLs, cookies or credential headers are included.

No learner state, movie bytes or production source was changed, and this record adds no editorial acceptance credit.
