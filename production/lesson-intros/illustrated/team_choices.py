"""S058. Assemble ice creams, fold an ordered-pair grid and enumerate four distinct teams of artists, builders and coders."""
from collections import Counter
from itertools import combinations, product
from math import comb, cos, pi, sin
from captioned_film import cue, font, mix

ID='S058'
ORIGINAL='3955e0d6242276ecaaafd06c186653174b05613b30d95e66821e1770a742d864'
START=(0.,16.76,35.16,47.46,61.22,74.47,87.27,105.8,129.79,145.31,161.31)
POSTER=139.8
PAPER='#fff3da'
DARK,INK,GRID='#373e53','#4b4859','#d5c5af'
BERRY,LEMON,MINT='#b85878','#eaae4b','#70ac93'
PALETTE=(BERRY,LEMON,MINT)
CONE,CREAM,BLUE='#cf975b','#fff8ec','#3b6784'
PEOPLE=tuple('ABCDE')
GROUPS=('artist','builder','coder')
PATTERNS=((2,2,0),(2,1,1),(3,1,0),(3,0,1))
AMOUNTS=(4,3,3)
PEERS=tuple((g,i) for g,n in enumerate(AMOUNTS) for i in range(n))
def label(c,s,x,y,z=29,col=DARK,anchor='lm'):c.text(s,x,y,z,col,anchor,True)
def title(c,s):
    z=41
    while font(round(z*c.scale),True).getlength(s)>1140*c.scale:z-=1
    label(c,s,65,55,z)
def star(c,x,y,r,colour):
    c.poly([(x+(r if i%2==0 else .43*r)*cos(-pi/2+i*pi/5),y+(r if i%2==0 else .43*r)*sin(-pi/2+i*pi/5)) for i in range(10)],colour,None)
def cone(c,x,y,s,f,top=None):
    # y marks the junction of the scoop and wafer.
    c.poly([(x-32*s,y),(x+32*s,y),(x,y+66*s)],CONE,DARK,2)
    for k in (-1,0,1):
        c.line([(x+(k*10-9)*s,y+7*s),(x+(k*5+4)*s,y+35*s)],'#936a4b',1)
    c.dot(x,y-10*s,32*s,PALETTE[f])
    for j in (-1,0,1):c.dot(x+j*18*s,y+5*s,12*s,PALETTE[f])
    if top==0:star(c,x,y-30*s,12*s,CREAM)
    if top==1:
        for dx,dy in ((-12,-20),(4,-31),(11,-13),(-1,-17)):c.dot(x+dx*s,y+dy*s,4*s,DARK)
def badge(c,x,y,kind,i,size=31):
    c.dot(x,y,size,DARK);c.dot(x,y,size-3,PALETTE[kind])
    label(c,'ABC'[kind]+str(i+1),x,y,max(13,round(size*.72)),DARK,'mm')
def helper(c,x,y,letter,s=28):
    c.dot(x,y,s,CREAM);c.line([(x-s*.65,y+s*.6),(x+s*.65,y+s*.6)],BLUE,3)
    label(c,letter,x,y-2,s,BLUE,'mm')
def row_equations(c,show=4,totals=False):
    for row,(a,b,d) in enumerate(PATTERNS[:show]):
        y=175+row*96
        for k,n in enumerate((a,b,d)):
            for p in range(n):badge(c,122+k*147+p*42,y,k,p,19)
        facts=[comb(n,k) for n,k in zip(AMOUNTS,(a,b,d))]
        n=facts[0]*facts[1]*facts[2]
        label(c,' × '.join(map(str,facts)),617,y,32)
        if totals:label(c,'= '+str(n),884,y,35,BLUE)
def opening(c,t):
    title(c,'What makes two outcomes different?')
    for i in range(3):cone(c,170+140*i,267,1,i)
    if t>=3.4:
        for k in range(2):cone(c,230+160*k,457,.78,0,k)
        label(c,'One flavour × one topping',86,558,27)
    if t>=9.4:
        a=cue(t,10.35,2.3)
        for x,l in [(mix(834,1020,a),'A'),(mix(1020,834,a),'B')]:helper(c,x,320,l,41)
        c.line([(791,390),(1061,390)],BLUE,3)
        label(c,'Same two helpers',769,448,31,BLUE)
