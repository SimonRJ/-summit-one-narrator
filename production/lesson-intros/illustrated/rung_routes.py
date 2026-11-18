"""S052. A fixed lamp anchors a doubling display; a broken ladder partitions the final jumps."""
from math import sin,pi
from collections import Counter
from captioned_film import cue,mix
ID='S052'
ORIGINAL='290d74be586ef0d9c2b54995b397533c1d91221b06e6b85c743c28e4854cee61'
START=(0,17.72,35.32,48.1,60.74,76.39,97.98,115.55,136.34,152.18,165.78)
POSTER=134.7
PAPER='#222f30';WHITE='#fff1dc';GREEN='#9ce6b5';YELLOW='#f6c579';RED='#ffa292';AQUA='#91d9eb'
MUTED='#bfd1c8';SHELF='#405350';DARK='#182629'
COUNTS=(1,1,2,0,2,2,4,6,10,16)
def label(c,s,x,y,z=30,col=WHITE,anchor='mm'):c.text(s,x,y,z,col,anchor,True)
def head(c,s):label(c,s,59,61,40,WHITE,'lm')
def xof(n):return 125+n*112
def number_path(c,vals,phase):
    n=len(vals);base=166;step=280;y=302
    for i,v in enumerate(vals):
        x=base+step*i;c.dot(x,y,45,SHELF);c.dot(x,y,41,DARK)
        if i<=phase:label(c,v,x,y,42,YELLOW)
        label(c,'term '+str(i+1),x,y+95,25,MUTED)
        if i<n-1 and phase>i:
            p=min(1,phase-i);c.line([(x+53,y),(x+53+(step-107)*p,y)],AQUA,4)
            label(c,'+4',x+step/2,y-47,28,AQUA)
def intro(c,t):
    head(c,'A state can inherit routes from two places')
    for i,(x,y,name) in enumerate(((244,210,'two below'),(244,423,'one below'),(664,316,'landing'))):
        c.dot(x,y,48,SHELF);c.dot(x,y,40,DARK);label(c,name,x,y+(69 if i!=1 else 66),25,MUTED)
    for y,col,start in [(210,YELLOW,5.1),(423,AQUA,8.9)]:
        p=cue(t,start,1.6);c.line([(296,y),(mix(296,613,p),mix(y,316,p))],col,4)
    if t>=11.4:label(c,'Last jump: 1 or 2',1003,260,30,GREEN)
    if t>=14:label(c,'Add the route counts.',1002,362,26)

def short_paths(blocked):
    out=[1]
    for i in range(1,5):out.append(0 if i==blocked else out[i-1]+(out[i-2] if i>=2 else 0))
    return out
def exams(c,t):
    head(c,'Change one landing and follow the effect')
    a=short_paths(None);b=short_paths(2)
    for r,vals in enumerate((a,b)):
        yy=251+160*r
        if r and t<26.8:continue
        for j,n in enumerate(vals):
            xx=289+j*170;col=RED if r and j==2 else GREEN
            c.line([(xx-73,yy),(xx+73,yy)],SHELF,4);c.dot(xx,yy,23,col)
            label(c,j,xx,yy,22,DARK);label(c,n,xx,yy+58,30,col)
        label(c,('open','blocked at 2')[r],138,yy,23,MUTED)
    label(c,'route counts below the landings',640,555,26,MUTED)
def basic_q(c,t):
    head(c,'Start at six and add four each time')
    number_path(c,(6,10,14,18),0)
    if t>=37.4:label(c,'One move adds 4.',640,490,31,AQUA)
    if t>=41.4:label(c,'Term 1 is the starting value.',640,548,28,MUTED)
def basic_a(c,t):
    head(c,'Make the three additions')
    phase=cue(t,48.15,1.15)+cue(t,50.65,1.1)+cue(t,52.1,1.1)
    number_path(c,(6,10,14,18),phase)
    if t>=54:label(c,'10 − 6 = 14 − 10 = 18 − 14 = 4',640,504,33,GREEN)
def display(c,count):
    x=166;u=8.55;y=385
    c.rect(x,y-45,u*97,45,DARK,SHELF,2)
    c.rect(x,y-45,u,45,YELLOW)
    c.rect(x+u,y-45,count*u,45,GREEN)
    for a in (0,1,25,49,73,97):
        xx=x+a*u;c.line([(xx,y),(xx,y+12)],MUTED,2)
        if a!=1:label(c,a,xx,y+41,22,MUTED)
    label(c,'1 fixed',x+31,249,27,YELLOW)
    c.line([(x+u/2,y-48),(x+u/2,283),(x+75,283)],YELLOW,2)
def middle_q(c,t):
    head(c,'Each new reading is twice the last, minus one')
    display(c,3);label(c,'starting reading   4',739,218,32,GREEN)
    if t>=65.5:label(c,'After five changes?',862,505,31)
    if t>=69.6:label(c,'Separate the fixed 1.',390,505,28,YELLOW)
