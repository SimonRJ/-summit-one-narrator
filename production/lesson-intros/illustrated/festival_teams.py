"""S069. Build a sundae menu, fold ordered pairs, then count a festival crew."""
from itertools import combinations, permutations, product
from math import comb, prod, sin, pi
from captioned_film import cue, mix

ID = 'S069'
ORIGINAL = '4f6c55622bd900860b4385567f975375f2c605ba4ff5c9719f00eae993f9ba7c'
START = (0,17.24,35.32,47.62,61.86,75.11,87.91,106.92,131.07,147.71,163.87)
POSTER = 144
PAPER = '#162339'
WHITE, QUIET, LINE, PANEL = '#fff5df','#c2d3dc','#456174','#21344a'
PEACH, GOLD, MINT, BLUE = '#ffab94','#ffd275','#92debd','#a9caff'
FLAVOURS = ('Berry','Lemon','Mint','Blueberry')
COLOURS = (PEACH,GOLD,MINT,BLUE)
GROUPS = (5,4,4)
PATTERNS = ((2,2,0),(2,1,1),(3,1,0),(3,0,1))
MEMBERS = tuple((g,i) for g,n in enumerate(GROUPS) for i in range(n))
TEAMS = [[team for team in combinations(MEMBERS,4)
          if tuple(sum(g == k for g,i in team) for k in range(3)) == pattern]
         for pattern in PATTERNS]

def label(c,s,x,y,size=30,col=WHITE,anchor='mm'):
    c.text(s,x,y,size,col,anchor,True)

def header(c,s):
    label(c,s,52,56,42,WHITE,'lm')
    c.line([(52,98),(1228,98)],LINE,2)

def cup(c,x,y,f,topping,size=1):
    r=25*size
    c.dot(x,y-r*.35,r,COLOURS[f])
    c.poly([(x-r*1.25,y),(x+r*1.25,y),(x+r*.83,y+r*1.15),(x-r*.83,y+r*1.15)],WHITE,None)
    c.line([(x-r*.78,y+r*.48),(x+r*.78,y+r*.48)],LINE,3)
    if topping==0: # cherry
        c.dot(x,y-r*1.27,r*.32,'#e35b72')
        c.line([(x,y-r*1.48),(x+r*.30,y-r*1.8)],MINT,3)
    elif topping==1: # chocolate chips
        for dx,dy in ((-.55,-.76),(.15,-1.13),(.53,-.68)):
            c.poly([(x+(dx-.16)*r,y+dy*r),(x+dx*r,y+(dy-.31)*r),(x+(dx+.16)*r,y+dy*r)],'#513530',None)
    elif topping==2: # sprinkles
        for j,(dx,dy) in enumerate(((-.64,-.66),(-.39,-1.01),(.08,-.8),(.31,-1.06),(.6,-.71))):
            c.line([(x+dx*r,y+dy*r),(x+(dx+.15)*r,y+(dy-.17)*r)],(WHITE,'#ba3b67',PAPER)[j%3],3)

def badge(c,x,y,who,r=32):
    g,i=who
    c.dot(x,y,r,COLOURS[g])
    label(c,'ABC'[g]+str(i+1),x,y,r*.82,PAPER)

def pair_swap(c,t,x,y,roles=False):
    u=cue(t,1.5,2.6)
    for a,col,l in ((0,MINT,'Jo'),(1,GOLD,'Kit')):
        px=mix(x+a*150,x+(1-a)*150,u)
        py=y+(1 if a else -1)*47*sin(pi*u)
        c.dot(px,py,35,col)
        label(c,l,px,py,24,PAPER)
    for j,s in enumerate(('Lead','Deputy') if roles else ('Helper','Helper')):
        label(c,s,x+150*j,y+67,24,QUIET)

def opening(c,t):
    header(c,'What makes two choices different?')
    for f in range(4):
        if t>=.5+f*.5: cup(c,133+109*f,254,f,None,1.12)
    if t>4:
        for k in range(3):cup(c,185+k*143,423,0,k)
        label(c,'One flavour × one topping',330,535,28)
    if t>8:
        pair_swap(c,t-8,797,322)
        label(c,'One pair, chosen either way',883,535,27,MINT)

