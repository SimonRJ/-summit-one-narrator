"""S097. A two-row workshop proves forced placements, separation and seam parity."""
BACKGROUND=('#faf0d3','#e1c99c')
BRIDGE='Trace the seam between columns three and four. If just one domino crossed it, how many cells would still need covering on the left?'
INK='#334237';BLUE='#35628c';JADE='#327364';CLAY='#ae553a';PAPER='#fff8e6';EDGE='#927d60';GOLD='#e1af5a';CORK='#dbbf92'
TITLES=['Start at a notched corner','Fit the three forced pieces','Work around a glued domino',
        'Count the three remaining patterns','Require a crossing at the seam','Prove why a second crossing is forced',
        'Multiply the choices in the two rooms','Keep upright dominoes apart']


def all_tilings(width,missing=()):
    cells={(r,c) for r in range(2) for c in range(width)}-set(missing)
    def cover(open_cells):
        if not open_cells:
            yield ()
            return
        r,c=min(open_cells)
        for other in [(r,c+1),(r+1,c)]:
            if other in open_cells:
                domino=((r,c),other)
                for tail in cover(open_cells-set(domino)):yield (domino,)+tail
    return list(cover(cells))


def check_maths():
    assert len(all_tilings(4,[(0,0),(0,3)]))==1
    assert sum(((0,1),(1,1)) in arrangement for arrangement in all_tilings(5))==3
    crosses=[sum(a[1]==2 and b[1]==3 for a,b in layout) for layout in all_tilings(6)]
    assert crosses.count(1)==0 and crosses.count(2)==4
    solutions=[]
    for layout in all_tilings(7):
        vertical=sorted(a[1] for a,b in layout if a[1]==b[1])
        if len(vertical)==3 and all(b-a>1 for a,b in zip(vertical,vertical[1:])):solutions.append(vertical)
    assert solutions==[[0,3,6]]


def text(a,s,x,y,size=33,col=INK,op=1):
    a.text(s,x,y,size,col,bold=True,opacity=op)


def grid(a,x,y,cols,s):
    for r in range(2):
        for c in range(cols):a.box(x+c*s,y+r*s,s,s,fill=PAPER,edge=EDGE,radius=2,stroke=2)


def tile(a,x,y,s,upright,op=1,col=None):
    w,h=(s,2*s) if upright else (2*s,s)
    colour=col or (BLUE if upright else JADE)
    a.box(x+3,y+3,w-6,h-6,fill=colour,edge=INK,stroke=2,radius=max(4,s*.11),opacity=op)
    for cx,cy in ([(x+s/2,y+s/2),(x+s/2,y+1.5*s)] if upright else [(x+s/2,y+s/2),(x+1.5*s,y+s/2)]):
        a.dot(cx,cy,max(3,s*.075),PAPER,op)


def notches(a,x,y,s,op=1):
    for c in (0,3):
        cx=x+c*s;a.box(cx+1,y+1,s-2,s-2,fill=CORK,edge=CLAY,radius=2,opacity=op)
        a.line([(cx+14,y+14),(cx+s-14,y+s-14)],CLAY,3,op)
        a.line([(cx+s-14,y+14),(cx+14,y+s-14)],CLAY,3,op)


def pair(a,x,y,s,op=1,col=None):
    tile(a,x,y,s,False,op,col);tile(a,x,y+s,s,False,op,col)


def room(a,x,y,s,vertical,op=1):
    if vertical:
        tile(a,x,y,s,True,op);tile(a,x+s,y,s,True,op)
    else:pair(a,x,y,s,op)


def pin(a,x,y,s,op=1):
    tile(a,x,y,s,True,op,CLAY)
    a.dot(x+s/2,y+s,s*.11,PAPER,op);a.line([(x+s*.44,y+s),(x+s*.56,y+s)],INK,3,op)


def seam(a,x,y,s):
    a.dashed((x,y-27),(x,y+2*s+28),CLAY,4,11,6)


