"""S089. An orbiting orthographic view keeps paint attached to the original external unit faces."""
from itertools import product
from math import cos,sin,radians
from collections import Counter
from captioned_film import cue,mix,font
from folding_box import Camera
ID='S089'
ORIGINAL='fd0c3aa7c0719c37a1b1688578cfa1ec15ff77c120bda8a739bd97b64a4ad278'
START=(0,17.56,35.64,51.93,65.37,81.66,98.30,115.23,141.46,160.17,177.61)
POSTER=110.35
PAPER='#172c35';INK='#fff5de';SOFT='#c1d3d3';GRID='#597078';ICE='#9cded4'
GOLD='#ffc588';CUT='#253942';CORAL='#ffa599';ALL=frozenset(range(6));OPEN=ALL-{5}
PAINT=('#ad6c3a','#eea763','#cd8147','#e49b59','#ae7148','#ffcd91')
BARE=('#a3bfc0','#bfd5d0','#9ebabb','#c5dbd6','#aac3c3','#d9e4d9')
def label(c,s,x,y,size=31,col=INK,anchor='lm'):c.text(s,x,y,size,col,anchor,True)
def title(c,s):
    z=42
    while font(round(z*c.scale),True).getlength(s)>1140*c.scale:z-=1
    label(c,s,60,60,z)
def touches(pos,dims,paint):
    return frozenset(2*a+i for a in range(3) for i,match in enumerate((pos[a]==0,pos[a]==dims[a]-1)) if match and 2*a+i in paint)
def allc(d):return product(*(range(n) for n in d))
def tally(d,paint):return Counter(len(touches(k,d,paint)) for k in allc(d))
def polyface(center,face):
    axis,high=divmod(face,2);axes=[i for i in range(3) if i!=axis];out=[]
    for u,v in ((0,0),(1,0),(1,1),(0,1)):
        p=list(center);p[axis]+=high-.5;p[axes[0]]+=u-.5;p[axes[1]]+=v-.5;out.append(tuple(p))
    return out
def block(c,d,paint,view=(400,325,57,37,28),gap=0,layer_gap=0,visible=None,outline=None):
    px,py,unit,az,el=view;cam=Camera(px,py,unit,az,el)
    direction=(sin(radians(az))*cos(radians(el)),-cos(radians(az))*cos(radians(el)),sin(radians(el)))
    faces=[2*a+int(v>0) for a,v in enumerate(direction) if abs(v)>1e-5]
    cubes=[]
    for p in allc(d):
        if visible and not visible(p):continue
        base=[(p[a]+.5-d[a]/2)*(1+gap+(layer_gap if a==2 else 0)) for a in range(3)]
        cubes.append((cam.depth(base),p,base))
    for _,p,center in sorted(cubes):
        coloured=touches(p,d,paint)
        for face in faces:
            projected=[cam.project(v) for v in polyface(center,face)]
            ink=ICE if outline and outline(p) else CUT
            c.poly(projected,PAINT[face] if face in coloured else BARE[face],ink,2.4 if ink==ICE else 1.4)
def legend(c,y=529):
    c.rect(145,y-9,23,18,PAINT[5]);label(c,'Painted original face',181,y,23,GOLD)
    c.rect(552,y-9,23,18,BARE[5]);label(c,'Bare face',589,y,23,SOFT)
def mapgrid(c,x,y,u,z,d=(5,4,3),paint=OPEN,show=4,picks=False):
    for xx in range(d[0]):
        for yy in range(d[1]):
            n=len(touches((xx,yy,z),d,paint));px=x+xx*u;py=y+(d[1]-1-yy)*u
            hot=n==2;draw=n<=show
            c.rect(px,py,u,u,('#aee5d4' if hot else '#3b5560') if draw else '#293e47',PAPER,2)
            if draw and (not picks or hot):label(c,str(n),px+u/2,py+u/2,round(u*.52),CUT if hot else INK,'mm')
def intro(c,t):
    title(c,'Paint stays on each cube when the block separates')
    allpaint=OPEN if t>=13 else ALL
    block(c,(3,3,3),allpaint,(390,310,67,27+22*cue(t,.7,6.5),28),gap=.36*cue(t,3.2,4))
    if t>=6.6:label(c,'Count the outside faces',789,198,29,GOLD)
    if t>=8.8:label(c,'Corner · edge · face · core',789,279,26)
    if t>=13:label(c,'Now the top is bare.',789,365,28,ICE)
    legend(c)
