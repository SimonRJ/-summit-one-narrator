"""S009. A wooden exchange counter, with loose brass units and removable tens sleeves."""
from stage import mix

BACKGROUND = ('#f2e7cd', '#e4cd9c')
BRIDGE = 'Track the sleeve that crosses from the units drawer into the tens drawer. Later, read the hundreds drawer first.'
INK, DARK, WOOD, EDGE = '#29382e', '#34483b', '#ad7950', '#73553c'
UNIT, SLEEVE, PAPER, GREEN = '#f3cb53', '#ebefce', '#fff5d7', '#34705c'


def check_maths():
    assert 68 + 68 == 136 and divmod(8 + 8, 10) == (1, 6) and divmod(6 + 6 + 1, 10) == (1, 3)
    assert [a for a in range(10) if a + a == 6] == [3]
    assert [(a,b) for a in range(1,10) for b in range(10)
            if a != b and 2*(10*a+5) == 70+b] == [(3,0)]
    choices = []
    for value in range(10,100):
        a,b = divmod(value,10)
        hundreds,remainder = divmod(2*value,100)
        c,d = divmod(remainder,10)
        if b == hundreds and b and len({a,b,c,d}) == 4:
            choices.append(value)
    assert choices and min(choices) == 51 and 2*51 == 102


def counter(a,x,y,opacity=1):
    a.dot(x+2,y+3,14,EDGE,opacity)
    a.dot(x,y,14,UNIT,opacity)
    a.dot(x-3,y-3,3,'#fff0a2',opacity)


def sleeve(a,x,y,opacity=1):
    a.box(x-9,y-38,18,76,radius=6,fill=SLEEVE,edge=GREEN,stroke=2,opacity=opacity)
    for row in range(1,10):
        a.line([(x-6,y-37+7.5*row),(x+6,y-37+7.5*row)],GREEN,1,opacity)


def tray(a,x,y,w,h,label):
    a.box(x+3,y+8,w,h,fill=EDGE,radius=22)
    a.box(x,y,w,h,fill=WOOD,edge=EDGE,radius=22)
    a.box(x+10,y+10,w-20,h-25,fill='#c89b70',edge=EDGE,radius=17)
    a.box(x+w/2-72,y+h-27,144,34,fill=PAPER,edge=EDGE,radius=7)
    a.text(label,x+w/2,y+h-10,22,INK,bold=True)


def equation(a,text,op=1):
    a.text(text,640,554,46,INK,bold=True,opacity=op)


