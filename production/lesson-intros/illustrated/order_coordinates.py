"""S050: a cafe tray, a stationery drawer and an order lattice give three elimination views."""
from captioned_film import cue,mix
ID='S050'
ORIGINAL='84e042cbba10d6bc6bc11d75693874d12afe6c8283afc3c3bee16dfab35a9ddb'
START=(0,16.44,38.19,51.93,63.45,78.62,94.78,113.63,135.54,150.42,163.06)
POSTER=128.5
PAPER='#f5efe1';INK='#2e3544';LIGHT='#fffaf0';GRID='#d8ccba';BLUE='#256aa1';RED='#ad424d'
GREEN='#0a7765';CREAM='#ebca85';COPPER='#b96e43';GRAY='#556575'

def text(c,s,x,y,size=29,col=INK,anchor='mm'):c.text(s,x,y,size,col,anchor,True)
def head(c,s):text(c,s,58,57,40,INK,'lm')
def bun(c,x,y,k):
    c.dot(x,y,23*k,COPPER);c.rect(x-25*k,y+2*k,50*k,25*k,LIGHT)
    c.line([(x-23*k,y+3*k),(x+23*k,y+3*k)],INK,2)
    for dx,dy in [(-9,-8),(0,-14),(10,-6)]:c.line([(x+dx*k,y+dy*k),(x+(dx+3)*k,y+(dy-2)*k)],CREAM,2)
def drink(c,x,y,k):
    c.poly([(x-14*k,y-20*k),(x+16*k,y-20*k),(x+11*k,y+16*k),(x-9*k,y+16*k)],'#9dd6cd',GREEN,2)
    c.line([(x-18*k,y-21*k),(x+19*k,y-21*k)],GREEN,3)
    c.line([(x+4*k,y-22*k),(x+12*k,y-38*k),(x+19*k,y-38*k)],GREEN,3)
def pen(c,x,y,k,marker=False):
    col=RED if marker else BLUE;wid=8 if marker else 4
    c.poly([(x-23*k,y+13*k),(x+16*k,y-15*k),(x+(16+wid)*k,y+(-15+wid)*k),(x+(-23+wid)*k,y+(13+wid)*k)],col,INK,1.3)
    if marker:c.line([(x+5*k,y-6*k),(x+13*k,y+2*k)],CREAM,3)
    else:c.poly([(x-23*k,y+13*k),(x-20*k,y+17*k),(x-30*k,y+22*k)],CREAM,INK,1)
def dishes(c,t,solved=False):
    disappear=cue(t,52.15,2.65) if solved else 0
    for i,(n,cost) in enumerate(((1,21),(2,26))):
        if i and not solved and t<41.4:continue
        yy=235+i*157
        c.rect(123,yy-57,715,113,LIGHT,GRID,2)
        for j in range(3):
            if disappear<1:
                x=225+j*122;dy=(1 if not i else -1)*59*disappear
                if j<2:drink(c,x,yy+dy,1-disappear*.8)
                else:bun(c,x,yy+dy,1-disappear*.8)
        if n==2 and (solved or t>=40.7):bun(c,592,yy,1)
        if not i or solved or t>=41.4:text(c,'$'+str(cost),749,yy,34)
    if not solved and t>=44.6:text(c,'Price of one bun?',1039,284,28,RED)
    if solved and t>=56.6:text(c,'1 bun',1034,255,34,RED)
    if solved and t>=58.6:text(c,'$26 − $21 = $5',1026,349,26,GREEN)
def cancellation(c,t):
    head(c,'Find what changes when the other items match')
    for i in range(2):
        yy=229+i*151;c.rect(155,yy-46,679,93,LIGHT,GRID)
        shrink=cue(t,3.25,2.15)
        for j in range(2):
            if shrink<1:drink(c,238+j*108,yy+(1 if i==0 else -1)*44*shrink,1-.75*shrink)
        for j in range(1+i):bun(c,512+112*j,yy,1)
    if t>=6:text(c,'1 extra bun',1033,277,32,RED)
    if t>=9:text(c,'b = one bun’s price',994,377,26)
    if t>=12:text(c,'d = one drink’s price',994,437,25,GREEN)
