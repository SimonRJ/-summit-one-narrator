"""S001: actual shapes, place-value remainders and three compatible conditions."""
import math

from visuals import AQUA, BLUE, GOLD, PINK, SOFT, VIOLET, WHITE, ease


INKS=(GOLD,BLUE,AQUA,VIOLET,PINK,'#b9da97')
NAMES=('triangle','square','circle','star','diamond','hexagon')


def label(a,value,x,y,size=34,colour=WHITE,alpha=1):
    a.label(value,x,y,size,colour,alpha,bold=True)


def glyph(a, kind, x, y, r, colour, progress=1, highlight=False):
    if progress<=0: return
    if kind==2:
        points=[(x+r*math.cos(2*math.pi*i/64),y+r*math.sin(2*math.pi*i/64)) for i in range(65)]
    elif kind==0:
        points=[(x+r*math.cos(-math.pi/2+2*math.pi*i/3),y+r*math.sin(-math.pi/2+2*math.pi*i/3)) for i in range(3)]
        points.append(points[0])
    elif kind==1:
        z=r*.78
        points=[(x-z,y-z),(x+z,y-z),(x+z,y+z),(x-z,y+z),(x-z,y-z)]
    elif kind==3:
        points=[]
        for i in range(10):
            radius=r if i%2==0 else r*.43
            angle=-math.pi/2+i*math.pi/5
            points.append((x+radius*math.cos(angle),y+radius*math.sin(angle)))
        points.append(points[0])
    elif kind==4:
        points=[(x,y-r),(x+r*.72,y),(x,y+r),(x-r*.72,y),(x,y-r)]
    else:
        points=[(x+r*math.cos(math.pi/3*i),y+r*math.sin(math.pi/3*i)) for i in range(6)]
        points.append(points[0])
    if highlight:
        a.circle((x,y),r+19,colour,.13)
        a.trace([(x+(r+19)*math.cos(math.pi*2*i/64),y+(r+19)*math.sin(math.pi*2*i/64)) for i in range(65)],1,colour,3,False)
    a.polygon(points[:-1],colour,.12*progress)
    a.trace(points,progress,colour,5,False)


def strip(a,c, y=300, numbered=False, highlight=-1):
    for i,name in enumerate(NAMES):
        x=210+i*172
        glyph(a,i,x,y,42,INKS[i],c.after(name,.6),highlight==i)
        if numbered:
            label(a,str(i+1),x,y+91,31,SOFT,c.after('give each position'))


def idea(a,c):
    a.heading('Remainders are useful clues',AQUA)
    p=c.after('look as if',2.4)
    enter=c.opening(1.4)
    for group in range(4):
        for j in range(3):
            number=3*group+j
            start=260+number*58
            end=230+group*225+j*44
            a.circle((start+(end-start)*p,323),15,BLUE,enter)
    r=c.after('the remainder',.8)
    for j in range(2):
        start=260+(12+j)*58
        end=1100+j*44
        a.circle((start+(end-start)*p,323),15,GOLD,enter)
    label(a,'4 groups of 3',560,438,37,BLUE,p)
    label(a,'2 left',1100,438,37,GOLD,r)
    label(a,'14 = 4 × 3 + 2',640,545,42,WHITE,r)


def digit_prompt(a,c):
    a.heading('Is 2,473 divisible by 3?',GOLD)
    p=c.after('Easy problem',1)
    for i,(digit,col) in enumerate(zip('2473',INKS)):
        x=352+i*192
        a.rounded(x-66,258,132,130,16,col,.2*p)
        label(a,digit,x,323,72,col,p)
    label(a,'Look at the digits',640,510,38,WHITE,c.after('look at its digits'))


