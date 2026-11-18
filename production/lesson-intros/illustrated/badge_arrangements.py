"""Count actual badge orders. Colour and silhouette persist through grouping, flipping and sorting."""
from itertools import permutations
from math import sin,cos,pi
from captioned_film import cue,mix

ID='S023'
ORIGINAL='a14eb946e9f31d2fc830a1b5d56b86ea681591e6f36e462feaf10950aa157854'
START=(0,15,32.28,46.17,61.85,76.86,94.78,113.63,140.98,158.42,177.46)
POSTER=87.2
PAPER='#22223b';WHITE='#fff4dc';GOLD='#f2c577';PINK='#ffa6aa';ICE='#a8e4db';SOFT='#cdc8de'
COL={'A':'#f4ada5','B':'#82cfc5','C':'#adbbff','D':'#ffc76b','E':'#e7aee9'}
EDGE='#242235'
def title(c,s):c.text(s,66,65,43,WHITE,'lm',True)
def note(c,s,x,y,size=32,ink=WHITE):c.text(s,x,y,size,ink,'lm',True)
def badge(c,name,x,y,r):
    r=float(r);col=COL[name]
    def contour(k):
        if name=='A':return [(x+cos(i*pi/24)*r*k,y+sin(i*pi/24)*r*k) for i in range(48)]
        if name=='B':p=[(-.91,-.88),(.91,-.88),(.91,.12),(.66,.62),(0,1.06),(-.66,.62),(-.91,.12)]
        elif name=='C':p=[(cos(i*pi/3),sin(i*pi/3)) for i in range(6)]
        elif name=='D':p=[(0,-1.12),(1.06,0),(0,1.12),(-1.06,0)]
        else:p=[((1 if i%2==0 else .72)*cos(i*pi/5-pi/2),(1 if i%2==0 else .72)*sin(i*pi/5-pi/2)) for i in range(10)]
        return [(x+k*r*i,y+k*r*j) for i,j in p]
    c.poly(contour(1),WHITE,EDGE,max(1,r*.055))
    c.poly(contour(.84),col,EDGE,max(1,r*.032))
    c.text(name,x,y,r*1.04,EDGE,bold=True)
def bracket(c,x1,x2,y,col=GOLD,depth=14):
    c.line([(x1,y-depth),(x1,y),(x2,y),(x2,y-depth)],col,4)
def row(c,letters,x,y,space,r,mark=()):
    for i,l in enumerate(letters):badge(c,l,x+i*space,y,r)
    for pair,col in mark:
        inds=[i for i,v in enumerate(letters) if v in pair]
        if len(inds)==2 and inds[1]-inds[0]==1:bracket(c,x+inds[0]*space-r,x+inds[1]*space+r,y+r+12,col,8)
def flip(c,x,y,r,gap,progress):
    for i,l in enumerate('AB'):
        offset=1 if i==0 else -1
        px=x+offset*(progress-.5)*gap
        py=y-offset*sin(progress*pi)*r*.78
        badge(c,l,px,py,r)
def pair_in(s,a,b):return abs(s.index(a)-s.index(b))==1
GROUPS={p:[] for p in [(False,False),(True,False),(True,True),(False,True)]}
for order in permutations('ABCDE'):
    GROUPS[pair_in(order,'A','B'),pair_in(order,'C','D')].append(''.join(order))
EXAMPLES={ (True,False):'ABDEC',(True,True):'ABECD',(False,True):'ACDEB',(False,False):'ACBED'}
def idea(c,t):
    title(c,'When can two badges travel as one?')
    p=cue(t,4.7,2.6);x=mix(440,510,p);gap=mix(265,148,p);u=cue(t,8.8,2.8)
    flip(c,x,290,66,gap,u)
    badge(c,'C',mix(937,842,p),290,66)
    if p>0:bracket(c,x-gap/2-67,x+gap/2+67,410)
    if t>=5.8:c.text('one movable block',x,470,34,GOLD,bold=True)
    if t>=11:c.text('AB and BA are different orders',640,555,31,WHITE,bold=True)
