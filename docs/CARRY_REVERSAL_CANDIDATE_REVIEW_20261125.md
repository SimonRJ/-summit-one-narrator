# Carry and reversal films — candidate review, 25 November 2026

The two replacement films have passed encoded-master verification and all five
candidate browser profiles. Their immutable release is still queued at the time
of this review. Neither film receives final editorial credit from this document.

| Lesson | Title | Duration | Exact candidate SHA-256 |
| --- | --- | --- | --- |
| S009 | The carry counter | 132.433333 seconds | `39d28fec11fe4cc1b1d1b840d01ab8d8b3ae3ccb6d184bf37c1ccf4e37c16ef6` |
| S010 | The reversal line | 140.433333 seconds | `e8e2e6f697b00cd9401479a603bf6992c2538a107b3fbd519cac0e0b9b7f9a71` |

The source edition is `bcbd31159202426b90d4ec7250edf43910dc8a37` on
`production/carry-reversal-reviewed-20261125`. Workflow run
[45488154406](https://github.com/SimonRJ/-summit-one-narrator/actions/runs/45488154406)
has successful render jobs and successful iPhone portrait/landscape, iPad
portrait/landscape and PC playback jobs. Release job `138819426221` remains
queued. Leave that existing job and the separate voice-recording jobs intact.

## What this review establishes

The exact candidates were decoded and compared again with their archived Voice C
recordings and drawing sources. The 274 whole-second artwork comparisons passed;
all fourteen complete scene audio correlations exceeded 0.9995. The authored
scripts equal the scripts recovered from the recording archives. Each film has
seven chapters, a separate transcript and one burned-in caption layer.

An independent enumeration of all four-distinct-digit assignments gives first
addends 51, 71, 81 and 91 for S009, establishing 51 as its minimum. For S010 it
gives 61, 71 and 81. The smaller candidate 51 + 59 = 110 fails because B and D
would both be 1. Enumerating all two-digit integers independently confirms the
reversal answers 26 and 47. The other displayed exchanges, including 68 + 68 =
136, also check out.

There are no exact scene matches in the comparison with 180 other guide editions
(1,948 scenes, including historical illustrated editions). The longest shared
passages are five-word arithmetic phrases. The candidate contact sheets and
small-screen worked-example captures were inspected. This supplements the
encoded comparisons; it does not claim manual inspection of every video frame.

All ten downloaded device results identify the exact candidate hashes and verify
gallery chapters, active lessons, practice flow and immutable notebook replay.
The iPhone portrait profile additionally played each whole film, unmuted at
normal speed. These are browser profiles against the workflow's localhost
candidate site, not physical-device certification or deployed-main evidence.

The complete records are `review/S009-carry-counter-candidate-qa.json` and
`review/S010-reversal-line-candidate-qa.json`. They deliberately retain
`final_editorial_credit: false`.

## Integration and remaining acceptance

The expected immutable release tag is
`carry-reversal-reviewed-20261125-bcbd31159202`. After it exists, confirm the
returned MP4 digests against the table above. Mount the guides in
`data/recorded-studies.json`; assign the dedicated films to slots 9 and 10 and
the technique revisits to slots 228 and 319. Preserve the lesson IDs, question
IDs, grading edition and historical completed-lesson movie snapshots.

After deployment, run `tools/check_lesson_film_routes.py` for S009 and S010 on
each of its five profiles using the public site URL. Retain those returned
results with their exact digests and complete final editorial acceptance before
changing the lesson review register or completion count.

To reproduce the candidate comparison, recover each release's
`S009-recording.zip` / `S010-recording.zip` into a separate build directory and
place its exact MP4 in `media/lesson-films/`. Then run
`python production/lesson-films/verify_recorded.py S009 <recording-directory>`
and the corresponding command for S010. The checked guides and captions are in
`production/lesson-films/S009/` and `production/lesson-films/S010/`.
