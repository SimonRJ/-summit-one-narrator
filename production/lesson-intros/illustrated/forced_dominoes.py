"""S036. A tile workshop. Every two-row strip and every block choice is an actual exact cover."""
from itertools import combinations
from math import cos,sin,pi
from captioned_film import mix
PAPER='#42342f';CREAM='#fff0d2';WOOD='#755346';LINE='#382e2c';SAND='#dcb58c';SEA='#9ed8cf';CORAL='#f6af92';GHOST='#a98572'
def heading(c,s):c.text(s,61,65,42,CREAM,'lm',True)
def note(c,s,x,y,size=32,col=CREAM):c.text(s,x,y,size,col,'lm',True)
def board(c,x,y,w,h,u,missing=()):
    c.rect(x-7,y-7,w*u+14,h*u+14,WOOD)
    for col in range(w):
        for row in range(h):
            if (col,row) in missing:continue
            c.rect(x+col*u+1,y+row*u+1,u-2,u-2,'#604a40',GHOST,1.6)
def tile(c,x,y,w,h,u,col=CREAM):
    pad=max(1,u*.045)
    c.rect(x+pad+1.5,y+pad+3,w*u-pad*2,h*u-pad*2,LINE)
    c.rect(x+pad,y+pad,w*u-pad*2,h*u-pad*2,col,LINE,1.5)
    for k in range(1,w):c.line([(x+k*u,y+pad+1),(x+k*u,y+h*u-pad-1)],GHOST,max(1,u*.025))
    for k in range(1,h):c.line([(x+pad+1,y+k*u),(x+w*u-pad-1,y+k*u)],GHOST,max(1,u*.025))
def outlines(picks):
    parts=[];x=0
    for i in range(5):
        if i in picks:parts.append([(x,0,1,2)]);x+=1
        else:parts.append([(x,0,2,1),(x,1,2,1)]);x+=2
    return parts
ALL=list(combinations(range(5),2))
def strip(c,picks,x,y,u,built=5,hot=None):
    board(c,x,y,8,2,u)
    for i,part in enumerate(outlines(picks)):
        p=max(0,min(1,built-i))
        if not p:continue
        for cx,cy,w,h in part:
            tile(c,x+cx*u,y+cy*u-(1-p)*u*.8,w,h,u,SEA if hot==i or hot is None and len(part)==1 else CREAM)
def shape(c,theta,x=382,y=335,u=82,attached=1):
    coords=[(-1.25,-.75),(-.25,-.75),(.75,-.75),(-1.25,.25)]
    def pt(a,b):return x+u*(a*cos(theta)-b*sin(theta)),y+u*(a*sin(theta)+b*cos(theta))
    for i,(a,b) in enumerate(coords):
        if i==3 and not attached:continue
        quad=[pt(a,b),pt(a+1,b),pt(a+1,b+1),pt(a,b+1)]
        c.poly(quad,SEA if i==3 else CREAM,LINE,3)
        if i==3:c.dot(*pt(a+.5,b+.5),8,LINE)
def intro(c,q):
    heading(c,'Can every square be covered exactly once?')
    x,y,u=175,209,78;board(c,x,y,4,3,u)
    p=q.after('Slide a domino',2.3);tile(c,mix(73,x,p),mix(135,y,p),2,1,u)
    if q.after('two cells'):note(c,'1 domino covers 2 cells.',722,225,33,SEA)
    fill=q.after('last gap',1.6)
    for j,(dx,dy) in enumerate(((2,0),(0,1),(2,1),(0,2))):
        phase=max(0,min(1,fill*4-j))
        if phase:tile(c,x+dx*u,y+dy*u-(1-phase)*36,2,1,u)
    last=q.after('every cell',1.2)
    if last:tile(c,x+2*u+(1-last)*106,y+2*u,2,1,u,SEA)
    if q.after('every cell'):note(c,'Inside the board. No overlaps.',722,364,30)
def exam(c,q):
    heading(c,'Test the first move at a boundary')
    x,y,u=163,247,71;board(c,x,y,6,2,u)
    p=q.after('try a move',1.2);tile(c,x,y-(1-p)*u,2,1,u)
    if q.after('first move'):
        c.line([(x+3,y+u+3),(x+u-3,y+u+3),(x+u-3,y+2*u-3),(x+3,y+2*u-3),(x+3,y+u+3)],SEA,5)
    if q.after('next one'):tile(c,x,y+u,2,1,u,SEA)
    note(c,'What can go below it?',712,293,37)
def basic(c,q):
    heading(c,'How many squares survive a quarter turn?')
    shape(c,0,attached=q.after('Attach one more'))
    if q.after('one more'):note(c,'Three in a row, one below.',719,249,32)
    if q.after('quarter turn'):note(c,'Predict before turning.',719,374,32,SEA)
def rotate(c,q):
    heading(c,'Follow the marked square')
    p=q.after('as the piece turns',2.8);shape(c,pi/2*p)
    note(c,'The marked cell moves with the piece.',698,226,26,SEA)
    if q.after('Four squares before'):note(c,'4 before',737,348,41)
    if q.after('four squares afterwards'):note(c,'4 afterwards',737,428,41,SEA)
def missing(c,remove,fill=0):
    x,y,u=182,197,77
    board(c,x,y,4,3,u,[(3,0)] if remove else [])
    if remove:
        tile(c,x+3*u+56*remove,y-68*remove,1,1,u,CORAL)
    for j in range(3):
        p=max(0,min(1,fill-j))
        if p:tile(c,x-(1-p)*72,y+u*j,3,1,u,CREAM)
    if fill>=3:
        for row in (1,2):c.dot(x+3.5*u,y+(row+.5)*u,8,SEA)
