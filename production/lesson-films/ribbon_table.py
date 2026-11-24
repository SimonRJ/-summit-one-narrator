"""Scale drawings of two successive cuts, with the current whole bracketed."""
from fractions import Fraction
from stage import blend
BACKGROUND = ('#322e32','#1b2629')
INK,RED,BLUE,GOLD,LINE='#fff6dc','#ed958a','#8bc8e5','#e7bd69','#85786a'
BRIDGE='When a gold piece measuring 6 cm is left on the cutting table, pause. Which earlier whole can you reconstruct from four copies of that piece?'
HEAD=('A cut changes the whole','Read the second instruction','Three colours of bunting','Fold before cutting','Only the gold remains','Undo the blue cut','Restore the red strip','Test the cuts forwards')
def check_maths():
    assert Fraction(20-5,2)==Fraction(15,2)
    assert Fraction(1,4)==Fraction(1,3)*(1-Fraction(1,4))
    assert [n for n in range(1,301) if n*(1-Fraction(1,5))*(1-Fraction(3,4))==6]==[30]
    assert 30//5==6 and (30-6)*3//4==18 and 30-6-18==6

def text(a,s,x,y,size=35,col=INK,t=1):
    a.text(str(s),x,y,size,col,bold=True,opacity=t)

def strip(a,y,segments,labels):
    x=140
    for (width,col,alpha),label in zip(segments,labels):
        if alpha:
            col=blend('#28282b',col,alpha)
            a.box(x,y,width-4,75,radius=3,fill=col)
            for j in range(12,int(width-12),30):
                a.line([(x+j,y+6),(x+j+7,y+6)],'#fff9e0',2,alpha*.6)
                a.line([(x+j,y+68),(x+j+7,y+68)],'#fff9e0',2,alpha*.6)
            if label:text(a,label,x+width/2,y+37,32,'#17242a',alpha)
        x+=width

def bracket(a,y,left,right,label,col,t):
    a.line([(left,y-13),(left,y),(right,y),(right,y-13)],col,4,t)
    text(a,label,(left+right)/2,y+33,32,col,t)
def draw(a,n,c):
    a.label(HEAD[n-1],64,71,45,INK,bold=True)
    a.line([(64,124),(1216,124)],LINE,3)
    if n<=2:
        if n==1:
            cut=c.reveal('Cut five centimetres')
            strip(a,225,[(1000,GOLD,1)],['20 cm']) if cut<.02 else strip(a,225,[(750,GOLD,1),(250,RED,cut)],['Ribbon on the table','5 cm'])
            a.line([(890,198),(890,327)],INK,4,cut)
            bracket(a,370,140,890,'Length left on the table?',BLUE,c.reveal('which length'))
            text(a,'20 cm before cutting',640,510,37,INK)
        else:
            strip(a,224,[(375,BLUE,1),(375,BLUE,1),(250,RED,.48)],['7½ cm','7½ cm','cut off'])
            bracket(a,352,140,890,'15 cm remain',BLUE,1)
            text(a,'½ of 15 cm = 7½ cm',640,506,41,GOLD,c.reveal('seven and a half'))
    elif n==3:
        a.label('Instructions for the new ribbon',140,186,33,INK)
        strip(a,232,[(1000,GOLD,1)],['Original length unknown'])
        text(a,'Red uses ¼ of the original.',640,375,37,RED,c.reveal('one quarter'))
        text(a,'Blue uses ⅓ of what remains.',640,440,37,BLUE,c.reveal('one third'))
        text(a,'Which colours use the same length?',640,538,38,INK,c.reveal('same amount'))
    elif n==4:
        a.label('Original ribbon',140,187,30,INK)
        red=c.reveal('Take one strip')
        blue=c.reveal('exactly one strip')
        gold=c.reveal('Two strips remain')
        strip(a,249,[(250,RED,red),(250,BLUE,blue),(250,GOLD,gold),(250,GOLD,gold)],['Red','Blue','Gold','Gold'])
        bracket(a,366,390,1140,'The whole for the second cut',BLUE,c.reveal('Three strips stay'))
        text(a,'Red = ¼ of the ribbon = blue',640,516,38,INK,c.reveal('Red and blue match'))
    else:
        if n==5:
            text(a,'Red: ⅕ of the original',640,201,38,RED,c.reveal('one fifth'))
            text(a,'Blue: ¾ of the rest',640,293,38,BLUE,c.reveal('three quarters'))
            strip(a,371,[(200,GOLD,c.reveal('six centimetres'))],['6 cm'])
            text(a,'Gold is all that remains',728,411,37,INK,c.reveal('remain for gold'))
            text(a,'How long was the original ribbon?',640,531,37,GOLD,c.reveal('How long'))
        elif n==6:
            t=c.reveal('Copy the six')
            strip(a,260,[(200,RED,0)]+[(200,BLUE,t)]*3+[(200,GOLD,1)],['','6 cm','6 cm','6 cm','6 cm'])
            bracket(a,385,340,1140,'After red: four quarters of 6 cm',BLUE,t)
            text(a,'4 × 6 cm = 24 cm',640,529,42,INK,c.reveal('twenty four'))
        else:
            cols=[RED,BLUE,BLUE,BLUE,GOLD]; labs=['Red','Blue','Blue','Blue','Gold']
            vals=[c.reveal('Return the missing') if n==7 else c.reveal('Red gets six'),1,1,1,1]
            if n==8:vals=[c.reveal('Red gets six')]+[c.reveal('Blue gets three')]*3+[c.reveal('Gold gets six')]
            strip(a,250,[(200,col,v) for col,v in zip(cols,vals)],labs)
            if n==7:
                bracket(a,375,340,1140,'Four fifths = 24 cm',BLUE,1)
                text(a,'5 × 6 cm = 30 cm',640,522,42,INK,c.reveal('Five parts'))
            else:
                bracket(a,370,340,940,'18 cm of blue ribbon',BLUE,c.reveal('or eighteen'))
                text(a,'6 cm + 18 cm + 6 cm = 30 cm',640,522,37,INK,c.reveal('restores thirty'))
def poster(draw):return draw(7,1)
