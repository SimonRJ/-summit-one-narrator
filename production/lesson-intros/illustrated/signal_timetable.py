"""T03.2. Advance two signal lights on a common time ruler. Move the starting phase and send the buses from a clock face at 09:24."""
from math import cos,exp,lcm,pi,sin
from captioned_film import cue,mix
ID='T03.2'
ORIGINAL='94dec4e8ebef32fc2ae2e4fd82fa68c3aeb008d87855c1feeffab00f41dc0fca'
START=(0.,14.68,31.,46.81,68.4,86.32,102.31)
POSTER=83.9
PAPER='#152735'
INK,MUTED,GRID='#f9efcf','#abc1c4','#48616c'
A,B,MEET='#f0b869','#83cfc3','#dba3bb'
def text(c,s,x,y,z=31,colour=INK,origin='lm'):c.text(s,x,y,z,colour,origin,True)
def title(c,s):text(c,s,56,54,39)
def ink(a,b,f):
    values=tuple(round(mix(int(a[i:i+2],16),int(b[i:i+2],16),f)) for i in (1,3,5))
    return '#%02x%02x%02x'%values
def signal(c,x,y,name,colour,intensity):
    c.rect(x-74,y-60,148,120,'#253c47',GRID,3)
    c.dot(x,y,47,'#172b35');c.dot(x,y,37,ink('#35434a',colour,intensity))
    c.dot(x-10,y-11,8,ink('#44545a',INK,intensity))
    text(c,name,x,y+86,24,colour,'mm')
def pulse(clock,period,offset=0):
    if clock<offset:return .09
    since=(clock-offset)%period
    return .09+.91*exp(-(since/.63)**2)
def x_at(n):return 198+n*39.5
def tracks(c,nmax=24,odd=False):
    for n in range(nmax+1):
        x=x_at(n)
        if odd:
            c.rect(x-10,159,20,249,'#333b49' if n%2 else '#233e46')
        c.line([(x,296),(x,307 if n%2 else 315)],GRID,2)
        if n%2==0:text(c,str(n),x,337,20,MUTED,'mm')
    for y,col,name in ((226,A,'4 sec'),(399,B,'6 sec')):
        c.line([(x_at(0),y),(x_at(nmax),y)],GRID,3)
        text(c,name,62,y,28,col)
def marks(c,y,period,offset,reached,col,appear=1,nmax=24):
    for start in range(0,nmax+1,period):
        n=start+offset
        if n>nmax or start>reached+.0001:continue
        x=x_at(n);c.dot(x,y,8*appear,col)
def connection(c,n,p=1):
    x=x_at(n);c.line([(x,228),(x,mix(228,397,p))],MEET,5)
    for y in (226,399):c.dot(x,y,8,MEET)
def gap(c,a,b,y,word):
    x,q=x_at(a),x_at(b)
    c.line([(x,y-11),(x,y),(q,y),(q,y-11)],MEET,3)
    text(c,word,(x+q)/2,y+28,24,MEET,'mm')
def opening(c,t):
    title(c,'Two signals share one clock')
    sim=min(24,max(0,(t-.55)*1.8))
    signal(c,256,246,'Every 4 seconds',A,pulse(sim,4))
    signal(c,1012,246,'Every 6 seconds',B,pulse(sim,6))
    text(c,f'{sim:04.1f} s',635,241,53,INK,'mm')
    for i in range(25):
        x=142+i*42;c.line([(x,452),(x,467 if i%4==0 or i%6==0 else 458)],GRID)
        if i<=sim:
            if i%4==0:c.dot(x,419,7,A)
            if i%6==0:c.dot(x,490,7,B)
    if t>=7:text(c,'First meeting after the start?',640,540,31,MEET,'mm')
    if t>=10.4:
        c.rect(270,509,740,78,PAPER)
        text(c,'How far to the following meeting?',640,540,31,MEET,'mm')
def multiples(c,t):
    title(c,'Lay each period on the same time ruler')
    tracks(c)
    if t<21.4:
        marks(c,226,4,0,24,A);marks(c,399,6,0,24,B)
        connection(c,24)
        if t>=18.4:connection(c,12,cue(t,18.4,.8))
        text(c,'24 is a common multiple.',640,520,30,INK,'mm')
    else:
        high=24*cue(t,23.95,4.8)
        for y,period,colour in ((226,4,A),(399,6,B)):
            marks(c,y,period,0,high,colour)
            for start in range(0,24,period):
                q=max(0,min(1,(high-start)/period))
                if q==0:continue
                x0,x1=x_at(start),x_at(start+period)
                coords=[(mix(x0,x1,k*q/18),y-sin(pi*k*q/18)*40) for k in range(19)]
                c.line(coords,colour,2)
        text(c,'Begin at zero. Add the period.',640,525,30,INK,'mm')
def question(c,t):
    title(c,'After time zero, when do both signals light?')
    tracks(c);marks(c,226,4,0,0,A);marks(c,399,6,0,0,B);connection(c,0)
    if t>=33.4:text(c,'+ 4',x_at(2),193,23,A,'mm')
    if t>=35.4:text(c,'+ 6',x_at(3),437,23,B,'mm')
    if t>=37.8:text(c,'Find the first shared positive time.',640,525,34,MEET,'mm')
