"""S037. Position the walkers and runners from their actual speeds; race times use one start clock."""
from math import sin,cos,pi,atan2,dist,isclose
from captioned_film import cue,mix
ID='S037'
ORIGINAL='6ca19b6243de9773271adf5fd352e4323a292ecb4242a977b69009fb48fd34eb'
START=(0,14.52,30.52,45.85,56.10,70.15,91.74,113.14,136.65,153.93,168.81)
POSTER=144.5
PAPER='#f1f4ed';INK='#183b35';SUB='#45615a';TEAL='#007e77';ROSE='#b84243';GOLD='#9d621e';TURF='#d9e6d7';TRACK='#c68a6f';CHALK='#faf6e8';DASH='#6f8a7f'
def title(c,s):c.text(s,60,60,41,INK,'lm',True)
def note(c,s,x,y,size=32,col=INK):c.text(s,x,y,size,col,'lm',True)
def arrow(c,a,b,col,w=4,head=13):
    c.line([a,b],col,w);ang=atan2(b[1]-a[1],b[0]-a[0])
    c.poly([b,*[(b[0]-head*cos(ang+j),b[1]-head*sin(ang+j)) for j in (-.46,.46)]],col,None)
def person(c,x,foot,name,col,direction,clock,pose=1,scale=1):
    k=scale;d=direction
    # Coordinates follow each runner's centre. Different bobbing arm and leg poses make direction readable.
    stride=sin(clock*5)*pose
    def xy(i,j):return (x+d*i*k,foot+j*k)
    c.dot(*xy(8,-87),12*k,col)
    c.line([xy(5,-71),xy(-4,-43)],col,10*k)
    c.line([xy(2,-65),xy(-7-11*stride,-48),xy(5-18*stride,-45)],col,6*k)
    c.line([xy(3,-65),xy(11+11*stride,-54),xy(17+14*stride,-66)],col,5*k)
    for sign in (-1,1):
        c.line([xy(-4,-43),xy(sign*17*stride,-21),xy(sign*26*stride,0),xy(sign*26*stride+8,0)],col,6*k)
    c.text(name,x,foot-120*k,21*k,col,bold=True)
def strip(c,x,foot,w,span):
    c.rect(x-26,foot+8,w+52,79,TURF)
    c.line([(x,foot+7),(x+w,foot+7)],INK,2.5)
    for v in range(0,int(span)+1,4 if span<=32 else 5):
        X=x+w*v/span
        c.line([(X,foot+7),(X,foot+17)],SUB,2)
        if v%(8 if span<=32 else 10)==0:c.text(str(v),X,foot+36,20,SUB)
    c.text('metres',x+w,foot+66,19,SUB,'rm')
def gap(c,xa,xb,y,txt):
    if abs(xb-xa)>7:
        c.line([(xa,y-8),(xa,y+3),(xb,y+3),(xb,y-8)],GOLD,3)
    c.text(txt,(xa+xb)/2,y+30,26,GOLD,bold=True)
def race(c,clock,opposite=True,show_gap=True):
    ox,w=117,606;span=32 if opposite else 55;foot=342
    strip(c,ox,foot,w,span)
    if opposite:
        a,b=3*clock,32-5*clock;direction=-1;shared=clock
    else:
        shared=max(0,clock-5);a,b=4*clock,7*shared;direction=1
    xa=ox+w*a/span;xb=ox+w*b/span
    # Keep each figure attached to its exact mark when the two reach the same point.
    close=abs(xa-xb)<32
    if close:
        c.line([(xa,foot),(xa,foot-57)],TEAL,1.5)
        person(c,xa,foot-52,'A',TEAL,1,clock,1,.77)
        person(c,xb,foot,'B',ROSE,direction,shared,1,.77)
    else:
        person(c,xa,foot,'A',TEAL,1,clock)
        person(c,xb,foot,'B',ROSE,direction,shared,1 if shared else 0)
    if not close:
        arrow(c,(xa-15,foot-147),(xa+22,foot-147),TEAL,3,9)
        if opposite or shared>0:arrow(c,(xb-15*direction,foot-147),(xb+22*direction,foot-147),ROSE,3,9)
    if show_gap:
        d=abs(b-a);gap(c,xa,xb,445,(str(round(d)) if abs(round(d)-d)<.01 else f'{d:.1f}')+' m gap')
