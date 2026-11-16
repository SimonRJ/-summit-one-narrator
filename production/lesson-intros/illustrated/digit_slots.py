"""S004: move digit cards, partition by endings, and eliminate used cards."""
import math
from visuals import AQUA, BLUE, GOLD, PINK, SOFT, WHITE, ease, mix


def label(a,text,x,y,size=35,colour=WHITE,alpha=1):
    a.label(text,x,y,size,colour,alpha,bold=True)


def card(a,x,y,value,colour=BLUE,alpha=1,w=92,h=90):
    a.rounded(x-w/2,y-h/2,w,h,12,colour,.23*alpha)
    label(a,value,x,y,48 if w>=90 else 31,colour,alpha)


def slots(a,positions,y,alpha=1):
    for x,name in positions:
        a.dashed((x-55,y-52),(x+55,y-52),SOFT,2,alpha)
        a.dashed((x-55,y+52),(x+55,y+52),SOFT,2,alpha)
        a.path(((x-55,y-52),(x-55,y+52)),SOFT,2,alpha)
        a.path(((x+55,y-52),(x+55,y+52)),SOFT,2,alpha)
        label(a,name,x,y+88,25,SOFT,alpha)


def introduction(a,c):
    a.heading('Every place has a job',AQUA)
    p=c.after('moving just one card',1.7)
    slots(a,[(430,'hundreds'),(640,'tens'),(850,'ones')],315,c.opening())
    card(a,mix(430,640,p),315-115*math.sin(math.pi*p),'4',BLUE)
    card(a,mix(640,430,p),315-20*math.sin(math.pi*p),'0',GOLD)
    card(a,850,315,'7',AQUA)
    label(a,'407',640,522,42,BLUE,max(0,1-2*p))
    label(a,'047 is not three-digit',640,522,35,PINK,max(0,2*p-1))


def exam(a,c):
    a.heading('Let restrictions organise the search',AQUA)
    slots(a,[(310,'first'),(475,''),(640,''),(805,''),(970,'last')],304,c.opening())
    first=c.after('first digit',.8)
    last=c.after('last digit',.8)
    repeat=c.after('cards may repeat',.8)
    card(a,310,304,'4',GOLD,first)
    card(a,970,304,'0',AQUA,last)
    label(a,'size',310,482,31,GOLD,first)
    label(a,'divisibility',970,482,31,AQUA,last)
    label(a,'Use each card as allowed',640,542,32,SOFT,repeat)


def smallest_prompt(a,c):
    a.heading('Make the smallest three-digit number',GOLD)
    p=c.after('digit cards zero',.8)
    for i,v in enumerate('047'):card(a,440+i*200,240,v,(GOLD,BLUE,AQUA)[i],p)
    slots(a,[(430,'hundreds'),(640,'tens'),(850,'ones')],448,p)


def smallest_answer(a,c):
    a.heading('Put the smallest legal digit first',GOLD)
    slots(a,[(430,'hundreds'),(640,'tens'),(850,'ones')],350,1)
    four=c.after('Four is our smallest choice',.9)
    zero=c.after('Put zero in the tens',.9)
    seven=c.after('seven in the units',.9)
    card(a,mix(300,430,four),mix(196,350,four),'4',BLUE)
    card(a,mix(640,640,zero),mix(196,350,zero),'0',GOLD)
    card(a,mix(980,850,seven),mix(196,350,seven),'7',AQUA)
    label(a,'407',640,555,50,WHITE,c.after('four hundred and seven'))


def even_prompt(a,c):
    a.heading('Count the even numbers',BLUE)
    p=c.after('zero, two and five',.8)
    for i,v in enumerate('025'):card(a,440+i*200,245,v,(GOLD,BLUE,AQUA)[i],p)
    slots(a,[(430,'hundreds'),(640,'tens'),(850,'ones')],438,p)
    q=c.after('units place',.8)
    a.trace([(795,380),(905,380),(905,495),(795,495),(795,380)],q,GOLD,4,False)
    label(a,'End in 0 or 2',640,567,34,GOLD,c.after('each allowed ending'))


def even_answer(a,c):
    a.heading('Split by the last card',BLUE)
    zero=c.after('A final zero',.8)
    a.arrow((330,249),(420,249),GOLD,zero)
    label(a,'ends in 0',275,249,31,GOLD,zero)
    for i,v in enumerate(('250','520')):card(a,610+i*230,249,v,AQUA,zero,w=150)
    two=c.after('A final two',.8)
    label(a,'ends in 2',275,408,31,BLUE,two)
    a.arrow((330,408),(420,408),BLUE,two)
    card(a,610,408,'502',AQUA,two,w=150)
    card(a,840,408,'052',PINK,two,w=150)
    a.path(((775,451),(905,364)),PINK,4,two)
    label(a,'3 valid numbers',640,549,40,WHITE,c.after('three numbers altogether'))


