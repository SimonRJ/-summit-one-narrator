"""An out-and-back ride with a distance counter, an elapsed clock and a ferry gate."""
from fractions import Fraction
from math import cos,pi,sin
from stage import clamp, mix

BACKGROUND=('#293b39','#1e2e31')
BRIDGE='On the film’s out-and-back ride, the distance counter stops for twelve minutes. Does the elapsed-time counter stop too? Decide which total belongs under the total distance.'
HEAD=('Two counters on a bike','Out to the ferry','Wait by the gate','Follow the return wheel','Read both final totals','Find one steady speed','Home by the deadline','Use the time still available')
PAPER,GOLD,SEA,RED,DIM='#fff3d9','#ffc477','#91d1c6','#ec957f','#687d79'


def check_maths():
    out,home,wait=Fraction(24,12),Fraction(24,24),Fraction(12,60)
    assert (out+home+wait)*60==192 and 48/(out+wait+home)==15
    assert 24/(3-out-wait)==30


def txt(a,s,x,y,size=34,col=PAPER,q=1,align='left'):
    a.label(s,x,y,size,col,q,align=align,bold=True)


def bicycle(a,x,y,t):
    for dx in (-26,26):
        a.dot(x+dx,y,18,PAPER);a.dot(x+dx,y,14,'#293b39')
        az=t*6*pi
        a.line([(x+dx-12*cos(az),y-12*sin(az)),(x+dx+12*cos(az),y+12*sin(az))],SEA,2)
    a.line([(x-26,y),(x-10,y-27),(x+5,y),(x-26,y),(x+17,y-23),(x+26,y)],GOLD,4)
    a.line([(x-15,y-28),(x-7,y-28)],PAPER,4)


def road(a,t,gate=0,back=False):
    left,right=136,1110;y=330
    a.line([(left,y),(right,y)],DIM,7)
    for x,name in ((left,'Home'),(right,'Ferry')):
        a.dot(x,y,7,PAPER);a.text(name,x,y+42,26,PAPER,bold=True)
    if gate:
        a.line([(right+25,y-4),(right+25,y-64)],RED,6)
        a.line([(right+25,y-54),(right-35,y-54)],RED,7,gate)
    pos=mix(right,left,t) if back else mix(left,right,t)
    bicycle(a,pos,y-21,t)


def counters(a,d,m):
    for x,value,word,col in [(236,d,'distance travelled',GOLD),(731,m,'elapsed since start',SEA)]:
        a.box(x,437,327,109,radius=12,fill='#233232',edge=DIM,stroke=2)
        a.text(word,x+163,464,24,col,bold=True)
        a.text(value,x+163,514,40,PAPER,bold=True)


def draw(a,n,c):
    txt(a,HEAD[n-1],71,70,48)
    a.line([(71,121),(1204,121)],DIM,2)
    if n==1:
        q=c.reveal('waits at a red signal',2.3)
        road(a,.45,1);counters(a,'6 km',f'{20+round(3*q)} min')
        txt(a,'A red signal',140,205,32,RED,q)
    elif n==2:
        p=c.reveal('After one hour',1.85);q=c.reveal('After two hours',1.85);t=(p+q)/2
        road(a,t);counters(a,f'{round(24*t)} km',f'{round(120*t)} min')
        txt(a,'12 km in each hour',138,207,37,GOLD,c.reveal('twelve kilometres per hour'))
    elif n==3:
        q=c.reveal('clock advances',2.8)
        road(a,1,1);counters(a,'24 km',f'{120+round(12*q)} min')
        txt(a,'Gate closed',140,200,39,RED,c.reveal('gate is closed'))
    elif n==4:
        q=c.reveal('One more hour',2.8)
        road(a,q,back=True);counters(a,f'{24+round(24*q)} km','? min')
        txt(a,'Return speed: 24 km/h',136,205,37,GOLD,c.reveal('twenty-four kilometres per hour'))
    elif n==5:
        for x,label,val,col,phrase in [(90,'Outward','120 min',GOLD,'one hundred and twenty minutes'),(490,'Wait','12 min',RED,'twelve minutes'),(883,'Home','60 min',SEA,'sixty minutes')]:
            t=c.reveal(phrase)
            a.box(x,218,280,146,fill='#263334',edge=col,stroke=3,opacity=t)
            txt(a,label,x+140,255,28,col,t,'center');txt(a,val,x+140,321,42,PAPER,t,'center')
        txt(a,'192 minutes = 3⅕ hours',639,467,50,PAPER,c.reveal('three and one fifth hours'),'center')
    elif n==6:
        txt(a,'Whole ride',144,184,32,SEA)
        txt(a,'48 km',434,279,54,GOLD);a.line([(397,328),(709,328)],PAPER,4)
        txt(a,'16/5 h',449,379,51,SEA,c.reveal('sixteen fifths'))
        txt(a,'= 15 km/h',777,337,54,PAPER,c.reveal('fifteen kilometres per hour'))
        txt(a,'15 × 16/5 = 48 km',640,522,40,GOLD,c.reveal('Check by multiplying'),'center')
    elif n==7:
        q=c.reveal('one hundred and eighty minutes')
        txt(a,'Deadline: 180 min',118,204,40,SEA,q)
        a.line([(145,372),(1115,372)],DIM,10)
        for frac,num,col in [(0,'0',PAPER),(120/180,'120',GOLD),(132/180,'132',RED),(1,'180',SEA)]:
            x=mix(145,1115,frac);a.dot(x,372,8,col);a.text(num,x,422 if num=='132' else 332,27,col,bold=True)
        txt(a,'How much time is left for 24 km?',640,532,36,PAPER,c.reveal('same twenty-four kilometres'),'center')
    else:
        txt(a,'Time left',109,200,32,SEA);txt(a,'180 − 132 = 48 min',109,273,47,PAPER)
        txt(a,'48 min = 4/5 h',689,272,43,GOLD,c.reveal('four fifths of an hour'))
        a.line([(110,352),(1163,352)],DIM,2)
        txt(a,'Return speed',109,411,32,SEA)
        txt(a,'24 km ÷ 4/5 h = 30 km/h',109,504,51,PAPER,c.reveal('thirty kilometres per hour'))


def poster(draw):return draw(2,1)
