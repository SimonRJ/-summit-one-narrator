"""Flag halyards, moveable pairs and an independent alternating-colour count."""
from itertools import permutations
from math import factorial
from stage import blend
BACKGROUND=('#1d3a43','#15242e')
INK,WHITE,BLUE,ORANGE,ROPE,GREEN='#132737','#fff2cf','#8ccbe4','#ffb16e','#a39d88','#a4dfba'
BRIDGE='When the harbourmaster crosses out the rows with A beside B and the rows with C beside D, find a signal crossed out twice. How many orders can the two clips make?'
HEAD=('A signal is a row','Can the clip turn?','Two pairs need space','Count all signals','Clip one forbidden pair','Where did our row go?','Return the double crossings','Count by the first flag')
def check_maths():
    rows=list(permutations('ABCD'))
    def near(row,x,y):return abs(row.index(x)-row.index(y))==1
    assert len(rows)==factorial(4)==24
    assert sum(near(r,'A','B') for r in rows)==12
    assert sum(near(r,'C','D') for r in rows)==12
    assert sum(near(r,'A','B') and near(r,'C','D') for r in rows)==8
    assert sum(not near(r,'A','B') and not near(r,'C','D') for r in rows)==8
def text(a,s,x,y,size=35,col=WHITE,t=1):
    a.text(str(s),x,y,size,col,bold=True,opacity=t)
def row(a,s,x,y,dx=120,t=1,clip=()):
    if not t:return
    w=dx*.75;h=dx*.72
    a.line([(x-dx*.18,y),(x+(len(s)-1)*dx+w+dx*.18,y)],ROPE,4,t)
    for i,char in enumerate(s):
        left=x+i*dx
        col=BLUE if char in 'AB' else ORANGE
        a.polygon([(left,y),(left+w,y),(left+w,y+h*.84),(left+w*.52,y+h*.68),(left,y+h)],blend('#19343b',col,t))
        text(a,char,left+w/2,y+h*.34,round(dx*.36),INK,t)
    for i in clip:
        a.line([(x+i*dx+4,y-7),(x+i*dx+4,y-22),(x+(i+1)*dx+w-3,y-22),(x+(i+1)*dx+w-3,y-7)],GREEN,5,t)
def draw(a,n,c):
    a.label(HEAD[n-1],65,71,44,WHITE,bold=True)
    a.line([(65,125),(1214,125)],ROPE,3)
    if n==1:
        row(a,'ABC',430,273,158,1,(0,) if c.reveal('Clip those two')>.35 else ())
        text(a,'A immediately before B',640,479,39,BLUE,c.reveal('immediately before'))
    elif n==2:
        row(a,'ABC',160,228,128,1,(0,))
        row(a,'CAB',737,228,128,c.reveal('or after C'),(1,))
        text(a,'AB cannot turn',640,420,38,GREEN,c.reveal('Reversing the clip'))
        text(a,'Touching alone allows AB or BA',640,517,34,WHITE,c.reveal('both directions'))
    elif n==3:
        row(a,'ABCD',395,193,130)
        text(a,'A apart from B',380,359,38,BLUE,c.reveal('A must stay apart'))
        text(a,'C apart from D',907,359,38,ORANGE,c.reveal('C must stay apart'))
        row(a,'ACBD',475,460,89,c.reveal('Try making a row'))
    elif n==4:
        for i,(amount,cue) in enumerate([(4,'four ways'),(3,'Three flags'),(2,'then two'),(1,'then one')]):
            x=300+i*224;t=c.reveal(cue)
            a.box(x-78,230,156,116,fill='#28505c',edge=ROPE,opacity=t)
            text(a,amount,x,287,63,WHITE,t)
        text(a,'4 × 3 × 2 × 1 = 24',640,480,46,GREEN,c.reveal('twenty four'))
    elif n==5:
        row(a,'ABCD',168,220,109,1,(0,));row(a,'BACD',706,220,109,c.reveal('turn either way'),(0,))
        text(a,'The AB clip, C and D are three objects.',640,396,34,WHITE,c.reveal('three objects'))
        text(a,'6 object orders × 2 clip directions = 12',640,500,37,GREEN,c.reveal('twelve rows'))
    elif n==6:
        row(a,'ABDC',378,234,141,1)
        for k,(start,col,cue) in enumerate([(0,BLUE,'A B D C'),(2,ORANGE,'both touching pairs')]):
            x=387+start*141;y=382
            a.line([(x,y),(x+238,y)],col,7,c.reveal(cue))
        text(a,'Two crossings apply to the same signal',640,497,36,WHITE,c.reveal('twice explains'))
    elif n==7:
        row(a,'ABCD',194,229,105,1,(0,2));row(a,'CDAB',735,229,105,c.reveal('two orders for the clips'),(0,2))
        text(a,'2 clip orders × 2 directions × 2 directions = 8',640,393,33,GREEN,c.reveal('eight doubly'))
        text(a,'24 − 12 − 12 + 8 = 8',640,513,46,WHITE,c.reveal('plus eight'))
    else:
        row(a,'ACBD',170,242,110,1);row(a,'CADB',732,242,110,c.reveal('Pick which group starts'))
        text(a,'Choose the starting colour, then order each pair.',640,406,33,WHITE,c.reveal('then order its flags'))
        text(a,'2 × 2 × 2 = 8',640,515,46,GREEN,c.reveal('again gives eight'))
def poster(draw):return draw(7,1)
