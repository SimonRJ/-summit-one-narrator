"""S024. Count coloured beads, read an architect's two scale views, then move identical counters."""
from math import sin,pi
from captioned_film import mix
PAPER='#faf1e9';INK='#323549';MUTE='#726d73';RED='#c7494d';BLUE='#386fba';ICE='#cee4f5';SALMON='#f3c3b9';GREEN='#40845e';ORANGE='#cc7729';BORDER='#665d65';IVORY='#faf2cf'
def head(c,s):c.text(s,61,63,42,INK,'lm',True)
def note(c,s,x,y,size=32,col=INK):c.text(s,x,y,size,col,'lm',True)
def bead(c,x,y,r,col):
    c.dot(x,y+2,r,BORDER);c.dot(x,y,r-1,col)
    c.dot(x-r*.28,y-r*.30,r*.16,'#fff6e6')
    c.dot(x+r*.12,y+r*.06,r*.105,'#575764')
def strand(c,x,y,r,spacing,counts=(2,5),colours=(RED,BLUE),p=1):
    n=sum(counts)
    c.line([(x-r*1.75,y),(x+(n-1)*spacing+r*1.75,y)],'#a28770',3)
    for i in range(n):
        phase=max(0,min(1,p*n-i))
        if phase<=0:continue
        bead(c,x+i*spacing,y-32*(1-phase),r,colours[0 if i<counts[0] else 1])
def brace(c,x,X,y,col,txt):
    c.line([(x,y-9),(x,y),(X,y),(X,y-9)],col,3)
    c.text(txt,(x+X)/2,y+31,27,col,bold=True)
def idea(c,q):
    head(c,'Which quantities does the ratio compare?')
    strand(c,173,245,32,66,p=q.after('These beads',1.45))
    if q.after('two are red'):brace(c,142,274,313,RED,'2 red')
    if q.after('five are blue'):brace(c,282,601,313,BLUE,'5 blue')
    if q.after('two to five'):note(c,'Red to blue   2 : 5',725,225,34,BLUE)
    if q.after('two sevenths'):
        brace(c,141,602,422,INK,'7 in the whole strand')
        note(c,'Red out of all   2/7',725,361,34,RED)
def uses(c,q):
    head(c,'Find out what one unit represents')
    if not q.after('transfer puzzle'):
        plan(c,4,1,False)
        note(c,'What does 1 cm stand for?',716,278,31,BLUE)
    else:
        trays(c,0,False);c.text('Moving counters preserves the total.',640,529,34,INK,bold=True)
def basic(c,q):
    head(c,'Make three matching bead strands')
    strand(c,208,219,27,57,p=q.after('one strand',1.35))
    for j in (1,2):
        y=219+j*102;c.line([(160,y),(600,y)],'#b99c83',3)
    note(c,'2 red and 5 blue per strand',718,223,31)
    if q.after('three matching'):note(c,'3 strands',718,322,41,BLUE)
    if q.after('how many blues'):note(c,'Count each colour.',718,436,34)
def copies(c,q):
    head(c,'Copy every bead in the strand')
    strand(c,201,193,27,58)
    p=q.after('Copy the entire strand',2.25)
    for k in (1,2):
        f=max(0,min(1,p*2-k+1))
        if f:strand(c,201,193+103*k*f,27,58)
    if q.after('six red beads'):note(c,'3 × 2 = 6 red',725,228,39,RED)
    if q.after('fifteen blue beads'):note(c,'3 × 5 = 15 blue',725,319,39,BLUE)
    if q.after('dividing both numbers'):note(c,'6 : 15  →  2 : 5',725,442,39)
