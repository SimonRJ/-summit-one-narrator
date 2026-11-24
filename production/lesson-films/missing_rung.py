"""A beetle's ladder and its landing log for the missing-rung study."""
from math import pi, sin
from stage import blend, clamp, mix

BACKGROUND = ('#123b39', '#11262e')
PAPER, JADE, HONEY, CORAL = '#fbefd6', '#90e0c0', '#ffd276', '#ff9c8e'
STEEL, WOOD, INK = '#739b94', '#ce9f6a', '#183d40'
BRIDGE = 'Pause when the film marks rung 3 as broken. Is rung 4 still reachable? Trace its possible final jumps before the film fills in the table.'
HEADINGS = ('The landing log', 'Sort the final jumps', 'Strike out a landing', 'Jump over the gap',
            'Build the landing log', 'The brass bell', 'Pair the pieces', 'Add arrivals, multiply choices')


def paths(landing, broken=()):
    if landing < 0 or landing in broken:
        return []
    if landing == 0:
        return [(0,)]
    return [p + (landing,) for jump in (1, 2) for p in paths(landing-jump, broken)]


def check_maths():
    assert len(paths(2)) == 2 and len(paths(3)) == 3
    assert [len(paths(n, (3,))) for n in range(9)] == [1,1,2,0,2,2,4,6,10]
    through = {p for p in paths(8,(3,)) if 5 in p}
    joined = {a + tuple(5+x for x in b[1:]) for a in paths(5,(3,)) for b in paths(3)}
    assert joined == through and len(through) == 6


def beetle(a,x,y,scale=1):
    for side in (-1,1):
        for h in (-5,2,9):
            a.line([(x+side*4*scale,y+h*scale),(x+side*12*scale,y+(h+3)*scale)],PAPER,2)
    a.dot(x,y-6*scale,5*scale,INK)
    a.dot(x,y,8*scale,CORAL)
    a.line([(x,y-6*scale),(x,y+7*scale)],INK,2)
    for side in (-1,1):
        a.dot(x+side*3.2*scale,y-1.5*scale,1.5*scale,INK)


def bell(a,x,y,t=1):
    if t <= 0: return
    a.dot(x,y+8,6,HONEY,t)
    a.box(x-10,y-9,20,18,radius=8,fill=HONEY,opacity=t)
    a.line([(x-13,y+8),(x+13,y+8)],HONEY,4,t)
    a.line([(x,y-9),(x,y-18)],HONEY,3,t)


def ladder(a, top, broken=0, has_bell=0):
    x,y,dy=291,550,min(163,383/top)
    a.line([(x-58,y+4),(x-58,y-top*dy-28)],WOOD,8)
    a.line([(x+58,y+4),(x+58,y-top*dy-28)],WOOD,8)
    for i in range(top+1):
        row=y-i*dy
        a.label('ground' if i==0 else str(i),193,row,25,PAPER,align='right',bold=True)
        if i==3 and broken:
            gap=33*broken
            a.line([(x-57,row),(x-gap,row)],WOOD,8)
            a.line([(x+gap,row),(x+57,row)],WOOD,8)
            a.line([(x-10,row-9),(x+10,row+9)],CORAL,3,broken)
            a.line([(x+10,row-9),(x-10,row+9)],CORAL,3,broken)
        else:
            a.line([(x-58,row),(x+58,row)],WOOD,8)
        if i==5: bell(a,x-34,row-14,has_bell)
    return x,y,dy


def trace(a, geometry, route, t, colour, lane=0, insect=False):
    """An arc has exactly the landings written on its route ticket."""
    if t<=0:return
    x,y,dy=geometry
    travel=clamp(t)*(len(route)-1)
    end=None
    for k,(src,dst) in enumerate(zip(route,route[1:])):
        f=clamp(travel-k)
        if not f:break
        arc=44 if dst-src==1 else 81
        def point(u):
            return (x+lane+arc*sin(pi*u),y-mix(src,dst,u)*dy-10)
        points=[point(f*i/20) for i in range(21)]
        a.line(points,colour,4)
        a.dot(*points[0],5,colour)
        end=points[-1]
        if f>=.999:a.dot(*end,5,colour)
    if insect and end:beetle(a,*end)


def label(a,x,y,text,colour=PAPER,size=36,t=1):
    a.label(text,x,y,size,colour,t,bold=True)


def row(a,y,steps,colour,t):
    if t<=0:return
    xs=[566+66*i for i in range(len(steps))]
    for i,(x,digit) in enumerate(zip(xs,steps)):
        if i:a.line([(xs[i-1]+20,y),(x-20,y)],colour,3,t)
        a.dot(x,y,19,blend(INK,colour,.24),t)
        a.text(str(digit),x,y,27,colour,bold=True,opacity=t)


def note(a,text,t=1):
    label(a,496,538,text,HONEY,32,t)


