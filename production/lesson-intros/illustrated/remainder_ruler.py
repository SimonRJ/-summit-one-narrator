"""Draw the S066 packet experiment and translate its bounded number line."""
from math import sin, pi

PAPER = '#faf5e9'
INK = '#23384a'
TEAL = '#12756f'
GOLD = '#a95715'
PALE = '#dcebe3'
MUTED = '#626f77'
RED = '#af4543'
POINTS = (80, 120, 160, 200)


def title(c, text):
    c.text(text, 70, 63, 42, INK, 'lm', True)


def caption(c, text):
    c.text(text, 640, 528, 36, INK, bold=True)


def tray(c, x, y, capacity, filled, extra):
    for i in range(capacity):
        cx = x + i * 58
        c.rect(cx-24, y-24, 48, 48, PALE, TEAL, 2)
        if i < filled:
            c.dot(cx, y, 17, TEAL)
        elif extra:
            c.dot(cx, y - 65*(1-extra), 17, GOLD)
    c.text(str(capacity)+' spaces', x, y+65, 26, INK, 'lm')


def opening(c, q):
    title(c, 'Remainders: how far to the next multiple?')
    c.text('The remainder is what stays outside full groups.', 640, 145, 31, INK)
    if q.after('space for five'):
        tray(c, 150, 265, 5, 4, q.after('One more counter'))
    if q.after('space for eight'):
        tray(c, 650, 265, 8, 7, q.after('One more counter'))
    if q.after('one empty space'):
        caption(c, '4 + 1 = 5      •      7 + 1 = 8' if q.after('One more counter') else '4 of 5      •      7 of 8')


def joint(c, q):
    title(c, 'Exam clue: one short in two different groups')
    c.text('In an AMC or Rossmoyne-style problem, look for two almost-full groups.',
           640, 149, 30, INK)
    p = q.after('Add one to that number')
    tray(c, 150, 265, 5, 4, p)
    if q.after('grouped in eights'):
        tray(c, 650, 265, 8, 7, p)
    if q.after('both times tables'):
        caption(c, 'N + 1 is a multiple of both 5 and 8')