def applications(c,t):
    title(c,'A neighbour rule restricts the line')
    order='EABDC';sp=143
    for i,l in enumerate(order):
        x=350+sp*i;y=mix(356,268,cue(t,15.1+i*.33,1.0))
        badge(c,l,x,y,51)
    if t>=20.9:bracket(c,350+sp-55,350+2*sp+55,350,GOLD)
    if t>=22.4:note(c,'A next to B',355,437,36,GOLD)
    if t>=26.7:
        bracket(c,350+sp*3-55,350+sp*4+55,350,ICE)
        note(c,'C next to D',731,437,36,ICE)
    if t>=28.4:c.text('One line can satisfy both rules.',640,542,32,WHITE,bold=True)
def basic(c,t):
    title(c,'How many lines can three badges make?')
    for i,l in enumerate('ABC'):
        slide=cue(t,39.4,1.7) if i==0 else 0
        x=mix(435+i*205,460,slide);y=mix(250,432,slide)
        badge(c,l,x,y,60)
    for x in (460,640,820):c.line([(x-62,522),(x+62,522)],SOFT,3)
    c.text('First',460,563,26,SOFT);c.text('Second',640,563,26,SOFT);c.text('Last',820,563,26,SOFT)
    if t>=39:note(c,'Choose a first badge.',68,396,27,GOLD)
def six(c,t):
    title(c,'Every first choice branches into two')
    for i,first in enumerate('ABC'):
        x=230+i*410
        if t<46.2+i*.27:continue
        badge(c,first,x,175,45)
        for j,s in enumerate(s for s in permutations('ABC') if s[0]==first):
            y=320+j*110
            reveal=cue(t,49.0+i*.15+j*.3,.8)
            if reveal<=0:continue
            c.line([(x,229),(x,242),(x-145,242),(x-145,mix(242,y,reveal)),(x-117,mix(242,y,reveal))],SOFT,2)
            for k,l in enumerate(s):
                if k==2 and t<51.7:continue
                badge(c,l,x+(k-1)*76,y,31)
    if t>=53.6:c.text('3 × 2 × 1',565,554,42,WHITE,bold=True)
    if t>=59.1:note(c,'= 6',684,554,41,GOLD)
def four(c,t):
    title(c,'Four badges in a row. Keep A beside B.')
    p=cue(t,64.5,1.5);q=cue(t,69.0,2.0)
    gap=mix(202,136,p)
    flip(c,490,310,60,gap,q)
    badge(c,'C',mix(790,778,p),310,60);badge(c,'D',mix(992,944,p),310,60)
    if p:bracket(c,490-gap/2-59,490+gap/2+59,408)
    if t>=66.6:c.text('How many different lines are possible?',640,507,36,WHITE,bold=True)