def draw(a,n,t):
    titles=['Two equal trays','Exchange ten loose units','Where did seven tens come from?',
            'Read the counter backwards','Only one hundred can arrive','The first working pair','Carry through a second drawer']
    a.label(titles[n-1],76,81,47,INK,bold=True)
    a.line([(77,122),(1203,122)],EDGE,2)
    if n==1:
        tray(a,124,215,430,222,'A')
        tray(a,727,215,430,222,'A')
        f=t.reveal('Split them equally',1.7)
        for i in range(6):
            left=i%2==0; k=i//2
            cx=(228 if left else 830)+k*80
            counter(a,mix(492+i*55,cx,f),mix(172,322,f))
        equation(a,'3 + 3 = 6',t.reveal('Three on this tray'))
    elif n==2:
        a.text('A5 + A5 = 7B',640,160,40,INK,bold=True)
        tray(a,94,205,495,248,'TENS')
        tray(a,693,205,495,248,'UNITS')
        gather=t.reveal('All ten fit',1.3)
        carry=t.reveal('one ten',1.1)
        for row in range(2):
            for j in range(5):
                counter(a,mix(780+77*j,962,gather),mix(292+56*row,314,gather),1-gather)
        sleeve(a,mix(962,340,carry),314-50*4*carry*(1-carry),gather)
        a.text('0',944,322,78,INK,bold=True,opacity=t.reveal('Its digit is zero'))
        equation(a,'5 + 5 = 10',t.reveal('two groups of five'))
    elif n==3:
        tray(a,92,206,1098,249,'TENS')
        split=t.reveal('shared equally',1.4)
        separate=t.reveal('Take that one aside',1.1)
        for j in range(6):
            target=(226 if j<3 else 574)+(j%3)*62
            sleeve(a,mix(295+91*j,target,split),323)
        sleeve(a,mix(841,1040,separate),mix(323,263,separate))
        a.text('from units',1040,342,22,INK,bold=True,opacity=separate)
        a.text('3 tens',290,397,29,INK,bold=True,opacity=split)
        a.text('3 tens',635,397,29,INK,bold=True,opacity=split)
        equation(a,'35 + 35 = 70',t.reveal('Thirty five and thirty five'))
    elif n==7:
        carry_units = t.reveal('send one ten across', 1.1)
        count_tens = t.reveal('make thirteen tens', .6)
        carry_tens = t.reveal('Exchange ten of those tens', 1.4)
        show_units = t.reveal('Leave six in the units drawer', .55)
        for x, label in zip((85, 466, 847), ('HUNDREDS', 'TENS', 'UNITS')):
            tray(a,x,215,345,222,label)
        for index in range(6):
            x, y = 914 + index % 3 * 63, 290 + index // 3 * 50
            counter(a,x,y,show_units)
        sleeve(a,mix(1110,758,carry_units),304-57*4*carry_units*(1-carry_units),
               t.reveal('Leave six in the units drawer')*(1-carry_tens))
        for index in range(12):
            x = 497 + index % 6 * 39
            y = 269 + index // 6 * 82
            grouped = index < 9
            # The ninth original sleeve joins the carried sleeve to make ten.
            sleeve(a,mix(x,605,carry_tens) if grouped else x,
                   mix(y,307,carry_tens) if grouped else y,
                   count_tens*(1-carry_tens if grouped else 1))
        block_x=mix(630,260,carry_tens)
        a.box(block_x-45,266,90,90,fill=SLEEVE,edge=GREEN,radius=3,stroke=3,opacity=carry_tens)
        for i in range(1,10):
            a.line([(block_x-45+9*i,266),(block_x-45+9*i,356)],GREEN,1,carry_tens)
            a.line([(block_x-45,266+9*i),(block_x+45,266+9*i)],GREEN,1,carry_tens)
        equation(a,'68 + 68 = 136',t.reveal('The drawers read'))
    else:
        # A full-width addition counter holds the same place-value columns throughout.
        a.box(92,156,602,354,fill=DARK,edge=EDGE,radius=20)
        for j,h in enumerate(('H','T','U')):
            a.text(h,280+152*j,194,25,'#d7e1ca',bold=True)
        for j,y in enumerate((253,321,422)):
            a.text('+' if j==1 else '',141,y,44,PAPER)
            if n==4: characters=(' AB',' AB','BCD')[j]
            elif n==5: characters=(' AB',' AB','BCD')[j]
            else: characters=(' A1',' A1','1C2')[j]
            if n==5:
                if t.reveal('B is one')>0.5: characters=characters.replace('B','1')
                if t.reveal('D is two')>0.5: characters=characters.replace('D','2')
            if n==6 and t.reveal('Five on each tray')>0.5: characters=characters.replace('A','5')
            if n==6 and t.reveal('C is zero')>0.5: characters=characters.replace('C','0')
            for x,c in zip((280,432,584),characters):
                if c!=' ':a.text(c,x,y,46,PAPER,bold=True)
        a.line([(180,365),(640,365)],PAPER,3)
        if n==4:
            a.label('A B + A B',758,241,48,INK,bold=True)
            a.label('Four different digits',758,335,30,INK, t.reveal('Different letters'))
            a.label('Smallest first number?',758,406,29,GREEN,t.reveal('smallest possible'))
        if n==5:
            a.label('99 + 99 = 198',743,214,41,INK,bold=True)
            a.label('B = 1',743,304,49,GREEN,t.reveal('B is one'),bold=True)
            a.label('1 + 1 = 2',743,393,40,INK,t.reveal('One plus one'))
            equation(a,'D = 2',t.reveal('D is two'))
        if n==6:
            a.label('4 tens each → 8 tens',744,222,34,INK)
            a.label('5 tens each → 10 tens',744,303,35,GREEN,t.reveal('Five on each tray'),bold=True)
            a.label('1 hundred, 0 tens',744,395,32,INK,t.reveal('one hundred'))
            equation(a,'51 + 51 = 102',t.reveal('Read the finished drawers'))


def poster(draw):
    return draw(8,1.5)