def draw(a,n,t):
    a.label(TITLES[n-1],76,73,43,INK,bold=True);a.line([(76,119),(1201,119)],EDGE,3)
    if n in (1,2):
        x,y,s=369,205,133;grid(a,x,y,4,s)
        notches(a,x,y,s,t.reveal('first and last squares') if n==1 else 1)
        if n==1:
            text(a,'?',x+s/2,y+1.5*s,58,CLAY,t.reveal('bottom left corner'))
            text(a,'Which neighbour shares an edge?',640,562,37,INK,t.reveal('Which way'))
        else:
            tile(a,x,y+s,s,False,t.reveal('must point right',.85))
            tile(a,x+2*s,y+s,s,False,t.reveal('must point left',.85))
            tile(a,x+s,y,s,False,t.reveal('last horizontal domino',.85),BLUE)
            text(a,'3 forced placements → 1 tiling',640,566,39,JADE,t.reveal('Every placement'))
    elif n==3:
        x,y,s=341,209,111;grid(a,x,y,5,s)
        for c in range(5):text(a,str(c+1),x+(c+.5)*s,y-29,22,EDGE)
        pin(a,x+s,y,s,t.reveal('glued into the second column'))
        text(a,'Fixed',x+1.5*s,y+2*s+43,28,CLAY,t.reveal('must stay there'))
        text(a,'How many completions?',640,565,39,INK,t.reveal('How many ways'))
    elif n==4:
        x,y,s=103,260,70;grid(a,x,y,5,s);pin(a,x+s,y,s)
        tile(a,x,y,s,True,t.reveal('needs one upright domino'))
        text(a,'The left is forced',300,472,28,INK)
        for i,(seq,cue) in enumerate([('VVV','three upright dominoes'),('HV','pair before one'),('VH','pair after it')]):
            x0=549+i*223;s0=57;grid(a,x0,275,3,s0);c=0
            for ch in seq:
                op=t.reveal(cue)
                if ch=='V':tile(a,x0+c*s0,275,s0,True,op);c+=1
                else:pair(a,x0+c*s0,275,s0,op);c+=2
            text(a,str(i+1),x0+1.5*s0,453,31,JADE,t.reveal(cue))
        text(a,'1 choice on the left × 3 on the right = 3 tilings',640,566,35,JADE,t.reveal('only patterns'))
    elif n in (5,6):
        x,y,s=322,216,105;grid(a,x,y,6,s)
        for c in range(6):text(a,str(c+1),x+(c+.5)*s,y-32,22,EDGE)
        seam(a,x+3*s,y,s)
        if n==5:
            tile(a,x+2*s,y,s,False,t.reveal('one domino crosses'),CLAY)
            text(a,'Can exactly one domino cross?',640,557,39,CLAY,t.reveal('Could exactly one'))
        else:
            tile(a,x+2*s,y,s,False,1,CLAY)
            forced=t.reveal('lower domino must cross',.9)
            for j,(r,c) in enumerate([(0,0),(0,1),(1,0),(1,1),(1,2)]):
                op=t.reveal('Five cells would still')*(1-forced)
                text(a,str(j+1),x+(c+.5)*s,y+(r+.5)*s,38,BLUE,op)
            tile(a,x+2*s,y+s,s,False,forced,CLAY)
            text(a,'6 − 1 = 5 cells',640,493,35,INK,t.reveal('Five cells would still')*(1-forced))
            text(a,'Left room',x+s,y+2*s+45,29,JADE,forced);text(a,'Right room',x+5*s,y+2*s+45,29,JADE,forced)
            text(a,'Both crossings are forced',640,569,37,CLAY,forced)
    elif n==7:
        for j,(left,right) in enumerate([(True,True),(True,False),(False,True),(False,False)]):
            x=180+(j%2)*549;y=160+(j//2)*175;s=57
            grid(a,x,y,6,s);pair(a,x+2*s,y,s,col=CLAY)
            op=t.reveal('two upright dominoes' if j==0 else 'two horizontal dominoes' if j==1 else 'Either choice on the left',.8,offset=.18*(j-1) if j>1 else 0)
            room(a,x,y,s,left,op);room(a,x+4*s,y,s,right,op)
            text(a,' '.join(['Upright' if left else 'Horizontal','/','Upright' if right else 'Horizontal']),x+3*s,y+2*s+27,22,INK,op)
        text(a,'2 left choices × 2 right choices = 4',640,565,37,JADE,t.reveal('Two times two'))
    else:
        x,y,s=255,230,109;grid(a,x,y,7,s)
        for c in range(7):text(a,str(c+1),x+(c+.5)*s,y-30,20,EDGE)
        for c in (1,4):pair(a,x+c*s,y,s,t.reveal('Lay down those two pairs',1.0))
        gap=t.reveal('There are three gaps',.8);fill=t.reveal('All three gaps must be filled',1.05)
        for j,c in enumerate((0,3,6)):
            text(a,'?',x+(c+.5)*s,y+s,40,CLAY,gap*(1-fill))
            tile(a,x+c*s,y,s,True,t.reveal('All three gaps must be filled',.6,offset=j*.2))
        text(a,'No neighbouring upright dominoes',640,505,29,INK,t.reveal('no two in neighbouring columns'))
        text(a,'3 gaps, 3 upright dominoes → 1 tiling',640,571,36,JADE,t.reveal('exactly one tiling'))


def poster(draw):
    return draw(9,1.5)
