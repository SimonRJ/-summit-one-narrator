"""S067. Sort number tickets, pair prize badges, and curate three museum galleries."""
from itertools import permutations
from math import cos, pi, sin

from captioned_film import cue, mix

ID = 'S067'
ORIGINAL = '34b4c70ad9a008656a343d39dfcb4333cfb8c3a477232ec9912ca7df6ece77d7'
START = (0., 16.92, 34.2, 48.25, 61.21, 74.31, 88.07, 113.95, 137.62, 152.18, 169.46)
POSTER = 143.5
PAPER, WHITE, INK = '#f8f3e6', '#fffaf0', '#202f3d'
MUTED, GRID, MINT, PALE = '#4b5e69', '#a8b6b2', '#086d63', '#daebe2'
RED, RED_L, RED_D = '#bb423f', '#ed7770', '#85363b'
BLUE, BLUE_L, BLUE_D = '#28679c', '#62a3d1', '#244c73'
AMBER, SAND = '#925216', '#fae1aa'
CENTRES = (278, 640, 1002)
REDS, BLUES = 'ABCDE', 'UVWX'
RACK = REDS + BLUES
DEMO = ((('A', 'C', 'D'), 'Three reds · B excluded'),
        (('A', 'U', 'B'), 'Blue in the middle · B allowed'),
        (('U', 'A', 'V'), 'A between two blues'))


def label(c, value, x, y, size=30, colour=INK, anchor='mm', bold=True):
    c.text(str(value), x, y, size, colour, anchor, bold)


def heading(c, value):
    label(c, value, 60, 50, 41, anchor='lm')


def route(c, a, b, progress, colour=MINT, weight=4):
    if progress > 0:
        c.line([a, (mix(a[0], b[0], progress), mix(a[1], b[1], progress))], colour, weight)


def ticket(c, x, y, number, border=MINT, width=97, height=61, size=34):
    c.rect(x - width / 2, y - height / 2, width, height, WHITE, border, 3)
    label(c, number, x, y, size, border)


