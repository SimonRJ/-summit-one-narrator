"""S074. Bound the search on a number line, pair two lengths and grow exact rectangles."""
from itertools import combinations_with_replacement
from captioned_film import cue,mix

ID='S074'
ORIGINAL='f3b1f1067928303c06af68f231cc4a0668af9d96837c3a6c4a8955590d66b8cc'
START=(0,14.36,32.6,48.25,62.65,78.78,93.02,110.75,128.51,147.39,164.99)
POSTER=138.2
PAPER='#fff6df'
INK,QUIET,TEAL,ORANGE,RED,LINE='#20384a','#516677','#126f72','#c88532','#a0454a','#abaf9f'
SEA,SAND,PINK,SKY='#9bd7c9','#f6cd83','#f1aba3','#afcee0'
def text(c,s,x,y,z=30,col=INK,anchor='mm'):
    c.text(s,x,y,z,col,anchor,True)
def title(c,s):
    text(c,s,55,55,42,INK,'lm');c.line([(55,99),(1225,99)],LINE,2)
def tag(c,x,y,s,col=TEAL,w=205):
    c.rect(x-w/2,y-29,w,58,PAPER,col,2);text(c,s,x,y,26,col)
def axis(c,low,high,y,*,x1=100,x2=1180):
    def xpos(n):return mix(x1,x2,(n-low)/(high-low))
    c.line([(x1,y),(x2,y)],INK,4)
    for k in range(low,high+1):
        xx=xpos(k);c.line([(xx,y-6),(xx,y+8)],INK,2)
    return xpos
def marker(c,x,y,col,inside=True,r=12):
    c.dot(x,y,r,col)
    if not inside:c.dot(x,y,r-4,PAPER)
def arrow(c,x1,x2,y,col,p=1):
    if p<=0:return
    x=mix(x1,x2,p);d=1 if x2>x1 else -1
    c.line([(x1,y),(x,y)],col,4);c.poly([(x,y),(x-12*d,y-7),(x-12*d,y+7)],col,None)
def pairstrip(c,x,y,n,unit=29):
    for i in range(17):
        pos=x+i*unit
        c.rect(pos,y,unit-2,37,SEA if i<n else SAND,INK,1)
    text(c,str(n),x+n*unit/2,y+63,26,TEAL)
    text(c,str(17-n),x+(n+(17-n)/2)*unit,y+63,26,ORANGE)
def intro(c,t):
    title(c,'What would make an answer unique?')
    text(c,'Which positive integer doubles to 10?',640,143,29)
    xs=axis(c,1,8,304,x1=211,x2=1069)
    for k in range(1,9):text(c,k,xs(k),351,28)
    if t>1:marker(c,xs(5),304,TEAL)
    if t>3:tag(c,xs(5),206,'Works',TEAL,150)
    if t>6:
        for k in (1,2,3,4,6,7,8):
            if t>6+.4*k:text(c,'×',xs(k),258,35,RED)
        text(c,'Show why every alternative fails.',640,474,37,TEAL)
    if t>10:text(c,'Below 5 the double is too small. Above 5 it is too large.',640,558,27,QUIET)
def context(c,t):
    title(c,'A short search still needs a reason')
    xs=axis(c,1,12,316)
    for k in range(1,13):text(c,k,xs(k),364,24)
    if t>17:
        c.line([(xs(4),291),(mix(xs(4),xs(7),cue(t,17,1.8)),291)],TEAL,8)
        text(c,'Suppose the clues force 4 ≤ x ≤ 7.',640,194,32)
    if t>20:
        for k in range(4,8):
            if cue(t,20+(k-4)*.5,.6)>.4:marker(c,xs(k),316,TEAL)
    if t>23:text(c,'Now there are four candidates to check.',640,465,31,TEAL)
    if t>27:text(c,'A bound, a complete list, or a rule that covers every candidate.',640,552,26)
