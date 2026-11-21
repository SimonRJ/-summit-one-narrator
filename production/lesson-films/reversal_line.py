"""S010. A railway ticket press with reversing digit wheels and a rejection punch."""
from math import cos, pi, sin
from stage import mix

BACKGROUND = ('#112937','#1b4655')
BRIDGE = 'Follow the two digits when the ticket turns. At inspection, compare both the printed sum and the letters that received its digits.'
CREAM, INK, BLUE, MUSTARD = '#fcf0d0','#173542','#80d2df','#ffbb66'
PAPER, MAROON, TEAL = '#fae1ad','#9b303d','#195a5b'


def check_maths():
    assert [a for a in range(10) if a+a==8]==[4]
    reversed_pairs=[(a,b) for a in range(1,10) for b in range(1,10)
                    if a+b==8 and 10*b+a-(10*a+b)==36]
    assert reversed_pairs==[(2,6)]
    allowed=[]
    for first in range(10,100):
        a,b=divmod(first,10)
        for c in range(10):
            total=first+10*a+c
            h,rem=divmod(total,100); d,last=divmod(rem,10)
            if b==h and b and last==0 and len({a,b,c,d})==4:
                allowed.append((first,10*a+c,total))
    assert min(allowed)==(61,69,130) and 51+59==110


def ticket(a,x,y,w,h,caption):
    a.box(x+4,y+7,w,h,radius=12,fill='#10232b')
    a.box(x,y,w,h,radius=12,fill=PAPER,edge='#c19a67')
    for cy in (y+h*.33,y+h*.67):
        a.dot(x,cy,9,'#193b48');a.dot(x+w,cy,9,'#193b48')
    a.label(caption,x+27,y+30,21,INK,bold=True)
    a.dashed((x+20,y+56),(x+w-20,y+56),'#937e5c',2,7,6)


def tile(a,x,y,text,col=INK):
    a.box(x-43,y-51,86,102,fill='#fff5de',edge='#b69d78',radius=7)
    a.text(text,x,y,68,col,bold=True)


def row(a,text,x,y,size=34,color=CREAM,op=1):
    a.label(text,x,y,size,color,op,bold=True)


def stamp(a,x,y,label,col,op):
    a.box(x,y,288,76,fill=PAPER,edge=col,stroke=5,radius=3,opacity=op)
    a.text(label,x+144,y+38,41,col,bold=True,opacity=op)


def draw(a,n,t):
    # The route strip carries position labels, drawn independently of the tickets.
    for x in range(72,1210,48):
        a.line([(x,122),(x+25,122)],'#53747a',2)
    titles=['A reversible number ticket','Measure the gain per unit','Which ticket gains thirty-six?',
            'Send two tickets to inspection','Check the letter identities','Issue the first legal ticket']
    row(a,titles[n-1],70,76,48)
    if n==1:
        ticket(a,138,183,1004,318,'RETURN TICKET')
        u=t.reveal('each box shows four')
        tile(a,530,357,'4' if u>0.5 else '?')
        tile(a,750,357,'4' if u>0.5 else '?')
        a.text('+',640,354,41,INK)
        a.text('total 8',640,457,30,INK,bold=True)
        row(a,'Same digits. Same return trip.',280,561,35,BLUE,t.reveal('change nothing'))
    elif n==2:
        ticket(a,80,188,620,318,'ONE UNIT OF DIGIT DIFFERENCE')
        move=t.reveal('from units to tens',1.8)
        for word,sg in [('smaller',1),('larger',-1)]:
            x=390-sg*126*cos(pi*move)
            y=351+sg*43*sin(pi*move)
            a.box(x-83,y-38,166,76,fill='#fff5de',edge=INK,radius=8)
            a.text(word,x,y,32,INK,bold=True)
        a.text('tens',264,455,26,INK)
        a.text('units',516,455,26,INK)
        row(a,'+10 in tens',738,261,40,BLUE,t.reveal('gains ten'))
        row(a,'−1 in units',738,333,40,MUSTARD,t.reveal('loses one'))
        row(a,'Net +9',738,430,53,CREAM,t.reveal('net gain is nine'))
        row(a,'36 ÷ 9 = 4',738,523,43,BLUE,t.reveal('digit four larger'))
    elif n==3:
        ticket(a,81,178,577,335,'OUTWARD / RETURN')
        move=t.reveal('then reverse it',1.4)
        reveal=t.reveal('smaller digit is two')
        for digit,sg in [('2',1),('6',-1)]:
            x=370-sg*87*cos(pi*move);y=374+sg*43*sin(pi*move)
            tile(a,x,y,digit if reveal>.5 else '?')
        row(a,'sum = 8',708,218,39)
        row(a,'difference = 4',708,285,38,MUSTARD)
        for j in range(8):
            split=t.reveal('four counters aside',1.1)
            cx=739+(j%4)*49+(24 if j>=4 else 0)*split
            if j in (2,3): cx+=34*t.reveal('two matching pairs',.8)
            cy=369+52*(j//4)
            a.dot(cx,cy,14,MUSTARD if j>=4 else BLUE)
        row(a,'62 − 26 = 36',707,505,45,CREAM,t.reveal('Sixty two minus'))
    else:
        ticket(a,78,168,567,384,'COLUMN INSPECTION')
        if n==4:
            shown=['AB','AC','BD0']
            if t.reveal('B is one')>.5: shown=['A1','AC','1D0']
        elif n==5:
            shown=['A1','A9','1D0'] if t.reveal('Only nine')>.5 else ['A1','AC','1D0']
            if t.reveal('Fifty one plus')>.5:shown=['51','59','110']
        else:shown=['61','69','130']
        for idx,(y,number) in enumerate(zip((292,369,477),shown)):
            a.text(number,530,y,68,INK,bold=True,align='right')
            if idx==1:a.text('+',186,y,48,INK)
        a.line([(171,416),(551,416)],INK,4)
        if n==4:
            row(a,'A, B, C, D',697,253,48,BLUE)
            row(a,'4 different digits',697,327,34)
            row(a,'Smallest AB?',697,403,42,MUSTARD,t.reveal('smallest A B'))
            row(a,'B = 1',697,516,52,CREAM,t.reveal('B is one'))
        elif n==5:
            row(a,'1 + C = 10',695,220,40,BLUE)
            row(a,'2 × A + 1 ≥ 10',695,287,37,CREAM,t.reveal('twice A plus one'))
            row(a,'A = 5',695,360,42,MUSTARD,t.reveal('first candidate is five'))
            row(a,'B = 1 and D = 1',695,426,36,CREAM,t.reveal('Two different letters'))
            stamp(a,695,486,'REJECTED',MAROON,t.reveal('Reject that ticket'))
        else:
            row(a,'A     B     C     D',692,246,37,BLUE)
            row(a,'6     1     9     3',692,327,39,CREAM,t.reveal('six one nine three'))
            stamp(a,701,402,'ACCEPTED',TEAL,t.reveal('None collides'))
            row(a,'Minimum AB = 61',690,559,39,MUSTARD,t.reveal('smallest legal'))


def poster(draw):
    return draw(7,1.5)
