"""S081. Construct every ray from its angle and recompute the incenter as the triangle changes shape."""
from math import atan2,cos,degrees,dist,isclose,pi,radians,sin,tan
from captioned_film import cue,mix
ID='S081'
ORIGINAL='4340914a42905bf29abde737e04cb1609de05615c36eb38fda00619db3256fe4'
START=(0,15.16,32.44,48.89,63.93,80.7,103.89,124.97,149.76,167.68,184.48)
POSTER=157.6
PAPER='#171e34';INK='#f4f3ec';SUB='#b2c4d1';EDGE='#d0d9e4';CYAN='#76decc';GOLD='#f3c276';PINK='#f1a7b5';FILL='#273550';INNER='#394f5a';GHOST='#49566b'
def head(c,s):c.text(s,63,61,41,INK,'lm',True)
def note(c,s,x,y,size=32,col=INK):c.text(s,x,y,size,col,'lm',True)
def radial(v,ang,r):
    a=radians(ang);return v[0]+r*cos(a),v[1]-r*sin(a)
def direction(v,p):return degrees(atan2(v[1]-p[1],p[0]-v[0]))
def delta(v,p,q):return (direction(v,q)-direction(v,p)+180)%360-180
def angle(v,p,q):return abs(delta(v,p,q))
def interp(a,b,t):return tuple(mix(x,y,t) for x,y in zip(a,b))
def trace(c,a,b,p,ink=EDGE,width=4):
    if p>0:c.line([a,interp(a,b,p)],ink,width)
def sector(c,v,a,b,r,col,p=1,fill=None,description=None,second=False):
    d=delta(v,a,b);s=direction(v,a);n=max(2,int(abs(d)*p/2)+2)
    pts=[radial(v,s+d*p*i/(n-1),r) for i in range(n)]
    if fill:c.poly([v,*pts],fill,None)
    c.line(pts,col,4)
    if second:c.line([radial(v,s+d*p*i/(n-1),r+6) for i in range(n)],col,1.8)
    if description and p>=.99:
        x,y=radial(v,s+d/2,r+23)
        c.text(description,x,y,23,col,bold=True)
def point(c,p,label,dx,dy,col=INK):
    c.dot(*p,4.5,col);c.text(label,p[0]+dx,p[1]+dy,25,col,bold=True)
def triangle(B,C,beta,gamma):
    h=(C[0]-B[0])/(1/tan(radians(beta))+1/tan(radians(gamma)))
    A=(B[0]+h/tan(radians(beta)),B[1]-h)
    a,b,c=dist(B,C),dist(C,A),dist(A,B)
    I=tuple((a*A[k]+b*B[k]+c*C[k])/(a+b+c) for k in (0,1))
    return A,I
def extend(B,A,length):
    d=dist(B,A);return tuple(A[k]+(A[k]-B[k])*length/d for k in (0,1))
def scale(c,O,r):
    for deg in range(0,181,5):
        a,b=radial(O,deg,r),radial(O,deg,r-(13 if deg%30==0 else 6))
        c.line([a,b],SUB if deg%30==0 else GHOST,2)
    pts=[radial(O,i,r) for i in range(181)]
    c.line(pts,GHOST,1.5)
def straight(c,deg,p=1,large=None,known=True,labels=True):
    O=(397,445);L=(99,445);R=(696,445);X=radial(O,deg,240)
    scale(c,O,244)
    trace(c,L,R,1,EDGE,4);trace(c,O,X,p,CYAN,5)
    if p>.98:
        sector(c,O,R,X,82,GOLD,description=(str(round(deg))+'°' if known else None))
        if large is not None:
            sector(c,O,X,L,111,PINK,description=large)
    if labels:
        for P,k,dx,dy in [(L,'L',0,28),(O,'O',0,29),(R,'R',0,28)]:point(c,P,k,dx,dy)
        if p>.98:point(c,X,'X',16,-14,CYAN)
def intro(c,t):
    head(c,'An angle measures a turn')
    O=(398,439);a=mix(15,112,cue(t,.8,3.6));scale(c,O,238)
    trace(c,O,radial(O,0,268),1);trace(c,O,radial(O,a,226),1,CYAN,5)
    sector(c,O,radial(O,0,180),radial(O,a,180),92,GOLD)
    if t>=3.4:trace(c,O,radial(O,180,263),cue(t,3.4,.8),EDGE,4)
    if t>=8.6:point(c,O,'O',0,30)
    note(c,'Two rays',778,212,40,CYAN)
    if t>=3.4:note(c,'One shared vertex',778,308,35)
    if t>=9.4:note(c,'Name the vertex first.',778,448,30,GOLD)
