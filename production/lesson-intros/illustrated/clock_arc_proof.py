"""T12.2. Trace twelve exact clock gaps, move the observer and build the two-triangle proof."""
from math import acos, atan2, cos, degrees, hypot, pi, radians, sin
from captioned_film import cue, mix

ID='T12.2'
ORIGINAL='705a213376bf556e664ab405ceda90b52960bd3a1d4df851055ba9764b0f0890'
START=(0.,17.23,29.39,41.36,54.48,70.95,98.61,116.84)
POSTER=95.4
PAPER='#f3efe1'
INK,SOFT,GRID='#213d42','#527075','#c6cbbb'
BLUE, TEAL, CORAL, GOLD='#286c87','#137762','#ab5338','#aa7835'
SKY,MINT,PEACH,CREAM='#b9dce1','#c1dfc9','#f1c9af','#fbf8e9'
O=(395,330);R=201
def label(c,s,x,y,z=30,col=INK,anchor='lm'):c.text(s,x,y,z,col,anchor,True)
def title(c,s):label(c,s,60,53,40)
def at(o,r,h):
    th=h*pi/6
    return (o[0]+r*sin(th),o[1]-r*cos(th))
def segment(c,a,b,f,col,w=4):
    if f>0:c.line([a,(mix(a[0],b[0],f),mix(a[1],b[1],f))],col,w)
def rim(c,o,r,h1,h2,ink,w=4):
    n=max(2,round(abs(h2-h1)*8))
    c.line([at(o,r,mix(h1,h2,i/n)) for i in range(n+1)],ink,w)
def sector(c,o,r,h1,h2,fill):
    if abs(h2-h1)<.001:return
    n=max(2,round(abs(h2-h1)*12))
    c.poly([o]+[at(o,r,mix(h1,h2,i/n)) for i in range(n+1)],fill,None)
def clock(c,o=O,r=R,points=12,numbers=(12,4,8),ticks=True):
    rim(c,o,r,0,12,SOFT,3)
    if ticks:
        for h in range(60):
            u=h/5
            c.line([at(o,r-(10 if h%5==0 else 4),u),at(o,r,u)],GRID,2)
    for j in range(points):
        h=(j+1)%12;c.dot(*at(o,r,h),5,INK)
    for h in numbers:
        c.text(at_label(h),*at(o,r+26,h),22,INK,'mm',True)
    c.dot(*o,5,INK)
def at_label(h):return str(int(h) or 12)
def short(c,vertex,p,q,rad,fill,edge):
    a=atan2(p[1]-vertex[1],p[0]-vertex[0]);b=atan2(q[1]-vertex[1],q[0]-vertex[0])
    diff=(b-a+pi)%(2*pi)-pi
    arc=[(vertex[0]+rad*cos(a+diff*i/30),vertex[1]+rad*sin(a+diff*i/30)) for i in range(31)]
    c.poly([vertex,*arc],fill,None);c.line(arc,edge,3)
def centre(c,p=1):
    sector(c,O,64,0,4*p,PEACH);rim(c,O,64,0,4*p,CORAL,3)
    for h in (0,4):segment(c,O,at(O,R,h),1,CORAL)
def intercept(c,o=O,r=R,progress=1):
    rim(c,o,r,0,4*progress,TEAL,8)
    for h in (0,4):c.dot(*at(o,r,h),6,TEAL)
def triangle(c,h,rays=1):
    x=at(O,R,h);a=at(O,R,0);b=at(O,R,4)
    for p in (a,b):segment(c,x,p,rays,BLUE,4)
    c.dot(*x,7,BLUE)
    return x,a,b
def tick(c,p,q,col=TEAL):
    dx=q[0]-p[0];dy=q[1]-p[1];n=hypot(dx,dy)
    a=(p[0]+dx*.53,p[1]+dy*.53);k=7
    c.line([(a[0]-k*dy/n,a[1]+k*dx/n),(a[0]+k*dy/n,a[1]-k*dx/n)],col,3)
def gaps(c,t):
    title(c,'What does one gap measure?')
    clock(c,points=0,numbers=())
    for h in range(12):
        f=cue(t,.65+h*.23,.24)
        if f:c.dot(*at(O,R,h),6*f,INK)
        if t>=4:c.text(at_label(h),*at(O,R+26,h),20,SOFT,'mm',True)
    turn=cue(t,5.8,2)
    if turn:rim(c,O,R-17,0,12*turn,TEAL,4)
    for h in range(12):
        f=cue(t,7.7+h*.22,.33);segment(c,O,at(O,R,h),f,SOFT,2)
    if t>=7.6:label(c,'One full turn',740,219,34)
    if t>=8.8:label(c,'360° ÷ 12 gaps',740,300,40,BLUE)
    if t>=11:
        sector(c,O,110,0,cue(t,11,.65),PEACH);rim(c,O,110,0,cue(t,11,.65),CORAL,4)
        label(c,'30° per gap',740,389,43,CORAL)
    if t>=13:rim(c,O,R,0,cue(t,13,.55),CORAL,8)
