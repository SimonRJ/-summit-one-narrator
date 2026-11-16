"""Lesson 108. Follow oriented boundaries and cancel pairs of interior edges."""
from collections import Counter
from math import sin

from visuals import AQUA, BLUE, GOLD, PINK, SOFT, VIOLET, WHITE, bounds, clamp, ease


def tile_edges(cells):
    edges = Counter()
    for x,y in cells:
        corners = bounds(x,y,1,1)
        edges.update(tuple(sorted((p,q))) for p,q in zip(corners,corners[1:]))
    return edges


L_CELLS = [(i,2) for i in range(6)] + [(0,1),(0,0)]
L_OUTLINE = [(0,3),(6,3),(6,2),(1,2),(1,0),(0,0),(0,3)]
BOARD = {(x,y) for x in range(8) for y in range(8)}
HOLE = {(x,3) for x in range(2,6)}
CORNER = {(7,0)}
OUTSIDE = [(0,0),(7,0),(7,1),(8,1),(8,8),(0,8),(0,0)]
INSIDE = [(2,3),(6,3),(6,4),(2,4),(2,3)]
assert Counter(tile_edges(L_CELLS).values()) == {1:18,2:7}
assert Counter(tile_edges(BOARD-HOLE-CORNER).values())[1] == 42


def unit_point(p,x,y,u):
    return x+p[0]*u,y+p[1]*u


def transform(points,x,y,u):
    return [unit_point(p,x,y,u) for p in points]


def rectangle(art,c,solution=False):
    x,y,u=427,186,34
    w,h=12*u,9*u
    draw = c.opening() if solution else c.after("A rectangle",1.1)
    dims = [c.after("length twelve"),c.after("length nine")] if solution else [
            c.after("twelve metres wide"),c.after("nine metres tall")]
    step = c.after("Add all four",2.2) if solution else c.after("Trace around the outside",3.1)
    a = c.says("forty-two metres") if solution else 0
    art.rect(x,y,w,h,BLUE,.11*draw)
    art.trace(bounds(x,y,w,h),draw,SOFT,3,False)
    art.dimension((x,y-13),(x+w,y-13),"12 m",AQUA,dims[0],offset=21,size=32)
    art.dimension((x+w+21,y),(x+w+21,y+h),"9 m",GOLD,dims[1],offset=-43,size=32)
    if solution:
        art.dimension((x,y+h+18),(x+w,y+h+18),"12 m",AQUA,dims[0],offset=-20,size=32)
        art.dimension((x-21,y),(x-21,y+h),"9 m",GOLD,dims[1],offset=42,size=32)
    else:
        art.label("How long is the walk?", 640, 581, 36, WHITE,c.after("What is its perimeter"),bold=True)
    corners=bounds(x,y,w,h)
    seen=0
    for i,(p,q) in enumerate(zip(corners,corners[1:])):
        length = w if i%2==0 else h
        amt=clamp((step*2*(w+h)-seen)/length)
        art.trace((p,q),amt,AQUA if i%2==0 else GOLD,7)
        seen+=length
    if solution:
        art.label("12 + 9 + 12 + 9 = 42 m",640,583,45,WHITE,a,bold=True)


def l_shape(art,c,solution=False):
    x,y,u=210,241,85
    if not solution:
        pc=c.after("six unit squares",1.85)
        stack=c.after("Add two more",1.7)
        contact=c.after("contacts between pairs",1.25)
    else:
        pc=stack=1
        contact=c.after("There are seven shared edges",2.1)
    settle=(c.after("There are seven shared edges",1.40) if solution else 1)
    spread=26*(1-settle)
    for index,(a,b) in enumerate(L_CELLS):
        p = ease(pc*1.7-index*.1) if index<6 else ease(stack*1.35-(index-6)*.3)
        if p:
            xx=x+a*u+spread*a
            yy=y+b*u+spread*b+(1-p)*21
            art.rect(xx+1,yy+1,u-2,u-2,BLUE,.22*p)
            art.trace(bounds(xx,yy,u,u),p,SOFT,3,False)
    edges=tile_edges(L_CELLS)
    pair=c.after("counted twice",1.6) if solution else 0
    for index,(p,q) in enumerate((edge for edge,n in edges.items() if n==2)):
        p,q=unit_point(p,x,y,u),unit_point(q,x,y,u)
        phase=ease(contact*1.55-index*.09)
        if phase:
            art.trace((p,q),phase,PINK,5,False)
            off = 5*pair
            if p[0]==q[0]:
                for d in (-off,off):
                    art.path(((p[0]+d,p[1]+10),(q[0]+d,q[1]-10)),PINK,2,pair)
            else:
                for d in (-off,off):
                    art.path(((p[0]+10,p[1]+d),(q[0]-10,q[1]+d)),PINK,2,pair)
            mid=((p[0]+q[0])/2,(p[1]+q[1])/2)
            art.circle(mid,12,PINK,phase)
            art.label(index+1,*mid,15,"#171d2a",phase,bold=True)
    if solution:
        trail=c.after("walking around the outside",3.6)
        art.trace(transform(L_OUTLINE,x,y,u),trail,AQUA,7)
        art.label("8 × 4 = 32",952,265,43,WHITE,c.after("four edge units each"),bold=True)
        art.label("− 2 × 7",952,353,46,PINK,pair,bold=True)
        art.label("18 units",952,482,61,AQUA,c.says("eighteen units"),bold=True)
        art.label("Some edges belonged to two squares",x+3*u,568,27,PINK,pair)
    else:
        art.dimension((x,y+3*u+14),(x+u,y+3*u+14),"1 unit",SOFT,pc,offset=-24)
        art.label("Which edges face out?",976,376,34,AQUA,c.after("What is the perimeter"),bold=True)


