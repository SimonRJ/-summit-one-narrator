"""S008: printing plates fold into matching pairs, separate, then count valid prints."""
from math import cos, pi, sin

from stage import blend, clamp, mix

BACKGROUND = ("#182b31", "#101b22")
PAPER = "#f8ecd3"
INK = "#203139"
OUT = "#f5b784"
INNER = "#83d4c4"
WHITE = "#fff4db"
MUTED = "#b6c5c5"
METAL = "#577277"
FRAME = "#314a50"
DARK = "#1a2e33"
BRIDGE = "When the printing press shows 2,772, pause before the strip splits. How much of the number comes from the two outside 2s together? How much comes from the two inside 7s?"

TITLES = (
    "The folding number press", "Fold matching places together",
    "Lift out the two pairs", "Find eleven in both strips",
    "Will every strip pass?", "Check the second factor",
    "Count the choices on the press", "Test a tempting shortcut",
)


def check_maths():
    assert 111 * 3 == 333
    assert 2 * 1001 == 2002 == 11 * 182
    assert 7 * 110 == 770 == 11 * 70
    assert 2002 + 770 == 2772 == 11 * (182 + 70) == 11 * 252
    groups = [0, 0, 0]
    prints = set()
    for outside in range(1, 10):
        for inside in range(10):
            number = 1001 * outside + 110 * inside
            assert str(number) == f"{outside}{inside}{inside}{outside}"
            assert number % 11 == 0
            assert (number % 33 == 0) == ((outside + inside) % 3 == 0)
            if number % 33 == 0:
                groups[outside % 3] += 1
                prints.add(number)
    assert groups == [12, 9, 9]
    assert len(prints) == 30
    assert prints == {n for n in range(1000, 10000) if str(n) == str(n)[::-1] and n % 33 == 0}
    assert int("0660") == 660 and 9009 in prints


def stamp(a, x, y, digit, tone, opacity=1, width=83, height=88):
    if opacity <= 0:
        return
    a.box(x - width / 2, y - height / 2 + 5, width, height, radius=7,
          fill=blend(tone, DARK, .60), opacity=opacity)
    a.box(x - width / 2, y - height / 2, width, height, radius=7,
          fill=tone, edge=blend(tone, PAPER, .35), opacity=opacity)
    a.text(str(digit), x, y, height * .65, INK, bold=True, opacity=opacity)


def strip(a, digits, x, y, *, pitch=70, h=70, alpha=1, tones=None):
    """Show a strip as four physical place cells, including printed leading zeroes."""
    if alpha <= 0:
        return
    w = len(digits) * pitch
    a.box(x - w / 2 - 8, y - h / 2 - 6, w + 16, h + 12,
          radius=7, fill=PAPER, edge="#bead8d", opacity=alpha)
    for i, digit in enumerate(digits):
        cx = x + (i - (len(digits) - 1) / 2) * pitch
        if i:
            a.line([(cx - pitch / 2, y - h / 2), (cx - pitch / 2, y + h / 2)], "#c6b89f", 1, alpha)
        if digit != " ":
            a.text(str(digit), cx, y, h * .69, INK, bold=True, opacity=alpha)
            if tones and tones[i]:
                tone = tones[i]
                a.line([(cx - pitch * .24, y + h * .42), (cx + pitch * .24, y + h * .42)],
                       tone, 5, alpha)


def title(a, number):
    a.label(TITLES[number - 1], 67, 65, 43, WHITE, bold=True)
    a.line([(69, 112), (1210, 112)], METAL, 2)


def platen(a, cx, y, count, down, digit, reveal=1):
    pitch = 112
    w = count * pitch + 72
    a.box(cx - w/2 - 20, y - 160, 22, 242, radius=5, fill=FRAME)
    a.box(cx + w/2 - 2, y - 160, 22, 242, radius=5, fill=FRAME)
    a.box(cx - w/2 - 21, y - 171, w + 42, 24, radius=7, fill=METAL)
    a.box(cx - w/2 - 24, y + 68, w + 48, 18, radius=6, fill=METAL)
    a.box(cx - 9, y - 148, 18, 52 + 35 * down, radius=3, fill=METAL)
    a.box(cx - w/2, y - 113 + 35*down, w, 20, radius=4, fill=FRAME)
    strip(a, " " * count, cx, y + 30, pitch=pitch, h=59)
    for i in range(count):
        x = cx + (i - (count - 1)/2) * pitch
        sy = y - 57 + 35*down
        stamp(a, x, sy, digit, INNER, width=66, height=63)
        a.text(str(digit), x, y+30, 40, INK, bold=True, opacity=reveal)


