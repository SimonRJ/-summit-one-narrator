# S102: correct the tens/units pairing

## Scope and current state

This is a scoped mathematical correction to scene 8 of **Digit sums and counting digits in ranges**. The other ten narration passages and their original pictures are retained. The single approved-voice take completed at 32.29 seconds and is saved losslessly. The final local corrected master has passed encoded comparisons; **there is no gated production release, final editorial acceptance, or changed live assignment yet**.

The old narration says “swapping the two end digits”. For the required pairing, 153 must become 135. Hundreds stay fixed; tens and units swap. Reversing the operation returns the starting number. Keeping the hundreds digit is what preserves the full interval 100–599.

### Temporary correction beside the published film

Until the verified replacement is mounted, the bridge cues for consumers **102** and **296** explicitly correct “two end digits” to **keep hundreds fixed and swap tens and units: 153 becomes 135**. Session 102 retains its separate-column counting cue; session 296 retains its multiples-of-nine and missing-digit cue. The same correction appears on Read, Watch and the locked completed replay, using the existing bridge rendering. The existing public-guide note mechanism also adds a correction specifically for `S102-Intro.mp4`.

These are temporary wording corrections, with matching entries in the existing generator revisions. Questions, marking, saved answers and movie URLs are unchanged. When the verified S102 replacement is assigned to both consumers, replace both temporary bridges and their generator entries with cues for the corrected film, and remove the old-file guide note. The filename-specific note does not apply to the replacement's `S102.mp4` asset. This text correction does not itself count as a repaired or accepted film.

| Units-column occurrence | Tens-column partner |
| --- | --- |
| 153 | 135 |
| 243 | 234 |
| 333 | 333 |
| 423 | 432 |
| 513 | 531 |

The fixed point 333 remains in both column counts. Each column has five occurrences. The untouched next scene supplies the eleven hundreds occurrences, giving 5 + 5 + 11 = 21. `digit_swap_scene.check_maths()` independently enumerates every eligible multiple of nine and checks the mapping, inverse, digit sum, hundreds digit and counts.

## Corrected spoken scene

Fix the ones digit at three. For hundreds digits one through five, the tens digits are five, four, three, two and one. Now keep the hundreds digit fixed and swap the tens and units digits. One hundred and fifty-three becomes one hundred and thirty-five. The digit sum and hundreds range are unchanged. Swapping back recovers the original, so this pairs the two lists exactly. The ones and tens columns contribute five each. Three hundred and thirty-three contributes once to each column.

The corrected generator retains all other S102 narration verbatim. Its common positional wording is also corrected for future regeneration of the other digit-sum visits; their published films are not replaced or credited by this change.

## Source and recording identity

- Original movie: `https://github.com/SimonRJ/-summit-one-narrator/releases/download/lesson-introductions/S102-Intro.mp4`
- Original movie SHA-256: `538f9142a5113e5d14d3a35b6a7851e8dd331e16aba7d98224a7d0c294601612`
- Original public guide SHA-256: `4ff0df3427a7f09492a68252f931a1c2b39dcf98aaa4ea3af60b99b086c38b94`
- Recovered original word timeline SHA-256: `81837aeb40efb9e7d5c6f1fed5994a504d0e939c29b20e36c201a8e63af5244e`
- Corrected scene narration SHA-256: `25199fc25ed5d068cddd06cc45faf56d0821748ebc59a31b69afbe2dc32aa50e`
- Voice C reference SHA-256: `0f3304a393ee504e9fa22537267ac03f150569a5fab0859616f261d009513362`
- VoxCPM2 model revision: `7936080b41163874f38610f46f438e2c0757f9fd`
- VoxCPM runtime commit: `300e4260b509066151d623dc9c0aa922cf82232b`

The original public guide contains exact scene starts but no word timing. `source-timelines/S102-public.json` records measured timing recovered from that pinned movie with the established `base.en` recognizer. Preserved scenes align at 94.51–100%. The discarded faulty scene scores 84.15% because the recognizer prints forms such as “100's”; it is not part of the replacement acceptance gate. Embedded captions in the ten retained scenes remain in their original pictures. New scene captions use one stable glyph layer.

The frame-aligned splice is original frames 3750 through 4589 (125.0–153.0 seconds). The last 40 ms before both boundaries have maximum decoded amplitudes below 0.005. The replacement is padded at natural speed to a complete 30 fps frame; later chapters and measured caption timings shift by the same duration difference.

The source take was recorded once with this command; reproducing the correction restores the saved take:

```sh
python production/t01-studio/synth.py --lesson S102 --scene 8 --threads 2
```

Restore its original samples and identity into the build directory:

```sh
python - <<'PY'
import sys
sys.path.insert(0, 'production/lesson-films')
from repair_digit_swap import saved_recording
saved_recording()
PY
```

The preserved source is `production/lesson-films/voice-c-repairs/S102-tens-units.flac` plus its identity JSON. Its SHA-256 is `4582dcd016527a350da681f165b53e32ade863c7e3ea011aa5863e892cb8593b`. All 1,549,920 PCM samples match the original 32.29-second WAV exactly. The workflow requires this exact digest and cannot synthesize a duplicate.

