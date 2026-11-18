"""T12.1. Lay a calibrated straightedge, slide a marked tracing and turn both base angles onto a parallel."""
from math import atan,atan2,cos,sin,pi,radians,degrees,tan,hypot
from captioned_film import cue,mix,font
ID='T12.1';ORIGINAL='ef0a6580ad766664ad876d76a753afd7239d39bc0595af732fefdb06192c846b';START=(0,19.32,28.77,43.30,59.14,73.22,91.29,105.21);POSTER=68.2
PAPER='#192739';INK='#f8ecda';LINE='#67809a';BLUE='#8ecaea';GREEN='#91dfbd';YELLOW='#f4c86e';ROSE='#eeaa9b';DARK='#23384b';SOFT='#b5c8ce'

def title(c,s):
    size=42
    while font(round(size*c.scale),True).getlength(s)>1149*c.scale:size-=1
    c.text(s,62,62,size,INK,'lm',True)
def note(c,s,x,y,sz=32,col=INK):c.text(s,x,y,sz,col,'lm',True)
def ray(p,a,r):return (p[0]+r*cos(radians(a)),p[1]+r*sin(radians(a)))
def dis(a,b):return degrees(atan2(b[1]-a[1],b[0]-a[0]))
def blended(a,b,p):return (mix(a[0],b[0],p),mix(a[1],b[1],p))
def rgb(col):return tuple(int(col[i:i+2],16) for i in (1,3,5))
def tint(col):return tuple(round(v*.19+w*.81) for v,w in zip(rgb(col),rgb(PAPER)))
def wedge(c,p,a,b,r,col,lab='',offset=17):
    steps=max(3,int(abs(b-a)/2));arc=[ray(p,mix(a,b,k/steps),r) for k in range(steps+1)];c.poly([p,*arc],tint(col),None);c.line(arc,col,3)
    if lab:c.text(lab,*ray(p,(a+b)/2,r+offset),26,col,bold=True)
def stroke(c,p,q,col,k=1,w=3,pen=False):
    v=blended(p,q,k);c.line([p,v],col,w)
    if pen and k<.995:
        x,y=v;c.poly([(x,y),(x+6,y-21),(x+30,y-46),(x+40,y-35),(x+16,y-10)],YELLOW,INK,1.4);c.dot(x,y,3,INK)

def basics(c,t):
    title(c,'Build an angle chain from facts')
    if t<8.3:
        # One real example moves from a given angle, through the corresponding angle, to its supplement.
        parallel_lines(c,1);top,lower=crosses();wedge(c,top,-65,0,43,YELLOW,'65°')
        if t>=3.18:
            p=blended(top,lower,cue(t,3.18,1.65));wedge(c,p,-65,0,43,GREEN,'65°')
        if t>=5.84:wedge(c,lower,-180,-65,56,ROSE,'115°')
        note(c,'Given → copy → supplement',783,364,27,SOFT)
    elif t<13.785:
        O=(404,329);c.line([(187,329),(623,329)],LINE,2);k=cue(t,8.3,1.8);l=cue(t,11.1,2.2);angle=180*k+180*l
        stroke(c,O,ray(O,-angle,158),YELLOW);wedge(c,O,0,-angle,101,YELLOW);c.dot(*O,6,INK)
        note(c,'Straight angle   180°',705,245,31,BLUE)
        if t>=11.08:note(c,'Full turn   360°',705,359,33,GREEN)
    else:
        O=(418,340)
        for a in (0,-52):c.line([ray(O,a,198),ray(O,a+180,198)],BLUE,4)
        wedge(c,O,-52,0,72,YELLOW,'a');wedge(c,O,128,180,72,YELLOW,'a');note(c,'Vertically opposite',737,278,32,GREEN);note(c,'angles are equal.',737,341,32)

def parallel_lines(c,p):
    top,low=crosses()
    for y in (top[1],low[1]):
        stroke(c,(158,y),(849,y),BLUE,min(1,p*1.7),4,True)
        if p>.5:c.line([(236,y-9),(250,y),(236,y+9)],BLUE,3)
    a=ray(top,-65,76);b=ray(low,115,83);stroke(c,a,b,INK,max(0,min(1,(p-.34)/.66)),3,True)

def crosses():
    H=209;dx=H/tan(radians(65));return (601,205),(601-dx,205+H)

def rules(c,t):
    title(c,'What does the drawing actually guarantee?')
    L,R=186,751;y=314
    # Both pairs have matching parallel marks. Moving one whole pair changes the angle in a second diagram.
    for j,(x,a) in enumerate(((L,54),(R,74))):
        for yy in (255,399):
            c.line([(x-71,yy),(x+282,yy)],BLUE,3);c.line([(x-25,yy-8),(x-12,yy),(x-25,yy+8)],BLUE,2.5)
        o=(x+113,y);c.line([ray(o,-a,169),ray(o,180-a,169)],INK,3)
        if t>=22.72:
            dx=(y-255)/tan(radians(a));wedge(c,(o[0]+dx,255),-a,0,37,YELLOW)
            dx=(399-y)/tan(radians(a));wedge(c,(o[0]-dx,399),-a,0,37,GREEN)
    if t>=25.82:note(c,'Matching positions on parallel lines give equal angles.',142,544,31,GREEN)

