"""Lesson 19: a distinct storyboard, from paired counters to a colouring proof.

All geometry is constructed from actual equal squares and every animation cue
is tied to a phrase in this lesson's newly authored recording.
"""
from math import cos, pi, sin
from visuals import AQUA, BLUE, GOLD, PINK, SOFT, WHITE, VIOLET, clamp, ease


def title(a, section, name):
    a.label(section.upper(), 80, 55, 19, AQUA, align='left', bold=True)
    a.label(name, 80, 105, 39, WHITE, align='left', bold=True, display=True)
    a.path(((80, 138), (1200, 138)), SOFT, 2, .35)


def txt(a, s, x, y, size=31, colour=WHITE, alpha=1, align='center'):
    a.label(s, x, y, size, colour, alpha, align=align, bold=True)


def board(a, x, y, u, reveal=1, colour=1, removed=0):
    for r in range(4):
        for col in range(4):
            index = r * 4 + col
            appear = clamp(reveal * 16 - index)
            gone = removed if (r, col) in ((0, 0), (3, 3)) else 0
            fill = BLUE if (r + col) % 2 == 0 else GOLD
            base = (x + col*u, y + r*u)
            # A faint neutral tile remains visible before the colours are revealed.
            a.rect(base[0]+2, base[1]+2, u-4, u-4, SOFT, .12 * appear * (1-gone))
            a.rect(base[0]+2, base[1]+2, u-4, u-4, fill, .72 * appear * colour * (1-gone))
            a.path((base, (base[0]+u,base[1]), (base[0]+u,base[1]+u),
                    (base[0],base[1]+u), base), SOFT, 2, appear)
            if gone:
                a.path(((base[0]+15,base[1]+15), (base[0]+u-15,base[1]+u-15)), PINK, 3, gone)
                a.path(((base[0]+15,base[1]+u-15), (base[0]+u-15,base[1]+15)), PINK, 3, gone)


def domino(a, cx, cy, u, theta=0, opacity=1, colour=True):
    def pt(x,y): return (cx+x*cos(theta)-y*sin(theta), cy+x*sin(theta)+y*cos(theta))
    for points, ink in [([(-u,-u/2),(0,-u/2),(0,u/2),(-u,u/2)], BLUE),
                        ([(0,-u/2),(u,-u/2),(u,u/2),(0,u/2)], GOLD)]:
        points=[pt(x,y) for x,y in points]
        a.polygon(points, ink if colour else SOFT, .82*opacity)
        a.path(points+[points[0]], WHITE, 3, opacity)


def intro(a,c):
    title(a,'A visual idea','Colour can reveal a hidden rule')
    p=c.after('chessboard',1.2)
    board(a,180,175,92,p,c.after('colours',1.2),0)
    q=c.after('colours',1.0)
    txt(a,'SAME BOARD',850,235,28,SOFT,q)
    domino(a,850,335,75,theta=c.after('covering',1.4)*pi/2,opacity=q)
    txt(a,'one blue  +  one gold',850,455,31,WHITE,q)
    txt(a,'Can every square be covered?',850,520,29,PINK,c.after('impossible'))


def applications(a,c):
    title(a,'Where to use it','Patterns, proof and investigation')
    for x,name,p in [(260,'AMC',c.after('AMC')),(640,'ROSSMOYNE',c.after('Rossmoyne')),(1020,'MAWA',c.after('MAWA'))]:
        a.rounded(x-155,190,310,320,18,SOFT,.13*p)
        txt(a,name,x,235,27,AQUA,p)
    p=c.after('odd or even pattern')
    for i in range(5): a.circle((175+i*42,340),14,BLUE if i<4 else PINK,p)
    txt(a,'pairs + one',260,440,27,WHITE,p)
    q=c.after('same rule')
    domino(a,640,340,48,opacity=q)
    txt(a,'one of each',640,440,27,WHITE,q)
    r=c.after('boards can be tiled')
    for i in range(3): domino(a,1020,300+i*48,38,opacity=r)
    txt(a,'test arrangements',1020,470,27,WHITE,r)