def scene_one(a, c):
    imp = c.reveal("print a one", 1.2)
    lift = c.reveal("the strip reads", .75)
    platen(a, 640, 365, 3, imp - lift, "1", imp)
    a.text("100     +     10     +     1     =     111", 640, 507, 37, WHITE,
           bold=True, opacity=c.reveal("one hundred and eleven"))
    a.text("repunit", 954, 395, 29, INNER, bold=True, opacity=c.reveal("called a repunit"))
    query = c.reveal("if each stamp")
    a.text("3 × 111 = ?", 640, 564, 35, INNER, bold=True, opacity=query)


def folding_strip(a, c):
    """Swing the right half around the central crease; a turned face shows its backing."""
    close = c.reveal("fold the strip", 2.0)
    reopen = c.reveal("open the strip", 1.7)
    angle = pi * clamp(close - reopen)
    origin, cy, cell, hh = 640, 343, 107, 70
    faces = (OUT, INNER, INNER, OUT)
    for i in range(4):
        if i < 2:
            left, right = origin + (i-2)*cell, origin + (i-1)*cell
            lift0 = lift1 = 0
        else:
            # A little perspective makes registration visible even during the edge-on frame.
            u0, u1 = (i-2)*cell, (i-1)*cell
            left, right = origin + u0*cos(angle), origin + u1*cos(angle)
            lift0, lift1 = -u0*sin(angle)*.38, -u1*sin(angle)*.38
        tone = faces[i]
        face = blend(tone, PAPER, .33) if i >= 2 and angle > pi/2 else tone
        a.polygon([(left,cy-hh+lift0), (right,cy-hh+lift1), (right,cy+hh+lift1),
                   (left,cy+hh+lift0)], face, DARK, 3)
        if i < 2 or angle < .45*pi:
            available = abs(right - left) / cell
            if available > .7:
                cx, yy = (left+right)/2, cy+(lift0+lift1)/2
                marked = reopen if i<2 else clamp((.45*pi-angle)/(.45*pi))*reopen
                if marked<1:
                    for q in ((0,) if i in (0,3) else (-9,9)):
                        a.dot(cx+q, yy, 6, INK, 1-marked)
                a.text("4884"[i], cx, yy, 66, INK, bold=True, opacity=marked)
        else:
            cx, y = (left+right)/2, cy+(lift0+lift1)/2
            if abs(right-left) > 14:
                for offset in ((0,) if i == 3 else (-9, 9)):
                    a.dot(cx + offset * abs(cos(angle)), y, 6, INK)
    a.dashed((origin,cy-hh-30),(origin,cy+hh+33),PAPER,width=2,dash=7,gap=7)
    a.text("crease", origin, cy+hh+61, 25, MUTED)
    if reopen > 0:
        a.text("outside ↔ outside      inside ↔ inside", 640, 529, 31, WHITE, bold=True, opacity=reopen)


def scene_two(a, c):
    to_fold = c.reveal("now fit four", .7)
    if to_fold < .5:
        platen(a, 640, 355, 3, 0, "3")
        a.text("300 + 30 + 3 = 333", 640, 517, 41, WHITE, bold=True)
    else:
        folding_strip(a, c)


