"""S076. Measure exposed grid edges, a corner exchange and the separate walk around a hole."""
from collections import Counter
from math import hypot
from captioned_film import cue,mix
ID='S076'
ORIGINAL='eb266bd86f373213101976fae677788e787df6ff70616b0de74ef96c05832e91'
START=(0,13.88,29.24,41.22,52.74,68.39,86.78,104.19,126.1,140.5,154.26)
POSTER=135.2
PAPER='#f6eedc'
INK,DIM,GRID='#253d48','#516570','#9da99b'
FILL,TEAL,GOLD,RED,BLUE='#ccdfcc','#09756d','#a56a14','#b1483c','#386891'
L_CELLS={(0,0),(0,1),*((i,2) for i in range(5))}
L_WALK=((0,0),(1,0),(1,2),(5,2),(5,3),(0,3),(0,0))
FULL={(x,y) for x in range(7) for y in range(7)}
VOID={(x,y) for x in range(2,5) for y in range(2,4)}
CORNER=(6,0)
SQUARE=((0,0),(7,0),(7,7),(0,7),(0,0))
OUTER=((0,0),(6,0),(6,1),(7,1),(7,7),(0,7),(0,0))
HOLE=((2,2),(5,2),(5,4),(2,4),(2,2))

def text(c,s,x,y,z=30,col=INK,anchor='mm'):
    c.text(s,x,y,z,col,anchor,True)
def title(c,s):
    text(c,s,49,54,41,INK,'lm');c.line([(49,98),(1231,98)],GRID,2)
def trace(c,path,x,y,u,f,col,width=7,head=True):
    lengths=[hypot(x1-x0,y1-y0) for (x0,y0),(x1,y1) in zip(path,path[1:])]
    left=max(0,min(1,f))*sum(lengths)
    if left<=0:return
    for a,b,length in zip(path,path[1:],lengths):
        ratio=min(1,left/length)
        start=(x+a[0]*u,y+a[1]*u)
        end=(x+mix(a[0],b[0],ratio)*u,y+mix(a[1],b[1],ratio)*u)
        c.line([start,end],col,width)
        left-=length
        if left<=.00001:break
    if head and f<1:c.dot(*end,8,col)
def cells(c,coords,x,y,u,spread=0):
    for i,j in sorted(coords):
        xx=x+i*(u+spread);yy=y+j*(u+spread)
        c.rect(xx,yy,u,u,FILL,GRID,2)
def edges(coords):
    counts=Counter()
    for i,j in coords:
        loop=((i,j),(i+1,j),(i+1,j+1),(i,j+1),(i,j))
        for a,b in zip(loop,loop[1:]):counts[tuple(sorted((a,b)))]+=1
    return counts
def shared(c,coords,x,y,u,t,at):
    joints=[e for e,k in sorted(edges(coords).items()) if k==2]
    for i,e in enumerate(joints):
        trace(c,e,x,y,u,cue(t,at+i*.25,.4),RED,5)
def panel(c,s,x,y,col=TEAL):text(c,s,x,y,34,col)
def opening(c,t):
    title(c,'Which edges belong to the boundary?')
    gap=56*(1-cue(t,2,2))
    cells(c,{(0,0),(1,0)},144,225,111,gap)
    if t<3.8:
        for i in range(2):
            trace(c,((0,0),(1,0),(1,1),(0,1),(0,0)),144+i*(111+gap),225,111,cue(t,.3,.9),TEAL)
    else:
        trace(c,((0,0),(2,0),(2,1),(0,1),(0,0)),144,225,111,cue(t,3.8,1.2),TEAL)
        trace(c,((1,0),(1,1)),144,225,111,1,RED,4)
    text(c,'A shared edge',272,408,28,RED)
    if t>6:
        coords={(i,j) for i in range(3) for j in range(3)}-{(1,1)}
        cells(c,coords,831,178,54)
        trace(c,((0,0),(3,0),(3,3),(0,3),(0,0)),831,178,54,cue(t,6,1),TEAL)
        trace(c,((1,1),(2,1),(2,2),(1,2),(1,1)),831,178,54,cue(t,8.2,1.35),BLUE,6)
        text(c,'An enclosed edge',915,408,28,BLUE)
    if t>10:text(c,'Follow the outside. Include a hole when the question asks.',640,535,30)
