"""S009: animate the actual addition columns, carries and digit constraints."""
from visuals import AQUA, BLUE, GOLD, PINK, SOFT, WHITE, VIOLET, ease, mix


def text(a,t,x,y,size=34,col=WHITE,alpha=1):a.label(t,x,y,size,col,alpha,bold=True)


def column(a,first,second,answer,x=505,y=245,alpha=1,carry=None,carry_target=-1,swaps=None):
    colours={'A':BLUE,'B':GOLD,'C':AQUA,'D':PINK,'0':AQUA,'1':GOLD,'2':PINK,'3':BLUE,'5':BLUE,'6':WHITE,'7':WHITE}
    swaps=swaps or {}
    for row,value in enumerate((first,second,answer)):
        yy=y+row*105+(27 if row==2 else 0)
        for i,ch in enumerate(value.rjust(3)):
            if ch==' ':continue
            xx=x+(i-2)*100
            if ch not in swaps:text(a,ch,xx,yy,68,colours.get(ch,WHITE),alpha)
            else:
                replacement,p=swaps[ch]
                text(a,ch,xx,yy,68,colours.get(ch,WHITE),alpha*max(0,1-2*p))
                text(a,replacement,xx,yy,68,colours.get(replacement,WHITE),alpha*max(0,2*p-1))
    text(a,'+',x-245,y+105,48,SOFT,alpha)
    a.path(((x-225,y+165),(x+55,y+165)),SOFT,3,alpha)
    if carry is not None:text(a,'1',x+100*carry_target,y-80,35,GOLD,carry)


def moving_carry(a,start,end,p):
    if p<.5:
        x=start[0];y=mix(start[1],end[1],2*p)
    else:
        x=mix(start[0],end[0],2*p-1);y=end[1]
    text(a,'1',x,y,33,GOLD,p)


def opening(a,c):
    a.heading('One letter keeps one digit',BLUE)
    p=c.after('one digit wherever it appears',.7)
    for x in (360,640,920):
        a.rounded(x-55,240,110,110,15,BLUE,.17*p)
        text(a,'A',x,295,66,BLUE,p)
    q=c.after('Different letters',.7)
    text(a,'A',500,485,52,BLUE,q);text(a,'B',780,485,52,GOLD,q)
    text(a,'different when the rules require it',640,550,28,SOFT,q)


def exams(a,c):
    a.heading('A hidden digit in each column',AQUA)
    column(a,'AB','AB','BCD',alpha=c.after('letters or boxes'))
    p=c.after('leading digit',.8)
    a.arrow((230,482),(275,482),AQUA,p)
    text(a,'a carry can fix',975,280,34,SOFT,p)
    text(a,'the leading digit',975,330,34,AQUA,p)


def easy(a,c):
    a.heading('A + A = 6',BLUE)
    p=c.after('same digit A',.7)
    for x in (420,860):
        a.rounded(x-100,240,200,155,16,BLUE,.18*p)
        text(a,'A',x,315,76,BLUE,p)
    text(a,'+',640,315,65,WHITE,p)
    q=c.after('result is six',.6)
    for i in range(6):a.circle((390+i*100,505),18,GOLD,ease(q*2-i*.12))
    text(a,'6',1100,505,42,GOLD,q)


def easy_answer(a,c):
    a.heading('Split six into two equal groups',BLUE)
    p=c.after('dividing the whole result',1.8)
    for k,x in enumerate((450,830)):
        a.rounded(x-145,240,290,145,15,BLUE,.14*p)
        text(a,'A',x,215,40,BLUE,p)
        for i in range(3):
            start_x=390+(3*k+i)*100;end_x=x-80+i*80
            a.circle((mix(start_x,end_x,p),mix(480,312,p)),18,GOLD,c.opening())
    q=c.after('Half of six is three',.7)
    text(a,'3 + 3 = 6',640,490,56,WHITE,q)
    text(a,'A = 3',640,555,37,BLUE,q)


