"""Each drawn deck and cover is an explicit set of edge-neighbouring squares."""
from functools import lru_cache
from itertools import product
from math import cos, pi, sin

from stage import blend, clamp, mix

BACKGROUND = ('#183641', '#10242c')
PAPER, GILT, ICE, METAL, RIM, RED = '#f8edde', '#e4a854', '#a8d5e5', '#607a80', '#a0b3af', '#ff8978'
BRIDGE = 'Follow the two ends of one plate. Watch what happens when both tips of the narrow deck need the same neighbour.'
FULL = frozenset(product(range(4), repeat=2))
SMALL = frozenset(product(range(3), range(2)))
PINCH = frozenset({(0,0),(1,0),(2,0),(1,1),(1,2),(0,3),(1,3),(2,3)})
DIAGONAL = {(0,0),(3,3)}
TOP = {(0,0),(3,0)}
CONSTRUCTION = [((1,0),(2,0))] + [((x,y),(x+1,y)) for y in (1,2,3) for x in (0,2)]


def adjacent(a,b):
    return sum(abs(x-y) for x,y in zip(a,b)) == 1


@lru_cache(None)
def coverings(cells):
    if not cells:
        return 1
    tip = min(cells)
    return sum(coverings(cells-{tip,neighbour}) for neighbour in cells if adjacent(tip,neighbour))


def check_maths():
    def count_colours(cells):
        return tuple(sum((x+y)%2 == tint for x,y in cells) for tint in (0,1))
    assert coverings(SMALL)==3
    assert count_colours(FULL)==(8,8)
    assert count_colours(FULL-DIAGONAL)==(6,8) and coverings(FULL-DIAGONAL)==0
    assert count_colours(FULL-TOP)==(7,7) and coverings(FULL-TOP)>0
    assert all(adjacent(a,b) for a,b in CONSTRUCTION)
    plated=[c for pair in CONSTRUCTION for c in pair]
    assert len(plated)==len(set(plated))==14 and set(plated)==FULL-TOP
    assert count_colours(PINCH)==(4,4) and coverings(PINCH)==0
    assert all({p for p in PINCH if adjacent(tip,p)}=={(1,0)} for tip in [(0,0),(2,0)])


def mark(art,x,y,tint,r,colour,base):
    art.dot(x,y,r,colour)
    if tint:
        art.dot(x,y,r*.58,base)


def grid(art,cells,origin,size,colour=1,removed=()):
    ox,oy=origin
    for x,y in sorted(cells):
        left,top=ox+x*size,oy+y*size
        tint=(x+y)%2
        solid=blend(METAL,(GILT,ICE)[tint],colour*.79)
        if (x,y) in removed:
            art.box(left+1,top+1,size-2,size-2,radius=3,fill='#102832',edge='#53727d',stroke=2)
            for i in range(3):
                start=i*size/3.6
                art.line([(left+7+start,top+size-8),(left+size-8,top+7+start)],'#3f5961',2)
            continue
        art.box(left+1,top+1,size-2,size-2,radius=4,fill=solid,edge='#243b42',stroke=2)
        if colour>0:
            mark(art,left+size/2,top+size/2,tint,size*.12,blend(solid,'#253c43',colour),solid)


def plate(art,x,y,size,angle,grow=1):
    """One rotating rectangular two-cell plate, coordinates anchored at the first cell centre."""
    if grow<=0:return
    ux,uy=cos(angle),sin(angle)
    height=(.43*size)*clamp(grow*2)
    def at(a,b):
        return (x+ux*a-uy*b,y+uy*a+ux*b)
    left,right=-.43*size,(-.43+1.86*grow)*size
    outline=[at(left,-height),at(right,-height),at(right,height),at(left,height)]
    art.polygon(outline,'#547783','#d7ebdf',3)
    if grow>.32:
        art.line([at(-.28*size,-.29*size),at(min(right-.07*size,1.27*size),.29*size)],'#8ba8aa',3)
    for end in (0,1):
        if end*size < right-.09*size:
            ax,ay=at(end*size,0)
            art.dot(ax,ay,.105*size,'#d8e5da')
            art.dot(ax,ay,.048*size,'#334e58')


def place(art,pair,origin,size,t):
    (x,y),(u,v)=pair
    assert (u-x,v-y) in ((1,0),(0,1))
    px,py=origin
    plate(art,px+(x+.5)*size,py+(y+.5)*size,size,0 if y==v else pi/2,t)


def note(art,x,y,text,colour=PAPER,size=34,amount=1):
    art.label(text,x,y,size,colour,amount,bold=True)


def key(art,x,y,tint,n):
    mark(art,x,y,tint,16,(GILT,ICE)[tint],BACKGROUND[1])
    note(art,x+34,y,str(n),size=41)


