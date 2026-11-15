"""Use rotations and pairings while retaining every distinct case."""

from itertools import combinations, product
import math

from geometry_marks import region
from series_marks import (BLUE, GOLD, MINT, MUTED, RED, RIM, WHITE, cards, chart, cue,
                          equation, exercise, link, move, network, note, ring, scene, tile)
from stage import mix
from studio_diagrams import fit


def square(stage,x,y,side,mask=(),angle=0,opacity=1,letters=None,mirror=1):
    width=side/2
    sn,cs=math.sin(angle),math.cos(angle)
    def place(a,b):
        a *= mirror
        return x+a*cs-b*sn,y+a*sn+b*cs
    for k in range(4):
        r,c=divmod(k,2)
        a,b=(c-1)*width,(r-1)*width
        colour=BLUE if letters else "#0b1019" if k in mask else WHITE
        pts=[place(a+i*width,b+j*width) for i,j in ((0,0),(1,0),(1,1),(0,1))]
        region(stage,pts,colour,opacity=opacity,tint=.89 if not letters else .27,outline=False)
        stage.line([*pts,pts[0]],RIM,2,opacity)
        if letters:
            fit(stage,letters[k],*place(a+width/2,b+width/2),31,width-4,WHITE,opacity)


def solo_turn(stage,s, words):
    p=cue(s,words,duration=1.3)
    square(stage,640,346,190,(0,),angle=p*1.5*math.pi)


def two_kinds(stage,s):
    p=cue(s,"free to turn",duration=1)
    for i,mask in enumerate(combinations(range(4),2)):
        target=361 if mask in ((0,1),(0,2),(1,3),(2,3)) else 919
        x=245+158*i
        square(stage,mix(x,target,p),mix(279,388,p),107,mask,angle=p*math.pi/2,opacity=1-p)
    square(stage,361,387,162,(0,1),opacity=p)
    square(stage,919,387,162,(0,3),opacity=p)
    fit(stage,"Side by side",361,522,35,340,BLUE,p)
    fit(stage,"Diagonal",919,522,35,340,GOLD,p)


