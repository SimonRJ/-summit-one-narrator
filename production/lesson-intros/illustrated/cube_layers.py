"""S006: exact unit-cube models and plans, timed to the published narration."""
from visuals import AQUA, BLUE, GOLD, PINK, SOFT, WHITE, VIOLET, ease, mix

PALETTES = (
    ('#8dc1ff','#527eaf','#3d628e'),
    ('#ffd27c','#be924c','#96713f'),
    ('#83dfce','#4a9e91','#367e76'),
    ('#cfbaff','#8b72bb','#6c5995'),
)
CUT = ('#ffa6a9','#c36572','#9a4c5d')
TUNNEL = ('#c4affd','#8b72bb','#6c5995')
EDGE = '#263a4a'


def text(a,t,x,y,size=32,col=WHITE,alpha=1):
    a.label(t,x,y,size,col,alpha,bold=True)


def project(x,y,z,ox,oy,u,dy=0):
    return (ox+(x-y)*u, oy+(x+y)*u*.5-z*u+dy)


def block(a,cells,ox,oy,u,gap=0,marked=None,alpha=1):
    """Draw exposed faces of exact unit cubes, with optional exploded layers."""
    cells=set(cells); marked=marked or {}
    for x,y,z in sorted(cells,key=lambda p:(p[0]+p[1],p[2],p[0])):
        dy=-z*gap
        def P(dx,dy_,dz):return project(x+dx,y+dy_,z+dz,ox,oy,u,dy)
        top,side_x,side_y=marked.get((x,y,z),PALETTES[z%len(PALETTES)])
        faces=[]
        if (x+1,y,z) not in cells:
            faces.append(([P(1,0,0),P(1,1,0),P(1,1,1),P(1,0,1)],side_x))
        if (x,y+1,z) not in cells:
            faces.append(([P(0,1,0),P(1,1,0),P(1,1,1),P(0,1,1)],side_y))
        if gap>1 or (x,y,z+1) not in cells:
            faces.append(([P(0,0,1),P(1,0,1),P(1,1,1),P(0,1,1)],top))
        for pts,col in faces:
            a.polygon(pts,col,alpha)
            a.path(pts+[pts[0]],EDGE,1.5,alpha)


def rectangle(nx,ny,nz):
    return {(x,y,z) for x in range(nx) for y in range(ny) for z in range(nz)}


def plan(a,x,y,cols,rows,cell,occupied,colour=BLUE,alpha=1,removed=None):
    """Each square denotes one unit cube in a single layer, viewed from above."""
    removed=removed or {}
    for row in range(rows):
        for col in range(cols):
            xx=x+col*cell;yy=y+row*cell
            if (col,row) in occupied:
                a.rounded(xx+2,yy+2,cell-4,cell-4,3,colour,.62*alpha)
            else:
                a.rounded(xx+2,yy+2,cell-4,cell-4,3,SOFT,.08*alpha)
            if (col,row) in removed:
                c,p=removed[(col,row)]
                a.path(((xx+7,yy+7),(xx+cell-7,yy+cell-7)),c,3,p*alpha)
                a.path(((xx+7,yy+cell-7),(xx+cell-7,yy+7)),c,3,p*alpha)


def opening(a,c):
    a.heading('Look inside the solid',BLUE)
    p=c.after('solid from little',.7)
    lift=56*c.after('lifting one level',1.8)
    block(a,rectangle(3,2,2),575,385,66,gap=lift,alpha=p)
    text(a,'hidden cubes count too',1030,370,30,SOFT,c.after('some cubes are hidden'))


def exams(a,c):
    a.heading('See a shape; sketch its layers',AQUA)
    p=c.after('how many cubes',.8)
    cells=rectangle(3,3,2)-{(1,1,1)}
    block(a,cells,350,350,47,gap=32*c.after('holes or an opening',1.5),alpha=p)
    q=c.after('plan of each layer',.7)
    text(a,'one layer, viewed from above',895,250,30,SOFT,q)
    plan(a,800,295,3,3,55,{(x,y) for x in range(3) for y in range(3)}-{(1,1)},AQUA,q,
         {(1,1):(PINK,q)})
    text(a,'example opening',882,515,29,PINK,q)


