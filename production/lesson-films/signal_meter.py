"""Regroup railway signal lamps, then restore the covers on ten sockets."""
from stage import mix
BACKGROUND=('#253338','#1b272d')
BRIDGE='When the two racks are switched on together, group the six lamps into identical pairs. Which two meter readings can you subtract to learn what one amber lamp draws?'
HEAD=('Same colour, same current','Two signal racks','Plug the racks together','What one pair draws','Check both meter readings','An unlabelled row','Restore the colours','Spot the faulty meter')
PAPER,AMBER,BLUE,SEA,RED,DIM='#f4efdf','#f2be61','#8fbde4','#90d2b1','#f19b91','#617581'

def check_maths():
    assert [(a,b) for a in range(18) for b in range(20) if 2*a+b==17 and a+2*b==19]==[(5,7)]
    assert [b for b in range(11) if 5*(10-b)+7*b==62]==[6]
    assert all((5*(10-b)+7*b)%2==0 for b in range(11))

def label(a,s,x,y,size=35,col=PAPER,t=1,align='left'):
    a.label(s,x,y,size,col,t,align=align,bold=True)

def lamp(a,x,y,kind,t=1):
    colour={'A':AMBER,'B':BLUE,'?':DIM}[kind]
    a.box(x-15,y+16,30,14,radius=3,fill=DIM,opacity=t);a.dot(x,y,26,colour,t)
    a.text(kind,x,y,24,'#293036',bold=True,opacity=t)

def rack(a,x,y,kinds):
    for i,k in enumerate(kinds):lamp(a,x+(i%5)*81,y+(i//5)*91,k)

def meter(a,x,y,n,t=1):
    a.box(x,y,233,82,fill='#1d282b',edge=SEA,radius=7,stroke=3,opacity=t)
    a.text(f'{n} mA',x+117,y+41,40,SEA,bold=True,opacity=t)

def draw(a,n,c):
    label(a,HEAD[n-1],70,73,46);a.line([(70,122),(1210,122)],DIM,2)
    if n==1:
        rack(a,210,314,'AAB');meter(a,713,275,'?',c.reveal('meter displays'))
        label(a,'Same colour, same current',640,515,40,SEA,c.reveal('same electric current'),'center')
    elif n==2:
        rack(a,190,242,'AAB');meter(a,677,198,17,c.reveal('seventeen milliamps'))
        rack(a,190,415,'ABB');meter(a,677,371,19,c.reveal('nineteen milliamps'))
    elif n==3:
        t=c.reveal('Slide one blue lamp',1.7)
        before=[(192,231),(273,231),(354,231),(192,423),(273,423),(354,423)]
        after=[(168,319),(399,319),(247,319),(630,319),(478,319),(709,319)]
        for i,k in enumerate('AABABB'):lamp(a,mix(before[i][0],after[i][0],t),mix(before[i][1],after[i][1],t),k)
        meter(a,894,278,36,c.reveal('thirty-six milliamps'))
        label(a,'3 identical pairs',439,496,38,SEA,c.reveal('identical pairs'),'center')
    elif n==4:
        rack(a,182,246,'AB');label(a,'36 ÷ 3 = 12 mA',567,248,42,SEA,c.reveal('one pair draws twelve'))
        rack(a,182,410,'AAB');label(a,'17 − 12 = 5 mA',567,411,42,AMBER,c.reveal('from seventeen'))
    elif n==5:
        rack(a,180,271,'AAB');rack(a,180,435,'ABB')
        label(a,'5 + 5 + 7 = 17 mA',577,271,42,AMBER,c.reveal('five plus five plus seven'))
        label(a,'5 + 7 + 7 = 19 mA',577,435,42,BLUE,c.reveal('five plus seven plus seven'))
    elif n==6:
        rack(a,162,254,'?'*10);meter(a,764,257,62,c.reveal('sixty-two milliamps'))
        label(a,'10 sockets. Which colours?',640,507,38,PAPER,c.reveal('what change'),'center')
    elif n==7:
        b=round(c.reveal('six swaps',1.3)*6);rack(a,162,255,'B'*b+'A'*(10-b));meter(a,777,247,50+2*b)
        label(a,'50 + 2 × 6 = 62 mA',636,509,42,SEA,c.reveal('six blue lamps'),'center')
    else:
        meter(a,111,218,63);label(a,'Possible readings from ten lamps',500,250,36,PAPER,c.reveal('different arrangement'))
        label(a,'50   52   54   56   58   60   62   64   66   68   70',640,412,32,SEA,c.reveal('add two'),'center')
        label(a,'63 falls between two possible readings.',640,517,37,RED,c.reveal('Every possible reading is even'),'center')

def poster(draw):return draw(4,1)
