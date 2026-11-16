"""S011: prime factors as selectable and pairable objects."""
from visuals import AQUA, BLUE, GOLD, PINK, SOFT, WHITE, VIOLET, ease, mix


def text(a,t,x,y,size=34,col=WHITE,alpha=1):a.label(t,x,y,size,col,alpha,bold=True)

def chip(a,t,x,y,col,alpha=1,r=27):
    a.circle((x,y),r,col,.20*alpha)
    text(a,t,x,y,max(33,round(r*1.15)),col,alpha)


def intro(a,c):
    a.heading('Primes are multiplication building blocks',BLUE)
    p=c.after('exactly two positive factors')
    chip(a,'7',640,235,BLUE,c.opening(),40)
    a.arrow((615,288),(490,375),BLUE,p);a.arrow((665,288),(790,375),BLUE,p)
    chip(a,'1',465,410,SOFT,p);chip(a,'7',815,410,BLUE,p)
    text(a,'exactly two positive factors',640,525,32,WHITE,p)


def exams(a,c):
    a.heading('Factor clues come in different forms',AQUA)
    p=c.after('possible rectangles',.8)
    for row in range(3):
        for col in range(4):a.rounded(220+col*55,250+row*55,48,48,5,BLUE,.6*ease(p*2-(row*4+col)*.07))
    text(a,'3 × 4 = 12',302,485,34,BLUE,p)
    q=c.after('perfect squares',.8)
    for row in range(3):
        for col in range(3):a.rounded(810+col*55,250+row*55,48,48,5,AQUA,.6*ease(q*2-(row*3+col)*.08))
    text(a,'3 × 3 = 9',892,485,34,AQUA,q)


def prime_question(a,c):
    a.heading('Is 37 prime?',BLUE)
    text(a,'37',640,260,104,BLUE,c.after('thirty-seven'))
    p=c.after('square root',.8)
    text(a,'6² = 36   <   37   <   49 = 7²',640,450,38,WHITE,p)
    text(a,'Only possible small factors need checking',640,535,29,SOFT,p)


def prime_answer(a,c):
    a.heading('Test primes up to √37',BLUE)
    for i,(n,cue) in enumerate((('2','two'),('3','three'),('5','five'))):
        x=340+i*300;p=c.after(cue,.7)
        chip(a,n,x,280,(BLUE,GOLD,AQUA)[i],p,45)
        q=c.after('None divides',.7)
        a.path(((x-30,385),(x+30,445)),PINK,5,q);a.path(((x-30,445),(x+30,385)),PINK,5,q)
    text(a,'37 is prime',640,525,45,WHITE,c.after('thirty-seven is prime'))


def factor_question(a,c):
    a.heading('How many divisors does 60 have?',GOLD)
    text(a,'60',640,240,86,GOLD,c.after('sixty'))
    p=c.after('prime factors',.8)
    for x,n,col in ((400,'2',BLUE),(640,'3',GOLD),(880,'5',AQUA)):
        chip(a,n,x,435,col,p,45)
    text(a,'Choose how many copies of each',640,545,30,SOFT,c.after('number of copies'))


def factor_answer(a,c):
    a.heading('Each exponent is a choice',GOLD)
    text(a,'60 = 2² × 3 × 5',640,185,40,WHITE,c.after('prime factorisation'))
    p=c.after('three choices',.7)
    for col,(name,mul) in enumerate((('×1',1),('×3',3),('×5',5),('×15',15))):
        x=430+col*155
        text(a,name,x,260,33,SOFT,p)
        for row,factor in enumerate((1,2,4)):
            y=325+row*80
            q=ease(p*2-(row*4+col)*.055)
            a.rounded(x-58,y-30,116,60,8,BLUE,.16*q)
            text(a,str(mul*factor),x,y,40,WHITE,q)
    for row,name in enumerate(('×1','×2','×4')):text(a,name,235,325+row*80,33,BLUE,p)
    text(a,'3 × 2 × 2 = 12 divisors',640,570,35,GOLD,c.after('twelve divisors'))


