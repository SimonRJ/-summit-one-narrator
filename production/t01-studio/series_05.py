"""Count orders, disjoint cases and reversible arrangements."""

from itertools import combinations

from series_marks import (BLUE, GOLD, MINT, MUTED, RED, WHITE, cards,
                          chart, cue, equation, link, move, note, outline, scene, tile)
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


def hundreds_choices(stage, s):
    fit(stage, "Even numbers made from 0, 1, 2, 3, 4 without repeats", 640, 173, 32, 1140)
    for y, last, digits, words, colour in (
        (321, 0, "1234", "the number of choices", BLUE),
        (452, 2, "134", "when a restriction changes", GOLD),
    ):
        p = cue(s, words)
        fit(stage, f"Last digit {last}", 295, y, 36, 325, colour, p)
        for i, digit in enumerate(digits):
            tile(stage, 593 + 122*i, y, digit, colour, 97, 68, p)
    fit(stage, "Possible hundreds digits", 769, 240, 27, 620, MUTED)


def case_counts(stage, s):
    xs = (251, 511, 783, 1035)
    for x, title in zip(xs, ("Last digit", "Hundreds", "Tens", "Numbers")):
        fit(stage, title, x, 215, 30, 230, MUTED)
    rows = (
        (("0", "last digit is zero"), ("4", "four choices"), ("3", "middle has three"), ("12", "twelve numbers")),
        (("2", "last digit is two or four"), ("3", "leaving three choices"), ("3", "and the middle has three"), ("9", "two times three times three")),
        (("4", "last digit is two or four"), ("3", "leaving three choices"), ("3", "and the middle has three"), ("9", "two times three times three")),
    )
    for row, entries in enumerate(rows):
        for x, (label, words) in zip(xs, entries):
            tile(stage, x, 299 + 84*row, label, (BLUE, GOLD, MINT)[row], 126, 60, cue(s, words))


def digit_challenge(stage, s):
    if s.t < s.at("notebook challenge"):
        fit(stage, "Count by last digit", 640, 90, 48)
        for i, (last, product, colour) in enumerate((("0", "4 × 3", BLUE), ("2", "3 × 3", GOLD), ("4", "3 × 3", MINT))):
            x = 320 + 320*i
            tile(stage, x, 266, "Last " + last, colour, 214, 74, cue(s, "split at the feature"))
            fit(stage, product, x, 386, 43, 245, colour, cue(s, "multiply within a case"))
        fit(stage, "12 + 9 + 9 = 30", 640, 534, 44, 800, MINT, cue(s, "add the cases"))
        return
    fit(stage, "Two-digit numbers with different digits", 640, 90, 44)
    p = cue(s, "two-digit numbers")
    q = cue(s, "two different digits")
    fit(stage, "Tens", 177, 221, 29, 147, BLUE, p)
    fit(stage, "Units digit", 677, 157, 29, 420, GOLD, p)
    for unit in range(10):
        fit(stage, str(unit), 321 + 77*unit, 219, 27, 70, GOLD, p)
    for tens in range(1, 10):
        y = 251 + 34*(tens-1)
        fit(stage, str(tens), 177, y, 25, 80, BLUE, p)
        for unit in range(10):
            x = 321 + 77*unit
            stage.box(x-25, y-13, 50, 26, radius=3, edge=MUTED, fill=None, opacity=p)
            if unit == tens:
                stage.line(((x-14,y+9),(x+14,y-9)), RED, 4, q)
    fit(stage, "9 tens choices × 9 allowed units = 81", 640, 584, 33, 1090, MINT, q)


digit_challenge.chapter = "Your turn"


SEATING = ("G1", "B1", "G2", "G3", "B2")


def seated_row(stage, y, words, s):
    for i, pupil in enumerate(SEATING):
        tile(stage, 280 + 180*i, y, pupil, BLUE if pupil.startswith("G") else GOLD,
             125, 68, cue(s, words, delay=.06*i))


def seat_address(stage, s):
    seated_row(stage, 242, "every outcome", s)
    for y, text, words, colour in (
        (360, "Girls from left to right   G1, G2, G3", "from the outcome", BLUE),
        (434, "B1 uses gap 2     ·     B2 uses gap 4", "which choices made it", GOLD),
        (535, "Put each boy back in his gap to recover the same row", "a real outcome", MINT),
    ):
        fit(stage, text, 640, y, 36, 1130, colour, cue(s, words))


def repeat_or_miss(stage, s):
    fit(stage, "Place B1 in gap 2 and B2 in gap 4", 640, 174, 35)
    for y, txt in ((247, "Insert B1, then B2"), (314, "Insert B2, then B1")):
        fit(stage, txt, 640, y, 29, 850, GOLD, cue(s, "double counting"))
    seated_row(stage, 410, "double counting", s)
    fit(stage, "Both insertion orders produce this one row", 640, 487, 31, 1080, MINT, cue(s, "double counting"))
    fit(stage, "Ignoring either end gap would miss legal rows", 640, 556, 31, 1120, RED, cue(s, "missed cases"))


