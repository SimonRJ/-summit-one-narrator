// Original, short decision practice. No exam questions, time score or mastery credit.
// Each row: question, correct choice, plausible misconception, explanation.
export function techniqueCards(id,visit=1){
 const n=3+((visit-1)%7),x=n+4;
 const c=(q,yes,no,why)=>({q,yes:String(yes),no:String(no),why});
 switch(id){
 case 'DIG-01':return [
 c(`You need ${x} × 99. Which shortcut keeps the value unchanged?`,`${x} × 100 − ${x}`,`${x} × 100 − 1`,'Each of the groups gained one, so remove one for every group.'),
 c(`Find ${100*n-2} + 36 mentally. Which first move is valid?`,`${100*n} + 36 − 2`,`${100*n} + 36 + 2`,'Rounding the first number up adds two too many; compensate by subtracting.'),
 c('A machine adds 200 instead of 198 on each of 7 cycles. What must be corrected?','Subtract 14','Subtract 2','The error of two is repeated seven times.'),
 c(`For ${20*n} − 19, which is equivalent?`,`${20*n} − 20 + 1`,`${20*n} − 20 − 1`,'Subtracting twenty removes one too much; restore it.'),
 c('A receipt has a fixed $5 fee plus 8 items at $49. Which total fits?','8 × 50 − 8 + 5','8 × 50 − 1 + 5','Compensate for all eight prices, then add the separate fixed fee.')];
 case 'DIG-02':return [
 c('A three-digit number uses 0, 3 and 8 once each. Can it start with 0?','No','Yes','A leading zero would make it a two-digit number.'),
 c('A three-digit number must be even. Which position should you restrict first?','The units digit','The hundreds digit','Evenness depends on the final digit.'),
 c('Use 0, 2, 5 and 7 without repeats. If the last digit is 0, how many choices remain for the first?','3','2','All three remaining digits are nonzero and may begin the number.'),
 c('Use 0, 2, 5 and 7 without repeats. If the last digit is 2, how many choices remain for the first?','2','3','Only 5 and 7 can start; the remaining zero cannot.'),
 c('For even numbers made without repeating digits, why separate a zero ending from other even endings?','The first-place choices change','Zero is not an even digit','Zero is even, but using it at the end removes the leading-zero restriction from the remaining digits.')];
 case 'DIG-03':return [
 c('How many copies of digit 2 are printed in 22?','2','1','Count occurrences, not how many numbers contain the digit.'),
 c(`Labels run from ${10*n} through ${10*n+9}, inclusive. How many labels are there?`,'10','9','The difference counts gaps; add one to count both endpoints.'),
 c('To count copies of digit 3 from 1 to 49, what should you count separately?','Tens and units positions','Odd and even numbers','A digit can appear in either position; 33 contributes in both.'),
 c('Printing labels 98, 99, 100 uses how many digit characters?','7','6','The first two labels use two digits each; 100 uses three.'),
 c('A question asks how many labels contain at least one 4. How should label 44 count?','Once','Twice','This time the objects are labels, not copies of the digit. Read what is being counted.')];
 case 'DIG-04':return [
 c('Which description gives a four-digit palindrome?','ABBA','ABAB','The first and last digits match, as do the middle two.'),
 c('A four-digit palindrome begins 37. What are its final two digits?','73','37','Mirror the first half in reverse order.'),
 c('For a three-digit palindrome ABA, which choice is forbidden?','A = 0','B = 0','A leading zero would stop it being three-digit; the middle may be zero.'),
 c('A palindrome ABBA has digit sum 18. Which equation follows?','A + B = 9','A + B = 18','Each chosen digit occurs twice.'),
 c('The smallest palindrome strictly above 3553 is needed. Is mirroring 35 enough?','No: it gives the boundary itself','Yes: 3553 is a palindrome','Strictly above excludes equality. Increase the first half, then mirror again.')];
 case 'DIG-05':return [
 c('In a digit puzzle, what does 4A mean?','40 + A','4 × A','A letter occupies the units place here; it is not multiplication.'),
 c('The units column totals 15. What goes in that column?','Write 5; carry 1','Write 1; carry 5','Ten units become one ten, leaving five units.'),
 c('In A7 + 7A, what is the coefficient of A?','11','2','A contributes 10A in one number and A in the other.'),
 c('In 2A + 2A = 54, what does A equal?','7','27','Remove the forty contributed by the tens, then halve the remaining fourteen.'),
 c('A letter puzzle says different letters mean different digits. Is a result with A = B acceptable?','No','Yes, if the sum is correct','The answer must satisfy the distinct-digit condition as well as the arithmetic.')];
 case 'DIV-01':return [
 c('Equal packs must use all 42 tokens. Which pack size is allowed?','7','8','A pack size must divide the total without a remainder.'),
 c('For a divisor of 2³ × 5, how many powers of 2 can you choose?','4 choices: 0, 1, 2, 3','3 choices: 1, 2, 3','Exponent zero is allowed; it means choosing no factor of two.'),
 c('2² × 3² has how many positive divisors?','9','4','There are three exponent choices for each prime: 3 × 3.'),
 c('A grouping requires more than one group and more than one item per group. Which divisors are excluded?','1 and the total','Only 1','A pack equal to the total would give just one group.'),
 c('To make 2³ × 5² a square by multiplying, what is the smallest multiplier?','2','5','Squares have even prime exponents. Only the exponent of two needs another copy.')];
 case 'DIV-02':return [
 c(`Two signals repeat every ${2*n} and ${3*n} seconds. Which tool finds their common repeat period?`,'Least common multiple','Greatest common divisor','A common repeat time must be a multiple of both periods.'),
 c('Signals start together and repeat every 6 and 8 seconds. Next shared flash?','24 seconds','48 seconds','48 is shared, but 24 is the least positive common time.'),
 c('A shared flash occurs every 12 seconds. How many occur in the next 36 seconds, excluding now but including the end?','3','4','Count 12, 24 and 36; the starting instant is excluded.'),
 c('Two signals start at different times. Is the least common multiple necessarily their first shared time?','No','Yes','Their starting offsets also matter. The common period gives a gap between shared flashes.'),
 c('Signals flash at 5,11,17,… and 9,17,25,… . After the shared flash at 17, what comes next?','41','24','Their common period is 24; add it to the shared time 17.')];
 case 'DIV-03':return [
 c(`A total is written 7 × ${x} + 3. What does the 3 tell you?`,'The remainder after division by 7','The number of complete groups','The product counts complete groups; the extra three are left over.'),
 c('A proposed remainder after division by 5 is 7. Can that be the final remainder?','No','Yes','A remainder must be smaller than the divisor; another group of five can still be removed.'),
 c(`A machine has ${7*x+2} tokens and packs 7 per box. How many more tokens fill its unfinished box?`,'5','2','Two are left over, but the question asks for the empty spaces: 7 − 2.'),
 c('N leaves remainder 4 on division by 7. What remainder does N + 5 leave?','2','9','Add the remainders, then remove a full group of seven: 9 becomes 2.'),
 c('N leaves remainder 3 on division by 7. To find the remainder of N², which small calculation helps?','3², then reduce modulo 7','3 × 2','Squaring squares the remainder too; it does not double it. Nine leaves remainder two.')];
 case 'DIV-04':return [
 c('A move adds 6 to a counter. Which property definitely stays fixed?','Its remainder on division by 3','Its exact value','Six is a multiple of three, so the remainder stays unchanged.'),
 c('Exactly three lamps change colour in a move. What happens to the parity of the gold-lamp count?','It switches odd/even','It always stays the same','An odd number of flips changes parity, regardless of how many flips add or remove gold.'),
 c('A counter starts at 8. Moves add 6 or subtract 9. Can it reach 10?','No','Yes','The start leaves remainder two modulo three; the target leaves remainder one.'),
 c('A proposed invariant fails for one legal move. Is it usable as an invariant?','No','Yes, if it usually holds','It must be preserved by every allowed move.'),
 c('A target passes your invariant test. Does that alone prove it is reachable?','No: a construction may still be needed','Yes: the test guarantees a route','An invariant can rule out a target; passing it is only a necessary condition.')];
 case 'DIV-05':return [
 c('To find the units digit of a huge power, what is useful first?','A cycle of units digits','The full power','The last digits often repeat long before the full numbers do.'),
 c('Powers of 2 end 2,4,8,6,… . Which last digit belongs to exponent 4?','6','2','Count the cycle from exponent one.'),
 c(`Powers of 3 have a four-step last-digit cycle. For exponent ${4*n+1}, which cycle position matters?`,'First','Fourth','The exponent leaves remainder one after complete groups of four.'),
 c('An exponent is divisible by 4 in a four-step cycle starting at exponent 1. Which entry is used?','The fourth entry','An extra zero entry','Remainder zero means a completed cycle, not exponent zero.'),
 c('Two large powers end in 7 and 8. What does their sum end in?','5','15','Add the last digits, then retain only the units digit.')];
 case 'FRAC-01':return [
 c('Half a tank is used, then a third of what remains. The second fraction refers to…','The remaining half-tank','The original full tank','The words “what remains” change the whole.'),
 c(`A box has ${12*n} counters. A third are removed. How many remain?`,8*n,4*n,'One third is removed, so keep two thirds.'),
 c('Half an amount remains, then half of that is kept. Fraction of the original kept?','1/4','0','Multiply the retained fractions; do not subtract two halves of different wholes.'),
 c('After a quarter of an amount is spent, 18 remains. Recover the amount by…','18 ÷ 3/4','18 ÷ 1/4','The remainder represents three quarters, not the quarter spent.'),
 c('A garden receives half the seeds, then another receives a third of the remainder. Which fraction of the original is left?','1/3','1/6','Keep 1/2, then 2/3 of that: 1/2 × 2/3 = 1/3.')];
 case 'FRAC-02':return [
 c('Red:blue is 2:5. How many equal parts are in the total?','7','3','Add ratio parts for a total; subtract them for a difference.'),
 c(`Oats:seeds is 5:3. Oats exceed seeds by ${2*n} grams. One part weighs…`,n,2*n,'The difference is two parts, so divide the difference by two.'),
 c('A 3:4 mix contains 12 units of the first ingredient. How much of the second?','16','9','Three parts represent twelve, so each part is four.'),
 c('Only blue paint is added to a blue:white mix. Which quantity anchors the comparison?','The unchanged white amount','The unchanged total','Adding blue changes the total, but not the amount of white.'),
 c('Blue:white is 2:5 with 6 mL blue. To make 1:1 by adding blue, add…','9 mL','3 mL','White is 15 mL. Blue must increase from 6 to 15.')];
 case 'FRAC-03':return [
 c('A price rises by 20%. What is the percentage based on?','The price before the rise','The price after the rise','Name the base before calculating a percentage change.'),
 c(`A $${20*n} kit is discounted by 25%. The amount paid for the kit is…`,15*n,5*n,'A 25% discount leaves 75% to pay.'),
 c('A price rises 20%, then falls 20%. Does it return to its original value?','No','Yes','The second change acts on a larger base: 1.2 × 0.8 = 0.96.'),
 c('A club goes from 40 members to 50. Returning to 40 requires a decrease of…','20% of 50','25% of 50','The decrease is 10 out of the new 50.'),
 c('A $7 delivery charge is added after a 10% discount. Which calculation fits an $80 item?','80 × 0.9 + 7','87 × 0.9','Only the item price is discounted; the charge comes afterwards.')];
 case 'FRAC-04':return [
 c('Half of 10 children and a quarter of 20 adults wear hats. What should be combined first?','The numbers wearing hats','The two fractions directly','The fractions refer to groups of different sizes.'),
 c('A third of 18 and a half of 8 are selected. Total selected?','10','13','Convert each fraction into a count: 6 + 4.'),
 c('Two groups contain 12 and 8 people. A fraction of everyone must use which denominator?','20','2','The whole is the combined population, not the number of groups.'),
 c('Two groups have equal size. Is averaging their selected fractions valid?','Yes','No','Equal group sizes give equal weight. This shortcut fails for unequal sizes.'),
 c('Of 30 bottles, 12 are empty. What fraction are full?','3/5','2/5','Eighteen are full. The question asks for the complement of the empty fraction.')];
 case 'RATE-01':return [
 c(`A bell rings ${n+2} times. How many gaps are there from first ring to last?`,n+1,n+2,'There is no waiting interval before the first ring in the measured span.'),
 c('Five posts are 6 metres apart. Distance from first to last?','24 metres','30 metres','Five posts create four intervals.'),
 c('A sensor records immediately and every 8 seconds. Time of its fourth reading?','24 seconds','32 seconds','The readings occur at 0, 8, 16 and 24 seconds.'),
 c('A rover covers 36 metres in 12 seconds. What is its speed?','3 metres per second','3 seconds per metre','Distance divided by time gives metres per second; the units identify the quantity.'),
 c('Two timers take 8 and 6 readings at 5-second intervals, starting with an immediate reading. Difference between their durations?','10 seconds','15 seconds','They have seven and five gaps, a difference of two gaps.')];
 case 'RATE-02':return [
 c('A tap fills a tank in 6 hours. Its rate is…','1/6 tank per hour','6 tanks per hour','Divide one whole job by the time needed.'),
 c('Two workers act together at steady independent rates. What should be added?','Their rates','Their completion times','In each hour they contribute fractions of the same job.'),
 c('A pump adds 5 L/min while a leak removes 2 L/min. Net rate?','3 L/min','7 L/min','Opposing flows subtract.'),
 c('Together two machines make 18 parts/hour. One makes 7. The other makes…','11 parts/hour','25 parts/hour','Subtract the known contribution from the combined rate.'),
 c('A machine makes 8 parts/hour. Time for 24 parts?','3 hours','192 hours','Time is required work divided by rate.')];
 case 'RATE-03':return [
 c('Speed is in km/h; time is 15 minutes. Which time fits the distance calculation?','1/4 hour','15 hours','Use compatible units before multiplying.'),
 c(`Travel at ${4*n} km/h for 30 minutes. Distance?`,`${2*n} km`,`${8*n} km`,'Thirty minutes is half an hour.'),
 c('A journey includes a ten-minute stop. The stop adds…','Time but no distance','Distance but no time','Stopped time matters for a whole-journey average.'),
 c('Equal distances are travelled at different speeds. Whole-trip average speed is…','Total distance ÷ total time','Always the mean of the speeds','The slower speed is used for longer, so equal weighting is usually wrong.'),
 c('A return trip covers 12 km in 2 hours and 12 km in 1 hour. Average speed?','8 km/h','9 km/h','The whole trip is 24 km in 3 hours.')];
 case 'RATE-04':return [
 c('Walkers approach each other at 3 and 2 km/h. Gap-closing speed?','5 km/h','1 km/h','Both movements reduce the gap, so add speeds.'),
 c('A runner chases another moving in the same direction at 7 and 4 m/s. Gap-closing speed?','3 m/s','11 m/s','The front runner keeps moving away, so subtract speeds.'),
 c(`A gap of ${3*n} metres closes at 3 m/s. Catch-up time?`,`${n} seconds`,`${9*n} seconds`,'Time equals gap divided by the rate at which it closes.'),
 c('Two runners start together around a circular track. For their first meeting after the start, count time zero?','No','Yes','The wording excludes the starting instant.'),
 c('Opposite-direction runners on a 60-metre track have speeds 2 and 4 m/s. Time between meetings?','10 seconds','30 seconds','Together they close one full track length at 6 m/s.')];
 case 'ALG-01':return [
 c('A workshop charges $8 entry and $3 per model. Which model fits m models?','8 + 3m','8m + 3','The entry fee occurs once; the model charge repeats.'),
 c('Three identical pens and a $5 book cost $20. Remove what first?','$5','$20 ÷ 3','Separate the fixed item before dividing among the pens.'),
 c('Tickets cost $9 adult or $5 child. A useful baseline for 8 tickets is…','Pretend all 8 are child tickets','Pretend there are 8 of each type','The baseline must preserve the known total number of tickets.'),
 c('Replacing one $5 child ticket by a $9 adult ticket increases the total by…','$4','$9','The adult replaces a child ticket already counted in the baseline.'),
 c('A proposed answer fits the cost but gives the wrong number of tickets. Accept it?','No','Yes','Both the total count and the cost are constraints.')];
 case 'ALG-02':return [
 c('Two piles total 30 and differ by 6. To find the smaller, use…','(30 − 6) ÷ 2','30 ÷ 2 − 6','Remove the extra part, leaving two equal smaller piles.'),
 c('Two weights total 34 and differ by 8. The larger is…','21','13','The larger is (total + difference)/2; 13 is the smaller.'),
 c('An answer gives piles 8 and 14 for total 22, difference 6. Which check matters?','Both sum and difference','Only the sum','Checking both conditions verifies the model and the arithmetic.'),
 c('After 3 cm is cut off the longer rope, it is 5 cm longer. Original difference?','8 cm','2 cm','Restore the removed amount before applying the original total.'),
 c('Two whole-number counts total 25 and differ by 4. Can both conditions hold?','No','Yes','They would be (25−4)/2 and (25+4)/2, not whole numbers.')];
 case 'ALG-03':return [
 c('2 boxes + 3 lamps and 2 boxes + 5 lamps have known costs. What cancels when subtracting?','The two boxes','All the lamps','Subtract equal contributions to isolate the changed part.'),
 c('The second purchase above costs $18 more. One extra lamp costs…','$9','$18','The difference buys two extra lamps.'),
 c('One equation has 3 jars; another has 6. What can make jar contributions match?','Double the first equation','Add 3 to its total only','Scaling an equation means multiplying every term on both sides.'),
 c('After doubling 3 jars + 2 mugs, the result contains…','6 jars + 4 mugs','6 jars + 2 mugs','Both item counts must be scaled.'),
 c('A recovered price satisfies the first purchase. What is the next check?','Substitute into the second too','Stop: one equation is enough','Elimination used both conditions; the answer must satisfy both.')];
 case 'ALG-04':return [
 c('Multiply by 3, add 8, then halve. Which operation is undone first?','The halving','The multiplication by 3','Undo the final operation first.'),
 c(`A number is tripled and becomes ${3*n}. Undo this by…`,'Dividing by 3','Subtracting 3','The inverse of multiplication is division.'),
 c('Spend $6, then finish with $14. What was the starting amount?','$20','$8','Working backwards restores what was spent.'),
 c('Half the remaining amount is spent, leaving $12. What was there immediately before that spend?','$24','$6','The final amount is one of two equal halves.'),
 c('You worked backwards to a starting value. Best final check?','Run the original actions forwards','Repeat the same backwards arithmetic only','A forward check tests the order and each inverse operation.')];
 case 'ALG-05':return [
 c('Move one counter from a larger pile to a smaller pile. How does their gap change?','It decreases by 2','It decreases by 1','One pile loses one while the other gains one.'),
 c('Piles differ by 10. How many transfers make them equal?','5','10','Each transfer closes two units of the gap.'),
 c('Counters move between two piles. Which quantity stays fixed?','The combined total','Each pile’s size','Transfers redistribute counters without adding or removing them.'),
 c('Two piles total 36. Their final ratio is 2:1. The smaller final pile is…','12','18','Equality is not the target here; use three ratio parts.'),
 c('A pile starts at 7 and must finish at 12 through transfers into it. How many arrive?','5','19','Find the change in that pile, then check the other loses the same amount.')];
 case 'SEQ-01':return [
 c('A pattern starts at 7 and gains 4 each stage. How many increases lead to stage 6?','5','6','Stage one already contains the starting amount.'),
 c(`Term 1 is ${n}; each later term adds 3. Term 4 is…`,n+9,n+12,'Three increases separate the first and fourth terms.'),
 c('To total 4 + 7 + 10 + 13, which pairing helps?','4+13 and 7+10','4+7 and 10+13','Pairing opposite ends creates equal pair totals.'),
 c('A pattern increases by the same amount each time. Which model fits?','Add a fixed amount','Multiply by a fixed factor','Constant differences identify arithmetic growth.'),
 c('Stage 1 uses 6 blocks. Each new stage adds 4. Which stage uses 26 blocks?','Stage 6','Stage 5','The increase of 20 is five increments, so add one for the starting stage.')];
 case 'SEQ-02':return [
 c('A population doubles each hour. The change is…','A fixed multiplier','A fixed extra number','Doubling depends on the current population.'),
 c(`Start with ${n} cells at hour zero. After three doublings there are…`,8*n,6*n,'Three doublings multiply by 2 × 2 × 2, not by 2 × 3.'),
 c('Payments are 3,6,12,24. Total earned after four payments?','45','24','Distinguish the last term from the running total.'),
 c('A total is exactly 63 after six rounds. The question asks when it first exceeds 63. Is six enough?','No','Yes','Strictly exceeds rules out equality.'),
 c('For 1+2+4+8, doubling the sum and subtracting the original leaves…','16 − 1','16 + 1','The middle terms cancel; the unmatched terms are the next power and the initial one.')];
 case 'SEQ-03':return [
 c('Routes use jumps of 1 or 3. Splitting by the last jump gives earlier lengths…','k−1 and k−3','k−1 and k−2','The permitted moves determine the recurrence.'),
 c('A route has length zero. How many sequences reach it without moving?','1 empty sequence','0','This base case makes the count for a single final jump work correctly.'),
 c('Binary lamp rows cannot have adjacent ON lamps. If the last lamp is ON, the previous lamp must be…','OFF','ON','Respect the local restriction before reducing to a smaller row.'),
 c('Two recurrence cases describe different final moves. Should their counts be added or multiplied?','Added','Multiplied','The alternatives are disjoint routes, not sequential choices within one route.'),
 c('A recurrence fits three examples. What makes it reliable for later lengths?','Every route belongs to exactly one case','The next value looks plausible','Explain completeness and non-overlap; a pattern alone is not a proof.')];
 case 'SEQ-04':return [
 c('Instructions repeat Right, Right, Up, Left. Does the position return after one block?','No','Yes','The instructions repeat, but the block still moves one right and one up.'),
 c('A four-step cycle runs for 19 moves. Split this into…','4 full cycles and 3 moves','3 full cycles and 4 moves','Use quotient and remainder, with the remainder smaller than four.'),
 c('A display changes every 3 seconds and a lamp toggles every 2. Full-state repeat period?','6 seconds','3 seconds','Both components must return together.'),
 c('A pointer starts north at move zero, then turns clockwise. After one move?','East','North','Anchor the indexing at the stated initial time.'),
 c('A repeated instruction block moves a robot two metres. After five blocks, can displacement be ignored?','No: it has accumulated 10 metres','Yes: the instructions reset','A cycle in instructions is different from a cycle in complete state.')];
 case 'COUNT-01':return [
 c('Pairs are unordered. Are (2,7) and (7,2) two different outcomes?','No','Yes','Swapping the names of an unordered pair does not create another pair.'),
 c('To list positive pairs adding to 13, which convention avoids duplicates?','Write the smaller number first','Write both orders','Each pair then has one unique entry in the list.'),
 c('Triples are unordered. Which condition is useful for listing?','a ≤ b ≤ c','a, b and c must be different','Sorting prevents repeated permutations without wrongly excluding equal entries.'),
 c('Two different positive numbers add to 10. Is (5,5) allowed?','No','Yes','The word different excludes the equal pair.'),
 c('A list finds five valid cases. What is still needed to establish the total?','A reason no other cases exist','One more example','A systematic stopping rule turns a sample into an exhaustive count.')];
 case 'COUNT-02':return [
 c('Captain and deputy are chosen. Does swapping them make a different selection?','Yes','No','The roles are distinct.'),
 c('Two pupils form a team with no roles. Does swapping their order change the team?','No','Yes','Only membership matters.'),
 c(`Choose a captain and deputy from ${x} pupils. The count starts with…`,`${x} × ${x-1}`,`${x} × ${x}`,'The same pupil cannot hold both roles.'),
 c('Ordered pairs count each two-person team twice. Correct the count by…','Dividing by 2','Subtracting 2','Every team appears in two orders, not just two extra teams overall.'),
 c('Choose an unordered pair of dishes and one dessert. Combine the pair count and dessert count by…','Multiplying','Adding','Each dish pair can be followed by any dessert choice.')];
 case 'COUNT-03':return [
 c('A and B must be neighbours in a row. Useful first representation?','Treat AB as one block','Fix A at the left end','A block preserves all possible positions of the pair.'),
 c('The AB block can have how many internal orders?','2','1','Both AB and BA satisfy adjacency unless another rule forbids one.'),
 c('A and B must NOT be neighbours. A useful count is…','All rows minus adjacent rows','All rows minus two rows','There are many possible adjacent arrangements.'),
 c('Five numbered positions hold two identical sensors. Adjacent position pairs number…','4','5','Adjacent pairs correspond to the four gaps between positions.'),
 c('One magnet is fixed first before arranging the others. Should it remain a free choice in the factorial?','No','Yes','Apply the fixed-position restriction before counting the remaining arrangements.')];
 case 'COUNT-04':return [
 c('12 play chess, 9 play music, 4 do both. At least one activity means…','12 + 9 − 4','12 + 9 + 4','The overlap was counted twice, so remove one copy.'),
 c('There are 25 people and 17 do at least one activity. How many do neither?','8','17','Neither is the complement within the whole group.'),
 c('A question says chess OR music, but NOT both. The overlap must be subtracted…','Twice from the sum of group sizes','Once from that sum','The sum counts the overlap twice; neither copy should remain.'),
 c('Multiples of 2 and multiples of 3 overlap at multiples of…','6','5','Being in both groups means being a common multiple.'),
 c('Bad routes pass through A or B. A route through both was subtracted twice. What correction is needed?','Add it back once','Subtract it once more','Inclusion–exclusion ensures each forbidden route is removed only once.')];
 case 'COUNT-05':return [
 c('Each bridge joins two islands. Adding all island degrees counts each bridge…','Twice','Once','A bridge contributes one endpoint at each island.'),
 c('The degree sum is 18. Number of bridges?','9','18','Divide endpoint reports by two.'),
 c('A proposed network has total degree 13. Can it exist?','No','Yes','The sum must be twice an integer number of edges.'),
 c('12 people each join 2 workshops. Total person–workshop memberships?','24','6','Count each membership once from its person.'),
 c('Those 24 memberships are spread across workshops of 6 people. Number of workshops?','4','12','Now count the same memberships from the workshop side.')];
 case 'COUNT-06':return [
 c('A code has exactly one 2. Which case split is useful?','Which position contains the 2','Whether it contains a 2','The second description does not divide the valid possibilities into useful cases.'),
 c('Two digits must include exactly one 1. Is 11 allowed?','No','Yes','Exactly one excludes two occurrences.'),
 c('Three-position codes use digits 1–4, with exactly one 2. How many choices for each other position?','3','4','The other positions must avoid 2.'),
 c('A counting case appears in two groups. Can their totals simply be added?','No','Yes','Overlapping cases require a correction or a disjoint reclassification.'),
 c('You divide possibilities into cases. Which pair of checks is essential?','No overlaps and no missing cases','Equal-sized cases and equal answers','Case sizes can differ; completeness and uniqueness of classification matter.')];
 case 'LOGIC-01':return [
 c('A label says “The key is not in box 1”. If the key is in box 1, the label is…','False','True','Evaluate the whole statement for a specified situation.'),
 c('Exactly one of two labels must be true. A candidate makes both false. Keep it?','No','Yes','Exactly one excludes zero as well as two.'),
 c('A robot always lies. Its statement says both robots lie. If that statement is false, what follows?','At least one robot tells the truth','Both robots tell the truth','The negation of “both lie” is “not both lie”, not “both are truthful”.'),
 c('A candidate fits one label. What should be tested next?','Every remaining statement','Only the next plausible label','All truth conditions must hold simultaneously.'),
 c('Three key locations are possible. Why make a small truth table?','It checks every location consistently','It allows skipping an awkward case','Organised cases prevent guessing from one attractive statement.')];
 case 'LOGIC-02':return [
 c('A number is odd AND divisible by 3. A candidate is odd but not divisible by 3. Keep it?','No','Yes','AND requires both conditions.'),
 c('A whole number is strictly between 10 and 15. Is 15 a candidate?','No','Yes','Strict inequalities exclude the endpoints.'),
 c('To find a number in a short interval with two remainder conditions, begin by…','Listing candidates meeting one condition','Choosing the middle number','A constrained list is complete; a guess need not satisfy either condition.'),
 c('A digit solution works numerically but repeats two digits when repeats are forbidden. Accept it?','No','Yes','Check the domain and distinctness rules as well as the equations.'),
 c('One candidate works. To prove it is the only one, you need…','To rule out the other allowed candidates','To check it again','Existence and uniqueness are different claims.')];
 case 'LOGIC-03':return [
 c('A table’s row totals sum to 43. What must its column totals sum to?','43','It depends on the number of columns','Both groupings count the same entries once.'),
 c('Rows total 18 and 24; the first column totals 15. Other column total?','27','57','The grand total is 42; subtract the known column.'),
 c('One table entry increases by 6. How much does the grand total change?','6','12','It appears in a row and a column, but is still only one entry.'),
 c('If a table’s row totals sum to 40 and its column totals sum to 41, can all totals be correct?','No','Yes','The two views must describe the same grand total.'),
 c('A missing column total is requested. Must every individual entry be found first?','No','Yes','The grand-total relationship can reveal the missing aggregate directly.')];
 case 'LOGIC-04':return [
 c('One arrangement works. What has been proved?','That a solution exists','That it is the only solution','An example establishes possibility, not uniqueness.'),
 c('Two positive integers have a fixed product. Which list can prove uniqueness with an extra clue?','All factor pairs','A few nearby numbers','Factor pairs exhaust the possible positive integer pairs.'),
 c('A claim says every case works. What can disprove it?','One legal counterexample','One supporting example','A universal claim fails as soon as one allowed case fails.'),
 c('A maximum of 12 is claimed. Which evidence completes a proof?','No result exceeds 12, and 12 is attainable','Several results are below 12','Both an upper bound and a construction are required.'),
 c('A proof quietly excludes equal values, but the question permits them. Is it complete?','No','Yes','The proof must cover the entire stated domain, including boundary cases.')];
 case 'GEO-01':return [
 c('Two shapes join along a 4-cm side. What changes in their combined outside perimeter?','Subtract 8 cm from separate perimeters','Subtract 4 cm','The shared side was counted once on each shape and becomes internal.'),
 c('A corner square is cut from a rectangle. What should you compare for perimeter?','Deleted edges and newly exposed edges','Only the removed area','Boundary length and area measure different things.'),
 c('A 2-cm-wide notch goes 3 cm inward from a straight edge. Perimeter increase?','6 cm','12 cm','The 2-cm opening is replaced by a 2-cm back edge; only the two 3-cm sides add net length.'),
 c('A perimeter answer should use…','cm','cm²','Perimeter measures length, not area.'),
 c('A diagram has an internal join. Should it count toward the outside perimeter?','No','Yes','Trace only the exposed boundary of the whole shape.')];
 case 'GEO-02':return [
 c('For triangle area, the height must be…','Perpendicular to the chosen base','Any sloping side','Area uses perpendicular distance to the base line.'),
 c('A triangle has base 10 and height 6. Area?','30','60','A triangle occupies half the corresponding base-by-height rectangle.'),
 c('Slide a triangle’s top vertex parallel to its base, keeping its height fixed. Its area…','Stays the same','Must increase','The base and perpendicular height remain unchanged.'),
 c('A triangle uses a rectangle’s entire bottom side and a vertex on its top side. Fraction of rectangle outside it?','1/2','1/3','The triangle has the same base and height as the rectangle, so takes half its area.'),
 c('Two triangles share a base; one has triple the height. Their area ratio is…','3:1','9:1','With only height scaled, area scales by that same factor.')];
 case 'GEO-03':return [
 c('Two angles form a straight line. Their total is…','180°','360°','A straight angle is a half-turn.'),
 c('Angles around a point fill a complete turn. Their total is…','360°','180°','A full turn is 360 degrees.'),
 c('A triangle has angles 45° and 65°. Its third angle is…','70°','110°','Subtract both known angles from 180 degrees.'),
 c('An exterior angle is 120°. The adjacent interior angle is…','60°','120°','They form a straight line and add to 180 degrees.'),
 c('A drawing looks like it has two equal angles, but gives no equality marks or facts. May equality be assumed?','No','Yes','Use stated or proved relationships; sketches need not be to scale.')];
 case 'GEO-04':return [
 c('A rotation preserves an outline but swaps red and blue markings. Is it a colour-preserving symmetry?','No','Yes','Every marked feature must match, not just the outline.'),
 c('A regular hexagon has no markings. Does a 60° turn preserve it?','Yes','No','A one-vertex-step rotation maps an unmarked regular hexagon onto itself.'),
 c('Its vertices are alternately blue and gold. Does that same 60° turn preserve colours?','No','Yes','One step swaps colours; two steps restore them.'),
 c('A reflection and a rotation are…','Different transformations','Always interchangeable','Reflection reverses orientation; rotation turns the shape.'),
 c('One vertex is uniquely red. A valid reflection must…','Keep that red vertex in place','Move it to any corner','A unique marking must map to itself.')];
 case 'GEO-05':return [
 c('You find a rectangle of area 36. Does that alone prove 36 is the largest possible?','No','Yes','An example proves attainment; a bound must exclude larger areas.'),
 c('Positive side lengths have sum 10. Which pair gives greater area?','5 and 5','2 and 8','Balanced factors give 25 instead of 16.'),
 c('A pen uses a wall for one side. With width w and length l, the fence needed is…','2w + l','2w + 2l','The wall replaces one length of fence.'),
 c('The best real-number side length is 4.5, but whole numbers are required. What next?','Check the permitted neighbouring integers','Use 4.5 anyway','Optimise within the allowed domain.'),
 c('A bound is 50, but your construction reaches only 48. Have you proved a maximum of 50?','No','Yes','The bound may not be attainable; a sharp result needs matching evidence.')];
 case 'SOLID-01':return [
 c('A solid block is 4 cubes wide, 3 deep and 2 high. Cubes inside it count…','Even when hidden','Only if visible','Volume includes all unit cubes, not just visible faces.'),
 c('One layer contains 12 cubes and there are 5 equal layers. Total?','60','17','Multiply the number per layer by the number of layers.'),
 c('A model has layers of 12, 8 and 3 cubes. Total?','23','36','Unequal layers must be counted separately and added.'),
 c('A 1-by-2 tunnel passes through 7 layers. Cubes removed?','14','7','Each cross-section removes two cubes.'),
 c('A picture could show a hollow or a solid model. What determines the count?','The stated construction','Assuming everything unseen is filled','Hidden structure must come from the conditions, not a guess about the drawing.')];
 case 'SOLID-02':return [
 c('A cube is painted on all outer faces. A corner unit cube has how many painted faces?','3','2','Three outer planes meet at a corner.'),
 c('Which cubes have exactly two painted faces in a fully painted cuboid?','Edge cubes excluding corners','All edge cubes including corners','Corners have three, so they belong in a different category.'),
 c('An edge is 7 cubes long. How many are not its two corners?','5','7','Remove both endpoints.'),
 c('Only the top and bottom faces of a four-layer block are painted. Can a small cube touch both painted faces?','No','Yes','The top and bottom layers are disjoint when the height exceeds one.'),
 c('The painting instructions change. Can the same face-count formula always be reused?','No','Yes','Reclassify using the faces that are actually painted.')];
 case 'SOLID-03':return [
 c('An open-topped cuboid has how many rectangular material faces?','5','6','There is a base and four sides, but no lid.'),
 c('Surface area uses which units?','Square centimetres','Cubic centimetres','It adds areas of faces, not enclosed volume.'),
 c('A cuboid is cut once into two pieces. How many new exposed faces does the cut make?','2','1','Each piece has one face along the cut.'),
 c('Cutting a solid without removing material changes its total volume…','Not at all','By the area of the cut','Volume is conserved while surface area can increase.'),
 c('A box net is being measured. What should be added?','The areas of all included faces','The lengths of all face edges','A net unfolds surface area; edge length would answer a different question.')];
 case 'SPATIAL-01':return [
 c('A shortest route needs 3 Right and 2 Up moves. Total moves?','5','6','The required horizontal and vertical changes add.'),
 c('A compulsory waypoint divides a route into two sections. Combine their route counts by…','Multiplying','Adding','Each route to the point can be paired with each valid route from it.'),
 c('A waypoint is forbidden. Which strategy can help?','All routes minus routes through it','All routes minus one','One blocked point can invalidate many complete routes.'),
 c('A grid point can be reached from its left or below. Its route count is…','The sum of those incoming counts','Their product','Those final approaches are alternative routes.'),
 c('Two blocked points can occur on the same route. What needs attention when subtracting?','The overlap of the two bad-route sets','Only the order of subtraction','A route through both would otherwise be removed twice.')];
 case 'SPATIAL-02':return [
 c('How many vertical boundaries define a rectangle?','2','4','Choose its left and right boundaries, then its horizontal pair.'),
 c('A grid has 4 vertical lines. How many pairs of vertical boundaries?','6','4','There are 4 × 3 ordered pairs; halve because order does not matter.'),
 c('Three horizontal lines offer how many top–bottom pairs?','3','2','Adjacent and non-adjacent pairs both define rectangles.'),
 c('Each vertical pair can combine with each horizontal pair. Use…','Multiplication','Addition','A rectangle needs one choice of each type.'),
 c('A new vertical line is added. Every newly created rectangle must use…','The new line as a boundary','Two entirely old vertical boundaries','Old boundary choices already existed before the new line arrived.')];
 case 'SPATIAL-03':return [
 c('A domino covers two squares. Can an odd number of squares be fully covered?','No','Yes','Every domino contributes an even area.'),
 c('On a checkerboard, an edge-adjacent domino covers…','One square of each colour','Two squares of the same colour','Moving one square horizontally or vertically switches colour.'),
 c('Removing two squares of the same colour leaves unequal colour totals. Can dominoes tile the remainder?','No','Yes','Every domino preserves equality of covered colour counts.'),
 c('The remaining black and white counts are equal. Does that alone guarantee a tiling?','No','Yes','Colour balance is necessary, but geometry can create other obstructions.'),
 c('To prove a particular board CAN be tiled, the strongest finishing step is…','Give a complete valid tiling','Show its area is even','A construction proves sufficiency; an even area alone does not.')];
 case 'SPATIAL-04':return [
 c('A trail must use every edge once. May it revisit a vertex?','Yes','No','The no-repeat rule concerns edges, not necessarily vertices.'),
 c('In a connected graph, a closed trail using every edge once needs…','Every vertex degree even','Exactly two odd degrees','Arrivals and departures pair at every vertex on a closed trail.'),
 c('A connected graph has exactly two odd-degree vertices. A full edge trail must start and finish…','At the two odd vertices','At any two vertices','Only the endpoints can have an unmatched arrival or departure.'),
 c('All degrees are even, but two edge-containing components are disconnected. Can one trail cover everything?','No','Yes','The degree test also requires the relevant edges to be connected.'),
 c('A drawn crossing has no junction according to the rules. Can a route switch lines there?','No','Yes','Connections come from the stated network, not just intersecting ink.')];
 case 'DATA-01':return [
 c('A probability ratio uses equally likely outcomes. Which group belongs in the denominator?','All currently possible outcomes','Only favourable outcomes','The denominator represents the whole sample space.'),
 c('A bag has 3 gold and 5 blue tokens. Chance of gold?','3/8','3/5','Count gold out of all eight tokens.'),
 c('A gold token is drawn and not replaced. For the next draw, use…','2 gold among 7 tokens','3 gold among 8 tokens','Both the favourable count and total have changed.'),
 c('You are told a chosen number is divisible by 3. Your new sample space contains…','Only the allowed multiples of 3','All the original numbers','Condition on the information before calculating the next probability.'),
 c('Two independent coin flips give HH, HT, TH, TT. Are “two heads”, “one head”, “no heads” equally likely?','No','Yes','One head has two underlying outcomes, while the other categories have one each.')];
 case 'DATA-02':return [
 c(`The mean of ${n} values is 8. Their total is…`,8*n,`${n} ÷ 8`,'Mean multiplied by count recovers the total.'),
 c('Groups of 2 and 8 have different means. To find the combined mean, start with…','Their totals and counts','The unweighted mean of the two means','The larger group must contribute more weight.'),
 c('A recorded 19 should have been 9. What changes in the total?','Subtract 10','Subtract 9','Replace the wrong entry: remove nineteen and add nine.'),
 c('Correcting one value without removing it changes the count…','Not at all','By one','The number of observations stays the same.'),
 c('Four scores average 10. A fifth score of 20 is added. New mean?','12','15','The new total is 60 across five scores.')];
 case 'DATA-03':return [
 c('A full picture represents 6 bikes. A half-picture represents…','3 bikes','Half a bike','Read the chart key before converting symbols into quantities.'),
 c('A chart baseline is 40. A bar rises 12 above it. Represented value?','52','12','Add the baseline when reading an absolute value.'),
 c('Two bars share baseline 40 and rise 8 and 13. Difference in values?','5','45','The common baseline cancels when subtracting.'),
 c('The same two bars represent values 48 and 53. Their sum is…','101','21','The baseline cancels for a difference, but not for a sum.'),
 c('A graph asks for the total number of pupils. The vertical axis is a percentage. What else is needed?','A population count or equivalent clue','Only the tallest bar','Percentages alone do not determine the number of people.')];
 default:throw Error('Missing flash-card technique: '+id);
 }
}

