"""S086. Follow a single batch and a graduated tank through the leak opening."""
from fractions import Fraction
from pumps_and_packing import carton
from captioned_film import mix
PAPER='#152d39'
INK='#fff2de'; AQUA='#8de4dd'; WATER='#327fa1'; GOLD='#ffca70'; RED='#ffa68f'; LINE='#7894a0'; EMPTY='#213d4b'

def heading(c,text):
    c.text(text,55,57,40,INK,'lm',True)
    c.line([(54,105),(1220,105)],LINE,2)

def note(c,text,y,col=INK,size=32):
    c.text(text,944,y,size,col,bold=True)

def tank(c,volume,leak=False,active=0):
    x,y,w,h=160,167,416,312
    unit=h/24
    c.rect(x,y,w,h,EMPTY,None)
    if volume>0:
        c.rect(x+3,y+h-unit*volume,w-6,unit*volume,WATER,None)
        c.line([(x+3,y+h-unit*volume),(x+w-3,y+h-unit*volume)],AQUA,3)
    for n in range(25):
        yy=y+h-n*unit
        c.line([(x-12,yy),(x+(21 if n%3==0 else 8),yy)],LINE,2)
        if n in (0,3,9,15,24):
            c.text(str(n),x-28,yy,25,INK,'rm',True)
    c.line([(x,y),(x,y+h),(x+w,y+h),(x+w,y)],INK,4)
    if leak or active:
        for i,(xx,col) in enumerate(((x+94,AQUA),(x+w-99,GOLD))):
            c.line([(xx-46,y-28),(xx,y-28),(xx,y-1)],col,8)
            if active>i and volume<24:c.line([(xx,y),(xx,y+h-volume*unit)],col,4)
    if leak:
        cy=y+h-18
        c.line([(x+w,cy),(x+w+45,cy),(x+w+45,cy+38)],RED,5)
        c.dot(x+w+18,cy,9,RED)
        if active and volume<24:
            c.line([(x+w+45,cy+39),(x+w+45,cy+72)],RED,4)
            c.poly([(x+w+36,cy+64),(x+w+54,cy+64),(x+w+45,cy+81)],RED,None)
    c.text('Tank volume (units)',x+w/2,537,29,INK,bold=True)

