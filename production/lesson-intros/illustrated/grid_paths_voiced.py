"""Word-cued lattice walks, closed intersections and a required checkpoint for S093."""
from itertools import combinations
from math import comb, hypot

from captioned_film import mix

PAPER, INK, SOFT = '#102833', '#f8f8ec', '#c1d2d4'
GRID, TEAL, GOLD, RED, BLUE = '#537075', '#74e3d5', '#ffcf84', '#ffa7a1', '#a9ceff'
BLOCKED = ((2, 2), (3, 3))


def counts(w, h, blocked=(), closed_edges=()):
    totals = {}
    for y in range(h + 1):
        for x in range(w + 1):
            point = x, y
            incoming = ((x-1, y), (x, y-1))
            totals[point] = 0 if point in blocked else 1 if point == (0, 0) else sum(
                totals.get(p, 0) for p in incoming if (p, point) not in closed_edges)
    return totals


def verify():
    for w,h,blocked,answer in ((2,1,(),3),(3,2,(),10),(5,4,BLOCKED,42)):
        dp = counts(w,h,blocked)
        last = [0,0]
        for ups in combinations(range(w+h),h):
            x = y = 0
            for i in range(w+h):
                if i in ups: y += 1
                else: x += 1
                if (x,y) in blocked: break
            else: last[int(i in ups)] += 1
        assert sum(last) == dp[w,h] == answer
        assert last == [dp[w-1,h], dp[w,h-1]]
    assert counts(5,4,BLOCKED)[4,4] == 18 and counts(5,4,BLOCKED)[5,3] == 24
    assert comb(9,4) - comb(4,2)*comb(5,2) - comb(6,3)*3 + comb(4,2)*2*3 == 42


def heading(c, text):
    c.text(text,55,55,42,INK,'lm',True)


def caption(c,text,y,colour=INK):
    c.text(text,895,y,32,colour,bold=True)


class Grid:
    def __init__(self,c,w,h,x=133,y=466,step=None):
        self.c,self.w,self.h,self.x,self.y = c,w,h,x,y
        self.step = step or min(110,344/max(h,1),488/max(w,1))

    def pos(self,p):
        return self.x + self.step*p[0], self.y - self.step*p[1]

    def base(self,axes=True):
        for x in range(self.w+1):
            self.c.line([self.pos((x,0)),self.pos((x,self.h))],GRID,3)
            if axes:self.c.text(x,self.pos((x,0))[0],self.y+42,24,SOFT)
        for y in range(self.h+1):
            self.c.line([self.pos((0,y)),self.pos((self.w,y))],GRID,3)
            if axes:self.c.text(y,self.x-42,self.pos((0,y))[1],24,SOFT)
        for x in range(self.w+1):
            for y in range(self.h+1):self.c.dot(*self.pos((x,y)),4,SOFT)

    def value(self,p,v,colour=TEAL,r=20):
        x,y=self.pos(p)
        self.c.dot(x,y,r+2,colour)
        self.c.dot(x,y,r,PAPER)
        self.c.text(v,x,y,round(r*1.3),colour,bold=True)

    def barrier(self,p,zero=False):
        x,y=self.pos(p)
        if zero:
            self.value(p,'0',RED)
        else:
            self.c.dot(x,y,14,PAPER)
            self.c.line([(x-10,y-10),(x+10,y+10)],RED,5)
            self.c.line([(x-10,y+10),(x+10,y-10)],RED,5)

    def arrow(self,a,b,v=1,col=GOLD):
        if v<=0:return
        x,y=self.pos(a);xx,yy=self.pos(b)
        dx,dy=xx-x,yy-y;length=hypot(dx,dy);u,z=dx/length,dy/length
        start=(x+21*u,y+21*z);tip=(mix(start[0],xx-22*u,v),mix(start[1],yy-22*z,v))
        self.c.line([start,tip],col,5)
        if v>.18:
            self.c.poly([tip,(tip[0]-11*u-5*z,tip[1]-11*z+5*u),(tip[0]-11*u+5*z,tip[1]-11*z-5*u)],col,None)

    def path(self,moves,v,col):
        x=y=0
        for i,step in enumerate(moves):
            nx=x+(step=='R');ny=y+(step=='U')
            a=self.pos((x,y));b=self.pos((nx,ny));p=max(0,min(1,v*len(moves)-i))
            if p:self.c.line([a,(mix(a[0],b[0],p),mix(a[1],b[1],p))],col,8)
            x,y=nx,ny

    def fill(self,table,points,progress=1):
        for p in list(points)[:round(progress*len(points))]:
            self.value(p,table[p],RED if not table[p] else TEAL)


