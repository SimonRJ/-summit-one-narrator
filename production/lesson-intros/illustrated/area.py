"""Lesson 78. The complement is a moving, measured region in every example."""
from visuals import AQUA, BLUE, GOLD, PINK, SOFT, VIOLET, WHITE, bounds, grid, mix


def rect_outline(art, box, colour, progress, width=3, cursor=False):
    art.trace(bounds(*box), progress, colour, width, cursor)


def add_rectangles(art, c, solution=False):
    a = c.opening() if solution else c.after("six by five")
    b = c.opening() if solution else c.after("three by four", 1.15)
    slide = 1 if solution else c.after("along an edge", 1.2)
    first_count = c.says("thirty") if solution else 0
    second_count = c.says("twelve") if solution else 0
    seam = c.after("joining along an edge") if solution else c.after("A shared edge")
    scale = 56
    x, y = 368, 205
    lower = y + scale*5
    bx, by = x + 6*scale + (1-slide)*100, lower - 4*scale
    for ox, oy, w, h, colour, p in ((x, y, 6, 5, AQUA, a), (bx, by, 3, 4, GOLD, b)):
        art.rect(ox, oy, w*scale, h*scale, colour, .23*p)
        grid(art, ox, oy, w, h, scale, colour, .35*p)
        rect_outline(art, (ox, oy, w*scale, h*scale), colour, p)
    if seam:
        art.trace(((x+6*scale,by),(x+6*scale,lower)), seam, WHITE, 5)
    art.dimension((x,y-16),(x+6*scale,y-16),"6",AQUA,a)
    art.dimension((x-15,y),(x-15,lower),"5",AQUA,a,offset=24,size=30)
    art.dimension((bx,by-17),(bx+3*scale,by-17),"3",GOLD,b)
    art.dimension((bx+3*scale+14,by),(bx+3*scale+14,lower),"4",GOLD,b,offset=-23,size=30)
    art.label("30", x+3*scale, y+2.5*scale, 67, AQUA, first_count, bold=True)
    art.label("12", bx+1.5*scale, by+2*scale, 67, GOLD, second_count, bold=True)
    if solution:
        answer = c.says("forty-two square units")
        art.label("30 + 12 = 42 square units",640,565,46,WHITE,answer,bold=True)
    else:
        art.label("What is the combined area?",640,555,38,WHITE,c.after("Find their combined area"),bold=True)
        art.label("The common edge has zero area",640,610,26,SOFT,seam)


def corner(art, c, solution=False):
    x, y, u = 265, 207, 37
    w, h = 11*u, 9*u
    hinge = x+w-5*u, y
    top_right = x+w, y
    lower_right = x+w, y+4*u
    box = c.opening() if solution else c.after("eleven by nine",1.25)
    cut = c.opening() if solution else c.after("right triangle removed",1.4)
    measured = c.opening() if solution else c.after("five and four units", .55)
    lifted = c.after("Subtract the triangle",1.55) if solution else 0
    full = c.says("ninety-nine") if solution else 0
    half = c.after("half of a rectangle",1.0) if solution else 0
    half_labels = c.says("five and four") if solution else 0
    answer = c.says("eighty-nine square units") if solution else 0
    art.rect(x,y,w,h,AQUA,.19*box)
    grid(art,x,y,11,9,u,AQUA,.23*box)
    rect_outline(art,(x,y,w,h),AQUA,box,3)
    art.polygon((hinge,top_right,lower_right),PAPER_COLOUR,cut*lifted)
    kept = ((x,y),hinge,lower_right,(x+w,y+h),(x,y+h),(x,y))
    art.trace(kept,lifted,AQUA,4,False)
    art.dimension((x,y+h+20),(x+w,y+h+20),"11 units",AQUA,box,offset=-25)
    art.dimension((x-24,y),(x-24,y+h),"9 units",AQUA,box,offset=48)
    dy, dx = -35*lifted, 144*lifted
    triangle = [(a+dx,b+dy) for a,b in (hinge,top_right,lower_right,hinge)]
    art.polygon(triangle,GOLD,.46*cut)
    art.trace(triangle,cut,GOLD,4)
    if measured:
        hx,hy=triangle[0]
        rx,ry=triangle[1]
        art.dimension((hx,hy-13),(rx,ry-13),"5 units",GOLD,measured,offset=20,size=30)
        art.dimension((rx+15,ry),(rx+15,ry+4*u),"4 units",GOLD,measured,offset=-42,size=27)
        art.path(((rx-14,ry),(rx-14,ry+14),(rx,ry+14)),WHITE,2,measured)
    if solution:
        art.label("11 × 9 = 99",1045,220,40,AQUA,full,bold=True)
        ox, oy, step = 952, 302, 28
        if half:
            art.rect(ox,oy,5*step,4*step,BLUE,.12*half)
            grid(art,ox,oy,5,4,step,BLUE,.35*half)
            rect_outline(art,(ox,oy,5*step,4*step),SOFT,half,2)
            piece = [(ox,oy),(ox+5*step,oy),(ox+5*step,oy+4*step),(ox,oy)]
            art.polygon(piece,GOLD,.46*half)
            art.trace(piece,half,GOLD,3,False)
        art.label("½ × 5 × 4 = 10",1038,455,36,GOLD,half_labels,bold=True)
        art.label("99 − 10 = 89",1038,533,46,WHITE,answer,bold=True)
        art.label("square units",1038,580,28,AQUA,answer)
    else:
        question=c.after("Find the area left")
        art.label("Shaded area",958,337,46,AQUA,question,bold=True)
        art.label("How much is left?",958,408,33,WHITE,question)


