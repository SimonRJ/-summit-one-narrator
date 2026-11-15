"""Build recurrences from last moves and follow states through a cycle."""

from functools import lru_cache

from series_marks import (BLUE, GOLD, MINT, MUTED, RED, RIM, WHITE, board, cards, change,
                          chart, cue, equation, exercise, link, move, network, note, ring,
                          scene, tile)
from stage import mix
from studio_diagrams import bead, fit, rail


@lru_cache
def tilings(n):
    if n==0:
        return ((),)
    return tuple(tiles+(length,) for length in (1,2) if length<=n for tiles in tilings(n-length))


def strip(stage, start, y, tiles, size=66, opacity=1, accent_last=False):
    for i,length in enumerate(tiles):
        w=length*size
        face=MINT if accent_last and i==len(tiles)-1 else GOLD if length==2 else BLUE
        stage.box(start+2,y-20,w-4,40,edge=face,fill="#254050",radius=5,opacity=opacity)
        if length==2:
            stage.line([(start+size,y-14),(start+size,y+14)],MUTED,2,opacity*.45)
        start+=w


def list_tilings(stage,s):
    for x,n,words in ((355,4,"the number for length four"),(835,3,"the number for length three")):
        p=cue(s,words)
        rest=5-n
        for i,tiles in enumerate(tilings(n)):
            y=246+i*57
            strip(stage,x-146,y,tiles,54,p)
            strip(stage,x-146+n*54,y,(rest,),54,cue(s,"five plus three",delay=i*.08),True)


def stair_moves(stage,s):
    nodes=[(386+77*i,471-44*i) for i in range(7)]
    for i,(x,y) in enumerate(nodes[:-1]):
        next_x,next_y=nodes[i+1]
        stage.line([(x,y),(next_x,y),(next_x,next_y)],BLUE,4)
    for a,b,label,colour in ((4,6,"Double",GOLD),(5,6,"Single",MINT)):
        p=cue(s,"double" if a==4 else "single step")
        x,y=nodes[a]
        edge=(nodes[b][0],nodes[b][1]-7)
        stage.arrow((x-4,y-22),edge,colour,p)
        fit(stage,label,x-55,y-63,24,155,colour,p)


def cycle(stage,s, *, explain=None):
    pos=ring(4,x=697,y=362,radius=119)
    for i,(a,b) in enumerate(zip(pos,(*pos[1:],pos[0]))):
        p=cue(s,explain,delay=.13*i)
        stage.arrow(a,b,(BLUE,GOLD,MINT,GOLD)[i],p,3)
    for (x,y),text in zip(pos,"ABCD"):
        tile(stage,x,y,text,BLUE,70,57,size=31)


def robot_state(stage,s):
    board(3,5,width=83,y=341)(stage,s)
    p=cue(s,"which way it just moved",duration=.85)
    bead(stage,mix(556,640,p),341,BLUE,1,22)
    stage.arrow((554,341),(645,341),MINT,p,4)
    fit(stage,"×",556,341,36,72,RED,p)
    fit(stage,"Position + direction of the last move",640,556,35,1020,MINT,p)


def game_line(limit, *, start=None, last=10):
    def draw(stage,s):
        xs=[640+(i-last/2)*89 for i in range(last+1)]
        p=cue(s,start)
        rail(stage,xs,349,[str(i) for i in range(last+1)],opacity=p)
        for i,x in enumerate(xs):
            if start=="with one or two counters" and i>3:
                continue
            trigger="three is a losing position" if i==3 and start=="with one or two counters" else start
            if i==0 and start=="with one or two counters":
                continue
            tile(stage,x,306,"L" if i%(limit+1)==0 else "W",GOLD if i%(limit+1)==0 else MINT,
                 60,50,cue(s,trigger,delay=.063*i),27)
    return draw


