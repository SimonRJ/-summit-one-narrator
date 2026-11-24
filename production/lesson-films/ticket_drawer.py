"""A drawer of 24 counterfoils carries both a ticket count and a till amount."""
from stage import clamp
BACKGROUND=('#382d3a','#26263a')
BRIDGE='In the film’s ticket office, there are 24 tickets in all. If x are adult tickets, why can 24 − x stand for the child tickets? Write a money total and check the units of each term.'
HEAD=('Twenty-four counterfoils','Name one unknown','Read the till','Fill the drawer with child tickets','Upgrade one counterfoil','Restore the actual sale','The exchange window','Check tickets and dollars separately')
PAPER,GOLD,LILAC,SEA,DIM='#f9f1de','#efc374','#c8b6e9','#8ed3bd','#796c80'


def check_maths():
    assert [(a,24-a) for a in range(25) if 8*a+5*(24-a)==150]==[(10,14)]
    assert (10-2)+(14+3)==25 and 8*8+17*5==149


def label(a,s,x,y,size=35,col=PAPER,t=1,align='left'):
    a.label(s,x,y,size,col,t,align=align,bold=True)


def drawer(a,adults=0,children=24,unknown=False):
    a.box(68,174,588,380,radius=18,fill='#493e48',edge=DIM,stroke=3)
    for i in range(adults+children):
        x,y=93+i%6*90,202+i//6*73
        col=GOLD if i<adults else LILAC if not unknown else PAPER
        a.box(x,y,75,52,radius=4,fill=col)
        a.line([(x+15,y+6),(x+15,y+45)],'#59474e',2)
        a.text('A' if i<adults else 'C' if not unknown else '•',x+44,y+27,24,'#362d3a',bold=True)


def draw(a,n,c):
    label(a,HEAD[n-1],72,70,46);a.line([(72,120),(1205,120)],DIM,2)
    if n==1:
        drawer(a,unknown=True)
        label(a,'24 tickets',711,251,49,GOLD,c.reveal('twenty-four counterfoils'))
        label(a,'Adult or child?',711,391,40,PAPER,c.reveal('adult tickets'))
    elif n==2:
        r=c.reveal('Try x equal to six');drawer(a,6,18) if r>=.5 else drawer(a,unknown=True)
        label(a,'Adult tickets: x',704,240,38,GOLD);label(a,'Child tickets: 24 − x',704,352,36,LILAC,c.reveal('twenty-four minus x'))
        label(a,'6 + 18 = 24',704,478,39,PAPER,c.reveal('eighteen children'))
    elif n==3:
        drawer(a,unknown=True);label(a,'Adult $8     Child $5',685,217,36,GOLD,c.reveal('five dollars'))
        label(a,'8x + 5(24 − x)',706,348,42,PAPER,c.reveal('Multiply each price'))
        label(a,'Till total: $150',706,476,38,SEA,c.reveal('one hundred and fifty'))
    elif n==4:
        drawer(a);label(a,'24 × $5 = $120',697,238,39,LILAC,c.reveal('one hundred and twenty dollars'))
        label(a,'Till total: $150',703,341,38,PAPER,c.reveal('actual till total'))
        label(a,'Difference: $30',703,462,38,SEA,c.reveal('missing thirty dollars'))
    elif n==5:
        t=c.reveal('adult ticket');drawer(a,round(t),24-round(t))
        label(a,'1 C becomes 1 A',705,219,38,GOLD,t)
        label(a,'Still 24 tickets',705,332,37,PAPER,c.reveal('still contains'))
        label(a,'$8 − $5 = $3',705,457,41,SEA,c.reveal('eight minus five'))
    elif n==6:
        r=c.reveal('Ten changes',1.4);adt=round(r*10);drawer(a,adt,24-adt)
        label(a,'10 adults → $80',705,224,37,GOLD,c.reveal('eighty dollars'))
        label(a,'14 children → $70',705,334,37,LILAC,c.reveal('seventy dollars'))
        label(a,'24 tickets   •   $150',684,478,35,SEA,c.reveal('two counts'))
    elif n==7:
        label(a,'Returned',138,211,34,GOLD);label(a,'Sold',724,211,34,LILAC)
        label(a,'−2 adults',139,326,50,PAPER,c.reveal('two adults return'))
        label(a,'+3 children',721,326,50,PAPER,c.reveal('Three children'))
        label(a,'One more sale. What happens to the till?',640,505,37,SEA,c.reveal('one extra sale'),'center')
    else:
        label(a,'Tickets',119,205,32,GOLD);label(a,'10 − 2 = 8',120,300,43,GOLD,c.reveal('drops from ten to eight'))
        label(a,'14 + 3 = 17',710,300,43,LILAC,c.reveal('rises from fourteen to seventeen'))
        label(a,'8 + 17 = 25 tickets',119,402,41,PAPER,c.reveal('twenty-five tickets'))
        label(a,'$150 − $16 + $15 = $149',119,520,44,SEA,c.reveal('one hundred and forty-nine'))


def poster(draw):return draw(3,1)
