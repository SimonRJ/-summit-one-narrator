"""S044: reverse a machine, return a missing pile, then sieve the output interval."""
from fractions import Fraction
from math import atan2, cos, sin, pi
from captioned_film import cue, mix

ID = 'S044'
ORIGINAL = '4f387b33f72f195c643e7c0dbb76de07982a7b9144102965069d09a2326cb523'
START = (0,14.52,31.8,45.53,60.09,75.9,93.5,111.71,135.54,153.14,169.78)
POSTER = 143.4
PAPER, INK, TEAL, GOLD, CORAL, QUIET, LINE, DEEP = (
    '#112c32','#f6f3dc','#72ddc7','#ffd17c','#ff9d83','#b6caca','#36565a','#1a383e')
OUTPUTS = tuple(range(23,33))
VALID = tuple(y for y in OUTPUTS if 2*(y+4)%3==0)

def words(c, value, x, y, size=30, col=INK, anchor='mm'):
    c.text(value,x,y,size,col,anchor,True)

def heading(c, value):
    words(c,value,65,61,40,INK,'lm')

def arrow(c, a, b, fraction, col, weight=4):
    if fraction<=0:return
    x,y=(mix(a[0],b[0],fraction),mix(a[1],b[1],fraction))
    c.line([a,(x,y)],col,weight)
    angle=atan2(b[1]-a[1],b[0]-a[0])
    c.poly([(x,y),(x-15*cos(angle-.44),y-15*sin(angle-.44)),
            (x-15*cos(angle+.44),y-15*sin(angle+.44))],col,None)

def machine(c, values, forward, back):
    xs=(211,641,1071); y=306
    for x,v,col in zip(xs,values,(TEAL,INK,GOLD)):
        c.dot(x,y,61,LINE);c.dot(x,y,57,DEEP);words(c,v,x,y,49,col)
    for i,(operation,undo) in enumerate((('+3','−3'),('×3','÷3'))):
        a,b=xs[i]+83,xs[i+1]-83; mid=(a+b)/2
        c.line([(a,y-37),(b,y-37)],LINE,2);c.line([(a,y+56),(b,y+56)],LINE,2)
        if forward[i]>0:
            words(c,operation,mid,y-79,34,GOLD);arrow(c,(a,y-37),(b,y-37),forward[i],GOLD)
        if back[i]>0:
            words(c,undo,mid,y+103,34,TEAL);arrow(c,(b,y+56),(a,y+56),back[i],TEAL)
    for x,label in zip(xs,('input','after adding','output')):
        words(c,label,x,190,24,QUIET)

def opening(c,t):
    heading(c,'Run the machine in either direction')
    reverse1=cue(t,5.8,1.6);reverse2=cue(t,9.3,1.5)
    f=(cue(t,12,.7),cue(t,12.9,.7))
    machine(c,('2' if reverse2>.73 else '?','5' if reverse1>.73 else '?','15'),f,(reverse2,reverse1))
    if t>=9.3:words(c,'Undo the last operation first.',639,520,33,TEAL)

def exams(c,t):
    heading(c,'A whole-number input narrows the search')
    f=cue(t,16.5,1.8);r=cue(t,23,2.3)
    for i,(y,result) in enumerate(((24,'8'),(25,'25/3'))):
        yy=236+i*146;words(c,y,181,yy,49,GOLD);arrow(c,(261,yy),(525,yy),f,TEAL)
        if f:words(c,'÷3',392,yy-44,30,TEAL)
        if f==1:words(c,result,633,yy,46,INK)
        if r>.45:words(c,('whole number','between 8 and 9')[i],962,yy,31,(TEAL,CORAL)[i])
    if t>=29.4:words(c,'Keep only states allowed by the question.',640,521,32,TEAL)

