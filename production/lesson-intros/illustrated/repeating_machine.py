"""S054. Turn a compass, couple two detented dials, and follow a marble through a one-way five-state loop."""
from math import cos,sin,pi,hypot,floor
from captioned_film import cue,mix,font
ID='S054'
ORIGINAL='425f62a72fe8011a7829c7714729f9cd58f8d1b62d386d66d2872011ff90c9cb'
START=(0,17.08,35.48,49.38,60.59,75.44,89.52,107.41,126.60,141.64,156.52)
POSTER=124.6
PAPER='#252038';INK='#fff2d8';MUTED='#d7c9da';STRIP='#423952';METAL='#73657f';AQUA='#85e7d0';GOLD='#ffd184';RED='#ff9b96';SHADOW='#171322'

def label(c,text,x,y,size=30,col=INK,anchor='lm'):
    c.text(text,x,y,size,col,anchor,True)
def title(c,s):
    size=42
    while font(round(size*c.scale),True).getlength(s)>1160*c.scale:size-=1
    label(c,s,62,58,size)
def circular(x,y,r,turn):
    theta=turn*2*pi-pi/2
    return (x+r*cos(theta),y+r*sin(theta))
def arrow(c,a,b,ink,t=.6):
    dx=b[0]-a[0];dy=b[1]-a[1];n=hypot(dx,dy);u,v=dx/n,dy/n
    px=mix(a[0],b[0],t);py=mix(a[1],b[1],t)
    c.poly([(px+9*u,py+9*v),(px-7*u-6*v,py-7*v+6*u),(px-7*u+6*v,py-7*v-6*u)],ink,None)
def dial(c,x,y,r,n,turn,colour,names,cardinal=False):
    c.dot(x+3,y+5,r+9,SHADOW);c.dot(x,y,r+8,METAL);c.dot(x,y,r+4,STRIP);c.dot(x,y,r-3,PAPER)
    for j in range(n):
        a=circular(x,y,r-9,j/n);b=circular(x,y,r-21,j/n)
        c.line([a,b],colour,4)
        tx,ty=circular(x,y,r+30,j/n);label(c,names[j],tx,ty,27 if cardinal else 24,colour,'mm')
    # The pointer and its counterweight turn rigidly about the same centre.
    tip=circular(x,y,r-22,turn);tail=circular(x,y,r*.42,turn+.5)
    left=circular(x,y,9,turn+.25);right=circular(x,y,9,turn-.25)
    c.poly([left,tip,right],colour,None);c.poly([left,tail,right],METAL,None);c.dot(x,y,9,INK)
def step_at(t,start,end,n):
    z=max(0,min(n,n*(t-start)/(end-start)))
    j=floor(z);q=min(1,(z-j)*1.65)
    return j+q*q*(3-2*q)

# All directed edges are structural. State one feeds state two and has no incoming edge.
POINTS={1:(112,325),2:(318,325),3:(452,169),4:(678,222),5:(689,399),6:(461,467)}
def state(move):
    return 1 if move==0 else 2+(move-1)%5
def state_point(m):
    k=floor(m);a=POINTS[state(k)];b=POINTS[state(k+1)];p=m-k
    return mix(a[0],b[0],p),mix(a[1],b[1],p)
def track(c,m,tail=True,highlight=None):
    for a,b in ((1,2),(2,3),(3,4),(4,5),(5,6),(6,2)):
        p,q=POINTS[a],POINTS[b];col=GOLD if a==1 and tail else METAL if a==1 else AQUA
        c.line([p,q],SHADOW,17);c.line([p,q],METAL,9);c.line([p,q],STRIP,5);arrow(c,p,q,col,t=.57)
    for s,(x,y) in POINTS.items():
        colour=GOLD if s==1 and tail else METAL if s==1 else AQUA
        c.dot(x,y,31,colour);c.dot(x,y,27,STRIP)
        label(c,str(s),x,y+1,31,INK,'mm')
    x,y=state_point(m)
    c.dot(x,y,23,SHADOW);c.dot(x,y-2,19,RED);c.dot(x-6,y-8,5,INK)
    # Keep the state number readable when the marble is over its socket.
    if abs(m-round(m))<.02:label(c,str(state(round(m))),x,y-1,23,SHADOW,'mm')
    if highlight:label(c,highlight,410,552,28,AQUA,'mm')