def challenge_prompt(a,c):
    a.heading('Combine the two restrictions',GOLD)
    p=c.after('zero, one, two, four and six',1)
    for i,v in enumerate('01246'):card(a,280+i*180,235,v,(BLUE,BLUE,BLUE,GOLD,AQUA)[i],p)
    slots(a,[(280,'first'),(460,''),(640,''),(820,''),(1000,'last')],412,p)
    label(a,'greater than 40,000',375,560,29,GOLD,c.after('exceed forty thousand'))
    label(a,'divisible by 4',925,560,29,AQUA,c.after('divisible by four'))


ENDINGS=('20','40','60','12','04','24','64','16')


def ending_grid(a,alpha=1,y=310,colour=BLUE):
    for i,v in enumerate(ENDINGS):
        x=220+i*120
        card(a,x,y,v,colour,alpha,w=80,h=70)


def endings(a,c):
    a.heading('Check the final two digits',GOLD)
    first=c.after('first digit is four or six',.8)
    label(a,'First digit: 4 or 6',640,190,34,WHITE,first)
    groups=[('Ending in zero',('20','40','60')),('Ending in two',('12',)),
            ('Ending in four',('04','24','64')),('Ending in six',('16',))]
    for row,(cue,values) in enumerate(groups):
        p=c.after(cue,.8);y=265+row*77
        label(a,('last 0','last 2','last 4','last 6')[row],325,y,29,SOFT,p)
        for j,value in enumerate(values):card(a,530+j*160,y,value,AQUA,p,w=100,h=60)


def crossing(a,x,y,visible):
    a.path(((x-39,y+35),(x+39,y-35)),PINK,4,visible)


def count_cases(a,c):
    a.heading('The first card cannot be reused',GOLD)
    p=c.after('With four first',.8)
    q=c.after('With six first',.8)
    first=p*max(0,1-2*q)
    second=max(0,2*q-1)
    for lead,alpha in (('4',first),('6',second)):
        label(a,lead+' first',640,178,38,GOLD if lead=='4' else AQUA,alpha)
        for i,v in enumerate(ENDINGS):
            x=340+(i%4)*200;y=270+(i//4)*105
            card(a,x,y,v,BLUE,alpha,w=112,h=78)
            if lead in v:crossing(a,x,y,alpha)
        reveal=c.after('Four endings remain' if lead=='4' else 'Five endings remain',.8)
        label(a,'4 endings' if lead=='4' else '5 endings',640,480,37,WHITE,alpha*reveal)
    label(a,'Two remaining cards can swap',640,558,33,SOFT,c.after('either order'))


def total(a,c):
    a.heading('Count each case once',AQUA)
    a1=c.after('four times two',.8);a2=c.after('five times two',.8)
    label(a,'4 endings × 2 middle orders = 8',640,230,38,GOLD,a1)
    label(a,'5 endings × 2 middle orders = 10',640,320,38,AQUA,a2)
    label(a,'8 + 10 = 18',640,414,49,WHITE,c.after('eighteen numbers'))
    ex=c.after('sixty-one thousand two hundred and four',.8)
    label(a,'Example: 61,204 ends in 04',640,530,34,BLUE,ex)


def mistakes(a,c):
    a.heading('Zero can be inside, not first',PINK)
    p=c.after('cannot go at the very start',.8)
    label(a,'01246',400,273,54,PINK,p)
    a.path(((310,319),(490,227)),PINK,5,p)
    label(a,'60,124',890,273,54,AQUA,p)
    q=c.after('already used at the front',.8)
    label(a,'A card used first cannot also be in the ending',640,424,32,WHITE,q)
    label(a,'Count both middle orders',640,534,33,SOFT,c.after('middle cards'))


def recap(a,c):
    a.heading('A shorter exam search',AQUA)
    p=c.after('strongest rules first',.8)
    slots(a,[(280,'first'),(460,''),(640,''),(820,''),(1000,'last')],280,p)
    card(a,280,280,'4',GOLD,p)
    card(a,1000,280,'0',AQUA,p)
    label(a,'1. Fix the strongest restriction',640,445,34,GOLD,p)
    label(a,'2. Count each remaining order once',640,525,34,AQUA,c.after('exactly one case'))


SCENES=(introduction,exam,smallest_prompt,smallest_answer,even_prompt,even_answer,
        challenge_prompt,endings,count_cases,total,mistakes,recap)


def draw(art,cues,scene):
    SCENES[scene-1](art,cues)
