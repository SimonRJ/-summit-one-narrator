"""Angle diagrams, symmetry orbits, painted solids and practical nets."""

from itertools import combinations, product
from math import comb, cos, radians, sin

from story import Example, Topic, chain, cubes, geometry, grid, say, table, tiles


def triangle_points(b, c):
    b,c=map(radians,(b,c))
    height=sin(b)*sin(c)/sin(b+c)
    return (height*cos(b)/sin(b),height)


def angles(lesson):
    v=lesson.visit
    first=37+7*v
    b,c=44+v,58+2*v
    a=180-b-c
    apex=triangle_points(b,c)
    triangle=geometry(((0,0,"B"),(1,0,"C"),(*apex,"A"),(1.37,0,"D")),
                      ((0,1,0),(0,2,0),(1,2,0),(1,3,1)),polygons=((0,1,2),))
    angle_a=46+6*v
    angle_b=52+v
    angle_c=180-angle_a-angle_b
    peak=triangle_points(angle_b,angle_c)
    centre=triangle_points(angle_b/2,angle_c/2)
    outside=(peak[0]*1.38,peak[1]*1.38,"P")
    challenge=geometry(((0,0,"B"),(1,0,"C"),(*peak,"A"),(*centre,"I"),outside),
                       ((0,1,0),(0,2,0),(1,2,0),(2,4,1),(0,3,2),(1,3,2)),polygons=((0,1,2),(0,1,3)))
    small=geometry(((-1,0,"L"),(0,0,"O"),(1,0,"R"),(cos(radians(first)),sin(radians(first)),"X")),
                   ((1,0,0),(1,2,0),(1,3,1)))
    answer=90+angle_a//2
    assert 180-(angle_b+angle_c)/2==answer
    return Topic(
        (("An angle is a turn between two rays. When angles share a straight line, a vertex or a triangle, their sum gives you an equation.", "Use a known whole angle to find its parts."),
         ("Label the vertex first. A short angle chase can link two separate triangles.", "Follow angle relationships across the diagram.")),
        (("In AMC practice, mark a straight line and any angles you can read once you extend a side. Often that reveals a triangle sum.", "AMC Upper Primary · mark a known angle sum"),
         ("A Rossmoyne style question may add bisectors or an extension. Write the half angles and look for a sum you already know.", "Rossmoyne-style · combine angle rules")),
        (
            Example("Find the other part of a straight angle", (
                (f"Points L, O and R lie in that order on a straight line. Angle X O R is {say(first)} degrees. Find angle L O X.", f"∠XOR = {first}°. Find ∠LOX."),
                ("The two requested parts meet at O on a straight line.", "Their sum is 180°.")),
                ((f"Angle L O X and angle X O R together make the whole turn from ray O L to ray O R. That turn is one hundred and eighty degrees.", "∠LOX + ∠XOR = 180°."),
                 (f"Subtract {say(first)} degrees to get {say(180-first)} degrees for angle L O X.", f"180° − {first}° = {180-first}°.")),small),
            Example("Use a triangle and extend one side", (
                (f"In triangle A B C, the angles at B and C are {say(b)} and {say(c)} degrees. Extend B C through C to a point D.", f"∠ABC = {b}°, ∠ACB = {c}°. Find ∠ACD."),
                ("Find the interior angle at A and the exterior angle at C.", "Use the triangle sum and the straight line.")),
                ((f"Inside the triangle the three angles add to one hundred and eighty. The angle at A is {say(a)} degrees.", f"∠A = 180° − {b}° − {c}° = {a}°."),
                 (f"The exterior angle at C forms a straight line with the interior angle of {say(c)} degrees. The exterior angle is {say(180-c)} degrees.", f"∠ACD = 180° − {c}° = {180-c}°."),
                 ("It also equals the sum of the two interior angles at A and B. That gives a quick check.", f"{a}° + {b}° = {180-c}°.")),triangle),
            Example("Find the angle where two bisectors meet", (
                (f"Extend B A past A to P. The exterior angle C A P equals {say(180-angle_a)} degrees. The interior angle bisectors from B and C meet at I.", f"∠CAP = {180-angle_a}°. I lies on both interior bisectors."),
                ("Find angle B I C. Neither angle at B nor angle at C is given on its own.", "Find ∠BIC from a sum.")),
                ((f"The interior angle A is supplementary to C A P. It equals {say(angle_a)} degrees. Therefore B plus C is {say(180-angle_a)} degrees.", f"∠A = {angle_a}°; ∠B + ∠C = {180-angle_a}°."),
                 (f"The small triangle B I C uses half the angle at B and half the angle at C. Those two half angles together make {say((180-angle_a)//2)} degrees.", f"½(∠B + ∠C) = {(180-angle_a)//2}°."),
                 (f"Subtract that from the triangle sum. Angle B I C is {say(answer)} degrees.", f"∠BIC = 180° − {(180-angle_a)//2}° = {answer}°.")),
                challenge,proof=(("Changing the shape of the large triangle while keeping angle A fixed changes the two half angles separately. Their sum stays the same.", "Only the sum of the two half angles matters."),
                  ("This gives a shortcut for any such pair of interior bisectors. Angle B I C equals ninety degrees plus half of angle A.", "∠BIC = 90° + ½∠A.")),proof_art=challenge),
        ),
        (("The middle letter of an angle name gives the vertex. Angle A B C is at B, even when A is the first letter you read.", "Mark the first letter as the vertex", "Locate the middle letter first"),
         ("An angle labelled outside a triangle usually does not belong in the interior sum. Use the straight line to move inside first.", "Include the exterior angle in the triangle sum", "Find the interior supplement first")),
        (("Copy the diagram and mark angle totals you can justify. Use the units and symbols attached to the correct vertex.", "Mark straight lines and triangles", "Record the angle sum you use."),
         ("When two unknown angles occur only as a sum, work with that sum directly. Check the angle you found is the one requested.", "Use sums of unknown angles", "Follow the angle name to the correct vertex.")),
        cover=triangle,
    )


