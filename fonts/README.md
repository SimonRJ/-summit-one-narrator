# Summit One typefaces

These are the exact WOFF2 files returned by the existing Google Fonts CSS request on 25 November 2026, now served by Summit One. The family names, styles, weights, Unicode ranges and `font-display: swap` declarations are preserved in `design-system.css`. No glyphs, outlines or font tables were edited.

The 28 unique files total 991,328 bytes and cover Source Sans 3, Source Serif 4, Source Code Pro and STIX Two Math. The browser selects only the subsets it needs. The service worker also saves these public files so the existing typefaces remain available to the offline reader.

`sources.json` records every original download URL, SHA-256 digest, filename, subset and weight, together with the four upstream license URLs and their digests. The four accompanying `*-OFL.txt` files reproduce the licenses supplied by the official Google Fonts repository.

This removes the blocking external stylesheet import observed in the lesson-gallery navigation trace. A single measured trace reached DOM readiness at about 40 seconds, including approximately 20 seconds for the HTML response and 19 seconds for the external font stylesheet. Those are observations from the review environment, not a promise about production speed or a benchmark for every device.
