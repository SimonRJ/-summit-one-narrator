"""S026. Conserve individual beads, balance two unequal groups, and peel apart overlapping readings."""
from fractions import Fraction
from math import sin, pi
from captioned_film import cue, mix

ID='S026'
ORIGINAL='33d1245e0b74f7821abbdb307120c94d343c6e135eed37916cd43cc9114fe4a4'
START=(0,14.04,31,44.9,55.79,70.8,92.39,109.32,130.27,146.75,160.51)
POSTER=126.6
PAPER='#122b32'; INK='#fff5e2'; MINT='#84ddc4'; GOLD='#f9c568'; CORAL='#fa9f83'; SOFT='#b9cdca'; LINE='#557377'; DARK='#183740'

def title(c,s): c.text(s,63,65,42,INK,'lm',True)
def label(c,s,x,y,size=30,ink=INK): c.text(s,x,y,size,ink,'lm',True)

def pos(g,j): return 202+g*177,496-j*20

def heaps(c,t,moves,levels=True):
    # Each of the four moving beads is an existing member of its source stack.
    flights={(1,12):(0,8),(2,14):(0,9),(2,13):(0,10),(2,12):(0,11)}
    for g,n in enumerate((8,13,15)):
        x,_=pos(g,0)
        c.line([(x-46,508),(x+46,508)],LINE,4)
        c.text(str(g+1),x,549,25,SOFT)
        for j in range(n):
            x,y=pos(g,j);index=list(flights).index((g,j)) if (g,j) in flights else -1
            if index>=0:
                p=moves[index];xx,yy=pos(*flights[g,j]);x=mix(x,xx,p);y=mix(y,yy,p)-95*sin(pi*p)
            c.dot(x,y,9,(MINT,GOLD,CORAL)[g]);c.dot(x-2,y-2,2,INK)
    if levels:
        y=pos(0,11)[1]-10
        for x in range(127,621,17):c.line([(x,y),(x+8,y)],SOFT,1.4)

def timing(t,starts,duration):return [cue(t,s,duration) for s in starts]

def intro(c,t):
    title(c,'What does an average share?')
    if t<8.2:
        heaps(c,t,timing(t,(.65,1.1,1.55,2),1.15));label(c,'36 beads',730,218,46,MINT)
        if t>=2.9:label(c,'3 equal stacks',730,299,38)
        if t>=5.1:label(c,'12 × 3 = 36',730,404,45,GOLD)
    else:
        dots(c,194,225,3,26,MINT);dots(c,194,386,6,8,GOLD)
        label(c,'Pool the two totals',740,249,37)
        if t>=11.2:label(c,'Share across 9 places',740,384,36,MINT)

def dots(c,x,y,count,value,colour,known=True):
    for j in range(count):
        X=x+j*72;c.dot(X,y,29,colour);c.text(str(value) if known else '·',X,y,21 if known else 29,DARK,bold=True)

def bracket(c,x1,x2,y,s,colour,above):
    dep=12 if above else -12
    c.line([(x1,y+dep),(x1,y),(x2,y),(x2,y+dep)],colour,3)
    c.text(s,(x1+x2)/2,y+(-23 if above else 24),25,colour,bold=True)

def readings(c,t,first,last,shared=False,value='D'):
    x0=167;y=317;dx=149
    for i in range(6):
        x=x0+i*dx;c.dot(x,y,34,GOLD if i==3 and shared else LINE)
        c.text(value if i==3 else 'ABCDEF'[i],x,y,27,DARK if i==3 and shared else INK,bold=True)
    if first:bracket(c,x0-31,x0+3*dx+31,y-76,first,MINT,True)
    if last:bracket(c,x0+3*dx-31,x0+5*dx+31,y+65,last,CORAL,False)

def uses(c,t):
    title(c,'Scores, measures and overlapping days')
    if t<23.6:
        for i,n in enumerate((3,6)):
            y=221+i*154;dots(c,182,y,n,(26,8)[i],(MINT,GOLD)[i],False)
            label(c,('3 readings · mean 26','6 readings · mean 8')[i],719,y,32,(MINT,GOLD)[i])
        if t>=20.6:label(c,'Every mean has a count.',411,515,31)
    else:
        readings(c,t,'first four','last three' if t>=25.6 else '',t>=27.6)
        if t>=27.6:label(c,'Day D belongs to both runs.',289,507,35,GOLD)

def basic(c,t):
    title(c,'Share the readings 8, 13 and 15 equally')
    p=timing(t,(38.9,39.8,40.7,41.6),1.3);heaps(c,t,p,levels=t>=38.4)
    label(c,'8 + 13 + 15',733,248,43)
    if t>=35.4:label(c,'Same total',737,348,38,MINT)
    if t>=38.4:label(c,'Equal heights',737,416,38,GOLD)

def basic_result(c,t):
    title(c,'Keep every bead when you redistribute')
    p=timing(t,(48.2,49,49.8,50.6),1.15);heaps(c,t,p,levels=t>=50.8)
    label(c,'8 + 13 + 15 = 36',720,244,36)
    if t>=50.8:label(c,'36 ÷ 3',720,352,44,GOLD)
    if t>=52:label(c,'= 12 each',720,426,44,MINT)

