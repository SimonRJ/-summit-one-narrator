# Deployed S009, S010 and S012 routes

All 21 required functional cases passed against the actual public site at commit `585081646578fe8b0020d2dee831a8f853eb3bca`, using the exact immutable movies whose hashes are recorded in `results.json`.

| Film | Canonical lesson | Later technique lesson | Passed cases |
|---|---:|---:|---:|
| S009, The carry counter | 9 | 228 | 7 |
| S010, The reversal line | 10 | 319 | 7 |
| S012, The missing rung | 12 | 248 | 7 |

Each canonical lesson passed desktop Chromium plus iPhone and iPad WebKit in portrait and landscape. Each later technique lesson passed PC and iPad portrait. The checks covered the public gallery, every chapter button, active Read → Watch → Practise, both fixture grading outcomes, a decoded worked-example frame at the actual inline size, and replay from the immutable completed notebook. No player frame was clipped horizontally or vertically. Each canonical iPhone portrait case also played the complete film unmuted at normal speed to its ended state.

The actual learner backend was blocked and replaced with the established in-memory fixture. Replay left the fixture answers, progress and write log unchanged. These are browser-emulation results, not physical-device tests or human listening approvals.

Initial failures are retained in `initial-failures/`. S010's PC consumer encountered a gallery navigation timeout, then passed an isolated retry with the same deadline. Its iPad consumer encountered one chapter-progress timeout and then passed without changing the media assertions; that failure's cause remains unproven. S012's two initial PC attempts exceeded the 30-second navigation deadline. A separate trace measured approximately 40 seconds to DOM readiness, including an external font stylesheet delay. Its failed PC case was repeated with a bounded 60-second navigation allowance; content, grading and playback checks were unchanged. Completed cases were not repeated to hide those failures.

The shared harness now retains the original exception even if a diagnostic screenshot or media-state query also fails. The font dependency exposed by the navigation trace is separately addressed by the local-font change.

Actual decoded caption transitions in all three published movies show overlapping regular/bold glyphs. Those findings are retained in `../caption-layer-holds-20261125/`; they require caption-only refreshes preserving the approved audio. Functional playback success does not remove that quality hold or increase final editorial completion.
