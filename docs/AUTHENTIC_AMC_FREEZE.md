# The authentic AMC subsystem is frozen

Genuine AMC past papers are examination conditions for the learner. Nothing in them is to be edited, re-worded, re-drawn, re-keyed, re-timed, re-styled or re-ordered, and no stored sitting or score is to be touched.

## What is frozen

| Part | Where |
|---|---|
| 19 Upper Primary papers, 2007–2025 | `exam_catalog` rows with `source_type = 'authentic_amc_past_paper'` |
| Their 570 questions, choices, keys, explanations, images and figures | `exam_questions` rows for those papers |
| 152 authentic-linked problem records | `content_problems` rows with `source_type = 'authentic_amc'` |
| Exam interface, navigation, timers, one-attempt rule | `exam-rules.js`, `exam.css`, `exam-diagnostics.js`, the exam sections of `app-main.js`, and the `grade-exam` Edge Function |
| Sittings and results | `exam_sittings`, `exam_result_snapshots` |

Original Summit One content (source types beginning `original_`, `summit_`) is outside the freeze and is where improvement work happens.

## Fingerprint

`tools/check_amc_freeze.sql` is a read-only query. It returns a count and an MD5 fingerprint for each frozen part. It writes nothing and does not start a sitting.

| Item | Count | Fingerprint on 14 Nov 2026 |
|---|---:|---|
| authentic exam catalog | 19 | `a9652815abf28c4a2c1327f2001dd2f6` |
| authentic exam questions | 570 | `3273298d1e754278fd8c40c195fd9506` |
| authentic-linked content problems | 152 | `741c136ddd8bde41193f7ba8077393c1` |
| problem attempts | 7 | `44f8364e9e71761753ed85db1d442e3c` |

The first three must never change. The fourth changes only when the learner makes a new attempt; existing attempts must never be edited.

## Evidence from the 14 November 2026 content batch

The fingerprints of the exam questions and authentic-linked problems were taken before the batch and again after 60 original lesson problems were updated. They were identical. The update statement was restricted to `source_type = 'original_authored'`, to five named technique families, and to problems with no recorded attempts.

## Working rules

1. Run the fingerprint query before and after any database change and compare.
2. Scope every `update` with an explicit original `source_type` condition.
3. Do not run any test that begins a real exam sitting for the learner's account.
4. If a genuine paper appears to contain an error, record it for the parent. Do not fix it.
