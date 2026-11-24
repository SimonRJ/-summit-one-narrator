"""A speed-time tape keeps the widths of moving and stationary intervals."""
from fractions import Fraction
from stage import clamp,mix
BACKGROUND=('#2a353a','#1b2b31')
BRIDGE='On the sorter’s speed tape, the fast and slow strips have different widths. What do the width, height and area of each rectangle measure?'
HEAD=('Read a speed tape','Two speeds for equal times','Flatten the two strips','The damaged printout','Start with the slow strip','Restore the missing width','A scanner pauses the belt','Choose the clock in the question')
PAPER,GOLD,SEA,BLUE,PINK,DIM='#fff0dc','#f2bf70','#8dd5be','#9dbde7','#efa8b7','#627b80'


def check_maths():
    assert (10*30+10*10)/20==20
    assert [t for t in range(51) if 30*t+10*(50-t)==900]==[20]
    assert Fraction(900,50)==18 and Fraction(900,60)==15


def label(a,s,x,y,size=33,col=PAPER,t=1,align='left'):
    a.label(s,x,y,size,col,t,align=align,bold=True)


def tape(a,blocks,total,mean=0):
    x0,x1,y0,dy=154,745,491,7.7
    a.line([(x0,210),(x0,y0),(x1+16,y0)],PAPER,3)
    for speed in (0,10,20,30):
        y=y0-speed*dy
        a.line([(x0-6,y),(x0,y)],PAPER,2);a.text(str(speed),x0-18,y,23,PAPER,align='right',bold=True)
    label(a,'cm/s',84,185,22,SEA)
    time=0
    for duration,speed,col in blocks:
        if duration<=0:continue
        x=x0+time/total*(x1-x0);w=duration/total*(x1-x0);time+=duration
        if speed:
            a.box(x,y0-speed*dy,w,speed*dy,radius=0,fill=col,opacity=.70)
            a.line([(x,y0-speed*dy),(x+w,y0-speed*dy)],col,4)
        else:a.line([(x,y0-3),(x+w,y0-3)],col,6)
    if mean:a.dashed((x0,y0-mean*dy),(x1,y0-mean*dy),PAPER,3,9,6)
    for t in sorted(set([0,total]+[sum(x[0] for x in blocks[:i+1]) for i in range(len(blocks))])):
        if round(t)!=t or t<0:continue
        x=x0+t/total*(x1-x0); a.text(str(round(t)),x,y0+27,24,PAPER,bold=True)
    label(a,'time in seconds',x1,y0+66,22,SEA,1,'right')


def draw(a,n,c):
    label(a,HEAD[n-1],72,70,45);a.line([(72,120),(1205,120)],DIM,2)
    if n==1:
        p=c.reveal('ten seconds wide',1.2);tape(a,[(10*p,30,GOLD)],10)
        label(a,'Width = 10 s',822,259,34,SEA,p);label(a,'Height = 30 cm/s',809,351,32,GOLD,c.reveal('thirty centimetres per second'))
        label(a,'Area = 300 cm',817,456,35,PAPER,c.reveal('three hundred centimetres'))
    elif n==2:
        q=c.reveal('ten more seconds',1.2);tape(a,[(10,30,GOLD),(10*q,10,BLUE)],20)
        label(a,'Fast: 300 cm',824,269,35,GOLD,c.reveal('three hundred centimetres'))
        label(a,'Slow: 100 cm',823,378,35,BLUE,c.reveal('one hundred centimetres'))
    elif n==3:
        p=c.reveal('Slide part of the taller',2);tape(a,[(10,30-10*p,GOLD),(10,10+10*p,BLUE)],20,20)
        label(a,'Area = 400 cm',812,265,34,PAPER,c.reveal('four hundred centimetres'))
        label(a,'Width = 20 s',812,367,34,SEA,c.reveal('width is still'))
        label(a,'400 ÷ 20 = 20 cm/s',787,474,31,GOLD,c.reveal('twenty centimetres per second'))
    elif n==4:
        tape(a,[],50,18);label(a,'50 seconds',831,250,36,SEA)
        label(a,'Average 18 cm/s',808,341,32,GOLD,c.reveal('eighteen centimetres'))
        label(a,'Fast for how long?',807,466,33,PINK,c.reveal('faster speed'))
    elif n==5:
        tape(a,[(50,10,BLUE)],50,18)
        label(a,'Target 900 cm',815,241,34,GOLD,c.reveal('nine hundred centimetres'))
        label(a,'Slow base 500 cm',812,350,30,BLUE,c.reveal('five hundred centimetres'))
        label(a,'Extra 400 cm',813,471,37,PINK,c.reveal('four hundred centimetres'))
    elif n==6:
        p=c.reveal('twenty seconds',1.2);tape(a,[(20*p,30,GOLD),(50-20*p,10,BLUE)],50,18)
        label(a,'Fast: 20 × 30 = 600',789,279,29,GOLD,c.reveal('six hundred centimetres'))
        label(a,'Slow: 30 × 10 = 300',786,380,29,BLUE,c.reveal('three hundred from'))
        label(a,'Sum: 900 cm',814,484,35,PAPER,c.reveal('give nine hundred'))
    elif n==7:
        p=c.reveal('ten extra seconds',1.2);tape(a,[(20,30,GOLD),(30,10,BLUE),(10*p,0,PINK)],60)
        label(a,'Scanner: 0 cm/s',809,297,35,PINK,p)
        label(a,'Which clock?',827,445,36,PAPER,c.reveal('whole parcel trip'))
    else:
        tape(a,[(20,30,GOLD),(30,10,BLUE),(10,0,PINK)],60,15)
        label(a,'Trip: 60 seconds',802,240,32,SEA,c.reveal('sixty seconds'))
        label(a,'Distance: 900 cm',804,346,32,PAPER,c.reveal('nine hundred centimetres'))
        label(a,'900 ÷ 60 = 15 cm/s',787,464,31,GOLD,c.reveal('fifteen centimetres per second'))


def poster(draw):return draw(4,1)