PAPER_COLOUR = "#101c2a"
CHALLENGE = (238,178,46)
LOWER = {(col,row) for col in range(7) for row in range(6)}
UPPER = {(col,row) for col in range(3,10) for row in range(2,9)}
BOARD = {(col,row) for col in range(10) for row in range(9)}
FIRST = {(col,row) for col,row in BOARD-UPPER-LOWER if row < 2}
SECOND = BOARD-UPPER-LOWER-FIRST
assert tuple(map(len,(LOWER,UPPER,LOWER&UPPER,FIRST,SECOND))) == (42,49,16,6,9)


def challenge_board(art, x, y, u, base=1, a=1, b=1, overlap=0, first=0, second=0, muted=0):
    if base > 0:
        art.rect(x,y,10*u,9*u,BLUE,.07*base)
    for col,row in sorted(LOWER|UPPER|FIRST|SECOND):
        candidates = ((AQUA,a*.38 if (col,row) in LOWER else 0),
                      (GOLD,b*.38 if (col,row) in UPPER else 0),
                      (VIOLET,overlap*.68 if (col,row) in LOWER&UPPER else 0),
                      (AQUA,first*.65 if (col,row) in FIRST else 0),
                      (GOLD,second*.65 if (col,row) in SECOND else 0))
        for colour, alpha in candidates:
            if alpha > 0:
                art.rect(x+col*u,y+(8-row)*u,u,u,colour,alpha*(1-.64*muted))
    grid(art,x,y,10,9,u,SOFT,.32*base)
    rect_outline(art,(x,y,10*u,9*u),SOFT,base,2)
    rect_outline(art,(x,y+3*u,7*u,6*u),AQUA,a,3)
    rect_outline(art,(x+3*u,y,7*u,7*u),GOLD,b,3)
    rect_outline(art,(x+3*u,y+3*u,4*u,4*u),VIOLET,overlap,4,True)
    return x,y,u


def overlap(art,c,scene):
    x,y,u = CHALLENGE
    if scene==7:
        base=c.after("ten by nine board",1.25)
        a=c.after("lower-left rectangle",1.9)
        b=c.after("rectangle covering all columns",2.25)
        art.label("What stays unshaded?", 937, 274, 36, WHITE, c.after("How much area is unshaded"),bold=True)
        art.label("Rows count upwards",936,416,28,SOFT,c.after("rows numbered from the bottom"))
        art.arrow((x-25,y+9*u),(x-25,y+2*u),SOFT,c.after("rows numbered from the bottom",1.2))
        for index in range(10):
            art.label(index+1,x+(index+.5)*u,y+9*u+21,20,SOFT,base)
        for index in range(9):
            art.label(index+1,x-47,y+(8.5-index)*u,20,SOFT,base)
        challenge_board(art,x,y,u,base,a,b)
        art.label("7 × 6",x+1.5*u,y+6.6*u,27,AQUA,a,bold=True)
        art.label("7 × 7",x+8.1*u,y+1.4*u,27,GOLD,b,bold=True)
        return
    if scene==8:
        cross=c.after("Adding them directly",1.6)
        measure=c.after("width four and height four")
        challenge_board(art,x,y,u,1,1,1,cross)
        art.dimension((x+3*u,y+3*u-12),(x+7*u,y+3*u-12),"4",VIOLET,measure,offset=15)
        art.dimension((x+7*u+12,y+3*u),(x+7*u+12,y+7*u),"4",VIOLET,measure,offset=-17)
        art.label("42  +  49",953,240,48,WHITE,c.says("forty-nine"),bold=True)
        art.label("− 16 overlap",953,321,35,VIOLET,c.says("sixteen"),bold=True)
        art.label("90 − (42 + 49 − 16)",953,444,36,WHITE,c.after("from the full board"))
        art.label("15 square units",953,535,45,AQUA,c.says("fifteen square units"),bold=True)
    else:
        first=c.after("bottom right block",.8)
        second=c.after("top left block",.8)
        challenge_board(art,x,y,u,1,1,1,0,first,second,.55)
        art.label("3 × 2", x+8.5*u, y+8*u,31,AQUA,first,bold=True)
        art.label("3 × 3", x+1.5*u, y+1.5*u,31,GOLD,second,bold=True)
        art.label("6 + 9 = 15",947,351,61,WHITE,c.after("Their sum confirms"),bold=True)
        art.label("Two separate uncovered regions",947,419,27,AQUA,c.after("disjoint interiors"))


