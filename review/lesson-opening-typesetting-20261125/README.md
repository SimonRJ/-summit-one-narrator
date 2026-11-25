# Deterministic checks for typeset lesson openings

## Finding

Main source `585081646578fe8b0020d2dee831a8f853eb3bca` failed workflow
**45516930775** on all five profiles. The failed assertions named lessons 2, 3,
53, 173 and 362. `ci-failures.json` preserves the original job identities and
failure excerpts; those failed CI results are not relabelled as passes.

The lesson text is correct. The checker compared the authored strings with raw
DOM `textContent` after yielding to image decoding. During that yield, the live
mathematics observer could replace an arithmetic expression with KaTeX's
accessible MathML, TeX annotation and visual HTML. Their combined `textContent`
contains multiple representations of the same expression.

`before-finding.json` reproduces the original assertion at lesson 2. The first
step starts with the exact authored `30 × 8 = 240`, then its raw DOM text contains
`30×8=240`, `30 \\times  8 = 240`, and the visual expression. The original
`data-math-source`, accessible label and rendered TeX annotation remain correct.
The card remains connected as **Session 2**, so this reproduction is not an app
rerender replacing the lesson. A separate controlled call to the unchanged
typesetter produces the same expansion.

The diagnostic used unchanged app, renderer, typesetter and lesson data from the
failed commit. The already approved local font implementation was served as a
read-only overlay to avoid the independently diagnosed Google Fonts request
block. Its exact CSS hash is recorded. The optional screenshot encountered a
capture timeout after its font wait; no screenshot is used as evidence for this
text comparison finding.

## Narrow repair

Only `tools/check_lesson_reading_layouts.py` changes in production test code.
Application rendering, lesson content, questions, answers and grading editions
remain unchanged.

The checker waits for the existing typesetter, calls it explicitly for each
rendered lesson, waits for fonts and a layout frame, and verifies that the same
lesson card remains attached. It compares an exact clone of the authored text,
replacing each KaTeX wrapper with its preserved `data-math-source`. Before that
replacement, it verifies the accessible label and the rendered TeX annotation
against the wrapper's source metadata. A fallback must contain the exact source.

The checks now cover the prompt and first step as well as the original prediction
and full working. Geometry is measured after typesetting. The existing 283-lesson
count, two-pixel overflow limits, and device-specific scrolling policy stay intact.

## Validation

`after/validation-summary.json` and the individual case JSON files record all
**283 lessons across eight required cases**: PC 1440×900, 1366×768 and 1280×720;
iPhone portrait and landscape; iPad portrait, landscape and 1024×768 landscape.
All exact authored-content checks pass. Every case has zero horizontal overflow;
all PC/iPad cases have zero stage scrolling. Phone lesson content can scroll as
before, while its footer remains inside the viewport.

Three deliberately corrupted cases are rejected: a changed authored numeral,
extra working text, and a changed rendered TeX annotation. They demonstrate that
the repair does not broadly discard mathematical content to make the test pass.

`diagnose_checker.py` loads the original checker directly from the failed Git
commit and asserts the app/renderer/data inputs still match that commit.
`validate_checker.py` runs the real checker with an isolated synthetic learner,
blocks real backend access, and accepts optional existing browser/font locations.
The evidence uses Chromium/WebKit device profiles, not physical device testing.

The original GitHub workflow remains a historical failure. A new CI run on the
integrated source is still needed for a new green workflow result; the local
cases above validate the narrow repair without publishing or rerunning anything.
