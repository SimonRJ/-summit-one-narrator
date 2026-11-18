"""S027. Deal the actual card collections, gather nine stars, then exchange rates in bundles of six."""
from math import cos,sin,pi,gcd
from fractions import Fraction
from captioned_film import cue,mix

ID='S027';ORIGINAL='45159244c655b6c2b9e9c81a3601e89bbd85995a40e94e3f68e38ef85327bcc8'
START=(0,14.04,29.56,42.98,53.07,71.12,92.39,112.68,134.91,148.35,162.59)
POSTER=129.4
PAPER='#f4ecdf';INK='#292b39';RED='#b33d4c';BLUE='#28588a';MUTED='#665f60';EDGE='#c7bba9';STAR='#df9e32';HANDFILL='#fffaf2';LIGHT='#e5dbc9';MARK='#087f7b'

def title(c,s):c.text(s,64,67,42,INK,'lm',True)
def line(c,s,x,y,size=32,colour=INK):c.text(s,x,y,size,colour,'lm',True)
def star(c,x,y,r,colour):
    pts=[]
    for j in range(10):
        a=-pi/2+j*pi/5;v=r if j%2==0 else r*.44;pts.append((x+v*cos(a),y+v*sin(a)))
    c.poly(pts,colour,None)

def face(c,x,y,w,h,colour,marked,opacity=1):
    c.rect(x+2,y+3,w,h,EDGE);c.rect(x,y,w,h,HANDFILL,colour,2)
    c.line([(x+3,y+4),(x+3,y+h-4)],colour,3)
    # A corner pip is a small diamond on red cards and a dot on blue cards.
    if colour==RED:c.poly([(x+9,y+5),(x+12,y+9),(x+9,y+13),(x+6,y+9)],colour,None)
    else:c.dot(x+9,y+9,3,colour)
    if marked:star(c,x+w*.54,y+h*.54,min(w,h)*.29*opacity,colour)

def spots():
    allcards=[]
    for n,columns,base,col in [(12,3,142,RED),(20,4,548,BLUE)]:
        for i in range(n):
            row,j=divmod(i,columns)
            allcards.append((base+j*63,179+row*73,col,j==0))
    return allcards

CARDS=spots()

def decks(c,t,nred,nblue,rm,bm):
    for i,(x,y,col,marked) in enumerate(CARDS):
        group=i if i<12 else i-12
        if group < (nred if i<12 else nblue):
            k=group//(3 if i<12 else 4)+1
            face(c,x,y,46,58,col,marked and (rm if i<12 else bm)>=k)

def deck_labels(c,red='12 red cards',blue='20 blue cards'):
    line(c,red,139,132,26,RED);line(c,blue,545,132,26,BLUE)

def stamps(c,x,y,columns,rows,marked,colour,unit=27):
    for j in range(rows):
        for i in range(columns):
            X=x+i*unit;Y=y+j*(unit+6);c.dot(X,Y,unit*.38,colour if i<marked else LIGHT)
            if i<marked:star(c,X,Y,unit*.24,HANDFILL)

def intro(c,t):
    title(c,'A fraction belongs to a particular group')
    for j,(x,n,marked,col) in enumerate([(192,3,1,RED),(627,4,1,BLUE)]):
        copies=(4,5)[j]
        for row in range(copies):
            for i in range(n):
                face(c,x+i*43,169+row*46,36,39,col,i==0 and t>=4.2+row*.24)
        c.text(('1 in 3','1 in 4')[j],x+(n-1)*21.5+18,454,30,col,bold=True)
    if t>=8:line(c,'All marked cards',150,538,30,INK)
    if t>=11.2:line(c,'÷   all cards in both groups',460,538,30,INK)

def uses(c,t):
    title(c,'A group fraction can run in either direction')
    if t<22.6:
        for i in range(3):face(c,175+i*92,230,69,99,RED,t>=20 and i==0)
        for i in range(4):face(c,646+i*92,230,69,99,BLUE,t>=20 and i==0)
        line(c,'One out of three',137,400,29,RED);line(c,'One out of four',634,400,29,BLUE)
    else:
        line(c,'Given the marks',124,209,38,MARK)
        for j in range(9):star(c,155+53*j,301,17,MARK)
        if t>=25.8:
            c.line([(329,360),(329,421)],EDGE,4);c.poly([(317,411),(341,411),(329,430)],EDGE,None)
            line(c,'Recover the size of a group.',130,494,39)