def symmetry(lesson):
    v=lesson.visit
    x,y=2+v,1+v
    sx,sy=2+v,3+v
    dx,dy=5+v,-1-v
    final=(dx-sy,sx+dy)
    half=2+v
    side=2*half+1
    board=grid(*tuple(tuple("◆" if x0==half and y0==half else "•" if x0==half or y0==half else "□"
                          for x0 in range(side)) for y0 in range(side)),highlight=((half,half),))
    orbits={
        frozenset(product({x0,side-1-x0},{y0,side-1-y0}))
        for x0,y0 in product(range(side),repeat=2)
    }
    counts={size:sum(len(orbit)==size for orbit in orbits) for size in (1,2,4)}
    assert counts=={1:1,2:2*half,4:half*half}
    total=counts[4]+comb(counts[2],2)
    assert total==sum(sum(map(len,sel))==5 for k in (2,3) for sel in combinations(orbits,k))
    basic_art=geometry(((0,-1,""),(0,y+1,""),(x,y,"P"),(-x,y,"P′")),((0,1,3),(2,3,1)))
    rotation_art=geometry(((-sy-1,0,""),(max(sx,final[0])+1,0,""),(0,-1,""),(0,max(sy,final[1])+1,""),
        (sx,sy,"P"),(-sy,sx,"Q"),(*final,"R")),((0,1,3),(2,3,3),(4,5,0),(5,6,1)))
    return Topic(
        (("A symmetry leaves a shape or colouring the same after a transformation. A reflection mirrors each point across a line.", "Pair points that a mirror swaps."),
         ("If several reflections are required, one marked cell may force several other cells. Work with the whole group at once.", "Follow all the positions that move together.")),
        (("A competition practice question can ask where a point lands after a flip or a turn. Mark the mirror or the centre and keep the order of moves.", "AMC Upper Primary · track the image after each move"),
         ("A Rossmoyne style colouring problem can require two symmetries at once. Count groups of linked cells instead of making every colouring.", "Rossmoyne-style · count groups of matching cells")),
        (
            Example("Reflect a point in the vertical axis", (
                (f"Point P is {say(x)} units right of the vertical axis and {say(y)} units above the horizontal axis. Reflect it across the vertical axis.", f"P = ({x}, {y}). Reflect across x = 0."),
                ("Which coordinate changes sign?", "The mirror is vertical.")),
                ((f"Keep the height of {say(y)}. Move from {say(x)} units on the right to {say(x)} units on the left.", f"Preserve y = {y}; reverse the horizontal offset."),
                 (f"The reflected point is at minus {say(x)}, {say(y)}. Both points are equally far from the vertical mirror.", f"P′ = ({-x}, {y}).")),basic_art),
            Example("Compose a quarter turn with a translation", (
                (f"Start at coordinates {say(sx)}, {say(sy)}. Rotate ninety degrees anticlockwise about the origin. Then move {say(dx)} units right and {say(-dy)} units down.", f"Start ({sx}, {sy}). Turn 90° anticlockwise, then translate."),
                ("Find the final point. Complete the turn before the move.", "What are the final coordinates?")),
                ((f"A ninety-degree anticlockwise turn sends a rightward offset to the upward direction and an upward offset to the left. The new point is minus {say(sy)}, {say(sx)}.", f"Rotate (x,y) → (−y,x): Q = ({-sy}, {sx})."),
                 (f"Now add the horizontal move and subtract the downward move. The result is {say(final[0])}, {say(final[1])}.", f"R = ({-sy} + {dx}, {sx} − {-dy}) = {final}."),
                 ("The move acts on the point after the turn. Changing the order can produce a different point.", "Apply each rule to the previous result.")),rotation_art),
            Example("Count colourings symmetric in both centre lines", (
                (f"On a square board with {say(side)} rows and {say(side)} columns, colour exactly five cells. The pattern must be unchanged by both the horizontal and the vertical centre-line reflections.", f"{side} × {side} board. Colour exactly 5 cells with both mirror symmetries."),
                ("Count the patterns on the fixed board. Patterns with different coloured positions count separately.", "How many patterns are possible?")),
                ((f"The centre stands alone. On either centre line, each noncentral cell has a partner, giving {say(counts[2])} pairs in all.", f"1 centre, {counts[2]} pairs on the axes."),
                 (f"An off-axis cell has three partners. The four quadrants have matching positions, producing {say(counts[4])} separate groups of four.", f"Off-axis: {half} × {half} = {counts[4]} groups of 4."),
                 ("Because five is odd and every other group has even size, the centre must be coloured. Complete the last four with one four-cell group or two pairs.", "5 = centre + 4, or centre + 2 + 2.")),
                board,proof=(
                    (f"Choose one of the {say(counts[4])} groups of four, or two of the {say(counts[2])} pairs. The pair choice can be made in {say(comb(counts[2],2))} ways.", f"One group: {counts[4]}. Two pairs: {counts[2]} × {counts[2]-1} ÷ 2 = {comb(counts[2],2)}."),
                    (f"Add the cases, giving {say(total)} patterns. The two cases are distinct because only one colours any off-axis cell.", f"{counts[4]} + {comb(counts[2],2)} = {total}.")),
                proof_art=table(("Group size","Available"),(1,1),(2,counts[2]),(4,counts[4]))),
        ),
        (("For a vertical mirror the sideways distance changes side. The height stays exactly the same.", "Flip both coordinate signs", "Change only the coordinate across the mirror"),
         ("A cell off both axes must travel under both reflections. One reflected copy is not enough.", "Colour only one mirrored partner", "Include every cell in the reflection group")),
        (("Find the mirror line, turn centre or translation. Track one labelled point at a time and record the new position.", "Mark the transformation", "Keep its order and centre clear."),
         ("For a symmetric pattern, use entire groups of matching cells. Build the requested total with legal group sizes, and count one case at a time.", "Count whole groups", "Check each candidate meets all requested symmetries.")),
        cover=grid(("•","□","•"),("□","◆","□"),("•","□","•"),highlight=((1,1),)),
    )


