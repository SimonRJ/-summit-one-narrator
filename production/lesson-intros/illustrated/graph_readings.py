"""S045: trace survey readings, compare unequal time intervals, and price whole visits."""
from fractions import Fraction
from captioned_film import cue, mix
ID='S045'
ORIGINAL='f3179ce53caca59bac0aa1858b0ceff0d10d40209decf5cb2abc7e181a8c7b1d'
START=(0,15.96,34.68,51.45,62.65,80.54,98.45,114.9,136.81,148.65,162.57)
POSTER=128
PAPER='#f7f3e8';INK='#1d3346';FAINT='#d9ded7';SOFT='#536971';GREEN='#007771'
RED='#ad3e49';BLUE='#355caa';YELLOW='#f1c879';MILK='#fffdf5';MINT='#d8ece0'
DATA=((0,0),(2,4),(5,22),(9,38))
HOURLY=((1,1),(2,5),(3,12),(4,18))

def label(c,s,x,y,size=28,col=INK,anchor='mm'):
    c.text(s,x,y,size,col,anchor,True)

def title(c,s):label(c,s,61,64,41,INK,'lm')

class Plot:
    def __init__(self,c,xmax,ymax,xstep,ystep,xname,yname,box=(142,490,635,310)):
        self.c=c;self.x,self.y,self.width,self.height=box;self.xmax=xmax;self.ymax=ymax
        for x in range(0,xmax+1,xstep):
            xx,yy=self.pt(x,0);c.line([(xx,yy),(xx,yy-self.height)],FAINT,2)
            c.line([(xx,yy),(xx,yy+6)],INK,2);label(c,x,xx,yy+25,21,SOFT)
        for y in range(0,ymax+1,ystep):
            xx,yy=self.pt(0,y);c.line([(xx,yy),(xx+self.width,yy)],FAINT,2)
            label(c,y,xx-15,yy,21,SOFT,'rm')
        c.line([(self.x,self.y-self.height),(self.x,self.y),(self.x+self.width,self.y)],INK,3)
        label(c,yname,self.x,self.y-self.height-29,24,INK,'lm')
        label(c,xname,self.x+self.width*.5,self.y+62,24,INK)
    def pt(self,x,y):
        return self.x+self.width*x/self.xmax,self.y-self.height*y/self.ymax
    def segment(self,a,b,p,col,w=4):
        if p<=0:return
        a,b=self.pt(*a),self.pt(*b)
        self.c.line([a,(mix(a[0],b[0],p),mix(a[1],b[1],p))],col,w)
    def dot(self,x,y,col,r=8):
        self.c.dot(*self.pt(x,y),r,col)
    def guide(self,x,y,p):
        if p<=0:return
        left=min(1,2*p);up=min(1,max(0,2*p-1))
        self.segment((x,0),(x,y),left,RED,3)
        self.segment((x,y),(0,y),up,RED,3)
        if up:self.dot(x,y,RED,9)

def trace(c,p,data,phase,ink=GREEN):
    for i,(x,y) in enumerate(data):
        if phase<i:break
        if i+1<len(data):p.segment((x,y),data[i+1],min(1,phase-i),ink,4)
        p.dot(x,y,ink)

def note(c,s,x=844,y=225,size=30,col=INK):
    label(c,s,x,y,size,col,'lm')

def readings():
    return [(0,0),(1,3),(2,6),(3,9),(4,12)]

def opening(c,t):
    title(c,'A point has two readings')
    p=Plot(c,4,12,1,3,'hours','count')
    trace(c,p,readings(),4*cue(t,.65,2.4));p.guide(3,9,cue(t,3.05,1.45))
    if t>=4.4:note(c,'3 hours',y=227,col=RED);note(c,'9 counted',y=289,col=GREEN)
    if t>=8.2:
        p.segment((1,3),(3,3),cue(t,8.25,1.25),BLUE);p.segment((3,3),(3,9),cue(t,9.5,1.1),RED)
        note(c,'Rise   9 − 3 = 6',y=378,size=27,col=RED)
    if t>=11:note(c,'6 over 2 hours',y=443,size=27,col=BLUE)
    if t>=13.4:note(c,'3 per hour',y=512,col=GREEN)

