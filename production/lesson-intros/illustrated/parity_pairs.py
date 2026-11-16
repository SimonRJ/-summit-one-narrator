"""S018: pairs, even-length jumps, and an invariant during merges."""
from math import sin,pi
from visuals import AQUA, BLUE, GOLD, PINK, SOFT, WHITE, VIOLET, ease, mix


def text(a,t,x,y,size=34,col=WHITE,alpha=1):a.label(t,x,y,size,col,alpha,bold=True)


def pair(a,x,y,col=BLUE,alpha=1):
    a.rounded(x-31,y-22,62,44,9,col,.15*alpha)
    a.circle((x-12,y),9,col,alpha);a.circle((x+12,y),9,col,alpha)


def pair_rows(a,p=1,q=1):
    text(a,'13',115,270,44,BLUE,p)
    for i in range(6):pair(a,240+i*115,270,BLUE,p)
    a.circle((1030,270),11,PINK,p)
    text(a,'18',115,440,44,GOLD,q)
    for i in range(9):pair(a,215+i*100,440,GOLD,q)


def card(a,n,x,y=300,alpha=1):
    a.rounded(x-62,y-48,124,96,12,BLUE,.17*alpha)
    text(a,str(n),x,y,46,WHITE,alpha)


def number_line(a,token=13,arc=0,unreachable=0):
    x0=180;step=92;y=375
    a.path(((x0,y),(x0+10*step,y)),SOFT,3)
    for n in range(10,21):
        x=x0+(n-10)*step;col=BLUE if n%2 else GOLD
        a.path(((x,y-10),(x,y+10)),col,4)
        text(a,str(n),x,y+55,30,col)
    a.circle((x0+(token-10)*step,y-arc),16,AQUA)
    text(a,'start: 13',x0+3*step,235,30,AQUA)
    text(a,'target: 18',x0+8*step,235,30,PINK)
    a.path(((x0+8*step-30,275),(x0+8*step+30,335)),PINK,4,unreachable)
    a.path(((x0+8*step-30,335),(x0+8*step+30,275)),PINK,4,unreachable)


def intro(a,c):
    a.heading('Even means complete pairs',BLUE)
    p=c.after('even number as pairs')
    for i in range(3):pair(a,350+i*110,280,BLUE,p)
    text(a,'6 is even',460,365,33,BLUE,p)
    q=c.after('odd number as pairs')
    for i in range(3):pair(a,740+i*110,280,GOLD,q)
    a.circle((1080,280),11,PINK,q)
    text(a,'7 is odd',850,365,33,GOLD,q)
    text(a,'one counter is left over',640,520,31,SOFT,c.after('one left over'))


def exams(a,c):
    a.heading('Parity can reveal an impossibility',AQUA)
    p=c.after('jumps')
    for i in range(5):a.circle((340+i*150,300),15,BLUE if i%2 else GOLD,p)
    a.arrow((340,245),(640,245),AQUA,p)
    text(a,'a two-step move keeps the colour',640,460,33,SOFT,c.after('two-colour pattern'))


def easy(a,c):
    a.heading('13 + 18: odd or even?',BLUE)
    pair_rows(a,c.after('thirteen'),c.after('eighteen'))
    text(a,'Look for an unpaired counter',640,550,30,SOFT,c.after('unpaired counters'))


def easy_answer(a,c):
    a.heading('One counter remains unpaired',BLUE)
    pair_rows(a,c.opening(),c.opening())
    text(a,'one extra',1080,335,29,PINK,c.after('one extra counter'))
    text(a,'13 + 18 = 31, odd',640,555,40,WHITE,c.after('thirty-one'))


def jump_prompt(a,c):
    a.heading('Can even moves reach 18?',GOLD)
    p=c.after('even number of steps',1.6);q=c.after('direction may change',1.6)
    if q>0:token=15-2*q;arc=75*sin(pi*q)
    else:token=13+2*p;arc=75*sin(pi*p)
    number_line(a,token,arc)
    text(a,'Each move may be any even length',640,535,31,SOFT,c.after('even number of steps'))