def painted_block(w,d,h,top):
    sx=w-1
    sy=d-1
    sz=h-1
    cells=set(product(range(w),range(d),range(h)))
    painted=[]
    for x,y,z in cells:
        for visible,on_face in (((1,0,0),x==sx),((0,1,0),y==sy),((0,0,1),top and z==sz)):
            if on_face:
                painted.append((x,y,z,*visible))
    return {**cubes(cells),"painted":painted}


def paint(lesson):
    v=lesson.visit
    side=3+v
    w,d,h=4+v,3+v%3,3+v%2
    both=4*(w+d+h-6)
    assert both==sum((x in (0,w-1))+(y in (0,d-1))+(z in (0,h-1))==2
                    for x,y,z in product(range(w),range(d),range(h)))
    ww,dd,hh=5+v,4+v%3,3+v%4
    bottom=2*(ww+dd-4)
    upper=4*(hh-1)
    answer=bottom+upper
    assert answer==sum((x in (0,ww-1))+(y in (0,dd-1))+(z==0)==2
                       for x,y,z in product(range(ww),range(dd),range(hh)))
    bottom_map=grid(*tuple(tuple("3" if x in (0,ww-1) and y in (0,dd-1) else
        "2" if x in (0,ww-1) or y in (0,dd-1) else "1" for x in range(ww)) for y in range(dd)),
        highlight=tuple((y,x) for y in range(dd) for x in range(ww) if (x in (0,ww-1)) != (y in (0,dd-1))))
    return Topic(
        (("When you paint the outside of a cube block, the small pieces get different numbers of painted faces. Their position tells you how many.", "Location determines how many faces receive paint."),
         ("Check the corners, edges, face interiors and hidden cells. If one surface is unpainted, the old category counts can change.", "Count by the surfaces each small cube touches.")),
        (("An AMC practice problem can describe a painted cube before it is split. Count the unit cubes after splitting, using the original outside surface.", "AMC Upper Primary · classify the boundary cells"),
         ("In a Rossmoyne style extension, a different set of faces may be painted. Split the solid into layers where the rule is consistent.", "Rossmoyne-style · inspect painted and unpainted surfaces")),
        (
            Example("Identify cubes with three painted faces", (
                (f"A solid cube built from {say(side)} by {say(side)} by {say(side)} unit cubes has all six big faces painted. How many unit cubes have three painted faces?", f"{side} × {side} × {side}; paint all 6 faces."),
                ("Find the positions where three outside faces touch.", "Which cubes touch three painted faces?")),
                (("A corner touches three of the large faces. Along the interior of an edge a cube touches only two.", "Three painted faces means a corner."),
                 ("There are four corner cubes on the top layer and four on the bottom layer. There are eight in all.", "4 top + 4 bottom = 8.")),painted_block(side,side,side,True)),
            Example("Count exactly two painted faces on every edge", (
                (f"Paint all six faces of a solid {say(w)} by {say(d)} by {say(h)} cuboid. How many small cubes have exactly two faces painted?", f"Cuboid {w} × {d} × {h}; count exactly 2 painted faces."),
                ("A corner touches three large faces. Remove the corners from the edge counts.", "Count the interiors of the twelve edges.")),
                ((f"There are four edges of each length. The edges of lengths {say(w)}, {say(d)} and {say(h)} have {say(w-2)}, {say(d-2)} and {say(h-2)} cubes between their endpoints.", f"Per edge: {w} − 2, {d} − 2, {h} − 2."),
                 (f"Multiply the sum of these three counts by four. This gives {say(both)} cubes with exactly two painted faces.", f"4 × ({w-2} + {d-2} + {h-2}) = {both}.")),painted_block(w,d,h,True)),
            Example("Count again when the top is left unpainted", (
                (f"A cuboid is {say(ww)} unit cubes wide, {say(dd)} deep and {say(hh)} high. Paint the four vertical sides and the bottom. Leave the top unpainted.", f"{ww} × {dd} × {hh}; paint the sides and bottom only."),
                ("How many pieces have exactly two painted faces after splitting it into unit cubes?", "Count the bottom layer and all other layers separately.")),
                ((f"The bottom layer already supplies one painted face. Exactly two requires one more, so count the bottom edge positions excluding its four corners.", f"Bottom layer: 2({ww}−2) + 2({dd}−2) = {bottom}."),
                 (f"Every layer above the bottom has painted vertical faces only. The four corner positions of each layer touch two side faces. The top layer follows this same rule.", f"Above the bottom: 4 × ({hh}−1) = {upper}."),
                 (f"Add the bottom and upper layer counts. There are {say(answer)} cubes with exactly two painted faces.", f"{bottom} + {upper} = {answer}.")),
                painted_block(ww,dd,hh,False),worked_art=bottom_map,proof=(
                    (f"On the bottom map, the corners have three, sides between corners have two, and the interior has one. Above that layer, remove the bottom contribution from the same positions.", "Each upper layer has four cells with exactly two."),
                    ("This checks the classification covers every unit cube. No inner cell on an upper layer reaches a painted side.", "Every cell fits one layer and one boundary type.")),
                proof_art=table(("Layers","Cubes with 2 faces"),("Bottom",bottom),(f"Other {hh-1}",upper),("Total",answer))),
        ),
        (("A corner of an entirely painted block touches three faces. Subtract the endpoints before counting edge positions with exactly two.", "Keep the ends of all twelve edges", "Exclude corners when counting exactly two"),
         ("An unpainted face adds zero to a cube's painted-face count. A top corner may then have two painted faces rather than three.", "Treat an unpainted face as painted", "Count only the specified faces")),
        (("List which outside faces are painted, and draw a footprint if the solid is hard to see. Include hidden edges in your count.", "Mark the actual painted faces", "Lay out the boundary by layers."),
         ("Group cells that touch the same number of paint surfaces. Add the groups that match exactly what the question asks for.", "Check the word exactly", "Test a corner and an edge before totalling.")),
        cover=painted_block(4,3,3,False),
    )