def idea(art,c,exam=False):
    x,y,u=262,208,49
    if exam:
        a=c.after("easy surrounding shape",1.5)
        b=c.after("may make regions overlap",1.5)
        points=[(x+4*u,y),(x+7*u,y),(x+7*u,y+3*u)]
        art.polygon([(x,y),points[0],points[2],(x+7*u,y+6*u),(x,y+6*u)],AQUA,.25)
        art.trace(bounds(x,y,7*u,6*u),a,SOFT,3)
        art.trace([*points,points[0]],a,GOLD,4)
        art.label("Start with the whole shape",436,550,28,AQUA,a)
        for ox,oy,col in [(755,241,AQUA),(861,326,GOLD)]:
            art.rect(ox,oy,200,157,col,.27*b)
            rect_outline(art,(ox,oy,200,157),col,b)
        art.rect(861,326,94,72,VIOLET,.62*b)
        art.label("Count the overlap once",908,550,28,VIOLET,c.after("exactly once"))
    else:
        count=c.after("square units fill",1.5)
        split=c.after("Draw an extra line",1.3)
        outside=c.after("whole rectangle",1.4)
        visible=((x,y),(x+7*u,y),(x+7*u,y+3*u),(x+4*u,y+3*u),(x+4*u,y+6*u),(x,y+6*u),(x,y))
        art.polygon(visible,AQUA,.25*c.opening())
        art.trace(visible,c.opening(1.1),AQUA,4)
        for row in range(6):
            grid(art,x,y+row*u,7 if row<3 else 4,1,u,SOFT,.29*count)
        art.rect(x+4*u,y,3*u,3*u,GOLD,.30*split)
        art.trace(((x+4*u,y),(x+4*u,y+3*u)),split,GOLD,4)
        art.dashed((x+7*u,y+3*u),(x+7*u,y+6*u),SOFT,3,outside)
        art.dashed((x+7*u,y+6*u),(x+4*u,y+6*u),SOFT,3,outside)
        art.label("Split what you have",946,304,34,GOLD,split,bold=True)
        art.label("or subtract what is missing",946,404,31,AQUA,outside,bold=True)


def mistakes(art,c,recap=False):
    if recap:
        base=c.after("full surrounding shape")
        a=c.after("Name each piece")
        measure=c.after("label its needed lengths")
        common=c.after("Check the intersection")
        last=c.after("a different split is easy")
        challenge_board(art,276,179,43,base,a,a,common,last,last)
        art.dimension((276,590),(706,590),"10 units",SOFT,measure,offset=-24)
        art.label("Name the regions",928,303,32,AQUA,a,bold=True)
        art.label("Check the intersection",928,397,31,VIOLET,common,bold=True)
        art.label("Try another split",928,496,32,GOLD,last,bold=True)
    else:
        area=c.after("Area uses square units")
        edge=c.after("length around the edge",1.45)
        for y in range(4):
            for x in range(5):
                p = max(0,min(1,area*1.5-(y*5+x)*.025))
                art.rect(182+x*51,238+y*51,49,49,AQUA,.38*p)
        art.trace(bounds(182,238,255,204),edge,PINK,4)
        art.label("Area counts these squares",309,513,29,AQUA,area,bold=True)
        art.label("Perimeter follows this edge",309,562,26,PINK,edge)
        p=c.after("both shaded rectangles",1.1)
        overlap=c.after("removes the overlap again")
        fix=c.after("Add that common area back once")
        challenge_board(art,718,182,41,p,p,p,overlap)
        art.label("Add the shared area back once",923,597,27,VIOLET,fix,bold=True)


TITLES = {
    1:("See the area inside",None),
    2:("Spot the surrounding shape","AMC Upper Primary  ·  Rossmoyne-style reasoning"),
    3:("Join two rectangles",None),
    4:("Area adds across a shared edge",None),
    5:("A triangle is cut away",None),
    6:("Measure what was removed",None),
    7:("Two regions overlap",None),
    8:("Count the overlap once",None),
    9:("Check by counting what is left",None),
    10:("Watch the units and the overlap",None),
    11:("Draw, label, check",None),
}


def draw(art,c,scene):
    title, subtitle = TITLES[scene]
    art.heading(title,AQUA,subtitle)
    if scene in (1,2):
        idea(art,c,scene==2)
    elif scene in (3,4):
        add_rectangles(art,c,scene==4)
    elif scene in (5,6):
        corner(art,c,scene==6)
    elif scene in (7,8,9):
        overlap(art,c,scene)
    else:
        mistakes(art,c,scene==11)