def exams(c,t):
    title(c,'Follow the same reading from table to graph' if t<26 else 'At a crossing, both prices agree')
    if t>=26:
        p=Plot(c,4,12,1,3,'visits','dollars')
        a=[(x,4+x) for x in range(5)];b=[(x,3*x) for x in range(5)]
        z=4*cue(t,26.1,2.5);trace(c,p,a,z,BLUE);trace(c,p,b,z,GREEN)
        if t>=29.2:p.guide(2,6,cue(t,29.2,1.4));note(c,'2 visits, $6',y=290,col=RED)
        if t>=31.4:note(c,'Next visit',y=375);note(c,'$7 versus $9',y=440,col=GREEN)
    else:
        p=Plot(c,4,12,1,3,'hours','count');trace(c,p,readings(),4)
        for i in range(1,5):
            yy=204+i*64
            if i==3 and t>=20:c.rect(844,yy-25,291,49,MINT)
            label(c,i,900,yy,28);label(c,i*3,1070,yy,28,GREEN)
        label(c,'hour',900,190,24);label(c,'count',1070,190,24)
        p.guide(3,9,cue(t,19.8,2.0))

def hour_scene(c,t,solved):
    title(c,'How much was added between hour 2 and hour 4?')
    values=(1,5,12,18);cols=(222,455,688,921)
    for i,(n,x) in enumerate(zip(values,cols)):
        c.line([(x-83,425),(x+83,425)],SOFT,2)
        show=1 if solved else cue(t,38.2+i*.43,1.2)
        h=n*12*show
        if h:c.rect(x-43,425-h,86,h,GREEN if i in (1,3) and (solved or t>=41.2) else '#789b9b')
        label(c,'hour '+str(i+1),x,469,26)
        if show>.85:label(c,n,x,400-h,31,GREEN)
    if solved:
        q=cue(t,53.6,1.3);a,b=425-5*12,425-18*12
        c.line([(984,a),(1035,a)],BLUE,2)
        if q:c.line([(1033,a),(1033,mix(a,b,q))],RED,5)
        if q==1:c.line([(986,b),(1035,b)],BLUE,2)
        if t>=58.2:label(c,'18 − 5',1128,273,29,RED)
        if t>=60.8:label(c,'= 13',1128,325,33,RED)
    elif t>=41.2:
        c.line([(455,510),(455,526),(921,526),(921,510)],RED,3)
        label(c,'compare these readings',690,566,26,RED)

def question(c,t):hour_scene(c,t,False)
def answer(c,t):hour_scene(c,t,True)

def rates(c,t,solved):
    title(c,'Which stretch has the fastest increase?')
    p=Plot(c,9,40,1,10,'minutes','total count')
    trace(c,p,DATA,3 if solved else 3*cue(t,66.9,4.1))
    slopes=(2,6,4);colours=(BLUE,RED,GREEN)
    if solved:
        for i,((a,b),(x,y)) in enumerate(zip(DATA,DATA[1:])):
            r=cue(t,(83.4,87.45,89.55)[i],1.35)
            if r:
                p.segment((a,b),(x,b),min(1,2*r),colours[i],4)
                p.segment((x,b),(x,y),max(0,2*r-1),colours[i],4)
                yy=220+i*80
                note(c,f'{y-b} ÷ {x-a} = {slopes[i]}/min',y=yy,size=27,col=colours[i])
        if t>=92.8:
            p.segment(DATA[1],DATA[2],cue(t,92.8,1.35),RED,9)
            note(c,'Highest rate',y=465,col=RED);note(c,'minutes 2 to 5',y=525,size=26)
    else:
        for i,(x,y) in enumerate(DATA):
            if t>=67.2+i*.82:note(c,f'{x} min',y=194+i*66,size=26);note(c,f'{y}',x=1107,y=194+i*66,size=28,col=GREEN)
        if t>=75:note(c,'Widths   2, 3, 4 min',y=504,size=26,col=RED)

def rate_q(c,t):rates(c,t,False)
def rate_a(c,t):rates(c,t,True)

