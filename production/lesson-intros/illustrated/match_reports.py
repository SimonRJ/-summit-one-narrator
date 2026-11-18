"""S065. Trace the two endpoints of a match and count the same 48 bookings from opposite sides of a room roster."""
from itertools import combinations
from math import cos,pi,sin
from captioned_film import cue,font,mix
ID='S065'
ORIGINAL='bb8b5dfb5d9cf7075ba55ddd2c6cc67701184b5e88ca9955b29b817a01374146'
START=(0.,15.32,34.52,47.94,59.47,76.24,88.73,105.34,118.46,131.58,149.34)
POSTER=128.3
PAPER='#142835'
WHITE,SOFT,LINE='#f8f0d9','#b0c1c3','#43606b'
SUN,CYAN,CORAL,PURPLE='#f0c878','#8bd2c5','#ed9480','#bdadd4'
PEOPLE='ABCDEFGHIJ'
TRIOS=tuple(i for i in combinations(range(6),3) if 0 in i)[:8]
BOOKED=tuple(g for a in TRIOS for g in (a,tuple(sorted(set(range(6))-set(a)))))
MATCHES=tuple(combinations(range(10),2))
MISSED=((4,5),(6,7),(8,9))
PLAYED=tuple(pair for pair in MATCHES if pair not in MISSED)
def label(c,s,x,y,z=28,col=WHITE,anchor='lm'):c.text(s,x,y,z,col,anchor,True)
def title(c,s):
    sz=41
    while font(round(sz*c.scale),True).getlength(s)>1147*c.scale:sz-=1
    label(c,s,58,52,sz)
def seat(o,r,i,n):
    a=2*pi*i/n-pi/2
    return o[0]+r*cos(a),o[1]+r*sin(a)
def player(c,p,xy,r=24,colour=CYAN):
    c.dot(*xy,r,colour);label(c,PEOPLE[p],*xy,round(r*1.03),PAPER,'mm')
def trail(c,a,b,q,col,width):
    if q:c.line([a,(mix(a[0],b[0],q),mix(a[1],b[1],q))],col,width)
def wheel(c,o,r,n,links,selected=None,phase=1):
    pts=[seat(o,r,i,n) for i in range(n)]
    for i,j in links:
        chosen=selected is not None and selected in (i,j)
        trail(c,pts[i],pts[j],phase,CYAN if chosen else LINE,4 if chosen else 2.3)
    for i,pt in enumerate(pts):player(c,i,pt,23,SUN if selected==i else CYAN)
def board(c,x,y,gap,highlight_room=None,highlight_person=None,fade=1):
    label(c,'Helper',x-65,y-52,22,SOFT)
    for p in range(16):
        xx=x+p*gap;label(c,p+1,xx,y-34,18,SUN if p==highlight_person else SOFT,'mm')
        for r in range(6):
            yy=y+r*48
            if p==0:label(c,'Room '+str(r+1),x-34,yy,21,CYAN if r==highlight_room else SOFT,'rm')
            c.rect(xx-gap*.4,yy-13,gap*.8,26,'#263d4a',LINE,1)
            if r in BOOKED[p] and p+.2<16*fade:
                tone=SUN if p==highlight_person else CYAN if r==highlight_room else '#91a7ad'
                c.dot(xx,yy,7.5,tone)
def first(c,t):
    title(c,'A link has two endpoints')
    a,b=(244,290),(801,290)
    trail(c,a,b,cue(t,.6,1.5),CYAN,8)
    player(c,0,a,48,SUN);player(c,1,b,48,SUN)
    if t>=3:
        label(c,'A reports B',136,431,28,SOFT);label(c,'B reports A',714,431,28,SOFT)
    if t>=9:
        q=cue(t,9,1.7)
        for xx in (mix(a[0]+60,503,q),mix(b[0]-60,542,q)):c.dot(xx,290,12,CORAL)
    if t>=12:label(c,'2 reports  →  1 link',640,530,36,CORAL,'mm')
