"""S079. Sort every integer, badge pair and three-room exhibit into exactly one case."""
from itertools import permutations,product
from math import sin,cos,pi
from captioned_film import cue,mix
ID='S079'
ORIGINAL='da2f2dd65ff100684d42718722c8d9f7f0c1581a50c4262d5523aec82d2887b4'
START=(0,16.92,34.68,48.73,61.53,74.63,88.55,114.27,137.78,153.14,170.1)
POSTER=148.8
PAPER='#23223a'
WHITE,DIM,PANEL,LINE='#fff1d9','#c7c4d4','#34354d','#686982'
RED,BLUE,GOLD,MINT='#ffac9b','#a6cffe','#f9cf75','#a6dfbd'
REDS=tuple('ABCDEF');BLUES=tuple('PQRST')
PATTERNS=('RRR','RBR','BRB')
def pattern(p):return ''.join('R' if s in REDS else 'B' for s in p)
def legal(p):
    key=pattern(p)
    return 'A' in p and ((key=='RRR' and 'B' not in p) or key=='RBR' or (key=='BRB' and p[1]=='A'))
CASES=tuple(tuple(p for p in permutations(REDS+BLUES,3) if legal(p) and pattern(p)==key) for key in PATTERNS)
def txt(c,s,x,y,size=30,col=WHITE,anchor='mm'):
    c.text(s,x,y,size,col,anchor,True)
def heading(c,s):
    txt(c,s,52,54,41,WHITE,'lm');c.line([(52,99),(1227,99)],LINE,2)
def star(c,x,y,r,col):
    c.poly([(x+(r if i%2==0 else r*.43)*cos(-pi/2+i*pi/5),y+(r if i%2==0 else r*.43)*sin(-pi/2+i*pi/5)) for i in range(10)],col,None)
def badge(c,x,y,n,col,r=24):
    c.dot(x,y,r,col)
    if n==0:star(c,x,y,r*.73,PAPER)
    else:txt(c,n,x,y,round(r*.99),PAPER)
def exhibit(c,x,y,ch,r=27):
    col=RED if ch in REDS else BLUE
    # The red collection uses square frames; blue pieces use round frames.
    if ch in REDS:c.rect(x-r,y-r,2*r,2*r,col,None)
    else:c.dot(x,y,r,col)
    txt(c,ch,x,y,round(r*1.1),PAPER)
def rooms(c,x,y,triplet,u=88,labels=False):
    for k,ch in enumerate(triplet):
        xx=x+k*u;c.rect(xx-u*.45,y-u*.43,u*.88,u*.86,PANEL,LINE,2)
        if ch:exhibit(c,xx,y,ch,u*.29)
        if labels:txt(c,('Left','Middle','Right')[k],xx,y+u*.69,round(u*.23),DIM)
