# Publish the corrected domino and repeating-cycle films

The corrected films are still held until their complete production workflows succeed. A finished render or a partially passed playback matrix does not satisfy that gate.

| Film | Required run | Required public release |
|---|---:|---|
| S019 | 45491819969 | `s019-domino-condition-20261125-3d94f6856b47` |
| S020 | 45503875492 | `s020-stable-captions-20261125-0dfec081086f` |

S019 must be the final CI master with SHA-256 `51545b1baf76d155f052fdcedc6bfde126e45c63845e97468166c0e069bc365f`. Its earlier local playback evidence has a different hash. For S020, use the final production hash; the local stable export is not a substitute for that release. The old doubled-caption master `fa00a38665821402f0a2060c40b4aa7ae4b89632609862a80607f39a4cc5006f` is explicitly rejected.

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

Use the corresponding files and `--lesson S020` for the cycle film. The helper checks the successful run, source commit, workflow path, published immutable tag, all six public asset locations, sizes and GitHub SHA-256 digests. It also checks the guide/movie/QA identities, chapter timing, exact S019 edition and S020 audio/caption-preservation evidence.

The output is a plan outside the repository. It never changes the live catalogue, source data, learner records or editorial completion credit. Pending workflows, drafts, missing assets, mismatched public bytes and the held S020 edition produce no plan.

## Apply only after verification

Use the plan's catalogue entry and field-level assignments. Preserve lesson 333's S019 technique bridge and lesson 283's S020 technique bridge. Update the canonical bridge in the content generator, refresh the combined catalogue/app/service-worker versions, then run the existing catalogue and read/practice checks. Verify gallery, active lesson and immutable notebook playback against the exact public files before final editorial acceptance.

If a corrected workflow is superseded by a different source commit or run, review that production evidence and deliberately update the helper's pinned policy first. It must not silently accept the latest release.

## Helper verification

Synthetic successful-release metadata was exercised against the actual local asset packages to check plan construction. Queued and in-progress workflows, wrong public digests and the held S020 package were rejected. Technique bridges were preserved, and all source data remained byte-identical. These helper tests are not evidence that either public release has completed.
