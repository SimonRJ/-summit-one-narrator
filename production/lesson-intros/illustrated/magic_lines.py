"""S073. Follow each sum through the grid, keeping track of the shared centre."""
from itertools import permutations
from math import hypot
from captioned_film import cue, mix

ID = 'S073'
ORIGINAL = '97cee91597f3e23f7173f8bb73f5b08764cdc6e6256e71b2e5bcfc0a4fe4ac8a'
START = (0,17.24,33.24,45.22,56.74,77.03,101.02,117.15,138.42,155.86,170.42)
POSTER = 135.8
PAPER, TILE, LINE = '#172236','#22344a','#4e6377'
TEXT, MUTED, GOLD, JADE, SKY, ROSE = '#fff5e6','#bfcedb','#fbd37a','#8be2c5','#a6cfff','#ffac9d'
SQUARE = (8,1,6,3,5,7,4,9,2)
ROWS = ((0,1,2),(3,4,5),(6,7,8))
COLS = ((0,3,6),(1,4,7),(2,5,8))
DIAGS = ((0,4,8),(2,4,6))
LINES = ROWS + COLS + DIAGS
CROSS = (ROWS[1],COLS[1],*DIAGS)
COLOURS = (JADE,SKY,GOLD,ROSE)

def text(c,s,x,y,z=30,colour=TEXT,anchor='mm'):
    c.text(s,x,y,z,colour,anchor,True)

def title(c,s):
    text(c,s,52,58,41,TEXT,'lm')
    c.line([(52,103),(1228,103)],LINE,2)

