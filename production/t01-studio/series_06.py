"""Count incidences, solve paired measurements and verify a resource bound."""

from itertools import combinations
import math

from series_marks import (BLUE, GOLD, MINT, MUTED, RED, RIM, WHITE, balance, board, cards,
                          change, chart, cue, equation, exercise, link, move, network,
                          note, outline, ring, scene, tile)
from stage import mix
from studio_diagrams import bead, fit


SIX = ring(6, x=582, y=350, radius=144)
FIVE = ring(5, x=511, y=350, radius=132)
TRIANGLE = ((640,197),(395,445),(885,445),(517.5,321),(762.5,321),(640,445))


def edge_set(n, colour=RIM, words=None):
    return tuple((a,b,colour,words) for a,b in combinations(range(n),2))


def handshake_ends(stage, s):
    p=cue(s,"every handshake has two hands")
    pos = ((386,277),(894,277),(386,436),(894,436))
    network(pos,"ABCD",((0,1,MINT,None),(0,2,RIM,"that small fact"),
                       (1,3,RIM,"that small fact")),radius=32)(stage,s)
    for x in (389,891):
        fit(stage,"1",x,219,32,70,MINT,cue(s,"once by each person"))
    fit(stage,"Both people report the same handshake",640,550,37,1100,MINT,p)


def cube_faces(stage,s):
    yaw=.52 + .24*cue(s,"every edge belongs",duration=1.2)
    tilt=.58
    coords={}
    for x in (-1,1):
        for y in (-1,1):
            for z in (-1,1):
                a=x*math.cos(yaw)+z*math.sin(yaw)
                depth=z*math.cos(yaw)-x*math.sin(yaw)
                b=y*math.cos(tilt)-depth*math.sin(tilt)
                coords[(x,y,z)]=(635+104*a,357-104*b)
    for (p,a),(q,b) in combinations(coords.items(),2):
        if sum(x!=y for x,y in zip(p,q))==1:
            incident=p[0]==q[0]==1 and p[1]==q[1]==1
            stage.line([a,b],MINT if incident else BLUE,6 if incident else 3)
    for p, label, colour in (((-1,1,-1),"Top face",GOLD),((1,-1,1),"Side face",BLUE)):
        a=coords[p]
        x = 320 if p[0] < 0 else 936
        y = 245 if p[0] < 0 else 399
        stage.arrow((x,y+25),a,colour,cue(s,"each face has four"),2)
        fit(stage,label,x,y,28,235,colour,cue(s,"each face has four"))


def handshake_proof(stage,s):
    all_lines=cue(s,"fifteen handshakes",duration=.8)
    network(SIX,"ABCDEF",edge_set(6,RIM,"fifteen handshakes")+((0,1,GOLD,None),))(stage,s)
    for point,offset in ((SIX[0],-43),(SIX[1],49)):
        fit(stage,"1 report",point[0]+offset,point[1]-36,26,175,GOLD,
            cue(s,"both of the people")*(1-.55*all_lines))


def report_five(stage,s):
    network(SIX,"ABCDEF",tuple((0,i,BLUE,"five others") for i in range(1,6)))(stage,s)
    for x,y in SIX:
        a,b = 582+(x-582)*1.30, 350+(y-350)*1.30
        fit(stage,"5",a,b,27,73,GOLD,cue(s,"each person reports five"))


