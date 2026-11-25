# S009 public seek diagnosis

The active-player frame-capture timeout comes from the short test deadline during public-media seek loading in the pinned WebKit/proxy environment. It does not establish an application pause or a permanent decoder freeze. The same exact master and seek pass locally, and the public URL passes when allowed to finish loading.

| Case | Original sequence | Result | Decoded frame |
| --- | --- | --- | --- |
| Public URL, original deadline | Short playback, pause, play, seek to 96.1286; two 10-second capture attempts | Both timed out; displayed frame remained near 0.77 seconds | None in either capture window |
| Exact public bytes served locally | Identical active player and pause/play/seek sequence | Passed first attempt, about 2.68 seconds after seeking | 98.733333 seconds |
| Public URL, 60-second allowance | Identical sequence, one seek with no intervening retry or restart | Passed first attempt, about 22.38 seconds after seeking | 98.733333 seconds |

The capture still requires an actual `requestVideoFrameCallback` timestamp in the intended chapter: at least **98.7286** seconds and below **104.88** seconds. In the successful public run, the playhead had advanced to **98.682593406** seconds, the player was unpaused and no longer seeking, and 83 frame callbacks had been observed. The screenshot shows the intended working pair, **51 + 51 = 102**, rather than the opening frame.

## What the failure trace establishes

Before seeking, WebKit reported the whole 0–132.434-second interval as buffered and seekable, with ready state 4 and network state 1. That did not mean the seek could complete without more network loading: it subsequently requested `Range: bytes=5341570-`.

In the original failure, the corresponding GitHub redirect was observed about 9.49 seconds after the request, and the asset's correct 206 response was observed about 33.86 seconds after that initial request. Both 10-second capture windows had already elapsed. The playhead reported the requested 96.1286 seconds while decoded-frame callbacks stayed at the opening frame. `paused` was false, and there was no media error.

These are Playwright observation timings, including the time to retrieve response headers, rather than packet-level latency measurements. The decisive result is the differential: the exact same bytes decode locally, and the public URL decodes and advances when its capture window is long enough. The local passing trace also contains native request cancellation/reissue, so a cancellation alone is not evidence of an application failure.

The active lesson source has no auto-pause handler for seeks or visibility changes. Its explicit pause occurs when moving between learning screens, which this diagnostic did not do during capture. Gallery chapters already passed in the original route check; this focused diagnostic did not repeat full playback.

## Evidence and limits

`diagnosis.json` retains the original timeout, successful local differential, successful public 60-second run, media state/events, and sanitized request timing. Network metadata is restricted to host/path, Range, status, Content-Range, and timing; signed redirect query strings, cookies, credential headers, and tokens are omitted.

The local differential used the already downloaded **7,470,927-byte** public master, SHA-256 **39d28fec11fe4cc1b1d1b840d01ab8d8b3ae3ccb6d184bf37c1ccf4e37c16ef6**. No video was regenerated or modified. Both screenshots are original browser captures.

This checks pinned WebKit 26.0 with iPhone 13 emulation and the required workspace proxy, using the existing isolated learner backend. It is not a physical-iPhone test or a direct, non-proxied network test. No app/player workaround is supported by these findings. Extending the harness allowance to 60 seconds, while preserving its actual decoded-frame and chapter-bound checks, addresses the demonstrated test limitation.
