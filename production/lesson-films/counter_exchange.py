"""Individual counters travel between trays and remain visible through every move."""
from math import pi, sin
from stage import blend, clamp, mix

BACKGROUND=('#392a26','#211f24')
WHITE, YELLOW, GREEN, BLUE, RIM = '#f4edda','#ffc47c','#9bdab1','#8cc7e5','#846b5a'
COLOURS=(YELLOW,GREEN,BLUE)
BRIDGE='When you undo a move, follow the same counters back to their original tray. Which pile was the fraction taken from?'


def check_maths():
    assert (12-1,8+1,4-2)==(11,9,2)
    assert [(a,48-a) for a in range(49) if a-6==48-a+6]==[(30,18)]
    outcomes=[]
    for a in range(37):
        for b in range(37-a):
            c=36-a-b
            if a%2 or (a//2+b)%3:continue
            give=(a//2+b)//3
            if a//2==a//2+b-give==c+give:outcomes.append((a,b,c))
    assert outcomes==[(24,6,6)]


def gridpos(tray,index,centres):
    cols=6 if len(centres)==3 else 8
    return centres[tray]+(index%cols-(cols-1)/2)*33, 395-(index//cols)*38


def counter(a,x,y,col):
    a.dot(x,y+3,13,'#291e1d');a.dot(x,y,12,col);a.dot(x-2,y-3,5,blend(col,WHITE,.3))


def trays(a, initial, src=None, dst=None, count=0, t=0, labels=True):
    centres=(348,929) if len(initial)==2 else (255,640,1025)
    width=330 if len(initial)==3 else 414
    for k,x in enumerate(centres):
        a.box(x-width/2,201,width,242,radius=20,fill='#473932',edge=RIM,stroke=4)
        a.label(('LEFT','RIGHT')[k] if len(centres)==2 else ('FIRST','SECOND','THIRD')[k],
                x-width/2+17,173,23,COLOURS[k],bold=True)
    for tray,total in enumerate(initial):
        for index in range(total):
            p=gridpos(tray,index,centres)
            if tray==src and index>=total-count:
                j=index-(total-count)
                progress=clamp((t*1.25-j/max(1,count)*.25))
                q=gridpos(dst,initial[dst]+j,centres)
                p=(mix(p[0],q[0],progress),mix(p[1],q[1],progress)-sin(progress*pi)*92)
            counter(a,*p,COLOURS[tray])
    for k,total in enumerate(initial):
        if not labels:continue
        if t>=1-1e-6:
            total+=count*(k==dst)-count*(k==src)
        elif 0<t<1 and k in (src,dst): continue
        a.text(str(total),centres[k],478,37,WHITE,bold=True)


def draw(a,n,c):
    title=['The same counters change trays','A one-counter transfer','Two cases finish equal','Send the six badges back',
           'Work back from three equal trays','Reverse the second move','Reverse the first move','Check the moves forwards'][n-1]
    a.label(title,75,78,45,WHITE,bold=True)
    if n==1:
        trays(a,(13,7),0,1,3,c.reveal('move three counters',2.4))
        a.text('Total = 20',640,555,34,YELLOW,bold=True)
    elif n==2:
        t=c.reveal('move one across',1.7);trays(a,(12,8),0,1,1,t)
        a.text('12 − 8 = 4',390,552,34,YELLOW,opacity=1-t)
        a.text('11 − 9 = 2',908,552,34,YELLOW,opacity=t)
    elif n==3:
        trays(a,(24,24),labels=False)
        a.text('Final total = 48 badges',640,520,33,WHITE,bold=True)
        a.text('What were the two starting counts?',640,573,26,YELLOW,opacity=c.reveal('how many badges'))
    elif n==4:
        trays(a,(24,24),1,0,6,c.reveal('put the six badges back',2.3))
        a.text('Gap = 30 − 18 = 12',640,555,35,YELLOW,opacity=c.reveal('their difference is twelve'),bold=True)
    elif n==5:
        trays(a,(12,12,12),labels=False)
        a.text('36 counters altogether',640,528,34,WHITE,bold=True)
        a.text('Finish with equal piles',640,575,26,YELLOW,opacity=c.reveal('all three finish equal'))
    elif n==6:
        t=c.reveal('each third is six',2.2);trays(a,(12,12,12),2,1,6,t)
        a.text('Two thirds = 12     •     One third = 6',640,555,33,YELLOW,opacity=c.reveal('those two thirds'),bold=True)
    elif n==7:
        t=c.reveal('passed twelve to the second',2.35);trays(a,(12,18,6),1,0,12,t)
        a.text('Start: 24, 6, 6',640,558,36,YELLOW,opacity=c.reveal('starting counts'),bold=True)
    else:
        first=c.reveal('its new pile',2.05); second=c.reveal('record who gives',2.05)
        if second>0:trays(a,(12,18,6),1,2,6,second)
        else:trays(a,(24,6,6),0,1,12,first)
        a.text('½ of 24 = 12',365,555,31,YELLOW,opacity=first,bold=True)
        a.text('⅓ of the new 18 = 6',915,555,31,GREEN,opacity=second,bold=True)


def poster(draw):return draw(4.25,1.5)