def digit_sum(a,c):
    a.heading('Why does the digit sum work?',GOLD)
    p=c.after('Every 10',.8)
    for i in range(10):
        x=290+(i//3)*175+(i%3)*45
        a.circle((x,224),14,GOLD if i==9 else BLUE,p)
    label(a,'10 = 3 + 3 + 3 + 1',640,303,37,WHITE,p)
    label(a,'100 = 99 + 1    •    1,000 = 999 + 1',640,374,30,SOFT,c.after('100 or 1000'))
    s=c.after('2 plus 4 plus 7 plus 3',.75)
    label(a,'2 + 4 + 7 + 3 = 16',640,457,44,AQUA,s)
    r=c.after('16 leaves remainders 1',.7)
    label(a,'16 = 5 × 3 + 1',640,533,39,GOLD,r)
    label(a,'Not divisible by 3',640,586,30,PINK,c.after('not divisible by 3'))


def cycle_prompt(a,c):
    a.heading('Which shape comes next?',AQUA,'One cycle has six different shapes')
    strip(a,c,300,True)
    label(a,'Which is shape 1,739?',640,535,42,WHITE,c.after('Which symbol'))


def cycle_answer(a,c):
    a.heading('Count complete cycles',AQUA)
    p=c.after('equals 6 times 289',.8)
    label(a,'1,739 = 6 × 289 + 5',640,201,43,WHITE,p)
    label(a,'289 whole cycles',640,260,30,SOFT,c.after('289 complete cycles'))
    five=c.after('5 positions left over',1.15)
    for i in range(6):
        x=210+i*172
        glyph(a,i,x,375,39,INKS[i],1,False)
        label(a,str(i+1),x,452,30,SOFT,1)
        if i<5:
            a.circle((x,507),10,AQUA,ease(five*1.6-i*.12))
    transition=c.after('remainder of 0',.8)
    fifth=c.after('fifth symbol is the diamond',.75)*max(0,1-2*transition)
    zero=max(0,2*transition-1)
    glyph(a,4,898,375,39,PINK,1,fifth>.35)
    glyph(a,5,1070,375,39,INKS[5],1,zero>.35)
    label(a,'5th: diamond',640,565,38,PINK,fifth)
    label(a,'Remainder 0: the 6th shape',640,565,36,INKS[5],zero)


def conditions(a,c):
    a.heading('Three clues, one number',GOLD,'Find the smallest three-digit N')
    one=c.after('remainder 4',.8)
    two=c.after('remainders 6',.8)
    three=c.after('divisible by 9',.8)
    label(a,'N = a multiple of 5 + 4',640,235,37,BLUE,one)
    label(a,'N = a multiple of 7 + 6',640,327,37,GOLD,two)
    label(a,'N is divisible by 9',640,419,37,AQUA,three)
    p=c.after('one less than the divisor',.8)
    label(a,'Add 1 to complete both groups',640,539,40,WHITE,p)


def combine(a,c):
    a.heading('One more completes both cycles',GOLD)
    p=c.after('multiple of both 5 and 7',.8)
    label(a,'N + 1 is a multiple of 5 and 7',640,205,34,WHITE,p)
    for i in range(7):
        x=190+i*150
        a.circle((x,308),22,BLUE,ease(p*1.8-i*.1))
        label(a,str(5*(i+1)),x,308,22,WHITE,p)
    for i in range(5):
        x=330+i*190
        a.circle((x,415),22,GOLD,ease(p*1.7-i*.13))
        label(a,str(7*(i+1)),x,415,22,WHITE,p)
    mul=c.after('35 times a whole number',.8)
    label(a,'N + 1 = 35k',640,512,43,AQUA,mul)
    label(a,'N = 35k − 1',640,574,43,WHITE,c.after('n equals 35 k minus 1'))


def solve(a,c):
    a.heading('Use the third clue',AQUA)
    p=c.after('35 k must leave remainder 1',.8)
    label(a,'35k must leave remainder 1 when divided by 9',640,195,30,WHITE,p)
    q=c.after('35 leaves remainders 8',.8)
    label(a,'35 = 4 × 9 − 1',640,276,39,GOLD,q)
    q2=c.after('same as minus 1',.8)
    label(a,'Remainders of 35, 70, …, 280',640,343,28,SOFT,q2)
    for i in range(8):
        x=290+i*100
        colour=AQUA if i==7 else BLUE
        a.circle((x,390),25,colour,q2)
        label(a,str(8-i),x,390,25,WHITE,q2)
    first=c.after('smallest positive choice is 8')
    label(a,'First remainder 1: k = 8',640,450,34,AQUA,first)
    ans=c.after('equals 279',.8)
    label(a,'35 × 8 − 1 = 279',640,505,41,WHITE,ans)
    check=c.after('Check the remainders',.8)
    label(a,'279 = 5 × 55 + 4',380,556,28,BLUE,check)
    label(a,'279 = 7 × 39 + 6',900,556,28,GOLD,check)
    label(a,'2 + 7 + 9 = 18',640,584,27,AQUA,c.after('digits sum to 18'))


def recap(a,c):
    a.heading('Use the clue, keep the condition',AQUA)
    one=c.after('digit sum',.7)
    two=c.after('repeating cycle',.7)
    three=c.after('number satisfying',.7)
    label(a,'2 + 4 + 7 + 3 = 16',640,242,36,GOLD,one)
    for i in range(6): glyph(a,i,290+i*140,383,30,INKS[i],two,False)
    label(a,'N + 1 = 35k',640,524,38,AQUA,three)


SCENES=(idea,digit_prompt,digit_sum,cycle_prompt,cycle_answer,conditions,combine,solve,recap)


def draw(art,cues,scene):
    SCENES[scene-1](art,cues)
