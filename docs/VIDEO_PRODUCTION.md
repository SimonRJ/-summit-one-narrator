# Video production

The visual and teaching standard is in [VIDEO_TEACHING_STANDARD.md](VIDEO_TEACHING_STANDARD.md). This document records what exists and how scripts become videos.

## Registry of teaching videos (15 November 2026)

| Status | Count | Which |
|---|---:|---|
| Finished and approved | 2 | T02.1 (the studio benchmark) and T02.2. Their audio must not be changed. |
| Published for review | 69 | Teaching films through T18.3 are available in [Teaching videos](../teaching-videos.html). |
| Script ready | 1 | The remaining items in `data/teaching-72.json`. |

The full list with lengths is generated at [production/scripts/INDEX.md](../production/scripts/INDEX.md).

Other finished public videos in `media/` include the AMC introduction, the welcome video, session introductions S001 and S002, and one AMC 2025 solution pilot. The four T01 studio films are available in the opening and replay screens for Lessons 1–4. Teaching videos in the course menu lists the published films in chapter order.

## Scripts

- **Source:** `production/scripts/src/*.txt`, one block per video.
- **Build:** `python tools/video/build_scripts.py` writes one JSON file per video to `production/scripts/` and regenerates the index. `--check` validates without writing.
- **Each script has:** a one-line goal; scenes tagged INSIGHT, WHY, PUZZLE, DEVELOP, VARIATION, RECAP; for each scene a visual direction and the narration; a notebook exercise with its answer for the producer.
- **Concept videos** open with the insight and why it matters before any puzzle, as the standard requires. **Worked examples** go straight to the problem.
- **Narration** is written for speech: numbers and operations are spelled out, with no symbols. The validator rejects symbols in narration and any reference to archive question codes.
- **Length:** The index includes word counts and planning estimates. Final timing comes from the recorded audio.

All examples in the scripts are original to Summit One. None reuses a competition question.

## From script to video

1. Read the script JSON and storyboard each scene from its `visual` field, following the T02.1 art system: matte background, one focal idea, objects that keep their identity as they move.
2. Record with the approved male Voice C at natural speed. The reference is `media/voice-audition/vox-australian-male-c.mp3`. Reuse the `openbmb/VoxCPM2` revision pinned in `production/voice-c-welcome/synth.py` and its reference prompt. The reference file matches the SHA-256 in `review/AMC2025Q17-voice-c.json`.
3. Time animation to the recorded audio. Do not stretch speech.
4. Burn in one caption layer only.
5. Check the mathematics on screen, caption alignment, legibility on a phone, and the published HTTPS link.
6. Record the checked video as published for review. Work through the teaching lessons in order and then produce the exam solution videos.

Studio sources are in `production/t01-studio/`. The Voice C workflow records groups of scenes with the approved reference. The render workflow aligns speech, animates the maths, and checks the final media. Each QA report in `review/` records the reference fingerprint, word alignment, format and playback duration.

The release workflow stages the next five consecutive films, or the final one, with their watch pages, transcript entries and verification reports. Each release saves the current count here and on the teaching video list. After GitHub Pages deploys, the workflow checks that each new watch page loads the same MP4 bytes as the verified export.

## Review status of the scripts

The mathematics in all 70 scripts was checked by the author while writing; two errors found in notebook answers were corrected before release. The scripts have not been read by a second reviewer or tried with the learner. Treat them as ready for storyboarding, and expect small wording changes when they are recorded.
