"""S029. Quarter a 124-link chain, rank two score slopes and reconstruct the register receipt."""
from math import sin,cos,pi
from fractions import Fraction
from captioned_film import cue,mix,font
ID='S029';ORIGINAL='3e9be04b3fad2a113e7e60b321d71dbf3db250d2a72b3423f32d8416d089f4e9';START=(0,15.8,33.4,47.45,63.61,82.46,107.09,126.10,149.61,165.45,179.21);POSTER=143.54
PAPER='#f4ecdf';INK='#2e303b';SOFT='#685e59';EDGE='#c6b7a4';TICKET='#fffaf1';RED='#a13b40';BLUE='#355b89';GREEN='#147061';CREAM='#dbac64';LIGHT='#ebe0cb'

def title(c,s):
    size=43
    while font(round(size*c.scale),True).getlength(s)>1154*c.scale:size-=1
    c.text(s,63,63,size,INK,'lm',True)
def say(c,s,x,y,sz=33,col=INK):c.text(s,x,y,sz,col,'lm',True)
def dial(c,x,y,n,p,r=102):
    c.dot(x,y,r+3,INK);c.dot(x,y,r,TICKET)
    for i in range(100):
        a=-pi/2+2*pi*i/100;R=r-(10 if i%5==0 else 5);c.line([(x+R*cos(a),y+R*sin(a)),(x+(r-1)*cos(a),y+(r-1)*sin(a))],SOFT,1.8)
    ang=2*pi*p-.5*pi;points=[(x,y)]+[(x+(r-15)*cos(-pi/2+2*pi*j*p/45),y+(r-15)*sin(-pi/2+2*pi*j*p/45)) for j in range(46)]
    c.poly(points,CREAM,None);c.line([(x,y),(x+(r-8)*cos(ang),y+(r-8)*sin(ang))],RED,4);c.dot(x,y,5,INK)
    c.text(n,x,y+r+41,28,INK,bold=True)

def intro(c,t):
    title(c,'A quarter of which whole?');p=.25*cue(t,.6,2.8)
    dial(c,265,312,'Out of 100',p);say(c,'25 / 100',564,230,43,RED)
    if t>=3.8:say(c,'= 0.25 = 25%',564,312,39)
    if t>=8:say(c,'25% of 80 = 20',565,434,32,BLUE)
    if t>=10.8:say(c,'25% of 120 = 30',565,493,32,GREEN)

def receipt(c,x,y,w,h):
    edge=[(x,y),(x+w,y),(x+w,y+h)]+[(x+w-j*w/26,y+h-(7 if j%2 else 0)) for j in range(1,27)];c.poly([(a+5,b+5) for a,b in edge],EDGE,None);c.poly(edge,TICKET,EDGE,1.5)

def uses(c,t):
    title(c,'Compare scores or trace a changing price');receipt(c,155,164,920,344)
    if t<25.2:
        say(c,'SCORE',208,225,25,SOFT);say(c,'Correct / attempted',409,225,35,BLUE)
        say(c,'SHOP',208,354,25,SOFT);say(c,'Discount / earlier price',409,354,35,RED)
        if t>=22.2:say(c,'Put both comparisons in the same form.',211,451,28,GREEN)
    else:
        say(c,'Price paid',217,235,37);say(c,'First adjustment',217,315,31,BLUE)
        if t>=27:say(c,'Second adjustment',217,382,31,RED)
        if t>=29:say(c,'Each uses its own starting price.',217,461,28,GREEN)

def chain(c,progress,highlight=True):
    # Four equal rows, each of thirty-one numbered positions. Pull one whole strand down.
    for row in range(4):
        y=216+row*73+(29*progress if row==3 else 0);col=(GREEN if row==3 and highlight else BLUE)
        for j in range(30):c.line([(175+j*23,y),(175+(j+1)*23,y)],col,2.5)
        for j in range(31):
            x=175+j*23;c.dot(x,y,6 if j%5 else 7,col);c.dot(x,y,2,TICKET)
        c.text('31' if progress else 'ABCD'[row],128,y,24,col,bold=True)
    if highlight and progress:say(c,'one strand',930,461,28,GREEN)

def basic(c,t):
    title(c,'Find 25% of 124');chain(c,0,False)
    say(c,'124 links',150,145,28,SOFT)
    if t>=37:say(c,'25/100',917,227,34,RED)
    if t>=40.4:say(c,'= 1/4',917,317,37,GREEN)

def basic_result(c,t):
    title(c,'Separate four equal strands');p=cue(t,54.4,2.1);chain(c,p)
    say(c,'25 / 100',150,143,31,RED)
    if t>=51.6:say(c,'= 1/4',400,143,32,GREEN)
    if t>=57.2:say(c,'124 ÷ 4 = 31 links',336,552,38,GREEN)

