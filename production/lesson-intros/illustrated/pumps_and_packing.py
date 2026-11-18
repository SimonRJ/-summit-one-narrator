"""S031. Label real cartons, combine production lines and measure a tank across a leak opening."""
from fractions import Fraction
from math import sin,cos,pi
from captioned_film import cue,mix,font
ID='S031';ORIGINAL='17be693aea49845531652c4be6665d322041b6da6d8080bf54b2578a023257e5';START=(0,17.71,35.79,48.88,62,76.37,94.29,111.54,132.49,147.05,160.65);POSTER=127.4
PAPER='#1f2735';INK='#fcf2df';SOFT='#b9c9d1';RIM='#667787';OFF='#374557';CORAL='#f09e86';GOLD='#f4c978';TEAL='#7ad8c4';AQUA='#a9e7ec';WATER='#357da0';DARK='#273440';BROWN='#b77858';TOP='#e7b891';SIDE='#975f48'

def title(c,s):
    size=41
    while font(round(size*c.scale),True).getlength(s)>1145*c.scale:size-=1
    c.text(s,62,64,size,INK,'lm',True)
def label(c,s,x,y,size=32,col=INK):c.text(s,x,y,size,col,'lm',True)

def carton(c,x,y,w,stamp):
    a=w*.27;b=w*.18;h=w*.70
    c.poly([(x,y),(x+w,y),(x+w,y+h),(x,y+h)],BROWN,DARK,2)
    c.poly([(x,y),(x+a,y-b),(x+w+a,y-b),(x+w,y)],TOP,DARK,2)
    c.poly([(x+w,y),(x+w+a,y-b),(x+w+a,y+h-b),(x+w,y+h)],SIDE,DARK,2)
    c.line([(x+w*.51,y-1),(x+w*.51+a,y-b)],SIDE,2)
    if stamp>0:
        X=x+w*.18;Y=y+h*.25;c.rect(X,Y,w*.58*stamp,h*.45,TEAL)
        if stamp>.9:c.line([(X+w*.12,Y+h*.23),(X+w*.2,Y+h*.32),(X+w*.37,Y+h*.09)],DARK,2)

def belt(c,y,t,n,marked,progress=0):
    L,R=107,1100;floor=y+74;c.rect(L,floor,R-L,36,OFF,RIM,3)
    for i in range(13):
        x=L+38+i*76;rad=10;c.dot(x,floor+18,rad,RIM);a=t*.9
        c.line([(x-rad*.72*cos(a),floor+18-rad*.72*sin(a)),(x+rad*.72*cos(a),floor+18+rad*.72*sin(a))],DARK,2)
    for i in range(n):carton(c,148+i*148+progress,y,77,max(0,min(1,marked-i)))

def tank_amount(minute):return min(18,max(0,5*min(2,minute)+4*max(0,minute-2)))

def pipe(c,path,colour,active):
    c.line(path,RIM,15);c.line(path,colour if active else OFF,7)

def tank(c,units,phase,tick,show_leak,labels=True):
    # The vessel has parallel sides, so equal rises represent equal volumes.
    L,R,T,B=261,654,186,493;h=(B-T)/18
    if units>0:
        waterline=B-units*h;c.rect(L+4,waterline,R-L-8,max(1,B-waterline-3),WATER)
        c.line([(L+4,waterline),(R-4,waterline)],AQUA,3)
    for n in range(19):
        y=B-n*h;c.line([(L-13 if n%2==0 else L-7,y),(L,y)],SOFT,2)
        if n in (0,10,18):c.text(str(n),L-24,y,23,SOFT,'rm',True)
    c.line([(L,T),(L,B),(R,B),(R,T)],INK,5)
    pipe(c,[(143,169),(356,169),(356,190)],TEAL,phase>0);pipe(c,[(699,140),(553,140),(553,190)],GOLD,phase>0)
    if labels:
        label(c,'A',143,132,23,TEAL);label(c,'B',700,114,23,GOLD)
    if phase>0 and units<18:
        surface=B-units*h
        for x,col,offset in [(356,TEAL,0),(553,GOLD,.48)]:
            c.line([(x,192),(x,surface-2)],col,3)
            if surface>210:c.dot(x,198+((tick*.93+offset)%1)*max(0,surface-202),4,col)
    if show_leak:
        pipe(c,[(R,B-54),(714,B-54),(714,B-29)],CORAL,phase==2)
        if phase==2 and units<18:
            c.line([(714,B-29),(714,529)],CORAL,3)
            c.dot(714,472+((tick*.77)%1)*48,4,CORAL)

