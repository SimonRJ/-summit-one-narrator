"""S059. Grow a three-lamp sign, assemble 63 unit tiles and spend a 636-token stockroom in complete days."""
from captioned_film import cue,font,mix
from itertools import accumulate
ID='S059'
ORIGINAL='538e800ed3b4cecdb729e694129c0e916f5554620fc15cbe9cdbc7188d15d660'
START=(0.,17.72,35.,48.09,60.09,72.7,91.9,109.47,132.02,148.02,161.46)
POSTER=129.8
PAPER='#142431'
INK,DIM,GRID='#fff3d6','#adc3c1','#43606a'
MINT,GOLD,PINK,BLUE='#89d9af','#f0c86e','#ed9b87','#8dc4de'
TONES=('#7ea8c2','#9dcfc6','#e1c375','#db9c79','#b196bb','#80b395','#e38173')
COST=tuple(4*2**i for i in range(8))
TOTAL=tuple(accumulate(COST))
def label(c,s,x,y,z=30,col=INK,anchor='lm'):c.text(s,x,y,z,col,anchor,True)
def title(c,s):
    size=40
    while font(round(size*c.scale),True).getlength(s)>1150*c.scale:size-=1
    label(c,s,58,49,size)
def lamp(c,x,y,r,on,base=GOLD):
    c.dot(x,y,r+3,GRID if not on else '#73684a')
    c.dot(x,y,r,base if on else '#283b42')
    if on:c.dot(x-r*.30,y-r*.30,max(1,r*.24),'#fff4bd')
def sign(c,p,x0=137,y0=202):
    # One founder per lane. Each coloured lane carries its own descendants.
    count=int(p);fraction=p-count
    for row in range(3):
        for j in range(16):
            x=x0+48*j;y=y0+77*row
            active=j<count
            lamp(c,x,y,15,active,(GOLD,MINT,PINK)[row])
            if j==count and fraction:lamp(c,x,y,round(13*fraction)+1,True,(GOLD,MINT,PINK)[row])
def sequence(c,t):
    title(c,'A doubling grows by a different amount each time')
    n=1+cue(t,.6,1.2)+2*cue(t,2.5,1.2)+4*cue(t,4.,1.1)
    for i in range(8):
        lamp(c,171+i*85,248,23,i<int(n))
        lamp(c,171+i*85,396,17,i<int(1+3*cue(t,5,2.6)),BLUE)
    label(c,'×2',924,246,40,GOLD);label(c,'+1',924,396,40,BLUE)
    if t>=10:
        label(c,'1 + 2 + 4 + 8',128,510,30,INK)
        if t>=12.8:label(c,'2 + 4 + 8 + 16',554,510,30,GOLD)
        if t>=14.6:label(c,'16 − 1',949,510,33,MINT)