def basic(c,t):
    title(c,'How many cards carry a star?');deck_labels(c)
    decks(c,t,round(12*cue(t,29.56,1.2)),round(20*cue(t,31.7,1.6)),4*cue(t,32.8,1.5),5*cue(t,33.3,1.5))
    if t>=34.8:line(c,'Stars?',936,258,39)
    if t>=37:line(c,'Count each',922,352,28);line(c,'colour first.',922,392,28)

def basic_result(c,t):
    title(c,'One marked card in every row');deck_labels(c,'12 ÷ 3 = 4','20 ÷ 4 = 5' if t>=45.2 else '20 blue cards')
    decks(c,t,12,20,4*cue(t,42.98,1.1),5*cue(t,45.2,1.2))
    if t>=47.6:line(c,'4 + 5',920,267,45)
    if t>=50.4:line(c,'= 9 stars',879,350,43,MARK)

def complete_collection(c,p,show_marks,show_count=False):
    for i,(startx,starty,col,marked) in enumerate(CARDS):
        row,idx=divmod(i,8);x=mix(startx,152+79*idx,p);y=mix(starty,199+row*79,p)
        face(c,x,y,46,58,col,marked and show_marks)
    if show_count:line(c,'32 cards in all',244,540,31)

def medium(c,t):
    title(c,'What fraction of all 32 cards is starred?')
    complete_collection(c,cue(t,54.1,2.6),t>=56.2,True)
    if t>=61.8:line(c,'Starred',867,255,35,MARK)
    if t>=65:
        c.line([(850,304),(1100,304)],INK,3);line(c,'All cards',867,357,35)

def medium_result(c,t):
    title(c,'Keep every card in the denominator');complete_collection(c,1,True,t>=78.2)
    if t>=74.4:line(c,'4 + 5',910,198,33)
    if t>=76.4:line(c,'9',960,280,51,MARK)
    if t>=78.2:
        c.line([(904,324),(1079,324)],INK,4);line(c,'32',941,374,51)
    if t>=83.8:line(c,'Lowest terms',874,486,28,MUTED)

