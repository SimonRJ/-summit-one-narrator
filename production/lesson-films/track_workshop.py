"""Matching copies of calibrated straight track, curved track and one bridge."""
from math import cos,pi,sin
BACKGROUND=('#343238','#222b34')
BRIDGE='The workshop doubles the complete second sample. Before removing any matching pieces, list all its straights, bends and centimetres. Where did each doubled quantity come from?'
HEAD=('Measure the path','Clip two sample trains','Copy every piece and its length','Lift out matching pieces','Restore the straight','The mystery bridge','Compare before finding the bridge','Find the bridge and check')
PAPER,GREEN,BLUE,GOLD,DIM='#fff3e3','#92d2a4','#90c5ed','#f4c17a','#697583'

def check_maths():
    assert [(s,b) for s in range(23) for b in range(23) if 2*s+b==22 and s+2*b==20]==[(8,6)]
    assert 49-3*8-2*6==53-2*8-4*6==13

def label(a,s,x,y,size=35,col=PAPER,t=1,align='left'):
    a.label(s,x,y,size,col,t,align=align,bold=True)

def piece(a,x,y,k,t=1):
    col={'S':GREEN,'B':BLUE,'G':GOLD}[k]
    if k=='B':
        for radius in (25,36):
            pts=[(x-26+radius*sin(j*pi/36),y-9+radius*cos(j*pi/36)) for j in range(19)]
            a.line(pts,col,3,t)
        for j in (1,4,7,10,13,16):
            a.line([(x-26+21*sin(j*pi/36),y-9+21*cos(j*pi/36)),(x-26+41*sin(j*pi/36),y-9+41*cos(j*pi/36))],col,3,t)
    else:
        for offset in (-6,6):a.line([(x-30,y+offset),(x+30,y+offset)],col,3,t)
        for dx in (-24,-12,0,12,24):a.line([(x+dx,y-12),(x+dx,y+12)],col,3,t)
        if k=='G':a.line([(x-30,y-12),(x-16,y-28),(x,y-12),(x+15,y-28),(x+30,y-12)],col,3,t)
    a.text(k,x,y+43,21,col,bold=True,opacity=t)

def row(a,x,y,s):
    for i,k in enumerate(s):piece(a,x+i*77,y,k)

def draw(a,n,c):
    label(a,HEAD[n-1],70,73,46);a.line([(70,122),(1210,122)],DIM,2)
    if n==1:
        piece(a,227,322,'S');label(a,'Green straight',311,330,34,GREEN)
        piece(a,749,322,'B');label(a,'Blue bend',827,330,34,BLUE)
        label(a,'Measure along the middle of each piece.',640,514,38,PAPER,c.reveal('Measure along each curve'),'center')
    elif n==2:
        row(a,155,239,'SSB');label(a,'= 22 cm',621,245,43,PAPER,c.reveal('twenty-two centimetres'))
        row(a,155,423,'SBB');label(a,'= 20 cm',621,429,43,PAPER,c.reveal('twenty centimetres'))
    elif n==3:
        row(a,159,244,'SBB');label(a,'20 cm',712,250,38,BLUE)
        for i,k in enumerate('SSBBBB'):piece(a,159+i*77,419,k,c.reveal('two copies',1))
        label(a,'2 × 20 = 40 cm',709,422,40,GOLD,c.reveal('forty centimetres'))
    elif n==4:
        p=c.reveal('Remove them from both',.8);q=c.reveal('one blue bend from each side',.7)
        for yy,ss in [(255,'SSBBBB'),(425,'SSB')]:
            for i,k in enumerate(ss):piece(a,150+i*77,yy,k,1-.85*(p if i<2 else q if i==2 else 0))
        label(a,'40 − 22 = 18 cm',682,265,42,GOLD,c.reveal('eighteen centimetres more'))
        label(a,'3 bends = 18 cm',681,410,39,BLUE,c.reveal('three extra bends'))
    elif n==5:
        row(a,161,249,'BBB');label(a,'18 ÷ 3 = 6 cm',626,255,41,BLUE,c.reveal('one bend is six'))
        row(a,161,423,'SBB');label(a,'20 − 2 × 6 = 8 cm',626,429,40,GREEN,c.reveal('straight measures eight'))
    elif n==6:
        row(a,120,245,'SSSBBG');label(a,'49 cm',803,248,43,PAPER,c.reveal('forty-nine centimetres'))
        row(a,120,427,'SSBBBBG');label(a,'53 cm?',801,431,43,GOLD,c.reveal('fifty-three'))
    elif n==7:
        piece(a,176,323,'S');label(a,'−8 cm',239,325,40,GREEN,c.reveal('eight centimetres'))
        row(a,533,323,'BB');label(a,'+12 cm',703,325,40,BLUE,c.reveal('bends are twelve'))
        label(a,'+12 − 8 = +4 cm',640,503,45,GOLD,c.reveal('four centimetres longer'),'center')
    else:
        row(a,115,247,'SSSBBG');label(a,'49 − 36 = 13 cm',677,256,38,GOLD,c.reveal('other thirteen'))
        row(a,115,422,'SSBBBBG');label(a,'16 + 24 + 13 = 53 cm',676,429,34,PAPER,c.reveal('which is fifty-three'))

def poster(draw):return draw(3,1)
