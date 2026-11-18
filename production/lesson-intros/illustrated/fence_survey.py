"""S053. Slide a measured boundary, then reflect a three-sided pen across its unfenced wall."""
from math import floor
from captioned_film import cue,mix,font
ID='S053'
ORIGINAL='9a630de4d77132a13b25d2a1508b68605a79834c48a39329857119672e7b3da8'
START=(0,17.24,34.04,47.30,59.94,73.36,90.0,105.49,130.11,145.79,160.83)
POSTER=135.3
PAPER='#edf0df';INK='#2a382d';SOFT='#566653';GRASS='#c2d5a7';GRID='#9aab83';RUST='#9e4b35'
WALL='#526478';BLUE='#385d7e';FENCE='#854d31';POST='#503d32';LIGHT='#fff9e5';HEDGE='#507a4c';GHOST='#dbe4cd'
def label(c,s,x,y,size=30,col=INK,anchor='lm'):c.text(s,x,y,size,col,anchor,True)
def title(c,s):
    sz=42
    while font(round(sz*c.scale),True).getlength(s)>1145*c.scale:sz-=1
    label(c,s,63,60,sz)
def fmt(n):
    return str(int(round(n))) if abs(n-round(n))<.005 else f'{n:.1f}'
def dim(c,a,b,s,col=SOFT,side='h'):
    x,y=a;u,v=b;c.line([a,b],col,1.8)
    if side=='h':
        for xx in (x,u):c.line([(xx,y-5),(xx,y+5)],col,2)
        label(c,s,(x+u)/2,y+22,24,col,'mm')
    else:
        for yy in (y,v):c.line([(x-5,yy),(x+5,yy)],col,2)
        label(c,s,x-10,(y+v)/2,24,col,'rm')
def grid(c,x,y,a,b,u,fill=GRASS,side_col=GRID):
    c.rect(x,y,a*u,b*u,fill)
    for i in range(1,int(a)+1):
        if i<a:c.line([(x+i*u,y),(x+i*u,y+b*u)],side_col,1)
    for j in range(1,int(b)+1):
        if j<b:c.line([(x,y+j*u),(x+a*u,y+j*u)],side_col,1)
def stake_edge(c,a,b):
    c.line([a,b],FENCE,5)
    for x,y in (a,b):c.rect(x-3.5,y-3.5,7,7,POST)
def wall(c,x,y,w):
    c.rect(x-14,y-14,w+28,14,WALL)
    for i in range(0,int(w)+9,21):c.line([(x-9+i,y-13),(x-9+i,y-6)],'#8e9baa',1.3)
    for i in range(9,int(w)+12,21):c.line([(x-9+i,y-6),(x-9+i,y-1)],'#8e9baa',1.3)
def field(c,a,b,u,cx=423,cy=322,against=False,dimensions=True,units=' m',shade=GRASS):
    w=a*u;h=b*u;x=cx-w/2;y=cy-h/2
    grid(c,x,y,a,b,u,shade)
    corners=[(x,y),(x+w,y),(x+w,y+h),(x,y+h)]
    if against:wall(c,x,y,w)
    else:stake_edge(c,corners[0],corners[1])
    for j in (1,2,3):stake_edge(c,corners[j],corners[(j+1)%4])
    if dimensions:
        dim(c,(x,y+h+16),(x+w,y+h+16),fmt(a)+units)
        dim(c,(x-14,y),(x-14,y+h),fmt(b)+units,side='v')
    return x,y,w,h
def intro(c,t):
    title(c,'What can change when the fence length stays fixed?')
    b=2+3*cue(t,6.0,5.8);a=11-b;field(c,a,b,47)
    label(c,'Boundary   22 m',835,211,33,FENCE)
    if t>=6:label(c,'Length + width = 11 m',835,310,27)
    if t>=10.6:label(c,'Area   '+fmt(a*b)+' m²',835,405,34,HEDGE)
