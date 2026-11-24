"""Trace three equal-area cuts with different effects on exposed boundary."""
BACKGROUND = ("#19343a", "#294548")
INK, WOOD, OLD, NEW, PAPER = "#f7f0dd", "#e6c58c", "#ffe8ab", "#ff9483", "#203b3d"
BRIDGE = "The same offcut comes from a corner, an edge or the centre. Which old edges disappear in each drawing, and which new edges need tape?"
HEAD = ("Three trays, one offcut", "Before any cut", "Clip the corner", "Exchange two edges", "Move the cut along", "Cut a window", "Two loops to tape", "Sort the three orders")
CUTS = {"Full": None, "Corner": (0,0), "Notch": (4,0), "Window": (4,3)}


def check_maths():
    board = {(x, y) for x in range(12) for y in range(8)}
    for label, position in CUTS.items():
        cut = set() if position is None else {(position[0]+x,position[1]+y) for x in range(3) for y in range(2)}
        cells = board-cut
        edge = sum((x+dx,y+dy) not in cells for x,y in cells for dx,dy in ((-1,0),(1,0),(0,-1),(0,1)))
        assert edge == {"Full":40,"Corner":40,"Notch":44,"Window":50}[label]
        assert len(cells) == (96 if position is None else 90)


def sign(a, name, x, y, step):
    def path(points, colour, line):
        a.line([(x+u*step,y+v*step) for u,v in points],colour,line)
    corner=[(3,0),(12,0),(12,8),(0,8),(0,2),(3,2)]
    notch=[(0,0),(4,0),(4,2),(7,2),(7,0),(12,0),(12,8),(0,8)]
    outer=corner if name=="Corner" else notch if name=="Notch" else [(0,0),(12,0),(12,8),(0,8)]
    a.polygon([(x+u*step,y+v*step) for u,v in outer],WOOD)
    path(outer+[outer[0]],OLD,5)
    if name=="Corner":
        path([(0,2),(3,2),(3,0)],NEW,7)
        a.dashed((x,y),(x+3*step,y),"#a2b4aa",3);a.dashed((x,y),(x,y+2*step),"#a2b4aa",3)
    if name=="Notch":
        path([(4,0),(4,2),(7,2),(7,0)],NEW,7)
        a.dashed((x+4*step,y),(x+7*step,y),"#a2b4aa",3)
    if name=="Window":
        hole=[(4,3),(7,3),(7,5),(4,5)]
        a.polygon([(x+u*step,y+v*step) for u,v in hole],PAPER)
        path(hole+[hole[0]],NEW,6)


def draw(a,n,c):
    a.text(HEAD[n-1],64,71,47,INK,bold=True,align="left");a.line([(65,122),(1215,122)],"#74938b",3)
    if n in (1,8):
        for i,(name,num,word) in enumerate((("Corner",40,"Corner"),("Notch",44,"Notch"),("Window",50,"Window"))):
            x=108+411*i;sign(a,name,x,232,20);a.text(name,x+120,175,32,INK,bold=True)
            a.text("3 × 2 cm removed" if n==1 else f"{num} cm of tape",x+120,440,27,INK,bold=True,opacity=1 if n==1 else c.reveal(word))
        a.text("Which order needs the longest strip?" if n==1 else "Tape the outside and every window edge.",640,549,36,INK)
        return
    name={2:"Full",3:"Corner",4:"Corner",5:"Notch",6:"Window",7:"Window"}[n];sign(a,name,140,215,30)
    a.text("12 cm",320,170,27,OLD);a.text("8 cm",76,338,25,OLD)
    if n==2:
        rows=[("Outside loop","Trace all four sides",1),("12 + 8 + 12 + 8","40 cm",c.reveal("Forty centimetres"))]
    elif n in (3,4):
        rows=[("Old top and left","3 + 2 = 5 cm",1),("New cut edges","2 + 3 = 5 cm",c.reveal("Five replaces"))] if n==4 else [("Old top and left","3 + 2 = 5 cm",c.reveal("Those five")),("New exposed edges","Trace the corner",1)]
    elif n==5:
        rows=[("Old top edge","3 cm",1),("New cut edges","2 + 3 + 2 = 7 cm",c.reveal("Seven centimetres"))]
    elif n==6:
        rows=[("Previous notch","40 + 4 = 44 cm",c.reveal("forty four")),("Enclosed window","Which edges disappear?",1)]
    else:
        rows=[("Outside loop","40 cm",1),("Inside loop","3 + 2 + 3 + 2 = 10 cm",c.reveal("ten centimetres"))]
    for j,(title,value,alpha) in enumerate(rows):
        y=215+143*j;a.text(title,636,y,27,OLD,align="left");a.text(value,636,y+52,35,INK,bold=True,align="left",opacity=alpha)
    if n==4:a.text("40 − 5 + 5 = 40 cm",640,552,37,INK,bold=True,opacity=c.reveal("forty centimetres"))
    if n==7:a.text("All exposed edges: 40 + 10 = 50 cm",640,552,37,INK,bold=True,opacity=c.reveal("fifty centimetres"))


def poster(draw):
    return draw(8,1)
