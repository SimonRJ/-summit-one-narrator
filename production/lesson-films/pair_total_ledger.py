"""S095, an illustrated ticket-office ledger with colour, point, seat and parity checks."""
from itertools import product

BACKGROUND=('#faf6e9','#e5e9dd')
BRIDGE='Watch what changes when a plain ticket becomes a star ticket. Later, use the same idea to count only the extra seats in each matched pair.'
INK='#263e40';BLUE='#396189';YELLOW='#e1b24e';JADE='#2c756b';RUST='#a74c36';PAPER='#fffaf1';RULE='#9aa99e'
TITLES=['Count the two ticket colours','Unfold five matching groups','Price a bundle in points',
        'Change one ticket at a time','Sort three kinds of travel ticket','Match the extra seats',
        'Audit both columns of the ledger','Catch a report that cannot balance']


def check_maths():
    assert [(b,y) for b,y in product(range(21),repeat=2) if b+y==20 and y==3*b]==[(5,15)]
    assert [(p,s) for p,s in product(range(8),repeat=2) if p+s==7 and p+4*s==19]==[(3,4)]
    assert [(s,d,f) for s,d,f in product(range(17),repeat=3) if s+d+f==16 and s+2*d+4*f==36 and d==f]==[(6,5,5)]
    assert 12+15+20==47 and not [(a,b,c) for a,b,c in product(range(21),repeat=3) if (a+b,b+c,c+a)==(12,15,20)]


def text(a,s,x,y,size=32,col=INK,op=1):
    a.text(s,x,y,size,col,bold=True,opacity=op)


def paper(a,x,y,w,h):
    a.box(x+4,y+5,w,h,fill='#adbaae',radius=10);a.box(x,y,w,h,fill=PAPER,edge=RULE,radius=10)


def ticket(a,x,y,w,h,fill,mark,op=1):
    a.box(x,y,w,h,fill=fill,edge=INK,radius=7,stroke=2,opacity=op)
    for edge in (x,x+w):a.dot(edge,y+h/2,h*.095,PAPER,op)
    if mark:
        ink=PAPER if fill in (BLUE,JADE,RUST) else INK
        text(a,mark,x+w/2,y+h/2,min(30,h*.63),ink,op)


def pass_type(a,x,y,seats,op=1):
    colors={1:BLUE,2:JADE,4:RUST}
    ticket(a,x,y,143,83,colors[seats],str(seats),op)


