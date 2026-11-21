"""Choose the four lines of a rectangle on square-cell grids for S094."""
from itertools import combinations
from math import comb

PAPER, INK, MUTED = '#13272e', '#f5f5e9', '#abc4ca'
GRID, AQUA, GOLD, RED, BLUE = '#4f747d', '#70e5cf', '#ffd58d', '#ffa697', '#a5ccff'
A, B = (2, 3), (5, 3)


def verify():
    assert (5 + 1) * (3 + 1) == 24
    assert comb(7, 2) * comb(6, 2) == 315
    rectangles = [(l, r, b, t) for l, r in combinations(range(9), 2)
                  for b, t in combinations(range(6), 2)]
    def contains(rect, cell):
        l, r, b, t = rect
        x, y = cell
        return l < x <= r and b < y <= t
    include_a = [r for r in rectangles if contains(r, A)]
    both = [r for r in include_a if contains(r, B)]
    legal = [r for r in include_a if not contains(r, B)]
    assert (len(include_a), len(both), len(legal)) == (126, 72, 54)
    assert {r[1] for r in legal} == {2, 3, 4}


def title(c, text):
    c.text(text, 54, 57, 39, INK, 'lm', True)


def label(c, text, y, colour=INK, size=29):
    c.text(text, 927, y, size, colour, bold=True)


class Grid:
    def __init__(self, c, w, h):
        self.c, self.w, self.h = c, w, h
        self.step = min(91, 478 / w, 298 / h)
        self.x = 343 - self.step*w/2
        self.y = 336 + self.step*h/2

    def pos(self, x, y):
        return self.x+x*self.step, self.y-y*self.step

    def base(self):
        for i in range(self.w+1): self.vertical(i, GRID, 2)
        for j in range(self.h+1): self.horizontal(j, GRID, 2)

    def vertical(self, x, colour, width=5):
        self.c.line([self.pos(x,0), self.pos(x,self.h)], colour, width)

    def horizontal(self, y, colour, width=5):
        self.c.line([self.pos(0,y), self.pos(self.w,y)], colour, width)

    def lines(self, axis, choices, colour, progress):
        choices = list(choices)
        for value in choices[:round(progress*len(choices))]:
            if axis == 'x':
                self.vertical(value, colour)
                x,y = self.pos(value,0)
                self.c.text(value,x,y+26,21,colour,bold=True)
            else:
                self.horizontal(value, colour)
                x,y = self.pos(0,value)
                self.c.text(value,x-26,y,21,colour,bold=True)

    def area(self, l,r,b,t, colour, fill=None, width=5):
        x,y = self.pos(l,t)
        self.c.rect(x,y,(r-l)*self.step,(t-b)*self.step,fill,colour,width)

    def cell(self, x,y,name,colour):
        self.area(x-1,x,y-1,y,colour,'#253c42',3)
        self.c.text(name,*self.pos(x-.5,y-.5),24,colour,bold=True)

    def dimensions(self):
        x,y = self.pos(self.w/2,0)
        self.c.text(f'{self.w} columns',x,y+42,24,BLUE)
        x,y = self.pos(0,self.h/2)
        self.c.text(f'{self.h}',x-41,y-12,24,GOLD)
        self.c.text('rows',x-41,y+15,17,GOLD)

    def cells_axes(self):
        for v in range(1,self.w+1):
            x,y=self.pos(v-.5,0); self.c.text(v,x,y+24,19,BLUE)
        for v in range(1,self.h+1):
            x,y=self.pos(0,v-.5); self.c.text(v,x-22,y,19,GOLD)

    def point(self,x,y,colour=AQUA):
        self.c.dot(*self.pos(x,y),6,colour)


def opening(c,q):
    title(c,'What does the question count?')
    g=Grid(c,4,3); g.base()
    if q.after('choose the two lines'):
        g.vertical(0,BLUE);g.vertical(3,BLUE);label(c,'Choose 2 vertical lines',230,BLUE)
        if q.after('pair of opposite edges'):
            g.horizontal(0,GOLD);g.horizontal(2,GOLD)
            g.area(0,3,0,2,AQUA);label(c,'Choose 2 horizontal lines',326,GOLD)
            label(c,'These sides give 1 rectangle',431,AQUA,27)
        return
    if q.after('made from lines'):
        g.vertical(1,BLUE);label(c,'A line',199,BLUE)
    if q.after('spaces between the lines'):
        g.cell(2,2,'',GOLD);label(c,'A cell',266,GOLD)
    if q.after('where the lines meet'):
        g.point(3,2);label(c,'A crossing',333,AQUA)



