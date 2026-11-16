"""S013: shared schedules, exactly filled packs and coprime factor pairs."""
from visuals import AQUA, BLUE, GOLD, PINK, SOFT, WHITE, VIOLET, ease

RED='#ff7777'

def text(a,t,x,y,size=34,col=WHITE,alpha=1):a.label(t,x,y,size,col,alpha,bold=True)


def schedules(a,p6=1,p12=1,p18a=1,p9=1,p18b=1,mark=0,moving=False):
    def X(t):return 210+51*t
    for y,col,period in ((265,BLUE,'6 min'),(430,GOLD,'9 min')):
        text(a,period,100,y,30,col)
        a.path(((X(0),y),(X(18),y)),SOFT,3)
        for t in range(19):a.path(((X(t),y-5),(X(t),y+5)),SOFT,2,.6)
        a.circle((X(0),y),12,col)
        text(a,'0',X(0),y+42,25,SOFT)
    for t,p in ((6,p6),(12,p12),(18,p18a)):
        a.circle((X(t),265),15,BLUE,p);text(a,str(t),X(t),220,30,BLUE,p)
    for t,p in ((9,p9),(18,p18b)):
        a.circle((X(t),430),15,GOLD,p);text(a,str(t),X(t),475,30,GOLD,p)
    if moving:
        a.circle((X(6*p6+6*p12+6*p18a),265),8,WHITE)
        a.circle((X(9*p9+9*p18b),430),8,WHITE)
    a.path(((X(18),285),(X(18),410)),AQUA,5,mark)
    text(a,'first match: 18 min',640,555,36,WHITE,mark)


def intro(a,c):
    a.heading('What must divide what?',BLUE)
    p=c.after('equal grouping')
    for i in range(4):
        x=300+i*110
        a.rounded(x-40,250,80,80,9,BLUE,.18*p)
        for j in range(2):a.circle((x-17+j*34,290),10,BLUE,p)
    text(a,'equal groups',465,385,30,BLUE,p)
    q=c.after('meeting schedules')
    for i in range(4):a.circle((760+i*95,300),12,GOLD,ease(q*2-i*.2))
    text(a,'repeat together',900,385,30,GOLD,q)
    text(a,'common factor',465,505,32,SOFT,p)
    text(a,'common multiple',900,505,32,SOFT,q)


def exams(a,c):
    a.heading('The question tells you the job',AQUA)
    p=c.after('identical packs')
    text(a,'packs',380,270,43,BLUE,p)
    text(a,'must divide both totals',380,355,29,SOFT,p)
    q=c.after('repeating events')
    text(a,'meeting time',900,270,43,GOLD,q)
    text(a,'must be a multiple of both periods',900,355,26,SOFT,q)
    text(a,'HCF and LCM can also reveal a pair',640,520,32,WHITE,c.after('original pair'))


def timing_prompt(a,c):
    a.heading('When do they restart together?',GOLD)
    schedules(a,0,0,0,0,0,0)
    text(a,'both start at 0',640,555,31,SOFT,c.after('time zero'))


def timing_answer(a,c):
    a.heading('Follow both schedules',GOLD)
    p6=c.after('six twelve',.6);p12=c.after('twelve and eighteen',.6)
    p18a=c.after('eighteen The second',.6);p9=c.after('second goes nine',.6)
    p18b=c.says('nine and eighteen');mark=c.after('first match',.9)
    schedules(a,p6,p12,p18a,p9,p18b,mark,moving=True)


