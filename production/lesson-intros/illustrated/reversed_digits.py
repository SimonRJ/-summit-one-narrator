"""S010: animate a digit reversal and a separate column-carry puzzle."""
from math import sin,pi
from visuals import AQUA, BLUE, GOLD, PINK, SOFT, WHITE, VIOLET, ease, mix


def text(a,t,x,y,size=34,col=WHITE,alpha=1):a.label(t,x,y,size,col,alpha,bold=True)


def card(a,value,x,y,col,alpha=1,size=92):
    a.rounded(x-size/2,y-size/2,size,size,14,col,.20*alpha)
    text(a,value,x,y,48,col,alpha)


def pair(a,left,right,x,y,p=0):
    """The two digit cards swap on separate curved paths."""
    lift=65*sin(pi*p)
    card(a,left,mix(x-65,x+65,p),y-lift,BLUE)
    card(a,right,mix(x+65,x-65,p),y+lift,GOLD)


def add_grid(a,top,second,result,p=1,swaps=None,carry=0):
    colours={'A':BLUE,'B':GOLD,'C':AQUA,'D':PINK,'1':GOLD,'2':BLUE,'3':PINK,'4':BLUE,'5':BLUE,'6':BLUE,'9':AQUA,'0':WHITE}
    swaps=swaps or {}
    for row,value in enumerate((top,second,result)):
        yy=235+row*100+(22 if row==2 else 0)
        for i,ch in enumerate(value.rjust(3)):
            if ch==' ':continue
            x=500+(i-2)*94;col=colours.get(ch,WHITE)
            a.rounded(x-38,yy-38,76,76,10,col,.13*p)
            if ch in swaps:
                replacement,q=swaps[ch]
                text(a,ch,x,yy,48,col,p*max(0,1-2*q))
                text(a,replacement,x,yy,48,colours.get(replacement,WHITE),p*max(0,2*q-1))
            else:text(a,ch,x,yy,48,col,p)
    text(a,'+',242,335,43,SOFT,p)
    a.path(((260,395),(550,395)),SOFT,3,p)
    text(a,'1',406,157,30,GOLD,carry)


def intro(a,c):
    a.heading('Letters hide digits',AQUA)
    p=c.after('one digit wherever it appears')
    card(a,'A',430,300,BLUE,p);card(a,'A',640,300,BLUE,p);card(a,'A',850,300,BLUE,p)
    text(a,'same letter, same digit',640,440,36,WHITE,p)
    text(a,'different letters may need different digits',640,525,28,SOFT,c.after('Different letters'))


def exams(a,c):
    a.heading('A number can change when digits move',AQUA)
    p=c.after('letters or boxes')
    card(a,'A',540,300,BLUE,p);card(a,'B',740,300,GOLD,p)
    text(a,'tens',540,395,28,SOFT,p);text(a,'ones',740,395,28,SOFT,p)
    text(a,'Leading digits cannot be zero',640,520,32,WHITE,c.after('leading digit'))


def easy(a,c):
    a.heading('The same digit twice',BLUE)
    p=c.after('same digit A')
    card(a,'A',440,300,BLUE,p);card(a,'A',840,300,BLUE,p)
    text(a,'+',640,300,52,WHITE,p)
    q=c.after('result is eight')
    for i in range(8):a.circle((325+90*i,480),15,GOLD,ease(q*2-i*.1))
    text(a,'8',1110,480,38,GOLD,q)


def easy_answer(a,c):
    a.heading('Share eight equally',BLUE)
    p=c.after('Dividing the whole result',1.7)
    for group,x in enumerate((450,830)):
        a.rounded(x-160,235,320,150,14,BLUE,.14*p)
        text(a,'A',x,210,38,BLUE,p)
        for i in range(4):
            sx=325+(group*4+i)*90;dx=x-105+70*i
            a.circle((mix(sx,dx,p),mix(485,310,p)),15,GOLD,c.opening())
    text(a,'4 + 4 = 8',640,505,50,WHITE,c.after('Half of eight is four'))


