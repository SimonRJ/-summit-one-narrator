"""Truth values, constraints and complete arguments."""

from itertools import permutations, product

from story import Example, Topic, chain, geometry, grid, say, spoken_list, table, tiles


def truth_liars(lesson):
    v=lesson.visit
    a,b,c,d=(("Ava","Ben","Chen","Dara"),("Iris","Kai","Lia","Mo"),
             ("Noor","Oli","Pia","Raj"),("Sam","Tess","Uri","Val"),("Wren","Xia","Yara","Zac"))[v]
    first=v%2==1
    next_=v%3!=1
    third=v<3
    relation=first==next_
    different=(v%2==0)
    fourth=relation!=different
    truth_c=fourth==third
    truth_b=truth_c==next_
    truth_a=truth_b==first
    labels={True:"truthful",False:"a liar"}
    mark=lambda value: "T" if value else "L"
    assert [(aa,bb,cc,dd) for aa,bb,cc,dd in product((False,True),repeat=4)
        if aa==(bb==first) and bb==(cc==next_) and cc==(dd==third)
        and dd==((aa!=cc)==different)]==[(truth_a,truth_b,truth_c,fourth)]
    comparison="different types" if different else "the same type"
    return Topic(
        (
            ("In a truth-teller puzzle, a person's type agrees with the truth of their statement. A truth-teller's statement is true, and a liar's statement is false.", "Type agrees with the truth of the statement."),
            ("Turn each sentence into a short condition. Then combine the conditions before assigning everyone's type.", "Link the statements and test a complete case."),
        ),
        (
            ("AMC logic practice can ask who made a correct statement or which claims can all hold at once. Keep a small table of cases.", "AMC Upper Primary · test consistent claims"),
            ("A Rossmoyne style argument may need to rule out every alternative. Use a contradiction if some proposed assignment cannot fit its own statements.", "Rossmoyne-style · rule out impossible cases"),
        ),
        (
            Example("Test a statement about yourself", (
                (f"Everyone in a puzzle is either always truthful or always lies. {a} says: I am a liar. Can {a} say that consistently?", f"{a}: I am a liar."),
                ("Check what would happen under each of the two possible types.", "Test both types."),
            ), (
                (f"If {a} is truthful, the claim of being a liar is false. That type cannot make the statement.", "Truthful person → sentence false"),
                (f"If {a} is a liar, the claim is true. That also contradicts the type. Neither case works.", "Liar → sentence true; impossible"),
            ), table(("Possible type","Sentence"),("Truthful","False"),("Liar","True"))),
            Example("Use a statement about both people", (
                (f"Two people are each truthful or a liar. {b} says that both of them are liars. Work out the types of both people.", f"{b}: We are both liars."),
                ("The second person makes no statement. Can the first claim its own type consistently?", "Which types are forced?"),
            ), (
                (f"If {b} were truthful, both would be liars by the statement. That contradicts the idea that {b} is truthful.", f"{b} must be a liar."),
                (f"The claim must be false. Since {b} really is a liar, the other person has to be truthful to make the pair different.", "The other person must be truthful."),
            ), tiles(b,"Other"),worked_art=tiles("Liar","Truthful",highlight=(1,))),
            Example("Solve a chain of four statements", (
                (f"{a} says {b} is {labels[first]}. {b} says {c} is {labels[next_]}.", f"{a} → {b}: {labels[first]}. {b} → {c}: {labels[next_]}."),
                (f"{c} says {d} is {labels[third]}.", f"{c} → {d}: {labels[third]}."),
                (f"{d} says that {a} and {c} are {comparison}. Everyone is either always truthful or always lies. Who is truthful?", f"{d}: {a} and {c} are {comparison}."),
            ), (
                (f"A claim that someone is truthful makes the two types match. A claim that they lie makes the types opposite. Follow the first two links from {a} to {c}.", "Claim truthful: same type. Claim liar: opposite."),
                (f"Those two links make {a} and {c} {'the same type' if relation else 'opposite types'}. This determines the final statement without guessing any individual type.", f"{a} and {c}: {'same' if relation else 'different'}"),
                (f"The statement by {d} is {'true' if fourth else 'false'}. So {d} is {labels[fourth]}.", f"{d}: {mark(fourth)}"),
            ), chain(a,b,c,d), proof=(
                (f"Now use the statement about {d} to identify {c}, which is {labels[truth_c]}. Then {b} is {labels[truth_b]} and {a} is {labels[truth_a]}.", f"{a} {mark(truth_a)}, {b} {mark(truth_b)}, {c} {mark(truth_c)}, {d} {mark(fourth)}"),
                ("Check each sentence with that assignment. The last statement fixed one type, and each link then forced the next, proving there is only one assignment.", "One forced type unlocks the entire chain."),
            ), proof_art=table((a,b,c,d),tuple(mark(t) for t in (truth_a,truth_b,truth_c,fourth)))),
        ),
        (
            ("A liar's entire stated sentence must be false. When the sentence says both people lie, one truthful person is enough to make it false.", "Negate each part separately", "Negate the whole sentence"),
            ("Checking one person's statement is a start. All statements must agree with the proposed types at the same time.", "Keep an assignment after one check", "Test every statement at the end"),
        ),
        (
            ("Mark each statement as a condition. Decide whether it gives same types, opposite types, or another relationship.", "Write the relationships", "Make the truth rule explicit."),
            ("Look for a type forced by several conditions. Then check the remaining assignments against all the statements.", "Prove a unique assignment", "Show why no alternative can fit."),
        ), cover=chain("Statement","True or false","Person's type"),
    )


