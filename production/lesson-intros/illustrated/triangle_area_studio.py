"""T13.1. A half-turn, a height-preserving shear, three rigid cutouts and a movable apex."""
from fractions import Fraction
from math import cos,pi,sin,hypot
from captioned_film import cue,mix,font
ID='T13.1';ORIGINAL='f941cf5944869274bdb6151774bf83e79ede38c18d15a4561d3c78d53d3713c8'
START=(0,17.56,30.36,48.25,66.49,82.65,95.62,109.86);POSTER=63.61
PAPER='#eaf1ee';INK='#203646';SOFT='#566d74';GRAPH='#bdceca';TEAL='#137967';BLUE='#285b92';SAFF='#9a570f';ROSE='#a64157';P1='#a7d8c2';P2='#f4d59a';P3='#a8c6df';P4='#e9b8be';LIGHT='#f8fbf6'

def title(c,s):
    size=42
    while font(round(size*c.scale),True).getlength(s)>1154*c.scale:size-=1
    c.text(s,62,61,size,INK,'lm',True)
def txt(c,s,x,y,size=32,col=INK):c.text(s,x,y,size,col,'lm',True)
def rotate(v,o,angle):
    x,y=v[0]-o[0],v[1]-o[1];return (o[0]+x*cos(angle)-y*sin(angle),o[1]+x*sin(angle)+y*cos(angle))
def dashed(c,a,b,col,width=2):
    dx,dy=b[0]-a[0],b[1]-a[1];length=hypot(dx,dy)
    if not length:return
    for k in range(0,int(length),17):
        p=k/length;q=min(1,(k+9)/length);c.line([(a[0]+dx*p,a[1]+dy*p),(a[0]+dx*q,a[1]+dy*q)],col,width)
def right(c,x,y,sx=1,sy=-1,n=17,colour=INK):c.line([(x+sx*n,y),(x+sx*n,y+sy*n),(x,y+sy*n)],colour,2.5)
def measure(c,a,b,label,col,vertical=False):
    c.line([a,b],col,2)
    for x,y in (a,b):
        c.line([(x-7,y),(x+7,y)] if vertical else [(x,y-7),(x,y+7)],col,2.4)
    x=(a[0]+b[0])/2;y=(a[1]+b[1])/2
    c.text(label,x+(14 if vertical else 0),y+(0 if vertical else 27),27,col,'lm' if vertical else 'mm',True)

def rigid(c,t):
    title(c,'Two identical triangles make one parallelogram')
    shear=cue(t,4.8,2.6);A=(166,460);B=(535,460);C=(252-86*shear,231);pivot=((B[0]+C[0])/2,(B[1]+C[1])/2)
    c.line([(111,231),(699,231)],GRAPH,2);c.line([(111,460),(699,460)],GRAPH,2)
    c.poly([A,B,C],P1,TEAL,4)
    turn=cue(t,.64,2.35)
    if turn>0:
        twin=[rotate(v,pivot,pi*turn) for v in (A,B,C)];c.poly(twin,P2,SAFF,3);c.dot(*pivot,6,INK)
    if t<5:txt(c,'The copy turns 180°.',744,283,32,SAFF)
    elif t<9.26:
        txt(c,'Same base',746,248,36,TEAL);txt(c,'Same height',746,325,36,BLUE)
    else:
        txt(c,'Area of one triangle',710,215,32);txt(c,'= ½ × base × height',710,297,35,TEAL)
    if t>=12.9:
        dashed(c,(C[0],460),C,BLUE,3);measure(c,(110,231),(110,460),'h',BLUE,True)
        if t>=15.16:right(c,C[0],460,1,-1,21,BLUE)

def common_error(c,t):
    title(c,'Which line measures the height?')
    if t<24.38:
        A=(153,470);B=(673,470);C=(329,163);c.poly([A,B,C],P1,TEAL,3)
        q=cue(t,17.56,1.25);c.line([A,(mix(A[0],C[0],q),mix(A[1],C[1],q))],ROSE,7)
        txt(c,'Sloping side',754,242,35,ROSE)
        if t>=19.8:
            p=cue(t,19.8,1);dashed(c,C,(C[0],mix(C[1],470,p)),BLUE,4)
            if p>.95:right(c,C[0],470,1,-1,21,BLUE)
            txt(c,'Perpendicular height',754,338,31,BLUE)
    else:
        core,parts=outer_points();draw_frame(c,True);c.poly(core,P1,TEAL,3)
        for i,tr in enumerate(parts):
            if t>=26.1+i*.6:c.poly(tr,(P2,P3,P4)[i],(SAFF,BLUE,ROSE)[i],2)
        txt(c,'Rectangle',819,248,34);txt(c,'− outside pieces',819,335,32,SAFF)

