"""The sorting drawers, a film about what defines one case in a systematic list."""
from itertools import permutations, product

BACKGROUND = ('#f6f2e1', '#e2e7d6')
INK = '#293d3b'
GREEN = '#3d6b5b'
GOLD = '#e6b95d'
RED = '#a05238'
PAPER = '#fff9e9'
WOOD = '#b99572'
RULE = '#aa9273'
TITLES = [
    'Choose the first digit', 'Finish every digit drawer', 'Read two labelled counters',
    'List each ordered pair', 'Open three labelled boxes', 'Set the limits of each row',
    'Count the fourteen triples', 'Pack two unlabelled parcels',
]
BRIDGE = 'Follow one drawer all the way across before opening the next. In the last chapter, check how the list changes when the two parcels can swap places.'


def check_maths():
    assert sorted(10*a+b for a,b in permutations((1,2,3),2)) == [12,13,21,23,31,32]
    pairs = [(a,b) for a,b in product(range(1,9),repeat=2) if a+b==13]
    assert pairs == [(5,8),(6,7),(7,6),(8,5)]
    triples = [(a,b,c) for a,b,c in product(range(1,7),repeat=3) if a%2==0 and a+b+c==11]
    assert [[b for a,b,c in triples if a==k] for k in (2,4,6)] == [[3,4,5,6],[1,2,3,4,5,6],[1,2,3,4]]
    assert len(triples)==14 and all(11-a-b==c for a,b,c in triples)
    loads={tuple(sorted((a,b))) for a,b in product(range(1,9),repeat=2) if a+b==10}
    assert sorted(loads)==[(2,8),(3,7),(4,6),(5,5)]


def text(a, label, x, y, size=32, color=INK, opacity=1):
    a.text(label,x,y,size,color,bold=True,opacity=opacity)


def drawer(a,x,y,w,h):
    a.box(x+5,y+6,w,h,radius=10,fill=RULE)
    a.box(x,y,w,h,radius=10,fill=WOOD,edge=INK,stroke=2)
    a.box(x+9,y+9,w-18,h-18,radius=7,fill=PAPER,edge=RULE,stroke=2)


def tab(a, x, y, label, color=GREEN, opacity=1, width=105, height=60):
    a.box(x,y,width,height,radius=6,fill=color,edge=INK,opacity=opacity)
    text(a,label,x+width/2,y+height/2,round(height*.56),PAPER if color!=GOLD else INK,opacity)


def counter(a,x,y,label):
    a.dot(x,y,77,INK);a.dot(x,y,71,GOLD);a.dot(x,y,61,PAPER)
    text(a,label,x,y,62,GREEN)


def parcel(a,x,y,weight,opacity):
    a.box(x,y,98,70,fill=WOOD,edge=INK,radius=4,opacity=opacity)
    a.line([(x+48,y+3),(x+48,y+67)],GOLD,6,opacity)
    a.box(x+10,y+20,78,31,fill=PAPER,radius=3,opacity=opacity)
    text(a,str(weight)+' kg',x+49,y+35,21,INK,opacity)


