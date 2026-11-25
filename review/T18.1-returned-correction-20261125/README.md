# T18.1 returned correction: integration handoff

The corrected `thirteen-search` package is prepared for integration. Its delivered
MP4 is **3527d02410e4b1158af7d42a5d8abce16cb6fed702947b8fa864af25590635ce**.
Public watch/gallery byte/route verification and final full audiovisual editorial approval
remain pending. This handoff does not mark the film complete.

## Returned assets and source

Notebook run **45496023370**, source
`50d2fe13de6c946dd485df013865aa5559aebfb4`, finished films 14–18 and its package
job successfully. The package release commit is
`d42bd9ea29a5da70cf936422779489bbdea3f493`. Artifact **14978062503** contains the
T18 outputs; only **T18.1** is installed here. The movie, VTT and QA have exactly
the Git blob identities in that release commit. The existing poster is unchanged
and has the same Git blob in both sources.

The existing publisher now retains `T18.1: thirteen-search`. Its regenerated
watch page is byte-for-byte the returned release page. The catalogue and public
source/direct-download URLs agree. The page uses the already established chapter
helper and small landscape video bound. No question, grade, learner record,
approved T02.1/T02.2 asset, other film or global cache revision changes.

The rendering recipe remains pinned to the completed production source:

- [Notebook builder at the exact source commit](https://github.com/SimonRJ/-summit-one-narrator/blob/50d2fe13de6c946dd485df013865aa5559aebfb4/production/lesson-films/build_companion_notebook.py)
- [Notebook artwork at the exact source commit](https://github.com/SimonRJ/-summit-one-narrator/blob/50d2fe13de6c946dd485df013865aa5559aebfb4/production/lesson-films/companion_notebooks.py)
- [Completed notebook run](https://github.com/SimonRJ/-summit-one-narrator/actions/runs/45496023370)

## Why the earlier content evidence remains applicable

The returned container differs from the earlier checked `b06f8c…` candidate by
one byte overall. **All 9,029 encoded packets match**, including payload hashes,
PTS/DTS, durations, sizes, flags and side data; both decoder configurations also
match. Video and audio payload hashes are recorded in
`packet-and-container-identity.json`. Approved Voice C audio is unchanged.

The differences are confined to muxer/encoder labels, an average-bitrate metadata
field, and a one-byte shift of chunk offsets. The corrected 42-cue VTT is identical
to the earlier candidate. The prior three perimeter/answer frame observations,
mathematical checks and full PC normal-speed unmuted playback therefore remain
evidence for the same encoded content. They are not newly counted, and do not
constitute a complete audible editorial review.

The container comparison used `ffprobe -show_packets -show_data_hash sha256`,
compared every returned field except the physical file position `pos`, compared
codec configuration/extradata hashes, and checked each stream using
`ffmpeg -map 0:v:0 -c copy -f hash -hash sha256 -` (and `0:a:0` for audio).
The JSON records the canonical packet-comparison digest and complete differing
MP4 leaf-atom descriptions.

## Targeted local delivery checks

`check_candidate_delivery.py` exercises the exact returned master and generated
watch page. It requires decoded video-frame callbacks in the correct interval
after each of eight chapter clicks, checks the repaired caption moment, player
bounds, transcript and worked variation. It records computed theme colours and
captures the actual player. It uses only a local file server; no learner backend
or external publication is involved.

Run with the already installed Playwright browsers:

```sh
python review/T18.1-returned-correction-20261125/check_candidate_delivery.py \
  --output /tmp/t181-local-check
node tools/check_companion_release_routes.mjs
```

Optional `--chromium`, `--chromium-args` and `--webkit` arguments select an existing
pinned local runtime. `--profiles` permits individual profile checks without
repeating already recorded cases. Device profiles are browser emulation, not
physical Apple hardware. The all-72-route consistency and negative URL tests pass.

### Recorded results and checker correction

The exact returned container now passes **all five profiles**: PC, iPhone
portrait/landscape and iPad portrait/landscape. Each result includes all eight
decoded chapter starts, the repaired caption at approximately 79.900 seconds,
player bounds, light colours, transcript and worked variation. The earlier PC
result is retained; all four Apple results are fresh returned-container runs.
See `devices/device-results.json` and the five screenshots.

The bounded trace located the earlier hang after all eight chapter checks had
completed, while awaiting a programmatic `video.play()` promise after pausing
and seeking for the caption. The checker now starts that check with the
existing chapter button and lets playback reach the **same strict decoded
79.9–80.5-second interval**. It also starts initial playback through the actual
chapter button before waiting for metadata, and rotates a device `screen`
only when that optional descriptor is present. No learner player, media,
chapter helper or assertion was weakened or changed. Supabase requests are
explicitly blocked.

`diagnostics/` preserves the incomplete attempts, the exact waiting stack,
independent first-chapter playback evidence and the successful retry logs.
The first successful iPhone case was followed by a harness `KeyError` for an
absent optional `screen` field; only the three unrun profiles were retried.
The stable fixture manifest records exact input hashes, avoiding the earlier
sparse-checkout issue in which a temporary media copy disappeared during Git
operations. These are browser-emulation checks, not physical Apple hardware
or full audible editorial approval. No fresh full narration playback was run.

## Native chapters and remaining gates

Native-chapter run **45497364270** also succeeded, but its artifact contains
**41 reports through T13.2 and no T18.1 output**. The returned T18.1 master has no
embedded native chapter track. Its eight page chapter buttons remain available.
No native chapter credit is inferred from that unrelated batch.

Before final acceptance, root must integrate this package in its coherent cache
release, publish it, verify the exact public movie/VTT/QA/poster/source bytes,
exercise the public watch page and teaching-video gallery link, and complete the
full moving-picture and audible editorial review. If embedded native chapters
are required for completion, that work remains outstanding for T18.1.

`handoff.json` contains exact artifact hashes and gate boundaries. Historical
candidate/public-source observations remain in the earlier companion evidence;
this handoff supersedes their T18.1 delivery preparation status only.

T18.1 has no current/completed learner-slot mapping in `curriculum.js` methods
or the opening-film array. Those learner-route gates are inapplicable to this
film; no curriculum assignment is introduced for testing. The all-72 resolver
check still verifies its safe catalogue URL and public-page agreement.
