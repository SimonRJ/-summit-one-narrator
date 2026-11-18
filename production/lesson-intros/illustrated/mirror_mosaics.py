"""S083. A real moving reflection, a rigid quarter turn and every legal five-stone mirror mosaic."""
from itertools import product,combinations
from math import sin,cos,pi
from captioned_film import mix,font
PAPER='#e8eef0';INK='#223c48';SILVER='#a5bac3';GRID='#becbd0';GLASS='#f4f5ec';TEAL='#127866';PURPLE='#6d50a4';CORAL='#a64439';GOLD='#aa692b';PALE='#cadfda'
def label(c,s,x,y,size=31,col=INK,anchor='lm'):c.text(s,x,y,size,col,anchor,True)
def title(c,s):
    sz=42
    while font(round(sz*c.scale),True).getlength(s)>1145*c.scale:sz-=1
    label(c,s,60,60,sz)
def pt(x,y):return (392+45*x,340-45*y)
def dash(c,a,b,col):
    for i in range(14):
        u=i/14;v=(i+.52)/14;c.line([(mix(a[0],b[0],u),mix(a[1],b[1],u)),(mix(a[0],b[0],v),mix(a[1],b[1],v))],col,2)
def axes(c,mirror=False):
    for k in range(-5,6):
        c.line([pt(k,-4),pt(k,4)],GRID,1)
    for k in range(-4,5):c.line([pt(-5,k),pt(5,k)],GRID,1)
    c.line([pt(-5,0),pt(5,0)],INK,2);c.line([pt(0,-4),pt(0,4)],TEAL if mirror else INK,4 if mirror else 2)
    for k in (-4,-2,2,4):
        x,y=pt(k,0);label(c,str(k),x,y+19,18,SOFT,'mm')
    for k in (-3,-1,1,3):
        x,y=pt(0,k);label(c,str(k),x-10,y,17,SOFT,'rm')
    label(c,'x',*pt(5.4,0),23);label(c,'y',*pt(.04,4.4),23)
SOFT='#596f7c'
def dot(c,x,y,col,name='',offset=(12,-18)):
    px,py=pt(x,y);c.dot(px,py,8,col)
    if name:label(c,name,px+offset[0],py+offset[1],23,col)
def move(c,a,b,p,col,size=4):
    stop=(mix(a[0],b[0],p),mix(a[1],b[1],p));c.line([pt(*a),pt(*stop)],col,size);return stop
def quarter(c,p):
    pts=[]
    for j in range(49):
        a=pi/2*p*j/48;pts.append(pt(2*cos(a)-3*sin(a),2*sin(a)+3*cos(a)))
    if p:c.line(pts,PURPLE,4)
    a=pi/2*p;x=2*cos(a)-3*sin(a);y=2*sin(a)+3*cos(a)
    c.line([pt(0,0),pt(x,y)],PURPLE,2);dot(c,x,y,PURPLE)
    return x,y
def orbit(p):
    x,y=p;return frozenset(product({x,-x},{y,-y}))
SINGLE=frozenset({(0,0)})
PAIRS=tuple(orbit(p) for p in ((1,0),(2,0),(0,1),(0,2)))
QUADS=tuple(orbit(p) for p in ((1,1),(1,2),(2,1),(2,2)))
SOL=[[SINGLE,q] for q in QUADS]+[[SINGLE,a,b] for a,b in combinations(PAIRS,2)]
def board(c,x,y,u,active=None,axes_on=True):
    active=active or {}
    for i,j in product(range(-2,3),repeat=2):
        xx=x+(i+2)*u;yy=y+(2-j)*u
        c.rect(xx,yy,u,u,GLASS,SILVER,max(1,u*.03))
        if (i,j) in active:
            col=active[(i,j)];p=round(max(1,u*.11),1);c.rect(xx+p,yy+p,u-2*p,u-2*p,col)
    if axes_on:
        c.line([(x+2.5*u,y-5),(x+2.5*u,y+5*u+5)],PURPLE,max(1,u*.023))
        c.line([(x-5,y+2.5*u),(x+5*u+5,y+2.5*u)],TEAL,max(1,u*.023))
def force(c,q,x=165,y=163,u=70):
    points={(1,2):GOLD}
    if q>.18:points[-1,2]=GOLD
    if q>.49:points[1,-2]=GOLD
    if q>.71:points[-1,-2]=GOLD
    board(c,x,y,u,points)