def graph(c,m):
    x=lambda z:825+80*z;y=lambda u:462-u*11.8
    c.line([(x(0),y(18)-8),(x(0),y(0)),(x(4)+23,y(0))],SOFT,2)
    for k in (0,2,4):c.text(str(k),x(k),y(0)+23,20,SOFT)
    for k in (0,10,18):c.text(str(k),x(0)-13,y(k),18,SOFT,'rm')
    c.text('minutes',x(2),y(0)+63,22,SOFT)
    seg=min(m,2);c.line([(x(0),y(0)),(x(seg),y(5*seg))],TEAL,4)
    if m>2:c.line([(x(2),y(10)),(x(m),y(tank_amount(m)))],CORAL,4)
    c.dot(x(m),y(tank_amount(m)),6,INK)

def intro(c,t):
    title(c,'Measure progress in one minute')
    if t<10.4:
        belt(c,292,t,6,cue(t,5.4,2.0));label(c,'One whole batch',131,182,32)
        if t>=5.4:label(c,'1/6 batch per minute',305,510,40,TEAL)
    else:
        minute=2*cue(t,10.4,4.0)+.5*cue(t,14.4,2);tank(c,tank_amount(minute),2 if t>=14.4 else 1,t,True)
        label(c,'Inlets add',778,267,35,TEAL)
        if t>=13.4:label(c,'A leak subtracts',778,355,31,CORAL)

def uses(c,t):
    title(c,'How much of the job gets done each minute?')
    if t<26:
        belt(c,288,t,6,2.7*cue(t,18.0,5.4));label(c,'A batch on a production line',142,164,34)
    else:
        p=2*cue(t,26,4.5)+2*cue(t,30.5,3.5);tank(c,tank_amount(p),1 if p<=2 else 2,t,True)
        label(c,'Whole job',789,243,35)
        if t>=28.6:label(c,'Rate change',789,331,35,CORAL)
        if t>=32.6:label(c,'Work remaining',789,417,33,GOLD)

def basic(c,t):
    title(c,'Labelling one batch takes six minutes')
    belt(c,284,t,6,cue(t,40.6,1.7));label(c,'Six equal portions',135,169,33)
    if t>=40.6:label(c,'How much is labelled after one minute?',204,507,34,TEAL)

def basic_result(c,t):
    title(c,'Match each minute to an equal portion')
    marked=cue(t,52.2,1.25)+5*cue(t,57.6,2.9)
    belt(c,282,t,6,marked)
    for j in range(6):c.text(str(j+1),192+j*148,218,26,SOFT,bold=True)
    if t>=54.4:label(c,'1/6 batch per minute',143,512,33,TEAL)
    if t>=57.6:label(c,'× 6 min = 1 batch',687,512,32,GOLD)