def use(c,t):
    title(c,'Choose the boundary the question actually gives')
    use_wall=t>=27.8;field(c,8,3,45,430,315,use_wall)
    if not use_wall:
        label(c,'All four sides fenced',830,209,28,FENCE)
        if t>=21.8:label(c,'2(8 + 3) = 22 m',830,321,31)
    else:
        label(c,'One side is a wall',830,209,29,BLUE)
        label(c,'8 + 3 + 3 = 14 m',830,321,31,FENCE)
    if t>=30.8:label(c,'Count each fenced side.',830,431,26)
def basic(c,t,worked):
    title(c,'Trace the two lengths and the two widths')
    x,y,w,h=field(c,8,3,57,407,310,False,False)
    # Draw the two sides of one half-perimeter over the actual boundary.
    p=cue(t,50.2 if worked else 40.2,2.7)
    distance=11*p
    c.line([(x,y),(x+min(distance,8)*57,y)],RUST,7)
    if distance>8:c.line([(x+w,y),(x+w,y+(distance-8)*57)],RUST,7)
    dim(c,(x-13,y),(x-13,y+h),'3 m',side='v')
    dim(c,(x,y+h+18),(x+w,y+h+18),'8 m' if worked and t>=53.4 else '? m')
    label(c,'Perimeter   22 m',835,195,32,FENCE)
    if t>=(50.2 if worked else 40.2):label(c,'Halfway around   11 m',835,286,26,RUST)
    if worked and t>=53.4:label(c,'Length   11 − 3 = 8 m',835,371,27)
    if worked and t>=56.4:label(c,'8 × 3 = 24 m²',835,463,31,HEDGE)
def basic_q(c,t):basic(c,t,False)
def basic_a(c,t):basic(c,t,True)
def compare(c,t):
    title(c,'Use 22 units of boundary for both rectangles')
    field(c,9,2,41,347,337,False,True,'')
    if t>=66.6:field(c,6,5,41,957,337,False,True,'')
    label(c,'9 + 2 = 11',347,165,30,FENCE,'mm')
    if t>=68.6:label(c,'6 + 5 = 11',957,165,30,FENCE,'mm')
def transfer(c,t):
    title(c,'Shorten the longer side by one. Extend the shorter side by one.')
    # Three metres move smoothly within the family of rectangles having a+b=11.
    b=3+cue(t,77,2.5)+cue(t,81.9,1.7);a=11-b
    field(c,a,b,48,397,323,False,True,'')
    label(c,'Side sum   11',822,179,31,FENCE)
    if t>=77:label(c,'3 × 8 = 24',822,265,31)
    if t>=79.6:label(c,'4 × 7 = 28',822,338,31)
    if t>=83.6:label(c,'5 × 6 = 30',822,410,31,HEDGE)
    if t>=86.6:label(c,'Largest area   30',822,495,29,HEDGE)
def pen(c,t):
    title(c,'Use 38 metres of fence. The wall closes the fourth side.')
    b=6+2*cue(t,92,4);a=38-2*b
    field(c,a,b,20,421,310,True)
    label(c,'Along the wall   no fence',801,182,27,BLUE)
    if t>=95.2:label(c,'Two widths + one length',801,276,28,FENCE)
    if t>=97.2:label(c,'Whole metres only',801,364,30)
    if t>=99:label(c,'Which pen is largest?',801,457,30,HEDGE)
