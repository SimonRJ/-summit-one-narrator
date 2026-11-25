# Publish the corrected domino, repeating-cycle and digit-swap films

S020 and S102 have completed their production workflows, all five playback profiles and independent public-byte checks. Their exact returned guides are integrated with both canonical and technique-consumer assignments in this revision. S015 has separately completed the same public-release boundary and its twenty-one compound-number timing checks; its returned guide is assigned to lessons 15 and 260. Application deployment and final editorial acceptance remain separate evidence boundaries.

S019's earlier production workflow succeeded and all six immutable public assets match their digests, but actual decoded scene-five frames show doubled glyphs. Its staged assignments were withdrawn before publication. The helper refuses that edition. The replacement source is published at `ac244dec713654fa7fb47693c8c179d9fb436479`, run `45524933207`; verify that complete workflow and exact returned public assets before changing its pinned policy or assignments.

| Film | Required run | Required public release |
|---|---:|---|
| S019 | 45491819969 | `s019-domino-condition-20261125-3d94f6856b47` |
| S020 | 45503875492 | `s020-stable-captions-20261125-0dfec081086f` |
| S102 | 45518273975 | `s102-tens-units-20261125-a84046b06450` |

The held S019 CI master has SHA-256 `51545b1baf76d155f052fdcedc6bfde126e45c63845e97468166c0e069bc365f`. Its earlier local playback evidence has a different hash. The published master passes technical playback but fails the targeted caption-quality check; do not mount it as the replacement. The verified public S020 master is `5308674d7d66dee6545d05699311a192b13e2fce2d48b6d2f560ec35ce1e57f3`; its returned artifact, guide and QA report agree. All seven actual public assets match their GitHub digests. The old doubled-caption master `fa00a38665821402f0a2060c40b4aa7ae4b89632609862a80607f39a4cc5006f` is explicitly rejected.

S102's successful isolated production run restored the one lossless saved Voice C take and measured passage timings. It did not synthesize another recording. Its exact public master is `f08e10363f675d7cb9e46fd31e5f766fdbbacd248af3ddded95b2a06eb40f6e1`. All six actual public assets match their digests. The helper verified that exact source recording, the scene-eight-only scope, all five checked digit pairs, 21 total printed threes, four measured passages and all 216 encoded-picture comparisons. Both earlier local numeral-timing masters remain held.

S015's public master is `19765de3ce9c28259d244c41d370cb3073513bc928124167e58cc21497098c89`, from run `45522486565` and source `41b7922d37ed4415b8798f6af1da4b7a1a8f1ae0`. Its six actual public assets match their digests; all 7,280 original AAC packet payloads and timestamps are preserved. The returned recording archive matches the reviewed corrected timeline/VTT, unchanged script and FLAC, with all twenty-one complete compound-number groups retained in their captions.

## Prepare a checked integration plan

Save the unmodified REST payloads for the required workflow run and release, then download the six public release assets: movie, VTT, guide, QA, poster and recording archive. Run:

```sh
python tools/prepare_spoken_film_release.py \
  --lesson S019 \
  --run-report /tmp/s019-run.json \
  --release-report /tmp/s019-release.json \
  --package /tmp/public-s019 \
  --output /tmp/s019-integration-plan.json
```

Use the corresponding files and `--lesson S020` or `--lesson S102` for the other corrections. The helper checks the successful run, source commit, workflow path, published immutable tag, all six public asset locations, sizes and GitHub SHA-256 digests. It also checks the guide/movie/QA identities, chapter timing and each correction's required evidence.

The output is a plan outside the repository. It never changes the live catalogue, source data, learner records or editorial completion credit. Pending workflows, drafts, missing assets, mismatched public bytes and either held S019 or held S020 edition produce no plan.

## Apply only after verification

Use the plan's catalogue entry and field-level assignments. Preserve lesson 333's S019 technique bridge and lesson 283's S020 technique bridge. For S102, replace the temporary old-film correction in both lessons 102 and 296 with the separately specified canonical and technique prompts. Apply both `canonical_opening_bridge` and `additional_opening_bridges` to the generator's revision file; otherwise regenerating lesson 296 would restore its old-film warning. Retain the filename-specific old-film clarification for saved notebooks that still reference `S102-Intro.mp4`. Refresh the combined catalogue/app/service-worker versions, then run the existing catalogue and read/practice checks. Verify gallery, active lesson and immutable notebook playback against the exact public files before final editorial acceptance.

If a corrected workflow is superseded by a different source commit or run, review that production evidence and deliberately update the helper's pinned policy first. It must not silently accept the latest release.

## Helper verification

Synthetic successful-release metadata was exercised against the actual S019/S020 CI packages and the S102 local package to check all three original plan paths. A later frame review placed S019 on hold, so its once-successful historical fixture is superseded by the explicit rejection. Queued workflows, wrong source commits, wrong public digests, a different S102 take, changed mathematical totals, missing passage timing and incomplete picture checks were rejected. Existing S019/S020 technique bridges were preserved; S102 received its two distinct corrected prompts. All source data remained byte-identical. See [the helper checks](../review/spoken-release-plan-checks-20261125.json). These fixture checks are not evidence that any pending public release has completed.