def question(c,t):
    title(c,'Find the marked angle at the lower crossing');parallel_lines(c,cue(t,28.77,2.1));top,low=crosses()
    if t>=31.87:wedge(c,top,-65,0,52,YELLOW,'65°')
    if t>=34.79:wedge(c,low,-180,-65,66,ROSE,'?')
    if t>=36.79:
        p=cue(t,36.79,2.5);origin=blended(top,low,p);c.dot(*origin,7,GREEN)
        note(c,'Follow the crossing',874,260,25,SOFT);note(c,'down the transversal.',862,309,24,SOFT)

def copy(c,t):
    title(c,'Slide the 65° tracing to the matching corner');parallel_lines(c,1);top,low=crosses();wedge(c,top,-65,0,53,YELLOW,'65°')
    p=cue(t,49.30,2.12);o=blended(top,low,p)
    if t>=46.6:
        # Both traced rays move as one rigid piece. The plate never changes angle or radius.
        for a in (-65,0):c.line([o,ray(o,a,90)],GREEN,3)
        wedge(c,o,-65,0,50,GREEN,'65°' if p==1 else '')
        if 0<p<1:c.dot(*o,5,GREEN)
    if t>=54.02:note(c,'Same angle',867,276,33,GREEN);note(c,'Same orientation',858,335,26)
    if t>=56.26:note(c,'Corresponding angles',762,529,29,YELLOW)

def supplement(c,t):
    title(c,'The two adjacent angles fill one straight angle');parallel_lines(c,1);top,low=crosses()
    wedge(c,top,-65,0,48,YELLOW,'65°');wedge(c,low,-65,0,54,GREEN,'65°');p=cue(t,61.86,1.5)
    wedge(c,low,-180,mix(-180,-65,p),71,ROSE,'115°' if t>=65.54 else '?')
    if t>=63.06:note(c,'180° − 65°',864,253,37)
    if t>=65.54:note(c,'= 115°',865,332,41,ROSE)
    if t>=68.94:note(c,'Corresponding, then supplementary.',645,541,29,GREEN)

def triangle(c,t):
    title(c,'Move both base angles onto the parallel through the apex')
    A,B,C=(214,470),(784,470),(472,210)
    c.poly([A,B,C],DARK,BLUE,3);la=-dis(A,C);rb=180+dis(B,C)
    wedge(c,A,-la,0,57,YELLOW,'a');wedge(c,B,-180,-180+rb,57,GREEN,'b')
    if t>=76.88:stroke(c,(148,C[1]),(877,C[1]),SOFT,cue(t,76.88,2.1),3,True)
    p=cue(t,80.58,2.55)
    if p>0:
        # Turn each translucent base wedge through 180° while translating it to its alternate interior position.
        for orig,start,end,col,lab in ((A,-la,0,YELLOW,'a'),(B,-180,-180+rb,GREEN,'b')):
            o=blended(orig,C,p);wedge(c,o,start+180*p,end+180*p,57,col,lab if p>.91 else '')
        wedge(c,C,rb,180-la,61,BLUE,'c')
    if t>=83.28:note(c,'a + c + b',896,271,32)
    if t>=86.62:note(c,'= 180°',896,339,39,YELLOW)

def iso(c,t,small,question_mode=False):
    x,y=536,192;h=304;w=h/tan(radians(small));A=(x-w,y+h);B=(x+w,y+h);C=(x,y)
    c.poly([A,B,C],DARK,BLUE,3)
    if not question_mode or t>=108.39:
        for a in (A,B):
            pt=blended(C,a,.5);d=dis(C,a)+90;c.line([ray(pt,d,10),ray(pt,d+180,10)],YELLOW,3)
    if question_mode:
        if t>=111.87:wedge(c,A,-small,0,51,GREEN,'55°');wedge(c,B,180,180+small,51,GREEN,'55°')
        if t>=115.51:wedge(c,C,small,180-small,51,ROSE,'?')
    else:
        if t>=93.87:
            for a,d1,d2 in [(A,-small,0),(B,180,180+small)]:wedge(c,a,d1,d2,51,GREEN,'70°' if t>=101.51 else 'x')
        if t>=98.67:wedge(c,C,small,180-small,58,YELLOW,'40°')

def equal(c,t):
    title(c,'Equal sides have equal opposite angles');iso(c,t,70)
    if t>=98.67:note(c,'180° − 40° = 140°',781,258,33)
    if t>=101.51:note(c,'140° ÷ 2 = 70°',781,348,34,GREEN)

def practice(c,t):
    title(c,'Notebook challenge · find the third angle');iso(c,t,55,True)
    if t>=108.39:note(c,'Two equal sides',809,250,33,YELLOW)
    if t>=111.87:note(c,'Two 55° angles',809,336,33,GREEN)
    if t>=115.51:note(c,'55° + 55° + ? = 180°',827,432,27)
SCENES=(basics,rules,question,copy,supplement,triangle,equal,practice)
def verify():
    a,b=crosses();assert abs(dis(a,b)-115)<1e-7 and 65+115==180
    A,B,C=(214,470),(784,470),(472,210);u=-dis(A,C);v=180+dis(B,C);peak=abs(dis(C,A)-dis(C,B));assert abs(u+v+peak-180)<1e-8
    for small,peak in [(70,40),(55,70)]:
        w=304/tan(radians(small));assert abs(2*degrees(atan(w/304))-peak)<1e-8
