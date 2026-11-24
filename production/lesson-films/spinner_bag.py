"""A sector wheel, a two-spinner sample space and labelled draws without replacement."""
from itertools import combinations, permutations, product
from fractions import Fraction
from math import cos,pi,sin
from stage import blend,clamp
BACKGROUND=('#29363f','#1c2937')
BRIDGE='At the spinners, notice what one square of the outcome table represents. At the bag of counters, ask what replaces those squares as the equally likely outcomes.'
HEAD=('What counts as one outcome?','Start with equal chances','Five equal sectors','Count the two green sectors','Two spinners, two readings','The four pairs that sum to five','Three draws without replacement','Count sets of three counters','Check all three colour orders','After each draw','Choose the outcomes first')
PAPER,SEA,GOLD,RED,BLUE,DIM,INK='#f7f0dc','#98dbb7','#f7c171','#f29b90','#9ab9eb','#64798a','#243342'

def check_maths():
    assert Fraction(sum(k=='G' for k in 'GBBGB'),5)==Fraction(2,5)
    assert [(x,y) for x,y in product(range(1,5),repeat=2) if x+y==5]==[(1,4),(2,3),(3,2),(4,1)]
    codes='RRRRBBB'
    u=list(combinations(range(7),3));v=list(permutations(range(7),3))
    assert len(u)==35 and sum(sum(codes[i]=='R' for i in s)==2 for s in u)==18
    assert Fraction(sum(sum(codes[i]=='R' for i in s)==2 for s in v),len(v))==Fraction(18,35)

def text(a,s,x,y,size=34,col=PAPER,t=1,align='left'):
    a.label(s,x,y,size,col,t,align=align,bold=True)

def wheel(a,x,y,r,t=1,green=True):
    for i in range(5):
        base=-pi/2+i*2*pi/5
        points=[(x,y)]+[(x+r*cos(base+j*2*pi/100),y+r*sin(base+j*2*pi/100)) for j in range(21)]
        col=(SEA if green and i in (0,3) else BLUE)
        a.polygon(points,blend(INK,col,.76),INK,3)
        mid=base+pi/5;a.text(('G' if i in (0,3) else 'B') if green else str(i+1),x+.70*r*cos(mid),y+.70*r*sin(mid),31,INK,bold=True)
    phi=-pi/2+(t*2+.12)*2*pi
    a.arrow((x,y),(x+.63*r*cos(phi),y+.63*r*sin(phi)),PAPER,1,5);a.dot(x,y,8,PAPER)

def grid(a,x,y,q=0,wide=79):
    for k in range(1,5):
        a.text(str(k),x+(k-.5)*wide,y-25,27,GOLD,bold=True)
        a.text(str(k),x-32,y+(k-.5)*wide,27,BLUE,bold=True)
    for r in range(4):
        for col in range(4):
            yes=r+col==3 and q>0
            a.box(x+col*wide,y+r*wide,wide-3,wide-3,radius=3,fill=blend(INK,SEA,.75*q) if yes else INK,edge=DIM,stroke=2)
            a.text(f'{r+1},{col+1}',x+(col+.5)*wide,y+(r+.5)*wide,23,INK if yes and q>.55 else PAPER,bold=True)

def counter(a,x,y,k,i):
    col=RED if k=='R' else BLUE
    a.dot(x,y,24,col);a.text(k+str(i),x,y,19,INK,bold=True)

def bag(a,x,y):
    a.box(x-46,y-49,360,178,fill='#2d4150',edge=DIM,stroke=3)
    for i in range(4):counter(a,x+i*76,y,'R',i+1)
    for i in range(3):counter(a,x+31+i*76,y+76,'B',i+1)