def line_plot(rows, lines, horizontal="Input", vertical="Total"):
    xmax=max(x for x, _ in rows)
    ymax=max(y for _, y in rows)
    points=[(x,y,"") for x,y in rows]
    axis=len(points)
    points.extend(((0,0,""),(xmax*1.12,0,""),(0,ymax*1.12,"")))
    edges=[(axis,axis+1,3),(axis,axis+2,3),*lines]
    labels=[(xmax*.6,-ymax*.16,horizontal,3), (xmax*.15,ymax*1.13,vertical,3)]
    for x in sorted({point[0] for point in rows}):
        labels.append((x,-ymax*.05,x,3))
    step = (ymax + 4) // 5
    if step >= 5:
        step = (step + 4) // 5 * 5
    for y in range(step, ymax + 1, step):
        labels.append((-xmax*.065,y,y,3))
    return geometry(points,edges,captions=labels,keep_aspect=False)


def graphs(lesson):
    from fractions import Fraction
    v=lesson.visit
    readings=(1+v,5+v,12+2*v,18+3*v)
    total=readings[3]-readings[1]
    times=(0,2,5,9)
    rates=(2+v%3,6+v,4+v%2)
    values=(0,rates[0]*2,rates[0]*2+rates[1]*3,rates[0]*2+rates[1]*3+rates[2]*4)
    assert [Fraction(values[i+1]-values[i], times[i+1]-times[i]) for i in range(3)]==list(rates)
    readings_by_time = list(zip(times, values))
    slow=2+v%3
    faster=slow+2+v%2
    cross=4+v
    fixed=(faster-slow)*cross
    tie=fixed+slow*cross
    nodes=[(0,fixed),(cross,tie),(cross+2,fixed+(cross+2)*slow),(0,0),(cross+2,(cross+2)*faster)]
    return Topic(
        (("A graph connects each horizontal value to a vertical reading. Read the axis names and units before comparing points.", "Read the axes first."),
         ("A change is a difference between readings. A rate of change divides that difference by the distance along the horizontal axis.", "Change per step = rise ÷ run.")),
        (("In AMC Upper Primary questions, graphs and tables often represent the same information. Read the requested interval, row or category carefully.", "AMC Upper Primary · locate the correct values"),
         ("A Mawa style comparison can use a crossing point. At that point two rules give the same value, and their order may change afterwards.", "MAWA-style · explain a crossover")),
        (
            Example("Read two values and compare them", (
                (f"The table shows cumulative counts at hours one to four: {spoken_list(readings)}. How much did the count rise from hour two to hour four?", "Read the values at hours 2 and 4."),
                ("The question asks for a change, not a final total.", "Find the difference.")),
                ((f"The hour two count is {say(readings[1])}. The hour four count is {say(readings[3])}. Both readings use the same units.", f"Count at hour 2: {readings[1]}. At hour 4: {readings[3]}."),
                 (f"Subtract the earlier count from the later one. The increase is {say(total)}.", f"{readings[3]} − {readings[1]} = {total}")), table(("Hour",1,2,3,4),("Total",*readings),highlight=((1,2),(1,4)))),
            Example("Find the fastest rise across unequal intervals", (
                (f"A chart shows times zero, two, five and nine minutes. The total counts at those times are {spoken_list(values)}.", f"Times 0, 2, 5, 9 min. Totals {', '.join(map(str,values))}."),
                ("During which interval was the rate of increase highest? The intervals have different lengths.", "Compare change per minute.")),
                ((f"Divide each rise by its own time interval. The first rise is {say(values[1])} over two minutes, giving {say(rates[0])} per minute.", f"0–2: {values[1]} ÷ 2 = {rates[0]} / min"),
                 (f"The next two rates are {say(rates[1])} and {say(rates[2])} per minute. Use intervals of three minutes and four minutes.", f"2–5: {rates[1]}/min; 5–9: {rates[2]}/min"),
                 (f"The highest rate is {say(rates[1])}. This is the interval from minute two to minute five.", "Fastest rise: minutes 2–5.")),
                line_plot(readings_by_time,[(0,1,0),(1,2,0),(2,3,0)],"Minutes","Total count"),
                worked_art=line_plot(readings_by_time,[(0,1,0),(1,2,1),(2,3,0)],"Minutes","Total count")),
            Example("Locate a crossing and interpret the prices", (
                (f"Plan A charges a fixed fee of {say(fixed)} dollars and then {say(slow)} dollars per visit. Plan B charges {say(faster)} dollars per visit with no fixed fee.", f"A costs {fixed} + {slow}x. B costs {faster}x."),
                ("At how many visits are the costs equal, and which plan is cheaper after that?", "Find the crossover on the graph.")),
                ((f"At a crossing the two costs are equal. A starts {say(fixed)} dollars higher, while B rises {say(faster-slow)} dollars faster per visit.", f"Initial gap ${fixed}. Gap closes by ${faster-slow} each visit."),
                 (f"Divide to find the intersection at {say(cross)} visits. At that point both costs equal {say(tie)} dollars.", f"{fixed} ÷ {faster-slow} = {cross} visits. Cost ${tie}."),
                 ("After the crossing B is higher on the graph, because its cost rises faster. Plan A is cheaper beyond that visit count.", f"After {cross} visits, A is cheaper.")),
                line_plot(nodes,[(0,1,0),(1,2,0),(3,4,1)],"Visits","Cost ($)"),proof=(
                    (f"Test one visit after the crossover. A costs {say(tie+slow)} dollars. B costs {say(tie+faster)} dollars.", f"At {cross+1}: A ${tie+slow}; B ${tie+faster}."),
                    ("B adds the larger amount every further visit, so the choice will not switch again.", "The steeper line stays above after the crossing."))),
        ),
        (("Read both axis scales. A vertical rise alone doesn't tell you the rate if time intervals are different.", "Compare the increases alone", "Divide each increase by its own interval"),
         ("At a crossing, both graph rules give the same value. Read the horizontal coordinate to find when it happens.", "Read the cost as the number of visits", "Use the horizontal axis for visits")),
        (("Label the horizontal and vertical quantities. Trace to the axis or row before performing a calculation.", "Read the axes and scale", "Use units in the answer."),
         ("For a change, take a difference. For a rate, divide by the interval. For an intersection, check both rules at the same input.", "Interpret the result", "Check how the graph answers the exact question.")),
        cover=line_plot([(0,0),(2,3),(5,4),(7,8)],[(0,1,0),(1,2,0),(2,3,1)]),
    )
