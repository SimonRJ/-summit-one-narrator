"""S015: group actual counters, test digit endings and shift a bounded search."""
from visuals import AQUA, BLUE, GOLD, PINK, SOFT, WHITE, VIOLET, ease, mix


def text(a,t,x,y,size=34,col=WHITE,alpha=1):a.label(t,x,y,size,col,alpha,bold=True)


def group_position(g):return (220+(g%4)*270,255+(g//4)*165)


def counters(a,alpha=1):
    for g in range(7):
        x,y=group_position(g)
        for k in range(5):a.circle((x-52+k*26,y),9,BLUE,alpha)
    a.circle((1020,420),11,PINK,alpha);a.circle((1060,420),11,PINK,alpha)


def intro(a,c):
    a.heading('One step to the next multiple',BLUE)
    for i,n in enumerate((8,9,10,11,12)):
        x=240+i*200
        a.circle((x,350),8,BLUE,c.opening())
        text(a,str(n),x,410,38,GOLD if n in (8,12) else SOFT,c.opening())
    a.path(((240,350),(1040,350)),SOFT,3,c.opening())
    text(a,'11 leaves remainder 3 on division by 4',640,225,33,WHITE,c.after('one below the divisor'))
    p=c.after('one step before',1.5)
    a.arrow((840,315),(1040,315),AQUA,p)
    text(a,'+1',940,255,31,AQUA,p)
    text(a,'12 is a multiple of 4',640,525,34,WHITE,c.after('common multiples problem'))


def exams(a,c):
    a.heading('Almost full groups can simplify a search',AQUA)
    p=c.after('one short of a multiple')
    text(a,'one short',440,290,42,GOLD,p)
    a.arrow((580,290),(720,290),AQUA,p)
    text(a,'add 1',870,290,42,AQUA,p)
    text(a,'remember the interval',640,485,32,SOFT,c.after('use the interval'))


def packet_prompt(a,c):
    a.heading('37 counters into packets of 5',GOLD)
    counters(a,c.after('thirty-seven counters',.8))
    text(a,'How many are left over?',640,545,36,WHITE,c.after('remain outside'))


def packet_answer(a,c):
    a.heading('Seven full packets and a remainder',GOLD)
    counters(a,c.opening())
    p=c.after('seven packets',2)
    for g in range(7):
        x,y=group_position(g);q=ease(p*2-g*.15)
        a.trace(((x-73,y-28),(x+73,y-28),(x+73,y+28),(x-73,y+28),(x-73,y-28)),q,GOLD,4,False)
    text(a,'7 × 5 = 35',640,120,32,SOFT,c.after('thirty-five'))
    text(a,'37 − 35 = 2',640,545,39,WHITE,c.after('get two'))


def digit_prompt(a,c):
    a.heading('Choose the final digit',VIOLET)
    text(a,'34?',640,290,105,WHITE,c.after('three-digit number'))
    text(a,'divisible by 4 and by 3',640,455,40,SOFT,c.after('four and three'))
    text(a,'last two digits • digit sum',640,535,30,AQUA,c.after('last two digits'))


def digit_answer(a,c):
    a.heading('Test both conditions',VIOLET)
    cues=('forty forty-four','forty-four and forty-eight','forty-eight')
    sums=('7','11','15')
    for i,n in enumerate(('340','344','348')):
        x=320+i*320;p=c.after(cues[i],.7)
        a.rounded(x-115,210,230,110,14,BLUE,.17*p)
        text(a,n,x,265,56,WHITE,p)
        q=c.after('fixed digits sum to seven')
        text(a,'digit sum '+sums[i],x,395,31,SOFT,q*p)
        reject=c.after('only eight',.7)
        if i<2:
            a.path(((x-48,460),(x+48,525)),PINK,4,reject)
            a.path(((x-48,525),(x+48,460)),PINK,4,reject)
        else:text(a,'✓',x,490,58,AQUA,reject)
    text(a,'348 passes both tests',640,565,35,WHITE,c.after('three hundred and forty-eight'))


def bounds_prompt(a,c):
    a.heading('Two remainders, one interval',AQUA)
    text(a,'56 ≤ N ≤ 211',640,245,50,WHITE,c.after('fifty-six'))
    text(a,'N leaves 3 when divided by 4',640,355,34,BLUE,c.after('remainder is three'))
    text(a,'N leaves 5 when divided by 6',640,440,34,GOLD,c.after('remainder five'))
    text(a,'What changes if N becomes N + 1?',640,535,33,AQUA,c.after('add one'))


def multiples_line(a,p_first=1,p_last=1,fill=1):
    def X(n):return 160+(n-57)*(960/155)
    y=390;a.path(((X(57),y),(X(212),y)),SOFT,4)
    text(a,'57',X(57),465,29,SOFT);text(a,'212',X(212),465,29,SOFT)
    for i,n in enumerate(range(60,205,12)):
        p=p_first if i==0 else p_last if i==12 else ease(fill*2-i*.08)
        a.circle((X(n),y),11,AQUA,p)
    text(a,'60',X(60),320,31,AQUA,p_first)
    text(a,'204',X(204),320,31,AQUA,p_last)


def bounds_answer(a,c):
    a.heading('Add 1 to both the number and bounds',AQUA)
    text(a,'N + 1 is a multiple of 12',640,205,38,WHITE,c.after('multiple is twelve'))
    text(a,'57 ≤ N + 1 ≤ 212',640,275,33,SOFT,c.after('shifted interval'))
    first=c.after('start at sixty',.7);last=c.after('two hundred and four',.7);fill=c.after('Step by twelve',1.5)
    multiples_line(a,first,last,fill)
    text(a,'12 apart',640,545,31,GOLD,fill)


def count_answer(a,c):
    a.heading('Count numbers, not just gaps',AQUA)
    multiples_line(a)
    p=c.after('twelve steps')
    text(a,'12 gaps',455,220,40,WHITE,p)
    q=c.after('thirteen numbers',.7)
    a.arrow((570,220),(700,220),AQUA,q)
    text(a,'13 multiples',850,220,40,WHITE,q)
    text(a,'subtract 1 from each',640,525,31,SOFT,c.after('Subtract one'))
    text(a,'first N = 59',640,575,31,GOLD,c.after('fifty-nine'))


def mistakes(a,c):
    a.heading('Keep the remainder and bounds valid',PINK)
    text(a,'0 ≤ remainder < divisor',640,240,45,WHITE,c.after('smaller than the divisor'))
    text(a,'56 ≤ N ≤ 211',410,385,34,BLUE,c.after('bounded search'))
    text(a,'+1',640,385,38,AQUA,c.after('shift the endpoints'))
    text(a,'57 ≤ N + 1 ≤ 212',930,385,34,GOLD,c.after('shift the endpoints'))
    text(a,'shift answers back afterwards',640,525,31,SOFT,c.after('Pull each answer back'))


def recap(a,c):
    a.heading('Shift, count, then check',BLUE)
    text(a,'N + 1: 60, 72, …, 204',640,240,39,AQUA,c.after('a multiple'))
    text(a,'N: 59, 71, …, 203',640,335,39,BLUE,c.after('first and last values'))
    text(a,'13 numbers',640,445,44,WHITE,c.after('include the first'))
    text(a,'both remainder conditions hold',640,530,30,SOFT,c.after('every condition'))


SCENES=(intro,exams,packet_prompt,packet_answer,digit_prompt,digit_answer,
        bounds_prompt,bounds_answer,count_answer,mistakes,recap)
def draw(a,c,scene):SCENES[scene-1](a,c)
