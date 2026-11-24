"""S097. A cork worktable makes every orientation, boundary and forced domino visible."""
from math import cos, pi, sin
from functools import lru_cache

BACKGROUND=('#f8edcd','#e2c99c')
BRIDGE='At the left edge, put a horizontal domino in the top row. Which cell now forces a second horizontal domino underneath?'
INK='#323e36';BLUE='#315e83';JADE='#397464';CLAY='#b65a36';PAPER='#fff8e5';EDGE='#8a7759';GOLD='#e2ad52'
TITLES=['Turn a five-square shape','Follow the five cells','Two corners leave the board',
        'Count what the tiles can cover','Begin at the left edge','Build with two block types','Count every tiling once']
SHAPE=[(0,0),(1,0),(2,0),(3,0),(0,1)]


def check_maths():
    from itertools import product
    from math import comb
    assert len(set(SHAPE))==len({(-y,x) for x,y in SHAPE})==5
    assert divmod(5*3-2,3)==(4,1)
    @lru_cache(None)
    def fill(mask,vertical):
        if vertical>3:return 0
        free=next((i for i in range(18) if not mask&(1<<i)),None)
        if free is None:return int(vertical==3)
        row,col=divmod(free,9); total=0
        if row==0 and not mask&(1<<(free+9)):total+=fill(mask|(1<<free)|(1<<(free+9)),vertical+1)
        if col<8 and not mask&(1<<(free+1)):total+=fill(mask|(1<<free)|(1<<(free+1)),vertical)
        return total
    choices=[z for z in product('VH',repeat=6) if z.count('V')==3]
    assert fill(0,0)==len(choices)==comb(6,3)==20
    assert all(sum(1 if slot=='V' else 2 for slot in seq)==9 for seq in choices)


def text(a,s,x,y,size=33,color=INK,op=1):
    a.text(s,x,y,size,color,opacity=op,bold=True)


def cell(a,x,y,side,fill=PAPER):
    a.box(x,y,side,side,fill=fill,edge=EDGE,radius=2,stroke=2)


def poly(a,cx,cy,side,angle,mark=0):
    for k,(sx,sy) in enumerate(SHAPE):
        def rot(u,v):
            u=(u-1.65)*side;v=(v-.85)*side
            return (cx+u*cos(angle)-v*sin(angle),cy+u*sin(angle)+v*cos(angle))
        points=[rot(sx,sy),rot(sx+1,sy),rot(sx+1,sy+1),rot(sx,sy+1)]
        a.polygon(points,CLAY if k==4 else JADE,outline=INK,width=3)
        if mark>.5:
            tx,ty=rot(sx+.5,sy+.5);text(a,str(k+1),tx,ty,29,PAPER,mark)


def grid(a,x,y,cols,rows,s):
    for row in range(rows):
        for col in range(cols):cell(a,x+col*s,y+row*s,s)


def holes(a,x,y,s,op):
    for col,row in ((0,0),(4,2)):
        xx=x+col*s;yy=y+row*s
        a.box(xx+1,yy+1,s-2,s-2,fill='#d2b78e',edge=CLAY,stroke=3,radius=1,opacity=op)
        for m in (0,1):
            a.line([(xx+13,yy+(13 if m==0 else s-13)),(xx+s-13,yy+(s-13 if m==0 else 13))],CLAY,3,op)


def domino(a,x,y,s,vertical,op=1):
    w,h=(s,2*s) if vertical else (2*s,s)
    color=BLUE if vertical else JADE
    a.box(x+3,y+3,w-6,h-6,fill=color,edge=INK,stroke=2,radius=max(4,s*.13),opacity=op)
    for cx,cy in ([(x+s/2,y+s/2),(x+s/2,y+1.5*s)] if vertical else [(x+s/2,y+s/2),(x+1.5*s,y+s/2)]):
        a.dot(cx,cy,max(3,s/12),PAPER,op)


def strip(a,x,y,s,sequence,limit=6):
    grid(a,x,y,9,2,s);col=0
    for i,block in enumerate(sequence):
        if i>=limit:break
        if block=='V':domino(a,x+col*s,y,s,True);col+=1
        else:
            domino(a,x+col*s,y,s,False);domino(a,x+col*s,y+s,s,False);col+=2


