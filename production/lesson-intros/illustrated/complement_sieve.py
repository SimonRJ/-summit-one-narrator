"""S062. Build the sixteen strings, merge duplicate pupils and sieve the 84 actual integers by their divisor stamps."""
from itertools import product,combinations
from captioned_film import cue,font,mix
ID='S062'
ORIGINAL='88e9a5a4da124e68f6b6a9ebdf10be1d19a0f98f1c2a9b4431ca9c1a6e207a7b'
START=(0.,16.76,33.24,47.13,59.13,73.18,85.5,98.6,125.95,139.08,153.16)
POSTER=136.9
PAPER='#f5f0e2'
INK,SOFT,GRID='#233d45','#53696f','#c7c9bb'
MINT,GREEN,TEAL='#bedec9','#20745d','#4b91a2'
TINT,RED,BLUE,GOLD='#fbf8eb','#ad624e','#396e9d','#a68030'
DIVISORS=(2,3,5);PIGMENT=(RED,BLUE,GOLD)
WORDS=tuple(''.join(x) for x in product('HT',repeat=4))
def label(c,s,x,y,z=29,col=INK,anchor='lm'):c.text(s,x,y,z,col,anchor,True)
def title(c,s):
    z=40
    while font(round(z*c.scale),True).getlength(s)>1150*c.scale:z-=1
    label(c,s,62,52,z)
def ticket(c,word,x,y,w=103,h=42,select=False,reject=False):
    c.rect(x,y,w,h,'#e2e3d7' if reject else MINT if select else TINT,GREEN if select else GRID,2)
    label(c,word,x+w/2,y+h/2,round(h*.54),SOFT if reject else INK,'mm')
    if reject:c.line([(x+6,y+h-4),(x+w-6,y+4)],RED,3)
def pupil(c,num,x,y,tags,r=22):
    c.dot(x,y,r,TINT)
    if 'T' in tags:c.draw.arc(c.xy((x-r,y-r,x+r,y+r)),90,270,fill=GREEN,width=max(2,round(5*c.scale)))
    if 'S' in tags:c.draw.arc(c.xy((x-r,y-r,x+r,y+r)),-90,90,fill=BLUE,width=max(2,round(5*c.scale)))
    label(c,str(num),x,y,max(14,round(r*.75)),INK,'mm')
def square_rules(c,n,x,y,active,view='stamps',w=49,h=49):
    hits=[d for d in DIVISORS if n%d==0]
    remain=not hits
    fill=(MINT if remain else '#e6e6d9') if view=='survivors' else TINT
    c.rect(x,y,w-3,h-3,fill,GREEN if view=='survivors' and remain else GRID,1)
    label(c,str(n),x+(w-3)/2,y+.36*h,min(46,max(21,round(.44*w))),INK if view!='survivors' or remain else SOFT,'mm')
    for j,d in enumerate(DIVISORS):
        if d in hits and d in active:
            c.rect(x+w*(.10+.27*j),y+h*.72,w*.20,max(5,h*.11),PIGMENT[j])
    if view=='triple' and len(hits)==3:c.rect(x,y,w-3,h-3,None,GREEN,3)
