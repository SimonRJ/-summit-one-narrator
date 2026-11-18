"""S060. Slide letter tiles into neighbour brackets, expand both orientations and sort all 720 seating orders."""
from collections import Counter
from itertools import permutations
from math import factorial, floor, pi, sin
from captioned_film import cue,font,mix

ID='S060'
ORIGINAL='0c5486ec5021a07f7e772433aa2aa85cdaa1192db370c8ce030c62a9d456087c'
START=(0.,15.,32.28,46.49,62.17,77.34,95.58,114.75,143.06,160.5,179.54)
POSTER=152.9
PAPER='#f5f2e9'
INK,SOFT,GRID='#252f45','#566675','#cbd0c7'
AB,CD,BOTH,OTHER='#ba665e','#518aa1','#705d92','#bec8c4'
FILL={'A':'#f3c9bd','B':'#f4dfbd','C':'#c7dfe8','D':'#c3ded0','E':'#ded3e6','F':'#ecd99d'}
PAIRS=tuple(permutations('ABC'))
NAMES='ABCDEF'
def mask(order):
    return int(abs(order.index('A')-order.index('B'))==1)+2*int(abs(order.index('C')-order.index('D'))==1)
CLASSES=(1,3,2,0)
ORDERS=tuple(sorted(permutations(NAMES),key=lambda v:(CLASSES.index(mask(v)),v)))
M={1:AB,2:CD,3:BOTH,0:OTHER}
def label(c,s,x,y,z=29,col=INK,anchor='lm'):c.text(s,x,y,z,col,anchor,True)
def title(c,s):
    z=40
    while font(round(z*c.scale),True).getlength(s)>1152*c.scale:z-=1
    label(c,s,58,52,z)
def card(c,l,x,y,side=70):
    c.rect(x-side/2+3,y-side*.55+4,side,side*1.1,'#d9d4c7')
    c.rect(x-side/2,y-side*.55,side,side*1.1,FILL[l],INK,2)
    label(c,l,x,y,round(side*.57),INK,'mm')
def row(c,order,x,y,spacing=91,side=65):
    for i,l in enumerate(order):card(c,l,x+spacing*i,y,side)
def bracket(c,x1,x2,y,col,depth=14):
    c.line([(x1,y-depth),(x1,y),(x2,y),(x2,y-depth)],col,4)