def basic(a,c):
    a.heading('How many cubes?',GOLD)
    p=c.opening(.6)
    block(a,rectangle(3,2,2),430,375,65,alpha=p)
    text(a,'3 wide',925,270,44,BLUE,c.after('three cubes wide'))
    text(a,'2 deep',925,360,44,AQUA,c.after('two deep'))
    text(a,'2 high',925,450,44,GOLD,c.after('two high'))
    text(a,'Start with one layer',925,540,30,SOFT,c.after('bottom layer'))


def basic_answer(a,c):
    a.heading('Count a layer, then lift it',GOLD)
    gap=62*c.after('upper layer',1.6)
    block(a,rectangle(3,2,2),400,390,62,gap=gap,alpha=c.opening())
    text(a,'2 rows × 3 = 6',920,300,42,BLUE,c.after('six cubes'))
    text(a,'another 6 above',920,390,38,GOLD,c.after('same six positions'))
    text(a,'6 + 6 = 12',920,490,48,WHITE,c.after('twelve cubes'))


HEIGHTS=((4,1,3),(1,3,2)) # back row, then front row


def stacks(a,c):
    a.heading('Six stacks of different heights',VIOLET)
    words=c.scene['words']; first,_=c.find('one three two then four one three')
    indexes=[first,first+1,first+2,first+4,first+5,first+6]
    entries=[(0,1,1),(1,1,3),(2,1,2),(0,0,4),(1,0,1),(2,0,3)]
    ps=[ease((c.t-words[i]['start'])/1.0) for i in indexes]
    cells={(x,y,z) for (x,y,h),p in zip(entries,ps) for z in range(h) if p>(z+1)/(h+1)}
    block(a,cells,320,385,48)
    text(a,'front',395,545,26,SOFT,c.after('front row first'))
    for row,y in enumerate((0,1)):
        text(a,'BACK' if row==0 else 'FRONT',725,268+row*125,25,SOFT,c.after('front row first'))
        for x in range(3):
            k=3+x if y==0 else x
            xx=845+x*120;yy=268+row*125
            a.rounded(xx-42,yy-42,84,84,10,BLUE,.16*ps[k])
            text(a,str(HEIGHTS[y][x]),xx,yy,48,BLUE,ps[k])
    text(a,'All stacks stand on the table',940,510,27,SOFT,c.after('rest on the table'))


def layer_count(a,c):
    a.heading('Count each level',BLUE)
    cues=('Level one','Four of those stacks','Three stacks','one reaches level four')
    counts=(6,4,3,1)
    for level in range(1,5):
        p=c.after(cues[level-1],.7);x=115+(level-1)*300
        text(a,'LEVEL '+str(level),x+63,225,27,SOFT,p)
        occupied={(col,row) for row in range(2) for col in range(3) if HEIGHTS[row][col]>=level}
        plan(a,x,260,3,2,42,occupied,PALETTES[(level-1)%4][0],p)
        text(a,str(counts[level-1]),x+63,400,42,WHITE,p)
    text(a,'6 + 4 + 3 + 1 = 14',640,510,43,WHITE,c.after('fourteen'))
    text(a,'heights also add to 14',640,565,27,SOFT,c.after('Summing the six heights'))


def challenge(a,c):
    a.heading('A column and a tunnel meet',AQUA)
    p=c.opening();split=c.after('vertical column',1.8)
    col=c.after('vertical column',.7);tun=c.after('straight tunnel',.7)
    block(a,rectangle(4,4,3),415,350,46,alpha=p*(1-split))
    flat=rectangle(4,4,1)
    lift_column=c.after('three cubes',1.2,.7)
    lift_tunnel=c.after('middle layer',1.0,.15)
    for k in range(3):
        marked={xyz:PALETTES[k] for xyz in flat}
        if col>.5:marked[(1,1,0)]=CUT
        if k==1 and tun>.5:
            marked.update({(x,1,0):TUNNEL for x in range(4) if x!=1})
        column_cell={(1,1,0)}
        tunnel_cells={(x,1,0) for x in (0,2,3)} if k==1 else set()
        base=flat-(column_cell if lift_column>0 else set())-(tunnel_cells if lift_tunnel>0 else set())
        ox=mix(415,220+k*250,split);size=mix(46,28,split)
        block(a,base,ox,350,size,marked=marked,alpha=p*split)
        if 0<lift_column<1:
            block(a,column_cell,ox,350-42*lift_column,size,marked=marked,alpha=p*split*(1-lift_column))
        if 0<lift_tunnel<1:
            block(a,tunnel_cells,ox,350-42*lift_tunnel,size,marked=marked,alpha=p*split*(1-lift_tunnel))
        text(a,('bottom','middle','top')[k],220+k*250,500,26,SOFT,split)
    text(a,'4 × 4 × 3 = 48',1020,240,35,BLUE,c.after('four by four'))
    text(a,'column: 3 cubes',1020,335,29,PINK,col)
    text(a,'tunnel: 4 cubes',1020,410,29,VIOLET,tun)
    text(a,'they share one cube',1020,500,27,AQUA,c.after('same column'))


