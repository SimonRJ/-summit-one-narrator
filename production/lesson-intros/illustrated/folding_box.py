"""S090. Fold/unfold rigid panels about real hinges and fill a 4×3×2 solid with unit cubes."""
from itertools import product
from math import cos, sin, pi, radians, isqrt
from captioned_film import cue,mix

ID='S090'
ORIGINAL='3c06c2494aa197258633cabb461d9cb366a727446f6c5e6a7864a043d0b208aa'
START=(0,14.36,31.32,45.37,54.66,71.27,85.99,105.16,130.43,147.71,162.59)
POSTER=76.9
PAPER='#f4f0e4';INK='#192d36';MUTED='#4c6268';LINE='#344e54'
BASE='#a5d1bd';LONG='#edb36d';SHORT='#8ebde4';CREAM='#fffaf1';BLUE='#246492';OCHRE='#91501a'
def heading(c,s):
    c.text(s,64,58,43,INK,'lm',True)
    c.line([(65,102),(1215,102)],'#aab9af',1.5)
def note(c,s,x,y,size=31,col=INK):c.text(s,x,y,size,col,'lm',True)
def line_of_text(c,s,y):c.text(s,650,y,33,INK,bold=True)

class Camera:
    def __init__(self,x,y,unit,azimuth=34,elevation=36):
        self.x,self.y,self.unit=x,y,unit
        self.az,self.el=radians(azimuth),radians(elevation)
    def project(self,p):
        x,y,z=p;a=self.az;e=self.el
        return (self.x+self.unit*(x*cos(a)+y*sin(a)),self.y+self.unit*((x*sin(a)-y*cos(a))*sin(e)-z*cos(e)))
    def depth(self,p):
        x,y,z=p
        return (x*sin(self.az)-y*cos(self.az))*cos(self.el)+z*sin(self.el)

def panels(a,b,h,f):
    """Base plus four rectangles, with real side lengths at every fold angle."""
    x=a/2;y=b/2;out=h*cos(f*pi/2);z=h*sin(f*pi/2)
    return [
      (BASE,[(-x,-y,0),(x,-y,0),(x,y,0),(-x,y,0)]),
      (LONG,[(-x,-y,0),(x,-y,0),(x,-y-out,z),(-x,-y-out,z)]),
      (LONG,[(-x,y,0),(x,y,0),(x,y+out,z),(-x,y+out,z)]),
      (SHORT,[(-x,-y,0),(-x,y,0),(-x-out,y,z),(-x-out,-y,z)]),
      (SHORT,[(x,-y,0),(x,y,0),(x+out,y,z),(x+out,-y,z)])]
def centroid(pts):return tuple(sum(p[k] for p in pts)/len(pts) for k in range(3))
def net(c,cam,a,b,h,fold,labels=False,shaded=None):
    fs=panels(a,b,h,fold)
    for n,(col,pts) in sorted(enumerate(fs),key=lambda v:cam.depth(centroid(v[1][1]))):
        corners=[cam.project(p) for p in pts]
        c.poly(corners,col if shaded is None or n in shaded else '#deddd3',LINE,2.7)
        if labels:
            center=cam.project(centroid(pts));dims=(f'{a} × {b}',f'{a} × {h}',f'{a} × {h}',f'{b} × {h}',f'{b} × {h}')[n]
            c.text(dims,*center,24 if n>=3 else 31,INK,bold=True)
def model(c,fold,a=5,b=3,h=2,labels=False,shaded=None):
    cam=Camera(407,348+48*fold,56,34*fold,90-53*fold)
    net(c,cam,a,b,h,fold,labels,shaded)
def measure(c,cam,p,q,text,dx,dy):
    p=cam.project(p);q=cam.project(q);a=(p[0]+dx,p[1]+dy);b=(q[0]+dx,q[1]+dy)
    c.line([p,a,b,q],MUTED,1.8)
    c.text(text,(a[0]+b[0])/2+dx*.5,(a[1]+b[1])/2+dy*.6,28,INK,bold=True)
def cube_faces(x,y,z,upper=False):
    x0=x-2;y0=y-1.5
    top=[(x0,y0,z+1),(x0+1,y0,z+1),(x0+1,y0+1,z+1),(x0,y0+1,z+1)]
    front=[(x0,y0,z),(x0+1,y0,z),top[1],top[0]]
    right=[(x0+1,y0,z),(x0+1,y0+1,z),top[2],top[1]]
    return list(zip((('#f7c986','#dba458','#b57e41') if upper else ('#b4dcce','#73ac9a','#619580')),(top,front,right)))
