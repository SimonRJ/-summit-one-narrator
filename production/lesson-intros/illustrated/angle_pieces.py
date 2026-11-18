"""S131. Cut out angle pieces, recombine their turns, and follow the moving incenter on its locus."""
from math import atan2,cos,sin,radians,degrees,tan,dist,acos
from captioned_film import cue,mix,font
ID='S131';ORIGINAL='bdcb0d4811eb39d5784ce239b923702e5459898e54a404bbe000942fde4f9ef4';START=(0,15.16,32.44,49.05,64.25,80.54,104.05,126.25,151.52,169.12,185.92);POSTER=157.7
PAPER='#e9edf3';INK='#28374a';SOFT='#55677e';GRID='#bdc8d3';MILK='#f6f8f9';VIOLET='#694e94';ORANGE='#b05635';TEAL='#157267';LILAC='#d6cde5';PEACH='#eed0b8';MINT='#b9dcd1';BLUE='#3c7194'

def title(c,s):
    size=42
    while font(round(size*c.scale),True).getlength(s)>1150*c.scale:size-=1
    c.text(s,62,61,size,INK,'lm',True)
def text(c,s,x,y,sz=32,col=INK):c.text(s,x,y,sz,col,'lm',True)
def ray(p,d,r):a=radians(d);return (p[0]+r*cos(a),p[1]+r*sin(a))
def interp(a,b,p):return (mix(a[0],b[0],p),mix(a[1],b[1],p))
def line(c,a,b,p,col,w=3):c.line([a,interp(a,b,p)],col,w)
def pts(c,p,s,dx,dy):c.dot(*p,5,INK);c.text(s,p[0]+dx,p[1]+dy,24,INK,bold=True)
def angle(c,p,a,b,r,pen,paper,label='',out=18):
    n=max(2,int(abs(b-a)/2));arc=[ray(p,mix(a,b,j/n),r) for j in range(n+1)];c.poly([p,*arc],paper,None);c.line(arc,pen,3)
    if label:c.text(label,*ray(p,(a+b)/2,r+out),min(28,max(20,r//3)),pen,bold=True)
def axes(c,p,L,R):c.line([(L,p[1]),(R,p[1])],INK,3);pts(c,(L,p[1]),'L',0,25);pts(c,p,'O',0,25);pts(c,(R,p[1]),'R',0,25)
def fold(c,t,turn=44,large=True,small=True):
    O=(420,431);axes(c,O,132,706);X=ray(O,-turn,245);c.line([O,X],INK,4);pts(c,X,'X',11,-22)
    if large:angle(c,O,-180,-turn,112,VIOLET,LILAC,'136°' if abs(turn-44)<.01 else '')
    if small:angle(c,O,-turn,0,85,ORANGE,PEACH,'44°' if abs(turn-44)<.01 else '')

def intro(c,t):
    title(c,'An angle measures a turn around its vertex');O=(377,427);a=70*cue(t,.6,2.5);axes(c,O,147,675);X=ray(O,-a,228);c.line([O,X],INK,3);angle(c,O,-a,0,89,ORANGE,PEACH)
    if t>=3.4:angle(c,O,-180,-a,108,VIOLET,LILAC)
    if t>=6:text(c,'Two parts make 180°.',729,273,32)
    if t>=9.4:text(c,'Vertex O',729,351,35,ORANGE)
    if t>=11.2:text(c,'Follow the angle to its next triangle.',730,475,24,TEAL)

def triangle(b,c,B,C):
    L=C[0]-B[0];tb,tc=tan(radians(b)),tan(radians(c));x=L*tc/(tb+tc);A=B[0]+x,B[1]-x*tb
    tb,tc=tan(radians(b/2)),tan(radians(c/2));x=L*tc/(tb+tc);I=B[0]+x,B[1]-x*tb
    return A,I
B,C=(204,486),(531,486)
def construction(c,b,halves=True,ext=True,shade=False,unknown=False):
    g=128-b;A,I=triangle(b,g,B,C);P=ray(A,-b,53)
    c.poly([B,C,A],MILK,INK,3)
    if shade:c.poly([B,C,I],MINT,TEAL,2)
    if ext:c.line([B,P],INK,3);pts(c,P,'P',10,-14);angle(c,A,-b,g,43,ORANGE,PEACH)
    if halves:c.line([B,I,C],TEAL,3);angle(c,B,-b/2,0,60,VIOLET,LILAC);angle(c,C,180,180+g/2,60,ORANGE,PEACH);pts(c,I,'I',0,-21)
    for p,s,dx,dy in [(A,'A',-23,2),(B,'B',-21,16),(C,'C',22,16)]:pts(c,p,s,dx,dy)
    if unknown:angle(c,I,g/2,180-b/2,43,TEAL,MINT,'?')
    return A,I

def uses(c,t):
    title(c,'Extend a side, then look for a known angle total');b=55
    construction(c,b,halves=t>=24.4,ext=t>=19.2,shade=t>=28.6)
    text(c,'Extend BA through A.',695,228,32)
    if t>=24.4:text(c,'Bisect the base angles.',695,332,30,TEAL)
    if t>=28.6:text(c,'The two halves belong to BIC.',677,436,27,VIOLET)

def basic(c,t):
    title(c,'Angles LOX and XOR meet at O');O=(420,431);axes(c,O,132,706)
    turn=44*cue(t,36.8,1.1);X=ray(O,-turn,245)
    if t>=36.8:c.line([O,X],INK,4);pts(c,X,'X',13,-16);angle(c,O,-turn,0,84,ORANGE,PEACH,'44°' if turn==44 else '')
    if t>=39.8:angle(c,O,-180,-turn,112,VIOLET,LILAC,'?');text(c,'Find ∠LOX.',771,326,40,VIOLET)

def pieces(c,t):
    title(c,'A 44° piece and its neighbour fill a half-turn');fold(c,t,large=False)
    O=(420,431);p=cue(t,50,2.3);angle(c,O,-180,-180+136*p,112,VIOLET,LILAC,'136°' if t>=60.4 else '')
    if t>=55.6:text(c,'Whole turn here  180°',737,240,30)
    if t>=58.2:text(c,'180° − 44°',737,330,39,ORANGE)
    if t>=60.4:text(c,'= 136°',737,415,42,VIOLET)

def maintri(c,t,answers=False):
    BB,CC=(159,460),(647,460);A,_=triangle(45,60,BB,CC);D=(796,460);c.poly([BB,CC,A],MILK,INK,3)
    if answers or t>=70.8:c.line([CC,D],INK,3);pts(c,D,'D',0,26)
    for p,s,dx,dy in [(A,'A',0,-23),(BB,'B',-10,25),(CC,'C',2,25)]:pts(c,p,s,dx,dy)
    angle(c,BB,-45,0,60,VIOLET,LILAC,'45°')
    if answers or t>=68.4:angle(c,CC,180,240,62,ORANGE,PEACH,'60°')
    if answers or t>=73.6:angle(c,A,60,135,48,TEAL,MINT,'75°' if answers and t>=84.8 else '?')
    if answers or t>=75.8:angle(c,CC,-120,0,78,BLUE,'#c9dde9','120°' if answers and t>=93.8 else '?')

def medium(c,t):
    title(c,'The exterior angle is at C');maintri(c,t)
    if t>=73.6:text(c,'Find ∠BAC',868,258,31,TEAL)
    if t>=75.8:text(c,'and ∠ACD.',868,347,31,BLUE)

def medium_result(c,t):
    title(c,'Inside the triangle, then outside at C');maintri(c,t,True)
    if t>=84.8:text(c,'180 − 45 − 60 = 75°',808,220,28,TEAL)
    if t>=88.2:text(c,'180 − 60 = 120°',808,336,29,BLUE)
    if t>=97.2:text(c,'75 + 45 = 120°',808,443,29,VIOLET)

def challenge(c,t):
    title(c,'Where do the two angle bisectors meet?')
    construction(c,55,halves=t>=112.2,ext=t>=104.2,shade=t>=116.4,unknown=t>=116.4)
    if t>=107:text(c,'Given ∠CAP = 128°',701,205,34,ORANGE)
    if t>=112.2:text(c,'BI and CI bisect the base angles.',671,309,26,TEAL)
    if t>=116.4:text(c,'Find ∠BIC.',701,425,39,VIOLET)

def angular_sum(c,b,phase,answer=False):
    g=128-b;O=(912,382);r=100
    c.line([ray(O,-180,147),ray(O,0,147)],GRID,2)
    angle(c,O,-180,-180+b/2*phase,r,VIOLET,LILAC)
    if phase>0:angle(c,O,-180+b/2*phase,-180+(b+g)/2*phase,r,ORANGE,PEACH)
    if answer:angle(c,O,-116,0,r,TEAL,MINT,'116°',23)
    if phase>=.99:c.text('64°',O[0]-99,O[1]+35,26,VIOLET,bold=True)

def deduct(c,t):
    title(c,'The two half-angles add to half of 128°');A,I=construction(c,55,True,True,t>=136.2)
    if t>=130.2:angle(c,A,73,125,39,TEAL,MINT,'52°',20)
    if t>=132.2:text(c,'B + C = 128°',760,158,32,ORANGE)
    if t>=136.2:angular_sum(c,55,cue(t,136.2,5.7),t>=148)
    if t>=142:text(c,'B/2 + C/2 = 64°',719,484,32,VIOLET)
    if t>=148:text(c,'∠BIC = 180° − 64° = 116°',651,552,32,TEAL);angle(c,I,73/2,180-55/2,41,TEAL,MINT)

def invariant(c,t):
    title(c,'Watch the two half-angles trade degrees');motion=cue(t,151.65,3.65)-cue(t,156.6,3.65)
    b=46+28*motion;g=128-b
    # The faint dotted paths show computed earlier apex and incenter positions under this constraint.
    for k in range(46,75,2):
        A,I=triangle(k,128-k,B,C);c.dot(*A,2,GRID);c.dot(*I,2,GRID)
    A,I=construction(c,b,True,False,True);angle(c,I,g/2,180-b/2,43,TEAL,MINT)
    text(c,'∠A stays 52°',722,160,31,TEAL);angular_sum(c,b,1,True)
    if t<164.2:
        text(c,f'{b/2:.1f}° + {g/2:.1f}° = 64°',702,483,31,VIOLET)
        text(c,'This is one possible triangle.',707,540,23,SOFT)
    else:text(c,'90° + ½ × 52° = 116°',672,511,35,TEAL)

def mistakes(c,t):
    title(c,'The middle letter names the vertex');maintri(c,100,True)
    text(c,'∠ABC',851,213,46,VIOLET)
    if t>=172.8:text(c,'Vertex B',849,295,34,VIOLET)
    if t>=177.4:text(c,'∠ACD lies outside.',829,401,29,BLUE)
    if t>=182.6:text(c,'120° + 60° = 180°',850,522,28)

def finish(c,t):
    title(c,'Mark the angle the question asks for');A,I=construction(c,60,True,True,True)
    angle(c,I,34,150,44,TEAL,MINT,'?' if t<198.2 else '116°')
    text(c,'∠CAP = 128°',719,180,32,ORANGE)
    if t>=189.8:text(c,'∠BAC = 52°',719,262,32,TEAL)
    if t>=192.8:text(c,'Half of B + half of C = 64°',696,353,27,VIOLET)
    if t>=198.2:text(c,'∠BIC = 116°',710,472,40,TEAL)
SCENES=(intro,uses,basic,pieces,medium,medium_result,challenge,deduct,invariant,mistakes,finish)
def measure(a,o,c):
    u=(a[0]-o[0],a[1]-o[1]);v=(c[0]-o[0],c[1]-o[1]);dot=u[0]*v[0]+u[1]*v[1];return degrees(acos(max(-1,min(1,dot/dist(a,o)/dist(c,o)))))
def verify():
    assert 180-44==136
    A,_=triangle(45,60,B,C);assert abs(measure(B,A,C)-75)<1e-8 and abs(measure(A,C,(C[0]+1,C[1]))-120)<1e-8
    for k in range(87,161):
        b=k/2;g=128-b;A,I=triangle(b,g,B,C);P=ray(A,-b,53)
        assert abs(measure(C,A,P)-128)<1e-8 and abs(measure(B,A,C)-52)<1e-8 and abs(measure(B,I,C)-116)<1e-8
        assert abs(measure(C,B,I)-b/2)<1e-8 and abs(measure(B,C,I)-g/2)<1e-8
