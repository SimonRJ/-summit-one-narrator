"""S030. Follow a measured trail and superimpose two independently timed log strips."""
from math import hypot,lcm,sin,cos,pi
from captioned_film import cue,mix,font
ID='S030';ORIGINAL='ca8eab12c44a639ca5e7a31a1c13798e28564f39db03539667ddff0cf3a25d88';START=(0,15.16,32.6,45.38,57.86,75.11,95.26,115.55,140.98,157.46,173.94);POSTER=134.9
PAPER='#152a36';INK='#fff0cf';GREEN='#85ddb2';AMBER='#f4ba6b';BLUE='#8dc7ed';MUTED='#bbcbcc';RIM='#47616c';DARK='#172e37';DIM='#304955'

def title(c,s):
    size=42
    while font(round(size*c.scale),True).getlength(s)>1150*c.scale:size-=1
    c.text(s,63,65,size,INK,'lm',True)
def text(c,s,x,y,size=32,colour=INK):c.text(s,x,y,size,colour,'lm',True)
def lens(c,x,y,col,mark=True,r=19):
    c.dot(x,y,r+4,RIM);c.dot(x,y,r,col if mark else DARK)
    if mark:c.dot(x-r*.25,y-r*.26,r*.17,INK)

def timer(c,x,y,secs,r=88):
    c.dot(x,y,r+4,RIM);c.dot(x,y,r,DARK)
    for i in range(60):
        a=i*pi/30-pi/2;long=i%5==0
        rr=r-7 if long else r-3;c.line([(x+rr*cos(a),y+rr*sin(a)),(x+r*cos(a),y+r*sin(a))],MUTED if long else RIM,2 if long else 1)
    a=(secs%60)*pi/30-pi/2;c.line([(x,y),(x+(r-12)*cos(a),y+(r-12)*sin(a))],AMBER,4);c.dot(x,y,6,INK)
    c.text(f'{int(secs)//60}:{int(secs)%60:02d}',x,y+r+40,30,INK,bold=True)
HOME=(155.,426.);DIRS=((.8,-.6),(.8,.6),(1.,0.));U=.385

def pos(metres):
    x,y=HOME
    for length,(a,b) in zip((1000.,1000.,350.),DIRS):
        travel=min(length,max(0,metres));x+=a*travel*U;y+=b*travel*U;metres-=travel
    return x,y

def trail(c,metres,labels,converted):
    previous=0
    for i,end in enumerate((1000,2000,2350)):
        a,b=pos(previous),pos(end);c.line([a,b],RIM,12)
        if metres>previous:c.line([a,pos(min(end,metres))],(GREEN,BLUE,AMBER)[i],9)
        for tick in range(previous+100,end,100):
            xx,yy=pos(tick);dx,dy=DIRS[i];c.line([(xx-dy*4,yy+dx*4),(xx+dy*4,yy-dx*4)],MUTED,1)
        c.dot(*a,7,INK);c.dot(*b,7,INK)
        if i<labels:
            mx,my=(a[0]+b[0])/2,(a[1]+b[1])/2;txt=('1,000 m' if converted else '1 km') if i<2 else '350 m'
            c.text(txt,mx,my-(38 if i<2 else 46),28,(GREEN,BLUE,AMBER)[i],bold=True)
        previous=end
    c.dot(*pos(metres),11,INK);c.dot(*pos(metres),6,AMBER)
    c.text('START',HOME[0],HOME[1]+39,21,MUTED,bold=True)

def intro(c,t):
    title(c,'Which unit? Which instants count?')
    if t<9.2:
        timer(c,268,328,60*cue(t,.6,5.7));text(c,'60 seconds',569,269,40,AMBER)
        if t>=5.2:text(c,'= 1 minute',568,353,40)
    else:
        text(c,'Start',164,196,30);text(c,'Finish',879,196,30)
        c.line([(198,327),(969,327)],RIM,5)
        for i in range(7):lens(c,198+i*128,327,GREEN,i>0 and i/6<=cue(t,9.2,3.4),13)
        if t>=11.8:text(c,'Decide which endpoints are included.',266,463,34,AMBER)

def uses(c,t):
    title(c,'Read the unit beside each number')
    if t<24.8:
        timer(c,258,328,60*cue(t,15.7,4.3));text(c,'1 minute = 60 seconds',568,252,34,AMBER)
        if t>=18.6:text(c,'1 kilometre = 1,000 metres',568,357,30,GREEN)
    else:
        text(c,'Signal A',142,235,30,BLUE);text(c,'Signal B',142,355,30,AMBER)
        for i in range(7):
            if i%2==0:lens(c,404+100*i,235,BLUE,i<=6*cue(t,25.2,2.7),16)
            if i%3==0:lens(c,404+100*i,355,AMBER,i<=6*cue(t,27.0,2.7),16)
        if t>=29:text(c,'Both signals share the start and the finish here.',159,487,30,GREEN)

def basic(c,t):
    title(c,'How many metres long is the trail?')
    m=2000*cue(t,32.6,2.2)+350*cue(t,34.9,.9);trail(c,m,3,False)
    if t>=36.8:text(c,'2 km + 350 m',343,523,40)

def convert(c,t):
    title(c,'Measure every section in metres');m=1000*cue(t,45.38,1.3)+1000*cue(t,48.8,1.5)+350*cue(t,51.6,1.1);trail(c,m,3,True)
    if t>=51.6:text(c,'2,000 m + 350 m',190,534,36)
    if t>=54.2:text(c,'= 2,350 m',641,534,38,GREEN)