def dots(c,x,y,n,col,extent,step=12):
    for j in range(min(n,round(n*extent))):
        c.dot(x+j%10*step,y+j//10*step,step*.33,col)
def opening(c,t):
    heading(c,'Every outcome needs exactly one home')
    for i,(p,key) in enumerate(zip((('A','C','D'),('A','Q','F'),('P','A','R')),PATTERNS)):
        at=.5+3.8*i
        if t<at:continue
        y=190+118*i
        step=cue(t,at,1.3)
        rooms(c,mix(235,559,step),y,p,74)
        txt(c,key,976,y,37,(RED,GOLD,BLUE)[i])
    txt(c,'R = red      B = blue',270,467,25,DIM)
    if t>9:txt(c,'Use the order of the colours to name a row.',640,556,31,MINT)
def exam(c,t):
    heading(c,'Choose a rule that separates the cases')
    rooms(c,207,288,('A','P','E'),102,True)
    if t>20.4:txt(c,'Read left to right',388,455,28,DIM)
    if t>23:
        for k,key in enumerate(PATTERNS):
            y=195+k*106
            c.rect(816,y-32,217,64,PANEL,MINT if k==1 else LINE,3)
            txt(c,key,925,y,33,MINT if k==1 else WHITE)
        txt(c,'Red · blue · red',919,526,29,MINT)
def parity(c,t):
    solving=t>=START[3]
    heading(c,'Odd and even from 20 through 30')
    if solving:move=1
    else:move=cue(t,39.2,3.0)
    for j,n in enumerate(range(20,31)):
        orig=104+j*106
        x=mix(orig,311+(j//2)*127,move)
        y=mix(294,247 if n%2==0 else 412,move)
        c.dot(x,y,28,BLUE if n%2==0 else RED)
        txt(c,n,x,y,25,PAPER)
    if move>.5:
        txt(c,'Even',149,247,31,BLUE);txt(c,'Odd',149,412,31,RED)
    if not solving and t>43:txt(c,'Each row advances by 2.',640,541,30)
    if solving and t>49.1:txt(c,'6',1103,247,43,BLUE)
    if solving and t>54:txt(c,'5',1103,412,43,RED)
    if solving and t>56:txt(c,'11 integers = 6 even + 5 odd',640,549,34,MINT)
def badge_q(c,t):
    heading(c,'One red badge and one blue badge')
    for row,(n,col) in enumerate(((5,RED),(6,BLUE))):
        for j in range(n):
            if t>61.5+row*.45+j*.17:badge(c,227+j*93,235+145*row,j,col,32)
    if t>65:txt(c,'One star of each colour',971,266,27,GOLD)
    if t>68:txt(c,'Exactly one star',971,356,36)
    if t>70:txt(c,'Which colour could supply it?',640,541,30,MINT)
def badge_a(c,t):
    heading(c,'Give each legal pair a place in the grid')
    x0,y0,step=232,221,61
    for j in range(6):badge(c,x0+j*step,y0-65,j,BLUE,22)
    for i in range(5):
        badge(c,x0-66,y0+i*step,i,RED,22)
        for j in range(6):
            legal_cell=(i==0)^(j==0)
            show=(i==0 and t>74.8+.42*j) or (j==0 and t>78.3+.43*i)
            c.rect(x0+j*step-24,y0+i*step-24,48,48,RED if show and legal_cell and i==0 else BLUE if show and legal_cell else PANEL,LINE,1)
            if show and legal_cell:txt(c,'✓',x0+j*step,y0+i*step,24,PAPER)
            if i==0 and j==0:txt(c,'×',x0,y0,25,GOLD)
    if t>=76:txt(c,'Red star: 5 blue partners',913,236,28,RED)
    if t>=79.5:txt(c,'Blue star: 4 red partners',913,327,28,BLUE)
    if t>=83:txt(c,'5 + 4 = 9 pairs',913,442,38,MINT)
def challenge(c,t):
    heading(c,'Three named rooms, eleven distinct exhibits')
    for j,s in enumerate(REDS):exhibit(c,100+72*j,195,s,24)
    for j,s in enumerate(BLUES):exhibit(c,100+72*j,291,s,24)
    if t>=92:rooms(c,786,242,(None,None,None),126,True)
    if t>=96:txt(c,'Every display uses A.',310,385,27,GOLD)
    conditions=((98,'RRR: exclude B.'),(101,'RBR: blue in the middle.'),(105,'BRB: A in the middle.'))
    for i,(at,s) in enumerate(conditions):
        if t>at:txt(c,s,718,398+64*i,26,(RED,GOLD,BLUE)[i],'lm')
    if t>=109:txt(c,'How many displays?',309,507,35)
def casework(c,t):
    heading(c,'Read the room colours, then multiply the choices')
    j=0 if t<121.7 else 1 if t<128.9 else 2
    start=(114.27,121.7,128.9)[j]
    if j==0:
        k=min(2,int(max(0,t-start)/1.65));p=[c for c in ('C','D')];p.insert(k,'A')
        formula='3 × 4 × 3 = 36'; lines=('3 places for A','4 eligible reds for the next room','3 remaining reds for the last')
    elif j==1:
        p=('A','Q','B') if t<124.8 else ('B','Q','A')
        formula='2 × 5 × 5 = 50'; lines=('2 ends for A','5 other reds, including B','5 blue middle exhibits')
    else:
        p=CASES[2][int((t-start)/1.4)%len(CASES[2])]
        formula='5 × 1 × 4 = 20'; lines=('5 blues on the left','A must occupy the middle','4 different blues on the right')
    if j==0 or j==1:
        if j==0:
            phase=min(2,int((t-start)/1.65))
            old=[('A','C','D'),('C','A','D'),('C','D','A')][max(0,phase-1)]
            progress=cue(t,start+phase*1.65,.92) if phase else 1
        else:
            old=('A','Q','B')
            progress=cue(t,124.8,1.25) if t>=124.8 else 1
        rooms(c,177,281,(None,None,None),128,True)
        for ch in p:
            left,right=old.index(ch),p.index(ch)
            x=177+128*mix(left,right,progress)
            y=281+(1 if right<left else -1)*44*sin(pi*progress) if right!=left else 281
            exhibit(c,x,y,ch,37)
    else:
        rooms(c,177,281,p,128,True)
    txt(c,'Case '+PATTERNS[j],311,460,37,(RED,GOLD,BLUE)[j])
    for k,s in enumerate(lines):
        if t>start+k*.9:txt(c,s,943,189+k*75,26,DIM)
    if t>start+3.4:txt(c,formula,937,469,38,MINT)
    if t>134.5:txt(c,'Each complete display has just one colour pattern.',640,568,29)
def totals(c,t):
    heading(c,'Disjoint colour patterns cover every legal display')
    for j,(group,key) in enumerate(zip(CASES,PATTERNS)):
        px=112+j*392
        txt(c,key,px+92,161,29,(RED,GOLD,BLUE)[j])
        example=group[(int((t-START[8])/2)*3)%len(group)]
        rooms(c,px+23,244,example,68)
        p=cue(t,137.9+j*1.0,.95)
        dots(c,px+24,326,len(group),(RED,GOLD,BLUE)[j],p,15)
        if p==1:txt(c,len(group),px+100,455,38)
    if t>142:txt(c,'36 + 50 + 20 = 106 arrangements',640,539,39,MINT)
    if t>146:txt(c,'Exhibit B is excluded only from the all-red case.',640,586,24,DIM)
def mistakes(c,t):
    heading(c,'At least one star or exactly one star?')
    for j,p in enumerate(((0,1),(1,0),(0,0))):
        x=203+376*j
        badge(c,x,245,p[0],RED,38);badge(c,x+90,245,p[1],BLUE,38)
        txt(c,('Red star only','Blue star only','Two stars')[j],x+45,354,26)
        if t>155+j*.55:txt(c,'Allowed' if j<2 else 'Excluded',x+45,433,30,MINT if j<2 else GOLD)
    if t>160:txt(c,'Both-star pairs satisfy “at least one”. Exactly one excludes them.',640,538,28)
def recap(c,t):
    heading(c,'Test your split before adding')
    rooms(c,188,269,('Q','A','S'),110,True)
    for j,key in enumerate(PATTERNS):
        if t>171+j*.5:
            y=202+87*j
            txt(c,key,867,y,31,MINT if j==2 else DIM)
            if j==2 and t>175:txt(c,'✓',1009,y,39,MINT)
    if t>174:txt(c,'This display belongs only in BRB.',352,456,26,MINT)
    if t>180:txt(c,'Cover every allowed display once. Add 36, 50 and 20.',640,548,30)
SCENES=(opening,exam,parity,parity,badge_q,badge_a,challenge,casework,totals,mistakes,recap)
def verify():
    assert len([n for n in range(20,31) if n%2==0])==6
    assert sum((r==0)^(b==0) for r,b in product(range(5),range(6)))==9
    assert tuple(map(len,CASES))==(3*4*3,2*5*5,5*4)==(36,50,20)
    assert len(set().union(*map(set,CASES)))==106
    assert not any('B' in p for p in CASES[0])
    assert ('B','Q','A') in CASES[1] and ('Q','A','S') in CASES[2]
