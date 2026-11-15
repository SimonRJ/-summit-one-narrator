"""Logic puzzles, magic-grid structure and completeness proofs."""

from itertools import permutations

from story import Example, Topic, chain, grid, say, spoken_list, table, tiles


def deduction(lesson):
    v=lesson.visit
    items=("paintings","short films","models","speakers","robots","kites","science displays")
    item=items[v]
    names=("Ada","Ben","Chloe","Dylan","Eva") if v%2==0 else ("Finn","Grace","Hugo","Ivy","Jack")
    names=names[v%5:]+names[:v%5]
    a,b,c,d,e=names
    candidates=[]
    for arrangement in permutations(names):
        order={name:i+1 for i,name in enumerate(arrangement)}
        if order[c]==order[b]+1 and order[c]==order[a]+2 and order[d] in (1,5) and order[d]<order[a] and order[e]!=2:
            candidates.append(arrangement)
    assert candidates==[(d,a,b,c,e)]
    return Topic(
        (("In a deduction puzzle, each clue rules out some possibilities. Put positions and candidates in view so that you can see what a clue changes.", "Use clues to remove possibilities."),
         ("Combine clues about the same position or person. A small forced block can determine most of the arrangement.", "Link clues that share a subject.")),
        (("AMC practice may ask who finished first or which option has to be true. Build a short order diagram and mark fixed positions.", "AMC Upper Primary · mark forced positions"),
         ("A Rossmoyne style puzzle may ask for a unique arrangement. Show where the alternatives fail before checking that the survivor works.", "Rossmoyne-style · show why the result is unique")),
        (
            Example("Combine two clues about one position", (
                (f"Three people line up. {a} is not at either end. {b} stands before {a}. In what order do {a}, {b} and {c} stand?", "Three positions. One name cannot go at either end."),
                ("Start with the clue that fixes an exact position.", "Which name belongs in the middle?")),
                ((f"{a} must go in position two. The only position earlier than two is position one, so {b} goes there.", f"1 {b} · 2 {a} · 3 ?"),
                 (f"The final position takes {c}. Check the order obeys both clues.", f"{b} → {a} → {c}.")),tiles("1","2","3")),
            Example("Combine a neighbour clue with an end clue", (
                (f"Arrange {a}, {b}, {c} and {d} in four positions. {b} is immediately after {a}, and {d} is at one end.", f"{a}–{b} is a block; {d} is at an end."),
                (f"{c} is first. What is the only order?", f"{c} must stand first.")),
                ((f"{c} is first, so {d} cannot use that end and must be fourth. The remaining two positions are two and three.", f"1 {c} · 2 ? · 3 ? · 4 {d}"),
                 (f"Put {a} in two and {b} in three, because {b} immediately follows {a}. That fixes every name.", f"{c} → {a} → {b} → {d}.")),tiles("1","2","3","4")),
            Example("Reduce a five-position puzzle to two candidates", (
                (f"Five distinct {item} have numbered places one to five, with names {spoken_list(sorted(names))}. {b} is immediately before {c}, and {a} is two places before {c}.", f"{b} immediately before {c}; {a} two places before {c}."),
                (f"{d} is at one end and earlier than {a}. {e} is not in position two. Find the complete order.", f"{d} at an end and before {a}; {e} cannot be second.")),
                ((f"The first two clues force a consecutive block in the order {a}, {b}, {c}. Because {d} is before the block and at an end, {d} can only be first.", f"{d} is first. Place the block {a} → {b} → {c}."),
                 (f"The block can start in position two or three. Starting in three leaves position two for {e}, which the last clue excludes.", f"Start at 3 → {e} would be second. Cross out."),
                 (f"Start at two. The final order is {spoken_list((d,a,b,c,e))}.", f"{d} → {a} → {b} → {c} → {e}.")),
                tiles("1","2","3","4","5"),worked_art=table(("Start","1","2","3","4","5"),(2,d,a,b,c,e),(3,d,e,a,b,c)),proof=(
                    (f"The gap between {a} and {c} is two places and {b} sits immediately before {c}. {d} is first, before {a}, and {e} is fifth.", "Check the distance, adjacency, end position and exclusion."),
                    ("The block had just two starting positions after the end clue. One failed, so the order that passed is unique.", "Only one arrangement survives all the clues."))),
        ),
        (("Immediately before means the two positions touch. Earlier than only compares order, so a gap between the names can still be allowed.", "Treat earlier than as a neighbour rule", "Keep the two clues distinct"),
         ("Finish by checking the arrangement against the original constraints. A solution may look plausible even when it violates an exclusion.", "Stop after placing every name", "Test every placement against the clues")),
        (("Turn each clue into a fixed place, order or distance. Apply the strongest clues to shrink the possible positions first.", "Mark the strongest restrictions", "Look for a group that moves together."),
         ("If more than one case remains, write each one and identify the clue that accepts or rejects it. Verify the final survivor.", "Prove that only one survives", "Show where alternatives fail.")),
        cover=chain("Clue","Block","Order"),
    )


