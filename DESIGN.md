# Summit One — product design system

> Authoritative design specification for the learner app. Updated 21 November 2026.

## Purpose

A focused, academically rigorous and calm maths trainer for one learner progressing through 372 sessions. Prioritise understanding, a clear next action, legible mathematical notation and credible assessment over decoration or gamification.

## Visual language

- **Learning screens:** warm chalk canvas (#F6F7F4), white paper panels, dark ink (#182C3D), deep blue primary actions (#24598E), coral (#C66D54) as a small accent, and a restrained 64px mathematical grid. Do not add gratuitous decorative cards or gradients.
- **Type:** Source Serif 4 for editorial page and lesson headings, Source Sans 3 for controls, labels and long explanations, Source Code Pro for tabular figures. KaTeX/STIX for maths. Preserve existing logo.
- **Density:** one dominant task per viewport; generous space between unrelated groups; simple sequential lesson stages. Use a consistent border, shadow and radius scale. Surface answers and worked steps clearly.
- **Motion:** keep routine navigation fast and quiet; press feedback under 160ms and optional gentle hover feedback. Animations must explain a concept or signal state, not delay repeated work. Respect reduced-motion preferences.
- **Mobile:** work at 320–390px widths, iPhone safe areas and keyboard zoom; 44px touch targets, >=16px focused inputs on touch devices, no horizontal overflow. Desktop lesson navigation remains screen-based and iPhone content may scroll within the lesson panel.
- **Accessibility:** semantic controls, visible focus ring, high-contrast text, useful labels, preserved browser zoom. Do not replace genuine diagrams with decorative shapes.

## Critical assessment boundary

The authentic AMC exam-taking workspace is an intentional simulation of the real exam. **Do not change its white question area, turquoise sidebar, question navigation, timer, choices, spacing, sizing or interaction layout as part of general visual polish.** The file `exam.css` is frozen at Git blob `17953e7757a605a334ea1c46c13ed7bb9ebb0338`. The visual layer `summit-polish.css` must use selectors scoped to `body:not(.exam-mode)`. Keep `tests.js` mode transitions and `exam.css` unchanged unless the user separately requests a change to the authentic exam itself. `tools/check_design_boundary.mjs` enforces this boundary in CI.

## Sources studied (guidance, not copied dependencies)

- [Emil Kowalski / skills](https://github.com/emilkowalski/skills), MIT: interface motion, mobile-native behaviour, animation review and worst-case UI testing.
- [Paul Bakaus / Impeccable](https://github.com/pbakaus/impeccable), Apache-2.0: type, layout, polish, accessibility and deterministic code-level critique.
- [Leonxlnx / Taste Skill](https://github.com/Leonxlnx/taste-skill), MIT: strong content hierarchy, cohesive design tokens and cross-viewport verification. Its marketing-site WebGL, shader effects and mandatory full-screen sections are not appropriate to repeated maths study.

These repositories are design-agent instructions, not runtime dependencies. The production site remains lightweight static HTML, CSS and JavaScript.

## Review before shipping

Inspect representative states: new learner, long lesson title, completed profile, open lesson menu, narrow iPhone portrait and landscape, and exam selection. Test the full exam mode separately for unchanged layout. Run `node tools/check_design_boundary.mjs` and the existing release QA suite. Hardware Safari testing is still required for final iOS touch and safe-area validation.
