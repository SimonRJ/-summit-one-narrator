"""A five-position proscenium distinguishes a directed pair from either neighbour."""
from itertools import permutations

BACKGROUND = ("#3e3341", "#282732")
PAPER, INK, WOOD, YELLOW, BLUE, RED, LINE = (
    "#fbefd6", "#332c35", "#be9d83", "#eac57e", "#abd5dc", "#efa393", "#897d87")
HEADINGS = (
    "Five marked places", "Count all the bows", "Count the forbidden ends",
    "Treat the bow pair as one", "Find the double crossing", "Restore one crossing",
    "Check from the inside", "Change the stage direction",
)
BRIDGE = "Place the owl on an end of the puppet stage, then try to put the fox immediately to its right. Which end can receive both pencil marks? Why must six orders be added back?"


def check_maths():
    orders = set(permutations(("Owl", "Fox", "Bear", "Hare", "Mouse")))
    ends = {r for r in orders if r.index("Owl") in (0, 4)}
    pair = {r for r in orders if r.index("Fox") == r.index("Owl") + 1}
    both_sides = {r for r in orders if abs(r.index("Fox") - r.index("Owl")) == 1}
    assert [len(s) for s in (orders, ends, pair, ends & pair)] == [120, 48, 24, 6]
    assert len(orders - ends - pair) == 54 and len(orders - ends - both_sides) == 36


def label(board, value, x, y, size, colour=PAPER, opacity=1):
    board.text(str(value), x, y, size, colour, bold=True, opacity=opacity)


def puppet(board, x, y, name):
    colours = {"Owl": YELLOW, "Fox": RED, "Bear": "#ccaa89", "Hare": BLUE, "Mouse": "#c5c2d2"}
    colour = colours[name]
    board.line([(x,y+16),(x,y+39)], WOOD, 5)
    if name == "Hare":
        for dx in (-11,11):
            board.box(x+dx-5,y-45,10,33,fill=colour,radius=5)
    elif name in ("Owl","Fox"):
        for sign in (-1,1):
            board.polygon([(x+22*sign,y-27),(x+20*sign,y-5),(x+3*sign,y-9)], colour)
    else:
        for dx in (-17,17):
            board.dot(x+dx,y-16,10,colour)
    board.dot(x,y,24,colour)
    for dx in (-8,8):
        board.dot(x+dx,y-3,2.5,INK)
    if name in ("Owl","Fox"):
        board.polygon([(x-4,y+5),(x+4,y+5),(x,y+11)],INK)


def stage(board, places, y=279, forbidden=()):
    board.box(99,y-86,1082,180,fill="#302d36",edge=LINE,stroke=3,radius=12)
    for index, name in enumerate(places):
        x = 235 + index*203
        board.line([(x-59,y+44),(x+59,y+44)],WOOD,5)
        label(board,index+1,x,y+71,23,WOOD)
        if name:
            puppet(board,x,y-19,name)
            label(board,name,x,y+28,22)
        if index+1 in forbidden:
            board.line([(x+41,y-42),(x+65,y-18)],RED,5)
            board.line([(x+65,y-42),(x+41,y-18)],RED,5)


def tied_pair(board):
    board.box(247,215,343,149,edge=RED,stroke=5,radius=14)
    puppet(board,342,275,"Owl")
    puppet(board,501,275,"Fox")
    label(board,"Owl",342,337,26,YELLOW)
    label(board,"Fox",501,337,26,RED)
    for index, animal in enumerate(("Bear","Hare","Mouse")):
        x=735+index*147
        puppet(board,x,275,animal)
        label(board,animal,x,337,26)


def draw(board, scene, cue):
    board.label(HEADINGS[scene-1],64,70,42,PAPER,bold=True)
    board.line([(64,124),(1216,124)],LINE,3)
    if scene == 1:
        stage(board,("Bear","Owl","Hare","Fox","Mouse"))
        label(board,"Audience’s left",267,443,33,BLUE)
        label(board,"Audience’s right",1000,443,33,BLUE)
        label(board,"All five puppets are different.",640,536,37,PAPER,cue.reveal("Switching any two"))
    elif scene == 2:
        stage(board,("",)*5)
        label(board,"5 × 4 × 3 × 2 × 1 = 120",640,443,42,YELLOW,cue.reveal("one hundred and twenty"))
        label(board,"Owl off the ends. Fox never just to Owl’s right.",640,542,31,PAPER,cue.reveal("must never stand"))
    elif scene == 3:
        stage(board,("Owl","","","",""),forbidden=(1,5))
        label(board,"2 end choices  ×  24 orders for the others",640,444,35,PAPER,cue.reveal("two choices for its end"))
        label(board,"48 forbidden end orders",640,546,40,RED,cue.reveal("forty eight orders"))
    elif scene == 4:
        tied_pair(board)
        label(board,"1 directed pair + 3 other puppets = 4 objects",640,448,34,PAPER,cue.reveal("four objects"))
        label(board,"24 forbidden pair orders",640,547,38,RED,cue.reveal("twenty four orders"))
    elif scene == 5:
        stage(board,("Owl","Fox","","",""),forbidden=(1,))
        label(board,"Both marks force Owl first and Fox second.",640,441,34,RED,cue.reveal("Only owl first"))
        label(board,"3 × 2 × 1 = 6 double crossings",640,544,38,YELLOW,cue.reveal("six ways"))
    elif scene == 6:
        for i,(amount,description,colour) in enumerate((
            ("120","all",PAPER),("−48","owl on end",RED),("−24","owl then fox",RED),("+6","both marks",BLUE))):
            x=220+280*i
            label(board,amount,x,292,61,colour)
            label(board,description,x,364,27,colour)
        label(board,"54 allowed bows",640,514,46,YELLOW,cue.reveal("fifty four allowed"))
    else:
        blocked = (4,) if scene==7 else (2,4)
        stage(board,("","","Owl","",""),forbidden=blocked)
        if scene==7:
            label(board,"3 owl places  ×  3 fox places  ×  6 orders",640,447,34,PAPER,cue.reveal("fox has three choices"))
            label(board,"54 allowed",640,547,43,BLUE,cue.reveal("again makes fifty four"))
        else:
            label(board,"3 owl places  ×  2 fox places  ×  6 orders",640,447,34,PAPER,cue.reveal("Only two of the four"))
            label(board,"36 allowed",640,547,43,BLUE,cue.reveal("thirty six bows"))


def poster(draw_frame):
    return draw_frame(7,1)
