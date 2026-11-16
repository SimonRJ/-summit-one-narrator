"""S012: growing readings and routes on the actual broken-rung ladder."""
from math import sin,pi
from visuals import AQUA, BLUE, GOLD, PINK, SOFT, WHITE, VIOLET, ease, mix


def text(a,t,x,y,size=34,col=WHITE,alpha=1):a.label(t,x,y,size,col,alpha,bold=True)

def box(a,t,x,y,col=BLUE,alpha=1,w=110,h=86,size=48):
    a.rounded(x-w/2,y-h/2,w,h,12,col,.18*alpha)
    text(a,t,x,y,size,col,alpha)


def ladder(a,x=300,alpha=1):
    a.path(((x-75,130),(x-75,548)),SOFT,5,alpha)
    a.path(((x+75,130),(x+75,548)),SOFT,5,alpha)
    for n in range(9):
        y=530-n*48
        text(a,str(n),x-125,y,33,SOFT,alpha)
        if n==3:
            a.path(((x-75,y),(x-22,y)),PINK,6,alpha)
            a.path(((x+22,y),(x+75,y)),PINK,6,alpha)
            a.path(((x-14,y-13),(x+14,y+13)),PINK,3,alpha)
            a.path(((x-14,y+13),(x+14,y-13)),PINK,3,alpha)
        else:a.path(((x-75,y),(x+75,y)),BLUE,5,alpha)


def intro(a,c):
    a.heading('The next state follows a rule',BLUE)
    p=c.after('starting state')
    for i,n in enumerate(('5','8','11','14')):
        x=275+i*245;box(a,n,x,300,BLUE,ease(p*2-i*.2))
        if i<3:
            q=ease(p*2-i*.2-.15);a.arrow((x+65,300),(x+180,300),GOLD,q)
            text(a,'+3',x+120,250,27,GOLD,q)
    text(a,'keep the rule with the starting value',640,495,31,SOFT,c.after('what is repeated'))


def exams(a,c):
    a.heading('Repeated moves can branch',AQUA)
    p=c.after('repeated moves')
    a.circle((640,240),23,BLUE,p)
    for dx in (-220,220):a.arrow((640,270),(640+dx,375),AQUA,p)
    for x in (420,860):a.circle((x,400),23,AQUA,p)
    text(a,'change the rule',440,525,29,SOFT,c.after('change a starting rule'))
    text(a,'or block a route',840,525,29,PINK,c.after('block one route'))


def sequence_prompt(a,c):
    a.heading('Start at 5; add 3 each time',BLUE)
    p=c.after('sequence at five')
    box(a,'5',250,320,BLUE,p)
    for i in range(1,4):box(a,'?',250+i*260,320,SOFT,c.after('first four terms'))
    text(a,'The start is term 1',640,520,32,GOLD,c.after('starting value'))


def sequence_answer(a,c):
    a.heading('Count the starting term',BLUE)
    cues=(None,'eight','eleven','fourteen')
    for i,n in enumerate(('5','8','11','14')):
        p=1 if i==0 else c.after(cues[i],.55)
        x=250+i*260;box(a,n,x,320,BLUE,p)
        if i:
            a.arrow((x-185,320),(x-65,320),GOLD,p)
            text(a,'+3',x-125,260,28,GOLD,p)
    text(a,'four terms; three additions',640,520,34,WHITE,c.after('Each difference'))


def display_prompt(a,c):
    a.heading('Twice the reading, minus 1',VIOLET)
    box(a,'3',290,310,VIOLET,c.after('starts at three'),140,105,61)
    a.arrow((390,310),(570,310),AQUA,c.after('twice the last reading'))
    box(a,'?',690,310,SOFT,c.after('four changes'),140,105,61)
    text(a,'4 changes',500,405,29,SOFT,c.after('four changes'))
    text(a,'Watch the distance from 1',640,525,34,GOLD,c.after('distance from one'))