def scene_three(a, c):
    printed2 = c.reveal("two on the outside")
    printed7 = c.reveal("seven on the inside")
    sep = c.reveal("lift the inside", 1.5)
    deeper = c.reveal("separate strip", 1)
    cols = (OUT, INNER, INNER, OUT)
    top, bottom, cx = 290, 475, 640
    strip(a, "    ", cx, top, pitch=89, h=92)
    strip(a, "    ", cx, bottom, pitch=89, h=92, alpha=sep)
    for i,v in enumerate("2772"):
        pair = i in (0,3)
        x = cx + (i-1.5)*89
        y = top if pair else mix(top,bottom,sep)
        # The new strip stays below the first. Each stamp travels in its own place column.
        if not pair:
            a.text("0", x, top, 57, "#7d827a", opacity=clamp((sep-.22)/.6))
        else:
            a.text("0", x, bottom, 57, "#7d827a", opacity=deeper)
        if not pair and 0 < sep < 1:
            a.box(x-30, y-41, 60, 83, radius=5, fill=PAPER)
        a.text(v, x, y, 64, INK, bold=True, opacity=printed2 if pair else printed7)
        a.line([(x-22,y+37),(x+22,y+37)],cols[i],4,printed2 if pair else printed7)
    a.text("2,772 ÷ 11 = ?", 640, 165, 39, WHITE, bold=True,
           opacity=c.reveal("can you divide"))
    a.label("2,002", 875, top, 38, OUT, c.reveal("contributes two thousand"), bold=True)
    a.text("+", 403, bottom, 42, WHITE, bold=True, opacity=deeper)
    a.label("770", 875, bottom, 39, INNER, c.reveal("value is seven"), bold=True)


def proof_lane(a, y, digits, first, second, colour, alpha, beta):
    strip(a, digits, 237, y, pitch=53, h=61)
    a.arrow((370,y),(459,y),colour,alpha)
    a.label(first,484,y,36,WHITE,alpha,bold=True)
    a.arrow((752,y),(823,y),colour,beta)
    a.label(second,849,y,38,colour,beta,bold=True)


def scene_four(a, c):
    a.text("2,772 ÷ 11", 640, 163, 39, WHITE, bold=True)
    proof_lane(a, 258, "2002", "2 × 1,001", "11 × 182", OUT,
               c.reveal("one thousand and one"), c.reveal("one hundred and eighty two"))
    proof_lane(a, 386, "0770", "7 × 110", "11 × 70", INNER,
               c.reveal("one hundred and ten"), c.reveal("eleven times seventy"))
    addition = c.reveal("add the two quotients", 1)
    a.label("1,001 = 11 × 91", 484, 307, 28, OUT, c.reveal("eleven times ninety one"), bold=True)
    a.label("110 = 11 × 10", 484, 435, 28, INNER, c.reveal("eleven times ten"), bold=True)
    a.terms([("182", OUT, addition), ("+", WHITE, addition), ("70", INNER, addition),
             ("= 252", WHITE, c.reveal("two hundred and fifty two"))], 537, 49)


def scene_five(a, c):
    al = c.reveal("change the outside")
    be = c.reveal("change the inside")
    for i,v in enumerate("ABBA"):
        stamp(a,247 + i*83,263,v,OUT if i in (0,3) else INNER,
              al if i in (0,3) else be,width=70,height=85)
    a.label("outside", 680, 198, 24, OUT, al)
    a.label("A × 1,001", 680, 251, 43, WHITE, al,bold=True)
    a.label("inside", 680, 327, 24, INNER, be)
    a.label("B × 110", 680, 380, 43, WHITE, be,bold=True)
    a.label("Always divisible by 11", 155, 482, 37, INNER,
            c.reveal("both contributions"),bold=True)
    a.text("How many are divisible by 33?",640,562,35,WHITE,bold=True,
           opacity=c.reveal("how many four digit"))


