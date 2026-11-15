"""Scene registration and chapter labels for the first five lesson introductions."""

import intro_digit_counts
import intro_digit_positions
import intro_divisibility
import intro_inverse
import intro_place_value


FILMS = {
    "S001": intro_divisibility.SCENES,
    "S002": intro_place_value.SCENES,
    "S003": intro_inverse.SCENES,
    "S004": intro_digit_positions.SCENES,
    "S005": intro_digit_counts.SCENES,
}


def chapters(lesson):
    end = len(FILMS[lesson])
    return (
        (1, "The technique"), (2, "Where it shows up"), (3, "Basic example"),
        (5, "Medium example"), (7, "Exam-style challenge"), (end - 1, "Common mistakes"),
        (end, "Exam checklist"),
    )
