"""Review lessons that combine representations and check against the original conditions."""

from math import isqrt

from story import Example, Topic, bars, chain, say, spoken_list, table, tiles


def schedule_challenge(v):
    remainder=2+v//3
    start,end=24*(3+v),24*(5+v)+remainder
    rows=[(k,24*k+remainder,3*k) for k in range(3+v,6+v)]
    allowed=[n for _,n,b in rows if b%2]
    assert allowed==[n for n in range(start,end+1)
                     if n%6==n%8==remainder and (n//8)%2==1]
    return Example("Combine two remainder conditions and an odd count",(
        (f"A stack contains between {say(start)} and {say(end)} cards, inclusive. Making complete groups of six leaves {say(remainder)} cards. Making complete groups of eight leaves the same remainder.", f"{start}–{end} cards. The remainder is {remainder} for groups of 6 or 8."),
        ("The number of complete groups of eight is odd. Find every possible stack size.", "The quotient for groups of 8 must be odd.")),
        ((f"Remove the common remainder of {say(remainder)}. The remaining total is divisible by both six and eight, so it is a multiple of their least common multiple, twenty-four.", f"N − {remainder} is divisible by 24."),
         (f"The original count has the form twenty-four times k plus {say(remainder)}. The bounds limit k to {spoken_list([k for k,_,_ in rows])}.", f"N = 24k + {remainder}; k = {', '.join(str(k) for k,_,_ in rows)}."),
         ("Each full group of twenty-four contains three groups of eight. The quotient is three times k, which is odd exactly when k is odd.", "Groups of 8 = 3k. Keep odd k.")),
        tiles("Groups of 6","Groups of 8","Odd count"),worked_art=table(("k","Cards","Groups of 8"),*rows),
        proof=((f"The possible stack {'sizes are' if len(allowed)>1 else 'size is'} {spoken_list(allowed)}. Test each accepted value in both grouping rules and count the complete groups of eight.", f"Possible {'sizes' if len(allowed)>1 else 'size'}: {', '.join(map(str,allowed))}."),
               ("Any other size in the interval either leaves a wrong remainder or has an even number of groups of eight. The table accounts for every candidate.", "Verify the two remainders and the quotient parity.")),
        proof_art=table(("Cards"," remainder by 6 "," remainder by 8 ","Groups of 8"),
                        *((n,n%6,n%8,n//8) for n in allowed)))


def paving_challenge(v):
    area=60+8*(v-1)
    pairs=[(a,area//a) for a in range(3,isqrt(area)+1,3) if area%a==0]
    border=lambda a,b:2*(a+b)-4
    cols,rows=min(pairs,key=sum)
    boundary=border(cols,rows)
    inside=area-boundary
    assert inside==max((a-2)*(b-2) for a,b in pairs)
    return Example("Maximise a garden interior under a divisibility rule",(
        (f"A rectangular garden uses exactly {say(area)} paving squares. Every side has a whole-number length, and the shorter side is a positive multiple of three.", f"{area} squares. Short side is a multiple of 3."),
        ("The outer ring of squares is grey. How many non-grey interior squares can there be at most?", "Maximise the number of interior squares.")),
        ((f"The shorter side times the longer side is {say(area)}. Test multiples of three up to the square root of {say(area)}, since the shorter side cannot be larger than that.", f"Short side a ≤ √{area}; a is a multiple of 3."),
         ("For each pair, the grey ring has two rows and two columns of squares. Subtract four to correct for counting the corners twice.", "Grey border = 2a + 2b − 4."),
         (f"The least grey border occurs for sides {say(cols)} and {say(rows)}, using {say(boundary)} grey squares.", f"Best pair {cols} × {rows}; border {boundary}.")),
        tiles("Fixed area","Factor pairs","Border"),worked_art=table(("Short","Long","Border","Inside"),
                                                                  *((a,b,border(a,b),area-border(a,b)) for a,b in pairs)),
        proof=((f"Subtract the winning border count from the total. The greatest interior has {say(inside)} squares.", f"{area} − {boundary} = {inside}."),
               (f"Check directly by removing one layer along each side. The remaining rectangle is {say(cols-2)} by {say(rows-2)}, which also gives {say(inside)}.", f"({cols}−2) × ({rows}−2) = {inside}.")))


def boxes_challenge(v):
    total=5*(15+v)+8*(6+v)
    possible=[(b,(total-8*b)//5,(total-8*b)//5+b)
              for b in range(total//8+1) if (total-8*b)%5==0]
    best,small,used=possible[-1]
    remainder=possible[0][0]
    assert used==min(a+b for a in range(total//5+1) for b in range(total//8+1) if 5*a+8*b==total)
    return Example("Use a remainder to minimise the number of boxes",(
        (f"Ship exactly {say(total)} items in full boxes. There are boxes that each hold five items and boxes that each hold eight. You have as many of each type as you need.", f"Ship {total} items in full boxes of 5 or 8."),
        ("What is the smallest number of boxes that fits exactly?", "Find an exact total with as few boxes as possible.")),
        ((f"Let b be the number of eight-item boxes. The remaining {say(total)} minus eight b items must make complete groups of five.", f"{total} − 8b must be divisible by 5."),
         (f"Modulo five, eight leaves remainder three. So three b must leave remainder {say(total%5)}. Test the five possible remainders for b; the matching one is {say(remainder)}.", f"3b leaves remainder {total%5} when divided by 5. b = {remainder} + 5k."),
         (f"The largest allowed b is {say(best)} because any next value would exceed total capacity. It leaves {say(small*5)} items, taking {say(small)} smaller boxes.", f"{best} large boxes + {small} small boxes.")),
        tiles("5 items","8 items",f"{total} total"),worked_art=table(("Large boxes","Small boxes","Total boxes"),*possible),
        proof=(("Among exact solutions, adding five large boxes replaces eight small boxes, since both hold forty items. This saves three boxes.", "Swap 8 small boxes for 5 large boxes to save 3."),
               (f"That proves the largest legal number of large boxes is optimal. It uses {say(used)} boxes, and we can check the shipping total exactly.", f"Minimum {used}: 8×{best} + 5×{small} = {total}.")))


def capstone(lesson):
    v=lesson.visit
    group=7+v
    packs=4+v
    remainder=2+v%4
    total=group*packs+remainder
    count=12+v
    cheap=3+v%3
    spread=2+v%4
    dearer=cheap+spread
    actual=4+v//2
    value=count*cheap+actual*spread
    assert value==actual*dearer+(count-actual)*cheap
    harder=(schedule_challenge if v%3==0 else paving_challenge if v%3==1 else boxes_challenge)(v)
    return Topic(
        (("When a problem gives several conditions, one method may narrow the options and another may finish the job. Match each clue to a calculation you can check.", "Match each condition to a useful calculation."),
         ("A good solution records why the result works and why competing candidates are impossible or worse.", "Compare candidates against the original rules.")),
        (("For a Rossmoyne entrance practice problem, write a simple representation you can add to as more clues take effect. An equation or a case table can save time.", "Rossmoyne-style · choose a representation you can extend"),
         ("For an AMC integer-answer problem or a Mawa style investigation, give your answer a second check based on the original quantities.", "AMC and MAWA-style · verify against the question")),
        (
            Example("Translate complete groups and a remainder",(
                (f"You have {say(total)} counters. Put as many as possible into full bags of {say(group)}. How many full bags are there, and how many counters remain?", f"{total} counters, {group} per full bag."),
                ("Find a multiple of the bag size just below the total.", "How many full groups fit?")),
                ((f"{say(packs).capitalize()} bags use {say(group*packs)} counters, and the difference is {say(remainder)}. Another whole bag would require {say(group)} additional counters.", f"{total} = {group} × {packs} + {remainder}."),
                 (f"The remainder is smaller than a full bag. That confirms there are {say(packs)} complete bags and {say(remainder)} left.", f"{packs} whole bags; {remainder} left.")),
                tiles(f"{group} per bag",f"{total} counters")),
            Example("Use a baseline to find two kinds of tickets",(
                (f"A box office sold {say(count)} tickets. A child ticket cost {say(cheap)} dollars and a family upgrade ticket cost {say(dearer)} dollars. The sales total was {say(value)} dollars.", f"{count} tickets; $ {cheap} or $ {dearer}; total $ {value}."),
                ("How many tickets were the more expensive kind? Begin by treating all of them as the cheaper kind.", "Find how much was spent above the cheapest baseline.")),
                ((f"If every ticket were cheaper, the total would be {say(count*cheap)} dollars. The real total is {say(actual*spread)} dollars higher.", f"Extra = {value} − {count*cheap} = {actual*spread}."),
                 (f"Each expensive ticket adds {say(spread)} dollars, so divide the extra by {say(spread)}. There were {say(actual)} expensive tickets and {say(count-actual)} cheaper tickets.", f"{actual*spread} ÷ {spread} = {actual}; cheaper = {count-actual}."),
                 ("Check both the number of tickets and the sales calculation. The same count must fit both conditions.", f"{actual}×{dearer} + {count-actual}×{cheap} = {value}.")),
                bars(("Cheapest baseline",((count*cheap,f"$ {count*cheap}"),)),
                     ("Actual sales",((count*cheap,f"$ {count*cheap}"),(actual*spread,f"$ {actual*spread}"))))),
            harder,
        ),
        (("Every condition has to hold for the same candidate. A partial match can be a useful starting point but it does not settle the question.", "Stop after matching one clue", "Test the same answer against all constraints"),
         ("When the question asks for an optimum or every possible value, one successful example is not enough. Explain why your method covers the alternatives.", "Give an example when an optimum is asked for", "Show the bound or compare a complete list")),
        (("Mark the quantity you need and label the information that restricts it. Choose the first method that cuts down the range.", "Identify the most useful constraint", "A good first step creates fewer candidates."),
         ("Check the final result against the original problem. In your next practice, record whether the setup, calculation or check was the slow part and revise that step.", "Check and improve your method", "Use your working to plan the next attempt.")),
        cover=chain("Translate","Narrow","Verify"),
    )
