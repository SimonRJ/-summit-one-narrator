"""S082. Choose visible boundary lines for each rectangle; subtract the frames covering both marked cells."""
from itertools import combinations, product
from captioned_film import cue,mix
ID='S082'
ORIGINAL='56bb62b632b1fa518679be9d7023cddfdeef57f270e1387dffcc4ea0fc08098f'
START=(0,14.36,31.96,45.37,57.38,71.91,93.03,118.59,142.42,157.94,173.62)
POSTER=153.9
PAPER='#152833'
WHITE,DIM,LINE,BOARD='#fff2dc','#bfd0d0','#587581','#223a46'
MINT,BLUE,GOLD,RED='#91dcc3','#a6cfff','#ffcf77','#ffac9e'
VERT=tuple(combinations(range(6),2));HORIZ=tuple(combinations(range(5),2))
ALL=tuple((l,r,b,t) for (l,r),(b,t) in product(combinations(range(8),2),combinations(range(6),2)))
A=(3,3); B=(6,2)
def contains(rect,p):
    l,r,b,t=rect;x,y=p
    return l<x<=r and b<y<=t
COVERS=tuple(r for r in ALL if contains(r,A))
BOTH=tuple(r for r in COVERS if contains(r,B))
ALLOWED=tuple(r for r in COVERS if not contains(r,B))
def txt(c,s,x,y,z=30,col=WHITE,anchor='mm'):
    c.text(s,x,y,z,col,anchor,True)
def title(c,s):
    txt(c,s,49,55,41,WHITE,'lm');c.line([(50,100),(1230,100)],LINE,2)
def base(c,x,y,u,w,h,marked=(),number=False):
    # x,y is the lower left corner. The coordinates label cells from 1.
    c.rect(x,y-h*u,w*u,h*u,BOARD,None)
    for i,j,ch,col in marked:
        c.rect(x+(i-1)*u,y-j*u,u,u,col,None)
        txt(c,ch,x+(i-.5)*u,y-(j-.5)*u,round(u*.50),PAPER)
    for i in range(w+1):c.line([(x+i*u,y-h*u),(x+i*u,y)],LINE,2)
    for j in range(h+1):c.line([(x,y-j*u),(x+w*u,y-j*u)],LINE,2)
    if number:
        for i in range(w):txt(c,i+1,x+(i+.5)*u,y+25,22,DIM)
        for j in range(h):txt(c,j+1,x-28,y-(j+.5)*u,22,DIM)
def vertical(c,x,y,u,h,i,col,p=1):
    if p:c.line([(x+i*u,y),(x+i*u,y-h*u*p)],col,5)
def horizontal(c,x,y,u,w,j,col,p=1):
    if p:c.line([(x,y-j*u),(x+w*u*p,y-j*u)],col,5)
def frame(c,x,y,u,rect,col,p=1):
    l,r,b,t=rect
    pts=[(x+l*u,y-b*u),(x+r*u,y-b*u),(x+r*u,y-t*u),(x+l*u,y-t*u),(x+l*u,y-b*u)]
    left=p*2*((r-l)+(t-b))*u
    for a,z in zip(pts,pts[1:]):
        length=abs(z[0]-a[0])+abs(z[1]-a[1])
        if left<=0:break
        f=min(1,left/length);c.line([a,(mix(a[0],z[0],f),mix(a[1],z[1],f))],col,7)
        left-=length
def markboth(c,x=135,y=497,u=69):
    base(c,x,y,u,7,5,((3,3,'A',MINT),(6,2,'B',RED)),True)
def opening(c,t):
    title(c,'A line, a cell and a crossing')
    x,y,u=152,443,84;base(c,x,y,u,5,3)
    if t<3.8:
        vertical(c,x,y,u,3,2,MINT,cue(t,0,1.2));txt(c,'A grid line',934,290,39,MINT)
    elif t<6.7:
        base(c,x,y,u,5,3,((3,2,'',GOLD),));txt(c,'A cell between lines',929,290,35,GOLD)
    elif t<9:
        c.dot(x+3*u,y-2*u,12,BLUE);txt(c,'A crossing point',929,290,35,BLUE)
    else:
        frame(c,x,y,u,(1,4,0,2),MINT,cue(t,9,2.5));txt(c,'Four edges fix a rectangle.',930,287,29,MINT)