def units(c,t):
    title(c,'What does one entry count?')
    a,b=(192,294),(461,294);trail(c,a,b,1,CYAN,5);player(c,0,a);player(c,1,b)
    if t>=19.6:
        label(c,'A → B',193,389,27,SUN);label(c,'B → A',389,389,27,SUN)
    if t>=24.8:
        for j,n in enumerate((1,2,4)):
            c.rect(810,180+j*101,224,71,'#263d4a',LINE,2)
            label(c,'Room '+str(n),837,218+j*101,27)
        if t>=30.2:label(c,'One helper · three bookings',690,522,30,CYAN)
def five(c,t):
    title(c,'Five students shake hands once per pair')
    phase=cue(t,35.3,2.7)
    wheel(c,(382,335),177,5,tuple(combinations(range(5),2)),phase=phase)
    if t>=38.6:label(c,'How many handshakes?',723,260,36)
    if t>=40.8:
        wheel(c,(382,335),177,5,tuple(combinations(range(5),2)),selected=min(4,int((t-40.8)/.9)))
        label(c,'Follow one person’s links.',723,390,27,SOFT)
def reports(c,t):
    title(c,'Two reports describe one handshake')
    selected=min(4,max(0,int((t-48)/.56)))
    wheel(c,(363,331),168,5,tuple(combinations(range(5),2)),selected=selected)
    if t>=48.2:label(c,'5 students × 4 reports',686,189,33,SUN)
    if t>=50.8:label(c,'20 endpoint reports',686,270,34)
    if t>=52.6:
        a,b=(756,375),(1002,375);player(c,0,a,20);player(c,1,b,20)
        c.line([(a[0]+22,375),(b[0]-22,375)],CYAN,4)
        for x in (mix(790,855,cue(t,52.6,1.2)),mix(968,894,cue(t,52.6,1.2))):c.dot(x,375,9,CORAL)
    if t>=55.2:label(c,'20 ÷ 2 = 10 handshakes',661,482,37,CYAN)
