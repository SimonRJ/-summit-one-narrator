# AMC rehearsal interface and first solution pilot

The Test Centre now follows the controls observed in AMT's public Student Navigation Test on 11 November 2026:

- Entry overview lists questions, marks and answered/not answered status.
- A left question menu allows skipping and returning. The current question and answered questions have separate markers.
- Previous and Next sit above the question; the timer remains visible there.
- Multiple-choice selection saves immediately. Erase clears the saved response.
- Integer questions use an explicit Save button, with Save and Erase below the input. Typing alone does not submit an answer.
- The final question's Next button returns to the overview. End competition opens an answered/unanswered review and a final Yes/No confirmation.
- Before submission there are no hints, solutions or correctness indicators. Existing authenticated server grading and timer enforcement remain in place.

Sources inspected:

- https://amt.edu.au/run-competitions-programs
- https://competitions.amt.edu.au/index.php?action=anon_join&grp_id=379
- https://amt.edu.au/wp-content/uploads/2026/2026-Competitions-Handbook.pdf

This is Summit One practice, with its own branding. It reproduces the observed navigation model, not the official AMT service or login. A phone gets a collapsible version of the question menu; a larger screen gives the closer rehearsal. Future official interfaces may change.

## Reviewing a completed paper

Every question has a results row containing the submitted answer, correct/incorrect/not answered status, marks and a link to its review. Review sections show the original question, the correct answer and the worked explanation where one is installed. Missing explanations and videos are labelled honestly. All 30 questions in the supplied 2025 paper have worked explanations; some older papers currently have verified answer keys only.

Only the approved-for-review pilot is connected to video at this stage: authentic 2025 Upper Primary question 17. It opens in another tab so the completed exam review remains available. Additional solution videos await the user's review of the pilot's standard.

## Pilot: the number pyramid

The five positions contribute with weights 1, 2, 3, 2, 1. An optimal arrangement is 1, 3, 5, 4, 2. The middle row is 9, 12, 11 and the top is 32, option C. The film traces the centre's contribution, builds the weights, places the digits, demonstrates an improving swap, and finishes by adding upwards. Its maximum is verified against all 120 permutations.

Artwork is original, with a black background, white serif mathematics, cyan objects and gold emphasis drawn to match the supplied visual references. Movements use word timestamps from the finished narration. Optional English captions are separate from the mathematical artwork. The synthetic narrator is Kokoro `af_heart`, the current approved T02.1 course voice, freshly generated at 0.82 speed; it is not a verified match or clone of Mathsy's narrator. The build rejects any film longer than 60 seconds and verifies 1080p H.264/AAC playback by decoding the entire file.

## Verification

Browser checks use a synthetic local fixture only. They exercise the overview, direct navigation, explicit integer Save, unsaved drafts, save-failure rollback, Erase for both question types, final confirmation/cancellation, result labels and solution/video links. Desktop and phone layouts are captured and checked for horizontal overflow. No real learner progress or exam records are changed by QA.
