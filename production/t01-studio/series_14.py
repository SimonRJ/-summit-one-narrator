"""Follow legal moves, rule out impossible routes and build schedules."""

from itertools import combinations

from series_marks import (BLUE, GOLD, MINT, MUTED, RED, RIM, WHITE, cards, chart, cue, equation,
                          link, network, note, ring, scene, tile)
from studio_diagrams import bead, fit


def corners(start=(455,225), gap=154):
    return [(start[0]+c*gap,start[1]+r*gap) for r in range(3) for c in range(3)]


def streets(stage,s,mode):
    pts=corners((466,218),150)
    edges=[(i,j,RIM,None) for i,j in combinations(range(9),2)
           if abs(i//3-j//3)+abs(i%3-j%3)==1]
    network(pts,[""]*9,edges,radius=13)(stage,s)
    if mode=="puzzle":
        for point,label,shift in ((pts[6],"Start",-90),(pts[2],"Finish",100)):
            fit(stage,label,point[0]+shift,point[1]+2,28,182,MINT)
        return
    result=[1,3,6,1,2,3,1,1,1] if mode!="block" else [1,1,2,1,0,1,1,1,1]
    for i,(x,y) in enumerate(pts):
        if mode=="base" and i not in (0,3,6,7,8):
            continue
        if mode=="base":
            words="write one on each"
        elif mode=="block":
            words="write zero there" if i==4 else "carry on adding" if i in (1,2,5) else None
        else:
            words={4:"the middle corner",1:"the next corners",5:"the next corners",2:"the final corner"}.get(i)
        tile(stage,x,y,result[i],RED if mode=="block" and i==4 else MINT if i==2 else BLUE,
             69,55,cue(s,words),30)


def bridge(stage,s):
    stage.line([(394,326),(582,326),(602,297),(684,297),(705,326),(888,326)],BLUE,5)
    stage.line([(640,193),(640,274)],GOLD,5)
    stage.line([(640,317),(640,477)],GOLD,5)
    for (x,y),c in (((394,326),BLUE),((888,326),BLUE),((640,193),GOLD),((640,477),GOLD)):
        bead(stage,x,y,c,1,16)
    fit(stage,"The two routes cross without a junction",640,559,37,1115,MINT,
        cue(s,"you cannot turn there") if s.scene["n"]!=1 else cue(s,"not a junction"))


SPIRAL=(0,1,2,5,8,7,6,3,4)
SPIRAL_CUES=("go along the top","go along the top","down the right side","down the right side",
             "along the bottom","along the bottom","up the left","step into the centre")


def visit_grid(stage,s,mode):
    pts=corners((479,219),144)
    pairs=[(i,j,RIM,None) for i,j in combinations(range(9),2)
           if abs(i//3-j//3)+abs(i%3-j%3)==1]
    network(pts,[""]*9,pairs,radius=17)(stage,s)
    if mode=="colour":
        for i,p in enumerate(pts):
            bead(stage,*p,BLUE if (i//3+i%3)%2==0 else GOLD,cue(s,"colour the dots"),25)
    elif mode=="path":
        for i,(a,b) in enumerate(zip(SPIRAL,SPIRAL[1:])):
            stage.arrow(pts[a],pts[b],MINT,cue(s,SPIRAL_CUES[i],delay=.22*(i%2)),4)
        for k,i in enumerate(SPIRAL,1):
            fit(stage,str(k),pts[i][0],pts[i][1]-33,23,50,MINT,
                cue(s,SPIRAL_CUES[max(0,k-2)],delay=.13*(k%2)))
    else:
        bead(stage,*pts[0],MINT,1,25)
        fit(stage,"Start",pts[0][0]-97,pts[0][1],27,156,MINT)
        fit(stage,"?",pts[4][0],pts[4][1],26,98,WHITE)


FOUR=ring(4,x=510,y=349,radius=137)
FOUR_EDGES=[(a,b,RIM,None) for a,b in combinations(range(4),2)]
SETS=(("AB","CD"),("AC","BD"),("AD","BC"))
MEET=(("AB","CE"),("AC","BE"),("AD",))
GROUP_COLOURS=(BLUE,GOLD,MINT)
MEET_POINTS=((392,343),(540,225),(531,466),(253,348),(659,344))


def meeting_net(stage,s, *, pupils="ABCD", groups=SETS, positions=FOUR, reveal=(), active=None):
    all_edges=[]
    for g,row in enumerate(groups):
        for edge in row:
            a,b=(pupils.index(ch) for ch in edge)
            all_edges.append((a,b,RIM,None))
            if reveal:
                all_edges.append((a,b,GROUP_COLOURS[g],reveal[g]))
            if active and "A" in edge:
                all_edges.append((a,b,BLUE,active))
    network(positions,pupils,all_edges,radius=26)(stage,s)


def coloured_schedule(stage,s, meeting=False):
    words=(("slot one","slot two","slot three") if meeting else ("round one","round two","round three"))
    pairs=MEET if meeting else SETS
    meeting_net(stage,s,pupils="ABCDE" if meeting else "ABCD",groups=pairs,
                positions=MEET_POINTS if meeting else FOUR,reveal=words)
    for i,row in enumerate(pairs):
        p=cue(s,words[i])
        y=258+i*91
        tile(stage,932,y," + ".join(row),GROUP_COLOURS[i],240,63,p,32)
        fit(stage,f"{'Slot' if meeting else 'Round'} {i+1}",753,y,25,147,WHITE,p)


def street_counts(stage,s):
    challenge=s.t>=s.at("notebook challenge")
    width=3 if challenge else 2
    fit(stage,"Count the routes across three blocks and up two" if challenge else "Label each legal arrival",640,87,42)
    counts={}
    for y in range(3):
        for x in range(width+1):
            xx,yy=381+150*x,492-139*y
            if x:
                stage.arrow((xx-123,yy),(xx-29,yy),RIM,1,3)
            if y:
                stage.arrow((xx,yy+111),(xx,yy+28),RIM,1,3)
            blocked=not challenge and (x,y)==(1,1) and s.t>=s.at("a blocked point")
            counts[x,y]=0 if blocked else (int((x,y)==(0,0))+counts.get((x-1,y),0)+counts.get((x,y-1),0))
            show=cue(s,("three wide" if challenge else "label each point"),delay=(x+y)*.13)
            tile(stage,xx,yy,str(counts[x,y]),RED if blocked else MINT if (x,y)==(width,2) else BLUE,69,51,show,29)
    fit(stage,"Start",294,492,26,125,MUTED)
    fit(stage,"Finish",381+150*width+109,214,26,144,MUTED)
    if challenge:
        fit(stage,"6 from the left + 4 from below = 10",640,580,36,1080,MINT,cue(s,"two high"))
    else:
        fit(stage,"A closed crossing contributes zero",640,580,33,1080,RED,cue(s,"a blocked point"))


street_counts.chapter="Your turn"


def ends_grid(stage,s):
    if s.t<s.at("notebook challenge"):
        fit(stage,"Cross off the visited dots",640,87,45)
        pts=corners((487,201),140)
        for i,p in enumerate(pts):
            for j in (i+1,i+3):
                if j<len(pts) and (j==i+3 or i//3==j//3):
                    stage.line((p,pts[j]),RIM,3)
            bead(stage,*p,BLUE if (i//3+i%3)%2==0 else GOLD,cue(s,"colouring can prove"),19)
        fit(stage,"Check that every remaining dot is reachable",640,567,34,1080,WHITE,cue(s,"everything unvisited"))
        return
    fit(stage,"Can the two top corners be the endpoints?",640,87,43)
    pts=[(439+197*(i%3),270+133*(i//3)) for i in range(6)]
    for i,p in enumerate(pts):
        for j in (i+1,i+3):
            if j<6 and (j==i+3 or i//3==j//3):stage.line((p,pts[j]),RIM,4)
    for i,p in enumerate(pts):
        bead(stage,*p,BLUE if i%2==0 else GOLD,cue(s,"two rows"),25)
    fit(stage,"Start",439,210,29,180,BLUE,cue(s,"starting at one end"))
    fit(stage,"Finish?",833,210,29,180,BLUE,cue(s,"finishing at the other"))
    for i in range(6):
        bead(stage,445+78*i,500,BLUE if i%2==0 else GOLD,cue(s,"every dot once",delay=i*.07),15)
    fit(stage,"Five steps switch colour five times. The endpoints must differ.",640,576,30,1120,WHITE,cue(s,"finishing at the other"))


ends_grid.chapter="Your turn"


def six_player_schedule(stage,s):
    if s.t<s.at("notebook challenge"):
        fit(stage,"A round is a set of disjoint games",640,87,44)
        meeting_net(stage,s,reveal=("sharing no dot",)*3,groups=(("AB","CD"),(),()))
        fit(stage,"AB and CD can take place together",640,565,36,1050,MINT,cue(s,"sharing no dot"))
        return
    fit(stage,"Schedule six players in the fewest rounds",640,87,43)
    rounds=(("AF","BE","CD"),("BF","AC","DE"),("CF","BD","AE"),("DF","CE","AB"),("EF","AD","BC"))
    chart(("Round","Game 1","Game 2","Game 3"),[((str(i+1),*row),"no player playing twice") for i,row in enumerate(rounds)],
          y=201,row_height=53,width=895,font=27)(stage,s)
    fit(stage,"15 different pairs ÷ 3 games per round = 5 rounds",640,563,34,1090,MINT,cue(s,"fewest rounds"))


six_player_schedule.chapter="Your turn"


def sixth_meeting(stage,s):
    challenge=s.t>=s.at("then decide")
    fit(stage,"Add one more meeting without adding a slot" if challenge else "Check one slot at a time",640,87,44)
    pairs=(("AB","DE"),("AC","BE"),("AD","CE")) if challenge else MEET
    words="d with e" if challenge else "build a timetable"
    for i,row in enumerate(pairs):
        y=240+94*i;show=cue(s,words,delay=i*.12)
        fit(stage,f"Slot {i+1}",395,y,31,190,WHITE,show)
        for j,pair in enumerate(row):
            tile(stage,602+j*235,y,pair,GOLD if pair=="DE" else (BLUE,MINT)[j],148,62,show,32)
    fit(stage,"A attends AB, AC and AD, so at least three slots are needed",640,546,29,1100,WHITE,cue(s,"sixth meeting" if challenge else "busiest person"))
    if challenge:fit(stage,"All six meetings fit",640,597,28,1000,MINT,cue(s,"is added"))


sixth_meeting.chapter="Your turn"


FILMS={
 "T14.1":(
    scene("The movement rules define a route",bridge),
    scene("Write one count at each point",
          network(ring(5,radius=128),"ABCDE",[(0,1,BLUE,"writing one number"),(1,2,BLUE,"writing one number"),
                  (2,3,BLUE,"writing one number"),(3,4,BLUE,"writing one number")]),
          note("Count routes into a point instead of tracing them all", "counts all routes at once")),
    scene("Move only right or up",lambda stage,s:streets(stage,s,"puzzle"),
          note("How many routes reach the top-right corner?", "how many different routes",y=588)),
    scene("The edges have only one way in",lambda stage,s:streets(stage,s,"base"),
          note("Along the bottom or up the left, just one route", "there is only one way",y=587)),
    scene("Add the routes from the left and below",lambda stage,s:streets(stage,s,"count"),
          equation(("3 + 3",BLUE,"three plus three"),("= 6 routes",MINT,"six routes"),y=575)),
    scene("A blocked corner contributes zero",lambda stage,s:streets(stage,s,"block"),
          note("Only the two outside routes remain", "only two routes remain",y=572)),
    scene("A bridge crossing is not a junction",bridge),
    street_counts,
 ),
 "T14.2":(
    scene("Look at what a move leaves behind",
          network(((339,366),(542,311),(742,311),(911,365),(542,470)),"ABCDE",
                  ((0,1,BLUE,None),(1,2,BLUE,"perfectly legal now"),(2,3,BLUE,"perfectly legal now"),
                   (1,4,GOLD,"cutting off a place")),radius=28),
          note("Leaving B can strand E", "cutting off a place")),
    scene("Spot dead ends early",
          cards((("Check the unvisited dots",BLUE),("Save a route to each",MINT)),342,
                words="checking what remains",width=376,gap=442,size=31),
          note("Can you still reach every place you must visit?", "catches dead ends early")),
    scene("Start in a corner and finish in the centre",lambda stage,s:visit_grid(stage,s,"start"),
          note("Use horizontal or vertical steps. Visit every dot once.", "visit every dot exactly once",y=564,size=31)),
    scene("A spiral visits every dot exactly once",lambda stage,s:visit_grid(stage,s,"path"),
          note("Nine dots visited; the centre is last", "the path ends in the centre",y=571)),
    scene("Every move changes chessboard colour",lambda stage,s:visit_grid(stage,s,"colour"),
          note("5 blue and 4 gold dots", "four dots",x=1012,y=370,width=362,size=31),
          note("Can the route start at a gold dot?", "can a path start",y=569)),
    scene("Starting with a side dot would require five",
          cards(tuple(("L",GOLD) if i%2==0 else ("D",BLUE) for i in range(9)),339,width=87,gap=109,
                words="would visit light"),
          note("It needs 5 light dots, but only 4 exist", "only four light dots",y=503),
          note("That starting point is impossible", "no such path exists",y=572,colour=GOLD)),
    scene("A dot with just one edge must be an endpoint",
          network(((640,340),(337,264),(927,264),(642,498)),"ABCD",
                  ((0,1,BLUE,"first or the last"),(0,2,BLUE,"first or the last"),(0,3,BLUE,"three such dots"))),
          note("Three required endpoints cannot fit on one path", "no route can visit them all",y=578,size=34)),
    ends_grid,
 ),
 "T14.3":(
    scene("A meeting is an edge between two people",
          lambda stage,s:meeting_net(stage,s,groups=(("AB","CD"),(),()),reveal=("the same time slot",)*3),
          note("In one slot, the meetings share no person", "no dot in common")),
    scene("A network makes conflicts visible",
          network(FOUR,"ABCD",((0,1,GOLD,"avoid clashes"),(0,2,GOLD,"avoid clashes"))),
          note("A cannot attend both meetings at once", "the number of slots")),
    scene("Schedule all games for four players",network(FOUR,"ABCD",FOUR_EDGES),
          note("At most one game per player per round", "at most one game per round",y=544),
          note("How many rounds are needed?", "smallest number of rounds",y=592,size=29)),
    scene("Six games take at least three rounds",network(FOUR,"ABCD",FOUR_EDGES),
          cards((("6 games",BLUE),),294,x=949,width=223,words="there are six games"),
          cards((("Up to 2 in a round",GOLD),),396,x=949,width=294,words="at most two games",size=29),
          equation(("6 ÷ 2",WHITE,"six divided by two"),("= 3 at least",MINT,"three rounds are needed"),y=570)),
    scene("Build three rounds without clashes",coloured_schedule,
          note("All six games fit in three rounds", "all six games are played")),
    scene("Five players also fit at most two games per round",
          chart(("Round","Game 1","Game 2"),[((str(i+1),*pair),"five-day pairing schedule")
                for i,pair in enumerate((("AB","CD"),("AC","BE"),("AD","CE"),("AE","BD"),("BC","DE")))],
                x=669,y=188,row_height=59,width=786),
          note("10 games ÷ 2 per round = at least 5 rounds", "takes at least five rounds",y=575,size=34)),
    scene("The busiest player gives another lower bound",
          network(((640,339),(327,251),(951,255),(638,477)),"ABCD",
                  ((0,1,BLUE,None),(0,2,GOLD,None),(0,3,MINT,None))),
          note("Three meetings for A need three distinct slots", "needs at least three slots")),
    six_player_schedule,
 ),
 "T14.E":(
    scene("Schedule only the five required meetings",
          lambda stage,s:meeting_net(stage,s,pupils="ABCDE",groups=MEET,positions=MEET_POINTS),
          note("AB, AC, AD, BE, CE", "b with e",x=967,y=328,width=415,size=33,colour=BLUE),
          note("How many slots are needed?", "the smallest number of slots")),
    scene("Three meetings use the same pupil",
          lambda stage,s:meeting_net(stage,s,pupils="ABCDE",groups=MEET,positions=MEET_POINTS,active="in three meetings"),
          note("A needs three separate slots", "at least three slots",x=986,y=346,width=395,size=30)),
    scene("Build a schedule with three slots",lambda stage,s:coloured_schedule(stage,s,meeting=True)),
    scene("Each pupil appears at most once in a slot",
          chart(("Slot","Meetings","Pupils, each once"),
                [(("1","AB + CE","A, B, C, E"),"in slot one"),
                 (("2","AC + BE","A, B, C, E"),"in slot two"),
                 (("3","AD","A, D"),"in slot three")],
                y=219,row_height=78,highlight=((0,2),(1,2),(2,2))),
          note("All five meetings scheduled", "all five meetings")),
    scene("The total meeting count gives the same lower bound",
          cards((("2 slots hold at most 4 meetings",BLUE),("There are 5 meetings",GOLD)),343,
                width=404,gap=456,words="a slot holds at most",size=27),
          note("At least 3 slots, and our construction reaches 3", "both limits say three")),
    sixth_meeting,
 ),
}