def scene_six(a, c):
    a.text("33 = 3 × 11", 640, 175, 44, WHITE, bold=True)
    a.text("11 is already a factor", 640, 309, 34, INNER, bold=True,
           opacity=c.reveal("already have the eleven")*(1-c.reveal("each chosen digit")))
    digit_sum = c.reveal("each chosen digit", .85)
    for i, digit in enumerate("ABBA"):
        stamp(a, 225 + i * 83, 290, digit, OUT if i in (0,3) else INNER, digit_sum, 69, 70)
    a.label("A + B + B + A", 690, 255, 36, WHITE, digit_sum, bold=True)
    a.label("= 2 × (A + B)", 690, 320, 38, INNER,
            c.reveal("twice the sum"), bold=True)
    maps = c.reveal("doubling cycles", 1.4)
    for i, (old, new) in enumerate(((0,0), (1,2), (2,1))):
        x = 263 + i * 295
        alpha = clamp(maps*3-i)
        a.box(x, 419, 184, 68, radius=9, fill=FRAME, opacity=alpha)
        a.text(f"{old}  →  {new}", x + 92, 453, 32, WHITE, bold=True, opacity=alpha)
    a.text("Remainders after doubling", 640, 384, 25, MUTED, opacity=maps)
    a.text("A + B must be a multiple of 3", 640, 559, 37, INNER, bold=True,
           opacity=c.reveal("two chosen digits must"))


def scene_seven(a, c):
    remainder_trays = (("0, 3, 6, 9", 0),("1, 4, 7", 1),("2, 5, 8", 2))
    a.label("Inside digits", 76, 160, 28, INNER, bold=True)
    a.label("Outside digits", 679, 160, 28, OUT, bold=True)
    a.label("Prints", 1040, 160, 28, WHITE, bold=True)
    # The first tray holds four options, so give it the same width as the other trays.
    for i,(digits, rem) in enumerate(remainder_trays):
        y = 235 + i*103
        shown = c.reveal("zero three six" if rem==0 else "other trays", .8, offset=0 if rem<2 else .2)
        a.box(75, y-36, 442, 73, radius=9, fill=FRAME, edge=METAL, opacity=shown)
        a.label(f"Rem {rem}", 96, y, 31, MUTED, shown)
        a.label(digits, 225, y, 35, WHITE, shown, bold=True)
    rows = (
        (2, "1, 4, 7", "3 × 3 = 9", "outside digits one", "that gives nine strips"),
        (1, "2, 5, 8", "3 × 3 = 9", "two five and eight", "nine more"),
        (0, "3, 6, 9", "3 × 4 = 12", "three six and nine need", "that gives twelve"),
    )
    for rem, outer, count, choose, total in rows:
        y = 235 + rem*103
        t = c.reveal(choose, .8)
        a.label(outer, 682, y, 35, OUT, t, bold=True)
        a.arrow((635, y), (531, y), INNER, t)
        a.label(count, 987, y, 31, WHITE, c.reveal(total), bold=True)
    a.text("9 + 9 + 12 = 30", 640, 554, 45, INNER, bold=True, opacity=c.reveal("thirty different"))


def scene_eight(a, c):
    invalid = c.reveal("try printing", .8)
    vanish = c.reveal("leading zero disappears", 1.2)
    for i in range(4):
        stamp(a, 197+i*83, 292, "?" if i in (0,3) else " ", OUT if i in (0,3) else INNER,
              1-invalid, width=69, height=88)
    for i, v in enumerate("0660"):
        movement = .5 * 83 * vanish if i else 0
        x = 197 + i * 83 - movement
        stamp(a, x, 292, v, OUT if i in (0,3) else INNER,
              invalid * (1 - vanish if i==0 else 1), width=69,height=88)
    a.text("3 digits", 318, 402, 33, OUT, bold=True,
           opacity=c.reveal("only three digits"))
    valid = c.reveal("nine thousand and nine", .85)
    for i, v in enumerate("9009"):
        stamp(a, 786+i*83, 292, v, OUT if i in (0,3) else INNER, valid, width=69,height=88)
    a.text("4 digits", 913, 402, 33, INNER, bold=True, opacity=valid)
    finish = c.reveal("next time", 1)
    a.line([(127,474),(1154,474)],METAL,2,finish)
    a.text("Pair the places. Test the sum. Count the choices.", 640, 548, 33, WHITE, bold=True,
           opacity=finish)


SCENES = (scene_one, scene_two, scene_three, scene_four, scene_five, scene_six, scene_seven, scene_eight)


def draw(a, n, c):
    title(a, n)
    SCENES[n-1](a, c)


def poster(draw):
    return draw(3.0, 1.5)