def reverse_prompt(a,c):
    a.heading('A two-digit reversal',GOLD)
    p=c.after('reverses its digits',1.8)
    pair(a,'A','B',540,300,p)
    text(a,'A + B = 8',980,270,38,WHITE,c.after('sum eight'))
    text(a,'AB + 36 = BA',950,400,37,GOLD,c.after('thirty-six'))
    text(a,'Both numbers have two digits',640,535,30,SOFT,c.after('Both numbers'))


def reverse_answer(a,c):
    a.heading('Compare the place values',GOLD)
    text(a,'AB = 10A + B',430,220,37,BLUE,c.after('A B means'))
    text(a,'BA = 10B + A',850,220,37,GOLD,c.after('B A means'))
    text(a,'BA − AB = 9(B − A)',640,320,39,WHITE,c.after('nine times B minus A'))
    text(a,'B − A = 36 ÷ 9 = 4',640,405,38,AQUA,c.after('difference in the two digits'))
    text(a,'A + B = 8',430,495,34,SOFT,c.after('given sum'))
    text(a,'A = 2     B = 6',850,495,38,WHITE,c.after('A is two'))
    text(a,'26 + 36 = 62',640,562,35,GOLD,c.after('Check the two-digit numbers'))


def hard(a,c):
    a.heading('Find the smallest AB',VIOLET)
    add_grid(a,'AB','AC','BD0',c.after('A B plus A C'))
    text(a,'A, B, C, D are distinct',920,265,30,SOFT,c.after('distinct digits'))
    text(a,'A and B are nonzero',920,340,30,SOFT,c.after('nonzero'))
    text(a,'Use the hundreds carry',920,475,32,GOLD,c.after('carry creates'))


def hard_answer(a,c):
    a.heading('Follow the hundreds and units',VIOLET)
    b=c.after('B is one',.7);nine=c.after('C is nine',.7);carry=c.after('one ten carries',1.2)
    add_grid(a,'AB','AC','BD0',swaps={'B':('1',b),'C':('9',nine)},carry=carry)
    text(a,'B = 1',940,230,37,GOLD,b)
    text(a,'1 + C = 10',940,320,37,AQUA,c.after('One plus C'))
    text(a,'C = 9',940,395,37,AQUA,nine)
    text(a,'2A + 1 determines D',940,490,31,WHITE,c.after('twice A plus one'))


def hard_check(a,c):
    a.heading('Test the smallest possibilities',VIOLET)
    first=c.after('Try A equals five',.7);invalid=c.after('already used by B',.7)
    card(a,'5',310,275,BLUE,first)
    text(a,'A = 5 → D = 1',650,275,42,WHITE,first)
    text(a,'D and B would both be 1',650,345,30,PINK,invalid)
    a.path(((850,245),(900,305)),PINK,4,invalid);a.path(((850,305),(900,245)),PINK,4,invalid)
    good=c.after('Six works',.7)
    card(a,'6',310,455,BLUE,good)
    text(a,'A = 6 → D = 3',650,455,42,WHITE,good)
    text(a,'61 + 69 = 130',940,540,35,AQUA,c.after('sixty-nine'))


def mistakes(a,c):
    a.heading('Letters still have place value',PINK)
    text(a,'AB',410,285,68,BLUE,c.after('two-digit number'))
    text(a,'=',610,285,50,SOFT,c.after('two-digit number'))
    text(a,'10A + B',875,285,57,WHITE,c.after('ten times as much'))
    text(a,'A in the tens place is worth ten A',640,430,32,SOFT,c.after('tens place'))
    text(a,'Check leading digits and distinctness',640,530,31,PINK,c.after('leading zero'))


def recap(a,c):
    a.heading('Write, carry, check',AQUA)
    p=c.after('columns and mark',.7)
    add_grid(a,'61','69','130',p,carry=p)
    text(a,'A = 6   B = 1',930,265,36,BLUE,c.after('first digit'))
    text(a,'C = 9   D = 3',930,350,36,AQUA,c.after('first digit'))
    text(a,'61 + 69 = 130',930,465,35,WHITE,c.after('each value back'))


SCENES=(intro,exams,easy,easy_answer,reverse_prompt,reverse_answer,hard,hard_answer,hard_check,mistakes,recap)
def draw(a,c,scene):SCENES[scene-1](a,c)
