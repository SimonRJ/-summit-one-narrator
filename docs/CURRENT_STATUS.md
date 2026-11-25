# Summit One current status

The [live progress bar](../review/course-progress.html) reads the current [review scope](../review/course-review-scope.json), [lesson film register](lesson-introduction-review-register-20261116.csv) and [companion film register](teaching-video-review-register-20261116.csv). Signed-in learners can see every released practice set in [the exam centre](../tests.html).

## Priority repair pass — 25 November 2026

This revision brings the learner player back into agreement with the already published companion editions for T05.2, T05.3, T06.1, T06.3 and T16.3. The missing T16.3 mapping suppressed its finished video in the optional lesson review; the other four mappings retained older cache tokens. The app and service-worker revisions change together so existing installations fetch the corrected routes. `tools/check_companion_release_routes.mjs` now checks all 72 public watch pages against the catalogue and learner resolver during release QA, including rejection of protected or unpublished film IDs.

The affected mapped lessons were also exercised through current-lesson review and the locked completed notebook using the exact current companion media, desktop Chromium and iPhone WebKit emulation. All 12 route checks decoded and played the expected edition, preserved the fixture's answers and progress, and made no learner-state writes. See [the route evidence](../review/companion-learner-routes-20261125.json). The public review list now includes the already approved T12.E film: its 42 reviewed entries and the separate two previously approved films agree with the 44 approved companion register entries.

The earliest film repairs are saved with precise publication boundaries:

- **S009 and S010:** the immutable release is now published. All twelve returned assets match their published digests, and both movies match the exact candidates that passed rendering and five-profile playback. This revision integrates the returned guides and assigns the new films to lessons 9/10 and technique revisits 228/319, preserving all practice content and grading editions. Application, gallery and offline dependencies share a new cache revision. Live Pages delivery and final editorial acceptance remain separate gates. See [the candidate review](CARRY_REVERSAL_CANDIDATE_REVIEW_20261125.md).
- **S012, S015 and S017:** original missing-rung, mail-train and tile-frame sources are saved. S012's immutable release has passed its five candidate profiles; all six returned assets match their published digests. This revision assigns it to lessons 12 and 248 while retaining both bridges. S015 recovery run `45512588528` encoded the eight exact saved takes, but a targeted audit found the 344 caption starts about 0.94 seconds after the spoken phrase. That candidate is held while the measured word timing is repaired; no recording needs repeating. All eight S017 recordings are also complete. Its pre-encode audit found the same collapsed-number timing for “twenty four”, so that correction is being carried into its isolated recovery source before execution. See [the early-study evidence](EARLY_STUDY_CANDIDATES_20261125.md).
- **S019:** the spoken domino condition correctly specifies the two leftmost top-row squares. Its exact CI master passed five playback profiles; all six immutable public assets match their digests, and five integrated preview routes passed. A subsequent decoded-frame review found doubled caption glyphs during scene-five emphasis transitions. Its staged assignments have therefore been withdrawn before publication. The exact approved audio, timeline and VTT can be retained for a stable-caption refresh; the existing accurate written bridge remains in place.
- **S020:** the spoken explanation distinguishes exponent 49 from position 1 in the repeating cycle. The stable-caption CI render is complete and its exact returned artifact, movie, guide and QA agree. The decoded 145.5-second frame has one clear “position” caption, and the corrected scene's number words all have positive timing. Its five browser profiles, later lesson 283 and immutable public-release gates remain required. The approved Voice C audio packets and VTT timing are preserved.
- **T05.1, T13.3 and T16.3:** the current corrected masters have targeted mathematics, caption and playback evidence; their stale register descriptions have been reconciled. **T18.1** has a corrected caption candidate whose publication remains pending. See [the companion acceptance evidence](../review/companion-correction-acceptance-20261125.json).
- **S102:** the 153 → 135 example now has a precise source correction: keep hundreds fixed and swap tens/units. The single Voice C take is saved losslessly; its measured-timing local master verifies all five reversible pairs, including 333, and preserves the other ten performances. Isolated run `45518273975` restores that exact recording for CI rendering and device/public-byte gates, with no synthesis path. The temporary correct instruction beside the existing film in lessons 102/296 and its public guide remains required until the replacement is verified and integrated. Those cues passed iPhone Read, Watch and locked-replay checks. See [the scoped correction](S102_DIGIT_SWAP_REPAIR_20261125.md).

