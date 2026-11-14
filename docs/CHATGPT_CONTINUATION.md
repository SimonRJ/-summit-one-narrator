# Summit One continuation

Repository `SimonRJ/-summit-one-narrator`. Live site https://simonrj.github.io/-summit-one-narrator/.

Read [current status](CURRENT_STATUS.md), [audit register](CONTENT_AUDIT_REGISTER.md), [authentic AMC freeze](AUTHENTIC_AMC_FREEZE.md) and [teaching script index](../production/scripts/INDEX.md). Verify the live database and Pages separately from the repository. Claude's verified starting commit was `e3f87185f08a30573b1e14ea83a46e655b78ba93`. Its three named workflow runs and Pages build passed.

## Lesson bank

All 566 standard Try and Transfer problems have been individually reviewed and independently checked. This pass revised 469, including nine follow-ups from earlier batches, and retained four with saved attempts plus 93 from earlier audits. The register records a difficulty estimate for each problem. The browser fixture renders all 113 figures and displays and checks all questions and worked solutions at 320 and 390 CSS pixels. The live release in [PR #12](https://github.com/SimonRJ/-summit-one-narrator/pull/12) was independently verified on Pages and in Supabase. See [current status](CURRENT_STATUS.md#release-verification).

Rebuild public prompts and the figure manifest with `build(map_course(), output, public_only=True)` from `tools/content/build_original_lessons.py`. The matching private source is the project owner's file named `SummitOne_Lesson_Solutions_20261114.json`. With `SUMMIT_ONE_LESSON_SOLUTIONS` pointing to that file, the builder exports the complete 566 rows and `check_reviewed_lessons.py`, `audit_all_lessons.py` and `tools/browser_lesson_fixed.py` test the exact private keys and solutions. Keep the source and its generated database payload in a private workspace. The source also retains the 28 original live rows that differed from their pre-audit Git version, for rollback if needed.

Compare live row fingerprints before changes. Update only the exact intended `original_authored` IDs when no problem attempt or saved session record exists. Update title, prompt, key and solution together. Verify all authored row fingerprints after the update and confirm that the live Pages manifest matches the repository. The renderer uses a stem fingerprint to avoid attaching a figure to an earlier version of a question during deployment.

The optional flash cards, drill variants, MAWA investigations and original mock papers remain separate from the completed 566-problem audit.

## Authentic AMC freeze

Keep official papers, linked problems, exam behaviour and results frozen. Run `tools/check_amc_freeze.sql` before and after any database change. Expected values are 19 catalog rows `a9652815abf28c4a2c1327f2001dd2f6`, 570 questions `3273298d1e754278fd8c40c195fd9506`, and 152 linked problems `741c136ddd8bde41193f7ba8077393c1`. Never start a genuine sitting for the learner while verifying.

## Video and other work

Voice C is the approved male VoxCPM2 reference described in [video production](VIDEO_PRODUCTION.md). Preserve the approved T02.1 and T02.2 videos. Five scripts received editorial or mathematical clarifications in PR #9. Independently solve the examples and notebook answers across the full set of 70 drafts. Produce one concept pilot and one worked-example pilot before batch recording. Aim for 3–5 minutes of finished runtime where the teaching needs it, and check timing, captions and mathematics on iPhone.

Continue the original AMC split papers, Rossmoyne and MAWA review, interface work and Supabase defensive review. The student and parent guides are linked from the documentation index. Part A is questions 1–20, using a count-up timer and a 20-minute accuracy target. Part B is questions 21–30, with five multiple-choice and five integer answers and a 40-minute target. Keep original practice separate from authentic papers.
