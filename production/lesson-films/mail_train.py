"""Parcel bundles, sorting stamps and two aligned scales for remainder problems."""
from stage import blend, clamp, mix
BACKGROUND = ('#332f38','#20262e')
PAPER, GOLD, SKY, GREEN, RED, RULE = '#fff2dc','#ffcc7e','#a3d8fc','#94dfb6','#f6a29c','#787786'
BRIDGE = 'When the film adds 1 to make a number divisible by both 4 and 6, pause. Where must the two ends of the search interval move? After finding a common multiple, how will you get back to the original number?'
HEAD = ('The loose parcel','Two sorting stamps','Read only what each stamp needs','One parcel short',
        'Move both end stops','Mark the shared stops','Unload the extra parcel','Which numbers are we counting?')


def check_maths():
    assert divmod(17,4)==(4,1) and 20-17==3
    assert [n for n in (324,344,354,384) if n%12==0]==[324,384]
    assert [n for n in range(23,60) if (n+1)%4==(n+1)%6==0]==[23,35,47,59]


def txt(a,x,y,s,k=PAPER,size=38,t=1):
    a.text(str(s),x,y,size,k,bold=True,opacity=t)


def parcel(a,x,y,t=1):
    a.box(x-26,y-19,52,38,fill='#bd8f66',edge='#f3d7b4',radius=4,opacity=t)
    a.line([(x,y-19),(x,y+19)],'#f5ce8e',6,t)
    a.line([(x-24,y+4),(x+24,y+4)],'#f5ce8e',4,t)


def cards(a,c,n):
    labels=(324,344,354,384)
    for i,value in enumerate(labels):
        x=188+i*294
        a.box(x-97,207,194,135,radius=12,fill='#ddd4bc',edge='#f6e9d0')
        txt(a,x,269,value,'#292d37',58)
        square=(c.reveal('pass') if i!=2 else 0) if n==3 else 0
        tri=(c.reveal('first and last') if i in (0,3) else 0) if n==3 else 0
        if square: a.box(x-47,363,32,32,fill=SKY,radius=3,opacity=square)
        if tri: a.polygon([(x+27,360),(x+8,396),(x+46,396)],blend('#262b32',GOLD,tri))
        if n==3 and i!=2:
            txt(a,x,457,'sum = '+str(sum(map(int,str(value)))),PAPER,29,c.reveal('sums'))
        if n==3 and i==2:txt(a,x,382,'54 fails',RED,28,c.reveal('Fifty four fails'))


def position(v):
    return 150+(v-20)*23.4


def ruled(a,y):
    a.line([(position(20),y),(position(62),y)],RULE,4)
    for v in range(20,63):
        x=position(v);a.line([(x,y-4),(x,y+5)],RULE,2)


def stops(a,y,values,col,alpha=1):
    for v in values:
        x=position(v);a.dot(x,y,9,col,alpha);txt(a,x,y+37,v,col,32,alpha)


def draw(a,n,c):
    a.label(HEAD[n-1],65,72,44,PAPER,bold=True)
    a.line([(64,122),(1214,122)],RULE,2)
    if n==1:
        for group in range(5):
            left=105+223*group
            a.box(left,234,173,157,fill='#38343a',edge=RULE,radius=12,stroke=3)
            for k in range(4):
                idx=4*group+k; alpha=1 if idx<17 else c.reveal('Three',1.0,(idx-17)*.15)
                parcel(a,left+49+73*(k%2),281+62*(k//2),alpha)
        txt(a,640,480,'17 = 4 × 4 + 1',GOLD,44,c.reveal('one loose'))
        txt(a,640,549,'3 spaces left',GREEN,33,c.reveal('what is missing'))
    elif n in (2,3):
        cards(a,c,n)
        if n==2:
            txt(a,420,472,'■    groups of 4',SKY,36,c.reveal('square stamp'))
            txt(a,845,472,'▲    groups of 3',GOLD,36,c.reveal('triangle stamp'))
        else:
            txt(a,640,548,'Both sorting stamps: 324 and 384',GREEN,35,c.reveal('get both stamps'))
    elif n==4:
        txt(a,640,243,'Original load',PAPER,32)
        ruled(a,360);stops(a,360,[23,59],SKY)
        a.line([(position(23),360),(position(59),360)],SKY,5)
        txt(a,640,512,'Add 1  →  groups of 4 and groups of 6',GOLD,35,c.reveal('Add one parcel'))
    elif n==5:
        txt(a,587,198,'Original loads',SKY,31);ruled(a,265);stops(a,265,[23,59],SKY)
        amt=c.reveal('one place',1.6); y=mix(265,433,amt)
        if amt:
            for v in (23,59):
                a.arrow((position(v),300),(position(v+1),406),GOLD,amt,3)
            a.line([(position(23+amt),y),(position(59+amt),y)],GOLD,5)
            for v in (23,59):a.dot(position(v+amt),y,9,GOLD)
        if amt>.98:stops(a,433,[24,60],GOLD)
        txt(a,640,530,'Shifted loads',GOLD,32,c.reveal('shifted interval'))
    elif n==6:
        for step,y,col,cue in [(4,245,SKY,'multiples of four'),(6,351,GOLD,'multiples of six')]:
            a.label('× '+str(step),66,y,34,col,bold=True);ruled(a,y)
            for v in range(24,61,step):
                a.dot(position(v),y,8,col,c.reveal(cue,.65,(v-24)*.02))
        t=c.reveal('shared stops',.9)
        for v in (24,36,48,60):
            x=position(v);a.line([(x,254),(x,341)],GREEN,4,t);txt(a,x,433,v,GREEN,38,t)
        txt(a,640,530,'12 between shared stops',PAPER,37,c.reveal('repeats every twelve'))
    elif n==7:
        for i,v in enumerate((24,36,48,60)):
            x=218+i*280;txt(a,x,231,v,GOLD,52)
            t=c.reveal('Take one away',.8,.12*i);a.arrow((x,280),(x,350),SKY,t,4);txt(a,x,408,v-1,SKY,55,t)
        txt(a,640,533,'60 = 15 × 4 = 10 × 6',GREEN,41,c.reveal('fifteen fours'))
    else:
        txt(a,640,220,'Original:  23,   35,   47,   59',SKY,39)
        txt(a,640,364,'Shifted:   24,   36,   48,   60',GOLD,39,c.reveal('two different number lines'))
        a.arrow((277,272),(277,322),GOLD,c.reveal('Move the end stops'),4)
        a.arrow((1004,328),(1004,270),SKY,c.reveal('undo the change'),4)
        txt(a,640,526,'Move both ends.  Test.  Undo the move.',GREEN,34,c.reveal('undo the change'))


def poster(draw):return draw(6,1)
