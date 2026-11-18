"""S046: lift margins off a score, rebuild three teams, and transfer nine actual points."""
from math import sin, pi
from captioned_film import cue, mix
ID='S046'
ORIGINAL='70ba8e4186c8dd4d6f09e8435761081280eeeb9c85abe79e92dbfe657a53e0dc'
START=(0,16.76,37.4,51.14,62.99,78.32,94.8,113.49,136.36,151.08,164.36)
POSTER=143.65
PAPER='#1c243e';WHITE='#fff4de';SOFT='#c3c9da';SHADOW='#131c31';EDGE='#56607c'
BLUE='#7dd8ee';ORANGE='#ffc782';PINK='#f49fae';GREEN='#b3e5b2';COL=(BLUE,ORANGE,PINK)

def name(c,s,x,y,size=29,col=WHITE,anchor='mm'):
    c.text(s,x,y,size,col,anchor,True)
def title(c,s):name(c,s,58,64,39,WHITE,'lm')
def chip(c,x,y,w,col):
    c.rect(x-w/2,y-w/2,w,w,col)
    if w>=14:c.line([(x-w*.3,y-w*.25),(x+w*.25,y-w*.25)],SHADOW,1.5)

def row(c,y,n,base,tag,u=24,drop=0,x=221):
    name(c,tag,x-38,y,26,SOFT,'rm')
    for i in range(n):
        chip(c,x+i*u,y-(drop if i>=base else 0),u*.78,ORANGE if i>=base else BLUE)
    c.line([(x-u*.45,y+u*.68),(x+(n-.55)*u,y+u*.68)],EDGE,2)

def basic_demo(c,t):
    title(c,'Measure the gap between the two scores')
    base,win=5,8
    row(c,228,base,base,'Blue',u=45)
    row(c,345,base+round(3*cue(t,3.8,2.1)),base,'Gold',u=45)
    if t>=6.6:
        x=221+5*45;y=397;c.line([(x-17,y),(x-17,y+14),(x+107,y+14),(x+107,y)],ORANGE,3)
        name(c,'margin 3',x+45,452,27,ORANGE)
    if t>=9:name(c,'Blue   5',905,240,34,BLUE);name(c,'Gold   5 + 3',905,338,34,ORANGE)
    if t>=12.4:name(c,'Total   13 points',903,460,29,GREEN)

def exams(c,t):
    title(c,'One pair of scores must satisfy both clues')
    row(c,247,8,8,'First',u=36);row(c,350,8+round(4*cue(t,20.4,2)),8,'Second',u=36)
    if t>=23.4:name(c,'same base',391,446,26,BLUE);name(c,'4 extra',565,490,27,ORANGE)
    if t>=27.8:name(c,'Total   20',950,271,32,GREEN);name(c,'Margin   4',950,355,32,ORANGE)
    if t>=33.2:name(c,'8 + 12 = 20',949,441,28);name(c,'12 − 8 = 4',949,504,28)

def base_piece(c,x,y,w,v,col=BLUE):
    c.rect(x,y,w,52,SHADOW,col,3);name(c,v,x+w/2,y+26,29,col)

def basic_q(c,t):
    title(c,'Two teams share 42 points')
    for i,k in enumerate(('lower','higher')):
        yy=216+i*113;name(c,k,206,yy+26,27,SOFT,'rm');base_piece(c,243,yy,360,'same score')
        if i and t>=40.6:
            d=cue(t,44,2);base_piece(c,604+37*d,yy-54*d,120,'+6',ORANGE)
    if t>=42.6:name(c,'What is each score?',971,245,30)
    if t>=44:name(c,'Lift off the lead.',974,414,29,ORANGE)

def basic_a(c,t):
    title(c,'Lift six points off the higher score')
    lift=cue(t,51.2,1.6)*(1-cue(t,60.4,1.6))
    row(c,242,18,18,'lower',u=28)
    row(c,362,24,18,'higher',u=28,drop=70*lift)
    if t>=53.4:name(c,'42 − 6 = 36',1029,200,29,ORANGE)
    if t>=55.8:name(c,'36 ÷ 2 = 18',1029,277,29,BLUE)
    if t>=57.6:name(c,'18 and 24',1029,387,33,GREEN)
    if t>=60.4:name(c,'24 − 18 = 6',1029,471,27)

def symbolic(c,t,solved):
    title(c,'Build each score up from the lowest')
    for i,tag in enumerate(('lowest','middle','highest')):
        y=183+i*104;name(c,tag,194,y+25,26,SOFT,'rm');base_piece(c,225,y,288,'12' if solved and t>=88.4 else 'x')
        if i>=1 and (solved or t>=63.1):base_piece(c,515,y,72,'+3',ORANGE)
        if i==2 and (solved or t>=65.8):base_piece(c,589,y,120,'+5',PINK)
    if not solved and t>=68.4:name(c,'Total   47',973,257,34,GREEN)
    if solved:
        if t>=82.4:name(c,'3 + 5 = 8 extra',976,207,27,PINK)
        if t>=85.2:name(c,'47 − 3 − 8 = 36',976,285,27,ORANGE)
        if t>=88.4:name(c,'36 ÷ 3 = 12',976,367,30,BLUE)
        if t>=90.2:name(c,'12, 15, 20',976,462,36,GREEN)

