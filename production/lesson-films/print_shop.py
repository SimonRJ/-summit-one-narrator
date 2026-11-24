"""Press sheets, common-denominator rulers and reversible price tags."""
from fractions import Fraction
from math import sin, cos, pi
from stage import blend
BACKGROUND=('#243946','#172933')
INK,PAPER,SKY,RED,GOLD,GREEN='#172d39','#fff2db','#95d8f5','#f2a18b','#f1c275','#a3d9b8'
BRIDGE='Pause when the price tag turns from $80 to $100. To undo the $20 rise, which price belongs under the fraction bar on the sale sticker?'
HEAD=('A percentage has a base','Use copies of equal size','Which machine wastes less?','Compare one hundred sheets','Reverse a price rise','Find the new whole','Try using the old rate','Choose a strip of ten')
def check_maths():
    assert Fraction(10,50)==Fraction(20,100)
    assert Fraction(3,20)==Fraction(15,100)<Fraction(16,100)==Fraction(4,25)
    assert 80*Fraction(5,4)==100 and 100*Fraction(4,5)==80 and 100*Fraction(3,4)==75
    assert 50*Fraction(6,5)*Fraction(5,6)==50
def text(a,s,x,y,size=36,col=PAPER,t=1):
    a.text(str(s),x,y,size,col,bold=True,opacity=t)
def sheet(a,x,y,rows,marked,label,t=1):
    if t<=0:return
    a.box(x-15,y-14,248,rows*19+25,radius=4,fill=PAPER,opacity=t)
    for i in range(10*rows):
        cx=x+12+22*(i%10);cy=y+9+19*(i//10)
        points=[(cx+(8 if j%2==0 else 3.5)*cos(j*pi/5-pi/2), cy+(8 if j%2==0 else 3.5)*sin(j*pi/5-pi/2)) for j in range(10)]
        a.polygon(points,blend('#f5ebd6', '#ac690b' if i<marked else '#527989',t))
    text(a,label,x+106,y+rows*19+54,32,PAPER,t)
def tag(a,x,y,label,colour,t=1):
    a.box(x-120,y-49,240,98,radius=17,fill=colour,opacity=t)
    text(a,label,x,y,48,INK,t)
def scale(a,x,y,f,col,cap,t):
    a.line([(x,y),(x+564,y)],PAPER,4,t)
    for k in range(0,101,10):
        pos=x+5.64*k;a.line([(pos,y-5),(pos,y+10)],PAPER,2,t)
    a.line([(x,y),(x+564*f/100,y)],col,16,t);a.dot(x+564*f/100,y,10,col,t)
    text(a,cap,x+290,y+53,30,col,t)
def draw(a,n,c):
    a.label(HEAD[n-1],64,72,45,PAPER,bold=True);a.line([(64,125),(1216,125)],'#688491',3)
    if n in (1,2):
        sheet(a,160,197,5,10,'10 of 50')
        if n==1:
            sheet(a,857,197,10,20,'20 of 100',c.reveal('large sheet'))
            text(a,'Does the gold share change?',640,536,38,SKY,c.reveal('larger gold percentage'))
        else:
            sheet(a,445,197,5,10,'another 10 of 50',c.reveal('second copy'))
            sheet(a,857,197,10,20,'20 of 100',c.reveal('among one hundred'))
            text(a,'10 ÷ 50 = 20 ÷ 100',640,542,40,GREEN,c.reveal('proportions match'))
    elif n in (3,4):
        for i,(label,num,den,col) in enumerate([('Press A',3,20,SKY),('Press B',4,25,RED)]):
            y=215+i*147
            text(a,label,210,y,34,col)
            if n==3:
                for k in range(den):a.dot(390+(k%13)*48,y-13+(k//13)*33,11,col if k<num else '#667b82')
                text(a,f'{num} spoiled out of {den}',665,y+77,30,PAPER)
            else:
                val=15+i;t=c.reveal('fifteen sheets' if i==0 else 'sixteen')
                scale(a,360,y,val,col,f'{val} spoiled per 100 sheets',t)
        text(a,'Which rate is smaller?' if n==3 else '15% < 16%',640,549,41,GREEN,c.reveal('decide fairly') if n==3 else c.reveal('smaller share'))
    else:
        if n==5:
            tag(a,285,272,'$80',SKY);tag(a,930,272,'Sale: ?',GOLD,c.reveal('During a sale'))
            a.arrow((429,272),(779,272),PAPER,c.reveal('one quarter'),4)
            text(a,'Increase by ¼',620,220,32,PAPER,c.reveal('one quarter'))
            text(a,'Which discount returns the price to $80?',640,484,35,GREEN,c.reveal('What percentage'))
        elif n==6:
            tag(a,260,245,'$80',SKY);a.arrow((402,245),(496,245),PAPER,c.reveal('twenty dollars'),4)
            tag(a,640,245,'$100',GOLD,c.reveal('one hundred'));a.arrow((778,245),(883,245),PAPER,c.reveal('remove twenty'),4)
            tag(a,1025,245,'$80',SKY,c.reveal('back to eighty'))
            text(a,'$20 ÷ $100 = 20%',640,459,47,GREEN,c.reveal('Twenty out of'))
        elif n==7:
            tag(a,345,245,'$100',GOLD);tag(a,930,245,'$75',RED,c.reveal('leaves seventy five'))
            a.arrow((485,245),(778,245),RED,c.reveal('removes twenty five'),5)
            text(a,'A 25% sale takes $25 from $100',640,395,37,PAPER,c.reveal('twenty five dollars'))
            text(a,'The target price was $80.',640,506,37,SKY,c.reveal('too far'))
        else:
            for i in range(6):
                t=1 if i<5 else c.reveal('goes up')
                a.box(157+i*162,220,155,103,radius=4,fill=SKY if i<5 else GOLD,opacity=t)
                text(a,'$10',232+i*162,270,40,INK,t)
            text(a,'$50 + $10 = $60',640,409,39,PAPER,c.reveal('sixty'))
            text(a,'Return $10 out of $60: ⅙ of the higher price',640,522,35,GREEN,c.reveal('one sixth'))
def poster(draw):return draw(8,1)