def context(c,t):
    title(c,'A boundary problem can hide its useful edges')
    cells(c,L_CELLS,153,189,57)
    shared(c,L_CELLS,153,189,57,t,15.4)
    text(c,'Mark the joins',295,442,30,RED)
    if t>18:
        cells(c,FULL-VOID-{CORNER},825,150,37)
        trace(c,OUTER,825,150,37,cue(t,18.5,2.0),TEAL,4)
        trace(c,HOLE,825,150,37,cue(t,21.2,1.6),BLUE,4)
        text(c,'Follow the cuts',955,442,30,BLUE)
    if t>24:text(c,'What length disappears? What length appears?',640,546,32)
def square_q(c,t):
    title(c,'Six metres wide and six metres tall')
    cells(c,{(0,0)},225,179,291)
    text(c,'6 m',370,513,32,TEAL);text(c,'6 m',159,325,31,TEAL)
    trace(c,((0,0),(1,0),(1,1),(0,1),(0,0)),225,179,291,cue(t,33.6,4.2),TEAL,7)
    text(c,'How long is one trip',908,275,34)
    text(c,'around the outside?',908,340,34)
def square_a(c,t):
    title(c,'Walk around the square once')
    x,y,u=225,179,291;cells(c,{(0,0)},x,y,u)
    path=((0,0),(1,0),(1,1),(0,1),(0,0))
    for i in range(4):
        f=cue(t,41.25+i*.85,.75)
        trace(c,path[i:i+2],x,y,u,f,TEAL)
        if f>.6:
            pos=((370,142),(572,327),(370,518),(165,327))[i];text(c,'6 m',*pos,28,TEAL)
    if t>44.8:panel(c,'6 + 6 + 6 + 6',930,248)
    if t>46.7:text(c,'24 metres',930,341,43)
    if t>48.7:text(c,'Perimeter measures length.',929,452,27,DIM)
def l_question(c,t):
    title(c,'Seven unit squares make an L')
    # Anchor the five-square row; stack the other two directly over its left end.
    active={(i,2) for i in range(5) if t>=52.75+i*.28}
    if t>=55.4:active.add((0,1))
    if t>=56.4:active.add((0,0))
    cells(c,active,151,187,77)
    if t>57:text(c,'Every small side is 1 unit.',927,253,29)
    if t>59:text(c,'Which edges meet?',927,348,32,RED)
    if t>62:shared(c,active,151,187,77,t,62)
    if t>64:text(c,'Count each touching pair of squares once.',640,540,29)
def l_solution(c,t):
    title(c,'One shared side removes two counted edges')
    x,y,u=143,172,76
    gap=14*(1-cue(t,70.3,1.2));cells(c,L_CELLS,x,y,u,gap)
    if t<71.6:
        for i,j in L_CELLS:trace(c,((0,0),(1,0),(1,1),(0,1),(0,0)),x+i*(u+gap),y+j*(u+gap),u,cue(t,68.5,.75),TEAL,3)
    else:shared(c,L_CELLS,x,y,u,t,71.6)
    if t>69:panel(c,'7 × 4 = 28',937,210)
    if t>74:text(c,'6 joins × 2 edges = 12',937,298,32,RED)
    if t>77:text(c,'28 − 12 = 16 units',937,391,35)
    if t>79.4:
        trace(c,L_WALK,x,y,u,cue(t,79.4,3.8),TEAL,7)
        text(c,'Walking the outline also gives 16.',640,535,31,TEAL)
def board_question(c,t):
    title(c,'Two cuts in a seven-by-seven board')
    shape=FULL if t<90.3 else FULL-VOID if t<93.9 else FULL-VOID-{CORNER}
    cells(c,shape,168,153,50)
    text(c,'7',344,545,29);text(c,'7',122,329,28)
    if t>=90.3:
        trace(c,HOLE,168,153,50,cue(t,90.3,1.4),BLUE,5)
        text(c,'Interior hole: 3 by 2',915,236,31,BLUE)
    if t>=93.9:
        trace(c,((6,0),(6,1),(7,1)),168,153,50,cue(t,93.9,.9),RED,5)
        text(c,'Corner removed: 1 by 1',915,328,30,RED)
    if t>=99:text(c,'Include the full edge of the hole.',914,450,27)