def challenge_plans(a,c):
    a.heading('Mark the cuts on each layer',AQUA)
    total={(x,y) for x in range(4) for y in range(4)}
    column=c.after('vertical column',.8);tunnel=c.after('tunnel runs',.8)
    for k in range(3):
        x=170+k*350
        text(a,('BOTTOM','MIDDLE','TOP')[k],x+90,220,29,(BLUE,GOLD,AQUA)[k])
        cuts={(1,1):(PINK,column)}
        if k==1:
            cuts.update({(i,1):(VIOLET,tunnel) for i in (0,2,3)})
        plan(a,x,265,4,4,45,total,(BLUE,GOLD,AQUA)[k],1,cuts)
    text(a,'the middle cell is already marked',640,510,31,PINK,c.after('already empty'))
    text(a,'3 in column + 3 more in tunnel',640,560,31,WHITE,c.after('three more cubes'))


def remaining(a,c):
    a.heading('What remains in each layer?',AQUA)
    base={(x,y,0) for x in range(4) for y in range(4)}
    layers=(base-{(1,1,0)},base-{(x,1,0) for x in range(4)},base-{(1,1,0)})
    for k in range(3):
        ox=260+k*380
        text(a,('BOTTOM','MIDDLE','TOP')[k],ox,240,29,(BLUE,GOLD,AQUA)[k])
        block(a,layers[k],ox,325,29,marked={xyz:PALETTES[k] for xyz in layers[k]})
        p=c.after('bottom and top',.7) if k!=1 else c.after('middle has twelve',.7)
        text(a,('15','12','15')[k],ox,475,42,WHITE,p)
    text(a,'15 + 12 + 15 = 42',640,535,38,WHITE,c.after('forty-two'))
    text(a,'48 − 6 = 42',640,575,29,SOFT,c.after('forty-eight minus six'))


def mistakes(a,c):
    a.heading('Count the shared cube once',PINK)
    p=c.after('subtracting three',.7)
    cells=[(640,270,PINK),(640,340,PINK),(640,410,PINK),
           (500,340,VIOLET),(570,340,VIOLET),(710,340,VIOLET)]
    for x,y,col in cells:a.rounded(x-28,y-28,56,56,6,col,.55*p)
    text(a,'column',385,270,30,PINK,p)
    text(a,'tunnel',850,340,30,VIOLET,p)
    q=c.after('shared cube',.7)
    a.path(((612,312),(668,368)),WHITE,3,q);a.path(((612,368),(668,312)),WHITE,3,q)
    text(a,'shared',640,215,28,WHITE,q)
    text(a,'3 + 4 − 1 = 6 removed',640,520,42,WHITE,c.after('subtract the shared cell'))


def recap(a,c):
    a.heading('Sketch, mark, check',BLUE)
    text(a,'4 × 4 base • 3 levels',640,210,40,BLUE,c.after('base dimensions'))
    total={(x,y) for x in range(4) for y in range(4)}
    p=c.after('layer sketch',.7)
    for k in range(3):
        x=210+k*330
        cuts={(1,1):(PINK,c.after('common cell',.7))}
        if k==1:cuts.update({(i,1):(VIOLET,c.after('two cuts cross',.7)) for i in (0,2,3)})
        plan(a,x,270,4,4,35,total,(BLUE,GOLD,AQUA)[k],p,cuts)
    text(a,'48 − 6 = 42',640,515,45,WHITE,c.after('full volume'))


SCENES=(opening,exams,basic,basic_answer,stacks,layer_count,
        challenge,challenge_plans,remaining,mistakes,recap)


def draw(art,cues,scene):
    SCENES[scene-1](art,cues)
