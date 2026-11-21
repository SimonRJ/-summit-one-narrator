"""A working flow bench and a calibrated pen recorder for S138."""
from math import cos, pi, sin
from stage import between, clamp, mix

BACKGROUND = ('#0b3440', '#101f2a')
INK, WATER, LEAK, PAPER, LINES = '#e4f2ee', '#65e0dd', '#ffb270', '#e6e8ce', '#446776'
BRIDGE = 'Follow the pen until the valve closes. What changes at the bend, and which flow keeps its old rate?'


def check_maths():
    assert [sum(7 - 2 for _ in range(t)) for t in range(4)] == [0, 5, 10, 15]
    assert [leak for leak in range(10) if 10 + 4 * (9 - leak) == 34] == [3]
    assert [shut for shut in range(11) if 8 + sum(7 - 2 * (m < shut) for m in range(10)) == 66] == [6]
    assert (8 + 6 * 5, 38 + 4 * 7) == (38, 66)


def meter(a, x, label, rate, colour, t):
    y = 254
    a.dot(x, y, 81, LINES); a.dot(x, y, 75, '#183443')
    for k in range(11):
        angle = pi * (.83 + 1.34 * k / 10)
        a.line([(x+59*cos(angle), y+59*sin(angle)), (x+68*cos(angle), y+68*sin(angle))], PAPER, 2)
    if rate is not None:
        angle = pi*(.83+1.34*rate/10)
        a.arrow((x, y), (x+51*cos(angle), y+51*sin(angle)), colour, width=4)
        a.dot(x, y, 7, colour)
        a.text(f'{rate} L/min', x, y+40, 23, INK, bold=True)
    else:
        a.text('?', x, y+10, 52, LEAK, bold=True)
    a.text(label, x, y-111, 25, colour, bold=True)


def sheet(a, limit, max_y, x_ticks, y_ticks):
    x, y, w, h = 151, 500, 715, 318
    xy = lambda t,v: (x+w*t/limit, y-h*v/max_y)
    for t in x_ticks:
        xx = xy(t, 0)[0]
        a.line([(xx, y-h), (xx, y+6)], LINES, 1); a.text(str(t), xx, y+24, 24, INK)
    for v in y_ticks:
        yy = xy(0,v)[1]
        a.line([(x-5, yy), (x+w, yy)], LINES, 1); a.label(str(v), x-14, yy, 24, INK, align='right')
    a.line([(x,y-h), (x,y), (x+w,y)], INK, 3)
    a.label('Water (L)', 91, 141, 25, INK); a.label('Time (min)', x+w, y+61, 24, INK, align='right')
    return xy


def trace(a, xy, points, until, colour=WATER):
    for (t1,v1),(t2,v2) in zip(points,points[1:]):
        if until <= t1: continue
        end = min(t2, until)
        a.line([xy(t1,v1),xy(end,mix(v1,v2,(end-t1)/(t2-t1)))], colour, 6)
    if until <= points[0][0]: a.dot(*xy(*points[0]), 5, colour)


def note(a, tag, value, y, opacity=1, colour=INK):
    a.label(tag, 925, y, 22, '#b6cbd1', opacity); a.label(value, 923, y+40, 32, colour, opacity, bold=True)