def multiples(c,t):
    solved=t>=START[3]
    title(c,'Which multiples of 5 lie from 20 through 32?')
    xs=axis(c,14,36,345,x1=79,x2=1202)
    left=xs(20);right=xs(32)
    c.line([(left,313),(mix(left,right,cue(t,33.7,1.5)),313)],TEAL,7)
    for v in (20,32):
        marker(c,xs(v),313,TEAL);text(c,v,xs(v),252,25,TEAL)
    if not solved:
        for k in (15,20,25,30,35):
            if t>34+(k-15)*.15:text(c,k,xs(k),391,25,QUIET)
        if t>39:text(c,'Both ends are included. Step forward by five.',640,508,32)
    else:
        for k,at in ((20,48.3),(15,49.7),(25,52.3),(30,54),(35,57.4)):
            if t<at:continue
            col=TEAL if 20<=k<=32 else RED
            marker(c,xs(k),345,col)
            text(c,k,xs(k),399,30,col)
        if t>=51:
            for k,at in ((20,51.4),(25,53.2),(30,56.5)):
                arrow(c,xs(k)+15,xs(k+5)-15,450,TEAL if k<30 else RED,cue(t,at,.8))
        if t>58.8:text(c,'15 is too small. 35 is too large. None were skipped.',640,548,31)
def pair_question(c,t):
    title(c,'Two whole numbers add to 17')
    text(c,'Smaller number',347,218,30,TEAL)
    text(c,'Larger number',911,218,30,ORANGE)
    tag(c,347,322,'x',TEAL,224);tag(c,911,322,'17 − x',ORANGE,224)
    text(c,'+',632,322,50)
    if t>68:text(c,'Both numbers are positive. Each is at most 12.',640,449,32)
    if t>73:text(c,'Count a pair and its reverse only once.',640,541,29,TEAL)
def pair_solution(c,t):
    title(c,'Bound the smaller number from both sides')
    if t<85.8:
        n=4 if t<80.1 else 5 if t<82.7 else 8
        pairstrip(c,105,272,n,33)
        text(c,'17 − x ≤ 12',931,240,41)
        if n==4:text(c,'13 exceeds the cap.',931,335,28,RED)
        if t>80:text(c,'x ≥ 5',931,328,43,TEAL)
        if t>82.5:text(c,'x ≤ 17 − x  →  x ≤ 8',850,435,31)
        if t>82.5:text(c,'The smaller part cannot exceed half of 17.',635,548,27,QUIET)
    else:
        for j,n in enumerate(range(5,9)):
            if t<85.8+j*.65:continue
            y=151+j*98;pairstrip(c,185,y,n,27)
            text(c,f'({n}, {17-n})',874,y+23,34,TEAL)
        if t>89.5:text(c,'Every x from 5 through 8 has exactly one partner.',640,563,29)
def rect(c,n,ox,base,u,*,colour=SEA,grow=0,labels=True):
    # Keep the shorter side vertical and grow both dimensions by one unit.
    width,height=n+6,n
    x,y=ox,base-height*u
    c.rect(x,y,width*u,height*u,colour,INK,2)
    if grow:
        c.rect(x+width*u,y,grow*u,height*u,SAND,INK,1)
        c.rect(x,y-grow*u,(width+grow)*u,grow*u,SAND,INK,1)
    for k in range(1,width):c.line([(x+k*u,y-grow*u),(x+k*u,base)],QUIET,1)
    for k in range(1,height):c.line([(x,y+k*u),(x+(width+grow)*u,y+k*u)],QUIET,1)
    if labels:
        end=1 if grow>=.999 else 0
        text(c,width+end,ox+(width+grow)*u/2,base+35,27)
        text(c,n+end,ox-34,base-(n+grow)*u/2,28)
