"""Cumulative entry readings and an intersection falling between whole visit counts."""
from fractions import Fraction
BACKGROUND=("#162c42","#213e4d")
INK, GRID, BLUE, ORANGE, MINT="#f4f3e1","#648292","#79d3f1","#ffd38c","#9bddb8"
BRIDGE="Compare the arrivals using each interval’s own minutes. On the cost chart, can the crossing itself be a legal number of visits?"
HEAD=("Twelve on the dial","Match a row to a point","Find the busiest interval","Give every rise its time","Two ways to pay","Between two visits","What the crossing means","Choose the right reading")
TIMES=(0,2,8,11);TOTALS=(12,24,48,63)


def check_maths():
    assert [Fraction(TOTALS[i+1]-TOTALS[i],TIMES[i+1]-TIMES[i]) for i in range(3)]==[6,4,5]
    v=Fraction(14,7-3);assert v==Fraction(7,2) and 7*v==14+3*v==Fraction(49,2)
    assert all((7*n<14+3*n)==(n<=3) for n in range(30))


def graph(a,kind,n,c):
    x,y,width,height=146,495,585,276
    max_x,max_y=(12,70) if kind=="arrivals" else (6,45)
    X=lambda t:x+t*width/max_x;Y=lambda v:y-v*height/max_y
    xs=(0,2,4,6,8,10,12) if kind=="arrivals" else range(7)
    ys=(0,10,20,30,40,50,60,70) if kind=="arrivals" else (0,10,20,30,40)
    for v in ys:
        a.line([(X(0),Y(v)),(X(max_x),Y(v))],GRID,1);a.text(str(v),x-33,Y(v),19,INK)
    for t in xs:
        a.line([(X(t),y),(X(t),y+8)],INK,2);a.text(str(t),X(t),y+27,20,INK)
    a.line([(x,y-height),(x,y),(x+width,y)],INK,3)
    a.text("Counter reading (visitors)" if kind=="arrivals" else "Total cost ($)",x,174,25,INK,align="left");a.text("Minutes after noon" if kind=="arrivals" else "Number of visits",x+width/2,560,25,INK)
    if kind=="arrivals":
        points=[(X(t),Y(v)) for t,v in zip(TIMES,TOTALS)];a.line(points,BLUE,5)
        for px,py in points:a.dot(px,py,7,ORANGE)
        if n==4:a.line(points[:2],MINT,8)
    else:
        for fixed,rate,col in ((0,7,ORANGE),(14,3,BLUE)):
            a.line([(X(0),Y(fixed)),(X(6),Y(fixed+6*rate))],col,4)
            for t in range(7):a.dot(X(t),Y(fixed+t*rate),5,col)
        if n>=7:
            a.dashed((X(3.5),y),(X(3.5),Y(24.5)),MINT,2);a.dashed((x,Y(24.5)),(X(3.5),Y(24.5)),MINT,2);a.dot(X(3.5),Y(24.5),9,MINT)


def draw(a,n,c):
    a.text(HEAD[n-1],63,72,46,INK,bold=True,align="left");a.line([(63,122),(1215,122)],GRID,3)
    if n==1:
        for x,title,num in ((159,"At noon","12"),(758,"Two minutes later","24")):
            a.box(x,217,359,181,fill="#102638",edge=BLUE,stroke=4,radius=18);a.text(title,x+179,260,30,INK);a.text(num,x+179,343,79,ORANGE,bold=True)
        a.text("How many entries happened between these readings?",640,504,36,INK,bold=True);return
    graph(a,"arrivals" if n<=4 else "cost",n,c)
    if n in (2,3):
        a.text("Minute",841,178,27,INK,bold=True);a.text("Counter",1077,178,27,INK,bold=True)
        for i,(t,total) in enumerate(zip(TIMES,TOTALS)):
            y=239+64*i;a.text(str(t),841,y,32,BLUE,bold=True);a.text(str(total),1077,y,32,ORANGE,bold=True)
        a.text("One row = one reading",967,535,29,INK)
    elif n==4:
        for i,(label,val,word) in enumerate((("0–2 min","12 ÷ 2 = 6","six per minute"),("2–8 min","24 ÷ 6 = 4","four per minute"),("8–11 min","15 ÷ 3 = 5","five per minute"))):
            y=205+i*108;a.text(label,804,y,25,INK,align="left");a.text(val,804,y+46,32,MINT if i==0 else BLUE,bold=True,align="left",opacity=c.reveal(word))
        a.text("Visitors per minute",985,540,29,INK)
    elif n==5:
        for i,(lab,rule,col) in enumerate((("Visitor","$7 per visit",ORANGE),("Member","$14 once + $3 per visit",BLUE))):
            y=240+i*145;a.text(lab,796,y,29,col,bold=True,align="left");a.text(rule,796,y+52,27,INK,align="left")
    elif n==6:
        for j,(v,visitor,member) in enumerate(((3,21,23),(4,28,26))):
            y=207+j*163;a.text(f"{v} visits",800,y,30,INK,bold=True,align="left");a.text(f"Visitor  ${visitor}",800,y+47,27,ORANGE,align="left");a.text(f"Member  ${member}",800,y+87,27,BLUE,align="left")
    elif n==7:
        a.text("Fee gap",812,223,28,INK,align="left");a.text("$14 ÷ $4 = 3½ visits",812,279,33,MINT,bold=True,align="left",opacity=c.reveal("three and a half"));a.text("At the intersection",812,381,28,INK,align="left");a.text("Both lines show $24.50",812,440,31,MINT,bold=True,align="left",opacity=c.reveal("fifty cents"))
    else:
        a.text("Up to 3 whole visits",795,235,30,INK,align="left");a.text("Visitor pays less",795,291,34,ORANGE,bold=True,align="left");a.text("4 whole visits or more",795,393,30,INK,align="left");a.text("Member pays less",795,448,34,BLUE,bold=True,align="left")


def poster(draw):
    return draw(4,1)
