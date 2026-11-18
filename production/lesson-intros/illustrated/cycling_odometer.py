"""S034. A side-on bicycle, a calibrated odometer and one common clock across an out-and-back ride."""
from fractions import Fraction
from math import cos,pi,sin
from captioned_film import cue,mix,font
ID='S034';ORIGINAL='a06df6625f194a1a9ec5035873baa17c6f643352f2f578417b10de499deaa509';START=(0,17.08,33.56,46.02,57.71,71.44,84.88,101.97,123.72,140.52,158.28);POSTER=119.2
PAPER='#eff1e5';INK='#283b37';SOFT='#5a6964';EDGE='#b8c4ad';DARK='#4f6159';GREEN='#16755e';CORAL='#b04c39';BLUE='#356d87';GOLD='#f2c276';CLOUD='#e0e7d8';GLASS='#fbfaee';LIGHT='#d7e6dc'

def title(c,s):
    size=42
    while font(round(size*c.scale),True).getlength(s)>1148*c.scale:size-=1
    c.text(s,62,61,size,INK,'lm',True)
def label(c,s,x,y,sz=32,col=INK):c.text(s,x,y,sz,col,'lm',True)
def line(c,a,b,colour,k=1,w=3):c.line([a,(mix(a[0],b[0],k),mix(a[1],b[1],k))],colour,w)
def bike(c,x,y,forward,turn,k=.78):
    def pt(a,b):return (x+(1 if forward else -1)*a*k,y+b*k)
    def bars(points,colour,w):c.line([pt(a,b) for a,b in points],colour,w*k)
    for center in (-32,32):
        a,b=pt(center,0);c.dot(a,b,19*k,INK);c.dot(a,b,16*k,PAPER)
        for z in range(6):
            w=turn+z*pi/3;bars([(center,0),(center+15*cos(w),15*sin(w))],EDGE,1.5)
        c.dot(a,b,2*k,INK)
    bars([(-32,0),(-11,-25),(0,0),(-32,0)],GREEN,5);bars([(0,0),(20,-28),(32,0)],GREEN,4);bars([(-11,-25),(20,-28)],GREEN,4)
    bars([(-11,-24),(-13,-32),(-21,-32)],INK,3);bars([(20,-28),(17,-37),(25,-37)],INK,3)
    bars([(-12,-32),(-13,-51),(0,-63),(17,-42),(24,-37)],BLUE,5);c.dot(*pt(2,-73),7*k,CORAL)
    d=(9*cos(turn),9*sin(turn));bars([(-13,-47),(4,-29),d],INK,3.5);c.dot(*pt(0,0),4*k,INK)

def road(c,dist,maximum,forward,odo,marks,showbike=True):
    x0,x1,y=150,1076,340
    c.poly([(x0,285),(x0+92,224),(x0+184,267),(x0+314,179),(x0+464,272),(x0+638,211),(x1,282),(x1,324),(x0,324)],CLOUD,None)
    c.line([(x0,y),(x1,y)],DARK,3)
    for d,txt in marks:
        X=x0+(x1-x0)*d/maximum;c.line([(X,y+4),(X,y+17)],INK,2);c.text(txt,X,y+40,24,SOFT,bold=True)
    X=x0+(x1-x0)*dist/maximum
    if showbike:bike(c,X,y-16,forward,odo*.82,.88)
    return X

def window(c,x,y,w,heading,value,col):
    c.rect(x,y,w,85,GLASS,EDGE,2);c.text(heading,x+15,y+20,17,SOFT,'lm',True);c.text(value,x+15,y+57,30,col,'lm',True)

def hm(t):
    whole=round(t);return f'{whole//60} h {whole%60:02d} min'

def position(m):return min(m,120)*.2 if m<=132 else max(0,24-(m-132)*.4)
def odometer(m):return m*.2 if m<=120 else 24 if m<=132 else 24+(m-132)*.4

def intro(c,t):
    title(c,'A rider, a distance counter and a clock');m=60*cue(t,.6,5.8);road(c,m/10,6,True,m/10,((0,'0 km'),(3,'3 km'),(6,'6 km')))
    stopped=12*cue(t,13.2,2.4)
    window(c,153,452,258,'TIME',hm(m+stopped),BLUE);window(c,469,452,261,'DISTANCE',f'{m/10:.1f} km',GREEN)
    if t>=6.8:window(c,785,452,280,'SPEED','0 km/h' if t>=13.2 else '6 km/h',CORAL)
    if t>=13.2:label(c,'A stop adds elapsed time.',437,577,26,SOFT)

def uses(c,t):
    title(c,'Use one clock for all stages of the ride')
    for i,(x,s,n) in enumerate([(152,'Outward','hours'),(478,'Stop','minutes'),(808,'Return','hours')]):
        window(c,x,214,269,s,n if t<23.2 else 'minutes', (GREEN,CORAL,BLUE)[i])
    if t>=26.2:
        for i,(a,b,col) in enumerate(((0,120,GREEN),(120,132,CORAL),(132,192,BLUE))):
            p=cue(t,26.2+i*.55,.9);c.rect(167+4.63*a,421,4.63*(b-a)*p,40,col)
        label(c,'Outward',161,498,27,GREEN);label(c,'Stop',701,498,23,CORAL);label(c,'Return',931,498,27,BLUE)

def basic(c,t):
    title(c,'18 kilometres over three equal hours');h=3*cue(t,33.56,4.6);road(c,6*h,18,True,6*h,((0,'0 km'),(6,'6 km'),(12,'12 km'),(18,'18 km')))
    for i in range(3):window(c,151+i*324,448,267,'HOUR '+str(i+1),'6 km' if t>=40.6 and i==0 else '·',(GREEN,BLUE,CORAL)[i])
    if t>=38.4:label(c,'How far in one hour?',443,570,29)