def board_solution(c,t):
    title(c,'Separate the corner cut from the hole')
    x,y,u=153,146,51
    shape=FULL if t<107.7 else FULL-{CORNER} if t<113.9 else FULL-VOID-{CORNER}
    cells(c,shape,x,y,u)
    trace(c,SQUARE if t<107.7 else OUTER,x,y,u,cue(t,104.2,1.3),TEAL,6)
    if 106.5<t<109.5:trace(c,((6,0),(7,0),(7,1)),x,y,u,1,RED,6)
    if t>107.7:trace(c,((6,0),(6,1),(7,1)),x,y,u,cue(t,107.7,.8),GOLD,7)
    text(c,'Outside: 4 × 7 = 28',933,198,32,TEAL)
    if t>108.3:text(c,'Corner: −2 + 2 = 0',933,284,32,GOLD)
    if t>113.9:
        trace(c,HOLE,x,y,u,cue(t,114,2.1),BLUE,7)
        text(c,'Hole: 3 + 2 + 3 + 2 = 10',929,368,30,BLUE)
    if t>119:text(c,'28 + 10 = 38 units',931,476,37)
    if t>121:text(c,'The corner changes the shape but keeps the outer length.',640,567,27)
def disjoint(c,t):
    title(c,'Trace two disjoint boundary walks')
    x,y,u=149,150,51;cells(c,FULL-VOID-{CORNER},x,y,u)
    trace(c,OUTER,x,y,u,cue(t,126.1,3.1),TEAL,7)
    if t>=129:trace(c,HOLE,x,y,u,cue(t,129.5,2.0),BLUE,7)
    text(c,'28 outside',936,245,38,TEAL)
    if t>130:text(c,'10 inside',936,341,38,BLUE)
    if t>133:text(c,'Every counted edge has board on one side',930,439,25)
    if t>133:text(c,'and empty space on the other.',930,486,25)
    if t>136:text(c,'No edge belongs to both walks.',640,560,31)
def pitfall(c,t):
    title(c,'Two different reasons the boundary changes')
    gap=48*(1-cue(t,141.1,1.8))
    cells(c,{(0,0),(1,0)},169,232,97,gap)
    if gap>1:
        trace(c,((1,0),(1,1)),169,232,97,1,RED,5)
        trace(c,((0,0),(0,1)),266+gap,232,97,1,RED,5)
    else:trace(c,((0,0),(2,0),(2,1),(0,1),(0,0)),169,232,97,1,TEAL,6)
    text(c,'A join hides two edge counts.',284,444,25,RED)
    if t>146:
        cells(c,FULL-VOID,830,164,33)
        trace(c,HOLE,830,164,33,cue(t,146,1.5),BLUE,5)
        text(c,'A hole adds an inner walk.',948,444,25,BLUE)
    if t>151:text(c,'Read whether the question asks for all boundaries.',640,542,31)
def recap(c,t):
    title(c,'Account for the edges before calculating')
    x,y,u=169,157,48;cells(c,FULL-VOID-{CORNER},x,y,u)
    trace(c,OUTER,x,y,u,cue(t,154.4,2.2),TEAL,6)
    trace(c,HOLE,x,y,u,cue(t,156.6,1.7),BLUE,6)
    if t<158:trace(c,((1,4),(2,4)),x,y,u,1,RED,5)
    text(c,'Trace exposed edges.',929,206,32,TEAL)
    if t>=157:text(c,'Measure in units of length.',929,301,29)
    if t>=161:text(c,'Subtract lost edges. Add new ones.',921,395,28,GOLD)
    if t>=165:text(c,'28 outside + 10 inside = 38',918,490,31,BLUE)
SCENES=(opening,context,square_q,square_a,l_question,l_solution,board_question,board_solution,disjoint,pitfall,recap)
def verify():
    assert 4*6==24
    e=edges(L_CELLS); assert len(L_CELLS)==7 and list(e.values()).count(2)==6 and list(e.values()).count(1)==16
    def segments(path):
        out=set()
        for (x,y),(u,v) in zip(path,path[1:]):
            dx,dy=(u>x)-(u<x),(v>y)-(v<y)
            assert dx*dy==0
            while (x,y)!=(u,v):
                a=(x,y);x+=dx;y+=dy;out.add(tuple(sorted((a,(x,y)))))
        return out
    assert segments(L_WALK)=={e for e,k in edges(L_CELLS).items() if k==1}
    outer,inner=segments(OUTER),segments(HOLE)
    assert len(outer)==28 and len(inner)==10 and outer.isdisjoint(inner)
    assert outer|inner=={e for e,k in edges(FULL-VOID-{CORNER}).items() if k==1}
