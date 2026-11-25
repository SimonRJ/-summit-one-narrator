# Held S015 numeral-caption timing evidence

The candidate from run **45512588528**, source **8fb7e5e6e3fbe8923c9c5152368b89efdeadef9b**, is held for caption timing. Its exact MP4 SHA-256 is `f4bb4b7e43d5d0037680d07ff8b65a375fd552f865406657d7e2b259604eca52` (8,459,211 bytes; 155.3 seconds). The returned artifact ZIP digest, movie digest, guide and render QA agree.

The saved voice performance and the mathematical artwork remain usable. This evidence adds no editorial or device acceptance credit.

## Concrete finding

The original timeline collapses all the words of **three hundred and forty four** to 30.74 seconds, which also becomes the phrase-caption start. A focused pass through the existing local recognizer, with numeral tokens suppressed, measures the spoken words from **29.80 to 31.06 seconds**. The resulting caption begins **0.94 seconds after the measured speech onset**.

`S015-30.14.png` is decoded from the actual candidate and has no caption during the high-confidence measured word **hundred** (29.94–30.24). `S015-30.84.png` shows the delayed caption. Decoded voice energy is strong during the first frame; this is not merely a missing word highlight.

The captions beginning with 24 and 54 start approximately 0.22 and 0.26 seconds after their measured onsets. The 24 onset is less certain (first-word probability 0.395), so its exact offset should not be treated as manually certified. Two other collapsed groups, 48 and 35, already occur inside earlier visible phrase captions; those observations do not show a missing phrase.

## Evidence and limits

- `caption-findings.json`: targeted finding, original anchors, measured intervals and decoded-frame observations.
- `number-word-onsets.json`: complete raw measurements for the two original source scenes only, including confidence values.
- `read-only-audit.json`: all six returned asset hashes, original collapsed words, and ordered positive phrase-cue checks.
- Returned guide, QA and recovery provenance establish the candidate identity and reused eight-take source.

The render job passed six recovery tests, 156 picture/caption comparisons and eight source-audio comparisons. Those comparisons use the same timeline to draw their reference, so they cannot independently certify the recognizer's original word timings.

`check_number_word_onsets.py` is the exact scratch diagnostic used for these measurements. It depends on the downloaded candidate at the explicit workspace path recorded in the script and the existing cached base.en model. It was run with `PYTHONPATH=/workspace/scratch/d5cfe38d5338/asr HF_HUB_OFFLINE=1 /workspace/scratch/45c9a6d8bd47/private-film-runtime/venv/bin/python`; no model download or voice generation occurred. These are recognizer measurements supported by decoded frames, not a claim of human-certified phonetic boundaries.

No original recording, source file, job, release or learner state was changed. The separate S009/S010/S012 audit found no corresponding numeric-anchor defect.