def pile(c,cam,upper=0,lift=0,lower=12):
    cells=sorted(product(range(4),range(3)),key=lambda cell:cam.depth((*cell,0)))
    faces=[]
    for level,count in ((0,lower),(1,upper)):
        for i,(x,y) in enumerate(cells[:int(count+.00001)]):
            faces.extend(cube_faces(x,y,level+(lift if level else 0),bool(level)))
    for col,pts in sorted(faces,key=lambda item:cam.depth(centroid(item[1]))):
        c.poly([cam.project(p) for p in pts],col,LINE,1.8)
def gate(t,k):return t>=k

def idea(c,t):
    heading(c,'How can flat card become a box?')
    f=cue(t,.7,3.6)
    model(c,f)
    fill=cue(t,8.2,3.3)
    if fill:
        cam=Camera(407,396,56,34,37)
        z=2*fill
        # Keep the near faces in outline so the newly filled space is visible.
        corners=[(-2.5,-1.5,z),(2.5,-1.5,z),(2.5,1.5,z),(-2.5,1.5,z)]
        for face in [[(-2.5,-1.5,0),(2.5,-1.5,0),corners[1],corners[0]],
                     [(2.5,-1.5,0),(2.5,1.5,0),corners[2],corners[1]],corners]:
            c.poly([cam.project(p) for p in face],'#81bbb4',LINE,2)
        for i in range(1,5):
            c.line([cam.project((-2.5+i,-1.5,z)),cam.project((-2.5+i,1.5,z))],LINE,1.5)
        for j in range(1,3):
            c.line([cam.project((-2.5,-1.5+j,z)),cam.project((2.5,-1.5+j,z))],LINE,1.5)
        for _,pts in panels(5,3,2,1)[1:]:
            projected=[cam.project(p) for p in pts]
            c.line(projected+[projected[0]],LINE,2)
    if gate(t,4.6):note(c,'Surface area',775,205,41);note(c,'Count the faces.',775,262,30,MUTED)
    if gate(t,8.2):note(c,'Volume',775,375,41);note(c,'Fill the inside.',775,432,30,MUTED)
    if gate(t,10.4):note(c,'Base area × height',775,510,31,BLUE)
def applications(c,t):
    heading(c,'Match the edges at each fold')
    f=1-cue(t,15,3)+cue(t,21,2.4)
    f=min(1,f)
    model(c,f,labels=f<.06)
    note(c,'Card',780,228,40);note(c,'Which faces are needed?',780,282,30,MUTED)
    if gate(t,23.0):note(c,'Fixed volume',780,401,39);note(c,'Which base uses least card?',780,456,28,BLUE)
def volume_question(c,t):
    heading(c,'How many unit cubes fill this block?')
    cam=Camera(400,410,75,34,34)
    pile(c,cam,12*cue(t,33.6,1.8),lower=12*cue(t,31.35,1.8))
    if gate(t,31.8):measure(c,cam,(-2,-1.5,0),(2,-1.5,0),'4',-11,27)
    if gate(t,33):measure(c,cam,(2,-1.5,0),(2,1.5,0),'3',25,13)
    if gate(t,34.8):measure(c,cam,(2,1.5,0),(2,1.5,2),'2',30,0)
    if gate(t,36.4):note(c,'4 long × 3 wide × 2 high',750,266,32)
    if gate(t,39.2):note(c,'Look for equal layers.',750,374,33,BLUE)
def volume_answer(c,t):
    heading(c,'Build one layer, then another')
    cam=Camera(401,421,75,34,34)
    build=cue(t,45.5,2.2);top=cue(t,50.2,1.4);settle=cue(t,51.7,1.5)
    pile(c,cam,12*top,.64*(1-settle),12*build)
    if gate(t,47):note(c,'1 layer',775,195,37);note(c,'4 × 3 = 12 cubes',775,255,33,BLUE)
    if gate(t,50.35):note(c,'2 layers',775,385,37)
    if gate(t,52.2):note(c,'2 × 12 = 24 cubes',775,445,34,OCHRE)
def medium(c,t):
    heading(c,'Open the box along its hinges')
    f=1-cue(t,61.4,4.0)
    model(c,f,labels=f<.03)
    note(c,'Base',790,196,34);note(c,'5 by 3 units',790,247,35,BLUE)
    if gate(t,57.8):note(c,'Wall height',790,335,34);note(c,'2 units',790,385,35,OCHRE)
    if gate(t,64.8):note(c,'Each wall shares a base edge.',720,516,28)
def card_answer(c,t):
    heading(c,'Add the five faces of card')
    selected={0}
    if t>=73.9:selected.update((1,2))
    if t>=76.2:selected.update((3,4))
    model(c,0,labels=True,shaded=selected)
    note(c,'Base      5 × 3 = 15',770,195,32)
    if gate(t,74):note(c,'Long walls   2 × 5 × 2 = 20',745,277,30,OCHRE)
    if gate(t,76.2):note(c,'Short walls  2 × 3 × 2 = 12',745,351,30,BLUE)
    if gate(t,80.4):note(c,'15 + 20 + 12',785,441,43)
    if gate(t,82.6):note(c,'47 square units',785,517,38)
