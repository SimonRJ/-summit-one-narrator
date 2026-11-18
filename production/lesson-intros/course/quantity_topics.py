"""Ratios, percentages, weighted totals and quantities with units."""

from fractions import Fraction as F
from math import lcm

from story import Example, Topic, bars, chain, say, spoken_list, table, tiles


def ratios(lesson):
    v=lesson.visit
    a,b,t=2+v%3,5+v%3,3+v
    scale=(100,200,500,1000,100,200,500)[v]
    cm=4+v
    metre=F(cm*scale,100)
    p,q=4+v%3,2+v%2
    end_red,end_blue=q,p
    total=(p+q)*(6+v)
    shift=(p-q)*(6+v)
    assert F(total*q,p+q)+shift == F(total*end_blue,end_red+end_blue)
    return Topic(
        (("A ratio compares amounts measured in consistent units. To keep the same ratio, multiply or divide all the parts by the same factor.", "Both terms scale together."),
         ("A proportion of the whole uses the sum of the ratio parts. A transfer changes the parts while leaving that whole fixed.", "Share of the whole = parts ÷ total parts.")),
        (("In AMC practice, look for scale drawings, recipes, or quantities mixed in the same proportion. Check that the units agree.", "AMC Upper Primary · common scale factor"),
         ("In a Rossmoyne style puzzle, the ratio can change after something moves. Look for a total that stays constant.", "Rossmoyne-style · compare two ratios")),
        (
            Example("Scale equal groups", (
                (f"One mixture uses {say(a)} red beads for every {say(b)} blue beads. Find the quantities for {say(t)} identical batches.", f"{a} : {b} in one batch. Make {t} batches."),
                ("Which scale factor applies to each count?", "Scale both colours.")),
                ((f"Multiply the red count and the blue count by {say(t)}. That preserves the comparison per batch.", f"{a} × {t} reds; {b} × {t} blues"),
                 (f"The new counts are {say(a*t)} reds and {say(b*t)} blues. Dividing both by {say(t)} recovers the original ratio.", f"{a*t} : {b*t}")), bars(("One batch",((a,a),(b,b))),("Scaled",((a*t,a*t),(b*t,b*t))))),
            Example("Use the scale in the right units", (
                (f"On a one to {say(scale)} drawing, a wall is {say(cm)} centimetres long. Find the actual wall length in metres.", f"Scale 1 : {scale}, drawing {cm} cm. Actual length in metres?"),
                ("First decide what one centimetre on the drawing represents.", "Convert the units at the end.")),
                ((f"One centimetre represents {say(scale)} centimetres. Multiply by {say(cm)} to get the real length in centimetres.", f"{cm} × {scale} = {cm*scale:,} cm"),
                 (f"There are one hundred centimetres in one metre. Divide the centimetre result by one hundred.", f"{cm*scale:,} cm ÷ 100"),
                 (f"The length is {say(metre)} metres. The factor from drawing to real length is the same before converting units.", f"{metre} m")), table(("Drawing","Real"),("1 cm",f"{scale} cm"),(f"{cm} cm",f"{cm*scale} cm"))),
            Example("Use a fixed total when a ratio changes", (
                (f"Two trays, Red and Blue, contain identical counters. The counts in Red and Blue are in the ratio {say(p)} to {say(q)}. Move {say(shift)} counters from Red to Blue.", f"Red tray : Blue tray = {p} : {q}. Move {shift} to Blue."),
                (f"The new ratio is {say(end_red)} to {say(end_blue)}. How many counters are there in all?", f"New ratio {end_red} : {end_blue}. Find the total.")),
                ((f"The total stays the same. In both ratios there are {say(p+q)} equal parts of that same total.", f"Same total, split into {p+q} parts"),
                 (f"The Blue tray goes from {say(q)} parts to {say(p)} parts. That increase of {say(p-q)} parts consists of exactly the {say(shift)} transferred counters.", f"{p} − {q} = {p-q} parts = {shift} counters"),
                 (f"One part is {say(shift//(p-q))}. Multiply by the full {say(p+q)} parts. Together the trays contain {say(total)} counters.", f"{p+q} × {shift//(p-q)} = {total}")),
                bars(("Before",((p,f"red {p}"),(q,f"blue {q}"))),("After",((q,f"red {q}"),(p,f"blue {p}")))), proof=(
                    (f"The original tray counts are {say(p*(6+v))} and {say(q*(6+v))}. The transfer changes them to {say(q*(6+v))} and {say(p*(6+v))}.", f"{p*(6+v)} : {q*(6+v)} → {q*(6+v)} : {p*(6+v)}"),
                    ("Reduce both pairs by the same part size. The two given ratios return, and the total is unchanged.", "Verify both ratios using one part size."))),
        ),
        (("Multiplying just one ratio term changes the comparison. Apply the same scale factor to every term.", "Scale a single ratio term", "Scale all terms by the same factor"),
         ("When you need a fraction of the whole, add both ratio terms first. A three to five ratio gives three eighths for the first group.", "Read 3 : 5 as 3/5 of the whole", "The first share is 3/8 of the whole")),
        (("Check that both sides use consistent units before calculating. Name one ratio part and write what it represents.", "Match the units", "Write a label on each quantity."),
         ("For a change from one ratio to another, identify what stays fixed. Compare the same fraction of that fixed quantity.", "Look for a fixed whole", "Use the change in parts to find one part.")),
        cover=bars(("One group",((3,3),(5,5))),("Two groups",((6,6),(10,10)))),
    )


