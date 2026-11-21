"""Count orders, disjoint cases and reversible arrangements."""

from itertools import combinations

from series_marks import (BLUE, GOLD, MINT, MUTED, RED, WHITE, cards,
                          chart, cue, equation, exercise, link, move, note, outline, scene, tile)
from stage import mix
from studio_diagrams import fit


A, B, C = (("A", BLUE), ("B", GOLD), ("C", MINT))
RACE = ((A, B), (A, C), (B, C))


def podium(stage, s):
    p = cue(s, "swapping the two people", duration=.85)
    q = cue(s, "in a team")
    for i, (x, heading) in enumerate(((300, "1st"), (511, "2nd"))):
        tile(stage, x, 426, heading, BLUE, 158, 73)
        label, colour = (A, B)[i]
        target = (511, 300)[i]
        tile(stage, mix(x, target, p), 328 + (2 * i - 1) * 84 * p * (1 - p),
             label, colour, 109, 62, cue(s, "choosing a winner"))
    stage.box(721, 287, 369, 136, fill=None, edge=MINT, opacity=q)
    for x, (name, colour) in zip((826, 986), (A, B)):
        tile(stage, x, 352, name, colour, 115, 65, q)
    fit(stage, "One team", 905, 457, 33, 300, MINT, q)


def ordered_cards(stage, s):
    pairs = ("AB", "AC", "BA", "BC", "CA", "CB")
    for i, pair in enumerate(pairs):
        g = i // 2
        p = cue(s, "then two remaining", delay=.13*i)
        tile(stage, 329 + 311*g + 72*(i % 2 - .5), 398, pair, (BLUE, GOLD, MINT)[g],
             64, 54, p, 26)


def merge_pairs(stage, s):
    p = cue(s, "merge in pairs", duration=1.0)
    for i, (a, b) in enumerate(RACE):
        x = 311 + 329*i
        y = 364
        tile(stage, mix(x - 64, x, p), mix(275, y, p), a[0]+b[0], BLUE, 104, 66, 1-p)
        tile(stage, mix(x + 64, x, p), mix(275, y, p), b[0]+a[0], GOLD, 104, 66, 1-p)
        tile(stage, x, y, "{"+a[0]+", "+b[0]+"}", MINT, 151, 87, p)