def draw(a, n, c):
    titles = ['Two flow meters','What stays in the tank?','The hidden leak','Read a change in volume',
              'A valve closes once','Compare two finishes','Check the bend','Equal flow rates']
    a.label(titles[n-1], 82, 82, 47, INK, bold=True)
    if n <= 2:
        meter(a, 294, 'INLET', 7 if n==2 else None, WATER, c.t)
        meter(a, 622, 'OUTLET', 2 if n==2 else None, LEAK, c.t)
        if n == 1:
            a.label('TANK RECORD', 871, 160, 23, PAPER)
            a.line([(878,365),(878,215),(1174,215)], LINES, 3)
            step=c.reveal('a pen records',2.4)
            a.line([(882,345),(882+243*step,345-91*step)], WATER, 5)
            a.dot(882+243*step,345-91*step,7,PAPER)
            a.text('inlet − outlet = net rate', 640, 515, 44, INK, opacity=c.reveal('the difference'),bold=True)
        else:
            separate=c.reveal('pair two outgoing marks',1.1)
            keep=c.reveal('five litres stay')
            for j in range(7):
                a.dot(180+j*44,420,13, WATER)
                if j<2: a.dot(180+j*44, mix(485,450,separate), 12, LEAK)
            a.label('5 L each minute',866,245,33,WATER,keep,bold=True)
            a.label('3 × 5 = 15 L',866,327,35,INK,c.reveal('three groups of five'),bold=True)
        return
    if n in (3,4):
        xy=sheet(a,5,40,range(6),range(0,41,10))
        t=1+4*(c.reveal('thirty four litres',1.5) if n==3 else 1)
        if n==4 or c.reveal('ten litres'): a.dot(*xy(1,10),7,WATER)
        trace(a,xy,[(1,10),(5,34)],t)
        if t>=5:a.dot(*xy(5,34),7,WATER)
        if n==3:
            note(a,'Inlet','9 L/min',235)
            note(a,'Leak','? L/min',343,colour=LEAK)
        else:
            a.dashed(xy(1,10),xy(5,10),PAPER,fraction=c.reveal('four minutes'))
            a.dashed(xy(5,10),xy(5,34),LEAK,fraction=c.reveal('twenty four litres'))
            note(a,'Net gain','24 ÷ 4 = 6',232,c.reveal('six litres stay'),WATER)
            note(a,'Leak in L/min','9 − 6 = 3',359,c.reveal('three litres per'),LEAK)
        return
    if n==8:
        xy=sheet(a,5,20,range(6),range(0,21,5))
        trace(a,xy,[(0,10),(5,10)],5*c.reveal('inlet and outlet',2.3))
        note(a,'Inlet','5 L/min',234,c.reveal('inlet and outlet'),WATER)
        note(a,'Outlet','5 L/min',340,c.reveal('inlet and outlet'),LEAK)
        return
    xy=sheet(a,10,80,range(0,11,2),range(0,81,20))
    a.dot(*xy(0,8),6,WATER);a.label('8',xy(0,8)[0]+11,xy(0,8)[1]-8,22,WATER)
    if n==5:
        t=c.reveal('final reading is sixty six'); a.dot(*xy(10,66),7,LEAK,t)
        note(a,'Start','8 L',212);note(a,'Finish','66 L',319,t,LEAK)
        a.label('Valve closes at…?',922,478,27,INK,c.reveal('at which minute'))
    elif n==6:
        trace(a,xy,[(0,8),(10,78)],10*c.reveal('closed from the start',1.6),PAPER)
        diff=c.reveal('twelve litres lower')
        a.dot(*xy(10,66),6,LEAK,diff);a.line([xy(10,66),xy(10,78)],LEAK,6,diff)
        note(a,'Shortfall','78 − 66 = 12',249,diff,LEAK)
        note(a,'Open time','12 ÷ 2 = 6 min',368,c.reveal('twelve divided'),WATER)
    else:
        trace(a,xy,[(0,8),(6,38)],6*c.reveal('six minutes',1.8))
        trace(a,xy,[(6,38),(10,66)],6+4*c.reveal('last four minutes',1.8),PAPER)
        a.dot(*xy(6,38),7,LEAK,c.reveal('thirty eight'));a.dashed(xy(6,0),xy(6,38),LEAK,fraction=c.reveal('thirty eight'))
        note(a,'At 6 min','8 + 30 = 38',231,c.reveal('thirty eight'),LEAK)
        note(a,'At 10 min','38 + 28 = 66',363,c.reveal('twenty eight more'),WATER)


def poster(draw):
    return draw(2.0, 1.5)
