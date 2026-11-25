# Release cache upgrade evidence

The release was checked against the actual `2cc35f1` service worker and public files, using current release `a8ae5f6` plus the offline reader root-colour correction. No production backend, learner records, or media files were changed by this check.

## What the browser test proves

The test first installs the older worker and warms its Cache Storage and the browser HTTP cache. Public assets deliberately receive a fresh, long-lived HTTP-cache response, making stale browser-cache reuse reproducible. The server then switches to the current files while holding the new `sw.js` response. This prevents the new worker from refreshing any assets before the current-page assertions.

The old URLs remain stale as a negative control: T16.3 still resolves to `teaching-films-v1`, and the old recorded-study catalogue has no S009/S010 entries. Under that same old controller, the new URLs load:

- S009 and S010's current reading bridges and immutable movie routes.
- T16.3's `score-notebook` catalogue declaration.
- Current gallery titles and the S010 guide's title, chapters, and movie route.
- The current offline-reader manifest before the new worker can install.

The test then permits installation, verifies activation and removal of the old cache, shuts down the local origin, and opens a fresh page with the browser offline. S010's new reading still loads. The lesson picker retains the intended available readings: session 1 and the readings opened during the test, sessions 9 and 10.

This is a real Chromium service-worker and HTTP-cache test using the repository's isolated learner fixture. Playwright request routing is deliberately unused because it disables the HTTP cache being tested. Movie routes are inspected; movies are not played and this evidence adds no editorial acceptance credit.

## Observed theme defect and correction

`before.json` records a passing cache upgrade before the visual correction. Its body and picker computed colours were light, but `offline-reader-before.png` shows dark navy canvas gutters outside the centred, maximum-width body. The reader's inline `:root` background and colour scheme remained dark.

The narrow correction makes that root background `#f6f7f4`, with dark root text and a light colour scheme. The body and picker retain their existing styles. `after.json` includes computed canvas, body, and picker colours from the fresh offline page; `offline-reader-after.png` shows the corrected canvas. The test now also asserts the light root background and colour scheme.

## Reproduce

Use Python with `aiohttp` and Playwright, plus an installed Chromium runtime:

```bash
python tools/check_release_cache_upgrade.py \
  --root . \
  --previous-ref 2cc35f1 \
  --output /tmp/amc-cache-upgrade \
  --chromium /path/to/chromium
```

The optional `--browser-flags` accepts a file containing the runtime's JSON argument array, or its existing two-line executable-path/JSON format. The report records the browser version and SHA-256 hashes of the application files it checks. The fixture snapshots files into memory; it does not alter either checkout.