def twelve(c,t):
    title(c,'Six outer orders, two ways inside each bracket')
    for i,perm in enumerate(permutations(('X','C','D'))):
        x=104+(i%3)*409;y=217+(i//3)*181
        if t<77+i*.36:continue
        p=cue(t,84.4+i*.10,2.0)
        for token in perm:
            if token=='X':
                flip(c,x+37,y,30,72,p);bracket(c,x-29,x+103,y+52,GOLD,10);x+=152
            else:badge(c,token,x,y,30);x+=77
    if t>=88:c.text('6 × 2 = 12 arrangements',640,553,44,GOLD,bold=True)
def rings(c,left,right):
    # One actual crossing pair of circles, with a labelled shared region.
    y=377;r=114
    for x,ink in ((547,GOLD),(733,ICE)):
        pts=[(x+r*cos(k*pi/90),y+r*sin(k*pi/90)) for k in range(181)]
        c.line(pts,ink,4)
    c.text(left,491,366,31,GOLD,bold=True);c.text(right,790,366,31,ICE,bold=True)
def challenge(c,t):
    title(c,'Which lines avoid both neighbour pairs?')
    row(c,'ABCDE',381,181,130,42)
    if t>=99.6:
        bracket(c,339,554,245,GOLD)
        bracket(c,600,812,245,ICE)
    if t>=106.5:rings(c,'AB','CD')
    if t>=108.6:c.text('Count the lines outside both circles.',640,551,34,WHITE,bold=True)
def partition(c):
    # The width of each strip is proportional to the exact number of orders.
    x=112;y=457;unit=8.8
    for key,colour,n in [((True,False),'#e8b87c',24),((True,True),'#ccaddc',24),((False,True),'#83c9be',24),((False,False),'#ede7d7',48)]:
        w=n*unit;c.rect(x,y,w,65,colour,PAPER,3)
        c.text(str(n),x+w/2,y+32,30,EDGE,bold=True)
        label={(True,False):'AB only',(True,True):'both',(False,True):'CD only',(False,False):'neither'}[key]
        c.text(label,x+w/2,555,25,WHITE,bold=True)
        x+=w
def overlap(c,t):
    title(c,'Count the orders that appear in both sets')
    note(c,'All five badges',75,162,30);note(c,'5 × 4 × 3 × 2 × 1 = 120',75,216,30,WHITE)
    if t>=116.5:note(c,'AB adjacent',75,292,29,GOLD);note(c,'2 × 24 = 48',75,342,31,GOLD)
    if t>=121.0:note(c,'CD adjacent',75,411,29,ICE);note(c,'2 × 24 = 48',75,461,31,ICE)
    if t>=123.3:
        row(c,'ABECD',657,245,100,36,[(('A','B'),GOLD),(('C','D'),ICE)])
        c.text('3 objects to order',870,359,32,WHITE,bold=True)
    if t>=127.4:c.text('Two orders in each pair',870,423,30,SOFT,bold=True)
    if t>=129.9:c.text('6 × 2 × 2 = 24 shared',870,503,33,PINK,bold=True)
    if t>=134.5:c.text('These same 24 belong to both sets.',648,569,25,SOFT)
def complement(c,t):
    title(c,'Remove the union to leave neither pair together')
    if t>=141:note(c,'At least one',83,158,33,GOLD);note(c,'48 + 48 − 24 = 72',83,215,36)
    if t>=147.5:note(c,'Neither',83,312,33,ICE)
    if t>=149.35:
        note(c,'120 − 72 = 48',83,374,37,ICE);partition(c)
    if t>=151.5:
        row(c,EXAMPLES[False,False],700,245,88,33)
        c.text('A and B apart. C and D apart.',870,325,26,WHITE,bold=True)
def warnings(c,t):
    title(c,'Read each neighbour rule literally')
    flip(c,324,263,55,131,cue(t,161.5,2.1))
    bracket(c,202,448,357)
    c.text('Required pair',328,424,36,GOLD,bold=True)
    if t>=165:c.text('Two different badges',328,486,27,SOFT)
    if t>=168.5:
        row(c,EXAMPLES[False,False],662,263,105,37)
        c.text('Both pairs forbidden',874,424,34,ICE,bold=True)
    if t>=173.3:c.text('Subtract the shared orders once.',868,493,26,SOFT)
def recap(c,t):
    title(c,'Decide what moves and what overlaps')
    if t>=177.5:
        row(c,'DABCE',326,231,152,48)
    if t>=179.4:bracket(c,426,681,318,GOLD)
    if t>=182:note(c,'Bracket the required pair.',72,414,32,GOLD)
    if t>=184.2:note(c,'Count its internal orders.',72,485,31,WHITE)
    if t>=186.5:
        note(c,'For two restrictions',715,414,32,ICE)
        note(c,'Count the overlap once.',715,485,31,WHITE)
SCENES=(idea,applications,basic,six,four,twelve,challenge,overlap,complement,warnings,recap)
def verify():
    assert len(set(permutations('ABC')))==6
    assert sum(pair_in(s,'A','B') for s in permutations('ABCD'))==12
    assert [len(GROUPS[k]) for k in [(True,False),(True,True),(False,True),(False,False)]]==[24,24,24,48]
    assert all(s in GROUPS[k] for k,s in EXAMPLES.items())
    assert len(set.union(*(set(v) for v in GROUPS.values())))==120