def beam(c,t,pivot,marked=True,tilt=0):
    x=lambda n:160+38*(n-5)
    ground=391
    # A support to the right of the weighted mean leaves the left load lower.
    y=lambda n:ground+tilt*((pivot if pivot is not None else 14)-n)
    c.line([(x(5),y(5)),(x(29),y(29))],INK,7)
    for n in range(5,30):
        X,Y=x(n),y(n);c.line([(X,Y),(X,Y+(18 if n in (8,14,26) else 8))],SOFT,2)
        if n in (8,26):c.text(str(n),X,Y+45,28,GOLD if n==8 else MINT,bold=True)
    for n,count,col in [(8,6,GOLD),(26,3,MINT)]:
        for j in range(count):
            X=x(n)+(j%3-1)*26;Y=y(n)-24-(j//3)*27;c.dot(X,Y,12,col)
        c.text(f'{count} readings',x(n),y(n)-100,26,col,bold=True)
    if pivot is not None:
        X=x(pivot);c.poly([(X,ground+5),(X-30,ground+98),(X+30,ground+98)],CORAL,INK,2)
        if marked:c.text('14',X,ground+77,21,DARK,bold=True)

def medium(c,t):
    title(c,'Combine two groups with different counts')
    label(c,'Equal shares within each group',147,132,25,SOFT)
    label(c,'Mean 26',147,183,30,MINT);dots(c,178,259,3,26,MINT)
    if t>=59.2:
        label(c,'Mean 8',637,183,30,GOLD);dots(c,672,259,6,8,GOLD)
    if t>=62:label(c,'All readings together',153,379,35)
    if t>=65.2:
        for j in range(9):c.dot(186+92*j,477,20,MINT if j<3 else GOLD)
        c.text('3 + 6 = 9 places',570,543,31,INK,bold=True)

def medium_result(c,t):
    title(c,'The larger group pulls the mean towards 8')
    label(c,'3 × 26 = 78',135,174,34,MINT)
    if t>=73.2:label(c,'6 × 8 = 48',466,174,34,GOLD)
    if t>=78.8:label(c,'78 + 48 = 126',790,174,34)
    if t<83:
        dots(c,173,333,3,26,MINT);dots(c,548,333,6,8,GOLD)
        label(c,'After sharing equally within each group',159,246,27,SOFT)
        if t>=80:label(c,'Nine equally weighted readings',270,478,37)
    else:
        progress=cue(t,83.5,2.5)
        beam(c,t,mix(17,14,progress),progress==1,3.1*(1-progress))
        if t>=85.2:label(c,'126 ÷ 9 = 14',437,548,38,CORAL)

def challenge(c,t):
    title(c,'Which reading belongs to both groups?')
    label(c,'Six readings · mean 35/3',165,144,30)
    readings(c,t,'4 readings · mean 23/2' if t>=96.2 else '','3 readings · mean 37/3' if t>=99.4 else '',t>=102.8)
    if t>=102.8:label(c,'Find reading D.',326,527,39,GOLD)

def total_rows(c,t):
    for i,(s,v,when,col) in enumerate([('First four','4 × 23/2 = 46',114.4,MINT),('Last three','3 × 37/3 = 37',116.3,CORAL),('All six','6 × 35/3 = 70',118.3,INK)]):
        y=188+i*105;label(c,s,118,y,32,col)
        if t>=when:label(c,v,417,y,35,col)

def challenge_result(c,t):
    title(c,'Recover the totals, then find the extra reading')
    if t<121:total_rows(c,t);return
    readings(c,t,'first four · total 46','last three · total 37',True,'13' if t>=125 else 'D')
    label(c,'46 + 37 = 83',105,518,36)
    if t>=125:label(c,'83 − 70 = 13',563,518,38,GOLD)

def split_rows(c,t,remove):
    # A B C D above; D E F below. Move the duplicate D towards the original, leaving six places.
    x=176;dx=143;y=239
    for j,ch in enumerate('ABCDEF'):
        X=x+dx*j;Y=y if j<4 else mix(y+136,y,remove)
        c.dot(X,Y,34,GOLD if j==3 else MINT if j<3 else CORAL);c.text('13' if j==3 else ch,X,Y,26,DARK,bold=True)
    if remove<1:
        X=x+dx*3;Y=mix(y+136,y,remove);c.dot(X,Y,34,GOLD);c.text('13',X,Y,26,DARK,bold=True)

def check(c,t):
    title(c,'Count the shared reading exactly once')
    split_rows(c,t,cue(t,139.6,2.3));label(c,'4 + 3 − 1 = 6 distinct positions',132,460,38)
    if t>=139.6:label(c,'46 + 37 − 13 = 70',294,538,39,GOLD)

def mistakes(c,t):
    title(c,'Place each reading in the total once')
    if t<153.6:
        beam(c,t,14);label(c,'Six at 8',148,170,35,GOLD);label(c,'Three at 26',812,170,35,MINT)
        if t>=149.6:label(c,'(48 + 78) ÷ 9 = 14',411,535,35)
    else:
        split_rows(c,t,cue(t,157.4,2));label(c,'D occurs in both subtotals.',216,507,35,GOLD)

def finish(c,t):
    title(c,'Write the count beside each mean')
    for j,(h,col) in enumerate([('Mean',MINT),('Count',GOLD),('Total',CORAL)]):
        x=170+j*327;label(c,h,x,195,36,col);label(c,('35/3','6','70')[j],x,291,48,col)
    if t>=163.2:label(c,'(35/3) × 6 = 70',333,410,41)
    if t>=166.2:label(c,'First four + last three − their shared reading',141,510,30,SOFT)

SCENES=(intro,uses,basic,basic_result,medium,medium_result,challenge,challenge_result,check,mistakes,finish)
def verify():
    assert sum((8,13,15))==3*12 and (13-12)+(15-12)==12-8
    assert Fraction(3*26+6*8,9)==14 and 6*(14-8)==3*(26-14)
    first,last,whole=4*Fraction(23,2),3*Fraction(37,3),6*Fraction(35,3)
    assert (first,last,whole,first+last-whole)==(46,37,70,13) and 4+3-1==6
