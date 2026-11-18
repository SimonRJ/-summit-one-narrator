"""Trace the exact oriented boundary of each polyomino, including the loop around its hole."""
from collections import Counter
from math import hypot
from captioned_film import cue,mix

ID='S043'
ORIGINAL='c3a3dd134f8dae38605a29e9e9a6db8779a54aaf43d899380ffc71264f6e8553'
START=(0,13.88,29.24,41.86,52.90,68.39,87.10,104.19,126.26,140.82,154.58)
POSTER=122.8
PAPER='#102f36';WHITE='#f3f5d8';SAGE='#a2beb0';FILL='#477975';GRID='#76a098';ORANGE='#ffb760';AQUA='#84eade';ROSE='#ffa2a1';DARK='#193c40'
L={(0,0),(0,1),(0,2),(1,2),(2,2),(3,2)}
BOARD={(x,y) for x in range(6) for y in range(6)}
HOLE={(2,2),(3,2)};CORNER=(5,0)
HOLED=BOARD-HOLE
CUT=HOLED-{CORNER}
RECT={(x,y) for x in range(2) for y in range(3)}
def title(c,s):c.text(s,64,61,39 if len(s)>49 else 43,WHITE,'lm',True)
def note(c,s,x,y,size=32,col=WHITE):c.text(s,x,y,size,col,'lm',True)
def sheet(c,x0=66,y0=127,x1=680,y1=566):
    for x in range(x0,x1+1,24):c.line([(x,y0),(x,y1)],'#1e4145',1)
    for y in range(y0,y1+1,24):c.line([(x0,y),(x1,y)],'#1e4145',1)
def sides(x,y):
    a=(x,y);b=(x+1,y);d=(x,y+1);e=(x+1,y+1)
    return ((a,b),(b,e),(e,d),(d,a))
def edgekey(a,b):return tuple(sorted((a,b)))
def incidences(cells):
    return Counter(edgekey(a,b) for x,y in cells for a,b in sides(x,y))
def loops(cells):
    count=incidences(cells)
    nxt={a:b for x,y in sorted(cells) for a,b in sides(x,y) if count[edgekey(a,b)]==1}
    result=[]
    while nxt:
        start=min(nxt,key=lambda p:(p[1],p[0]))
        points=[start];cur=start
        while True:
            cur=nxt.pop(cur);points.append(cur)
            if cur==start:break
        result.append(points)
    return sorted(result,key=len,reverse=True)
def screen(point,ox,oy,u):return (ox+u*point[0],oy+u*point[1])
def cell(c,x,y,ox,oy,u,fill=FILL):
    X,Y=screen((x,y),ox,oy,u);c.rect(X,Y,u,u,fill,GRID,1.5)
def cells(c,shape,ox,oy,u):
    for x,y in sorted(shape):cell(c,x,y,ox,oy,u)
def ink(c,path,ox,oy,u,amount,col,width=7,tip=True):
    points=[screen(p,ox,oy,u) for p in path];remaining=sum(hypot(b[0]-a[0],b[1]-a[1]) for a,b in zip(points,points[1:]))*max(0,min(1,amount))
    traced=[points[0]]
    for a,b in zip(points,points[1:]):
        d=hypot(b[0]-a[0],b[1]-a[1])
        if remaining<d:
            traced.append((mix(a[0],b[0],remaining/d),mix(a[1],b[1],remaining/d)))
            break
        traced.append(b);remaining-=d
    c.line(traced,col,width)
    if tip and amount>0:
        x,y=traced[-1]
        c.dot(x,y,8.5,WHITE);c.dot(x,y,4.5,col)
def contacts(c,shape,ox,oy,u,t,start,step=.35):
    shared=sorted(edge for edge,n in incidences(shape).items() if n==2)
    for i,edge in enumerate(shared):
        p=cue(t,start+i*step,.33)
        if p:ink(c,edge,ox,oy,u,p,ROSE,6,False)
def outline(c,shape,ox,oy,u,amount,col=ORANGE):
    ink(c,loops(shape)[0],ox,oy,u,amount,col)
def dimension(c,p,q,label,horizontal=True):
    x,y=p;X,Y=q;c.line([p,q],SAGE,2)
    if horizontal:
        for a in (x,X):c.line([(a,y-8),(a,y+8)],SAGE,2)
        c.text(label,(x+X)/2,y+22,26,WHITE,bold=True)
    else:
        for b in (y,Y):c.line([(x-8,b),(x+8,b)],SAGE,2)
        c.text(label,x-13,(y+Y)/2,26,WHITE,'rm',True)
