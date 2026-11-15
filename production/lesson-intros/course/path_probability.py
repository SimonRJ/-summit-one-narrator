"""Route restrictions, dynamic totals and equally likely outcomes."""

from fractions import Fraction
from itertools import combinations, permutations, product
from math import comb, factorial

from story import Example, Topic, chain, geometry, grid, say, spoken_list, table, tiles


def totals(w,h,closed=()):
    counts={}
    for y in range(h+1):
        for x in range(w+1):
            cell=(x,y)
            if cell in closed:
                counts[cell]=0
            elif cell==(0,0):
                counts[cell]=1
            else:
                counts[cell]=counts.get((x-1,y),0)+counts.get((x,y-1),0)
    return counts


def route_map(w,h,counts=None,closed=()):
    points=[(x,y,"S" if (x,y)==(0,0) else "F" if (x,y)==(w,h) else "×" if (x,y) in closed else "")
            for y in range(h+1) for x in range(w+1)]
    if counts is not None:
        rows=tuple(tuple("×" if (x,y) in closed else counts[x,y] for x in range(w+1))
                   for y in reversed(range(h+1)))
        return {**grid(*rows,highlight=((0,w),(h,0))),"bottom_up":True}
    edges=[]
    for y in range(h+1):
        for x in range(w+1):
            index=y*(w+1)+x
            if x<w: edges.append((index,index+1,0))
            if y<h: edges.append((index,index+w+1,0))
    return geometry(points,edges)


def dynamic_paths(lesson):
    v=lesson.visit
    a=2+v
    mw,mh=3+v,2+v
    mid=totals(mw,mh)
    width,height=5+v,4+v
    b1=(2,2)
    b2=(3+v,3)
    blocked=(b1,b2)
    hard=totals(width,height,blocked)
    choose_paths=lambda dx,dy: comb(dx+dy,dx)
    all_ways=choose_paths(width,height)
    through_first=choose_paths(*b1)*choose_paths(width-b1[0],height-b1[1])
    through_second=choose_paths(*b2)*choose_paths(width-b2[0],height-b2[1])
    through_both=choose_paths(*b1)*choose_paths(b2[0]-b1[0],b2[1]-b1[1])*choose_paths(width-b2[0],height-b2[1])
    assert hard[width,height]==all_ways-through_first-through_second+through_both
    assert mid[mw,mh]==comb(mw+mh,mw)
    return Topic(
        (("On a grid with steps only right or up, each route to a point has a last step. It came from the left or from below.", "Count routes by their last step."),
         ("Add the route totals from those two starting points for the last step. Filling the grid in a useful order saves repeated work.", "New total = left total + lower total.")),
        (("AMC practice may ask how many shortest routes reach a point. Check whether shortest forces the allowed directions before counting.", "AMC Upper Primary · use the forced directions"),
         ("A Rossmoyne style extension might block intersections. Put zero at a closed position, then keep adding the available incoming totals.", "Rossmoyne-style · work around closed intersections")),
        (
            Example("Count routes with exactly one up step", (
                (f"Go from grid intersection zero, zero to {say(a)}, one. Each move is one step right or one step up. How many routes are there?", f"From (0,0) to ({a},1). Right and up only."),
                ("Think of your walk as a sequence of steps.", "Place the single up step.")),
                ((f"Each route uses {say(a)} right steps and one up step. The up step can go in any of the {say(a+1)} step positions.", f"{a} right steps + 1 up."),
                 (f"Choosing where the up step goes fixes the whole route. There are {say(a+1)} routes.", f"{a+1} possible positions, so {a+1} routes.")),route_map(a,1)),
            Example("Fill the grid using its incoming totals", (
                (f"Walk right or up along a grid from zero, zero to {say(mw)}, {say(mh)}. Use a one-step move each time. How many routes reach the end?", f"From (0,0) to ({mw},{mh}), right/up only."),
                ("Set the starting total to one, for the route that has made no moves yet.", "Enter 1 at the start.")),
                ((f"The bottom and left edges each have one route to every point on them. For an inside point, add its left and lower neighbours.", "Interior total = left + below."),
                 (f"At the finish the last step can come from a point with {say(mid[mw-1,mh])} routes or one with {say(mid[mw,mh-1])} routes. Add these.", f"{mid[mw-1,mh]} + {mid[mw,mh-1]} = {mid[mw,mh]} routes.")),
                route_map(mw,mh),worked_art=route_map(mw,mh,mid)),
            Example("Count routes around two closed intersections", (
                (f"Walk from zero, zero to {say(width)}, {say(height)}, moving right or up one step at a time. The intersections two, two and {say(b2[0])}, three are closed.", f"Finish ({width},{height}); closed (2,2) and ({b2[0]},3)."),
                ("No route may enter either closed intersection. How many routes are possible?", "Find the routes that stay open.")),
                ((f"Put a zero at each closed intersection. The paths that would enter it stop there, so they cannot contribute to a later point.", f"W(2,2) = W({b2[0]},3) = 0."),
                 (f"Fill the grid starting at the bottom left. At every other point add the number from the left and the number from below.", "Keep the same addition rule at every open point."),
                 (f"The finish has {say(hard[width-1,height])} routes entering from the left and {say(hard[width,height-1])} from below. The total is {say(hard[width,height])}.", f"{hard[width-1,height]} + {hard[width,height-1]} = {hard[width,height]} routes.")),
                route_map(width,height,closed=blocked),worked_art=route_map(width,height,hard,blocked),proof=(
                    ("Every legal route reaches the finish by exactly one last step. These counts overlap nowhere, so it is safe to add them.", "Each last step belongs to one disjoint case."),
                    ("The same argument holds for each open point in the grid. Starting with only the legal choices makes the whole table complete.", "One legal start, zero at closures, then left plus below.")),
                proof_art=route_map(width,height,hard,blocked)),
        ),
        (("The start total is one: there is one way to be at the start without moving. Using zero there would make every count zero.", "Write zero at the start", "Use one empty route at the starting point"),
         ("A grid intersection is a point. Blocking it forbids entering that point, even when surrounding unit squares are drawn.", "Treat a blocked point as a missing square", "Put zero at the actual closed intersection")),
        (("Circle the start, finish and blocked points. Confirm the legal step directions and fill in the edge totals.", "Set the grid boundaries", "Mark which values are fixed at zero."),
         ("Fill the remaining totals in an order where the incoming neighbours are already known. Check the last step at the finish before adding.", "Use each possible last step", "Record the route total at the finish.")),
        cover=route_map(4,3),
    )