def rail_base(c):
    c.line([(123,184),(949,184)],GRAPH,2);dashed(c,(123,484),(949,484),GRAPH)
    c.line([(220,484),(700,484)],INK,4);measure(c,(220,527),(700,527),'8 cm',INK)

def three(c,t):
    title(c,'Three triangles share one base');rail_base(c)
    tops=(279,541,793);colours=(TEAL,SAFF,BLUE)
    for i,(X,col) in enumerate(zip(tops,colours)):
        p=cue(t,30.6+i*1.14,.92)
        if p>0:
            a=(220,484);b=(700,484);peak=(X,184)
            # Draw the two rising sides to their fixed apex on the upper parallel.
            c.line([a,(mix(a[0],X,p),mix(a[1],184,p))],col,3);c.line([b,(mix(b[0],X,p),mix(b[1],184,p))],col,3)
            if p==1:c.dot(*peak,6,col)
    if t>=36.64:measure(c,(959,184),(959,484),'5 cm',BLUE,True)
    if t>=40.2:txt(c,'Which has the largest area?',805,565,24)

def slide(c,t):
    title(c,'Slide the apex. The height stays 5 cm.');rail_base(c)
    if t<60.73:
        for i,(X,col) in enumerate(zip((279,541,793),(TEAL,SAFF,BLUE))):
            c.line([(220,484),(X,184),(700,484)],col,3);c.dot(X,184,6,col)
            p=cue(t,48.25+.7*i,1)
            if p>0:dashed(c,(X,184),(X,184+300*p),col,2)
            if p==1:right(c,X,484,1,-1,14,col)
    else:
        X=mix(279,807,cue(t,60.73,2.35))-271*cue(t,63.3,2.2)
        c.poly([(220,484),(700,484),(X,184)],P1,TEAL,3);dashed(c,(X,184),(X,484),BLUE,3);right(c,X,484,1,-1,16,BLUE);c.dot(X,184,8,TEAL)
    if t>=48.25:measure(c,(928,184),(928,484),'5 cm',BLUE,True)
    if t>=54.23:txt(c,'½ × 8 × 5',791,532,31,TEAL)
    if t>=56.67:txt(c,'= 20 cm²',1012,532,30,TEAL)

def g(x,y):return (212+65*x,462-65*y)
def outer_points():
    core=[g(0,0),g(6,3),g(2,4)];parts=[[g(0,0),g(6,0),g(6,3)],[g(0,0),g(0,4),g(2,4)],[g(2,4),g(6,4),g(6,3)]]
    return core,parts

def draw_frame(c,grid=True,dimensions=True):
    c.rect(*g(0,4),390,260,LIGHT,INK,3)
    if grid:
        for i in range(1,6):c.line([g(i,0),g(i,4)],GRAPH,1.3)
        for j in range(1,4):c.line([g(0,j),g(6,j)],GRAPH,1.3)
    if dimensions:
        measure(c,g(0,-.55),g(6,-.55),'6 cm',INK);measure(c,g(-1.5,0),g(-1.5,4),'4 cm',INK,True)

def component(c,tr,i,shift,show):
    offsets=((72,49),(-41,-36),(87,-59));dx,dy=offsets[i];vs=[(x+dx*shift,y+dy*shift) for x,y in tr]
    c.poly(vs,(P2,P3,P4)[i],(SAFF,BLUE,ROSE)[i],3)
    x,y=vs[1];right(c,x,y,-1 if i!=1 else 1,-1 if i==0 else 1,12,(SAFF,BLUE,ROSE)[i]);
    if show:
        xx=sum(v[0] for v in vs)/3;yy=sum(v[1] for v in vs)/3;c.text(str((9,4,2)[i]),xx,yy,23,INK,bold=True)

