"""Working backwards, changing totals and identifying a hidden quantity."""

from fractions import Fraction
from functools import lru_cache

from story import Example, Topic, bars, chain, say, spoken_list, table, tiles


def backwards(lesson):
    v=lesson.visit
    x,a,m=5+v,2+v,2+v%3
    end=(x+a)*m
    r=3+v%2
    given=6+v
    middle=(r-1)*given
    award=4+v
    final=middle+award
    multiplier,divisor=((3,2),(5,2),(4,3),(3,4))[v-1]
    add=1+v
    subtract=3+v
    low=21+2*v
    high=low+8+v
    scores=tuple(n for n in range(low,high+1) if divisor*(n+subtract)%multiplier==0)
    inputs=tuple(divisor*(n+subtract)//multiplier-add for n in scores)
    assert inputs==tuple(q for q in range(100) if (q+add)*multiplier%divisor==0
                         and low<=(q+add)*multiplier//divisor-subtract<=high)
    return Topic(
        (
            ("Work backwards when you know where an operation ended but need to find where it began. Each step has an inverse that restores its input.", "A forward step has a reverse step."),
            ("For a chain of changes, undo the last change first. Then test the whole forward chain.", "Reverse the order and every operation."),
        ),
        (
            ("An AMC Upper Primary problem may tell you what happened to a mystery number, a balance or a pile and ask for the starting amount.", "AMC Upper Primary · find the unknown start"),
            ("A Rossmoyne style question can also constrain the final range or require whole numbers along the way. Reverse only the legal states.", "Rossmoyne-style · apply the whole-number rule"),
        ),
        (
            Example("Reverse a two-step machine", (
                (f"A machine adds {say(a)} to a number, then multiplies by {say(m)}. The final output is {say(end)}. What went in?", f"Input → plus {a} → times {m} → {end}"),
                ("Trace from the right of the diagram to the left.", "Which step must be undone first?"),
            ), (
                (f"Undo the multiplication by dividing {say(end)} by {say(m)}. The result is {say(x+a)}, just after the original addition.", f"{end} ÷ {m} = {x+a}"),
                (f"Now subtract {say(a)} to find the input {say(x)}. As a check, forward addition and multiplication return {say(end)}.", f"({x+a} − {a}) = {x}"),
            ), chain("?",f"+{a}",f"×{m}",end),worked_art=chain(end,f"÷{m}",f"−{a}",x)),
            Example("Put the original whole back together", (
                (f"Remove one of {say(r)} equal parts of a pile. Then add {say(award)} counters. There are {say(final)} counters afterwards.", f"Remove 1/{r} of the original, then add {award}."),
                ("How many were in the pile at the start? Write the intermediate state before restoring the whole.", f"Final count: {final}. Original count: ?"),
            ), (
                (f"Subtract the addition of {say(award)}. That leaves {say(middle)}, which is {say(r-1)} of the original {say(r)} equal parts.", f"{final} − {award} = {middle}"),
                (f"Divide those {say(middle)} counters by {say(r-1)}. One original part has {say(given)} counters.", f"One part: {middle} ÷ {r-1} = {given}"),
                (f"Rebuild the original {say(r)} parts. There were {say(r*given)} counters before either operation.", f"Original = {r} × {given} = {r*given}"),
            ), bars(("Original",tuple((1,f"1/{r}") for _ in range(r))),
                    ("After removal",tuple((1,f"1/{r}") for _ in range(r-1))))),
            Example("Work backwards through a range of outputs", (
                (f"Start with a positive whole number. Add {say(add)}, multiply by {say(multiplier)}, divide by {say(divisor)}, and subtract {say(subtract)}.", f"Input → +{add} → ×{multiplier} → ÷{divisor} → −{subtract}"),
                (f"The final reading is a whole number from {say(low)} to {say(high)} inclusive. Find all possible whole-number inputs.", f"Legal readings: {low}–{high}. Which inputs work?"),
            ), (
                (f"Take each possible reading, add {say(subtract)}, then multiply by {say(divisor)}. We are undoing the final two operations.", f"Reading y → {divisor}(y + {subtract})"),
                (f"An input can be whole only if that intermediate result is divisible by {say(multiplier)}. Check the readings against this condition before going further.", f"Keep multiples of {multiplier}."),
                (f"The allowed readings are {spoken_list(scores)}. Undo the first two operations for those readings only.", f"Readings kept: {', '.join(map(str,scores))}"),
            ), chain(f"+{add}",f"×{multiplier}",f"÷{divisor}",f"−{subtract}"),proof=(
                (f"Divide each allowed intermediate value by {say(multiplier)}, then subtract {say(add)}. This gives {spoken_list(inputs)}.", f"Inputs: {', '.join(map(str,inputs))}"),
                (f"For example, starting at {say(inputs[0])} and running all four steps forward gives {say(scores[0])}. Every reading in the requested interval was tested.", f"Check: {inputs[0]} → {scores[0]} in the original machine"),
            ),proof_art=table(("Reading","Input"),*zip(scores,inputs))),
        ),
        (
            ("Undo multiplication with division, and undo addition with subtraction. Reversing just the signs without reversing the order changes the input.", "Undo in the original order", "Undo the last operation first"),
            ("A fraction refers to the whole at the time it was used. Check how many equal parts the intermediate value represents.", "Divide by the full number of parts", "Recover the size of one remaining part"),
        ),
        (
            ("Write a short arrow for every step. Work from the known output, writing the inverse of the last arrow first.", "Draw the forward and reverse rules", "Keep each change beside its arrow."),
            ("Check required whole numbers and allowed ranges as you reverse. Confirm your answer by running each claimed input forward.", "Check the original rule", "Use the exact order and test the final value."),
        ), cover=chain("Input","Change","Output"),
    )


def recurrence(lesson):
    v=lesson.visit
    start,step=5+v,3+v
    short=[start+i*step for i in range(4)]
    x=3+v
    stages=4+v
    values=[(x-1)*2**j+1 for j in range(stages+1)]
    finish=8+v
    broken=3+v//2
    counts=[1]
    for n in range(1,finish+1):
        counts.append(0 if n==broken else counts[n-1]+(counts[n-2] if n>=2 else 0))

    @lru_cache(maxsize=None)
    def direct(n):
        if n in (broken,finish+1):
            return 0
        if n == finish:
            return 1
        return direct(n+1)+direct(n+2)

    assert direct(0)==counts[-1]
    return Topic(
        (
            ("A recurrence tells you how a new state follows from earlier ones. Write the starting state and exactly what is repeated.", "Start value + rule for the next value"),
            ("If a state can be reached in more than one way, split the count by the final step. This can turn a branching tree into a short table.", "Count by the last step."),
        ),
        (
            ("AMC Upper Primary questions can use growing shapes or repeated moves. Translate the pattern into a stated rule before extending it.", "AMC Upper Primary · build the next term"),
            ("In a Mawa style investigation, change a starting rule or block one route. Explain how that adjustment spreads through the table.", "MAWA-style · change one state"),
        ),
        (
            Example("Name a start and a next step", (
                (f"Start a sequence at {say(start)}. Add {say(step)} to get each next term. What are the first four terms?", f"Start {start}, then add {step} each time."),
                ("Remember the starting value already counts as the first term.", "The start is term 1."),
            ), (
                (f"The first addition produces {say(short[1])}. Repeat the same addition to get {say(short[2])}, then {say(short[3])}.", " → ".join(map(str,short))),
                ("Each difference is the same, so the rule predicts the list from its first term without any guess about the pattern.", f"Each arrow adds {step}."),
            ), chain(start,f"+{step}","?"),worked_art=chain(*short)),
            Example("Reveal the doubling hidden in a rule", (
                (f"A display starts at {say(x)}. Each new reading is twice the last reading, minus one. Find its value after {say(stages)} changes.", f"Start {x}. Repeat ×2, then −1."),
                ("Try tracking the distance from one as well as the reading itself.", f"Find the reading after {stages} changes."),
            ), (
                ("If a reading equals one plus a gap, doubling and subtracting one makes it one plus twice that gap. The gap doubles each time.", "2(1 + gap) − 1 = 1 + 2 × gap"),
                (f"The first gap is {say(x-1)}. After {say(stages)} changes it is {say(x-1)} times two to the power {say(stages)}.", f"Gap: {x-1} × 2^{stages} = {values[-1]-1}"),
                (f"Add back the fixed one. The final reading is {say(values[-1])}. Compare the first two steps to check the pattern.", f"Final reading = {values[-1]}"),
            ), chain(*values[:4])),
            Example("Count routes past one broken rung", (
                (f"Start on rung zero. A move goes up one or two rungs. Rung {say(broken)} is broken, so no route can land there.", f"Allowed jumps: +1 or +2. Avoid rung {broken}."),
                (f"How many different move sequences finish exactly on rung {say(finish)}? Count by the last jump onto each rung.", f"How many routes reach rung {finish}?"),
            ), (
                ("There is one way to be at the start: make no jumps. There are zero ways to land on the broken rung.", f"W(0) = 1, W({broken}) = 0"),
                ("To arrive at an allowed rung, the previous rung is either one below or two below. Add the counts of those disjoint kinds of route.", "W(n) = W(n−1) + W(n−2) on open rungs."),
                (f"Fill the table in order. The two entries just before the finish are {spoken_list(counts[-3:-1])}. Their sum is {say(counts[-1])}.", f"{counts[-3]} + {counts[-2]} = {counts[-1]} routes"),
            ), tiles(*range(finish+1),highlight=(broken,)),worked_art=table(("Rung",*range(finish+1)),("Ways",*counts),
                  highlight=((1,broken+1),(1,finish+1))), proof=(
                ("The broken rung stops landings, but a jump of two can go over it. That is why an open rung after it can still have a positive count.", f"Skipping over rung {broken} is allowed."),
                ("The last-jump cases partition the routes. No route can end with both a one-rung jump and a two-rung jump.", "Last steps are separate cases."),
            ),proof_art=chain(broken-1,"+2",broken+1)),
        ),
        (
            ("Put one at the starting state when counting routes. The one empty route is what gives the first legal jump a route to extend.", "Start the route table at zero", "Use 1 way to stand at the start"),
            ("A broken rung removes the routes landing there. A move that jumps over it can still be legal.", "Set every later entry to zero", "Set just the broken landing to zero"),
        ),
        (
            ("State the starting values and the recurrence. Work in an order where every entry you need has already been found.", "Start from known states", "Write the rule for each legal next state."),
            ("Check the first steps and any exceptional states. If counting routes, explain why the last-step cases cannot overlap.", "Verify the transition", "Handle forbidden positions separately."),
        ), cover=chain("Start","Rule","Next"),
    )


def part_whole(lesson):
    v=lesson.visit
    a,b=3+v%3,2+v%2
    groups=5+v
    n=a*groups
    start=a*b*groups
    after=(a-1)*b*groups
    end=(a-1)*(b-1)*groups
    gift=b*(2+v)
    new=after+gift
    finish=new*(b-1)//b
    assert new%b==0 and finish*b//(b-1)==new
    return Topic(
        (
            ("A fraction tells you about a particular whole. When the whole changes, the same fraction can describe a different number of pieces.", "Name the whole before using a fraction."),
            ("Draw equal parts for the first whole, then mark which amount becomes the whole for the next instruction.", "Track the amount each instruction refers to."),
        ),
        (
            ("In AMC practice, a fraction of the original pile and a fraction of what is left can occur in the same problem. Underline the words after of.", "AMC Upper Primary · original or remaining?"),
            ("A Rossmoyne style word puzzle may reveal the ending and ask you to recover the starting quantity. Reverse one change at a time.", "Rossmoyne-style · recover the starting whole"),
        ),
        (
            Example("Find the fraction that remains", (
                (f"There are {say(n)} tokens. A player takes one of {say(a)} equal parts. How many tokens remain?", f"Start {n}. Remove 1/{a}."),
                ("Show the difference between the amount removed and the amount the question asks for.", "Find the number left."),
            ), (
                (f"One part has {say(groups)} tokens. The remaining {say(a-1)} parts contain {say(n-groups)} tokens.", f"One part = {n} ÷ {a} = {groups}"),
                (f"Check by adding the removed part back. {say(n-groups)} plus {say(groups)} returns {say(n)}.", f"Remaining = {n} − {groups} = {n-groups}"),
            ), bars(("Original",tuple((1,groups) for _ in range(a))))),
            Example("Change the whole for the second fraction", (
                (f"A box starts with {say(start)} chalk pieces. A class uses one of {say(a)} equal parts. Then another class uses one of {say(b)} equal parts of what is left.", f"{start} start, use 1/{a}, then 1/{b} of the remainder."),
                ("How many pieces remain after both classes? Label the whole for each fraction.", "Count the remaining chalk."),
            ), (
                (f"After the first class the remaining count is {say(after)}, since {say(start)} divided by {say(a)} were used.", f"First remainder = {after}"),
                (f"The next whole is now {say(after)}. Divide it into {say(b)} equal parts. The second class uses {say(after//b)} pieces.", f"Second use = {after} ÷ {b} = {after//b}"),
                (f"Subtract the second use to get {say(end)}. This is {say(b-1)} of the second whole's parts.", f"Left at the end = {end}"),
            ), bars(("Original",((start-after,f"used"),(after,"left"))),
                    ("New whole",((after//b,"used"),(end,"left"))))),
            Example("Reverse two fractions with a gift in between", (
                (f"Take one of {say(a)} equal parts from a pile. Add a gift of {say(gift)} pieces. Then take one of {say(b)} equal parts of that new amount.", f"Remove 1/{a}, add {gift}, then remove 1/{b}."),
                (f"There are {say(finish)} pieces left. How many were in the original pile?", f"Left at the end: {finish}. Find the starting pile."),
            ), (
                (f"The ending {say(finish)} pieces represent {say(b-1)} of the last {say(b)} equal parts. Find one part, then rebuild that whole.", f"Before last removal: {finish} ÷ {b-1} × {b} = {new}"),
                (f"Undo the gift by subtracting {say(gift)}. The remaining {say(after)} pieces are what was left after the first removal.", f"{new} − {gift} = {after}"),
                (f"Those were {say(a-1)} of the original {say(a)} equal parts. Restoring the missing part gives {say(start)}.", f"Original: {after} ÷ {a-1} × {a} = {start}"),
            ), chain("Start","Remove",f"+{gift}","Remove",finish),proof=(
                (f"Run the recipe forward. Remove {say(start//a)} from {say(start)} to get {say(after)}. Add the gift to get {say(new)}.", f"{start} − {start//a} + {gift} = {new}"),
                (f"The final removal is {say(new//b)}. That leaves {say(finish)}, the stated ending. Each fraction has used its own whole.", f"{new} − {new//b} = {finish}"),
            ),proof_art=chain(start,after,new,finish)),
        ),
        (
            ("Add fractions directly only when they refer to the same original whole. A fraction of what is left uses a new whole.", "Add the two fractions used", "Name the whole at each step"),
            ("When reversing a removal, divide the remaining amount by the number of remaining parts first. The denominator names the size of the full set of parts.", "Divide the remainder by all parts", "Divide by the surviving parts"),
        ),
        (
            ("Write the word original, remaining or new above each fraction. Draw equal parts for that named whole.", "Mark each whole", "Use bars when the base amount changes."),
            ("If the ending is known, rebuild the last whole first. Then reverse any addition and earlier removal.", "Reverse and recheck", "Forward steps must reproduce the ending."),
        ), cover=bars(("Original",((1,"used"),(4,"left"))),("New whole",((1,"used"),(3,"left")))),
    )


def linear_context(definition, application, first, second, examples, diagram):
    """Build an outline around explicit, question-specific mathematical moves."""
    idea, point = definition
    clue, exam = application
    err1, right1, why1 = first
    err2, right2, why2 = second
    return Topic(
        ((idea, point), ("Put a label on each unknown before you use a symbol. As you work, keep the same label attached to the same quantity.", "One symbol keeps one meaning.")),
        ((f"In AMC Upper Primary practice, look for {clue}. A diagram or short equation can collect the clues in one place.", "AMC Upper Primary · "+exam),
         ("In a Rossmoyne style puzzle, two or more conditions can constrain the same value. Substitute your result into the original conditions to prove it fits.", "Rossmoyne-style · check every condition")),
        examples, ((why1,err1,right1),(why2,err2,right2)),
        (("Name the unknown quantity and write what each given relationship says about it. Label your equations with the units used in the story.", "Translate every condition", "Use the same units and the same unknown names."),
         ("Recheck the result by applying the original relationships, including each bound, whole-number rule or shared total.", "Verify the result", "Substitute back into the original conditions.")),
        cover=diagram,
    )


def word_equations(lesson):
    v=lesson.visit
    x=7+v
    a,b=3+v%2,5+v
    simple=a*x+b
    dif=4+2*v
    medium_total=2*x+dif
    adult,child=8+v,4+v
    na,nb=10+2*v,14+v
    tickets=na+nb
    dollars=na*adult+nb*child
    assert (dollars-tickets*child)//(adult-child)==na
    return linear_context(
        ("An equation says two expressions measure the same amount. Name the unknown, then represent each action on that amount with an operation.", "Write one expression for each side."),
        ("stories giving a total, a fixed cost or a difference between two quantities", "turn a sentence into an equation"),
        ("Use the same letter for two prices", "Assign one letter per unknown", "One letter names one quantity. Use separate variables when the ticket prices or numbers can differ."),
        ("Use a total without checking its units", "Keep counts and money separate", "Ticket counts add to a number of tickets. Each price must multiply a count before it contributes to a total cost."),
        (
            Example("Write a one-variable equation", (
                (f"Multiply a number by {say(a)} and add {say(b)}. The result is {say(simple)}. Find the number.", f"{a}x + {b} = {simple}"),
                ("Use x for the input and check what the result measures.", "Let x be the original number.")),
                ((f"Subtract {say(b)} from both sides to keep the equation balanced. The remaining multiple of x equals {say(a*x)}.", f"{a}x = {simple} − {b} = {a*x}"),
                 (f"Divide by {say(a)} to get {say(x)}. Multiplying and adding in the original order checks the equation.", f"x = {x}")), chain("x",f"×{a}",f"+{b}",simple)),
            Example("Build both quantities from one unknown", (
                (f"A team collects {say(medium_total)} points in two rounds. The second round has {say(dif)} more points than the first. Find each round's score.", f"Total {medium_total}, second is {dif} more."),
                ("Let x stand for the score in the first round.", "Represent both scores using x.")),
                ((f"The first score is x. The second is x plus {say(dif)}. Together the scores total {say(medium_total)}.", f"x + (x + {dif}) = {medium_total}"),
                 (f"Subtract the fixed difference and divide the rest by two. The first score is {say(x)}, and the second is {say(x+dif)}.", f"Scores {x} and {x+dif}")), bars(("Round 1",((x,"x"),)),("Round 2",((x,"x"),(dif,f"+{dif}"))))),
            Example("Model ticket counts and revenue separately", (
                (f"An event sells {say(tickets)} tickets. Adult tickets cost {say(adult)} dollars each and child tickets cost {say(child)} dollars each.", f"{tickets} tickets at either ${adult} or ${child}."),
                (f"The total revenue is {say(dollars)} dollars. How many adult tickets and child tickets were sold?", f"Revenue ${dollars}. Find both ticket counts.")),
                ((f"Let x be the number of adult tickets. Since {say(tickets)} tickets were sold, {say(tickets)} minus x is the number of child tickets.", f"Adult x, child {tickets} − x"),
                 (f"Price times count gives each revenue. Combine the two products in the same equation to match the stated total.", f"{adult}x + {child}({tickets} − x) = {dollars}"),
                 (f"Collect x terms. The baseline from child-price tickets would be {say(tickets*child)} dollars. Each adult ticket adds {say(adult-child)} dollars above it.", f"({adult} − {child})x = {dollars} − {tickets*child}")),
                table(("Ticket","Count","Price"),("Adult","x",adult),("Child",f"{tickets}−x",child)),proof=(
                    (f"Divide by {say(adult-child)} to get {say(na)} adult tickets. The remaining {say(nb)} tickets are child tickets.", f"x = {na}, child tickets = {nb}"),
                    (f"Check both counts and costs. The tickets sum to {say(tickets)}, and their prices sum to {say(dollars)} dollars.", f"{na} × {adult} + {nb} × {child} = {dollars}"))),
        ), tiles("Count","Price","Total"),
    )


def simultaneous(lesson):
    v=lesson.visit
    x,y=10+v,6+v%3
    plus=x+y
    gap=x-y
    a,b=7+v,11+v//2
    one=2*a+b
    two=a+2*b
    third=12+v
    ab,bc,ca=a+b,b+third,third+a
    total=a+b+third
    assert ab+bc+ca==2*total
    return linear_context(
        ("Simultaneous conditions describe the same unknowns at the same time. A solution must make every condition true together.", "Use the conditions together."),
        ("two totals or a sum and a difference describing the same values", "combine the information from both clues"),
        ("Find any pair with the right sum", "Test the second condition too", "A single total can fit many pairs. Use the second condition to choose a particular pair."),
        ("Add pair totals as if they were disjoint", "Account for the repeated values", "In the three pair totals, each single quantity appears twice. Divide the combined pair totals by two."),
        (
            Example("Use a sum and a difference together", (
                (f"Two numbers add to {say(plus)}. The larger is {say(gap)} more than the smaller. What are they?", f"Sum {plus}, difference {gap}"),
                ("Picture the two amounts lined up, with an extra piece on the larger one.", "Align the equal parts.")),
                ((f"Remove the extra {say(gap)} from the total. The remaining {say(plus-gap)} comprises two equal copies of the smaller number.", f"{plus} − {gap} = {2*y}"),
                 (f"So the smaller is {say(y)} and the larger is {say(x)}. Check both the sum and the difference.", f"{y}, {x}")), bars(("Small",((y,"same"),)),("Large",((y,"same"),(gap,gap))))),
            Example("Add two conditions to find a shared sum", (
                (f"Two notebooks and a ruler cost {say(one)} dollars. One notebook and two rulers cost {say(two)} dollars.", f"2N + R = {one}; N + 2R = {two}"),
                ("Find the price of one notebook plus one ruler, then recover each price.", "Find N + R, then N and R.")),
                ((f"Add the equations, giving three notebooks and three rulers for {say(one+two)} dollars.", f"3N + 3R = {one+two}"),
                 (f"Divide by three. One of each costs {say(a+b)} dollars. Subtract that from the price of two notebooks and a ruler.", f"N + R = {a+b}"),
                 (f"The notebook costs {say(a)}, leaving {say(b)} for the ruler. Both original prices work.", f"N = ${a}, R = ${b}")),table(("Bundle","N","R"),("First",2,1),("Second",1,2))),
            Example("Recover three unknowns from overlapping totals", (
                (f"Three boxes A, B and C contain counters. Boxes A and B together hold {say(ab)}. B and C hold {say(bc)}.", f"A + B = {ab}. B + C = {bc}."),
                (f"C and A hold {say(ca)}. Find how many counters are in each box.", f"C + A = {ca}. Find A, B and C.")),
                ((f"Add all three conditions. Each box appears twice, so the combined sum {say(2*total)} is twice the number of counters in the three boxes.", f"2(A+B+C) = {2*total}"),
                 (f"Halve it to get the complete total {say(total)}. Subtract a pair's total to find the missing box.", f"A + B + C = {total}"),
                 (f"Subtract B plus C to get A equals {say(a)}. The same method gives B equals {say(b)} and C equals {say(third)}.", f"A = {a}, B = {b}, C = {third}")),
                table(("Pair","Total"),("A + B",ab),("B + C",bc),("C + A",ca)),proof=(
                    (f"The resulting pairs total {say(ab)}, {say(bc)} and {say(ca)}. Each matches its clue.", f"Check {a}+{b}, {b}+{third}, {third}+{a}"),
                    ("The original clues forced the overall total and then each single box. There can be only one such assignment.", "The three pair totals determine the three boxes."))),
        ), tiles("A+B","B+C","C+A"),
    )


def differences(lesson):
    v=lesson.visit
    x,y=4+v,7+v
    a=x+2*y
    b=2*x+2*y
    s,t=2+v%2,3+v%2
    m1,m2=s*x+y,t*x+2*y
    # A different pair of coefficients for the harder example.
    r1,r2=3+v,5+v
    k1,k2=2,3
    full1=r1*x+k1*y
    full2=r2*x+k2*y
    coef=k1*r2-k2*r1
    if coef==0:
        r2+=1
        full2=r2*x+k2*y
        coef=k1*r2-k2*r1
    diff=k1*full2-k2*full1
    assert diff == coef*x and coef
    return linear_context(
        ("When two totals share the same contribution, subtracting them removes that contribution. The difference isolates the part that changed.", "Match one contribution, then subtract."),
        ("bundles with matching parts or clues about what extra objects cost", "cancel a common part"),
        ("Subtract totals with unequal hidden contributions", "Match the quantities first", "The other parts must match before they cancel. Scale an equation if the two numbers of matching objects differ."),
        ("Change a coefficient without changing the total", "Scale the whole equation", "Multiplying an equation scales every coefficient and the total on the other side by the same factor."),
        (
            Example("Cancel a matching pair of items", (
                (f"One bun and two drinks cost {say(a)} dollars. Two buns and two drinks cost {say(b)} dollars. Find the price of a bun.", f"B+2D={a}; 2B+2D={b}"),
                ("Compare what changed between the orders.", "What accounts for the difference in prices?")),
                ((f"The two drinks occur in both orders, so their total price cancels. Only one additional bun remains.", f"(2B+2D)−(B+2D) = B"),
                 (f"The price increase is {say(x)} dollars. That is the cost of one bun.", f"B = {b} − {a} = ${x}")), table(("Order","Buns","Drinks"),("1",1,2),("2",2,2))),
            Example("Scale a bundle to match one part", (
                (f"{say(s).capitalize()} pens and one marker cost {say(m1)} dollars. {say(t).capitalize()} pens and two markers cost {say(m2)} dollars.", f"{s}P + M = {m1}; {t}P + 2M = {m2}"),
                ("Find each price. Create two orders with the same number of markers first.", "Make both orders contain 2 markers.")),
                ((f"Double the first bundle to make {say(2*s)} pens and two markers costing {say(2*m1)}.", f"{2*s}P + 2M = {2*m1}"),
                 (f"Subtract the second bundle. This leaves {say(2*s-t)} {'pen' if 2*s-t==1 else 'pens'} worth {say(2*m1-m2)} dollars.", f"{2*s-t}P = {2*m1-m2}"),
                 (f"One pen costs {say(x)} dollars. Substitute into the first order to get {say(y)} dollars for a marker.", f"P = ${x}, M = ${y}")), table(("Bundle","P","M"),("First",s,1),("Second",t,2))),
            Example("Choose a matching coefficient from both orders", (
                (f"A stall sells two kinds of pack, X and Y. An order of {say(r1)} X packs and two Y packs costs {say(full1)} dollars.", f"{r1}X + 2Y = {full1}"),
                (f"An order of {say(r2)} X packs and three Y packs costs {say(full2)} dollars. Find each unit price.", f"{r2}X + 3Y = {full2}")),
                (("The smallest equal number of Y packs in the two scaled orders is six. Multiply the first entire equation by three and the second by two.", "Make both amounts of Y equal to 6."),
                 (f"Subtract the scaled first equation from the scaled second. That leaves {say(coef)} X {'pack' if coef==1 else 'packs'} worth {say(diff)} dollars.", f"({2*r2} − {3*r1})X = {2*full2} − {3*full1}"),
                 (f"Dividing gives {say(x)} dollars for X. Putting that into the first condition gives {say(y)} dollars for Y.", f"X = ${x}, Y = ${y}")),
                table(("Scaled","X","Y"),("First ×3",r1*3,6),("Second ×2",r2*2,6)),proof=(
                    (f"Rebuild both purchases. The first costs {say(full1)} and the second costs {say(full2)} dollars.", f"{r1}×{x}+2×{y}={full1}; {r2}×{x}+3×{y}={full2}"),
                    ("The difference equation had a nonzero coefficient for X. That forced its price before we substituted to find Y.", "Matching one term isolates the other."))),
        ), tiles("Same part","Subtract","Remainder"),
    )


def margins(lesson):
    v=lesson.visit
    second=18+v
    gap=6+v
    sum2=2*second+gap
    bottom=12+v
    g1,g2=3+v,5+v
    totals=3*bottom+2*g1+g2
    fair=25+3*v
    move_a,move_b=7+v,2+v
    x,y,z=fair+move_a,fair+move_b,fair-move_a-move_b
    a,b=x-y,y-z
    assert x+y+z==3*fair and x-move_a==y-move_b==z+move_a+move_b
    return linear_context(
        ("A margin is the difference between two scores. Use the smaller score as a base, then build the other scores by adding their margins.", "A higher score equals a base plus a gap."),
        ("shared totals with one score stated relative to another", "write every score from the same base"),
        ("Treat a margin as one score", "A margin is a difference", "A winning margin measures how far ahead the winner is. It is not either team's score."),
        ("Change the total when transferring points", "Transfers preserve the total", "When the same points move from one team to another, the shared total stays constant. Only its distribution changes."),
        (
            Example("Find both scores from the winning margin", (
                (f"Two teams score {say(sum2)} points in total. The winner leads by {say(gap)}. Find both scores.", f"Total {sum2}, winning margin {gap}"),
                ("Imagine removing the extra points the winner has above the losing score.", "Equalise the two scores.")),
                ((f"Subtract the {say(gap)} extra points. The remaining {say(2*second)} splits evenly between two equal parts.", f"{sum2} − {gap} = {2*second}"),
                 (f"The two scores are {say(second)} and {say(second+gap)}. Restore the original margin to check.", f"{second} and {second+gap}")), bars(("Lower",((second,"base"),)),("Higher",((second,"base"),(gap,gap))))),
            Example("Line up three scores by their differences", (
                (f"The middle score is {say(g1)} above the lowest. The highest is {say(g2)} above the middle. Together the scores total {say(totals)}.", f"Middle leads low by {g1}; high leads middle by {g2}."),
                ("Find the three scores. Take the lowest score as x.", f"Total {totals}. Write all three using x.")),
                ((f"The scores are x, x plus {say(g1)}, and x plus {say(g1+g2)}. The highest has both gaps above the lowest.", f"x, x+{g1}, x+{g1+g2}"),
                 (f"Subtract the extras from the total and divide by three. The lowest score is {say(bottom)}.", f"3x = {totals} − {2*g1+g2}"),
                 (f"Add the margins back in order, giving {say(bottom)}, {say(bottom+g1)} and {say(bottom+g1+g2)}.", f"{bottom}, {bottom+g1}, {bottom+g1+g2}")), chain("Low",f"+{g1}","Middle",f"+{g2}","High")),
            Example("Use margins and an unchanged shared total", (
                (f"Teams A, B and C share {say(3*fair)} points. A leads B by {say(a)}, and B leads C by {say(b)}.", f"Total {3*fair}. A−B={a}, B−C={b}."),
                ("Give points from A and B to C so all scores become equal. How many points must each higher team give?", "How much must A and B transfer to C?")),
                ((f"Write C as c. Then B equals c plus {say(b)}, and A equals c plus {say(a+b)}.", f"C=c, B=c+{b}, A=c+{a+b}"),
                 (f"Add the scores and subtract the extra amounts. This gives three c equal to {say(3*z)}, so C has {say(z)}.", f"3c = {3*fair} − {a+2*b} = {3*z}"),
                 (f"The original scores were {say(x)}, {say(y)} and {say(z)}. The equal score is {say(fair)}, one third of the fixed total.", f"Scores {x}, {y}, {z}; equal target {fair}")),
                bars(("C",((z,"base"),)),("B",((z,"base"),(b,b))),("A",((z,"base"),(a+b,a+b)))),proof=(
                    (f"A gives {say(move_a)} and B gives {say(move_b)}. Subtract these from the first two scores and add both to C.", f"A gives {move_a}; B gives {move_b}."),
                    (f"All scores then equal {say(fair)}. The total is still {say(3*fair)}, so this is the only possible equal score.", f"{x}−{move_a}={y}−{move_b}={z}+{move_a}+{move_b}={fair}"))),
        ), tiles("Base","Margin","Total"),
    )
