"""Three physical route-number drums and a dispatch board expose the effects of choosing each digit."""
from itertools import permutations

from stage import clamp, mix, blend

BACKGROUND=('#f0e9ce','#ded9b8')
INK,FOREST,RAIL,WINDOW='#23372e','#286247','#769074','#163b30'
WHITE,GOLD,RED,PALE,CARD='#f8f4dd','#d5ac4f','#984930','#b8caac','#f4f1d8'
BRIDGE='Set the first and last drums before the middle. Notice how choosing six at the front changes which even cards are still available.'
DIGITS=(0,2,3,6,9)
SEGMENTS={'0':'abcdef','1':'bc','2':'abdeg','3':'abcdg','4':'bcfg','5':'acdfg','6':'acdefg','7':'abc','8':'abcdefg','9':'abcdfg'}
LINES={'a':((.23,.12),(.78,.12)),'b':((.84,.18),(.84,.45)),'c':((.84,.55),(.84,.82)),
       'd':((.23,.89),(.78,.89)),'e':((.16,.55),(.16,.82)),'f':((.16,.18),(.16,.45)),'g':((.23,.50),(.78,.50))}


def check_maths():
    a=[10*x+y for x,y in permutations((0,4,7),2) if x]
    routes=[100*x+10*y+z for x,y,z in permutations(DIGITS,3) if x]
    nozero=[n for n in routes if '0' not in str(n)]
    evening=[n for n in routes if n>500 and n%2==0]
    assert min(a)==40 and len(routes)==len(set(routes))==48 and len(nozero)==24
    assert len(evening)==15 and [sum(n//100==h for n in evening) for h in (6,9)]==[6,9]
    assert 930 in evening
    assert all(len(set(s))==len(s) and set(s)<=set(LINES) for s in SEGMENTS.values())


def words(a,text,x,y,size=36,colour=INK,t=1,align='left'):
    a.label(text,x,y,size,colour,t,align=align,bold=True)


def digit(a,x,y,w,h,d,off=WINDOW,on=WHITE):
    s=SEGMENTS.get(str(d),'')
    for key,(p,q) in LINES.items():
        a.line([(x+w*p[0],y+h*p[1]),(x+w*q[0],y+h*q[1])],on if key in s else off,max(2,int(w*.085)))


def blind(a,x,y,w,h,values,active=()):
    # A rubber surround and the centre hinge hold the numbered drum windows.
    a.box(x-11,y-11,w*len(values)+22,h+22,fill=FOREST,edge=INK,radius=12,stroke=4)
    for i,val in enumerate(values):
        xx=x+i*w
        a.box(xx,y,w-4,h,fill=WINDOW,edge=RAIL,radius=4,stroke=2)
        digit(a,xx+9,y+6,w-24,h-12,val,off='#204437',on=GOLD if i in active else WHITE)
        a.line([(xx+3,y+h*.51),(xx+w-7,y+h*.51)],'#324a38',2)
        if i in active:a.line([(xx+9,y+h-4),(xx+w-14,y+h-4)],GOLD,4)


def rack(a,x,y,digits,taken=(),size=65,emphasis=()):
    for j,v in enumerate(digits):
        xx=x+j*(size+10);occupied=v in taken
        a.box(xx+2,y+5,size,size+14,fill=RAIL,radius=5)
        a.box(xx,y,size,size+13,fill=PALE if occupied else CARD,edge=FOREST,radius=5,stroke=3)
        words(a,str(v),xx+size/2,y+size*.53,int(size*.58),RAIL if occupied else (RED if v in emphasis else INK),align='center')
        if occupied:a.line([(xx+8,y+size+4),(xx+size-8,y+8)],RAIL,3)


def header(a,title):
    words(a,title,72,80,47)
    a.line([(64,137),(1200,137)],FOREST,4)
    for x in (75,1200):
        a.dot(x,137,8,FOREST);a.dot(x,137,3,CARD)


def panel(a,x,y,w,h):
    a.box(x,y,w,h,fill='#f8f4dc',edge='#9baf88',radius=10,stroke=2)


def draw(a,n,c):
    titles=['A zero on the front drum','Set the front drum first','A drawer of five route cards','Choose the three drums','Which routes contain zero?','Account for every route','A restriction at either end','The two evening services','Dispatch route 930']
    header(a,titles[n-1])
    if n in (1,2):
        if n==1:
            blind(a,125,226,144,215,(0,4),active=(0,))
            words(a,'Route 4',162,521,48,FOREST,c.reveal('names route four'))
            rack(a,701,238,(0,4,7),size=93)
            words(a,'Smallest two-digit route?',664,462,38,RED,c.reveal('smallest genuine'))
        else:
            t1=c.reveal('that is four',.7);t2=c.reveal('may use zero',.7)
            blind(a,125,226,144,215,(4 if t1>.4 else None,0 if t2>.4 else None),active=(0,))
            rack(a,681,225,(0,4,7),taken=([4] if t1>.4 else [])+([0] if t2>.4 else []),size=91)
            words(a,'4 tens + 0 units',664,445,42,FOREST,c.reveal('route is forty'))
            words(a,'40',197,535,48,INK,c.reveal('route is forty'))
    elif n in (3,4):
        if n==3:
            blind(a,134,214,119,180,(None,None,None),active=(0,))
            rack(a,648,246,DIGITS,size=83,emphasis=(0,))
            words(a,'Which cards can lead?',141,494,46,RED,c.reveal('hundreds drum first'))
        else:
            choices=(c.reveal('four choices for hundreds'),c.reveal('four choices remain for tens'),c.reveal('three cards then remain'))
            example=tuple(v if t>.65 else None for v,t in zip((2,0,3),choices))
            blind(a,135,195,119,172,example)
            words(a,'One possible setting',133,545,27,FOREST,choices[-1])
            for i,(v,t) in enumerate(zip((4,4,3),choices)):
                words(a,str(v),191+i*119,426,53,FOREST,t,align='center')
                words(a,('Hundreds','Tens','Units')[i],191+i*119,481,21,INK,t,align='center')
            rack(a,679,217,DIGITS,taken=tuple(v for v in example if v is not None),size=75)
            words(a,'4 × 4 × 3 = 48',663,394,53,FOREST,c.reveal('forty-eight different'))
            words(a,'Each setting is one route',667,494,33,INK,c.reveal('one ordered set'))
    elif n in (5,6):
        panel(a,94,196,506,343);panel(a,656,196,519,343)
        words(a,'No zero',139,252,47,FOREST)
        words(a,'Contains zero',699,252,45,RED)
        rack(a,137,321,(2,3,6,9),size=68)
        rack(a,699,321,(0,),size=68,emphasis=(0,))
        if n==5:
            words(a,'How many?',139,464,43,INK,c.reveal('how many'))
            words(a,'How many remain?',700,464,35,RED,c.reveal('forty-eight numbers'))
            words(a,'48 routes altogether',640,579,32,INK,c.reveal('forty-eight numbers'),align='center')
        else:
            words(a,'4 × 3 × 2 = 24',138,460,42,FOREST,c.reveal('twenty-four numbers'))
            words(a,'48 − 24 = 24',700,460,43,RED,c.reveal('other twenty-four'))
    elif n==7:
        blind(a,113,213,124,174,(None,None,None),active=(0,2))
        words(a,'Hundreds',163,444,29,FOREST,c.reveal('only six or nine'),align='center')
        words(a,'Units',405,444,29,RED,c.reveal('even cards'),align='center')
        rack(a,684,222,DIGITS,size=73)
        words(a,'First  ·  6 or 9',690,390,43,FOREST,c.reveal('six or nine'))
        words(a,'Last  ·  0, 2 or 6',690,492,43,RED,c.reveal('even cards'))
    elif n==8:
        for i,h in enumerate((6,9)):
            x=100+i*564;t=c.reveal(('if six leads','if nine leads')[i])
            panel(a,x,177,519,380)
            blind(a,x+39,213,75,106,(h,None,None),active=(0,))
            words(a,'Final card',x+35,376,31,RED,t)
            rack(a,x+211,342,(0,2) if i==0 else (0,2,6),size=45)
            words(a,('2 × 3 = 6','3 × 3 = 9')[i],x+35,477,44,FOREST,c.reveal(('gives six routes','give nine routes')[i]))
        words(a,'6 + 9 = 15 routes',640,590,39,INK,c.reveal('add to fifteen'),align='center')
    else:
        vals=[9 if c.reveal('nine') else None,3 if c.reveal('three') else None,0 if c.reveal('zero') else None]
        blind(a,115,217,130,190,vals,active=(0,2))
        words(a,'930 > 500',698,235,48,FOREST,c.reveal('greater than five hundred'))
        words(a,'Final digit = 0',698,342,43,RED,c.reveal('even'))
        words(a,'3 different cards',698,446,42,INK,c.reveal('free of repeated digits'))


def poster(draw):return draw(8,1.5)
