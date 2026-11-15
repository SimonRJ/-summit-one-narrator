"""Visual reasoning in grids, geometry and three-dimensional solids."""

from fractions import Fraction
from itertools import product

from story import Example, Topic, bars, cubes, geometry, grid, say, spoken_list, table, tiles


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
    sample_width=3+v
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
                (f"A shape has a row of {say(sample_width)} unit squares and one extra square attached underneath the left end. How many unit squares are in it after a quarter turn?", f"Row of {sample_width}, plus one square underneath."),
                ("Picture the solid piece turning without coming apart.", "What area does it cover after the turn?")),
                ((f"The top row has {say(sample_width)} cells. The extra cell shares an edge but is a different square.", f"{sample_width} + 1 = {sample_width+1} cells"),
                 (f"A quarter turn moves each cell to one new position. It preserves the {say(sample_width+1)} squares and the same area.", f"Area = {sample_width+1} square units")),
                grid(tuple("■" for _ in range(sample_width)),("■",*tuple("" for _ in range(sample_width-1))))),
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


def rectangle(w,h, *, labels=()):
    nodes=((0,0,""),(w,0,""),(w,h,""),(0,h,""))
    return geometry(nodes,((0,1,0),(1,2,0),(2,3,0),(3,0,0)),polygons=((0,1,2,3),),captions=labels)


