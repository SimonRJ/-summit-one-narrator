"""Graduated bottle volumes, receipts and minimum whole-bottle orders."""
from fractions import Fraction
from math import ceil
BACKGROUND=('#34443c','#21342f')
PAPER,BIG,SMALL,GOLD,INK,LINE='#fff4d9','#a4dec1','#b5d7f0','#efc77e','#254033','#6d897a'
HEAD=('Two labels use different wholes','Fill the first jug','Change the second price','Put equal volumes on the bench','The order must use whole bottles','Fill the school order','Where did forty cents come from?','An order that exactly fits')
BRIDGE='Place 100 mL from each offer side by side. Why can two offers have the same price for that amount but different bills for the school’s 2500 mL order?'
def check_maths():
    assert 600*Fraction(3,2)==900 and 240*Fraction(2,3)==160
    assert Fraction(360,900)==Fraction(160,400)==Fraction(2,5)
    assert [(ceil(2500/v),ceil(2500/v)*price) for v,price in [(900,360),(400,160)]]==[(3,1080),(7,1120)]
    assert 4*900==9*400==3600 and 4*360==9*160==1440
def txt(a,s,x,y,size=35,k=PAPER,t=1):a.text(str(s),x,y,size,k,bold=True,opacity=t)
def jug(a,cx,ml,col,label):
    x,y,w,h=cx-66,229,132,198
    a.box(x,y,w,h,fill='#263e36',edge=PAPER,stroke=3,radius=9)
    fill=(h-8)*ml/1000;a.box(x+5,y+h-fill-4,w-10,fill,radius=2,fill=col)
    for m in range(100,1001,100):
        yy=y+h-4-(h-8)*m/1000
        a.line([(x+w-20,yy),(x+w-5,yy)],PAPER,2)
    txt(a,label,cx,y+h+43,32,col)
def bottles(a,x,y,n,col):
    for i in range(n):
        xx=x+i*72
        a.box(xx-10,y-32,20,15,fill=col,radius=3)
        a.box(xx-22,y-19,44,56,fill=col,edge=PAPER,radius=9)
def draw(a,n,c):
    a.label(HEAD[n-1],64,70,43,PAPER,bold=True);a.line([(64,125),(1216,125)],LINE,3)
    if n in (1,2,3):
        if n==1:
            jug(a,325,600,BIG,'600 mL');jug(a,937,400,SMALL,'400 mL')
            txt(a,'Extra liquid',325,180,34,BIG);txt(a,'Price reduction',937,180,34,SMALL)
            txt(a,'What is the whole in each offer?',640,554,35,GOLD,c.reveal('Which parts'))
        elif n==2:
            jug(a,340,600+300*c.reveal('adds three hundred',1.6),BIG,'Large bottle')
            txt(a,'600 mL + 300 mL = 900 mL',873,307,34,BIG,c.reveal('nine hundred millilitres'))
            txt(a,'The price stays $3.60.',872,418,36,GOLD,c.reveal('same'))
        else:
            jug(a,339,400,SMALL,'400 mL')
            txt(a,'Normal price: $2.40',891,263,38,PAPER)
            txt(a,'One third off: 80 cents',895,348,34,GOLD,c.reveal('eighty cents'))
            txt(a,'Sale price: $1.60',891,437,38,SMALL,c.reveal('one dollar sixty'))
    elif n==4:
        for i,(cap,vol,price,col) in enumerate([('Large',900,360,BIG),('Small',400,160,SMALL)]):
            y=233+i*157;txt(a,cap,166,y,31,col)
            for j in range(vol//100):a.box(289+j*66,y-25,56,48,fill=col,radius=3)
            txt(a,f'{price} cents ÷ {vol//100} groups',574,y+66,29,col)
        txt(a,'Both cost 40 cents per 100 mL.',640,555,38,GOLD,c.reveal('also gives forty'))
    elif n==5:
        txt(a,'School order: at least 2500 mL',640,245,45,GOLD,c.reveal('at least'))
        bottles(a,245,373,3,BIG);bottles(a,794,373,4,SMALL)
        txt(a,'900 mL per large bottle',315,475,29,BIG);txt(a,'400 mL per small bottle',887,475,29,SMALL)
    elif n==6:
        bottles(a,160,240,3,BIG);txt(a,'3 × 900 = 2700 mL',667,238,33,BIG,c.reveal('Three hold'))
        txt(a,'$10.80',1060,238,40,BIG,c.reveal('cost ten dollars eighty'))
        bottles(a,160,393,7,SMALL);txt(a,'2800 mL',850,392,32,SMALL,c.reveal('twenty eight hundred'))
        txt(a,'$11.20',1060,392,40,SMALL,c.reveal('eleven dollars twenty'))
        txt(a,'40 cents less with three large bottles',640,552,35,GOLD,c.reveal('forty cents less'))
    elif n==7:
        for i,(v,col) in enumerate([(2700,BIG),(2800,SMALL)]):
            x,y=190,246+133*i
            a.box(x,y,750,47,fill=col,radius=3)
            a.box(x+753,y,(v-2500)*.3,47,fill=GOLD,radius=3)
            txt(a,f'{v-2500} mL surplus',1046,y+74,27,GOLD)
        txt(a,'2500 mL target',537,202,32,PAPER)
        txt(a,'100 mL of extra soap costs 40 cents.',640,553,34,GOLD,c.reveal('exactly forty cents'))
    else:
        bottles(a,166,231,4,BIG);txt(a,'4 × 900 = 3600 mL',876,232,36,BIG,c.reveal('Four large'))
        bottles(a,165,377,9,SMALL);txt(a,'9 × 400 = 3600 mL',970,378,30,SMALL,c.reveal('Nine small'))
        txt(a,'Both bills: $14.40',640,534,45,GOLD,c.reveal('fourteen dollars forty'))
def poster(draw):return draw(9,1)
