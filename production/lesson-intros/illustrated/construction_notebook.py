"""T12.3. A parallel rule through a bend, matched angular sectors and a grid dissection of a tilted square."""
from math import sin,cos,tan,radians,atan2,degrees,pi,hypot
from captioned_film import cue,mix,font
ID='T12.3';ORIGINAL='bd9f0f0b039c224d91c6209e697a295dd7114125405fdf9e054c01d63ad463e6'
START=(0,14.52,28.12,45.36,51.77,64.41,88.24,98.65);POSTER=83.9
PAPER='#f4f0e7';INK='#28394a';GRID='#d0cec1';OCEAN='#246b89';TEAL='#197863';RED='#a65037';PURPLE='#755292';PEACH='#e8b08d';MINT='#b3d8c9';SKY='#b1d5df';CREAM='#fff9e7'
def label(c,s,x,y,z=30,col=INK,anchor='lm'):c.text(s,x,y,z,col,anchor,True)
def title(c,s):
    size=42
    while font(round(size*c.scale),True).getlength(s)>1146*c.scale:size-=1
    label(c,s,60,61,size)
def draw(c,a,b,p,col=INK,width=3):
    c.line([a,(mix(a[0],b[0],p),mix(a[1],b[1],p))],col,width)
def dashed(c,a,b,col=OCEAN):
    n=int(hypot(b[0]-a[0],b[1]-a[1])/15)+1
    for k in range(n):
        p=k/n;q=min(1,(k+.53)/n);c.line([(mix(a[0],b[0],p),mix(a[1],b[1],p)),(mix(a[0],b[0],q),mix(a[1],b[1],q))],col,2)
def wedge(c,p,a,b,r,tone,edge):
    pts=[p]
    for j in range(41):
        theta=radians(mix(a,b,j/40));pts.append((p[0]+r*cos(theta),p[1]+r*sin(theta)))
    c.poly(pts,tone,edge,2)
def squaremark(c,x,y,k=15):
    c.line([(x,y-k),(x+k,y-k),(x+k,y)],TEAL,3)
B=(554,313);A=(B[0]-133/tan(radians(35)),180);C=(B[0]-153,466)
def path(c,aux=0):
    for y in (A[1],C[1]):c.line([(131,y),(749,y)],OCEAN,3)
    if aux:draw(c,(131,B[1]),(749,B[1]),aux,PURPLE,3)
    c.line([A,B,C],INK,4)
    for p in (A,B,C):c.dot(*p,5,INK)
def ruler(c,y):
    x=145;w=583
    c.rect(x,y,w,32,'#e9d7b0','#aa8f63',2)
    for i in range(39):
        xx=x+6+i*15;c.line([(xx,y+1),(xx,y+(11 if i%5==0 else 6))],'#90734c',1.5)
def mainangles(c,both=True):
    wedge(c,A,0,35,61,PEACH,RED);label(c,'35°',A[0]+80,A[1]+20,26,RED)
    if both:wedge(c,C,-45,0,51,MINT,TEAL);label(c,'45°',C[0]+70,C[1]-18,26,TEAL)
def intro(c,t):
    title(c,'Add the line that connects the known angles')
    p=cue(t,3.88,1.75);path(c,p)
    if t>=5.38:mainangles(c)
    if t>=8.72:
        k=1-cue(t,11,1.35)
        if k>0:draw(c,(157,459),(642,187),k,GRID,2)
    label(c,'What must the new line do?',786,205,29)
    if t>=5.38:label(c,'Carry a known angle.',786,325,32,OCEAN)
