"""S040. Re-pair stationery and trace the same boxes through three different weighings."""
from itertools import product
from captioned_film import cue,mix,font
ID='S040'
ORIGINAL='58af22c732509cefe2a1b3c5ea0de214cbc88d763b48aff323f7ce8c0bcefef8'
START=(0,15.64,36.43,49.52,62.64,77.97,95.25,112.82,134.25,147.69,161.29)
POSTER=130.5
PAPER='#f6eddd';INK='#262f44';SOFT='#575e68';PENCIL='#b3a990';RULE='#d9ceb6'
TEAL='#217564';BLUE='#345e9a';RED='#a04b49';GOLD='#c69139'
LIGHT=('#d7e8da','#d4dfef','#f0d8c8');DARK=(TEAL,BLUE,RED);EDGE='#5e5747';WHITE='#fff9ec'
def label(c,s,x,y,size=30,col=INK,anchor='lm'):c.text(s,x,y,size,col,anchor,True)
def title(c,s):
    sz=42
    while font(round(sz*c.scale),True).getlength(s)>1140*c.scale:sz-=1
    label(c,s,64,60,sz)
def simpleline(c,x,y,n,colour,u=42,known=True):
    for i in range(n):
        c.rect(x+i*u+1,y,u-2,45,colour,EDGE,1)
    if not known:c.rect(x+1,y+1,n*u-2,43,colour)