def readout(c,n):
    x=846;c.rect(x-12,142,343,109,STRIP,METAL,2)
    label(c,'COMPLETED MOVES',x+9,169,21,MUTED)
    label(c,str(n),x+8,215,41,INK)
def intro(c,t):
    title(c,'A machine with one entry and a repeating loop')
    m=step_at(t,.6,7.95,6);track(c,m)
    if t>=5.2:label(c,'Back at state 2' if m==6 else 'Watch for state 2.',821,228,33,AQUA)
    if t>=10.6:label(c,'1 → 2 happens once.',821,336,28,GOLD)
    if t>=13.8:label(c,'The next five moves repeat.',821,433,25,MUTED)
def uses(c,t):
    title(c,'Predict the next move from the complete state')
    # Put the same pointer in two states whose second setting differs.
    full=t>=23.8
    for i,x in enumerate((325,842)):
        turn=cue(t,17.5,2.2)/4
        dial(c,x,303,84,4,turn,AQUA,('N','E','S','W'),True)
        if full:
            col=(GOLD,RED)[i];c.dot(x+155,300,18,col);label(c,('gold','red')[i],x+155,356,23,col,'mm')
    if full:label(c,'Compare both the heading and the colour.',633,497,31,INK,'mm')
    else:label(c,'The headings agree.',633,500,30,MUTED,'mm')
def compass(c,t,worked):
    title(c,'Eleven clockwise quarter turns')
    if worked:
        steps=step_at(t,49.4,52.45,4) if t<52.6 else (4+step_at(t,52.6,55.65,4) if t<55.8 else 8+step_at(t,55.8,58.17,3))
    else:steps=step_at(t,43,48.65,4) if t>=43 else 0
    dial(c,360,324,145,4,steps/4,AQUA,('N','E','S','W'),True)
    n=floor(steps+.0001);label(c,f'{n} turns completed',718,225,34,AQUA)
    if worked:
        if t>=52.6:label(c,'11 = 4 + 4 + 3',718,319,38,GOLD)
        if t>=55.8:label(c,'N → E → S → W',718,403,33)
        if t>=58.2:label(c,'Final heading   West',718,500,31,RED)
    elif t>=38:label(c,'One turn = 90°',718,333,33,GOLD)
    if not worked and t>=41.4:label(c,'Predict the final heading.',718,448,30)
def compass_q(c,t):compass(c,t,False)
def compass_a(c,t):compass(c,t,True)
def gear_pair(c,steps):
    dial(c,287,293,87,2,steps/2,GOLD,('0','1'))
    dial(c,648,293,87,3,steps/3,AQUA,('0','1','2'))
    label(c,'2 positions',287,453,27,GOLD,'mm');label(c,'3 positions',648,453,27,AQUA,'mm')
def dials(c,t):
    title(c,'One press advances both dials')
    steps=step_at(t,65.4,67.4,1);gear_pair(c,steps)
    label(c,'Start   (0, 0)',850,228,31)
    if t>=65.4:label(c,'One press   (1, 1)',850,315,29)
    if t>=68.2:label(c,'When do both reset?',850,416,29,RED)
def dial_sol(c,t):
    title(c,'Find the first positive press that restores both settings')
    steps=step_at(t,75.65,83.45,6);gear_pair(c,steps);n=floor(steps+.0001)
    label(c,f'After {n} '+('press' if n==1 else 'presses'),866,198,29)
    label(c,f'({n%2}, {n%3})',866,298,58,AQUA if n==6 else INK)
    if t>=81.4:label(c,'2, 4, 6, …',866,400,27,GOLD)
    if t>=82.15:label(c,'3, 6, 9, …',866,446,27,AQUA)
    if t>=83.5:label(c,'First joint reset   6',866,519,26,RED)