def square_question(a,c):
    a.heading('Make 2016 a square',AQUA)
    text(a,'2016 = 2⁵ × 3² × 7',640,220,42,WHITE,c.after('factorisation uses'))
    p=c.after('pairs of identical factors',.7)
    positions=(140,220,330,410,520,740,820,960)
    vals=('2','2','2','2','2','3','3','7')
    cols=(BLUE,BLUE,BLUE,BLUE,BLUE,GOLD,GOLD,AQUA)
    for i,(x,v,col) in enumerate(zip(positions,vals,cols)):chip(a,v,x,385,col,ease(p*2-i*.09),33)
    text(a,'What is the smallest multiplier?',640,535,34,SOFT,c.after('smallest positive'))


def square_answer(a,c):
    a.heading('Pair every prime',AQUA)
    xs=(140,220,330,410,520,740,820,960)
    for x,v,col in zip(xs,('2','2','2','2','2','3','3','7'),(BLUE,BLUE,BLUE,BLUE,BLUE,GOLD,GOLD,AQUA)):
        chip(a,v,x,335,col,c.opening(),33)
    q=c.after('Add one copy of two',1.2)
    chip(a,'2',600,mix(235,335,q),BLUE,q,33)
    r=c.after('one copy of seven',1.2)
    chip(a,'7',1040,mix(235,335,r),AQUA,r,33)
    for x,w in ((105,150),(295,150),(485,150),(705,150),(925,150)):
        a.path(((x,390),(x+w,390)),SOFT,3,c.after('even exponents'))
    text(a,'multiply by 2 × 7 = 14',640,520,42,WHITE,c.after('fourteen'))


def square_check(a,c):
    a.heading('Two identical groups make a square',AQUA)
    p=c.after('Halve every exponent',.8)
    for row in range(2):
        for i,(n,col) in enumerate(zip(('2','2','2','3','7'),(BLUE,BLUE,BLUE,GOLD,AQUA))):
            chip(a,n,350+i*140,245+row*125,col,ease(p*2-(row*5+i)*.06),35)
    text(a,'168',1060,245,48,WHITE,c.after('one hundred and sixty-eight'))
    text(a,'168',1060,370,48,WHITE,c.after('one hundred and sixty-eight'))
    text(a,'168 × 168 = 28,224',640,520,39,WHITE,c.after('twenty-eight thousand'))
    text(a,'2016 × 14 = 28,224',640,570,30,SOFT,c.after('exactly fourteen'))


def mistakes(a,c):
    a.heading('Do not forget zero copies',PINK)
    text(a,'1 has just one positive factor',640,230,37,WHITE,c.after('one positive factor'))
    text(a,'so 1 is not prime',640,290,35,PINK,c.after('prime factorisation'))
    text(a,'For a prime with exponent 3:',640,390,30,SOFT,c.after('exponent of three'))
    p=c.after('zero one two or three',.7)
    for i,n in enumerate(('0','1','2','3')):chip(a,n,370+i*180,485,(BLUE,GOLD,AQUA,VIOLET)[i],ease(p*2-i*.15),32)
    text(a,'4 choices',640,570,31,WHITE,c.after('all four choices'))


def recap(a,c):
    a.heading('Two jobs for exponents',BLUE)
    p=c.after('count divisors',.7);q=c.after('even exponents',.7)
    text(a,'60 = 2² × 3 × 5',350,260,36,WHITE,c.after('same prime together'))
    text(a,'3 × 2 × 2 = 12 divisors',350,365,32,GOLD,p)
    text(a,'2016 = 2⁵ × 3² × 7',940,260,36,WHITE,c.after('same prime together'))
    text(a,'pair the odd exponents',940,365,32,AQUA,q)
    text(a,'multiply by 14',940,440,32,AQUA,q)


SCENES=(intro,exams,prime_question,prime_answer,factor_question,factor_answer,
        square_question,square_answer,square_check,mistakes,recap)
def draw(a,c,scene):SCENES[scene-1](a,c)