def plan(c,n,p,real):
    x=169;y=232;u=101
    # The plan is magnified for visibility. The real-wall elevation has its own labelled metre scale.
    c.rect(x-29,y-81,4*u+61,207,'#e2eef0',None)
    for i in range(15):c.line([(x-28+i*32,y-78),(x-28+i*32,y+125)],'#c6dcdd',1)
    for i in range(7):c.line([(x-27,y-78+i*32),(x+4*u+28,y-78+i*32)],'#c6dcdd',1)
    c.rect(x,y-26,n*u*p,26,BLUE);c.text('Plan',x-19,y-111,25,BLUE,'lm',True)
    c.line([(x,y+28),(x+4*u,y+28)],INK,2.5)
    for tick in range(41):
        X=x+u*tick/10;Y=y+28
        c.line([(X,Y),(X,Y+(20 if tick%10==0 else 7))],INK,2 if tick%10==0 else 1)
        if tick%10==0:c.text(str(tick//10),X,Y+44,23,INK,bold=True)
    c.text('cm on the drawing',x+2*u,y+95,25,BLUE,bold=True)
    if real:
        X=142;Y=498;w=111
        c.text('Actual wall',X,Y-105,26,INK,'lm',True)
        for i in range(4):
            c.rect(X+i*w,Y-70,w,53,'#dfbba6',BORDER,2)
            c.line([(X+i*w,Y-42),(X+(i+1)*w,Y-42)],BORDER,1.5)
            c.line([(X+i*w+w/2,Y-70),(X+i*w+w/2,Y-42)],BORDER,1.5)
            c.line([(X+i*w,Y+1),(X+(i+1)*w,Y+1)],INK,2)
            c.line([(X+i*w,Y-4),(X+i*w,Y+7)],INK,2)
        c.line([(X+4*w,Y-4),(X+4*w,Y+7)],INK,2)
        c.text('4 equal metre lengths',X+2*w,Y+37,24,INK,bold=True)
def scale_question(c,q):
    head(c,'Measure the wall on the architect’s plan')
    plan(c,4,q.after('wall measures',1.45),False)
    note(c,'Scale   1 : 100',731,226,39,BLUE)
    if q.after('ruler against'):note(c,'Drawing   4 cm',731,328,37)
    if q.after('How many metres'):note(c,'Actual length in metres?',713,444,32)
def scale_answer(c,q):
    head(c,'Read the scale before changing units')
    plan(c,4,1,q.after('one metre at a time')>0)
    note(c,'1 cm on the plan → 100 cm',701,197,31,BLUE)
    if q.after('four hundred centimetres'):note(c,'4 × 100 cm = 400 cm',701,308,35)
    if q.after('is four metres'):note(c,'400 cm = 4 m',701,426,41,RED)
TRAY_X=(93,680)
def origin(tray,group):
    return TRAY_X[tray]+73+(group%2)*208,219+(group//2)*105
def token(c,x,y,small=False):
    r=11 if small else 14
    c.dot(x,y+1.5,r+1,BORDER);c.dot(x,y,r,IVORY);c.dot(x-3,y-4,2.3,'#ffffff')
def group(c,tray,k,shown,offset=None):
    x,y=origin(tray,k)
    if offset:x,y=offset
    c.rect(x-21,y-18,117,68,'#f5e9d2','#b6a28e',2)
    if shown:
        for n in range(6):token(c,x+(n%3)*37,y+(n//3)*32,True)
def trays(c,p,show):
    for i,(col,bg,label) in enumerate(((RED,SALMON,'RED TRAY'),(BLUE,ICE,'BLUE TRAY'))):
        x=TRAY_X[i]
        c.rect(x,147,493,306,bg,col,4)
        c.text(label,x+246,174,24,col,bold=True)
    for tray,k in [(0,0),(0,1),(1,0),(1,1)]:group(c,tray,k,show)
    for k in (2,3):
        a=origin(0,k);b=origin(1,k)
        f=max(0,min(1,p*2-(k-2)));pos=(mix(a[0],b[0],f),mix(a[1],b[1],f)-74*sin(pi*f))
        group(c,0,k,show,pos)
def trays_question(c,q):
    head(c,'Move twelve identical counters between two trays')
    p=q.after('Move twelve counters',2.55)
    trays(c,p,False)
    c.text('Each outlined group is one equal part.',640,491,30,INK,bold=True)
    if q.after('ratio becomes'):c.text('4 : 2 before     →     2 : 4 after',640,550,36,BLUE,bold=True)
def trays_answer(c,q):
    head(c,'What is one equal part worth?')
    p=q.after('two extra parts appear',2.3);open_groups=q.after('One part holds six')>0
    trays(c,p,open_groups)
    if q.after('twelve counters'):c.text('2 parts = 12 counters',640,486,35,BLUE,bold=True)
    if q.after('Six parts therefore'):c.text('6 parts × 6 counters = 36',640,552,40,INK,bold=True)
def backwards(c,q):
    head(c,'Watch all twelve counters cross')
    p=q.after('Move exactly twelve',2.4);trays(c,p,True)
    if p<1:c.text('Before   24 in Red and 12 in Blue',640,505,34,INK,bold=True)
    else:c.text('After   12 in Red and 24 in Blue',640,495,34,INK,bold=True)
    if q.after('all thirty-six counters'):c.text('12 + 24 = 36',640,557,39,BLUE,bold=True)
def fraction(c,q):
    head(c,'Count the whole strand for a fraction')
    strand(c,156,246,29,60,(3,5),(ORANGE,GREEN))
    brace(c,131,302,307,RED,'3 orange')
    if q.after('all eight beads'):brace(c,131,608,410,INK,'8 beads altogether')
    if q.after('Three eighths'):note(c,'Orange out of all   3/8',715,254,33,RED)
    if q.after('Three fifths'):note(c,'Orange to green   3 : 5',715,375,32,GREEN)
def checklist(c,q):
    head(c,'Follow the unit, the recipe or the transfer')
    if not q.after('In a recipe'):
        plan(c,4,1,False);note(c,'Map one unit to its real length.',692,305,29,BLUE)
    elif not q.after('When the question'):
        strand(c,166,282,32,62);note(c,'Copy every colour together.',718,305,30,RED)
    else:
        trays(c,q.after('follow the objects',2),True)
        c.text('Both trays together still hold 36 counters.',640,525,34,INK,bold=True)
SCENES=(idea,uses,basic,copies,scale_question,scale_answer,trays_question,trays_answer,backwards,fraction,checklist)
def verify():
    assert (3*2,3*5)==(6,15) and 4*100/100==4
    assert 24-12==12 and 12+12==24 and 24+12==36
    assert 24/12==4/2 and 12/24==2/4
    for p in (0,1):
        group_centres=[origin(0,k) for k in range(2)]+[origin(1,k) for k in range(2)]+[origin(int(p),k) for k in (2,3)]
        assert len(set(group_centres))==6
    assert 3+5==8