def applications(c,t):
    title(c,'Choose where the angle is measured')
    # Three physical clock relationships drawn to their own scale.
    for j,hname in enumerate(('Clock hands','Wheel spokes','Regular hexagon')):
        o=(235+405*j,311);r=113
        clock(c,o,r,0,(),False)
        if j==0:
            segment(c,o,at(o,r*.76,0),1,INK,5)
            segment(c,o,at(o,r*.85,1+2*cue(t,17.5,1.3)),1,CORAL,5)
        elif j==1:
            for k in range(12):segment(c,o,at(o,r,k+.55*cue(t,18.1,1.6)),cue(t,17.8+.055*k,.3),SOFT,3)
        else:
            for k in range(6):segment(c,at(o,r,k*2),at(o,r,2*k+2),cue(t,18.6+.17*k,.35),TEAL,4)
        c.text(hname,o[0],483,26,INK,'mm',True)
    if t>=21.8:
        o=(1045,311);v=at(o,113,8)
        for k in (0,4):segment(c,v,at(o,113,k),cue(t,21.8,.85),BLUE,4)
        if t>=24.6:short(c,v,at(o,113,0),at(o,113,4),26,SKY,BLUE);c.dot(*v,6,BLUE)
def question(c,t):
    title(c,'From twelve to four · how large is the turn?')
    clock(c,numbers=range(1,13))
    segment(c,O,at(O,R,0),cue(t,30,1),CORAL)
    segment(c,O,at(O,R,4),cue(t,32,.9),CORAL)
    if t>=34.4:
        sector(c,O,62,0,4*cue(t,34.4,.8),PEACH)
        label(c,'Measure at the centre.',716,255,34)
    if t>=36.6:label(c,'How many gaps?',716,374,42,TEAL)
def four_gaps(c,t):
    title(c,'Four gaps join five clock points')
    clock(c,numbers=(12,1,2,3,4))
    for k in range(4):
        f=cue(t,41.4+.42*k,.49)
        if f:
            sector(c,O,R-7,k,k+f,(CREAM,MINT)[k%2]);rim(c,O,R,k,k+f,TEAL,7)
            segment(c,O,at(O,R,k),1,GRID,2)
    for h in (0,4):segment(c,O,at(O,R,h),1,CORAL,4)
    if t>=44.2:label(c,'4 × 30° = 120°',720,235,44,CORAL)
    if t>=47.2:label(c,'Count the spaces between.',710,317,29)
    if t>=49.6:
        for j in range(5):
            x=747+j*86
            if j<4:c.line([(x,436),(x+86,436)],TEAL,5)
            c.dot(x,436,8,INK)
            c.text(at_label(j),x,402,22,INK,'mm',True)
        if t>=52.2:
            for j in range(4):c.text(str(j+1),790+j*86,477,23,TEAL,'mm',True)
def edge(c,t):
    title(c,'Two viewpoints share the same arc')
    clock(c);centre(c)
    h=8+.95*sin(pi*cue(t,65.6,4))
    v,a,b=triangle(c,h,cue(t,55.3,1.1));intercept(c,progress=cue(t,57.4,1.3))
    if t>=60.8:
        short(c,v,a,b,55,SKY,BLUE);label(c,'At the centre',733,208,28,CORAL)
        label(c,'120°',733,265,47,CORAL)
    if t>=63.4:label(c,'At the rim',733,361,28,BLUE);label(c,'60°',733,420,48,BLUE)
    if t>=65.6:label(c,'Both see the green arc.',733,518,29,TEAL)
