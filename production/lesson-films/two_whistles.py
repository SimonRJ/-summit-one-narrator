"""A head-start lane and an opposite-direction oval with separate runner clocks."""
from fractions import Fraction
from math import cos,pi,sin
from stage import clamp,mix

BACKGROUND=('#302e46','#1e263a')
BRIDGE='Start a second clock when the chasing runner sets off. What gap has already opened? In the round-track puzzle, which clock does the question use for the second meeting?'
HEAD=('The first whistle','Run both stopwatches','Meet on the lane','Read the earlier clock','Two directions around a track','Find the first meeting','One more meeting','Check the two readings')
PAPER,GOLD,BLUE,CORAL,DIM='#f9f2eb','#f3c278','#91c6e7','#f4a28f','#70748b'


def check_maths():
    b=Fraction(20,7-4);assert b==Fraction(20,3) and 7*b==4*(5+b)==Fraction(140,3)
    assert [t for t in range(5,124) if (2*t+3*(t-5))%300==0]==[63,123]
    assert (2*123,3*118)==(246,354)


def txt(a,s,x,y,size=35,col=PAPER,q=1,align='left'):
    a.label(s,x,y,size,col,q,align=align,bold=True)


def runner(a,x,y,col,letter):
    a.dot(x,y,15,col);a.text(letter,x,y,19,'#222638',bold=True)


def lane(a,x_a,x_b):
    left,right=162,1097
    for y,who,col,metres in [(290,'A',GOLD,x_a),(375,'B',BLUE,x_b)]:
        a.line([(left,y),(right,y)],DIM,4)
        for k in range(0,51,10):
            x=mix(left,right,k/50);a.line([(x,y-7),(x,y+7)],DIM,2)
        runner(a,mix(left,right,metres/50),y,col,who)
    txt(a,'0 m',left,426,24,PAPER,1,'center'); txt(a,'50 m',right,426,24,PAPER,1,'center')


def track(a,first,second):
    def xy(u):
        u=-pi/2+2*pi*u
        return (365+206*cos(u),373+116*sin(u))
    for off,col in [(0,DIM),(-7,'#8b8191')]:
        pts=[]
        for j in range(101):
            x,y=xy(j/100);pts.append((x,y+off))
        a.line(pts,col,3)
    a.line([(365,238),(365,272)],PAPER,4)
    a.text('Start',365,209,25,PAPER,bold=True)
    for travel,col,lane_y,letter in [(first,GOLD,0,'A'),(-second,BLUE,-13,'B')]:
        x,y=xy(travel/300);runner(a,x,y+lane_y,col,letter)
    a.text('300 m per lap',365,372,31,PAPER,bold=True)


def draw(a,n,c):
    txt(a,HEAD[n-1],71,70,48);a.line([(71,121),(1205,121)],DIM,2)
    if n==1:
        q=c.reveal('waits five seconds',2.1);lane(a,20*q,0)
        txt(a,'Asha: 4 m/s',146,198,36,GOLD,c.reveal('four metres per second'))
        txt(a,'4 × 5 = 20 m ahead',640,526,43,GOLD,c.reveal('twenty metre lead'),'center')
    elif n==2:
        t=c.reveal('Over one more second',2);lane(a,20+4*t,7*t)
        txt(a,'Asha: 4 m/s',145,195,34,GOLD);txt(a,'Ben: 7 m/s',704,195,34,BLUE,c.reveal('seven metres per second'))
        txt(a,'The gap closes at 7 − 4 = 3 m/s',640,526,42,PAPER,c.reveal('gap shrinks'),'center')
    elif n==3:
        t=6*c.reveal('After six seconds',1.6)+(2/3)*c.reveal('another second',1)
        lane(a,20+4*t,7*t)
        txt(a,'Gap: 20 m',144,195,35,GOLD);txt(a,'Closing speed: 3 m/s',673,195,35,BLUE)
        txt(a,'Ben’s time = 20/3 s = 6⅔ s',640,534,43,PAPER,c.reveal('Ben runs for six'),'center')
    elif n==4:
        txt(a,'Asha’s watch',153,214,34,GOLD);txt(a,'Ben’s watch',734,214,34,BLUE)
        txt(a,'11⅔ s',156,326,56,PAPER,c.reveal('eleven and two thirds seconds'))
        txt(a,'6⅔ s',738,326,56,PAPER,c.reveal('five seconds earlier'))
        txt(a,'4 × 11⅔ = 7 × 6⅔ = 46⅔ m',640,491,47,GOLD,c.reveal('forty-six and two thirds metres'),'center')
    elif n==5:
        q=c.reveal('Ben waits five seconds',1.9);track(a,10*q,0)
        txt(a,'Asha clockwise: 2 m/s',666,242,34,GOLD,c.reveal('two metres per second'))
        txt(a,'Ben anticlockwise: 3 m/s',666,332,34,BLUE,c.reveal('other way'))
        txt(a,'10 m covered before Ben starts',644,477,31,PAPER,c.reveal('ten metres of the lap'))
    elif n==6:
        q=c.reveal('fifty-eight seconds',2.1);track(a,10+2*58*q,3*58*q)
        txt(a,'300 − 10 = 290 m',678,232,39,PAPER,c.reveal('ninety metres remain'))
        txt(a,'2 + 3 = 5 m/s',678,331,40,BLUE,c.reveal('five metres'))
        txt(a,'Ben 58 s  •  Asha 63 s',667,468,35,GOLD,c.reveal('sixty-three seconds'))
    elif n==7:
        q=c.reveal('sixty more seconds',2.3);track(a,126+120*q,174+180*q)
        txt(a,'One more full lap',679,232,37,PAPER,c.reveal('one whole lap'))
        txt(a,'300 m ÷ 5 m/s = 60 s',644,385,39,GOLD,c.reveal('sixty more seconds'))
    else:
        track(a,246,354)
        txt(a,'Asha: 63 + 60 = 123 s',636,216,35,GOLD,c.reveal('twenty-three seconds'))
        txt(a,'Ben: 123 − 5 = 118 s',636,311,35,BLUE,c.reveal('eighteen seconds'))
        txt(a,'246 + 354 = 600 m',636,426,39,PAPER,c.reveal('six hundred metres'))
        txt(a,'Two complete laps',636,504,32,GOLD,c.reveal('exactly two laps'))


def poster(draw):return draw(2,1)