def percentages(lesson):
    v=lesson.visit
    percent=(35,25,45,60)[v]
    whole=(80,124,60,95)[v]
    part=percent*whole//100
    assert part*100==percent*whole
    na,da,nb,db=17+v,40+5*v,53+3*v,120+5*v
    first,second=F(na,da),F(nb,db)
    better="A" if first>second else "B" if first<second else "Both"
    p,q=(25,20,50,10)[v],(10,25,20,30)[v]
    initial=200+200*v
    up=initial*(100+p)//100
    final=up*(100-q)//100
    factor=F(100+p,100)*F(100-q,100)
    assert F(final,initial)==factor
    return Topic(
        (("A percentage is a fraction with denominator one hundred. A fraction, a decimal and a percentage can describe the same share.", "Percent means per hundred."),
         ("Give every percentage a base amount. If the base changes, the absolute size of the same percent changes too.", "Always ask: percent of which amount?")),
        (("In AMC practice, percentages may compare scores, discounts or part of a collection. Convert to one form to make fair comparisons.", "AMC Upper Primary · compare equivalent shares"),
         ("A Rossmoyne style problem may apply two percentage changes. Keep the base for each change and work with exact multipliers.", "Rossmoyne-style · follow the changing base")),
        (
            Example("Take a percent of a whole", (
                (f"Find {say(percent)} percent of {say(whole)}. Write the percent as an exact fraction before multiplying.", f"{percent}% of {whole}"),
                ("Can you simplify the fraction to make each part easier to find?", "Reduce the fraction first.")),
                ((f"{say(percent)} percent means {say(percent)} over one hundred. Its simplified form is {say(F(percent,100))}.", f"{percent}% = {F(percent,100)}"),
                 (f"Take this fraction of {say(whole)}. The result is {say(part)}. It is smaller than the original because the percent is below one hundred.", f"{whole} × {F(percent,100)} = {part}")), bars(("Whole",((percent,f"{percent}%"),(100-percent,f"{100-percent}%"))))),
            Example("Compare two unequal sample sizes", (
                (f"Team A answers {say(na)} out of {say(da)} correctly. Team B answers {say(nb)} out of {say(db)} correctly. Which accuracy is higher?", f"A: {na}/{da}. B: {nb}/{db}."),
                ("Compare the fractions, since the teams faced different numbers of questions.", "Compare the share correct.")),
                ((f"Express the shares over a common denominator, or compare the cross products. Multiply {say(na)} by {say(db)} for A.", f"A cross product: {na} × {db} = {na*db}"),
                 (f"For B multiply {say(nb)} by {say(da)}. Compare the numerators over the same positive denominator.", f"B cross product: {nb} × {da} = {nb*da}"),
                 (("The two cross products agree, so the accuracies are equal." if better=="Both" else f"Team {better} has the higher accuracy. It has the larger numerator after a fair comparison.")+
                  " The totals of correct answers alone were not enough.", "Equal accuracy" if better=="Both" else f"Higher accuracy: Team {better}")), table(("Team","Correct","Total"),("A",na,da),("B",nb,db))),
            Example("Reverse two percentage changes", (
                (f"A price is increased by {say(p)} percent. The new price is then reduced by {say(q)} percent.", f"Increase by {p}%, then reduce by {q}%."),
                (f"The final price is {say(final)} dollars. What was the original price? Each percent acts on the price immediately before that change.", f"Final price ${final}. Find the original.")),
                ((f"The discount leaves {say(100-q)} percent of the increased price. Undo it by dividing the final price by {say(F(100-q,100))}.", f"${final} ÷ {(100-q)}/100 = ${up}"),
                 (f"The increased price was {say(up)} dollars. It is {say(100+p)} percent of the original. Divide again to undo that increase.", f"${up} ÷ {(100+p)}/100 = ${initial}"),
                 (f"The original price was {say(initial)} dollars. Check by applying the increase first and taking the discount from that result.", f"${initial} → ${up} → ${final}")),
                chain("Original",f"+{p}%",f"−{q}%",f"${final}"),proof=(
                    (f"The combined multiplier is {say(F(100+p,100))} times {say(F(100-q,100))}, which is {say(factor)}.", f"{(100+p)}/100 × {(100-q)}/100 = {factor}"),
                    ("Multiplying the original price by that factor returns the final price. Subtracting the two percentage numbers would use the same base for both changes.", "Multiply the two percentage factors."))),
        ),
        (("Compare proportions with a common denominator. A larger numerator by itself says little when the totals differ.", "Compare only the number correct", "Compare correct ÷ total"),
         ("A price reduction of twenty percent leaves eighty percent. Use the amount that remains as a multiplier.", "Multiply the old price by 20% for the new price", "Multiply by 80% to keep what remains")),
        (("Name the base under every percentage. Convert to a fraction or a multiplier you can check exactly.", "Label the base", "Percent of which whole?"),
         ("When several percentages act in sequence, write one multiplier for each step. Reverse division and multiplication in the correct order.", "Keep a multiplier chain", "Check by running the changes forward.")),
        cover=tiles("Fraction","Percent","Same share"),
    )