def bundles(c,x,y,groups,colour,marked,cols=6,u=14,gain=None):
    # Six objects, read by columns. Two stars at one third and three at one half.
    bw=u*4.6;bh=u*3.4
    for j in range(groups):
        X=x+(j%cols)*(bw+10);Y=y+(j//cols)*(bh+8)
        c.rect(X,Y,bw,bh,HANDFILL,EDGE,1.6)
        for k in range(6):
            xx=X+u*(.97+(k%3)*1.24);yy=Y+u*(.95+(k//3)*1.36)
            if gain is not None and k==2:
                c.dot(xx,yy,u*.44,LIGHT)
                p=gain[j] if j<len(gain) else 0
                if p>0:star(c,xx,yy-31*(1-p),u*.49*p,MARK)
            elif k<marked:star(c,xx,yy,u*.49,colour)
            else:c.dot(xx,yy,u*.44,LIGHT)

def triple_grid(c,x,y,n,marked,cols=8,u=16):
    for j in range(n):
        X=x+(j%cols)*u*5.25;Y=y+(j//cols)*u*2.43
        c.rect(X,Y,u*4.62,u*1.85,HANDFILL,EDGE,1.5)
        for k in range(3):
            a=X+(k*1.42+.9)*u;b=Y+.9*u
            if k<marked:star(c,a,b,u*.51,BLUE)
            else:c.dot(a,b,u*.45,LIGHT)

def challenge(c,t):
    title(c,'Recover the sizes of groups A and B')
    line(c,'69 items altogether',136,192,40)
    if t>=96.2:
        line(c,'A · one half marked',134,295,33,RED);line(c,'B · one third marked',649,295,33,BLUE)
        stamps(c,164,371,2,1,1,RED,34);stamps(c,682,371,3,1,1,BLUE,34)
    if t>=99.2:line(c,'27 marks altogether',136,456,35,MARK)
    if t>=104.4:line(c,'How many marks if every group used one third?',137,538,28,MUTED)

def baseline(c,t):
    title(c,'Compare against one mark for every three items')
    if t<120.2:
        triple_grid(c,113,219,round(23*cue(t,112.68,2.4)),1)
        if t>=115.4:line(c,'69 ÷ 3 = 23 marks',122,426,37,BLUE)
        if t>=118:
            line(c,'27 − 23 = 4 extra',680,426,36,MARK)
            for j in range(4):
                size=18*cue(t,118+j*.28,.45)
                if size>0:star(c,704+j*55,509,size,MARK)
    else:
        n=1 if t<126.4 else 4
        line(c,'One third',134,163,31,BLUE);line(c,'One half',134,331,31,RED)
        bundles(c,135,201,n,BLUE,2,4,18)
        gains=[cue(t,121.5,.85)]+[cue(t,126.5+j*.36,.72) for j in range(3)]
        bundles(c,135,369,n,RED,3,4,18,gains)
        line(c,'2 marks per 6',736,228,32,BLUE);line(c,'3 marks per 6',736,395,32,RED)
        if t>=123.4:line(c,'Gain one mark per six items',563,302,29,MARK)
        if t>=126.4:line(c,'A = 4 × 6 = 24',138,512,36,RED)
        if t>=130.4:line(c,'B = 69 − 24 = 45',668,512,36,BLUE)

def challenge_check(c,t):
    title(c,'Check the items and the marks separately')
    line(c,'A · 24 items',123,161,32,RED);bundles(c,129,212,4,RED,3 if t>=137.4 else 0,2,17)
    line(c,'B · 45 items',548,161,32,BLUE);triple_grid(c,554,208,15,1 if t>=139.2 else 0,5,14)
    if t>=137.4:line(c,'12 marked',129,414,32,RED)
    if t>=139.2:line(c,'15 marked',552,414,32,BLUE)
    if t>=141.6:line(c,'24 + 45 = 69',127,526,34);line(c,'12 + 15 = 27',550,526,34,MARK)

def mistakes(c,t):
    title(c,'Count the unmarked cards too');complete_collection(c,1,True,t>=156)
    if t<152.8:line(c,'1/3 and 1/4',847,263,30);line(c,'of which groups?',824,333,26,MUTED)
    else:
        line(c,'12 × 1/3 = 4',820,232,31,RED);line(c,'20 × 1/4 = 5',820,301,31,BLUE)
        if t>=156:line(c,'9 out of 32',850,395,34,MARK)

def finish(c,t):
    title(c,'Check the two totals in separate columns')
    X=(151,393,641,905)
    for x,s in zip(X,('Group','Size','Rate','Marked')):line(c,s,x,173,30,MUTED)
    for i,(row,col) in enumerate([(('A','24','1/2','12'),RED),(('B','45','1/3','15'),BLUE)]):
        y=259+i*87
        for x,s in zip(X,row):line(c,s,x,y,39,col)
    if t>=168.6:
        c.line([(143,410),(1100,410)],EDGE,3);line(c,'Baseline',150,461,26,MUTED);line(c,'69 × 1/3 = 23',382,461,30)
    if t>=172.6:line(c,'24 + 45 = 69 items',141,543,31);line(c,'12 + 15 = 27 marks',663,543,31,MARK)

SCENES=(intro,uses,basic,basic_result,medium,medium_result,challenge,baseline,challenge_check,mistakes,finish)
def verify():
    assert len(CARDS)==32 and sum(v[3] for v in CARDS[:12])==4 and sum(v[3] for v in CARDS[12:])==5
    assert gcd(9,32)==1 and Fraction(1,2)-Fraction(1,3)==Fraction(1,6)
    assert [(a,69-a) for a in range(70) if Fraction(a,2)+Fraction(69-a,3)==27]==[(24,45)]
    assert 4*(3-2)==27-23 and 4*6+15*3==69 and 4*3+15==27