def dots(n, *, x=640,y=344,s=62,row=None,column=None,show=None):
    def draw(stage,t):
        for r in range(n):
            for c in range(n):
                if row and r==n-1:
                    words,face=row,GOLD
                elif column and c==n-1 and r<n-1:
                    words,face=column,MINT
                elif (row or column) and c==n-1:
                    continue
                else:
                    words,face=show,BLUE
                a=cue(t,words,delay=.045*(r+c),duration=.38)
                bead(stage,x+s*(c-(n-1)/2),y+s*(r-(n-1)/2),face,a,min(22,s*.25))
    return draw


FILMS={
 "T10.1":(
    scene("Build big cases from smaller ones",board(1,4,width=104,y=327),
          lambda stage,s:strip(stage,434,327,(1,2,1),104,cue(s,"how each case is built")),
          note("A rule from smaller cases is a recurrence", "called a recurrence")),
    scene("A short rule replaces a long list",
          cards(("1","1","2","3","5","8","13","21","34","55","89"),343,width=73,gap=90,words="nine small additions",size=26),
          note("89 tilings for a length-10 strip", "eighty-nine ways")),
    scene("How many tilings for five cells?",
          chart(("Length","1","2","3","4","5"),
                [(("Tilings","1","2","3","5","?"),"length four in five ways")],y=211,row_height=93,width=1020),
          board(1,5,width=94,y=434),
          note("A tile covers one or two cells", "pause and look at how a tiling ends",y=553)),
    scene("Sort by how the last tile ends the strip",
          board(1,5,width=78,x=640,y=265,cells=((0,4,MINT,"it is a single"),)),
          board(1,5,width=78,x=640,y=423,cells=((0,3,GOLD,"it is a double"),(0,4,GOLD,"it is a double"))),
          note("4 cells left", "length four",x=287,y=266,width=280,size=29,colour=BLUE),
          note("3 cells left", "length three",x=287,y=425,width=280,size=29,colour=BLUE),
          note("A tiling ends in exactly one of these ways", "exactly one of these")),
    scene("Append a last tile to each smaller case",list_tilings,
          equation(("5",BLUE,"five plus three"),("+ 3",GOLD,"five plus three"),("= 8 tilings",MINT,"is eight"),y=564)),
    scene("Each number adds the previous two",
          cards(("1","2","3","5","8"),261,width=104,gap=128),
          cards(("13","21","34","55","89"),411,width=104,gap=128,face=MINT,words="eight plus five"),
          note("8 + 5 = 13, then 13 + 8 = 21", "then twenty-one")),
    scene("Single and double steps make the same recurrence",stair_moves,
          note("Six stairs can be climbed in 13 ways", "thirteen ways")),
    exercise((("Sort by last move","by their last move"),("Use smaller cases","smaller case"),
              ("Add the counts","add the groups")),"notebook challenge",
             ("How many ways can singles and doubles tile seven cells?",)),
 ),
 "T10.2":(
    scene("A state decides the next step",lambda stage,s:cycle(stage,s,explain="the same state must lead"),
          note("The same state leads to the same next state", "the same next state")),
    scene("Replace a long list with one cycle",lambda stage,s:cycle(stage,s,explain="repeat in a short cycle"),
          note("Only the position inside the cycle matters", "the position inside the cycle")),
    scene("Double, then keep only the last digit",
          cards(("3","6","2","4","8","6"),344,words="the list begins",width=111,gap=138),
          note("The first term is 3", "start with three",y=209,colour=BLUE),
          note("What is the 50th term?", "the fiftieth number")),
    scene("The cycle starts at position two",
          cards((("3",GOLD),"6","2","4","8","6","2","4","8"),338,width=94,gap=115,words="after the first number"),
          note("The first 3 never comes back", "three itself never comes back"),
          link((249,431),(687,431),"the cycle starts",colour=MINT,width=4)),
    scene("Index the repeated block",
          cards((("6",MINT),"2","4","8"),341,width=114,gap=142,words="the first in the cycle"),
          note("Positions 2 through 50 contain 49 terms","forty-nine numbers",y=229,colour=BLUE),
          equation(("49 = 12 × 4",WHITE,"twelve complete cycles"),("+ 1",GOLD,"and one more"),
                   ("   So term 50 is 6",MINT,"first in the cycle"),size=37)),
    scene("One number can be too little information",
          cards(("1","1","2","3","5","8","3","1","4"),322,width=91,gap=108,
                words="last digit of the sum"),
          note("Seeing 1 alone does not determine what follows", "seeing a one",y=441,colour=GOLD),
          note("Keep the previous two digits as the state", "you need the last two numbers")),
    scene("A robot may need to remember its direction",robot_state),
    exercise((("Name the state","decide what the state is"),("Find the first repeat","where a state first repeats"),
              ("Locate the remainder","use a remainder")),"notebook challenge",
             ("Start with 7. Triple each term and keep its last digit.","What is the 30th term?")),
 ),
 "T10.3":(
    scene("Label positions for the player about to move",game_line(2,start="label each position",last=4),
          note("W means winning. L means losing.", "winning or losing",y=509)),
    scene("Work up from small positions",
          cards((("W",MINT),("L",GOLD),("W",MINT)),317,words="labelling positions",width=115,gap=162),
          note("The labels show both the winner and the best move", "the best move")),
    scene("Choose whether to move first",
          cards(("1","2","3","4","5","6","7","8","9","10"),321,width=86,gap=103,
                words="pile of ten",size=27),
          note("Take 1 or 2. The last counter wins.", "whoever takes the last counter",y=461,colour=GOLD),
          note("Would you go first or second?", "would you rather go first",y=545)),
    scene("Three leaves a winning position for the opponent",
          game_line(2,start="with one or two counters"),
          link((466,268),(285,273),"you leave one or two",colour=GOLD,arrow=True),
          link((466,250),(370,261),"you leave one or two",colour=GOLD,arrow=True),
          note("With 1 or 2 you can win immediately", "those are winning positions",y=498,size=33)),
    scene("Winning moves leave a losing position",game_line(2,start="the losing positions"),
          note("From 4 or 5, leave 3 to the other player","from four or five",y=508,colour=GOLD),
          note("The losing piles are multiples of 3","the multiples of three",y=566)),
    scene("Start at ten and leave nine",
          cards((("10",BLUE),("9",GOLD),("6",GOLD),("3",GOLD),("0",MINT)),348,width=112,gap=195,
                words="leaving nine"),
          note("Take 1 first", "go first and take one", y=233, colour=BLUE),
          note("Then make each pair of moves remove 3","makes three altogether")),
    scene("Taking up to three changes the losing piles",game_line(3,start="four is losing"),
          note("Leave a multiple of 4", "the losing positions are the multiples of four")),
    exercise((("Find a losing target","move to a losing one"),("Work from the smallest case","start labelling")),
             "notebook challenge",("You can take 1 or 2 counters. The last counter wins.",
                                   "What should the first player take from 14?")),
 ),
 "T10.E":(
    scene("Grow a square from 3 × 3 to 4 × 4",dots(3,x=405,s=56),dots(4,x=875,s=56),
          note("How many dots are added?", "how many dots are added")),
    scene("The new bottom row has four dots",dots(4,row="add a new bottom row"),
          note("Keep all 9 original dots", "keep the nine original dots")),
    scene("Count the right column without its corner",dots(4,row="now add",column="three more dots"),
          note("The bottom-right dot is already counted", "its bottom dot is already there")),
    scene("Add the new row and column",dots(4,row="four plus three",column="four plus three"),
          equation(("4 + 3 = 7 added",GOLD,"seven dots added"),("    9 + 7 = 16 total",MINT,"nine plus seven"),
                   y=549,size=38)),
    scene("Any larger square adds an odd number of dots",
          dots(6,s=46,row="add a row",column="a column of n"),
          equation(("n + 1",GOLD,"a row of n plus one"),("+ n",BLUE,"a column of n"),
                   ("= 2n + 1",MINT,"two n plus one"),y=563,size=40)),
    exercise((("Keep the old square","the gaps between square numbers"),("Add the next odd number","odd numbers")),
             "then answer",("How many dots are added when a 20 × 20 square grows to 21 × 21?",)),
 ),
}