def averages(lesson):
    v=lesson.visit
    mid=12+v
    scores=(mid-4-v%2,mid+1,mid+3+v%2)
    n,m=3+v%3,6+v//3
    center=14+v
    first,second=center+2*m,center-2*n
    total=n*first+m*second
    assert F(total,n+m)==center
    left,right=4+v%3,3+v%2
    count=left+right-1
    readings=[10+v+(i%5) for i in range(count)]
    common=readings[left-1]
    a,b=sum(readings[:left]),sum(readings[-right:])
    full=sum(readings)
    assert a+b-full==common
    return Topic(
        (("The mean shares a total equally among the readings. If a mean and its count are known, multiply to restore the total.", "Mean × count = total"),
         ("When combining groups, put the totals together and divide by the total number of readings.", "Combine totals, then share again.")),
        (("AMC practice questions can describe average scores, measurements or totals over several days. Write the number of readings beside each mean.", "AMC Upper Primary · use the count with the mean"),
         ("A Rossmoyne style average puzzle can give overlapping groups. Restoring their totals exposes a shared reading.", "Rossmoyne-style · use an overlap")),
        (
            Example("Share a total evenly", (
                (f"Find the mean of three readings: {spoken_list(scores)}. State what a mean represents for these readings.", f"Find the mean of {', '.join(map(str,scores))}."),
                ("Imagine redistributing the total to three equal amounts.", "Share the sum into three equal parts.")),
                ((f"The three readings sum to {say(sum(scores))}. Keep all three values when finding the total.", f"Sum = {sum(scores)}"),
                 (f"Divide by three. Each equal share is {say(mid)}, so that is the mean.", f"{sum(scores)} ÷ 3 = {mid}")), tiles(*scores)),
            Example("Combine groups of different sizes", (
                (f"One group has {say(n)} values with mean {say(first)}. A second group has {say(m)} values with mean {say(second)}.", f"{n} values at mean {first}; {m} values at mean {second}."),
                ("Find the mean after combining the two groups. They contain different numbers of readings.", "What is the combined mean?")),
                ((f"The first total is {say(n*first)}. The second is {say(m*second)}. Compute each by multiplying its mean by its count.", f"Group totals: {n} × {first} and {m} × {second}"),
                 (f"The combined total is {say(total)} from {say(n+m)} readings. Divide this total by the combined count.", f"{total} ÷ {n+m}"),
                 (f"The combined mean is {say(center)}. It lies between the two means and closer to the larger group's mean.", f"Combined mean = {center}")), table(("Group","Count","Mean"),("First",n,first),("Second",m,second))),
            Example("Find a reading shared by two averages", (
                (f"There are {say(count)} readings with mean {say(F(full,count))}. The first {say(left)} have mean {say(F(a,left))}.", f"All {count} mean {F(full,count)}. First {left} mean {F(a,left)}."),
                (f"The last {say(right)} have mean {say(F(b,right))}. Exactly one reading is in both groups. Find it.", f"Last {right} mean {F(b,right)}. Find the overlap.")),
                ((f"Recover the first and last totals by multiplying the means by their counts. The first total is {say(a)} and the last is {say(b)}.", f"First total {a}; last total {b}"),
                 (f"The total of the full list is {say(full)}. Adding the first and last totals counts the shared reading twice.", f"{a} + {b} includes the overlap twice."),
                 (f"The excess above the whole list is {say(common)}. This is the one shared reading.", f"{a} + {b} − {full} = {common}")), bars(("First readings",((left-1,"first"),(1,"shared"))),
                    ("Last readings",((1,"shared"),(right-1,"last")))), proof=(
                    ("There are exactly as many distinct positions as the first count plus the last count minus one. That explains why the total correction is a single value.", f"{left} + {right} − 1 = {count} positions"),
                    (f"Add the totals and remove one copy of {say(common)}. You recover {say(full)}, the total for the stated overall mean.", f"{a} + {b} − {common} = {full}"))),
        ),
        (("A group with more readings has more weight. Add the original totals instead of sharing the two means equally.", "Average the two group means", "Weight by the number of readings"),
         ("A reading shared by two groups contributes to both totals. Count one fewer copy in the full collection.", "Add overlapping totals as if disjoint", "Remove the extra shared copy")),
        (("Write mean, count and total together. Start each calculation with the pair you actually know.", "Restore totals", "Use mean × count."),
         ("Check the groups for overlap and the final denominator for how many readings there really are.", "Count values accurately", "Use the full total divided by the full count.")),
        cover=tiles("Count","Mean","Total"),
    )


