"""Successive ticket prices, a common scoreboard and two reversible strip models."""
from fractions import Fraction

BACKGROUND = ("#eee7d8", "#d9e5d8")
INK, RULE, GOLD, TEAL, RED = "#20372f", "#54796b", "#e9b954", "#207c70", "#ac4238"
BRIDGE = "The bicycle costs $360 after the sale. Which three equal shares does that ticket buy, and what did one share cost before the discount?"
HEAD = ("One tag, two prices","Choose the bottom number","Compare the teams","Give the scores one scale","The missing ticket","Rebuild the sale price","Rebuild the opening price","Name a whole")


def check_maths():
    assert Fraction(18,24) == Fraction(3,4) > Fraction(28,40)
    assert 400 * Fraction(6,5) * Fraction(3,4) == 360


def tag(a,x,y,title,price,alpha=1):
    a.box(x,y,310,150,fill="#fffcf3",edge=RULE,stroke=3,radius=14)
    a.dot(x+23,y+25,8,RULE)
    a.text(title,x+155,y+42,25,INK,bold=True)
    a.text(price,x+155,y+106,54,TEAL,bold=True,opacity=alpha)


def strip(a,x,y,n,filled,width=100):
    for i in range(n):
        a.box(x+i*width,y,width-4,52,fill=TEAL if i<filled else "#e4c69e",edge=RULE,radius=3)
    a.text(f"{filled} of {n} shares",x+n*width/2,y+82,26,INK)


def draw(a,n,c):
    a.text(HEAD[n-1],62,73,46,INK,bold=True,align="left")
    a.line([(62,124),(1217,124)],RULE,3)
    if n in (1,2):
        tag(a,145,163,"Original","$50");tag(a,829,163,"Sale","$40")
        a.arrow((484,235),(786,235),RED,c.reveal("Forty" if n==1 else "Cross off"),5)
        strip(a,372,368,5,4,108)
        cue="Ten dollars" if n==1 else "twenty five percent"
        a.text("$10 removed" if n==1 else "$10 ÷ $50 = 20%    •    $10 ÷ $40 = 25%",641,519,40,INK,bold=True,opacity=c.reveal(cue))
    elif n in (3,4):
        for y,title,correct,total,colour in ((198,"Red",18,24,RED),(350,"Blue",28,40,TEAL)):
            a.text(f"{title}   {correct} / {total}",84,y+38,34,INK,align="left",bold=True)
            a.box(365,y,680,64,fill="#f9f6e8",edge=RULE,radius=4,stroke=2)
            a.box(366,y+1,678*correct/total,62,fill=colour,radius=3)
            if n==4:a.text(f"{correct*100//total}%",1114,y+33,37,INK,bold=True,opacity=c.reveal("seventy five" if title=="Red" else "seventy out"))
        if n==4:a.text("5 percentage points",640,520,39,INK,bold=True,opacity=c.reveal("five percentage points"))
    else:
        prices={5:("?", "?", "$360"),6:("?", "$480", "$360"),7:("$400","$480","$360"),8:("$400","$480","$360")}[n]
        for i,(heading,price) in enumerate(zip(("Original","After rise","After sale"),prices)):
            alpha=c.reveal("four hundred dollars") if n==7 and i==0 else c.reveal("four hundred and eighty") if n==6 and i==1 else 1
            tag(a,76+i*409,160,heading,price,alpha)
        for x,cap in ((389,"+20%"),(798,"−25%")):
            a.text(cap,x+48,361,33,INK,bold=True)
        if n==6:
            strip(a,412,409,4,3,115);a.text("1 share = $120",640,551,34,INK,opacity=c.reveal("one hundred and twenty"))
        elif n==7:
            strip(a,352,409,6,5,96);a.text("1 share = $80",640,551,34,INK,opacity=c.reveal("eighty dollars"))
        else:
            a.text("Which price is 100% before the discount?" if n==5 else "Rise uses $400.   Sale uses $480.",640,462,36,INK,bold=True)


def poster(draw):
    return draw(6,1)