def basic_result(c,t):
    title(c,'Mark the distance at the end of each hour');h=3*cue(t,46.1,5.25);road(c,6*h,18,True,6*h,((0,'0'),(6,'1 h · 6 km'),(12,'2 h · 12 km'),(18,'3 h · 18 km')))
    if t>=49.4:label(c,'18 ÷ 3 = 6 km/h',141,485,37,GREEN)
    if t>=54.2:label(c,'6 km/h × 3 h = 18 km',649,485,32,BLUE)

def dial(c,x,y,m):
    r=94;c.dot(x,y,r+3,INK);c.dot(x,y,r,GLASS)
    for j in range(60):
        a=j*pi/30-pi/2;v=r-(10 if j%5==0 else 5);c.line([(x+v*cos(a),y+v*sin(a)),(x+r*cos(a),y+r*sin(a))],SOFT,2 if j%5==0 else 1)
    a=min(60,m)*pi/30-pi/2
    if m>0:c.poly([(x,y)]+[(x+(r-14)*cos(-pi/2+(a+pi/2)*i/50),y+(r-14)*sin(-pi/2+(a+pi/2)*i/50)) for i in range(51)],LIGHT,None)
    c.line([(x,y),(x+(r-10)*cos(a),y+(r-10)*sin(a))],CORAL,4);c.dot(x,y,5,INK);c.text(f'{round(m)} min',x,y+r+38,28,INK,bold=True)

def medium(c,t):
    title(c,'12 km/h for 45 minutes');dial(c,299,309,45*cue(t,58.7,2.5));label(c,'Speed   12 km / hour',600,247,33,GREEN)
    if t>=61.6:label(c,'Distance   ?',600,329,35,BLUE)
    if t>=63.4:label(c,'45 of the 60 minutes',600,426,30)

def medium_result(c,t):
    title(c,'Three quarters of one hour’s distance');m=45*cue(t,73.8,3.4);road(c,.2*m,12,True,.2*m,((0,'0'),(3,'3 km'),(6,'6 km'),(9,'9 km'),(12,'12 km')))
    label(c,'45/60 = 3/4 hour',138,488,33,BLUE)
    if t>=76.8:label(c,'12 × 3/4 = 9 km',680,488,35,GREEN)

def trip(c,m):
    road(c,position(m),24,m<=132,odometer(m),((0,'Home · 0 km'),(12,'12 km'),(24,'Turnaround · 24 km')))
    for x,heading,val,col in [(150,'ELAPSED',hm(m),BLUE),(473,'ODOMETER',f'{odometer(m):.1f} km',GREEN),(795,'CURRENT SPEED',('12' if m<120 else '0' if m<=132 or m>=192 else '24')+' km/h',CORAL)]:window(c,x,438,276,heading,val,col)

def challenge(c,t):
    title(c,'One ride out, a stop, and the same road home');m=120*cue(t,85,3.05)+12*cue(t,88.3,2.05)+60*cue(t,90.65,3.0);trip(c,m)
    if t>=95.4:label(c,'What is the average for the whole trip?',290,569,30)

def row(c,y,s,a,b,col):label(c,s,148,y,29,col);label(c,a,512,y,31,col);label(c,b,883,y,31,col)

def solve(c,t):
    title(c,'Add all distances and all elapsed times');row(c,153,'Stage','Distance','Time',SOFT)
    row(c,225,'Outward','24 km','120 min' if t>=105 else '24 ÷ 12 h',GREEN)
    if t>=106.9:row(c,358,'Return','24 km','60 min',BLUE)
    if t>=108.8:row(c,291,'Stop','0 km','12 min',CORAL)
    if t>=110.2:
        c.line([(140,407),(1115,407)],EDGE,2);row(c,454,'Whole trip','48 km' if t>=113.4 else '·','192 min',INK)
    if t>=117.6:label(c,'48 ÷ (192/60)',146,557,34,BLUE)
    if t>=120.6:label(c,'= 15 km/h',653,557,37,GREEN)

def clocked(c,t):
    title(c,'Watch the clock during the stop');m=min(192,max(0,192*(t-123.87)/13.1));trip(c,m)
    if t>=132.8:label(c,'The odometer stays at 24 km throughout the stop.',184,565,28)

def mistakes(c,t):
    title(c,'Keep the units attached through the calculation')
    if t<150.6:
        dial(c,281,310,45);label(c,'45 minutes = 3/4 hour',561,250,33,BLUE)
        if t>=145.4:label(c,'12 km/h × 3/4 h = 9 km',561,363,32,GREEN)
    else:
        trip(c,120+12*cue(t,150.7,2.5));label(c,'Zero kilometres during these twelve minutes.',236,566,28,CORAL)

def finish(c,t):
    title(c,'Keep the stop in the journey total');row(c,152,'Stage','Distance','Elapsed time',SOFT);row(c,236,'Outward','24 km','120 min',GREEN);row(c,306,'Stop','0 km','12 min',CORAL);row(c,376,'Return','24 km','60 min',BLUE)
    if t>=164.6:c.line([(136,423),(1125,423)],EDGE,2);row(c,462,'Total','48 km','192 min',INK)
    if t>=168.4:label(c,'48 km ÷ 3.2 h = 15 km/h',306,553,35,GREEN)
SCENES=(intro,uses,basic,basic_result,medium,medium_result,challenge,solve,clocked,mistakes,finish)
def verify():
    assert 18/3==6 and 12*Fraction(45,60)==9
    assert (position(120),position(132),position(192))==(24,24,0) and (odometer(120),odometer(132),odometer(192))==(24,24,48)
    assert Fraction(48,1)/(Fraction(24,12)+Fraction(12,60)+Fraction(24,24))==15
