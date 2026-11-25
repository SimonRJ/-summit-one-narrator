# Harness notes

The successful full runs are retained in `before.json` and `after.json`. A later redundant run encountered the app's boot overlay still intercepting a click at the harness's original 15-second limit during concurrent browser workload. The harness now uses Playwright's ordinary 30-second interaction allowance. That transient harness timeout is separate from the completed cache-upgrade and offline checks; no site change was made for it.

The initial PNG preview of the after screenshot appeared blank in the inspection tool. Inspection of the actual pixel data and a JPEG view confirmed the complete rendered reader, including the heading, current S010 reading, light picker, and light canvas. The committed PNG is the original browser screenshot, unchanged.