def grid(c,x0,y0,size,visible,high=None):
    for i,order in enumerate(ORDERS):
        key=mask(order);colour=M[key] if key in visible else '#e5e7df'
        if high is not None and key not in high:colour='#e5e7df'
        x=x0+(i%36)*size;y=y0+(i//36)*size
        c.rect(x,y,size-2,size-2,colour)
def example_order(c,t,begin,end,base):
    # The selected square has a stable identity in the enumeration.
    step=int((t-begin)//1.45)
    index=base+step%end
    x=100+(index%36)*18;y=143+(index//36)*18
    c.rect(x-2,y-2,21,21,None,INK,3)
    order=ORDERS[index]
    row(c,order,842,394,43,32)
    for a,b,col in (('A','B',AB),('C','D',CD)):
        i,j=order.index(a),order.index(b)
        if abs(i-j)==1:bracket(c,842+43*min(i,j)-17,842+43*max(i,j)+17,425,col,7)

def overlap(c,x,y):
    # Clip the intersection to the true circular boundaries.
    radius=96;delta=105
    c.draw.ellipse(c.xy((x-radius,y-radius,x+radius,y+radius)),fill='#f1d4c8',outline=AB,width=max(1,round(3*c.scale)))
    c.draw.ellipse(c.xy((x+delta-radius,y-radius,x+delta+radius,y+radius)),fill='#d2e4e6',outline=CD,width=max(1,round(3*c.scale)))
    pts=[]
    for i in range(65):
        xx=x+delta-radius+(2*radius-delta)*i/64
        h=min((max(0,radius**2-(xx-x)**2))**.5,(max(0,radius**2-(xx-x-delta)**2))**.5)
        pts.append((xx,h))
    c.poly([(xx,y+h) for xx,h in pts]+[(xx,y-h) for xx,h in reversed(pts)],'#cdbbd2',None)
    label(c,'AB',x-25,y,24,AB,'mm');label(c,'CD',x+delta+25,y,24,CD,'mm')
def block(c,t):
    title(c,'Treat a required pair as a movable unit')
    p=cue(t,3.6,2.2);q=cue(t,6,1.7);swap=cue(t,9,1.7)
    # A and B approach, travel together and then exchange places within their bracket.
    left=mix(250,430,p)+135*q;right=mix(812,532,p)+135*q
    card(c,'A',mix(left,right,swap),305-48*sin(pi*swap),82)
    card(c,'B',mix(right,left,swap),305+48*sin(pi*swap),82)
    if p>.8:bracket(c,left-49,right+49,399,AB)
    if t>=8.4:label(c,'AB or BA',640,497,39,AB,'mm')
def applications(c,t):
    title(c,'Start with the strongest neighbour rule')
    row(c,'CABDE',163,247,109,70)
    if t>=17.7:bracket(c,225,420,316,AB)
    if t>=22.4:label(c,'A next to B',194,401,31,AB)
    if t>=25:
        overlap(c,902,287)
        if t>=28.4:label(c,'Some orders meet both rules.',749,456,27,SOFT)
def three(c,t):
    title(c,'Three distinct cards · how many lines?')
    p=cue(t,39,1.2)
    for i,l in enumerate('ABC'):card(c,l,mix(332+i*275,257+i*275,p),mix(281,249 if i==0 else 297,p),92)
    for j in range(3):
        x=253+j*271
        c.line([(x-71,413),(x+71,413)],SOFT,3);label(c,str(j+1),x,465,25,SOFT,'mm')
    if t>=39:label(c,'Choose a first card.',836,514,28,AB)
def six(c,t):
    title(c,'Every completed branch is one full order')
    for k,(left,right) in enumerate(((PAIRS[0],PAIRS[1]),(PAIRS[2],PAIRS[3]),(PAIRS[4],PAIRS[5]))):
        xx=132+385*k
        if t>=46.6+.42*k:card(c,left[0],xx+92,176,53)
        if t>=49.6:
            for j,order in enumerate((left,right)):
                y=294+j*108;segment=[(xx+92,209),(xx+92,226),(xx-20,253),(xx-20,y)]
                c.line(segment,GRID,2)
                row(c,order,xx,y,64,42)
    if t>=54:label(c,'3 choices × 2 × 1',640,520,34,SOFT,'mm')
    if t>=60:label(c,'6 orders',1049,526,32,AB,'mm')
def five(c,t):
    title(c,'Five name cards, with A next to B')
    row(c,'CABDE',195,255,176,82)
    if t>=65.2:bracket(c,318,598,331,AB)
    if t>=69:
        a=cue(t,69.2,1.2);card(c,'A',mix(525,664,a),477-25*sin(pi*a),62);card(c,'B',mix(664,525,a),477+25*sin(pi*a),62)
        bracket(c,482,707,542,AB)
    if t>=71.6:label(c,'Both orders are allowed.',783,485,28,AB)
def four_objects(c,t):
    title(c,'Compress, arrange, then reopen the pair')
    f=cue(t,77.4,1.8);swap=cue(t,85.4,1.5)
    centres=(167,394,681,915)
    card(c,'C',centres[0],265,70)
    x1=mix(323,centres[1]-37,f);x2=mix(531,centres[1]+37,f)
    card(c,'A',mix(x1,x2,swap),265-31*sin(pi*swap),63);card(c,'B',mix(x2,x1,swap),265+31*sin(pi*swap),63)
    bracket(c,x1-37,x2+37,344,AB)
    card(c,'D',centres[2],265,70);card(c,'E',centres[3],265,70)
    if t>=79.8:
        for i,x in enumerate(centres):label(c,str(i+1),x,392,23,SOFT,'mm')
    if t>=82:label(c,'4! = 24 block orders',124,506,33)
    if t>=88.8:label(c,'× 2 = 48 full orders',693,506,33,AB)
def sets(c,t):
    title(c,'Which orders have exactly one neighbouring pair?')
    row(c,'ABCDEF',132,231,104,65)
    if t>=100.4:
        bracket(c,94,277,293,AB);bracket(c,303,487,293,CD)
    if t>=107.6:overlap(c,918,281)
    if t>=105.8:label(c,'An order with both pairs fails the condition.',129,451,30,SOFT)
def all_orders(c,t):
    title(c,'One square per arrangement of the six cards')
    active={0,1,2,3} if t<118 else {1,3} if t<123.8 else {1,2,3} if t<129.8 else {3}
    grid(c,100,143,18,active)
    label(c,'6! = 720 orders',842,177,32)
    if t>=118:label(c,'AB together   240',842,259,28,AB)
    if t>=123.8:label(c,'CD together   240',842,325,28,CD)
    if t>=125.8:example_order(c,t,125.8,96,144)
    if t>=129.8:label(c,'Both = 4! × 2 × 2 = 96',818,495,27,BOTH)
    if t>=134.8:label(c,'All 96 shared orders occur in both counts.',103,551,28,BOTH)
def exclusive(c,t):
    title(c,'Remove the overlap from each pair count')
    active={1,2,3} if t<144 else {1,2}
    grid(c,100,143,18,active)
    label(c,'AB only',827,175,29,AB)
    if t>=143.3:label(c,'240 − 96 = 144',827,231,32,AB)
    if t>=146.4:label(c,'CD only',827,300,29,CD);label(c,'240 − 96 = 144',827,356,32,CD)
    if t>=151.4:label(c,'144 + 144 = 288',811,462,35)
    if t>=153.8:
        row(c,'ABCEDF',129,552,57,40);bracket(c,105,211,588,AB,7)
        row(c,'AECDBF',528,552,57,40);bracket(c,620,720,588,CD,7)
def traps(c,t):
    title(c,'Required neighbours and forbidden neighbours')
    row(c,'DABCE',153,235,100,65);bracket(c,218,388,299,AB)
    if t>=163.6:row(c,'DBACE',153,397,100,65);bracket(c,218,388,461,AB)
    if t>=170.6:
        overlap(c,898,290);label(c,'Outside both regions',789,444,28)
    if t>=175.4:label(c,'For “neither”, subtract the union.',743,524,25,SOFT)
def recap(c,t):
    title(c,'Test an actual arrangement against both rules')
    cases=(('ABCEDF','AB only',AB),('AECDBF','CD only',CD),('ABCDEF','Both',BOTH),('ACEBDF','Neither',SOFT))
    for j,(order,name,col) in enumerate(cases):
        x=152+591*(j%2);y=194+196*(j//2)
        if t<179.6+1.45*j:continue
        row(c,order,x,y,59,40);m=mask(order)
        for yes,a,b,colour in ((m&1,'A','B',AB),(m&2,'C','D',CD)):
            if yes and t>=181.4:
                ix=min(order.index(a),order.index(b));bracket(c,x+ix*59-22,x+(ix+1)*59+22,y+40,colour,7)
        if t>=186.2:label(c,name,x,y+88,27,col)
    if t>=188.6:label(c,'Exactly one pair   →   keep AB only or CD only.',640,548,25,INK,'mm')
SCENES=(block,applications,three,six,five,four_objects,sets,all_orders,exclusive,traps,recap)
def verify():
    freq=Counter(mask(order) for order in ORDERS)
    assert freq=={0:336,1:144,2:144,3:96} and sum(freq.values())==factorial(6)==720
    assert freq[1]+freq[3]==freq[2]+freq[3]==240 and freq[1]+freq[2]==288
    assert [mask(o) for o in ('ABCEDF','AECDBF','ABCDEF','ACEBDF')]==[1,2,3,0]
    assert sum(abs(o.index('A')-o.index('B'))==1 for o in permutations('ABCDE'))==48 and len(PAIRS)==6