def weighted_fractions(lesson):
    v=lesson.visit
    a,b=12+6*v,20+4*v
    useful1,useful2=a//3,b//4
    x,y=6*(4+v),9*(5+v)
    combined=x+y
    yes=x//2+y//3
    baseline=F(combined,3)
    extra=F(yes)-baseline
    assert extra*6==x and F(x,2)+F(y,3)==yes
    return Topic(
        (("Grouped fractions refer to different group sizes. Find the actual contribution from each group before combining them.", "Find each group's contribution."),
         ("A combined proportion is the total success count divided by the total group size.", "Overall share = combined successes ÷ combined size.")),
        (("In AMC practice, a problem may give fractions for two groups of people or objects. Convert each fraction into a count.", "AMC Upper Primary · calculate group contributions"),
         ("A Rossmoyne style problem can work in reverse: use the combined total to recover the size of one group.", "Rossmoyne-style · recover group sizes")),
        (
            Example("Add contributions from two groups", (
                (f"One third of {say(a)} red cards and one quarter of {say(b)} blue cards are starred. How many starred cards are there?", f"Starred: 1/3 of {a} and 1/4 of {b}."),
                ("Find both counts separately, then add them.", "How many stars altogether?")),
                ((f"One third of {say(a)} is {say(useful1)}. One quarter of {say(b)} is {say(useful2)}.", f"{a} ÷ 3 = {useful1}; {b} ÷ 4 = {useful2}"),
                 (f"These are different cards, so their counts add. There are {say(useful1+useful2)} starred cards.", f"{useful1} + {useful2} = {useful1+useful2}")), table(("Colour","All","Starred"),("Red",a,"1/3"),("Blue",b,"1/4"))),
            Example("Use the combined group size", (
                (f"The same groups have {say(a+b)} cards in total. One third of the red group of {say(a)} and one quarter of the blue group of {say(b)} are starred.", f"{a} red at 1/3; {b} blue at 1/4"),
                ("What fraction of all the cards are starred? Identify the numerator and denominator separately.", "Find the share of the full collection.")),
                ((f"The numerator is the count of starred cards. The two contributions are {say(useful1)} and {say(useful2)}, or {say(useful1+useful2)} in total.", f"Starred total = {useful1+useful2}"),
                 (f"The full collection has {say(a+b)} cards. Put the starred count over that full size.", f"Share = {useful1+useful2}/{a+b}"),
                 (f"In lowest terms that is {say(F(useful1+useful2,a+b))}. This uses actual counts, so the unequal group sizes have their proper weight.", f"Fraction starred = {F(useful1+useful2,a+b)}")), bars(("All cards",((a,"red"),(b,"blue"))),("Starred",((useful1,useful1),(useful2,useful2))))),
            Example("Recover two group sizes from their rates", (
                (f"There are {say(combined)} items in groups A and B. Half of A and one third of B are marked. In total {say(yes)} items are marked.", f"{combined} items, {yes} marked; rates 1/2 and 1/3."),
                ("Find the size of each group. Compare the actual marked count with what one third of the entire collection would give.", "How many items are in A and B?")),
                ((f"If every item used the lower rate, one third of {say(combined)} would give {say(baseline)} marks.", f"Baseline = {combined} ÷ 3 = {baseline}"),
                 (f"The extra is {say(extra)} marks. Every item in A adds a difference of one half minus one third, which is one sixth of a mark.", f"Extra rate for A = 1/2 − 1/3 = 1/6"),
                 (f"Six times the excess gives group A's size, {say(x)}. Subtract that from the full size to find group B, {say(y)}.", f"A = {extra} × 6 = {x}; B = {y}")),
                bars(("Whole",((combined,"all items"),)),("Two groups",((x,"A"),(y,"B")))),proof=(
                    (f"Check the actual marked count. Half of A gives {say(x//2)}. One third of B gives {say(y//3)}.", f"{x} ÷ 2 + {y} ÷ 3 = {yes}"),
                    ("Both the total size and the marked count match. The fixed difference in rates determines A uniquely.", f"{x} + {y} = {combined}"))),
        ),
        (("Adding the fractions of two separate groups does not add their amounts. Multiply by each corresponding group size first.", "Add 1/3 and 1/4 of different groups", "Calculate both actual counts"),
         ("For the combined proportion, use the combined size, including unmarked items and every group.", "Use a single group's denominator", "Use the full collection size")),
        (("Write one row per group with its size, rate and contribution. Keep those three columns distinct.", "Make a short table", "Contribution = rate × size."),
         ("When the combined amount is known, compare with a simple baseline. Test the recovered group sizes with both original totals.", "Check the weighted total", "Verify the group sizes and their contributions.")),
        cover=bars(("Group A",((3,"1/3"),(6,"rest"))),("Group B",((3,"1/4"),(9,"rest")))),
    )


