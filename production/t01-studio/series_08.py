"""Draw sample spaces, updated branches and probability after new information."""

from series_marks import (BLUE, GOLD, MINT, MUTED, RED, RIM, WHITE, blocks, board, cards,
                          change, chart, cue, equation, link, note, outline, scene, tile)
from stage import mix
from studio_diagrams import bead, fit


def coins(*, show=None, reject=None, remove=(), select=None, chosen=()):
    def draw(stage,s):
        marks=[]
        cells=[]
        for r in range(2):
            for c in range(2):
                i=2*r+c
                marks.append((r,c,"HT"[r]+"HT"[c],RED if i in remove and reject and s.t >= s.at(reject) else WHITE,show))
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
        for value in range(1, 7):
            x = 640 + (value-3.5)*149
            drop = cue(s, "the result is even") if value % 2 else 0
            die(stage, x, 331, value, BLUE, 1-.8*drop, width=106)
            if value % 2:
                stage.line([(x-42,370),(x+42,292)], RED, 4, drop)
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
        p=cue(s,words[i]) if route=="RR" or (route is None and i) else 1
        colour=(RED,BLUE)[i%2]
        on=i in (1,2) and route=="two"
        stage.arrow((origin[0]+74,origin[1]),(x-102,y),MINT if on else colour,p)
        tile(stage,x,y,("RR","RB","BR","BB")[i],MINT if on else colour,199,59,p)
        fit(stage,("1/3","2/3","2/3","1/3")[i],741,y-12,28,110,WHITE,p)
        if route!="RR":
            fit(stage,("1/6","1/3","1/3","1/6")[i],1091,y,31,120,MINT if on else WHITE,p)


def named_coin_pairs(stage, s):
    board(2, 2, width=122, x=662, y=348)(stage, s)
    for i, face in enumerate("HT"):
        fit(stage, face, 601+122*i, 200, 32, 104, GOLD)
        fit(stage, face, 493, 287+122*i, 32, 104, BLUE)
    fit(stage, "Second coin", 661, 162, 27, 286, GOLD)
    fit(stage, "First coin", 360, 345, 28, 178, BLUE)
    start = next(i+1 for i, w in enumerate(s.words) if w["text"].rstrip(":,.").lower() == "outcomes")
    words = [w for w in s.words[start:] if w["text"].rstrip(".,:").lower() in ("head","tail")]
    for i, pair in enumerate(("HH", "HT", "TH", "TT")):
        row, column = divmod(i, 2)
        opacity = max(0, min(1, (s.t-words[2*i]["start"])/.18))
        fit(stage, pair, 601+122*column, 287+122*row, 38, 109, WHITE, opacity)


def different_faces(stage, s):
    challenge = s.t >= s.at("then try")
    fit(stage, "The coins show different faces" if challenge else "Keep outcomes with at least one head",
        640, 87, 44)
    if challenge:
        coins(reject="do not show the same face", remove=(0,3),
              select="the first coin is heads", chosen=(1,))(stage, s)
        fit(stage, "HT and TH survive", 1030, 292, 30, 365, GOLD, cue(s, "the same face"))
        fit(stage, "First head: HT", 1030, 372, 33, 365, MINT, cue(s, "the first coin is heads"))
        fit(stage, "1 out of 2", 1030, 446, 36, 365, MINT, cue(s, "first coin is heads", delay=.22))
    else:
        coins(reject="information removes outcomes", remove=(3,),
              select="the new total", chosen=(0,))(stage, s)
        fit(stage, "HH is 1 of 3", 1025, 337, 34, 363, MINT, cue(s, "the new total"))


different_faces.chapter = "Your turn"


def matching_dice(stage, s):
    challenge = s.t >= s.at("notebook challenge")
    fit(stage, "Matching numbers on two dice" if challenge else "Count ordered pairs", 640, 87, 45)
    width = 53
    centre_x, centre_y = 477, 350
    show = "two dice are rolled" if challenge else "label the objects"
    select = "numbers are the same" if challenge else "then count favourable"
    selected = [(r, c, MINT, select) for r in range(6) for c in range(6)
                if (r == c if challenge else r + c == 5)]
    board(6, 6, width=width, x=centre_x, y=centre_y, cells=selected)(stage, s)
    for i in range(6):
        fit(stage, str(i + 1), centre_x + (i - 2.5) * width, 164, 25, 48, GOLD, cue(s, show))
        fit(stage, str(i + 1), centre_x - 191, centre_y + (i - 2.5) * width, 25, 48, BLUE, cue(s, show))
    fit(stage, "Die 1", 198, centre_y, 26, 124, BLUE, cue(s, show))
    fit(stage, "Die 2", centre_x, 128, 26, 140, GOLD, cue(s, show))
    fit(stage, "36 equally likely pairs", 916, 285, 34, 470, WHITE,
        cue(s, show if challenge else "equally likely"))
    fit(stage, "6 matching pairs" if challenge else "6 pairs total seven", 916, 373, 35, 490, MINT, cue(s, select))
    fit(stage, "6 / 36 = 1 / 6", 916, 461, 39, 465, GOLD, cue(s, select, delay=.3))


