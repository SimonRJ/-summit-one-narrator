"""Positional thinking and counting written digits on later course visits."""

from itertools import permutations

from story import Example, Topic, bars, chain, say, spoken_list, table, tiles


def digit_sums(lesson):
    v=lesson.visit
    n=375+11*v
    digits=tuple(map(int,str(n)))
    remainder=sum(digits)%9
    assert remainder==n%9
    digit=2+v
    end=100*digit+16+13*v if v in (2,4) else 226+21*v
    places=[]
    for place in (1,10,100):
        cycles,low=divmod(end+1,10*place)
        tail=max(0,min(place,low-digit*place))
        places.append(cycles*place+tail)
    assert sum(places)==sum(str(x).count(str(digit)) for x in range(1,end+1))
    hundreds=4+v%5
    tail_bonus=int(1<=9-digit<=hundreds)
    per_end=hundreds+tail_bonus
    hundred_count=((100*digit+99)//9-(100*digit-1)//9) if digit<=hundreds else 0
    last=hundreds*100+99
    answer=2*per_end+hundred_count
    assert answer==sum(str(x).count(str(digit)) for x in range(100,last+1) if x%9==0)
    bonus=(f"Here the hundreds digit {say(9-digit)} gives that double choice." if tail_bonus
           else "None of the allowed hundreds digits gives that double choice.")
    hundred_work=(f"The hundred block starting at {say(100*digit)} contributes {say(hundred_count)} occurrences, one for every multiple of nine in that block."
                  if hundred_count else f"The digit {say(digit)} never appears as a hundreds digit in the requested range.")
    return Topic(
        (("A digit has a value and a position. The digit sum forgets the positions, but a count of written digits must consider every position.", "Digit sum and digit frequency answer different questions."),
         ("Break a range count into the ones, tens and hundreds places, then add those separate counts.", "Count appearances one place at a time.")),
        (("The AMC can ask how often a digit is written. Work in complete blocks, then inspect the last incomplete block.", "AMC Upper Primary · use complete and partial blocks"),
         ("In Mawa primary application practice, digit sum restrictions can be combined with range restrictions. Use place value to prove which cases count.", "MAWA-style · work from the digit conditions")),
        (
            Example("Use a digit sum to find a remainder", (
                (f"What remainder does {say(n)} leave after division by nine? Use its digits to find the remainder without long division.", f"Remainder when {n} is divided by 9."),
                ("Ten and one hundred both leave remainder one when divided by nine.", "Replace each place value by its remainder.")),
                ((f"One hundred, ten and one each contribute the same remainder as one. The digit sum is {say(digits[0])} plus {say(digits[1])} plus {say(digits[2])}, which is {say(sum(digits))}.", f"{digits[0]} + {digits[1]} + {digits[2]} = {sum(digits)}."),
                 (f"The remainder of that sum is {say(remainder)}, which is also the remainder of {say(n)}.", f"{n} and {sum(digits)} both leave remainder {remainder}.")),tiles(*digits)),
            Example("Count occurrences in a list of consecutive numbers", (
                (f"Write every whole number from one through {say(end)}. How many times do you write the digit {say(digit)}? Each occurrence counts separately.", f"Write 1–{end}. Count each written {digit}."),
                ("Track the ones, tens and hundreds separately.", "Use one table row for each place.")),
                ((f"In the ones place every complete block of ten contributes one occurrence, with a possible extra at the end. The ones total is {say(places[0])}.", f"Ones: {places[0]}."),
                 (f"In the tens place, each complete hundred contains one run of ten occurrences. Include any matching part of the last hundred. That gives {say(places[1])}. In the hundreds place, only the block starting at {say(100*digit)} could match. It contributes {say(places[2])}.", f"Tens: {places[1]}; hundreds: {places[2]}."),
                 (f"Adding the three totals gives {say(sum(places))} written occurrences.", f"{' + '.join(map(str,places))} = {sum(places)}.")),
                table(("Place","Block size"),("Ones",10),("Tens",100),("Hundreds",1000)),
                worked_art=table(("Place","Matches"),("Ones",places[0]),("Tens",places[1]),("Hundreds",places[2]))),
            Example("Count a digit while writing only multiples of nine", (
                (f"Write the multiples of nine from one hundred through {say(last)}, including any endpoint that is a multiple. Count every written {say(digit)}.", f"Multiples of 9 only, from 100 through {last}. Count all {digit}s."),
                ("Split the appearances among the three places. A number can contribute in more than one place.", "Count written appearances, including repeats.")),
                ((f"Fix the ones digit at {say(digit)}. For each hundreds digit, choose a tens digit so the three digits add to a multiple of nine.", f"Ones fixed: h + t + {digit} must be divisible by 9."),
                 (f"Each required remainder for the tens digit gives one choice, except remainder zero gives zero and nine. {bonus}", f"{hundreds} ordinary choices and {tail_bonus} extra."),
                 (f"The tens count is the same, since swapping the two end digits preserves the digit sum and the hundreds range. Each of these places contributes {say(per_end)}.", f"Ones {per_end}; tens {per_end}.")),
                table(("Hundreds","Tens","Ones"),("h","t",digit),("h",digit,"t")),proof=(
                    (f"For the hundreds place, fix the hundreds digit instead. {hundred_work}", f"Hundreds contribution: {hundred_count}."),
                    (f"Add the three position counts. An occurrence in one position is different from an occurrence in another, even in the same number. The total is {say(answer)}.", f"{per_end} + {per_end} + {hundred_count} = {answer}.")),
                proof_art=table(("Position","Occurrences"),("Ones",per_end),("Tens",per_end),("Hundreds",hundred_count))),
        ),
        (("If a number contains the requested digit twice, it contributes two occurrences. Compare counting numbers with counting written digits.", "Count at most once per number", "Count every matching position"),
         ("Digits zero and nine both have remainder zero on division by nine. Include both when zero is permitted in the position.", "Use only zero for a zero remainder", "Consider nine as a second digit with that remainder")),
        (("Write whether you need a sum, a number of valid integers or a count of written occurrences. Record the exact range.", "Identify what is being counted", "Track the ones, tens and hundreds separately."),
         ("Use place-value blocks or digit-sum restrictions to organise the work. Check an endpoint and a number with a repeated digit before totalling.", "Check boundaries and repeats", "Each legal occurrence contributes once.")),
        cover=tiles(100,10,1),
    )


def place_value(lesson):
    v=lesson.visit
    a=4+v
    b=75+3*v
    product=(100-a)*b
    gap=6+2*v
    left=100+gap
    med=left*(100-gap)
    m=1000+v
    far,near=8+v,2+v
    p=(m-far)*(m+far)
    q=(m-near)*(m+near)
    assert q-p==far**2-near**2
    return Topic(
        (("Place value lets you split an awkward number into a friendly part and a small correction. Pick a nearby ten, hundred or thousand.", "Use a friendly anchor and keep the correction."),
         ("An estimate checks size. Keep the correction algebra if the question needs an exact value or comparison.", "Use the correction to make the estimate exact.")),
        (("AMC Upper Primary often rewards enough estimation to reject an option. For close options, compare the corrections exactly.", "AMC Upper Primary · estimate first, then distinguish close values"),
         ("A Rossmoyne style problem may use two large products. If the products share a useful midpoint, compare only the parts that differ.", "Rossmoyne-style · expose a shared part")),
        (
            Example("Multiply by a number just below one hundred", (
                (f"Find {say(100-a)} times {say(b)} without long multiplication. The first factor is {say(a)} below one hundred.", f"{100-a} × {b} = (100 − {a}) × {b}."),
                ("Begin with a product you can read from place value.", "Multiply by 100, then compensate.")),
                ((f"One hundred times {say(b)} is {say(100*b)}. The extra {say(a)} copies of {say(b)} total {say(a*b)}.", f"Anchor = {100*b}; extra = {a} × {b} = {a*b}."),
                 (f"Subtract the extra copies. The exact result is {say(product)}.", f"{100*b} − {a*b} = {product}.")),bars(("100 copies",((100-a,str(100-a)),(a,"extra"))))),
            Example("Multiply numbers equally far above and below one hundred", (
                (f"Find {say(left)} times {say(100-gap)}. Both factors are the same distance from one hundred.", f"{left} × {100-gap} = (100 + {gap})(100 − {gap})."),
                ("Watch what happens to the two equal cross products.", "Expand around the shared midpoint.")),
                ((f"Multiply one hundred by one hundred. The cross terms are a gain and a loss of {say(100*gap)}, so they cancel.", f"10,000 + {100*gap} − {100*gap} − {gap}²."),
                 (f"The small product is minus {say(gap**2)} because one correction is negative. The exact result is {say(med)}.", f"10,000 − {gap**2} = {med}.")),tiles("100 + d","100 − d")),
            Example("Compare two close products without full multiplication", (
                (f"Which is larger, {say(m-far)} times {say(m+far)}, or {say(m-near)} times {say(m+near)}? Find how much larger it is.", f"A = {m-far} × {m+far}; B = {m-near} × {m+near}."),
                ("Look for the same midpoint hiding in both factor pairs.", "Find the difference between the products.")),
                ((f"Both pairs have midpoint {say(m)}. In A the offsets are plus and minus {say(far)}, while B uses plus and minus {say(near)}.", f"A: ({m}−{far})({m}+{far}); B: ({m}−{near})({m}+{near})."),
                 (f"For each product the cross terms cancel. It is the square of the midpoint minus the square of its offset.", "Product = midpoint² − offset²."),
                 (f"B loses only {say(near**2)}, while A loses {say(far**2)} from the same starting number. B is larger by {say(q-p)}.", f"B − A = {far}² − {near}² = {q-p}.")),
                table(("Pair","Midpoint","Offset"),("A",m,far),("B",m,near)),proof=(
                    ("The nearer pair is more balanced, so it removes the smaller square. The result works for any two factor pairs with the same midpoint.", "Same midpoint means a smaller offset gives a bigger product."),
                    ("When the midpoints differ, the starting squares can differ as well. Check that the anchor is shared before using the shortcut.", "Check that the two pair sums match.")),
                proof_art=table(("Product","Exact form"),("A",f"{m}² − {far**2}"),("B",f"{m}² − {near**2}"))),
        ),
        (("If a number is below its anchor, the correction is a subtraction. Check the sign by deciding whether the rounded product is too high or too low.", "Always add the correction", "Record whether the anchor overestimates"),
         ("Two cross terms cancel only when they have equal magnitude and opposite signs. Check the offsets around the midpoint.", "Cancel unmatched terms", "Choose a shared midpoint with equal offsets")),
        (("Choose a nearby round number. Write the original factors as exact sums or differences and estimate the expected size.", "Choose a useful anchor", "Use the estimate as a check."),
         ("Compare the small corrections directly if the large part cancels. If the question asks by how much, give the exact difference.", "Find what changes", "Use exact arithmetic for close comparisons.")),
        cover=chain("Anchor","Correction","Exact value"),
    )


def digit_positions(lesson):
    v=lesson.visit
    digits=(0,1,2,3,4,5+v)
    basic_digits=(0,v+1,v+5)
    basic=[n for n in permutations(basic_digits) if n[0]]
    evens=[x for x in digits if x and x%2==0]
    nonzero=len(digits)-1
    two_places=(len(digits)-2)*(len(digits)-3)
    zero_ways=nonzero*two_places
    other_ways=len(evens)*(nonzero-1)*two_places
    medium=zero_ways+other_ways
    assert medium==sum(a!=0 and d%2==0 for a,b,c,d in permutations(digits,4))
    cap=3+v
    allowed={digit for digit in digits if 0<digit<cap}
    endings=[(c,d) for c,d in permutations(digits,2) if (10*c+d)%4==0]
    cases={}
    per_hundreds=len(digits)-3
    for c,d in endings:
        used=len({c,d}&allowed)
        cases[used]=cases.get(used,0)+1
    answer=sum(amount*(len(allowed)-used)*per_hundreds for used,amount in cases.items())
    assert answer==sum(0<a<cap and (10*c+d)%4==0 for a,b,c,d in permutations(digits,4))
    text_end=", ".join(f"{a}{b}" for a,b in endings)
    case_rows=sorted(cases.items())
    return Topic(
        (("The places in a number have different rules. A leading zero cannot start a four-digit number, but zero can appear in any of the other positions if allowed.", "The leading digit must be nonzero."),
         ("If the question restricts the last digit or last two digits, fill those first and keep track of what remains.", "Place the restricted suffix before the other digits.")),
        (("An AMC digit puzzle may put one condition on the size and another on divisibility. These conditions usually restrict different positions.", "AMC Upper Primary · separate size and suffix rules"),
         ("In Mawa primary practice, use an ordered list of cases and explain why no valid leading digit or ending was lost.", "MAWA-style · account for zero and repeated digits")),
        (
            Example("Place zero in a genuine three-digit number", (
                (f"Use each of the digits {spoken_list(basic_digits)} exactly once. How many three-digit numbers can be made?", f"Use {', '.join(map(str,basic_digits))} once each."),
                ("Start with the hundreds place, which cannot be zero.", "How many legal first digits are there?")),
                (("There are two nonzero choices for the hundreds digit. Either choice leaves zero and one other digit.", "2 legal hundreds choices."),
                 ("The last two digits can go in either order, so two times two gives four genuine three-digit numbers.", "2 × 2 = 4 numbers.")),
                tiles("Hundreds","Tens","Ones"),worked_art=table(("First","Numbers"),*((a,', '.join(''.join(map(str,t)) for t in basic if t[0]==a)) for a in basic_digits[1:]))),
            Example("Count even four-digit numbers with distinct digits", (
                (f"Use four different digits from {spoken_list(digits)} to make a four-digit even number. How many can you make?", f"Digits {', '.join(map(str,digits))}; select 4 distinct."),
                ("The last digit must be even. Separate zero from the other even endings because it affects the first position.", "Count ending zero and ending nonzero even separately.")),
                ((f"Ending in zero leaves {say(nonzero)} choices to start. The middle two digits have {say(two_places)} ordered choices after the first and last are taken.", f"End 0: {nonzero} × {two_places} = {zero_ways}."),
                 (f"In each other even ending, zero is unused but still cannot start. There are {say(nonzero-1)} valid first digits and the same middle choices.", f"Nonzero even endings: {len(evens)} × {nonzero-1} × {two_places} = {other_ways}."),
                 (f"Add the two cases to get {say(medium)} different even numbers.", f"{zero_ways} + {other_ways} = {medium}.")),
                tiles(*digits),worked_art=table(("Final digit","Leading choices"),(0,nonzero),("Nonzero even",nonzero-1))),
            Example("Use the last-two-digit test and a first-digit bound", (
                (f"Choose four different digits from {spoken_list(digits)}.", f"Allowed digits: {', '.join(map(str,digits))}."),
                (f"How many four-digit numbers are divisible by four and below {say(1000*cap)}? Start by listing the legal endings.", f"4 distinct digits. Number < {1000*cap}; divisible by 4.")),
                ((f"Only the last two digits determine divisibility by four, because one hundred is a multiple of four. This gives {say(len(endings))} endings with distinct digits from our set.", f"Legal endings: {text_end}."),
                 (f"The thousands digit must be one of {spoken_list(sorted(allowed))}. Remove any of these choices already used in the last two places.", f"First digit choices = {len(allowed)} minus eligible digits used in the ending."),
                 (f"Once the ending and thousands digit are chosen, the hundreds digit has {say(per_hundreds)} choices. It can be zero if still available.", f"Each suffix/first combination has {per_hundreds} choices in the hundreds place.")),
                tiles("Thousands","Hundreds","Tens","Ones"),
                worked_art=table(("Ending uses","Endings","First choices"),
                    *((used,amount,len(allowed)-used) for used,amount in case_rows)),proof=(
                        (f"Multiply the ending count, first-digit count and hundreds count in each row. Add those products to get {say(answer)} valid numbers.", f"{' + '.join(f'{amount}×{len(allowed)-used}×{per_hundreds}' for used,amount in case_rows)} = {answer}."),
                        ("An ending like zero four means the last two digits are zero and four. That zero is allowed there because the first digit is a separate nonzero choice.", "04 is a valid suffix when both digits may be used."))),
        ),
        (("Dropping a leading zero changes the length of the number. An internal zero still occupies its own place.", "Accept zero as a first digit", "Enforce the first place before counting"),
         ("A divisibility test can use zero as part of the final pair. Use the printed last two digits even if their value is below ten.", "Reject endings such as zero four", "Treat the ending as two positions")),
        (("Mark the legal first digits and the allowed endings. Decide whether repetition or leading zero is permitted before calculating.", "Mark the positional restrictions", "Apply separate tests to separate positions."),
         ("Count the most restricted positions first. Check what they remove from the other places, and add only disjoint cases.", "Track the available digits", "Verify each number fits the length and the range.")),
        cover=tiles("Leading","Middle","Ending"),
    )