def choices(c,t):
    title(c,'Three constructions with three different jobs')
    for i,x in enumerate((220,632,1027)):
        y=324
        if i==0:
            c.line([(x-118,y-40),(x+118,y-40)],OCEAN,3);c.line([(x-118,y+40),(x+118,y+40)],OCEAN,3)
            if t>=22.36:c.line([(x-89,y+83),(x+83,y-89)],RED,3)
        elif i==1:
            c.poly([(x-105,y+58),(x+95,y+58),(x-32,y-68)],SKY,INK,2)
            if t>=23.3:dashed(c,(x-32,y-68),(x-32,y+58),TEAL);squaremark(c,x-32,y+58,12)
        else:
            pts=[(x-96,y+55),(x+96,y+55),(x,y-62)];c.line(pts[:2],INK,3)
            if t>=24.8:
                c.line([pts[0],pts[2],pts[1]],PURPLE,3)
                for sign in (-1,1):
                    xm=x+sign*48;c.line([(xm-8,y+1),(xm+8,y-6)],PURPLE,3)
        if t>=(22.36,23.3,24.8)[i]:label(c,('Parallel lines','A height','Equal sides')[i],x,474,27,(OCEAN,TEAL,PURPLE)[i],'mm')
def ask(c,t):
    title(c,'How large is the angle at the bend?');path(c)
    if t>=33.26:mainangles(c,t>=35.72)
    if t>=38.04:wedge(c,B,135,215,47,SKY,OCEAN);label(c,'?',B[0]-70,B[1],32,OCEAN)
    label(c,'Two parallel lines',799,219,32,OCEAN)
    if t>=39.76:label(c,'Which line would help?',799,360,30)
def add(c,t):
    title(c,'Slide a parallel rule until its edge meets the bend')
    p=cue(t,45.36,2.0);path(c,cue(t,47.0,1.65));mainangles(c)
    if t<48.76:ruler(c,mix(A[1],B[1],p))
    if t>=48.76:
        wedge(c,B,180,215,57,PEACH,RED);wedge(c,B,135,180,57,MINT,TEAL)
    label(c,'Same direction at every height',785,239,25,PURPLE)
    if t>=48.76:label(c,'Two parts of one angle',785,363,29)
def transport(c,p,q,a,b,r,col,edge,f):
    center=(mix(p[0],q[0],f),mix(p[1],q[1],f))
    wedge(c,center,a+180*f,b+180*f,r,col,edge)
def join(c,t):
    title(c,'Match the two angles across the new parallel')
    path(c,1);mainangles(c)
    p=cue(t,51.9,2.45);q=cue(t,56.47,1.7)
    if p:transport(c,A,B,0,35,53,PEACH,RED,p)
    if q:transport(c,C,B,-45,0,53,MINT,TEAL,q)
    if t>=54.59:label(c,'Upper angle   35°',806,203,29,RED)
    if t>=56.47:label(c,'Lower angle   45°',806,294,29,TEAL)
    if t>=58.75:label(c,'35° + 45°',806,390,35)
    if t>=61.35:label(c,'= 80°',806,455,42,OCEAN)
def tiled(c,t,k,mini=False):
    w=69 if k==3 else 87;x=211;y=172;n=k+1
    def pt(q):return(x+q[0]*w,y+q[1]*w)
    for i in range(n+1):
        c.line([pt((0,i)),pt((n,i))],GRID,1);c.line([pt((i,0)),pt((i,n))],GRID,1)
    pts=((1,0),(n,1),(k,n),(0,k));outer=((n,0),(n,n),(0,n),(0,0));drawn=t>=67.07 if not mini else True
    if drawn:
        c.poly([pt(z) for z in pts],MINT,TEAL,3)
        # Keep the integer grid visible through the interior of the tilted square.
        for i in range(1,n):
            for vertical in (False,True):
                axis=int(not vertical);other=1-axis;loc=i;inter=[]
                for a,b in zip(pts,(*pts[1:],pts[0])):
                    if a[axis]==b[axis] or (loc-min(a[axis],b[axis]))*(loc-max(a[axis],b[axis]))>0:continue
                    ratio=(loc-a[axis])/(b[axis]-a[axis]);p=[0,0];p[axis]=loc;p[other]=mix(a[other],b[other],ratio);inter.append(pt(p))
                if len(inter)>=2:c.line([min(inter),max(inter)],'#91c2ad',1)
    if (not mini and t>=68.79) or mini and t>=110.81:
        v=cue(t,68.79 if not mini else 110.81,1);draw(c,pt(pts[0]),pt(outer[0]),v,RED,4)
        label(c,str(k),x+(1+k/2)*w,y-26,27,RED,'mm')
    if (not mini and t>=71.25) or mini and t>=113.37:
        draw(c,pt(outer[0]),pt(pts[1]),1,PURPLE,4);label(c,'1',x+n*w+27,y+w/2,26,PURPLE,'mm')
    return w,pt,pts,outer
