"""Cups, bowls and groups of four clay pieces changing a kiln's dot count."""
from fractions import Fraction
BACKGROUND=('#47332e','#2a282b')
PAPER,CLAY,PALE,BLUE,GOLD,RED,DARK,LINE='#fff2d7','#d28e74','#e6c8a5','#77d3df','#efd089','#f4a68e','#312b32','#967f75'
BRIDGE='At the kiln, four pale pieces have one dot and four dark pieces have three dots. What happens to the number of dots when you exchange one group of four?'
HEAD=('Which pots have a glaze?','Count before combining','Mix two sample crates','Every pot gets one vote','Two clay types, one label','Start at the lower rate','Swap a group of four','Open both kiln shelves')
def check_maths():
    assert Fraction(12,4)==3 and Fraction(4,2)==2 and Fraction(3+2,16)==Fraction(5,16)
    assert Fraction(8//2+16//4,8+16)==Fraction(1,3)
    valid=[d for d in range(0,41,4) if Fraction(3*d,4)+Fraction(40-d,4)==18]
    assert valid==[16] and 16*3//4==12 and 24//4==6
def text(a,s,x,y,size=36,col=PAPER,t=1):
    a.text(str(s),x,y,size,col,bold=True,opacity=t)
def pot(a,x,y,colour,mark=False,shape='cup'):
    if shape=='cup':
        a.box(x+8,y-10,15,17,radius=6,fill=DARK,edge=colour,stroke=4)
        a.box(x-17,y-17,33,30,radius=7,fill=colour)
    else:
        a.polygon([(x-20,y-13),(x+20,y-13),(x+13,y+8),(x+7,y+13),(x-9,y+13),(x-15,y+7)],colour)
    if mark:
        a.dot(x,y-2,8,'#22556c');a.dot(x,y-2,4,'#86deeb')
def shelf(a,x,y,count,mark,label,shape,col=PALE):
    if label:a.label(label,x-13,y-58,29,PAPER,bold=True)
    for i in range(count):pot(a,x+54*(i%8),y+56*(i//8),col,i<mark,shape)
    for row in range((count+7)//8):
        w=54*min(8,count-8*row)
        a.line([(x-23,y+20+56*row),(x+w-25,y+20+56*row)],LINE,4)
def grouped(a,y,dark_groups):
    for g in range(10):
        x=145+106*g;dark=g<dark_groups;col=CLAY if dark else PALE
        a.box(x-40,y-38,86,90,radius=7,fill='#3c3334',edge=LINE)
        for i in range(4):
            xx=x+(i%2)*34-13;yy=y+(i//2)*32-11
            a.dot(xx,yy,13,col);a.dot(xx,yy,7,'#1b5369' if i<(3 if dark else 1) else col)
def draw(a,n,c):
    a.label(HEAD[n-1],64,72,44,PAPER,bold=True);a.line([(64,124),(1216,124)],LINE,3)
    if n in (1,2):
        marked=n==2 or c.reveal('blue glaze')>.9
        shelf(a,162,266,12,3 if marked else 0,'12 cups','cup')
        shelf(a,821,266,4,2 if marked else 0,'4 bowls','bowl')
        if n==1:
            text(a,'¼ of the cups',355,423,36,BLUE,c.reveal('one quarter'))
            text(a,'½ of the bowls',907,423,36,BLUE,c.reveal('half have'))
            text(a,'Which shelf holds more blue pieces?',640,532,37,GOLD,c.reveal('larger blue fraction'))
        else:
            text(a,'3 blue cups',351,420,38,BLUE);text(a,'2 blue bowls',912,420,38,BLUE)
            text(a,'5 blue pieces out of 16',640,531,39,GOLD,c.reveal('five blue pieces'))
    elif n in (3,4):
        shelf(a,164,266,8,4,'8 cups','cup')
        shelf(a,710,266,16,4,'16 bowls','bowl')
        if n==3:text(a,'What fraction of all 24 pieces has glaze?',640,510,37,GOLD,c.reveal('all the pottery'))
        else:
            text(a,'4 glazed cups + 4 glazed bowls',640,434,37,BLUE,c.reveal('also contributes four'))
            text(a,'8 out of 24 = ⅓',640,536,43,GOLD,c.reveal('one third'))
    elif n==5:
        shelf(a,210,267,4,3,'Dark clay','cup',CLAY);shelf(a,785,267,4,1,'Pale clay','cup')
        text(a,'3 dots per 4 pieces',302,361,32,BLUE);text(a,'1 dot per 4 pieces',883,361,32,BLUE)
        text(a,'40 pieces in the kiln, 18 with dots.',640,462,38,GOLD,c.reveal('eighteen pieces'))
        text(a,'How many are dark clay?',640,543,34,PAPER,c.reveal('How many dark'))
    elif n==6:
        grouped(a,278,0)
        text(a,'40 pale pieces = 10 groups of four',640,403,36,PAPER,c.reveal('quarter of forty'))
        text(a,'18 actual dots − 10 baseline dots = 8 extra',640,523,37,GOLD,c.reveal('eight extra dots'))
    elif n==7:
        t=c.reveal('switch four groups',1.4)
        grouped(a,277,round(4*t))
        text(a,'One group gains 3 − 1 = 2 dots',640,405,39,BLUE,c.reveal('adds two dots'))
        text(a,'4 switched groups × 4 pieces = 16 dark pieces',640,522,34,GOLD,c.reveal('sixteen dark pieces'))
    else:
        grouped(a,272,4)
        text(a,'Dark clay: ¾ × 16 = 12 dotted',640,394,35,CLAY,c.reveal('twelve dark'))
        text(a,'Pale clay: ¼ × 24 = 6 dotted',640,454,35,PALE,c.reveal('six pale'))
        text(a,'12 + 6 = 18 dotted pieces',640,547,38,BLUE,c.reveal('restores eighteen'))
def poster(draw):return draw(9,1)
