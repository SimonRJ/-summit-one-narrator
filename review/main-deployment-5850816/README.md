# Deployed 5850816 source identity

Pages run **45516929578** completed successfully at **2026-11-25 00:35:16 UTC** for commit **585081646578fe8b0020d2dee831a8f853eb3bca**.

At **00:37:49 UTC**, all **14** checked public HTTP responses were byte-for-byte identical to that exact Git commit. They cover the index, application, service worker, course menu, gallery and guide page, their media/library modules, all four revised lesson/catalogue JSON files, and the offline reader page/module. Actual URLs, status codes, byte counts and SHA-256 values are in `live-byte-comparison.json`.

All **six declared routes** matched the immutable releases and previously verified movie hashes:

| Film | Slots | Release |
|---|---|---|
| S009 | 9, 228 | carry-reversal-reviewed-20261125-bcbd31159202 |
| S010 | 10, 319 | carry-reversal-reviewed-20261125-bcbd31159202 |
| S012 | 12, 248 | s012-missing-rung-20261125-b46d28d6d374 |

The application and gallery therefore declare the same movie editions and recorded guide metadata. The source check is pinned to the commit rather than a later local worktree HEAD.

## Scope

This is a source-delivery and mapping check. It does not exercise learner accounts, play the public videos, replace coordinated deployed route checks, or confer editorial acceptance.

`check_live_bytes.py` reproduces the read-only check. It requests the URLs actually referenced by this release, with its `priority-films-20261125` query revision where applicable, and compares the complete responses against `git show` from the pinned commit. It does not use a random cache-busting URL.

At the last recorded workflow snapshot, Pages and four QA workflows had passed; the lesson-opening and recorded-playback workflows remained queued. Their later status must not be inferred from this source-delivery result. `workflow-snapshots.json` retains the observed states.