def opening(c,q):
    heading(c,'Count the possible last steps')
    g=Grid(c,2,1,167,406,157);g.base()
    g.value((2,1),'?',GOLD)
    if q.after('from the left'):
        g.value((1,1),2,BLUE);g.arrow((1,1),(2,1),q.after('from the left'),BLUE)
        caption(c,'2 routes from the left',233,BLUE)
    if q.after('from below'):
        g.value((2,0),1,GOLD);g.arrow((2,0),(2,1),q.after('from below'),GOLD)
        caption(c,'1 route from below',304,GOLD)
    if q.after('add the route totals'):
        g.value((2,1),3);caption(c,'2 + 1 = 3',417,TEAL)


def exam_cues(c,q):
    heading(c,'Read the permitted moves')
    g=Grid(c,3,2);g.base()
    if q.after('shortest routes'):
        if not q.after('block intersections'):
            g.path('RURUR',q.after('shortest routes',1.6),TEAL)
        elif q.after('available incoming totals'):
            g.path('RRRUU',q.after('available incoming totals',1.15),BLUE)
        caption(c,'3 right steps + 2 up steps',212,TEAL)
    if q.after('allowed directions'):
        caption(c,'A shortest walk has 5 steps',287)
    if q.after('block intersections'):
        g.barrier((1,1));caption(c,'Closed intersection (1, 1)',378,RED)
    if q.after('put zero'):
        g.barrier((1,1),True);caption(c,'Enter 0 here',456,RED)


def easy_question(c,q):
    heading(c,'Easy · Walk from (0, 0) to (2, 1)')
    g=Grid(c,2,1,152,405,166);g.base()
    g.value((0,0),'S',TEAL);g.value((2,1),'F',GOLD)
    if q.after('one step right'):g.arrow((0,0),(1,0),q.after('one step right'),TEAL)
    if q.after('one step up'):g.arrow((0,0),(0,1),q.after('one step up'),GOLD)
    if q.after('how many routes'):caption(c,'How many step sequences?',305)
    if q.after('sequence of steps'):caption(c,'Use R and U',411,TEAL)


def three_walks(c,q):
    heading(c,'Place the single up-step')
    for i,moves in enumerate(('URR','RUR','RRU')):
        left=99+390*i;g=Grid(c,2,1,left,378,119);g.base(False)
        c.text('Up-step '+str(i+1),left+119,176,30,SOFT,bold=True)
        p=q.after('any of the three step positions',1.05,delay=.72*i)
        g.path(moves,p,(TEAL,GOLD,BLUE)[i])
        if p:c.text('  '.join(moves),left+119,448,32,(TEAL,GOLD,BLUE)[i],bold=True)
    if q.after('there are three routes'):c.text('3 positions for U give 3 different routes',640,555,38,INK,bold=True)


def medium_question(c,q):
    heading(c,'Medium · Walk from (0, 0) to (3, 2)')
    g=Grid(c,3,2);g.base()
    g.value((3,2),'F',GOLD)
    if q.after('one-step move'):
        g.arrow((0,0),(1,0),q.after('one-step move'),TEAL)
        g.arrow((0,0),(0,1),q.after('one-step move'),GOLD)
    if q.after('starting total to one'):
        g.value((0,0),1);caption(c,'1 way to start',287,TEAL)
    if q.after('made no moves'):caption(c,'The empty walk counts',384)


def medium_solve(c,q):
    heading(c,'Add the left and lower totals')
    g=Grid(c,3,2);g.base();t=counts(3,2)
    edges=[p for p in t if min(p)==0]
    g.fill(t,edges,q.after('bottom edge',2.3))
    if q.after('one plus one'):
        g.arrow((0,1),(1,1),1,BLUE);g.arrow((1,0),(1,1),1,GOLD)
        g.value((1,1),2);caption(c,'At (1, 1)     1 + 1 = 2',224)
    interior=[p for p in t if min(p)>0 and p not in ((1,1),(3,2))]
    g.fill(t,interior,q.after('continue along each row',1.5))
    if q.after('six routes arrive'):
        g.value((2,2),6,BLUE);g.arrow((2,2),(3,2),q.after('six routes arrive'),BLUE)
        caption(c,'6 routes from the left',308,BLUE)
    if q.after('four arrive from below'):
        g.value((3,1),4,GOLD);g.arrow((3,1),(3,2),q.after('four arrive from below'),GOLD)
        caption(c,'4 routes from below',377,GOLD)
    if q.after('gives ten'):g.value((3,2),10);caption(c,'6 + 4 = 10',468,TEAL)


def hard_question(c,q):
    heading(c,'Hard · Avoid two closed intersections')
    g=Grid(c,5,4);g.base();g.value((0,0),'S');g.value((5,4),'F',GOLD)
    caption(c,'Start (0, 0)     Finish (5, 4)',213)
    if q.after('moving right or up'):caption(c,'Each move is right or up',293,BLUE)
    if q.after('two two'):g.barrier(BLOCKED[0]);caption(c,'Closed at (2, 2)',377,RED)
    if q.after('three three'):g.barrier(BLOCKED[1]);caption(c,'Closed at (3, 3)',440,RED)


