"""Systematic enumeration and counting with overlapping or disjoint sets."""

from itertools import combinations, product
from math import comb, lcm

from story import Example, Topic, chain, say, spoken_list, table, tiles, venn


def enumeration(lesson):
    v=lesson.visit
    available=tuple(range(1+v,4+v))
    two_digits=[10*a+b for a,b in product(available,repeat=2) if a!=b]
    total=13+v
    cap=8+v//2
    pairs=[(a,total-a) for a in range(1,cap+1) if 1 <= total-a <= cap]
    goal=11+v
    limit=6+v%2
    rows=[]
    for a in range(2,limit+1,2):
        minimum=max(1,goal-a-limit)
        maximum=min(limit,goal-a-1)
        rows.append((a,minimum,maximum,max(0,maximum-minimum+1)))
    result=sum(row[3] for row in rows)
    assert result==sum(a+b+c==goal and a%2==0 for a,b,c in product(range(1,limit+1),repeat=3))
    return Topic(
        (("A complete list follows a rule you can explain. Fix one choice and list every possible ending before changing the first choice.", "Fix the first choice, then list the endings."),
         ("When a list gets long, record a range or a subtotal for each first choice. This keeps the reason that the list is complete.", "Use rows for the first choices.")),
        (("A late AMC counting question may hide a short list behind several conditions. Pick one condition that makes the list shrink quickly.", "AMC Upper Primary · choose an efficient first case"),
         ("In Mawa primary application practice, a complete list can be part of the answer. The published application questions ask students to explain their reasoning.", "MAWA-style · show why the list covers everything")),
        (
            Example("Make a short list in order", (
                (f"Use two different digits chosen from {spoken_list(available)}. List all the possible two-digit numbers in increasing order.", f"Available digits: {', '.join(map(str,available))}."),
                ("Think about which position decides the order first.", "List numbers by their tens digit.")),
                ((f"Start with tens digit {say(available[0])}. The other two digits are the only possible ones digits, so write those endings in order.", f"{two_digits[0]}, {two_digits[1]}"),
                 (f"Repeat with each remaining tens digit. The complete list is {spoken_list(two_digits)}.", f"{', '.join(map(str,two_digits))}")),tiles(*available),worked_art=table(("Tens","Numbers"),*((a,', '.join(str(n) for n in two_digits if n//10==a)) for a in available))),
            Example("Turn a pair condition into bounds", (
                (f"Two numbered counters A and B show whole numbers from one to {say(cap)}. Their values sum to {say(total)}.", f"Both values 1 to {cap}. Total {total}."),
                ("How many possible ordered pairs of readings are there? A and B are distinct counters.", "Count possible readings for A.")),
                ((f"B equals {say(total)} minus A. Since B is at most {say(cap)}, A must be at least {say(total-cap)}.", f"B = {total} − A; A ≥ {total-cap}."),
                 (f"The cap on A is {say(cap)}. Every integer in that inclusive range gives one legal B, for {say(len(pairs))} pairs.", f"A from {pairs[0][0]} through {pairs[-1][0]}: {len(pairs)} pairs.")),
                table(("A","B"),("?","?")),worked_art=table(("A","B"),*pairs)),
            Example("Enumerate an ordered triple with a parity rule", (
                (f"Three labelled boxes A, B and C contain a total of {say(goal)} tokens. Each holds between one and {say(limit)} tokens inclusive. A holds an even number.", f"A+B+C = {goal}; each 1–{limit}; A even."),
                ("Count the different ordered triples of box sizes. The boxes keep their labels.", "How many triples (A, B, C)?")),
                ((f"The possible values for A are {spoken_list([row[0] for row in rows])}. Make a row for each one.", f"Rows for A = {', '.join(str(row[0]) for row in rows)}."),
                 (f"In each row B plus C is {say(goal)} minus A. Requiring C to be at most {say(limit)} gives a lower bound on B.", f"B ≥ {goal} − A − {limit}; also B ≥ 1."),
                 (f"Requiring C to be positive gives the upper bound. Use the cap of {say(limit)} on B as well, then count the range inclusively.", f"B ≤ {goal} − A − 1; also B ≤ {limit}.")),
                tiles("A","B","C"),worked_art=table(("A","B min","B max","Count"),*rows),proof=(
                    (f"The row counts are {spoken_list([r[3] for r in rows])}, so there are {say(result)} triples altogether.", f"{' + '.join(str(r[3]) for r in rows)} = {result}."),
                    ("Each legal triple has exactly one value for A. Within that row a legal B fixes C, so every triple is covered exactly once.", "One row and one entry per legal triple."))),
        ),
        (("An inclusive range includes both endpoints. Subtract first from last and then add one, provided the range is nonempty.", "Count last minus first", "For a nonempty range, add one"),
         ("When the boxes are labelled, swapping two different readings changes the triple. Retain the positions while you count.", "Sort every triple before counting", "Keep the order the question specifies")),
        (("Find a first choice whose legal values fit in a short list. Label the rows with those values.", "Fix a useful first choice", "Every solution belongs to a row."),
         ("Write why each row covers its legal endings. Check both endpoints and add the disjoint row totals.", "Justify the bounds", "End with a count for the stated question.")),
        cover=chain("A","B","C"),
    )


def selections(lesson):
    v=lesson.visit
    flavours, toppings=3+v,2+v%3
    names=5+v
    a,b,c=4+v,3+v%3,3+v%2
    ways=(comb(a,2)*comb(b,2),comb(a,2)*b*c,comb(a,3)*b,comb(a,3)*c)
    total=sum(ways)
    assert total==sum(
        sum(x<a for x in team) in (2,3) and sum(x>=a+b for x in team)<=1
        for team in combinations(range(a+b+c),4)
    )
    assert comb(names,2)==len(list(combinations(range(names),2)))
    return Topic(
        (("For a recipe with several separate choices, multiply the numbers of choices when every choice in one stage can go with every choice in the next.", "Multiply compatible choices."),
         ("For a team the order of selection usually does not matter. Use a list or divide out the orders that describe the same team.", "Decide whether order matters.")),
        (("AMC Upper Primary practice may ask how many designs or teams can be made. Look for distinct stages of choice, then ask what makes a final outcome different.", "AMC Upper Primary · identify one outcome"),
         ("A Rossmoyne style challenge can restrict the number chosen from each group. Split by group totals before multiplying.", "Rossmoyne-style · count each group pattern")),
        (
            Example("Choose a flavour and a topping", (
                (f"A stall has {say(flavours)} flavours and {say(toppings)} toppings. You order one of each, and every pairing is allowed.", f"{flavours} flavours and {toppings} toppings."),
                ("How many different flavour-and-topping orders are possible?", "Choose one from each group.")),
                ((f"For each flavour there are {say(toppings)} different toppings. Listing one row per flavour creates equal row lengths.", f"{toppings} choices per row"),
                 (f"Multiply by the {say(flavours)} flavours, giving {say(flavours*toppings)} combinations. Each order has one flavour and one topping.", f"{flavours} × {toppings} = {flavours*toppings}.")),chain(f"{flavours} flavours",f"{toppings} toppings")),
            Example("Choose a pair without caring about order", (
                (f"Pick an unlabelled pair of helpers from {say(names)} students. The two students have the same job and no student can be chosen twice.", f"Choose 2 of {names} for the same job."),
                ("How many different pairs are possible?", "Count pairs independently of selection order.")),
                ((f"Count an ordered first and second pick. There are {say(names)} first choices and {say(names-1)} second choices after each one.", f"{names} × {names-1} = {names*(names-1)} ordered pairs."),
                 (f"Every team appears in two orders. Halve the ordered count to get {say(comb(names,2))} teams.", f"{names*(names-1)} ÷ 2 = {comb(names,2)}.")),tiles("A then B","B then A",highlight=(0,1))),
            Example("Choose a team across three groups", (
                (f"There are {say(a)} artists, {say(b)} builders and {say(c)} coders. Choose four people with either two or three artists and at most one coder.", f"Choose 4. Artists: {a}, builders: {b}, coders: {c}."),
                ("People belong to one group each, and the team has no named roles. How many different teams are possible?", "Use 2 or 3 artists and at most 1 coder.")),
                ((f"With two artists, the other two can be two builders or one builder and one coder. There are {say(comb(a,2))} artist pairs in either case.", f"(2,2,0) or (2,1,1); artists have {comb(a,2)} choices."),
                 (f"With three artists, the fourth can be a builder or a coder. There are {say(comb(a,3))} ways to choose the three artists.", f"(3,1,0) or (3,0,1); artists have {comb(a,3)} choices."),
                 ("Within one row, multiply the choices from different groups. Between rows, add, because each team fits exactly one group pattern.", "Multiply within each row; add the four row totals.")),
                tiles(f"{a} artists",f"{b} builders",f"{c} coders"),worked_art=table(("Artists","Builders","Coders","Teams"),
                   *[(x,y,z,w) for (x,y,z),w in zip(((2,2,0),(2,1,1),(3,1,0),(3,0,1)),ways)]),
                proof=((f"The four row totals are {spoken_list(ways)}. Their sum is {say(total)} teams.", f"{' + '.join(map(str,ways))} = {total} teams."),
                       ("Check that selecting zero coders was allowed, and that you used both allowed artist totals. Those choices account for all four patterns.", "Both artist totals and both coder totals included."))),
        ),
        (("Switching two people on a team without named jobs leaves the same team. Count both orders only when the roles differ.", "Treat choose two as first and second", "Divide by the number of orders per pair"),
         ("You can multiply choices that make up one outcome. Distinct allowable patterns for a whole team are alternatives, so add them.", "Multiply the totals for different cases", "Add totals for disjoint cases")),
        (("Decide whether the objects have named positions. Write a short group pattern before calculating individual choices.", "Identify the final object", "A committee is a set; a lineup is ordered."),
         ("Multiply the compatible choices within a pattern. Then add the pattern totals after checking each team can fit only one.", "Count by group pattern", "Check for missing and repeated outcomes.")),
        cover=chain("Choose","Pair","Count"),
    )


def complement(lesson):
    v=lesson.visit
    length=4+v
    left,right,overlap=11+v,9+v,4+v%3
    n=(84,108,126,145,160,198)[v]
    start=1 if v<3 else 12+v
    a,b,c=(2,3,5) if v%2==0 else (3,4,7)
    count=lambda k:n//k-(start-1)//k
    singles=[count(k) for k in (a,b,c)]
    pairs=[count(lcm(x,y)) for x,y in ((a,b),(a,c),(b,c))]
    triple=count(lcm(a,b,c))
    union=sum(singles)-sum(pairs)+triple
    answer=n-start+1-union
    assert answer==sum(all(x%k for k in (a,b,c)) for x in range(start,n+1))
    return Topic(
        (("The complement of an event is everything outside it. When that opposite set is simpler, count it and subtract from the whole.", "Wanted = whole set minus unwanted."),
         ("When an item satisfies two rules, the two rule totals overlap. Correct those overlaps before subtracting the union.", "Correct overlaps before subtracting.")),
        (("AMC practice can ask for at least one or for none. Those conditions are opposites inside the same sample space.", "AMC Upper Primary · often count the opposite"),
         ("A Mawa style extension may combine several rules for the same number. Show how many times a number is counted when it obeys more than one rule.", "MAWA-style · account for every overlap")),
        (
            Example("Count strings with at least one T", (
                (f"Write a string of {say(length)} letters. Each position can be H or T. How many strings have at least one T?", f"{length} positions; each H or T."),
                ("Consider how many strings have no T anywhere.", "Which strings are excluded?")),
                ((f"Every position has two choices. There are {say(2**length)} possible strings before the condition.", f"2 to the power {length} = {2**length}."),
                 (f"Only the all-H string has no T. Subtract it to leave {say(2**length-1)} strings with at least one T.", f"{2**length} − 1 = {2**length-1}.")),tiles(*(["H/T"]*length))),
            Example("Include two groups and correct their overlap", (
                (f"In a class, {say(left)} students play tennis, {say(right)} swim and {say(overlap)} do both. How many do at least one?", f"Tennis {left}; swimming {right}; both {overlap}."),
                ("Someone in both activities still counts as a single student.", "Find the total in either circle.")),
                ((f"Adding the two activity totals gives {say(left+right)}. It includes each of the {say(overlap)} shared students twice.", f"{left} + {right} = {left+right}, including two copies of the overlap."),
                 (f"Remove one copy of the overlap. There are {say(left+right-overlap)} students who do at least one of the activities.", f"{left} + {right} − {overlap} = {left+right-overlap}.")),
                 venn("?","?",overlap),worked_art=venn(left-overlap,right-overlap,overlap)),
            Example("Count numbers that avoid three divisibility tests", (
                (f"Consider integers from {say(start)} through {say(n)}, inclusive. How many are divisible by none of {spoken_list((a,b,c))}?", f"{start}–{n} inclusive. Avoid multiples of {a}, {b}, {c}."),
                ("Count the union of the three unwanted lists first.", "Exclude every number divisible by at least one.")),
                ((f"Count each individual list by the multiples up to {say(n)} minus the multiples below the start. The three counts are {spoken_list(singles)}.", f"Single-rule counts: {', '.join(map(str,singles))}."),
                 (f"A shared number is a multiple of the least common multiple for that pair. Subtract the pair counts {spoken_list(pairs)} to correct double counting.", f"Pair counts: {', '.join(map(str,pairs))}."),
                 (f"A triple match has been added three times and removed three times. Add the {say(triple)} triple matches back so that they contribute once.", f"Triple overlap = {triple}.")),
                tiles(f"×{a}",f"×{b}",f"×{c}"),proof=(
                    (f"There are {say(union)} excluded integers after the overlap corrections. The whole inclusive range contains {say(n-start+1)} integers.", f"Excluded = {sum(singles)} − {sum(pairs)} + {triple} = {union}."),
                    (f"Subtract the excluded count once from the whole range, leaving {say(answer)} integers.", f"{n-start+1} − {union} = {answer}.")),
                proof_art=table(("Contribution","Count"),("Singles",sum(singles)),("Pairs",sum(pairs)),("Triple",triple))),
        ),
        (("The opposite of at least one is zero. Exactly one can leave out outcomes where two or more rules are true.", "Treat at least one as exactly one", "Include every allowed positive number of matches"),
         ("Three-way overlap belongs to all three pair intersections. Add it back after subtracting those intersections.", "Stop after removing pair overlaps", "Add back the triple matches")),
        (("Define the whole set using the bounds in the question. Write the exact complementary condition.", "Write the opposite event", "Use the same universe on both sides."),
         ("If the excluded rules overlap, correct the union first. Then subtract it once and check that the result is between zero and the total.", "Correct the overlaps", "Finish with the requested count.")),
        cover=venn("A","B","Both"),
    )


def double_counting(lesson):
    v=lesson.visit
    people=5+v
    rooms=6+v
    assigned=8+2*v
    shifts=3+v%2
    volunteers=rooms*assigned//shifts
    if volunteers*shifts!=rooms*assigned:
        assigned=6*shifts
        volunteers=rooms*assigned//shifts
    assert volunteers*shifts==rooms*assigned
    players=10+2*v
    untouched=3+v
    # Cancel disjoint pairs from a complete schedule to make a feasible degree pattern.
    missed=players-untouched
    if missed%2:
        untouched+=1
        missed-=1
    blocked={(i,i+1) for i in range(0,missed,2)}
    games=[e for e in combinations(range(players),2) if e not in blocked]
    degree_sum=untouched*(players-1)+missed*(players-2)
    assert 2*len(games)==degree_sum
    return Topic(
        (("A double-counting argument counts the same thing from two viewpoints. Both totals must describe the same physical objects or links.", "Count one set in two ways."),
         ("If every link is reported by its two endpoints, the endpoint total is twice the number of links.", "One link gives two endpoint reports.")),
        (("AMC Upper Primary practice can use handshakes or matches. Draw one pair to see how many times it appears when people report their own totals.", "AMC Upper Primary · use each link once"),
         ("In a Mawa style counting argument, name exactly what the two calculations count. A participant-room booking differs from an individual participant.", "MAWA-style · name the shared object")),
        (
            Example("Count greetings from the people involved", (
                (f"{say(people).capitalize()} students each shake hands with every other student once. How many handshakes take place?", f"{people} students, one handshake per pair."),
                ("Imagine asking each student how many handshakes they took part in.", "Count all the reports first.")),
                ((f"Each student reports {say(people-1)} handshakes. The reports add to {say(people*(people-1))}.", f"{people} × {people-1} = {people*(people-1)} reports."),
                 (f"A handshake is reported by both students in the pair. Divide by two to find {say(comb(people,2))} different handshakes.", f"{people*(people-1)} ÷ 2 = {comb(people,2)}.")),chain("Person A","One greeting","Person B")),
            Example("Count the same bookings by room and by helper", (
                (f"At a festival, each of {say(rooms)} rooms schedules {say(assigned)} different helpers. Each helper has a booking in exactly {say(shifts)} distinct rooms.", f"{rooms} rooms × {assigned} bookings, {shifts} per helper."),
                ("Find the total number of helpers. A booking is one helper assigned to one room.", "Two ways to count helper-room bookings.")),
                ((f"By rooms there are {say(rooms*assigned)} total bookings. Counting by helpers gives {say(shifts)} bookings for every helper.", f"Bookings = {rooms} × {assigned} = {rooms*assigned}."),
                 (f"Divide the booking total by {say(shifts)}. This gives {say(volunteers)} individual helpers.", f"{rooms*assigned} ÷ {shifts} = {volunteers} helpers.")),table(("By room","By helper"),(f"{assigned} each",f"{shifts} each"))),
            Example("Recover the number of matches from unequal totals", (
                (f"In a tournament of {say(players)} players each pair can play at most once. Exactly {say(untouched)} players each play against everyone else.", f"{players} players; {untouched} meet everybody."),
                (f"Each of the other {say(missed)} players misses exactly one opponent. How many matches are played?", f"{missed} players miss one opponent each.")),
                ((f"The first group each reports {say(players-1)} matches, and the second group each reports {say(players-2)} matches.", f"Reports = {untouched} × {players-1} + {missed} × {players-2}."),
                 (f"The reports add to {say(degree_sum)}. Each played match has two players, so the actual count is {say(len(games))}.", f"{degree_sum} ÷ 2 = {len(games)} matches.")),
                table(("Players","Matches each"),(untouched,players-1),(missed,players-2)),proof=(
                    (f"Check from the full schedule of {say(comb(players,2))} matches. The {say(missed)} missed-opponent reports come in pairs, giving {say(len(blocked))} matches that fell through.", f"Missing matches = {missed} ÷ 2 = {len(blocked)}."),
                    (f"The difference is {say(len(games))}, agreeing with the endpoint count.", f"{comb(players,2)} − {len(blocked)} = {len(games)}."))),
        ),
        (("In a two-person match, each report identifies one endpoint. A total of personal match counts records twice as many entries as actual matches.", "Report personal totals as match totals", "Divide by the actual reporting multiplicity"),
         ("Room bookings and helpers are different units. Read whether the question asks for assignments or the number of people who hold those assignments.", "Equate bookings with people", "Keep track of the unit both ways")),
        (("Write what one object is, such as a match or a helper-room booking. Then write down each viewpoint.", "Name the object being counted", "Draw one example if the multiplicity is unclear."),
         ("Work out how many times your calculation reports one object. Use that ratio to put the answer in the units requested.", "Find the reporting multiplicity", "Check the result using the other viewpoint.")),
        cover=chain("Endpoint","One link","Endpoint"),
    )


def partition_cases(lesson):
    v=lesson.visit
    lo,hi=19+v,28+2*v
    evens=[n for n in range(lo,hi+1) if n%2==0]
    reds, blues=4+v,5+v
    teams=5+v
    other=4+v%2
    all_red=3*(teams-2)*(teams-3)
    red_ends=2*(teams-1)*other
    centre=other*(other-1)
    result=all_red+red_ends+centre
    # Let A occupy one of the two outside rooms or the middle room.
    blue=set(range(teams,teams+other))
    candidates=set(range(teams+other))
    assert result==sum(
        0 in line and (
            (line[1] in blue and line[0]<teams and line[2]<teams)
            or (line[1] not in blue and
                ((all(x<teams for x in line) and 1 not in line) or (line[1]==0 and line[0] in blue and line[2] in blue)))
        )
        for line in product(candidates,repeat=3)
        if len(set(line))==3
    )
    return Topic(
        (("A partition splits a set into cases that do not overlap. Each allowed outcome must belong in exactly one of your cases.", "Every outcome goes in exactly one case."),
         ("Look for a choice with natural alternatives, such as a first digit, a position, or whether a specific object is used.", "Split by a definite feature.")),
        (("A late AMC problem can hide several different arrangements in one question. A short case table turns them into smaller counts.", "AMC Upper Primary · count a short list of cases"),
         ("A Rossmoyne style solution may require you to justify why every possibility is covered. State a rule that forces each candidate into one row.", "Rossmoyne-style · justify case coverage")),
        (
            Example("Separate odd and even numbers", (
                (f"Consider consecutive integers from {say(lo)} to {say(hi)}, including both ends. How many are odd and how many are even?", f"Numbers from {lo} to {hi} inclusive."),
                ("Start each list with the first eligible number. Go up by two.", "Use two disjoint parity cases.")),
                ((f"The even list has {say(len(evens))} entries. Every even number differs from the previous even number by two.", f"Even: {evens[0]}, {evens[1]}, …, {evens[-1]}."),
                 (f"The whole list contains {say(hi-lo+1)} numbers. The rest are odd, giving {say(hi-lo+1-len(evens))} odd numbers.", f"{hi-lo+1} − {len(evens)} = {hi-lo+1-len(evens)} odd.")),tiles("Even","Odd")),
            Example("Use exactly one of two named choices", (
                (f"Choose one of {say(reds)} red badges and one of {say(blues)} blue badges. Each colour has a single star badge.", f"{reds} red, {blues} blue; 1 star in each colour."),
                ("How many pairs contain exactly one star badge?", "Exactly one star can be red or blue.")),
                ((f"If the star is red, the blue badge has {say(blues-1)} plain choices. If the star is blue, there are {say(reds-1)} plain red choices.", f"Red star: {blues-1}. Blue star: {reds-1}."),
                 (f"The two cases cannot describe the same pair. Add to get {say(blues+reds-2)} choices.", f"{blues-1} + {reds-1} = {blues+reds-2}.")),table(("Only red is star","Only blue is star"),(blues-1,reds-1))),
            Example("Choose three distinct exhibits for labelled rooms", (
                (f"There are {say(teams)} red exhibits, including A and B, and {say(other)} blue exhibits. Three distinct exhibits fill left, middle and right rooms. A must be used.", f"Place 3 distinct exhibits. A must appear."),
                ("You may use three reds with B excluded, or a blue in the middle and one red on either end. A third option is A in the middle between two blues. Count arrangements.", "Legal patterns: RRR without B, RBR, or blue–A–blue.")),
                ((f"With three reds, A has three room choices. The other two reds come in order from the {say(teams-2)} remaining eligible reds.", f"RRR without B: 3 × {teams-2} × {teams-3}."),
                 (f"With a blue in the middle and red ends, A can go at either end. Choose any other red, including B, and any blue.", f"RBR: 2 × {teams-1} × {other}."),
                 (f"With A in the middle and two blues, there are {say(other)} choices for the left and {say(other-1)} for the right. The three colour patterns are different.", f"Blue–A–blue: {other} × {other-1}.")),
                tiles("Left","Middle","Right"),proof=(
                    (f"The three row totals are {spoken_list((all_red,red_ends,centre))}. Add them to get {say(result)} arrangements.", f"Total = {result}."),
                    ("Check the rule about B applies to the all-red case only. Read each row against the conditions for its exact colour pattern.", "Check each restriction in its own case."))),
        ),
        (("At least one and exactly one accept different outcomes. If each group supplies a star, both-star pairs are excluded when the rule says exactly one.", "Keep both stars in an exactly-one case", "Read the quantifier before counting"),
         ("Cases that overlap can count one outcome twice. Name the property that distinguishes a row from every other row.", "Label cases by overlapping conditions", "Use a unique property such as a fixed pattern")),
        (("Write a clean split before counting. Check that an arbitrary valid arrangement has a home in your table.", "Prove every outcome has a row", "Separate the cases by a definite feature."),
         ("Confirm that no outcome has two homes, calculate each row, and add the subtotals. Read the final question for its required units.", "Prove rows are disjoint", "Finish with the exact total requested.")),
        cover=tiles("Case 1","Case 2","Case 3"),
    )
