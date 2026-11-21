"""An urn, two order branches and the lamp's finite conditional sample space."""
from fractions import Fraction
from itertools import permutations
from math import cos, pi, sin
from stage import between, blend, clamp, mix

BACKGROUND = ('#241e3a', '#191b29')
LIGHT, SUN, MOON, DUSK, PANEL, DIM = '#fff1d4','#ffd176','#a8c5ea','#81739a','#37324c','#605b71'
BRIDGE = 'When the lamp lights, find the pairs you can cross out before choosing the denominator.'


def check_maths():
    pairs=list(permutations(range(5),2))
    sun=lambda d:d<2
    lit=[p for p in pairs if any(map(sun,p))]
    assert len(pairs)==20 and len(lit)==14
    assert Fraction(sum(sun(i) and sun(j) for i,j in pairs),20)==Fraction(1,10)
    assert Fraction(sum(sun(i)!=sun(j) for i,j in pairs),20)==Fraction(3,5)
    assert Fraction(sum(sun(i) and sun(j) for i,j in lit),len(lit))==Fraction(1,7)


def stamp(a,x,y,sun,r=31,selected=True):
    edge = SUN if sun else MOON
    if not selected:edge=DIM
    a.dot(x,y,r,edge);a.dot(x,y,r-3,PANEL)
    if sun:
        a.dot(x,y,r*.29,edge)
        for j in range(8):
            angle=2*pi*j/8
            a.line([(x+cos(angle)*r*.43,y+sin(angle)*r*.43),(x+cos(angle)*r*.64,y+sin(angle)*r*.64)],edge,3)
    else:
        a.dot(x-2,y,r*.57,edge);a.dot(x+r*.18,y-r*.13,r*.46,PANEL)


def lamp(a,x,y,on):
    a.dot(x,y,48,blend(DIM,SUN,on));a.dot(x,y,40,blend(PANEL,'#ffe290',on))
    a.line([(x-15,y+45),(x-10,y+61),(x+10,y+61),(x+15,y+45)],MOON,4)
    if on>0:
        for j in range(7):
            ang=pi*(1.05+j*.15)
            a.line([(x+57*cos(ang),y+57*sin(ang)),(x+72*cos(ang),y+72*sin(ang))],SUN,3,on)


def paired_row(a,y,first,second,reveal,math_line,math_op):
    stamp(a,187,y,first,38);a.arrow((245,y),(393,y),DUSK,reveal,3)
    if reveal>.05:stamp(a,453,y,second,38)
    a.label(math_line,574,y,34,LIGHT,math_op,bold=True)


def draw(a,n,c):
    titles=['Two suns and three moons','Leave the first disc out','One of each, in either order',
            'Count the two orders','What did the lamp reveal?','Cross out the dark outcomes','Read the lit outcomes']
    a.label(titles[n-1],82,88,46,LIGHT,bold=True)
    if n in (1,2):
        xs=[180,372,564,756,948]
        for i,x in enumerate(xs):
            take=c.reveal('after that sun comes out',1.2) if n==2 and i==0 else 0
            stamp(a,x,y=mix(280,181,take),sun=i<2,r=57)
        if n==1:
            a.text('Draw two discs. Keep the first disc out.',640,479,36,MOON,opacity=c.reveal('leave the first disc out'))
        else:
            a.label('First draw',144,414,25,MOON)
            a.label('2 / 5',144,471,40,LIGHT,bold=True)
            a.label('Second draw',470,414,25,MOON,c.reveal('one sun remains'))
            a.label('1 / 4',470,471,40,LIGHT,c.reveal('one sun remains'),bold=True)
            a.label('Two suns',834,414,25,SUN,c.reveal('the chance of two suns'))
            a.label('2/5 × 1/4 = 1/10',834,471,35,LIGHT,c.reveal('that is one tenth'),bold=True)
    elif n in (3,4):
        paired_row(a,249,True,False,c.reveal('three of the four') if n==3 else 1,
                   '2/5 × 3/4 = 6/20',0 if n==3 else c.reveal('sun then moon'))
        paired_row(a,408,False,True,c.reveal('if a moon comes first') if n==3 else 1,
                   '?' if n==3 else '3/5 × 2/4 = 6/20',
                   c.reveal('how many') if n==3 else c.reveal('moon then sun'))
        if n==4:
            a.text('6/20 + 6/20 = 3/5',734,533,40,SUN,opacity=c.reveal('so add them'),bold=True)
    elif n==5:
        a.box(155,200,532,260,radius=25,fill=PANEL,edge=DUSK,stroke=4)
        for x in (312,525):a.dot(x,326,64,DIM);a.text('?',x,326,52,LIGHT,bold=True)
        lamp(a,945,307,c.reveal('at least one sun',1))
        a.text('At least one sun',942,434,30,SUN,opacity=c.reveal('at least one sun'),bold=True)
        a.text('Are both discs suns?',640,537,35,LIGHT,opacity=c.reveal('both discs show suns'))
    else:
        left,top,sz=274,188,66
        a.label('First',74,336,26,MOON);a.text('Second draw',left+2.5*sz,133,23,MOON)
        for i in range(5):
            code=('S'+str(i+1)) if i<2 else ('M'+str(i-1))
            a.text(code,left+(i+.5)*sz,top-22,25,SUN if i<2 else MOON,bold=True)
            a.text(code,left-37,top+(i+.5)*sz,25,SUN if i<2 else MOON,bold=True)
        gone=c.reveal('six dark pairs',1.0) if n==6 else 1
        both=c.reveal('both suns',.8) if n==7 else 0
        revealed=clamp((c.t-c.start)/2.4)*25 if n==6 else 25
        for i in range(5):
            for j in range(5):
                x,y=left+j*sz,top+i*sz
                if i==j:
                    a.line([(x+19,y+47),(x+46,y+20)],DIM,3);continue
                if i*5+j>revealed:continue
                dark=min(i,j)>=2
                fill=blend('#5d647c',PANEL,gone) if dark else blend('#61707d',SUN,both if max(i,j)<2 else 0)
                a.box(x+3,y+3,sz-6,sz-6,radius=7,fill=fill)
                if dark and gone>.05:
                    a.line([(x+18,y+17),(x+48,y+47)],MOON,3,gone)
                    a.line([(x+48,y+17),(x+18,y+47)],MOON,3,gone)
                if n==7 and max(i,j)<2 and both:a.text('●',x+sz/2,y+sz/2,23,PANEL,opacity=both)
        lamp(a,921,242,1)
        if n==6:
            a.text('20 ordered pairs',925,363,31,LIGHT,opacity=c.reveal('twenty equally likely'),bold=True)
            a.text('20 − 6 = 14',925,445,40,SUN,opacity=c.reveal('fourteen pairs'),bold=True)
        else:
            a.text('Two orders with both suns',924,365,25,LIGHT,opacity=both)
            a.text('2/14 = 1/7',925,445,45,SUN,opacity=c.reveal('one seventh'),bold=True)
        a.label('Diagonal: the same disc twice',270,570,21,MOON)


def poster(draw):
    return draw(4.1,1.5)
