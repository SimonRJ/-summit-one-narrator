"""Keep track of the whole, decimal place value and equation balance."""

from series_marks import (BLUE, GOLD, MINT, MUTED, RED, RIM, WHITE, balance, blocks, board,
                          cards, change, chart, cue, equation, link, move, note, scene, tile)
from stage import mix
from studio_diagrams import bead, fit, prime


def chocolate(stage,s):
    removed=[(r,c,BLUE,"half of a whole bar") for r in range(3) for c in (0,1)]
    removed += [(r,2,GOLD,"half of what is left") for r in range(3)]
    board(3,4,width=83,y=345,cells=removed)(stage,s)
    fit(stage,"6 of 12",416,506,30,223,BLUE,cue(s,"six squares"))
    fit(stage,"3 of the remaining 6",812,506,30,359,GOLD,cue(s,"three squares"))


def marbles(n, *, prompt=None, take=None, owner=""):
    def draw(stage,s):
        for i in range(n):
            j,k=divmod(i,10)
            centre=640+(j-(n/10-1)/2)*202
            p=cue(s,prompt,delay=.012*i)
            q=cue(s,take,duration=1.02) if j==0 and take else 0
            xx=centre+34*((k%5)-2)
            yy=325+42*(k//5)
            bead(stage,mix(xx,225+34*((k%5)-2),q),mix(yy,470+32*(k//5),q),
                 (GOLD,BLUE,MINT,BLUE)[j + (n==30)],p,13)
        if take:
            fit(stage,owner,229,547,27,270,GOLD,cue(s,take))
            if n==40:
                fit(stage,"10 in each group",640,430,30,517,BLUE,1-cue(s,take))
    return draw


def price_bar(stage,s):
    rise=cue(s,"to one hundred and ten",duration=.75)
    fall=cue(s,"price becomes ninety-nine",duration=.85)
    width=5.5*(100+10*rise-11*fall)
    stage.box(331,320,width,90,fill="#28495b",edge=BLUE,radius=6,stroke=3)
    before=float(100+10*rise-11*fall)
    fit(stage,"$"+str(round(before)),331+width/2,365,42,420,WHITE)
    up=cue(s,"goes up by ten percent")
    down=cue(s,"is eleven")
    fit(stage,"+ $10",947,251,33,260,GOLD,up)
    fit(stage,"− $11",947,484,33,260,RED,down)
    fit(stage,"Ten percent is a different amount the second time",640,568,31,1120,MINT,fall)


def fraction(n,d,x,y, *, words=None, colour=WHITE, size=48,width=235):
    def draw(stage,s):
        p=cue(s,words)
        fit(stage,str(n),x,y-41,size,width,colour,p)
        stage.line([(x-width*.38,y),(x+width*.38,y)],colour,3,p)
        fit(stage,str(d),x,y+43,size,width,colour,p)
    return draw


def tens(stage,s):
    x0=476
    for i in range(3):
        x=x0+i*167
        prime(stage,x,312,2,cue(s,"forty is two"),73)
        if i:
            p=cue(s,"supply two more fives",delay=.16*(i-1),duration=.8)
            prime(stage,x,mix(495,402,p),5,p,73)
        else:
            prime(stage,x,402,5,cue(s,"three twos and one five"),73)
        fit(stage,"10",x,465,27,99,MINT,cue(s,"multiply top and bottom"))


def pan(stage,s, pouches, counters, *, y=368, remove=None, opened=False):
    """Move equal quantities off the two pans without changing the balance."""
    rem_pouches,rem_count,words=remove if remove else (0,0,None)
    progress=cue(s,words,duration=.9) if remove else 0
    stage.line([(190,y+38),(1090,y+38)],MINT,5)
    stage.line([(601,y+120),(640,y+40),(679,y+120),(601,y+120)],RIM,4)
    for j,(x,pcs,n) in enumerate(zip((383,897),pouches,counters)):
        for i in range(pcs):
            p=progress if i>=pcs-rem_pouches else 0
            ix=x+99*(i-(pcs-1)/2)
            tile(stage,ix,y-101-74*p,"7" if opened else "P",BLUE,89,61,1-p,30)
        for i in range(n):
            p=progress if i>=n-rem_count else 0
            cols = 10 if n > 12 else 6
            ix=x+32*((i%cols)-(cols-1)/2)
            iy=y-31+29*(i//cols)
            bead(stage,ix,iy-118*p,GOLD,1-p,11)


def equation_rows(rows):
    def draw(stage,s):
        for i,(text,when) in enumerate(rows):
            fit(stage,text,640,215+119*i,44,1080,(BLUE,GOLD,MINT)[i],cue(s,when))
    return draw


def tray_pouches(stage,s, *, reveal=None):
    for i in range(3):
        x=356+284*i
        p=cue(s,reveal,delay=.14*i)
        stage.box(x-120,261,240,176,fill=None,edge=RIM,opacity=p)
        tile(stage,x-47,340,"P",BLUE,78,73,p)
        for dx in (25,76):
            bead(stage,x+dx,339,GOLD,p,17)



def tank_left(stage, s):
    challenge = s.t >= s.at("notebook challenge")
    fit(stage, "Use the amount that remains" if not challenge else "Track fifths of the original tank",
        640, 87, 44)
    if not challenge:
        marbles(30, take="update the whole", owner="Bea takes 10")(stage,s)
        fit(stage,"One third of 30 is 10",640,219,35,830,MINT,cue(s,"fraction of what"))
        return
    monday=cue(s,"one fifth is used",duration=.85)
    tuesday=cue(s,"one quarter of the remainder",duration=.85)
    start=cue(s,"a tank is full")
    x,y,w,h=234,248,810,171
    stage.box(x,y,w,h,radius=0,fill="#17303c",edge=RIM,opacity=start)
    filled=w*(1-monday/5-tuesday/5)
    stage.box(x,y,filled,h,radius=0,fill="#3a7287",edge=BLUE,opacity=start)
    for i in range(1,5):
        stage.line([(x+w*i/5,y),(x+w*i/5,y+h)],WHITE,2,start)
    fit(stage,"Monday: 4 fifths remain",640,479,34,900,BLUE,monday)
    fit(stage,"Tuesday: 3 of the original 5 fifths remain",640,552,35,1100,MINT,tuesday)


tank_left.chapter = "Your turn"


def decimal_decisions(stage, s):
    challenge = s.t >= s.at("notebook challenge")
    fit(stage,"Which decimals stop?" if challenge else "Look at the reduced denominator",640,87,44)
    if challenge:
        cases=[("7/20","20 = 2² × 5","0.35","seven twentieths",MINT),
               ("5/12","12 = 2² × 3","repeats","five twelfths",GOLD),
               ("9/75 = 3/25","25 = 5²","0.12","nine seventy-fifths",MINT)]
    else:
        cases=[("6/15 = 2/5","5","0.4","simplify the fraction",MINT),
               ("3/40","40 = 2³ × 5","0.075","built only from",MINT),
               ("1/6","6 = 2 × 3","repeats","any other prime",GOLD)]
    for x,heading in zip((292,654,1000),("Fraction","Denominator","Decimal")):
        fit(stage,heading,x,210,27,330,MUTED)
    for i,(fraction_text,factors,result,when,colour) in enumerate(cases):
        y=292+94*i
        p=cue(s,when)
        fit(stage,fraction_text,292,y,35,365,WHITE,p)
        fit(stage,factors,654,y,34,345,BLUE,p)
        fit(stage,result,1000,y,36,310,colour,cue(s,when,delay=.24))


decimal_decisions.chapter = "Your turn"


def reversible_balance(stage,s):
    if s.t >= s.at("doubling takes us back"):
        pouches,counts=(2,0),(6,20)
        rule="Double both sides";expression="2P + 6 = 20"
    elif s.t >= s.at("halve both sides"):
        pouches,counts=(1,0),(3,10)
        rule="Halve both sides";expression="P + 3 = 10"
    elif s.t >= s.at("addition takes us back"):
        pouches,counts=(2,0),(6,20)
        rule="Add 3 to both sides";expression="2P + 6 = 20"
    elif s.t >= s.at("take three from both sides"):
        pouches,counts=(2,0),(3,17)
        rule="Take 3 from both sides";expression="2P + 3 = 17"
    else:
        pouches,counts=(2,0),(6,20)
        rule="A level balance";expression="2P + 6 = 20"
    pan(stage,s,pouches,counts,y=353)
    fit(stage,rule,640,178,34,990,GOLD)
    fit(stage,expression,640,554,41,1000,MINT)


def three_pouches(stage,s):
    challenge=s.t>=s.at("notebook challenge")
    fit(stage,"Find the seven counters in each pouch" if not challenge else "Three pouches against one",
        640,87,44)
    if not challenge:
        pan(stage,s,(2,1),(5,12),opened=s.t>=s.at("check your answer"))
        fit(stage,"2 × 7 + 5 = 7 + 12 = 19",640,550,36,1120,MINT,cue(s,"check your answer"))
        return
    if s.t>=s.at("three pouches"):
        pan(stage,s,(3,1),(4,18),y=344)
    fit(stage,"3P + 4 = P + 18",640,500,36,810,WHITE,cue(s,"eighteen counters"))
    fit(stage,"2P = 14     P = 7",640,564,38,870,MINT,cue(s,"each pouch"))


three_pouches.chapter = "Your turn"


def four_bags(stage,s):
    challenge=s.t>=s.at("then try this")
    fit(stage,"Share 21 or remove six loose counters" if not challenge else "Four bags, forty marbles",640,87,44)
    if challenge:
        for i in range(4):
            x=256+i*256
            p=cue(s,"four identical bags",delay=.08*i)
            stage.box(x-105,239,210,164,radius=13,fill=None,edge=RIM,opacity=p)
            tile(stage,x-38,319,"B",BLUE,76,75,cue(s,"one box"))
            for v in range(3):
                bead(stage,x+35+(v%2)*29,305+30*(v//2),GOLD,cue(s,"three loose marbles",delay=.07*v),10)
        fit(stage,"40 ÷ 4 = 10 per bag",640,471,35,992,WHITE,cue(s,"forty marbles altogether"))
        fit(stage,"10 − 3 = 7 in each box",640,554,38,994,MINT,cue(s,"in each box"))
    else:
        tray_pouches(stage,s)
        fit(stage,"21 ÷ 3 − 2 = 5",640,478,34,950,MINT,cue(s,"share first"))
        fit(stage,"(21 − 6) ÷ 3 = 5",640,550,34,950,GOLD,cue(s,"remove the extras"))


four_bags.chapter = "Your turn"


FILMS = {
    "T09.1": (
        scene("Name the whole before finding a fraction",chocolate,
              note("Same fraction, a different whole","same fraction different whole",y=566)),
        scene("The next percentage has a new whole",
              cards((("+10%",BLUE),("−10%",GOLD)),318,gap=335,width=237,
                    words="when things change",size=49),
              note("Do these changes take the price back to the start?", "the new amount")),
        scene("Two people take marbles from the same jar",marbles(40,prompt="forty marbles"),
              note("Ali takes one quarter", "ali takes one quarter",y=455,colour=BLUE),
              note("Bea takes one third of what remains", "of what remains",y=503,colour=GOLD),
              note("How many are left?", "how many marbles are left",y=576)),
        scene("Ali uses the original forty",marbles(40,take="which is ten",owner="Ali takes 10"),
              equation(("40 − 10",WHITE,"thirty marbles remain"),("= 30 left",MINT,"thirty marbles remain"))),
        scene("Bea uses the thirty that remain",marbles(30,take="that is ten more",owner="Bea takes 10"),
              equation(("30 − 10",WHITE,"twenty marbles are left"),("= 20 left",MINT,"twenty marbles"),y=574)),
        scene("See a fraction of a fraction",
              board(3,4,width=83,y=343,
                    cells=tuple((r,c,BLUE,"shade three of four columns") for r in range(3) for c in range(3))
                      +tuple((r,c,MINT,"take two of the three rows") for r in range(2) for c in range(3))),
              equation(("2/3 × 3/4",BLUE,"two thirds of three quarters"),("= 6/12",GOLD,"six cells"),
                       ("= 1/2",MINT,"one half"),y=539)),
        scene("Up 10 percent and down 10 percent",price_bar),
        tank_left,
    ),
    "T09.2": (
        scene("Decimal places are powers of ten",
              fraction(375,1000,835,319,words="three hundred and seventy-five thousandths",colour=GOLD),
              cards((("0.375",BLUE),),320,x=376,width=236,words="nought point three",size=49),
              link((506,320),(697,320),"three hundred and seventy-five thousandths",arrow=True,colour=MINT),
              note("1,000 = (2 × 5) × (2 × 5) × (2 × 5)", "every power of ten")),
        scene("Predict a stopping decimal",cards(("1/3","1/4","1/6","1/8"),326,width=177,gap=204),
              note("Which denominators can turn into powers of ten?", "which fractions make decimals")),
        scene("Does 3/40 give a decimal that stops?",fraction(3,40,533,337,colour=BLUE),
              cards(("?",),339,x=783,face=GOLD,width=156,size=52),
              note("Start by factorising 40", "pause and factorise forty")),
        scene("Pair every two with a five",tens,
              note("40 × 25 = 1,000", "bottom by twenty-five",y=207,colour=BLUE),
              equation(("3/40",BLUE,"three fortieths becomes"),("= 75/1,000",GOLD,"seventy-five thousandths"),
                       ("= 0.075",MINT,"nought point nought seven five"),y=556,size=43)),
        scene("One sixth has a factor of three",
              fraction(1,6,317,346,colour=BLUE),
              cards((("2",BLUE),("3",RED)),339,x=820,gap=144,width=105,words="two times three"),
              note("1/6 = 0.1666…", "one sixth never stops")),
        scene("Simplify before inspecting the denominator",
              fraction(6,15,382,343,words="six fifteenths",colour=BLUE),
              link((493,343),(586,343),"but it cancels",arrow=True,colour=MINT),
              fraction(2,5,707,343,words="is two fifths",colour=MINT),
              note("= 0.4", "nought point four",x=971,y=346,width=247,size=47)),
        scene("Find a multiplier that makes a whole number",
              equation_rows((("0.25 = 1/4","is a quarter"),("0.25 × 4 = 1","multiplying by four"),
                             ("0.25 × 100 = 25","multiplied by one hundred")))),
        decimal_decisions,
    ),
    "T09.3": (
        scene("Use moves that you can undo",reversible_balance),
        scene("A reversible move preserves the solutions",
              cards((("Subtract 3",BLUE),("Add 3",MINT)),312,gap=336,width=241,
                    words="reversible moves",size=34),
              link((549,383),(721,383),"solve the equation",colour=BLUE,arrow=True),
              link((721,441),(549,441),"kept all",colour=MINT,arrow=True),
              note("Check the step works in both directions", "kept all of its possible answers")),
        scene("Find the counters in each pouch",lambda stage,s:pan(stage,s,(2,1),(5,12)),
              note("Identical pouches, equal counts on both sides", "every pouch holds")),
        scene("Remove one pouch from both pans",
              lambda stage,s:pan(stage,s,(2,1),(5,12),remove=(1,0,"remove one pouch")),
              equation(("P + 5",BLUE,"now one pouch"),("= 12",MINT,"balance twelve"),y=551)),
        scene("Remove five loose counters from both pans",
              lambda stage,s:pan(stage,s,(1,0),(5,12),remove=(0,5,"remove five counters")),
              equation(("P",BLUE,"one pouch balances"),("= 7",MINT,"each pouch holds seven"),y=551)),
        scene("Check in the original balance",
              lambda stage,s:pan(stage,s,(2,1),(5,12),opened=True),
              equation(("7 + 7 + 5",BLUE,"two sevens and five"),("= 7 + 12",GOLD,"one seven and twelve"),
                       ("= 19",MINT,"both sides agree"),y=548,size=43)),
        scene("Undo addition, then undo halving",
              equation_rows((("x/2 + 3 = 11","half a number plus three"),
                             ("x/2 = 8","half the number is eight"),
                             ("x = 16","the number is sixteen")))),
        scene("Check the zero case before dividing",
              note("x × x = 5 × x", "a number times itself",y=211,colour=WHITE,size=48),
              cards((("x = 5 if x is nonzero",BLUE),),346,x=893,width=408,
                    words="dividing gives five",size=32),
              cards((("0 × 0 = 5 × 0",MINT),),346,x=389,width=338,
                    words="zero times zero",size=34),
              note("Both 0 and 5 satisfy the original equation", "all possibilities")),
        three_pouches,
    ),
    "T09.E": (
        scene("Three equal trays contain 21 counters",lambda stage,s:tray_pouches(stage,s,reveal="three identical trays"),
              note("How many counters are inside a pouch?", "how many counters are in each pouch")),
        scene("Share the total equally",
              blocks(((1,"7",BLUE,None),(1,"7",BLUE,None),(1,"7",BLUE,None)),
                     words="twenty-one divided by three",y=341),
              note("21 ÷ 3 = 7 on each tray", "each tray holds seven")),
        scene("Separate the loose counters from the pouch",
              blocks(((5,"Inside the pouch",BLUE,None),(2,"2",GOLD,None)),words="two of the seven",y=343),
              note("7 − 2 = 5 inside each pouch", "seven minus two is five")),
        scene("The bars and equation describe the same steps",
              equation_rows((("3 × (P + 2) = 21","three lots of a pouch"),
                             ("P + 2 = 7","pouch plus two equals seven"),("P = 5","a pouch equals five")))),
        scene("Or remove the loose counters first",
              blocks(((5,"5",BLUE,None),(5,"5",BLUE,None),(5,"5",BLUE,None)),
                     words="fifteen counters remain",y=338),
              equation(("21 − 6",GOLD,"take away all six loose counters"),
                       ("= 15",WHITE,"fifteen counters remain"),("   15 ÷ 3 = 5",MINT,"five each"),y=555,size=39)),
        four_bags,
    ),
}