def triples(stage, s):
    p = cue(s, "six orders")
    q = cue(s, "ten groups")
    labels=("ABC","ACB","BAC","BCA","CAB","CBA")
    for i, label in enumerate(labels):
        x = mix(266+i*150, 640, q)
        tile(stage, x, mix(325, 290, q), label, BLUE, 111, 64, p*(1-q), 28)
    for i, group in enumerate(combinations("ABCDE", 3)):
        tile(stage, 339+(i%5)*150, 319+(i//5)*82, "".join(group), MINT, 113, 60,
             cue(s, "ten groups", delay=.07*i), 29)


def pair_challenge(stage, s):
    if s.t < s.at("notebook challenge"):
        fit(stage, "Count the roles, then the teams", 640, 90, 48)
        cards((("AB", BLUE), ("BA", GOLD)), 265, words="positions or roles differ", gap=220)(stage, s)
        link((530, 306), (625, 400), "only membership matters")(stage, s)
        link((750, 306), (655, 400), "only membership matters")(stage, s)
        tile(stage, 640, 446, "{A, B}", MINT, 180, 70, cue(s, "divide by the number"))
        return
    fit(stage, "Six players", 640, 90, 48)
    for i, name in enumerate("ABCDEF"):
        tile(stage, 265 + 150*i, 208, name, BLUE, 105, 66, cue(s, "from six players", delay=.06*i))
    for y, label, detail, words, colour in (
        (358, "Captain and vice-captain", "6 × 5 = 30", "a captain and a vice-captain", GOLD),
        (484, "Two equipment carriers", "30 ÷ 2 = 15", "carry the equipment", MINT),
    ):
        p = cue(s, words)
        fit(stage, label, 405, y, 36, 570, colour, p)
        fit(stage, detail, 925, y, 40, 405, colour, p)


pair_challenge.chapter = "Your turn"


FILMS = {
    "T05.1": (
        scene("Does order matter?", podium,
              note("Different podium places", "on the podium", x=405, y=505, width=427, size=31),
              note("Same team members", "swapping them changes nothing", x=900, y=505, width=416, size=31)),
        scene("The wording decides whether to count a swap", cards((("AB",BLUE),("BA",GOLD)), 251, gap=200),
              link((540,295),(640,410),"or halves it",colour=MINT),
              link((740,295),(640,410),"or halves it",colour=MINT),
              note("Two distinct people · two podium orders", x=640, y=155, size=31),
              cards((("{A, B}",MINT),), 452, words="or halves it", width=171),
              note("Two orders can describe one team", "decide about order")),
        scene("Three runners, two different counts", cards((A, B, C), 237, words="ava ben and cal"),
              note("How many ways to fill first and second?", "in how many ways", y=389, colour=BLUE),
              note("How many teams of two?", "how many different pairs", y=478, colour=GOLD)),
        scene("Choose first place, then second", cards((A, B, C), 249, words="three choices for first",
              gap=311, width=104), ordered_cards,
              equation(("3", BLUE, "three choices"), ("×", WHITE, "then two"), ("2", GOLD, "then two"),
                       ("= 6 ordered results", MINT, "six ordered results"))),
        scene("Pair the orders that name the same team", merge_pairs,
              equation(("6 ÷ 2", WHITE, "merge in pairs"), ("= 3 teams", MINT, "leaving three teams"))),
        scene("Choose three of five people", cards(tuple("ABCDE"), 197, words="choose three people", gap=135),
              note("5 × 4 × 3 = 60", "five times four times three", y=266, colour=BLUE),
              triples, equation(("60 ÷ 6", WHITE, "sixty divided by six"), ("= 10 groups", MINT, "ten groups"))),
        scene("Different jobs make order matter", cards((A, B, C), 298, gap=285),
              cards((("Captain", BLUE), ("Scorer", GOLD), ("Timekeeper", MINT)), 421,
                    words="captain scorer and timekeeper", gap=285, width=254),
              note("5 × 4 × 3 = 60 assignments", "the answer is sixty")),
        pair_challenge,
    ),
    "T05.2": (
        scene("Split a difficult count into cases",
              outline(115, 315, 310, 130, "split them into cases"),
              outline(485, 315, 310, 130, "split them into cases"),
              outline(855, 315, 310, 130, "split them into cases"),
              *(move(letter, (396+i*97, 219), (170+369*(i//3)+97*(i%3), 382),
                     "split them into cases", colour=(BLUE, GOLD, MINT)[i//3], width=78, delay=.085*i)
                for i, letter in enumerate("ABCDEFGHI")),
              note("Every outcome goes in exactly one case", "every outcome belongs to one")),
        scene("Does the restriction change the count?",
              chart(("First decision", "Choices available next"),
                    [(("Case A", "4"), "the number of choices"), (("Case B", "3"), "when a restriction changes")],
                    y=245, row_height=88),
              note("Count each case using its own choices", "splitting at the restriction")),
        scene("How many even three-digit numbers?",
              cards(tuple("01234"), 228, words="zero one two three and four", gap=143),
              cards(("?", "?", "?"), 382, words="how many even", gap=167, face=GOLD),
              note("Use each digit at most once", "with no digit repeated", y=501)),
        scene("Split by the last digit",
              cards((("0", BLUE), ("2", GOLD), ("4", GOLD)), 241, words="zero two or four", gap=155),
              link((485,280),(354,382),"split by the last digit",colour=BLUE,arrow=True),
              link((719,280),(925,382),"or it is two or four",colour=GOLD,arrow=True),
              cards((("Last is 0", BLUE),), 430, words="either it is zero", x=354, width=290),
              cards((("Last is 2 or 4", GOLD),), 430, words="or it is two or four", x=925, width=355),
              note("A three-digit number cannot start with 0", "cannot start with zero", y=555)),
        scene("Count inside each class",
              chart(("Last digit", "Choices for first", "Choices for middle", "Number of results"),
                    [(("0","4","3","12"),"if the last digit is zero"),
                     (("2","3","3","9"),"if the last digit is two or four"),
                     (("4","3","3","9"),"if the last digit is two or four")],
                    y=219, row_height=76, width=1112, highlight=((0,3),(1,3),(2,3))),
              equation(("Last 0: 12", BLUE, "twelve numbers"),
                       ("    Last 2 or 4: 18", GOLD, "eighteen numbers"), y=562, size=37)),
        scene("A number belongs to just one class",
              move("12", (360,290),(533,369),"add them",colour=BLUE,width=142),
              move("18", (914,290),(748,369),"add them",colour=GOLD,width=142),
              equation(("12",BLUE,"twelve plus eighteen"),("+",WHITE,"twelve plus eighteen"),
                       ("18",GOLD,"twelve plus eighteen"),("= 30",MINT,"is thirty"))),
        scene("Count the complement when it is shorter",
              chart(("Switch 1","Switch 2"),[(("Off","Off"),None),(("Off","On"),None),
                                             (("On","Off"),None),
                                             ((("On",RED),("On",RED)),"two switches have four")],
                    y=204,row_height=62),
              note("Subtract the forbidden pair", "subtract that one", y=532, size=34, colour=RED),
              equation(("4 − 1", WHITE, "subtract that one"),("= 3", MINT,"leaving three"),y=586,size=38)),
        exercise((("Split at the restriction","split at the feature"),
                   ("Multiply within a case","multiply within a case"),("Add the cases","add the cases")),
                 "notebook challenge",("How many two-digit numbers have different digits?",),
                 sub="Try counting all two-digit numbers and removing the repeats."),
    ),
    "T05.3": (
        scene("Give each outcome one address",
              *(outline(267+i*275,370,196,94,"every outcome has exactly") for i in range(3)),
              *(move(label,(365+i*275,219),(365+i*275,418),"from the outcome",
                     colour=(BLUE,GOLD,MINT)[i], width=148,delay=.13*i)
                for i,label in enumerate(("Outcome A","Outcome B","Outcome C"))),
              note("Outcome and choices recover each other","tell which choices made it",y=555)),
        scene("Look for repeats and omissions",
              outline(245,351,342,99),outline(692,351,343,99),
              move("A", (285,239),(348,400),"double counting",colour=BLUE),
              move("A", (558,239),(466,400),"double counting",colour=RED),
              note("Same outcome twice", "double counting", x=410,y=498, width=470, colour=RED, size=30),
              note("An outcome missing", "missed cases", x=864,y=498,width=470,colour=GOLD,size=30)),
        scene("Seat five different people",cards((("G1",BLUE),("G2",BLUE),("G3",BLUE),
              ("B1",GOLD),("B2",GOLD)),243,words="three are girls",gap=155),
              cards(("","","","",""),393,width=111,gap=129),
              note("The two boys must have someone between them", "must not sit next to each other")),
        scene("Seat the girls first",
              cards((("G1",BLUE),("G2",BLUE),("G3",BLUE)),336,words="seat the girls first",gap=249),
              cards(("Gap 1","Gap 2","Gap 3","Gap 4"),440,words="four gaps",gap=249,face=GOLD,width=159),
              note("3 × 2 × 1 = 6 girl orders", "arranged in six orders")),
        scene("Choose two gaps in order",
              cards(("1","2","3","4"),398,gap=240,face=MUTED,width=135),
              move("B1",(491,240),(520,324),"four gaps to choose",colour=GOLD),
              move("B2",(783,240),(1000,324),"the second has three",colour=MINT),
              equation(("6 girl orders",BLUE,"six times twelve"),("× 12 gap choices",GOLD,"that is twelve ways"),
                       ("= 72",MINT,"seventy-two seatings"),y=550,size=36)),
        scene("Recover the choices from the row",
              cards((("G1",BLUE),("B1",GOLD),("G2",BLUE),("G3",BLUE),("B2",GOLD)),244,gap=145),
              cards((("G1",BLUE),("G2",BLUE),("G3",BLUE)),392,words="remove the boys",gap=246),
              note("Girls’ order", "see the girls' order", y=326,colour=BLUE),
              note("B1 used gap 2, B2 used gap 4","you see which gaps they used",y=523,colour=GOLD)),
        scene("Check by grouping the neighbours",
              move("B1",(350,248),(427,355),"glue the boys together",colour=GOLD,width=96),
              move("B2",(580,248),(527,355),"glue the boys together",colour=GOLD,width=96),
              outline(367,313,218,85,"as one block",colour=GOLD),
              cards(("G1","G2","G3"),353,x=847,gap=126,width=108),
              note("Arrange 4 objects, then 2 orders inside the block","times two for the boys swapping",y=477,size=32),
              equation(("120",BLUE,"one hundred and twenty ways"),("− 48",GOLD,"forty-eight unwanted rows"),
                       ("= 72",MINT,"is seventy-two"),y=562)),
        exercise((("Recover the choices","recover the choices"),("Check every choice is legal","give a legal outcome")),
                 "notebook challenge",("Arrange four different books on a shelf.",
                                        "Two particular books cannot sit together. How many orders?")),
    ),
}


def lunch_tree(stage, s, branch=None):
    tile(stage, 640, 208, "Lunch", WHITE, 169, 63)
    for x, text, colour in ((339,"Cheese",BLUE),(941,"Bean",MINT)):
        stage.arrow((640,239),(x,305),colour,1)
        tile(stage,x,341,text,colour,205,63)
        if branch not in ("both", text):
            continue
        when="the allowed fruits" if text=="Cheese" and branch=="Cheese" else "all three fruits" if text=="Bean" else None
        for i, fruit in enumerate(("Apple","Pear","Plum")):
            p=cue(s,when,delay=.15*i)
            xx=x+145*(i-1)
            forbidden=text=="Cheese" and fruit=="Plum"
            colour=RED if forbidden else GOLD
            stage.arrow((x,375),(xx,444),colour,p)
            tile(stage,xx,479,fruit,colour,127,61,p,29)
            if forbidden:
                stage.line([(xx-46,496),(xx+46,461)],RED,4,p)


FILMS["T05.E"] = (
    scene("Pick one sandwich and one fruit",
          cards((("Cheese",BLUE),("Bean",MINT)),238,words="cheese or bean",gap=228,width=194),
          cards(("Apple","Pear","Plum"),377,words="apple pear or plum",gap=182,face=GOLD,width=149),
          note("Cheese and plum cannot be paired","cheese may not be paired",y=496,colour=RED),
          note("How many lunches?", "how many different lunches", y=574)),
    scene("The sandwich determines the case",lunch_tree,
          note("A lunch chooses exactly one branch", "a lunch has exactly one sandwich")),
    scene("Cheese allows two fruit choices",lambda stage,s:lunch_tree(stage,s,"Cheese"),
          note("2 lunches in the cheese branch","that is two lunches",y=575)),
    scene("Bean allows all three choices",lambda stage,s:lunch_tree(stage,s,"both"),
          equation(("2",BLUE,"add the cases"),("+",WHITE,"add the cases"),("3",GOLD,"three lunches"),
                   ("= 5 lunches",MINT,"is five"),y=573,size=40)),
    scene("Check by removing the forbidden pair",
          chart(("Sandwich","Apple","Pear","Plum"),
                [(("Cheese","Yes","Yes",("No",RED)),"without the rule"),(("Bean","Yes","Yes","Yes"),"without the rule")],
                y=249,row_height=95,highlight=((0,1),(0,2),(1,1),(1,2),(1,3))),
          equation(("6",BLUE,"six lunches"),("− 1",RED,"exactly one"),("= 5",MINT,"six minus one is five"))),
    exercise((("Add unequal branches","different sizes"),("Check the missing case","rebuild the tree")),
             "then try this",("Three shirts and four pairs of shorts.","The red shirt cannot go with either orange pair."),
             sub="How many outfits can you make?"),
)