def basic_question(c,t):
    heading(c,'What number went into the machine?')
    machine(c,('?','?','27' if t>=36 else '?'),(cue(t,31.9,1.4),cue(t,34,1.4)),(0,0))
    if t>=39.6:arrow(c,(1060,508),(222,508),cue(t,39.6,2.4),TEAL)
    if t>=41.4:words(c,'start here',1068,553,23,TEAL)

def basic_solution(c,t):
    heading(c,'Return to the value before each operation')
    r1=cue(t,45.7,2.4);r2=cue(t,52.6,1.4)
    machine(c,('6' if r2>.72 else '?','9' if t>=49.5 else '?','27'),
            (cue(t,55.6,1.1),cue(t,57.2,1.1)),(r2,r1))
    if t>=57.9:words(c,'(6 + 3) × 3 = 27',640,523,38,GOLD)

def token(c,x,y,col):
    c.dot(x,y,12,DEEP);c.dot(x,y-2,11,col);c.line([(x-4,y-2),(x+4,y-2)],DEEP,2)

def tray(c,i,amount,dx=0,dy=0,colour=TEAL):
    x=144+i*245+dx;y=255+dy
    c.rect(x,y,197,122,DEEP,LINE,3)
    for j in range(amount):token(c,x+36+j%4*40,y+40+j//4*44,colour)

def pile_q(c,t):
    heading(c,'One equal part is removed, then five counters arrive')
    take=cue(t,60.45,2);add=cue(t,63.1,1.65)
    for i in range(4):
        x=144+i*245;y=255-97*take*(i==3)
        c.rect(x,y,197,122,DEEP,CORAL if i==3 else LINE,3)
        words(c,'1 part',x+99,y+62,31,CORAL if i==3 else TEAL)
    if take==1:words(c,'removed',978,128,23,CORAL)
    for j in range(5):
        if add:token(c,400+j*42,466-50*add,GOLD)
    if add==1:words(c,'5 added',715,416,26,GOLD)
    if t>=64.8:words(c,'Final pile   26 counters',640,534,36,INK)

def pile_a(c,t):
    heading(c,'Rebuild the pile one equal part at a time')
    remove=cue(t,76.05,1.9);split=cue(t,82.6,2.3);restore=cue(t,87.8,2.0)
    for i in range(3):
        x=144+i*245
        if split:c.rect(x,255,197,122,DEEP,LINE,3)
        for j in range(7):
            k=i*7+j
            token(c,mix(185+(k%11)*51,x+36+j%4*40,split),
                  mix(288+(k//11)*56,295+j//4*44,split),TEAL)
    if remove<1:
        for j in range(5):token(c,433+j*48,459+156*remove,GOLD)
    if t>=78:words(c,'26 − 5 = 21',215,479,31,GOLD)
    if t>=85:words(c,'21 ÷ 3 = 7',631,479,31,TEAL)
    if restore:
        tray(c,3,7,0,-102*(1-restore),CORAL)
        if restore==1:words(c,'4 × 7 = 28',1045,479,31,CORAL)

def rail(c, values, labels, count):
    n=len(values);xs=[138+1005*i/(n-1) for i in range(n)]
    for i,(x,v) in enumerate(zip(xs,values)):
        c.dot(x,296,43,LINE);c.dot(x,296,39,DEEP)
        if i<=count:words(c,v,x,296,34,GOLD if i==n-1 else INK)
        if i<n-1:
            progress=max(0,min(1,count-i));a=(x+50,296);b=(xs[i+1]-50,296)
            c.line([a,b],LINE,2)
            if progress:arrow(c,a,b,progress,TEAL);words(c,labels[i],(x+xs[i+1])/2,237,29,TEAL)

def challenge(c,t):
    heading(c,'Which inputs land inside the permitted interval?')
    rail(c,('n','?','?','?','y'),('+2','×3','÷2','−4'),4*cue(t,95.8,4.9))
    if t>=101.2:
        words(c,'Permitted output y',640,420,26,QUIET)
        for i,val in enumerate(OUTPUTS):
            if cue(t,101.2,2.9)>i/10:words(c,val,181+i*102,494,34,GOLD)

def table(c,t,final=False):
    heading(c,'Work back from every possible output' if not final else 'Recover the inputs that passed the test')
    x0=340;dx=89
    rows=[('output',OUTPUTS,GOLD,1),
          ('add 4',tuple(y+4 for y in OUTPUTS),INK,1 if final else cue(t,111.85,1.7)),
          ('multiply by 2',tuple(2*(y+4) for y in OUTPUTS),INK,1 if final else cue(t,114.6,1.7))]
    if final:
        rows.extend([('divide by 3',tuple(2*(y+4)//3 if y in VALID else '' for y in OUTPUTS),TEAL,cue(t,135.6,1.5)),
                     ('subtract 2',tuple(2*(y+4)//3-2 if y in VALID else '' for y in OUTPUTS),GOLD,cue(t,138.6,1.5))])
    for j,(name,vals,col,p) in enumerate(rows):
        y=162+j*65;words(c,name,86,y,25,QUIET,'lm');c.line([(286,y+30),(1205,y+30)],LINE,2)
        for i,v in enumerate(vals):
            if p>i/len(vals):words(c,v,x0+dx*i,y,29,col)
    scan=1 if final else cue(t,121.6,6.3)
    for i,n in enumerate(OUTPUTS):
        if scan<=(i+.1)/10:continue
        x=x0+dx*i;good=n in VALID
        if good:c.rect(x-33,261,66,63,None,TEAL,3)
        else:c.line([(x-22,310),(x+22,273)],CORAL,3)
    if not final and t>=129.8:words(c,'Keep 23, 26, 29 and 32.',642,478,32,TEAL)
    if final and t>=140.2:words(c,'Possible inputs   16, 18, 20, 22',640,530,34,TEAL)

def filtered(c,t):table(c,t)

def recover(c,t):
    if t<143.8:table(c,t,True)
    else:
        heading(c,'Check one of the recovered inputs')
        rail(c,(16,18,54,27,23),('+2','×3','÷2','−4'),4*cue(t,143.8,4.1))
        if t>=149.6:words(c,'All ten outputs were tested.',640,488,32,TEAL)

def mistakes(c,t):
    if t<162:
        heading(c,'Changing the order changes the answer')
        machine(c,('6','9','27'),(0,0),(cue(t,155,1.5),cue(t,153.25,1.5)))
        if t>=157.6:words(c,'Subtracting first gives (27 − 3) ÷ 3 = 8.',640,520,29,CORAL)
    else:
        heading(c,'Identify the whole used for the fraction')
        for i in range(3):tray(c,i,7)
        if t>=165.4:tray(c,3,7,0,0,CORAL)
        words(c,'21 counters are three parts.',580,468,32,TEAL)
        if t>=166.9:words(c,'All four parts contain 28.',640,530,32,CORAL)

def close(c,t):
    heading(c,'Trace an input through the complete chain')
    if t<180.8:
        rail(c,(32,36,72,24,22),('+4','×2','÷3','−2'),4*cue(t,172.2,5.0))
        words(c,'Starting at an allowed output',640,462,29,GOLD)
    else:
        rail(c,(22,24,72,36,32),('+2','×3','÷2','−4'),4*cue(t,180.8,3.0))
        words(c,'The input 22 returns to the output 32.',640,462,32,TEAL)

SCENES=(opening,exams,basic_question,basic_solution,pile_q,pile_a,challenge,filtered,recover,mistakes,close)
def verify():
    forward=lambda n: Fraction((n+2)*3,2)-4
    assert [n for n in range(1,100) if forward(n) in OUTPUTS]==[16,18,20,22]
    assert tuple(forward(n) for n in (16,18,20,22))==VALID
    assert (6+3)*3==27 and 28-28//4+5==26 and 21==3*7
