# AMC Upper Primary Practice Simulator Specification

## Purpose

Provide faithful rehearsal of the official online AMC interaction pattern without copying Australian Maths Trust branding or representing the simulator as an official AMT product.

## Official competition facts to preserve

- Division: Upper Primary (Australian Years 5–6).
- Questions: 30.
- Time: 60 minutes.
- Question types:
  - Q1–Q25 multiple choice.
  - Q26–Q30 integer answer.
- Scoring:
  - Q1–10: 3 marks each.
  - Q11–20: 4 marks each.
  - Q21–25: 5 marks each.
  - Q26: 6 marks.
  - Q27: 7 marks.
  - Q28: 8 marks.
  - Q29: 9 marks.
  - Q30: 10 marks.
  - Maximum: 135.
- No penalty for incorrect responses.

## Interaction model

### Before Start
Display:
- paper title/year
- division
- 30 questions
- 60-minute duration
- permitted-practice-material note
- Start button

Timer must not begin until Start is pressed.

### During exam
Always visible:
- countdown timer
- current question number
- question navigation/menu
- answered/unanswered state

Allow:
- skipping ahead
- returning to previous questions
- changing multiple-choice answers before finish
- changing integer answers before finish

### Multiple choice Q1–Q25
- clear A–E response buttons
- selected state visible
- response saved immediately when selected

### Integer Q26–Q30
- numeric response field
- explicit Save button
- unsaved answer state visually distinct
- navigating away without pressing Save must not silently treat the typed value as submitted
- permit correction and re-save before time expires

### Timer
- 60:00 at Start
- monotonic countdown based on an immutable exam-start timestamp
- refresh/reopen restores remaining time from saved server start time
- ordinary page refresh cannot reset the clock
- when timer reaches zero:
  - freeze responses
  - save current submitted responses
  - close exam mode
  - show completion state

### During exam: prohibited
Do not show:
- answer correctness
- hints
- worked solutions
- teaching videos
- mastery prompts
- XP celebrations
- technique labels that reveal approach
- score projections

### After exam
Show:
- total score /135
- Q1–Q30 response summary
- correct answers
- marks by section
- time usage
- unanswered count
- changed-answer history if useful for review
- topic/technique analysis
- links back to learning modules for missed concepts

Post-exam review is separate from the timed sitting.

## Sitting integrity

Each practice sitting stores:
- exam ID/year
- user ID
- start timestamp
- expiry timestamp
- final submit timestamp
- response per question
- save timestamp for integer answers
- final score
- completion status

Once completed, the sitting record is immutable.

## Device target

Official AMT guidance states competitions must not be completed on mobile phones.

For training:
- allow phone access to review completed exams,
- target the actual exam simulator for iPad/tablet or desktop/laptop dimensions,
- display a rehearsal warning if exam mode is started on a narrow phone viewport.

## Branding

Do not:
- copy AMT logo
- claim official affiliation
- clone proprietary artwork
- deliberately make the site visually indistinguishable from the official portal

Do:
- match the operational workflow students need to rehearse
- use Summit One branding
- include a short note that the simulator is an independent training environment.

## Validation

Before release, compare the simulator against:
- current AMT competition handbook
- current AMT student Competition Portal Navigation Test
- current AMC Upper Primary competition format

Re-check these sources annually because delivery software and instructions can change.