## Stable timing for the spoken numbers

The first full-take recognizer returned zero-duration timestamps for 153 and 333, although it recognized the correct numbers. That made their captions late. The saved timing file now aligns each of the four original recorded passages separately, suppressing numeral tokens so the recognizer times the full spoken words. Their 150 ms inter-passage gaps are verified against the exact zero samples in the original take. All 81 spoken words now have positive, ordered durations; passage recognition scores are 100%, 97.96%, 100% and 100%.

The renderer checks the timing file against the exact FLAC hash and complete narration, then reuses these measured word times. It independently checks the full take again for content. Neither alignment nor rendering changes the audio samples or voice speed.

The full-take recognizer also printed a low-confidence extra “each” (probability 0.036). Focused tail recognition with and without silence filtering did not repeat it. The unedited take remains the source, and the complete listening review remains pending. These recognition results are evidence for review, not a claim of final listening acceptance.

The first local movie, `dad309128905a96c6b3784b63eb12df2b6545ffe9fc930b7cf7ded0c89b9cec4`, is held because it has the late numeral timings. Use the final measured-timing candidate and, ultimately, the separately verified production release.

## Final local candidate

- Movie SHA-256: `e627ab6df0a16f75adce97fdbf021013a84cf01b3d124ca43dc8afa7b2fc947a`
- Duration: 215.633333 seconds; 1920 × 1080 at 30 fps.
- Full-take recognition: 98.22%; saved passage timing scores: 100%, 97.96%, 100%, 100%.
- Minimum correlation across all eleven scene audio spans: 0.999958.
- 216 decoded reference comparisons across the entire film; largest mean picture/caption differences: 2.112 / 1.592 (limit 5).
- Final AAC packets are identical to the initial render: timing corrections changed pictures and captions only.
- Encoded proof frames were inspected for the 153 ↔ 135 pairing and 333 fixed point. Both numeral phrases now have full spoken-word durations.

Complete evidence and every local asset hash are in `review/s102-digit-swap-local-qa-20261125.json`. This local digest is a review identity. The eventual CI master must pass its own exact-byte device and public-download gates.

## Render, gates and immutable release

```sh
python production/lesson-films/repair_digit_swap.py build/s102-candidate
```

The builder pins source bytes, checks the narration and voice hashes, validates the mathematical pairing, measures replacement ASR alignment, preserves natural speed, verifies complete decoding, checks every scene's waveform correlation, and compares intended picture and caption regions once per second through the entire corrected master. These checks support review; they do not substitute for a complete listen/watch.

`.github/workflows/s102-digit-swap.yml` contains saved-take restoration → render → five-profile playback → immutable release. The isolated `production/s102-digit-swap` branch was published once at `a84046b0645063f273951ce85d938aa71fffa9ee`, with tree `d6988eba0b6b56646526a9745fa28e7f8e74709d` exactly matching the reviewed local source. It started run `45518273975`; its saved-take restoration job was queued at the recorded checkpoint. This branch does not update main or live lesson assignments, and contains no synthesis path.

The workflow checks iPhone and iPad in portrait and landscape plus PC, and checks consumer 296 on PC and iPad portrait. The release tag is `s102-tens-units-20261125-<commit-prefix>`. The six release assets are `S102.mp4`, `S102.vtt`, `S102-guide.json`, `S102-poster.jpg`, `S102-recording.zip`, and `S102-qa.json`; returned public bytes must match. The workflow does not change the live catalogue or learner records.

`tools/prepare_spoken_film_release.py --lesson S102` pins this source commit, run and exact immutable tag. It prepares a field-level integration plan only after the successful full workflow and all six public-asset digests have been verified. It rejects the held local timings, a different Voice C take, changed proof counts or an old-guide bridge. Preparation adds no editorial credit.

## Integration and remaining acceptance

Consumers are **102** (dedicated film) and **296** (technique film). Integrate only a successfully gated, immutable public release whose movie digest matches its guide and QA report. Update both movie URLs together and remove the temporary wording-error sentence for the new film only. The final guide supplies this canonical 102 bridge:

> Keep the hundreds digit fixed and swap tens and units: 153 becomes 135. Count the printed threes in each column separately.

Preserve the independent 296 technique prompt with this post-release bridge:

> For the multiples-of-nine count, keep hundreds fixed and swap tens and units: 153 becomes 135. Which digit choices force the missing digit?

Update the matching `S102` and `S296` bridge overrides in `tools/content/practice-revisions-20261121.json` together with those two route rows. The integration plan includes both overrides so regeneration cannot restore the old warning underneath the corrected film. Every practice item remains unchanged. Recheck the live gallery, active lesson and immutable completed-notebook routes; old completed notebooks still need the old-film wording clarification when they retain that old movie.

This repair earns no blanket “100% complete” or originality credit. The full corrected take still needs listening review; the exact production master needs all playback gates; and S102's four shared template scenes and related example family remain part of the broader originality work.