def intro(c,t):
    title(c,'Which edges count towards the perimeter?')
    sheet(c,68,154,1210,524)
    if t<8:
        join=cue(t,3.7,2.1);ox=351;oy=237;u=126
        for off in (0,mix(2.8,1,join)):cell(c,off,0,ox,oy,u)
        if t<5.7:
            for off in (0,mix(2.8,1,join)):ink(c,[(off,0),(off+1,0),(off+1,1),(off,1),(off,0)],ox,oy,u,cue(t,.25,2.3),ORANGE)
        else:
            outline(c,{(0,0),(1,0)},ox,oy,u,cue(t,5.7,1.9))
            contacts(c,{(0,0),(1,0)},ox,oy,u,t,5.7)
        c.text('Trace the exposed edges.',820,464,31,WHITE,bold=True)
    else:
        ox=350;oy=150;u=64;s={(x,y) for x in range(5) for y in range(5)}-{(2,2)}
        cells(c,s,ox,oy,u)
        outer,hole=loops(s)
        ink(c,outer,ox,oy,u,1,ORANGE,6,False)
        ink(c,hole,ox,oy,u,cue(t,9.8,2.4),AQUA)
        note(c,'Outside edge',798,273,35,ORANGE)
        if t>=10:note(c,'Edge of the hole',798,385,35,AQUA)
def applications(c,t):
    title(c,'A stepped outline can hide a shared edge')
    sheet(c)
    shape={(0,1),(1,1),(2,1),(1,0),(2,0)}
    ox,oy,u=179,240,105
    cells(c,shape,ox,oy,u)
    outline(c,shape,ox,oy,u,cue(t,14.3,3.8))
    if t>=20.35:contacts(c,shape,ox,oy,u,t,20.35)
    note(c,'Exposed',780,240,37,ORANGE)
    if t>=20.35:note(c,'Shared',780,340,37,ROSE)
    if t>=24.4:note(c,'Which edges change after a cut?',732,484,26)
def rectangle(c,t):
    title(c,'Walk around a 2 m by 3 m rectangle')
    sheet(c);ox,oy,u=285,190,99
    cells(c,RECT,ox,oy,u)
    dimension(c,(ox,oy+3*u+23),(ox+2*u,oy+3*u+23),'2 m')
    dimension(c,(ox-28,oy),(ox-28,oy+3*u),'3 m',False)
    outline(c,RECT,ox,oy,u,cue(t,34.6,5.7))
    note(c,'Start at a corner.',743,253,33)
    if t>=34.6:note(c,'Follow all four sides.',743,356,32,ORANGE)
def rect_answer(c,t):
    title(c,'Count each side once')
    sheet(c);ox,oy,u=270,182,100;cells(c,RECT,ox,oy,u)
    path=((0,0),(2,0),(2,3),(0,3),(0,0))
    for i in range(4):
        p=cue(t,41.94+i*.77,.77);col=ORANGE if i%2==0 else AQUA
        if p:
            a,b=path[i:i+2];ink(c,[a,b],ox,oy,u,p,col,7,False)
            mid=screen(((a[0]+b[0])/2,(a[1]+b[1])/2),ox,oy,u)
            dx,dy=((0,-24),(37,0),(0,25),(-37,0))[i]
            c.text('2 m' if i%2==0 else '3 m',mid[0]+dx,mid[1]+dy,24,col,bold=True)
    if t>=45.65:note(c,'2 + 3 + 2 + 3',738,256,43)
    if t>=46.95:note(c,'= 10 m',738,352,57,ORANGE)
    if t>=49:note(c,'Perimeter measures length.',738,460,28,SAGE)
def l_question(c,t):
    title(c,'Build the L one square at a time')
    sheet(c);ox,oy,u=160,168,97
    order=[(0,2),(1,2),(2,2),(3,2),(0,1),(0,0)]
    for i,(x,y) in enumerate(order):
        start=(53.0+i*.44) if i<4 else 55.9+(i-4)*.85
        p=cue(t,start,.48)
        if p:cell(c,x,y,mix(ox+32,ox,p),mix(oy-20,oy,p),u)
    if t>=54:note(c,'Four across',750,235,35)
    if t>=56:note(c,'Two above the left end',750,306,31)
    if t>=60:note(c,'Which edges touch?',750,437,34,ROSE)
    if t>=62.4:contacts(c,L,ox,oy,u,t,62.6,.7)
def l_answer(c,t):
    title(c,'Each shared edge was counted twice')
    sheet(c);ox,oy,u=164,181,96
    p=cue(t,71.6,1.6)
    for x,y in sorted(L):cell(c,x,y,ox+12*x*(1-p),oy+12*y*(1-p),u)
    if t>=68.5:note(c,'6 squares × 4 = 24',735,201,36)
    if t>=73.15:
        contacts(c,L,ox,oy,u,t,73.15,.29)
        note(c,'5 shared edges',735,276,34,ROSE)
    if t>=75.1:note(c,'24 − 2 × 5',735,354,36)
    if t>=80.25:note(c,'= 14 units',735,431,47,ORANGE)
    if t>=83.3:outline(c,L,ox,oy,u,cue(t,83.3,3.35))
