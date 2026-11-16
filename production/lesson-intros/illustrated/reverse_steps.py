"""S003: reverse a number machine, restore stamps, then rewind ticket stations."""
from visuals import AQUA, BLUE, GOLD, PINK, SOFT, WHITE, ease, mix


def label(a,text,x,y,size=35,colour=WHITE,alpha=1):
    a.label(text,x,y,size,colour,alpha,bold=True)


def badge(a,x,y,value,colour=BLUE,alpha=1):
    a.rounded(x-55,y-43,110,86,15,colour,.2*alpha)
    label(a,value,x,y,32 if len(str(value))>3 else 45,colour,alpha)


def stamp(a,x,y,colour=BLUE,alpha=1):
    a.rounded(x-18,y-21,36,42,5,colour,.75*alpha)
    a.circle((x,y),6,WHITE,alpha)


def machine(a, values, forward=(1,1), reverse=(0,0)):
    xs=(240,640,1040)
    for x,value,col in zip(xs,values,(AQUA,BLUE,GOLD)):
        badge(a,x,320,value,col)
    for i,(operation,undo,col) in enumerate((('×4','÷4',BLUE),('+7','−7',GOLD))):
        left,right=xs[i]+75,xs[i+1]-75
        a.arrow((left,286),(right,286),col,forward[i])
        label(a,operation,(left+right)/2,240,35,col,forward[i])
        a.arrow((right,359),(left,359),col,reverse[i])
        label(a,undo,(left+right)/2,416,35,col,reverse[i])


def introduction(a,c):
    a.heading('Walk the story backwards',AQUA)
    p=c.after('how a value changed',.9)
    q=c.after('where the story ends',.9)
    back=c.after('walk back along its steps',1)
    badge(a,230,329,'?',BLUE,c.opening(.7))
    badge(a,1050,329,'31',GOLD,q)
    a.arrow((315,291),(965,291),BLUE,p)
    label(a,'changes',640,240,35,BLUE,p)
    a.arrow((965,369),(315,369),AQUA,back)
    label(a,'undo changes',640,435,35,AQUA,back)


def exams(a,c):
    a.heading('Start with what you know',AQUA)
    p=c.after('number machine',.8)
    for i,v in enumerate(('?','×4','+7','31')):
        x=260+i*250
        badge(a,x,279,v,(BLUE,BLUE,GOLD,WHITE)[i],p)
        if i<3: a.arrow((x+65,279),(x+185,279),SOFT,p)
    r=c.after('Reverse the steps',1)
    a.arrow((1015,436),(265,436),AQUA,r)
    label(a,'Undo the last step first',640,515,38,AQUA,r)


def basic_prompt(a,c):
    a.heading('Find the hidden input',BLUE)
    machine(a,('?','','31' if c.after('output is thirty-one')>.5 else '?'),
            (c.after('multiplies the input'),c.after('adds seven')))
    label(a,'Which step touched the result last?',640,545,34,SOFT,c.after('which step touched'))


def basic(a,c):
    a.heading('Reverse the order',BLUE)
    sub=c.after('Thirty-one minus seven',.9)
    div=c.after('dividing by four',.9)
    forward=c.after('Run six forward',1)
    machine(a,('6' if div>.5 else '?','24' if sub>.5 else '', '31'),
            (forward,forward),(div,sub))
    label(a,'(31 − 7) ÷ 4 = 6',640,536,45,AQUA,c.after('input is six'))


def stamp_prompt(a,c):
    a.heading('Sam’s stamp pile',GOLD)
    p=c.after('one third',.8)
    for i in range(3):
        x=370+i*270
        a.rounded(x-112,251,224,116,14,GOLD if i==0 else BLUE,(.12 if i==0 else .25)*p)
        label(a,'1 part',x,309,32,GOLD if i==0 else BLUE,p)
    label(a,'given away',370,420,28,GOLD,p)
    a.arrow((370,378),(370,397),GOLD,p)
    add=c.after('receives seven stamps',.8)
    label(a,'+ 7 stamps',640,480,37,GOLD,add)
    label(a,'25 at the end',640,552,42,WHITE,c.after('ends up with twenty-five'))