def clocklabel(c,s):c.text(s,419,142,31,INK,bold=True)
def instant(v):return str(round(v)) if abs(v-round(v))<.025 else f'{v:.1f}'
def intro(c,t):
    title(c,'How quickly does the gap close?')
    if t<8.3:
        v=3*cue(t,2.2,4.4);race(c,v)
        note(c,'Toward each other',770,247,34)
        if t>=4.2:note(c,'Add the speeds.',770,352,34,TEAL)
    else:
        v=5+4*cue(t,8.5,4.9);race(c,v,False)
        note(c,'Same-direction chase',770,247,31)
        if t>=10.7:note(c,'Subtract the speeds.',770,352,31,ROSE)
def circpoint(distance,r=185):
    a=-pi/2+2*pi*distance/300
    return 394+r*cos(a),352+r*sin(a)
def positions(t):return 2*t,-3*max(0,t-5)
def track(c,t,trail=False):
    X,Y=394,352;r=185
    c.dot(X,Y,r+19,TRACK);c.dot(X,Y,r-19,TURF)
    for rr in (r+14,r-14):
        c.line([circpoint(k*300/145,rr) for k in range(146)],CHALK,2)
    for k in range(0,300,25):
        c.line([circpoint(k,r-16),circpoint(k,r+16)],CHALK,2 if k%75 else 4)
    c.line([circpoint(0,r-21),circpoint(0,r+22)],INK,4)
    c.text('START',394,121,23,INK,bold=True)
    a,b=positions(t)
    if trail:
        for dist_run,col,roff in [(a,TEAL,-7),(b,ROSE,7)]:
            n=max(2,int(abs(dist_run)))
            c.line([circpoint(dist_run*i/n,r+roff) for i in range(n+1)],col,3)
    A=circpoint(a);B=circpoint(b)
    c.dot(*A,12,TEAL);c.dot(*B,8,ROSE)
    # The pointers terminate on the centre line; at a meeting both colours sit on the same mark.
    for pt,dx,dy,label,col in ((A,-31,-18,'A',TEAL),(B,31,17,'B',ROSE)):
        px,py=pt;c.line([(px,py),(px+dx*.72,py+dy*.74)],col,1.8)
        c.text(label,px+dx,py+dy,23,col,bold=True)
    c.text('Race clock',X,Y-22,25,SUB)
    c.text(instant(t)+' s',X,Y+22,38,INK,bold=True)
def applications(c,t):
    title(c,'A delayed start changes the initial gap')
    track(c,5*cue(t,15.2,3.1)+9*cue(t,23.0,3.8),True)
    note(c,'A leaves first.',742,235,35,TEAL)
    if t>=22:note(c,'B starts from the same mark.',719,331,29,ROSE)
    if t>=26:note(c,'One lap brings them together.',712,441,30)
def basic(c,t):
    title(c,'Two walkers start 32 metres apart')
    timer=cue(t,39.6,2.9);race(c,timer);clocklabel(c,'Time   '+instant(timer)+' s')
    note(c,'A   3 m/s',789,208,37,TEAL)
    if t>=34:note(c,'B   5 m/s',789,290,37,ROSE)
    if t>=37.2:note(c,'When do they meet?',759,416,32)
def basic_answer(c,t):
    title(c,'Each second closes 3 + 5 metres')
    v=1+3*cue(t,48.1,5.4);race(c,v);clocklabel(c,'Time   '+instant(v)+' s')
    note(c,'Gap closes at 8 m/s.',766,234,32,TEAL)
    if t>=51.5:note(c,'32 ÷ 8',766,327,41)
    if t>=53.6:note(c,'= 4 seconds',766,423,43,GOLD)
def chase(c,t):
    title(c,'Give the first runner a five-second head start')
    v=5*cue(t,56.5,5.4);race(c,v,False);clocklabel(c,'From A’s start   '+instant(v)+' s')
    note(c,'A   4 m/s',783,208,37,TEAL)
    if t>=58.5:note(c,'B waits 5 seconds.',762,293,32,ROSE)
    if t>=60.8:note(c,'Then B runs at 7 m/s.',762,364,31,ROSE)
    if t>=63.8:note(c,'Time from B’s start?',761,461,33)
