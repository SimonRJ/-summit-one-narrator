"""Place-specific digit choices on mechanical wheels and in a compartmented tray."""
from itertools import permutations
BACKGROUND=('#293b3e','#18282e')
PAPER,INK,GOLD,BLUE,RED,GREEN,LINE='#fff2d8','#24343a','#f4bd70','#a6d9df','#f4a191','#a1dbaa','#70878c'
HEAD=('A printed zero has two jobs','Place the end wheel first','The museum changes its order','Open with two','Open with five','Inspect the printed strips','Why one plausible strip fails','Move the lower stop')
BRIDGE='When the first ticket wheel shows 2, which choice is forced at the far right? Find the ticket that uses all the right digits but misses the lower stop.'
def numbers(lo):
    return sorted(int(''.join(p)) for p in permutations('0257') if p[0]!='0' and p[-1] in '02' and lo<int(''.join(p))<6000)
def check_maths():
    good=numbers(2600)
    assert good==[2750,5072,5270,5702,5720]
    assert set(numbers(2500))-set(good)=={2570}
def text(a,s,x,y,size=36,k=PAPER,t=1):
    a.text(str(s),x,y,size,k,bold=True,opacity=t)
def wheels(a,digits,focus=(),y=281):
    a.box(200,y-91,880,187,fill='#425659',edge=LINE,stroke=3,radius=24)
    for i,char in enumerate(digits):
        x=294+196*i;edge=GOLD if i in focus else LINE
        a.box(x,y-58,115,120,fill='#eddbc0',edge=edge,stroke=6,radius=11)
        text(a,char,x+58,y,64,INK)
        a.line([(x+6,y-39),(x+109,y-39)],'#b8a790',2)
def tray(a,values,cx,y,colour):
    width=145;left=cx-(len(values)-1)*84
    for index,value in enumerate(values):
        x=left+index*168;a.box(x-width/2,y-32,width,65,fill=colour,radius=3)
        text(a,value,x,y,34,INK)
def draw(a,n,c):
    a.label(HEAD[n-1],65,69,43,PAPER,bold=True);a.line([(65,124),(1215,124)],LINE,3)
    if n==1:
        wheels(a,'0257',(0,))
        text(a,'Printed code: 0257',640,443,37,BLUE)
        text(a,'Ordinary number: 257',640,525,38,GOLD,c.reveal('ordinary number on this strip'))
    elif n==2:
        wheels(a,'???0' if c.reveal('zero or two')<.8 else '???2',(0,3))
        text(a,'Units wheel: 0 or 2',640,449,38,BLUE,c.reveal('zero or two'))
        text(a,'Leading wheel: a nonzero unused digit',640,533,31,GOLD,c.reveal('thousands place'))
    elif n==3:
        wheels(a,'????',(0,3))
        text(a,'2600 < ticket < 6000',640,446,44,GOLD,c.reveal('two thousand six hundred'))
        text(a,'Use 0, 2, 5 and 7 exactly once.',640,530,34,BLUE,c.reveal('using all four digits'))
    elif n==4:
        d=['2','?','?','?']
        if c.reveal('must now be zero')>.05:d[3]='0'
        if c.reveal('only seven works')>.05:d[1]='7'
        if c.reveal('Five takes the tens')>.05:d[2]='5'
        wheels(a,d,(1,3))
        text(a,'A leading 2 leaves 0 for the last wheel.',640,445,33,BLUE,c.reveal('even final wheel'))
        text(a,'2750 clears the lower stop.',640,533,37,GREEN,c.reveal('strip reads'))
    elif n==5:
        wheels(a,'5???',(0,),226)
        if c.reveal('zero is last')>.05:tray(a,['5270','5720'],385,432,GOLD)
        if c.reveal('two is last')>.05:tray(a,['5072','5702'],893,432,BLUE)
        text(a,'Last wheel 0',381,521,30,GOLD,c.reveal('zero is last'));text(a,'Last wheel 2',892,521,30,BLUE,c.reveal('two is last'))
    elif n==6:
        text(a,'Leading 2',238,226,32,BLUE);tray(a,['2750'],765,226,BLUE)
        text(a,'Leading 5, ending 0',276,336,29,GOLD);tray(a,['5270','5720'],765,336,GOLD)
        text(a,'Leading 5, ending 2',276,447,29,GREEN);tray(a,['5072','5702'],765,447,GREEN)
        text(a,'1 + 2 + 2 = 5 tickets',640,551,39,PAPER,c.reveal('Together that makes five'))
    elif n==7:
        wheels(a,'2570',(1,),252)
        text(a,'2570 < 2600',640,425,44,RED,c.reveal('lies below'))
        text(a,'A leading zero also misses the interval.',640,532,31,BLUE,c.reveal('begins with zero'))
    else:
        text(a,'Old lower stop: 2600',640,224,41,PAPER);text(a,'New lower stop: 2500',640,325,42,BLUE,c.reveal('two thousand five hundred'))
        if c.reveal('previously rejected strip')>.05:tray(a,['2570'],640,432,GOLD)
        text(a,'Only one extra strip',640,534,39,GREEN,c.reveal('Only one extra strip'))
def poster(draw):return draw(7,1)