def stamp_answer(a,c):
    a.heading('Restore the missing third',GOLD)
    move=c.after('Remove the seven received stamps',1.4)
    for i in range(25):
        x0=470+(i%5)*66; y0=190+(i//5)*62
        if i<18:
            x1=300+(i%9)*80; y1=235+(i//9)*95
            stamp(a,mix(x0,x1,move),mix(y0,y1,move),BLUE)
        else:
            stamp(a,x0+240*move,y0,GOLD,1-move)
    two=c.after('two of the original three equal parts',.8)
    a.dashed((262,390),(1018,390),SOFT,2,two)
    nine=c.after('nine stamps per part',.8)
    label(a,'18 ÷ 2 = 9 per part',640,509,38,WHITE,nine)
    restore=c.after('Three parts is twenty-seven',1)
    for i in range(9): stamp(a,300+i*80,420,AQUA,ease(restore*1.8-i*.09))
    label(a,'3 × 9 = 27 stamps',640,574,40,AQUA,restore)


def stations_prompt(a,c):
    a.heading('Three ticket stations',GOLD)
    p=c.after('three stations',.8)
    for i in range(3):
        x=310+i*330
        a.rounded(x-100,234,200,126,15,BLUE,.24*p)
        label(a,'station '+str(i+1),x,297,29,BLUE,p)
        if i<2: a.arrow((x+110,297),(x+220,297),SOFT,p)
    rule=c.after('half the tickets',.8)
    label(a,'At each stop: halve, then subtract 2',640,451,36,WHITE,rule)
    label(a,'After station 3: 5 tickets',640,545,39,GOLD,c.after('five tickets'))


def last_station(a,c):
    a.heading('Rewind station 3',GOLD)
    add=c.after('Add back the last two tickets',.9)
    double=c.after('Double seven',.9)
    for i in range(7):
        x=340+i*100
        stamp(a,x,260,GOLD if i>=5 else BLUE,add if i>=5 else 1)
        stamp(a,x,377,AQUA,double)
    label(a,'5 + 2 = 7',640,332,38,WHITE,add)
    label(a,'7 × 2 = 14',640,484,42,AQUA,double)
    label(a,'Add 2, then double',640,552,32,SOFT,c.after('same reverse rule'))


def rewind(a,c):
    a.heading('Keep rewinding',AQUA)
    a2=c.after('fourteen plus two',.8)
    a1=c.after('thirty-two plus two',.8)
    finish=c.after('sixty-eight',.6)
    values=[('68',finish),('32',c.after('get thirty-two',.7)),('14',1),('5',1)]
    for i,(value,p) in enumerate(values):
        x=190+i*300
        badge(a,x,308,value,(AQUA,BLUE,BLUE,GOLD)[i],p)
        label(a,('start','after 1','after 2','after 3')[i],x,390,26,SOFT,p)
    for i,p in ((0,a1),(1,a2),(2,1)):
        left=190+i*300
        a.arrow((left+225,273),(left+75,273),GOLD,p)
        label(a,'+2, then ×2',left+150,225,23,GOLD,p)
    check=c.after('Check forward',.8)
    for i in range(3):
        x=190+i*300;a.arrow((x+75,342),(x+225,342),BLUE,check)
    label(a,'Forward check: halve, then subtract 2',640,538,35,WHITE,check)


def mistakes(a,c):
    a.heading('The order matters',PINK)
    p=c.after('Doubling five',.8)
    label(a,'5 × 2 + 2 = 12',640,235,43,PINK,p)
    label(a,'12 ÷ 2 − 2 = 4',640,314,38,PINK,c.after('result is four'))
    correct=c.after('route fails',.8)
    label(a,'(5 + 2) × 2 = 14',640,424,43,AQUA,correct)
    label(a,'Each half is of the current pile',640,535,34,SOFT,c.after('pile currently in front'))


def recap(a,c):
    a.heading('Reverse, then check',AQUA)
    badge(a,230,296,'start',BLUE,c.opening())
    badge(a,1050,296,'end',GOLD,c.opening())
    back=c.after('inverse operations',.8)
    a.arrow((970,275),(310,275),AQUA,back)
    label(a,'undo in reverse order',640,223,34,AQUA,back)
    forward=c.after('run your starting value forward',.8)
    a.arrow((310,370),(970,370),BLUE,forward)
    label(a,'check forward',640,432,34,BLUE,forward)


SCENES=(introduction,exams,basic_prompt,basic,stamp_prompt,stamp_answer,
        stations_prompt,last_station,rewind,mistakes,recap)


def draw(art,cues,scene):
    SCENES[scene-1](art,cues)
