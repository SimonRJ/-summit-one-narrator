"""Count incidences, solve paired measurements and verify a resource bound."""

from itertools import combinations
import math

from series_marks import (BLUE, GOLD, MINT, MUTED, RED, RIM, WHITE, balance, board, cards,
                          change, chart, cue, equation, link, move, network,
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
            stage.line([a,b],RIM,3)
    faces = (
        ("Top face", GOLD, [(-1,1,-1),(1,1,-1),(1,1,1),(-1,1,1)], (320,245)),
        ("Side face", BLUE, [(-1,-1,-1),(-1,1,-1),(-1,1,1),(-1,-1,1)], (304,419)),
    )
    for label,colour,face,(x,y) in faces:
        points=[coords[p] for p in face]
        progress=cue(s,"each face has four")
        stage.line([*points,points[0]],colour,4,progress)
        centre=tuple(sum(p[k] for p in points)/4 for k in (0,1))
        stage.arrow((x+88,y),centre,colour,progress,3)
        fit(stage,label,x,y,30,202,colour,progress)
    stage.line([coords[(-1,1,-1)],coords[(-1,1,1)]],MINT,8,cue(s,"every edge belongs"))



def handshake_proof(stage,s):
    all_lines=cue(s,"fifteen handshakes",duration=.8)
    network(SIX,"ABCDEF",edge_set(6,RIM,"fifteen handshakes")+((0,1,GOLD,None),))(stage,s)
    for point,offset in ((SIX[0],-43),(SIX[1],49)):
        fit(stage,"1 report",point[0]+offset,point[1]-36,26,175,GOLD,
            cue(s,"both of the people")*(1-.55*all_lines))


def report_five(stage,s):
    network(SIX,"ABCDEF",tuple((i,j,BLUE if i==0 else RIM,"five others" if i==0 else "each person reports five") for i,j in combinations(range(6),2)))(stage,s)
    for x,y in SIX:
        a,b = 582+(x-582)*1.21, 350+(y-350)*1.21
        fit(stage,"5",a,b,27,73,GOLD,cue(s,"each person reports five"))


def tournament(stage, s):
    if s.t < s.at("notebook challenge"):
        fit(stage, "Two reports per handshake", 640, 88, 46)
        pos = ((427,320),(853,320))
        network(pos,"AB",((0,1,MINT,None),),radius=38)(stage,s)
        for x in (427,853):
            fit(stage,"1 report",x,415,32,210,GOLD,cue(s,"add the reports"))
        fit(stage,"2 reports ÷ 2 = 1 handshake",640,534,40,1030,MINT,cue(s,"then divide"))
        return
    fit(stage,"Eight teams play every other team once",640,88,45)
    pos=ring(8,x=386,y=360,radius=172)
    edges=tuple((i,j,BLUE if i==0 else RIM,"each play every other team") for i,j in combinations(range(8),2))
    network(pos,"ABCDEFGH",edges,radius=23)(stage,s)
    fit(stage,"7 opponents per team",895,284,34,470,GOLD,cue(s,"every other team once"))
    fit(stage,"8 × 7 = 56 reports",895,387,34,490,BLUE,cue(s,"how many games"))
    fit(stage,"56 ÷ 2 = 28 games",895,486,34,490,MINT,cue(s,"games are played"))


tournament.chapter = "Your turn"


def weigh_pair_boxes(stage,s):
    for col,(first,second) in enumerate(("AB","BC","AC")):
        x=313+327*col
        p=cue(s,"totals of pairs",delay=.18*col)
        for xoff,letter in ((-48,first),(48,second)):
            tile(stage,x+xoff,330,letter,{"A":BLUE,"B":GOLD,"C":MINT}[letter],84,76,p,35)
        stage.line([(x-106,378),(x+106,378)],RIM,5,p)
    counts=cue(s,"how many times each unknown")
    fit(stage,"A appears twice     ·     B appears twice     ·     C appears twice",
        640,480,31,1170,WHITE,counts)


def paired_challenge(stage,s):
    if s.t < s.at("notebook challenge"):
        fit(stage,"Rebuild the three box masses",640,88,44)
        fit(stage,"10 + 14 + 12 = 36 kg",640,249,39,1070,BLUE,cue(s,"add the measurements"))
        fit(stage,"Each box occurs twice    ·    total = 18 kg",640,353,35,1120,GOLD,cue(s,"count how often"))
        fit(stage,"18 − 14 = 4 kg for the first box",640,467,37,1090,MINT,cue(s,"then subtract"))
        return
    fit(stage,"Reconstruct three numbers from their pair totals",640,88,42)
    for i,(value,words) in enumerate(((17,"seventeen"),(20,"twenty and"),(23,"twenty-three"))):
        tile(stage,330+310*i,242,str(value),[BLUE,GOLD,MINT][i],163,76,cue(s,words),43)
    if s.t >= s.at("what are the three numbers"):
        fit(stage,"(17 + 20 + 23) ÷ 2 = 30",640,371,41,1070,WHITE)
        fit(stage,"30 − 17 = 13      30 − 20 = 10      30 − 23 = 7",
            640,476,34,1160,MINT,cue(s,"what are the three numbers",delay=.3))


paired_challenge.chapter = "Your turn"


SIX_TEAM_ROUNDS=(("AF","BE","CD"),("AE","DF","BC"),("AD","CE","BF"),("AC","BD","EF"),("AB","CF","DE"))


def chess_challenge(stage,s):
    if s.t < s.at("notebook challenge"):
        fit(stage,"Match the bound to a real schedule",640,89,45)
        fit(stage,"Five students supply 10 different pairs",640,268,37,1100,BLUE,cue(s,"limited supply"))
        fit(stage,"10 pairs ÷ 2 games per day = 5 days at most",640,386,35,1120,GOLD,cue(s,"divide to get a ceiling"))
        fit(stage,"Five rows of the schedule use every pair once",640,502,33,1130,MINT,cue(s,"build an example"))
        return
    fit(stage,"Six players · three games a day",640,89,46)
    fit(stage,"Day",272,189,29,125,MUTED)
    fit(stage,"Three disjoint games",698,189,31,720,MUTED)
    for j,row in enumerate(SIX_TEAM_ROUNDS):
        y=247+60*j
        p=cue(s,"each day three games",delay=.12*j)
        fit(stage,str(j+1),272,y,31,90,WHITE,p)
        for i,pair in enumerate(row):
            tile(stage,487+210*i,y,pair,(BLUE,GOLD,MINT)[i],147,46,p,27)
    fit(stage,"15 distinct pairs ÷ 3 games = 5 days",640,558,36,1120,MINT,cue(s,"largest possible number of days"))


chess_challenge.chapter = "Your turn"


def rectangle_challenge(stage,s):
    question=s.t>=s.at("then find the perimeter")
    cols=3 if question else 2
    w=103;left=640-cols*w/2;top=225
    fit(stage,"Six unit squares in two rows" if question else "Count the outside once",
        640,88,46)
    for row in range(2):
        for col in range(cols):
            stage.box(left+col*w,top+row*w,w,w,radius=0,fill="#223948",edge=BLUE,stroke=3)
    p=cue(s,"two by three rectangle") if question else cue(s,"minus two for every join")
    for col in range(1,cols):
        for row in range(2):
            xx=left+col*w;yy=top+row*w
            stage.line([(xx,yy+4),(xx,yy+w-4)],GOLD,5,p)
            stage.dot(xx,yy+w/2,6,GOLD,p)
    for col in range(cols):
        xx=left+col*w;yy=top+w
        stage.line([(xx+4,yy),(xx+w-4,yy)],GOLD,5,p)
        stage.dot(xx+w/2,yy,6,GOLD,p)
    stage.box(left,top,cols*w,2*w,radius=0,fill=None,edge=MINT,stroke=5,opacity=p)
    if question:
        fit(stage,"3 units",640,176,31,360,MINT,p)
        fit(stage,"2 units",left-108,top+w,31,200,MINT,p)
        fit(stage,"4 vertical joins + 3 horizontal joins = 7",640,491,31,1110,GOLD,p)
        fit(stage,"24 − 2 × 7 = 10 units",640,567,39,1110,MINT,p)
    else:
        fit(stage,"16 edge reports − 2 × 4 joins = 8 units",640,529,38,1110,MINT,p)


rectangle_challenge.chapter = "Your turn"


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
              equation(("6 × 5",WHITE,"six reports of five"),("= 30 reports",MINT,"add to thirty"),y=568)),
        scene("Two reports count one handshake",handshake_proof,
              equation(("30 reports",BLUE,"so thirty counts"),("÷ 2",GOLD,"divided by two"),
                       ("= 15 handshakes",MINT,"fifteen handshakes"),y=565,size=40)),
        scene("An odd report total cannot happen",network(ring(7,radius=143),"3333333"),
              equation(("7 × 3",BLUE,"reports would add"),("= 21",RED,"twenty-one is odd"),
                       ("    Must be even",MINT,"so it must be even"),y=562,size=38)),
        scene("Two faces share each cube edge",cube_faces,
              equation(("6 × 4",BLUE,"each face has four edges"),("÷ 2",GOLD,"belongs to two faces"),
                       ("= 12 edges",MINT,"twelve edges"),y=566,size=42)),
        tournament,
    ),
    "T06.2": (
        scene("Measure boxes in pairs",weigh_pair_boxes),
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
                    [(("A","Yes","", "Yes","2"),"each box was on the scales"),
                     (("B","Yes","Yes", "", "2"),"each box was on the scales"),
                     (("C","","Yes", "Yes","2"),"each box was on the scales")],
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
        paired_challenge,
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
        vertical = cue(s,"two along the vertical") if joins=="four inside joins" else p
        horizontal = cue(s,"two along the horizontal") if joins=="four inside joins" else p
        for row in range(2):
            y=244+row*103
            stage.line([(640,y+2),(640,y+101)],GOLD,5,vertical)
            stage.dot(640,y+51.5,7,GOLD,vertical)
        for col in range(2):
            x=537+col*103
            stage.line([(x+2,347),(x+101,347)],GOLD,5,horizontal)
            stage.dot(x+51.5,347,7,GOLD,horizontal)
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
    chess_challenge,
)


