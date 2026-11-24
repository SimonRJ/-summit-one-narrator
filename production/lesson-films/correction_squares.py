"""A five-row cut, signed area tiles, and two exact grids around a common midpoint."""
from stage import blend,clamp
BACKGROUND=('#30343c','#222c35')
BRIDGE='Look at 108 × 92 in the film. Which pieces from breaking around 100 cancel, and which small piece still has to be removed?'
HEAD=('Round and correct','Compare the parts that change','Five rows short of one hundred','Remove five copies of 78','Equal offsets around 100','Cancel the two cross terms','Two products, one midpoint','Squares of nine and three','Why the closer pair wins','Check the sign of the change','Give the exact difference')
PAPER,GOLD,BLUE,RED,GREEN,DIM='#f6efdf','#f2c27b','#94bfdf','#f19e8d','#a0cfb6','#6e7b88'

def check_maths():
    assert 95*78==100*78-5*78==7410
    assert 108*92==10000-64==9936
    assert (992+1010)//2==(998+1004)//2==1001
    assert 998*1004-992*1010==9**2-3**2==72

def label(a,s,x,y,sz=35,col=PAPER,t=1,align='left'):
    a.label(s,x,y,sz,col,t,align=align,bold=True)

def cut_board(a,removed):
    x,y=155,219;w,h=324,292
    a.box(x,y,w,h,radius=0,fill='#467080',edge=BLUE,stroke=3)
    for k in range(1,10):a.line([(x,y+k*h/10),(x+w,y+k*h/10)],'#6c929b',1)
    a.box(x,y+h*.95,w,h*.05,radius=0,fill=RED,opacity=removed)
    a.text('78 per row',x+w/2,y-31,27,GOLD,bold=True)
    label(a,'100 rows',x+w+22,y+73,23,BLUE)
    label(a,'5 cut',x+w+22,y+h-6,23,RED,removed)

def tile(a,x,y,w,h,words,col,t=1):
    a.box(x,y,w,h,radius=7,fill=blend('#26313b',col,.22),edge=col,stroke=3,opacity=t)
    a.text(words,x+w/2,y+h/2,35,col,opacity=t,bold=True)

def offsets(a,first,second,mid=1001):
    x0,x1,y=149,1114,386
    a.line([(x0,y),(x1,y)],DIM,3)
    def x(k):return (x0+x1)/2+(k-mid)*47
    for value in (mid-first,mid-second,mid,mid+second,mid+first):
        col=GOLD if value==mid else RED if abs(value-mid)==first else BLUE
        a.dot(x(value),y,7,col);a.text(str(value),x(value),y+49 if abs(value-mid)==second else y-48,27,col,bold=True)
    for amount,col,dy in [(first,RED,-12),(second,BLUE,13)]:
        a.line([(x(mid-amount),y+dy),(x(mid+amount),y+dy)],col,3)

def grid(a,x,y,count,col,alpha=1):
    unit=23
    for r in range(count):
        for c in range(count):a.box(x+c*unit,y+r*unit,unit-2,unit-2,radius=0,fill=col,opacity=alpha)

def draw(a,n,c):
    label(a,HEAD[n-1],71,70,45);a.line([(71,118),(1205,118)],DIM,2)
    if n==1:
        label(a,'95',164,324,62,GOLD);a.arrow((322,324),(515,324),BLUE,c.reveal('nearby ten'),4)
        label(a,'100 − 5',589,324,58,PAPER,c.reveal('small correction'))
        label(a,'Anchor plus a signed correction',640,499,37,GREEN,c.reveal('exact value'),'center')
    elif n==2:
        offsets(a,9,3)
        label(a,'Compare the offsets from one midpoint',638,207,39,PAPER,c.reveal('midpoint'),'center')
        label(a,'992 and 1,010               998 and 1,004',640,547,31,GOLD,c.reveal('parts that differ'),'center')
    elif n in (3,4):
        q=c.reveal('five below' if n==3 else 'extra five copies',1.2);cut_board(a,q)
        label(a,'100 × 78 = 7,800',700,245,37,BLUE,c.reveal('one hundred') if n==4 else c.reveal('one hundred'))
        label(a,'5 × 78 = 390',700,355,39,RED,c.reveal('three hundred and ninety') if n==4 else 0)
        label(a,'7,800 − 390 = 7,410',665,481,40,GREEN,c.reveal('exact result') if n==4 else 0)
    elif n in (5,6):
        label(a,'108 = 100 + 8',150,193,36,BLUE);label(a,'92 = 100 − 8',724,193,36,RED)
        if n==5:
            tile(a,160,300,405,130,'+8 × 100',BLUE,c.reveal('same distance'))
            tile(a,700,300,405,130,'100 × (−8)',RED,c.reveal('two equal cross products'))
            label(a,'Which pieces cancel?',640,533,38,GOLD,c.reveal('cross products'),'center')
        else:
            q=c.reveal('so they cancel')
            for x,v,col in [(145,'+800',BLUE),(422,'−800',RED)]:
                tile(a,x,276,211,103,v,col)
                a.line([(x+18,367),(x+188,292)],PAPER,4,q)
            tile(a,727,276,304,103,'−8 × 8 = −64',RED,c.reveal('minus sixty-four'))
            label(a,'10,000 − 64 = 9,936',640,503,47,GREEN,c.reveal('exact result'),'center')
    elif n==7:
        offsets(a,9,3)
        label(a,'A: 992 × 1,010',160,213,38,RED)
        label(a,'B: 998 × 1,004',724,213,38,BLUE,c.reveal('nine hundred and ninety-eight'))
        label(a,'Which product is larger? By how much?',640,534,36,PAPER,c.reveal('how much larger'),'center')
    elif n==8:
        q=c.reveal('minus nine');r=c.reveal('minus three')
        grid(a,165,218,9,RED,q);grid(a,600,218,3,BLUE,r)
        label(a,'A removes 81',161,475,34,RED,c.reveal('eighty-one'))
        label(a,'B removes 9',563,374,35,BLUE,c.reveal('loses only nine'))
        label(a,'81 − 9 = 72',827,463,42,GREEN,c.reveal('larger by seventy-two'))
    elif n==9:
        label(a,'Same midpoint',147,222,34,GOLD);label(a,'Same starting square',662,222,34,PAPER,c.reveal('same midpoint'))
        grid(a,178,305,9,RED,.85);grid(a,464,305,3,BLUE,.85)
        label(a,'Smaller offset → less removed',665,409,33,GREEN,c.reveal('smaller square'))
        label(a,'Each grid illustrates a squared offset.',640,550,27,DIM,c.reveal('anchor is shared'),'center')
    elif n==10:
        tile(a,135,232,405,125,'95 = 100 − 5',RED,c.reveal('below its anchor'))
        tile(a,683,232,405,125,'108 = 100 + 8',BLUE,c.reveal('too high or too low'))
        label(a,'Opposite signs and equal sizes cancel.',640,499,39,GREEN,c.reveal('equal magnitude'),'center')
    else:
        label(a,'1,001² − 81',159,247,48,RED,c.reveal('exact sums or differences'))
        label(a,'1,001² − 9',721,247,48,BLUE,c.reveal('exact sums or differences'))
        label(a,'B exceeds A by 72',640,467,51,GREEN,c.reveal('give the exact difference'),'center')

def poster(draw):return draw(4,1)