def machine(c,t):
    title(c,'Follow the numbered machine for 51 moves')
    m=step_at(t,91.85,94.65,5)+step_at(t,94.85,97.2,1)
    track(c,m);readout(c,floor(m+.0001))
    label(c,'Start at state 1.',842,312,30,GOLD)
    if t>=94.8:label(c,'6 returns to 2.',842,385,31,AQUA)
    if t>=101.8:label(c,'Where is move 51?',842,477,29,RED)
def laps(c,t):
    title(c,'Enter once, then count complete laps')
    m=step_at(t,107.45,110.55,1)
    if t>=114.4:m=1+step_at(t,114.4,116.4,5)
    if t>=116.6:m=6+step_at(t,116.6,122.65,45)
    track(c,m,tail=t<112.6);readout(c,floor(m+.0001))
    if t>=110.8:label(c,'Entry   move 1',842,307,29,GOLD)
    if t>=116.6:label(c,'51 − 1 = 50',842,365,34)
    if t>=119.8:label(c,'50 = 10 × 5 + 0',842,427,30,AQUA)
    if t>=123:label(c,'Move 51   state 2',842,502,32,RED)
def zero(c,t):
    title(c,'Zero extra moves leaves the marble at the loop entry')
    m=51 if t<134.65 else 50+step_at(t,134.65,137.2,1)
    track(c,m,False);readout(c,floor(m+.0001))
    label(c,'Moves 1, 6, 11, …, 51',837,329,27,AQUA)
    if t>=131.4:label(c,'Move 50 → move 51' if 134.65<=t<137.2 else 'Each lands on 2.',837,408,31)
    if t>=137.4:label(c,'No edge leads to 1.',837,483,29,GOLD)
def pitfalls(c,t):
    title(c,'Matching one dial can give the wrong period' if t<150.2 else 'Remove the entry move before counting laps')
    if t<150.2:
        n=step_at(t,142.1,145.55,2);gear_pair(c,n)
        label(c,'After two presses',842,225,31)
        if t>=145.8:label(c,'First dial   0',842,322,31,GOLD);label(c,'Second dial   2',842,400,31,AQUA)
    else:
        m=step_at(t,150.2,152.6,1);track(c,m)
        label(c,'One move to enter',845,241,30,GOLD)
        if t>=152.8:label(c,'Then use (51 − 1) ÷ 5.',845,362,27,AQUA)
def finish(c,t):
    title(c,'Record each move and the state it reaches')
    for i in range(7):
        x=151+153*i
        if t<156.55+i*.45:continue
        label(c,'move '+str(i),x,222,25,MUTED,'mm')
        col=GOLD if i==0 else RED if i in (1,6) else AQUA
        c.dot(x,325,42,col);c.dot(x,325,37,STRIP);label(c,str(state(i)),x,327,38,col,'mm')
        if i and t>=156.55+i*.45:
            c.line([(x-107,325),(x-49,325)],METAL,3);arrow(c,(x-107,325),(x-49,325),MUTED)
    if t>=160.6:
        a,b=151+153,151+153*6;c.line([(a,383),(a,420),(b,420),(b,383)],RED,3)
        label(c,'Same full state, five moves apart.',(a+b)/2,477,30,RED,'mm')
    if t>=166.2:label(c,'Move 0 is the starting state.',151,552,27,GOLD)
SCENES=(intro,uses,compass_q,compass_a,dials,dial_sol,machine,laps,zero,pitfalls,finish)
def verify():
    heading='N'
    compass_next={'N':'E','E':'S','S':'W','W':'N'}
    for _ in range(11):heading=compass_next[heading]
    assert heading=='W'
    pair=[(i%2,i%3) for i in range(7)]
    assert len(set(pair[:6]))==6 and pair[6]==pair[0]==(0,0) and pair[2]==(0,2)
    transitions={1:2,2:3,3:4,4:5,5:6,6:2}
    actual=1
    for i in range(102):
        assert state(i)==actual and state_point(i)==POINTS[actual]
        actual=transitions[actual]
    assert state(51)==2 and (51-1)//5==10