def restricted_routes(lesson):
    v=lesson.visit
    height=3+v
    width=4
    basic=grid(("Across a side","Diagonal"),("Start","Across a side"),highlight=((1,0),))
    n=3+v
    rows=[("R1","B?","R?","B?","…",f"B{n}"),("Start","", "", "", "", "Finish")]
    unconstrained=factorial(n-1)**2
    adjacency=(2*n-3)*factorial(n-2)**2
    result=unconstrained-adjacency
    rs_list=list(permutations(range(2,n+1)))
    bs_list=list(permutations(range(1,n)))
    assert result==sum(next(j for j,b in enumerate(s) if b==1) not in (i,i+1)
                       for r in rs_list for s in bs_list for i in (r.index(2),))
    return Topic(
        (("A route follows legal connections. Two places can look close on a picture without having an edge between them. Read exactly what makes them neighbours.", "Only legal edges create neighbours."),
         ("When paths must avoid a particular connection, look for an easy total and subtract the routes that use that connection.", "Count the unrestricted routes and test the restriction.")),
        (("In AMC grid practice, sharing a side and sharing a corner are different. Mark the legal exits before counting routes.", "AMC Upper Primary · distinguish edges from corners"),
         ("In a Rossmoyne style route problem, the order of visits can matter even when the same stops appear. Label both the places and the route positions.", "Rossmoyne-style · separate stops from positions")),
        (
            Example("Count legal neighbours at a corner", (
                (f"A {say(width)} by {say(height)} board has a marked corner cell. Two cells are neighbours only if they share a full side. How many neighbours does it have?", f"{width} × {height} cells. Start in a corner."),
                ("Test the cells directly across each of the four sides.", "Does an adjoining corner count?")),
                (("Two sides of a corner cell touch the boundary. Across each of its other two sides there is a cell on the board.", "Two sides lead to other cells."),
                 ("A diagonal cell touches only at a point. The marked corner has exactly two neighbours.", "2 neighbours across full sides.")),basic),
            Example("Use the shared neighbours of two stops", (
                (f"On a grid, start at intersection one, {say(height)} and stop at two, {say(height+1)}. Every move is one horizontal or vertical step.", f"From (1,{height}) to (2,{height+1}). No diagonal moves."),
                ("List the possible intermediate points on a two-step route.", "Find the common legal neighbours.")),
                ((f"Moving right then up passes through two, {say(height)}. Moving up then right passes through one, {say(height+1)}.", f"Right–up: (2,{height}); up–right: (1,{height+1})."),
                 ("Any other first move leaves you more than one step from the finish. There are only two legal routes in exactly two steps.", "2 possible two-step routes.")),
                geometry(((0,0,"S"),(1,0,""),(0,1,""),(1,1,"F")),((0,1,0),(1,3,0),(0,2,1),(2,3,1)))),
            Example("Count alternating routes with one closed connection", (
                (f"There are {say(n)} red stops and {say(n)} blue stops, each labelled. Every red can be followed by every blue and vice versa, except between red two and blue one.", f"{n} red and {n} blue stops. No edge R2–B1."),
                (f"Start at red one, finish at blue {say(n)}, and visit every stop exactly once. How many routes are legal?", f"R1 first; B{n} last; visit every stop once.")),
                ((f"Colours alternate. The free red stops can fill their {say(n-1)} positions in {say(factorial(n-1))} orders. The free blue stops have the same count.", f"Unrestricted: ({n-1}!)² = {unconstrained}."),
                 (f"Count the forbidden routes in both directions. When red two is followed by blue one, there are {say(n-2)} positions for the pair because the endpoints are already reserved.", f"R2 then B1: {n-2} locations."),
                 (f"In the reverse order there are {say(n-1)} positions. When either pair is placed, the other {say(n-2)} free stops of each colour can be ordered independently.", f"B1 then R2: {n-1} locations. Per pair: ({n-2}!)².")),
                table(*rows),proof=(
                    (f"A route contains only one red two and one blue one. Its forbidden pair has a unique orientation and position, so there are {say(adjacency)} forbidden routes.", f"({n-2} + {n-1}) × ({n-2}!)² = {adjacency}."),
                    (f"Subtract those from all alternating routes. The number of legal routes is {say(result)}.", f"{unconstrained} − {adjacency} = {result}.")),
                proof_art=table(("Orientation","Locations"),("R2–B1",n-2),("B1–R2",n-1))),
        ),
        (("Sharing a corner does not count as sharing a full side. Apply the exact adjacency definition each time you list neighbours.", "Count touching corners as side neighbours", "Follow the given definition of a legal move"),
         ("A closed two-way connection is forbidden in either direction. Check both ways it could appear in the route.", "Subtract only one orientation", "Count both directions of the closed edge")),
        (("Sketch the legal edges and mark the endpoint rules. Decide whether the question counts endpoints, intermediate stops or whole routes.", "Draw the possible connections", "Write which moves are forbidden."),
         ("Look for a forced pattern such as alternating colours. Count those routes before removing any restricted cases, and check you removed each once.", "Count the legal orders", "Apply the restrictions to specific positions.")),
        cover=chain("R","B","R","B"),
    )