matching_dice.chapter = "Your turn"


def draw_again(stage, s):
    challenge = s.t >= s.at("notebook challenge")
    fit(stage, "Draw two red counters" if challenge else "Track the changing bag", 640, 87, 46)
    first = (RED, RED, RED, BLUE) if challenge else (RED, RED, BLUE, BLUE)
    when = "three red counters" if challenge else "update the situation"
    after = "without replacement" if challenge else "multiply along a route"
    for row, (colours, label, phrase) in enumerate(((first, "First draw", when),
                                                   (first[1:], "After a red", after))):
        y = 253 + 152 * row
        p = cue(s, phrase)
        fit(stage, label, 199, y, 31, 230, WHITE, p)
        stage.box(336, y-49, 400, 98, edge=RIM, fill=None, opacity=p)
        for j, colour in enumerate(colours):
            bead(stage, 397 + j*91, y, colour, p, 26)
        fit(stage, ("3 red / 4" if challenge else "2 red / 4") if row == 0 else
            ("2 red / 3" if challenge else "1 red / 3"), 954, y, 36, 389, RED, p)
    if not challenge and s.t >= s.at("add separate routes"):
        fit(stage, "RB or BR: 1/3 + 1/3 = 2/3", 640, 551, 37, 1070, MINT,
            cue(s, "add separate routes"))
    elif challenge:
        fit(stage, "(3/4) × (2/3) = 1/2", 640, 551, 40, 1010, MINT, cue(s, "both are red"))
    else:
        fit(stage, "RR: (2/4) × (1/3) = 1/6", 640, 551, 39, 1020, MINT, cue(s, after))


draw_again.chapter = "Your turn"


def odd_survivors(stage, s):
    challenge = s.t >= s.at("notebook challenge")
    fit(stage, "An odd result given a roll above two" if challenge else "Filter an even roll", 640, 87, 45)
    given = "greater than two" if challenge else "cross out"
    want = "it is odd" if challenge else "among the survivors"
    for value in range(1, 7):
        x = 640 + (value - 3.5) * 153
        survives = value > 2 if challenge else value % 2 == 0
        favourable = survives and (value % 2 == 1 if challenge else value > 3)
        p = cue(s, given)
        q = cue(s, want)
        die(stage, x, 326, value, MINT if favourable and q > .2 else BLUE,
            1 if survives else 1 - .78*p, width=108)
        if not survives:
            stage.line([(x-42,366),(x+42,286)],RED,4,p)
    fit(stage, "4 survivors: 3, 4, 5, 6" if challenge else "3 survivors: 2, 4, 6",640,466,33,950,WHITE,cue(s,given))
    fit(stage, "Odd: 3 and 5     2/4 = 1/2" if challenge else "Above three: 4 and 6     2/3",
        640,548,36,1020,MINT,cue(s,want))


odd_survivors.chapter = "Your turn"


FILMS = {
    "T08.1": (
        scene("Count equally likely outcomes",bag((RED,RED,BLUE),words="two red counters"),
              note("Two of the three counters are red", "two of them are red")),
        scene("Colours are names, counters are outcomes",
              cards((("Red",RED),("Blue",BLUE)),248,width=180,gap=285,words="counting names"),
              bag((RED,RED,BLUE),words="real outcomes",centre=640,y=407),
              note("2 red counters among 3 equally likely draws", "then count")),
        scene("Two fair coins, exactly one head?",
              cards(("Coin 1","Coin 2"),253,words="toss two fair coins",width=195,gap=244),
              cards(("Two heads","One head","No heads"),407,words="there are three results",width=236,gap=267,
                    face=GOLD,size=31),
              note("Are these three results equally likely?", "whether that is right")),
        scene("Keep the coins distinct",named_coin_pairs),
        scene("Two outcomes have exactly one head",coins(chosen=(1,2),select="head tail and tail head"),
              equation(("2 out of 4",BLUE,"two out of four"),("= 1/2",MINT,"one half"),y=552)),
        scene("On two dice, the pairs are equally likely",
              change("a total of two",
                     (dice_space(7,"a total of seven"),note("Sum 7 in 6 cells","six out of thirty-six",
                         x=1030,y=350,width=332,size=33)),
                     (dice_space(2,"a total of two"),note("Sum 2 in 1 cell","only one pair",
                         x=1030,y=350,width=332,size=33))),
              note("The totals are not equally likely", "the totals are not equally likely",y=565,size=34)),
        matching_dice,
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
        draw_again,
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
        odd_survivors,
    ),
    "T08.E": (
        scene("Two coins and at least one head",
              cards(("Coin 1","Coin 2"),332,words="two fair coins",width=209,gap=271),
              note("With at least one head, what is the chance of two?", "both show heads")),
        scene("Make the four outcomes visible",named_coin_pairs,
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
        different_faces,
    ),
}