FILMS["T06.E"]=(
    scene("Push four unit tiles together",lambda stage,s:squares(stage,s,motion="pushed together"),
          note("What is the outside perimeter?", "what is the perimeter")),
    scene("Count all the tile edges",lambda stage,s:squares(stage,s,separate=True),
          equation(("4 tiles",BLUE,"four tiles"),("× 4 edges",GOLD,"each tile has four edges"),
                   ("= 16 reports",MINT,"sixteen edges"))),
    scene("Find the four inside joins",lambda stage,s:squares(stage,s,joins="four inside joins"),
          equation(("2 vertical",GOLD,"two along the vertical"),("+ 2 horizontal",GOLD,"two along the horizontal"),size=36)),
    scene("Remove the two reports at each join",
          lambda stage,s:squares(stage,s,joins="both tiles beside it",boundary="the perimeter is eight"),
          equation(("16",BLUE,"sixteen minus eight"),("− 2 × 4",GOLD,"remove two reports"),
                   ("= 8",MINT,"eight is eight"),y=551)),
    scene("Rearranging the same tiles changes the boundary",
          change("now rearrange the tiles",
              (lambda stage,s:squares(stage,s,boundary="the big square"),note("4 × 2 = 8","times two is eight")),
              (lambda stage,s:squares(stage,s,motion="rearrange the tiles",row=True,from_square=True),
               equation(("16 − 2 × 3",GOLD,"three joins"),("= 10",MINT,"which is ten"))))),
    rectangle_challenge,
)
