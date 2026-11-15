"""Carry angles along parallel lines and connect chords with central angles."""

import math

from geometry_marks import corner, dashed, direction, polar, region, right_mark, sector
from series_marks import (BLUE, GOLD, MINT, MUTED, RED, RIM, WHITE, board, cards, cue,
                          equation, exercise, link, note, scene, tile)
from stage import mix
from studio_diagrams import fit


def angle_facts(stage,s):
    a,b=(362,368),(899,355)
    stage.line([(190,368),(532,368)],BLUE,4)
    stage.line([a,polar(a,-67,155)],BLUE,4)
    sector(stage,a,-180,180,74,GOLD,opacity=cue(s,"a straight line"),label="180°",at=(360,482))
    stage.line([(733,355),(1065,355)],BLUE,4)
    stage.line([polar(b,51,153),polar(b,231,153)],BLUE,4)
    q=cue(s,"angles opposite each other")
    sector(stage,b,0,51,70,MINT,opacity=q,label="a")
    sector(stage,b,180,51,70,MINT,opacity=q,label="a")


def parallels(stage,s, *, mode):
    y1,y2=242,424
    upper=(705,y1)
    lower=(705-(y2-y1)/math.tan(math.radians(65)),y2)
    for y in (y1,y2):
        stage.line([(260,y),(1060,y)],BLUE,4)
        stage.line([(330,y-10),(346,y),(330,y+10)],BLUE,4)
    stage.line([polar(upper,-65,76),polar(lower,115,113)],WHITE,4)
    expected=mode=="solve"
    sector(stage,upper,-65,65,64,GOLD,label="65°")
    if mode=="slide":
        p=cue(s,"slide it down",duration=.88)
        x,y=mix(upper[0],lower[0],p),mix(upper[1],lower[1],p)
        sector(stage,(x,y),-65,65,64,MINT,opacity=cue(s,"slide it down"),label="65°")
    elif expected:
        sector(stage,lower,-65,65,64,GOLD,label="65°")
    solved=expected and cue(s,"one hundred and fifteen")>.45
    sector(stage,lower,-180,115,84,MINT if solved else BLUE,
           label="115°" if solved else "?",at=(547,351))


def triangle_sum(stage,s):
    a,b,c=(385,461),(928,461),(585,213)
    region(stage,(a,b,c),BLUE,tint=.13)
    stage.line([(315,a[1]),(1056,a[1])],BLUE,3)
    p=cue(s,"draw a line through the top")
    stage.line([(299,c[1]),(1025,c[1])],MINT,4,p)
    left=abs(direction(a,c));right=180+direction(b,c)
    start=cue(s,"the two base angles reappear",duration=1.0)
    corner(stage,a,b,c,52,GOLD,label="a")
    corner(stage,b,a,c,52,MINT,label="b")
    a_copy=(mix(a[0],c[0],start),mix(a[1],c[1],start))
    b_copy=(mix(b[0],c[0],start),mix(b[1],c[1],start))
    sector(stage,a_copy,180,-left,76,GOLD,opacity=start,label="a")
    sector(stage,b_copy,0,right,76,MINT,opacity=start,label="b")
    sector(stage,c,right,180-left-right,77,BLUE,opacity=start,label="c")


def isosceles(stage,s):
    tip=(640,201);base_y=504
    dx=(base_y-tip[1])*math.tan(math.radians(20))
    a,b=(640-dx,base_y),(640+dx,base_y)
    region(stage,(tip,a,b),BLUE,tint=.17)
    corner(stage,tip,a,b,61,GOLD,label="40°")
    for v,o in ((a,b),(b,a)):
        corner(stage,v,o,tip,45,MINT,opacity=cue(s,"seventy each"),label="70°")
        xx,yy=(v[0]+tip[0])/2,(v[1]+tip[1])/2
        stage.line([(xx-10,yy),(xx+10,yy)],BLUE,4)