def hundred(c,active,view='stamps'):
    for n in range(1,85):
        i=n-1;square_rules(c,n,84+(i%12)*51,128+(i//12)*54,active,view,51,54)
def complements(c,t):
    title(c,'Count the group outside the rule')
    for i,word in enumerate(('HH','HT','TH','TT')):
        x=140+i*250
        ticket(c,word,x,218,159,85,select=t>=3.6 and 'T' in word,reject=t>=6 and 'T' not in word)
    if t>=6.6:label(c,'4 possibilities − 1 with no T = 3 with a T',148,385,33,GREEN)
    if t>=10.6:
        for j,n in enumerate((6,10,15,30)):square_rules(c,n,347+j*127,467,DIVISORS,'stamps',90,75)
        label(c,'Which numbers receive more than one stamp?',640,580,25,SOFT,'mm')
def exam(c,t):
    title(c,'“At least one” and “none” divide the same set')
    for i,word in enumerate(WORDS):
        ticket(c,word,134+(i%4)*152,161+(i//4)*83,120,54,select=t>=20.8 and 'T' in word,reject=False)
    if t>=20.8:label(c,'1 with no T',821,213,34,RED);label(c,'15 with a T',821,299,34,GREEN)
    if t>=24.6:
        square_rules(c,30,876,387,DIVISORS,'triple',87,65)
        if t>=28.6:label(c,'One number, three rules.',740,514,28)
def letters(c,t):
    title(c,'Write four letters using H or T')
    for i,l in enumerate('HTHT'):
        x=250+i*238;c.line([(x-57,367),(x+57,367)],SOFT,3)
        if t>=33.5+i*.46:ticket(c,l,x-38,242,76,75)
        label(c,'Slot '+str(i+1),x,427,24,SOFT,'mm')
    if t>=38.2:label(c,'How many strings contain at least one T?',640,528,36,INK,'mm')
def sixteen(c,t):
    title(c,'Lay out the full sample space')
    f=cue(t,47.2,2.1)
    for i,s in enumerate(WORDS):
        if i+1>max(1,16*f):continue
        ticket(c,s,132+i%4*160,150+i//4*91,135,62,t>=55.4 and 'T' in s,t>=52.6 and 'T' not in s)
    if t>=49.6:label(c,'2 × 2 × 2 × 2 = 16',801,219,32)
    if t>=52.6:label(c,'Only HHHH misses.',801,319,30,RED)
    if t>=55.4:label(c,'16 − 1 = 15',801,426,42,GREEN)
def class_question(c,t):
    title(c,'Count people who play tennis or swim')
    for i in range(11):pupil(c,i+1,148+(i%6)*87,201+(i//6)*75,'T',25)
    if t>=60.8:
        for i in range(9):pupil(c,i+8,725+(i%5)*83,201+(i//5)*75,'S',25)
    label(c,'Tennis · 11',153,384,30,GREEN)
    if t>=60.8:label(c,'Swimming · 9',725,384,30,BLUE)
    if t>=63:label(c,'Pupils 8–11 appear on both lists.',640,509,32,RED,'mm')
def class_answer(c,t):
    title(c,'Two registrations can belong to the same pupil')
    f=cue(t,76.4,3.7)
    # Merge the duplicate registration for pupils 8, 9, 10 and 11 onto its matching pupil.
    for i in range(1,17):
        x=149+((i-1)%8)*110;y=185+((i-1)//8)*94
        tags='T' if i<8 else 'S' if i>11 else 'TS' if f>.94 else 'T'
        pupil(c,i,x,y,tags,27)
    if f<.97:
        for j,n in enumerate(range(8,12)):
            dest=(149+((n-1)%8)*110,185+((n-1)//8)*94)
            pupil(c,n,mix(264+151*j,dest[0],f),mix(447,dest[1],f),'S',25)
    if t>=73.2:label(c,'11 + 9 = 20 registrations',121,554,32)
    if t>=81.6:label(c,'20 − 4 = 16 pupils',709,554,32,GREEN)
def sieve_question(c,t):
    title(c,'Which integers from 1 through 84 survive?')
    hundred(c,())
    label(c,'84 integers',777,195,35)
    if t>=89:
        for j,d in enumerate(DIVISORS):label(c,'Divisible by '+str(d),780,277+j*62,27,PIGMENT[j])
    if t>=92.4:label(c,'Exclude any integer on a list.',738,495,27)
def inclusion(c,t):
    title(c,'Stamp every multiple on the same number board')
    active=tuple(d for d,a in zip(DIVISORS,(99.,101.2,103.3)) if t>=a)
    hundred(c,active,'triple' if t>=118 else 'stamps')
    for i,d in enumerate(DIVISORS):
        if d in active:label(c,'×'+str(d)+'   '+str(84//d),786+i*133,163,25,PIGMENT[i])
    if t>=108.8:label(c,'Pair intersections',774,246,28,SOFT)
    for j,(q,n) in enumerate(((6,14),(10,8),(15,5))):
        if t>=112.+j*.78:label(c,'×'+str(q)+'   '+str(n),781+j*135,310,23,INK)
    if t>=118:
        square_rules(c,30,795,362,DIVISORS,'triple',100,82)
        square_rules(c,60,942,362,DIVISORS,'triple',100,82)
    if t>=121.8:label(c,'3 stamps − 3 pairs + 1 = 1',743,486,26)
    if t>=123.8:label(c,'Add both triple matches back.',733,545,26,GREEN)
def survivors(c,t):
    title(c,'Remove the 61 excluded integers once')
    hundred(c,DIVISORS,'survivors' if t>=130.4 else 'stamps')
    label(c,'42 + 28 + 16',778,205,34)
    if t>=126.6:label(c,'− 14 − 8 − 5 + 2',778,268,30)
    if t>=128.4:label(c,'= 61 excluded',778,335,34,RED)
    if t>=133.8:label(c,'84 − 61 = 23',778,447,39,GREEN)
def exactly(c,t):
    title(c,'“Exactly one” counts a different set')
    for j,n in enumerate((7,8,6,30)):
        square_rules(c,n,144+j*245,196,DIVISORS,'triple',158,97)
        hits=sum(n%d==0 for d in DIVISORS)
        if t>=142:label(c,str(hits)+' rules',216+j*245,352,26,GREEN if hits==0 else SOFT,'mm')
    if t>=146:label(c,'30 is in (2, 3), (2, 5) and (3, 5).',640,454,34,INK,'mm')
    if t>=149.8:label(c,'Its net count is 3 − 3 + 1.',640,527,32,GREEN,'mm')
def recap(c,t):
    title(c,'Check the complement against its whole')
    hundred(c,DIVISORS,'survivors' if t>=155.8 else 'stamps')
    label(c,'Inclusive whole = 84',747,192,32)
    if t>=155.8:label(c,'Green means no stamps.',747,281,29,GREEN)
    if t>=158.2:label(c,'Excluded union = 61',747,375,30,RED)
    if t>=161.6:label(c,'23 + 61 = 84',747,485,38)
SCENES=(complements,exam,letters,sixteen,class_question,class_answer,sieve_question,inclusion,survivors,exactly,recap)
def verify():
    assert len(WORDS)==16 and sum('T' in w for w in WORDS)==15
    tennis=set(range(1,12));swim=set(range(8,17))
    assert len(tennis&swim)==4 and len(tennis|swim)==16
    sets=[set(range(d,85,d)) for d in DIVISORS]
    assert list(map(len,sets))==[42,28,16]
    assert [len(a&b) for a,b in combinations(sets,2)]==[14,8,5]
    assert set.intersection(*sets)=={30,60} and len(set.union(*sets))==61
    assert len([n for n in range(1,85) if all(n%d for d in DIVISORS)])==23