def cues(c,t):
    title(c,'Mark the object you are counting')
    x,y,u=155,472,59;markboth(c,x,y,u)
    if t<20:
        for i in range(8):c.dot(x+i*u,y-5*u,7,BLUE)
        txt(c,'Points lie on lines.',924,277,34,BLUE)
    else:
        r=(1,5,1,4) if t<25 else (1,6,1,4)
        frame(c,x,y,u,r,MINT if t<25 else RED,cue(t,20 if t<25 else 25,1.4))
        txt(c,'Which cells lie inside?',924,262,35)
        if t>25:txt(c,'A wider frame also takes B.',924,378,28,RED)
def crossing_q(c,t):
    title(c,'Four columns, two rows: how many crossings?')
    x,y,u=151,430,110;base(c,x,y,u,4,2)
    for i in range(4):txt(c,i+1,x+(i+.5)*u,y+44,24,DIM)
    if t>36:
        for j in range(2):txt(c,j+1,x-38,y-(j+.5)*u,24,DIM)
    if t>40:
        c.dot(x,y,11,GOLD);c.dot(x+4*u,y-2*u,11,GOLD)
        txt(c,'Include the outside lines.',937,319,31,GOLD)
def crossing_a(c,t):
    title(c,'Every vertical line meets three horizontal lines')
    x,y,u=151,435,103;base(c,x,y,u,4,2)
    for i in range(5):vertical(c,x,y,u,2,i,BLUE,cue(t,45.4+i*.22,.55))
    for j in range(3):horizontal(c,x,y,u,4,j,MINT,cue(t,47.7+j*.23,.55))
    for i,j in product(range(5),range(3)):
        p=cue(t,49.6+i*.40+j*.12,.4)
        if p:c.dot(x+i*u,y-j*u,8*p,GOLD)
    txt(c,'5 vertical lines',944,221,32,BLUE)
    if t>47.5:txt(c,'3 horizontal lines',944,314,32,MINT)
    if t>51:txt(c,'5 × 3 = 15 crossings',944,433,35,GOLD)
def rectangle_q(c,t):
    title(c,'Rectangles in five columns and four rows')
    x,y,u=145,476,77;base(c,x,y,u,5,4)
    for at,r,col in ((59,(0,2,1,3),BLUE),(63,(1,5,0,1),GOLD),(66,(0,5,0,4),MINT)):
        if t>at:frame(c,x,y,u,r,col,cue(t,at,.8))
    txt(c,'Any size counts.',924,247,36)
    if t>63:txt(c,'Squares count too.',924,345,32,BLUE)
    if t>68:txt(c,'Which four lines form the edges?',918,449,26,DIM)
def pairs(c,t):
    title(c,'One vertical pair and one horizontal pair')
    x,y,u=143,462,76;base(c,x,y,u,5,4)
    l,r=VERT[int(max(0,t-72)/1.15)%len(VERT)] if t<80 else (1,5)
    b,z=HORIZ[int(max(0,t-80)/1.0)%len(HORIZ)] if t<86 else (0,3)
    vertical(c,x,y,u,4,l,BLUE);vertical(c,x,y,u,4,r,BLUE)
    txt(c,'6 lines → 15 vertical pairs',922,197,30,BLUE)
    if t>75.8:txt(c,'5 + 4 + 3 + 2 + 1 = 15',922,250,25,DIM)
    if t>80:
        horizontal(c,x,y,u,5,b,MINT);horizontal(c,x,y,u,5,z,MINT)
        txt(c,'5 lines → 10 horizontal pairs',918,324,28,MINT)
        if t>81:txt(c,'4 + 3 + 2 + 1 = 10',922,374,25,DIM)
    if t>85:
        frame(c,x,y,u,(l,r,b,z),GOLD,cue(t,85.1,1.15))
        txt(c,'15 × 10 = 150',924,469,41,GOLD)
def question(c,t):
    title(c,'Keep all of A and avoid the interior of B')
    x,y,u=135,497,69
    marked=[(3,3,'A',MINT)] if t>=96 else []
    if t>=99:marked.append((6,2,'B',RED))
    base(c,x,y,u,7,5,marked,True)
    txt(c,'Rows start at the bottom.',949,213,28)
    if t>=99:txt(c,'A: column 3, row 3',949,302,29,MINT)
    if t>=101:txt(c,'B: column 6, row 2',949,384,29,RED)
    if t>=106:frame(c,x,y,u,(2,5,1,4),GOLD,cue(t,106,1.5))
    if t>=110:txt(c,'Touching B’s edge is allowed.',949,483,26,GOLD)