def bookings(c,t):
    title(c,'Festival roster · one mark is one room booking')
    for r in range(6):
        x=98+(r%3)*387;y=128+(r//3)*167
        c.rect(x,y,328,137,'#233b49',LINE,2)
        label(c,'Room '+str(r+1),x+19,y+26,22,SOFT)
        occupants=[p for p,rooms in enumerate(BOOKED) if r in rooms]
        for k,p in enumerate(occupants):
            if t<59.6+.19*r+.12*k:continue
            xx=x+44+(k%4)*71;yy=y+66+(k//4)*39
            colour=SUN if p==0 and t>=63.8 else CYAN
            c.dot(xx,yy,14,colour)
            if colour==SUN:label(c,'1',xx,yy,15,PAPER,'mm')
    if t>=62:label(c,'8 helpers per room',128,505,29,CYAN)
    if t>=65.6:label(c,'Helper 1 appears in three rooms.',612,505,29,SUN)
    if t>=67.6:label(c,'How many different helpers?',640,566,29,WHITE,'mm')
def transposition(c,t):
    title(c,'Read the same 48 booking marks two ways')
    r=min(5,max(0,int((t-76.4)/.48)));p=None if t<79.6 else min(15,int((t-79.6)/.42))
    board(c,186,187,57,r if p is None else None,p)
    if t>=76.4:label(c,'6 rooms × 8 = 48 bookings',111,516,29,CYAN)
    if t>=83.4:label(c,'48 ÷ 3 = 16 helpers',687,516,33,SUN)
def tournament(c,t):
    title(c,'Ten players · every pair can play at most once')
    group=0 if t<93 else min(3,int((t-93)/.72)) if t<97 else min(9,4+int((t-97)/.76))
    wheel(c,(365,325),190,10,PLAYED,selected=group if t>=93 else None)
    if t>=93:label(c,'A–D play everyone.',708,227,34,SUN)
    if t>=97:label(c,'E–J each miss one opponent.',708,324,28,SOFT)
    if t>=100.2:label(c,'How many games were played?',697,455,28,CYAN)
def endpoints(c,t):
    title(c,'Count every player’s end of every match')
    for i in range(10):
        x=127+(i%5)*120;y=181+(i//5)*155
        player(c,i,(x,y),24,SUN if i<4 else CYAN)
        v=9 if i<4 else 8
        if t>=(105.4 if i<4 else 108.2):
            for j in range(v):c.dot(x-32+(j%5)*15,y+49+(j//5)*15,4,SUN if i<4 else CYAN)
            label(c,str(v),x,y+94,23,SOFT,'mm')
    if t>=105.4:label(c,'4 × 9',812,195,42,SUN)
    if t>=108.2:label(c,'6 × 8',812,275,42,CYAN)
    if t>=111.2:label(c,'36 + 48 = 84 reports',782,365,29)
    if t>=116:label(c,'84 ÷ 2 = 42 matches',745,471,35,CORAL)
def schedule(c,t):
    title(c,'Check the result against the complete schedule')
    # This upper triangle has a distinct square for each unordered pair of the ten players.
    x0,y0,step=139,164,38
    for k in range(10):
        label(c,PEOPLE[k],x0+k*step,y0-37,20,SOFT,'mm')
        label(c,PEOPLE[k],x0-37,y0+k*step,20,SOFT,'mm')
    for i,j in MATCHES:
        x=x0+j*step;y=y0+i*step
        missed=(i,j) in MISSED and t>=122+.57*MISSED.index((i,j))
        c.rect(x-15,y-15,30,30,'#4e3e42' if missed else CYAN)
        if missed:c.line([(x-9,y-9),(x+9,y+9)],CORAL,3);c.line([(x-9,y+9),(x+9,y-9)],CORAL,3)
    label(c,'45 possible matches',675,175,34)
    if t>=122:
        for k,(i,j) in enumerate(MISSED):
            xx=678+k*131
            if t>=122+.57*k:label(c,PEOPLE[i]+'–'+PEOPLE[j],xx,279,30,CORAL)
    if t>=124.6:label(c,'6 missed reports = 3 matches',665,369,29,SOFT)
    if t>=127.4:label(c,'45 − 3 = 42',692,474,42,CYAN)
def mistake(c,t):
    title(c,'Keep the units attached to the count')
    a,b=(151,248),(458,248);trail(c,a,b,1,CYAN,4);player(c,0,a,27);player(c,1,b,27)
    if t>=133.2:label(c,'1 game',239,334,30,CYAN)
    if t>=136:label(c,'2 player reports',162,432,29,SUN)
    if t>=141.2:
        label(c,'One helper',771,190,30,SUN)
        for j,r in enumerate((1,2,4)):
            c.rect(776,263+j*55,220,45,'#273e4a',LINE,1);label(c,'Room '+str(r),811,284+j*55,23)
        if t>=144:label(c,'3 bookings',800,461,30,CYAN)
def recap(c,t):
    title(c,'Write down what each total counts')
    if t<153.8:
        wheel(c,(357,340),166,5,tuple(combinations(range(5),2)),selected=0)
        label(c,'One match is one pair.',710,268,33)
        label(c,'One booking is one assignment.',666,378,28,SOFT)
    else:
        board(c,178,170,54,2 if t<155.6 else None,3 if t>=155.6 else None)
        if t>=155.6:label(c,'48 assignments',162,500,34,CYAN)
        if t>=159.2:label(c,'÷ 3 assignments each = 16 helpers',590,500,28,SUN)
SCENES=(first,units,five,reports,bookings,transposition,tournament,endpoints,schedule,mistake,recap)
def verify():
    assert len(tuple(combinations(range(5),2)))==10 and len(MATCHES)==45
    assert len(BOOKED)==16 and all(len(set(rooms))==3 for rooms in BOOKED)
    assert all(sum(r in rooms for rooms in BOOKED)==8 for r in range(6))
    assert len(PLAYED)==42 and [sum(i in game for game in PLAYED) for i in range(10)]==[9]*4+[8]*6
    assert set(MATCHES)-set(PLAYED)==set(MISSED) and len({p for pair in MISSED for p in pair})==6