def rect_problem(c,t):
    title(c,'A rectangle with area 135 square units')
    x,y,w,h=168,206,420,252
    c.rect(x,y,w,h,SEA,INK,3)
    text(c,'135 square units',x+w/2,y+h/2,34)
    if t>95.5:
        text(c,'x',x-40,y+h/2,35,TEAL)
        text(c,'x + 6',x+w/2,y+h+42,33,TEAL)
    text(c,'Positive integer sides',939,244,31)
    if t>99:text(c,'Longer side = shorter side + 6',928,346,27)
    if t>104:text(c,'Could a second pair work?',925,456,30,TEAL)
def witness(c,t):
    title(c,'Try consecutive shorter sides')
    p=cue(t,119.5,2)
    rect(c,8,137,472,29,grow=p)
    text(c,'Area = x(x + 6)',932,211,39)
    if t>114:text(c,'8 × 14 = 112',932,312,38,QUIET)
    if t>120.3:text(c,'9 × 15 = 135',932,414,41,TEAL)
    if t>124:tag(c,932,520,'One pair works',TEAL,308)
def uniqueness(c,t):
    title(c,'Increasing both positive sides increases area')
    p=cue(t,129.8,2.6)-cue(t,140.8,1.8)
    rect(c,9,113,464,26,grow=p)
    if t<134:
        text(c,'9 × 15 = 135',958,241,38)
        if t>130:text(c,'10 × 16 = 160',958,350,38,TEAL)
        if t>131.8:text(c,'The extra strip has positive area.',958,464,26,QUIET)
    else:
        for i,(s,col) in enumerate((('x < 9     area < 135',QUIET),('x = 9     area = 135',TEAL),('x > 9     area > 135',QUIET))):
            if t>134+i*.95:text(c,s,942,215+i*83,32,col)
        if t>141:text(c,'15 − 9 = 6',932,496,35,TEAL)
    if t>143:text(c,'Exactly one rectangle: 9 by 15.',640,565,34)
def traps(c,t):
    title(c,'What did your calculation prove?')
    if t<154.7:
        rect(c,9,185,437,20)
        text(c,'9 × 15 = 135',934,238,35)
        text(c,'At least one solution',932,334,32,TEAL)
        if t>150.5:text(c,'Strict growth rules out every other length.',640,540,32)
    else:
        xs=axis(c,19,33,329)
        for k in (20,25,30,32):text(c,k,xs(k),381,28)
        closed=t<159.7
        c.line([(xs(20),305),(xs(32),305)],TEAL,5)
        marker(c,xs(20),305,TEAL,closed,13);marker(c,xs(32),305,TEAL,True,13)
        text(c,'20 ≤ x ≤ 32' if closed else '20 < x ≤ 32',640,206,41)
        text(c,'20 qualifies.' if closed else 'With a strict lower bound, 20 drops out.',640,500,32,TEAL)
def recap(c,t):
    title(c,'Choose the right kind of proof')
    for j,(at,s,sub) in enumerate(((165,'All answers','A list with no gaps.'),(167.7,'At least one','An example that works.'),(170.5,'Exactly one','A witness and a reason all others fail.'))):
        if t<at:continue
        x=230+j*406
        tag(c,x,214,s,TEAL,270)
        if j==2:
            text(c,'One example works.',x,305,24);text(c,'All others fail.',x,366,24)
        else:text(c,sub,x,305,24)
    if t>174.6:text(c,'State the legal range. Show why it covers every possibility.',640,469,30)
    if t>180:text(c,'Check the surviving values in the original clues.',640,553,31,TEAL)
SCENES=(intro,context,multiples,multiples,pair_question,pair_solution,rect_problem,witness,uniqueness,traps,recap)
def verify():
    assert [n for n in range(20,33) if n%5==0]==[20,25,30]
    assert [(a,b) for a,b in combinations_with_replacement(range(1,13),2) if a+b==17]==[(5,12),(6,11),(7,10),(8,9)]
    assert [(a,135//a) for a in range(1,136) if 135%a==0 and 135//a-a==6]==[(9,15)]
    assert 8*14==112 and 9*15==135 and 10*16==160
