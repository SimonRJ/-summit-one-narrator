"""S020: the actual clock turns and units-digit cycles in the narration."""
from math import cos, pi, sin
from visuals import AQUA, BLUE, GOLD, PINK, SOFT, WHITE, VIOLET, clamp


def label(a,s,x,y,size=32,colour=WHITE,alpha=1,align='center'):
    a.label(s,x,y,size,colour,alpha,align=align,bold=True)


def title(a,s):
    a.label(s,640,70,42,WHITE,bold=True,display=True)


def clock(a,cx,cy,r,hour=9,arc=0):
    points=[(cx+r*cos(2*pi*i/120),cy+r*sin(2*pi*i/120)) for i in range(121)]
    a.path(points,SOFT,3,.85)
    for n in range(1,13):
        angle=-pi/2+2*pi*n/12
        x=cx+(r-43)*cos(angle);y=cy+(r-43)*sin(angle)
        label(a,str(n),x,y,30,AQUA if n==9 else WHITE)
    if arc>0:
        # Draw the traversed arc clockwise from 9, with angular distance in hours.
        steps=max(2,round(arc*6));pts=[]
        for i in range(steps+1):
            angle=-pi/2+2*pi*(9+arc*i/steps)/12
            pts.append((cx+(r+12)*cos(angle),cy+(r+12)*sin(angle)))
        a.path(pts,GOLD,5,.8)
    angle=-pi/2+2*pi*hour/12
    a.path(((cx,cy),(cx+.63*r*cos(angle),cy+.63*r*sin(angle))),AQUA,9)
    a.circle((cx,cy),12,WHITE)


def four(a,x,y,u,p=1,highlight=0):
    for i,(n,col) in enumerate(zip((3,9,7,1),(BLUE,GOLD,VIOLET,AQUA)),1):
        alpha=p[i-1] if isinstance(p,(list,tuple)) else clamp(p*4-(i-1))
        a.rounded(x+(i-1)*u,y, u-13,90,14,col,.27*alpha)
        label(a,str(n),x+(i-1)*u+(u-13)/2,y+45,48,col,alpha)
        label(a,str(i),x+(i-1)*u+(u-13)/2,y+115,23,SOFT,alpha)
        if highlight==i:
            x0=x+(i-1)*u
            a.path(((x0,y),(x0+u-13,y),(x0+u-13,y+90),(x0,y+90),(x0,y)),WHITE,5,alpha)


def cycles(a,c):
    title(a,'A cycle returns to the same states')
    p=c.opening(2.0)
    four(a,305,220,170,p)
    q=c.after('full cycle',1.2)
    a.arrow((894,350),(894,430),AQUA,q);a.arrow((894,430),(384,430),AQUA,q)
    a.arrow((384,430),(384,350),AQUA,q)
    # A travelling marker makes the order and wraparound visible.
    if c.local>=2:
        phase=(c.local-2)%8
        if phase<3:x,y=384+170*phase,190
        elif phase<4:x,y=894,190+240*(phase-3)
        elif phase<7:x,y=894-170*(phase-4),430
        else:x,y=384,430-240*(phase-7)
        a.circle((x,y),9,AQUA)
    label(a,'3 × 3 → 9',640,505,34,WHITE,c.after('multiply last digits'))


def uses(a,c):
    title(a,'Where do repeating cycles appear?')
    p=c.after('repeating picture')
    for i,col in enumerate((BLUE,GOLD,VIOLET,BLUE,GOLD,VIOLET)):
        a.circle((110+i*45,325),14,col,p)
    q=c.after('clock')
    if q>0:clock(a,640,340,128,9)
    label(a,'CLOCK',640,515,26,SOFT,q)
    r=c.after('last digit')
    label(a,'3 × 3 × 3',1030,300,33,WHITE,r)
    label(a,'last digits: 3, 9, 7',1030,375,29,AQUA,r)
    label(a,'base 3: length 4   •   base 5: length 1',640,565,29,SOFT,c.after('cycle length stays the same'))


def clock_question(a,c):
    title(a,'Nine o’clock + 17 hours')
    clock(a,430,350,190,9)
    label(a,'START',430,580,29,AQUA)
    label(a,'17 hours later?',920,290,40,WHITE,c.after('seventeen hours'))
    label(a,'What can a full turn remove?',920,400,28,SOFT,c.after('whole turns'))


def clock_answer(a,c):
    title(a,'A full turn, then five more hours')
    full=c.after('twelve hours',2.8);extra=c.after('Step five hours ahead',2.1)
    travel=12*full+5*extra
    clock(a,430,350,190,9+travel,min(12,travel))
    label(a,'12 hours → back to 9',930,240,34,AQUA,c.after('returns to the starting'))
    label(a,'17 = 12 + 5',930,330,38,WHITE,c.after('five extra hours'))
    label(a,'9 + 5 hours → 2',930,440,38,GOLD,c.after('hour hand points to two'))