def magic_grid(lesson):
    v=lesson.visit
    small=15+3*v
    sub=small-(4+v)-(5+v)
    start, step=1+v,1+v%3
    values=[start+i*step for i in range(9)]
    centre=values[4]
    target=3*centre
    diagonal_sum=2*centre
    base=((8,1,6),(3,5,7),(4,9,2))
    for _ in range(v%4):
        base=tuple(zip(*base[::-1]))
    if v%2==1:
        base=tuple(tuple(reversed(row)) for row in base)
    solution=tuple(tuple(values[n-1] for n in row) for row in base)
    (nw,n,ne),(w,m,e),(sw,s,se)=solution
    assert m==centre and nw+se==ne+sw==diagonal_sum
    assert all(sum(row)==target for row in (*solution,*zip(*solution)))
    partial=((nw,"?",ne),("?","?","?"),("?","?","?"))
    return Topic(
        (("A magic grid has the same sum along every row, column and long diagonal. Start with a line where only one entry is missing.", "Every full line shares a target sum."),
         ("Two or more intersecting lines reveal relationships that a single row cannot. Look for one cell that belongs to several useful lines.", "Use lines that meet.")),
        (("AMC Upper Primary practice can use a missing value in a number grid. Recover the shared target before filling the blanks.", "AMC Upper Primary · find the target sum"),
         ("A MAWA style extension may ask you to explain which blanks are forced. Keep the long diagonals as well as the rows and columns.", "MAWA-style · justify the completed grid")),
        (
            Example("Fill a missing value on a known line", (
                (f"Every row in a grid totals {say(small)}. One row contains {say(4+v)} and {say(5+v)}, with one empty cell.", f"Row: {4+v}, {5+v}, ?. Total {small}."),
                ("What number completes that row?", "Subtract the two known entries.")),
                ((f"The known entries add to {say(9+2*v)}. Together with the missing entry they must reach {say(small)}.", f"{4+v} + {5+v} = {9+2*v}."),
                 (f"The difference is {say(sub)}. Put that value in the empty cell so all three add to the target.", f"{small} − {9+2*v} = {sub}.")),grid((4+v,5+v,"?"))),
            Example("Find the line sum and centre", (
                (f"A three-by-three magic grid uses each of {spoken_list(values)} once. What are the common line sum and the centre entry?", f"Use {start}, {values[1]}, …, {values[-1]} once each."),
                ("The three rows cover the whole grid. The four straight lines through the centre overlap there.", "Compare the three rows with the four centre lines.")),
                ((f"The entries sum to {say(sum(values))}. Divide by three because there are three full rows of equal sum. The target is {say(target)}.", f"{sum(values)} ÷ 3 = {target}."),
                 (f"The central row, central column and both diagonals each sum to {say(target)}. Together they count all other entries once and the centre four times.", f"4 × {target} = {sum(values)} + 3 × centre."),
                 (f"Subtract the total of all nine entries and divide by three. The centre is {say(centre)}.", f"Centre = ({4*target} − {sum(values)}) ÷ 3 = {centre}.")),
                grid(("↘","↓","↙"),("→","?","←"),("↗","↑","↖"),highlight=((1,1),))),
            Example("Complete a grid from two specified corners", (
                (f"Use the same nine values once each in a three-by-three magic grid. The top left is {say(nw)} and the top right is {say(ne)}.", f"Top corners: {nw} and {ne}. Use the same nine values."),
                ("Fill the whole grid. Explain why no other completion can meet these clues.", "Find the unique finished square.")),
                ((f"The line sum is {say(target)} and the centre is {say(centre)}. Any two cells directly opposite through the centre must total {say(diagonal_sum)}.", f"Opposite cells sum to {target} − {centre} = {diagonal_sum}."),
                 (f"The bottom corners must therefore be {say(sw)} at the left and {say(se)} at the right. The top and bottom row blanks are {say(n)} and {say(s)}.", f"Opposite corners: {sw}, {se}. Row middles: {n}, {s}."),
                 (f"Fill the middle of column one with {say(w)} and column three with {say(e)}, using the same target sum.", f"Side blanks: {target} − {nw} − {sw} = {w}; {target} − {ne} − {se} = {e}.")),
                grid(*partial),worked_art=grid((nw,n,ne),("?",m,"?"),(sw,s,se)),
                proof=((f"The middle row is {say(w)}, {say(m)}, {say(e)}. The middle column is {say(n)}, {say(m)}, {say(s)}. Both sum to {say(target)}.", "Check the last row and column."),
                       ("The two diagonals match as well, and all nine values are used once. Every new entry came from a forced sum, so this grid is unique.", "Each entry forced, and every condition checked.")),
                proof_art=grid(*solution)),
        ),
        (("The line total is the sum of one row, not of all nine entries. Three full rows together use every cell once.", "Use the total of all entries for one row", "Divide the all-cell total by the three rows"),
         ("If diagonals count, check them. A grid that fits the rows and columns may fail the long diagonals.", "Check only horizontal and vertical sums", "Test both diagonal sums too")),
        (("Find the target and mark lines with one blank. When every line has several blanks, combine intersecting lines.", "Look for a forced value", "Use a line sum or a sum relationship."),
         ("After filling the grid, check all line totals and the rule about repeated entries. A chain of forced values proves uniqueness.", "Verify the finished grid", "Explain why each entry had to go there.")),
        cover=grid(("□","□","□"),("□","◇","□"),("□","□","□"),highlight=((1,1),)),
    )