def use(c,t):
    title(c,'Follow the original paint as the layers separate')
    k=cue(t,22.6,2.8);lg=.9*cue(t,32.2,2.1)
    block(c,(4,3,3),ALL if t<27.7 else OPEN,(409,318,54,24+23*cue(t,18,10),28),k*.14,lg)
    label(c,'Before splitting' if t<22.6 else 'The same 36 unit cubes',807,192,28)
    if t>=22.6:label(c,'Fresh cuts are bare.',807,277,29,ICE)
    if t>=32.2:label(c,'Inspect each layer.',807,376,28,GOLD)
    legend(c)
def basic(c,t):
    title(c,'A 3 × 3 × 3 cube with all six outer faces painted')
    angle=22+37*cue(t,36.3,7.1);block(c,(3,3,3),ALL,(385,311,72,angle,27),gap=.12*cue(t,42.3,2.5))
    label(c,'3 along each edge',799,217,32)
    if t>=42.2:label(c,'Which unit cubes touch',799,330,28,GOLD);label(c,'three painted faces?',799,370,28,GOLD)
    legend(c)
def corners(c,t):
    title(c,'A corner is the meeting place of three surfaces')
    d=(3,3,3);corn=lambda p:len(touches(p,d,ALL))==3
    if t<59.2:
        e=(2,0,2) if t<55.2 else (1,0,2)
        block(c,d,ALL,(385,311,70,34+17*cue(t,53,4),27),.11,visible=lambda p:p==e or t<54.4,outline=lambda p:p==e)
        label(c,'Corner   3 faces' if t<55.2 else 'Between corners   2 faces',781,285,30,GOLD)
    else:
        block(c,d,ALL,(395,312,64,38+28*cue(t,59.3,3.8),28),.10,.42,lambda p:corn(p) and (p[2]==2 or t>=62.4))
        label(c,'Top layer   4 corners',790,220,30,GOLD)
        if t>=62.4:label(c,'Bottom layer   4 corners',790,302,29,ICE)
        if t>=63.6:label(c,'4 + 4 = 8',790,409,41)
    legend(c)
def medium(c,t):
    title(c,'Exactly two painted faces on a 4 × 3 × 3 block')
    d=(4,3,3);v=lambda p:len(touches(p,d,ALL))<3 if t>=76 else True
    block(c,d,ALL,(389,313,66,29+33*cue(t,66,8),26),.18*cue(t,69.8,3.7),visible=v)
    label(c,'4 units × 3 units × 3 units',794,206,27)
    if t>=69.8:label(c,'Find the edge interiors.',794,310,29,GOLD)
    if t>=76:label(c,'Lift away all 8 endpoints.',794,411,26,ICE)
    legend(c)
def edge_work(c,t):
    title(c,'Count all four parallel copies of each edge')
    d=(4,3,3)
    def axis(p):
        inner=[i for i in range(3) if 0<p[i]<d[i]-1];return inner[0] if len(inner)==1 else None
    def keep(p):return axis(p) is not None and (axis(p)==0 or axis(p)==1 and t>=87.6 or axis(p)==2 and t>=89.0)
    block(c,d,ALL,(385,310,62,34+83*cue(t,82.0,10),30),.24,visible=keep)
    if t>=84.2:label(c,'Length 4   →   2 inside',786,189,29,GOLD)
    if t>=87.6:label(c,'Length 3   →   1 inside',786,257,29)
    if t>=89:label(c,'Length 3   →   1 inside',786,325,29)
    if t>=90.6:label(c,'4 × (2 + 1 + 1)',786,407,33,ICE)
    if t>=93.8:label(c,'= 16 cubes',786,471,36,ICE)
    legend(c)
def challenge(c,t):
    title(c,'5 × 4 × 3, with four painted sides and a painted base')
    # Rotate under the block as the bottom is named, then rise to reveal the unpainted top.
    el=25-57*cue(t,99.5,2.1)+62*cue(t,102.15,2.1)
    block(c,(5,4,3),OPEN,(395,318,58,30+23*cue(t,98.6,9),el),.16*cue(t,107,3.4))
    label(c,'5 by 4 in each layer',790,206,31)
    if t>=101.8:label(c,'Sides and bottom painted',790,292,27,GOLD)
    if t>=104.2:label(c,'Bare top',790,363,31,ICE)
    if t>=106.4:label(c,'Exactly 2 painted faces?',790,453,28)
    legend(c)
