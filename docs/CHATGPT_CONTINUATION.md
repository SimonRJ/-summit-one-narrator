# Summit One continuation

Repository `SimonRJ/-summit-one-narrator`. Live site https://simonrj.github.io/-summit-one-narrator/.

Read [current status](CURRENT_STATUS.md), [audit register](CONTENT_AUDIT_REGISTER.md), [authentic AMC freeze](AUTHENTIC_AMC_FREEZE.md) and [teaching script index](../production/scripts/INDEX.md). Verify the live database and Pages separately from the repository. Claude's verified starting commit was `e3f87185f08a30573b1e14ea83a46e655b78ba93`. Its three named workflow runs and Pages build passed.

## Spatial audit

The spatial batch shipped through PR #8 (`5e9cc143b30c20803859144714e6827b92881328`). It revises 30 prompts and worked solutions in SPATIAL-02 and SPATIAL-03 and adds 29 figures. The audit register gives the IDs and assurance levels. The generator has 268 distinct structures across 566 standard problems, with 298 repeated occurrences beyond first instances and 378 rows in repeated groups. There are 90 independently recomputed and individually read problems. Continue with DATA-03, then SOLID-02 and GEO-03, auditing complete statements, reasoning, keys, solutions and the rendered phone layout. The 30 new spatial rows and the 60 Claude rewrites match the live database. All three authentic AMC fingerprints matched before and after the spatial update. Pages published the client and diagram manifest. The 60 earlier rewrites still need an end-to-end authenticated live review when the relevant sessions can be accessed without changing learner progress. Use a test fixture for future locked sessions and verify the published client and live data independently.

For database releases, build with `tools/content/build_original_lessons.py` using `map_course()` from `audit_all_lessons.py`. Compare old values against the live database first. Scope replacements to exact `original_authored` IDs with no recorded attempts. Verify the full row contents after each update. The figure renderer compares the diagram’s stem signature with the fetched question before drawing it, so separately deployed assets and database rows can stay readable during rollout.

## Authentic AMC freeze

Keep official papers, linked problems, exam behaviour and results frozen. Run `tools/check_amc_freeze.sql` before and after any database change. Expected values are 19 catalog rows `a9652815abf28c4a2c1327f2001dd2f6`, 570 questions `3273298d1e754278fd8c40c195fd9506`, and 152 linked problems `741c136ddd8bde41193f7ba8077393c1`. Never start a genuine sitting for the learner while verifying.

## Video and other work

Voice C is the approved male VoxCPM2 reference described in [video production](VIDEO_PRODUCTION.md). Preserve the approved T02.1 and T02.2 videos. Independently solve the examples and notebook answers across the 70 remaining scripts. Produce one concept pilot and one worked-example pilot before batch recording. Aim for 3–5 minutes of finished runtime where the teaching needs it, and check timing, captions and mathematics on iPhone.

Continue the original AMC split papers, Rossmoyne and MAWA review, interface work, Supabase defensive review, and student and parent guides. Part A is questions 1–20, using a count-up timer and a 20-minute accuracy target. Part B is questions 21–30, with five multiple-choice and five integer answers and a 40-minute target. Keep original practice separate from authentic papers.
