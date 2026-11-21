"""S085. Equal-scale plots, conserved fence strips and a complete integer-area graph."""
from captioned_film import cue
ID='S085'
ORIGINAL='4bffd130ec4c25798e49381cde554c9832d1add3bb690abcf3f6520dabd647fb'
START=(0,17.24,34.04,47.46,60.42,73.84,90.64,106.61,130.43,145.31,160.35)
POSTER=138.7
PAPER='#152934'; INK='#f9efe0'; BLUE='#a4d8f7'; GOLD='#ffd078'; MINT='#9de7ba'; GRID='#577681'; GRASS='#274c4b'; RED='#ffae9f'
def label(c,s,x,y,size=33,col=INK):
    c.text(s,x,y,size,col,bold=True)
def header(c,s):
    c.text(s,48,54,41,INK,'lm',True)
    c.line([(48,100),(1230,100)],GRID,2)
def area(x):
    return x*(45-2*x)
def plot(c,l,w,u,wall=False,grid=True,dimensions=True):
    x,y=110,170
    c.rect(x,y,l*u,w*u,GRASS,None)
    if grid:
        for i in range(1,int(l)+1):
            c.line([(x+i*u,y),(x+i*u,y+w*u)],GRID,1)
        for i in range(1,int(w)+1):
            c.line([(x,y+i*u),(x+l*u,y+i*u)],GRID,1)
    c.line([(x,y),(x,y+w*u),(x+l*u,y+w*u),(x+l*u,y)],GOLD,5)
    c.line([(x,y),(x+l*u,y)],BLUE if wall else GOLD,8 if wall else 5)
    if wall:
        for i in range(int(l)):
            c.line([(x+i*u,y-2),(x+i*u+6,y-12)],BLUE,2)
        label(c,'wall',x+l*u/2,y-30,24,BLUE)
    if dimensions:
        label(c,f'{l:g} m',x+l*u/2,y+w*u+37,27,GOLD)
        label(c,f'{w:g} m',x-50,y+w*u/2,23,GOLD)
def pair(c,w):
    plot(c,13-w,w,45)
def explain(c,lines):
    for i,(s,col) in enumerate(lines):
        label(c,s,940,210+85*i,31,col)
def intro(c,t):
    header(c,'Which rectangle gives the most area?')
    p = cue(t,6,.8) + cue(t,11,.8)
    w=3+round(p)
    plot(c,10-p,3+p,45,grid=False,dimensions=False)
    explain(c,[('Fence length stays fixed',GOLD)]+([(f'{w} × {13-w} = {w*(13-w)} m²',MINT)] if p in (0,1,2) else []))
def exams(c,t):
    header(c,'Find the rule before choosing the sides')
    if t<26:
        pair(c,4);explain(c,[('All four sides use fence',GOLD),('Same perimeter',INK)])
    else:
        plot(c,23,11,21,True);explain(c,[('One side follows a wall',BLUE),('Only three sides use fence',GOLD)])
def easy(c,t):
    header(c,'26 metres of perimeter. How much area?')
    plot(c,9,4,55,dimensions=False);label(c,'4 m',61,282,26,GOLD)
    if t>38:label(c,'? m',357,429,29,GOLD)
    explain(c,[('Perimeter = 26 m',GOLD),('Width = 4 m',BLUE)])
def easy_answer(c,t):
    header(c,'One length and one width use half the perimeter')
    plot(c,9,4,55,dimensions=t>51)
    lines=[('26 ÷ 2 = 13 m',GOLD)]
    if t>50:lines.append(('13 − 4 = 9 m',BLUE))
    if t>55:lines.append(('9 × 4 = 36 m²',MINT))
    explain(c,lines)
def medium(c,t):
    header(c,'Keep the perimeter at 26 metres')
    w=min(4,1+int(max(0,t-60.42)/3))
    pair(c,w)
    explain(c,[('Whole metres only',INK),(f'{w} + {13-w} = 13',GOLD),(f'Area = {w*(13-w)} m²',MINT)])