def open_net(w,d,h):
    faces=((h,h,w,d),(0,h,h,d),(h+w,h,h,d),(h,0,w,h),(h,h+d,w,h))
    points=[]
    sides=[]
    polys=[]
    labels=[]
    for x,y,a,b in faces:
        start=len(points)
        points.extend(((x,y,""),(x+a,y,""),(x+a,y+b,""),(x,y+b,"")))
        codes=tuple(range(start,start+4))
        polys.append(codes)
        sides.extend((i,j,0) for i,j in zip(codes,codes[1:]+codes[:1]))
        labels.append((x+a/2,y+b/2,f"{a}×{b}",1))
    return geometry(points,sides,polygons=polys,captions=labels)


def nets(lesson):
    v=lesson.visit
    w,d,h=4+v,3+v,2+v
    area=w*d+2*w*h+2*d*h
    fixed_height=3+v
    base_area=(36,48,70)[v]
    volume=base_area*fixed_height
    pairs=[(a,base_area//a) for a in range(1,int(base_area**.5)+1) if base_area%a==0]
    u,z=min(pairs,key=sum)
    best=base_area+2*fixed_height*(u+z)
    assert best==min(base_area+2*fixed_height*(a+b) for a,b in pairs)
    box=cubes(set(product(range(w),range(d),range(h))))
    return Topic(
        (("A net shows the flat faces that can fold around a solid. Surface area adds the faces the object actually has.", "Use faces for surface area."),
         ("Volume counts how much fills the object. For a rectangular box it is the base area times the height.", "Use layers for volume.")),
        (("An AMC practice problem can ask which net folds to a box or how much card it needs. Label matching edge lengths on the net.", "AMC Upper Primary · connect flat faces to the solid"),
         ("A Rossmoyne style problem may fix volume and ask for the least surface area. Use the volume to constrain the possible dimensions first.", "Rossmoyne-style · choose dimensions under a constraint")),
        (
            Example("Find the volume from equal layers", (
                (f"A rectangular block is {say(w)} units long, {say(d)} units wide and {say(h)} units high. Find its volume in cubic units.", f"Block dimensions {w} × {d} × {h}."),
                ("Think of the base footprint repeating in every layer.", "How many cubes fill the block?")),
                ((f"One unit-high layer contains {say(w*d)} cubes because the base is {say(w)} by {say(d)}.", f"Base area = {w} × {d} = {w*d}."),
                 (f"With {say(h)} full layers, the volume is {say(w*d*h)} cubic units.", f"Volume = {w*d} × {h} = {w*d*h}.")),box),
            Example("Calculate the surface area of an open box", (
                (f"An open-top box has base {say(w+1)} by {say(d)} and height {say(h)} units. Ignore thickness and tabs. How much card is needed for the base and its walls?", f"Base {w+1} × {d}; height {h}; no lid."),
                ("Match each wall with the corresponding side of the base.", "Find the total area of five faces.")),
                ((f"Start with base area {say((w+1)*d)}. Two walls have width {say(w+1)} and the other two have width {say(d)}. The height is the same for all walls.", f"Face areas: {(w+1)*d}, {(w+1)*h}, {(w+1)*h}, {d*h}, {d*h}."),
                 (f"Add the base and four walls only. The card area is {say(area+d+2*h)} square units.", f"{(w+1)*d} + 2×{(w+1)*h} + 2×{d*h} = {area+d+2*h}.")),
                open_net(w+1,d,h)),
            Example("Use fixed volume to minimise card", (
                (f"An open-top rectangular box has height {say(fixed_height)} centimetres and capacity {say(volume)} cubic centimetres. Its base sides must be positive integers.", f"Height {fixed_height} cm; volume {volume} cm³. Integer base sides."),
                ("Find the least card area, including the base and the four walls. Ignore tabs and thickness.", "What is the smallest possible surface area?")),
                ((f"Divide the volume by the height. Every legal base has area {say(base_area)}, so the base sides must be a factor pair of {say(base_area)}.", f"Base area = {volume} ÷ {fixed_height} = {base_area}."),
                 (f"With base sides a and b, the wall area is twice the height times the sum of a and b. The base contributes the same amount in every case.", f"Card area = {base_area} + {2*fixed_height}(a+b)."),
                 (f"Compare the sums for the complete list of factor pairs. The smallest sum comes from {say(u)} and {say(z)}.", f"Minimise a+b. Best pair: {u} × {z}.")),
                tiles(f"Volume {volume}",f"Height {fixed_height}"),worked_art=table(("a","b","a+b"),*((a,b,a+b) for a,b in pairs)),proof=(
                    (f"The resulting total card area is {say(best)} square centimetres. This includes only the base and the walls.", f"{base_area} + {2*fixed_height} × ({u}+{z}) = {best}."),
                    ("Each unordered factor pair is listed by its shorter side, which cannot exceed the square root of the base area. Therefore no allowed dimensions are missing.", "Search stops at the square root of the base area.")),
                proof_art=open_net(u,z,fixed_height)),
        ),
        (("A box without a lid has five faces made of card. Do not include a second copy of the base.", "Use the closed box formula for an open box", "Draw and count the faces that exist"),
         ("Volume measures cubic units, while surface area measures square units. Read which of those quantities is fixed and which you need to find.", "Use volume as the surface area", "Write the units alongside both calculations")),
        (("Draw the net and label matching sides. List each face that contributes material, even when no diagram is given.", "Build a face list", "Record the missing faces as well."),
         ("For fixed volume, divide by height and check the possible base factor pairs. Compare the surface area rather than comparing the lengths alone.", "Use the volume constraint", "Check the units of the final area.")),
        cover=open_net(w,d,h),
    )