def exam(c,q):
    title(c,'Mark the object before counting')
    g=Grid(c,5,3);g.base()
    if q.after('one marked cell'):
        g.cell(2,2,'A',AQUA)
        if q.after('avoiding another'):g.cell(4,2,'B',RED)
        if q.after('possible boundaries'):g.area(0,3,1,3,GOLD);label(c,'Cover A and leave B out',357,GOLD)
    elif q.after('shapes cut out'):
        g.area(1,4,0,2,GOLD);label(c,'An outline',297,GOLD)
    elif q.after('paths'):
        c.line([g.pos(0,0),g.pos(2,0),g.pos(2,2),g.pos(4,2)],BLUE,6)
        label(c,'A path along lines',297,BLUE)
    elif q.after('intersections'):
        g.point(2,1);label(c,'A crossing',297,AQUA)


def easy(c,q):
    title(c,'How many crossings on a 5 by 3 grid?')
    g=Grid(c,5,3);g.base();g.dimensions()
    if q.after('points where'):g.point(2,2);label(c,'Count where two lines meet',287,AQUA,27)
    if q.after('outside edges'):
        g.area(0,5,0,3,GOLD);g.point(0,0,GOLD);g.point(5,3,GOLD)
        label(c,'Include the outer lines',391,GOLD)


def easy_solve(c,q):
    title(c,'Each vertical line has four crossings')
    g=Grid(c,5,3);g.base()
    g.lines('x',range(6),BLUE,q.after('six vertical lines'))
    g.lines('y',range(4),GOLD,q.after('four horizontal lines'))
    if q.after('six vertical lines'): label(c,'6 vertical lines',220,BLUE)
    if q.after('four horizontal lines'): label(c,'4 horizontal lines',293,GOLD)
    pts=[(x,y) for x in range(6) for y in range(4)]
    for a in pts[:round(24*q.after('each vertical line crosses',2.6))]:g.point(*a)
    if q.after('twenty-four crossing points'):label(c,'6 × 4 = 24 points',403,AQUA,35)


def medium(c,q):
    title(c,'Count every grid-line rectangle')
    g=Grid(c,6,5);g.base();g.dimensions()
    if q.after('all rectangles'):
        g.area(1,5,1,3,AQUA);label(c,'Four sides on grid lines',278,AQUA)
    if q.after('a square counts'):
        g.area(4,6,3,5,GOLD);label(c,'Include squares',386,GOLD)


def medium_solve(c,q):
    title(c,'Choose one pair in each direction')
    g=Grid(c,6,5);g.base()
    if q.after('number the seven'):
        for i in range(7):
            x,y=g.pos(i,0);c.text(i,x,y+26,20,BLUE)
    if q.after('six horizontal lines'):
        g.lines('y',range(6),GOLD,q.after('six horizontal lines',1.3))
        label(c,'Vertical pairs: 21',190,BLUE)
        if q.after('five plus four'):label(c,'5 + 4 + 3 + 2 + 1 = 15',274,GOLD,27)
        if q.after('each vertical pair'):
            g.vertical(1,BLUE);g.vertical(5,BLUE);g.horizontal(1,GOLD);g.horizontal(4,GOLD)
            g.area(1,5,1,4,AQUA)
        if q.after('three hundred and fifteen'):label(c,'21 × 15 = 315',404,AQUA,39)
    elif q.after('left edge is on line zero'):
        first=0
        for i,phrase in enumerate(('five choices remain','then four','three two','two and one','and one'),1):
            if q.after(phrase):first=i
        g.vertical(first,GOLD)
        g.lines('x',range(first+1,7),BLUE,1)
        label(c,f'Left on {first}: {6-first} right choices',253,GOLD,26)
        if q.after('twenty-one vertical pairs'):label(c,'6 + 5 + 4 + 3 + 2 + 1 = 21',353,BLUE,26)


def hard(c,q):
    title(c,'Cover A and leave B out')
    g=Grid(c,8,5);g.base();g.cells_axes()
    if q.after('mark cell a'):g.cell(*A,'A',AQUA);label(c,'A: column 2, row 3',218,AQUA)
    if q.after('mark cell b'):g.cell(*B,'B',RED);label(c,'B: column 5, row 3',285,RED)
    if q.after('a side may touch b'):
        g.area(0,4,1,4,GOLD);label(c,'Touching B is allowed',396,GOLD,27)


