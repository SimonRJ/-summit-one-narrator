"""Lesson 19: a distinct storyboard, from paired counters to a colouring proof.

All geometry is constructed from actual equal squares and every animation cue
is tied to a phrase in this lesson's newly authored recording.
"""
from math import cos, pi, sin
from visuals import AQUA, BLUE, GOLD, PINK, SOFT, WHITE, VIOLET, clamp, ease, mix


def title(a, section, name):
    a.label(section.upper(), 80, 55, 19, AQUA, align='left', bold=True)
    a.label(name, 80, 105, 39, WHITE, align='left', bold=True, display=True)
    a.path(((80, 138), (1200, 138)), SOFT, 2, .35)


def txt(a, s, x, y, size=31, colour=WHITE, alpha=1, align='center'):
    # Keep explanatory labels legible when the video is shown at phone width.
    a.label(s, x, y, max(size,32), colour, alpha, align=align, bold=True)


def board(a, x, y, u, reveal=1, colour=1, removed=0, holes=((0, 0), (3, 3))):
    for r in range(4):
        for col in range(4):
            index = r * 4 + col
            appear = clamp(reveal * 16 - index)
            gone = removed if (r, col) in holes else 0
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


def domino(a, cx, cy, u, theta=0, opacity=1, colour=True, swap=False):
    def pt(x,y): return (cx+x*cos(theta)-y*sin(theta), cy+x*sin(theta)+y*cos(theta))
    for points, ink in [([(-u,-u/2),(0,-u/2),(0,u/2),(-u,u/2)], GOLD if swap else BLUE),
                        ([(0,-u/2),(u,-u/2),(u,u/2),(0,u/2)], BLUE if swap else GOLD)]:
        points=[pt(x,y) for x,y in points]
        a.polygon(points, ink if colour else SOFT, .82*opacity)
    outer=[pt(-u,-u/2),pt(u,-u/2),pt(u,u/2),pt(-u,u/2),pt(-u,-u/2)]
    a.path(outer,WHITE,6,opacity)
    a.path((pt(0,-u/2),pt(0,u/2)),WHITE,2,opacity)


def intro(a,c):
    title(a,'A visual idea','Colour can reveal a hidden rule')
    p=c.after('chessboard',1.2)
    board(a,180,175,92,p,c.after('colours',1.2),0)
    q=c.after('colours',1.0)
    txt(a,'ONE DOMINO',850,235,28,SOFT,q)
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


def small_board(a, x, y, u, reveal=1, colour=1):
    for r in range(3):
        for col in range(3):
            appear=clamp(reveal*9-(r*3+col))
            a.rect(x+col*u+2,y+r*u+2,u-4,u-4,BLUE if (r+col)%2==0 else GOLD,.8*appear*colour)
            a.path(((x+col*u,y+r*u),(x+(col+1)*u,y+r*u),(x+(col+1)*u,y+(r+1)*u),
                    (x+col*u,y+(r+1)*u),(x+col*u,y+r*u)),SOFT,2,appear)


def basic(a,c):
    title(a,'Basic example','Count the colours on a 3 × 3 board')
    p=c.after('three by three',1.5); colour=c.after('blue',1.2)
    small_board(a,230,175,110,p,colour)
    txt(a,'Start in the top-left corner',850,260,29,SOFT,c.after('top-left'))
    txt(a,'How many blue?',850,355,34,BLUE,c.after('Count each colour'))
    txt(a,'How many gold?',850,415,34,GOLD,c.after('Count each colour'))
    txt(a,'Odd or even altogether?',850,500,30,WHITE,c.after('odd or even'))


def basic_answer(a,c):
    title(a,'Basic example','Nine squares leave one unpaired')
    small_board(a,230,175,110,c.opening(),1)
    p=c.after('five blue',1.2); q=c.after('four gold',1.0)
    for i in range(5): a.rounded(740+i*58,240,42,42,5,BLUE,clamp(p*5-i))
    for i in range(4): a.rounded(740+i*58,325,42,42,5,GOLD,clamp(q*4-i))
    txt(a,'5 blue + 4 gold = 9',860,430,34,WHITE,c.after('nine altogether'))
    txt(a,'4 pairs and 1 extra',860,505,31,PINK,c.after('one square remains'))


def medium(a,c):
    title(a,'Medium example','Remove two neighbouring squares')
    p=c.after('four by four',1.1); gone=c.after('Remove two neighbouring',1.3)
    board(a,210,170,94,p,1,gone,((0,0),(0,1)))
    q=c.after('Each domino')
    domino(a,920,325,83,opacity=q)
    txt(a,'two edge-sharing squares',920,440,27,SOFT,q)
    txt(a,'Can the rest be covered?',920,515,31,WHITE,c.after('cover the rest'))


def medium_answer(a,c):
    title(a,'Medium example','A covering that works')
    x,y,u=210,170,94
    board(a,x,y,u,1,.5,1,((0,0),(0,1)))
    slots=[(0,2)]+[(r,col) for r in (1,2,3) for col in (0,2)]
    first=c.after('Place one domino',2)
    rest=c.after('then place two horizontal dominoes',5)
    for i,(r,col) in enumerate(slots):
        slide=first if i==0 else ease(clamp(rest*6-(i-1)))
        origin_x=745+(i%4)*106
        origin_y=260+(i//4)*86
        target_x=x+(col+1)*u
        target_y=y+(r+.5)*u
        # A narrow inset preserves the seam between neighbouring dominoes.
        domino(a,mix(origin_x,target_x,slide),mix(origin_y,target_y,slide)-22*sin(pi*slide),
               mix(43,u-4,slide),swap=bool(r%2))
    txt(a,'1 + 2 + 2 + 2 = 7',925,425,37,WHITE,c.after('seven dominoes'))
    txt(a,'7 dominoes cover 14 squares',925,505,29,AQUA,c.after('fourteen squares'))


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
    txt(a,'14 ÷ 2 = 7 dominoes needed',640,215,37,WHITE,p)
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
