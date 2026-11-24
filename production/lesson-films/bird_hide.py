"""Seed piles and overlapping brackets on an observation rail."""
from fractions import Fraction
BACKGROUND=('#354032','#20322b')
PAPER,GOLD,SKY,RED,ROAD,GREEN='#fff1d2','#edc67a','#a5d5e2','#f19f87','#748b77','#b1dda1'
BRIDGE='Put a finger on each end of the bird hide’s two observation brackets. Which tally gets included a second time when you add their totals?'
HEAD=('Level the feeding trays','Build a total from the mean','Two lengths of observation','Restore both totals','One missing rail tag','Lay the brackets over the rail','Subtract the whole morning','Count what each bracket sees')
def check_maths():
    assert sum((2,4,6))/3==4 and 5*7==35
    assert (2*9+4*3)/6==5
    readings=[8,10,12,14,13,15]
    assert sum(readings)==6*12 and sum(readings[:4])==4*11 and sum(readings[-3:])==3*14
    assert 4*11+3*14-6*12==readings[3]
def text(a,s,x,y,size=36,col=PAPER,t=1):
    a.text(str(s),x,y,size,col,bold=True,opacity=t)
def seed(a,x,y,col,t=1):
    a.box(x-14,y-7,27,14,fill=col,radius=7,opacity=t)
def tray(a,x,y,count,col,i=0):
    a.box(x-69,y,138,16,fill=ROAD,radius=6);a.line([(x-59,y-13),(x-52,y+4),(x+55,y+4),(x+63,y-13)],PAPER,3)
    for k in range(count):
        seed(a,x+(k%2*35-17),y-15-22*(k//2),col)
def bracket(a,y,left,right,label,col,t):
    a.line([(left,y+9),(left,y),(right,y),(right,y+9)],col,5,t)
    text(a,label,(left+right)/2,y-34,30,col,t)
def rail(a,y,values):
    a.line([(100,y-80),(1180,y-80)],ROAD,8)
    for i,v in enumerate(values):
        x=180+184*i;a.line([(x,y-80),(x,y-48)],GOLD,4)
        a.box(x-66,y-47,132,95,fill='#e9d9b6' if v!='?' else GOLD,radius=7)
        text(a,v,x,y,40,'#27362c');text(a,'Period '+str(i+1),x,y+79,24,PAPER)
def draw(a,n,c):
    a.label(HEAD[n-1],64,72,44,PAPER,bold=True);a.line([(64,124),(1216,124)],ROAD,3)
    if n==1:
        # Two seeds travel from the third tray to the first, keeping the total visible.
        for i,k in enumerate((2,4,4)):tray(a,310+330*i,377,k,GOLD)
        t=c.reveal('Move two seeds',1.6)
        for k in range(2):seed(a,970+(k*35-17)-660*t,318-85*4*t*(1-t)+22*t,GOLD)
        text(a,'2 + 4 + 6 = 12 seeds',640,483,39,PAPER,1-t)
        text(a,'12 seeds shared across 3 trays = 4 each',640,500,36,GREEN,c.reveal('mean describes'))
    elif n==2:
        for i in range(5):tray(a,206+i*217,367,7,GOLD)
        text(a,'5 trays × 7 seeds = 35 seeds',640,505,41,GREEN,c.reveal('thirty five'))
    elif n in (3,4):
        text(a,'Imagine all periods at their own group mean',640,180,29,PAPER)
        for i in range(6):
            x=186+183*i;col=SKY if i<2 else GOLD
            a.box(x-58,253,116,96,radius=5,fill=col);text(a,9 if i<2 else 3,x,300,47,'#25372c')
        text(a,'2 periods at mean 9',276,409,29,SKY);text(a,'4 periods at mean 3',829,409,29,GOLD)
        if n==3:text(a,'How should six periods affect the mean?',640,534,34,PAPER,c.reveal('making a prediction'))
        else:text(a,'(18 + 12) ÷ 6 = 5 visits per period',640,531,38,GREEN,c.reveal('mean is five'))
    else:
        values=['–','–','–','?','–','–']
        if n==8:values=[8,10,12,14,13,15]
        if n==7 and c.reveal('fourteen visits')>.5:values[3]=14
        rail(a,341,values)
        if n in (5,6,8):
            ky='first four' if n!=6 else 'first bracket'
            bracket(a,223,115,798,'First four: mean 11' if n==5 else 'First four: total 44',SKY,c.reveal(ky))
            cue='last three' if n!=6 else 'last bracket'
            a.line([(671,440),(671,456),(1168,456),(1168,440)],GOLD,4,c.reveal(cue))
            text(a,'Last three: mean 14' if n==5 else 'Last three: total 42',919,491,30,GOLD,c.reveal(cue))
            if n==5:text(a,'Whole morning: mean 12',640,562,32,PAPER,c.reveal('mean over all six'))
            if n==6:text(a,'44 + 42 = 86, with period 4 counted twice',640,564,32,PAPER,c.reveal('eighty six'))
            if n==8:text(a,'The fourth observation is fixed.',640,565,32,GREEN,c.reveal('overlap total is fixed'))
        else:
            text(a,'6 periods × mean 12 = 72 visits',640,193,36,SKY,c.reveal('seventy two'))
            text(a,'86 − 72 = 14',640,517,48,GREEN,c.reveal('Eighty six minus'))
def poster(draw):return draw(6,1)
