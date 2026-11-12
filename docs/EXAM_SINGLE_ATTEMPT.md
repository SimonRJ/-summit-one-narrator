# One attempt per paper

The warning page is shown before any sitting is created. Start confirms the only attempt, and the database supplies its start and expiry times. The same sitting can resume while time remains; closing the page does not reset the timer. Submitted or expired sittings are review-only, including when entered through a course deep link. Saved result history has no 30-sitting display limit.

The database change in `supabase/changes/exam_single_attempt.sql` creates a unique pupil/paper index, retains own-result SELECT access, adds restrictive ownership and write policies that apply alongside the existing policies, prevents deleting attempts through the student API, and limits open-sitting writes to answers and integer save times. Only the grading service can seal a sitting. Existing completed rows remain immutable.

The final confirmation shows the same live countdown as the header. It lists unanswered question numbers separately from unsaved numeric changes; each number returns to that question. The default return action invites a final check, while submission explicitly says it locks the exam. The countdown grows at 3:00 and becomes red at 1:00. It uses no animation, flashing or sound.

Checks cover cancel-before-start, resuming, course links, repeated review, no second sitting, auto-submission after expiry, unanswered and unsaved answers, exact timer boundaries, and mobile layout. `tools/check_exam_lock.sql` is a rollback-only database verification and must never be run without a surrounding rollback transaction.