def split(c,t):
    title(c,'Count the bottom differently from the two upper layers')
    bottom=t<125
    d=(5,4,3)
    def keep(p):
        if bottom:return p[2]==0 and (t<122 or len(touches(p,d,OPEN))==2)
        return len(touches(p,d,OPEN))==2 and (p[2]<2 or t>=133)
    block(c,d,OPEN,(405,318,55,33+10*cue(t,116,7),29),.11,.58 if not bottom else .0,keep)
    if t>=118.8:label(c,'Bottom edge interiors',782,191,29,GOLD)
    if t>=122:label(c,'2 × 3 + 2 × 2 = 10',782,252,30)
    if t>=129.2:label(c,'Middle corners   4',782,331,29,ICE)
    if t>=133:label(c,'Top corners   4',782,389,29,ICE)
    if t>=135.6:label(c,'10 + 4 + 4 = 18',782,470,34,GOLD)
    legend(c)
def maps(c,t):
    title(c,'Each square records how many of its faces are painted')
    mapgrid(c,124,210,65,0,show=4)
    label(c,'Bottom layer',287,152,28,GOLD,'mm')
    if t>=148.2:
        mapgrid(c,662,210,65,1,show=4)
        label(c,'Either upper layer',825,152,28,ICE,'mm')
    if t>=152.4:label(c,'Every upper cell loses the bottom face contribution.',213,537,29)
    elif t>=144:label(c,'The ten mint squares each have two painted faces.',222,539,28,ICE)
def exceptions(c,t):
    title(c,'The same corner can lose one painted face')
    p=(4,0,2);d=(5,4,3)
    # Recenter the isolated physical unit cube, originally the north-east top corner.
    for x,paint in ((316,ALL),(850,OPEN)):
        if x==850 and t<168.8:continue
        cam=Camera(x,325,115,36,31)
        for face in (1,2,5):
            poly=[cam.project(v) for v in polyface((0,0,0),face)]
            c.poly(poly,PAINT[face] if face in touches(p,d,paint) else BARE[face],CUT,2.7)
        label(c,'All faces painted' if paint==ALL else 'Bare top',x,185,30,GOLD if paint==ALL else ICE,'mm')
        label(c,('3 painted faces' if paint==ALL else '2 painted faces'),x,451,28,INK,'mm')
    if 164.4<=t<168.8:label(c,'An edge endpoint',702,253,29);label(c,'is already a corner.',702,303,29,GOLD)
    if t>=173.2:label(c,'Keep the two painted vertical faces.',355,545,29)
def finish(c,t):
    title(c,'Locate every qualifying cube, including those at the back')
    d=(5,4,3);p=cue(t,183,4.3)
    if t<185.5:
        block(c,d,OPEN,(402,306,54,28+110*p,28),.14,.48,visible=lambda k:len(touches(k,d,OPEN))==2 if t>=183 else True)
        label(c,'Painted sides and base',786,236,28,GOLD)
        if t>=180.6:label(c,'Three layers of 5 × 4',786,340,29,ICE)
    else:
        for z in range(3):
            x=113+385*z;mapgrid(c,x,225,52,z,picks=True)
            label(c,('Bottom','Middle','Top')[z],x+130,166,29,(GOLD,ICE,ICE)[z],'mm')
            label(c,('10 cubes','4 cubes','4 cubes')[z],x+130,486,30,INK,'mm')
        if t>=189:label(c,'18 of the 60 unit cubes have exactly two painted faces.',201,556,29,ICE)
SCENES=(intro,use,basic,corners,medium,edge_work,challenge,split,maps,exceptions,finish)
def verify():
    assert tally((3,3,3),ALL)=={3:8,2:12,1:6,0:1}
    assert tally((4,3,3),ALL)[2]==4*(2+1+1)==16
    d=(5,4,3); by_layer=[sum(len(touches((x,y,z),d,OPEN))==2 for x in range(5) for y in range(4)) for z in range(3)]
    assert by_layer==[10,4,4] and sum(by_layer)==18
    for x,y,z in allc(d):
        assert len(touches((x,y,z),d,OPEN))==int(x in (0,4))+int(y in (0,3))+int(z==0)
    assert sum(tally(d,OPEN).values())==60