FILMS = {
    "T06.1": (
        scene("Every handshake has two ends",handshake_ends),
        scene("Count something in two ways",network(SIX,"ABCDEF",edge_set(6,RIM,"count lines")),
              cards((("Add reports",BLUE),),304,x=951,width=219,words="counting ends",height=72),
              cards((("Divide by 2",MINT),),409,x=951,width=219,words="counting ends",height=72),
              note("Count the ends to learn the number of lines","count lines")),
        scene("Six people all shake hands once",network(ring(6,radius=144),"ABCDEF"),
              note("How many handshakes take place?", "how many handshakes")),
        scene("Every person reports five",report_five,
              note("5 + 5 + 5 + 5 + 5 + 5", "six reports of five",x=1005,y=382,width=357,size=29,colour=BLUE),
              equation(("6 × 5",WHITE,"six reports of five"),("= 30 reports",MINT,"add to thirty"))),
        scene("Two reports count one handshake",handshake_proof,
              equation(("30 reports",BLUE,"so thirty counts"),("÷ 2",GOLD,"divided by two"),
                       ("= 15 handshakes",MINT,"fifteen handshakes"),y=565,size=40)),
        scene("An odd report total cannot happen",network(ring(7,radius=143),"3333333"),
              equation(("7 × 3",BLUE,"reports would add"),("= 21",RED,"twenty-one is odd"),
                       ("    Must be even",MINT,"so it must be even"),y=562,size=38)),
        scene("Two faces share each cube edge",cube_faces,
              equation(("6 × 4",BLUE,"each face has four edges"),("÷ 2",GOLD,"belongs to two faces"),
                       ("= 12 edges",MINT,"twelve edges"),y=566,size=42)),
        exercise((("Add the reports","add the reports"),("Find the repeat count","how many times"),
                  ("Divide","then divide")),"notebook challenge",
                 ("Eight teams each play every other team once.", "How many games are played?")),
    ),
    "T06.2": (
        scene("Measure boxes in pairs",
              cards((("A + B",BLUE),("B + C",GOLD),("A + C",MINT)),324,
                    words="totals of pairs",width=222,gap=260),
              note("How often does each box appear?", "how many times each unknown")),
        scene("Find the total first",balance("Three pair readings","Twice the total",words="find their total"),
              note("Subtract a pair to find the third box", "follows by subtraction")),
        scene("What does each box weigh?",
              chart(("Boxes on the scale","Weight"),
                    [(("A and B","10 kg"),"ten kilograms together"),
                     (("B and C","14 kg"),"weigh fourteen"),
                     (("A and C","12 kg"),"weigh twelve")],y=220,row_height=75,highlight=((0,1),(1,1),(2,1))),
              note("Find A, B and C", "how heavy is each box")),
        scene("Add the readings and count each box",
              chart(("Box","A + B","B + C","A + C","Appearances"),
                    [(("A","✓","", "✓","2"),"each box was on the scales"),
                     (("B","✓","✓", "", "2"),"each box was on the scales"),
                     (("C","","✓", "✓","2"),"each box was on the scales")],
                    y=217,row_height=69,highlight=((0,4),(1,4),(2,4))),
              note("10 + 14 + 12 = 36 kg", "is thirty-six",y=505,colour=BLUE),
              note("36 ÷ 2 = 18 kg in total", "weigh eighteen kilograms",y=568)),
        scene("Subtract the pair that excludes the box",
              chart(("Box","Subtract other pair","Result"),
                    [(("A","18 − 14","4 kg"),"eighteen minus fourteen"),
                     (("B","18 − 12","6 kg"),"the second weighs six"),
                     (("C","18 − 10","8 kg"),"third weighs eight")],
                    y=228,row_height=75,highlight=((0,2),(1,2),(2,2)))),
        scene("Check all three original weighings",
              chart(("Pair","Check","Reading"),
                    [(("A + B","4 + 6","10 kg"),"four and six"),
                     (("B + C","6 + 8","14 kg"),"six and eight"),
                     (("A + C","4 + 8","12 kg"),"four and eight")],
                    y=221,row_height=76,highlight=((0,2),(1,2),(2,2)))),
        scene("Sometimes the counts are unequal",
              network(TRIANGLE,("A","B","C","D","E","F"),((0,1,BLUE,"each side has a total"),
                      (0,2,GOLD,"each side has a total"),(1,2,MINT,"each side has a total"))),
              cards((("Corners × 2",BLUE),("Side middles × 1",GOLD)),539,
                    words="counts corners twice",gap=325,width=296),
              note("Track the two types separately", "keep track of that difference",y=597,size=29)),
        exercise((("Add the readings","add the measurements"),("Count appearances","how often"),
                  ("Subtract a pair","then subtract")),"notebook challenge",
                 ("Three numbers give pair totals of 17, 20 and 23.","Find the three numbers.")),
    ),
}


