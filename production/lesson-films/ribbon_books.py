"""Two stock books put the same delivery on opposite sides of a fractional cut."""

from fractions import Fraction

BACKGROUND = ("#fbf0dc", "#e9daca")
INK, NOTE, A, B, LINE, PAPER = "#352c35", "#6d5067", "#9e5260", "#3e7778", "#927d73", "#fff9eb"
BRIDGE = "The stock books end with the same twenty-two metres. At which point do you subtract the delivery when it came before both cuts, and when it came between them?"
HEAD = (
    "The cut end",
    "Restore a whole roll",
    "Three entries in the stock book",
    "Walk back to the delivery",
    "Undo the first cut",
    "The moved delivery slip",
    "Same ending, another start",
    "Check both stock books",
)


def check_maths():
    threequarters = Fraction(3, 4)
    twothirds = Fraction(2, 3)
    assert 28 * threequarters == 21
    assert (36 * threequarters + 6) * twothirds == 22
    assert (38 + 6) * threequarters * twothirds == 22


def ribbon(a, x, y, n, keep, label, col):
    length = 540
    w = length / n
    for i in range(n):
        a.box(
            x + i * w,
            y,
            w - 4,
            57,
            fill=col if i < keep else "#d4c6b7",
            edge=LINE,
            radius=4,
            stroke=2,
        )
        a.line([(x + i * w + 9, y + 14), (x + (i + 1) * w - 13, y + 14)], "#e6d9be", 2)
    a.text(label, x + length / 2, y + 94, 28, INK, bold=True)


def ledger(a, x, y, name, ops):
    a.text(name, x + 15, y, 27, NOTE, bold=True, align="left")
    for i, w in enumerate(ops):
        rx = x + i * 180
        a.box(rx, y + 39, 153, 62, fill=PAPER, edge=LINE, stroke=2, radius=8)
        a.text(w, rx + 76, y + 70, 23, A if w == "+ 6 m" else B, bold=True)
        if i < 2:
            a.arrow((rx + 154, y + 70), (rx + 177, y + 70), LINE, 1, 3)


def draw(a, n, c):
    a.text(HEAD[n - 1], 62, 70, 46, INK, bold=True, align="left")
    a.line([(63, 124), (1218, 124)], LINE, 3)
    if n in (1, 2):
        a.text("The original roll", 640, 187, 34, NOTE, bold=True)
        ribbon(a, 371, 273, 4, 3, "Three quarters still measure 21 m", B)
        a.text(
            "What length would restore the whole?" if n == 1 else "21 ÷ 3 = 7 m per box",
            640,
            458,
            39,
            INK,
            bold=True,
            opacity=1 if n == 1 else c.reveal("seven"),
        )
        if n == 2:
            a.text("4 × 7 = 28 m", 640, 546, 40, A, bold=True, opacity=c.reveal("twenty eight"))
        return
    if n in (3, 6, 8):
        ledger(a, 120, 208, "Book A", ("Keep ¾", "+ 6 m", "Keep ⅔"))
        a.text("Ends at 22 m", 867, 278, 32, INK, bold=True)
        if n >= 6:
            ledger(a, 120, 393, "Book B", ("+ 6 m", "Keep ¾", "Keep ⅔"))
            a.text("Ends at 22 m", 867, 462, 32, INK, bold=True)
        if n == 3:
            a.text("Which entry do you reverse first?", 640, 489, 36, INK, bold=True)
        if n == 8:
            a.text(
                "Starts at 36 m", 867, 336, 29, A, bold=True, opacity=c.reveal("first book began")
            )
            a.text("Starts at 38 m", 867, 520, 29, A, bold=True, opacity=c.reveal("thirty eight"))
        return
    if n == 4:
        ribbon(a, 99, 260, 3, 2, "2 equal parts = 22 m", B)
        labels = (
            ("One part", "11 m", "eleven metres"),
            ("Before final cut", "33 m", "thirty three"),
        )
    elif n == 5:
        ribbon(a, 99, 260, 4, 3, "After delivery is removed: 27 m", A)
        labels = (
            ("One old quarter", "9 m", "nine metres"),
            ("Book A started at", "36 m", "thirty six"),
        )
    else:
        ribbon(a, 99, 260, 4, 3, "Here 33 m represents three quarters", A)
        labels = (
            ("After delivery", "44 m", "forty four"),
            ("Book B started at", "38 m", "thirty eight"),
        )
    for i, (lab, value, word) in enumerate(labels):
        y = 232 + i * 146
        a.text(lab, 750, y, 28, NOTE, align="left")
        a.text(value, 750, y + 53, 44, INK, bold=True, align="left", opacity=c.reveal(word))
    if n == 7:
        a.text("44 m − 6 m = 38 m", 640, 548, 38, INK, bold=True, opacity=c.reveal("thirty eight"))


def poster(draw):
    return draw(6, 1)