def middle(c,t,showA=False,answer=False,control=1,exterior=True):
    B,C=(153,480),(589,480);A,I=triangle(B,C,44,58);D=(735,480)
    c.poly([A,B,C],FILL,EDGE,4)
    if exterior:trace(c,C,D,control,SUB,4)
    if t>=0:
        sector(c,B,C,A,43,GOLD,description='44°')
        sector(c,C,A,B,42,CYAN,description='58°')
    if showA:sector(c,A,B,C,42,PINK,description='78°' if answer or t>=84.6 else '?')
    if exterior and control>=.98:
        sector(c,C,D,A,67,PINK,description='122°' if answer else '?')
    for P,k,dx,dy in [(A,'A',0,-22),(B,'B',-13,25),(C,'C',0,27)]:point(c,P,k,dx,dy)
    if exterior and control>.98:point(c,D,'D',7,25)
def use(c,t):
    head(c,'Extend a side to reveal another angle')
    B,C=(175,485),(572,485);A,I=triangle(B,C,49,63);D=(716,485)
    c.poly([A,B,C],FILL,EDGE,4)
    trace(c,C,D,cue(t,17,1.7))
    if t>=19:sector(c,C,D,A,57,GOLD,cue(t,19,1.6))
    if t>=24.4:
        trace(c,B,I,cue(t,24.4,1.4),CYAN);trace(c,C,I,cue(t,25.4,1.4),PINK)
    for P,k,dx,dy in [(A,'A',0,-22),(B,'B',-12,25),(C,'C',0,26)]:point(c,P,k,dx,dy)
    note(c,'Look for a straight line.',760,217,32)
    if t>=21.6:note(c,'Triangle angles total 180°.',760,320,29,GOLD)
    if t>=25:note(c,'A bisector halves an angle.',760,434,29,CYAN)
def basic(c,t):
    head(c,'What angle does the 37° turn leave?')
    straight(c,37,cue(t,35.9,1.4),'?' if t>=39.5 else None)
    note(c,'L, O, R lie on one line.',763,231,32)
    if t>=36.6:note(c,'∠XOR = 37°',763,327,42,GOLD)
    if t>=39.5:note(c,'Find ∠LOX.',763,436,37,PINK)
def basic_answer(c,t):
    head(c,'Two turns make one straight angle')
    straight(c,37,1,'143°' if t>=59.7 else '?')
    note(c,'∠LOX + 37° = 180°',755,230,38)
    if t>=57.5:note(c,'180° − 37°',755,338,40,GOLD)
    if t>=59.8:note(c,'∠LOX = 143°',755,445,42,PINK)
def medium(c,t):
    head(c,'Extend BC through C')
    middle(c,t,showA=t>=73.1,control=cue(t,69.9,1.5),exterior=t>=69.9)
    note(c,'∠B = 44°',787,202,38,GOLD)
    if t>=66:note(c,'∠C = 58°',787,281,38,CYAN)
    if t>=73.1:note(c,'Find ∠A and ∠ACD.',773,425,32)
def medium_answer(c,t):
    head(c,'One triangle sum, then one straight line')
    middle(c,t,True,t>=94.6)
    note(c,'180° − 44° − 58°',777,187,32)
    if t>=84.6:note(c,'∠A = 78°',777,247,37,PINK)
    if t>=87.8:note(c,'180° − 58°',777,331,33)
    if t>=94.6:note(c,'∠ACD = 122°',777,395,38,PINK)
    if t>=98:note(c,'Check  78° + 44° = 122°',758,496,28,GOLD)
def hard(c,beta=58,draw=1,show='?',a_label=None,small=True):
    B,C=(210,511),(495,511);alpha=46;A,I=triangle(B,C,beta,180-alpha-beta);P=extend(B,A,65)
    c.poly([A,B,C],FILL,EDGE,4)
    if draw>0:
        if draw>=.99 and small:c.poly([B,I,C],INNER,None)
        trace(c,B,I,draw,CYAN,3.7);trace(c,C,I,draw,GOLD,3.7)
        if draw>=.99:
            for o,first,second,col in [(B,C,A,CYAN),(C,A,B,GOLD)]:
                sector(c,o,first,I,42,col)
                sector(c,o,I,second,42,col)
                for lo,hi in ((first,I),(I,second)):
                    midpoint=direction(o,lo)+delta(o,lo,hi)/2
                    for angle_offset in ((0,) if o==B else (-2.5,2.5)):
                        c.line([radial(o,midpoint+angle_offset,38),radial(o,midpoint+angle_offset,46)],col,2)
            if show is not None:sector(c,I,B,C,32,PINK,description=show)
            point(c,I,'I',0,-22)
    trace(c,A,P,1,SUB,3)
    sector(c,A,C,P,33,GOLD)
    if a_label:sector(c,A,B,C,41,CYAN,description=a_label)
    for pt,k,dx,dy in [(B,'B',-16,22),(C,'C',11,25),(A,'A',-23,0),(P,'P',13,-10)]:point(c,pt,k,dx,dy)
    return A,B,C,I,P