def tile_groups(stage,s, *, collapse=False):
    if collapse:
        masks=((),(0,),(0,1),(0,3),(0,1,2),(0,1,2,3))
        tells=("no black is one","with one black square","four are side by side",
               "two are diagonal","three black gives","all black gives")
        for i,(m,w) in enumerate(zip(masks,tells)):
            p=cue(s,w)
            x=248+i*157
            square(stage,x,340,112,m,opacity=p)
            fit(stage,str(len(m))+" black",x,431,25,144,MINT if len(m)==2 else WHITE,p)
    else:
        tells=("none black","one black","two black","three black","all black")
        for i,w in enumerate(tells):
            x=234+203*i
            for j,mask in enumerate(combinations(range(4),i)):
                xx=x+(-.52 if j%2==0 else .52)*74
                yy=288+75*(j//2)
                p=cue(s,w,delay=.10*j)
                square(stage,xx,yy,64,mask,opacity=p)
            fit(stage,f"{i} black",x,197,28,171,GOLD)
            fit(stage,str(math.comb(4,i)),x,551,36,147,MINT,cue(s,w))


def switches(stage,s,*, even=False):
    for i,tail in enumerate(product((0,1),repeat=2)):
        x=267+i*248
        for first in (0,1):
            bits=(first,*tail)
            y=281+151*first
            text="".join(map(str,bits))
            col=(MINT if sum(bits)%2==0 else GOLD) if even else BLUE if first==0 else GOLD
            p=cue(s,"one setting has an even" if even else "flipping the first switch")
            tile(stage,x,y,text,col,145,65,p,36)
        stage.line([(x,314),(x,400)],RIM,3,cue(s,"in each pair" if even else "settings really are in pairs"))


PAIR_ROWS=(("None","A"),("B","AB"),("C","AC"),("BC","ABC"))


FILMS={
 "T15.1":(
    scene("Does a turn give a new pattern?",lambda stage,s:solo_turn(stage,s,"turn it"),
          note("Decide which moves the rules allow", "what counts as the same")),
    scene("Read which moves count as the same",
          cards((("Fixed in place",BLUE),("Free to turn",MINT)),351,width=347,gap=426,
                words="fixed in place",size=36),
          note("The same pictures can have different counts","reading which is intended")),
    scene("Shade exactly one of four squares",
          lambda stage,s:square(stage,640,339,218,opacity=cue(s,"four smaller squares")),
          note("How many patterns are there?", "how many different patterns")),
    scene("Fixed in place gives four patterns",
          lambda stage,s:[square(stage,268+i*247,349,145,(i,),opacity=cue(s,"four patterns",delay=.16*i)) for i in range(4)],
          note("The shaded corner occupies a different place", "bottom-right")),
    scene("One tile can turn through all four pictures",
          lambda stage,s:solo_turn(stage,s,"a quarter turn"),
          note("One pattern when turning is allowed", "only one pattern")),
    scene("Two shaded squares produce two rotation groups",two_kinds,
          note("A turn preserves adjacency", "turning can never change",y=581,size=32)),
    scene("Check whether a flip is allowed",
          lambda stage,s:square(stage,368,341,183,letters=("A","B","C",""),mirror=math.cos(math.pi*cue(s,"flipping it over",duration=1.1))),
          lambda stage,s:square(stage,905,341,183,letters=("B","A","","C")),
          note("These marks match when flipped", "makes a match")),
    exercise((("Allowed moves","ask whether objects are fixed"),
              ("Test for a match","an allowed move takes one")),
             "notebook challenge",("Shade three of the four small squares.","How many patterns can a freely turning tile show?")),
 ),
 "T15.2":(
    scene("Some patterns repeat after fewer turns",
          lambda stage,s:[square(stage,315+325*i,340,154,m,angle=cue(s,"a pattern with its own symmetry",duration=1.05)*math.pi)
                          for i,m in enumerate(((),(0,3),(0,)))],
          note("The same number of turns need not give the same number of looks", "cannot always divide",size=31)),
    scene("Dividing by four assumes four copies each",
          cards((("1 picture",BLUE),("2 pictures",GOLD),("4 pictures",MINT)),337,width=235,gap=269,
                words="every pattern has been counted"),
          note("Check how many distinct pictures each tile makes","the same number of times")),
    scene("How many two-by-two tiles up to turning?",
          lambda stage,s:square(stage,640,326,211,(0,3)),
          note("There are 16 colourings fixed on the page", "sixteen colourings",y=508,colour=BLUE),
          note("How many when the tiles are free to turn?", "free to turn",y=574)),
    scene("Group the sixteen colourings by how many are black",tile_groups),
    scene("Count the rotation groups",lambda stage,s:tile_groups(stage,s,collapse=True),
          note("Six different tiles", "six tiles altogether")),
    scene("A tile’s group can contain 1, 2 or 4 pictures",
          cards((("1",GOLD),"4","4",("2",GOLD),"4",("1",GOLD)),336,width=111,gap=143,words="group sizes"),
          note("The six group sizes add to 16", "they are not all four")),
    scene("Five distinct seats have five possible starting places",
          network(ring(5,x=464,y=347,radius=128),"ABCDE"),
          note("5 rotations per circular order","exactly five times",x=938,y=336,width=403,size=32,colour=BLUE),
          equation(("120 ÷ 5",WHITE,"divided by five"),("= 24",MINT,"is twenty-four"),y=563)),
    exercise((("Check the repetition count","every arrangement is repeated"),
              ("Count the matching groups","sort the arrangements into groups")),
             "notebook challenge",("Four different people sit at a circular table.",
                                   "How many orders if turning the table counts as the same?")),
 ),
 "T15.3":(
    scene("Match each object to one of the other type",
          *(move("A"+str(i+1),(280+238*i,230),(280+238*i,321),"one partner",colour=BLUE)
            for i in range(4)),
          *(move("B"+str(i+1),(280+238*i,494),(280+238*i,414),"one partner",colour=GOLD)
            for i in range(4)),
          note("Each pair has one of each type", "half the objects")),
    scene("A pairing gives a reason for half",
          cards((("Even",BLUE),("Odd",GOLD)),329,width=200,gap=393,words="pairing arguments"),
          link((550,330),(730,330),"why the answer is half",colour=MINT,arrow=True),
          note("The rule must pair every outcome", "why the answer is half")),
    scene("How many of eight settings have even parity?",
          cards(("Switch A","Switch B","Switch C"),336,width=231,gap=277,words="three light switches"),
          note("Each switch can be on or off", "can each be on or off",y=475,colour=BLUE),
          note("Zero switches on is even", "zero counts as even",y=555)),
    scene("Flip the first switch to find the partner",switches,
          note("0 is off, 1 is on", "flipping the first switch",y=200,size=29),
          note("Flip it again to return to the original setting", "flip it again")),
    scene("Flipping one switch changes parity",lambda stage,s:switches(stage,s,even=True),
          note("4 even settings and 4 odd settings", "four settings are even")),
    scene("Use the same proof for ten switches",
          cards((("512 even",BLUE),("512 odd",GOLD)),344,width=273,gap=320,words="exactly half",size=39),
          note("1,024 settings split equally", "one thousand and twenty-four")),
    scene("Pair the first and last numbers",
          chart(("First number","Partner","Sum"),[(("1","100","101"),"pair one"),
               (("2","99","101"),"two with ninety-nine"),(("50","51","101"),"fifty pairs")],
                y=211,row_height=77,highlight=((0,2),(1,2),(2,2))),
          equation(("50 × 101",BLUE,"each adding"),("= 5,050",MINT,"five thousand and fifty"),y=565)),
    scene("Check for an object that pairs with itself",
          cards(("1, 36","2, 18","3, 12","4, 9",("6",GOLD)),325,width=139,gap=163,words="factors of thirty-six"),
          note("6 is the single factor paired with itself", "which pairs with itself")),
    exercise((("Pair every object","pairs every object"),
              ("Use one of each type","each pair has one")),
             "notebook challenge",("Find the sum of the whole numbers from 1 to 40.",)),
 ),
 "T15.E":(
    scene("Choose any subset of A, B and C",
          cards(("A","B","C"),336,width=142,gap=177,words="three objects"),
          note("The empty group is allowed", "including the empty group",y=465,colour=BLUE),
          note("Why do exactly half have even size?", "exactly half")),
    scene("Every object has two choices",
          cards(("None","A","B","C","AB","AC","BC","ABC"),337,width=103,gap=122,
                words="gives eight groups",size=28),
          equation(("2 × 2 × 2",BLUE,"two choices"),("= 8 groups",MINT,"gives eight groups"))),
    scene("Toggle A to pair each group",
          chart(("Without A","With A"),[(pair,"changing a") for pair in PAIR_ROWS],y=199,row_height=70),
          note("The second toggle returns to the starting group", "take a out")),
    scene("In each pair, sizes differ by one",
          chart(("Group and size","Partner and size"),
                [(("None: 0","A: 1"),"each pair"),(("B: 1","AB: 2"),"each pair"),
                 (("C: 1","AC: 2"),"each pair"),(("BC: 2","ABC: 3"),"each pair")],
                 y=198,row_height=68),
          note("Four pairs give four even groups", "four pairs give",y=563)),
    scene("Check the even-sized groups by listing",
          cards(("None","AB","AC","BC"),337,width=141,gap=181,words="the even groups"),
          equation(("4 out of 8",BLUE,"that is four"),("= 1/2",MINT,"half of eight"))),
    exercise((("Toggle one member","toggling one member"),("Check the opposite parity","pairs every even group")),
             "then say",("How many subsets of five objects have odd size?",)),
 ),
}
