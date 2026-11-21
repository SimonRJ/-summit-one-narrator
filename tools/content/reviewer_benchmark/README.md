# Check a lesson reviewer

Use these eight original examples when choosing or changing an AI reviewer for Summit One. They are separate from the student's practice bank.

1. Start a fresh review. Supply just the contents of [packet.json](packet.json), with repository access disabled. Save the returned JSON outside the checkout.
2. Run `python tools/content/reviewer_benchmark/score.py /path/to/response.json`. The score separates missed defects, false alarms on valid maths and incorrect diagnoses. Exit codes are 0 for exact verdicts, 1 for differences and 2 for an invalid report.
3. Read the reviewer's reasons against [key.json](key.json). A correct verdict earns its point even if the explanation is weak. Check that the reason actually demonstrates the issue before relying on the reviewer for course work.

Record the reviewer version and its first result. After showing it the key, use fresh examples for an independent comparison. The packet measures performance on these examples. A clean result still calls for checking the working and the pictures in the actual lesson.

Run the scorer's regression tests with `python -m unittest discover -s tools/content/reviewer_benchmark`.