def optimise(lesson):
    v=lesson.visit
    total=11+2*v
    width=3+v
    other=total-width
    half=total//2
    area=half*(total-half)
    fence=(38,45,54,61)[v]
    by_width={x:x*(fence-2*x) for x in range(1,(fence+1)//2)}
    maximum=max(by_width.values())
    best=[x for x,value in by_width.items() if value==maximum]
    candidate=sorted({n for n in (fence//4-1,fence//4,fence//4+1,fence//4+2) if n in by_width})
    assert {x for x in candidate if by_width[x]==maximum}==set(best)
    return Topic(
        (("An optimisation problem asks for the greatest or least possible result under a rule. First use the rule to express the possibilities in terms of one choice.", "State the constraint before optimising."),
         ("Many rectangle problems reward balance. Show why the nearby legal sizes give the best area.", "Compare the closest allowed products.")),
        (("AMC practice may ask for the largest area or smallest required boundary. Write which quantity stays fixed.", "AMC Upper Primary · find the fixed quantity"),
         ("A Rossmoyne style question may require whole-number dimensions or one side against a wall. Give a reason that every other choice is worse.", "Rossmoyne-style · prove the best legal size")),
        (
            Example("Turn a boundary constraint into a dimension", (
                (f"A rectangle has perimeter {say(2*total)} metres and width {say(width)} metres. What is its area?", f"P = {2*total} m, width = {width} m."),
                ("Use half of the perimeter to find one width plus one length.", "Find the missing side.")),
                ((f"The perimeter has two copies of each side. Half is {say(total)}, so the length is {say(total)} minus {say(width)}, which is {say(other)}.", f"Length = {total} − {width} = {other} m"),
                 (f"Multiply width by length. The area is {say(width*other)} square metres.", f"A = {width} × {other} = {width*other} m²")), rectangle(width,other)),
            Example("Balance two integer sides", (
                (f"A rectangle with whole-number side lengths has perimeter {say(2*total)}. What is the greatest possible area?", f"Two sides add to {total}. Maximise their product."),
                ("Compare side lengths close to each other with ones far apart.", "How close can the two sides be?")),
                (("If the longer side exceeds the shorter by at least two, moving one unit from the longer to the shorter makes their product larger. The sum of the sides stays fixed.", "(a+1)(b−1) − ab = b−a−1"),
                 (f"The closest pair has lengths {say(half)} and {say(total-half)}. The greatest area is {say(area)} square units.", f"{half} × {total-half} = {area}")), table(("Side A","Side B","Product"),
                   (half-2,total-half+2,(half-2)*(total-half+2)),(half-1,total-half+1,(half-1)*(total-half+1)),(half,total-half,area))),
            Example("Optimise the area with only three fenced sides", (
                (f"Build a rectangular pen against a wall using exactly {say(fence)} metres of fencing. Fence only the other three sides, and use whole-number lengths.", f"Fencing for 3 sides only: {fence} m."),
                ("Find the largest area and the dimensions that give it.", "What is the largest legal area?")),
                ((f"If x is a side going out from the wall, there are two such sides. The remaining fenced side measures {say(fence)} minus twice x.", f"Length along wall = {fence} − 2x"),
                 ("Area is half the product of twice x and the remaining length. Those two factors have a fixed sum, so the best factors are as close together as possible.", f"A = ½(2x)({fence}−2x)"),
                 (f"Twice x must be even. Check the even values closest to half of {say(fence)}.", f"Choose 2x closest to {fence}/2.")),
                rectangle(best[0],fence-2*best[0]),proof=(
                    ((f"The best widths are {spoken_list(best)} metres. Both give an area of {say(maximum)} square metres." if len(best)>1 else f"The best width is {say(best[0])} metres, giving an area of {say(maximum)} square metres."), f"Maximum = {maximum} m²"),
                    ("Any other candidate makes the two factors farther apart. The larger gap reduces their product, so no farther candidate can beat this result.", "Compare the two sides of the nearest feasible split.")),
                proof_art=table(("Width","Long side","Area"),*((x,fence-2*x,by_width[x]) for x in candidate))),
        ),
        (("A side against a wall does not use fencing. Count only the two widths and the fenced length before writing the equation.", "Use 2w + 2l for the fence", "The wall removes one fenced side"),
         ("The best real-number answer can break an integer rule. Compare the nearby whole-number possibilities around that balance point.", "Round a side without checking", "Test the allowed dimensions on both sides")),
        (("Write the fixed sum, boundary or budget. Reduce the possible outcomes to one variable.", "State the constraint", "And state which quantity you are optimising."),
         ("Show that moving towards balance increases the product until you reach the closest legal dimensions. Check any ties.", "Justify the optimum", "An example alone gives only a candidate.")),
        cover=rectangle(6,4),
    )


def shaded_area(lesson):
    v=lesson.visit
    w,h=5+v,4+v
    step=2+v%2
    extra=3+v
    simple=w*h+step*extra
    full_w,full_h=10+v,8+v
    a,b=4+v,3+v
    remaining=Fraction(full_w*full_h)-Fraction(a*b,2)
    width,height=9+v,8+v
    cut1=(0,0,6+v,5+v)
    cut2=(3,2,width,height)
    region1={(x,y) for x in range(cut1[2]) for y in range(cut1[3])}
    region2={(x,y) for x in range(3,width) for y in range(2,height)}
    overlap=len(region1&region2)
    white=width*height-len(region1|region2)
    assert white==width*height-len(region1)-len(region2)+overlap
    art=grid(*tuple(tuple("◆" if (x,y) in region1&region2 else "■" if (x,y) in region1|region2 else "□"
                        for x in range(width)) for y in reversed(range(height))))
    return Topic(
        (("An area measures how many square units fill a region. Draw an extra line to split a complicated shape into pieces whose areas you can find.", "Break the shape into known areas."),
         ("If the missing pieces are simpler, start with a whole rectangle and subtract them. Check whether those missing parts overlap.", "Use the whole minus the missing parts.")),
        (("AMC practice may shade the part left after one or more cuts. Compare the shaded region with an easy surrounding shape.", "AMC Upper Primary · use a surrounding area"),
         ("A Rossmoyne style area problem may make regions overlap. Count a shared piece exactly once when subtracting or adding.", "Rossmoyne-style · account for the overlap")),
        (
            Example("Combine two pieces with disjoint interiors", (
                (f"Join a {say(w)} by {say(h)} rectangle to a {say(step)} by {say(extra)} rectangle along an edge without overlap. Find their combined area.", f"Areas of {w} × {h} and {step} × {extra}"),
                ("A shared edge has length but contributes no extra area.", "Add the two separate areas.")),
                ((f"The first area is {say(w*h)} and the second is {say(step*extra)}. No unit square belongs to both interiors.", f"{w}×{h} = {w*h}; {step}×{extra} = {step*extra}"),
                 (f"The areas add to {say(simple)} square units. Joining along an edge leaves this total unchanged.", f"Combined area = {simple}")), tiles(f"{w} × {h}",f"{step} × {extra}")),
            Example("Subtract a triangle from a rectangle", (
                (f"A {say(full_w)} by {say(full_h)} rectangle has a right triangle removed from one corner. The perpendicular legs of the triangle are {say(a)} and {say(b)} units.", f"Whole {full_w} × {full_h}; triangle legs {a} and {b}."),
                ("Find the area left after that corner is removed.", "Subtract the triangle's area.")),
                ((f"The whole rectangle has area {say(full_w*full_h)}. The right triangle is half of a rectangle with sides {say(a)} and {say(b)}.", f"Triangle = ½ × {a} × {b} = {Fraction(a*b,2)}"),
                 (f"Subtract the triangle. That leaves {say(remaining)} square units.", f"{full_w*full_h} − {Fraction(a*b,2)} = {remaining}")), rectangle(full_w,full_h)),
            Example("Subtract two rectangles that overlap", (
                (f"On a {say(width)} by {say(height)} board, shade a lower-left rectangle {say(cut1[2])} columns wide and {say(cut1[3])} rows high.", f"Board {width} × {height}. Shade lower-left {cut1[2]} × {cut1[3]}."),
                (f"Shade the rectangle covering all columns from the fourth onwards and rows from the third upwards, with rows numbered from the bottom. How much area is unshaded?", f"Also shade x from 3 to {width}, y from 2 to {height}.")),
                ((f"The two shaded areas separately are {say(len(region1))} and {say(len(region2))}. Adding them directly would count the shared part twice.", f"Areas: {len(region1)} and {len(region2)}."),
                 (f"The overlap has width {say(cut1[2]-3)} and height {say(cut1[3]-2)}. Its area is {say(overlap)}.", f"Overlap = ({cut1[2]}−3) × ({cut1[3]}−2) = {overlap}"),
                 (f"Subtract the total shaded area from the full board. The overlap correction makes the unshaded area {say(white)} square units.", f"{width*height} − {len(region1)} − {len(region2)} + {overlap} = {white}")),
                art,proof=(
                    (f"Check by counting the unshaded bottom right block and the unshaded top left block. Their areas are {say((width-cut1[2])*2)} and {say(3*(height-cut1[3]))}.", f"Check: {width-cut1[2]} × 2 + 3 × {height-cut1[3]}"),
                    ("Those two unshaded blocks have disjoint interiors. Their sum confirms the calculation using the overlap.", f"Unshaded area = {white}")),proof_art=art),
        ),
        (("Area uses square units. Follow the interior and do not substitute the length around the edge for the covered region.", "Use perimeter as area", "Count square units within the boundary"),
         ("When subtracting both shaded rectangles, one subtraction removes the overlap again. Add that common area back once.", "Subtract the overlap twice", "Add the common area back once")),
        (("Draw the full surrounding shape. Name each piece you add or subtract, and label its needed lengths.", "Name the pieces", "Use known rectangle and triangle areas."),
         ("Check the intersection of any parts you counted separately. Add a second calculation if a different split is easy.", "Check what overlaps", "Every square unit contributes once.")),
        cover=rectangle(7,4),
    )


def layered_cubes(lesson):
    v=lesson.visit
    w,d,h=2+v%3,2+v%2,2+v//3
    simple=w*d*h
    all_cells=set(product(range(w),range(d),range(h)))
    heights=(1+v%2,3+v%2,2+v,2+v//3,4+v%2,1)
    stacks={(x,y,z) for y in range(2) for x in range(3) for z in range(heights[y*3+x])}
    counts=[sum(height>=level for height in heights) for level in range(1,max(heights)+1)]
    short=2+v%2
    peak=short+2+v
    low_heights=((short,peak,1),(1,1,short))
    high_heights=((short,peak,short),(short,short,short))
    lower=sum(map(sum,low_heights))
    upper=sum(map(sum,high_heights))
    def stack_shape(rows):
        return {(x,y,z) for y,row in enumerate(rows) for x,size in enumerate(row) for z in range(size)}
    for heights_map in (low_heights,high_heights):
        assert max(heights_map[0])==peak and max(heights_map[1])==short
        assert tuple(map(max,zip(*heights_map)))==(short,peak,short)
    return Topic(
        (("A solid made of unit cubes can be described by the height of each stack. Add the heights to count cubes, even where a view hides some stacks.", "A view hides cubes; stack heights describe them."),
         ("If you know only the views, several solids may fit. Maxima tell you how tall at least one stack must be in a row or column.", "Views record maximum heights.")),
        (("AMC Upper Primary practice can use unit cubes, layers and silhouettes. Record the counts on a footprint before adding them.", "AMC Upper Primary · count hidden cubes"),
         ("Rossmoyne style spatial problems can give two views and ask for the least or greatest possible block count.", "Rossmoyne-style · combine two views")),
        (
            Example("Use equal layers in a block", (
                (f"A solid block is {say(w)} cubes wide, {say(d)} deep and {say(h)} high. How many unit cubes are inside it altogether?", f"Block: {w} × {d} × {h}."),
                ("Count the cells of one layer before multiplying by the height.", "How many cubes in every level?")),
                ((f"The footprint is {say(w*d)} positions. There are {say(h)} equal layers, each filling this footprint.", f"{w} × {d} = {w*d} cubes per layer"),
                 (f"The full block contains {say(simple)} cubes. Cubes in the back and the centre are included.", f"{w*d} × {h} = {simple}")), cubes(all_cells,spread=30)),
            Example("Count a stack map by levels", (
                (f"The heights of six stacks in two rows of three are {spoken_list(heights[:3])} in the first row, and {spoken_list(heights[3:])} in the second.", f"Stack heights: {' '.join(map(str,heights[:3]))} and {' '.join(map(str,heights[3:]))}"),
                ("Every stack rests on the floor. Count the cubes in all the stacks.", "How many unit cubes do the stacks contain?")),
                ((f"For every level, count one cube above each footprint cell whose stack reaches it. The level counts are {spoken_list(counts)} from the floor up.", f"Level counts {', '.join(map(str,counts))}"),
                 (f"Add those counts, giving {say(len(stacks))}. Adding the six heights directly confirms the same total.", f"Total: {' + '.join(map(str,counts))} = {len(stacks)}")),
                cubes(stacks),worked_art=grid(heights[:3],heights[3:])),
            Example("Find the smallest and largest solids matching two views", (
                (f"Six nonempty stacks form two rows of three. Looking along the rows, the maximum heights in the three columns are {say(short)}, {say(peak)} and {say(short)}.", f"Column maxima: {short}, {peak}, {short}."),
                (f"The row maxima in order are {say(peak)} and {say(short)}. Find the least and greatest possible number of cubes. There are no gaps in any stack.", f"Row maxima: {peak}, {short}. Find the minimum and maximum.")),
                (("Every column needs one stack that attains its own maximum. Put those three tall stacks in separate columns. Each of the remaining three stacks must contain at least one cube.", f"Minimum lower bound: {short} + {peak} + {short} + 3"),
                 (f"Put the tall middle stack in the first row and one of the outer tall stacks in the second row. The row maxima are then satisfied without adding extra cubes.", f"Minimum {lower} cubes.")),
                table(("View","Maxima"),("Columns",f"{short}, {peak}, {short}"),("Rows",f"{peak}, {short}")),worked_art=cubes(stack_shape(low_heights)),proof=(
                    ("For the maximum, every stack is capped by both its row and column. Use the smaller of those two limits at every location.", "Tallest at each cell = min(row cap, column cap)."),
                    (f"That gives {say(short)}, {say(peak)}, {say(short)} in the first row and {say(short)} in every position of the second. Both views still fit, so the maximum is {say(upper)} cubes.", f"Maximum {upper} cubes.")),
                proof_art=cubes(stack_shape(high_heights))),
        ),
        (("The maximum seen in a view describes the tallest stack in a line of sight. It does not give that height to all stacks behind it.", "Treat a silhouette as every stack", "Use a maximum, not an exact height"),
         ("A maximum model must respect both views. A height allowed by one view may exceed the limit in the other.", "Apply only one view", "At each cell use the smaller cap")),
        (("Draw the footprint and mark row and column heights. Decide whether you know each stack, or only the maximum over a row or column.", "Label what each view means", "Use a table of stack heights."),
         ("For a bound, produce a model that reaches it. Verify all row maxima, all column maxima and the number of cubes.", "Check both views of your model", "Show the construction meets the bound.")),
        cover=cubes(all_cells,spread=25),
    )