def unit_rates(lesson):
    v=lesson.visit
    a,b=2+v,350+25*v
    gap=35+5*v
    duration=60*(7+v)
    repetitions,tail=divmod(duration,gap)
    first,second=70+10*v,105+15*v
    period=lcm(first,second)
    limit=60*(14+2*v)
    A,B,both=limit//first+1,limit//second+1,limit//period+1
    answer=A+B-both
    assert len(set(range(0,limit+1,first))|set(range(0,limit+1,second)))==answer
    return Topic(
        (("A rate pairs an amount with a unit of time, distance or work. Convert the units before you multiply, divide or compare.", "Choose one unit for each quantity."),
         ("For repeating events, decide whether the start counts and whether the last instant is included.", "Mark the start and finish on a timeline.")),
        (("AMC practice often mixes clocks, seconds, minutes and distances. Read the units printed beside each number before writing an equation.", "AMC Upper Primary · match the units"),
         ("A Mawa style investigation can combine two repeat schedules. Track the shared events as well as the individual schedules.", "MAWA-style · compare repeat periods")),
        (
            Example("Use one distance unit", (
                (f"A trail is {say(a)} kilometres and {say(b)} metres long. What is its length in metres?", f"{a} km {b} m → metres"),
                ("First convert the kilometres, then add the remaining metres.", "Use 1 km = 1,000 m.")),
                ((f"Each kilometre has one thousand metres. The kilometre part is {say(1000*a)} metres.", f"{a} km = {1000*a:,} m"),
                 (f"Adding the extra {say(b)} metres gives {say(1000*a+b)} metres in all.", f"{1000*a:,} + {b} = {1000*a+b:,} m")), chain(f"{a} km",f"{1000*a:,} m",f"+{b} m")),
            Example("Count full repeat intervals", (
                (f"A sensor flashes every {say(gap)} seconds, with its first flash after one complete interval. Count the flashes in {say(duration//60)} minutes, including the finish if there is a flash there.", f"Every {gap} s. First flash at {gap} s. Finish at {duration//60} min."),
                ("Convert the time window to seconds before dividing.", "Count only completed intervals.")),
                ((f"The window is {say(duration)} seconds. Each completed interval contains exactly one flash at its end.", f"{duration//60} × 60 = {duration} s"),
                 (f"Divide by {say(gap)}. There are {say(repetitions)} whole intervals and {say(tail)} seconds remaining.", f"{duration} = {gap} × {repetitions} + {tail}"),
                 (f"The count is {say(repetitions)}. At the start the light has not yet flashed, so no extra event belongs at zero.", f"{repetitions} flashes")), chain(0,gap,2*gap,repetitions*gap,duration)),
            Example("Count two schedules without counting meetings twice", (
                (f"Two signals flash at time zero. One repeats every {say(first)} seconds, and the other every {say(second)} seconds.", f"Start together. Periods {first} s and {second} s."),
                (f"In the first {say(limit//60)} minutes, including both endpoints, how many distinct instants have a flash? Count simultaneous flashes as one instant.", f"Through {limit//60} min inclusive, count distinct instants.")),
                ((f"The window is {say(limit)} seconds. In the first schedule there are {say(A-1)} later flashes, plus the one at zero.", f"First schedule: floor({limit}/{first}) + 1 = {A}"),
                 (f"The second schedule gives {say(B)} flashes including zero. Both schedules are aligned initially, so they coincide every {say(period)} seconds.", f"Second schedule: {B}; shared period: {period} s"),
                 (f"The shared count is {say(both)}, including the start. Subtract that from the two individual counts to keep one copy of each shared instant.", f"{A} + {B} − {both} = {answer} instants")),
                table(("Signal","Period"),("A",f"{first} s"),("B",f"{second} s")),proof=(
                    (f"The overlap uses the least common multiple of {say(first)} seconds and {say(second)} seconds. Both timers complete whole intervals at those instants.", f"LCM = {period} s"),
                    (f"The answer is {say(answer)}. A flash at either endpoint is counted once if it is in both schedules.", "Include zero once and inspect the far endpoint."))),
        ),
        (("A minute is sixty seconds, not a hundred. Multiply all time quantities into one shared unit before comparing repeat intervals.", "Mix minutes and seconds in a division", "First convert both times to seconds"),
         ("A count of full intervals does not include an event at time zero. Add that event if the wording says it belongs.", "Automatically skip or include time zero", "Use the stated first event")),
        (("Write the units next to the numbers. Convert to a common unit and use a short timeline to mark the first repeat.", "Standardise the units", "One minute equals sixty seconds."),
         ("For two schedules, check the shared starts and the repeated overlap. Verify whether the endpoint itself is a legal event.", "Check the overlap and endpoints", "Count a shared instant once.")),
        cover=chain("Minutes","×60","Seconds"),
    )