def challenge(c,t):
    head(c,'Two bisectors meet at I. What is ∠BIC?')
    hard(c,58,cue(t,111.3,2.0),'?' if t>=115.5 else None)
    note(c,'BA continues to P.',706,193,34)
    if t>=106.3:note(c,'∠CAP = 134°',706,267,41,GOLD)
    if t>=111.3:note(c,'BI and CI bisect ∠B and ∠C.',706,368,31)
    if t>=116:note(c,'Find the angle at I.',706,458,34,PINK)
def bisectors(c,t):
    head(c,'Use the two half-angles as a pair')
    hard(c,58,1,'113°' if t>=145.4 else '?','46°' if t>=128.7 else None)
    note(c,'∠A = 180° − 134°',688,168,34)
    if t>=128.7:note(c,'= 46°',688,218,33,CYAN)
    if t>=130.6:note(c,'∠B + ∠C = 134°',688,296,31)
    if t>=139.9:note(c,'½∠B + ½∠C = 67°',688,372,34,GOLD)
    if t>=145.4:note(c,'∠BIC = 180° − 67° = 113°',688,468,35,PINK)
def invariant(c,t):
    head(c,'Change the triangle while keeping ∠A fixed')
    beta=57+21*cue(t,150.2,5.5)-12*cue(t,157.5,5.5)
    hard(c,beta,1,'113°','46°')
    note(c,'∠A stays 46°',686,170,35,CYAN)
    shown=round(beta/2,1)
    note(c,f'½∠B ≈ {shown:.1f}°',686,247,30,CYAN)
    note(c,f'½∠C ≈ {67-shown:.1f}°',686,305,30,GOLD)
    if t>=156.4:note(c,'Their sum stays 67°.',686,389,32)
    if t>=162.6:note(c,'∠BIC = 90° + ½∠A',686,487,38,PINK)
def pitfalls(c,t):
    head(c,'The middle letter names the vertex')
    B,C=(154,474),(587,474);A,I=triangle(B,C,44,58)
    c.poly([A,B,C],FILL,EDGE,4)
    for P,k,dx,dy in [(A,'A',0,-22),(B,'B',-12,27),(C,'C',0,27)]:point(c,P,k,dx,dy)
    sector(c,B,C,A,57,CYAN,description='44°')
    if t>=175.7:
        D=(729,474);trace(c,C,D,cue(t,175.7,1.0));sector(c,C,D,A,56,GOLD,cue(t,176.8,1.1))
    note(c,'∠ABC is at B.',782,233,38,CYAN)
    if t>=176:note(c,'An exterior angle lies outside.',765,355,26,GOLD)
    if t>=181:note(c,'Use its straight-line partner.',765,446,28)
def recap(c,t):
    head(c,'Follow the rays to the requested angle')
    hard(c,65,1,'113°','46°')
    note(c,'Mark the known total.',686,215,34)
    if t>=188.2:note(c,'Name the vertex.',686,292,34,CYAN)
    if t>=191.4:note(c,'Keep the two halves together.',686,374,29,GOLD)
    if t>=196.5:note(c,'Read ∠BIC at I.',686,472,36,PINK)
SCENES=(intro,use,basic,basic_answer,medium,medium_answer,challenge,bisectors,invariant,pitfalls,recap)
def verify():
    B,C=(210,511),(495,511)
    for beta in range(52,86):
        A,I=triangle(B,C,beta,134-beta);P=extend(B,A,65)
        for got,want in [(angle(A,B,C),46),(angle(A,C,P),134),(angle(B,C,I),beta/2),(angle(C,B,I),(134-beta)/2),(angle(I,B,C),113)]:
            assert isclose(got,want,rel_tol=1e-9)
    A,I=triangle(B,C,44,58);D=(700,511)
    assert isclose(angle(A,B,C),78) and isclose(angle(C,A,D),122)
    O=(300,400);assert isclose(angle(O,radial(O,37,20),radial(O,180,30)),143)