def contain(c,q):
    title(c,'Choose the boundaries of a rectangle covering A')
    g=Grid(c,8,5);g.base()
    options=(('x',(0,1),BLUE,'the two lines','Left edge: 2',176),
             ('x',range(2,9),AQUA,'seven lines','Right edge: 7',235),
             ('y',(0,1,2),GOLD,'three lines can be','Bottom edge: 3',294),
             ('y',(3,4,5),RED,'three can be the top','Top edge: 3',353))
    for axis,values,colour,phrase,word,y in options:
        p=q.after(phrase)
        if p:g.lines(axis,values,colour,p);label(c,word,y,colour)
    g.cell(*A,'A',AQUA)
    if q.after('one hundred and twenty-six'):
        label(c,'2 × 7 × 3 × 3 = 126',458,INK,32)
    if q.after('one set of four boundaries'):g.area(1,6,1,4,INK, None,4)


def exclude(c,q):
    title(c,'Subtract the rectangles that also cover B')
    g=Grid(c,8,5);g.base()
    direct=q.after('check it directly')
    if direct:
        g.lines('x',(0,1),BLUE,1)
        g.lines('x',(2,3,4),GOLD,q.after('three right edges'))
        g.cell(*A,'A',AQUA);g.cell(*B,'B',RED)
        if q.after('stop before entering b'):
            g.area(1,4,2,3,GOLD);label(c,'Right edge on 2, 3 or 4',270,GOLD,29)
        if q.after('also gives fifty-four'):label(c,'2 × 3 × 3 × 3 = 54',388,AQUA,34)
        return
    g.area(1,5,2,3,GOLD);g.cell(*A,'A',AQUA);g.cell(*B,'B',RED)
    g.lines('x',(0,1),BLUE,q.after('two left choices'))
    g.lines('y',(0,1,2),GOLD,q.after('three bottom choices'))
    g.lines('y',(3,4,5),RED,q.after('three top choices'))
    g.lines('x',(5,6,7,8),AQUA,q.after('four choices'))
    if q.after('four choices'):label(c,'4 right edges reach B',218,AQUA,29)
    if q.after('gives seventy-two'):label(c,'2 × 4 × 3 × 3 = 72',319,GOLD,31)
    if q.after('to get fifty-four'):label(c,'126 − 72 = 54',423,AQUA,36)


def mistakes(c,q):
    title(c,'Count the outer lines and use each pair once')
    g=Grid(c,5,1);g.base()
    if q.after('outside boundary'):g.area(0,5,0,1,GOLD)
    if q.after('six lines'):g.lines('x',range(6),BLUE,1);label(c,'5 cells have 6 edge lines',235,BLUE,28)
    if q.after('left and right lines'):
        g.vertical(1,AQUA);g.vertical(4,AQUA);g.area(1,4,0,1,AQUA)
        label(c,'Lines 1 and 4',336,AQUA)
    if q.after('fixes their order'):
        label(c,'Left = 1     Right = 4',418,GOLD,29)


def transfer(c,q):
    title(c,'Use the restrictions on a new grid')
    g=Grid(c,4,3);g.base()
    if q.after('for a forbidden cell'):
        g.cell(2,2,'A',AQUA);g.cell(4,2,'B',RED)
        if q.after('restrict one boundary'):
            g.lines('x',(2,3),GOLD,1);label(c,'2 legal right edges',248,GOLD)
        if q.after('check by subtraction'):
            label(c,'3 possible − 1 covering B = 2',369,AQUA,26)
    elif q.after('for a square'):
        g.area(0,2,0,2,AQUA);label(c,'Width 2 fixes height 2',248,AQUA,29)
        if q.after('possible positions'):
            for x,y in [(i,j) for i in range(3) for j in range(2)]:g.point(x,y,GOLD)
            label(c,'3 × 2 = 6 starting corners',372,GOLD,27)
    elif q.after('for a rectangle'):
        g.vertical(0,BLUE);g.vertical(3,BLUE)
        if q.after('bottom and top'):g.area(0,3,1,3,AQUA)
        label(c,'Choose four boundary lines',302,AQUA,27)
    else:
        if q.after('counts cells'):g.cell(2,2,'',GOLD)
        if q.after('crossings'):g.point(2,2)
        if q.after('outlines'):g.area(1,3,0,2,BLUE)
        if q.after('outer lines'):g.area(0,4,0,3,GOLD)


SCENES=(opening,exam,easy,easy_solve,medium,medium_solve,hard,contain,exclude,mistakes,transfer)