def clock_diagram(stage,s, *, mode):
    proof=mode=="proof"
    semicircle=mode=="half"
    x=484 if proof else 642
    center=(x,348)
    radius=154 if proof else 162
    pts=[polar(center,-90+30*i,radius) for i in range(12)]
    stage.box(x-radius,348-radius,radius*2,radius*2,radius=radius,fill=None,edge=BLUE,stroke=3)
    for i,p in enumerate(pts):
        stage.dot(*p,4,BLUE)
        a,b=polar(center,-90+30*i,radius-19)
        fit(stage,str(i or 12),a,b,20,53,WHITE)
    if mode=="spokes":
        p=cue(s,"twelve equal angles")
        for point in pts:
            stage.line([center,point],BLUE,2,p*.62)
        sector(stage,center,-90,30,74,GOLD,opacity=p,label="30°")
        return
    a,b=pts[0],pts[6 if semicircle else 4]
    sector(stage,center,90 if semicircle else -90,180 if semicircle else 120,56,
           GOLD,label="180°" if semicircle else "120°" if mode!="question" else "?",
           at=(x-55,348) if semicircle else (x+68,321))
    for dest in (a,b):
        stage.line([center,dest],GOLD,3)
    if mode=="gaps":
        for i in range(4):
            arc=[polar(center,-90+i*30+2*k,radius+5) for k in range(16)]
            stage.line(arc,(BLUE,MINT,GOLD,MINT)[i],6,cue(s,"four gaps",delay=i*.15))
        return
    if mode=="question":
        return
    c=pts[3 if semicircle else 8]
    p=cue(s,"draw the radius" if proof else "a point on the circle" if mode=="edge" else "the angle on the circle")
    stage.line([a,c,b],BLUE,4,p)
    if proof:
        stage.line([center,c],MINT,4,p)
        corner(stage,c,a,center,57,BLUE,opacity=p,label="a")
        corner(stage,c,center,b,57,MINT,opacity=p,label="b")
        fit(stage,"180° − 2a",930,246,34,465,BLUE,cue(s,"minus two a"))
        fit(stage,"180° − 2b",930,340,34,465,MINT,cue(s,"minus two b"))
        fit(stage,"360° − both = 2a + 2b",930,440,33,449,GOLD,cue(s,"two a plus two b"))
    else:
        corner(stage,c,a,b,50,MINT,opacity=p,label="90°" if semicircle else "60°")


def bend_diagram(stage,s,mode):
    b=(756,342)
    a=(b[0]-132/math.tan(math.radians(35)),210)
    c=(b[0]-142,484)
    for y in (a[1],c[1]):
        stage.line([(252,y),(1040,y)],BLUE,4)
    stage.line([a,b,c],WHITE,5)
    sector(stage,a,0,35,75,GOLD,label="35°")
    sector(stage,c,-45,45,68,MINT,label="45°")
    if mode=="intro":
        word="a good extra line"
    elif mode=="add":
        word="draw a line through the bend"
    else:
        word=None
    if mode!="question":
        dashed(stage,(252,b[1]),(1059,b[1]),BLUE,cue(s,word))
    if mode=="solve":
        sector(stage,b,180,35,77,GOLD,opacity=cue(s,"matches the thirty-five"),label="35°",at=(629,294))
        sector(stage,b,135,45,77,MINT,opacity=cue(s,"the lower part matches"),label="45°",at=(632,381))
    elif mode=="question":
        corner(stage,b,a,c,78,GOLD,label="?")


def tilted_square(stage,s):
    w=74
    left,top=333,206
    at=lambda c,r:(left+c*w,top+r*w)
    pts=[at(*q) for q in ((1,0),(4,1),(3,4),(0,3))]
    board(4,4,width=w,x=481,y=354)(stage,s)
    region(stage,pts,MINT,opacity=cue(s,"tilted square"),tint=.20)
    across=cue(s,"three squares to the right")
    down=cue(s,"one square down")
    stage.line((pts[0],at(4,0)),BLUE,4,across)
    stage.line((at(4,0),pts[1]),BLUE,4,down)
    fit(stage,"3",left+2.5*w,top-22,26,56,BLUE,across)
    fit(stage,"1",left+4*w+27,top+.5*w,26,48,BLUE,down)
    q=cue(s,"four corner triangles")
    for i,p in enumerate((at(4,0),at(4,4),at(0,4),at(0,0))):
        region(stage,(pts[i],p,pts[(i+1)%4]),GOLD,opacity=q,tint=.17)
    fit(stage,"Outer area 16",935,250,31,421,BLUE,cue(s,"area sixteen"))
    fit(stage,"4 corners total 6",935,352,31,421,GOLD,cue(s,"six altogether"))
    fit(stage,"16 − 6 = 10",935,467,40,421,MINT,cue(s,"sixteen minus six"))