def complement(c,t):
    title(c,'Find the slanted triangle inside a 6 by 4 rectangle');draw_frame(c)
    core,parts=outer_points();c.poly(core,P1,TEAL,3)
    if t>=74:txt(c,'Whole rectangle',771,187,32);txt(c,'6 × 4 = 24 cm²',771,248,34)
    if t>=76.57:
        for i,tr in enumerate(parts):
            if t>=76.57+i*.65:component(c,tr,i,0,t>=79.59+i*.29)
    if t>=79.59:
        for i,(a,b,col) in enumerate([(6,3,SAFF),(4,2,BLUE),(4,1,ROSE)]):
            if t>=79.59+i*.29:txt(c,f'½ × {a} × {b} = {a*b//2}',775,327+i*55,28,col)

def subtract(c,t):
    title(c,'Remove the three right triangles');draw_frame(c,False,t<85.61)
    core,parts=outer_points();c.poly(core,P1,TEAL,4)
    for i,tr in enumerate(parts):component(c,tr,i,cue(t,85.61+i*.16,1.45),True)
    txt(c,'9 + 4 + 2 = 15',810,224,34)
    if t>=85.61:txt(c,'24 − 15 = 9',810,323,38,TEAL)
    if t>=88.05:
        x=sum(p[0] for p in core)/3;y=sum(p[1] for p in core)/3;c.text('9 cm²',x,y,29,TEAL,bold=True)
    if t>=91.95:txt(c,'Area left inside',810,431,29,SOFT)

def half(c,t):
    title(c,'Any point on the top edge gives the same half');L,R,T,B=188,848,173,470
    c.rect(L,T,R-L,B-T,LIGHT,INK,3);X=mix(329,745,cue(t,103.78,2.0))-435*cue(t,106.22,2.1)
    if t>=97.2:
        c.dot(X,T,8,TEAL);p=cue(t,97.2,2.4);apex=(X,T)
        if p==1:c.poly([(L,B),(R,B),apex],P1,TEAL,3)
        else:
            for v in ((L,B),(R,B)):c.line([apex,(mix(X,v[0],p),mix(T,v[1],p))],TEAL,3)
    if t>=101.32:dashed(c,(X,T),(X,B),BLUE,3);right(c,X,B,1,-1,16,BLUE)
    if t>=103.78:txt(c,'½',942,268,76,TEAL);txt(c,'of the rectangle',886,366,29)

def exercise(c,t):
    if t<119.32:
        title(c,'Use perpendicular height, or subtract surrounding areas')
        if t<116.3:
            c.rect(182,178,495,290,LIGHT,GRAPH,2);X=mix(260,559,cue(t,112.52,2.3));c.poly([(182,468),(677,468),(X,178)],P1,TEAL,3);dashed(c,(X,178),(X,468),BLUE);right(c,X,468)
            txt(c,'Area = ½ × b × h',756,300,35)
        else:
            draw_frame(c,True,False);core,parts=outer_points();c.poly(core,P1,TEAL,3)
            for i,tr in enumerate(parts):component(c,tr,i,cue(t,116.45,.95),True)
    else:
        title(c,'Notebook challenge · find the perpendicular height');L,R,T,B=213,653,173,481;X=379
        c.poly([(L,B),(R,B),(X,T)],P1,TEAL,3);measure(c,(L,520),(R,520),'10 cm',INK);dashed(c,(X,T),(X,B),BLUE,3);right(c,X,B,1,-1,17,BLUE)
        txt(c,'h = ?',398,319,30,BLUE)
        if t>=122.66:txt(c,'Area = 35 cm²',770,245,35,TEAL)
        if t>=126.1:txt(c,'½ × 10 × h = 35',769,337,32)

SCENES=(rigid,common_error,three,slide,complement,subtract,half,exercise)
def twice_area(vs):return abs(sum(v[0]*w[1]-v[1]*w[0] for v,w in zip(vs,vs[1:]+vs[:1])))
def verify():
    for x in range(170,970,5):assert Fraction(twice_area([(220,484),(700,484),(x,184)]),2*60**2)==20
    core,parts=outer_points();assert [Fraction(twice_area(poly),2*65**2) for poly in [core,*parts]]==[9,9,4,2]
    assert sum(Fraction(twice_area(p),2*65**2) for p in [core,*parts])==24
    A,B,C=(166,460),(535,460),(252,231);pivot=((B[0]+C[0])/2,(B[1]+C[1])/2)
    for i in range(31):
        v=[rotate(p,pivot,pi*i/30) for p in (A,B,C)];assert abs(twice_area(v)-twice_area([A,B,C]))<1e-6
    assert Fraction((653-213)*(481-173),2*44**2)==35