def draw(a,n,c):
    text(a,HEAD[n-1],71,69,45);a.line([(71,119),(1206,119)],DIM,2)
    if n in (1,3,4):
        wheel(a,344,367,161,c.reveal('five possible sectors' if n==4 else 'equally likely',1.8))
        if n==1:
            text(a,'Which sectors count?',645,265,39,GOLD)
            text(a,'Equal areas → equal chances',645,410,35,SEA,c.reveal('equally likely'))
        elif n==3:
            text(a,'5 equal sectors',661,245,41,PAPER,c.reveal('five equal sectors'))
            text(a,'2 marked G',661,365,40,SEA,c.reveal('two of them green'))
            text(a,'P(green) = ?',661,486,44,GOLD,c.reveal('probability'))
        else:
            text(a,'Favourable sectors: 2',622,242,36,SEA,c.reveal('two satisfy'))
            text(a,'Possible sectors: 5',622,356,36,BLUE,c.reveal('five possible sectors'))
            text(a,'P(green) = 2/5',622,480,44,GOLD,c.reveal('two over five'))
    elif n==2:
        grid(a,193,221,0,70)
        text(a,'One cell = one ordered pair',616,276,34,PAPER,c.reveal('ordered pairs'))
        text(a,'Why are the cells equally likely?',585,441,31,GOLD,c.reveal('equally likely'))
    elif n in (5,6):
        q=0 if n==5 else c.reveal('four favourable pairs',1.3)
        grid(a,158,211,q,75)
        text(a,'Row = first spinner',617,224,34,BLUE)
        text(a,'Column = second spinner',617,309,34,GOLD)
        text(a,'Wanted: sum 5',617,411,37,SEA)
        if n==6:text(a,'4/16 = 1/4',617,514,46,PAPER,c.reveal('one over four'))
    elif n==7:
        bag(a,162,303)
        text(a,'Draw three counters',620,236,37,GOLD,c.reveal('Draw three'))
        text(a,'Keep each counter out',621,335,33,BLUE,c.reveal('without replacing'))
        text(a,'Exactly 2 red',619,453,43,RED,c.reveal('exactly two red counters'))
    elif n==8:
        pairs=list(combinations(range(1,5),2))
        for i,(r,s) in enumerate(pairs):text(a,f'R{r}, R{s}',138+(i%3)*153,244+(i//3)*88,29,RED,c.reveal('two of the four reds'))
        for i in range(3):counter(a,723+i*91,283,'B',i+1)
        text(a,'6 red pairs × 3 blue choices = 18',630,424,36,PAPER,c.reveal('eighteen favourable sets'),'center')
        text(a,'18 favourable / 35 possible',640,520,40,SEA,c.reveal('eighteen over thirty-five'),'center')
    elif n==9:
        for i,(seq,label) in enumerate([('RRB','4/7 × 3/6 × 3/5'),('RBR','4/7 × 3/6 × 3/5'),('BRR','3/7 × 4/6 × 3/5')]):
            t=c.reveal('Red red blue') if i==0 else c.reveal('Red blue red')
            y=212+i*106
            for j,k in enumerate(seq):
                a.dot(179+j*66,y,23,RED if k=='R' else BLUE,t);a.text(k,179+j*66,y,24,INK,opacity=t,bold=True)
            text(a,label,455,y,33,PAPER,t)
        text(a,'3 × 6/35 = 18/35',641,549,39,SEA,c.reveal('three outcomes are distinct'),'center')
    elif n==10:
        grid(a,162,207,1,73);text(a,'Sums use different cell counts',599,238,33,GOLD)
        text(a,'Bag size: 7 → 6 → 5',598,382,39,BLUE,c.reveal('bag becomes smaller'))
        text(a,'Update eligible colours too.',598,495,30,SEA,c.reveal('eligible colours'))
    else:
        bag(a,157,300);text(a,'Event: exactly two red',612,231,35,RED,c.reveal('exactly'))
        text(a,'Sets: 18/35',612,340,40,SEA,c.reveal('zero and one'))
        text(a,'Orders: 108/210 = 18/35',589,469,33,PAPER,c.reveal('ordered or unordered'))

def poster(draw):return draw(4,1)
