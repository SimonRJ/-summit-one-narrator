"""A precisely enumerated voxel quarry and removable layer plates."""
from itertools import product
from stage import blend
BACKGROUND=('#323e47','#1b2631')
PAPER,STONE,SHAFT,TUNNEL,LINE,GOLD='#fbf0de','#9db5ac','#f2bd70','#e39180','#677e87','#f7cc82'
HEAD=('Lift the roof away','Look straight down','Build the quarry terraces','Give every floor a count','A shaft from the top','Meet inside the stone','Check the floors again','Count the empty positions')
BRIDGE='At the quarry, the top drill and the tunnel both pass through floor two. Which column and row identify the cube they share? Check your answer on each slide-out floor.'
CLIFF={(x,y,z) for x,y,z in product(range(4),range(3),range(4)) if z<2 or (z==2 and y<2) or (z==3 and y==0)}
VERT={p for p in CLIFF if p[:2]==(1,0)}
HORIZ={p for p in CLIFF if p[1:]==(0,1)}
def check_maths():
    assert len(CLIFF)==36 and len(VERT)==len(HORIZ)==4
    assert VERT&HORIZ=={(1,0,1)}
    final=CLIFF-(VERT|HORIZ)
    assert [sum(z==k for x,y,z in final) for k in range(4)]==[11,8,7,3] and len(final)==29
    ring=set(product(range(3),range(3)))-{(1,1)}
    assert len(ring)==8 and len(ring)+9==17
def text(a,s,x,y,size=34,col=PAPER,t=1):
    a.text(str(s),x,y,size,col,bold=True,opacity=t)
def solid(a,vox,cx,cy,u,high=None):
    def project(x,y,z):
        return (cx+(x-y)*u,cy+(x+y)*u*.44-z*u*.88)
    for x,y,z in sorted(vox,key=lambda p:(sum(p),p[2],p[1],p[0])):
        col=(high or {}).get((x,y,z),STONE)
        faces=[((1,0,0),[(1,0,0),(1,1,0),(1,1,1),(1,0,1)],.7),
               ((0,1,0),[(0,1,0),(1,1,0),(1,1,1),(0,1,1)],.52),
               ((0,0,1),[(0,0,1),(1,0,1),(1,1,1),(0,1,1)],1)]
        for (dx,dy,dz),corners,light in faces:
            if (x+dx,y+dy,z+dz) not in vox:
                a.polygon([project(x+i,y+j,z+k) for i,j,k in corners],blend('#1d3440',col,light),outline='#344954',width=2.7)
def plate(a,cx,top,occupied,cols=4,rows=3,cell=38,tint=None):
    for y,x in product(range(rows),range(cols)):
        left=cx+(x-cols/2)*cell;yy=top+y*cell
        col=(tint or {}).get((x,y),STONE if (x,y) in occupied else '#354850')
        a.box(left,yy,cell-2,cell-2,radius=1,fill=col,edge=LINE,stroke=1)
def floors(a,vox,show_counts=True):
    for z in range(4):
        x=190+300*z;cells={(xx,yy) for xx,yy,zz in vox if zz==z}
        text(a,'Floor '+str(z+1),x,227,32)
        plate(a,x,281,cells,cell=45)
        if show_counts:text(a,len(cells),x,482,45,GOLD)
def draw(a,n,c):
    a.label(HEAD[n-1],65,70,45,PAPER,bold=True);a.line([(65,126),(1215,126)],LINE,3)
    if n<=2:
        base=set(product(range(3),range(3)));top=base-{(1,1)}
        vox={(x,y,0) for x,y in base}|{(x,y,1) for x,y in top}
        solid(a,vox,335,329,56)
        text(a,'The two-floor cliff',331,482)
        plate(a,870,218,top,3,3,64,{(1,1):'#48555b'})
        if n==1:text(a,'Top floor: a ring',866,485,34,PAPER,c.reveal('floor above'))
        else:
            text(a,'Through the hole: 1 bottom cube',884,475,29,GOLD,c.reveal('middle cube'))
            text(a,'8 hidden • 17 cubes altogether',640,562,36,PAPER,c.reveal('seventeen cubes'))
    elif n==3:
        floors_seen=2+int(c.reveal('Floor three')>.2)+int(c.reveal('Floor four')>.2)
        solid(a,{p for p in CLIFF if p[2]<floors_seen},407,352,50)
        for z in range(floors_seen):
            plate(a,882+(z%2)*165,194+(z//2)*147,{(x,y) for x,y,zz in CLIFF if zz==z},cell=25)
            text(a,'Floor '+str(z+1),882+(z%2)*165,294+(z//2)*147,24)
        text(a,'Front rows stop lower; the back row reaches floor four.',640,550,30,PAPER,c.reveal('back row'))
    elif n==4:
        floors(a,CLIFF,c.reveal('bottom has twelve')>.15)
        text(a,'12 + 12 + 8 + 4 = 36',640,555,43,GOLD,c.reveal('Thirty six cubes'))
    elif n==5:
        high={p:SHAFT for p in VERT}
        solid(a,CLIFF,337,335,52,high)
        text(a,'Vertical shaft',335,502,34,SHAFT)
        plate(a,923,232,{(x,y) for x,y,z in CLIFF if z==1},cell=59,tint={(x,0):TUNNEL for x in range(4)} if c.reveal('horizontal tunnel')>.2 else {})
        text(a,'Floor 2: tunnel across the back',922,476,27,TUNNEL,c.reveal('horizontal tunnel'))
    elif n==6:
        high={(x,0):TUNNEL for x in range(4)}
        if c.reveal('where their paths meet')>.2:high[(1,0)]=SHAFT
        plate(a,415,207,{(x,y) for x,y,z in CLIFF if z==1},cell=73,tint=high)
        text(a,'Floor 2, seen from above',415,477,30)
        text(a,'Second column',948,281,35,SHAFT,c.reveal('second column'))
        text(a,'Back row',948,353,35,TUNNEL,c.reveal('back row'))
        text(a,'One cube on both paths',902,459,32,PAPER,c.reveal('very same cube'))
    elif n==7:
        floors(a,CLIFF-(VERT|HORIZ))
        text(a,'11 + 8 + 7 + 3 = 29',640,558,43,GOLD,c.reveal('eleven eight'))
    else:
        solid(a,CLIFF-(VERT|HORIZ),362,346,53)
        text(a,'Looking down hides the tunnel.',342,530,29,PAPER)
        plate(a,920,229,{(x,y) for x,y,z in CLIFF-(VERT|HORIZ) if z==1},cell=58)
        text(a,'Slide out floor 2',920,474,34,GOLD,c.reveal('floor two'))
def poster(draw):return draw(8,1)
