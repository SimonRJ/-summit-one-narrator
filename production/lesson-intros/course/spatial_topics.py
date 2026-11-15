"""Visual reasoning in grids, geometry and three-dimensional solids."""

from itertools import product

from story import Example, Topic, bars, cubes, geometry, grid, say, table, tiles


def pairs(n):
    return n*(n-1)//2


def lattice(width, height, marks=()):
    nodes=[]
    edges=[]
    faces=[]
    labels=[]
    def point(x,y):
        idx=len(nodes)
        nodes.append((x,y,""))
        return idx
    for x in range(width+1):
        edges.append((point(x,0),point(x,height),0))
    for y in range(height+1):
        edges.append((point(0,y),point(width,y),0))
    for i,(x,y,label) in enumerate(marks):
        face=(point(x,y),point(x+1,y),point(x+1,y+1),point(x,y+1))
        faces.append(face)
        edges.extend((a,b,i+1) for a,b in zip(face,(*face[1:],face[0])))
        labels.append((x+.5,y+.5,label,i+1))
    return geometry(nodes,edges,polygons=faces,captions=labels)


def crossings(lesson):
    v=lesson.visit
    w,h=3+v%4, 2+v//2
    answer=(w+1)*(h+1)
    m,n=4+v%3,3+v%4
    rectangles=pairs(m+1)*pairs(n+1)
    wide,tall=6+v%3, 5+v//3
    ax,ay=1+v%2,2
    bx,by=4+v%2,(2 if v==0 else v%4)
    one=(ax+1)*(wide-ax)*(ay+1)*(tall-ay)
    both=(min(ax,bx)+1)*(wide-max(ax,bx))*(min(ay,by)+1)*(tall-max(ay,by))
    final=one-both
    def covers(cell,left,right,down,up):
        x,y=cell
        return left<=x<right and down<=y<up
    assert final==sum(covers((ax,ay),l,r,d,u) and not covers((bx,by),l,r,d,u)
             for l,r,d,u in product(range(wide),range(1,wide+1),range(tall),range(1,tall+1)) if l<r and d<u)
    return Topic(
        (
            ("A grid is made from lines, spaces between the lines, and points where the lines meet. These are three different things to count.", "Name the object: cell, line or crossing."),
            ("For a rectangle on a grid, choose the two lines that form each pair of opposite edges.", "Two vertical lines and two horizontal lines."),
        ),
        (
            ("An AMC Upper Primary question can ask for intersections, paths, or shapes cut out by grid lines. Mark the object being counted.", "AMC Upper Primary · count the right objects"),
            ("A Rossmoyne style grid problem can require a shape to include one marked cell while avoiding another. Count by the possible boundaries.", "Rossmoyne-style · constrain the edges"),
        ),
        (
            Example("Count all the intersections", (
                (f"The grid has {say(w)} columns and {say(h)} rows of squares. How many points where vertical and horizontal lines meet are there?", f"{w} columns × {h} rows of cells"),
                ("Count the lines along the outside edges too.", "Include crossings on the boundary."),
            ), (
                (f"{say(w)} columns need {say(w+1)} vertical lines. {say(h)} rows need {say(h+1)} horizontal lines.", f"{w+1} vertical lines, {h+1} horizontal lines"),
                (f"Each vertical line crosses all {say(h+1)} horizontal lines. Multiply to get {say(answer)} crossing points.", f"{w+1} × {h+1} = {answer}"),
            ), lattice(w,h)),
            Example("Choose four lines to make a rectangle", (
                (f"A sheet has {say(m)} columns and {say(n)} rows of cells. Count all rectangles whose sides lie along its grid lines.", f"{m} by {n} cells. Count all grid-line rectangles."),
                ("Rectangles can have any size. A square counts too.", "Choose opposite sides in pairs."),
            ), (
                (f"Choose two of the {say(m+1)} vertical lines. An unordered pair makes the left and right edge. There are {say(pairs(m+1))} choices.", f"Vertical pairs: {m+1} × {m} ÷ 2 = {pairs(m+1)}"),
                (f"There are {say(pairs(n+1))} horizontal pairs. Choose one vertical pair and one horizontal pair independently.", f"Horizontal pairs: {n+1} × {n} ÷ 2 = {pairs(n+1)}"),
                (f"The four selected lines specify a unique rectangle. Multiply the counts to get {say(rectangles)}.", f"{pairs(m+1)} × {pairs(n+1)} = {rectangles}"),
            ), lattice(m,n,((1,1,""),))),
            Example("Include one cell and avoid another", (
                (f"On a {say(wide)} column by {say(tall)} row grid, cell A is in column {say(ax+1)}, row {say(ay+1)}. Rows are numbered from the bottom.", f"A is in column {ax+1}, row {ay+1}."),
                (f"Cell B is in column {say(bx+1)}, row {say(by+1)}. Count the grid-line rectangles containing all of A but none of the interior of B.", f"B is in column {bx+1}, row {by+1}."),
                ("One way to begin is to count every rectangle containing A. Then identify the unwanted ones.", "Count rectangles containing A and avoiding B."),
            ), (
                (f"To contain A, the left and right edges have {say(ax+1)} and {say(wide-ax)} choices respectively. The lower and upper edges have {say(ay+1)} and {say(tall-ay)} choices.", f"All four edges around A: {ax+1} × {wide-ax} × {ay+1} × {tall-ay}"),
                (f"That is {say(one)} rectangles. Each rectangle is counted once by the locations of its four sides.", f"{one} rectangles include A."),
                ("Now require it to contain both cells. Each side must sit outside the smallest block that contains A and B.", "Put four sides around both marked cells."),
            ), lattice(wide,tall,((ax,ay,"A"),(bx,by,"B"))),proof=(
                (f"The edge counts for a rectangle enclosing both are {say(min(ax,bx)+1)}, {say(wide-max(ax,bx))}, {say(min(ay,by)+1)} and {say(tall-max(ay,by))}. Their product is {say(both)}.", f"{min(ax,bx)+1} × {wide-max(ax,bx)} × {min(ay,by)+1} × {tall-max(ay,by)} = {both}"),
                (f"Subtract those from the count containing A. Exactly {say(final)} rectangles contain A and avoid B.", f"{one} − {both} = {final}"),
            ),proof_art=lattice(wide,tall,((ax,ay,"A"),(bx,by,"B")))),
        ),
        (
            ("The outside boundary contributes two edge lines in each direction. A row of five cells sits between six lines.", "5 cells use 5 grid lines", "5 cells sit between 6 lines"),
            ("For a rectangle, the pair of left and right lines has no order to choose twice. Choosing the lines fixes their order automatically.", "Count a line pair twice", "Use unordered pairs of lines"),
        ),
        (
            ("Mark whether you are choosing lines, crossing points or cells. Count the outer boundaries before using a formula.", "Label the grid objects", "A row of cells has one more boundary line."),
            ("Set constraints on one edge choice at a time. For a cell to be excluded, subtract exactly the choices that include it.", "Count by the boundaries", "The four sides specify each rectangle once."),
        ), cover=lattice(4,3,((1,1,"A"),)),
    )