def area(c,t):
    title(c,'Find the tilted square inside an exact 4 × 4 grid')
    w,pt,pts,outer=tiled(c,t,3)
    if t>=74.23:
        c.line([pt(v) for v in ((0,0),(4,0),(4,4),(0,4),(0,0))],INK,2)
        label(c,'Outer square   4 × 4 = 16',776,177,28)
    if t>=77.99:
        for i in range(4):
            p=cue(t,77.99+i*.4,1.1)
            if p:
                v=[pts[i],outer[i],pts[(i+1)%4]];dx,dy=((1,-1),(1,1),(-1,1),(-1,-1))[i];sep=18*cue(t,80.81,1.55)
                c.poly([(pt(a)[0]+dx*sep,pt(a)[1]+dy*sep) for a in v],PEACH,RED,2)
        label(c,'1 triangle   ½ × 3 × 1 = 1½',776,263,27,RED)
    if t>=80.81:label(c,'4 triangles   4 × 1½ = 6',776,340,28,RED)
    if t>=83.47:label(c,'16 − 6 = 10 square units',775,444,29,TEAL)
def height(c,t):
    title(c,'Drop a perpendicular to split the triangle')
    a=(176,453);b=(675,453);v=(365,179);d=(365,453)
    c.poly([a,b,v],SKY,INK,3)
    p=cue(t,91.6,1.9);draw(c,v,d,p,TEAL,4)
    if t>=94.54:
        c.poly([a,d,v],MINT,TEAL,3);c.poly([v,d,b],PEACH,RED,3);squaremark(c,*d,18)
        label(c,'Both triangles contain 90°.',788,302,28,TEAL)
    elif t>=91.6:label(c,'Straight down to the base',788,299,27,OCEAN)
def notebook(c,t):
    if t<107.61:
        title(c,'Choose the extra line for the fact you need')
        if t<103.04:path(c,1);mainangles(c);label(c,'A parallel carries angles.',780,299,29,OCEAN)
        elif t<104.35:
            c.poly([(196,441),(672,441),(373,178)],MINT,TEAL,3);dashed(c,(373,178),(373,441),OCEAN);squaremark(c,373,441)
            label(c,'A height creates a right angle.',780,299,27,TEAL)
        else:tiled(c,80,3);label(c,'A grid makes areas exact.',780,299,29,TEAL)
    else:
        title(c,'Find the area after moving two right and one down')
        tiled(c,t,2,True);label(c,'Trace the tilted square.',784,238,30,TEAL)
        if t>=114.99:label(c,'Which four pieces lie outside it?',784,355,25,RED)
SCENES=(intro,choices,ask,add,join,area,height,notebook)
def verify():
    upper=degrees(atan2(B[1]-A[1],B[0]-A[0]));lower=degrees(atan2(C[1]-B[1],B[0]-C[0]));assert abs(upper-35)<1e-9 and abs(lower-45)<1e-9
    for k,out in ((3,10),(2,5)):
        n=k+1;v=((1,0),(n,1),(k,n),(0,k));dirs=[(v[(j+1)%4][0]-x,v[(j+1)%4][1]-y) for j,(x,y) in enumerate(v)]
        assert all(x*x+y*y==out and x*dirs[(j+1)%4][0]+y*dirs[(j+1)%4][1]==0 for j,(x,y) in enumerate(dirs))
        assert n*n-4*k/2==out