def challenge(c,t):
    heading(c,'Keep the volume. Use the least card.')
    # One possible footprint is shown without revealing the optimum.
    cam=Camera(386,400,51,36-11*cue(t,87,6),37)
    net(c,cam,9,4,3,1)
    measure(c,cam,(4.5,2,0),(4.5,2,3),'3 cm',30,0)
    note(c,'Height  3 cm',763,197,36)
    if gate(t,89.2):note(c,'Volume  108 cm³',763,278,38,BLUE)
    if gate(t,93.2):note(c,'Whole-number base sides',763,369,29,MUTED)
    if gate(t,96.):note(c,'How little card will work?',763,487,31,OCHRE)
PAIRS=[(a,36//a) for a in range(1,isqrt(36)+1) if 36%a==0]
def footprints(c,t):
    heading(c,'Different footprints can hold the same volume')
    c.text('Base = 108 ÷ 3 = 36 cm²',640,152,36,BLUE,bold=True)
    for i,(a,b) in enumerate(PAIRS):
        if not gate(t,109.1+i*.95):continue
        cy=225+i*72;u=10
        note(c,f'{a} × {b}',85,cy,31,INK)
        x=285;y=cy-a*u/2
        c.rect(x,y,b*u,a*u,BASE,LINE,2)
        for j in range(1,b):c.line([(x+u*j,y),(x+u*j,y+a*u)],'#739b8d',1)
        for j in range(1,a):c.line([(x,y+u*j),(x+b*u,y+u*j)],'#739b8d',1)
        if gate(t,123.3+i*.42):note(c,f'Side sum  {a+b}',735,cy,29,INK if i!=4 else BLUE)
        if i==4 and gate(t,126.6):note(c,'smallest',1018,cy,30,BLUE)
    if gate(t,114.5) and t<123.3:
        note(c,'Wall area',730,302,35)
        note(c,'2 × 3 × (a + b)',730,371,36,OCHRE)
def optimum(c,t):
    heading(c,'The least card is 108 cm²')
    f=1-cue(t,132,3.5)
    cam=Camera(371,367+38*f,36,34*f,90-54*f)
    net(c,cam,6,6,3,f,labels=f<.04)
    note(c,'Base     6 × 6 = 36',734,201,33)
    if gate(t,131.1):note(c,'Walls    4 × 6 × 3 = 72',734,272,32,OCHRE)
    if gate(t,132.8):note(c,'36 + 72 = 108 cm²',734,355,37,BLUE)
    if gate(t,138):note(c,'Shorter side ≤ √36 = 6',734,453,30)
    if gate(t,144.6):note(c,'All five factor pairs checked.',734,522,28,MUTED)
def mistakes(c,t):
    heading(c,'Card covers faces. Cubes fill space.')
    fold=cue(t,148.1,3.0)
    model(c,fold)
    if gate(t,148):note(c,'1 base + 4 walls',781,190,36)
    if gate(t,151.6):note(c,'The top stays open.',781,253,30,OCHRE)
    if gate(t,154.4):note(c,'Capacity   108 cm³',755,385,32,BLUE)
    if gate(t,156.6):note(c,'Least card   108 cm²',755,464,32,INK)
def recap(c,t):
    heading(c,'From a drawing to a proof')
    fold=1-cue(t,162.7,2.5)
    model(c,fold,labels=fold<.03)
    note(c,'Draw and label the net.',755,205,32)
    if gate(t,165.6):note(c,'Count each face once.',755,289,32)
    if gate(t,170.4):note(c,'Base area = volume ÷ height',725,382,29,BLUE)
    if gate(t,175.2):note(c,'Compare all legal surfaces.',735,485,30,OCHRE)
SCENES=(idea,applications,volume_question,volume_answer,medium,card_answer,challenge,footprints,optimum,mistakes,recap)

def verify():
    from math import dist,isclose
    for a,b,h in [(5,3,2),(6,6,3),(9,4,3)]:
        for f in (0,.2,.5,.82,1):
            fs=panels(a,b,h,f)
            for i,(_,pts) in enumerate(fs):
                dims=(a,b) if i==0 else (a,h) if i<=2 else (b,h)
                assert isclose(dist(pts[0],pts[1]),dims[0]) and isclose(dist(pts[1],pts[2]),dims[1])
            assert len(fs)==5
    assert len(set(product(range(4),range(3),range(2))))==24
    assert 5*3+2*5*2+2*3*2==47
    cases=[(a,b,36+2*3*(a+b)) for a,b in PAIRS]
    assert cases==[(1,36,258),(2,18,156),(3,12,126),(4,9,114),(6,6,108)]
    assert min(cases,key=lambda c:c[2])==(6,6,108)