def medium_q(c,t):symbolic(c,t,False)
def medium_a(c,t):symbolic(c,t,True)

def rack(c,t,question):
    title(c,'How can all three teams finish level?' if question else 'Rebuild the three original scores')
    when=0 if not question else 98.8
    for i,tag in enumerate('ABC'):
        y=176+i*104;name(c,tag,129,y+27,34,COL[i]);base_piece(c,177,y,272,'16' if not question and t>=125.6 else 'c',PINK)
        if i<2 and t>=when:base_piece(c,451,y,187,'+11',ORANGE)
        if i==0 and t>=when:base_piece(c,640,y,85,'+5',BLUE)
    if question:
        name(c,'Total   75 points',984,227,31,GREEN)
        if t>=103.2:name(c,'A and B give to C.',984,348,29)
        if t>=107.6:name(c,'How many from each?',984,434,25,ORANGE)
    else:
        if t>=117:name(c,'B = c + 11',973,185,27,ORANGE)
        if t>=118.2:name(c,'A = c + 16',973,237,27,BLUE)
        if t>=120:name(c,'75 − 11 − 16 = 48',973,309,27)
        if t>=125.6:name(c,'C = 48 ÷ 3 = 16',973,369,27,PINK)
        if t>=127.4:name(c,'A 32    B 27    C 16',973,441,26,GREEN)
        if t>=131.4:name(c,'Target   75 ÷ 3 = 25',974,518,26)

def transfer_q(c,t):rack(c,t,True)
def solve_scores(c,t):rack(c,t,False)

CENTRES=(250,640,1030)
NAMES='ABC'
SCORES=(32,27,16)
def place(team,j):
    return CENTRES[team]-100+j%8*28.5,439-(j//8)*42

def ledger(c,t,start):
    for i,x in enumerate(CENTRES):
        c.rect(x-143,206,286,270,SHADOW,EDGE,2)
        name(c,'Team '+NAMES[i],x,168,30,COL[i])
    # Each named point has one address. Only the nine donated points change addresses.
    count=[0,0,0];flight=0
    counter=0
    for team,n in enumerate(SCORES):
        for j in range(n):
            sx,sy=place(team,j);ex,ey=sx,sy;p=0;dest=team
            if team<2 and j>=25:
                dest=2;ex,ey=place(2,16+counter)
                p=cue(t,start+.32*counter,1.0)
                counter+=1
            x=mix(sx,ex,p);y=mix(sy,ey,p)-(119 if team==0 else 67)*sin(pi*p)
            chip(c,x,y,19,COL[team])
            if p==0:count[team]+=1
            elif p==1:count[dest]+=1
            else:flight+=1
    for i,x in enumerate(CENTRES):name(c,count[i],x,507,35,COL[i])
    if flight:name(c,f'{flight} in transit',640,569,24,SOFT)
    return count

def exchange(c,t):
    title(c,'Move seven points from A and two from B')
    ledger(c,t,138.5)
    if t>=143:name(c,'25 + 25 + 25 = 75',639,570,30,GREEN)

def mistake(c,t):
    if t<156.8:
        title(c,'The margin is the extra part of the score')
        row(c,243,7,7,'lower',u=42);row(c,366,10,7,'higher',u=42,drop=54*cue(t,152.4,1.7))
        name(c,'10 − 7 = 3',943,273,35,ORANGE)
        if t>=154.4:name(c,'Scores   7 and 10',943,398,27,BLUE)
    else:
        title(c,'A transfer changes the split of a fixed total')
        ledger(c,t,156.9)
        if t>=161:name(c,'The 75 original points are all here.',640,565,29,GREEN)

def finish(c,t):
    title(c,'Check the scores against the original clues')
    for i,(tag,n) in enumerate(zip('ABC',SCORES)):
        yy=178+i*111;row(c,yy,n,16,tag,u=18.5,x=148)
        name(c,n,790,yy,28,COL[i])
    if t>=169:name(c,'points',790,496,24,SOFT)
    if t>=171.6:name(c,'32 − 27 = 5',1035,211,29,BLUE)
    if t>=174:name(c,'27 − 16 = 11',1035,310,29,ORANGE)
    if t>=176.6:name(c,'32 + 27 + 16 = 75',1035,410,25,GREEN)

SCENES=(basic_demo,exams,basic_q,basic_a,medium_q,medium_a,transfer_q,solve_scores,exchange,mistake,finish)
def verify():
    assert [(a,b) for a in range(43) for b in range(43) if a+b==42 and b-a==6]==[(18,24)]
    assert [(a,a+3,a+8) for a in range(48) if 3*a+11==47]==[(12,15,20)]
    assert [(c+16,c+11,c) for c in range(76) if 3*c+27==75]==[SCORES]
    assert (32-7,27-2,16+7+2)==(25,25,25)
    assert len({place(i,j) for i,n in enumerate(SCORES) for j in range(n)})==75
    assert len({place(i,j) for i in range(3) for j in range(25)})==75