def work_rates(lesson):
    v=lesson.visit
    a,b=6+2*v,9+3*v
    whole=lcm(a,b)
    duration=F(whole,whole//a+whole//b)
    before=2+v
    made=before*(whole//a+whole//b)
    net=whole//a+whole//b-1
    remaining=whole-made
    answer=before+F(remaining,net)
    assert (F(1,a)+F(1,b))*before+(F(1,a)+F(1,b)-F(1,whole))*(answer-before)==1
    return Topic(
        (("A work rate tells you how much of one complete job is done per unit of time. If one worker takes six minutes, the rate is one sixth of the job each minute.", "Rate = fraction of the job per minute."),
         ("Workers on the same job contribute their rates. An activity that undoes progress subtracts from that total rate.", "Add or subtract rates.")),
        (("In AMC practice, filling tanks, packing boxes or shared work can be described by the time for a whole task. Rewrite that time as progress per minute.", "AMC Upper Primary · convert time to rate"),
         ("A Rossmoyne style problem might change workers part of the way through. Split the timeline and keep the remaining work.", "Rossmoyne-style · divide the timeline")),
        (
            Example("Find a unit rate for one worker", (
                (f"A machine labels a whole batch of boxes in {say(a)} minutes at a steady rate. What fraction of the batch does it label in one minute?", f"One batch in {a} min"),
                ("Use equal parts of the job.", "Find progress in 1 minute.")),
                ((f"Divide the batch into {say(a)} equal portions. One minute is one of those portions.", f"1 ÷ {a} of the batch"),
                 (f"The rate is {say(F(1,a))} of a batch per minute. Multiply this fraction by {say(a)} minutes to check it gives one batch.", f"Rate = 1/{a} batch per minute")), tiles("1 batch",f"{a} min")),
            Example("Combine two rates", (
                (f"Machine A can finish one batch in {say(a)} minutes. Machine B takes {say(b)} minutes to finish a batch of the same size.", f"A takes {a} min. B takes {b} min."),
                ("How long does one batch take if they work together at their full rates?", "Find the combined completion time.")),
                ((f"Represent one batch by {say(whole)} units. A completes {say(whole//a)} units per minute, and B completes {say(whole//b)}.", f"Choose {whole} units → rates {whole//a} and {whole//b}"),
                 ("The combined rate is five units per minute. Both machines contribute during the same minute.", "Combined rate = 5 units per minute"),
                 (f"The time is {say(whole)} divided by five. That is {say(duration)} minutes.", f"Time = {whole} ÷ 5 = {duration} min")), table(("Machine","Minutes","Units/min"),("A",a,whole//a),("B",b,whole//b))),
            Example("Find when two pumps finish after a leak opens", (
                (f"Two pumps together fill a tank. Alone, one would take {say(a)} minutes and the other {say(b)} minutes.", f"Pumps alone: {a} min or {b} min for one tank."),
                (f"After {say(before)} minutes a leak opens which would empty a full tank in {say(whole)} minutes by itself. How long from the start until the tank is full?", f"Leak starts at {before} min. Leak alone empties in {whole} min.")),
                ((f"Use {say(whole)} units for a full tank. The pumps initially fill five units per minute, so they add {say(made)} before the leak.", f"Before leak: {before} × 5 = {made} units"),
                 (f"That leaves {say(remaining)} units. The leak removes one unit each minute, so the new net rate is four units per minute.", f"{whole} − {made} = {remaining}. New rate: 5 − 1 = 4."),
                 (f"Divide the remaining work by four, then add the initial {say(before)} minutes. The answer is {say(answer)} minutes.", f"{before} + {remaining} ÷ 4 = {answer} min")),
                chain("Start",f"{before} min","Leak","Full"),proof=(
                    (f"The first period contributes {say(made)} units. During the second period, the net addition is {say(remaining)} units.", f"{made} + {remaining} = {whole}"),
                    ("The two contributions fill exactly one tank. The two different rates apply to two different time intervals.", "Check one complete job."))),
        ),
        (("Times for a whole job do not add when two workers are working at once. Convert both times to rates before adding.", "Add the two completion times", "Add work completed per minute"),
         ("A leak running during the second period has no effect on the first period's work. Keep the rate with its own interval.", "Use the leak rate from the start", "Split at the time the leak opens")),
        (("Choose a convenient number of units for the job. A common multiple of the given times often gives whole-number rates.", "Choose work units", "Divide units by time to get a rate."),
         ("After every change, subtract completed work from the whole. Use the new net rate only for the remaining work.", "Track the remaining work", "Check that contributions sum to one full job.")),
        cover=bars(("A",( (3,"3"),)),("B",((2,"2"),)),("Together",((3,"3"),(2,"2")))),
    )


def distance_speed(lesson):
    v=lesson.visit
    distance=18+6*v
    time=3
    rate=distance//time
    speed=12+4*v
    length=3*speed
    minute=45+5*v
    ride=F(speed*minute,60)
    trip=(24,30,36,48)[v]
    outward,back=(12,18),(24,15)
    vo,vr=outward[v%2],back[v%2]
    break_minutes=12+6*v
    go=F(trip*60,vo)
    return_trip=F(trip*60,vr)
    total=go+return_trip+break_minutes
    mean=F(120*trip,total)
    assert mean*total/60==2*trip
    return Topic(
        (("Speed tells you how far you travel in one unit of time. The three quantities are connected: distance equals speed times time.", "Distance = speed × time."),
         ("An average speed uses total distance and total elapsed time. It includes stops if the question includes those in the time.", "Average speed = total distance ÷ elapsed time.")),
        (("In AMC practice, distance, speed and time often arrive in different units. Choose one time unit for your calculation first.", "AMC Upper Primary · keep rate units consistent"),
         ("A Rossmoyne style journey may have several stages. Work out each stage's distance or time before taking the average.", "Rossmoyne-style · combine journey stages")),
        (
            Example("Find speed from distance and time", (
                (f"A cyclist covers {say(distance)} kilometres in {say(time)} hours at a steady pace. Find the speed in kilometres per hour.", f"{distance} km in {time} h"),
                ("What distance is covered in one hour?", "Find distance per hour.")),
                ((f"Share {say(distance)} kilometres among {say(time)} equal hours. Each hour covers {say(rate)} kilometres.", f"{distance} ÷ {time} = {rate}"),
                 (f"The speed is {say(rate)} kilometres per hour. Multiplying back by the time recovers the full distance.", f"{rate} km/h")), bars(("Journey",tuple((1,rate) for _ in range(time))))),
            Example("Convert minutes before computing distance", (
                (f"A rider moves at {say(speed)} kilometres per hour for {say(minute)} minutes. How far do they travel?", f"{speed} km/h for {minute} min"),
                ("The rate already uses hours, so express the time as a fraction of an hour.", "Convert the time before multiplying.")),
                ((f"There are sixty minutes per hour. The travel time in hours is {say(F(minute,60))}.", f"{minute} min = {F(minute,60)} h"),
                 (f"Multiply by the speed to get {say(ride)} kilometres. If the time is below an hour, the distance is below the one-hour distance.", f"{speed} × {F(minute,60)} = {ride} km")), chain(f"{minute} min",f"{F(minute,60)} h",f"{ride} km")),
            Example("Find an average for a round trip with a stop", (
                (f"A rider travels {say(trip)} kilometres out at {say(vo)} kilometres per hour, stops for {say(break_minutes)} minutes, and returns along the same route at {say(vr)} kilometres per hour.", f"{trip} km out at {vo} km/h, {break_minutes} min stop, return at {vr} km/h."),
                ("What average speed covers the full trip including the stop?", "Use total elapsed time, including the stop.")),
                ((f"Time equals distance divided by speed. The outward and return times are {say(go)} and {say(return_trip)} minutes.", f"Out {go} min. Back {return_trip} min."),
                 (f"Add the stop. The elapsed time is {say(total)} minutes. The distance includes both legs, so it is {say(2*trip)} kilometres.", f"Elapsed {total} min. Travelled {2*trip} km."),
                 (f"Divide the total distance by that time in hours. The average is {say(mean)} kilometres per hour.", f"Average = {2*trip} ÷ ({total}/60) = {mean} km/h")),
                table(("Stage","Dist","Speed"),("Out",trip,vo),("Stop",0,0),("Return",trip,vr)),proof=(
                    ("The two moving stages cover the same distance but take different amounts of time. A simple mean of the two speeds would give them equal time weights.", "Different speeds act for different times."),
                    ("The stop contributes time and zero distance. Including it in the average correctly reduces the overall rate.", "Include stop time when the question asks."))),
        ),
        (("Multiplying kilometres per hour by minutes uses inconsistent time units. Convert the time to hours first, or change the speed to kilometres per minute.", "Multiply km/h by unconverted minutes", "Convert to hours first"),
         ("Use one total distance and one total time. Do not average the speeds without checking how long you travelled at each.", "Average the two stage speeds directly", "Divide total distance by total time")),
        (("Draw one row for each journey stage. Put speed, distance and time in matching units.", "Record each stage", "Use distance = speed × time."),
         ("For an average, check whether the time window includes stops. Add all the distances and the corresponding times first.", "Find the overall rate", "Make the total in the denominator explicit.")),
        cover=tiles("Distance","Speed","Time"),
    )


def relative_motion(lesson):
    v=lesson.visit
    p,q=3+v,5+v
    initial=4*(p+q)
    slow,fast=4+v,7+2*v
    wait=5+v
    lead=slow*wait
    catch=F(lead,fast-slow)
    track=300+60*v
    a,b=2+v,3+2*v
    delay=5+v
    gap=track-a*delay
    meet=F(gap,a+b)
    second=delay+meet+F(track,a+b)
    assert (a+b)*(second-delay)+a*delay==2*track
    return Topic(
        (("Relative speed measures how fast a gap changes. Moving towards each other closes a gap at the sum of the two speeds.", "Towards each other: add the speeds."),
         ("For a chase in the same direction, the gap closes at the faster speed minus the slower speed.", "Chase in one direction: use the difference.")),
        (("AMC questions about meetings, chases or moving markers often become short if you draw the gap that is changing.", "AMC Upper Primary · draw the gap"),
         ("A Rossmoyne style problem may have delayed starts or a circular route. Track when the shared motion begins and when a full lap has passed.", "Rossmoyne-style · account for timing")),
        (
            Example("Close a gap from both ends", (
                (f"Two walkers are {say(initial)} metres apart and walk directly towards each other at {say(p)} and {say(q)} metres per second.", f"Gap {initial} m. Speeds {p} and {q} m/s."),
                ("How many seconds until they meet? Think about the distance closed in one second.", "Find the rate at which the gap closes.")),
                ((f"The walkers together close {say(p+q)} metres every second. Both movements shorten the gap.", f"Closing speed: {p} + {q} = {p+q} m/s"),
                 (f"Divide the starting gap by that rate. They meet after four seconds.", f"{initial} ÷ {p+q} = 4 s")), bars(("Gap",((4*p,"left"),(4*q,"right"))))),
            Example("Catch a runner with a head start", (
                (f"A runner moves at {say(slow)} metres per second. A second runner starts from the same point {say(wait)} seconds later at {say(fast)} metres per second.", f"Speeds {slow} and {fast} m/s. Second starts {wait} s later."),
                ("How long after the second runner starts do they meet?", "Use the time measured from the later start.")),
                ((f"During the head start the first runner covers {say(lead)} metres. That is the gap when the chase starts.", f"Gap = {slow} × {wait} = {lead} m"),
                 (f"The faster runner closes {say(fast-slow)} metres each second, because both are moving in the same direction.", f"Closing speed: {fast} − {slow} = {fast-slow} m/s"),
                 (f"The catch happens after {say(catch)} seconds from the second start. Only add the head start if the question measures from the first start.", f"{lead} ÷ {fast-slow} = {catch} s")), chain("Start",f"+{wait}s",f"{lead}m gap","Catch")),
            Example("Track a delayed start around a circuit", (
                (f"A round track is {say(track)} metres long. Runner A starts at {say(a)} metres per second. After {say(delay)} seconds runner B leaves the same point in the opposite direction at {say(b)} metres per second.", f"Loop {track} m. A at {a} m/s, B at {b} m/s after {delay} s."),
                ("They keep running at those speeds. At what time after A starts do they meet for the second time?", "Find the second meeting time after A starts.")),
                ((f"At B's start, A has run {say(a*delay)} metres. They first meet when the combined distances reach one lap, so the unused part is {say(gap)} metres.", f"Distance left before first meet: {track} − {a*delay} = {gap}"),
                 (f"Together they cover {say(a+b)} metres each second. That gives {say(meet)} seconds from B's start to the first meeting.", f"First meeting after B starts: {gap} ÷ {a+b}"),
                 (f"The second meeting takes one more lap at the same combined rate. Add that time and the original delay.", f"Second meeting time = {delay} + {gap}/{a+b} + {track}/{a+b}")),
                chain("A starts","B starts","Meet 1","Meet 2"),proof=(
                    (f"The total elapsed time is {say(second)} seconds after A starts. At that time the two distances add to exactly {say(2*track)} metres.", f"Second meeting at {second} s, combined distance {2*track} m"),
                    ("The first meeting required one lap of combined movement. Adding a second lap accounts for exactly one further meeting.", "Track one lap between consecutive meetings."))),
        ),
        (("A same-direction chase uses the difference in speeds. Adding the speeds would model movement towards each other instead.", "Add speeds in a same-direction chase", "Subtract to find the rate of closing"),
         ("Timing from the later start measures only the shared motion. Check whether the requested clock started earlier.", "Forget the earlier runner's head start", "Use the requested starting time")),
        (("Draw arrows for the directions and label the gap. Decide whether the movements shorten the gap together or compete.", "Find the gap and its rate", "Use the sum or the difference."),
         ("For a loop, use one full circuit between matching positions. Check the final answer by reconstructing both distances.", "Check the meeting condition", "Allow for an offset or delayed start.")),
        cover=chain("Gap","Closing speed","Time"),
    )