def proof(c,t):
    title(c,'Why is the angle at the rim half as large?')
    a=at(O,R,0);v=at(O,R,8);b=at(O,R,4)
    if t>=78.6:
        c.poly([O,v,a],SKY,None);c.poly([O,v,b],MINT,None)
    clock(c);intercept(c)
    for point in (a,b):segment(c,O,point,1,CORAL);segment(c,v,point,1,INK)
    segment(c,v,O,cue(t,72.6,.85),BLUE,4)
    if t>=74.2:
        short(c,v,a,O,50,SKY,BLUE);short(c,v,O,b,64,MINT,TEAL)
        label(c,'a',v[0]+44,v[1]-51,23,BLUE)
        label(c,'b',v[0]+78,v[1]-19,23,TEAL)
        label(c,'Angle at 8 = a + b',720,176,33)
    if t>=78.6:
        for p in (a,v,b):tick(c,O,p)
        short(c,a,v,O,43,SKY,BLUE);short(c,b,O,v,43,MINT,TEAL)
        label(c,'a',a[0]-25,a[1]+66,24,BLUE)
        label(c,'b',b[0]-72,b[1]-18,24,TEAL)
    if t>=83.6:label(c,'Left angle = 180° − 2a',720,258,30,BLUE)
    if t>=87.1:label(c,'Lower angle = 180° − 2b',720,316,30,TEAL)
    if t>=90:label(c,'A full turn leaves',720,396,30)
    if t>=92.4:
        sector(c,O,56,0,4,PEACH);rim(c,O,56,0,4,CORAL,4)
        label(c,'2a + 2b = 2(a + b)',720,465,39,CORAL)
def diameter(c,t):
    title(c,'A diameter always gives a right angle at the rim')
    clock(c,numbers=(12,3,6))
    a,b=at(O,R,0),at(O,R,6)
    segment(c,a,b,cue(t,99.2,1),CORAL)
    f=cue(t,101.2,1.8)
    if f:rim(c,O,R,6,6+6*f,TEAL,7)
    h=3+1.15*sin(pi*2*cue(t,109.2,6.25));v=at(O,R,h)
    for p in (a,b):segment(c,v,p,cue(t,103.3,1),BLUE,4)
    if t>=104.4:label(c,'Diameter spans 180°',717,221,35,CORAL)
    if t>=107.4:
        def unit(p):
            d=hypot(p[0]-v[0],p[1]-v[1]);return ((p[0]-v[0])/d,(p[1]-v[1])/d)
        av,bv=unit(a),unit(b);s=23
        points=[(v[0]+s*(i*av[0]+j*bv[0]),v[1]+s*(i*av[1]+j*bv[1])) for i,j in ((1,0),(1,1),(0,1))]
        c.line(points,BLUE,4)
        label(c,'½ × 180° = 90°',717,325,42,BLUE)
    if t>=109.2:label(c,'Move the third corner.',717,450,28,TEAL)
def challenge(c,t):
    if t<125.4:
        title(c,'Trace the arc before choosing the angle')
        clock(c);centre(c);v,a,b=triangle(c,8);intercept(c)
        if t>=119.8:label(c,'4 equal gaps',735,218,35,TEAL)
        if t>=121.8:short(c,v,a,b,50,SKY,BLUE);label(c,'120° at the centre',735,311,35,CORAL)
        if t>=123:label(c,'60° at the rim',735,395,35,BLUE)
        return
    title(c,'Your turn · the smaller angle from two to seven')
    clock(c,numbers=range(1,13))
    for h in (2,7):segment(c,O,at(O,R,h),cue(t,126.8+(h==7)*1.5,.9),CORAL)
    if t>=129.6:label(c,'Count the shorter arc.',724,246,35)
    if t>=132.3:
        f=cue(t,132.3,1.7);rim(c,O,R,2,2+5*f,TEAL,8)
        if t>=134:label(c,'5 × 30° = 150°',724,367,40,TEAL)
SCENES=(gaps,applications,question,four_gaps,edge,proof,diameter,challenge)
def verify():
    def angle(v,p,q):
        a=(p[0]-v[0],p[1]-v[1]);b=(q[0]-v[0],q[1]-v[1])
        return degrees(acos(max(-1,min(1,sum(i*j for i,j in zip(a,b))/(hypot(*a)*hypot(*b))))))
    a,b,d=at(O,R,0),at(O,R,4),at(O,R,6)
    assert abs(angle(O,a,b)-120)<1e-8 and abs(angle(O,at(O,R,2),at(O,R,7))-150)<1e-8
    for h in (4.1,5,7.6,8,8.9,10,11.8):assert abs(angle(at(O,R,h),a,b)-60)<1e-8
    for h in (1,1.85,3,4.15,5.8):assert abs(angle(at(O,R,h),a,d)-90)<1e-8
    v=at(O,R,8)
    assert abs(angle(v,a,O)-angle(a,v,O))<1e-8 and abs(angle(v,b,O)-angle(b,v,O))<1e-8