def medium(c,q):
    heading(c,'Remove exactly one corner square')
    p=q.after('Lift out',1.55);missing(c,p)
    note(c,'4 columns × 3 rows',727,225,34)
    if q.after('three squares'):note(c,'Each piece covers 3 cells.',705,346,30,SEA)
    if q.after('board that remains'):note(c,'Can they cover it?',724,446,34)
def remainder(c,q):
    heading(c,'Can eleven cells form groups of three?')
    p=q.after('Place three pieces',2.4);missing(c,1,3*p)
    note(c,'12 − 1 = 11',735,201,41)
    if q.after('nine cells'):note(c,'3 × 3 = 9',735,305,38)
    if q.after('leaves two'):note(c,'2 cells remain',735,403,38,SEA)
    if q.after('No arrangement'):note(c,'11 is not divisible by 3.',730,497,29,CORAL)
def puzzle(c,q):
    heading(c,'Tile a 2 by 8 board with exactly two uprights')
    x,y,u=120,246,73;board(c,x,y,8,2,u)
    if q.after('two dominoes'):
        tile(c,832,216,1,2,54,SEA);tile(c,928,216,1,2,54,SEA)
        note(c,'Two uprights',800,379,30,SEA)
    if q.after('leftmost column'):
        c.line([(x,y-7),(x+u,y-7),(x+u,y+2*u+7),(x,y+2*u+7),(x,y-7)],CORAL,5)
def blocks(c,q):
    heading(c,'The first empty column forces the next move')
    x,y,u=129,206,67;board(c,x,y,3,2,u)
    if q.after('upright domino'):tile(c,x,y,1,2,u,SEA)
    c.text('1 column',x+1.5*u,420,31,SEA,bold=True)
    x=546;board(c,x,y,3,2,u)
    p=q.after('sideways domino',1.05)
    if p:tile(c,x,y-(1-p)*56,2,1,u)
    p=q.after('directly below',1.25)
    if p:tile(c,x,y+u+(1-p)*62,2,1,u)
    if q.after('single block'):c.text('2 columns',x+1.5*u,420,31,CORAL,bold=True)
    note(c,'Upright',920,240,35,SEA)
    if q.after('another sideways'):note(c,'or a forced pair',886,345,30,CORAL)
def ten(c,q):
    heading(c,'Two upright positions among five blocks')
    if not q.after('ten choices'):
        x,y,u=150,237,71;built=2+3*q.after('other six columns',1.9)
        strip(c,(0,1),x,y,u,built)
        note(c,'2 single columns',815,224,31,SEA)
        if q.after('three double blocks'):note(c,'3 double columns',815,310,30)
        if q.after('five blocks'):note(c,'5 blocks altogether',789,419,32,CORAL)
        return
    p=q.after('ten choices',2.4)
    for i,ch in enumerate(ALL):
        alpha=max(0,min(1,p*11-i))
        if not alpha:continue
        x=94+i%5*237;y=178+i//5*168
        strip(c,ch,x,y,23,5*alpha)
        c.text(str(i+1),x+92,y+73,23,SAND)
    c.text('Each strip has two teal uprights and three sideways pairs.',640,533,29,CREAM,bold=True)
def duplicates(c,q):
    heading(c,'Swap the pieces. The tile edges stay put.')
    x,y,u=237,216,86
    board(c,x,y,2,2,u)
    # Pull the pieces aside, swap their heights and return them to the identical occupied edges.
    p=q.after('Exchanging',2.4);excursion=sin(pi*p)
    for i in range(2):
        yy=mix(i,1-i,p)
        tile(c,x+(1 if i==0 else -1)*u*.95*excursion,y+yy*u,2,1,u)
    note(c,'Same occupied edges',681,255,37)
    if q.after('same tiling twice'):note(c,'One tiling',681,380,44,SEA)
def recap(c,q):
    heading(c,'Recover the sequence from the finished strip')
    x,y,u=141,243,75
    p=q.after('from left to right',4.1);highlight=min(4,int(p*5))
    strip(c,(1,4),x,y,u,5,highlight)
    parts=outlines((1,4))
    for i,part in enumerate(parts):
        if i<=highlight:
            x0=part[0][0];width=part[0][2]
            c.text('upright' if len(part)==1 else 'pair',x+(x0+width/2)*u,y+2*u+36,22,SEA if i==highlight else CREAM)
    note(c,'Read one block at a time.',790,254,30)
    if q.after('every tiling exactly once'):note(c,'10 distinct tilings',790,391,37,SEA)
SCENES=(intro,exam,basic,rotate,medium,remainder,puzzle,blocks,ten,duplicates,recap)
def verify():
    boardset={(x,y) for x in range(8) for y in range(2)}
    def search(rest,placed=(),vertical=0):
        if not rest:return {frozenset(placed)} if vertical==2 else set()
        x,y=min(rest);result=set()
        for dx,dy in ((1,0),(0,1)):
            d=frozenset(((x,y),(x+dx,y+dy)))
            if d<=rest and vertical+dy<=2:result|=search(rest-d,placed+(d,),vertical+dy)
        return result
    pics=set()
    for ch in ALL:
        dominoes=[]
        for part in outlines(ch):
            for x,y,w,h in part:dominoes.append(frozenset((x+i,y+j) for i in range(w) for j in range(h)))
        assert set.union(*(set(d) for d in dominoes))==boardset and sum(map(len,dominoes))==16
        pics.add(frozenset(dominoes))
    assert len(pics)==10 and pics==search(boardset)
    assert 4*3-1==3*3+2
