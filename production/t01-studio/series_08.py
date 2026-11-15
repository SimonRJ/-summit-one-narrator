"""Draw sample spaces, updated branches and probability after new information."""

from series_marks import (BLUE, GOLD, MINT, MUTED, RED, RIM, WHITE, blocks, board, cards,
                          change, chart, cue, equation, exercise, link, note, outline, scene, tile)
from stage import mix
from studio_diagrams import bead, fit


def coins(*, show=None, reject=None, remove=(), select=None, chosen=()):
    def draw(stage,s):
        marks=[]
        cells=[]
        for r in range(2):
            for c in range(2):
                i=2*r+c
                marks.append((r,c,"HT"[r]+"HT"[c],RED if i in remove else WHITE,show))
                if i in chosen:
                    cells.append((r,c,MINT,select))
        board(2,2,width=122,x=662,y=348,cells=cells,marks=marks)(stage,s)
        for i in range(2):
            fit(stage,"HT"[i],600+122*i,200,32,104,GOLD)
            fit(stage,"HT"[i],493,287+122*i,32,104,BLUE)
        fit(stage,"Second coin",661,162,27,286,GOLD)
        fit(stage,"First coin",360,345,28,178,BLUE)
        if reject:
            for i in remove:
                r,c=divmod(i,2)
                x,y=601+122*c,287+122*r
                p=cue(s,reject)
                stage.line([(x-42,y+35),(x+42,y-35)],RED,4,p)
    return draw


def dice_space(target, words, *, selected=None, focus=None):
    def draw(stage,s):
        w=52
        y=353
        left,top=598-3*w,y-3*w
        marks=[(r,c,str(r+c+2),WHITE,None) for r in range(6) for c in range(6)]
        cells=[(r,c,BLUE,words) for r in range(6) for c in range(6) if r+c+2==target]
        if selected:
            r,c=selected
            cells.append((r,c,MINT,focus))
        board(6,6,width=w,x=598,y=y,cells=cells,marks=marks)(stage,s)
        for i in range(6):
            fit(stage,str(i+1),left+(i+.5)*w,177,24,52,GOLD)
            fit(stage,str(i+1),left-30,top+(i+.5)*w,24,52,BLUE)
        fit(stage,"Die 1",left-121,y,28,112,BLUE)
        fit(stage,"Die 2",598,141,27,170,GOLD)
    return draw


PIPS = {
    1: ((0,0),),
    2: ((-1,-1),(1,1)),
    3: ((-1,-1),(0,0),(1,1)),
    4: ((-1,-1),(-1,1),(1,-1),(1,1)),
    5: ((-1,-1),(-1,1),(0,0),(1,-1),(1,1)),
    6: ((-1,-1),(-1,0),(-1,1),(1,-1),(1,0),(1,1)),
}


def die(stage,x,y,n,colour=BLUE,opacity=1,width=97):
    stage.box(x-width/2,y-width/2,width,width,fill="#233a4b",edge=colour,radius=12,opacity=opacity,stroke=3)
    for a,b in PIPS[n]:
        stage.dot(x+a*width*.26,y+b*width*.26,width*.068,colour,opacity)