def balance(c,t):
    header(c,'Shorten the long side and extend the short side')
    # Use one grid throughout the exchange. The red column is removed,
    # and a mint row is added below the shared rectangle.
    x,u=110,50
    w=4 if t<79 else 5
    l=13-w
    if t<84:
        plot(c,l,w,u,dimensions=False)
        if t>75:
            c.rect(x+(l-1)*u,170,u,w*u,RED,None)
            for j in range(1,w):c.line([(x+(l-1)*u,170+j*u),(x+l*u,170+j*u)],GRID,2)
            c.rect(x,170+w*u,(l-1)*u,u,MINT,None)
            for i in range(1,l-1):c.line([(x+i*u,170+w*u),(x+i*u,170+(w+1)*u)],GRID,2)
            explain(c,[(f'Remove {w} squares',RED),(f'Add {l-1} squares',MINT),(f'Gain {l-1-w} m²',INK)])
    else:
        pair(c,6);explain(c,[('Closest integer sides',GOLD),('6 m and 7 m',BLUE),('Greatest area = 42 m²',MINT)])
def hard(c,t):
    header(c,'Build a rectangular pen beside a wall')
    plot(c,23,11,22,True,grid=False,dimensions=False)
    lines=[('45 m of fencing',GOLD)]
    if t>94:lines.append(('Two widths + one length',INK))
    if t>100:lines.append(('Which whole metres?',BLUE))
    explain(c,lines)
def factors(c,t):
    header(c,'Pair the two widths before comparing products')
    plot(c,23,11,21,True,grid=False,dimensions=False)
    label(c,'x',59,276,29,GOLD);label(c,'45 − 2x',350,441,29,GOLD)
    explain(c,[('2x + L = 45',GOLD),('2 × area = (2x) × L',MINT)] if t>111 else [('2x + L = 45',GOLD)])
    if t>117:
        x,y,u=110,507,21
        c.rect(x,y,22*u,37,GOLD);c.rect(x+22*u,y,23*u,37,BLUE)
        label(c,'2x must be even',x+11*u,y+18,23,PAPER);label(c,'L',x+33*u,y+18,23,PAPER)
        label(c,'45 metres in all',x+22.5*u,y+69,26,INK)
def winner(c,t):
    header(c,'The closest permitted split is 22 and 23')
    plot(c,23,11,22,True,grid=True)
    lines=[('Width = 22 ÷ 2 = 11 m',GOLD),('11 × 23 = 253 m²',MINT)]
    if t>136:lines.append(('Next split: 24 and 21',BLUE))
    if t>139:lines.append(('12 × 21 = 252 m²',INK))
    explain(c,lines)
def mistakes(c,t):
    header(c,'Trace only the sides that use fencing')
    plot(c,23,11,22,True)
    explain(c,[('11 + 23 + 11 = 45 m',GOLD)]+([('A width of 11.25 m',RED),('breaks the integer rule.',INK)] if t>151 else []))
def recap(c,t):
    header(c,'Check every legal width against the same rule')
    label(c,'Area (m²)',112,151,24,MINT)
    x,y,dx=100,506,44
    for level in (0,100,200):
        py=y-level*1.15
        c.line([(x-4,py),(x+21*dx+24,py)],GRID,1)
        label(c,level,x-40,py,20,INK)
    c.line([(x,y),(x+22*dx,y)],GRID,3)
    for w in range(1,23):
        if t<160.35+w*.24:continue
        px=x+(w-1)*dx;h=area(w)*1.15
        c.rect(px,y-h,24,h,MINT if w==11 else GRID)
        if w in (1,6,11,16,22):label(c,w,px+12,y+23,19,INK)
    label(c,'Width (m)',x+11*dx,y+65,26,INK)
    if t>168:label(c,'253 m²',x+10*dx+12,y-area(11)*1.15-30,29,MINT)
    if t>173:label(c,'Only width 11 reaches the maximum.',893,151,29,GOLD)
SCENES=(intro,exams,easy,easy_answer,medium,balance,hard,factors,winner,mistakes,recap)
def verify():
    assert max((x*(13-x),x) for x in range(1,7))==(42,6)
    assert [x for x in range(1,23) if area(x)==max(map(area,range(1,23)))]==[11]
    assert area(11)==253 and area(12)==252 and 4*9==36
