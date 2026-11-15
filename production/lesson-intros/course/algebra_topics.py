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