def packs_prompt(a,c):
    a.heading('Make identical packs',BLUE)
    red=c.after('twenty-four red',.7);blue=c.after('thirty-six blue',.7)
    text(a,'24 red',390,215,39,RED,red);text(a,'36 blue',890,215,39,BLUE,blue)
    for i in range(24):a.circle((265+(i%6)*50,285+(i//6)*52),13,RED,ease(red*2-i*.035))
    for i in range(36):a.circle((765+(i%6)*50,270+(i//6)*43),13,BLUE,ease(blue*2-i*.025))
    text(a,'How many identical packs?',640,555,32,WHITE,c.after('many identical packs'))


def packs_answer(a,c):
    a.heading('Twelve packs, nothing left over',BLUE)
    text(a,'36 − 24 = 12',640,180,36,WHITE,c.after('difference'))
    p=c.after('Make twelve packs',1.6)
    for i in range(12):
        x=180+(i%6)*185;y=290+(i//6)*160
        q=ease(p*2-i*.07)
        a.rounded(x-75,y-56,150,112,9,SOFT,.13*q)
        for dx in (-20,20):a.circle((x+dx,y-23+30*(1-q)),12,RED,q)
        for dx in (-38,0,38):a.circle((x+dx,y+24+30*(1-q)),12,BLUE,q)
    text(a,'2 red + 3 blue in each pack',640,550,31,WHITE,c.after('two reds'))


def pair_prompt(a,c):
    a.heading('Find the closest original pair',VIOLET)
    text(a,'HCF = 6',390,260,48,BLUE,c.after('factor six'))
    text(a,'LCM = 180',890,260,48,GOLD,c.after('one hundred and eighty'))
    text(a,'smallest possible difference',640,420,36,WHITE,c.after('difference is as small'))
    text(a,'divide both numbers by 6 first',640,530,32,SOFT,c.after('dividing each number'))


def pair_answer(a,c):
    a.heading('Remove the common factor',VIOLET)
    text(a,'scaled numbers are coprime',640,180,31,SOFT,c.after('coprime'))
    text(a,'their product is 30',640,235,38,WHITE,c.after('multiply to thirty'))
    p=c.after('List the factor pairs',1.0)
    for i,(left,right,diff) in enumerate(((1,30,29),(2,15,13),(3,10,7),(5,6,1))):
        y=315+i*67;q=ease(p*2-i*.15)
        text(a,f'{left} × {right} = 30',420,y,34,BLUE,q)
        text(a,f'gap {diff}',840,y,31,GOLD,q)
    q=c.after('five and six',.7)
    a.path(((260,547),(990,547)),AQUA,4,q)
    text(a,'closest: 5 and 6',640,585,30,AQUA,q)


def pair_check(a,c):
    a.heading('Scale back and verify',VIOLET)
    p=c.after('Scale by six',.8)
    text(a,'5 × 6 = 30',390,250,42,BLUE,p)
    text(a,'6 × 6 = 36',890,250,42,GOLD,p)
    text(a,'gap = 6',640,355,42,WHITE,c.after('gap is six'))
    text(a,'HCF(30, 36) = 6',640,455,35,BLUE,c.after('common factor is six'))
    text(a,'LCM(30, 36) = 180',640,535,35,GOLD,c.after('one hundred and eighty'))


def mistakes(a,c):
    a.heading('Check the direction',PINK)
    p=c.after('packing problem divides')
    text(a,'packs divide the totals',640,250,38,BLUE,p)
    text(a,'periods divide the repeat time',640,345,38,GOLD,c.after('repeat time'))
    text(a,'scaled pair must be coprime',640,455,36,AQUA,c.after('coprime'))
    text(a,'a shared prime changes the HCF',640,535,29,SOFT,c.after('shared prime'))


def recap(a,c):
    a.heading('Group, meet, or find a pair',AQUA)
    text(a,'24 and 36 → 12 equal packs',640,240,36,BLUE,c.after('factor or multiple'))
    text(a,'6 and 9 → meet after 18 minutes',640,335,36,GOLD,c.after('factor or multiple'))
    text(a,'HCF 6 and LCM 180 → 30 and 36',640,440,35,AQUA,c.after('unknown pair'))
    text(a,'verify both clues',640,535,32,SOFT,c.after('verify both conditions'))


SCENES=(intro,exams,timing_prompt,timing_answer,packs_prompt,packs_answer,
        pair_prompt,pair_answer,pair_check,mistakes,recap)
def draw(a,c,scene):SCENES[scene-1](a,c)