def medium(a,c):
    a.heading('Follow the carry',GOLD)
    column(a,'A5','A5','7B',alpha=c.after('A five'))
    text(a,'A and B are different',930,315,31,SOFT,c.after('distinct digits'))
    text(a,'What are A and B?',930,455,37,WHITE,c.after('two digits'))


def medium_answer(a,c):
    a.heading('Five plus five makes a new ten',GOLD)
    zero=c.after('Write zero in the units',.7)
    ap=c.after('A is three',.65)
    column(a,'A5','A5','7B',swaps={'B':('0',zero),'A':('3',ap)})
    carry=c.after('carry one ten',1.5)
    moving_carry(a,(605,355),(405,165),carry)
    text(a,'5 + 5 = 10',930,255,42,GOLD,c.after('five plus five'))
    text(a,'2A + 1 = 7',930,365,40,BLUE,c.after('twice A plus one'))
    text(a,'A = 3   B = 0',930,480,36,AQUA,ap)


def hard(a,c):
    a.heading('Find the smallest AB',VIOLET)
    column(a,'AB','AB','BCD',alpha=c.after('A B plus A B'))
    text(a,'A, B, C, D are distinct',925,280,30,SOFT,c.after('distinct digits'))
    text(a,'A and B are nonzero',925,355,30,SOFT,c.after('leading digits'))
    text(a,'Start with the hundreds',925,480,34,GOLD,c.after('carry into hundreds'))


def hard_answer(a,c):
    a.heading('The first digit is a carry',VIOLET)
    b=c.after('B is one',.6);d=c.after('D equals two',.6)
    column(a,'AB','AB','BCD',swaps={'B':('1',b),'D':('2',d)})
    text(a,'B = 1',935,230,40,GOLD,b)
    text(a,'1 + 1 = 2, so D = 2',935,325,33,PINK,d)
    text(a,'2A reaches ten',935,420,35,BLUE,c.after('tens double A'))
    text(a,'A ≥ 5',935,495,41,BLUE,c.after('at least five'))


def hard_check(a,c):
    a.heading('Try the smallest allowed A',VIOLET)
    a5=c.after('Start at five',.65);c0=c.after('C equals zero',.65)
    column(a,'A1','A1','1C2',carry=c0,carry_target=-2,swaps={'A':('5',a5),'C':('0',c0)})
    text(a,'A = 5',930,245,39,BLUE,a5)
    text(a,'C = 0',930,325,39,AQUA,c0)
    text(a,'51 + 51 = 102',930,435,37,WHITE,c.after('fifty-one'))
    text(a,'all four digits differ',930,515,29,SOFT,c.after('distinct from the other letters'))


def mistakes(a,c):
    a.heading('A digit has a place value',PINK)
    p=c.after('two-digit number',.7)
    text(a,'51',430,290,87,WHITE,p)
    text(a,'=',610,290,58,SOFT,p)
    text(a,'50 + 1',870,290,62,WHITE,p)
    a.arrow((405,355),(810,440),BLUE,c.after('ten times as much',1.5))
    text(a,'5 tens',800,500,38,BLUE,c.after('tens place'))
    text(a,'1 one',1040,500,38,GOLD,c.after('units'))


def recap(a,c):
    a.heading('Columns, carries, then check',AQUA)
    p=c.after('columns and mark',.7)
    column(a,'51','51','102',alpha=p,carry=p,carry_target=-2)
    text(a,'A = 5     B = 1',930,260,37,BLUE,c.after('first digit'))
    text(a,'C = 0     D = 2',930,345,37,AQUA,c.after('first digit'))
    text(a,'check the digits and the sum',930,470,30,SOFT,c.after('each value back'))


SCENES=(opening,exams,easy,easy_answer,medium,medium_answer,hard,hard_answer,hard_check,mistakes,recap)
def draw(art,cues,scene):SCENES[scene-1](art,cues)