def same_start(c,t):
    title(c,'The first positive meeting is at twelve seconds')
    tracks(c)
    top=16*cue(t,46.81,3.9)+8*cue(t,61.6,3.1)
    low=18*cue(t,51.,3.)+6*cue(t,61.6,3.1)
    marks(c,226,4,0,top,A);marks(c,399,6,0,low,B)
    if t>=54.4:connection(c,12,cue(t,54.4,.8))
    if t>=57.6:text(c,'12 = 3 × 4 = 2 × 6',631,143,31,INK,'mm')
    if t>=64.2:connection(c,24,cue(t,64.2,.7));gap(c,12,24,471,'12 seconds later')
def delayed(c,t):
    title(c,'Slide the six-second signal two seconds later')
    tracks(c);offset=2*cue(t,68.62,1.7)
    marks(c,226,4,0,24,A);marks(c,399,6,offset,24,B)
    for v in (0,6,12,18):
        x=x_at(v+offset)
        if t>=71:text(c,str(round(v+offset)),x,435,22,B,'mm')
    if t>=73.8:
        for n in (0,4,8,12,16,20,24):text(c,str(n),x_at(n),190,21,A,'mm')
    if t>=77:connection(c,8,cue(t,77,.75))
    if t>=79.8:connection(c,20,cue(t,79.8,.75))
    if t>=81:text(c,'First meeting at 8 s',332,551,27,MEET,'mm')
    if t>=83.6:gap(c,8,20,481,'still 12 seconds apart')
def parity(c,t):
    title(c,'Can an even time coincide with an odd one?')
    tracks(c,odd=True)
    top=24*cue(t,92.4,3.15);low=24*cue(t,88.7,3.2)
    marks(c,399,6,1,low,B);marks(c,226,4,0,top,A)
    for n in range(1,25,6):
        if n-1<=low:text(c,str(n),x_at(n),437,22,B,'mm')
    for n in range(0,25,4):
        if n<=top:text(c,str(n),x_at(n),190,22,A,'mm')
    if t>=97:text(c,'Even times and odd times occupy different columns.',640,532,32,MEET,'mm')
def bus(c,x,y,col,letter):
    c.rect(x,y,125,49,col,INK,2)
    for j in range(4):c.rect(x+9+j*27,y+8,20,15,'#284855')
    for q in (23,102):c.dot(x+q,y+50,9,'#0d1c25');c.dot(x+q,y+50,4,MUTED)
    text(c,letter,x+61,y+36,15,PAPER,'mm')
def clockface(c,o,r,minute):
    c.dot(*o,r+3,GRID);c.dot(*o,r,'#203945')
    def direction(m,l):
        angle=2*pi*m/60-pi/2
        return (o[0]+l*cos(angle),o[1]+l*sin(angle))
    for i in range(60):
        c.line([direction(i,r-4),direction(i,r-(13 if i%5==0 else 7))],MUTED,2)
    for n in (12,3,6,9):text(c,str(n),*direction(n%12*5,r-32),23,INK,'mm')
    c.line([o,direction(45+minute/12,r*.46)],INK,6)
    c.line([o,direction(minute,r*.72)],MEET,4);c.dot(*o,5,INK)
def departures(c,t):
    if t<111.2:
        title(c,'The start sets the first meeting')
        tracks(c);marks(c,226,4,0,24,A);marks(c,399,6,2,24,B)
        connection(c,8);connection(c,20);gap(c,8,20,471,'LCM(4, 6) = 12 seconds')
        return
    title(c,'Two buses depart together at nine o’clock')
    minute=24*cue(t,119.6,3.45)
    clockface(c,(271,339),145,minute)
    text(c,f'09:{int(round(minute)):02d}',272,540,38,MEET,'mm')
    for j,(period,col) in enumerate(((8,A),(12,B))):
        y=218+167*j
        c.line([(505,y+62),(1155,y+62)],GRID,4)
        f=(minute%period)/period
        if minute>23.98:f=0
        xx=519+f*458+111*cue(t,123.1,.8)
        bus(c,xx,y,col,str(period)+' min')
        for n in range(0,25,period):
            x=538+n*23
            c.dot(x,y+100,6,col if n<=minute else GRID)
            text(c,f':{n:02d}',x,y+126,18,MUTED,'mm')
        text(c,'Every '+str(period)+' min',511,y-31,25,col)
    if t>=123.35:text(c,'24 minutes later',836,550,29,INK,'mm')
SCENES=(opening,multiples,question,same_start,delayed,parity,departures)
def verify():
    def common(offset):return sorted(set(range(0,73,4))&set(range(offset,73,6)))
    assert common(0)==list(range(0,73,12)) and common(2)==list(range(8,73,12)) and common(1)==[]
    assert min(x for x in range(1,49) if x%8==x%12==0)==24==lcm(8,12)
    assert all((x_at(n+2)-x_at(n))==79 for n in range(23))