def pallet(c,x,y,n,done,col,second=None):
    for i in range(n):
        X=x+(i%6)*58;Y=y+(i//6)*53;active=i<done
        ink=GOLD if second is not None and i>=second else col
        c.rect(X+2,Y+3,43,33,OFF);c.rect(X,Y,43,33,ink if active else DARK,ink if active else RIM,2)
        if active:c.line([(X+9,Y+16),(X+16,Y+22),(X+31,Y+9)],DARK,2)

def machine(c,t):
    title(c,'Two machines work on the same size batch');label(c,'Machine A · 6 min',116,169,31,TEAL)
    pallet(c,123,229,18,18*cue(t,62.1,2.7),TEAL)
    if t>=65.2:
        label(c,'Machine B · 9 min',660,169,31,GOLD);pallet(c,674,229,18,18*cue(t,65.2,3.5),GOLD)
    if t>=69.2:label(c,'What changes when both work at once?',173,520,34)

def together(c,t):
    title(c,'Both machines contribute in the same minute')
    a=3*cue(t,79.6,1.5);b=2*cue(t,81.1,1.3)
    label(c,'One batch = 18 units',124,154,31);pallet(c,142,233,18,a+b,TEAL,3)
    if t>=79.6:label(c,'A   18 ÷ 6 = 3 units/min',615,230,29,TEAL)
    if t>=81.1:label(c,'B   18 ÷ 9 = 2 units/min',615,293,29,GOLD)
    if t>=83.2:label(c,'Together   5 units/min',615,370,31)
    if t>=86:
        # One progress strip has unit length 18. Its five subdivisions per minute advance continuously.
        m=3.6*cue(t,86,4.2);L=148;Y=479;w=924
        c.rect(L,Y,w,24,OFF,RIM,2);c.rect(L,Y,w*min(1,m/3.6),24,TEAL)
        for n in range(1,18):c.line([(L+w*n/18,Y),(L+w*n/18,Y+24)],DARK,1.5)
        if t>=88.6:label(c,'18 ÷ 5 = 18/5 minutes',305,551,33)

def question(c,t):
    title(c,'A leak opens two minutes after the pumps start')
    m=2*cue(t,94.4,5.3);tank(c,tank_amount(m),2 if t>=100.4 else 1,t,t>=100.4)
    if t>=96.6:label(c,'A alone · 6 min',777,227,31,TEAL)
    if t>=98.8:label(c,'B alone · 9 min',777,293,31,GOLD)
    if t>=100.4:label(c,'Leak alone · 18 min',777,359,30,CORAL)
    if t>=105.6:label(c,'When is the tank full?',761,464,29)

def solve(c,t):
    title(c,'Measure the water before and after the leak opens')
    m=2*cue(t,114.2,3.1)+2*cue(t,123.7,5.3)
    tank(c,tank_amount(m),1 if t<120.6 else 2,t,t>=120.6)
    label(c,'Capacity · 18 units',776,167,30)
    if t>=114.2:label(c,'In   3 + 2 = 5 per min',776,234,28,TEAL)
    if t>=118.8:label(c,'At 2 min: 18 − 10 = 8',776,304,30,GOLD)
    if t>=120.6:label(c,'Net   5 − 1 = 4 per min',776,374,27,CORAL)
    if t>=125.8:label(c,'8 ÷ 4 = 2 more min',776,445,29)
    if t>=130:label(c,'Total   2 + 2 = 4 min',772,519,30,TEAL)

def check(c,t):
    title(c,'Read both rates from the rising water level')
    m=2*cue(t,132.5,2.7)+2*cue(t,135.6,3.5);tank(c,tank_amount(m),1 if m<=2 else 2,t,True);graph(c,m)
    if t>=139.4:label(c,'10 + 8 = 18 units',235,554,31,TEAL)
    if t>=143.2:label(c,'The slope changes at minute 2.',734,166,27,CORAL)

def mistakes(c,t):
    title(c,'Use the rate that applies during each interval')
    if t<154:
        pallet(c,139,213,18,5*cue(t,148.2,2.9),TEAL);label(c,'A   3 per min',663,250,34,TEAL);label(c,'B   2 per min',663,332,34,GOLD)
        if t>=151.6:label(c,'Together   5 per min',333,498,37)
    else:
        m=2*cue(t,154,2.4)+1.5*cue(t,156.7,2.4);tank(c,tank_amount(m),1 if m<=2 else 2,t,True)
        label(c,'0 to 2 min',782,237,35,TEAL);label(c,'Pumps only',782,290,27)
        if t>=156.6:label(c,'After 2 min',782,380,35,CORAL);label(c,'Pumps and leak',782,433,27)

def finish(c,t):
    title(c,'Choose a whole tank of 18 units')
    m=2 if t<167.6 else 2+2*cue(t,171.4,2.4);tank(c,tank_amount(m),1 if m<=2 else 2,t,t>=167.6)
    label(c,'18 ÷ 6 = 3',799,183,32,TEAL);label(c,'18 ÷ 9 = 2',799,245,32,GOLD)
    if t>=163.6:label(c,'18 ÷ 18 = 1',799,309,32,CORAL)
    if t>=167.6:label(c,'At 2 min: 8 units left',799,401,32)
    if t>=171.4:label(c,'8 ÷ 4 = 2 more min',775,478,30,TEAL)
SCENES=(intro,uses,basic,basic_result,machine,together,question,solve,check,mistakes,finish)
def verify():
    assert Fraction(1,6)+Fraction(1,9)==Fraction(5,18) and 1/Fraction(5,18)==Fraction(18,5)
    assert 18*(Fraction(1,6)+Fraction(1,9)-Fraction(1,18))==4
    assert [tank_amount(m) for m in range(5)]==[0,5,10,14,18]
    for a in [Fraction(k,20) for k in range(81)]:assert tank_amount(a)==(5*a if a<=2 else 10+4*(a-2))