def one_strip(c,moment,question=False):
    x=146;y=357;dx=75;c.line([(x,y),(x+12*dx,y)],RIM,4)
    for j in range(13):
        X=x+j*dx;c.line([(X,y-8),(X,y+8)],MUTED,2)
        if j>0 and j*35<=moment:lens(c,X,y,AMBER,True,11)
        if j in (0,1,6,12):c.text(str(j*35),X,y+43,25,MUTED)
    c.text('elapsed seconds',x+12*dx,y-75,22,MUTED,'rm')
    X=x+moment/35*dx;c.poly([(X-7,y-51),(X+7,y-51),(X,y-30)],GREEN,None)
    if not question:text(c,'Recorded flashes   '+str(int(moment//35)),203,489,37,AMBER)

def sensor(c,t):
    title(c,'One sensor. One flash after every 35 seconds.')
    moment=35*cue(t,58.2,3.9);one_strip(c,moment,True)
    text(c,'No flash at 0',145,193,35)
    if t>=60.4:text(c,'First flash at 35 s',644,193,32,AMBER)
    if t>=68.8:text(c,'7 minutes × 60 seconds/minute',245,513,33,GREEN)

def sensor_count(c,t):
    title(c,'Count the completed 35-second intervals')
    moment=420*cue(t,78.6,6.5);one_strip(c,moment)
    text(c,'7 min = 420 s',140,194,37,BLUE)
    if t>=83:text(c,'420 ÷ 35 = 12',677,194,37,GREEN)
    if t>=90:text(c,'0 s is just the starting point.',241,558,27,MUTED)

A=tuple(range(0,841,70));B=tuple(range(0,841,105));BOTH=tuple(sorted(set(A)&set(B)));UNION=tuple(sorted(set(A)|set(B)))

def joint(c,aa,bb,links,union=False):
    x=lambda v:236+v*1.035
    for y,ls,colour,label,until in [(234,A,BLUE,'70 s',aa),(334,B,AMBER,'105 s',bb)]:
        text(c,label,83,y,27,colour);c.line([(x(0),y),(x(840),y)],RIM,3)
        for v in ls:
            if v<=until:lens(c,x(v),y,colour,True,9)
    for v in BOTH:
        if v<=links:
            c.line([(x(v),251),(x(v),317)],GREEN,3);c.dot(x(v),284,5,GREEN)
            c.text(str(v),x(v),386,21,GREEN,bold=True)
    if union:
        c.line([(x(0),460),(x(840),460)],RIM,3);text(c,'Either',81,460,25)
        for v in UNION:lens(c,x(v),460,GREEN if v in BOTH else BLUE if v in A else AMBER,True,9)

def question(c,t):
    title(c,'When does either of the two signals flash?')
    aa=840*cue(t,98,6.2);bb=840*cue(t,100.4,6.2);joint(c,aa,bb,0 if t<109.4 else 840*cue(t,109.4,3))
    text(c,'Fourteen minutes, including both endpoints',164,492,31)

def overlap(c,t):
    title(c,'Line up both schedules in the same 840 seconds')
    aa=840*cue(t,118.6,3);bb=840*cue(t,123.2,2.9) if t>=123.2 else -1;links=840*cue(t,126.8,5.1) if t>=126.8 else -1
    joint(c,aa,bb,links,t>=135.6);text(c,'0–840 s',151,147,29,MUTED)
    if t>=121.6:text(c,'A: 13',355,147,28,BLUE)
    if t>=123.2:text(c,'B: 9',571,147,28,AMBER)
    if t>=132.4:text(c,'Both: 5',789,147,28,GREEN)
    if t>=135.6:text(c,'13 + 9 − 5',482,539,35)

def distinct(c,t):
    title(c,'The two signals coincide every 210 seconds');joint(c,840,840,840*cue(t,141,3.8),t>=150.2)
    if t<150.2:text(c,'3 × 70 s  =  2 × 105 s  =  210 s',223,504,34,GREEN)
    else:text(c,'13 + 9 − 5 = 17 distinct instants',278,548,35,GREEN)

def mistakes(c,t):
    title(c,'An interval is the space between two instants')
    if t<166:
        timer(c,268,318,60*cue(t,157.5,3.2));text(c,'1 min = 60 s',581,272,44,AMBER)
        if t>=160.8:text(c,'7 min = 420 s',581,373,36)
    else:
        c.line([(249,324),(964,324)],RIM,5)
        for j in range(4):
            X=249+j*238;lens(c,X,324,GREEN,j>0 or t>=170.8,17);c.text(str(j*35)+' s',X,378,26,MUTED)
        text(c,'Three intervals',152,496,33)
        if t>=170.8:text(c,'Four events if zero counts',555,496,31,GREEN)

def finish(c,t):
    title(c,'Which endpoints belong to the count?')
    if t<180.8:
        one_strip(c,35*cue(t,176.4,2.0),True);text(c,'First interval: 0 to 35 seconds',145,189,34)
    else:
        joint(c,840,840,840*cue(t,180.9,3.3),t>=185.2)
        if t>=185.2:text(c,'Both 0 and 840 are shared events.',262,536,33,GREEN)
SCENES=(intro,uses,basic,convert,sensor,sensor_count,question,overlap,distinct,mistakes,finish)
def verify():
    assert (len(A),len(B),len(BOTH),len(UNION))==(13,9,5,17) and lcm(70,105)==210
    assert BOTH==(0,210,420,630,840) and len(range(35,421,35))==12 and 420%35==0
    for a,b in ((0,1000),(1000,2000),(2000,2350)):assert abs(hypot(*(v-w for v,w in zip(pos(a),pos(b))))/U-(b-a))<1e-8
