"""S071. Slide named paintings along a numbered rail and disprove the rival hanging."""
from itertools import permutations
from math import sin, pi
from captioned_film import cue, mix
ID='S071'
ORIGINAL='5e4c1d79bf953e4379cbeecf4119588e302b2219dc4e62e606b3437f829d852c'
START=(0,16.92,34.52,49.85,62.33,77.19,92.39,115.07,140.02,157.3,172.98)
POSTER=137.8
PAPER='#f3eada'
INK, GREY, LINE, FRAME='#192e40','#536574','#a8ada7','#866e49'
TEAL, RED, GOLD='#087769','#a63d4a','#edbc65'
NAMES=('Ada','Ben','Chloe','Dylan','Eva')
PALETTE=('#ba5978','#568398','#599483','#9b6c98','#c88749')

def text(c,s,x,y,n=30,col=INK):
    c.text(s,x,y,n,col,bold=True)
def title(c,s):
    c.text(s,58,55,42,INK,'lm',True)
    c.line([(58,99),(1222,99)],LINE,2)
def tile(c,name,x,y,art=False,scale=1):
    i=NAMES.index(name); w=118*scale;h=81*scale
    if art:
        c.rect(x-w/2-5,y-h/2-5,w+10,h+10,FRAME)
        c.rect(x-w/2,y-h/2,w,h,'#faf0d3')
        left=x-w*.445;top=y-h*.42
        c.rect(left,top,w*.89,h*.84,PALETTE[i])
        # Each miniature painting has its own silhouette, even in greyscale.
        if i==0:
            c.dot(x+w*.19,y-h*.17,h*.13,GOLD)
            c.poly([(left,y+h*.37),(x-w*.15,y-h*.20),(x+w*.12,y+h*.37)],'#4c5962',None)
        elif i==1:
            c.poly([(x,y-h*.34),(x,y+h*.11),(x-w*.24,y+h*.11)],'#fff3cc',None)
            c.poly([(x-w*.31,y+h*.14),(x+w*.32,y+h*.14),(x+w*.18,y+h*.31),(x-w*.19,y+h*.31)],INK,None)
        elif i==2:
            for dx,r in ((-.18,.22),(.12,.28)):
                c.line([(x+dx*w,y),(x+dx*w,y+h*.32)],INK,3)
                c.dot(x+dx*w,y-h*.08,r*h,'#accaa5')
        elif i==3:
            for dx,hh in ((-.28,.32),(-.02,.60),(.20,.43)):
                c.rect(x+dx*w,y+h*(.33-hh),w*.17,h*hh,'#463d5c')
        else:
            c.dot(x,y,h*.30,'#ffe3a1');c.dot(x+w*.045,y-h*.12,h*.23,PALETTE[i])
        text(c,name,x,y+h*.81,round(22*scale))
    else:
        c.dot(x,y-13*scale,31*scale,PALETTE[i])
        c.dot(x,y-18*scale,13*scale,'#ffe2bc')
        c.poly([(x-w*.19,y+19*scale),(x-w*.11,y+4*scale),(x+w*.11,y+4*scale),(x+w*.19,y+19*scale)],PALETTE[i],None)
        text(c,name,x,y+43*scale,round(25*scale))

def rail(c,n,y):
    xs=[640+(i-(n-1)/2)*176 for i in range(n)]
    c.line([(xs[0]-66,y+82),(xs[-1]+66,y+82)],LINE,3)
    for i,x in enumerate(xs):
        c.line([(x,y+82),(x,y+92)],GREY,3)
        text(c,str(i+1),x,y+108,23,GREY)
    return xs

def place(c,t,name,source,dest,at,art=False):
    p=cue(t,at,1.2); x=mix(source[0],dest[0],p);y=mix(source[1],dest[1],p)-25*sin(pi*p)
    tile(c,name,x,y,art)

def line_up(c,t,order,moves):
    xs=rail(c,len(order),344)
    for j,name in enumerate(sorted(order)):
        at=moves.get(name)
        if at is None:tile(c,name,xs[j],169)
        else:place(c,t,name,(xs[j],169),(xs[order.index(name)],344),at)

def link(c,x1,x2,y,s,col=TEAL):
    c.line([(x1,y+14),(x1,y),(x2,y),(x2,y+14)],col,3)
    text(c,s,(x1+x2)/2,y-23,23,col)

def opening(c,t):
    title(c,'A clue changes the places that still work')
    xs=rail(c,4,335)
    for i,x in enumerate(xs):
        if t<4+i or i not in (0,3):c.dot(x,335,13,LINE)
        else:text(c,'×',x,335,46,RED)
    if t>6:tile(c,'Ada',mix(460,552,cue(t,7,1.2)),160)
    if t>10:
        link(c,xs[1],xs[2],263,'Neighbouring places')
        tile(c,'Ben',xs[2],335)
    if t>13:text(c,'Keep names and places visible together.',640,535,31)
def context(c,t):
    title(c,'What must be true?')
    xs=rail(c,4,295)
    tile(c,'Dylan',xs[0],295,True)
    if t>20:link(c,xs[1],xs[2],175,'A fixed block')
    if t>22:
        tile(c,'Ada',xs[1],295,True);tile(c,'Ben',xs[2],295,True)
    if t>25:text(c,'Which alternatives could still fit?',640,479,33,TEAL)
    if t>30:text(c,'Try each remaining position and test the clues.',640,547,27,GREY)
