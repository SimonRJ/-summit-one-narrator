"""S025. Change the denominator explicitly: 100 cells, 80 tokens, 120 attempts, then two successive prices."""
from fractions import Fraction
from captioned_film import cue,mix
ID='S025';ORIGINAL='b35d00165708c6d01637725b616d620bffdd2c24e3c5a06c0ed1855896179738'
START=(0,15.96,33.72,46.5,62.18,79.75,103.9,123.23,147.06,162.9,176.66)
POSTER=143.3
PAPER='#20283b';INK='#fff2dc';SOFT='#c2cbd3';GRID='#586277';TEAL='#86d5c2';RED='#f09fa1';YELLOW='#f4ca7c';OFF='#384258';DARK='#203346'
def title(c,s):c.text(s,63,62,40,INK,'lm',True)
def note(c,s,x,y,size=32,col=INK):c.text(s,x,y,size,col,'lm',True)
def hundred(c,x,y,u,count):
    for i in range(100):
        X=x+(i%10)*u;Y=y+(i//10)*u
        c.rect(X+1,Y+1,u-2,u-2,TEAL if i<count else OFF,None)
    for k in range(1,10):
        c.line([(x+k*u,y),(x+k*u,y+10*u)],PAPER,2.3)
        c.line([(x,y+k*u),(x+10*u,y+k*u)],PAPER,2.3)
    c.rect(x,y,10*u,10*u,None,SOFT,1.6)
def bundles(c,n,painted,unit=1):
    x,y=124,175;w,h=107,82
    for i in range(n):
        X=x+i%5*w;Y=y+i//5*h
        c.rect(X+4,Y+5,w-8,h-10,OFF,TEAL if i<painted else GRID,2)
        for k in range(4):c.dot(X+32+42*(k%2),Y+25+31*(k//2),9*unit,TEAL if i<painted else '#758398')
def basebars(c,base=200,inc=0,loss=0,showlabels=True):
    x,y,unit=109,313,2.13
    price=base+inc-loss
    c.rect(x,y,base*unit,68,TEAL,None)
    if inc>0:c.rect(x+base*unit,y,inc*unit,68,YELLOW,None)
    if loss>0:
        c.rect(x+price*unit,y,loss*unit,68,OFF,RED,2)
        n=max(1,int(loss*unit/9))
        for i in range(n):c.line([(x+price*unit+(i+.15)*loss*unit/n,y+55),(x+price*unit+(i+.95)*loss*unit/n,y+13)],RED,1.4)
    for v in range(0,251,25):
        X=x+v*unit;c.line([(X,y+82),(X,y+94)],SOFT,1.5)
        if v%50==0:c.text(str(v),X,y+116,20,SOFT)
    c.line([(x,y+84),(x+250*unit,y+84)],SOFT,2)
    c.text('dollars',x+125*unit,y+159,23,SOFT)
    if showlabels:
        X=x+price*unit
        c.line([(X,y-2),(X,y-34)],INK,2)
        c.rect(X-56,y-88,112,53,INK)
        c.text('$'+str(round(price)),X,y-61,29,DARK,bold=True)
def intro(c,t):
    title(c,'What amount is the percentage taken from?')
    if t>=10.65:
        for j,(n,y) in enumerate(((100,235),(60,388))):
            x=150;u=5.1;part=n*.35
            c.rect(x,y,n*u,52,OFF,GRID,2);c.rect(x,y,u*part*cue(t,10.65+j*.6,.9),52,TEAL)
            c.text(f'35% of {n} = {round(part)}',x,y-29,29,TEAL,'lm',True)
        note(c,'Same percentage',747,241,35);note(c,'Different amounts',747,377,35,YELLOW)
        return
    hundred(c,163,156,36,round(35*cue(t,.5,2.9)))
    note(c,'Out of 100',733,200,41,TEAL)
    if t>=4.9:note(c,'35/100 = 0.35 = 35%',733,306,35)
    if t>=8.15:note(c,'Name the whole first.',733,448,34,YELLOW)
def uses(c,t):
    title(c,'Use the same base for a fair comparison')
    x=144;y=245;u=72
    for i in range(5):
        c.rect(x+i*u,y,u-3,64,TEAL if i<2 else OFF,GRID,1)
    c.text('2 / 5',x+5*u/2,y-43,37,INK,bold=True)
    if t>=20:
        for i in range(10):
            c.rect(x+i*u/2,y+129,u/2-2,64,TEAL if i<4 else OFF,GRID,1)
        c.text('4 / 10',x+5*u/2,y+228,32,TEAL,bold=True)
    note(c,'Equal shares',710,229,38)
    if t>=23:note(c,'2/5 = 4/10 = 40%',710,325,38,TEAL)
    if t>=27:note(c,'For two changes, track both bases.',700,464,26,YELLOW)
def basic(c,t):
    title(c,'Find 35% of 80')
    hundred(c,160,151,36,round(35*cue(t,33.9,1.9)))
    note(c,'35 of the 100 cells',727,223,33,TEAL)
    if t>=37:note(c,'Which fraction is that?',725,327,32)
    if t>=40:note(c,'Now apply it to 80.',725,435,35,YELLOW)
def simple(c,t):
    title(c,'Give each twentieth four tokens')
    paint=round(7*cue(t,49.5,3.0))
    bundles(c,20,paint)
    note(c,'35/100 = 7/20',731,184,39,TEAL)
    if t>=51.8:note(c,'80 ÷ 20 = 4 per group',713,300,31)
    if t>=54.6:note(c,'7 groups × 4 = 28',713,417,39,YELLOW)
def scores(c,x,y,cols,rows,count,col,step):
    for i in range(cols*rows):
        cx=x+(i%cols)*step;cy=y+(i//cols)*step
        c.dot(cx,cy,step*.36,col if i<count else GRID)
def teams(c,t):
    title(c,'Can the number correct decide the winner?')
    scores(c,151,214,10,4,17,TEAL,24)
    c.text('Team A  ·  17 of 40',257,162,31,TEAL,bold=True)
    if t>=65.8:
        scores(c,643,215,15,8,53,RED,24)
        c.text('Team B  ·  53 of 120',800,162,31,RED,bold=True)
    if t>=71:c.text('Bring the attempts to the same denominator.',640,492,34,INK,bold=True)
def fair(c,t):
    title(c,'Compare both teams on a scale of 120')
    x,y=160,217;u=8
    for j,(n,name,col) in enumerate(((51,'A',TEAL),(53,'B',RED))):
        Y=y+j*105;c.text(name,x-42,Y+24,32,col,bold=True)
        c.rect(x,Y,u*120,49,OFF,GRID,2)
        shown=n*cue(t,80.4+j*.6,2.5)
        c.rect(x,Y,u*shown,49,col)
        for k in range(0,121,10):c.line([(x+k*u,Y+48),(x+k*u,Y+56)],SOFT,1)
        c.text(str(n)+'/120',x+n*u+86,Y+24,29,col,bold=True)
    if t<84.8:note(c,'17/40 = 51/120',169,468,34,TEAL)
    if t>=84.8:note(c,'17 × 120 = 2,040',163,458,32,TEAL)
    if t>=87.8:note(c,'53 × 40 = 2,120',692,458,32,RED)
    if t>=95.0:c.text('Team B has the higher accuracy.',640,544,38,INK,bold=True)
def price_problem(c,t):
    title(c,'Work backwards from the final price')
    # Equal-width diagram steps are operations. Price bars in the solution use one shared dollar scale.
    x0,x1,x2=227,640,1053
    for x,txt in ((x0,'original'),(x1,'increased'),(x2,'final')):
        c.text(txt,x,198,29,SOFT,bold=True)
        c.poly([(x-86,249),(x+62,249),(x+87,289),(x+62,332),(x-86,332)],OFF,GRID,2)
        c.text('$225' if x==x2 and t>=109.9 else '?',x,291,42,YELLOW if x==x2 else INK,bold=True)
    for a,b,label,col,when in ((x0,x1,'+25%',TEAL,104.2),(x1,x2,'−10%',RED,107.1)):
        if t>=when:
            c.line([(a+98,287),(b-97,287)],col,4);c.poly([(b-97,287),(b-113,277),(b-113,297)],col,None)
            c.text(label,(a+b)/2,254,31,col,bold=True)
    if t>=113.4:c.text('Undo the discount first.',640,461,34,INK,bold=True)
def undo(c,t):
    title(c,'Undo each change using the price it acted on')
    # Begin at the known final value. Restore the discounted part, then remove the original 25% increase.
    first=cue(t,126.75,3.4);second=cue(t,136.75,2.55)
    if t<141.95:basebars(c,200,50*(1-second),25*(1-first))
    else:
        a=cue(t,141.95,1.8);b=cue(t,144.2,1.65)
        basebars(c,200,50*a,25*b)
    note(c,'Final price   $225',757,180,35)
    if t>=126.65:note(c,'$225 ÷ 0.90 = $250',746,270,34,RED)
    if t>=136.75:note(c,'$250 ÷ 1.25 = $200',746,354,34,TEAL)
    if t>=141.95:note(c,'Check   200 → 250 → 225',722,459,31,YELLOW)
def combined(c,t):
    title(c,'A 25% rise and a 10% discount use different bases')
    basebars(c,200,50*cue(t,147.3,1.5),25*cue(t,149.5,1.45))
    note(c,'5/4 × 9/10 = 9/8',747,209,36)
    if t>=152.5:note(c,'$200 × 9/8 = $225',747,311,34,YELLOW)
    if t>=157.0:note(c,'The discount acts on $250.',727,439,29,RED)
def mistake(c,t):
    title(c,'Keep track of what remains')
    if t<169.6:
        scores(c,157,251,10,4,17,TEAL,25);scores(c,666,217,15,8,53,RED,25)
        c.text('17 of 40',272,191,32,TEAL,bold=True);c.text('53 of 120',840,171,32,RED,bold=True)
        c.text('Compare the shares on a common denominator.',640,487,32,INK,bold=True)
        return
    hundred(c,162,152,36,round(100-20*cue(t,169.8,1.9)))
    note(c,'A 20% reduction',729,236,36,RED)
    if t>=169.5:note(c,'100% − 20% = 80%',729,341,35)
    if t>=172.2:note(c,'Multiply by 0.80.',729,449,33,TEAL)
def recap(c,t):
    title(c,'Name the base, then write the multiplier')
    basebars(c,200,50*cue(t,178.4,2.3),25*cue(t,182.2,2.4))
    note(c,'Start at $200.',739,176,32,TEAL)
    if t>=178.4:note(c,'Rise on $200  →  $250',730,262,32)
    if t>=182.2:note(c,'Cut on $250  →  $225',730,347,32,RED)
    if t>=187.2:note(c,'Reverse the steps to go back.',711,468,28,YELLOW)
SCENES=(intro,uses,basic,simple,teams,fair,price_problem,undo,combined,mistake,recap)
def verify():
    assert Fraction(35,100)*80==28 and 7*4==28
    assert Fraction(17,40)==Fraction(51,120)<Fraction(53,120)
    assert 17*120==2040 and 53*40==2120
    assert Fraction(225)/Fraction(9,10)/Fraction(5,4)==200
    assert Fraction(200)*Fraction(5,4)*Fraction(9,10)==225