def board(c,shape):sheet(c);ox,oy,u=192,143,65;cells(c,shape,ox,oy,u);return ox,oy,u
def cut_question(c,t):
    title(c,'A corner cut and an enclosed hole')
    s=BOARD if t<88.85 else HOLED if t<94.0 else CUT
    ox,oy,u=board(c,s)
    if t>=88.85:
        inner=loops(HOLED)[1];ink(c,inner,ox,oy,u,cue(t,88.85,1.7),AQUA,5)
    if t>=94.0:
        ink(c,[(5,0),(5,1),(6,1)],ox,oy,u,cue(t,94.0,1.3),ORANGE)
    dimension(c,(ox,oy+6*u+20),(ox+6*u,oy+6*u+20),'6 units')
    note(c,'Original board   6 × 6',739,206,32)
    if t>=88.9:note(c,'Hole   2 × 1',739,286,35,AQUA)
    if t>=94:note(c,'Corner removed   1 × 1',739,366,31,ORANGE)
    if t>=97:note(c,'Find the total boundary length.',730,489,27)
def hard_answer(c,t):
    title(c,'The corner trades two edges. The hole adds six.')
    s=BOARD if t<110.65 else BOARD-{CORNER} if t<114 else CUT
    ox,oy,u=board(c,s)
    outline(c,BOARD,ox,oy,u,cue(t,104.19,2.5),ORANGE)
    if t>=107.4:
        ink(c,[(5,0),(6,0),(6,1)],ox,oy,u,cue(t,107.4,.95),ROSE,8,False)
    if t>=110.65:
        # Erase the original outside walk and trace the actual concave corner.
        cells(c,s,ox,oy,u)
        c.line([screen(p,ox,oy,u) for p in [(5,0),(6,0),(6,1)]],PAPER,10)
        outline(c,s,ox,oy,u,1,ORANGE)
        ink(c,[(5,0),(5,1),(6,1)],ox,oy,u,cue(t,110.65,1.35),ORANGE)
    if t>=114:
        ink(c,loops(CUT)[1],ox,oy,u,cue(t,114.0,3.8),AQUA)
    note(c,'Outside   4 × 6 = 24',735,185,34,ORANGE)
    if t>=110.7:note(c,'Corner   −2 + 2 = 0',735,261,32)
    if t>=116.0:note(c,'Hole   2 × 2 + 2 × 1 = 6',735,344,30,AQUA)
    if t>=122:note(c,'24 + 6 = 30 units',735,449,40)
def two_walks(c,t):
    title(c,'Trace where filled cells meet empty space')
    ox,oy,u=board(c,CUT);outer,hole=loops(CUT)
    ink(c,outer,ox,oy,u,cue(t,126.5,4.5),ORANGE)
    if t>=131.5:ink(c,hole,ox,oy,u,cue(t,131.5,2.75),AQUA)
    note(c,'Outer walk',750,234,35,ORANGE)
    if t>=131.5:note(c,'Inner walk',750,330,35,AQUA)
    if t>=136.8:note(c,'24 + 6 = 30',750,438,41)
def mistakes(c,t):
    title(c,'A shared join and a hole play different roles')
    sheet(c,67,153,1210,541)
    ox,oy,u=225,224,100
    cells(c,{(0,0),(1,0)},ox,oy,u)
    contacts(c,{(0,0),(1,0)},ox,oy,u,t,141.4)
    c.text('One join removes two counts.',330,442,28,ROSE,bold=True)
    if t>=147.2:
        ox,oy,u=757,185,49;cells(c,HOLED,ox,oy,u)
        ink(c,loops(HOLED)[1],ox,oy,u,cue(t,147.2,2.3),AQUA)
        c.text('A hole adds a whole walk.',907,529,27,AQUA,bold=True)
def recap(c,t):
    title(c,'Mark the edges before adding lengths')
    ox,oy,u=board(c,CUT)
    if t<160.4:
        ink(c,[(0,1),(1,1)],ox,oy,u,1,ROSE)
        ink(c,[(0,0),(1,0)],ox,oy,u,1,ORANGE)
        note(c,'Shared edge',752,211,36,ROSE);note(c,'Exposed edge',752,292,36,ORANGE)
        if t>=157.8:note(c,'Use units of length.',752,421,34)
    else:
        for i,loop in enumerate(loops(CUT)):
            ink(c,loop,ox,oy,u,cue(t,160.4+i*2.8,2.8),ORANGE if i==0 else AQUA)
        note(c,'Which edges disappeared?',735,238,30,ROSE)
        if t>=162.1:note(c,'Which new edges appeared?',735,328,30,AQUA)
        if t>=165:note(c,'Trace every required loop.',735,438,31)
SCENES=(intro,applications,rectangle,rect_answer,l_question,l_answer,cut_question,hard_answer,two_walks,mistakes,recap)
def verify():
    assert len(L)==6 and list(incidences(L).values()).count(2)==5
    for shape,expected in [(L,[14]),(RECT,[10]),(BOARD,[24]),(HOLED,[24,6]),(CUT,[24,6])]:
        paths=loops(shape)
        assert [len(p)-1 for p in paths]==expected
        traced=[edgekey(a,b) for path in paths for a,b in zip(path,path[1:])]
        assert len(traced)==len(set(traced))
        assert set(traced)=={e for e,n in incidences(shape).items() if n==1}
        assert all(p[0]==p[-1] for p in paths)
    assert 4*len(L)-2*5==14 and 24-2+2+6==30