def batch(c,n,stamped):
    # All cartons represent equal portions of one batch.
    for i in range(n):
        carton(c,98+(i%4)*141,227+(i//4)*140,78,max(0,min(1,stamped-i)))

def strips(c,filled_a,filled_b,legend):
    left,top=105,244
    c.text('One batch = 24 equal units',left,174,31,INK,'lm',True)
    for i in range(24):
        x=left+(i%8)*69;y=top+(i//8)*69
        c.rect(x,y,58,58,EMPTY,LINE,2)
        if i<filled_a:
            c.rect(x+2,y+2,54*min(1,filled_a-i),54,AQUA)
        if 23-i<filled_b:
            w=54*min(1,filled_b-(23-i));c.rect(x+56-w,y+2,w,54,GOLD)
    if legend:c.text('Machine A',192,500,26,AQUA,bold=True);c.text('Machine B',528,500,26,GOLD,bold=True)

def quantity(m):
    return min(24,5*min(m,3)+4*max(m-3,0))

def clock(c,m,show_finish=True):
    left,y,scale=720,451,88
    c.line([(left,y),(left+5.25*scale,y)],LINE,3)
    for t,s in ((0,'0'),(3,'3'),(5.25,'5¼')):
        x=left+t*scale
        c.line([(x,y-13),(x,y+10)],INK,3)
        if t<5.25 or show_finish:c.text(s,x,y+39,27,INK,bold=True)
    c.line([(left,y),(left+min(m,3)*scale,y)],AQUA,7)
    if m>3:c.line([(left+3*scale,y),(left+m*scale,y)],RED,7)
    c.dot(left+m*scale,y,8,INK)
    c.text('Minutes from the start',948,y+83,27,INK,bold=True)

def idea(c,q):
    heading(c,'What changes in a single minute?')
    p=q.after('water rises three marks',1.45)
    tank(c,3*p,active=1 if 0<p<1 else 0)
    if q.after('one minute on the clock'):note(c,'1 minute',204,GOLD)
    if p:note(c,'3 units out of 24',300,AQUA)
    if q.after('A work rate'):note(c,'3/24 = 1/8 tank per minute',413,INK,26)

def uses(c,q):
    heading(c,'Find the rate and mark any change')
    if not q.after('In a Rossmoyne-style problem'):
        strips(c,3*q.after('one minute'),0,False);note(c,'How much in one minute?',300)
    else:
        tank(c,15,True);clock(c,3,False);note(c,'Leak begins at minute 3',271,RED)

def easy(c,q):
    heading(c,'Label one batch of boxes in eight minutes')
    batch(c,8,q.after('one minute'))
    note(c,'8 equal portions',271,AQUA)
    if q.after('What fraction'):note(c,'What fraction in 1 minute?',376)

def solve_easy(c,q):
    heading(c,'Each minute labels one eighth of the batch')
    p=q.after('Multiply this fraction',2.5)
    batch(c,8,1+7*p)
    note(c,'1 minute → 1/8 batch',252,AQUA)
    if p:note(c,'8 × 1/8 = 1 batch',374,GOLD)

def medium(c,q):
    heading(c,'Two machines work on the same batch')
    strips(c,0,0,True)
    note(c,'A: 1 batch in 8 minutes',223,AQUA)
    if q.after('Machine B'):note(c,'B: 1 batch in 12 minutes',326,GOLD)
    if q.after('How long'):note(c,'How long together?',434)

def combined(c,q):
    heading(c,'Count what both machines do in the same minute')
    a=3*q.after('three units per minute');b=2*q.after('B completes two')
    # The colours meet only at completion, with continuously divisible work.
    elapsed=1+3.8*q.after('The time is twenty-four divided',2.4)
    strips(c,a*elapsed,b*elapsed,True)
    if q.after('combined rate'):note(c,'3 + 2 = 5 units/min',220,AQUA)
    if q.after('time is twenty-four'):note(c,'24 units ÷ 5 units/min',326)
    if q.after('over five minutes'):note(c,'24/5 minutes',426,GOLD,40)

def hard(c,q):
    heading(c,'Two pumps fill a tank. Then a leak opens.')
    p=q.after('After three minutes',2.1)
    tank(c,15*p,p>=1,active=2)
    note(c,'A: full tank in 8 min',205,AQUA)
    if q.after('other twelve'):note(c,'B: full tank in 12 min',274,GOLD)
    if q.after('empty a full tank'):note(c,'Leak: full tank in 24 min',347,RED,29)
    if p:clock(c,3*p,False)

def solve_hard(c,q):
    heading(c,'Split the timeline where the leak opens')
    a=q.after('initially fill five units',2.4)
    b=q.after('Divide the remaining work',2.3)
    minute=3*a+2.25*b
    leak=bool(q.after('leak removes one unit'))
    tank(c,quantity(minute),leak,active=2);clock(c,minute,bool(b))
    if q.after('fifteen before'):note(c,'3 × 5 = 15 units',176,AQUA)
    if q.after('leaves nine'):note(c,'24 − 15 = 9 left',237)
    if leak:note(c,'3 + 2 − 1 = 4 units/min',300,RED,28)
    if b:note(c,'3 + 9/4 = 21/4 min',370,GOLD)

def check(c,q):
    heading(c,'Account for the last quarter of a minute')
    p=q.after('Two minutes at the new rate',1.9)
    f=q.after('One last quarter',1.05)
    minute=3+2*p+.25*f
    tank(c,quantity(minute),True,active=2);clock(c,minute)
    note(c,'At 3 min: 15 units',192,AQUA)
    if p:note(c,'At 5 min: 15 + 8 = 23',272,GOLD)
    if f:note(c,'At 5¼ min: 23 + 1 = 24',349,INK,28)

def mistakes(c,q):
    heading(c,'Check the answer against the story')
    if not q.after('For the tank'):
        strips(c,3,2,True);note(c,'8 + 12 = 20 minutes?',215,RED)
        if q.after('faster machine'):note(c,'Together must beat 8 minutes.',347,AQUA,26)
    else:
        tank(c,15,False,active=0);clock(c,3,False);note(c,'First 3 min: drain closed',244,AQUA)

def recap(c,q):
    heading(c,'Keep the work already done')
    p=q.after('amount already finished',1.15)
    f=q.after('divide the work left',1.25)
    minute=3*p+2.25*f;tank(c,quantity(minute),bool(f),active=2)
    clock(c,minute)
    note(c,'Full tank = 24 units',188,AQUA)
    if p:note(c,'Carry forward 15 units',275)
    if f:note(c,'Last section: 9 ÷ 4 min',354,GOLD,30)

SCENES=(idea,uses,easy,solve_easy,medium,combined,hard,solve_hard,check,mistakes,recap)
def verify():
    a,b,drain=Fraction(1,8),Fraction(1,12),Fraction(1,24)
    assert 1/(a+b)==Fraction(24,5)
    assert (1-3*(a+b))/(a+b-drain)==Fraction(9,4)
    assert quantity(3)==15 and quantity(5)==23 and quantity(Fraction(21,4))==24