def middle_a(c,t):
    head(c,'The distance from one doubles')
    times=(84.0,85.9,87.0,88.0,89.1)
    elapsed=sum(cue(t,at,.82) for at in times);i=min(4,int(elapsed))
    gap=mix(3*2**i,3*2**(i+1),elapsed-i) if elapsed<5 else 96
    display(c,gap)
    label(c,'2(1 + g) − 1 = 1 + 2g',715,183,33,GREEN)
    if t>=85:label(c,'Gaps    3, 6, 12, 24, 48, 96',729,257,26,MUTED)
    if t>=91:label(c,'1 + 3 × 2⁵ = 97',712,504,37,YELLOW)
    if t>=95:label(c,'First readings    4 → 7 → 13',712,565,26)
def ladder(c,broken=True):
    for y in (256,369):c.line([(76,y),(1183,y)],SHELF,8)
    for i in range(10):
        x=xof(i)
        if broken and i==3:
            c.line([(x,260),(x,283),(x-6,296)],RED,7)
            c.line([(x+7,331),(x,342),(x,366)],RED,7)
        else:c.line([(x,259),(x,366)],MUTED,7)
        label(c,i,x,399,24,RED if broken and i==3 else MUTED)
    label(c,'rung',78,399,20,MUTED,'rm')
def hop(c,a,b,p,ink,offset=0):
    if p<=0:return
    x1,x2=xof(a),xof(b);y=261
    coords=[]
    for j in range(27):
        k=p*j/26;coords.append((mix(x1,x2,k),y-(47+12*(b-a)-offset)*sin(pi*k)))
    c.line(coords,ink,4);c.dot(*coords[-1],9,ink)
def counts(c,visible=9):
    for j in range(10):
        x=xof(j);c.rect(x-38,450,76,56,DARK,SHELF,2)
        if j<=visible:label(c,COUNTS[j],x,478,31,RED if j==3 else GREEN)
    label(c,'ways',77,479,20,GREEN,'rm')
def ladder_q(c,t):
    head(c,'Reach rung 9 without landing on rung 3')
    ladder(c,t>=102.4)
    if t>=99.8:
        hop(c,0,1,cue(t,99.85,.95),AQUA)
        hop(c,0,2,cue(t,101.1,1.05),YELLOW,-24)
    if t>=105.8:label(c,'Each route is a different sequence of 1s and 2s.',640,506,30)
    if t>=109.8:label(c,'Which rung could come immediately before 9?',640,565,26,YELLOW)
def ladder_a(c,t):
    head(c,'Add the two possible last-jump counts')
    ladder(c)
    visible=0 if t<121.8 else min(9,int(9*cue(t,122.0,11.75)))
    counts(c,visible)
    if 119.2<=t and visible<3:label(c,0,xof(3),478,31,RED)
    if t<130.8 and visible>=2:
        n=min(9,visible+1)
        if n!=3:
            for back,col in ((2,YELLOW),(1,AQUA)):
                if n-back!=3:hop(c,n-back,n,.99,col,-16 if back==2 else 6)
    if t>=130.8:
        hop(c,7,9,cue(t,130.8,1.35),YELLOW,-29);hop(c,8,9,cue(t,132.3,1.3),AQUA,5)
    if t>=134:label(c,'6 + 10 = 16 routes',640,561,35,GREEN)
def landings(c,t):
    head(c,'A broken rung rules out landings there')
    ladder(c);counts(c)
    if t<145.2:
        hop(c,2,4,cue(t,137,2.55),YELLOW)
        if t>=139.6:label(c,'2 → 4 jumps over the break.',640,565,30,YELLOW)
    else:
        hop(c,7,9,cue(t,145.2,1.6),YELLOW,-27);hop(c,8,9,cue(t,147.8,1.4),AQUA,4)
        label(c,'Every arrival has exactly one last jump.',640,565,29,GREEN)
def mistakes(c,t):
    head(c,'Count the empty route at the start')
    ladder(c);counts(c,0)
    if t>=155.6:hop(c,0,1,cue(t,155.6,1.8),AQUA);label(c,1,xof(1),478,31,GREEN)
    if t>=160:label(c,0,xof(3),478,31,RED)
    if t>=162.6:hop(c,2,4,cue(t,162.6,1.8),YELLOW)
    label(c,'Making no jumps is one way to be on rung 0.',640,562,27)
def finish(c,t):
    head(c,'Read the route table in dependency order')
    ladder(c);n=int(9*cue(t,166,7.5));counts(c,n)
    if t>=173:hop(c,2,4,cue(t,173.1,1.65),YELLOW)
    if t>=176.6:hop(c,7,9,cue(t,176.6,1.4),YELLOW,-26);hop(c,8,9,cue(t,178.1,1.45),AQUA)
    if t>=179:label(c,'Six finish with +2. Ten finish with +1.',640,559,29,GREEN)
SCENES=(intro,exams,basic_q,basic_a,middle_q,middle_a,ladder_q,ladder_a,landings,mistakes,finish)
def verify():
    from itertools import product
    from itertools import accumulate
    paths=[]
    for k in range(10):
        for jumps in product((1,2),repeat=k):
            reaches=(0,*accumulate(jumps))
            if 3 not in reaches and reaches[-1]<=9:paths.append((reaches[-1],jumps))
    assert tuple(sum(n==r for n,_ in paths) for r in range(10))==COUNTS
    assert Counter(m[-1] for n,m in paths if n==9)=={1:10,2:6}
    vals=[4]
    for _ in range(5):vals.append(2*vals[-1]-1)
    assert vals==[4,7,13,25,49,97] and 6+3*4==18