def exams(c,t):
    head(c,'The objects left behind explain the price gap')
    for row,vals in enumerate(((1,1),(2,1))):
        yy=230+row*149;c.rect(138,yy-47,597,95,LIGHT,GRID)
        for j in range(vals[0]):pen(c,227+j*92,yy,1.1)
        pen(c,570,yy,1.1,True)
        text(c,'$'+str((9,13)[row]),666,yy,31)
    if t>=24.4:text(c,'Same marker in both.',978,218,27,RED)
    if t>=28.6:text(c,'1 extra pen = $4',972,340,30,BLUE)
    if t>=33.8:text(c,'$4 + $5 = $9',973,427,26);text(c,'2 × $4 + $5 = $13',974,492,25)
def cafe_q(c,t):head(c,'What changed between the café orders?');dishes(c,t)
def cafe_a(c,t):head(c,'Remove the matching purchases from both trays');dishes(c,t,True)
def drawers(c,t,solved):
    head(c,'Make the number of markers equal')
    copy=cue(t,78.7,2.8) if solved else 0
    cancel=cue(t,84,2.3) if solved else 0
    for row,y in enumerate((232,402)):
        if row and not solved and t<66.8:continue
        c.rect(134,y-63,770,125,LIGHT,GRID,3)
        pnum=3 if row==0 else 4;mnum=1 if row==0 else 2
        for j in range(pnum+(3 if not row and copy else 0)):
            if j>=3 and not row and not copy:continue
            x=202+j*72
            if not row and j>=3:x=mix(202+(j-3)*72,x,copy)
            k=1
            if j<4:k=1-cancel
            if k>0:pen(c,x,y+12*(1-k),k)
        for j in range(mnum+(1 if not row and copy else 0)):
            if cancel<1:pen(c,660+j*60*(copy if not row else 1),y,1-cancel,True)
        cost=36 if row else (46 if copy>.95 else 23);text(c,'$'+str(cost),844,y,30)
    if solved:
        if t>=85.8:text(c,'2 pens = $10',1082,228,26,BLUE)
        if t>=88.4:text(c,'1 pen = $5',1082,315,26,BLUE)
        if t>=90.4:text(c,'$23 − 3 × $5',1082,411,26)
        if t>=92:text(c,'marker = $8',1082,476,26,RED)
    elif t>=70.2:text(c,'Two prices?',1084,270,26,GRAY)
    if not solved and t>=72.4:text(c,'Match the markers first.',640,533,30,RED)
def pens_q(c,t):drawers(c,t,False)
def pens_a(c,t):drawers(c,t,True)
ORIGIN=(141,493);SX=44;SY=47
def point(x,y):return (ORIGIN[0]+SX*x,ORIGIN[1]-SY*y)
def grid(c):
    for x in range(15):
        px,py=point(x,0);c.line([(px,py),point(x,7)],GRID,1)
        if x%2==0:text(c,x,px,py+23,20,GRAY)
    for y in range(8):
        px,py=point(0,y);c.line([(px,py),point(14,y)],GRID,1);text(c,y,px-17,py,20,GRAY)
    c.line([point(0,7),ORIGIN,point(14,0)],INK,3)
    text(c,'X packs',460,556,25);text(c,'Y packs',126,128,25)
def marker(c,x,y,col,sz=8):
    px,py=point(x,y);c.dot(px,py,sz+2,LIGHT);c.dot(px,py,sz,col)
def walk(c,x,y,number,col):
    count=int(number);frac=number-count
    for i in range(count):c.line([point(i*x,i*y),point((i+1)*x,(i+1)*y)],col,3)
    if frac:c.line([point(count*x,count*y),point(number*x,number*y)],col,3)
    for i in range(1,count+1):marker(c,i*x,i*y,col)
    if frac:marker(c,number*x,number*y,col)