def first_digit(c, t):
    heading(c, 'Partition the possibilities')
    numbers = (12, 13, 21, 23, 31, 32)
    for r in range(3):
        y = 193 + 114 * r
        if t >= 1.2 + .19 * r:
            c.rect(731, y - 43, 444, 86, PALE, GRID, 2)
            label(c, f'Starts with {r + 1}', 755, y, 26, MINT, 'lm')
    for i, number in enumerate(numbers):
        home = number // 10 - 1
        xp, yp = 164 + (i % 3) * 161, 252 + (i // 3) * 125
        p = cue(t, 1.5 + .61 * i, 1.28)
        xx, yy = mix(xp, 999 + (i % 2) * 106, p), mix(yp, 193 + home * 114, p)
        ticket(c, xx, yy - 25 * sin(pi * p), number, MINT, 84, 51, 30)
    if t >= 4.6:
        label(c, 'Each ticket has one home.', 333, 245, 34)
    if t >= 8.85:
        label(c, 'What fixes its row?', 332, 333, 30, MUTED)
    if t >= 11.6:
        label(c, 'Here, the first digit.', 333, 402, 35, MINT)
    if t >= 14.2:
        label(c, 'Other splits can use a position or a particular object.', 640, 546, 29)


def case_table(c, t):
    heading(c, 'Turn an arrangement problem into smaller counts')
    label(c, 'Make a two-digit number from 1, 2, 3 without repeats.', 638, 133, 30, MUTED)
    for i, values in enumerate(((12, 13), (21, 23), (31, 32))):
        y = 233 + 96 * i
        if t >= 21.2:
            c.rect(153, y - 35, 818, 70, PALE if i == 2 and t >= 30.3 else WHITE, GRID, 2)
            label(c, f'First digit {i + 1}', 179, y, 27, MINT, 'lm')
        for j, n in enumerate(values):
            p = cue(t, 21.25 + .22 * (2 * i + j), 1.05)
            x0 = 246 + (2 * i + j) * 155
            x, yy = mix(x0, 626 + 221 * j, p), mix(276, y, p)
            ticket(c, x, yy, n, AMBER if n == 31 and t >= 29.2 else MINT, 85, 50, 30)
        if t >= 24.1 + .15 * i:
            label(c, '2', 1080, y, 37, MINT)
    if t >= 25:
        label(c, 'Every number starts with 1, 2 or 3.', 637, 516, 31)
    if t >= 30.3:
        label(c, '31 can go only in the “starts with 3” row.', 637, 572, 28, AMBER)


def parity(c, t, solved=False):
    heading(c, 'Odd and even from 19 through 28')
    if t >= 38.6:
        for i, (name, colour) in enumerate((('Odd', AMBER), ('Even', MINT))):
            y = 259 + 135 * i
            label(c, name, 154, y, 35, colour, 'lm')
            c.line([(294, y + 45), (1085, y + 45)], GRID, 2)
    for i, n in enumerate(range(19, 29)):
        loc = i // 2
        x0 = 140 + 110 * i
        p = 1 if solved else cue(t, 41.0 + (0 if loc == 0 else 2.6 + .47 * (loc - 1)) + .16 * (i % 2), .92)
        x, y = mix(x0, 365 + 161 * loc, p), mix(162, 259 + 135 * (i % 2), p)
        if cue(t, 34.2 + .17 * i, .35):
            ticket(c, x, y, n, (AMBER if i % 2 == 0 else MINT) if p else MUTED, 77, 56, 31)
    if not solved:
        if t >= 43.9:
            label(c, 'Follow each row in jumps of 2.', 640, 536, 33)
    else:
        if t >= 48.6:
            label(c, '5 even', 1170, 393, 28, MINT)
        if 51.15 <= t < 55.0:
            for j in range(4):
                x = 365 + j * 161
                route(c, (x + 49, 395), (x + 113, 395), cue(t, 51.3 + .49 * j, .55), MINT)
            label(c, '+2 at each step', 640, 518, 32, MINT)
        if t >= 55:
            label(c, '28 − 19 + 1 = 10 integers', 640, 514, 32)
        if t >= 57.8:
            label(c, '5 odd', 1170, 259, 28, AMBER)
            label(c, '10 − 5 = 5 odd', 640, 564, 32, AMBER)


def parity_question(c, t):
    parity(c, t)


def parity_solution(c, t):
    parity(c, t, True)


def star(c, x, y, r, colour):
    points = []
    for i in range(10):
        a = -pi / 2 + i * pi / 5
        length = r if i % 2 == 0 else r * .44
        points.append((x + length * cos(a), y + length * sin(a)))
    c.poly(points, colour, None)


def badge(c, x, y, red, n, radius=34):
    colour, edge = (RED, RED_D) if red else (BLUE, BLUE_D)
    c.dot(x, y + 3, radius, edge)
    c.dot(x, y, radius, colour)
    c.dot(x, y, radius * .82, WHITE)
    c.dot(x, y, radius * .73, colour)
    if n == 0:
        star(c, x, y - 1, radius * .59, WHITE)
    else:
        label(c, n, x, y + 1, max(15, round(radius * .94)), WHITE)


def badge_question(c, t):
    heading(c, 'Choose one red badge and one blue badge')
    for row, count in enumerate((4, 5)):
        y = 226 + row * 157
        label(c, 'Red' if row == 0 else 'Blue', 187, y, 37, RED_D if row == 0 else BLUE_D, 'lm')
        for i in range(count):
            x = 438 + 141 * i
            p = cue(t, (61.4 if row == 0 else 63.2) + i * .14, .57)
            if p:
                badge(c, x, mix(y - 30, y, p), row == 0, i, 43)
    if t >= 65.4:
        label(c, 'One star of each colour', 640, 492, 31, MUTED)
    if t >= 67.9:
        label(c, 'How many pairs have exactly one star?', 640, 554, 36, MINT)


def badge_pair(c, x, y, r, b, size=27):
    c.rect(x - size * 2.4, y - size * 1.62, size * 4.8, size * 3.24, WHITE, GRID, 2)
    badge(c, x - size * 1.05, y, True, r, size)
    badge(c, x + size * 1.05, y, False, b, size)


def seven_pairs(c, t):
    heading(c, 'Which colour supplied the star?')
    for row, count in enumerate((4, 3)):
        y = 237 + row * 155
        on = 74.55 if row == 0 else 78.65
        if t >= on:
            label(c, 'Red star' if row == 0 else 'Blue star', 87, y, 31, RED_D if row == 0 else BLUE_D, 'lm')
            for j in range(count):
                x = 408 + 203 * j
                p = cue(t, on + .33 + j * .33, .5)
                if p:
                    badge_pair(c, x, mix(y - 26, y, p), 0 if row == 0 else j + 1, j + 1 if row == 0 else 0)
            if t >= on + 2.4:
                label(c, str(count), 1165, y, 43, MINT)
    if t >= 82.45:
        label(c, 'A pair with one star has just one of these homes.', 640, 499, 29, MUTED)
    if t >= 85.6:
        label(c, '4 + 3 = 7 pairs', 640, 561, 40, MINT)


def exhibit(c, x, y, code, r=28):
    """Each artefact keeps its colour, letter, silhouette and shading in transit."""
    is_red = code in REDS
    main, light, dark = (RED, RED_L, RED_D) if is_red else (BLUE, BLUE_L, BLUE_D)
    shape = (REDS if is_red else BLUES).index(code)
    if shape == 0:
        c.poly([(x, y-r*1.16), (x+r, y+r*.85), (x-r, y+r*.85)], main, dark, 2)
        c.poly([(x, y-r*1.16), (x-r, y+r*.85), (x-r*.42, y+r*.85)], light, None)
    elif shape == 1:
        pts = [(x-r*.72,y-r),(x+r*.72,y-r),(x+r*.48,y-r*.31),(x+r,y+r*.17),
               (x+r*.78,y+r*.84),(x-r*.78,y+r*.84),(x-r,y+r*.17),(x-r*.48,y-r*.31)]
        c.poly(pts, main, dark, 2)
        c.line([(x-r*.64,y-r*.82),(x+r*.64,y-r*.82)], light, 3)
    elif shape == 2:
        c.poly([(x-r*.95,y-r*.53),(x,y-r),(x+r*.95,y-r*.53),(x+r*.95,y+r*.67),
                (x,y+r),(x-r*.95,y+r*.67)], main, dark, 2)
        c.poly([(x-r*.95,y-r*.53),(x,y-r),(x+r*.95,y-r*.53),(x,y-r*.08)], light, None)
    elif shape == 3:
        c.dot(x, y, r, dark)
        c.dot(x, y-1, r*.88, main)
        c.line([(x-r*.60,y-r*.53),(x-r*.20,y-r*.75)], light, 3)
    else:
        c.poly([(x,y-r*1.1),(x+r*.98,y),(x,y+r),(x-r*.98,y)], main, dark, 2)
        c.poly([(x,y-r*1.1),(x-r*.98,y),(x-r*.45,y)], light, None)
    label(c, code, x, y + (3 if shape == 0 else 1), max(14, round(r*.95)), WHITE)


def rack_x(code):
    return (136 + 92 * REDS.index(code)) if code in REDS else (766 + 100 * BLUES.index(code))


def gallery(c, x, y, name):
    # A little recessed gallery and a bevelled plinth; the front face stays clear for its exhibit.
    w, h = 165, 128
    c.rect(x - w/2, y - h/2, w, h, '#e8e7dc', GRID, 2)
    c.poly([(x-w/2,y+h/2),(x-w/2+18,y+h/2-13),(x+w/2-18,y+h/2-13),(x+w/2,y+h/2)], '#d4dbcf', None)
    c.poly([(x-48,y+42),(x-35,y+31),(x+43,y+31),(x+51,y+42)], '#d0c1a5', None)
    c.rect(x-48, y+42, 99, 12, '#b9a78e', None)
    label(c, name, x, y + h/2 + 31, 24, MUTED)


def rack_to_rooms(c, t, arrangements, show_red=True, show_blue=True, rooms=True):
    """Relocate each unique original, through named arrangements, with one position per exhibit."""
    if show_red:
        label(c, 'Red collection · 5 in total', 317, 106, 24, RED_D)
        c.line([(86,196),(559,196)], GRID, 2)
    if show_blue:
        label(c, 'Blue collection · 4 in total', 924, 106, 24, BLUE_D)
        c.line([(713,196),(1125,196)], GRID, 2)
    if rooms:
        for x, name in zip(CENTRES, ('Left','Middle','Right')):
            gallery(c, x, 314, name)
    positions = {code:(rack_x(code),160) for code in RACK}
    for on, duration, arrangement in arrangements:
        if t <= on:
            break
        part = cue(t, on, duration)
        for code in RACK:
            end = (CENTRES[arrangement.index(code)],316) if code in arrangement else (rack_x(code),160)
            start = positions[code]
            travel = abs(end[0]-start[0]) + abs(end[1]-start[1])
            arc = min(55,travel*.13)*sin(pi*part)
            positions[code] = (mix(start[0],end[0],part),mix(start[1],end[1],part)-arc)
    # Keep foreground movers visible when passing the shelves.
    for code,(x,y) in sorted(positions.items(), key=lambda kv:kv[1][1]):
        if (code in REDS and show_red) or (code in BLUES and show_blue):
            exhibit(c,x,y,code,27 if y<224 else 31)


def museum_question(c, t):
    heading(c, 'How many three-room exhibitions are possible?')
    changes = [(99.5, 1.0, DEMO[0][0]), (102.1, 1.1, DEMO[1][0]), (106.1, 1.25, DEMO[2][0])]
    rack_to_rooms(c,t,changes,show_blue=t>=91.7,rooms=t>=93.7)
    if t >= 97.8:
        label(c, 'Use A. Each exhibit can occupy only one room.', 640, 443, 30)
    if t >= 99.5:
        which = 2 if t>=105.8 else 1 if t>=102.2 else 0
        label(c, DEMO[which][1], 640, 520, 36, MINT)
    if t >= 109.5:
        label(c, 'Count ordered arrangements in all three cases.', 640, 577, 27, MUTED)


def museum_solution(c, t):
    if t < 121.8:
        heading(c, 'Three reds: place A, then fill two vacant rooms')
        seq=[(113.0,.30,('A','','')), (115.2,.63,('','A','')), (116.0,.62,('','','A')),
             (116.7,.60,('A','','')), (117.5,.72,('A','C','')), (118.45,.72,('A','C','D')),
             (119.65,.79,('A','D','C'))]
        rack_to_rooms(c,t,seq)
        label(c,'B excluded',rack_x('B'),217,22,RED_D)
        if t>=114.0:
            label(c,'A: 3 possible rooms',344,460,31,MINT)
        if t>=117.4:
            label(c,'Others: C, D, E only',891,460,31,RED_D)
        if t>=119.25:
            label(c,'3 places for A  ×  3 first choices  ×  2 left = 18',640,548,33)
    elif t < 129.35:
        heading(c, 'Blue middle: put A on either red end')
        seq=[(121.05,.30,('A','U','')), (123.95,.88,('','U','A')),
             (126.25,.90,('B','U','A')), (127.95,.88,('B','W','A'))]
        rack_to_rooms(c,t,seq)
        label(c,'A: 2 ends',247,463,31,MINT)
        if t>=125.75:
            label(c,'Other red: B, C, D or E',689,463,29,RED_D)
        if t>=127.3:
            label(c,'4 blues',1073,463,31,BLUE_D)
            label(c,'2 × 4 × 4 = 32 arrangements',640,549,38)
    elif t < 134.9:
        heading(c, 'A in the middle: choose two different blues')
        seq=[(128.6,.3,('','A','')), (130.35,.75,('U','A','')), (131.55,.68,('W','A','')),
             (133.10,.72,('W','A','X'))]
        rack_to_rooms(c,t,seq)
        label(c,'4 options on the left',353,470,31,BLUE_D)
        if t>=133.15:
            label(c,'3 remaining on the right',925,470,31,BLUE_D)
        if t>=133.85:
            label(c,'4 × 1 × 3 = 12 arrangements',640,549,37)
    else:
        case_rows(c,t,False)


def mini_rooms(c, x, y, exhibits):
    for i, code in enumerate(exhibits):
        xx=x+i*83
        c.rect(xx-34,y-34,68,68,WHITE,GRID,2)
        exhibit(c,xx,y,code,23)


def case_rows(c, t, totals):
    heading(c, 'Three different room patterns')
    for j, row in enumerate(DEMO):
        y=169+j*115
        mini_rooms(c,160,y,row[0])
        label(c,('Red · Red · Red','Red · Blue · Red','Blue · A · Blue')[j],420,y,30,anchor='lm')
        if totals and t>=137.85+j*.82:
            label(c,('3 × 3 × 2 = 18','2 × 4 × 4 = 32','4 × 1 × 3 = 12')[j],1012,y,32,MINT)
    if totals:
        if t>=141.35:
            label(c,'18 + 32 + 12 = 62 arrangements',640,487,38)
        if t>=144:
            label(c,'B is forbidden in the first row and available as the other red in row two.',640,561,26,RED_D)
    else:
        label(c,'Each valid arrangement matches exactly one pattern.',640,526,31,MINT)


def museum_totals(c,t):
    case_rows(c,t,True)


def exactly(c,t):
    heading(c,'Exactly one star and at least one star')
    for i,pair in enumerate(((0,1),(1,0),(0,0))):
        x=476+i*257
        badge_pair(c,x,170,*pair,30)
    label(c,'At least one',218,301,30,anchor='lm')
    label(c,'Exactly one',218,409,30,anchor='lm')
    for j in range(3):
        x=476+j*257
        if t>=153+.30*j:
            label(c,'Yes',x,301,34,MINT)
        if t>=155.1+.32*j:
            label(c,'Yes' if j<2 else 'No',x,409,34,MINT if j<2 else RED_D)
    if t>=158:
        label(c,'Two stars fail the “exactly one” test.',640,494,29,RED_D)
    if t>=162.0:
        label(c,'“Red star” and “blue star” would overlap for the two-star pair.',640,552,28)


def final_walk(c,t):
    heading(c,'How to use a case split on a new problem')
    for j, name in enumerate(('All red','Blue middle','Two blue ends')):
        y=210+j*102
        c.rect(720,y-37,458,75,PALE if j==1 and t>=174.75 else WHITE,GRID,2)
        label(c,name,748,y,26,MINT,'lm')
    if t>=171.6:
        for k,code in enumerate(('D','V','A')):
            p=cue(t,173.1+.12*k,1.45)
            exhibit(c,mix(192+k*97,990+k*61,p),mix(250,312,p)-27*sin(pi*p),code,28)
        if t>=175.3:
            label(c,'Only the middle exhibit is blue.',352,308,29)
            label(c,'One arrangement, one row.',352,364,28,MINT)
    if t>=178.8:
        label(c,'Add the separate row totals.',640,504,32)
    if t>=182.0:
        label(c,'Give the unit: 62 arrangements.',640,565,32,MINT)


SCENES=(first_digit,case_table,parity_question,parity_solution,badge_question,seven_pairs,
        museum_question,museum_solution,museum_totals,exactly,final_walk)


def verify():
    assert [n for n in range(19,29) if n%2] == [19,21,23,25,27]
    assert [n for n in range(19,29) if n%2==0] == [20,22,24,26,28]
    assert sum((r==0)+(b==0)==1 for r in range(4) for b in range(5)) == 7
    allowed=[p for p in permutations(RACK,3) if 'A' in p]
    red_row={p for p in allowed if all(n in REDS for n in p) and 'B' not in p}
    blue_middle={p for p in allowed if p[0] in REDS and p[1] in BLUES and p[2] in REDS}
    blue_ends={p for p in allowed if p[0] in BLUES and p[1]=='A' and p[2] in BLUES}
    assert [len(k) for k in (red_row,blue_middle,blue_ends)]==[18,32,12]
    assert len(red_row|blue_middle|blue_ends)==62
    assert all(example in row for (example,_),row in zip(DEMO,(red_row,blue_middle,blue_ends)))
    assert ('D','V','A') in blue_middle