def context(c,t):
    header(c,'Designs, teams and restrictions')
    cup(c,210,295,3,0,2)
    label(c,'Different recipe?',210,453)
    if t>20:
        pair_swap(c,t-20,516,303)
        label(c,'Different people?',590,453)
    if t>26:
        for i,w in enumerate(((0,0),(0,1),(1,0),(2,0))): badge(c,944+67*(i%2),258+74*(i//2),w)
        label(c,'Allowed team?',979,453,30,GOLD)
    if t>31:label(c,'Pick the stages. Then test the restrictions.',640,553,31,QUIET)

def menu_question(c,t):
    header(c,'At the sundae stall')
    for f,s in enumerate(FLAVOURS):
        cup(c,145+143*f,268,f,None,1.2)
        label(c,s,145+143*f,343,22)
    for k,s in enumerate(('Cherry','Chips','Sprinkles')):
        if t>37+k*.5:
            cup(c,795+151*k,268,0,k,1.2)
            label(c,s,795+151*k,343,22)
    label(c,'Four flavours',345,428,32,MINT)
    if t>38:label(c,'Three toppings',952,428,32,GOLD)
    if t>42:label(c,'Choose one of each. How many different orders?',640,543,34)

def menu_solution(c,t):
    header(c,'A place on the menu for every order')
    for j,s in enumerate(('Cherry','Chips','Sprinkles')):label(c,s,325+j*155,151,23,QUIET)
    for f,s in enumerate(FLAVOURS):
        y=222+100*f
        label(c,s,68,y,24,COLOURS[f],'lm')
        for k in range(3):
            u=cue(t,47.7+f*1.37+k*.34,.65)
            if u:cup(c,mix(223,325+155*k,u),y,f,k,.72+.12*u)
    if t>=52:label(c,'4 rows × 3 orders',981,286,33)
    if t>=55:label(c,'12',981,378,88,GOLD)
    if t>=57:label(c,'different sundaes',981,467,30)

def pair_question(c,t):
    header(c,'Two helpers, one shared job')
    for j,ch in enumerate('ABCDEF'):
        x=202+175*j
        p=cue(t,64.1,2.5) if j in (0,2) else 0
        px=mix(x,520+125*(j//2),p)
        py=mix(252,420,p)
        c.dot(px,py,41,BLUE)
        label(c,ch,px,py,40,PAPER)
    if t>=65:label(c,'Same job',584,504,28,MINT)
    if t>=69:label(c,'How many pairs?',974,417,35)

def fold(c,t):
    header(c,'Fold the reversed orders together')
    step=61
    fold_by=cue(t,81.5,2.5)
    for i in range(6):
        for j in range(6):
            x,y=153+j*step,199+i*step
            c.rect(x-28,y-27,56,54,PANEL if i!=j else PAPER,LINE,1)
            if i==j:label(c,'×',x,y,26,LINE)
    for i,j in permutations(range(6),2):
        if t<75.2+.055*(6*i+j):continue
        x,y=153+j*step,199+i*step
        if i>j:
            if fold_by==1:continue
            x,y=mix(x,153+i*step,fold_by),mix(y,199+j*step,fold_by)
        label(c,'ABCDEF'[i]+'ABCDEF'[j],x,y,21,GOLD if i>j else MINT)
    for i,ch in enumerate('ABCDEF'):
        label(c,ch,153+i*step,145,20,QUIET)
        label(c,ch,100,199+i*step,20,QUIET)
    if t>76:label(c,'6 first picks × 5 second picks',887,216,30)
    if t>80:label(c,'AC and CA select the same pair.',887,326,30,MINT)
    if t>84:label(c,'30 ÷ 2 = 15 pairs',887,447,43,GOLD)

def roster(c,t):
    header(c,'Choose a four-person festival team')
    for g,(n,name) in enumerate(zip(GROUPS,('Artists','Builders','Coders'))):
        x=117+397*g
        label(c,name,x,177,34,COLOURS[g],'lm')
        for j in range(n):badge(c,x+32+(j%3)*78,270+82*(j//3),(g,j))
    if t>91:label(c,'2 or 3 artists',280,467,33,PEACH)
    if t>94:label(c,'At most 1 coder',926,467,33,MINT)
    if t>101:label(c,'No named jobs. Count each team once.',640,553,31)

def pattern_row(c,row,y,t,reveal,show_factors):
    group=TEAMS[row]
    # Change one actual example team while its roster pattern stays fixed.
    team=group[(int(max(0,t-reveal)/1.7)*7)%len(group)]
    for k,(g,i) in enumerate(team):badge(c,130+73*k,y,(g,i),25)
    factors=[comb(n,k) for n,k in zip(GROUPS,PATTERNS[row]) if k]
    if show_factors:label(c,' × '.join(map(str,factors)),551,y,31,WHITE,'lm')

def patterns(c,t):
    header(c,'Which group patterns can fill four places?')
    label(c,'Example team',228,142,22,QUIET)
    for i,at in enumerate((107,111,116,118)):
        if t>=at:pattern_row(c,i,205+i*86,t,at,t>=121)
    if t>=113:label(c,'5 artists',980,185,30,PEACH)
    if t>=114:label(c,'10 possible pairs',980,244,27)
    if t>=119:label(c,'10 possible trios',980,316,27)
    if t>=126:label(c,'Add across the four rows.',640,565,33,MINT)

def totals(c,t):
    header(c,'Every dot represents a different four-person team')
    for i,teams in enumerate(TEAMS):
        x=70+i*307
        label(c,' + '.join(str(v)+g for v,g in zip(PATTERNS[i],'ABC') if v),x+112,153,25)
        u=cue(t,131.1+i*.8,1.1)
        for j,team in enumerate(teams[:round(len(teams)*u)]):c.dot(x+j%16*14,203+j//16*16,5.4,COLOURS[i])
        if u==1:label(c,str(len(teams)),x+110,405,45,COLOURS[i])
    if t>136:label(c,'60 + 160 + 40 + 40 = 300 teams',640,508,43,GOLD)
    if t>140:label(c,'Zero coders is allowed. Both artist totals appear.',640,570,26,QUIET)

def pitfalls(c,t):
    header(c,'Swap the people. Does the outcome change?')
    pair_swap(c,t-148,214,287)
    label(c,'Same team',287,452,34,MINT)
    if t>151:
        pair_swap(c,t-151,845,287,True)
        label(c,'Different jobs',917,452,34,GOLD)
    if t>157:label(c,'Multiply choices within a team. Add separate patterns.',640,552,32)

def recap(c,t):
    header(c,'Count a new team without counting anyone twice')
    if t<168:pair_swap(c,t-164,563,290,True);label(c,'Do the places have names?',640,477,38);return
    for i in range(4):
        if t>=168+i*.65:
            y=167+i*88
            pattern_row(c,i,y,170,168, t>=171)
            if t>=175:label(c,'= '+str(len(TEAMS[i])),850,y,33,COLOURS[i])
    if t>=177:label(c,'Exactly one row per team  →  300 altogether',640,552,35,GOLD)

SCENES=(opening,context,menu_question,menu_solution,pair_question,fold,roster,patterns,totals,pitfalls,recap)
def verify():
    assert len(set(product(FLAVOURS,range(3))))==12
    assert len(set(tuple(sorted(p)) for p in permutations('ABCDEF',2)))==15
    assert [len(group) for group in TEAMS]==[60,160,40,40]
    legal={s for s in combinations(MEMBERS,4) if 2<=sum(g==0 for g,i in s)<=3 and sum(g==2 for g,i in s)<=1}
    assert len(legal)==300 and legal==set().union(*map(set,TEAMS))
    assert all(prod(comb(n,k) for n,k in zip(GROUPS,p))==len(group) for p,group in zip(PATTERNS,TEAMS))
