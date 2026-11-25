# Publish the corrected domino, repeating-cycle and digit-swap films

S019's complete production workflow has succeeded, and all six immutable public assets have been downloaded and digest-checked. Its catalogue and two lesson assignments were staged and then withdrawn before publication: actual decoded scene-five frames show doubled glyphs. The helper now refuses S019 integration until a verified stable-caption replacement is pinned. S020 and S102 still require their complete production workflows and public-byte checks. A finished render or a partially passed playback matrix does not satisfy that gate.

| Film | Required run | Required public release |
|---|---:|---|
| S019 | 45491819969 | `s019-domino-condition-20261125-3d94f6856b47` |
| S020 | 45503875492 | `s020-stable-captions-20261125-0dfec081086f` |
| S102 | 45518273975 | `s102-tens-units-20261125-a84046b06450` |

The held S019 CI master has SHA-256 `51545b1baf76d155f052fdcedc6bfde126e45c63845e97468166c0e069bc365f`. Its earlier local playback evidence has a different hash. The published master passes technical playback but fails the targeted caption-quality check; do not mount it as the replacement. The S020 stable-caption CI render is `5308674d7d66dee6545d05699311a192b13e2fce2d48b6d2f560ec35ce1e57f3`; its returned artifact, guide and QA report agree. Its five playback and public-release gates still remain separate. The old doubled-caption master `fa00a38665821402f0a2060c40b4aa7ae4b89632609862a80607f39a4cc5006f` is explicitly rejected.

S102's isolated production run restores the one lossless saved Voice C take and measured passage timings. It does not synthesize another recording. Its exact CI master and public release are still pending. The helper additionally requires that exact source recording, the scene-eight-only scope, all five checked digit pairs, 21 total printed threes, four measured passages and a complete encoded-picture comparison record. Both earlier local numeral-timing masters are held.

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