def consume_supply(stage,s):
    p=cue(s,"three per group",duration=1.35)
    for i in range(12):
        j,k=divmod(i,3)
        q=max(0,min(1,1.55*p-.18*j))
        x=mix(347+(i%6)*115,253+j*259+(k-1)*55,q)
        y=mix(222+(i//6)*58,418,q)
        bead(stage,x,y,(BLUE,GOLD,MINT,BLUE)[j],1,20)
    for j in range(4):
        stage.box(163+j*259,372,179,92,fill=None,edge=RIM,opacity=p)


DAYS=("day one","day two","day three","day four","day five")
SCHEDULE=(("AB","CD","E"),("AC","BE","D"),("AD","CE","B"),("AE","BD","C"),("BC","DE","A"))


def groups_of_three(stage,s):
    pts=((640,235),(369,348),(494,441),(911,348),(786,441))
    drawing=network(pts,"ABCDE",((0,1,BLUE,"share exactly one person"),(0,2,BLUE,"share exactly one person"),
                   (1,2,BLUE,"share exactly one person"),(0,3,MINT,"share exactly one person"),
                   (0,4,MINT,"share exactly one person"),(3,4,MINT,"share exactly one person")))
    drawing(stage,s)
    shared=cue(s,"using the shared person")
    without=cue(s,"leaving that person out")
    fit(stage,"Using A repeats an edge",640,516,33,999,GOLD,shared*(1-without))
    fit(stage,"Without A, three picks force BC or DE",640,516,33,999,GOLD,without)
    fit(stage,"Two groups fit. A third always repeats a pair.",640,577,32,1070,MINT,cue(s,"two groups fit"))


def squares(stage,s, *, motion=None, row=False, joins=None, boundary=None,
            separate=False, from_square=False):
    w=103
    for i in range(4):
        r,c=divmod(i,2)
        p=0 if separate else cue(s,motion,duration=1.0)
        start_x=640+(c-.5)*w if from_square else 640+(i-1.5)*196
        start_y=347+(r-.5)*w if from_square else 335
        cx=mix(start_x,640+(i-1.5)*w if row else 640+(c-.5)*w,p)
        cy=mix(start_y,348 if row else 347+(r-.5)*w,p)
        stage.box(cx-w/2,cy-w/2,w,w,radius=2,fill="#223948",edge=BLUE,stroke=2)
    if joins:
        p=cue(s,joins)
        stage.line([(640,245),(640,449)],GOLD,5,p)
        stage.line([(537,347),(743,347)],GOLD,5,p)
        for x,y in ((640,295),(640,397),(589,347),(692,347)):
            stage.dot(x,y,7,GOLD,p)
    if boundary:
        p=cue(s,boundary)
        stage.box(537,244,206,206,radius=1,fill=None,edge=MINT,stroke=6,opacity=p)


FILMS["T06.3"]=(
    scene("A supply limits how many groups fit",consume_supply,
          note("12 tokens ÷ 3 per group = 4 groups", "at most four groups")),
    scene("A maximum needs two parts",
          cards((("Prove a ceiling",BLUE),("Reach that ceiling",MINT)),344,words="a ceiling",
                gap=419,width=374,height=97,size=39),
          note("Show that the upper bound is attainable", "can actually be reached")),
    scene("How many days can the pairs work?",
          network(ring(5,radius=129),"ABCDE"),
          note("Two different pairs each day","two pairs work together",y=509,colour=BLUE),
          note("No pair can be repeated","partners more than once",y=576)),
    scene("Count the total supply of pairs",
          network(FIVE,"ABCDE",edge_set(5,BLUE,"ten different pairs")),
          cards((("10 pairs",BLUE),),282,x=887,width=195,words="ten different pairs"),
          cards((("2 per day",GOLD),),405,x=887,width=195,words="two new pairs"),
          equation(("10 ÷ 2",WHITE,"at most five days"),("= 5 days at most",MINT,"at most five days"))),
    scene("A schedule using all ten pairs",
          chart(("Day","First pair","Second pair","Resting"),
                [((str(i+1),*pairs),DAYS[i]) for i,pairs in enumerate(SCHEDULE)],
                y=199,row_height=60,highlight=tuple((r,c) for r in range(5) for c in (1,2))),
          note("Every pair appears exactly once", "all ten pairs appear",y=572)),
    scene("Three-person groups change the limit",groups_of_three,
          note("Pair count alone allows at most 3 groups","ceiling of three groups",y=166,colour=BLUE,size=28)),
    exercise((("Find the supply","find the limited supply"),("Prove a ceiling","divide to get a ceiling"),
              ("Try to reach it","build an example")),"notebook challenge",
             ("Six students play three chess games each day.","No pair repeats. How many days are possible?")),
)


FILMS["T06.E"]=(
    scene("Push four unit tiles together",lambda stage,s:squares(stage,s,motion="pushed together"),
          note("What is the outside perimeter?", "what is the perimeter")),
    scene("Count all the tile edges",lambda stage,s:squares(stage,s,separate=True),
          equation(("4 tiles",BLUE,"four tiles"),("× 4 edges",GOLD,"each tile has four edges"),
                   ("= 16 reports",MINT,"sixteen edges"))),
    scene("Find the four inside joins",lambda stage,s:squares(stage,s,joins="four inside joins"),
          note("2 vertical + 2 horizontal","two along the vertical",colour=GOLD)),
    scene("Remove the two reports at each join",
          lambda stage,s:squares(stage,s,joins="both tiles beside it",boundary="the perimeter is eight"),
          equation(("16",BLUE,"sixteen minus eight"),("− 2 × 4",GOLD,"remove two reports"),
                   ("= 8",MINT,"eight is eight"),y=551)),
    scene("Rearranging the same tiles changes the boundary",
          change("now rearrange the tiles",
              (lambda stage,s:squares(stage,s,boundary="the big square"),note("4 × 2 = 8","times two is eight")),
              (lambda stage,s:squares(stage,s,motion="rearrange the tiles",row=True,from_square=True),
               equation(("16 − 2 × 3",GOLD,"three joins"),("= 10",MINT,"which is ten"))))),
    exercise((("Count all tile edges","the total of all tile edges"),("Remove 2 per join","minus two for every join")),
             "then find the perimeter",("Arrange six unit squares in a 2 × 3 rectangle.",
                                        "What is the perimeter?"),sub="Count the joins as well as the tiles."),
)