def draw(a, number, t):
    a.label(TITLES[number-1],74,73,43,INK,bold=True)
    a.line([(75,117),(1205,117)],RULE,3)
    if number==1:
        drawer(a,90,163,524,340);drawer(a,665,163,524,340)
        text(a,'Digit tiles',352,223,33)
        for j in range(3):
            tab(a,146+j*135,313,str(j+1),GREEN,t.reveal(('one, two and three','two and three','three')[j]))
        text(a,'Tens',817,245,31);text(a,'Ones',1031,245,31)
        for x in (758,971):
            a.box(x,295,124,100,fill='#e9ecdb',edge=RULE,radius=5)
            text(a,'?',x+62,346,52,GREEN,t.reveal('two-digit numbers'))
        text(a,'Which position sorts the numbers first?',640,565,35,RED,t.reveal('which position'))
    elif number==2:
        for j,(label,values,cues) in enumerate([('Tens 1',(12,13),('twelve','thirteen')),('Tens 2',(21,23),('twenty-one','twenty-three')),('Tens 3',(31,32),('thirty-one','thirty-two'))]):
            x=86+j*375;drawer(a,x,166,352,347)
            text(a,label,x+176,235,40,GREEN)
            for k,v in enumerate(values):
                pos=x+47+140*k
                ready=t.reveal('other two digits') if j==0 else t.reveal('each remaining tens digit',.7,offset=.2*j)
                tab(a,pos,326,f'{j+1} | {v%10}',GREEN,ready)
                tab(a,pos,326,str(v),GOLD,t.reveal(cues[k]))
        text(a,'12 < 13 < 21 < 23 < 31 < 32',640,571,41,INK,t.reveal('thirty-two'))
    elif number==3:
        drawer(a,91,154,1098,375)
        counter(a,340,331,'A');counter(a,940,331,'B')
        text(a,'+',640,322,68,GREEN)
        for x in (340,940):
            text(a,'1 to 8',x,454,36,INK,t.reveal('one to eight'))
        text(a,'A + B = 13',640,561,42,RED,t.reveal('sum to thirteen'))
    elif number==4:
        drawer(a,95,155,1090,368)
        text(a,'A',202,278,46,GREEN);text(a,'B',202,426,46,RED)
        for i,(aa,bb) in enumerate(((5,8),(6,7),(7,6),(8,5))):
            x=327+i*201
            op=t.reveal('at least five') if i==0 else t.reveal('Every integer',.7,offset=.17*i)
            tab(a,x,242,str(aa),GREEN,op);tab(a,x,389,str(bb),RED,op)
        text(a,'B = 13 − A',368,569,36,INK,t.reveal('thirteen minus A'))
        text(a,'5 ≤ A ≤ 8 · 4 ordered pairs',901,569,34,GREEN,t.reveal('for four pairs'))
    elif number==5:
        for j,key in enumerate(('A','B','C')):
            x=98+j*371;drawer(a,x,158,339,272);text(a,key,x+169,222,46,GREEN)
            text(a,'1 to 6',x+169,320,37,INK,t.reveal('one and six'))
            if j==0:text(a,'even',x+169,379,28,RED,t.reveal('an even number'))
        for j in range(11):a.dot(252+j*78,508,20,GOLD,t.reveal('eleven tokens',1,offset=.04*j))
        text(a,'A + B + C = 11',640,575,37,INK,t.reveal('eleven tokens'))
    elif number in (6,7):
        drawer(a,83,144,1114,391)
        for x,label in [(181,'A'),(389,'B + C'),(727,'Possible values of B'),(1051,'Count')]:text(a,label,x,191,29,GREEN)
        for j,(aval,bc,bs,count) in enumerate(((2,9,'3, 4, 5, 6',4),(4,7,'1, 2, 3, 4, 5, 6',6),(6,5,'1, 2, 3, 4',4))):
            y=264+j*94
            a.line([(117,y+45),(1162,y+45)],RULE,2)
            text(a,str(aval),181,y,38,GREEN,t.reveal(('two','four','six')[j]) if number==6 else 1)
            text(a,str(bc),389,y,38,INK,t.reveal('eleven minus A') if number==6 else 1)
            if number==6:
                lower=(3,1,1)[j]; upper=(8,6,4)[j]
                limit=t.reveal('cap of six on B',.7,offset=.22*j)
                partial=f'{lower} ≤ B' if t.reveal('upper bound')<.5 else f'{lower} ≤ B ≤ {upper}'
                text(a,partial,728,y,32,GREEN,t.reveal('lower bound',.7,offset=.15*j)*(1-limit))
                text(a,bs,728,y,32,INK,limit)
            else:
                text(a,bs,728,y,32,INK)
            text(a,str(count),1050,y,40,RED,t.reveal('count the range',.7,offset=.18*j) if number==6 else t.reveal('four, six and four',.7,offset=.18*j))
        if number==6:text(a,'C = 11 − A − B, with 1 ≤ B, C ≤ 6',640,569,35,INK,t.reveal('upper bound'))
        else:text(a,'4 + 6 + 4 = 14 ordered triples',640,569,40,GREEN,t.reveal('fourteen triples'))
    else:
        drawer(a,78,151,1124,365)
        text(a,'Each load totals 10 kg',640,209,37,INK,t.reveal('ten kilograms'))
        open_case=1-t.reveal('The pairs are',.6)
        left_label='?' if t.reveal('starts at two')<.5 else '2–5' if t.reveal('ends at five')>.5 else '≥ 2'
        parcel(a,432,291,left_label,open_case);parcel(a,734,291,'?',open_case)
        text(a,'+',631,326,43,GREEN,open_case)
        text(a,'Lighter first',481,425,28,GREEN,t.reveal('lighter weight first')*open_case)
        text(a,'At most 8 kg',783,425,28,RED,t.reveal('cannot exceed eight')*open_case)
        for j,(left,right,cue) in enumerate(((2,8,'two and eight'),(3,7,'three and seven'),(4,6,'four and six'),(5,5,'five and five'))):
            x=123+j*270;op=t.reveal(cue)
            parcel(a,x,294,left,op);parcel(a,x+107,294,right,op)
            text(a,f'{left} + {right}',x+102,423,29,GREEN,op)
        text(a,'2 ≤ lighter weight ≤ 5',355,566,34,GREEN,t.reveal('ends at five'))
        text(a,'4 loads, including 5 + 5',917,566,34,RED,t.reveal('Four loads'))


def poster(draw):
    return draw(8,1.5)
