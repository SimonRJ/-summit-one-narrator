"""The end gaps of a line and the closing gap of a circular parade."""
from itertools import permutations,combinations
from math import sin,cos,pi
BACKGROUND=('#3a3546','#232137')
PAPER,ROAD,MINT,GOLD,ROSE,BLUE,LINE='#fff2dd','#878391','#9adeca','#f4cc7d','#ed9899','#a3d5f2','#6f677b'
BRIDGE='Pin the bell float at the gate so a rotation counts only once. Follow the route past the last float. Where is the gap that a straight-line count misses?'
HEAD=('Two breaks on a straight route','When the ends open','Bend the route into a loop','Pin the bell at the gate','Two named vans enter','The closing gap counts','Rebuild the full parade','Change just the van labels')
def check_maths():
    assert len(list(combinations(range(2),2)))==1 and len(list(combinations(range(4),2)))==6
    rows=[]
    for tail in permutations('SMDxy'):
        r=('B',)+tail
        if not any({r[i],r[(i+1)%6]}=={'x','y'} for i in range(6)):rows.append(r)
    assert len(rows)==72 and len({tuple('v' if c in 'xy' else c for c in r) for r in rows})==36
def text(a,s,x,y,size=35,col=PAPER,t=1):
    a.text(str(s),x,y,size,col,bold=True,opacity=t)
def badge(a,x,y,name,size=73,t=1):
    col={'Bell':GOLD,'Sail':MINT,'Moon':'#bdafdf','Drum':'#edaf84'}[name]
    a.box(x-size/2,y-23,size,46,radius=8,fill=col,opacity=t);text(a,name,x,y,26,'#2d2735',t)
def ring(a,fill,rotation=0,selected=None,plain=False):
    cx,cy,rad=400,357,155
    def pt(angle,r=rad):return cx+r*cos(angle),cy+r*sin(angle)
    angles=[-pi/2+i*pi/2+rotation for i in range(4)]
    circle=[pt(-pi/2+i*2*pi/80) for i in range(81)]
    a.line(circle,ROAD,7)
    a.line([(cx-33,cy-rad-30),(cx-33,cy-rad-40),(cx+33,cy-rad-40),(cx+33,cy-rad-30)],GOLD,3)
    text(a,'Gate',cx,cy-rad-59,22,GOLD)
    a.arrow(pt(-.95,rad+22),pt(-.65,rad+22),PAPER,1,3)
    for i,(name,ang) in enumerate(zip(('Bell','Sail','Moon','Drum'),angles)):
        x,y=pt(ang);badge(a,x,y,name,83)
        if fill:
            gx,gy=pt(ang+pi/4);a.dot(gx,gy,15,'#262333');a.dot(gx,gy,9,GOLD)
            if selected and i in selected:
                cap=selected[i]
                a.box(gx-27,gy-17,54,34,radius=2,fill=PAPER if plain else ROSE if cap=='R' else BLUE)
                text(a,cap,gx,gy,20,'#302a3b')
def draw(a,n,c):
    a.label(HEAD[n-1],65,71,44,PAPER,bold=True);a.line([(65,125),(1215,125)],LINE,3)
    if n in (1,2):
        a.line([(160,314),(1120,314)],ROAD,6)
        for x,label in zip((341,640,940),('Bell','Sail','Drum')):badge(a,x,314,label,114)
        pos=[493,793] if n==1 or c.reveal('beginning or at the end')<.1 else [185,493,793,1094]
        for x in pos:
            a.dot(x,314,20,'#282434');a.dot(x,314,11,GOLD)
        if n==1:
            text(a,'A break must fit between performances.',640,445,37,MINT,c.reveal('between performances'))
            text(a,'Two spaces for two identical breaks',640,532,34,GOLD,c.reveal('another between'))
        else:
            text(a,'Choose two gaps out of four',640,443,38,MINT,c.reveal('four available spaces'))
            text(a,'4 × 3 ÷ 2 = 6 pairs',640,535,43,GOLD,c.reveal('six choices'))
    else:
        rot=0
        if n==3:rot=.7*c.reveal('moving the starting mark',1.5)
        if n==4:rot=.7*(1-c.reveal('until the bell',1.5))
        selected=None;plain=n==8
        if n==6:
            selected={}
            if c.reveal('red van')>.1:selected[0]='R'
            if c.reveal('blue van')>.1:selected[2]='B'
        if n==7:
            selected={0:'R',2:'B'} if c.reveal('remove both vans')<.6 else {}
        if n==8:selected={0:'V',2:'V'}
        ring(a,n>=5,rot,selected,plain)
        if n==3:
            text(a,'Clockwise order',928,280,37,MINT);text(a,'A rotation is the same parade.',913,382,29,PAPER,c.reveal('same parade'))
        elif n==4:
            text(a,'Bell stays at the gate',924,263,33,GOLD,c.reveal('bell is at the gate'))
            text(a,'3 × 2 × 1 = 6',934,385,45,MINT,c.reveal('six orders'))
        elif n==5:
            text(a,'One red van',930,252,36,ROSE);text(a,'One blue van',931,318,36,BLUE)
            text(a,'How many gaps on the loop?',915,438,30,GOLD,c.reveal('how many gaps'))
        elif n==6:
            text(a,'4 gaps for red',924,252,37,ROSE,c.reveal('four gaps for the red'))
            text(a,'3 left for blue',924,335,37,BLUE,c.reveal('Three different gaps'))
            text(a,'4 × 3 = 12',925,451,46,GOLD,c.reveal('twelve placements'))
        elif n==7:
            text(a,'6 clockwise float orders',926,251,30,MINT)
            text(a,'12 van placements each',926,326,30,BLUE,c.reveal('twelve legal'))
            text(a,'6 × 12 = 72',922,447,48,GOLD,c.reveal('seventy two'))
        else:
            text(a,'The vans now match',928,255,33,PAPER)
            text(a,'12 ÷ 2 = 6 gap pairs',928,342,35,BLUE,c.reveal('placements become six'))
            text(a,'6 × 6 = 36',923,447,46,GOLD,c.reveal('thirty six parades'))
def poster(draw):return draw(7,1)