def roles(c,t):
    title(c,'Choose the stages of the counting problem')
    cone(c,213,323,1.65,1,1);label(c,'A design',126,508,31)
    if t>=20.6:
        helper(c,541,298,'A',39);helper(c,653,298,'B',39)
        label(c,'A team',543,508,31)
    if t>=27.6:
        for k,x in enumerate((885,980,1075)):badge(c,x,302,k,0)
        label(c,'A group pattern',856,508,31)
def stall(c,t):
    title(c,'Three flavours, two toppings · one of each')
    for i,s in enumerate(('Berry','Mango','Mint')):
        cone(c,199+i*200,296,1.02,i);label(c,s,199+i*200,416,24,INK,'mm')
    star(c,929,261,34,LEMON)
    for x,y in ((1038,250),(1063,260),(1050,278),(1076,242)):c.dot(x,y,8,DARK)
    label(c,'Stars',922,352,25,INK,'mm');label(c,'Chips',1056,352,25,INK,'mm')
    if t>=41.2:label(c,'How many different orders?',365,536,36,BLUE)
def menu(c,t):
    title(c,'Build every order once')
    for i,s in enumerate(('Berry','Mango','Mint')):
        y=176+i*142;label(c,s,139,y,30)
        for k in range(2):
            when=47.6+1.7*i+.67*k;f=cue(t,when,.7)
            if f:cone(c,mix(343,510+213*k,f),y+.15*20,.68*f+.02,i,k)
    if t>=50.4:
        label(c,'Star',508,103,23,INK,'mm');label(c,'Chips',723,103,23,INK,'mm')
    if t>=54.2:label(c,'3 × 2',918,265,52,BLUE)
    if t>=56.2:label(c,'6 orders',916,371,38)
def pair_question(c,t):
    title(c,'Choose two helpers for the same job')
    p=cue(t,65.2,1.3)
    for i,l in enumerate(PEOPLE):
        x=199+i*218
        if i<2:helper(c,mix(x,(501,743)[i],p),mix(250,457,p),l,round(mix(46,35,p)))
        else:helper(c,x,250,l,46)
    if t>=65:
        c.line([(415,514),(833,514)],BLUE,3)
    if t>=69:label(c,'How many pairs?',842,463,30,BLUE)
def pair_grid(c,t):
    title(c,'Two ordered picks describe each pair')
    x0,y0,step=175,185,70
    for i,l in enumerate(PEOPLE):
        label(c,l,x0+i*step,y0-51,23,INK,'mm');label(c,l,x0-54,y0+i*step,23,INK,'mm')
    fold=cue(t,81.6,1.8)
    for i,j in product(range(5),repeat=2):
        x,y=x0+j*step,y0+i*step
        c.rect(x-29,y-26,58,52,'#eee4cd' if i==j else CREAM,GRID,1)
    for i,j in product(range(5),repeat=2):
        if i==j or t<75+.16*(i*5+j):continue
        x,y=x0+j*step,y0+i*step
        if i>j:
            x,y=mix(x,x0+i*step,fold),mix(y,y0+j*step,fold)
            if fold>=.999:continue
        label(c,PEOPLE[i]+PEOPLE[j],x,y,21,BLUE,'mm')
    if t>=77.2:label(c,'5 first × 4 second',681,231,39)
    if t>=81.6:label(c,'AB and BA → one pair',680,345,33,BLUE)
    if t>=83.6:label(c,'20 ÷ 2 = 10 teams',680,453,40)
