"""Genuine boundary-line choices on a four-by-three marked wall."""
from itertools import combinations, product
from stage import blend, clamp, mix
BACKGROUND=('#242c47','#19243b')
PAPER,AMBER,BLUE,GR,LINE,ROSE='#f5f3e7','#ffbe6d','#93c7ff','#99dfc2','#94a8b8','#f8a1ac'
BRIDGE='In the film’s marked grid, first count rectangles containing cell A. To remove the unwanted ones, which four boundary choices guarantee a rectangle contains both A and B?'
HEAD=('Slide four edges','A two by one strip','Keep the amber tile','Count the four sliders','Keep a blue tile out','Clamp around both tiles','Subtract the frames that fail','An outside-corner test')
A,B=(1,1),(2,0)
BOTH=(1,3,0,2)


def rects(w,h):
    return [(l,r,t,b) for (l,r),(t,b) in product(combinations(range(w+1),2),combinations(range(h+1),2))]


def inside(p,r):
    x,y=p;l,rr,t,b=r
    return l<=x<rr and t<=y<b


def check_maths():
    rectangles=rects(4,3)
    assert len(rects(2,1))==3 and len(rectangles)==60
    a=[r for r in rectangles if inside(A,r)]
    assert len(a)==24 and sum(inside(B,r) for r in a)==8
    assert sum(not inside(B,r) for r in a)==16
    assert all((inside(A,r) and inside(B,r))==(r[0]<=1 and r[1]>=3 and r[2]<=0 and r[3]>=2) for r in rectangles)


def grid(a,x,y,g,w,h,marked=()):
    for r in range(h):
        for c in range(w):
            cell=(c,r);col='#3a4860' if (c+r)%2 else '#404f65'
            if cell in marked:col=AMBER if cell==A else BLUE
            a.box(x+c*g+4,y+r*g+4,g-8,g-8,radius=5,fill=col)
            if cell in marked:a.text('A' if cell==A else 'B',x+(c+.5)*g,y+(r+.5)*g,32,'#273247',bold=True)
    for c in range(w+1):a.line([(x+c*g,y),(x+c*g,y+h*g)],LINE,2)
    for r in range(h+1):a.line([(x,y+r*g),(x+w*g,y+r*g)],LINE,2)


def outline(a,x,y,g,r,col,t=1):
    if t<=0:return
    l,rr,top,bot=r
    pts=[(x+l*g,y+top*g),(x+rr*g,y+top*g),(x+rr*g,y+bot*g),(x+l*g,y+bot*g),(x+l*g,y+top*g)]
    for i,(p,q) in enumerate(zip(pts,pts[1:])):
        f=clamp(4*t-i)
        if f:a.line([p,(mix(p[0],q[0],f),mix(p[1],q[1],f))],col,8)


def txt(a,x,y,s,col=PAPER,size=38,t=1):a.label(s,x,y,size,col,t,bold=True)


def options(a,x,y,g,positions,col,t=1):
    for side,ns in positions.items():
        for n in ns:
            if side=='left':a.line([(x+n*g,y-27),(x+n*g,y-6)],col,7,t)
            if side=='right':a.line([(x+n*g,y+3*g+5),(x+n*g,y+3*g+26)],col,7,t)
            if side=='top':a.line([(x-28,y+n*g),(x-5,y+n*g)],col,7,t)
            if side=='bottom':a.line([(x+4*g+5,y+n*g),(x+4*g+28,y+n*g)],col,7,t)