def intro(c,q):
    title(c,'What a mirror does to a single mark')
    force(c,q.after('several reflections',2.7))
    label(c,'A vertical mirror',782,218,30,PURPLE)
    if q.after('several reflections'):label(c,'A horizontal mirror',782,308,30,TEAL)
    if q.after('whole group'):label(c,'One mark forces four.',782,425,33,GOLD)
def exam(c,q):
    title(c,'A flip and a turn move points in different ways')
    axes(c,True);dot(c,2,3,TEAL,'P')
    if q.after('a flip'):dot(c,2*cos(pi*q.after('a flip',1.4)),3,CORAL)
    if q.after('a turn'):quarter(c,q.after('a turn',1.65))
    label(c,'Mirror line',784,213,31,TEAL)
    if q.after('the centre'):label(c,'Turn centre   (0, 0)',784,305,30,PURPLE)
    if q.after('order of moves'):label(c,'Read the moves in order.',784,410,27)
def mirror_q(c,q):
    title(c,'Reflect P in the vertical axis')
    axes(c,True)
    right=q.after('two units to the right',1.1);up=q.after('one unit above',1)
    a=move(c,(0,0),(2,0),right,TEAL)
    if up:a=move(c,(2,0),(2,1),up,TEAL)
    dot(c,*a,TEAL,'P')
    if q.after('vertical mirror passes'):label(c,'P = (2, 1)',799,208,36,TEAL)
    if q.after('other side'):label(c,'Which coordinate changes?',751,352,29,PURPLE)
def mirror_a(c,q):
    title(c,'Both points stay one unit above the horizontal axis')
    axes(c,True);dash(c,pt(-2,1),pt(2,1),CORAL);dot(c,2,1,TEAL,'P')
    p=q.after('two units on the right',2.9);x=2*cos(pi*p)
    dot(c,x,1,PURPLE,'P′' if p>.99 else '',(-45,-22))
    label(c,'Same height   y = 1',773,201,30)
    if q.after('minus two'):label(c,'(2, 1)  →  (−2, 1)',773,311,34,PURPLE)
    if q.after('equally far'):label(c,'2 units from the mirror',773,421,28,TEAL)
def turn_q(c,q):
    title(c,'First rotate, then translate')
    axes(c);dot(c,2,3,TEAL,'P');c.line([pt(0,0),pt(2,3)],TEAL,2)
    # Briefly trace the beginning of the instructed turn without giving away the landing point.
    if q.after('quarter turn'):quarter(c,.43*q.after('quarter turn',1.8))
    label(c,'Start at (2, 3)',785,177,32,TEAL)
    if q.after('anticlockwise'):label(c,'1. Turn 90° anticlockwise.',785,272,27,PURPLE)
    if q.after('five units right'):label(c,'2. Move 5 right, 1 down.',785,367,27,CORAL)
    if q.after('final coordinates'):label(c,'Where do you finish?',785,472,29)
def turn_a(c,q):
    title(c,'The straight move begins at the rotated point')
    axes(c);dot(c,2,3,TEAL,'P');quarter(c,q.after('anticlockwise turn',3.7))
    if q.after('minus three'):dot(c,-3,2,PURPLE,'Q',(-34,-14))
    p=q.after('horizontal move',1.55);h=q.after('downward move',1.1)
    if p:move(c,(-3,2),(2,2),p,CORAL)
    if h:
        pos=move(c,(2,2),(2,1),h,CORAL);dot(c,*pos,CORAL,'R')
    label(c,'Quarter turn',775,171,31,PURPLE)
    if q.after('minus three'):label(c,'(2, 3) → (−3, 2)',775,235,29,PURPLE)
    if q.after('result is two'):label(c,'(−3 + 5, 2 − 1) = (2, 1)',775,344,27,CORAL)
    if q.after('Changing the order'):label(c,'Move first, then turn:',775,454,25);label(c,'(7, 2) → (−2, 7)',775,499,27,SOFT)
def mosaic_q(c,q):
    title(c,'Place exactly five tiles on the fixed board')
    # A single symmetric example demonstrates the condition without exhausting possible answers.
    sel={}
    if q.after('colour exactly five'):sel={(0,0):CORAL}
    if q.after('horizontal and the vertical'):
        p=q.after('horizontal and the vertical',1.75)
        for i,k in enumerate(sorted(QUADS[0])):
            if p>(i+.01)/4:sel[k]=TEAL
    board(c,177,154,71,sel)
    label(c,'Board   5 × 5',793,184,32)
    if q.after('centre-line reflections'):label(c,'Both mirror lines',793,283,30,PURPLE)
    if q.after('fixed board'):label(c,'Different positions count.',793,393,27,TEAL)