Candidate encoding and browser playback checks do not award final editorial completion. This repair pass does not increase the 44 approved companion count or alter practice questions, authentic papers, grading, learner answers or progress. Repository integration, Pages deployment and final editorial acceptance are tracked separately.

The three-film release at `585081646578fe8b0020d2dee831a8f853eb3bca` is now deployed. Its fourteen public app/page/catalogue responses match that commit byte for byte, and all six S009/S010/S012 lesson declarations select the intended immutable releases. The [live deployment evidence](../review/main-deployment-5850816/README.md) records that completed delivery boundary. Subsequent source corrections form the next revision; they are not covered by the earlier deployment claim. Actual decoded frames also expose doubled regular/bold captions in S009, S010 and S012. Their technical route checks remain valid, but a caption-only refresh is required before final editorial approval. See [the exact frame findings](../review/caption-layer-holds-20261125/README.md).

The companion player now takes each valid released edition directly from the teaching catalogue. It accepts only the 72 public companion IDs and their exact relative movie paths, rejects invalid declarations, and retains established fallbacks for blank legacy entries. All 72 current routes, all 72 simulated edition changes and 14 unsafe URL cases pass. The [earlier delivery checkpoint](../review/companion-catalogue-delivery-20261125.json) caught the old T16.3 movie before deployment. After Pages deployed `0dfec081`, the corrected public master and its five supporting app/page/catalogue files matched that source byte for byte. Its live current-lesson and completed-notebook routes passed on PC and iPhone emulation with no fixture writes. See [the completed live-delivery check](../review/companion-live-delivery-20261125.json).

An actual warmed service-worker and browser HTTP cache now verifies the update path. The old URLs remain stale as a negative control, while the new application, gallery, teaching catalogue and reader select the intended editions before the new worker can install. After activation, a fresh S010 reading also loads with its local origin shut down. The check exposed dark gutters around the offline reader; its page canvas now uses the same light theme as the body and lesson picker. See [the cache-upgrade results and before/after images](../review/cache-upgrade-20261125/README.md).

**19 November 2026 lesson structure.** All 283 teaching lessons now use Read → Watch → Practise. The [later lesson index](LATER_LESSONS.md) records the video assignment and problems for the remaining 228 lessons.

**First release through S068.** The [55 teaching sessions through S068](READ_WATCH_PRACTISE.md) now use Read → Watch → Practise. This adds a separate versioned bank of 220 protected questions, alongside 92 selected challenges from the original bank.

**14 November 2026 baseline.** The repository, public site and live database are verified separately. See [the lesson audit register](CONTENT_AUDIT_REGISTER.md) for the editorial checks and [the continuation](CHATGPT_CONTINUATION.md) for the release procedure.

## Content inventory on 14 November

| Item | Count |
|---|---:|
| Course sessions | 372, comprising 283 lessons, 53 investigation visits and 36 mock slots |
| Techniques | 52 |
| Standard Try and Transfer problems | 566 |
| `content_problems` rows | 760, comprising 608 original and 152 authentic-linked |
| Learner attempts at the start of the audit | 7 on O001T, O001X, O002T and O002X |
| Exam sittings at the start of the audit | 0 |

## Standard lesson bank

| Check | Result |
|---|---:|
| Prompts and worked solutions individually reviewed | 566 of 566 |
| Answers checked by a separate calculation or enumeration | 566 of 566 |
| Revised in the full-bank audit | 469 |
| Retained after an earlier individual review | 93 |
| Retained as saved, with learner attempts | 4 |
| Distinct titles and number-normalised stems | 566 each |
| Repeated number-normalised stems beyond the first occurrence | 0 |
| Figures, charts and tables rendered at 320 and 390 CSS pixels | 113 |