def reflection(c,t):
    title(c,'Reflect a copy across the wall to double the area')
    u=16;b=8;a=22;x=331-a*u/2;y=313
    p=cue(t,114,3.7)
    if p:
        grid(c,x,y-b*u*p,a,b*p,u,GHOST,'#bdcbb0');c.line([(x,y),(x,y-b*u*p),(x+a*u,y-b*u*p),(x+a*u,y)],HEDGE,2)
    grid(c,x,y,a,b,u);wall(c,x,y,a*u)
    c.line([(x,y),(x,y+b*u),(x+a*u,y+b*u),(x+a*u,y)],FENCE,5)
    if t>=105.6:dim(c,(x-15,y),(x-15,y+b*u),'x',side='v')
    if t>=109.8:dim(c,(x,y+b*u+13),(x+a*u,y+b*u+13),'38 − 2x')
    if t>=118.4:
        xx=x+a*u+17;c.line([(xx,y-b*u),(xx+9,y-b*u),(xx+9,y+b*u),(xx,y+b*u)],HEDGE,2);label(c,'2x',xx+22,y,25,HEDGE)
    label(c,'Fence   x + x + length = 38',727,164,26,FENCE)
    if t>=114:label(c,'Two pens   (2x)(38 − 2x)',727,263,27,HEDGE)
    if t>=118.4:label(c,'Factor sum   38',727,338,28)
    if t>=124:label(c,'2x must be even.',727,419,28,RUST)
    if t>=126.2:label(c,'Closest to 19   18 or 20',727,498,27)
def best(c,t):
    title(c,'Two different pens tie for the greatest area')
    field(c,20,9,16,332,323,True);field(c,18,10,16,948,323,True)
    if t>=133.2:
        label(c,'20 × 9 = 180 m²',332,158,30,HEDGE,'mm');label(c,'18 × 10 = 180 m²',948,158,30,HEDGE,'mm')
    if t>=136.6:label(c,'Next widths out   8 × 22 and 11 × 16 each give 176 m².',636,533,27,RUST,'mm')
def pitfalls(c,t):
    title(c,'The continuous optimum sits between two legal widths')
    x=9.5 if t>=153.4 else 9
    field(c,38-2*x,x,17,381,316,True)
    label(c,'Fence   2x + length = 38 m',767,198,26,FENCE)
    if t>=153.4:label(c,'Balance occurs at x = 9.5 m.',767,289,26,BLUE)
    if t>=156.6:label(c,'Test x = 9 and x = 10.',767,386,29,HEDGE)
def finish(c,t):
    title(c,'How the area changes with the whole-number width')
    x0,x1,y0,y1=155,787,465,157
    def pt(w,a):return x0+(x1-x0)*(w-1)/17,y0-(y0-y1)*a/190
    c.line([(x0,y1),(x0,y0),(x1,y0)],SOFT,2)
    label(c,'area (m²)',x0,y1-28,24)
    for v in (0,60,120,180):
        _,y=pt(1,v);c.line([(x0,y),(x1,y)],GRID,1);label(c,str(v),x0-10,y,20,SOFT,'rm')
    for w in (1,5,9,10,14,18):
        x,_=pt(w,0);label(c,str(w),x,y0+22,20,SOFT,'mm')
    label(c,'width (m)',x1,y0+61,23,SOFT,'rm')
    limit=1+17*cue(t,164,6.6)
    for w in range(1,19):
        if w<=limit:c.dot(*pt(w,w*(38-2*w)),7 if w in (9,10) else 5,RUST if w in (9,10) else HEDGE)
    label(c,'Area   x(38 − 2x)',846,208,29,HEDGE)
    if t>=169.4:label(c,'Highest two dots',846,309,29,RUST)
    if t>=172.8:label(c,'9 m and 10 m',846,382,30);label(c,'180 m² each',846,461,34,HEDGE)
SCENES=(intro,use,basic_q,basic_a,compare,transfer,pen,reflection,best,pitfalls,finish)
def verify():
    assert 3*(22//2-3)==24
    assert [(a,11-a) for a in range(1,6) if a*(11-a)==30]==[(5,6)]
    choices={w:w*(38-2*w) for w in range(1,19)}
    assert max(choices.values())==180 and [w for w in choices if choices[w]==180]==[9,10]
    assert choices[8]==choices[11]==176
    assert all(2*w+(38-2*w)==38 and 2*area==2*w*(38-2*w) for w,area in choices.items())