def chase_answer(c,t):
    title(c,'The faster runner gains 3 metres each second')
    shared=20/3*cue(t,76.6,6.5)
    elapsed=5*cue(t,70.25,2.25)+shared
    race(c,elapsed,False)
    clocklabel(c,'From B’s start   '+('6⅔' if shared>=20/3-.0001 else instant(shared))+' s')
    if t>=70.2:note(c,'Head start   4 × 5 = 20 m',751,192,31,TEAL)
    if t>=76.65:note(c,'7 − 4 = 3 m/s',752,288,37,ROSE)
    if t>=82.5:note(c,'20 ÷ 3 = 6⅔ s',752,392,39)
    if t>=85.3:note(c,'after B starts',755,457,27,GOLD)
def problem(c,t):
    title(c,'When is their second meeting on the 300 m track?')
    v=5*cue(t,94.5,3.0)+9*cue(t,100.2,3.3)
    track(c,v,True)
    note(c,'A   2 m/s clockwise',728,211,32,TEAL)
    if t>=97.8:note(c,'B waits five seconds.',728,293,31)
    if t>=100.3:note(c,'B   3 m/s anticlockwise',728,367,30,ROSE)
    if t>=106.1:note(c,'Time from A’s start?',728,478,35)
def two_meets(c,t):
    title(c,'One more full lap gives one more meeting')
    v=5+58*cue(t,122.8,4.8)+60*cue(t,130.0,3.3)
    track(c,v,True)
    note(c,'At 5 s, A is 10 m ahead.',714,172,31,TEAL)
    if t>=119.1:note(c,'300 − 10 = 290 m',714,239,31)
    if t>=123.0:note(c,'Closing rate   2 + 3 = 5 m/s',714,305,29)
    if t>=126.0:note(c,'First meet   290 ÷ 5 = 58 s',714,375,30,ROSE)
    if t>=128.5:note(c,'from B’s start',715,414,23,SUB)
    if t>=131.0:note(c,'Next meet   300 ÷ 5 = 60 s later',703,501,26,GOLD)
def check(c,t):
    title(c,'At the second meeting, check both distances')
    # Rewind explicitly before replaying both meetings.
    if t<146.1:v=123
    else:v=63+60*cue(t,148.1,3.0)
    track(c,v,True)
    note(c,'5 + 58 + 60 = 123 s',715,174,36)
    if t>=139.4:note(c,'A   2 × 123 = 246 m',715,258,32,TEAL)
    if t>=141.5:note(c,'B   3 × 118 = 354 m',715,328,32,ROSE)
    if t>=143.6:note(c,'246 + 354 = 600 m',715,411,34)
    if t>=146.1:note(c,'Replay   first to second meeting',698,505,26,GOLD)
def mistakes(c,t):
    title(c,'Choose the rate that follows the arrows')
    if t<161.4:
        race(c,6+3.4*cue(t,154.1,3.0),False)
        note(c,'Chasing in one direction',755,240,30)
        note(c,'7 − 4 = 3 m/s',755,338,37,ROSE)
    else:
        track(c,5+5*cue(t,161.7,2.6))
        note(c,'Whose clock started first?',726,245,31)
        note(c,'Elapsed from A = 5 s',726,340,31,TEAL)
        note(c,'+ elapsed from B.',726,398,31,ROSE)
def recap(c,t):
    title(c,'Use the changing gap to choose your calculation')
    if t<175.5:
        race(c,1.45*cue(t,169,4.1))
        note(c,'Toward each other',762,234,33,TEAL)
        note(c,'Both distances close the gap.',738,342,27)
    else:
        track(c,63+60*cue(t,175.8,3.2),True)
        note(c,'On the loop',758,200,34)
        note(c,'One lap between meetings.',726,298,30,GOLD)
        if t>=179.5:note(c,'Check  246 + 354 = 600 m.',720,422,29)
SCENES=(intro,applications,basic,basic_answer,chase,chase_answer,problem,two_meets,check,mistakes,recap)
def verify():
    assert 3*4==32-5*4==12
    assert isclose(4*(5+20/3),7*(20/3))
    assert positions(5)==(10,0) and positions(63)==(126,-174) and positions(123)==(246,-354)
    assert all(dist(circpoint(a),circpoint(b))<1e-8 for a,b in map(positions,(63,123)))
    assert all(dist(circpoint(a),circpoint(b))>.5 for a,b in map(positions,[*range(5,63),*range(64,123)]))