def bounds(c,t):
    title(c,'Count every rectangle that contains A')
    x,y,u=135,497,69;markboth(c,x,y,u)
    side=min(3,int(max(0,t-118.59)/2))
    choices=(range(3),range(3,8),range(3),range(3,6))[side]
    for j,k in enumerate(choices):
        p=cue(t,118.59+side*2+j*.13,.45)
        if side<2:vertical(c,x,y,u,5,k,(BLUE,MINT)[side],p)
        else:horizontal(c,x,y,u,7,k,(GOLD,RED)[side-2],p)
    for i,s in enumerate(('Left: 3 choices','Right: 5 choices','Lower: 3 choices','Upper: 3 choices')):
        if t>=118.59+i*2:txt(c,s,933,168+i*53,26,(BLUE,MINT,GOLD,RED)[i])
    if t>=127:
        if t<134:frame(c,x,y,u,COVERS[(int((t-127)/1.2)*19)%135],WHITE)
        txt(c,'3 × 5 × 3 × 3 = 135',932,418,33,WHITE)
    if t>=134:
        frame(c,x,y,u,(2,6,1,3),RED,cue(t,134,1.4))
        txt(c,'Both cells fit this smallest block.',928,524,25,RED)
def both(c,t):
    title(c,'Subtract only the frames containing both cells')
    x,y,u=135,497,69;markboth(c,x,y,u)
    frame(c,x,y,u,(2,6,1,3),RED)
    side=min(3,int(max(0,t-142.42)/1.22))
    options=(range(3),range(6,8),range(2),range(3,6))
    for k in options[side]:
        if side<2:vertical(c,x,y,u,5,k,GOLD)
        else:horizontal(c,x,y,u,7,k,GOLD)
    txt(c,('3 left edges','2 right edges','2 lower edges','3 upper edges')[side] if t<149.5 else 'Subtract the unwanted group.',942,207,28,GOLD)
    if t>147:txt(c,'3 × 2 × 2 × 3 = 36',934,307,34,RED)
    if t>149.5:
        base(c,x,y,u,7,5,((3,3,'A',MINT),(6,2,'B',RED)),True)
        frame(c,x,y,u,ALLOWED[(int((t-149.5)/1.45)*13)%99],MINT)
        txt(c,'135 − 36 = 99',934,418,42,MINT)
        txt(c,'A is inside. B is outside.',934,501,27)
def pitfalls(c,t):
    title(c,'Count each unordered pair of lines once')
    x,y,u=143,421,88;base(c,x,y,u,5,1)
    for i in range(6):
        vertical(c,x,y,u,1,i,BLUE,cue(t,158+i*.2,.5))
        txt(c,i,x+i*u,y+45,24,DIM)
    txt(c,'5 cells, 6 lines',950,231,34,BLUE)
    if t>163:
        for i in (1,4):vertical(c,x,y,u,1,i,GOLD)
        txt(c,'Lines 1 and 4',949,330,32,GOLD)
    if t>166:txt(c,'Choosing 4 then 1 gives the same edges.',909,433,24)
def recap(c,t):
    title(c,'Set one boundary at a time')
    x,y,u=135,497,69;markboth(c,x,y,u)
    if t<179:
        frame(c,x,y,u,(2,3,2,3),MINT)
        txt(c,'Cells occupy spaces.',940,237,30,MINT)
        txt(c,'Edges lie on grid lines.',940,327,30,BLUE)
    elif t<185:
        frame(c,x,y,u,(0,7,0,5),BLUE,cue(t,179,1.5));frame(c,x,y,u,(1,5,2,4),MINT,cue(t,181,1.2))
        txt(c,'Count the outside lines too.',937,264,29)
    else:
        frame(c,x,y,u,(2,6,1,3),RED,cue(t,185,.9))
        txt(c,'All frames with A: 135',939,227,28,MINT)
        txt(c,'Frames with both: 36',939,324,28,RED)
        txt(c,'Exactly 99 remain.',939,448,37,GOLD)
SCENES=(opening,cues,crossing_q,crossing_a,rectangle_q,pairs,question,bounds,both,pitfalls,recap)
def verify():
    assert len(set(product(range(5),range(3))))==15
    assert len(VERT)==15 and len(HORIZ)==10 and len(set(product(VERT,HORIZ)))==150
    assert len(COVERS)==3*5*3*3==135 and len(BOTH)==3*2*2*3==36 and len(ALLOWED)==99
    assert set(COVERS)==set(BOTH)|set(ALLOWED) and set(BOTH).isdisjoint(ALLOWED)
    assert contains((2,5,1,4),A) and not contains((2,5,1,4),B)
