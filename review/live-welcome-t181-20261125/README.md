# Bounded live welcome and T18.1 smoke check

Both public watch routes passed after the parent confirmed successful Pages run **45528346333** for commit `d51e1382373a03aa0a3a828cfffa0a2a6c6a0198`. This has the exact frozen source tree `de6b0b43b98bba31a2a6ec3cf633210c1c2b3bdf`, prepared locally as `e287b9102574b8a6cbc29beba97ccc9a7dc569fe`. No live navigation was made before that success signal.

The check visits only the public `welcome.html` and `watch-t18-1.html` routes in fresh iPhone WebKit contexts. It verifies the served page identity, local font loading and horizontal layout, the first actual chapter control, and one repaired chapter. The welcome sample plays from the Part A/Part B chapter to the corrected clock description. T18.1 plays from the rectangle chapter to the corrected perimeter caption. Both samples use normal-speed, unmuted playback and decoded frame callbacks. Neither film receives a full replay.

The script blocks actual Supabase and all non-GET/HEAD requests, disables service workers, and supplies no learner credentials or session. It checks that browser storage remains empty. Evidence consists of route results, initial and repaired-frame screenshots, media-event traces and the parent-supplied Pages identity. Exact public asset byte verification is owned by another agent.

This is modest live delivery evidence from emulated WebKit. It adds no physical-device, human-listening or final editorial acceptance credit.

## Results

| Public route | Actual chapter controls checked | Selected decoded frame | Result |
| --- | --- | --- | --- |
| Welcome | 0.00 and 228.42 seconds | 243.766666 seconds | Passed |
| T18.1 | 0.00 and 61.40 seconds | 79.90 seconds | Passed |

Both pages match their frozen HTML bytes and expected media URL. Both load Source Sans 3, Source Serif 4 and Source Code Pro from the site, have zero horizontal overflow, open the expected transcript, and retain empty local and session storage. There are no page errors, HTTP error responses, Supabase requests, write requests or external Google Fonts attempts. The repaired-frame screenshots were inspected: welcome shows the correct two practice clocks; T18.1 shows the four factor pairs and their correct perimeters.

`summary.json` links the final individual reports. `evidence/t181.json` is the successful T18.1 result from the first correctly pinned run. `welcome-registered-fonts/welcome.json` is the completed welcome result. T18.1 was not replayed after it passed.

## Harness findings preserved

The initial default client was Playwright 1.62.0 with existing WebKit build 2248. Page creation timed out before any live navigation; `incompatible-runtime-attempt.json` preserves that runner failure. The successful checks use the already installed matching Playwright 1.58.0 client and the same WebKit launcher.

On the first pinned welcome check, the immediate font API returned no faces before the stylesheet's font faces had registered. That result remains in `evidence/welcome.json`; it is not overwritten or reported as a pass. The focused welcome completion records zero faces initially, then 102 registered faces after explicitly awaiting the required families. The same strict three font-load assertions then pass, followed by its two chapter samples. The app, stylesheets, fonts, film and chapter logic were unchanged. The earlier combined `evidence/result.json` correctly retains its failed welcome precondition and successful T18.1 result.

The runner uses `PYTHONPATH=/workspace/scratch/45c9a6d8bd47/companion-runtime/playwright-client` and `PLAYWRIGHT_DISABLE_FORCED_CHROMIUM_PROXIED_LOOPBACK=1`, with existing launcher `/tmp/amc-intros/device/webkit.sh`. `--cases welcome` limits the remaining check to that route; it does not repeat T18.1 or any full film.