def packs(c,t,solution):
    head(c,'Match orders on the same horizontal grid line' if solution else 'Locate each order by its two pack counts')
    grid(c)
    if solution:
        a=1+2*cue(t,118.25,2.8);b=1+cue(t,121.0,1.6)
    else:a=cue(t,98.8,2.0);b=cue(t,103.1,2.2)
    walk(c,4,2,a,BLUE);walk(c,7,3,b,RED)
    if not solution:
        if t>=101.2:text(c,'(4, 2)   costs $36',1020,235,28,BLUE)
        if t>=106.2:text(c,'(7, 3)   costs $59',1020,330,28,RED)
        if t>=108.6:text(c,'Find both unit prices.',1020,450,26)
    else:
        if t>=116.4:
            c.line([point(0,6),point(14,6)],GREEN,2)
            text(c,'6 Y packs in both',1013,169,28,GREEN)
        if t>=118.2:text(c,'3 × $36 = $108',1013,235,27,BLUE)
        if t>=121:text(c,'2 × $59 = $118',1013,298,27,RED)
        if t>=124.6:
            a0=point(12,6);b0=point(14,6)
            c.line([a0,b0],INK,5);marker(c,12,6,BLUE);marker(c,14,6,RED)
            text(c,'2 more X for $10',1013,372,29,GREEN)
        if t>=129:text(c,'X costs $5',1013,451,31,BLUE)
        if t>=132.3:text(c,'Y costs $8',1013,519,31,RED)
def pack_q(c,t):packs(c,t,False)
def pack_a(c,t):packs(c,t,True)
def proof(c,t):
    head(c,'Rebuild both original prices')
    for i,(nx,ny,total) in enumerate(((4,2,36),(7,3,59))):
        yy=235+i*172
        for j in range(nx):
            x=153+j*66;c.rect(x,yy,46,48,'#d6e7f2',BLUE);text(c,'X',x+23,yy+23,26,BLUE)
        for j in range(ny):
            x=650+j*59;c.rect(x,yy,44,48,'#f3d7d1',RED);text(c,'Y',x+22,yy+23,26,RED)
        if t>=(137.6,139.4)[i]:text(c,f'{nx} × 5 + {ny} × 8 = {total}',1028,yy+25,25)
    if t>=142.2:text(c,'2X = 10 fixes X. Substitution then fixes Y.',640,545,28,GREEN)
def pitfalls(c,t):
    head(c,'A copied bundle includes its price')
    for i in range(3):
        if i and t<154+i*.8:continue
        y=170+93*i
        for j in range(4):
            xx=178+64*j;c.rect(xx,y,43,43,'#d6e7f2',BLUE);text(c,'X',xx+22,y+22,24,BLUE)
        for j in range(2):
            xx=485+j*62;c.rect(xx,y,43,43,'#f3d7d1',RED);text(c,'Y',xx+22,y+22,23,RED)
        text(c,'$36',710,y+22,29)
    if t>=157.2:text(c,'12 X and 6 Y',1000,244,29,GREEN)
    if t>=160:text(c,'3 × $36 = $108',1000,351,28,BLUE)
def finish(c,t):
    head(c,'Read the difference along the matched row')
    grid(c);walk(c,4,2,3,BLUE);walk(c,7,3,2,RED)
    if t>=165.6:c.line([point(12,6),point(14,6)],GREEN,5)
    text(c,'2 X packs  •  $10',1018,229,30,GREEN)
    if t>=167.6:text(c,'$5 per X pack',1018,311,29,BLUE)
    if t>=170.2:text(c,'4 × $5 + 2 × $8',1018,409,27);text(c,'= $36',1018,473,31,RED)
SCENES=(cancellation,exams,cafe_q,cafe_a,pens_q,pens_a,pack_q,pack_a,proof,pitfalls,finish)
def verify():
    assert 26-21==5 and 3*5+8==23 and 4*5+2*8==36
    assert [(x,y) for x in range(60) for y in range(60) if 4*x+2*y==36 and 7*x+3*y==59]==[(5,8)]
    assert (3*4,3*2,3*36)==(12,6,108) and (2*7,2*3,2*59)==(14,6,118)
    assert point(12,6)[1]==point(14,6)[1] and point(14,6)[0]-point(12,6)[0]==2*SX
