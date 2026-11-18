"""S057: ordered number tiles, a sliding pair of dials, and all fourteen possible labelled boxes."""
from itertools import permutations,product
from math import sin,pi
from captioned_film import cue,mix

ID='S057'
ORIGINAL='dfd47a0e033f55392cdff6aa9b204ae15ff51002407e49ef47ac5ce3b44e18ad'
START=(0,16.6,34.52,48.58,65.7,80.55,93.99,113.16,134.75,149.63,165.47)
POSTER=139.8
PAPER='#f3f1e5';INK='#243641';BLUE='#2d6393';RUST='#a84738';GREEN='#146c60'
DIM='#52656a';LINE='#bac4b9';WHITE='#fffdf4';TINT='#dfebdf';PEACH='#f2dfc9'
ROWS={a:[(a,b,11-a-b) for b in range(1,7) if 1<=11-a-b<=6] for a in (2,4,6)}
def text(c,s,x,y,z=28,col=INK,anchor='mm'):c.text(s,x,y,z,col,anchor,True)
def head(c,s):text(c,s,62,60,40,INK,'lm')
def tile(c,x,y,v,col,r=31):
    c.rect(x-r,y-r,2*r,2*r,WHITE,col,3);text(c,v,x,y+1,r,col)
def intro(c,t):
    head(c,'Keep the first choice fixed while endings change')
    for i,v in enumerate(('A','B','C')):
        yy=194+i*132;tile(c,241,yy,v,BLUE)
        for j in range(2):
            ii=i*2+j
            if cue(t,1.05+ii*.9,.8):
                x=538+293*j;tile(c,x,yy,v,BLUE);tile(c,x+70,yy,j+1,RUST)
        if t>=8.6+i*.65:text(c,'2 endings',1075,yy,26,GREEN)
    if t>=13.6:text(c,'3 rows × 2 endings = 6 pairs',640,564,30,GREEN)
def exams(c,t):
    head(c,'A condition can remove an entire row')
    for i,a in enumerate(range(1,7)):
        xx=159+i*186;tile(c,xx,275,a,BLUE,38)
        if a%2 and t>=21.4:c.line([(xx-30,303),(xx+30,247)],RUST,4)
        elif a%2==0 and t>=23.4:c.line([(xx-36,334),(xx+36,334)],GREEN,5)
    text(c,'Possible values in the first box',640,161,29,DIM)
    if t>=25:text(c,'An even first value leaves 2, 4 and 6.',640,438,31,GREEN)
    if t>=30:text(c,'Each legal ending belongs in exactly one row.',640,520,27)
def numbers_q(c,t):
    head(c,'Which two-digit numbers use two different tiles?')
    for i,n in enumerate((1,2,3)):tile(c,388+i*250,229,n,(BLUE,RUST,GREEN)[i],52)
    for i,tag in enumerate(('tens','ones')):
        x=484+312*i;tile(c,x,426,'?',(BLUE,RUST)[i],42);text(c,tag,x,511,26,DIM)
def numbers_a(c,t):
    head(c,'Tens first, then the legal endings')
    times=(49.0,52.7,56.1,57.1,58.45,59.55)
    for i,(a,b) in enumerate(permutations((1,2,3),2)):
        row=i//2;y=193+row*140;x=532+(i%2)*380
        tile(c,240,y,a,BLUE)
        p=cue(t,times[i],.8)
        if p:
            tile(c,mix(240,x,p),y,a,BLUE)
            tile(c,x+72,y,b,RUST)
    if t>=62:text(c,'12, 13, 21, 23, 31, 32',640,552,31,GREEN)
def dial(c,x,y,label,v,col):
    c.dot(x,y,71,LINE);c.dot(x,y,66,WHITE);c.dot(x,y,54,col);text(c,v,x,y,43,WHITE)
    text(c,label,x,y+107,28,col)
def pair(c,t,solved):
    head(c,'Two labelled counters must add to 13')
    if solved:
        n=min(8,5+int(3*cue(t,86.65,3.3)))
        dial(c,295,290,'A',n,BLUE);dial(c,729,290,'B',13-n,RUST)
        if t>=83:text(c,'A ≥ 5',1031,229,31,BLUE)
        if t>=86.6:text(c,'A ≤ 8',1031,310,31,BLUE)
        if t>=88.6:
            for j,a in enumerate(range(5,9)):
                if cue(t,88.6,2.75)>j/4:text(c,f'({a}, {13-a})',254+j*260,511,32,GREEN)
    else:
        dial(c,295,290,'A','?',BLUE);dial(c,729,290,'B','?',RUST)
        if t>=69.8:text(c,'A + B = 13',1028,270,32)
        if t>=75.2:text(c,'(A, B) records which counter shows which value.',640,526,28,GREEN)
