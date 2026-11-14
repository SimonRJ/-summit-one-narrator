# Video production

The visual and teaching standard is in [VIDEO_TEACHING_STANDARD.md](VIDEO_TEACHING_STANDARD.md). This document records what exists and how scripts become videos.

## Registry of teaching videos (14 November 2026)

| Status | Count | Which |
|---|---:|---|
| Finished and approved | 2 | T02.1 (the studio benchmark) and T02.2. Their audio must not be changed. |
| Script ready; not recorded, not animated | 70 | Every other item in `data/teaching-72.json`. |

The full list with lengths is generated at [production/scripts/INDEX.md](../production/scripts/INDEX.md).

Other finished public videos in `media/`: the AMC introduction, the welcome video, session introductions S001 and S002, and one AMC 2025 solution pilot. `media/T01.2_George_0.88.mp4` uses a retired voice and is a preview only; T01.2 now has a new script.

## Scripts

- **Source:** `production/scripts/src/*.txt`, one block per video.
- **Build:** `python tools/video/build_scripts.py` writes one JSON file per video to `production/scripts/` and regenerates the index. `--check` validates without writing.
- **Each script has:** a one-line goal; scenes tagged INSIGHT, WHY, PUZZLE, DEVELOP, VARIATION, RECAP; for each scene a visual direction and the narration; a notebook exercise with its answer for the producer.
- **Concept videos** open with the insight and why it matters before any puzzle, as the standard requires. **Worked examples** go straight to the problem.
- **Narration** is written for speech: numbers and operations are spelled out, with no symbols. The validator rejects symbols in narration and any reference to archive question codes.
- **Length:** 161 to 338 narration words each, 18,586 words in total. At an unhurried pace that is roughly two minutes of speech per video before pauses and animation time are added. Final timings must come from the recorded audio.

All examples in the scripts are original to Summit One. None reuses a competition question.

## From script to video

1. Read the script JSON and storyboard each scene from its `visual` field, following the T02.1 art system: matte background, one focal idea, objects that keep their identity as they move.
2. Record narration with the approved voice (`af_heart`, natural speed). An earlier preference recorded elsewhere as "Voice C" should be confirmed with the parent before a batch is recorded.
3. Time animation to the recorded audio. Do not stretch speech.
4. Burn in one caption layer only.
5. Check the mathematics on screen, caption alignment, legibility on a phone, and the published HTTPS link.
6. Change the script's status in the registry only when the video is published and checked.

## Review status of the scripts

The mathematics in all 70 scripts was checked by the author while writing; two errors found in notebook answers were corrected before release. The scripts have not been read by a second reviewer or tried with the learner. Treat them as ready for storyboarding, and expect small wording changes when they are recorded.