def packets(c, move):
    for i in range(51):
        group, spot = divmod(i, 6)
        gx, gy = 111+(group % 4)*245, 214+(group//4)*141
        if group == 8:
            gx, gy = 1040, 290
        x, y = 170+(i%17)*57, 195+(i//17)*55
        tx, ty = gx+(spot%3)*49, gy+(spot//3)*46
        p = min(1, max(0, move*9-group))
        if p > 0 and group < 8 and spot == 0:
            c.rect(gx-28,gy-24,154,95,PALE,TEAL,2)
        c.dot(x+(tx-x)*p, y+(ty-y)*p-22*sin(pi*p), 16, GOLD if group==8 and p else TEAL)


def packet_question(c,q):
    title(c,'Can every counter fit into a packet of six?')
    if q.after('fifty-one counters'):
        packets(c,0)
    if q.after('Each packet holds six'):
        caption(c,'51 counters     •     6 per packet')


def packet_answer(c,q):
    title(c,'Pack the same fifty-one counters')
    packets(c,q.after('Slide six counters',3))
    if q.after('Three counters stay loose'):
        caption(c,'8 × 6 + 3 = 51')


def endings(c,q):
    title(c,'Find the missing digit in 46□')
    if q.after('starts with four and six'):
        c.text('4  6  ?',640,148,48,INK,bold=True)
    if q.after('last two digits'):
        for i in range(10):
            x=131+113*i
            c.rect(x-42,246,84,70,PALE,TEAL)
            c.text(str(60+i),x,280,37,INK,bold=True)
    if q.after('four times table'):
        caption(c,'Which endings are multiples of 4?')


def digit_sums(c,q):
    title(c,'Use both divisibility tests')
    for i,(end,cue) in enumerate(zip((60,64,68),('Keep sixty','sixty-four','and sixty-eight'))):
        x=250+i*390
        if q.after(cue):
            c.text(str(end+400) if q.after('hundreds digit back') else str(end),x,224,60,INK,bold=True)
        if q.after(('are ten','fourteen','and eighteen')[i]):
            c.text(f'4 + 6 + {end%10} = {10+end%10}',x,342,33,TEAL,bold=True)
    if q.after('Only eighteen'):
        # Keep the three candidates visible and mark the one passing both tests.
        c.line([(887,385),(1174,385)],TEAL,5)
    if q.after('missing digit is eight'):
        c.text('The missing digit is 8.',640,451,40,TEAL,bold=True)
        caption(c,'468 ÷ 4 = 117       468 ÷ 3 = 156')


def xpos(n):
    return 88+(n-40)*5.4


def ruler(c,lo,hi):
    y=294
    c.line([(xpos(40),y),(xpos(240),y)],MUTED,3)
    c.line([(xpos(lo),y),(xpos(hi),y)],TEAL,10)
    for n in range(40,241,5):
        x=xpos(n)
        c.line([(x,y),(x,y+(20 if n%40==0 else 9))],INK,2)
        if n%40==0:
            c.text(str(n),x,y+49,27,INK)
    for n in (lo,hi):
        x=xpos(n)
        c.line([(x,y-28),(x,y+10)],TEAL,4)
        c.text(str(round(n)),x,y-61,30,TEAL,bold=True)


def mark(c,n,y,colour):
    x=xpos(n)
    c.line([(x,292),(x,y)],colour,2)
    c.dot(x,y,9,colour)
    c.text(str(round(n)),x,y+36,31,colour,bold=True)


def challenge(c,q):
    title(c,'Which points satisfy both conditions?')
    if q.after('allowed numbers'):
        ruler(c,63,222)
    if q.after('divided by five'):
        c.text('N ÷ 5 leaves 4',370,474,36,INK,bold=True)
    if q.after('divided by eight'):
        c.text('N ÷ 8 leaves 7',890,474,36,INK,bold=True)


def shift(c,q):
    title(c,'Mark the common multiples on the shifted ruler')
    p=q.after('one place right',1.1)
    ruler(c,63+p,222+p)
    if q.after('one place right'):
        c.text('63 + 1 = 64',291,148,31,TEAL,bold=True)
        c.text('222 + 1 = 223',982,148,31,TEAL,bold=True)
    if q.after('common multiple is forty'):
        c.text('LCM(5, 8) = 40',640,148,32,INK,bold=True)
    for n,phrase in zip(POINTS,('Mark eighty','one hundred and twenty','one hundred and sixty','sixty, and two hundred')):
        if q.after(phrase):
            mark(c,n,404,GOLD)
    if q.after('two hundred and forty'):
        mark(c,240,404,RED)


def restore(c,q):
    title(c,'Return to the original interval')
    p=q.after('one place left',1.2)
    ruler(c,64-p,223-p)
    for n in POINTS:
        mark(c,n-p,404,GOLD)
    if q.after('one place left'):
        c.text('Subtract 1 from each marked multiple.',640,145,32,TEAL,bold=True)
    if q.after('three gaps'):
        for left,right in zip(POINTS,POINTS[1:]):
            c.line([(xpos(left-1)+10,404),(xpos(right-1)-10,404)],TEAL,3)
        caption(c,'4 points     •     3 gaps')


def test(c,q):
    title(c,'Check both ends of the sequence')
    for row,(n,phrase,first,second) in enumerate(((79,'first point','seventy-five plus four','seventy-two plus seven'),(199,'last point','ninety-five plus four','ninety-two plus seven'))):
        y=219+row*130
        if q.after(phrase):
            c.text(str(n),159,y,45,GOLD,bold=True)
        if q.after(first):
            c.text(f'{n//5} × 5 + 4 = {n}',515,y,36,INK,bold=True)
        if q.after(second):
            c.text(f'{n//8} × 8 + 7 = {n}',960,y,36,INK,bold=True)
    if q.after('Stepping forty'):
        caption(c,'40 = 8 × 5 = 5 × 8')


def boundary(c,q):
    title(c,'What changes when the upper end moves?')
    p=q.after('down to one hundred and ninety-eight',1.7)
    hi=222-24*p
    ruler(c,63,hi)
    for n in POINTS:
        mark(c,n-1,404,GOLD if n-1<=hi else RED)
    if q.after('Three answers remain'):
        c.text('79, 119 and 159 remain',640,504,33,INK,bold=True)
    if q.after('A boundary can change'):
        c.text('Add 1 → find common multiples → subtract 1 → check bounds',
               640,570,32,TEAL,bold=True)


SCENES=(opening,joint,packet_question,packet_answer,endings,digit_sums,challenge,shift,restore,test,boundary)


def verify():
    assert divmod(51,6)==(8,3)
    assert [n for n in range(460,470) if n%4==n%3==0]==[468]
    assert [n for n in range(63,223) if n%5==4 and n%8==7]==[n-1 for n in POINTS]
    assert [n for n in range(63,199) if n%5==4 and n%8==7]==[79,119,159]