def roll_filter(stage,s, *, question=False, filter_word=None, favour=None):
    if question:
        tile(stage,640,318,"?",GOLD,119,119,size=58)
        return
    drop=cue(s,filter_word) if filter_word else 0
    chosen=cue(s,favour) if favour else 0
    for v in range(1,7):
        x=640+(v-3.5)*149
        p=1
        if v%2:
            p=1-.90*drop
        elif v in (4,6):
            x=mix(x,640+((v-4)//2)*197,chosen)
        elif v==2:
            x=mix(x,443,chosen)
        die(stage,x,331,v,MINT if v in (4,6) and chosen>.1 else BLUE,p,width=106)
        if v%2:
            stage.line([(x-42,370),(x+42,292)],RED,4,drop*(1-chosen))


def bag(colours, *, words=None, remove=None, centre=640, y=341):
    def draw(stage,s):
        stage.box(centre-216,y-87,432,174,radius=21,fill=None,edge=RIM,stroke=3)
        for i,colour in enumerate(colours):
            p=cue(s,words,delay=i*.13)
            out=cue(s,remove,duration=.94) if remove and i==0 else 0
            x=centre+(i-(len(colours)-1)/2)*94
            bead(stage,mix(x,centre+345,out),mix(y,y-55,out),colour,p,28)
    return draw


def colour_tree(stage,s, *, full=False, route=None):
    root=(259,342)
    mids=((561,253),(561,433))
    out=((933,200),(933,289),(933,396),(933,485))
    tile(stage,*root,"Draw 1",WHITE,160,67)
    for i,label in enumerate(("Red","Blue")):
        colour=(RED,BLUE)[i]
        x,y=mids[i]
        p=cue(s,"two of the four" if not full else None)
        stage.arrow((root[0]+82,root[1]),(x-73,y),colour,p)
        tile(stage,x,y,label,colour,146,62,p)
        fit(stage,"1/2",404,y+(-22 if i==0 else 22),33,100,colour,p)
    if not full:
        return
    words=("red again","red then blue","blue then red","blue then blue")
    for i,(x,y) in enumerate(out):
        if route=="RR" and i!=0:
            continue
        origin=mids[i//2]
        p=cue(s,words[i] if route=="RR" or not route and i else None)
        colour=(RED,BLUE)[i%2]
        on=i in (1,2) and route=="two"
        stage.arrow((origin[0]+74,origin[1]),(x-102,y),MINT if on else colour,p)
        tile(stage,x,y,("RR","RB","BR","BB")[i],MINT if on else colour,199,59,p)
        fit(stage,("1/3","2/3","2/3","1/3")[i],741,y-12,28,110,WHITE,p)
        if route!="RR":
            fit(stage,("1/6","1/3","1/3","1/6")[i],1091,y,31,120,MINT if on else WHITE,p)


FILMS = {
    "T08.1": (
        scene("Count equally likely outcomes",bag((RED,RED,BLUE),words="two red counters"),
              note("Two of the three counters are red", "two of them are red")),
        scene("Colours are names, counters are outcomes",
              cards((("Red",RED),("Blue",BLUE)),254,width=151,gap=185,words="counting names"),
              cards((("Red 1",RED),("Red 2",RED),("Blue 1",BLUE)),402,width=161,gap=196,
                    words="genuinely are equally likely"),
              note("Use the three equally likely counters", "then count")),
        scene("Two fair coins, exactly one head?",
              cards(("Coin 1","Coin 2"),253,words="toss two fair coins",width=195,gap=244),
              cards(("Two heads","One head","No heads"),407,words="there are three results",width=236,gap=267,
                    face=GOLD,size=31),
              note("Are these three results equally likely?", "whether that is right")),
        scene("Keep the coins distinct",coins(show="four outcomes")),
        scene("Two outcomes have exactly one head",coins(chosen=(1,2),select="head tail and tail head"),
              equation(("2 out of 4",BLUE,"two out of four"),("= 1/2",MINT,"one half"),y=552)),
        scene("On two dice, the pairs are equally likely",
              change("a total of two",
                     (dice_space(7,"a total of seven"),note("Sum 7 in 6 cells","six out of thirty-six",
                         x=1030,y=350,width=332,size=33)),
                     (dice_space(2,"a total of two"),note("Sum 2 in 1 cell","only one pair",
                         x=1030,y=350,width=332,size=33))),
              note("The totals are not equally likely", "the totals are not equally likely",y=565,size=34)),
        exercise((("Label each object","label the objects"),("Check equal likelihood","check the outcomes"),
                  ("Favourable out of total","then count")),"notebook challenge",
                 ("Roll two fair dice independently.", "What is the probability of a matching pair?")),
    ),
    "T08.2": (
        scene("A draw changes the bag",bag((RED,RED,BLUE,BLUE),remove="do not put it back"),
              note("The second draw starts with 3 counters", "the second draw is from")),
        scene("Update the bag after the first draw",
              bag((RED,RED,BLUE,BLUE),remove="updating after each step"),
              note("Use the counters that are still in the bag", "updating after each step")),
        scene("What is the chance of two reds?",bag((RED,RED,BLUE,BLUE),words="two red counters"),
              note("Draw twice at random, without replacement", "without putting the first back")),
        scene("Start with the first draw",colour_tree,
              equation(("2 red",RED,"two of the four"),("out of 4",WHITE,"two out of four"),
                       ("= 1/2",MINT,"one half"))),
        scene("Follow the red, then red route",
              lambda stage,s:colour_tree(stage,s,full=True,route="RR"),
              cards((("R",RED),("B",BLUE),("B",BLUE)),419,x=946,gap=80,width=62,height=53,
                    words="one red and two blue",size=24),
              equation(("1/2 × 1/3",WHITE,"one half times one third"),("= 1/6",MINT,"is one sixth"))),
        scene("Every possible route belongs in the tree",
              lambda stage,s:colour_tree(stage,s,full=True),
              equation(("1/6 + 1/3 + 1/3 + 1/6",WHITE,"four routes add"),("= 1",MINT,"add to one"),
                       y=573,size=38)),
        scene("One of each colour can happen two ways",
              lambda stage,s:colour_tree(stage,s,full=True,route="two"),
              equation(("1/3 + 1/3",WHITE,"one third plus one third"),("= 2/3",MINT,"two thirds"))),
        exercise((("Update the bag","update the situation"),("Multiply along a route","multiply along"),
                  ("Add separate routes","add separate routes")),"notebook challenge",
                 ("A bag has 3 red counters and 1 blue.","Draw twice without replacement. What is the chance of two reds?")),
    ),
    "T08.3": (
        scene("New information rules out outcomes",
              lambda stage,s:roll_filter(stage,s,filter_word="cross out every outcome"),
              note("Count again among the survivors", "what is left")),
        scene("The denominator changes",cards((("Original total",BLUE),("Surviving total",MINT)),342,
              words="the old total",width=332,gap=406),link((589,342),(683,342),"after information arrives",arrow=True),
              note("The denominator counts only possible outcomes", "the number of outcomes that survive")),
        scene("The die result is known to be even",lambda stage,s:roll_filter(stage,s,question=True),
              note("What is the chance it is greater than 3?", "greater than three")),
        scene("Keep only 2, 4 and 6",lambda stage,s:roll_filter(stage,s,filter_word="removes one three and five"),
              note("Three equally likely outcomes survive", "three outcomes survive")),
        scene("Two of the three survivors fit",
              lambda stage,s:roll_filter(stage,s,filter_word="of those three",favour="four and six"),
              equation(("2 out of 3",MINT,"two out of three"),("   instead of 3 out of 6",MUTED,"without the information"),
                       y=540,size=40)),
        scene("Condition on the total of two dice",dice_space(8,"five pairs survive",selected=(3,3),focus="only four and four"),
              note("1 match among 5 pairs", "one out of five",x=1028,y=349,width=371,size=34),
              note("Given that the sum is 8", "you are told the total",y=566)),
        scene("Count only when each survivor is equally likely",
              blocks(((1,"1/2",BLUE,None),(1,"1/2",MINT,None)),y=280,width=550,
                     words="equally likely before"),
              blocks(((1,"1/4",BLUE,None),(3,"3/4",GOLD,None)),y=420,width=550,
                     words="not equally likely"),
              note("With unequal chances, compare the probabilities", "compare their probabilities")),
        exercise((("Cross out ruled-out cases","cross out"),("Count the survivors","among the survivors")),
                 "notebook challenge",("A fair die shows a number greater than 2.",
                                       "What is the probability it is odd?")),
    ),
    "T08.E": (
        scene("Two coins and at least one head",
              cards(("Coin 1","Coin 2"),332,words="two fair coins",width=209,gap=271),
              note("With at least one head, what is the chance of two?", "both show heads")),
        scene("Make the four outcomes visible",coins(show="four equally likely"),
              note("Each pair originally has probability 1/4", "tail tail")),
        scene("At least one head rules out tail–tail",
              coins(reject="rules out tail tail",remove=(3,),select="three outcomes survive",chosen=(0,1,2)),
              note("Three equally likely outcomes survive", "are still equally likely")),
        scene("One of the survivors is head–head",
              coins(reject="only one",remove=(3,),select="only one",chosen=(0,)),
              equation(("1 out of 3",MINT,"one out of three"))),
        scene("Knowing the first coin gives a different total",
              coins(reject="only head head and head tail",remove=(2,3),select="probability of two heads",chosen=(0,)),
              equation(("1 out of 2",MINT,"one half"))),
        exercise((("Remove ruled-out outcomes","information removes"),("Use the new total","the new total")),
                 "then try",("Two fair coins show different faces.","What is the probability the first coin shows heads?")),
    ),
}