def draw(a,n,t):
    a.label(TITLES[n-1],77,74,45,INK,bold=True);a.line([(75,119),(1204,119)],RULE,3)
    if n in (1,2):
        paper(a,78,158,1124,363)
        if n==1:
            a.label('Ticket envelope',126,208,33,INK,bold=True)
            for j,shade in enumerate((BLUE,YELLOW,YELLOW,YELLOW)):
                ticket(a,156+112*j,289,90,70,shade,'B' if j==0 else 'Y',t.reveal('For every blue ticket'))
            text(a,'20 tickets in all',924,306,43,INK,t.reveal('twenty tickets'))
            text(a,'How many blue and yellow?',640,568,37,JADE,t.reveal('How many tickets'))
        else:
            for j in range(5):
                op=1 if j==0 else t.reveal('five complete groups',1.65,offset=.15*j)
                px=121+j*214
                a.box(px,239,180,166,radius=10,fill='#ececdf',edge=RULE,opacity=op)
                for k,col in enumerate((BLUE,YELLOW,YELLOW,YELLOW)):
                    ticket(a,px+13+(k%2)*80,259+(k//2)*60,71,51,col,'B' if k==0 else 'Y',op)
            text(a,'20 ÷ 4 = 5 groups',640,463,40,INK,t.reveal('five complete groups'))
            text(a,'5 blue + 15 yellow = 20 tickets',640,568,38,JADE,t.reveal('five blue tickets'))
    elif n in (3,4):
        paper(a,78,152,1124,349)
        ticket(a,146,194,103,68,'#e9e7d9','1');a.label('Plain · 1 point',275,229,31,INK)
        ticket(a,705,194,103,68,RUST,'★');a.label('Star · 4 points',830,229,31,INK)
        if n==3:
            fill=t.reveal('making all seven plain',1.0)
            for j in range(7):ticket(a,153+j*142,353,108,66,'#e9e7d9','1' if fill>.5 else '?')
            text(a,'7 tickets give 19 points',640,562,39,JADE,t.reveal('worth nineteen points'))
        else:
            one=t.reveal('Replace one plain ticket',.75)
            change=t.reveal('Four replacements',1.5)
            for j in range(7):
                op=one if j==0 else t.reveal('Four replacements',.65,offset=.2*j) if j<4 else 0
                ticket(a,153+j*142,350,108,66,'#e9e7d9','1')
                ticket(a,153+j*142,350,108,66,RUST,'★',op)
            text(a,'19 − 7 = 12 extra points',640,466,31,INK,t.reveal('twelve more'))
            text(a,'4 × 4 + 3 × 1 = 19',640,566,39,JADE,t.reveal('Four stars'))
            if one>.3 and change<.4:text(a,'4 − 1 = 3 extra',640,566,39,RUST,t.reveal('gain three points'))
    elif n==5:
        paper(a,80,155,1120,370)
        text(a,'16 tickets',345,218,42,INK,t.reveal('sixteen tickets'))
        text(a,'36 seats',927,218,42,JADE,t.reveal('thirty six seats'))
        for j,num in enumerate((1,2,4)):
            x=219+j*338;pass_type(a,x,285,num)
            text(a,str(num)+' seat'+('' if num==1 else 's'),x+72,412,30,INK)
        a.line([(617,462),(617,484),(963,484),(963,462)],RUST,3,t.reveal('Just as many'))
        text(a,'Equal numbers of 2-seat and 4-seat tickets',640,568,34,RUST,t.reveal('Just as many'))
    elif n==6:
        paper(a,77,148,1126,382)
        text(a,'Start with one seat on each ticket',374,203,29,INK)
        for j in range(16):
            x=150+(j%8)*61;y=273+(j//8)*64
            a.box(x,y,46,44,fill=BLUE,edge=INK,radius=5)
            a.line([(x+9,y+17),(x+9,y+31),(x+35,y+31)],PAPER,3)
        text(a,'36 − 16 = 20 extra seats',365,449,33,JADE,t.reveal('twenty extra seats'))
        a.line([(653,199),(653,482)],RULE,2)
        op=t.reveal('Match each two seat ticket');pass_type(a,736,262,2,op);pass_type(a,970,262,4,op)
        text(a,'+1',809,389,34,JADE,t.reveal('one plus three'));text(a,'+3',1043,389,34,RUST,t.reveal('one plus three'))
        text(a,'4 extra seats per pair',927,459,29,INK,t.reveal('one plus three extra seats'))
        text(a,'20 ÷ 4 = 5 matched pairs',640,572,40,JADE,t.reveal('Twenty divided by four'))
    elif n==7:
        paper(a,100,146,1080,395)
        for x,label in [(310,'Ticket type'),(674,'Tickets sold'),(980,'Seats covered')]:text(a,label,x,197,29,INK)
        for j,(name,count,seats,colour,cue) in enumerate([('Single',6,6,BLUE,'remaining six'),('Double',5,10,JADE,'Five two seat'),('Four-seat',5,20,RUST,'five four seat')]):
            y=267+j*83;op=t.reveal(cue)
            a.line([(137,y+39),(1140,y+39)],RULE,2)
            text(a,name,310,y,34,colour,op);text(a,str(count),674,y,38,INK,op)
            text(a,str(seats),980,y,38,colour,t.reveal(('Six singles','ten seats from the doubles','twenty seats from the fours')[j]))
        text(a,'6 + 5 + 5 = 16 tickets',350,572,32,INK,t.reveal('remaining six'))
        text(a,'6 + 10 + 20 = 36 seats',934,572,32,JADE,t.reveal('make thirty six'))
    else:
        paper(a,82,150,585,385)
        for j,(pair,num) in enumerate([('A + B',12),('B + C',15),('C + A',20)]):
            y=214+j*102;text(a,pair,261,y,40,INK,t.reveal('in pairs'))
            text(a,'=',410,y,32,INK,t.reveal('in pairs'));text(a,str(num),538,y,43,RUST,t.reveal(('twelve','fifteen','twenty')[j]))
        text(a,'2 × (A + B + C)',948,252,38,INK,t.reveal('counts each stall twice'))
        text(a,'12 + 15 + 20 = 47',948,342,35,RUST,t.reveal('forty seven'))
        text(a,'47 is odd',948,426,38,RUST,t.reveal('an odd number'))
        text(a,'A doubled whole number must be even',640,572,35,JADE,t.reveal('must be even'))


def poster(draw):
    return draw(8,1.5)