def cut_board(art, c, scene):
    x,y,u=240,176,54
    if scene==7:
        base=c.after("A square board",1.45)
        ho=c.after("Cut out an interior rectangle",1.6)
        cr=c.after("Then remove one square",1.1)
        dx=30*ho
    else:
        base=ho=cr=1
        dx=0
    original=transform(bounds(0,0,8,8),x,y,u)
    inner=transform(INSIDE,x,y,u)
    outer=transform(OUTSIDE,x,y,u)
    for a,b in sorted(BOARD,key=lambda p:(p[1],p[0])):
        aphase=ease(base*1.6-(a+b)*.04)
        if not aphase:
            continue
        if (a,b) in HOLE:
            op=(1-ho)*aphase
        elif (a,b) in CORNER:
            op=(1-cr)*aphase
        else:
            op=aphase
        art.rect(x+a*u+1,y+b*u+1,u-2,u-2,BLUE,.31*op)
    art.path(outer,SOFT,2,base*cr)
    art.path(original,SOFT,2,base*(1-cr))
    art.path(inner,GOLD,3,ho)
    if scene==7:
        px,py=unit_point((2,3),x,y,u)
        if 0 < ho < 1:
            art.rect(px+55*ho,py-dx,4*u,u,GOLD,.66*sin(3.14159*ho))
        k=c.after("side lengths four and one")
        art.dimension(unit_point((2,2.82),x,y,u),unit_point((6,2.82),x,y,u),"4",GOLD,k,offset=16)
        art.dimension(unit_point((6.18,3),x,y,u),unit_point((6.18,4),x,y,u),"1",GOLD,k,offset=-20)
        art.dimension((x,y+8*u+15),(x+8*u,y+8*u+15),"8 units",BLUE,base,offset=-19)
        art.label("Count both boundaries",970,345,39,WHITE,c.after("including the edge of the hole"),bold=True)
        art.label("Outside walk + hole",970,425,26,AQUA,c.after("Find the total boundary length"))
    if scene==8:
        original_colour=c.after("original outer boundary",1.6)
        for p,q in zip(original,original[1:]):
            art.dashed(p,q,SOFT,2,original_colour*.68,8)
        lost=c.after("loses two outer edges",1.1)
        exposed=c.after("exposes two equal inner edges",1.1)
        new=c.after("hole adds its full perimeter",2.0)
        art.trace(transform([(7,0),(8,0),(8,1)],x,y,u),lost,PINK,7)
        art.trace(transform([(7,0),(7,1),(8,1)],x,y,u),exposed,AQUA,7)
        art.trace(inner,new,GOLD,7)
        art.label("Outside 32 − 2 + 2 = 32",955,246,31,AQUA,original_colour,bold=True)
        art.label("Hole 4 + 1 + 4 + 1 = 10",955,349,30,GOLD,c.after("twice four plus twice one"),bold=True)
        art.label("32 + 10 = 42 units",955,503,40,WHITE,c.says("forty-two units"),bold=True)
        for p,q,text in (((6.7,0),(6.7,1),"1"),((7,1.25),(8,1.25),"1")):
            art.dimension(unit_point(p,x,y,u),unit_point(q,x,y,u),text,AQUA,exposed,offset=14,size=21)
    if scene==9:
        out=c.after("outer walk",2.1)
        inn=c.after("inner walk",1.65)
        art.trace(outer,out,AQUA,6)
        art.trace(inner,inn,GOLD,6)
        selection=c.after("filled cell on one side",1.1)
        art.arrow((748,307),point_on_board(x,y,u,5,2.5),BLUE,selection)
        art.arrow((749,409),point_on_board(x,y,u,5,3.5),GOLD,c.after("unfilled part",.8))
        art.label("Filled cell", 876,306,34,BLUE,selection,bold=True)
        art.label("Unfilled space",876,408,34,GOLD,c.after("unfilled part"),bold=True)
        art.label("Count each edge once",931,514,28,AQUA,c.after("keeps every requested edge once"))


