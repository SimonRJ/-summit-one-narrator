"""S095. Coloured ledger entries reveal how often each unknown occurs."""
from stage import mix

BACKGROUND=('#faf6e9','#e4e9dd')
BRIDGE='Follow the three pairs into the ledger. When you subtract a pair from the total of all three boxes, which box stays behind?'
INK='#263f40'; TEAL='#22776e'; RUST='#a44632'; BLUE='#355d8a'; PAPER='#fffaf0'; RULE='#99a9a0'
COLORS={'A':TEAL,'B':RUST,'C':BLUE}
TITLES=['Line up the two numbers','Take away the difference','Two receipts, two prices',
        'Price a notebook and a ruler','Read the three pair totals','Find the missing box',
        'Prove the assignment is unique']


def check_maths():
    assert [(u,v) for u in range(19) for v in range(19) if u+v==18 and v-u==4]==[(7,11)]
    assert [(n,r) for n in range(31) for r in range(31) if 2*n+r==27 and n+2*r==30]==[(8,11)]
    assert [(a,b,c) for a in range(25) for b in range(25) for c in range(25)
            if (a+b,b+c,c+a)==(19,24,21)]==[(8,11,13)]


def value(a,word,x,y,size=34,colour=INK,opacity=1):
    a.text(word,x,y,size,colour,bold=True,opacity=opacity)


def paper(a,x,y,w,h):
    a.box(x+4,y+6,w,h,fill='#afbaaf',radius=8)
    a.box(x,y,w,h,fill=PAPER,edge=RULE,radius=8)


def item(a,kind,x,y,opacity=1):
    if kind=='book':
        a.box(x-27,y-35,54,69,radius=4,fill=TEAL,edge=INK,opacity=opacity)
        a.line([(x-16,y-34),(x-16,y+34)],PAPER,2,opacity)
        a.box(x-8,y-13,27,18,radius=1,fill=PAPER,opacity=opacity)
    else:
        a.box(x-38,y-13,76,26,radius=2,fill='#eebd65',edge=RUST,opacity=opacity)
        for i in range(9):
            a.line([(x-32+i*8,y-12),(x-32+i*8,y-(1 if i%2==0 else 5))],RUST,2,opacity)


def entry(a,x,y,goods,total,op=1):
    for j,kind in enumerate(goods):
        item(a,kind,x+j*104,y,op)
        if j<len(goods)-1:value(a,'+',x+j*104+52,y,26,INK,op)
    value(a,'=',x+len(goods)*104-43,y,30,INK,op)
    value(a,total,x+len(goods)*104+42,y,38,RUST,op)


def token(a,letter,x,y,op=1):
    a.box(x-35,y-28,70,56,radius=8,fill=COLORS[letter],opacity=op)
    value(a,letter,x,y,36,PAPER,op)


def draw(a,n,t):
    a.label(TITLES[n-1],77,75,46,INK,bold=True)
    a.line([(75,116),(1203,116)],RULE,3)
    if n in (1,2):
        paper(a,76,155,1124,369)
        restore=t.reveal('larger is eleven',1.1) if n==2 else 0
        remove=t.reveal('Remove the extra four',1.15)*(1-restore) if n==2 else 0
        split=t.reveal('smaller is seven') if n==2 else 0
        op=t.reveal('four more') if n==1 else 1
        for y,label in [(292,'Smaller'),(402,'Larger')]:
            a.label('Larger − 4' if y==402 and remove>.65 else label,112,y,27,INK,bold=True)
            a.box(315,y-35,379,70,fill=TEAL,radius=4)
            value(a,'7' if split>.5 else '?',505,y,38,PAPER)
        x=mix(698,874,remove);y=mix(367,217,remove)
        a.box(x,y,215,70,fill=RUST,radius=4,opacity=op)
        value(a,'4',x+107,y+35,38,PAPER,op)
        if n==1:
            value(a,'Both rows total 18',625,562,41,TEAL,t.reveal('add to eighteen'))
        else:
            value(a,'18 − 4 = 14',1044,364,29,RUST,t.reveal('remaining fourteen'))
            value(a,'14 ÷ 2 = 7',1044,438,29,TEAL,t.reveal('two equal copies'))
            value(a,'7 + 11 = 18      11 − 7 = 4',640,568,36,INK,t.reveal('Check both'))
    elif n in (3,4):
        paper(a,77,154,675,362)
        a.label('Stationery receipts',115,193,30,INK,bold=True)
        entry(a,152,297,('book','book','ruler'),'$27')
        a.line([(116,361),(712,361)],RULE,2)
        entry(a,152,425,('book','ruler','ruler'),'$30',t.reveal('One notebook and two') if n==3 else 1)
        if n==3:
            item(a,'book',861,313);value(a,'+',922,313);item(a,'ruler',995,313)
            value(a,'= ?',1102,313,42,RUST,t.reveal('Find the price'))
        else:
            value(a,'3 matching pairs',986,202,33,INK,t.reveal('three notebooks'))
            value(a,'$57 ÷ 3 = $19',986,285,39,TEAL,t.reveal('Divide by three'))
            value(a,'$27 − $19 = $8',986,383,37,INK,t.reveal('Subtract that'))
            value(a,'$19 − $8 = $11',986,471,37,RUST,t.reveal('leaving eleven'))
            value(a,'2 × $8 + $11 = $27       $8 + 2 × $11 = $30',640,572,30,INK,t.reveal('Both original prices'))
    else:
        paper(a,78,145,546,403)
        a.label('Pairs in the ledger',114,183,30,INK,bold=True)
        for j,(letters,total,phrase) in enumerate([('AB',19,'A and B together'),('BC',24,'B and C hold'),('CA',21,'C and A hold')]):
            y=269+j*100
            op=t.reveal(phrase) if n==5 else 1
            token(a,letters[0],160,y,op);value(a,'+',232,y,26,INK,op)
            token(a,letters[1],306,y,op)
            value(a,'=',388,y,30,INK,op);value(a,str(total),488,y,43,RUST,op)
        if n==5:
            for j,letter in enumerate('ABC'):token(a,letter,744+j*148,308)
            value(a,'?',744,390,44,TEAL);value(a,'?',892,390,44,RUST);value(a,'?',1040,390,44,BLUE)
        elif n==6:
            value(a,'19 + 24 + 21 = 64',918,187,36,INK,t.reveal('combined sum sixty-four'))
            value(a,'2 × (A + B + C) = 64',918,256,35,INK,t.reveal('is twice the number'))
            value(a,'A + B + C = 32',918,330,38,TEAL,t.reveal('complete total thirty-two'))
            for j,(symbol,shown,cue) in enumerate([('A','32 − 24 = 8','A equals eight'),('B','32 − 21 = 11','B equals eleven'),('C','32 − 19 = 13','C equals thirteen')]):
                op=t.reveal(cue);value(a,symbol,741,400+j*52,30,COLORS[symbol],op);value(a,shown,964,400+j*52,32,INK,op)
        else:
            for j,(letter,number) in enumerate(zip('ABC',(8,11,13))):
                x=747+j*145;token(a,letter,x,206);value(a,str(number),x,271,38,COLORS[letter])
            for j,formula in enumerate(['8 + 11 = 19','11 + 13 = 24','13 + 8 = 21']):
                value(a,formula,893,357+j*63,32,INK,t.reveal(['nineteen','twenty-four','twenty-one'][j]))
            value(a,'One total, one value for each box',640,575,36,TEAL,t.reveal('only one such'))


def poster(draw):
    return draw(4.0,1.5)