def box(c,x,y,i,scale=1,show=0,count=None):
    w=142*scale;h=92*scale
    # An overhead counting tray with the case letter printed below the viewing window.
    x0=x-w/2;y0=y-h/2
    c.rect(x0+3*scale,y0+4*scale,w,h,RULE);c.rect(x0,y0,w,h,LIGHT[i],DARK[i],max(1,3*scale))
    if show:
        n=(7,11,12)[i] if count is None else count
        for j in range(n):
            xx=x+(j%4-1.5)*23*scale;yy=y-25*scale+(j//4)*19*scale
            c.dot(xx,yy,6.6*scale,DARK[i])
        label(c,chr(65+i),x,y+32*scale,max(14,round(21*scale)),DARK[i],'mm')
    else:
        c.line([(x0+10*scale,y0+9*scale),(x0+w-10*scale,y0+9*scale)],DARK[i],2)
        label(c,chr(65+i),x,y+3*scale,max(16,round(37*scale)),DARK[i],'mm')
def clip(c,x,y,w,h,col):
    c.line([(x,y),(x+w,y),(x+w,y+h),(x,y+h),(x,y)],col,2)
def stationery(c,kind,x,y,scale=1):
    if kind=='N':
        w=58*scale;h=73*scale;c.rect(x-w/2+3,y-h/2+3,w,h,RULE)
        c.rect(x-w/2,y-h/2,w,h,'#d7e8da',TEAL,2);c.rect(x-w/2+5*scale,y-h/2,6*scale,h,TEAL)
        c.rect(x-10*scale,y-15*scale,30*scale,18*scale,WHITE,TEAL,1)
    else:
        w=86*scale;h=26*scale;c.rect(x-w/2+2,y-h/2+3,w,h,RULE);c.rect(x-w/2,y-h/2,w,h,'#f1cc7e',EDGE,2)
        for j in range(11):
            xx=x-w/2+(3+8*j)*scale;c.line([(xx,y-h/2),(xx,y-h/2+(11 if j%5==0 else 6)*scale)],EDGE,1.4)
def intro(c,t):
    title(c,'A box keeps its identity when it appears in two clues')
    for i,x in enumerate((247,458,670)):
        box(c,x,303,i,1.25)
    if t>=4.8:clip(c,139,208,418,179,TEAL)
    if t>=8:
        p=cue(t,8.1,2.6);y=mix(405,391,p)
        clip(c,357,226,422,y-226,BLUE)
    if t>=8:label(c,'B is in both pairs.',846,250,29,BLUE)
    if t>=11.2:label(c,'The same B each time.',846,355,27)
def sets(c,t):
    title(c,'Which pair satisfies both clues?')
    pairs=[(1,9),(2,8),(3,7),(4,6),(5,5)]
    for j,(a,b) in enumerate(pairs):
        x=137+216*j;y=278;col=TEAL if t>=27.2 and b-a==4 else SOFT
        c.rect(x-44,y-63,176,133,WHITE,col,3);label(c,f'{a} + {b}',x+44,y,33,col,'mm')
        if t>=23.2:label(c,'= 10',x+44,y+102,24,col,'mm')
    label(c,'Clue 1   total 10',137,149,28)
    if t>=19.6:label(c,'Clue 2   difference 4',688,149,28,TEAL)
    if t>=32.2:label(c,'3 + 7 = 10     and     7 − 3 = 4',251,502,33,TEAL)
def lines(c,t,answer):
    title(c,'Two lengths total 16. One is 4 longer.')
    x,y,u=162,204,60
    separation=cue(t,49.6,2.25) if answer else 0
    known=bool(answer and t>=56.4)
    simpleline(c,x,y,6,LIGHT[0],u,known)
    simpleline(c,x,y+132,6,LIGHT[0],u,known)
    if t>=38.6:
        simpleline(c,x+6*u+separation*67,y+132-separation*56,4,LIGHT[2],u,True)
        label(c,'4',x+8*u+separation*67,y+155-separation*56,29,RED,'mm')
    if answer:
        if t>=52.2:label(c,'16 − 4 = 12',866,205,34)
        if t>=55:label(c,'12 ÷ 2 = 6',866,295,34,TEAL)
        if t>=56.4:label(c,'6 + 4 = 10',866,384,34,RED)
        if t>=59.8:label(c,'6 + 10 = 16,     10 − 6 = 4',277,510,30)
    elif t>=41.2:
        label(c,'Smaller',866,230,32,TEAL);label(c,'Larger',866,362,32,RED)
        label(c,'Together   16',306,509,35)
def lines_q(c,t):lines(c,t,False)
def lines_a(c,t):lines(c,t,True)
def row(c,x,y,kinds,scale=1):
    for j,k in enumerate(kinds):stationery(c,k,x+j*111*scale,y,scale)
def shopping(c,t):
    title(c,'What does one notebook and one ruler cost together?')
    row(c,219,222,'NNR',1.15);label(c,'$25',772,223,42,TEAL)
    if t>=66.2:row(c,219,374,'NRR',1.15);label(c,'$29',772,375,42,BLUE)
    if t>=69.6:
        c.line([(141,456),(1116,456)],RULE,2);row(c,218,525,'NR',.8);label(c,'One pair costs …',583,526,30)
def regroup(c,t):
    title(c,'Rearrange both purchases into three identical pairs')
    kinds='NNRNRR'
    start=[(235,188),(422,188),(610,188),(235,334),(422,334),(610,334)]
    end=[(194,252),(495,252),(282,252),(795,252),(583,252),(883,252)]
    if t<86.4:
        p=cue(t,78.0,4.4)
        for k,a,b in zip(kinds,start,end):
            stationery(c,k,mix(a[0],b[0],p),mix(a[1],b[1],p),1)
        if t>=80.8:label(c,'$25 + $29 = $54',156,460,34)
        if t>=83:
            for x in (139,440,740):clip(c,x,174,196,159,TEAL)
            label(c,'$54 ÷ 3 = $18 per pair',599,460,31,TEAL)
    else:
        row(c,206,272,'NNR',1.13);clip(c,274,196,252,151,BLUE)
        label(c,'$25',204,390,32);label(c,'One pair   $18',289,448,27,BLUE)
        if t>=89.8:label(c,'Notebook   $25 − $18 = $7',651,235,30,TEAL);label(c,'Ruler   $18 − $7 = $11',651,334,30,BLUE)
        if t>=93:label(c,'2 × $7 + $11 = $25     ·     $7 + 2 × $11 = $29',187,538,26)
PAIRS=((0,1,18),(1,2,23),(2,0,19))
def pair(c,x,y,j,opened=False):
    a,b,total=PAIRS[j];box(c,x,y,a,.72,opened);box(c,x+126,y,b,.72,opened)
    label(c,str(total),x+63,y+82,32,INK,'mm')
def clues(c,t):
    title(c,'Three pair totals. Find the count in each box.')
    for i,x in enumerate((155,537,918)):
        if t>=(99.2,102.4,104.8)[i]:pair(c,x,328,i)
    if t<99.2:
        for i,x in enumerate((351,641,930)):box(c,x,310,i,1.3)
    if t>=106.8:label(c,'Which box is absent from each pair?',259,505,32)
def double(c,t):
    title(c,'Follow both copies of each box')
    if t<123.8:
        prev=[(170,223),(294,223),(494,223),(618,223),(817,223),(941,223)]
        nexts=[(225,195),(525,195),(525,337),(825,195),(825,337),(225,337)]
        p=cue(t,114.8,2.7)
        for i,(a,b) in enumerate(zip(prev,nexts)):
            box(c,mix(a[0],b[0],p),mix(a[1],b[1],p),(0,1,1,2,2,0)[i],.78)
        if t>=114.8:label(c,'18 + 23 + 19 = 60',172,460,33)
        if t>=120.4:label(c,'60 ÷ 2 = 30',717,460,35,TEAL)
    else:
        opened=[t>=126.8,t>=129.4,t>=132.2]
        for i,x in enumerate((213,449,685)):
            box(c,x,283,i,1.23,opened[i])
            if opened[i]:label(c,str((7,11,12)[i]),x,401,40,DARK[i],'mm')
        label(c,'Total   30',884,175,33)
        if t>=126.8:label(c,'A = 30 − 23 = 7',884,267,27,TEAL)
        if t>=129.4:label(c,'B = 30 − 19 = 11',884,349,27,BLUE)
        if t>=132.2:label(c,'C = 30 − 18 = 12',884,430,27,RED)
def recheck(c,t):
    title(c,'Open each pair and count its contents')
    for i,x in enumerate((150,539,918)):
        if t>=134.25+i*.9:
            pair(c,x,275,i,True)
            a,b,tot=PAIRS[i];amounts=(7,11,12)
            label(c,f'{amounts[a]} + {amounts[b]} = {tot}',x+62,454,27,DARK[i],'mm')
    if t>=140.2:label(c,'The total of 30 and any pair fix the missing box.',177,548,30)
def mistakes(c,t):
    if t<154:
        sets(c,33 if t>=151 else 18)
        return
    title(c,'Counting pair totals counts each box twice')
    for i,x in enumerate((264,630,991)):
        box(c,x,243,i,.97);box(c,x,386,i,.97)
    if t>=158.4:label(c,'One complete row = 60 ÷ 2 = 30 counters',211,522,34,TEAL)
def finish(c,t):
    title(c,'Use the original clues to check every count')
    for i,x in enumerate((260,634,1003)):
        box(c,x,240,i,1.16,True);label(c,str((7,11,12)[i])+' counters',x,354,28,DARK[i],'mm')
    if t>=168.6:
        for i,x in enumerate((260,634,1003)):
            a,b,n=PAIRS[i];label(c,f'{chr(65+a)} + {chr(65+b)} = {n}',x,471,31,DARK[i],'mm')
SCENES=(intro,sets,lines_q,lines_a,shopping,regroup,clues,double,recheck,mistakes,finish)
def verify():
    assert [(a,b) for a,b in product(range(17),repeat=2) if a+b==16 and b-a==4]==[(6,10)]
    assert [(n,r) for n,r in product(range(30),repeat=2) if 2*n+r==25 and n+2*r==29]==[(7,11)]
    assert [(a,b,c) for a,b,c in product(range(24),repeat=3) if a+b==18 and b+c==23 and c+a==19]==[(7,11,12)]
    assert all((7,11,12)[a]+(7,11,12)[b]==n for a,b,n in PAIRS)