def easy_q(c,t):
    title(c,'Three people in a line')
    line_up(c,t,('Ben','Ada','Chloe'),{})
    if t>37:text(c,'Ada cannot stand at either end.',640,490,31)
    if t>40:text(c,'Ben stands before Ada.',640,551,29,TEAL)
def easy_a(c,t):
    title(c,'Start with the clue that fixes a place')
    line_up(c,t,('Ben','Ada','Chloe'),{'Ada':50,'Ben':53.7,'Chloe':57.4})
    text(c,'Ada takes the middle.' if t<54 else 'Only one place is earlier than Ada.' if t<58 else 'Ben  →  Ada  →  Chloe',640,526,33,TEAL)
def medium_q(c,t):
    title(c,'Can four names fit these three clues?')
    line_up(c,t,('Chloe','Ada','Ben','Dylan'),{})
    if t>64:text(c,'Ada immediately before Ben',352,493,28,TEAL)
    if t>67:text(c,'Dylan at an end',937,493,28)
    if t>69:text(c,'Chloe first',640,557,30)
def medium_a(c,t):
    title(c,'Fix the ends before placing the neighbours')
    line_up(c,t,('Chloe','Ada','Ben','Dylan'),{'Chloe':77.4,'Dylan':80,'Ada':84,'Ben':84})
    if t>84:link(c,552,728,264,'Immediately after')
    if t>87:text(c,'Four places, all forced.',640,537,34,TEAL)
def hard_q(c,t):
    title(c,'Hang five named paintings')
    xs=rail(c,5,320)
    for i,n in enumerate(NAMES):tile(c,n,xs[i],181,True,.85)
    if t>97:text(c,'Ben immediately before Chloe',361,474,26)
    if t>100:text(c,'Ada two places before Chloe',922,474,26)
    if t>104:text(c,'Dylan at an end, earlier than Ada',360,548,25,TEAL)
    if t>109:text(c,'Eva cannot be second',922,548,26,RED)
def block(c,t):
    title(c,'Slide the three-painting block')
    xs=rail(c,5,325)
    p=cue(t,126,1.8)-cue(t,132.6,1.8)
    for i,name in enumerate(NAMES[:3]):
        tile(c,name,xs[i+1]+p*176,325,True)
    link(c,xs[1]+p*176,xs[3]+p*176,215,'Ada … two places … Chloe')
    if t>119:place(c,t,'Dylan',(xs[0],178),(xs[0],325),120,True)
    if t>127.8:tile(c,'Eva',mix(xs[1],xs[4],cue(t,132.6,1.8)),325-112*sin(pi*cue(t,132.6,1.8)),True)
    if 127.8<t<132.8:text(c,'Rejected: Eva would be second.',640,534,33,RED)
    elif t>=134:text(c,'The block starts in place 2.',640,534,34,TEAL)
    elif t>121:text(c,'Dylan is at the earlier end. Try starts 2 and 3.',640,534,30)
def hard_a(c,t):
    title(c,'Check both the survivor and its rival')
    xs=rail(c,5,307)
    for x,n in zip(xs,('Dylan','Ada','Ben','Chloe','Eva')):tile(c,n,x,307,True)
    if t<148:link(c,xs[1],xs[3],201,'Two places')
    if t>145:text(c,'Dylan before Ada   •   Eva in place 5',640,477,30,TEAL)
    if t>150:text(c,'Start at 3 → Eva in place 2 → ruled out.',640,547,30,RED)
def pitfall(c,t):
    title(c,'“Earlier” and “immediately before”')
    xs=rail(c,4,319);p=cue(t,163.5,2.2)
    tile(c,'Ada',xs[0],319,True);tile(c,'Ben',mix(xs[1],xs[3],p),319,True)
    if t<163.6:link(c,xs[0],xs[1],215,'Touching places')
    if t>=165.6:link(c,xs[0],xs[3],215,'Earlier, with a gap')
    if t>167:text(c,'Read every clue again after the names fit.',640,522,33,TEAL)
def recap(c,t):
    title(c,'Use the same method on a new arrangement')
    xs=rail(c,5,321)
    if t>173:tile(c,'Dylan',xs[0],321,True)
    if t>177:
        for i,n in enumerate(NAMES[:3]):tile(c,n,xs[i+1],321,True)
        link(c,xs[1],xs[3],210,'Forced block')
    if t>186:tile(c,'Eva',xs[-1],321,True)
    text(c,'Mark fixed places.' if t<177 else 'Use distances to build a block.' if t<182 else 'Compare the possible starts.' if t<187 else 'Check all clues. Only one order survives.',640,533,32,TEAL)
SCENES=(opening,context,easy_q,easy_a,medium_q,medium_a,hard_q,block,hard_a,pitfall,recap)
def verify():
    easy=[p for p in permutations(NAMES[:3]) if p[1]=='Ada' and p.index('Ben')<p.index('Ada')]
    med=[p for p in permutations(NAMES[:4]) if p.index('Ben')==p.index('Ada')+1 and p.index('Dylan') in (0,3) and p[0]=='Chloe']
    cases=[p for p in permutations(NAMES) if p.index('Chloe')==p.index('Ben')+1==p.index('Ada')+2 and p.index('Dylan') in (0,4) and p.index('Dylan')<p.index('Ada')]
    assert easy==[('Ben','Ada','Chloe')] and med==[('Chloe','Ada','Ben','Dylan')]
    assert len(cases)==2 and [p for p in cases if p[1]!='Eva']==[('Dylan','Ada','Ben','Chloe','Eva')]