The audit began after the earlier spatial and data-reading batches, when 286 problems still shared an earlier number-normalised stem. This pass reviewed the remaining 464 problems and followed up on nine from earlier batches. The originality screen used the installed 19-paper archive, including OCR for 447 image-backed questions, and manual comparison of the closest matches. The difficulty bands in the register are estimates of the reasoning demanded by Upper Primary questions at those positions.

| Estimated AMC Upper Primary band | Problems |
|---|---:|
| Q1–10 | 2 |
| Q11–20 | 204 |
| Q21–25 | 302 |
| Q26–30 | 58 |

The checks cover the 566 standard lesson problems. Retrieval cards, extra technique drills, MAWA investigations, original practice papers and Rossmoyne mocks have their own content and release status.

### Release verification

The bank shipped in [PR #12](https://github.com/SimonRJ/-summit-one-narrator/pull/12), content commit `498072d13e07c46d4b5449f7f3fe2f2c07eb37d3`. Teaching behavior checks, Summit One release QA, AMC split training QA and the Pages deployment passed. The live Pages lesson manifest, renderer, entry page, application script and service worker matched the shipped files byte for byte.

A single guarded database update revised 469 unattempted rows. All 566 live standard lesson rows matched the generated release, with an aggregate fingerprint of `5848d505c470b06d8c0cb7741b663778`. The authentic AMC catalog, questions, linked problems and seven recorded learner attempts matched their fingerprints before and after the update. Two saved session records and zero authentic exam sittings were confirmed afterward.

A phone-width browser fixture used a local copy of the verified Pages assets to exercise submission, diagram rendering and solution reveal with test data. The actual learner’s progress was preserved.

## Examination papers on 14 November

| Category | Active | Inactive | Notes |
|---|---|---|---|
| Authentic AMC past papers | 19 papers, 570 questions | none | Frozen. See [authentic AMC freeze](AUTHENTIC_AMC_FREEZE.md). |
| Original AMC Part A / Part B split papers | 4 entries, 60 questions | 1 entry, 10 questions | Earlier plan called for about 30 sets per part. |
| AMC split familiarisation sets | none | 20 entries, 300 questions | Uses earlier questions. |
| Original authored mocks | 9 Rossmoyne-style papers, 207 questions | 10 AMC-style papers, 300 questions | |
| Earlier Summit-authored mocks | none | 25 papers, 750 questions | Retired. |
| Earlier Rossmoyne-authored mocks | none | 11 papers, 253 questions | Retired. |
| User-supplied original sample | 1 paper, 23 questions | none | |

## Videos and guides on 15 November

| Item | Status |
|---|---|
| Teaching videos | 72 of 72 online through T18.E. [Watch in teaching order](../teaching-videos.html). |
| Teaching scripts | 0 awaiting production |
| Lesson introduction videos | Lessons 1–6 online in the Video step and completed lesson review. [Watch in lesson order](../lesson-introduction-videos.html). |
| Other finished public videos | AMC introduction, welcome and one AMC solution pilot |
| Guides | [Student guide](STUDENT_GUIDE.md) and [parent guide](PARENT_GUIDE.md) |

## Verification commands

| Command | Checks |
|---|---|
| `tools/content/audit_all_lessons.py` | Canonical IDs, title and stem uniqueness, wording and required answer format |
| `tools/content/check_reviewed_lessons.py` | Answer calculations, fingerprints of checked prompts and exact agreement with the public diagram manifest |
| Both commands with `--solutions PATH` | Comparison of all 566 private answer keys to the calculations and consistency of final-answer lines |
| `tools/content/check_curated_{batch2,spatial,data}.py` | Independent checks for the earlier three releases |
| `tools/browser_lesson_fixed.py` | Layout of every prompt and figure at 320 and 390 CSS pixels and the lesson flow across phones, tablets and desktop |
| The browser test with `SUMMIT_ONE_LESSON_SOLUTIONS` set | Layout of all 566 worked solutions at both phone widths |
| `tools/check_learning.mjs`, `tools/check_fixed_lesson.mjs`, `tools/check_split_training.mjs` | Course mapping, lesson behaviour and AMC split structure |
| `tools/check_amc_freeze.sql` | Read-only fingerprints of the authentic archive and recorded attempts |