def mosaic_a(c,q):
    title(c,'Find the sets of cells that mirrors keep together')
    if q.after('Because five is odd'):
        board(c,165,162,68,{(0,0):CORAL})
        label(c,'5 is odd.',760,190,33,CORAL)
        if q.after('every other group'):label(c,'All other groups have 2 or 4.',760,291,26)
        if q.after('last four'):label(c,'5 = 1 + 4',760,385,31,TEAL);label(c,'5 = 1 + 2 + 2',760,456,31,PURPLE)
        return
    active={(0,0):CORAL};medium=q.after('each noncentral cell',2.9)
    for i,group in enumerate(PAIRS):
        if medium>(i+.01)/4:active.update(dict.fromkeys(group,(TEAL,PURPLE,'#42868f','#967a48')[i]))
    big=q.after('off-axis cell',2.4)
    if big:
        active={(0,0):CORAL}
        for i,k in enumerate(sorted(QUADS[1])):
            if big>(i+.01)/4:active[k]=GOLD
        if q.after('four separate groups'):
            for i,group in enumerate(QUADS):active.update(dict.fromkeys(group,(TEAL,PURPLE,GOLD,'#9c6786')[i]))
    board(c,165,162,68,active)
    label(c,'1 centre tile',760,195,31,CORAL)
    if medium:label(c,'4 pairs on the axes',760,300,29,PURPLE)
    if big:label(c,'4 groups of four off the axes',760,408,26,GOLD)
def ten(c,q):
    title(c,'See all ten patterns on the fixed board')
    limit=4*q.after('four groups of four',1.6)+6*q.after('pair choice',2.15)
    for j,groups in enumerate(SOL):
        if j>=limit:continue
        x=74+(j%5)*240;y=139+(j//5)*175
        active={(0,0):CORAL}
        for g in groups[1:]:active.update(dict.fromkeys(g,TEAL if j<4 else PURPLE))
        board(c,x,y,23,active)
        label(c,str(j+1),x+57,y+136,20,SOFT,'mm')
    if q.after('ten patterns'):label(c,'4 with an off-axis group   +   6 using pairs   =   10',641,548,30,INK,'mm')
def mistakes(c,q):
    if not q.after('off both axes'):
        title(c,'A vertical reflection preserves height');axes(c,True);dot(c,2,1,TEAL,'P')
        p=q.after('changes side',2);dot(c,2*cos(pi*p),1,PURPLE,'P′' if p>.99 else '',(-42,-17));dash(c,pt(-2,1),pt(2,1),CORAL)
        label(c,'The y-coordinate stays 1.',779,288,29)
    else:
        title(c,'One mirror image does not complete an off-axis group')
        force(c,q.after('both reflections',2.6))
        label(c,'Reflect vertically.',786,205,29,PURPLE)
        if q.after('both reflections'):label(c,'Reflect horizontally.',786,304,29,TEAL)
        if q.after('not enough'):label(c,'Keep all four cells.',786,408,30,GOLD)
def finish(c,q):
    title(c,'Follow one marking, then complete its mirror group')
    if not q.after('symmetric pattern'):
        axes(c);dot(c,2,3,TEAL,'P');quarter(c,q.after('turn centre',2.15))
        if q.after('new position'):dot(c,-3,2,PURPLE,'Q',(-36,-18))
        label(c,'Start  (2, 3)',776,213,31,TEAL);label(c,'Turn centre  (0, 0)',776,330,29,PURPLE)
    else:
        active={(0,0):CORAL}
        for j,k in enumerate(sorted(QUADS[3])):
            if q.after('entire groups',1.9)>(j+.01)/4:active[k]=TEAL
        board(c,167,158,70,active);label(c,'Centre + one off-axis group',762,234,28,TEAL)
        if q.after('legal group sizes'):label(c,'1 + 4 = 5',762,341,38)
        if q.after('one case at a time'):label(c,'The other case uses 2 pairs.',762,450,25,PURPLE)
SCENES=(intro,exam,mirror_q,mirror_a,turn_q,turn_a,mosaic_q,mosaic_a,ten,mistakes,finish)
def verify():
    assert (-3+5,2-1)==(2,1) and (-(3-1),2+5)==(-2,7)
    boardset=set(product(range(-2,3),repeat=2))
    listed={frozenset.union(*g) for g in SOL}
    def fixed(g):return {(-x,y) for x,y in g}==g=={(x,-y) for x,y in g}
    exhaustive={frozenset(g) for g in combinations(boardset,5) if fixed(set(g))}
    assert len(listed)==10 and exhaustive==listed
    assert all((0,0) in g and len(g)==5 for g in listed)
