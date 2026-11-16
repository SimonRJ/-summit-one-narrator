"""S022: exact token, chalk and changing-whole diagrams for the spoken examples."""
from visuals import AQUA, BLUE, GOLD, PINK, SOFT, VIOLET, WHITE, clamp, mix, lettering


def label(a,s,x,y,size=34,col=WHITE,alpha=1,align='center'):
    a.label(s,x,y,size,col,alpha,align=align,bold=True)


def heading(a,number,title):
    label(a,number,90,70,24,AQUA,align='left')
    size=43
    while lettering(title,a.px(size),True,True).width/a.scale>1030 and size>28:
        size-=1
    a.label(title,675,75,size,WHITE,bold=True,display=True)
    a.path(((75,125),(1205,125)),SOFT,2,.3)


def blocks(a,x,y,values,u=19,colour=AQUA,opacity=1):
    for n,v in enumerate(values):
        a.rounded(x+n*u*v,y,u*v-4,64,8,colour,.28*opacity)
        a.path(((x+n*u*v,y),(x+(n+1)*u*v-4,y),(x+(n+1)*u*v-4,y+64),(x+n*u*v,y+64),(x+n*u*v,y)),colour,3,opacity)
        label(a,str(v),x+(n+.5)*u*v,y+32,30,colour,opacity)


def counters(a,p=1,remove=0,show_groups=1):
    for group in range(3):
        x=180+group*300;y=330-120*remove if group==0 else 330
        if show_groups:
            a.rounded(x-15,y-38,240,78,12,GOLD if group==0 else AQUA,.12*p)
        for i in range(5):
            visible=clamp(p*15-(group*5+i))
            a.circle((x+i*42,y),14,GOLD if group==0 else AQUA,visible)
            a.circle((x+i*42-4,y-4),4,WHITE,.42*visible)