def display_answer(a,c):
    a.heading('The distance from 1 doubles',VIOLET)
    gap=c.after('first gap is two',.7)
    text(a,'change',155,235,27,SOFT,gap);text(a,'reading',155,330,27,VIOLET,gap);text(a,'gap from 1',155,425,26,GOLD,gap)
    p=c.after('four changes',2.5)
    for i,(value,g) in enumerate(zip((3,5,9,17,33),(2,4,8,16,32))):
        x=310+i*190;q=gap if i==0 else ease(p*2-i*.25)
        text(a,str(i),x,235,30,SOFT,q)
        reading=q if i<4 else c.after('thirty-three',.6)
        box(a,str(value),x,330,VIOLET,reading,115,75,43)
        text(a,str(g),x,425,39,GOLD,q)
    text(a,'1 + 2 × 2⁴ = 33',640,540,38,WHITE,c.after('thirty-three'))


def ladder_prompt(a,c):
    a.heading('Can you reach rung 8?',AQUA)
    ladder(a,300,c.opening())
    a.circle((300,530),18,GOLD,c.after('rung zero'))
    p=c.after('one or two rungs')
    a.arrow((425,530),(425,482),BLUE,p)
    a.arrow((485,530),(485,434),AQUA,p)
    text(a,'+1',425,550,25,BLUE,p);text(a,'+2',485,550,25,AQUA,p)
    text(a,'Rung 3 is broken',920,275,36,PINK,c.after('three is broken'))
    text(a,'Never land there',920,345,31,SOFT,c.after('no route can land'))
    text(a,'Finish exactly on 8',920,470,35,WHITE,c.after('rung eight'))


def ladder_table(a,c):
    a.heading('Count ways to reach each rung',AQUA)
    text(a,'rung',120,270,27,SOFT);text(a,'ways',120,390,27,SOFT)
    initial=c.after('one way',.6);broken=c.after('zero ways',.6);fill=c.after('Fill the table',1.8)
    counts=(1,1,2,0,2,2,4,6,10)
    for i,n in enumerate(counts):
        x=220+i*115
        text(a,str(i),x,270,34,PINK if i==3 else SOFT)
        q=initial if i==0 else broken if i==3 else c.after('sum is ten',.55) if i==8 else ease(fill*2-i*.13)
        box(a,str(n),x,390,PINK if i==3 else BLUE,q,90,75,39)
    text(a,'4 + 6 = 10',640,535,42,WHITE,c.after('sum is ten'))


def ladder_jump(a,c):
    a.heading('A jump can pass a broken rung',AQUA)
    ladder(a,300,c.opening())
    q=c.after('jump of two can go over it',2)
    if q>0:
        points=[(300+115*sin(pi*q*i/20),mix(434,338,q*i/20)) for i in range(21)]
        a.path(points,GOLD,3,.7)
    x=300+115*sin(pi*q);y=mix(434,338,q)
    a.circle((x,y),17,GOLD,c.opening())
    text(a,'2 → 4',855,280,55,GOLD,q)
    text(a,'Rung 3 is never landed on',855,385,32,PINK,c.after('stops landings'))
    text(a,'The last jump is either +1 or +2',855,510,30,SOFT,c.after('last-jump cases'))


def mistakes(a,c):
    a.heading('The empty route counts once',GOLD)
    p=c.after('one at the starting state')
    box(a,'0',310,280,SOFT,p);text(a,'1 way to start',660,280,40,WHITE,p)
    q=c.after('broken rung removes',.7)
    box(a,'3',310,425,PINK,q);text(a,'0 ways to land there',660,425,36,PINK,q)
    text(a,'A two-step jump may pass it',640,545,31,AQUA,c.after('jumps over it'))


def recap(a,c):
    a.heading('Start, apply the rule, check',BLUE)
    p=c.after('starting values')
    text(a,'ways(0) = 1',640,230,38,WHITE,p)
    text(a,'ways(3) = 0',640,310,38,PINK,c.after('exceptional states'))
    text(a,'ways(8) = ways(7) + ways(6)',640,410,37,WHITE,c.after('recurrence'))
    text(a,'6 + 4 = 10',640,510,44,AQUA,c.after('last-step cases'))


SCENES=(intro,exams,sequence_prompt,sequence_answer,display_prompt,display_answer,
        ladder_prompt,ladder_table,ladder_jump,mistakes,recap)
def draw(a,c,scene):SCENES[scene-1](a,c)