def counter_array(a, count, x0, y0, colour, pair, alpha=1, mark_extra=False):
    # Start with the two rows spread apart, then bring each partner together.
    # This prevents unrelated counters crossing or briefly overlapping.
    for i in range(count):
        pairindex=i//2
        newx=x0+pairindex*(59 if count == 15 else 48)
        oldx=newx; oldy=265+(i%2)*155
        newy=325+(i%2)*38
        x=oldx+(newx-oldx)*pair; y=oldy+(newy-oldy)*pair
        if mark_extra and i==14:
            a.circle((x,y),20,PINK,alpha)
        a.circle((x,y),14,colour,alpha)


def basic(a,c):
    title(a,'Basic example','Odd or even without adding?')
    p=c.after('fifteen blue'); q=c.after('twenty gold'); move=c.after('Group them in twos',2.0)
    txt(a,'15 BLUE',300,205,32,BLUE,p);txt(a,'20 GOLD',915,205,32,GOLD,q)
    counter_array(a,15,105,250,BLUE,move,p)
    counter_array(a,20,690,250,GOLD,move,q)
    txt(a,'Find any counter without a partner',640,515,29,SOFT,c.after('unpaired counter'))


def basic_answer(a,c):
    title(a,'Basic example','Pairs leave one extra')
    counter_array(a,15,105,250,BLUE,1,c.opening(),True)
    counter_array(a,20,690,250,GOLD,1,c.opening())
    txt(a,'7 pairs + 1',300,245,35,BLUE,c.after('seven pairs'))
    txt(a,'10 pairs',915,245,35,GOLD,c.after('ten pairs'))
    txt(a,'15 + 20 = 35   •   odd',640,505,39,WHITE,c.after('thirty-five'))


def line(a, location, arc=0, target=0):
    left,step,y=155,86,370
    a.path(((left,y),(left+11*step,y)),SOFT,3)
    for n in range(11,23):
        x=left+(n-11)*step; colour=BLUE if n%2 else GOLD
        a.circle((x,y),6,colour)
        txt(a,str(n),x,y+50,26,colour)
    x=left+(location-11)*step
    a.circle((x,y-arc),19,AQUA)
    a.circle((left+9*step,y),23,PINK,.24*target)
    txt(a,'target 20',left+9*step,255,27,PINK,target)


def medium(a,c):
    title(a,'Medium example','Can even jumps reach 20?')
    p=c.after('Jump any even number',1.5);q=c.after('left or right',1.5);r=c.after('Try a few jumps',1.5)
    if r>0:loc=21-2*r;arc=90*sin(pi*r)
    elif q>0:loc=17+4*q;arc=110*sin(pi*q)
    else:loc=15+2*p;arc=90*sin(pi*p)
    line(a,loc,arc,c.after('twenty'))
    txt(a,'Start: 15',290,230,29,AQUA,c.after('fifteen'))
    txt(a,'Each jump: 2, 4, 6, …',640,515,29,SOFT,c.after('even number'))


def medium_answer(a,c):
    title(a,'Medium example','Even jumps keep the position odd')
    p=c.after('jump of two',1.6);q=c.after('or four',1.6)
    loc=17+4*q if q>0 else 15+2*p
    arc=(115*sin(pi*q) if q>0 else 85*sin(pi*p))
    line(a,loc,arc,c.after('Twenty is even'))
    txt(a,'odd  +  even  =  odd',640,500,39,WHITE,c.after('stays on odd numbers'))


