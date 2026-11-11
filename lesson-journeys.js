// Explicit teaching content; original small examples, not exam questions.
export const journeys = {
  "DIG-01": {
    "id": "DIG-01",
    "hook": "Could you beat a long written calculation by changing it first?",
    "goal": "Calculate accurately by taking numbers apart and compensating.",
    "when": "Look for numbers close to 10, 100 or 1000. Useful for checking an answer as well as finding it.",
    "prerequisite": "Place value; adding and subtracting tens.",
    "starter": "Find 49 + 26 without column addition.",
    "steps": [
      "49 is one less than 50. Replace it with 50 to make an easier sum.",
      "50 + 26 = 76, but we added one too much.",
      "Take that one back: 75. Check that the result is near 50 + 25."
    ]
  },
  "DIG-02": {
    "id": "DIG-02",
    "hook": "Why is 012 different from 102 when counting three-digit numbers?",
    "goal": "Count valid numbers without accidentally allowing a leading zero.",
    "when": "Use this when a digit puzzle says different digits, no repeats, or exactly three digits.",
    "prerequisite": "A digit is one symbol; its position gives its value.",
    "starter": "Make two-digit numbers from 0, 1 and 2 without repeating a digit. How many?",
    "steps": [
      "The first digit is 1 or 2. Zero cannot begin a two-digit number.",
      "After choosing 1, the choices are 10 and 12. After choosing 2, they are 20 and 21.",
      "There are 4 numbers: 2 choices for the first place and 2 for the second."
    ]
  },
  "DIG-03": {
    "id": "DIG-03",
    "hook": "Writing 11 uses one number but two copies of the digit 1. What are we counting?",
    "goal": "Separate counting numbers from counting the digits written inside them.",
    "when": "Use this for page numbers, numbered tickets and repeated-digit counts.",
    "prerequisite": "Tens and units columns.",
    "starter": "How many copies of the digit 1 appear in the numbers 1 to 12?",
    "steps": [
      "The units column contributes a 1 in 1 and 11: two copies.",
      "The tens column contributes a 1 in 10, 11 and 12: three copies.",
      "Add the contributions: 2 + 3 = 5. Counting 11 twice is correct here."
    ]
  },
  "DIG-04": {
    "id": "DIG-04",
    "hook": "A palindrome is a number that reads the same forwards and backwards. How much of it must you choose?",
    "goal": "Use mirrored positions to reduce the number of free choices.",
    "when": "Look for repeated digits, mirrored digits or numbers read backwards.",
    "prerequisite": "Place value and the rule that a number cannot start with zero.",
    "starter": "How many three-digit palindromes begin with 2 and use a middle digit from 0, 1 or 2?",
    "steps": [
      "The first digit is fixed as 2.",
      "The final digit must match it, so the number is 2□2.",
      "Only the middle is free: 202, 212, 222. There are 3 choices."
    ]
  },
  "DIG-05": {
    "id": "DIG-05",
    "hook": "A carry is a clue travelling from one column to the next.",
    "goal": "Use place value and carries to recover missing digits.",
    "when": "Look for letter arithmetic or missing digits in a written sum.",
    "prerequisite": "Units, tens and carrying ten units into one ten.",
    "starter": "In 1A + 1A = 28, what digit is A?",
    "steps": [
      "1A means 10 + A, not 1 multiplied by A.",
      "The two tens already make 20. The units must add to the remaining 8.",
      "A + A = 8, so A = 4. Check 14 + 14 = 28."
    ]
  },
  "DIV-01": {
    "id": "DIV-01",
    "hook": "Could you find every divisor without testing every smaller number?",
    "goal": "Build divisors by choosing prime factors, then count those choices.",
    "when": "Use this when asked for how many factors or divisors, especially for a large product.",
    "prerequisite": "Multiplication, factor pairs and prime numbers.",
    "starter": "How many positive divisors does 12 have?",
    "steps": [
      "12 = 2 × 2 × 3. A divisor can use zero, one or two copies of 2.",
      "For each of those choices, use either zero or one copy of 3.",
      "The divisors are 1, 2, 4 and 3, 6, 12. Three choices times two choices gives 6."
    ]
  },
  "DIV-02": {
    "id": "DIV-02",
    "hook": "Two flashing lights have different rhythms. When will they agree again?",
    "goal": "Find the first shared multiple of repeating intervals.",
    "when": "Look for again together, common cycles, or equal groups of two sizes.",
    "prerequisite": "Skip-counting and multiples.",
    "starter": "Lights flash every 4 and 6 seconds. They flash together now. When next?",
    "steps": [
      "List positive flash times: 4, 8, 12… and 6, 12…",
      "The first shared positive time is 12.",
      "Time 0 was the starting flash. The question asks for the next one, so answer 12 seconds."
    ]
  },
  "DIV-03": {
    "id": "DIV-03",
    "hook": "You can often solve a huge-number puzzle by keeping only what is left over.",
    "goal": "Replace a full division with a smaller question about remainders.",
    "when": "Look for equal groups with leftovers, divisibility, clocks or repeating patterns.",
    "prerequisite": "Multiplication as equal groups; subtraction.",
    "starter": "Share 17 counters into groups of 5. What is left over?",
    "steps": [
      "Three full groups use 5 × 3 = 15 counters.",
      "17 − 15 = 2 counters remain. Write 17 = 5 × 3 + 2.",
      "The remainder is 2, smaller than 5. A remainder of 5 would make another complete group."
    ]
  },
  "DIV-04": {
    "id": "DIV-04",
    "hook": "Some targets are impossible, however long you keep trying. Odd and even can explain why.",
    "goal": "Track a feature that every allowed move preserves or switches.",
    "when": "Use this when moves repeat and the question asks whether a target is possible.",
    "prerequisite": "Odd and even; adding small numbers.",
    "starter": "Start at 2 and keep adding 4. Can you ever land on 11?",
    "steps": [
      "2 is even. Adding the even number 4 keeps the result even.",
      "The values 6, 10, 14 illustrate the pattern, but the even-plus-even rule proves it for every move.",
      "11 is odd, so no number of these moves can reach it."
    ]
  },
  "DIV-05": {
    "id": "DIV-05",
    "hook": "The millionth turn might be no harder than the fourth if the pattern repeats.",
    "goal": "Use a cycle length to jump over full repetitions.",
    "when": "Look for last digits, repeating colours, days or rotating positions.",
    "prerequisite": "Remainders and careful counting from the first item.",
    "starter": "Red, blue, green repeat in that order. What colour is position 8?",
    "steps": [
      "One cycle has 3 positions.",
      "8 = 2 × 3 + 2: skip two complete cycles and move two positions into the next.",
      "Position 7 is red and position 8 is blue. A remainder of zero would mean green."
    ]
  },
  "FRAC-01": {
    "id": "FRAC-01",
    "hook": "Half of what remains is not the same as half of what you started with.",
    "goal": "Keep track of the whole as a quantity changes in stages.",
    "when": "Look for of the remainder, then, or fractions of a changing total.",
    "prerequisite": "Fractions of small whole numbers.",
    "starter": "There are 12 cakes. Half are sold, then half of those left are sold. How many remain?",
    "steps": [
      "The first sale removes 6 and leaves 6.",
      "The second half refers to those 6 cakes, so it removes 3.",
      "3 remain. Check by adding the two sales and the remainder: 6 + 3 + 3 = 12."
    ]
  },
  "FRAC-02": {
    "id": "FRAC-02",
    "hook": "A ratio is a recipe made of equal-sized parts.",
    "goal": "Turn a comparison into a part value and rebuild the quantities.",
    "when": "Look for a ratio with a total, a difference or one known amount.",
    "prerequisite": "Equal groups and sharing.",
    "starter": "Red : blue counters is 2 : 3. There are 15 altogether. How many are blue?",
    "steps": [
      "Draw 2 red parts and 3 blue parts. There are 5 equal parts altogether.",
      "15 ÷ 5 = 3 counters in each part.",
      "Blue has 3 parts, so 9 counters. Red has 6; 6 + 9 = 15."
    ]
  },
  "FRAC-03": {
    "id": "FRAC-03",
    "hook": "Why does a rise of 10% followed by a fall of 10% fail to cancel?",
    "goal": "Track the amount a percentage is taken from.",
    "when": "Use this for price changes, discounts and successive increases or decreases.",
    "prerequisite": "One tenth and one hundredth of a quantity.",
    "starter": "A $100 price rises by 10%, then falls by 10%. Where does it finish?",
    "steps": [
      "The rise is $10, giving $110.",
      "The fall is 10% of $110, which is $11, not $10.",
      "The final price is $99. The two percentages acted on different starting amounts."
    ]
  },
  "FRAC-04": {
    "id": "FRAC-04",
    "hook": "Half of a small group and half of a big group represent different numbers of people.",
    "goal": "Convert each fraction to an actual quantity before combining groups.",
    "when": "Look for fractions of different groups, mixtures or combined survey results.",
    "prerequisite": "Fractions of a group and addition.",
    "starter": "Half of 8 children and a quarter of 12 adults wear hats. How many hats?",
    "steps": [
      "Half of 8 is 4 children.",
      "A quarter of 12 is 3 adults.",
      "There are 4 + 3 = 7 hats. Adding the fractions alone would ignore the group sizes."
    ]
  },
  "RATE-01": {
    "id": "RATE-01",
    "hook": "Four fence posts make only three gaps. That one gap can change the answer.",
    "goal": "Count intervals and put quantities into compatible units.",
    "when": "Look for first to last, regularly spaced events or unit conversions.",
    "prerequisite": "Drawing a line of points; seconds and minutes.",
    "starter": "A bell rings four times, five seconds apart. Time from first to last?",
    "steps": [
      "Draw four dots. There are three spaces between them.",
      "The ring times are 0, 5, 10 and 15 seconds.",
      "The elapsed time is 3 × 5 = 15 seconds, not 4 × 5."
    ]
  },
  "RATE-02": {
    "id": "RATE-02",
    "hook": "Two workers working together combine their work, not their finishing times.",
    "goal": "Convert completion times into work per unit of time.",
    "when": "Look for taps, machines or workers completing one job together.",
    "prerequisite": "Fractions of a whole and equal time intervals.",
    "starter": "One tap fills a tank in 2 minutes; another in 4. What fraction fills in one minute together?",
    "steps": [
      "The first tap fills 1/2 tank each minute.",
      "The second fills 1/4 tank each minute.",
      "Together they fill 1/2 + 1/4 = 3/4 tank in one minute. This is the combined rate."
    ]
  },
  "RATE-03": {
    "id": "RATE-03",
    "hook": "A journey becomes easier when its units tell the same story.",
    "goal": "Connect distance, speed and time using a consistent unit.",
    "when": "Look for travel, speed changes or minutes mixed with kilometres per hour.",
    "prerequisite": "Multiplication and converting minutes to hours.",
    "starter": "A cyclist travels at 12 km/h for half an hour. How far?",
    "steps": [
      "12 km/h means 12 kilometres in one whole hour.",
      "Half an hour allows half that distance at the same speed.",
      "12 × 1/2 = 6 km. A distance answer needs distance units."
    ]
  },
  "RATE-04": {
    "id": "RATE-04",
    "hook": "Instead of following two travellers, follow the gap between them.",
    "goal": "Find how quickly a separation grows or shrinks.",
    "when": "Look for meet, catch up, towards each other or moving in the same direction.",
    "prerequisite": "Distance = speed × time.",
    "starter": "Two walkers are 12 km apart, walking towards each other at 4 and 2 km/h. When do they meet?",
    "steps": [
      "In one hour, one removes 4 km of the gap and the other removes 2 km.",
      "Together the gap shrinks by 6 km per hour.",
      "12 ÷ 6 = 2 hours. Their distances 8 km and 4 km add to the original gap."
    ]
  },
  "ALG-01": {
    "id": "ALG-01",
    "hook": "An unknown number is not a reason to guess. Give it a job in the story.",
    "goal": "Translate a story into equal quantities and undo the operations.",
    "when": "Look for identical items with a total cost or a missing amount.",
    "prerequisite": "Equal groups, subtraction and division.",
    "starter": "Two equal-price notebooks and a $3 pen cost $11. What does one notebook cost?",
    "steps": [
      "Remove the known pen cost: 11 − 3 = 8.",
      "The $8 belongs equally to two notebooks, so each costs $4.",
      "Check in the story: 4 + 4 + 3 = 11."
    ]
  },
  "ALG-02": {
    "id": "ALG-02",
    "hook": "A total and a difference together reveal two hidden amounts.",
    "goal": "Remove the extra amount, then split what is left equally.",
    "when": "Look for altogether and more than in the same problem.",
    "prerequisite": "Halving and subtraction.",
    "starter": "Two piles total 14 counters. One has 4 more. How many in the smaller?",
    "steps": [
      "Temporarily remove the 4 extra counters from the larger pile.",
      "There are now 10 counters in two equal piles: 5 each.",
      "The original piles are 5 and 9. Total 14, difference 4."
    ]
  },
  "ALG-03": {
    "id": "ALG-03",
    "hook": "Two shopping baskets can reveal a price even when neither price is known.",
    "goal": "Subtract matching collections to make a shared unknown disappear.",
    "when": "Look for two totals containing the same items or an equal shared part.",
    "prerequisite": "Subtracting equal amounts from both sides.",
    "starter": "A pen and a book cost $7. Two pens and the same book cost $10. Price of a pen?",
    "steps": [
      "Line up the two baskets. Both contain one book and one pen.",
      "The second basket adds just one extra pen and costs $3 more.",
      "The pen costs $3. The book then costs $4, so both totals work."
    ]
  },
  "ALG-04": {
    "id": "ALG-04",
    "hook": "A result is a trail you can follow backwards.",
    "goal": "Undo a chain of operations in reverse order.",
    "when": "Look for a starting quantity hidden behind a sequence of changes.",
    "prerequisite": "Inverse operations: add/subtract, multiply/divide.",
    "starter": "A number is doubled, then 3 is added, giving 11. What was it?",
    "steps": [
      "The last action was adding 3. Undo it first: 11 − 3 = 8.",
      "Before that the number was doubled. Undo by dividing: 8 ÷ 2 = 4.",
      "Check forwards: 4 × 2 + 3 = 11. The start was 4."
    ]
  },
  "ALG-05": {
    "id": "ALG-05",
    "hook": "Moving one counter can close a gap by two.",
    "goal": "Track what a transfer changes and what stays constant.",
    "when": "Look for gives, moves from one pile to another, or equalising groups.",
    "prerequisite": "Subtraction and totals.",
    "starter": "A has 8 counters and B has 4. How many must A give B to make them equal?",
    "steps": [
      "The total stays 12, so equal piles must each have 6.",
      "The original gap is 4. Each transfer reduces A by 1 and increases B by 1.",
      "Two transfers close the gap: A = 6 and B = 6."
    ]
  },
  "SEQ-01": {
    "id": "SEQ-01",
    "hook": "Can you reach the hundredth term without writing the first ninety-nine?",
    "goal": "Use the starting value and the number of equal jumps.",
    "when": "Look for a constant increase or decrease in a sequence.",
    "prerequisite": "Repeated addition and multiplication.",
    "starter": "A pattern starts 5, 8, 11… What is its fifth term?",
    "steps": [
      "The first term is already 5. Reaching term 5 takes four jumps.",
      "Each jump adds 3, so the extra amount is 4 × 3 = 12.",
      "5 + 12 = 17. Listing 5, 8, 11, 14, 17 checks the method."
    ]
  },
  "SEQ-02": {
    "id": "SEQ-02",
    "hook": "Doubling grows surprisingly fast, but it also creates a useful cancellation.",
    "goal": "Recognise multiplicative growth and simplify doubling sums.",
    "when": "Look for each stage multiplying by the same amount, rather than adding it.",
    "prerequisite": "Doubling and the meaning of a power.",
    "starter": "Find 1 + 2 + 4 + 8 by comparing with twice the sum.",
    "steps": [
      "Call the sum S. Twice it is 2S = 2 + 4 + 8 + 16.",
      "Subtract the original sum. The 2, 4 and 8 cancel, leaving 2S − S = 16 − 1.",
      "So S = 15. Direct addition confirms it for this small example."
    ]
  },
  "SEQ-03": {
    "id": "SEQ-03",
    "hook": "A big route-counting problem can be built from two smaller ones.",
    "goal": "Count possibilities by the final move and reuse smaller answers.",
    "when": "Look for one-or-two-step moves or structures built from smaller structures.",
    "prerequisite": "Small ordered lists and addition.",
    "starter": "Climb 3 stairs using moves of one or two stairs. How many sequences?",
    "steps": [
      "A last move of 1 comes from stair 2: the earlier moves are 1+1 or 2.",
      "A last move of 2 comes from stair 1: the earlier move is 1.",
      "The full routes are 1+1+1, 2+1 and 1+2. There are 3; the last-move groups do not overlap."
    ]
  },
  "SEQ-04": {
    "id": "SEQ-04",
    "hook": "A repeated position can let you skip thousands of moves—if the whole situation repeats.",
    "goal": "Record enough information to identify a genuine repeating state.",
    "when": "Use this for rotating pointers or processes with a fixed next-step rule.",
    "prerequisite": "Remainders and compass directions.",
    "starter": "A pointer starts north and turns clockwise a quarter-turn five times. Where does it face?",
    "steps": [
      "After one, two, three and four turns it faces east, south, west and north.",
      "Four turns restore the complete starting state.",
      "Five turns are one full cycle and one extra turn, so it faces east."
    ]
  },
  "COUNT-01": {
    "id": "COUNT-01",
    "hook": "A tidy list is a mathematical argument when you can explain why nothing is missing.",
    "goal": "Choose an ordering rule that counts each possibility once.",
    "when": "Look for a small complete set of pairs or combinations.",
    "prerequisite": "Ordering whole numbers and addition.",
    "starter": "Find all unordered positive whole-number pairs adding to 7.",
    "steps": [
      "Start the smaller number at 1: (1,6), then (2,5), then (3,4).",
      "Starting at 4 would produce (4,3), a pair already counted backwards.",
      "There are 3 pairs. Every smaller number was considered in order."
    ]
  },
  "COUNT-02": {
    "id": "COUNT-02",
    "hook": "Choosing a captain and helper is different from choosing a two-person team.",
    "goal": "Decide whether order matters before multiplying choices.",
    "when": "Look for selections, teams or arrangements.",
    "prerequisite": "Multiplication as counting equal groups.",
    "starter": "How many two-person teams can A, B and C make?",
    "steps": [
      "If we choose a first and second person, there are 3 × 2 = 6 ordered choices.",
      "AB and BA name the same team; every team appears in exactly two orders.",
      "Divide by 2 to get 3 teams: AB, AC and BC."
    ]
  },
  "COUNT-03": {
    "id": "COUNT-03",
    "hook": "A restriction can make the organising plan clearer.",
    "goal": "Use blocks or gaps to handle neighbours and forbidden neighbours.",
    "when": "Look for together, adjacent, separated or not at an end.",
    "prerequisite": "Small arrangements and multiplication.",
    "starter": "Arrange books A, B and C with A and B next to each other. How many ways?",
    "steps": [
      "Treat A and B as one block. The block goes before or after C.",
      "Inside the block, the order can be AB or BA.",
      "The four arrangements are ABC, BAC, CAB and CBA. Two choices times two choices gives 4."
    ]
  },
  "COUNT-04": {
    "id": "COUNT-04",
    "hook": "Sometimes the easiest way to count what you want is to count what you do not want.",
    "goal": "Subtract unwanted cases or correct for an overlap.",
    "when": "Look for at least one, neither, both, or two overlapping groups.",
    "prerequisite": "Totals and subtraction.",
    "starter": "Six children play chess, five play music and two do both. How many do at least one?",
    "steps": [
      "Adding 6 + 5 counts the two children in both groups twice.",
      "Keep one copy of those two children by subtracting 2 once.",
      "6 + 5 − 2 = 9. The groups are chess only 4, both 2, music only 3."
    ]
  },
  "COUNT-05": {
    "id": "COUNT-05",
    "hook": "The same set can tell you its size in two different ways.",
    "goal": "Count connections from both endpoints and correct repeated counting.",
    "when": "Look for handshakes, shared edges or objects belonging to two groups.",
    "prerequisite": "Multiplication and halving.",
    "starter": "Four people each shake hands with everyone else once. How many handshakes?",
    "steps": [
      "Each person counts 3 partners, giving 4 × 3 = 12 reports.",
      "Every actual handshake is reported by both people involved.",
      "There are 12 ÷ 2 = 6 handshakes. The two reports describe one event."
    ]
  },
  "COUNT-06": {
    "id": "COUNT-06",
    "hook": "A case split turns a messy set into smaller sets you can trust.",
    "goal": "Choose cases that cover everything and never overlap.",
    "when": "Look for restrictions that suggest separate possibilities for a digit or position.",
    "prerequisite": "Organised lists and addition.",
    "starter": "Using digits 1 and 2, with repeats allowed, how many two-digit numbers contain a 1?",
    "steps": [
      "Case 1: the tens digit is 1. That gives 11 and 12.",
      "Case 2: the tens digit is not 1 but the units digit is. That gives 21.",
      "There are 3. The cases do not overlap, so 11 is not counted twice."
    ]
  },
  "LOGIC-01": {
    "id": "LOGIC-01",
    "hook": "A statement can be a clue even when the speaker is lying.",
    "goal": "Test truth assignments and follow their consequences.",
    "when": "Look for always truthful, always lies or claims about other statements.",
    "prerequisite": "Knowing what makes a complete statement false.",
    "starter": "A says “B is a liar.” If A tells the truth, what is B?",
    "steps": [
      "Assume the given condition: A is truthful.",
      "Then the whole statement “B is a liar” must be true.",
      "B is a liar. If A were lying instead, that statement would be false, so B would be truthful."
    ]
  },
  "LOGIC-02": {
    "id": "LOGIC-02",
    "hook": "One clue may leave several answers. The clues must work together.",
    "goal": "Eliminate candidates systematically and check every condition.",
    "when": "Look for number codes, several simultaneous clues or hidden assignments.",
    "prerequisite": "Small lists and checking arithmetic.",
    "starter": "A digit is greater than 3, less than 8, and even. What could it be?",
    "steps": [
      "The range clue leaves 4, 5, 6 and 7.",
      "The even clue removes 5 and 7.",
      "Both 4 and 6 remain. Do not claim a unique answer without another clue."
    ]
  },
  "LOGIC-03": {
    "id": "LOGIC-03",
    "hook": "Row totals and column totals are two descriptions of the same entries.",
    "goal": "Compare totals to find missing information without filling every cell.",
    "when": "Look for grids, row sums, column sums or repeated symbols.",
    "prerequisite": "Adding totals and identifying double counting.",
    "starter": "A two-row grid has row totals 7 and 9. One column totals 6. What is the other column total?",
    "steps": [
      "Both rows together total 7 + 9 = 16.",
      "Both columns together must also total 16 because they contain the same cells.",
      "The missing column total is 16 − 6 = 10."
    ]
  },
  "LOGIC-04": {
    "id": "LOGIC-04",
    "hook": "Finding an answer is one job. Showing it is the only answer is another.",
    "goal": "Separate existence from uniqueness.",
    "when": "Look for only, unique, all possibilities or prove there are no others.",
    "prerequisite": "Listing a bounded set and testing conditions.",
    "starter": "Which whole number between 1 and 5 is both even and a multiple of 3?",
    "steps": [
      "The even candidates are 2 and 4; neither is a multiple of 3.",
      "The multiples of 3 in the range contain only 3, which is odd.",
      "There is no solution. A puzzle does not have to have exactly one answer."
    ]
  },
  "GEO-01": {
    "id": "GEO-01",
    "hook": "When two shapes touch, some edges stop being outside edges.",
    "goal": "Trace the boundary and remove shared edges from perimeter totals.",
    "when": "Look for joined rectangles, fences or outlines.",
    "prerequisite": "Perimeter as distance around the outside.",
    "starter": "Join two unit squares along one full edge. What is the new perimeter?",
    "steps": [
      "Separately the squares have perimeter 4 + 4 = 8.",
      "The shared edge is inside, and it was included once for each square.",
      "Remove both copies: 8 − 2 = 6 units. Trace the resulting 2-by-1 rectangle to check."
    ]
  },
  "GEO-02": {
    "id": "GEO-02",
    "hook": "An awkward shape can hide inside an easy rectangle.",
    "goal": "Split, rearrange or subtract regions to measure area.",
    "when": "Look for shaded regions, cut-outs or triangles sharing a base or height.",
    "prerequisite": "Rectangle area; perpendicular height.",
    "starter": "A 4-by-3 rectangle is cut along a diagonal. What is the area of either triangle?",
    "steps": [
      "The whole rectangle has area 4 × 3 = 12.",
      "The diagonal splits it into two matching triangles.",
      "Each has area 6 square units. The height is perpendicular to the base, not the sloping side."
    ]
  },
  "GEO-03": {
    "id": "GEO-03",
    "hook": "A diagram is a set of facts, not a picture to measure by eye.",
    "goal": "Use angle relationships to deduce a missing angle.",
    "when": "Look for straight lines, triangles, parallel lines or turns.",
    "prerequisite": "A straight angle is 180 degrees.",
    "starter": "Two angles of a triangle are 50° and 60°. What is the third?",
    "steps": [
      "A triangle's interior angles total 180°.",
      "The known angles total 50 + 60 = 110°.",
      "The missing angle is 180 − 110 = 70°. Check that all three add to 180°."
    ]
  },
  "GEO-04": {
    "id": "GEO-04",
    "hook": "A shape can look unchanged after moving—even though its points moved.",
    "goal": "Describe and recognise reflections, rotations and translations.",
    "when": "Look for folding, matching positions or a shape mapping onto itself.",
    "prerequisite": "Left and right; quarter-turns and half-turns.",
    "starter": "Does a plain 2-by-1 rectangle match itself after a quarter-turn or a half-turn about its centre?",
    "steps": [
      "A quarter-turn swaps its horizontal and vertical dimensions. It does not cover its old outline.",
      "A half-turn returns the long sides and short sides to the same positions.",
      "It has half-turn symmetry. A square would also match after a quarter-turn."
    ]
  },
  "GEO-05": {
    "id": "GEO-05",
    "hook": "How do you know a good design is the best possible design?",
    "goal": "Combine a bound with an example that reaches it.",
    "when": "Look for greatest, smallest, maximum or minimum under a fixed condition.",
    "prerequisite": "Rectangle perimeter and area.",
    "starter": "Use 12 unit fence pieces to make a whole-number-sided rectangle. What is the largest area?",
    "steps": [
      "If side lengths are a and b, 2a + 2b = 12, so a + b = 6.",
      "Ignoring rotations, all pairs are (1,5), (2,4), (3,3). Their areas are 5, 8 and 9.",
      "The 3-by-3 square reaches 9. The complete list proves no allowed rectangle has more."
    ]
  },
  "SOLID-01": {
    "id": "SOLID-01",
    "hook": "A drawing shows surfaces, but a solid also has cubes you cannot see.",
    "goal": "Count complete layers rather than just visible cubes.",
    "when": "Look for stacks, hidden cubes or cuboids.",
    "prerequisite": "Rectangle arrays and multiplication.",
    "starter": "A block is 2 cubes wide, 3 deep and 2 high. How many cubes?",
    "steps": [
      "One complete layer contains 2 × 3 = 6 cubes.",
      "There are two such layers, including the hidden cubes.",
      "6 × 2 = 12 cubes. Counting visible faces would answer a different question."
    ]
  },
  "SOLID-02": {
    "id": "SOLID-02",
    "hook": "Paint records where a small cube lived in the large solid.",
    "goal": "Classify cubes by exposed faces or count the protected interior.",
    "when": "Look for a painted solid cut into small cubes.",
    "prerequisite": "Layers and the difference between a face, edge and corner.",
    "starter": "Paint all faces of a 3-by-3-by-3 cube. How many little cubes have no paint?",
    "steps": [
      "Every cube touching an outside face gets paint.",
      "Remove the outside layer at each end of each direction: 3 − 2 = 1 position remains per direction.",
      "The unpainted core is 1 × 1 × 1, so exactly one cube has no paint."
    ]
  },
  "SOLID-03": {
    "id": "SOLID-03",
    "hook": "Filling a box and wrapping a box ask for different measurements.",
    "goal": "Separate volume from surface area and count all six faces.",
    "when": "Look for nets, wrapping, open or closed boxes, and exposed surfaces.",
    "prerequisite": "Rectangle area and square units.",
    "starter": "What is the surface area of a closed 1-by-2-by-3 box?",
    "steps": [
      "Opposite faces match. The three different face areas are 1×2 = 2, 1×3 = 3 and 2×3 = 6.",
      "There are two of each: 2 × (2 + 3 + 6).",
      "The surface area is 22 square units. The volume would instead be 6 cubic units."
    ]
  },
  "SPATIAL-01": {
    "id": "SPATIAL-01",
    "hook": "You can count routes without drawing every complete journey.",
    "goal": "Build route counts from the final step into each point.",
    "when": "Look for shortest paths with only specified directions.",
    "prerequisite": "Grid moves and adding disjoint possibilities.",
    "starter": "Move two steps right and one step up. How many shortest routes?",
    "steps": [
      "Every route has exactly three moves: R, R and U.",
      "The U move can be first, second or third.",
      "The routes are URR, RUR and RRU: 3. Choosing move positions counts each once."
    ]
  },
  "SPATIAL-02": {
    "id": "SPATIAL-02",
    "hook": "A rectangle is determined by its boundaries, not by its smallest cells.",
    "goal": "Choose two vertical and two horizontal grid lines.",
    "when": "Look for all rectangles, grid lines or hidden larger shapes.",
    "prerequisite": "A rectangle has two opposite pairs of sides.",
    "starter": "Two adjacent unit squares make a 2-by-1 grid. How many rectangles are in it?",
    "steps": [
      "There are three vertical boundary lines. Choose the left and right boundary.",
      "The possible pairs make the left square, right square and whole wide rectangle.",
      "There are 3 rectangles. The horizontal boundary pair is fixed."
    ]
  },
  "SPATIAL-03": {
    "id": "SPATIAL-03",
    "hook": "A colouring can prove a tiling impossible without trying every arrangement.",
    "goal": "Use a quantity every tile preserves, then construct a tiling when possible.",
    "when": "Look for dominoes covering a board with missing squares.",
    "prerequisite": "Checkerboard colours and edge-adjacent squares.",
    "starter": "Can a 2-by-2 board with opposite corners removed be tiled by one domino?",
    "steps": [
      "Opposite corners have the same colour.",
      "The two remaining squares also share a colour, but any domino covers one square of each colour.",
      "No. The colour mismatch proves impossibility; the squares are not edge-adjacent either."
    ]
  },
  "SPATIAL-04": {
    "id": "SPATIAL-04",
    "hook": "A network puzzle is often about connections, not the drawing's shape.",
    "goal": "Count edges meeting at each point to test a one-stroke trail.",
    "when": "Look for crossing every bridge or using every edge exactly once.",
    "prerequisite": "A vertex is a point; an edge is a connection.",
    "starter": "Three separate edges meet at a hub, with three different outer endpoints. Can one trail use them all once?",
    "steps": [
      "Each outer endpoint has just one edge. Entering one ends the trail unless you repeat that edge.",
      "A trail has only two ends, but this network has three outer endpoints.",
      "No such trail exists. With only two branches, you could start at one end and finish at the other."
    ]
  },
  "DATA-01": {
    "id": "DATA-01",
    "hook": "Two possible answers need not be equally likely.",
    "goal": "Count equally likely individual outcomes before forming a probability.",
    "when": "Look for random draws, dice or chances of an event.",
    "prerequisite": "Fractions and counting a set.",
    "starter": "A bag has two red counters and one blue counter. Each counter is equally likely. Probability of red?",
    "steps": [
      "Label the counters R1, R2 and B. These are the three equally likely outcomes.",
      "Two of the three outcomes are red.",
      "The probability is 2/3, not 1/2. The two colour names do not have equal chances."
    ]
  },
  "DATA-02": {
    "id": "DATA-02",
    "hook": "An average hides a total. Recovering that total unlocks the problem.",
    "goal": "Turn means into totals before combining or changing groups.",
    "when": "Look for a missing score, a new average or unequal group sizes.",
    "prerequisite": "Multiplication and division.",
    "starter": "Three numbers have mean 4. Add a fourth number, 8. What is the new mean?",
    "steps": [
      "The original total is 3 × 4 = 12.",
      "The new total is 12 + 8 = 20, shared across four numbers.",
      "The new mean is 20 ÷ 4 = 5. Averaging 4 and 8 would ignore the original three numbers."
    ]
  },
  "DATA-03": {
    "id": "DATA-03",
    "hook": "Before calculating from a graph, discover what its numbers actually measure.",
    "goal": "Read labels, units and scale before comparing values.",
    "when": "Use this for charts, tables and graphs with unfamiliar scales.",
    "prerequisite": "Subtraction and reading labelled quantities.",
    "starter": "A table records Monday: 6 books; Tuesday: 10 books. How many more on Tuesday?",
    "steps": [
      "The entries count books, not children or days.",
      "More than asks for a difference: 10 − 6.",
      "Tuesday has 4 more books. Keep the unit in the answer."
    ]
  }
};
export const investigationOpeners = {
  "M01": {
    "hook": "Reverse a number and a surprising pattern appears. Is it luck, or must it happen?",
    "goal": "Use place value to explain a pattern for every allowed number.",
    "skill": "DIG-01",
    "starter": "Explore one two-digit case: 42 − 24.",
    "steps": [
      "42 − 24 = 18.",
      "Write the difference as (40 − 20) + (2 − 4) = 20 − 2.",
      "For digits a and b, the difference is 9(a − b). The place-value argument explains why multiples of 9 appear."
    ]
  },
  "M02": {
    "hook": "Can you see a square growing one border at a time?",
    "goal": "Turn a pattern in a picture into an argument about a whole sequence.",
    "skill": "SEQ-01",
    "starter": "Why is 1 + 3 + 5 = 9?",
    "steps": [
      "Start with one unit square.",
      "Add three squares to make a 2-by-2 square, then five to make a 3-by-3 square.",
      "The completed 3-by-3 square has area 9. A growing border can explain a sum."
    ]
  },
  "M03": {
    "hook": "Several rhythms can agree now and then separate again.",
    "goal": "Find shared cycles and justify which event happens first.",
    "skill": "DIV-02",
    "starter": "When do 2-second and 3-second rhythms next meet after time zero?",
    "steps": [
      "The first rhythm has positive times 2, 4, 6…",
      "The second has 3, 6…",
      "Their first shared positive time is 6 seconds. Listing in order explains why it is the first."
    ]
  },
  "M04": {
    "hook": "Rules about neighbours can organise a count instead of making it messy.",
    "goal": "Split arrangements into cases that obey every restriction.",
    "skill": "COUNT-03",
    "starter": "Arrange A, B and C with A and B together.",
    "steps": [
      "Treat A and B as a single block.",
      "Put the block before or after C, and choose AB or BA inside it.",
      "The four possibilities are ABC, BAC, CAB, CBA. This complete small list checks the block method."
    ]
  },
  "M05": {
    "hook": "Three chosen dots do not always make a triangle.",
    "goal": "Count choices while excluding geometrically impossible ones.",
    "skill": "COUNT-02",
    "starter": "There are two dots on a top line and two on a parallel lower line. How many triangles use these dots?",
    "steps": [
      "A triangle must use two dots on one line and one on the other.",
      "Two top and one bottom gives 2 choices. Two bottom and one top gives another 2.",
      "There are 4 triangles. The cases are separate and cover every possible triangle."
    ]
  },
  "M06": {
    "hook": "A blocked gate suggests counting journeys in two different groups.",
    "goal": "Subtract routes through a forbidden point from all routes.",
    "skill": "SPATIAL-01",
    "starter": "List shortest routes needing two Right moves and one Up move.",
    "steps": [
      "The Up move is first, second or third.",
      "The routes are URR, RUR and RRU.",
      "Each route is counted once. In a larger grid, a chosen point can split routes into before and after portions."
    ]
  },
  "M07": {
    "hook": "A complicated drawing may be built from just a few choices.",
    "goal": "Identify exactly which boundaries determine each triangle.",
    "skill": "COUNT-02",
    "starter": "Three rays from one point meet one straight baseline. How many triangles are formed?",
    "steps": [
      "A triangle uses two of the rays and the baseline between them.",
      "The ray pairs are first–second, first–third and second–third.",
      "There are 3 triangles, including the larger one. Count boundary choices rather than only the smallest regions."
    ]
  },
  "M08": {
    "hook": "Curved pieces can be rearranged into familiar shapes.",
    "goal": "Separate area from boundary length in a composite shape.",
    "skill": "GEO-02",
    "starter": "Two semicircles each have radius r. What is their combined area?",
    "steps": [
      "A semicircle is half a circle.",
      "Two equal halves have the area of one whole circle.",
      "Their combined area is πr². Whether straight edges belong to an outside perimeter depends on how the pieces are joined."
    ]
  },
  "M09": {
    "hook": "Removing a piece changes area and perimeter in different ways.",
    "goal": "Track what is removed and what becomes a new boundary.",
    "skill": "GEO-01",
    "starter": "Cut a 1-by-1 square from a corner of a 3-by-3 square. What changes?",
    "steps": [
      "Area falls from 9 to 8 square units.",
      "Two outer unit edges disappear, but two new unit edges are exposed inside the notch.",
      "Perimeter stays 12 units. A cut-out need not decrease perimeter; a curved cut needs its own edge accounting."
    ]
  },
  "M10": {
    "hook": "Finding a short route is not yet proving it is shortest.",
    "goal": "Combine a minimum required number of moves with a route achieving it.",
    "skill": "GEO-05",
    "starter": "A disc must move from (0,0) to (2,1), one horizontal or vertical square at a time. Fewest moves?",
    "steps": [
      "It must change its horizontal coordinate by 2 and its vertical coordinate by 1.",
      "Every move changes only one coordinate by 1, so at least 3 moves are needed.",
      "Right, Right, Up uses 3 legal moves. The bound and construction together prove optimality."
    ]
  },
  "M11": {
    "hook": "Painting only some faces changes which hidden cubes stay clean.",
    "goal": "Classify cubes according to exactly which outer faces are painted.",
    "skill": "SOLID-02",
    "starter": "Only the top face of a 2-by-2-by-2 block is painted. How many little cubes get paint?",
    "steps": [
      "The top layer contains 2 × 2 = 4 cubes.",
      "Each touches the painted top and so gets one painted face.",
      "The lower four cubes get none. Count only the faces the question says are painted."
    ]
  },
  "M12": {
    "hook": "A colouring can show why endless trial and error will never work.",
    "goal": "Prove impossibility with an invariant, or prove possibility by building a tiling.",
    "skill": "SPATIAL-03",
    "starter": "Remove opposite corners from a 2-by-2 checkerboard. Can one domino cover the rest?",
    "steps": [
      "The removed squares have the same colour.",
      "The remaining squares also have the same colour.",
      "A domino always covers one square of each colour, so it cannot cover this remainder."
    ]
  },
  "M13": {
    "hook": "Each extra clue should reduce the candidate list, not replace the earlier clues.",
    "goal": "Build a complete list, then filter it with all the constraints.",
    "skill": "LOGIC-02",
    "starter": "Different digits A and B are from 1, 2, 3 with A + B = 4. What are the assignments?",
    "steps": [
      "Test A = 1: B must be 3.",
      "A = 2 gives B = 2, which breaks the different-digits rule.",
      "A = 3 gives B = 1. Only (1,3) and (3,1) remain; another clue may distinguish them."
    ]
  },
  "M14": {
    "hook": "A magic square is a web of equal totals.",
    "goal": "Use total sums and shared entries to constrain a construction.",
    "skill": "LOGIC-03",
    "starter": "The numbers 1 to 9 fill three rows with the same total. What must each row total?",
    "steps": [
      "The nine numbers total 45.",
      "The three rows contain every number exactly once.",
      "Their common total must be 45 ÷ 3 = 15. This condition is necessary; a valid construction must also pass the column and diagonal tests."
    ]
  },
  "M15": {
    "hook": "A complete coin list needs a plan that cannot miss a collection.",
    "goal": "Use a bounded case split with both a value total and an item count.",
    "skill": "COUNT-06",
    "starter": "Use exactly three coins, each worth 1 or 2, to make 5. Which collection works?",
    "steps": [
      "Three 1-coins make 3. Changing a 1-coin to a 2-coin adds 1.",
      "To increase the value from 3 to 5, change exactly two coins.",
      "The collection is 2, 2, 1. Coin order does not create a new collection."
    ]
  },
  "M16": {
    "hook": "Every bridge is counted from two islands.",
    "goal": "Use degrees and double counting to test and construct networks.",
    "skill": "COUNT-05",
    "starter": "Three islands form a triangle, with one bridge on each side. What is the degree sum?",
    "steps": [
      "Each island touches two bridges, so each has degree 2.",
      "The degree sum is 2 + 2 + 2 = 6.",
      "There are 3 bridges: each contributed twice to that sum. An odd degree sum cannot describe an ordinary undirected network."
    ]
  },
  "M17": {
    "hook": "A board puzzle can hide a quick upper bound.",
    "goal": "Find a limit, then test whether a legal arrangement reaches it.",
    "skill": "LOGIC-04",
    "starter": "Why can a 2-by-2 board never hold three non-attacking rooks?",
    "steps": [
      "Rooks attack along a row or column.",
      "Three rooks in two rows would force two into the same row.",
      "At most two are possible; opposite corners achieve two. Queens add diagonal restrictions, so rooks are only the warm-up."
    ]
  },
  "M18": {
    "hook": "The largest-looking rectangle is not enough—you need to rule out the rest.",
    "goal": "Prove an optimum using a complete list or a general comparison.",
    "skill": "GEO-05",
    "starter": "Use a perimeter of 12 units and positive whole-number sides. Which rectangle has greatest area?",
    "steps": [
      "The two different side lengths must sum to 6.",
      "Ignoring rotation, pairs are (1,5), (2,4), (3,3). Areas are 5, 8, 9.",
      "The 3-by-3 square wins, and the complete list rules out a larger allowed area."
    ]
  },
  "M19": {
    "hook": "A winning game plan must survive your opponent's choices.",
    "goal": "Work backwards from the end and distinguish winning from losing positions.",
    "skill": "ALG-04",
    "starter": "Take 1 or 2 stones each turn; taking the last wins. Is a pile of 3 good for the player to move?",
    "steps": [
      "With 1 or 2 stones, the player can take all and win.",
      "From 3, removing 1 leaves 2, while removing 2 leaves 1.",
      "Either move lets the opponent take the last. Thus 3 is a losing position against correct play."
    ]
  },
  "M20": {
    "hook": "Carrying is not always in tens. Clocks already use a different base.",
    "goal": "Keep units separate and carry at the correct conversion threshold.",
    "skill": "DIG-05",
    "starter": "Add 58 minutes and 5 minutes, then express the result in hours and minutes.",
    "steps": [
      "58 + 5 = 63 minutes.",
      "60 minutes make one hour, leaving 3 minutes.",
      "The result is 1 hour 3 minutes. Old money uses different conversion thresholds, but the same regrouping idea."
    ]
  }
};