def point_on_board(x,y,u,a,b):
    return (x+a*u,y+b*u)


def join_demo(art,c,scene):
    seam=c.after("share an edge",1.3) if scene==1 else c.after("shared edge disappears",1.4)
    outline=c.after("length of the boundary",1.5) if scene==1 else c.after("adding all individual perimeters",1.4)
    ht=166
    bx=161+(1-seam)*(-27)
    by=278
    for ox,ink in ((bx,BLUE),(bx+ht+(1-seam)*62,AQUA)):
        art.rect(ox,by,ht,ht,ink,.29)
        art.trace(bounds(ox,by,ht,ht),outline,ink,4)
    art.trace(((bx+ht,by),(bx+ht,by+ht)),seam,PINK,6)
    art.label("Shared edge",bx+ht,475,29,PINK,seam,bold=True)
    if scene==1:
        progress=c.after("A cut can create",1.2)
    else:
        progress=c.after("Cutting around a hole",1.2)
    xx,yy,w=759,221,300
    art.rect(xx,yy,w,w,BLUE,.20*progress)
    art.trace(bounds(xx,yy,w,w),progress,AQUA,4)
    hole=(xx+92,yy+108,114,78)
    art.rect(*hole,"#111927",progress)
    art.trace(bounds(*hole),progress,GOLD,5)
    if scene==10:
        art.label("Include it when asked",909,570,27,GOLD,c.after("Include it if the problem asks"),bold=True)
    else:
        art.label("The cut makes a second boundary",909,570,26,GOLD,progress,bold=True)


def transfer(art,c,recap=False):
    x,y,u=242,267,72
    if recap:
        base=c.after("Mark shared and exposed edges")
        edge=c.after("units for perimeter",1.7)
        cut=c.after("old edges disappear",1.3)
        appear=c.after("new ones appear",1.3)
    else:
        base=c.after("a stepped outline",1.3)
        edge=c.after("Mark shared edges",1.7)
        cut=c.after("make several cuts",1.3)
        appear=c.after("changes the boundary length",1.3)
    for a,b in L_CELLS:
        art.rect(x+a*u+1,y+b*u+1,u-2,u-2,BLUE,.23*base)
    art.trace(transform(L_OUTLINE,x,y,u),max(.17*base,edge),AQUA,6)
    for (a,b),n in tile_edges(L_CELLS).items():
        if n==2:
            art.trace(transform((a,b),x,y,u),base,PINK,4,False)
    art.label("Exposed boundary",x+3*u,540,28,AQUA,edge,bold=True)
    ox,oy=846,244
    art.rect(ox,oy,222,222,BLUE,.19*cut)
    art.trace(bounds(ox,oy,222,222),cut,SOFT,2)
    art.rect(ox+155,oy,67,67,"#111927",appear)
    art.trace(((ox+155,oy),(ox+222,oy),(ox+222,oy+67)),cut,PINK,5)
    art.trace(((ox+155,oy),(ox+155,oy+67),(ox+222,oy+67)),appear,AQUA,5)
    art.label("Lost edges",837,521,28,PINK,cut,bold=True)
    art.label("New edges",1052,521,28,AQUA,appear,bold=True)


TITLES = {
    1:("Follow the boundary",None),
    2:("Spot the outside edge","AMC Upper Primary  ·  Rossmoyne-style reasoning"),
    3:("Walk around a 12 m by 9 m rectangle",None),
    4:("Add the four side lengths",None),
    5:("Build an L from eight unit squares",None),
    6:("A shared edge was counted twice",None),
    7:("Two cuts, two effects",None),
    8:("Track the lost and new edges",None),
    9:("Two distinct boundary walks",None),
    10:("A shared edge and a hole are different",None),
    11:("Mark what changes",None),
}


def draw(art,c,scene):
    title, subtitle = TITLES[scene]
    art.heading(title,AQUA,subtitle)
    if scene in (1,10):
        join_demo(art,c,scene)
    elif scene in (2,11):
        transfer(art,c,scene==11)
    elif scene in (3,4):
        rectangle(art,c,scene==4)
    elif scene in (5,6):
        l_shape(art,c,scene==6)
    else:
        cut_board(art,c,scene)
