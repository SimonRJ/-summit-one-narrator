"""Visual reasoning in grids, geometry and three-dimensional solids."""

from itertools import product

from story import Example, Topic, cubes, geometry, grid, say, table, tiles


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