def draw(art,n,c):
    # Riveted top rail and water lines identify these as plan drawings of bridge decks.
    art.line([(60,45),(1210,45)],'#729296',2)
    for x in (60,1210):art.dot(x,45,5,METAL)
    titles=['Which way can a plate turn?','A mark on each end','Inspect two corners','Can seven plates balance?',
            'Move one opening','Four dots and four rings','Both tips need the same socket','Two ways to finish a proof']
    note(art,65,91,titles[n-1],size=43)
    art.line([(67,598),(1213,598)],'#3b5f67',2)
    if n in (1,2):
        origin,size=(113,199),133
        colour=0 if n==1 else c.reveal('paint neighbouring squares',1.4)
        grid(art,SMALL,origin,size,colour)
        if n==1:
            t=c.reveal('turning a plate',1.35)
            plate(art,origin[0]+size/2,origin[1]+size/2,size,t*pi/2,c.reveal('each plate',1))
            note(art,650,285,'Two squares',ICE,38,c.reveal('two squares'))
            note(art,650,362,'One shared edge',GILT,34,c.reveal('share an edge'))
        else:
            t=c.reveal('turn it upright',1)
            first=c.reveal('a horizontal plate',1)
            plate(art,origin[0]+size/2,origin[1]+size/2,size,t*pi/2,first)
            deck=c.reveal('three upright plates',2)
            for i in (1,2):
                place(art,((i,0),(i,1)),origin,size,clamp(deck*2-(i-1)))
            note(art,650,300,'1 dot + 1 ring',PAPER,41,first)
            note(art,650,376,'3 plates fit',ICE,33,deck)
        return
    origin,size=(129,172),95
    if n in (3,4,5):
        removed=set()
        if n==3:
            if c.reveal('top left')>0:removed.add((0,0))
            if c.reveal('bottom right')>0:removed.add((3,3))
        elif n==4:removed=DIAGONAL if c.reveal('both missing corners')>0 else set()
        else:
            moved=c.reveal('top right corner',1)
            removed=TOP if moved>=1 else DIAGONAL
            if 0<moved<1:
                art.arrow((505,509),(505,222),ICE,moved,4)
        grid(art,FULL,origin,size,0 if n==3 else 1,removed=removed)
        if n==3:
            note(art,685,271,'16 − 2 = 14',PAPER,43,c.reveal('fourteen squares'))
            note(art,685,359,'14 ÷ 2 = 7',ICE,40,c.reveal('seven plates'))
        elif n==4:
            first=c.reveal('eight dots'); change=c.reveal('both missing corners')
            if first:
                key(art,712,265,0,6 if change else 8)
                key(art,924,265,1,8)
            note(art,680,361,'Seven plates need 7 + 7',PAPER,31,c.reveal('would need seven'))
            note(art,680,432,'Covering impossible',RED,38,c.reveal('one colour runs out'))
        else:
            first=c.reveal('cover the middle two',1.05)
            others=c.reveal('two horizontal plates',2.5)
            for i,pair in enumerate(CONSTRUCTION):
                place(art,pair,origin,size,first if i==0 else clamp(6*others-i+1))
            note(art,680,279,'7 dots + 7 rings',PAPER,40,c.reveal('the counts balance'))
            note(art,680,364,'1 + 2 + 2 + 2 = 7',ICE,35,others)
    elif n in (6,7):
        x,y=origin
        origin=(x+65,y)
        grid(art,PINCH,origin,size)
        if n==6:
            note(art,676,272,'3 + 1 + 1 + 3 = 8',PAPER,37,c.reveal('then three squares'))
            if c.reveal('four dots and four rings'):
                key(art,713,369,0,4);key(art,921,369,1,4)
        else:
            used=c.reveal('uses up the middle square',1.2)
            place(art,((0,0),(1,0)),origin,size,used)
            px,py=origin
            if (t:=c.reveal('upper right tip',1)):
                art.arrow((px+2.5*size,py+.5*size),(px+1.68*size,py+.5*size),RED,t,7)
            note(art,674,264,'Left tip → middle',PAPER,36,c.reveal('upper left tip'))
            note(art,674,338,'Right tip → middle',RED,36,c.reveal('exactly the same neighbour'))
            note(art,674,439,'One square cannot serve both',ICE,29,c.reveal('cannot both use'))
    else:
        first=(129,233);second=(711,233);sz=69
        grid(art,FULL,first,sz,removed=DIAGONAL)
        note(art,125,188,'Rule it out',RED,32)
        note(art,125,554,'6 dots ≠ 8 rings',PAPER,28,c.reveal('unequal totals'))
        grid(art,FULL,second,sz,removed=TOP)
        note(art,707,188,'Build a covering',ICE,32)
        t=c.reveal('show a placement',2)
        for i,pair in enumerate(CONSTRUCTION):
            place(art,pair,second,sz,clamp(7*t-i))
        note(art,707,554,'7 plates cover every cell',PAPER,27,t)


def poster(draw):
    return draw(7,1.5)