def probability(lesson):
    v=lesson.visit
    sectors=5+v
    green=2+v%2
    simple=Fraction(green,sectors)
    size=4+v
    target=5+v
    wins={(a,b) for a,b in product(range(1,size+1),repeat=2) if a+b==target}
    medium=Fraction(len(wins),size**2)
    red,blue=4+v,3+v%3
    n=red+blue
    good=comb(red,2)*blue
    all_groups=comb(n,3)
    answer=Fraction(good,all_groups)
    ordered=Fraction(red,n)*Fraction(red-1,n-1)*Fraction(blue,n-2)
    assert answer==3*ordered and good==sum(sum(x<red for x in s)==2 for s in combinations(range(n),3))
    outcomes=table(("A / B",*range(1,size+1)),*((a,*(a+b for b in range(1,size+1))) for a in range(1,size+1)),
                   highlight=tuple(wins))
    return Topic(
        (("Probability compares favourable outcomes with all possible outcomes when each outcome being counted is equally likely. First choose outcomes you can count fairly.", "Favourable outcomes ÷ equally likely outcomes."),
         ("With more than one draw, check whether drawing one object changes the choices on the next draw.", "Without replacement changes the next draw.")),
        (("AMC Upper Primary practice may use spinners, dice or draws from a bag. List ordered pairs if the individual choices are independent.", "AMC Upper Primary · make a fair sample space"),
         ("A MAWA style solution may ask you to justify the counting method. Explain why each choice in your denominator is equally likely.", "MAWA-style · justify the sample space")),
        (
            Example("Find a probability from equal spinner sections", (
                (f"A fair spinner has {say(sectors)} equal sectors, {say(green)} of them green. What is the probability it stops on green?", f"{sectors} equal sectors; {green} green."),
                ("Use each sector as one equally likely outcome.", "Count sectors, not colour names.")),
                ((f"There are {say(sectors)} possible sectors, and {say(green)} satisfy the condition. The probability is the green count over the whole count.", f"{green} / {sectors}."),
                 (f"As a fraction in simplest form that is {say(simple)}.", f"P(green) = {simple}.")),{"kind":"spinner","sectors":sectors,"green":green}),
            Example("Count ordered pairs with a given sum", (
                (f"Two fair independent spinners each have equal sectors numbered one to {say(size)}. What is the probability their numbers sum to {say(target)}?", f"Each spinner 1–{size}. Target sum {target}."),
                ("Make a row for every number on the first spinner, and a column for every number on the second.", "Count equal pairs, not possible sums.")),
                ((f"There are {say(size**2)} equally likely ordered pairs. In each row use a second reading of {say(target)} minus the first reading, if it is present.", f"{size} × {size} = {size**2} ordered pairs."),
                 (f"There are {say(len(wins))} favourable pairs. Dividing by the total gives {say(medium)}.", f"P(sum {target}) = {len(wins)}/{size**2} = {medium}.")),outcomes),
            Example("Draw exactly two red counters without replacement", (
                (f"A bag contains {say(red)} red counters and {say(blue)} blue counters. Draw three counters at random without replacing any of them.", f"{red} red, {blue} blue. Draw 3 without replacement."),
                ("What is the probability of getting exactly two red counters? Any order of colours is allowed.", "Find the chance of exactly 2 reds.")),
                ((f"Think of the counters as distinct. Each set of three is equally likely because each can be drawn in the same six orders.", "Every 3-counter set has 6 draw orders."),
                 (f"There are {say(all_groups)} sets altogether. A favourable set chooses two of the {say(red)} reds and one of the {say(blue)} blues.", f"Favourable = {comb(red,2)} red pairs × {blue} blues."),
                 (f"There are {say(good)} favourable sets. The probability is {say(answer)}.", f"{good} / {all_groups} = {answer}.")),
                tiles(f"{red} red",f"{blue} blue","Draw 3",colours=("#f39299","#7eb5f3","#eeb765")),proof=(
                    (f"Check with ordered draws. Red, red, blue has probability {say(red)} over {say(n)}, times {say(red-1)} over {say(n-1)}, times {say(blue)} over {say(n-2)}.", f"RRB: {red}/{n} × {red-1}/{n-1} × {blue}/{n-2}."),
                    ("Red, blue, red and blue, red, red have the same three factors in the numerators, just in another order. The three outcomes are distinct.", f"RRB, RBR and BRR: 3 × {ordered} = {answer}.")),
                proof_art=tiles("R R B","R B R","B R R")),
        ),
        (("A sum of two spinners is usually not equally likely with every other sum. Count the independent pairs that produce it.", "Use the number of different sums as the denominator", "Count equally likely ordered pairs instead"),
         ("Without replacement, the bag becomes smaller after each draw. Update the denominator and the count of eligible colours.", "Reuse the original bag counts for each draw", "Update both counts after each draw")),
        (("Write the event exactly, especially whether it says at least or exactly. Decide which equally likely outcomes you will count.", "Define the outcome and event", "Use the same model for both counts."),
         ("Compare your answer with zero and one. For a difficult draw problem, check against ordered or unordered counting with the same assumptions.", "Check the probability", "State the exact fraction you were asked for.")),
        cover=tiles("Outcome","Event","Probability"),
    )