export function investigationCards(id,visit=1){
 const c=(q,yes,no,why)=>({q,yes:String(yes),no:String(no),why});
 switch(id){
 case 'M01':return [
 c('A two-digit number AB means…','10A + B','A + B','Place value is what changes when the digits reverse.'),
 c('Reverse AB to BA. The difference AB − BA simplifies to…','9(A − B)','9(A + B)','Subtract 10B + A from 10A + B and collect the two digit contributions.'),
 c('Reversing 640 gives which three-place display?','046','406','Reverse positions exactly, keeping a leading zero for comparison.'),
 c('In ABC − CBA, which digit contribution cancels?','The middle digit B','The first digit A','The tens contribution 10B occurs equally in both numbers.'),
 c('Several examples have a middle digit of 9 after subtraction. What establishes the general claim?','An argument for every allowed outer-digit difference','Testing one more starting number','Expressing the difference as 99 times a digit difference explains all the cases.')];
 case 'M02':return [
 c('A 4-by-4 square grows to 5-by-5. Added squares?','9','1','The difference in areas is 25−16, an odd border strip.'),
 c('1 + 3 + 5 + 7 forms which square total?','16','49','The first four odd strips build a 4-by-4 square.'),
 c('Five consecutive odd numbers have middle value 25. Their total?','125','25','Pairs around the centre balance; the mean is 25 across five terms.'),
 c('To prove a rule for every positive n, are four matching examples enough?','No','Yes','Examples suggest a rule; a general area or pairing argument establishes it.'),
 c('A one-square border surrounds a 6-by-6 square. Its outer dimensions are…','8 by 8','7 by 7','The border adds one square on both sides of each dimension.')];
 case 'M03':return techniqueCards('DIV-02',visit);
 case 'M04':return techniqueCards('COUNT-03',visit);
 case 'M05':return [
 c('Three points chosen on one straight line make a triangle?','No','Yes','A non-degenerate triangle needs points that are not all collinear.'),
 c('Points lie on two parallel lines. Every triangle uses…','Two on one line and one on the other','One point from each of three lines','There are exactly two lines, so these two distributions exhaust the cases.'),
 c('Choose two upper points from four. Does their selection order matter?','No','Yes','The same two vertices produce the same triangle whichever is selected first.'),
 c('There are 6 choices of upper pair and 3 lower points. Triangles of this type?','18','9','Each pair combines with any lower point, so multiply.'),
 c('A point is removed. Which triangles disappear?','Exactly those containing that point','All triangles on its line','Classifying by membership of the removed point avoids recounting every surviving triangle.')];
 case 'M06':return techniqueCards('SPATIAL-01',visit);
 case 'M07':return [
 c('Rays from one point cross parallel levels. A triangle uses how many rays?','Two','Three','Two rays supply its sides and one level supplies its base.'),
 c('Can two parallel levels be two sides of the same triangle?','No','Yes','They do not meet, so cannot enclose a triangle with a single third side.'),
 c('Four rays offer how many pairs?','6','4','Choose two distinct rays; order does not matter.'),
 c('Each ray pair crosses 3 possible base levels. Combine the counts by…','Multiplication','Addition','Each pair can form a triangle with each of the levels.'),
 c('A new parallel level is added. New triangles correspond to…','All ray pairs using that new base','All pairs of levels','The new feature supplies a base, not a second parallel triangle side.')];
 case 'M08':return [
 c('Two semicircles of equal radius together have the area of…','One full circle','Two full circles','Each contributes half a circle.'),
 c('A rectangle has an outward semicircle on each short end. Do the shared diameters count in its outside perimeter?','No','Yes','Those straight joins are inside the combined shape.'),
 c('The semicircles have radius 3. The rectangle between them has height…','6','3','Each short side is a diameter, twice the radius.'),
 c('The rectangle length is 10 and the end radii are 2. Overall width?','14','12','The shape extends one radius beyond each end of the rectangle.'),
 c('Every length doubles. The area becomes…','Four times as large','Twice as large','Area scales in two dimensions; perimeter scales in one.')];
 case 'M09':return [
 c('A quarter-circle of radius r has area…','πr²/4','πr/4','Use one quarter of circle area, with squared radius.'),
 c('Its curved boundary has length…','πr/2','πr²/4','One quarter of circumference 2πr is πr/2; area is a different quantity.'),
 c('A quarter-circle is cut from a square corner. What happens to the two radius-length straight edges there?','They disappear from the boundary','They stay and the arc is added','The new boundary replaces those edges with the curved cut.'),
 c('Remaining area equals…','Square area minus removed area','Square perimeter minus arc length','Subtract quantities with the same units.'),
 c('Removing material must always reduce perimeter. Is that rule valid?','No','Yes','Cuts can introduce new edges; compare the old and new boundaries.')];
 case 'M10':return [
 c('A disc must move 2 right and 1 up, one square per move. Any route needs at least…','3 moves','2 moves','Each move changes only one coordinate by one.'),
 c('A three-move route is found. What combines with it to prove minimality?','A proof fewer than three is impossible','Another three-move route','A lower bound plus a construction establishes the minimum.'),
 c('A slide is legal only into an empty square. Can a shortest-distance route ignore other discs?','No','Yes','The construction must obey occupancy rules at every step.'),
 c('Four discs each need to leave their initial square. A single move slides only one disc. At least how many moves?','4','1','Each disc contributes an unavoidable move.'),
 c('The lower bound is four, but the only route you found takes five. Is the minimum proved?','No','Yes','The lower bound may be unattainable; matching construction and bound are still needed.')];
 case 'M11':return techniqueCards('SOLID-02',visit);
 case 'M12':return techniqueCards('SPATIAL-03',visit);
 case 'M13':return [
 c('A+B=8 and B+C=6. Which expressions use B as the single free value?','A=8−B and C=6−B','A=8+B and C=6+B','Rearrange each sum before listing candidates.'),
 c('A, B and C are distinct digits. A candidate has A=C. Keep it?','No','Yes','The distinctness rule is independent of the sums.'),
 c('Two assignments fit the first two clues. What does this show?','Those clues do not give uniqueness','Both assignments must be wrong','Several valid candidates mean another clue may be needed.'),
 c('A third clue is introduced. Which candidates are checked?','All survivors of the earlier clues','Only the first survivor','Filter the complete surviving list rather than guessing one.'),
 c('Only one assignment survives every clue. What must still be checked?','Its digits are in the permitted set','That its digits look plausible','The domain restrictions are part of the original problem.')];
 case 'M14':return [
 c('Numbers 1–9 have total 45 and fill three equal-sum rows. Each row totals…','15','45','The three rows partition all nine entries once.'),
 c('A square has equal row and column sums. Is that enough when the rules also require both diagonals?','No','Yes','Every required line must be checked.'),
 c('Add 2 to every entry of a 3-by-3 magic square. Each line total rises by…','6','2','Each line contains three changed entries.'),
 c('A transformed magic square has larger numbers. Can its centre be inferred by undoing the same entry transformation?','Yes','No','The centre is transformed like every other entry.'),
 c('One example has centre 5. Does it prove every valid square must have centre 5?','No','Yes','A general line-sum argument is needed to prove necessity.')];
 case 'M15':return [
 c('There are exactly five coins. Let a,b,c count the three denominations. Which equation is certain?','a+b+c=5','a+2b+5c=5','A count equation counts coins; a value equation weights them by denomination.'),
 c('Start with five 1-unit coins. Replacing one by a 5-unit coin raises the value by…','4','5','The original 1-unit contribution was already counted.'),
 c('Coins are a collection, with no order. Are the same coins written in reverse order a new solution?','No','Yes','Count denomination totals, not listing orders.'),
 c('A calculated denomination count is −1. Is the collection valid?','No','Yes','Counts must be nonnegative whole numbers.'),
 c('To prove all collections were found, a useful organising choice is…','List every possible count of the largest coin','Try random combinations','A bounded case split gives a complete, checkable search.')];
 case 'M16':return techniqueCards('COUNT-05',visit);
 case 'M17':return [
 c('Two queens occupy different rows and columns. Are they necessarily non-attacking?','No','Yes','They may still share a diagonal.'),
 c('On a four-row board, can five non-attacking queens fit?','No','Yes','Two would share a row, by the pigeonhole principle.'),
 c('Two positions share row−column. What do they share?','A diagonal','A column','One diagonal direction has constant row minus column.'),
 c('To check both diagonal directions, compare…','Both row−column and row+column','Only row−column','The other diagonal direction has constant row plus column.'),
 c('Trying one failed placement proves a placement is impossible?','No','Yes','An impossibility proof must rule out all valid candidates or give a general obstruction.')];
 case 'M18':return techniqueCards('GEO-05',visit);
 case 'M19':return [
 c('Players remove 1 or 2 stones; taking the last wins. With 1 stone left, the player to move…','Can win immediately','Must lose','There is a legal move that takes the last stone.'),
 c('From a pile of 3, the first player takes 1 or 2 stones. Can the opponent then win immediately?','Yes','No','If one was taken, take two; if two were taken, take one.'),
 c('To leave a multiple of 3 from a pile of 14, take…','2','1','Fourteen minus two is twelve.'),
 c('The opponent takes k stones, where k is 1 or 2. A reply keeping each pair of turns at 3 stones is…','3−k','3+k','The reply must complement the opponent’s move and remain legal.'),
 c('If taking 1, 2 or 3 is allowed instead, the matching response total becomes…','4','3','The strategy must change with the allowed moves.')];
 case 'M20':return [
 c('A clock has 60 minutes per hour. A total of 68 minutes becomes…','1 hour 8 minutes','6 hours 8 minutes','Carry at the stated base, not at ten.'),
 c('A system has 12 small units per middle unit. A small-unit total of 17 means…','Carry 1; leave 5','Carry 5; leave 1','Divide by twelve to find the whole groups and remainder.'),
 c('If 20 middle units make a large unit, when is a middle-unit carry needed?','When the total reaches 20','When the total reaches 10','Each column may have its own conversion base.'),
 c('A reliable check for mixed-unit addition is…','Convert everything to the smallest unit','Add the written digits as decimals','A single common unit provides an independent arithmetic check.'),
 c('A new robot clock uses 8 ticks per beat. May an old 12-unit carrying rule be reused?','No','Yes','The representation changes, but quotient-and-remainder reasoning transfers.')];
 default:throw Error('Missing investigation flash cards: '+id);
 }
}
export const FLASH_VERSION='decision-cards-v1';
export function flashDeck(id,visit,slot,investigation=false){
 const cards=investigation?investigationCards(id,visit):techniqueCards(id,visit);
 let h=2166136261;for(const c of `${id}:${visit}:${slot}`){h=Math.imul(h^c.charCodeAt(0),16777619)>>>0;}
 // Balanced answer positions with a deterministic shuffled order, stable after reload.
 const order=[0,1,2,3,4];for(let i=4;i>0;i--){h=(Math.imul(h,1664525)+1013904223)>>>0;const j=h%(i+1);[order[i],order[j]]=[order[j],order[i]];}
 const aPositions=new Set(order.slice(0,2+(slot%2)));
 return cards.map((c,i)=>({...c,id:`${FLASH_VERSION}:${id}:${visit}:${i}`,options:aPositions.has(i)?[c.yes,c.no]:[c.no,c.yes],answer:aPositions.has(i)?0:1}));
}