def draw(a,n,c):
    txt(a,68,72,HEAD[n-1],size=46);a.line([(68,118),(1205,118)],LINE,2)
    x,y,g=124,216,94
    if n==1:
        grid(a,178,190,109,4,3)
        t=c.reveal('slides two upright edges',2)
        outline(a,178,190,109,(mix(0,1,t),mix(4,3,t),0,mix(3,2,t)),AMBER,1)
        txt(a,740,252,'2 upright lines',AMBER,38);txt(a,740,330,'2 level lines',BLUE,38)
        a.dot(178+109,190,8,GR,c.reveal('A corner'));txt(a,740,445,'4 edges → 1 rectangle',GR,34,c.reveal('rectangle is fixed'))
    elif n==2:
        for i,(r,cue) in enumerate([((0,1,0,1),'left tile'),((1,2,0,1),'right tile'),((0,2,0,1),'whole strip')]):
            xx=102+i*394;grid(a,xx,285,133,2,1);outline(a,xx,285,133,r,AMBER,c.reveal(cue,.75))
        txt(a,351,514,'Choose 2 of the 3 upright lines',GR,39,c.reveal('Choose any two'))
    else:
        grid(a,x,y,g,4,3,(A,) if n<5 else (A,B))
        if n==3:
            txt(a,646,207,'A: row 2, column 2',AMBER,39)
            options(a,x,y,g,{'left':[0,1]},AMBER,c.reveal('Choose a left edge'))
            txt(a,646,330,'Left edge: 2 positions',PAPER,34,c.reveal('Choose a left edge'))
            txt(a,646,427,'Right edge: ?',GR,39,c.reveal('How many right edges'))
        elif n==4:
            for i,(side,ns,cue) in enumerate([('left',[0,1],'left slider'),('right',[2,3,4],'right has three'),('top',[0,1],'top and bottom'),('bottom',[2,3],'top and bottom')]):
                t=c.reveal(cue);options(a,x,y,g,{side:ns},(AMBER,BLUE,GR,ROSE)[i],t)
                txt(a,623+(i%2)*300,260+98*(i//2),side.title()+'   '+str(len(ns)),(AMBER,BLUE,GR,ROSE)[i],35,t)
            txt(a,627,491,'2 × 3 × 2 × 2 = 24',PAPER,40,c.reveal('Multiply'))
        elif n==5:
            txt(a,623,246,'Keep A. Leave B outside.',AMBER,36)
            t=c.reveal('more than one direction',1.0)
            outline(a,x,y,g,(1,2,1,2),GR,t)
            txt(a,624,379,'B is above AND to the right.',BLUE,32,t)
            txt(a,624,484,'Subtract which frames?',GR,36,c.reveal('subtract instead'))
        elif n==6:
            t=c.reveal('small box',1.4);outline(a,x,y,g,BOTH,GR,t)
            for i,(s,col,q) in enumerate([('Left: A',AMBER,'left boundary'),('Right: B',BLUE,'right boundary'),('Top: B',BLUE,'top is set'),('Bottom: A',AMBER,'bottom by A')]):
                txt(a,628+(i%2)*283,260+(i//2)*105,s,col,37,c.reveal(q))
            txt(a,624,496,'Every valid frame covers this box.',GR,31,c.reveal('whole box'))
        elif n==7:
            outline(a,x,y,g,BOTH,GR)
            for s,ns,q,col in [('left',[0,1],'left edge',AMBER),('right',[3,4],'right edge',BLUE),('top',[0],'top edge',GR),('bottom',[2,3],'bottom edges',ROSE)]:
                options(a,x,y,g,{s:ns},col,c.reveal(q))
            txt(a,634,261,'Both tiles',GR,36)
            txt(a,634,336,'2 × 2 × 1 × 2 = 8',PAPER,39,c.reveal('eight frames'))
            txt(a,634,472,'24 − 8 = 16',AMBER,46,c.reveal('remove those eight'))
        else:
            one=c.reveal('A alone',.75);full=c.reveal('whole wall',.8)
            outline(a,x,y,g,(1,2,1,2),GR,one)
            outline(a,x,y,g,(0,4,0,3),ROSE,full)
            txt(a,627,253,'A alone: keep',GR,40,one)
            txt(a,627,348,'Whole wall: remove',ROSE,36,full)
            txt(a,627,482,'Find the extreme tiles.',PAPER,37,c.reveal('extreme marked tiles'))


def poster(draw):return draw(3,1)
