"""S038. Remove equal weights, compare two score rows, and exchange child tickets for adult tickets."""
from math import cos,pi,sin
from captioned_film import cue,mix,font
ID='S038';ORIGINAL='0b6f9f3547dc11ad8a87c106357c73381726966583388b7dbaf802aabf346f87';START=(0,17.08,39.15,52.73,66.17,80.86,94.94,112.35,136.18,150.74,164.50);POSTER=140.6
PAPER='#2d2633';INK='#ffefdc';MUTED='#d0bcbb';LINE='#725d6d';DARK='#443646';BLUE='#8ccbd6';GOLD='#f4c375';RED='#ef9e90';MINT='#a8d8af';CREAM='#f3d7b7';BLACK='#3b3039'

def title(c,s):
    size=42
    while font(round(size*c.scale),True).getlength(s)>1150*c.scale:size-=1
    c.text(s,61,61,size,INK,'lm',True)
def label(c,s,x,y,sz=32,col=INK):c.text(s,x,y,sz,col,'lm',True)

def block(c,x,y,w,h,s,colour):
    c.rect(x,y,w,h,colour,BLACK,2.3);c.text(s,x+w/2,y+h/2,24 if h>37 else 19,BLACK,bold=True)

def bench(c):
    x=642;y=374;c.line([(205,y),(1078,y)],MUTED,6);c.poly([(x,y+3),(x-28,y+92),(x+28,y+92)],GOLD,INK,2);c.dot(x,y,7,INK)
    for xx in (358,925):c.line([(xx-157,y-8),(xx+157,y-8)],INK,4)

def weigh(c,detach=0,labels=True,known=False,total=None):
    bench(c)
    for j in range(3):block(c,203+j*80,305,70,57,'7' if known else 'x',BLUE)
    dx=31*detach;dy=111*detach
    block(c,449+dx,318-dy,44,45,'5',GOLD)
    if total is not None:
        block(c,783,303,236,60,total,MINT)
    else:
        if known:
            for i in range(3):block(c,771+i*61,318,55,45,'7',MINT)
        else:block(c,772,318,175,45,'21',MINT)
        block(c,960+dx,318-dy,54,45,'5',GOLD)
    if labels:
        c.text('3x + 5',352,498,36,BLUE,bold=True);c.text('26',914,498,36,MINT,bold=True)

def intro(c,t):
    title(c,'What quantity does x stand for?');bench(c);block(c,298,288,102,74,'x',BLUE);block(c,871,288,102,74,'?',MINT)
    label(c,'Same amount',446,170,37)
    if t>=4.4:label(c,'x = the starting number',180,534,33,BLUE)

def uses(c,t):
    title(c,'Each condition tells you what must balance');label(c,'Tickets sold',143,177,33,BLUE);label(c,'Money received',641,177,33,GOLD)
    for j in range(4):ticket(c,158+j*69,247,False if j%2 else True,1,False)
    if t>=21:
        for j in range(4):c.dot(687+57*j,279,19,GOLD);c.text('$',687+57*j,279,21,BLACK,bold=True)
    if t>=25.4:label(c,'count',157,382,29,BLUE);label(c,'price × count',653,382,29,GOLD)
    if t>=34.8:label(c,'Check both conditions on the same sale.',216,541,34,MINT)

def basic(c,t):
    title(c,'Triple a number, then add five');weigh(c,0,False,total='26' if t>=42.4 else '?')
    label(c,'3x + 5',251,505,39,BLUE)
    if t>=42.4:label(c,'= 26',826,505,40,MINT)
    if t>=46:label(c,'x is the starting number.',321,168,32)

def basic_result(c,t):
    title(c,'Remove five from both sides');p=cue(t,52.73,1.6);weigh(c,p,False,t>=59.6)
    label(c,'3x = 21',200,480,34,BLUE)
    if t>=59.6:label(c,'x = 7',671,480,38,MINT)
    if t>=62:label(c,'Check   3 × 7 + 5 = 26',343,557,30,GOLD)

def point(c,x,y,col,show=True):
    c.dot(x,y,13,col if show else DARK)
    if show:c.poly([(x,y-6),(x+6,y),(x,y+6),(x-6,y)],PAPER,None)

def scores(c,t,p,diff,solved=False):
    start=378;dx=57
    label(c,'First round',116,247,29,BLUE);label(c,'Second round',116,366,29,MINT)
    if not solved:
        block(c,start,210,7*dx-15,61,'x',BLUE);block(c,start,329,7*dx-15,61,'x',MINT)
    else:
        for i in range(7):point(c,start+20+i*dx,242,BLUE);point(c,start+20+i*dx,361,MINT)
    if diff:
        for i in range(4):point(c,start+20+(7+i)*dx,361+p*58,GOLD)

def medium(c,t):
    title(c,'A team earns 18 points across two rounds');scores(c,t,0,t>=69.6)
    if t>=69.6:label(c,'Round 2 has 4 extra.',309,475,32,GOLD)
    if t>=74.8:label(c,'Round 1 = x',306,545,31,BLUE)