def draw(a,n,t):
    a.label(TITLES[n-1],76,74,46,INK,bold=True);a.line([(76,119),(1200,119)],EDGE,3)
    if n in (1,2):
        if n==1:
            turn=t.reveal('solid piece turning',2.0)
            poly(a,610,350,90,pi/2*turn)
            text(a,'How many unit squares?',640,570,38,INK,t.reveal('How many'))
        else:
            poly(a,345,345,78,0,t.reveal('extra cell'))
            turn=t.reveal('quarter turn moves',1.75)
            poly(a,874,340,68,pi/2*turn,t.reveal('moves each cell'))
            a.line([(584,344),(652,344),(630,329)],BLUE,5)
            a.line([(652,344),(630,360)],BLUE,5)
            text(a,'5 squares before and after',640,570,38,JADE,t.reveal('preserves the five squares'))
    elif n in (3,4):
        x,y,s=111,216,83;grid(a,x,y,5,3,s)
        holes(a,x,y,s,t.reveal('corner cells removed') if n==3 else 1)
        if n==3:
            for col,row in ((0,0),(1,0),(0,1)):cell(a,878+col*60,245+row*60,60,JADE)
            text(a,'3 squares per piece',949,419,32,INK,t.reveal('three unit squares'))
            text(a,'Can the pieces cover the board?',640,560,39,BLUE,t.reveal('Can you tile'))
        else:
            text(a,'15 − 2 = 13',915,219,43,INK,t.reveal('removing the corners'))
            for j in range(13):
                group,unit=divmod(j,3)
                gx=657+(group%2)*216 if group<4 else 1119
                gy=305+(group//2)*77 if group<4 else 346
                xx=gx+unit*47
                shade=JADE if group<4 else CLAY
                a.box(xx,gy,41,45,fill=shade,edge=INK,radius=4,opacity=t.reveal('thirteen to be divisible'))
                if j==12:text(a,'1',xx+20,gy+22,25,PAPER,t.reveal('leftover cells'))
            text(a,'13 = 4 × 3 + 1',916,487,38,BLUE,t.reveal('leftover cells'))
            text(a,'One cell would remain',640,567,35,CLAY,t.reveal('tiling is impossible'))
    elif n==5:
        x,y,s=286,227,76;grid(a,x,y,9,2,s)
        for k in range(9):text(a,str(k+1),x+(k+.5)*s,y-28,23,EDGE)
        hor=t.reveal('horizontal domino',.8);domino(a,x,y,s,False,hor)
        a.box(x+4,y+s+4,s-8,s-8,fill='#efd08e',edge=CLAY,radius=4,opacity=hor)
        text(a,'?',x+s/2,y+1.5*s,42,INK,hor)
        text(a,'2 rows × 9 columns',640,469,37,INK)
        text(a,'Exactly 3 vertical dominoes',640,547,36,BLUE,t.reveal('three dominoes'))
    elif n==6:
        grid(a,119,235,3,2,62);grid(a,411,235,3,2,62)
        domino(a,119,235,62,True,t.reveal('vertical domino fills'))
        domino(a,411,235,62,False,t.reveal('horizontal domino there'))
        domino(a,411,297,62,False,t.reveal('another horizontal domino'))
        text(a,'1 column',213,410,28,BLUE,t.reveal('fills one column'))
        text(a,'2 columns',505,410,28,JADE,t.reveal('another horizontal domino'))
        text(a,'One complete arrangement',930,183,30,INK,t.reveal('three vertical dominoes'))
        a0=t.reveal('three vertical dominoes',1.45);a1=t.reveal('three pairs of horizontal dominoes',1.75)
        strip(a,693,258,51,'VVVHHH',min(6,int(a0*3+.05)+int(a1*3+.05)))
        if t.reveal('among the six blocks')>.5:
            text(a,'V    V    V    H    H    H',923,432,29,INK)
        text(a,'A horizontal pair counts as one block',640,562,34,JADE,t.reveal('horizontal pairs'))
    else:
        for j,(seq,top) in enumerate([('VVVHHH',196),('VHVHVH',385)]):
            strip(a,135,top,62,seq)
            text(a,' '.join(seq),952,top+40,36,INK)
        text(a,'V = one vertical     H = two horizontal',640,546,30,INK)
        text(a,'Choose 3 of 6 block positions → 20 tilings',640,600,36,BLUE,t.reveal('choices is twenty'))


def poster(draw):
    return draw(8,1.5)