def tiling(lesson):
    v=lesson.visit
    width=4+v
    height=3
    area=width*height
    gap=(1+v%2)
    left=area-gap
    removed={(0,0)} | ({(width-1,2)} if gap==2 else set())
    singles=2+v%2
    doubles=3+v//2
    cols=singles+2*doubles
    from math import comb
    answer=comb(singles+doubles,singles)
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def independent(n,s):
        if n<0 or s<0:
            return 0
        if n==0:
            return int(s==0)
        return independent(n-1,s-1)+independent(n-2,s)

    assert independent(cols,singles)==answer and left%3!=0
    return Topic(
        (("A polyomino joins unit squares edge to edge. A tiling covers a board exactly, with every piece inside and no squares covered twice.", "Tiles join squares edge to edge."),
         ("Check area for a quick obstruction. Then use the board's shape to find what placements are possible.", "Area first, then placements.")),
        (("In AMC practice, a shape puzzle may ask if pieces fit or how many arrangements form a rectangle. Draw the occupied cells.", "AMC Upper Primary · track occupied cells"),
         ("A Rossmoyne style tiling count may restrict the number of vertical or horizontal pieces. Replace forced runs by blocks.", "Rossmoyne-style · count forced blocks")),
        (
            Example("Count squares after a turn", (
                (f"A shape has a row of {say(3+v%3)} unit squares and one extra square attached underneath the left end. How many unit squares are in it after a quarter turn?", f"Row of {3+v%3}, plus one square underneath."),
                ("Picture the solid piece turning without coming apart.", "What area does it cover after the turn?")),
                ((f"The top row has {say(3+v%3)} cells. The extra cell shares an edge but is a different square.", f"{3+v%3} + 1 = {4+v%3} cells"),
                 (f"A quarter turn moves each cell to one new position. It preserves the {say(4+v%3)} squares and the same area.", f"Area = {4+v%3} square units")),
                grid(tuple("■" for _ in range(3+v%3)),("■",*tuple("" for _ in range(2+v%3))))),
            Example("Use area to rule out a tiling", (
                (f"A {say(width)} by three board has {say(gap)} corner {'cell' if gap==1 else 'cells'} removed. Can you tile what remains using pieces of exactly three unit squares?", f"{width} × 3 board, remove {gap} corner {'cell' if gap==1 else 'cells'}."),
                ("Pieces may be turned. They may not overlap, and each cell must be covered.", "Can three-square tiles cover it exactly?")),
                ((f"The original board has {say(area)} cells, and removing the corners leaves {say(left)}.", f"{width} × 3 − {gap} = {left}"),
                 (f"Every piece covers exactly three squares. An exact cover would require {say(left)} to be divisible by three.", f"{left} leaves remainder {left%3} on division by 3."),
                 ("There would be leftover cells even before any shape restrictions were checked. The tiling is impossible.", "The area test rules it out.")),
                grid(*(tuple("×" if (j,i) in removed else "□"
                             for j in range(width)) for i in range(3)))),
            Example("Count tilings with a fixed number of vertical pieces", (
                (f"Tile a two-row board of width {say(cols)} using dominoes. Exactly {say(singles)} dominoes must stand vertically and cover both rows of their column.", f"2 × {cols} strip. Exactly {singles} vertical dominoes."),
                ("How many tilings work? A horizontal domino in the leftmost uncovered column creates a forced placement beside it.", "Count the legal strip tilings.")),
                (("Look at the leftmost column still uncovered. A vertical domino fills one column. If you put a horizontal domino there, the other cell of the column must start another horizontal domino.", "One vertical fills 1 column. A horizontal pair fills 2."),
                 (f"The {say(singles)} vertical dominoes use {say(singles)} columns. After that, {say(2*doubles)} columns are covered by {say(doubles)} pairs of horizontal dominoes.", f"{singles} single-column blocks + {doubles} double-column blocks"),
                 (f"Choose the {say(singles)} positions occupied by the vertical blocks among the {say(singles+doubles)} blocks. The other positions are occupied by horizontal pairs.", f"Choose {singles} of {singles+doubles} block positions.")),
                lattice(cols,2),worked_art=tiles(*("V",)*singles,*("HH",)*doubles),proof=(
                    (f"The number of choices is {say(answer)}. Each sequence of these two block types gives a legal tiling when expanded from the left.", f"C({singles+doubles}, {singles}) = {answer}"),
                    ("A finished tiling determines its block sequence from the leftmost uncovered column on each step. That gives only one count per tiling.", "The correspondence works both ways.")),
                proof_art=bars(("Blocks",tuple([(1,"V")]*singles+[(2,"HH")]*doubles)))),
        ),
        (("Area that is a multiple of the tile size is only a starting check. The shapes must also fit inside the remaining board.", "Use divisible area as proof of a tiling", "Give placements or a construction"),
         ("Two horizontal dominoes in a two-row strip can be forced into a paired block. Counting their orders as if they were distinct adds duplicates.", "Count extra orders inside a forced pair", "Treat the horizontal double-column as one block")),
        (("Check the area, then look at a boundary cell where you have few choices. Ask which extra moves each placement forces.", "Start at a constrained cell", "Use area and shape together."),
         ("When counting block sequences, convert a sequence back into an actual tiling. Explain why the original tiling has just one block sequence.", "Use a one-to-one count", "Every legal arrangement appears once.")),
        cover=lattice(4,2,((0,0,""),(1,0,""))),
    )