def hard_solve(c,q):
    heading(c,'Fill the legal route totals')
    g=Grid(c,5,4);g.base();t=counts(5,4,BLOCKED)
    for p in BLOCKED:g.barrier(p,True)
    if q.after('starting at the bottom left'):g.value((0,0),1)
    cells=[p for p in t if p not in (*BLOCKED,(0,0),(5,4))]
    g.fill(t,cells,q.after('at every other point',4.0))
    if q.after('eighteen routes'):
        g.value((4,4),18,BLUE);g.arrow((4,4),(5,4),q.after('eighteen routes'),BLUE)
        caption(c,'From the left     18',265,BLUE)
    if q.after('twenty-four from below'):
        g.value((5,3),24,GOLD);g.arrow((5,3),(5,4),q.after('twenty-four from below'),GOLD)
        caption(c,'From below     24',342,GOLD)
    if q.after('total is forty-two'):g.value((5,4),42);caption(c,'18 + 24 = 42',445,TEAL)


def check_barriers(c,q):
    heading(c,'Check by counting the forbidden visits')
    g=Grid(c,5,4);g.base();g.value((0,0),'S');g.value((5,4),'F',GOLD)
    if q.after('unrestricted walks'):caption(c,'All walks     126',164)
    if q.after('six ways to the first crossing'):
        g.value(BLOCKED[0],'A',BLUE)
        a = '6' + (' × 10' if q.after('ten ways onward') else '') + (' = 60' if q.after('give sixty walks') else '')
        caption(c,'Through A     '+a,245,BLUE)
    if q.after('twenty ways'):
        g.value(BLOCKED[1],'B',GOLD)
        b = '20' + (' × 3' if q.after('three ways onward') else '') + (' = 60' if q.after('another sixty') else '')
        caption(c,'Through B     '+b,324,GOLD)
    if q.after('two between the crossings'):
        for p in ((2,3),(3,2)):
            g.arrow(BLOCKED[0],p,1,TEAL);g.arrow(p,BLOCKED[1],1,TEAL)
    if q.after('give thirty-six'):caption(c,'Both     6 × 2 × 3 = 36',405,TEAL)
    if q.after('add those back once'):
        c.text('126 − 60 − 60 + 36' + (' = 42' if q.after('leaves forty-two') else ''),640,564,41,INK,bold=True)


def mistakes(c,q):
    heading(c,'The start and the barriers have different jobs')
    g=Grid(c,3,2);g.base();g.value((0,0),1)
    if q.after('one way'):caption(c,'1 way to make no moves',222,TEAL)
    if q.after('using zero') and not q.after('a grid intersection'):
        for p in counts(3,2):g.value(p,0,RED)
        caption(c,'An incorrect 0 spreads',326,RED)
    if q.after('a grid intersection'):
        g.barrier((1,1));caption(c,'The closure is a point',326,RED)
    if q.after('surrounding unit squares'):
        g.path('RRRUU',q.after('surrounding unit squares',1.2),BLUE)
        caption(c,'Other edges stay open',422,BLUE)


def transfer(c,q):
    heading(c,'Choose the rule for the new grid')
    g=Grid(c,3,2);g.base();g.value((0,0),'S');g.value((3,2),'F',GOLD)
    if q.after('a blocked intersection') and not q.after('for a closed edge'):
        g.barrier((1,1),True);caption(c,'Blocked point     0',277,RED)
    if q.after('for a closed edge') and not q.after('must visit a checkpoint'):
        a,b=g.pos((0,1)),g.pos((1,1));x=(a[0]+b[0])/2;y=a[1]
        c.line([(x-10,y-10),(x+10,y+10)],RED,5);c.line([(x-10,y+10),(x+10,y-10)],RED,5)
        caption(c,'Only one incoming edge closes',232,RED)
        if q.after('still be reachable'):g.arrow((1,0),(1,1),1,GOLD);g.value((1,1),1,GOLD)
        if q.after('put one at the start'):g.value((0,0),1)
        if q.after('incoming counts'):
            g.fill(counts(3,2,closed_edges=[((0,1),(1,1))]),[(1,0),(0,1),(0,2),(2,0),(2,1)],q.after('incoming counts',1.2))
    if q.after('must visit a checkpoint'):
        g.value((1,1),'C',BLUE);caption(c,'Required checkpoint (1, 1)',227,BLUE)
        if q.after('ways to reach it'):caption(c,'2 ways to C',312,BLUE)
        if q.after('ways to finish'):caption(c,'3 ways from C to F',390,GOLD)
        if q.after('every continuation is allowed'):caption(c,'2 × 3 = 6 walks',474,TEAL)


SCENES=(opening,exam_cues,easy_question,three_walks,medium_question,medium_solve,
        hard_question,hard_solve,check_barriers,mistakes,transfer)