def roster(c,t):
    title(c,'A team of four with a restriction on its members')
    for k,n in enumerate(AMOUNTS):
        x=155+365*k; label(c,['Artists','Builders','Coders'][k],x,168,33)
        for i in range(n):badge(c,x+(i%2)*86,262+(i//2)*84,k,i,30)
    if t>=91.4:label(c,'2 or 3 artists',113,462,31,BERRY)
    if t>=94.4:label(c,'0 or 1 coder',873,462,31,BLUE)
    if t>=100.4:label(c,'How many four-person teams?',357,560,32)
def patterns(c,t):
    title(c,'Sort teams by how many come from each group')
    for k,s in enumerate(('Artists','Builders','Coders')):label(c,s,95+k*147,109,19)
    label(c,'One example team per row',92,555,22,INK)
    for row,(a,b,d) in enumerate(PATTERNS):
        if t<(105.8,108.9,114.,116.2)[row]:continue
        y=175+row*96
        for k,n in enumerate((a,b,d)):
            for p in range(n):badge(c,122+k*147+p*42,y,k,p,19)
        if t>=120.8:
            choices=[comb(n,k) for n,k in zip(AMOUNTS,(a,b,d))]
            label(c,' × '.join(map(str,choices)),612,y,29)
    if 111.2<=t<114:label(c,'Choose 2 of 4 artists in 6 ways.',613,236,28,BLUE)
    if 117.6<=t<120.8:label(c,'Choose 3 of 4 artists in 4 ways.',613,420,28,BLUE)
    if t>=124.8:label(c,'Add the four separate rows.',573,556,31,BLUE)
def totals(c,t):
    title(c,'Every dot is a different legal four-person team')
    groups=((18,BERRY),(54,LEMON),(12,MINT),(12,BLUE))
    for j,(n,col) in enumerate(groups):
        x=143+281*j;y=213
        label(c,' + '.join(str(k)+g for k,g in zip(PATTERNS[j],'ABC') if k),x,y-69,21,INK)
        f=cue(t,129.8+.7*j,.82)
        for i in range(min(n,int(n*f+.5))):c.dot(x+(i%9)*19,y+(i//9)*21,6,col)
        if f>.85:label(c,str(n),x+66,405,38,INK,'mm')
    if t>=133.6:label(c,'18 + 54 + 12 + 12 = 96 teams',640,525,38,BLUE,'mm')
def pitfalls(c,t):
    title(c,'Does switching the two people change their job?')
    f=cue(t,146.1,2.1)
    helper(c,mix(270,550,f),269,'A',45);helper(c,mix(550,270,f),269,'B',45)
    c.line([(183,346),(633,346)],BLUE,3)
    label(c,'Two ordinary helpers',209,409,31)
    if t>=150.4:
        helper(c,838,260,'A',39);helper(c,1080,260,'B',39)
        label(c,'Captain',838,351,26,INK,'mm');label(c,'Deputy',1080,351,26,INK,'mm')
    if t>=156.2:label(c,'Separate team patterns are alternatives. Add their counts.',640,527,29,BLUE,'mm')
def recap(c,t):
    title(c,'From a group pattern to a team count')
    if t<164.2:
        for k,x in enumerate((333,540,747)):badge(c,x,320,k,0,43)
        label(c,'Are the jobs named?',465,477,34)
    else:
        row_equations(c,min(4,1+int((t-164.2)/1.0)),t>=168.4)
        if t>=171.2:label(c,'Four exclusive rows give 96 teams.',600,554,29,BLUE)
SCENES=(opening,roles,stall,menu,pair_question,pair_grid,roster,patterns,totals,pitfalls,recap)
def verify():
    assert len(list(product(range(3),range(2))))==6
    assert len(list(combinations(PEOPLE,2)))==10
    teams=Counter()
    for team in combinations(PEERS,4):
        counts=tuple(sum(g==k for g,_ in team) for k in range(3))
        if counts[0] in (2,3) and counts[2]<=1:teams[counts]+=1
    assert set(teams)==set(PATTERNS) and [teams[k] for k in PATTERNS]==[18,54,12,12]
    assert sum(teams.values())==96
    assert 2*len(tuple(combinations(PEOPLE,2)))==5*4