def outer_boundary(cells):
    return sum((x+dx,y+dy) not in cells for x,y in cells for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)))


def perimeter(lesson):
    v=lesson.visit
    w,h=2+v,3
    unit=1+v
    basic=2*(w+h)*unit
    row=4+v
    cells={(x,0) for x in range(row)}|{(0,y) for y in (1,2)}
    internal=sum((x+1,y) in cells for x,y in cells)+sum((x,y+1) in cells for x,y in cells)
    middle=4*len(cells)-2*internal
    n=6+v
    hole_width,hole_height=2+v%3,1+v%2
    remain=set(product(range(n),repeat=2)) - {(x,y) for x in range(1,1+hole_width) for y in range(1,1+hole_height)} - {(n-1,n-1)}
    answer=4*n+2*(hole_width+hole_height)
    assert middle==outer_boundary(cells) and answer==outer_boundary(remain)
    return Topic(
        (("Perimeter is the total length of the boundary. When two pieces share an edge, that edge no longer lies on the outside.", "A shared edge is inside, so subtract both copies."),
         ("A cut can create a new boundary. Follow the edge of any hole if the question says to include it.", "Trace every boundary the question names.")),
        (("In AMC practice, a stepped outline or connected unit squares can hide which edges should be counted. Mark shared edges.", "AMC Upper Primary · trace exposed edges"),
         ("A Rossmoyne style question may make several cuts. Compute how each cut changes the boundary length.", "Rossmoyne-style · reason about changes")),
        (
            Example("Trace all four sides", (
                (f"A rectangle is {say(w*unit)} metres wide and {say(h*unit)} metres tall. What is its perimeter?", f"{w*unit} m by {h*unit} m"),
                ("Trace around the outside to see how many of each side length there are.", "Count each side exactly once.")),
                ((f"There are two sides of length {say(w*unit)} and two of length {say(h*unit)}. Add all four.", f"2 × {w*unit} + 2 × {h*unit}"),
                 (f"The perimeter is {say(basic)} metres. Length uses metres, even though the shape also has an area.", f"Perimeter = {basic} m")), lattice(w,h)),
            Example("Subtract shared edges from a count of unit squares", (
                (f"Draw {say(row)} unit squares in a horizontal row. Add two more unit squares stacked directly above its leftmost square.", f"{row} squares in a row, plus 2 above the left end."),
                ("What is the perimeter of this shape? Count the contacts between pairs of squares.", "How much edge is exposed?")),
                ((f"Taken separately, the {say(len(cells))} squares contribute four edge units each.", f"Separate edges: 4 × {len(cells)} = {4*len(cells)}"),
                 (f"There are {say(internal)} shared edges. Each is counted twice in the separate square totals, once by each square touching it.", f"Subtract 2 × {internal} = {2*internal}."),
                 (f"The exposed boundary length is {say(middle)} units. Check by walking around the outside of the L shape.", f"Perimeter = {4*len(cells)} − {2*internal} = {middle}")),
                grid(*tuple(tuple("■" if (x,2-y) in cells else "" for x in range(row)) for y in range(3)))),
            Example("Combine an inside cut with a corner cut", (
                (f"A {say(n)} by {say(n)} square board has a fully enclosed {say(hole_width)} by {say(hole_height)} rectangular hole cut out. Then remove one square at an outer corner far from the hole.", f"{n} × {n} board. Interior {hole_width} × {hole_height} hole. Cut a corner cell."),
                ("Find the total boundary length, including the edge of the hole.", "Count the outer boundary and the hole.")),
                ((f"The original outer boundary is {say(4*n)}. Removing one corner loses two outer edges of length one but exposes two equal inner edges.", f"Corner change = −2 + 2 = 0."),
                 (f"The hole adds its full perimeter, twice {say(hole_width)} plus twice {say(hole_height)}. Every side of the hole meets the remaining board.", f"Hole boundary: 2({hole_width} + {hole_height}) = {2*(hole_width+hole_height)}"),
                 (f"Add that to {say(4*n)}. The new total boundary length is {say(answer)} units.", f"{4*n} + {2*(hole_width+hole_height)} = {answer}")),
                grid(*tuple(tuple("■" if (x,n-1-y) in remain else "×" for x in range(n)) for y in range(n))),proof=(
                    ("A boundary is an edge with a filled cell on one side and an unfilled part on the other. This includes the through-hole boundary.", "Count filled-to-empty edges."),
                    ("The outer walk and the inner walk are disjoint. Adding their lengths keeps every requested edge once.", "Outer boundary + inner boundary."))),
        ),
        (("A shared edge disappears from the exterior twice when you start by adding all individual perimeters.", "Subtract one edge per contact", "Subtract two copies of a shared edge"),
         ("Cutting around a hole creates a boundary inside the shape. Include it if the problem asks for the total boundary.", "Trace only the outside loop", "Include each boundary named in the question")),
        (("Mark shared and exposed edges with different colours. The units for perimeter are units of length.", "Trace the boundary", "Count length, not area."),
         ("For a change of shape, list which old edges disappear and which new ones appear before re-counting everything.", "Track the change", "Check the result by walking the outline.")),
        cover=lattice(4,3,((0,0,""),(1,0,""))),
    )