def plans(c,t,stage):
    title(c,('When do the two plans cost the same?','Find the crossing at a whole number of visits','Compare the very next visit')[stage])
    p=Plot(c,7,32,1,8,'whole visits','cost ($)')
    a=[(v,8+2*v) for v in range(8)];b=[(v,4*v) for v in range(8)]
    pa=7 if stage else 7*cue(t,98.75,3.1)
    pb=7 if stage else 7*cue(t,103.05,3.4)
    # Integer markers are the prices a customer can actually be charged.
    trace(c,p,a,pa,BLUE)
    if stage or t>=103:trace(c,p,b,pb,GREEN)
    note(c,'A   $8 + $2 per visit',y=199,size=25,col=BLUE)
    if stage or t>=103:note(c,'B   $4 per visit',y=258,size=25,col=GREEN)
    if stage==1:
        if t>=117.6:note(c,'$8 gap at 0 visits',y=333,size=26)
        if t>=122.6:p.guide(4,16,cue(t,122.6,1.7));note(c,'8 ÷ (4 − 2) = 4',y=402,size=26,col=RED)
        if t>=125.6:note(c,'4 visits   •   $16 each',y=467,size=27,col=RED)
        if t>=133.8:note(c,'After 4, A is cheaper.',y=535,size=26,col=BLUE)
    if stage==2:
        if t>=138:p.segment((5,0),(5,20),cue(t,138,2),RED,3)
        if t>=139.2:p.dot(5,18,BLUE,9);note(c,'5 visits   A = $18',y=352,size=29,col=BLUE)
        if t>=140.8:p.dot(5,20,GREEN,9);note(c,'5 visits   B = $20',y=426,size=29,col=GREEN)
        if t>=144:note(c,'Gap grows $2 per visit.',y=507,size=25)

def plan_q(c,t):plans(c,t,0)
def plan_a(c,t):plans(c,t,1)
def check(c,t):plans(c,t,2)

def mistakes(c,t):
    if t<155.6:
        title(c,'Equal rises can take different times')
        p=Plot(c,5,12,1,3,'minutes','total count')
        trace(c,p,[(0,0),(1,6),(4,12)],2)
        for a,b,col in [((0,0),(1,6),RED),((1,6),(4,12),BLUE)]:
            p.segment(a,(b[0],a[1]),cue(t,150.9,1.2),col,4)
            p.segment((b[0],a[1]),b,cue(t,152,1.2),col,4)
        if t>=151:note(c,'6 in 1 minute',y=244,col=RED)
        if t>=153:note(c,'6 in 3 minutes',y=342,col=BLUE)
    else:
        title(c,'Read the visit count below the crossing')
        p=Plot(c,7,32,1,8,'whole visits','cost ($)')
        for k,col in [(lambda x:8+2*x,BLUE),(lambda x:4*x,GREEN)]:
            trace(c,p,[(x,k(x)) for x in range(8)],7,col)
        p.dot(4,16,RED,10);p.segment((4,16),(4,0),cue(t,158.8,1.4),RED,4)
        note(c,'$16 is the price.',y=270);note(c,'4 is the visit count.',y=362,col=RED)

def finish(c,t):
    title(c,'Read, then calculate')
    p=Plot(c,9,40,1,10,'minutes','total count');trace(c,p,DATA,3)
    p.guide(2,4,cue(t,165.6,1.45));p.guide(5,22,cue(t,167.2,1.45))
    if t>=169.2:note(c,'Change   22 − 4 = 18',y=230,size=27,col=RED)
    if t>=171.4:note(c,'Rate   18 ÷ 3 = 6/min',y=313,size=26,col=GREEN)
    if t>=173.4:
        note(c,'For a crossing,',y=424,size=27);note(c,'test the same input',y=481,size=25);note(c,'in both rules.',y=525,size=25)

SCENES=(opening,exams,question,answer,rate_q,rate_a,plan_q,plan_a,check,mistakes,finish)
def verify():
    assert HOURLY[-1][1]-HOURLY[1][1]==13
    assert [Fraction(y-b,x-a) for (a,b),(x,y) in zip(DATA,DATA[1:])]==[2,6,4]
    assert [v for v in range(100) if 8+2*v==4*v]==[4] and (8+2*5,4*5)==(18,20)
    assert all(8+2*v < 4*v for v in range(5,100))
