"""A surveyor's incoming heading, exterior steering angles and one reflex corner."""

from math import cos, sin, radians

BACKGROUND = ("#e5e9dd", "#d5e4df")
INK, EDGE, TURN, INSIDE, FILL = "#243c3c", "#57706d", "#a24835", "#207769", "#c0d9c5"
BRIDGE = "Trace the L-shaped yard in the direction of travel. What sign belongs to the change of heading at its notch, and which part of the full circle lies inside there?"
HEAD = (
    "Mark the old heading",
    "The two angles at a corner",
    "Around the bandstand",
    "One full turn",
    "The indented yard",
    "One turn goes back",
    "Which angle is inside?",
    "Keep two separate records",
)


def check_maths():
    assert 180 - 65 == 115 and 360 // (180 - 135) == 8
    assert 5 * 90 - 90 == 360 and 5 * 90 + 270 == 720


def arc(a, cx, cy, r, start, end, color):
    angles = [start + (end - start) * i / 38 for i in range(39)]
    a.line([(cx + r * cos(radians(t)), cy + r * sin(radians(t))) for t in angles], color, 5)


def draw(a, n, c):
    a.text(HEAD[n - 1], 62, 72, 45, INK, bold=True, align="left")
    a.line([(62, 121), (1215, 121)], EDGE, 3)
    if n <= 2:
        x, y = 338, 291
        q = (x + 181 * cos(radians(65)), y + 181 * sin(radians(65)))
        a.arrow((109, y), (x, y), EDGE, 1, 7)
        a.dashed((x, y), (602, y), EDGE, 3)
        a.arrow((x, y), q, INSIDE, 1, 7)
        a.dot(x, y, 7, INK)
        arc(a, x, y, 70, 0, 65, TURN)
        a.text("Incoming", 166, y - 40, 24, INK)
        a.text("Old heading", 510, y - 40, 24, EDGE)
        a.text("Turn", 439, 358, 26, TURN, bold=True)
        if n == 2:
            arc(a, x, y, 99, 65, 180, INSIDE)
            a.text("Inside", 259, 394, 26, INSIDE, bold=True)
        a.text("Right turn", 740, 230, 30, INK, align="left")
        a.text("65°", 740, 289, 48, TURN, bold=True, align="left")
        if n == 2:
            a.text(
                "Interior: 180° − 65° = 115°",
                740,
                409,
                32,
                INSIDE,
                bold=True,
                align="left",
                opacity=c.reveal("one hundred and fifteen"),
            )
    elif n <= 4:
        pts = [
            (363 + 158 * cos(radians(22.5 + 45 * i)), 362 + 158 * sin(radians(22.5 + 45 * i)))
            for i in range(8)
        ]
        a.polygon(pts, FILL, EDGE, 4)
        for i, p in enumerate(pts):
            a.dot(*p, 6, TURN if i == 0 else EDGE)
        a.text("135° inside", 363, 358, 34, INSIDE, bold=True)
        a.text("Interior angle", 730, 224, 28, INK, align="left")
        a.text("135°", 730, 275, 41, INSIDE, bold=True, align="left")
        if n == 4:
            a.text(
                "Steering angle: 45°",
                730,
                373,
                36,
                TURN,
                bold=True,
                align="left",
                opacity=c.reveal("forty five degree turn"),
            )
            a.text(
                "8 × 45° = 360°",
                730,
                474,
                36,
                INK,
                bold=True,
                align="left",
                opacity=c.reveal("three hundred and sixty"),
            )
        else:
            a.text("How far does the heading turn?", 730, 390, 29, INK, align="left")
    else:
        pts = [(119, 230), (551, 230), (551, 317), (294, 317), (294, 487), (119, 487)]
        a.polygon(pts, FILL, EDGE, 4)
        for i, p in enumerate(pts):
            q = pts[(i + 1) % 6]
            dx, dy = q[0] - p[0], q[1] - p[1]
            a.arrow(
                (p[0] + dx * 0.36, p[1] + dy * 0.36),
                (p[0] + dx * 0.61, p[1] + dy * 0.61),
                INK,
                1,
                4,
            )
            a.dot(*p, 7, TURN if i == 3 else EDGE)
        a.text("Notch", 349, 351, 22, TURN, bold=True)
        if n == 7:
            arc(a, 294, 317, 43, 90, 360, INSIDE)
        rows = {
            5: (
                ("Walk clockwise", "Keep the yard on your right."),
                ("At the notch", "Which way do you steer?"),
            ),
            6: (("Five right turns", "+5 × 90°"), ("One left turn", "−90°"), ("Net turn", "360°")),
            7: (("Steering", "90° left"), ("Inside the yard", "360° − 90° = 270°")),
            8: (
                ("Interior angles", "5 × 90° + 270° = 720°"),
                ("Signed heading changes", "5 × 90° − 90° = 360°"),
            ),
        }[n]
        for i, (label, val) in enumerate(rows):
            y = 205 + i * (106 if len(rows) == 3 else 149)
            a.text(label, 669, y, 25, EDGE, align="left")
            a.text(
                val,
                669,
                y + 45,
                30,
                TURN if n == 6 and i == 1 else INK,
                bold=True,
                align="left",
                opacity=c.reveal("two hundred and seventy") if n == 7 and i == 1 else 1,
            )


def poster(draw):
    return draw(7, 1)