def cell(i,x,y,step):
    return x+step*(i%3), y+step*(i//3)

def tiles(c,x,y,step,values,marked=()):
    for i,n in enumerate(values):
        px,py=cell(i,x,y,step);side=step-6
        c.rect(px-side/2,py-side/2,side,side,TILE,GOLD if i in marked else LINE,3 if i in marked else 2)
        if n is not None:text(c,n,px,py,round(step*.48),GOLD if i in marked else TEXT)

def stroke(c,line,x,y,step,f,colour):
    if f<=0:return
    a,b=cell(line[0],x,y,step),cell(line[-1],x,y,step)
    dx,dy=b[0]-a[0],b[1]-a[1]; length=hypot(dx,dy)
    ux,uy=dx/length,dy/length
    # Draw parallel to the values, leaving the digits unobstructed.
    off=step*.30; sx=a[0]-uy*off-ux*.34*step;sy=a[1]+ux*off-uy*.34*step
    ex=b[0]-uy*off+ux*.34*step;ey=b[1]+ux*off+uy*.34*step
    c.line([(sx,sy),(mix(sx,ex,f),mix(sy,ey,f))],colour,5)

def equation(c,s,x,y,colour=JADE):
    text(c,s,x,y,36,colour)

def opening(c,t):
    title(c,'One target for every straight line')
    board=[2,None,4,7,5,3,6,1,8]
    tiles(c,234,215,117,board)
    if t<7:
        row=ROWS[0] if t<2.6 else COLS[2] if t<4.8 else DIAGS[0]
        at=0 if t<2.6 else 2.6 if t<4.8 else 4.8
        stroke(c,row,234,215,117,cue(t,at,.8),JADE)
        text(c,'Row' if t<2.6 else 'Column' if t<4.8 else 'Long diagonal',894,283,40,JADE)
    elif t<11:
        stroke(c,ROWS[0],234,215,117,1,GOLD)
        equation(c,'2 + □ + 4 = 15',901,293,GOLD)
        text(c,'Follow the line with one blank.',901,393,27,MUTED)
    else:
        for j,line in enumerate(CROSS):stroke(c,line,234,215,117,cue(t,11+.64*j,.7),COLOURS[j])
        text(c,'Four lines meet here.',894,291,39)
        text(c,'Which cell do they share?',894,395,28,MUTED)

def exam(c,t):
    title(c,'Find the target before filling blanks')
    vals=[4,3,8,9,5,1,2,7,6]
    for i in (1,3,7):vals[i]=None
    tiles(c,244,214,115,vals)
    stroke(c,COLS[2],244,214,115,cue(t,17.4,1.3),JADE)
    if t>20:equation(c,'8 + 1 + 6 = 15',898,237)
    if t>23:
        stroke(c,ROWS[0],244,214,115,cue(t,23,1.2),GOLD)
        equation(c,'4 + □ + 8 = 15',898,344,GOLD)
    if t>28:
        stroke(c,DIAGS[1],244,214,115,cue(t,28.3,1.2),ROSE)
        text(c,'Include both long diagonals.',901,459,29,ROSE)

def simple(c,t):
    answering=t>=START[3]
    title(c,'One empty cell in a row of fifteen')
    for j,n in enumerate((4,5,6 if t>50.6 else '?')):
        if not answering and t < START[2]+j*1.1:continue
        x=296+j*180
        c.rect(x-67,176,134,107,TILE,GOLD if j==2 else LINE,3)
        text(c,n,x,230,56,GOLD if j==2 else TEXT)
    text(c,'= 15',907,230,59,JADE)
    for j in range(15):
        p=cue(t,(45.3+j*.085 if j<9 else 50.3+(j-9)*.15),.6) if answering else 0
        x=229+j*58
        if answering or t>=35+j*.14:c.dot(x,385,20,LINE)
        if p:c.dot(x,385,19*p,SKY if j<4 else JADE if j<9 else GOLD)
    if not answering:text(c,'Four and five are already in the row. What is missing?',640,508,32)
    elif t<50.6:equation(c,'4 + 5 = 9',640,508)
    else:equation(c,'15 − 9 = 6',640,508,GOLD)

def full_set(c,t):
    title(c,'Use 1 to 9 exactly once')
    tiles(c,220,219,106,(None,)*9,(4,))
    for i in range(9):
        x=715+(i%3)*122;y=203+(i//3)*102
        if t>=56.8+i*.36:
            c.dot(x,y,32,SKY if i!=4 else GOLD);text(c,i+1,x,y,33,PAPER)
    if t>64:text(c,'Line total?     Centre value?',886,530,31)
    if 68<t<72:
        for i,r in enumerate(ROWS):stroke(c,r,220,219,106,cue(t,68+i*.6,.7),JADE)
    if t>=72:
        for i,r in enumerate(CROSS):stroke(c,r,220,219,106,cue(t,72+i*.6,.7),COLOURS[i])

def centre(c,t):
    title(c,'Count how often each cell is used')
    if t<84.9:
        tiles(c,226,213,113,(4,3,8,9,5,1,2,7,6))
        for j,line in enumerate(ROWS):stroke(c,line,226,213,113,cue(t,77.2+j*.47,.7),JADE)
        text(c,'1 + 2 + … + 9 = 45',901,234,35)
        if t>=80:equation(c,'3 equal rows  →  45 ÷ 3 = 15',896,361)
        return
    counters=[0]*9
    for j,line in enumerate(CROSS):
        if t>=85+j*1.35:
            for i in line:counters[i]+=1
    tiles(c,226,213,113,[v if v else None for v in counters],(4,))
    for j,line in enumerate(CROSS):stroke(c,line,226,213,113,cue(t,85+j*1.35,.75),COLOURS[j])
    text(c,'Number of visits to each cell',340,538,25,MUTED)
    text(c,'4 lines × 15 = 60',899,215,37)
    if t>=90:
        text(c,'One whole grid uses 45.',899,308,30)
        for j in range(3):
            x=790+j*108
            c.rect(x-39,357,78,62,TILE,GOLD,2)
            text(c,'C' if t<97 else 5,x,387,37,GOLD)
    if t>=94:equation(c,'3 extra centres = 60 − 45',899,472,GOLD)
    if t>=97:equation(c,'Centre = 15 ÷ 3 = 5',899,552,JADE)

def hard(c,t):
    title(c,'Can two corner clues force the entire square?')
    vals=[None]*9
    if t>=103:vals[0]=8
    if t>=104.7:vals[2]=6
    tiles(c,222,211,117,vals)
    text(c,'Use 1–9 once each.',902,255,34)
    if t>=108:text(c,'Every line has the same sum.',904,350,29,JADE)
    if t>=112:text(c,'Where would you start?',904,459,33,GOLD)

def solve(c,t):
    title(c,'Each new entry is forced by a line')
    vals=[None]*9;vals[0]=8;vals[2]=6
    steps=((118,4),(123.4,6),(125.3,8),(128.3,1),(130.5,7),(133.2,3),(135.4,5))
    for when,i in steps:
        if t>=when:vals[i]=SQUARE[i]
    tiles(c,225,208,120,vals)
    if t<122:
        text(c,'15 − centre = opposite pair',903,254,31)
        if t>=118:equation(c,'15 − 5 = 10',903,358,GOLD)
    else:
        clues=((122,DIAGS[1],'6 + 5 + □ = 15','6 and 4 make 10.'),
               (124.3,DIAGS[0],'8 + 5 + □ = 15','8 and 2 make 10.'),
               (127,ROWS[0],'8 + □ + 6 = 15','Top middle is 1.'),
               (129.4,ROWS[2],'4 + □ + 2 = 15','Bottom middle is 9.'),
               (132,COLS[0],'8 + □ + 4 = 15','Left middle is 3.'),
               (134.4,COLS[2],'6 + □ + 2 = 15','Right middle is 7.'))
        j=max(k for k,row in enumerate(clues) if t>=row[0])
        at,line,eq,answer=clues[j]
        stroke(c,line,225,208,120,cue(t,at,.65),COLOURS[j%4])
        equation(c,eq,897,259,COLOURS[j%4])
        if t>=steps[j+1][0]:text(c,answer,897,384,34)
    text(c,'Target 15',343,549,29,JADE)
def check(c,t):
    title(c,'Check the completed square')
    tiles(c,224,213,115,SQUARE)
    ordered=(ROWS[1],COLS[1],DIAGS[0],DIAGS[1])
    j=0 if t<140.7 else 1 if t<144.2 else 2 if t<146.2 else 3
    line=ordered[j];at=(138.42,140.7,144.2,146.2)[j]
    stroke(c,line,224,213,115,cue(t,at,.7),COLOURS[j])
    equation(c,' + '.join(str(SQUARE[i]) for i in line)+' = 15',907,247,COLOURS[j])
    if t>=148:text(c,'1  2  3  4  5  6  7  8  9',905,367,32)
    if t>=150:text(c,'Every step had one possible value.',901,476,27,JADE)
def trap(c,t):
    title(c,'Rows and columns can pass while diagonals fail')
    swapped=SQUARE[3:6]+SQUARE[:3]+SQUARE[6:]
    if 161.8<t<163.0:
        shift=cue(t,161.8,1.2)
        tiles(c,224,213,115,(None,)*9)
        for i,n in enumerate(SQUARE):
            x,y=cell(i,224,213,115)
            direction=1 if i<3 else -1 if i<6 else 0
            x+=direction*27*4*shift*(1-shift)
            text(c,n,x,y+direction*115*shift,52,GOLD if direction else TEXT)
    else:
        tiles(c,224,213,115,SQUARE if t<162 else swapped)
    if t<162:
        for j,line in enumerate(ROWS):stroke(c,line,224,213,115,cue(t,156+j*.6,.7),JADE)
        text(c,'One row = 15',900,243,39,JADE)
        if t>=158:text(c,'All three rows = 45',900,350,32)
    else:
        text(c,'Two rows have traded places.',904,203,29)
        text(c,'Rows and columns still total 15.',904,285,27,MUTED)
        if t>=164:
            stroke(c,DIAGS[0],224,213,115,cue(t,164,.75),ROSE)
            equation(c,'3 + 1 + 2 = 6',900,392,ROSE)
        if t>=166.9:
            stroke(c,DIAGS[1],224,213,115,cue(t,166.9,.75),GOLD)
            equation(c,'7 + 1 + 4 = 12',900,478,GOLD)
def recap(c,t):
    title(c,'A method for the next missing-number grid')
    vals=list(SQUARE)
    if t<174:vals[1]=None
    tiles(c,224,213,115,vals)
    if t<176:stroke(c,ROWS[0],224,213,115,cue(t,170.6,1),JADE)
    elif t<180.2:
        for j,line in enumerate(CROSS):stroke(c,line,224,213,115,cue(t,176+j*.55,.7),COLOURS[j])
    else:
        for j,line in enumerate(LINES):stroke(c,line,224,213,115,cue(t,180.2+j*.52,.6),COLOURS[j%4])
    for j,(at,s) in enumerate(((170.5,'Find the common sum.'),(173,'Fill lines with one blank.'),(176,'Combine intersecting lines.'),(180.2,'Check all eight lines and digits.'))):
        if t>=at:text(c,s,674,192+j*92,26,COLOURS[j],'lm')
    if t>=185.2:text(c,'Forced at every step → unique.',897,543,28)
SCENES=(opening,exam,simple,simple,full_set,centre,hard,solve,check,trap,recap)
def verify():
    assert sum(range(1,10))==45 and len(set(SQUARE))==9
    assert all(sum(SQUARE[i] for i in line)==15 for line in LINES)
    assert [sum(i in line for line in CROSS) for i in range(9)]==[1,1,1,1,4,1,1,1,1]
    assert 4*15-45==3*5 and 15-4-5==6
    valid=[]
    for seq in permutations((1,2,3,4,5,7,9)):
        g=(8,seq[0],6,*seq[1:])
        if all(sum(g[i] for i in line)==15 for line in LINES):valid.append(g)
    assert valid==[SQUARE]
    bad=SQUARE[3:6]+SQUARE[:3]+SQUARE[6:]
    assert all(sum(bad[i] for i in line)==15 for line in ROWS+COLS)
    assert [sum(bad[i] for i in line) for line in DIAGS]==[6,12]