def term_total(c,t):
    title(c,'One day and the total answer different questions')
    for i,v in enumerate((1,2,4,8)):
        x=194+i*238
        for j in range(v):lamp(c,x+(j%4)*25,215+(j//4)*27,8,True)
        label(c,'Day '+str(i+1),x,334,24,DIM)
        label(c,str(v),x,386,32,GOLD)
    if t>=25:label(c,'On day 4',139,500,27,DIM);label(c,'8',331,500,39,GOLD)
    if t>=28:label(c,'Through day 4',568,500,27,DIM);label(c,'1 + 2 + 4 + 8 = 15',805,500,29,MINT)
    if t>=32.6:label(c,'Doubling the start doubles both answers.',640,568,26,BLUE,'mm')
def lamp_question(c,t):
    title(c,'Three lights on day one · how many on day five?')
    sign(c,1,155,199)
    if t>=38:label(c,'Each lane doubles daily.',192,499,32,DIM)
    if t>=41.6:label(c,'Count the jumps from day 1.',653,499,30,MINT)
def lamp_answer(c,t):
    title(c,'Follow each of the three original lights')
    jumps=(48.5,50.,51.5,53.1)
    n=1+sum(2**j*cue(t,a,1.1) for j,a in enumerate(jumps))
    sign(c,n,111,192)
    day=1+sum(t>=j+1.05 for j in jumps)
    label(c,'Day '+str(day),954,196,32)
    label(c,'3 × '+str(2**(day-1)),950,282,31,MINT)
    if t>=54.6:label(c,'3 × 2⁴',950,364,34,GOLD)
    if t>=57.4:label(c,'48 lights',919,453,38,GOLD)
    for j in range(5):
        x=155+184*j;colour=GOLD if j<day else GRID
        c.dot(x,514,8,colour);label(c,str(j+1),x,549,24,colour,'mm')
        if j<4:c.line([(x+10,514),(x+168,514)],colour,3)
def band_cells():
    # A gnomon decomposition of an 8-by-8 square. Each new rectangle is
    # as large as all the old pieces plus the missing corner, exactly doubling the area.
    return tuple((x,y) for x in range(8) for y in range(8))
def power(x,y):
    if x==y==0:return None
    for j,(w,h) in enumerate(((2,1),(2,2),(4,2),(4,4),(8,4),(8,8))):
        if x<w and y<h:return j
def mosaic(c,x0,y0,size,n,corner=False):
    for x,y in band_cells():
        k=power(x,y);on=k is not None and k<n
        tone=TONES[k] if on else '#243944'
        c.rect(x0+x*size,y0+y*size,size-1,size-1,tone,GOLD if corner and k is None else GRID,1)
    if corner:label(c,'1',x0+size/2,y0+size/2,17,GOLD,'mm')
def sum_question(c,t):
    title(c,'How many tiles are in the first six powers of two?')
    n=sum(t>=60.3+j*.78 for j in range(6))
    mosaic(c,186,143,48,n)
    for j,v in enumerate((1,2,4,8,16,32)):
        if j<n:label(c,str(v),773+j%3*120,208+j//3*121,35,TONES[j])
    if t>=66.2:label(c,'What survives subtraction?',693,447,30)
def subtract(c,t):
    title(c,'Align the shared powers and remove them')
    old=(1,2,4,8,16,32);new=(2,4,8,16,32,64)
    for row,vals in enumerate((old,new)):
        if row and t<74.4:continue
        for j,v in enumerate(vals):
            col=j+row;x=194+col*143;y=180+row*136
            done=(v in old and v in new and t>=79+.48*old.index(v))
            label(c,str(v),x,y,40,GRID if done else (GOLD if row else INK),'mm')
            if done:c.line([(x-30,y+17),(x+30,y-17)],MINT,3)
    label(c,'S',76,180,33,DIM)
    if t>=74.4:label(c,'2S',64,316,33,DIM)
    if t>=82.4:label(c,'2S − S = 64 − 1',118,470,40,INK)
    if t>=87.4:label(c,'63 tiles',855,470,49,MINT)
    if t>=86:mosaic(c,658,414,16,6,True)
def warehouse(c,spent=0):
    # One packet is four tokens. The last row has only nine packets.
    for i in range(159):
        x=119+(i%15)*33;y=160+(i//15)*32
        c.rect(x,y,28,26,'#2c424c' if i<spent else MINT,GRID,1)
        if i>=spent:
            for dx,dy in ((9,8),(19,8),(9,18),(19,18)):c.dot(x+dx,y+dy,1.9,'#29654e')
    label(c,'Each packet holds 4 tokens.',111,550,25,DIM)
def budget_question(c,t):
    title(c,'Stockroom · 636 tokens for complete days')
    warehouse(c)
    if t>=92:label(c,'Day 1 takes 4.',724,223,35,GOLD)
    if t>=95.2:label(c,'Next days take 8, 16, 32, …',694,320,29,DIM)
    if t>=100.6:label(c,'How many whole days?',702,457,32,MINT)
def payment(c,t):
    title(c,'Pay out whole packets, one day at a time')
    n=sum(2**j*cue(t,109.7+j*.85,.77) for j in range(7))
    warehouse(c,round(n))
    if t>=109.7:label(c,'Total for n days',720,161,29,DIM);label(c,'4 × (2ⁿ − 1)',720,222,39,INK)
    if t>=117:label(c,'Day 7 total',720,307,28,DIM);label(c,'508 ≤ 636',738,366,38,MINT)
    if t>=121.4:label(c,'Day 8 total   1,020',719,444,33,PINK)
    if t>=128.2:label(c,'32 packets left = 128 tokens',690,530,28,MINT)
def last_day(c,t):
    title(c,'Could the leftovers fund the next day?')
    # The 128 identical squares on the lower shelf are the next 512-token order.
    for row,n in enumerate((32,128)):
        y=166+row*198
        label(c,'Left over' if row==0 else 'Day 8 needs',102,y,26,DIM)
        for j in range(n):
            x=332+(j%32)*24; yy=y+(j//32)*24
            col=MINT if j<32 else PINK
            c.rect(x,yy,19,18,col if row==0 or t>=134.8 else '#263842',GRID,1)
        if row==0:label(c,'128 tokens',331,y+59,27,MINT)
        elif t>=134.8:label(c,'512 tokens',331,y+124,27,PINK)
    if t>=139.2:label(c,'Every later total is larger.',674,532,29,GOLD)
def indexing(c,t):
    title(c,'Read the word before the day number')
    for j in range(5):
        x=155+j*219;y=260
        label(c,'Day '+str(j+1),x,y-86,25,DIM,'mm')
        label(c,str(3*2**j),x,y,39,GOLD,'mm')
        if t>=150.1:label(c,str(3*(2**(j+1)-1)),x,y+118,35,MINT,'mm')
        if t>=156.2:label(c,str(j)+' jumps',x,y+216,22,DIM,'mm')
    if t>=153.4:label(c,'Gold shows lights on each day. Green adds every day so far.',640,562,27,INK,'mm')
def recap(c,t):
    title(c,'Find the two totals that straddle the budget')
    x0,w,y0,h=157,913,489,298
    def point(i,v):return (x0+i*w/8,y0-v*h/1050)
    c.line([(x0,y0-h-8),(x0,y0),(x0+w+17,y0)],DIM,2)
    y=point(0,636)[1]
    for x in range(x0,x0+w,24):c.line([(x,y),(x+13,y)],GOLD,2)
    label(c,'636',x0-17,y,22,GOLD,'rm')
    previous=point(0,0)
    for i,v in enumerate(TOTAL,1):
        pt=point(i,v);q=cue(t,161.7+.47*i,.6)
        if q:c.line([previous,(mix(previous[0],pt[0],q),mix(previous[1],pt[1],q))],MINT,4)
        if q>.9:c.dot(*pt,5,MINT)
        label(c,str(i),pt[0],y0+30,22,DIM,'mm');previous=pt
    if t>=167.8:label(c,'508',point(7,508)[0]-13,point(7,508)[1]+29,24,MINT,'rm')
    if t>=170.6:label(c,'1,020',point(8,1020)[0]-15,point(8,1020)[1]-16,24,PINK,'rm')
    if t>=171.6:label(c,'Seven complete days',640,562,32,GOLD,'mm')
SCENES=(sequence,term_total,lamp_question,lamp_answer,sum_question,subtract,budget_question,payment,last_day,indexing,recap)
def verify():
    assert len(band_cells())==64 and [sum(power(x,y)==j for x,y in band_cells()) for j in range(6)]==[1,2,4,8,16,32]
    assert 3*2**4==48 and sum(2**j for j in range(6))==63
    assert COST[7]==512 and TOTAL[6]==508<=636<TOTAL[7]==1020
    assert (636-508)//4==32 and len(set((j%15,j//15) for j in range(159)))==159