def power_question(a,c):
    title(a,'What is the units digit of 3^37?')
    label(a,'Start with small powers',640,205,31,SOFT,c.after('first few powers'))
    p=c.after('first few powers',2)
    four(a,305,270,170,p)
    label(a,'Repeat?',640,505,34,AQUA,c.after('first repeat'))


def power_answer(a,c):
    title(a,'Four last digits repeat')
    p=[c.after(word,.4) for word in ('three','nine','seven','one')]
    pos=c.after('position one');zero=c.after('remainder is zero')
    four(a,305,200,170,p,4 if zero>0 else 1 if pos>0 else 0)
    label(a,'37 = 9 × 4 + 1',640,425,40,WHITE,c.after('remainder of one'))
    label(a,'Position 1 → 3',640,490,39,AQUA,c.after('position one'))
    label(a,'Remainder 0 → position 4',640,555,28,GOLD,c.after('remainder is zero'))


def sum_question(a,c):
    title(a,'What is the units digit of this sum?')
    label(a,'3^1 + 3^2 + 3^3 + … + 3^51',640,230,43,WHITE,c.opening())
    label(a,'Group the last digits in blocks of four',640,345,31,SOFT,c.after('cycle of the last digits'))
    four(a,305,390,170,c.after('one whole block',1.2))


def sum_answer(a,c):
    title(a,'Twelve full cycles and three terms')
    label(a,'3',405,180,35,BLUE,c.after('three'))
    label(a,'+ 9',500,180,35,GOLD,c.after('nine'))
    label(a,'+ 7',595,180,35,VIOLET,c.after('seven'))
    label(a,'+ 1',690,180,35,AQUA,c.says('and one'))
    label(a,'= 20',825,180,35,WHITE,c.after('Their sum is twenty'))
    p=c.after('twelve full cycles',2)
    # Twelve separate packs, each representing the four-digit cycle.
    for i in range(12):
        row,col=divmod(i,4);x=130+col*155;y=245+row*92
        opacity=clamp(p*12-i)
        a.rounded(x,y,133,65,10,AQUA,.16*opacity)
        for j,ink in enumerate((BLUE,GOLD,VIOLET,AQUA)):
            a.circle((x+25+j*27,y+32),8,ink,opacity)
    label(a,'12 complete blocks',429,545,27,SOFT,p)
    q=c.after('three terms left')
    label(a,'Tail:',990,260,29,SOFT,q)
    label(a,'3 + 9 + 7',990,325,37,WHITE,c.after('first three digits'))
    label(a,'= 19',990,375,37,WHITE,c.after('Their sum is nineteen'))
    label(a,'Units digit: 9',990,450,38,GOLD,c.after('final units digit is nine'))


def why_sum(a,c):
    title(a,'Why can we use only last digits?')
    p=c.after('units digits of the addends')
    label(a,'Sum of the units digits',640,205,29,SOFT,p)
    label(a,'12 × 20 + 19 = 259',640,315,43,WHITE,p)
    label(a,'Full cycles contribute 240',640,405,31,AQUA,c.after('full cycle'))
    label(a,'Units digit: 9',640,500,43,GOLD,c.after('answer is nine'))
    label(a,'The next cycle starts after exponent 48',640,565,27,SOFT,c.after('multiple of four'))


def mistakes(a,c):
    title(a,'Two common cycle mistakes')
    p=c.after('multiple of the cycle length')
    label(a,'Remainder 0 → last position',640,205,38,WHITE,p)
    label(a,'4th units digit = 1',640,270,33,AQUA,c.after('last listed item'))
    q=c.after('For a sum')
    label(a,'A sum is not just the final term',640,395,36,WHITE,q)
    label(a,'3 + 9 + 7 + 1 = 20 → units 0',640,470,33,GOLD,c.after('earlier terms'))


def recap(a,c):
    title(a,'Find the cycle. Count the steps.')
    p=c.after('Record states');q=c.after('count the length');r=c.after('use the remainder');s=c.after('for a sum')
    label(a,'1',235,230,42,BLUE,p);label(a,'Write the states in order',320,230,34,WHITE,p,'left')
    label(a,'2',235,325,42,GOLD,q);label(a,'Count one complete cycle',320,325,34,WHITE,q,'left')
    label(a,'3',235,420,42,VIOLET,r);label(a,'Use the remainder',320,420,34,WHITE,r,'left')
    label(a,'4',235,515,42,AQUA,s);label(a,'For a sum, count full blocks too',320,515,34,WHITE,s,'left')


SCENES=(cycles,uses,clock_question,clock_answer,power_question,power_answer,sum_question,sum_answer,why_sum,mistakes,recap)
def draw(a,c,scene):SCENES[scene-1](a,c)