def triangle_height(stage,s):
    a,b,c,d=(394,460),(892,460),(585,224),(585,460)
    region(stage,(a,b,c),BLUE)
    p=cue(s,"dropping a perpendicular")
    dashed(stage,c,d,GOLD,p)
    right_mark(stage,d,colour=GOLD,opacity=p)


def exterior(stage,s, *, mode):
    p=cue(s,"sixty and fifty-five",duration=1.0) if mode=="change" else 0
    angle_b=67-12*p
    length=267
    b,c,d=(400,497),(400+length,497),(1029,497)
    tb,tc=math.tan(math.radians(angle_b)),math.tan(math.radians(65))
    dx=length*tc/(tb+tc)
    a=(400+dx,497-dx*tb)
    region(stage,(a,b,c),BLUE,tint=.11)
    stage.line([b,d],WHITE,4)
    for point,label,delta in ((a,"A",(0,-23)),(b,"B",(-28,14)),(c,"C",(0,30)),(d,"D",(18,23))):
        fit(stage,label,point[0]+delta[0],point[1]+delta[1],26,94,WHITE)
    corner(stage,a,b,c,55,BLUE,label=f"{round(115-angle_b)}°")
    corner(stage,b,a,c,51,GOLD,label=f"{round(angle_b)}°")
    if mode!="question":
        corner(stage,c,a,b,46,BLUE,label="65°",opacity=cue(s,"sixty-five degrees") if mode=="inside" else 1)
    if mode=="sum":
        q=cue(s,"forty-eight plus sixty-seven")
        sector(stage,c,-115,48,88,BLUE,opacity=q,label="48°")
        sector(stage,c,-67,67,88,GOLD,opacity=q,label="67°")
    elif mode!="inside":
        q=cue(s,"outside angle is") if mode=="outside" else 1
        corner(stage,c,a,d,79,MINT,opacity=q,label="?" if mode=="question" else "115°")


