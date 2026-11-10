# Summit One iPhone Narrator

Safari-first local narration generator for the remaining Summit One video queue.

- 175 video IDs / 780 chunks embedded.
- A040 is held unless manually enabled.
- Kokoro `af_heart`, speed `0.88`.
- Browser backend: WASM, q8 with q4 fallback.
- Audio is stored in IndexedDB, exported in small ZIP batches, then can be cleared without losing progress.
- Requires an HTTPS static host. GitHub Pages is suitable.

## Deploy with GitHub Pages
Upload the files in this folder to a repository root, then enable Pages from the `main` branch/root. No build step is required.

## iPhone use
Open the Pages URL in Safari, optionally Share → Add to Home Screen. Keep Safari foregrounded and the phone plugged in during generation. Load the model once, test the voice, then use batches of 1–5.