# Summit One exam-solution video standard

Required order for every film:

1. State the exact original question at the beginning, on screen and in narration. Include all conditions, the original diagram accurately redrawn, and the answer choices if present. Spoken numbers may use words; do not paraphrase away conditions. Keep the question readable for the time it is being read.
2. Identify the problem type in language a gifted ten-year-old understands. State what the solution involves before beginning the solution: what to notice, what to count or construct, and how that will answer the question.
3. Animate the reasoning, demonstrate why the method works, and finish with the checked answer and option where applicable.

The normal visual style is black with white mathematics, cyan objects and gold emphasis. These are decorative defaults. **Any colours that carry mathematical information must retain their actual source colours**, including shaded regions, coloured counters, paths, faces, keys, diagrams and colour-named objects. Never turn a green/gold question into a blue/gold one. Preserve the correspondence between diagram, labels, legend and narration throughout all transformations.

Use a light or neutral diagram panel, adjusted outline colours, and adequate contrast when true source colours are hard to see on black. Add labels or patterns for accessibility when useful without changing the original colour meaning. Inspect the supplied source; do not invent an unclear or missing colour.

Every question gets a `question.json` source-fidelity manifest validated by `solution_design.load_question`. Colour-dependent questions must supply a source palette and meanings. Rendering must obtain those colours through `source_colour`, rather than a cyan/gold substitution. The pilot includes its original pale-blue arrows, although those arrows do not themselves encode a mathematical category.

Use the approved synthetic course narrator unless the user changes that choice. Align actions to the completed speech. Keep each complete question-and-solution film at most 60 seconds without sacrificing conditions or rushing the reasoning. If that cannot be done clearly for a future question, resolve the duration trade-off with the user before producing its final film. Do not silently omit the problem statement.

The current pilot remains the only exam-solution video produced pending the user's review. Changing this standard does not authorise producing the remaining collection before that review.