def puzzle(a,c):
    title(a,'Harder challenge','Can dominoes cover this board?')
    gone=c.after('corners removed',1.1)
    board(a,210,170,94,c.after('four by four',1.1),0,gone)
    p=c.after('Each domino',.9)
    domino(a,930,290,83,opacity=p,colour=False)
    txt(a,'two edge-sharing squares',930,410,28,SOFT,p)
    txt(a,'7 dominoes?',930,500,35,WHITE,c.after('seven dominoes'))
    txt(a,'no overlap',930,548,25,PINK,c.after('no overlap'))


def colour_rule(a,c):
    title(a,'A colouring proof','Each domino needs one of each colour')
    p=c.after('Colour the full board',1.4)
    board(a,210,170,94,1,p,0)
    txt(a,'8 blue',790,205,31,BLUE,c.after('eight blue'))
    txt(a,'8 gold',1035,205,31,GOLD,c.after('eight gold'))
    q=c.after('Each domino',.6)
    turn=c.after('vertical',1.3)
    domino(a,920,355,87,turn*pi/2,q)
    txt(a,'1 blue  +  1 gold',920,495,33,WHITE,c.after('one of each colour'))


def mismatch(a,c):
    title(a,'A colouring proof','The missing corners break the balance')
    gone=c.after('removed corners',1.1)
    board(a,210,170,94,1,1,gone)
    have=c.after('six blue')
    txt(a,'AVAILABLE',800,220,24,SOFT,have,align='left')
    for i in range(8):
        x=800+i*45
        a.rounded(x,270,31,31,4,BLUE,.9*have if i<6 else .1*have)
        a.rounded(x,330,31,31,4,GOLD,.9*have)
    txt(a,'6 blue',800,382,26,BLUE,have,align='left')
    txt(a,'8 gold',1060,382,26,GOLD,have,align='left')
    q=c.after('need seven')
    txt(a,'7 blue needed',800,455,30,WHITE,q,align='left')
    txt(a,'but only 6 are available',800,505,28,PINK,c.after('only six blue'),align='left')
    txt(a,'No covering is possible',800,555,29,PINK,c.after('impossible'),align='left')


def mistake(a,c):
    title(a,'Common mistakes','An even area is only a first check')
    p=c.after('fourteen squares')
    txt(a,'14 squares = 7 dominoes',640,215,37,WHITE,p)
    q=c.after('colours do not balance')
    board(a,205,270,70,1,1,1)
    txt(a,'6 blue ≠ 8 gold',355,585,29,PINK,q)
    r=c.after('colour balance alone')
    txt(a,'Balanced colours may still be separated',865,290,27,SOFT,r)
    # Two isolated cells, one of each colour, on a row of four squares.
    for i in range(4):
        x=710+90*i
        a.path(((x,335),(x+90,335),(x+90,425),(x,425),(x,335)),SOFT,2,r)
        if i in (0,3):a.rect(x+3,338,84,84,BLUE if i==0 else GOLD,.8*r)
        else:
            a.path(((x+18,353),(x+72,407)),PINK,3,r)
            a.path(((x+18,407),(x+72,353)),PINK,3,r)
    txt(a,'1 blue + 1 gold, but no adjacent pair',865,485,26,WHITE,r)
    txt(a,'Still check the shape.',865,535,27,PINK,c.after('join up legally'))


def recap(a,c):
    title(a,'Exam checklist','Explain the rule, then count')
    p=c.after('allowed piece');q=c.after('colouring');r=c.after('Count the colours')
    txt(a,'1',135,230,42,AQUA,p);txt(a,'What does one piece cover?',200,230,33,WHITE,p,'left')
    txt(a,'2',135,320,42,AQUA,q);txt(a,'Choose a helpful colouring.',200,320,33,WHITE,q,'left')
    txt(a,'3',135,410,42,AQUA,r);txt(a,'Count and explain the mismatch.',200,410,33,WHITE,r,'left')
    domino(a,1030,345,65,opacity=q)


SCENES=(intro,applications,basic,basic_answer,medium,medium_answer,puzzle,colour_rule,mismatch,mistake,recap)
def draw(a,c,scene):SCENES[scene-1](a,c)