def pair_q(c,t):pair(c,t,False)
def pair_a(c,t):pair(c,t,True)
def box(c,x,y,n,tag,col):
    c.rect(x-108,y-78,216,157,WHITE,col,3);text(c,tag,x,y-111,30,col)
    for j in range(n):
        xx=x-54+j%3*54;yy=y-26+j//3*53
        c.dot(xx,yy,16,col);c.dot(xx-3,yy-3,4,WHITE)
    text(c,n,x,y+118,31,col)
def boxes(c,t):
    head(c,'Fill three labelled boxes with eleven tokens')
    for j,(n,tag,col) in enumerate(((2,'A',BLUE),(3,'B',RUST),(6,'C',GREEN))):
        box(c,251+j*389,305,n,tag,col)
    if t>=99.6:text(c,'Each holds 1 to 6 tokens.',635,504,28,DIM)
    if t>=103:text(c,'A must be even.',635,562,29,BLUE)
def lattice(c,shown,complete):
    for a in (2,4,6):
        i=a//2-1;y=225+i*119
        text(c,'A = '+str(a),136,y,28,BLUE)
        for b in range(1,7):
            x=324+(b-1)*140
            c.rect(x-56,y-34,112,68,WHITE,LINE,2)
            if i>shown:continue
            z=11-a-b
            if 1<=z<=6:
                c.rect(x-56,y-34,112,68,TINT,GREEN,2)
                text(c,f'{b}, {z}',x,y,25,GREEN)
            elif complete:c.line([(x-15,y+10),(x+15,y-10)],LINE,3)
        if complete and i<=shown:text(c,len(ROWS[a]),1171,y,32,GREEN)
    for b in range(1,7):text(c,'B = '+str(b),324+(b-1)*140,144,22,RUST)
    if complete:text(c,'ways',1171,144,22,GREEN)
def partition(c,t):
    head(c,'Fix A and list the allowed pairs (B, C)')
    shown=-1 if t<118.8 else min(2,int(3*cue(t,118.8,11.1)))
    lattice(c,shown,t>=130.2)
    if t<118.8:text(c,'A can be 2, 4 or 6.',640,561,29,BLUE)
    elif t<126.6:text(c,'For each row, C = 11 − A − B.',640,561,28)
    else:text(c,'Keep both B and C between 1 and 6.',640,561,28,GREEN)
def total(c,t):
    head(c,'Every accepted triple has one place in this table')
    lattice(c,2,True)
    if t>=137.8:text(c,'4 + 6 + 4 = 14 ordered triples',640,564,32,GREEN)
def mistakes(c,t):
    if t<158.4:
        head(c,'Include both ends of a nonempty range')
        for j,b in enumerate(range(3,7)):
            tile(c,298+j*225,295,b,GREEN,40)
        if t>=153:text(c,'6 − 3 + 1 = 4 choices',640,459,34,GREEN)
    else:
        head(c,'Swapping different box readings gives a new triple')
        p=cue(t,158.8,2.5)
        centres=(251,640,1029)
        for i,(tag,col) in enumerate(zip('ABC',(BLUE,RUST,GREEN))):
            x=centres[i];c.rect(x-108,230,216,157,WHITE,col,3);text(c,tag,x,197,30,col)
            if i==0 or p in (0,1):text(c,((2,3,6) if p==0 else (2,6,3))[i],x,426,30,col)
        for i,(n,col) in enumerate(((2,BLUE),(3,RUST),(6,GREEN))):
            dest=(0,2,1)[i];phase=0 if i==0 else p
            for j in range(n):
                x=mix(centres[i],centres[dest],phase)-54+j%3*54
                y=282+j//3*53+(1 if i==2 else -1)*70*sin(pi*phase)
                c.dot(x,y,16,col);c.dot(x-3,y-3,4,WHITE)
        text(c,'(2, 3, 6) and (2, 6, 3) are two different results.',640,548,27)
def finish(c,t):
    head(c,'Use one fixed value per row')
    lattice(c,min(2,int(3*cue(t,165.8,5.5))),True)
    if t>=171.8:text(c,'A fixes the row. B fixes C.',640,548,29,BLUE)
SCENES=(intro,exams,numbers_q,numbers_a,pair_q,pair_a,boxes,partition,total,mistakes,finish)
def verify():
    valid={v for v in product(range(1,7),repeat=3) if sum(v)==11 and v[0]%2==0}
    assert valid=={v for row in ROWS.values() for v in row} and list(map(len,ROWS.values()))==[4,6,4]
    assert [(a,b) for a,b in product(range(1,9),repeat=2) if a+b==13]==[(5,8),(6,7),(7,6),(8,5)]
    assert list(10*a+b for a,b in permutations((1,2,3),2))==[12,13,21,23,31,32]