FILMS={
 "T12.1":(
    scene("Build a chain of angle facts",angle_facts,
          note("A full turn is 360°","a full turn makes",y=560)),
    scene("Use the stated facts",
          cards((("Given angles",BLUE),("Valid angle rules",MINT)),343,gap=397,width=335,words="use the stated facts"),
          note("Name the rule that justifies each step","which angle rule")),
    scene("Find the marked lower angle",lambda stage,s:parallels(stage,s,mode="question")),
    scene("Parallel lines keep corresponding angles equal",lambda stage,s:parallels(stage,s,mode="slide"),
          note("The lower crossing has the same 65° angle","matching position")),
    scene("Angles on a straight line sum to 180°",lambda stage,s:parallels(stage,s,mode="solve"),
          equation(("180° − 65°",WHITE,"one hundred and eighty"),("= 115°",MINT,"one hundred and fifteen"),y=568)),
    scene("Copy the triangle’s base angles to the top",triangle_sum,
          note("The three interior angles total 180°", "add up to one hundred and eighty")),
    scene("Equal sides have equal opposite angles",isosceles,
          equation(("180° − 40°",GOLD,"the top angle is forty"),("= 140°",WHITE,"one hundred and forty"),
                   ("   Half is 70°",MINT,"seventy each"),y=563,size=37)),
    exercise((("Build a chain","build a chain"),("Name each fact","name the fact")),
             "notebook challenge",("An isosceles triangle has two angles of 55°.","What is its third angle?")),
 ),
 "T12.2":(
    scene("Twelve equal gaps share a full turn",lambda stage,s:clock_diagram(stage,s,mode="spokes"),
          equation(("360° ÷ 12",BLUE,"shared into twelve"),("= 30° per gap",MINT,"thirty degrees"),y=560,size=40)),
    scene("Choose where the angle is measured",lambda stage,s:clock_diagram(stage,s,mode="question"),
          note("At the centre or at a point on the circle?", "a point on the circle itself")),
    scene("Join twelve and four to the centre",lambda stage,s:clock_diagram(stage,s,mode="question"),
          note("Find the smaller angle between the spokes", "what angle is made")),
    scene("Count four gaps, not five points",lambda stage,s:clock_diagram(stage,s,mode="gaps"),
          equation(("4 × 30°",BLUE,"four times thirty"),("= 120°",MINT,"one hundred and twenty"),y=559,size=43)),
    scene("View the same arc from the edge",lambda stage,s:clock_diagram(stage,s,mode="edge"),
          note("120° at the centre, 60° at the edge","sixty degrees")),
    scene("Two isosceles triangles explain the half",lambda stage,s:clock_diagram(stage,s,mode="proof"),
          note("The angle at eight is a + b", "twice the whole angle",y=574)),
    scene("The angle in a semicircle is a right angle",lambda stage,s:clock_diagram(stage,s,mode="half"),
          note("Half of 180° is 90°", "the angle on the circle is ninety")),
    exercise((("Share the full turn","share three hundred"),("Count gaps","count gaps"),
              ("Same arc: halve at the edge","the angle on the circle")),
             "notebook challenge",("On a clock circle, find the smaller central angle","between two o’clock and seven o’clock.")),
 ),
 "T12.3":(
    scene("An extra line can connect what you know",lambda stage,s:bend_diagram(stage,s,"intro"),
          note("Choose a line with a purpose","when you can say what it is for")),
    scene("Choose a useful extra line",
          cards((("Parallel line",BLUE),("Height",GOLD),("Equal sides",MINT)),341,width=276,gap=315,
                words="a parallel line"),
          note("Look for a line that gives you a fact", "learning which lines")),
    scene("Find the angle where the path bends",lambda stage,s:bend_diagram(stage,s,"question")),
    scene("Draw a parallel line through the bend",lambda stage,s:bend_diagram(stage,s,"add"),
          note("The new line divides the unknown angle","splits the bend angle")),
    scene("Use alternate angles on both sides",lambda stage,s:bend_diagram(stage,s,"solve"),
          equation(("35°",GOLD,"matches the thirty-five"),("+ 45°",BLUE,"matches the forty-five"),
                   ("= 80°",MINT,"eighty degrees"),y=573)),
    scene("Find a tilted square’s area by subtraction",tilted_square),
    scene("A height gives two right triangles",triangle_height,
          note("A perpendicular gives an exact height","splits an awkward triangle")),
    exercise((("Use a purposeful line","add a line only"),("Carry angles or add a height","parallel lines carry"),
              ("Use an exact grid","a grid makes areas exact")),"notebook challenge",
             ("One side of a tilted grid square goes 2 squares right and 1 down.","What is its area?")),
 ),
 "T12.E":(
    scene("Find the angle outside the triangle",lambda stage,s:exterior(stage,s,mode="question")),
    scene("Find the remaining inside angle",lambda stage,s:exterior(stage,s,mode="inside"),
          equation(("180° − 48° − 67°",WHITE,"one hundred and eighty minus"),("= 65°",MINT,"sixty-five degrees"),y=579)),
    scene("The two angles at C share a straight line",lambda stage,s:exterior(stage,s,mode="outside"),
          equation(("180° − 65°",WHITE,"one hundred and eighty minus"),("= 115°",MINT,"one hundred and fifteen"),y=579)),
    scene("The two far interior angles add to the outside angle",lambda stage,s:exterior(stage,s,mode="sum"),
          equation(("48° + 67°",WHITE,"forty-eight plus sixty-seven"),("= 115°",MINT,"one hundred and fifteen"),y=579)),
    scene("Change the shape and check the relationship",lambda stage,s:exterior(stage,s,mode="change"),
          equation(("60° + 55°",WHITE,"sixty and fifty-five"),("= 115°",MINT,"one hundred and fifteen"),y=579)),
    exercise((("Locate the far inside angles","the sum of the two far"),("Add them","the outside angle equals")),
             "then find",("The two far interior angles are 35° and 80°.","Find the exterior angle.")),
 ),
}