def exhaustiveness(lesson):
    v=lesson.visit
    lo,hi,div=20+3*v,32+3*v,5+v
    values=[n for n in range(lo,hi+1) if n%div==0]
    total=17+2*v
    cap=12+v
    start=total-cap
    finish=total//2
    pairs=[(x,total-x) for x in range(start,finish+1)]
    diff=6+2*v
    lower=9+2*v
    units=lower*(lower+diff)
    near=lower-1
    assert [(a,a+diff) for a in range(1,units) if a*(a+diff)==units]==[(lower,lower+diff)]
    return Topic(
        (("A proof needs reasons that cover every allowed case. To prove a unique answer, show that it works and that every different answer fails.", "Existence checks one; uniqueness rules out all others."),
         ("A bound or an increasing pattern can eliminate an entire range in one step.", "Rule out whole ranges where you can.")),
        (("AMC practice may ask for the only integer satisfying a clue. Use the constraint to get a narrow range before testing candidates.", "AMC Upper Primary · shrink the search"),
         ("MAWA application practice rewards clear reasons. A proof can use inequalities, a complete list, or a pattern you justify for all values.", "MAWA-style · explain why the search is complete")),
        (
            Example("Find all divisible numbers in a closed interval", (
                (f"List the multiples of {say(div)} from {say(lo)} through {say(hi)}, counting both endpoints. Explain how you know the list is complete.", f"Multiples of {div} within {lo}–{hi}."),
                ("Find the first eligible multiple and step forward by the divisor.", "Check the multiple just outside each end.")),
                ((f"The first eligible value is {say(values[0])}. The preceding multiple is {say(values[0]-div)}, below the lower limit.", f"Start at {values[0]}; {values[0]-div} is too low."),
                 (f"The full list is {spoken_list(values)}. The next multiple is {say(values[-1]+div)}, which is already above the upper limit.", f"{', '.join(map(str,values))}. Next: {values[-1]+div}.")),chain(f"+{div}",f"+{div}",f"+{div}")),
            Example("Prove a short list of unordered pairs is complete", (
                (f"Two positive whole numbers add to {say(total)}. Neither can exceed {say(cap)}. List all pairs, counting a swapped pair only once.", f"x + y = {total}; both ≤ {cap}."),
                ("Call the smaller number x and use this to bound x from both sides.", "Choose the smaller member as the first variable.")),
                ((f"The larger number is {say(total)} minus x, so x is at least {say(start)}. Since x is the smaller, it is at most {say(finish)}.", f"{total} − {cap} ≤ x ≤ floor({total}/2)."),
                 (f"Each integer in that range gives exactly one partner. There are {say(len(pairs))} pairs. All of them meet the cap.", f"x runs {start}–{finish}; {len(pairs)} pairs.")),
                table(("Smaller","Larger"),*pairs)),
            Example("Show that a rectangle with a given area and gap is unique", (
                (f"An integer-sided rectangle has area {say(units)} square units. Its longer side is {say(diff)} units greater than its shorter side.", f"Area {units}; long side = short side + {diff}."),
                ("Find its two side lengths and prove that no second pair of positive integer lengths works.", "Show existence and uniqueness.")),
                ((f"Let x be the shorter side. The area is x times x plus {say(diff)}, with both terms positive. Try {say(near)} for x and check the area.", f"A = x(x + {diff}); A({near}) = {near*(near+diff)}."),
                 (f"The next integer, {say(lower)}, gives {say(lower)} times {say(lower+diff)}, exactly {say(units)}. That proves this pair exists.", f"{lower} × {lower+diff} = {units}.")),
                tiles("Short x",f"Long x + {diff}"),proof=(
                    (f"Every increase in x increases both positive factors. The area increases strictly. Any x below {say(lower)} gives too little area and any x above gives too much.", "If x rises, both positive factors rise."),
                    (f"The dimensions are therefore uniquely {say(lower)} and {say(lower+diff)} units. They check both the area and the side difference.", f"Unique sides: {lower} and {lower+diff}.")),
                proof_art=table(("Short","Long","Area"),(near,near+diff,near*(near+diff)),(lower,lower+diff,units),(lower+1,lower+1+diff,(lower+1)*(lower+1+diff)))),
        ),
        (("One candidate that works proves existence only. Give a bound, exhaustive list or increasing rule to exclude every other candidate.", "Stop after finding one answer", "Exclude every remaining possible answer"),
         ("When working with a closed interval, its boundary values are eligible. Test whether the inequality is strict before dropping an endpoint.", "Automatically drop the endpoints", "Respect the inclusive bounds")),
        (("State what you need to prove: all answers, at least one answer, or exactly one answer. List the restrictions that define a legal candidate.", "Read the proof goal", "Check the candidate domain."),
         ("Use a complete range or a justified relationship. Verify the survivor or survivors in the original problem before writing your answer.", "Prove the search complete", "Then verify each claimed solution.")),
        cover=chain("Bound","Check","Prove"),
    )