def chalk(a,appear=1,first=0,second=0):
    """Three groups of exactly ten chalk pieces, arranged five by two."""
    for group in range(3):
        x=170+group*325
        shift=-85*first if group==0 else (92*second if group==1 else 0)
        opacity=1-.65*first if group==0 else 1-.65*second if group==1 else 1
        a.rounded(x-22+shift,238,245,223,16,GOLD if group==0 else BLUE if group==1 else AQUA,.10*appear*opacity)
        for i in range(10):
            px=x+(i%5)*40+shift;py=265+(i//5)*92
            shown=clamp(appear*30-(group*10+i))
            ink=GOLD if group==0 else BLUE if group==1 else AQUA
            a.rounded(px,py,15,58,4,ink,.8*shown*opacity)
            a.rect(px+3,py+4,3,42,WHITE,.25*shown*opacity)


def intro(a,c):
    heading(a,'01','A fraction needs a whole')
    p=c.after('particular whole')
    blocks(a,220,225,(10,10,10),19,BLUE,p)
    label(a,'Original whole: 30',505,185,30,SOFT,p)
    q=c.after('whole changes',1.4)
    blocks(a,220,410,(10,10),19,AQUA,q)
    label(a,'New whole: 20',410,515,30,AQUA,q)
    label(a,'The whole has changed.',950,345,32,WHITE,c.after('different number of pieces'))


def exams(a,c):
    heading(a,'02','Read what comes after “of”')
    p=c.after('fraction of the original pile');q=c.after('fraction of what is left')
    label(a,'1/3 of 30',355,225,45,BLUE,p)
    blocks(a,185,275,(10,10,10),12,BLUE,p)
    label(a,'1/2 of 20',930,225,45,AQUA,q)
    blocks(a,800,275,(10,10),12,AQUA,q)
    label(a,'Original whole',355,405,30,SOFT,p)
    label(a,'Remaining whole',920,405,30,SOFT,q)
    a.arrow((900,520),(370,520),GOLD,c.after('Reverse one change'))
    label(a,'Undo changes in reverse order',640,575,29,GOLD,c.after('Reverse one change'))


def token_question(a,c):
    heading(a,'03','Fifteen tokens: take one third')
    p=c.after('fifteen tokens',1.6);take=c.after('takes one of three equal parts',1.3)
    counters(a,p,take)
    label(a,'One equal group is taken',285,180,31,GOLD,take)
    label(a,'How many remain?',755,500,42,WHITE,c.after('How many tokens remain'))


def token_answer(a,c):
    heading(a,'04','Two groups remain')
    back=c.after('adding the removed part back',1.4)
    counters(a,1,c.opening(1)*(1-back))
    label(a,'5 removed',285,170,32,GOLD,c.after('five tokens')*(1-back))
    label(a,'5 + 5 = 10 remain',730,425,40,AQUA,c.after('ten tokens')*(1-back))
    label(a,'10 + 5 = 15',730,505,36,WHITE,back)


def chalk_question(a,c):
    heading(a,'05','Thirty chalk pieces; two different wholes')
    p=c.after('thirty chalk pieces',1.4);first=c.after('uses one of three equal parts',1.2)
    second=c.after('uses one of two equal parts',1.2)
    chalk(a,p,first,second)
    label(a,'1/3 of the original',290,180,29,GOLD,first)
    label(a,'1/2 of what is left',730,495,30,BLUE,second)
    label(a,'What remains?',1000,570,34,WHITE,c.after('How many pieces remain'))


def chalk_answer(a,c):
    heading(a,'06','The remaining twenty become the new whole')
    first=c.opening(1);second=c.after('second class uses',1.3)
    chalk(a,1,first,second)
    label(a,'30 − 10 = 20',640,180,39,WHITE,c.after('remaining count is twenty'))
    label(a,'New whole: 20',800,490,32,AQUA,c.after('next whole is now twenty'))
    label(a,'20 − 10 = 10',640,555,38,WHITE,c.after('get ten'))


def challenge(a,c):
    heading(a,'07','Start with an unknown pile')
    xs=(160,475,790,1105);y=340
    events=[c.after('Take one of three'),c.after('Add a gift'),c.after('Then take one'),c.after('twelve pieces left')]
    values=('?','after 1/3','after +4','12 left')
    arrows=('remove 1/3','add 4','remove 1/2')
    for i,(x,p) in enumerate(zip(xs,events)):
        a.circle((x,y),70,(BLUE,AQUA,GOLD,VIOLET)[i],.16*p)
        label(a,values[i],x,y,36 if i in (0,3) else 28,WHITE,p)
        if i:
            a.arrow((xs[i-1]+80,y),(x-80,y),SOFT,p)
            label(a,arrows[i-1],(xs[i-1]+x)/2,270,26,SOFT,p)
    label(a,'What was the original pile?',640,540,34,WHITE,c.after('original pile'))


def reverse(a,c):
    heading(a,'08','Undo the last change first')
    p=c.after('ending twelve pieces');q=c.after('rebuild that whole',1.0)
    blocks(a,210,185,(12,),14,AQUA,p);blocks(a,378,185,(12,),14,GOLD,q)
    label(a,'12 × 2 = 24',900,217,37,WHITE,q)
    r=c.after('Undo the gift',1.0)
    blocks(a,210,330,(10,10),14,BLUE,r)
    blocks(a,490,330,(4,),14,GOLD,r)
    label(a,'24 − 4 = 20',900,362,37,WHITE,r)
    s=c.after('two of the original three equal parts',1.0);t=c.after('missing part',1.0)
    blocks(a,210,475,(10,10),14,BLUE,s);blocks(a,490,475,(10,),14,AQUA,t)
    label(a,'20 ÷ 2 × 3 = 30',900,507,35,WHITE,t)


def check(a,c):
    heading(a,'09','Check the story forwards')
    xs=(160,475,790,1105);y=320
    events=[c.after('Run the recipe'),c.after('get twenty'),c.after('get twenty-four'),c.after('leaves twelve')]
    for i,(x,p,n) in enumerate(zip(xs,events,('30','20','24','12'))):
        a.circle((x,y),66,(BLUE,AQUA,GOLD,VIOLET)[i],.2*p)
        label(a,n,x,y,43,WHITE,p)
        if i:
            a.arrow((xs[i-1]+78,y),(x-78,y),SOFT,p)
            label(a,('−10','+4','−12')[i-1],(xs[i-1]+x)/2,250,32,SOFT,p)
    label(a,'The last 12 matches the question.',640,490,35,AQUA,c.after('stated ending'))


def mistakes(a,c):
    heading(a,'10','Fractions must name the same whole')
    p=c.after('same original whole');q=c.after('uses a new whole')
    label(a,'Original: 30',85,215,30,BLUE,p,align='left')
    blocks(a,360,185,(10,10,10),14,BLUE,p)
    label(a,'1/3 of 30 = 10',1000,217,32,WHITE,p)
    label(a,'Remaining: 20',85,375,30,AQUA,q,align='left')
    blocks(a,360,345,(10,10),14,AQUA,q)
    label(a,'1/2 of 20 = 10',1000,377,32,WHITE,q)
    label(a,'Different wholes: do not add 1/3 and 1/2 directly.',640,520,30,PINK,q)


def recap(a,c):
    heading(a,'11','Name it, split it, rebuild it')
    p=c.after('original, remaining or new');q=c.after('Draw equal parts');r=c.after('rebuild the last whole first');s=c.after('reverse any addition')
    label(a,'1',175,225,42,BLUE,p);label(a,'Name each whole',245,225,37,WHITE,p,'left')
    label(a,'2',175,325,42,AQUA,q);label(a,'Draw its equal parts',245,325,37,WHITE,q,'left')
    label(a,'3',175,425,42,GOLD,r);label(a,'Rebuild from the ending',245,425,37,WHITE,r,'left')
    label(a,'4',175,525,42,VIOLET,s);label(a,'Reverse earlier steps',245,525,37,WHITE,s,'left')
    blocks(a,850,295,(10,10,10),9,BLUE,q)


SCENES=(intro,exams,token_question,token_answer,chalk_question,chalk_answer,challenge,reverse,check,mistakes,recap)
def draw(a,c,scene):SCENES[scene-1](a,c)
