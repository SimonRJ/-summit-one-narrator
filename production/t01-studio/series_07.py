"""Prove an upper or lower bound and build an arrangement that reaches it."""

import math

from series_marks import (BLUE, GOLD, MINT, RED, RIM, WHITE, board, cards, change, chart, cue,
                          equation, exercise, note, scene)
from stage import blend, mix
from studio_diagrams import bead, fit


PAIRS = (BLUE, GOLD, MINT, BLUE, GOLD)
SQUARE_EIGHT = tuple((r, c if r < 2 else c + 2) for r in range(4) for c in (0, 1))
TRAYS = ("RRBB", "RRB", "RRB", "R")


def cells(count, *, paired=False, occupied=(), place=None, cover=()):
    width=98
    left=640-count*width/2
    bands=[]
    if paired:
        bands=[(0,c,PAIRS[c//2],None) for c in range(count)]
    if cover:
        bands=[(0,i,(BLUE,GOLD,MINT)[i//3],cover) for i in range(count)]
    base=board(1,count,width=width,y=359,cells=bands)

    def draw(stage,s):
        base(stage,s)
        for i in range(count):
            xx=left+(i+.5)*width
            fit(stage,str(i+1),xx,441,24,92,WHITE)
        for j,i in enumerate(occupied):
            t=cue(s,place,delay=.12*j,duration=.70)
            bead(stage,left+(i-.5)*width,mix(240,359,t),MINT,t,24)
        if paired:
            for i in range(0,count,2):
                stage.bracket(left+i*width+4,left+min(count,i+2)*width-4,485,"≤ 1",PAIRS[i//2])
    return draw


def moving_rectangle(stage,s):
    p=cue(s,"the sides become more equal",duration=1.50)
    long,short=11-5*p,1+5*p
    w,h=39*long,39*short
    stage.box(640-w/2,337-h/2,w,h,edge=BLUE,fill="#244153",radius=2,stroke=4)
    if p < .05:
        fit(stage,"1 × 11",640,486,36,450,BLUE)
    elif p > .95:
        fit(stage,"6 × 6",640,486,36,450,BLUE)
    fit(stage,"The side lengths still add to 12",640,548,37,1050,MINT)


def pair_products(stage,s):
    readings=("one and eleven","two and ten","three and nine","four and eight","five and seven","six and six")
    for i,when in enumerate(readings,1):
        y=211+(i-1)*61
        p=cue(s,when)
        area=i*(12-i)
        colour=MINT if i==6 else BLUE
        fit(stage,f"{i} × {12-i}",238,y,31,235,WHITE,p)
        stage.box(385,y-20,area*17*p+1,40,fill="#294956",edge=colour,radius=4,opacity=p)
        fit(stage,str(area),1036,y,31,105,colour,p)


def lost_square(stage,s):
    p=cue(s,"move a strip",duration=1.45)
    q=cue(s,"a small square of side")
    stage.box(333,250,168,252,fill="#294956",edge=BLUE,radius=2,stroke=3)
    x,y=mix(543,459,p),mix(376,208,p)
    angle=-p*math.pi/2
    points=[]
    for u,v in ((-42,-126),(42,-126),(42,126),(-42,126)):
        points.append((int(stage.px(x+u*math.cos(angle)-v*math.sin(angle))),
                       int(stage.px(y+u*math.sin(angle)+v*math.cos(angle)))))
    stage.draw.polygon(points,fill=blend("#294956",GOLD,.38),outline=GOLD,width=stage.px(3))
    # In this example d is two units. The new rectangle excludes the two-by-two offcut.
    if p>.95:
        stage.box(501,166,84,84,radius=2,fill="#53333b",edge=RED,opacity=q,stroke=3)
        fit(stage,"d²",543,208,30,77,RED,q)
        stage.bracket(333,501,523,"6 − d",BLUE,q)
        fit(stage,"6 + d",278,350,30,151,BLUE,q)
    else:
        fit(stage,"6",279,365,30,100,BLUE)
    fit(stage,"(6 − d)(6 + d)",928,346,45,545,WHITE,cue(s,"write the two numbers"))
    fit(stage,"= 36 − d²",928,440,50,545,MINT,cue(s,"minus d squared"))


def columns(stage,s, *, failed=False,moving=False,check=False):
    x,y,w=535,338,77
    board(4,4,x=x,y=y,width=w)(stage,s)
    shift=cue(s,"rows three and four",duration=.87) if moving else 0
    show=cue(s,"exactly two counters") if failed else 1
    for i,(r,c) in enumerate(SQUARE_EIGHT):
        start=i%2
        col=start if failed else mix(start,c,shift) if moving else c
        p=cue(s,"rows one and two",delay=.12*i) if moving else show
        bead(stage,x+(col-1.5)*w,y+(r-1.5)*w,(BLUE,GOLD)[r//2],p,22)
    for i in range(4):
        word="would break the column rule" if failed else "every column has two" if moving else "every column"
        n = (4 if i<2 else 0) if failed else 2
        fit(stage,str(n),x+(i-1.5)*w,525,31,66,RED if failed and i<2 else MINT,cue(s,word))
        if check:
            fit(stage,"2",735,y+(i-1.5)*w,28,90,MINT,cue(s,"every row"))


def packing(stage,s, mode):
    if mode=="question":
        for i in range(11):
            bead(stage,230+82*i,286,RED if i<7 else BLUE,cue(s,"pack seven red",delay=.086*i),23)
        stage.box(405,370,470,95,fill=None,edge=RIM)
        for i in range(4):
            stage.dot(465+116*i,417,18,RIM,cue(s,"holds at most four"))
        return
    if mode=="filled":
        n=4
        contents=TRAYS
    elif mode=="red":
        n=3
        contents=("RR","RR","RR")
    else:
        n=3
        contents=("RRRR","RRRB","BBB")
    for i, contents_row in enumerate(contents):
        x=640+(i-(n-1)/2)*269
        stage.box(x-120,296,240,108,fill=None,edge=GOLD if mode=="red" else MINT)
        for j in range(4):
            if mode=="red" and j>=2:
                continue
            xx=x+54*(j-1.5)
            if j>=len(contents_row):
                stage.dot(xx,349,14,RIM)
            else:
                colour = WHITE if mode=="total" else RED if contents_row[j]=="R" else BLUE
                when="fill them like this" if mode=="filled" else "only six reds" if mode=="red" else "there are eleven counters"
                bead(stage,xx,349,colour,cue(s,when,delay=(i*4+j)*.11),18)
    if mode=="red":
        bead(stage,1021,466,RED,cue(s,"and there are seven"),23)
        fit(stage,"One red still needs a place",710,465,29,564,RED,cue(s,"and there are seven"))


FILMS = {
    "T07.1": (
        scene("What resource limits the arrangement?",cells(8),
              note("A proof explains why nobody could do better","why nobody could ever do better")),
        scene("Making four fit is only half the proof",cells(8,occupied=(1,3,5,7),place="finding a good arrangement"),
              note("Could another arrangement fit five?", "a cleverer arrangement")),
        scene("How many counters can fit?",cells(8),
              note("One per cell at most", "at most one per cell",y=503,colour=BLUE),
              note("No two counters in neighbouring cells", "no two counters",y=568)),
        scene("Each pair has room for at most one",cells(8,paired=True),
              equation(("4 pairs",BLUE,"four pairs means"),("× 1",GOLD,"at most one counter"),
                       ("= 4 counters at most",MINT,"at most four counters"),y=579,size=39)),
        scene("Reach the bound with separated counters",cells(8,occupied=(1,3,5,7),place="cells one three five and seven"),
              note("The largest possible number is 4", "the largest number is four")),
        scene("An extra cell creates an extra place",cells(9,paired=True,occupied=(1,3,5,7,9),
              place="cells one three five seven and nine"),
              note("Four pairs and one single cell allow at most 5", "at most five",y=578)),
        scene("For a minimum, count what each counter covers",
              cells(8,occupied=(2,5,8),place="cells two five and eight",cover="that coverage"),
              equation(("8 cells",BLUE,"eight cells"),("÷ up to 3 per counter",GOLD,"at most three cells"),
                       ("needs at least 3",MINT,"at least three counters"),y=565,size=36)),
        exercise((("Find the resource","find what is limited"),("Prove a limit","use it to prove"),
                 ("Reach it","show an arrangement")),"notebook challenge",
                 ("Eleven cells in a row, with no neighbouring counters.","What is the largest number that can fit?")),
    ),
    "T07.2": (
        scene("Equal sides enclose more area",moving_rectangle),
        scene("A pattern needs a reason",cards(("1 × 11","3 × 9","5 × 7"),309,
              words="trying examples",width=197,gap=239),
              note("What happens when perfect balance is forbidden?","perfect balance is not allowed")),
        scene("Find the largest product with sum 12",
              cards(("First part","Second part"),332,words="two positive",width=255,gap=330),
              note("Both parts are positive whole numbers", "add to twelve",y=454,colour=BLUE),
              note("How large can their product be?", "largest their product")),
        scene("Products grow as their factors get closer",pair_products),
        scene("The unequal rectangle loses a square",lost_square),
        scene("If the numbers differ, try the closest pair",
              cards((("6 × 6",RED),("5 × 7",MINT)),316,width=215,gap=338),
              note("Not allowed", "no longer allowed",x=472,y=417,colour=RED,width=288),
              note("Largest allowed product", "the most balanced pair",x=808,y=417,colour=MINT,width=349,size=26),
              note("5 × 7 = 35", "giving thirty-five")),
        scene("Changing the number of parts changes the comparison",
              cards(("4","4","4"),258,width=115,gap=137,words="three fours"),
              cards((("3",GOLD),)*4,397,width=115,gap=137,words="four threes"),
              note("64", "sixty-four",x=999,y=258,colour=BLUE,width=131,size=47),
              note("81", "eighty-one",x=999,y=397,colour=GOLD,width=131,size=47),
              note("Check how many parts are allowed", "check how many parts")),
        exercise((("Fix the sum","with a fixed total"),("Balance the two parts","the most balanced pair"),
                  ("Check restrictions","a rule forbids")),"notebook challenge",
                 ("A rectangle has whole-number sides and perimeter 22.","Find the largest possible area.")),
    ),
    "T07.3": (
        scene("A tight bound tells you how to build",
              board(1,4,width=142,y=321,cells=tuple((0,c,BLUE,"reach the limit exactly") for c in range(4))),
              note("Use every available place", "nothing in the proof may be wasted")),
        scene("Use the bound to direct your search",
              cards((("Find the limit",BLUE),("Find what must be full",GOLD),("Build to match",MINT)),
                    343,words="letting the proof guide you",width=278,gap=307,size=29),
              note("Does the construction actually reach the bound?", "whether the limit can be reached")),
        scene("Place counters on a 4 × 4 board",board(4,4,width=77,y=337),
              note("At most 2 in every row and every column","each row may contain",y=535,size=34),
              note("What is the largest total?", "largest number of counters",y=585,size=32)),
        scene("The row rule gives a ceiling",board(4,4,x=410,width=75,y=343),
              chart(("Row","Capacity"),[((str(i+1),"2"),"each holds at most two") for i in range(4)],
                    x=905,y=205,row_height=61,width=518),
              note("4 × 2 = 8 counters at most","at most eight counters",y=571)),
        scene("Filling the rows can still break the column rule",lambda stage,s:columns(stage,s,failed=True),
              note("The first two columns would each contain 4", "would break the column rule",
                   x=974,y=345,width=400,size=27,colour=RED)),
        scene("Spread the rows across the columns",lambda stage,s:columns(stage,s,moving=True),
              note("Each row and column has 2", "every row has two",x=966,y=382,width=387,size=28),
              note("8 counters", "eight is reached",x=966,y=472,width=310,size=37)),
        scene("Check every rule",lambda stage,s:columns(stage,s,check=True),
              note("At most one in each square", "every square passes",x=961,y=354,width=423,size=29),
              note("All eight counters fit", "every row",x=961,y=459,width=365,size=32)),
        exercise((("Prove the limit","prove the limit"),("Find what must be full","ask what must be full"),
                  ("Build and check","build the arrangement")),"notebook challenge",
                 ("On a 3 × 3 board, allow at most 1 counter in each row and column.",
                  "What is the largest total, and where can the counters go?")),
    ),
    "T07.E": (
        scene("Pack 7 red and 4 blue counters",lambda stage,s:packing(stage,s,"question"),
              note("At most 4 per tray, including at most 2 reds", "at most two of them may be red",y=530,size=35),
              note("What is the smallest number of trays?", "smallest number of trays",y=581,size=31)),
        scene("First bound from the total space",lambda stage,s:packing(stage,s,"total"),
              note("Two trays hold at most 8 of the 11 counters", "two trays are not enough",y=470,colour=BLUE,size=34),
              note("At least 3 trays", "at least three trays")),
        scene("A stronger bound from the red places",lambda stage,s:packing(stage,s,"red"),
              note("At least 4 trays", "at least four trays")),
        scene("Four trays can hold all eleven",lambda stage,s:packing(stage,s,"filled"),
              note("7 red and 4 blue, with both rules satisfied","all eleven counters are packed")),
        scene("The red limit decides",cards((("3 trays: up to 6 red",RED),("4 trays: all 7 red",MINT)),
              362,width=412,gap=470,words="four trays are enough",size=30),
              note("The minimum is 4 trays", "the answer is four")),
        exercise((("Find each lower bound","each rule for a lower bound"),("Use the strongest bound","the strongest bound"),
                  ("Build a packing","build a packing")),
                 "try it with",("Pack 9 red counters and 3 blue counters.","Allow at most 4 per tray and at most 2 red."),
                 sub="Find the minimum number of trays and build an example."),
    ),
}