def medium_result(c,t):
    title(c,'Remove the four extra points, then share the rest')
    p=cue(t,87.6,1.5)*(1-cue(t,90.5,.88));scores(c,t,p,t>=82.9,t>=89.8)
    if t>=85.4:label(c,'x + (x + 4) = 18',127,462,32)
    if t>=89.8:label(c,'(18 − 4) ÷ 2 = 7',648,462,31,BLUE)
    if t>=91.4:label(c,'First 7, second 11.',333,549,35,MINT)

def ticket(c,x,y,adult,k=1,face=True):
    w=56*k;h=38*k;col=GOLD if adult else BLUE
    c.rect(x+2,y+3,w,h,DARK);c.rect(x,y,w,h,col,BLACK,1.7)
    c.dot(x,y+h/2,4*k,PAPER);c.dot(x+w,y+h/2,4*k,PAPER)
    c.line([(x+w*.74,y+3*k),(x+w*.74,y+h-3*k)],BLACK,1.2)
    if face:c.text('$8' if adult else '$4',x+w*.38,y+h/2,round(17*k),BLACK,bold=True)

def tray(c,adults,flip=0,neutral=False):
    for j in range(24):
        a=j<adults;X=149+(j%6)*79;Y=194+(j//6)*72
        if neutral:
            c.rect(X,Y,56,38,DARK,LINE,2);c.text(str(j+1),X+28,Y+19,17,MUTED,bold=True)
        else:ticket(c,X,Y-(12*sin(pi*flip) if a and j==int(adults)-1 else 0),a,1.02)

def legend(c,y=201):
    ticket(c,746,y,True,1.24);label(c,'Adult · $8',842,y+23,30,GOLD)
    ticket(c,746,y+82,False,1.24);label(c,'Child · $4',842,y+106,30,BLUE)

def challenge(c,t):
    title(c,'24 tickets earn $136. How many are adult tickets?');tray(c,0,neutral=True)
    if t>=97.6:legend(c)
    if t>=102.4:label(c,'Takings  $136',748,415,35,MINT)

def baseline(c,t):
    title(c,'Start with all 24 tickets at the child price')
    tray(c,0,neutral=t<129);label(c,'x adult tickets',702,174,30,GOLD)
    if t>=115.2:label(c,'24 − x child tickets',702,244,30,BLUE)
    if t>=120.6:label(c,'8x + 4(24 − x)',702,320,31)
    if t>=123.6:label(c,'= 136 dollars',701,379,31,MINT)
    if t>=129:label(c,'24 × $4 = $96',148,523,35,BLUE)
    if t>=132.6:label(c,'One upgrade adds $4.',680,523,33,GOLD)

def revenue(c,t):
    title(c,'Upgrade tickets until the extra $40 is accounted for')
    exchange=10*cue(t,136.18,2.95);a=min(10,int(exchange+1e-7));tray(c,a,exchange%1)
    label(c,'Takings',738,178,26,MUTED);label(c,'$'+str(96+4*a),734,246,51,MINT)
    if t>=139.2:label(c,'10 adult + 14 child = 24',683,348,29)
    if t>=142.4:label(c,'10 × $8 = $80',708,416,29,GOLD);label(c,'14 × $4 = $56',708,465,29,BLUE)
    if t>=145.2:label(c,'$80 + $56 = $136',275,546,37,MINT)

def mistakes(c,t):
    title(c,'Ticket counts and dollar amounts use different units');tray(c,10)
    label(c,'Number of tickets',708,200,28,MUTED)
    if t>=153.2:label(c,'10 adults · 14 children',690,257,31)
    if t>=157.2:label(c,'10 + 14 = 24 tickets',690,343,31,BLUE)
    if t>=160:label(c,'8 × 10 + 4 × 14 = $136',687,424,30,GOLD)

def finish(c,t):
    title(c,'Check the unknown against both original totals');tray(c,10);label(c,'x = 10 adult tickets',679,182,32,GOLD)
    if t>=167:label(c,'24 − x = 14 child tickets',677,259,28,BLUE)
    if t>=170:label(c,'Count   10 + 14 = 24',682,351,31)
    if t>=171.6:label(c,'Takings   $80 + $56 = $136',676,432,27,MINT)
    if t>=174:label(c,'Both counts are whole numbers between 0 and 24.',197,549,28,MUTED)
SCENES=(intro,uses,basic,basic_result,medium,medium_result,challenge,baseline,revenue,mistakes,finish)
def verify():
    assert [x for x in range(27) if 3*x+5==26]==[7]
    assert [(x,18-x) for x in range(19) if 18-x==x+4]==[(7,11)]
    assert [(a,24-a) for a in range(25) if 8*a+4*(24-a)==136]==[(10,14)] and 136-24*4==10*4