def draw(a,n,c):
    label(a,70,69,HEADINGS[n-1],PAPER,46)
    a.line([(70,115),(1210,115)],STEEL,2,.65)
    if n==1:
        g=ladder(a,2)
        first=c.reveal('jump straight there',1)
        second=c.reveal('visit rung one first',1.6)
        trace(a,g,(0,2),first,HONEY,-20,True)
        trace(a,g,(0,1,2),second,JADE,12,True)
        label(a,510,205,'Where did it land?',size=36)
        row(a,319,(0,2),HONEY,first);row(a,402,(0,1,2),JADE,second)
    elif n==2:
        g=ladder(a,3)
        q=c.reveal('from rung two',1.1);r=c.reveal('single route',1.1)
        trace(a,g,(2,3),q,JADE,-22,True);trace(a,g,(1,3),r,HONEY,18,True)
        label(a,505,192,'Last jump into 3',size=35)
        row(a,282,(0,2,3),JADE,q);row(a,357,(0,1,2,3),JADE,q)
        row(a,432,(0,1,3),HONEY,r)
        note(a,'2 + 1 = 3 routes',c.reveal('makes three'))
    elif n==3:
        broken=c.reveal('third rung breaks',1)
        g=ladder(a,4,broken)
        beetle(a,g[0],g[1]-12)
        label(a,500,241,'One- or two-rung jumps',size=38)
        label(a,500,345,'Can it land on 4?',HONEY,42,c.reveal('rung four'))
    elif n==4:
        g=ladder(a,4,1)
        label(a,510,178,'Two ways to reach rung 2',size=36)
        q=c.reveal('Both routes',2.4)
        r=c.reveal('different beginnings',2.4)
        trace(a,g,(0,2,4),q,HONEY,-25,True)
        trace(a,g,(0,1,2,4),r,JADE,10,True)
        row(a,284,(0,2,4),HONEY,q);row(a,368,(0,1,2,4),JADE,r)
        note(a,'2 + 0 = 2 routes to rung 4',c.reveal('two routes beside four'))
    elif n==5:
        g=ladder(a,8,1)
        label(a,495,151,'Routes to each rung',size=36)
        log=[1,1,2,0,2,2,4,6,10]
        cues={5:'rung five',6:'At six',7:'At seven',8:'At eight'}
        for i,count in enumerate(log):
            t=c.reveal(cues[i],.55) if i in cues else 1
            if t>0:label(a,g[0]+91,g[1]-i*g[2],str(count),CORAL if i==3 else JADE,31,t)
        for j,(result,cue) in enumerate([('5    2 + 0 = 2','rung five'),('6    2 + 2 = 4','At six'),
                                        ('7    4 + 2 = 6','At seven'),('8    6 + 4 = 10','At eight')]):
            label(a,512,234+69*j,'Rung '+result,JADE if j<3 else HONEY,35,c.reveal(cue))
    elif n==6:
        g=ladder(a,8,1,c.reveal('brass bell'))
        a.dashed((387,g[1]-5*g[2]),(1110,g[1]-5*g[2]),HONEY,width=2,fraction=c.reveal('cutting'))
        label(a,513,210,'From the bell to 8',HONEY,36,c.reveal('two pieces'))
        label(a,513,462,'From the ground to the bell',JADE,35,c.reveal('two pieces'))
    elif n==7:
        label(a,72,161,'Arrivals at rung 5',JADE,32)
        label(a,475,161,'Final three rungs: jump sizes',HONEY,32)
        for j,seq in enumerate(('1 + 1 + 1','1 + 2','2 + 1')):
            x=520+236*j
            t=c.reveal(('three singles','single followed','double followed')[j])
            label(a,x,239,seq,HONEY,31,t)
        for i,begin in enumerate(('0 → 2 → 4 → 5','0 → 1 → 2 → 4 → 5')):
            y=339+85*i
            label(a,74,y,begin,JADE,29,c.reveal('Two routes'))
            for j in range(3):
                t=c.reveal('Each beginning',.95,offset=(i*3+j)*.13)
                x=570+236*j
                a.dot(x,y,13,JADE,t)
        label(a,435,545,'2 × 3 = 6 bell routes',PAPER,40,c.reveal('Two groups of three'))
    else:
        label(a,93,175,'Last jump',JADE,34)
        label(a,680,175,'Compulsory stop',HONEY,34)
        a.line([(631,150),(631,492)],STEEL,2)
        fall=c.reveal('separate piles')
        label(a,93,290,'From 7: 6 ways',PAPER,32,fall)
        label(a,93,362,'From 6: 4 ways',PAPER,32,fall)
        label(a,93,447,'6 + 4 = 10',JADE,42,fall)
        join=c.reveal('each beginning')
        label(a,680,290,'2 beginnings',PAPER,32,join)
        label(a,680,362,'3 endings',PAPER,32,join)
        label(a,680,447,'2 × 3 = 6',HONEY,42,join)
        label(a,93,555,'A broken rung gets a zero.',CORAL,30,c.reveal('Keep a zero'))


def poster(draw):
    return draw(1.4,1)