def jump_answer(a,c):
    a.heading('Even moves preserve oddness',GOLD)
    p=c.after('Adding an even number',1.8);q=c.after('Subtracting an even number',1.8)
    if q>0:token=17-2*q;arc=75*sin(pi*q)
    else:token=13+4*p;arc=75*sin(pi*p)
    number_line(a,token,arc,c.after('unreachable'))
    text(a,'odd ± even = odd',640,530,40,WHITE,c.after('remain odd'))


def hard(a,c):
    a.heading('Merge any two numbers',VIOLET)
    p=c.after('numbers three')
    for i,n in enumerate((3,7,9,14,19)):card(a,n,280+i*180,300,ease(p*2-i*.17))
    text(a,'replace a and b by a + b + 1',640,475,35,SOFT,c.after('sum plus one'))
    text(a,'What remains after four moves?',640,550,31,WHITE,c.after('only one number'))


def layout(n):return [640+(i-(n-1)/2)*180 for i in range(n)]


def merging(a,old,new,p):
    oldx=layout(len(old));newx=layout(len(new));arc=105*sin(pi*p)
    card(a,old[0],mix(oldx[0],newx[0],p),300-arc,1-p)
    card(a,old[1],mix(oldx[1],newx[0],p),300+arc,1-p)
    card(a,new[0],newx[0],300,p)
    for i in range(2,len(old)):card(a,old[i],mix(oldx[i],newx[i-1],p),300,1)


def hard_answer(a,c):
    a.heading('Every merge adds 1 to the total',VIOLET)
    states=((3,7,9,14,19),(11,9,14,19),(21,14,19),(36,19),(56,))
    ps=[c.after('adds exactly one',1.2),c.after('Every move decreases',1.2),
        c.after('Five entries',1.0),c.after('four moves',1.0)]
    stage=0
    while stage<4 and ps[stage]>=.999:stage+=1
    p=ps[stage] if stage<4 else 1
    if stage<4:merging(a,states[stage],states[stage+1],p)
    else:card(a,56,640)
    if stage<4 and .02<p<.98:
        total=f'total: {52+stage} → {53+stage}'
    else:
        total='total = '+str(52+stage+(1 if stage<4 and p>=.98 else 0))
    text(a,total,640,500,45,WHITE,c.after('fifty-two'))
    text(a,'5 entries → 4 moves',640,560,32,SOFT,c.after('four moves'))


def other_order(a,c):
    a.heading('Different first pairs, same total',AQUA)
    p=c.after('left to right')
    text(a,'3 + 7 + 1 = 11',640,245,40,BLUE,p)
    q=c.after('swapping the first pair')
    text(a,'7 + 9 + 1 = 17',640,335,40,GOLD,q)
    text(a,'both lead to 56 after four moves',640,445,35,WHITE,c.after('each move adds one'))
    text(a,'n entries → n − 1 moves',640,535,31,SOFT,c.after('n minus one'))


def mistakes(a,c):
    a.heading('Parity is a necessary check',PINK)
    text(a,'odd + even = odd',640,260,43,BLUE,c.after('odd or even'))
    text(a,'same parity does not prove reachability',640,390,33,PINK,c.after('does not prove'))
    text(a,'also construct a legal route',640,510,33,WHITE,c.after('Use a construction'))


def recap(a,c):
    a.heading('Pairs, moves, and a check',AQUA)
    text(a,'13 + 18 = 31: odd',640,235,39,BLUE,c.after('one move'))
    text(a,'odd ± even stays odd',640,335,39,GOLD,c.after('stays fixed'))
    text(a,'52 + 4 = 56: even',640,435,39,AQUA,c.after('follows a pattern'))
    text(a,'explain why every move follows the rule',640,535,30,SOFT,c.after('explaining why'))


SCENES=(intro,exams,easy,easy_answer,jump_prompt,jump_answer,hard,hard_answer,
        other_order,mistakes,recap)
def draw(a,c,scene):SCENES[scene-1](a,c)