def shelf_challenge(stage, s):
    if s.t < s.at("notebook challenge"):
        fit(stage, "Rebuild the same seating", 640, 89, 46)
        seated_row(stage, 265, "recover the choices", s)
        fit(stage, "G1, G2, G3     ·     B1 in gap 2     ·     B2 in gap 4",
            640, 398, 33, 1150, BLUE, cue(s, "recover the choices"))
        fit(stage, "Different gaps keep the boys apart", 640, 501, 34, 1040, MINT, cue(s, "give a legal outcome"))
        return
    fit(stage, "Arrange four different books", 640, 89, 46)
    for i, title in enumerate("ACBD"):
        tile(stage, 320 + 214*i, 297, title, GOLD if title in "AB" else BLUE,
             143, 134, cue(s, "four different books", delay=.08*i), 49)
    stage.line(((202,367),(1078,367)), MUTED, 5, cue(s, "stand on a shelf"))
    fit(stage, "A and B need a book between them", 640, 445, 37, 1100, GOLD, cue(s, "must not be next to each other"))
    fit(stage, "24 total − 2 × 6 with A and B together = 12", 640, 542, 34, 1130, MINT,
        cue(s, "next to each other", delay=.65))


shelf_challenge.chapter = "Your turn"


def lunch_check(stage, s):
    for c, name in enumerate(("Apple", "Pear", "Plum")):
        fit(stage, name, 490 + 231*c, 205, 32, 200, GOLD)
    for r, name in enumerate(("Cheese", "Bean")):
        y = 318 + 107*r
        fit(stage, name, 230, y, 34, 214, (BLUE, MINT)[r])
        for c in range(3):
            x = 490 + 231*c
            tile(stage, x, y, "1", (BLUE, MINT)[r], 153, 70, cue(s, "without the rule"))
            if (r, c) == (0, 2):
                p = cue(s, "cheese with plum")
                stage.line(((x-51,y+23),(x+51,y-23)), RED, 6, p)


def outfit_challenge(stage, s):
    if s.t < s.at("then try this"):
        fit(stage, "Count the lunches branch by branch", 640, 89, 47)
        lunch_tree(stage, s, "recap")
        fit(stage, "2 cheese lunches + 3 bean lunches = 5", 640, 574, 37, 1120, MINT,
            cue(s, "add them"))
        return
    fit(stage, "Three shirts and four pairs of shorts", 640, 89, 45)
    for i, shorts in enumerate(("Orange 1", "Orange 2", "Navy", "Grey")):
        x = 440 + 195*i
        fit(stage, shorts, x, 192, 29, 181, GOLD if i < 2 else MUTED, cue(s, "four pairs of shorts"))
        for j, shirt in enumerate(("Red", "Blue", "Green")):
            y = 284 + 91*j
            colour = (RED, BLUE, MINT)[j]
            if i == 0:
                fit(stage, shirt + " shirt", 221, y, 33, 248, colour, cue(s, "three shirts"))
            p = cue(s, "four pairs of shorts", delay=.055*(4*j+i))
            tile(stage, x, y, "1", colour, 139, 64, p)
            if j == 0 and i < 2:
                stage.line(((x-51,y+19),(x+51,y-19)), RED, 6, cue(s, "two orange pairs", delay=.13*i))
    fit(stage, "12 possible pairs − 2 forbidden = 10 outfits", 640, 572, 36, 1150, MINT,
        cue(s, "how many outfits", delay=.5))


outfit_challenge.chapter = "Your turn"


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
              hundreds_choices,
              note("Count each case using its own choices", "splitting at the restriction")),
        scene("How many even three-digit numbers?",
              cards(tuple("01234"), 228, words="zero one two three and four", gap=143),
              cards(("?", "?", "?"), 382, words="how many even", gap=167, face=GOLD),
              note("Use each digit at most once", "with no digit repeated", y=501)),
        scene("Split by the last digit",
              cards((("0", BLUE), ("2", GOLD), ("4", GOLD)), 241, words="zero two or four", gap=155),
              link((485,280),(354,382),"split by the last digit",colour=BLUE,arrow=True),
              link((640,280),(892,382),"or it is two or four",colour=GOLD,arrow=True),
              link((795,280),(957,382),"or it is two or four",colour=GOLD,arrow=True),
              cards((("Last is 0", BLUE),), 430, words="either it is zero", x=354, width=290),
              cards((("Last is 2 or 4", GOLD),), 430, words="or it is two or four", x=925, width=355),
              note("A three-digit number cannot start with 0", "cannot start with zero", y=555)),
        scene("Count inside each class",
              case_counts,
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
        digit_challenge,
    ),
    "T05.3": (
        scene("Give each outcome one address", seat_address),
        scene("Look for repeats and omissions", repeat_or_miss),
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
        shelf_challenge,
    ),
}


def lunch_tree(stage, s, branch=None):
    tile(stage, 640, 208, "Lunch", WHITE, 169, 63)
    for x, text, colour in ((339,"Cheese",BLUE),(941,"Bean",MINT)):
        stage.arrow((640,239),(x,305),colour,1)
        tile(stage,x,341,text,colour,205,63)
        if branch not in ("recap", "both", text):
            continue
        for i, fruit in enumerate(("Apple","Pear","Plum")):
            when = None
            if branch == "Cheese":
                when = "plum is not allowed" if fruit == "Plum" else "the allowed fruits"
            elif branch == "both" and text == "Bean":
                when = "all three fruits"
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
          lunch_check,
          equation(("6",BLUE,"six lunches"),("− 1",RED,"exactly one"),("= 5",MINT,"six minus one is five"))),
    outfit_challenge,
)