def plot(c,t,phase=0):
    # Both rays start at (0,0). Each grid unit has a fixed horizontal and vertical scale.
    X=lambda n:171+5.48*n;Y=lambda n:478-4.0*n
    c.line([(X(0),Y(65)),(X(0),Y(0)),(X(128),Y(0))],INK,2.3)
    for n in (0,25,45,75,100,125):
        c.line([(X(n),Y(0)),(X(n),Y(0)+7)],INK,2);c.text(str(n),X(n),Y(0)+23,19,SOFT)
    for n in (0,18,40,56):c.text(str(n),X(0)-13,Y(n),18,SOFT,'rm')
    c.text('questions attempted',X(63),554,24,SOFT)
    say(c,'correct answers',129,153,22,SOFT)
    say(c,'Line slope = accuracy',563,153,24,SOFT)
    for n,k,col,p in [(45,18,BLUE,phase[0]),(125,56,RED,phase[1])]:
        if p<=0:continue
        xx,yy=X(n*p),Y(k*p);c.line([(X(0),Y(0)),(xx,yy)],col,3.5);c.dot(xx,yy,6,col)
    if phase[2]>0:
        k=phase[2];n=45+80*k;xx=X(n);yy=Y(n*18/45)
        for d in range(0,int((n-45)*4)+1,12):
            stop=min(n,45+(d+7)/4);left=min(n,45+d/4)
            c.line([(X(left),Y(left*18/45)),(X(stop),Y(stop*18/45))],BLUE,3)
        c.dot(xx,yy,6,BLUE)
        if k==1:
            c.line([(X(125)+12,Y(50)),(X(125)+12,Y(56))],GREEN,4)

def scores(c,t):
    title(c,'Which team answered a larger share correctly?');plot(c,t,(cue(t,63.61,2.0),cue(t,67.8,2.1),0))
    say(c,'A',944,240,30,BLUE);say(c,'18 of 45',944,290,29,BLUE)
    if t>=67.8:say(c,'B',944,372,30,RED);say(c,'56 of 125',944,422,29,RED)

def compare(c,t):
    title(c,'Give both score lines the same number of attempts')
    plot(c,t,(1,1,cue(t,82.46,2.65)))
    say(c,'A: 50 / 125',921,199,27,BLUE);say(c,'B: 56 / 125',921,261,27,RED)
    if t>=87.6:say(c,'18 × 125 = 2,250',901,338,24,BLUE)
    if t>=90.8:say(c,'56 × 45 = 2,520',901,396,24,RED)
    if t>=98.2:say(c,'B is higher.',915,485,31,GREEN)

def price_ticket(c,t,labels,selection,notes):
    receipt(c,159,145,910,394)
    for i,(s,val) in enumerate(zip(('Original price','After 20% rise','After 25% discount'),labels)):
        y=223+104*i;ink=(INK,BLUE,RED)[i]
        if i==selection:c.rect(183,y-34,844,67,LIGHT)
        say(c,s,211,y,32,ink);c.text(val,1002,y,36,ink,'rm',True)
        if i<2:c.line([(205,y+53),(1020,y+53)],EDGE,1)
    if notes:say(c,notes,180,576,27,GREEN)

def challenge(c,t):
    title(c,'Recover the original price from the till receipt')
    price_ticket(c,t,('?','?','$360' if t>=113 else '?'),2 if t>=113 else 1,'Each change acts on the price on the line above.' if t>=118.8 else '')

def reverse(c,t):
    title(c,'Read the receipt upwards to reverse the changes')
    p=0 if t<129.8 else 1 if t<139.6 else 2
    vals=('$400' if t>=142.2 else '?','$480' if t>=133.8 else '?','$360')
    if p==0:note='After the discount, three quarters of the increased price remains.'
    elif p==1:note='$360 ÷ (3/4) = $480'
    else:note='$480 ÷ (6/5) = $400' if t<144.4 else 'Check forwards: $400 × 6/5 = $480. Then $480 × 3/4 = $360.'
    price_ticket(c,t,vals,2-p,note)
    # The pointer takes the reverse path during the two spoken divisions.
    y=431-104*cue(t,129.8,1.5)-104*cue(t,139.6,1.5)
    c.poly([(103,y-14),(103,y+14),(138,y)],GREEN,None)

def combined(c,t):
    title(c,'Two changes make a single exact multiplier');price_ticket(c,t,('$400','$480','$360'),-1,'6/5 × 3/4 = 9/10' if t>=152.8 else '6/5 × 3/4')
    if t>=160.6:
        c.rect(175,542,1000,62,PAPER);say(c,'The rise uses $400. The discount uses $480.',179,575,30,GREEN)

def mistakes(c,t):
    if t<172.4:
        title(c,'Compare both numerators over 125 attempts');plot(c,t,(1,1,cue(t,165.45,2.2)))
        say(c,'50 / 125',930,260,30,BLUE);say(c,'56 / 125',930,352,30,RED)
    else:
        title(c,'A 20% reduction keeps four fifths');dial(c,283,309,'Amount remaining',.8*cue(t,172.4,1.8));say(c,'100% − 20% = 80%',563,272,35)
        if t>=175.8:say(c,'Multiply by 0.80',563,369,37,GREEN)

def finish(c,t):
    title(c,'Which amount was the base at each step?');price_ticket(c,t,('$400','$480','$360'),0 if t<185.4 else 1 if t<190.2 else 2,'Undo the discount first, then undo the increase.' if t>=190.2 else 'Use × 6/5, then × 3/4.' if t>=185.4 else 'Name the base on the receipt.')
SCENES=(intro,uses,basic,basic_result,scores,compare,challenge,reverse,combined,mistakes,finish)
def verify():
    assert 4*31==124 and Fraction(25,100)==Fraction(1,4)
    assert Fraction(18,45)==Fraction(50,125)<Fraction(56,125) and 18*125==2250 and 56*45==2520
    assert 400*Fraction(6,5)==480 and 480*Fraction(3,4)==360 and Fraction(6,5)*Fraction(3,4)==Fraction(9,10)
