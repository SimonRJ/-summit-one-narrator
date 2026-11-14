"""Second reauthoring batch: mathematically distinct revisits for five more families.

Families: ALG-02, SEQ-04, LOGIC-02, FRAC-02, COUNT-01.
Only visits >= 2 are replaced; each family's first encounter keeps its original
statement. Every problem here is original to Summit One, has an integer answer,
and is independently recomputed by tools/content/check_curated_batch2.py.

Unlike curated_revisits.py, these replacements carry their own answer keys, so the
protected database rows (prompt, answer, title, solution) must be updated together
with this file. None of the affected problem IDs had recorded attempts when the
batch was released (see docs/CONTENT_AUDIT_REGISTER.md).
"""

SKILLS = ('ALG-02', 'SEQ-04', 'LOGIC-02', 'FRAC-02', 'COUNT-01')

def P(title, prompt, answer, steps, check, clue):
    return dict(title=title, prompt=prompt, answer=answer, steps=steps, check=check, clue=clue)

B = {}

# ---------------------------------------------------------------- ALG-02
B['ALG-02', 'try', 2] = P('Three sticker collections',
    'Ana, Ben and Cy have 64 stickers altogether. Ben has twice as many as Ana, and Cy has 4 more than Ben. How many stickers does Cy have?', 28,
    ['Measure everything in "Ana amounts". Ben has 2 of them, and Cy has 2 of them plus 4.',
     'So 5 Ana amounts plus 4 make 64, giving 5 Ana amounts = 60 and Ana has 12.',
     'Ben has 24 and Cy has 24 + 4 = 28.'],
    'Check the total: 12 + 24 + 28 = 64.',
    'When every quantity is described using one of them, write them all in terms of that one.')
B['ALG-02', 'transfer', 2] = P('Three bags weighed in pairs',
    'Three bags are weighed two at a time. The pairs weigh 31 kg, 35 kg and 38 kg. How heavy is the heaviest bag, in kg?', 21,
    ['Add the three weighings: 31 + 35 + 38 = 104. Each bag was on the scales exactly twice, so the three bags weigh 104 ÷ 2 = 52 kg together.',
     'The heaviest bag is the one left out of the lightest pair: 52 − 31 = 21 kg.',
     'The other bags are 52 − 38 = 14 kg and 52 − 35 = 17 kg.'],
    'Check the pairs: 14 + 17 = 31, 14 + 21 = 35 and 17 + 21 = 38.',
    'Adding all the equations can reveal the total before any single unknown is known.')
B['ALG-02', 'try', 3] = P('Wheels in the car park',
    'A car park holds only cars, with 4 wheels each, and motorbikes, with 2 wheels each. There are 23 vehicles and 74 wheels. How many cars are there?', 14,
    ['Imagine all 23 vehicles were motorbikes. That would give 23 × 2 = 46 wheels.',
     'The real count is 74 − 46 = 28 wheels higher. Swapping a motorbike for a car adds 2 wheels, so there are 28 ÷ 2 = 14 cars.'],
    'Check: 14 cars and 9 motorbikes have 56 + 18 = 74 wheels.',
    'Assume everything is the smaller type, then explain the shortfall with exchanges.')
B['ALG-02', 'transfer', 3] = P('Adult and child tickets',
    'A school play sold 40 tickets for $365 in total. Adult tickets cost $12 and child tickets cost $7. How many child tickets were sold?', 23,
    ['If all 40 tickets were adult tickets, the takings would be 40 × 12 = $480.',
     'The real takings are 480 − 365 = $115 lower. Each child ticket in place of an adult ticket lowers the total by $5, so there were 115 ÷ 5 = 23 child tickets.'],
    'Check: 17 adults pay $204 and 23 children pay $161, and 204 + 161 = 365.',
    'This time assume everything is the larger type and count exchanges downwards.')
B['ALG-02', 'try', 4] = P('Marbles passed both ways',
    'If Mia gives Leo 6 marbles, they will have the same number. If instead Leo gives Mia 6 marbles, Mia will have three times as many as Leo. How many marbles does Mia have?', 30,
    ['From the first statement, Mia has 12 more marbles than Leo.',
     'In the second situation the gap grows to 12 + 6 + 6 = 24, and Mia then has three times as many as Leo. The gap is two of Leo\'s shares, so Leo then has 12 and Mia has 36.',
     'Before that exchange Mia had 36 − 6 = 30 marbles (and Leo had 18).'],
    'Check both stories from 30 and 18: 24 and 24 are equal; 36 is three times 12.',
    'A transfer changes the difference by twice the amount moved.')
B['ALG-02', 'transfer', 4] = P('A rectangle that is nearly a square',
    'A rectangle has perimeter 58 cm. If its length were 5 cm shorter and its width 2 cm longer, it would be a square. What is the area of the rectangle, in square centimetres?', 198,
    ['Length plus width is half the perimeter: 29 cm.',
     'The square condition says length − 5 = width + 2, so the length is 7 cm more than the width.',
     'Two numbers with sum 29 and difference 7 are 18 and 11. The area is 18 × 11 = 198 cm².'],
    'Check the square: 18 − 5 = 13 and 11 + 2 = 13.',
    'Turn each sentence into a sum or a difference, then solve the sum-and-difference pair.')
B['ALG-02', 'try', 5] = P('Notebooks and pens',
    'A notebook costs $3 more than a pen. Four notebooks and three pens cost $40 altogether. How much does one notebook cost, in dollars?', 7,
    ['Replace each notebook by a pen plus $3. Four notebooks become four pens plus $12.',
     'So seven pens cost 40 − 12 = $28, and one pen costs $4.',
     'A notebook costs 4 + 3 = $7.'],
    'Check: 4 × 7 + 3 × 4 = 28 + 12 = 40.',
    'Exchange one kind of item for the other so that only one unknown price remains.')
B['ALG-02', 'transfer', 5] = P('Three fruit baskets',
    'At a stall, 2 apples, 1 banana and 1 mango cost $13. Also 1 apple, 2 bananas and 1 mango cost $12, and 1 apple, 1 banana and 2 mangoes cost $15. How much does one mango cost, in dollars?', 5,
    ['Add the three baskets: 4 apples, 4 bananas and 4 mangoes cost 13 + 12 + 15 = $40. So one of each costs $10.',
     'The third basket is "one of each" plus one extra mango, so a mango costs 15 − 10 = $5.'],
    'In the same way an apple is 13 − 10 = $3 and a banana is 12 − 10 = $2, and 3 + 2 + 5 = 10.',
    'A balanced set of equations can be added to find the total of one of each.')
B['ALG-02', 'try', 6] = P('A father and his two children',
    'The ages of a father and his two children add to 66. In 4 years the father will be exactly twice as old as his two children\'s ages added together. How old is the father now?', 48,
    ['Let the children\'s ages total C now, so the father is 66 − C.',
     'In 4 years the children\'s total is C + 8 (both children age) and the father is 70 − C. So 70 − C = 2(C + 8) = 2C + 16.',
     'Then 54 = 3C, so C = 18 and the father is 66 − 18 = 48.'],
    'Check in 4 years: father 52, children 18 + 8 = 26, and 52 = 2 × 26.',
    'When several people age, a combined age grows by more than one year per year.')
B['ALG-02', 'transfer', 6] = P('A jar of two kinds of coins',
    'A jar contains only 10-cent and 50-cent coins, worth $9.60 in total. There are 6 more 10-cent coins than 50-cent coins. How many coins are in the jar?', 36,
    ['Set aside the 6 extra 10-cent coins, worth 60 cents. The remaining 900 cents is made of pairs: one 10-cent coin with one 50-cent coin.',
     'Each pair is worth 60 cents, so there are 900 ÷ 60 = 15 pairs.',
     'That is 15 fifty-cent coins and 15 + 6 = 21 ten-cent coins: 36 coins.'],
    'Check the value: 21 × 10 + 15 × 50 = 210 + 750 = 960 cents.',
    'Remove the surplus first, then the rest pairs up evenly.')
B['ALG-02', 'try', 7] = P('Four numbers with overlapping sums',
    'Four numbers are written in a row and their sum is 90. The first three add to 61 and the last three add to 70. What is the sum of the two middle numbers?', 41,
    ['The fourth number is 90 − 61 = 29, and the first number is 90 − 70 = 20.',
     'The two middle numbers are what remains: 90 − 20 − 29 = 41.'],
    'Check with overlap: 61 + 70 counts the middle pair twice, and 61 + 70 − 90 = 41.',
    'You do not need each number separately; compare overlapping totals.')
B['ALG-02', 'transfer', 7] = P('A sum five times the difference',
    'The sum of two whole numbers is 5 times their difference. The larger number is 12 more than the smaller. What is the larger number?', 36,
    ['The difference is 12, so the sum is 5 × 12 = 60.',
     'Two numbers with sum 60 and difference 12: the larger is (60 + 12) ÷ 2 = 36 and the smaller is 24.'],
    'Check: 36 + 24 = 60 = 5 × 12.',
    'One condition gives the difference; use it to turn the other into a plain total.')
B['ALG-02', 'try', 8] = P('A quiz with penalties',
    'A quiz has 20 questions. Each correct answer scores 5 points and each wrong answer loses 2 points. Sam answered every question and scored 58. How many did Sam get right?', 14,
    ['A perfect paper scores 20 × 5 = 100.',
     'Each wrong answer costs 7 points compared with a right one: 5 not gained and 2 lost. Sam is 100 − 58 = 42 points short, so Sam had 42 ÷ 7 = 6 wrong.',
     'Sam got 20 − 6 = 14 right.'],
    'Check: 14 × 5 − 6 × 2 = 70 − 12 = 58.',
    'Start from the best possible total and count what each mistake really costs.')
B['ALG-02', 'transfer', 8] = P('Unicycles, bicycles and tricycles',
    'A shop sold 20 cycles in a week: unicycles, bicycles and tricycles. They had 44 wheels altogether, and twice as many bicycles as unicycles were sold. How many tricycles were sold?', 8,
    ['Group each unicycle with two bicycles. A group has 3 cycles and 1 + 2 + 2 = 5 wheels.',
     'If there are g groups and t tricycles, then 3g + t = 20 and 5g + 3t = 44. Tripling the first gives 9g + 3t = 60; subtracting the second gives 4g = 16, so g = 4.',
     'Then t = 20 − 12 = 8 tricycles.'],
    'Check: 4 unicycles, 8 bicycles and 8 tricycles are 20 cycles with 4 + 16 + 24 = 44 wheels.',
    'A fixed ratio between two unknowns lets you bundle them into a single unknown.')

# ---------------------------------------------------------------- SEQ-04
B['SEQ-04', 'try', 2] = P('Last digits of the powers of three',
    'Start with 3. To get each new number, multiply the previous number by 3 and keep only its last digit. The list begins 3, 9, 7, 1, 3, … What is the 50th number in the list?', 9,
    ['The list repeats the block 3, 9, 7, 1 of length 4.',
     '50 = 4 × 12 + 2, so the 50th number is the 2nd number of the block: 9.'],
    'The 48th number ends a block (it is 1), so the 49th is 3 and the 50th is 9.',
    'Once a state repeats, everything after it repeats; only the position inside the cycle matters.')
B['SEQ-04', 'transfer', 2] = P('Blue beads on a long string',
    'Beads are threaded in the repeating order red, red, blue, green, blue. How many of the first 73 beads are blue?', 29,
    ['Each block of 5 beads has 2 blue beads. 73 = 5 × 14 + 3, so there are 14 complete blocks with 28 blue beads.',
     'The 3 leftover beads are red, red, blue, adding 1 more: 29.'],
    'After 70 beads there are 28 blue; beads 71, 72, 73 are red, red, blue.',
    'Count whole cycles first, then deal carefully with the incomplete one.')
B['SEQ-04', 'try', 3] = P('A pointer jumping round a dial',
    'A dial has 12 positions numbered 0 to 11 in order round a circle. A pointer starts at 0 and jumps 5 positions clockwise every second. At which position is it after 2026 seconds?', 2,
    ['After 12 jumps the pointer has moved 60 positions, which is exactly 5 full turns, so it is back at 0. The pattern repeats every 12 seconds.',
     '2026 = 12 × 168 + 10, so the position matches 10 jumps: 50 positions, and 50 = 4 × 12 + 2.'],
    'Directly: 5 × 2026 = 10130 = 12 × 844 + 2.',
    'On a circle, only the remainder after whole turns matters.')
B['SEQ-04', 'transfer', 3] = P('Two lamps with different rhythms',
    'Lamp A repeats the 3-second pattern on, on, off. Lamp B repeats the 4-second pattern on, off, off, on. Both patterns start together at second 1. During the first 60 seconds, for how many seconds are both lamps on?', 20,
    ['The combined pattern repeats every 12 seconds, the lowest common multiple of 3 and 4.',
     'In seconds 1 to 12, lamp A is on in 1, 2, 4, 5, 7, 8, 10, 11 and lamp B is on in 1, 4, 5, 8, 9, 12. Both are on in seconds 1, 4, 5 and 8: four seconds.',
     '60 seconds is 5 full blocks, so both are on for 5 × 4 = 20 seconds.'],
    'List the second block, seconds 13 to 24, the same way: both lamps are on at 13, 16, 17 and 20, again four seconds.',
    'Two cycles running together make one longer cycle whose length is their lowest common multiple.')
B['SEQ-04', 'try', 4] = P('A halve-or-add-seven rule',
    'A list starts with 20. To get the next number: if the number is even, halve it; if it is odd, add 7. So the list begins 20, 10, 5, 12, … What is the 100th number in the list?', 6,
    ['Continue the list: 20, 10, 5, 12, 6, 3, 10, 5, 12, 6, 3, 10, … From the 2nd number on, it repeats the block 10, 5, 12, 6, 3 of length 5.',
     'The 100th number is the 99th number of the repeating part. 99 = 5 × 19 + 4, so it is the 4th number of the block: 6.'],
    'The 2nd, 7th, 12th, … numbers are all 10. The 97th is 10, so the 98th, 99th and 100th are 5, 12 and 6.',
    'A cycle need not start at the first term; find where the repetition begins.')
B['SEQ-04', 'transfer', 4] = P('Digits of one seventh',
    'As a decimal, 1/7 = 0.142857142857…, where the six digits 142857 repeat forever. What is the sum of the first 40 digits after the decimal point?', 177,
    ['One block 1, 4, 2, 8, 5, 7 has sum 27. 40 = 6 × 6 + 4, so there are 6 complete blocks with sum 6 × 27 = 162.',
     'The next 4 digits are 1, 4, 2, 8, with sum 15. The total is 162 + 15 = 177.'],
    'The 36th digit ends a block (a 7); digits 37 to 40 start a new block.',
    'Sum one cycle, multiply by the number of whole cycles, and add the leftover part.')
B['SEQ-04', 'try', 5] = P('A ball under four cups',
    'Four cups stand in a row in positions 1 to 4, with a ball under the cup in position 1. A performer swaps the cups in positions 1 and 2, then 2 and 3, then 3 and 4, and keeps repeating these three swaps in the same order. The ball stays under its cup. In which position is the ball after 20 swaps?', 2,
    ['Track the ball. After swaps 1, 2, 3 it is at positions 2, 3, 4. During swaps 4 and 5 it stays at 4; swap 6 moves it to 3; swap 7 leaves it; swap 8 moves it to 2; swap 9 leaves it; swap 10 moves it to 1; swaps 11 and 12 leave it at 1.',
     'After 12 swaps the ball is back at position 1 and the next swap is again "1 and 2", so everything repeats every 12 swaps.',
     '20 = 12 + 8, so the position after 20 swaps equals the position after 8 swaps: 2.'],
    'The state is the ball\'s position together with which swap comes next; both must match for the pattern to repeat.',
    'A repeating process is described by its full state, not just one visible number.')
B['SEQ-04', 'transfer', 5] = P('Units digit of a sum of powers',
    'What is the units digit of 2¹ + 2² + 2³ + … + 2⁵⁰?', 6,
    ['The units digits of the powers of 2 repeat 2, 4, 8, 6. One block adds to 20, which contributes 0 to the units digit.',
     '50 = 4 × 12 + 2, so after 12 complete blocks there are two more terms with units digits 2 and 4. The units digit of the sum is 2 + 4 = 6.'],
    'Another way: the sum equals 2⁵¹ − 2. Since 2⁵¹ ends in 8, the sum ends in 8 − 2 = 6.',
    'When only the last digit is wanted, replace each term by its last digit and use the cycle.')
B['SEQ-04', 'try', 6] = P('Even numbers in the Fibonacci list',
    'A list starts 1, 1, and every later number is the sum of the two before it: 1, 1, 2, 3, 5, 8, … How many of the first 60 numbers in the list are even?', 20,
    ['Track only odd (O) and even (E): O, O, E, O, O, E, … because odd + odd is even and odd + even is odd.',
     'The pattern O, O, E repeats every 3 terms, so exactly one third of the first 60 numbers are even: 20.'],
    'The 3rd, 6th, 9th numbers are 2, 8, 34, all even, and their neighbours are odd.',
    'Replace big numbers by a simple property that still obeys the rule.')
B['SEQ-04', 'transfer', 6] = P('A last-digit addition chain',
    'A list starts 1, 3. Every later number is the units digit of the sum of the two numbers before it, so the list begins 1, 3, 4, 7, 1, 8, … What is the 100th number in the list?', 7,
    ['Continue: 1, 3, 4, 7, 1, 8, 9, 7, 6, 3, 9, 2, 1, 3, … The pair 1, 3 has returned at the 13th and 14th numbers, so the list repeats with period 12.',
     '100 = 12 × 8 + 4, so the 100th number equals the 4th number: 7.'],
    'Each number depends only on the two before it, so a repeated neighbouring pair forces the whole list to repeat.',
    'When a rule uses the previous two terms, the state is a pair of terms.')
B['SEQ-04', 'try', 7] = P('A lighthouse signal',
    'A lighthouse lamp repeats this 10-second signal: on for 2 seconds, off for 3 seconds, on for 1 second, off for 4 seconds. The signal starts at the beginning of second 1. For how many of the first 337 seconds is the lamp on?', 102,
    ['Each 10-second signal has 2 + 1 = 3 seconds of light. 337 = 10 × 33 + 7, so 33 complete signals give 99 seconds of light.',
     'The first 7 seconds of the next signal are on, on, off, off, off, on, off: 3 more seconds.',
     'The total is 99 + 3 = 102 seconds.'],
    'The leftover part must be read from the start of a signal, not estimated as 7 tenths of 3.',
    'Whole cycles are easy; the partial cycle must be inspected in order.')
B['SEQ-04', 'transfer', 7] = P('Growing jumps round seven stations',
    'Seven stations numbered 0 to 6 are equally spaced round a circular track. A robot starts at station 0. Its 1st move advances 1 station, its 2nd move advances 2 stations, its 3rd move advances 3 stations, and so on. At which station is the robot after its 100th move?', 3,
    ['Seven moves in a row advance by amounts that together make a whole number of laps: for example 1 + 2 + … + 7 = 28 = 4 × 7. The same is true for any 7 consecutive moves, since their remainders on division by 7 are 0 to 6 in some order.',
     '100 = 7 × 14 + 2, so the first 98 moves return the robot to station 0.',
     'Moves 99 and 100 advance 99 and 100 stations, which act like 1 and 2. The robot finishes at station 3.'],
    'Directly: 1 + 2 + … + 100 = 5050 = 7 × 721 + 3.',
    'Even when the steps keep changing, their remainders can form a cycle.')

# ---------------------------------------------------------------- LOGIC-02
B['LOGIC-02', 'try', 2] = P('An odd number between 60 and 80',
    'A whole number is greater than 60 and less than 80. It is odd and its two digits add to 11. What is the number?', 65,
    ['The tens digit is 6 or 7. For the digits to add to 11 the number must be 65 or 74.',
     'Only 65 is odd.'],
    'Check 65: it lies between 60 and 80, is odd, and 6 + 5 = 11.',
    'Use the most restrictive clue first to shrink the list, then test the survivors.')
B['LOGIC-02', 'transfer', 2] = P('Five runners and four clues',
    'Ada, Bo, Cal, Dee and Eli ran a race with no ties. Ada finished exactly two places ahead of Bo. Cal finished immediately after Bo. Eli finished after Dee. Dee did not win. In which place, from 1 to 5, did Dee finish?', 2,
    ['Ada, Bo and Cal take places a, a + 2 and a + 3, so Ada was 1st or 2nd.',
     'If Ada was 2nd, Bo and Cal were 4th and 5th, leaving 1st and 3rd for Dee and Eli. Eli finished after Dee, so Dee would be 1st, but Dee did not win. This case is impossible.',
     'So Ada was 1st, Bo 3rd and Cal 4th, leaving 2nd and 5th. Eli finished after Dee, so Dee was 2nd and Eli 5th.'],
    'Check the order Ada, Dee, Bo, Cal, Eli against all four clues.',
    'Fix the most tightly linked group first, then test each possible position for it.')
B['LOGIC-02', 'try', 3] = P('An even multiple of seven',
    'A whole number between 100 and 200 is a multiple of 7. It is even and its digits add to 11. What is the number?', 182,
    ['The even multiples of 7 between 100 and 200 are 112, 126, 140, 154, 168, 182 and 196.',
     'Their digit sums are 4, 9, 5, 10, 15, 11 and 16. Only 182 has digit sum 11.'],
    'Check: 182 = 7 × 26, it is even, and 1 + 8 + 2 = 11.',
    'Combine two clues (multiple of 7 and even gives multiple of 14) to shorten the list before testing the third.')
B['LOGIC-02', 'transfer', 3] = P('Four boxes of marbles',
    'Boxes 1, 2, 3 and 4 contain 10, 20, 30 and 40 marbles in some order. Box 1 has more marbles than box 2. Box 3 has exactly 10 more than box 4. Box 2 does not have the fewest. How many marbles are in box 1?', 40,
    ['Boxes 3 and 4 hold (20, 10), (30, 20) or (40, 30).',
     'If they hold (30, 20) or (40, 30), then 10 marbles are in box 1 or box 2. Box 1 has more than box 2, so box 2 would have the 10, the fewest. That is not allowed.',
     'So box 3 has 20 and box 4 has 10. Boxes 1 and 2 share 30 and 40, and box 1 has more: 40.'],
    'Check: 40 > 30, 20 = 10 + 10, and box 2 (30) does not have the fewest.',
    'Split into cases using the clue with the fewest possibilities, and eliminate whole cases at once.')
B['LOGIC-02', 'try', 4] = P('Three factors of sixty',
    'Three different whole numbers, each greater than 1, multiply to make 60 and add to make 12. What is the largest of the three numbers?', 5,
    ['List the ways to write 60 as a product of three different whole numbers greater than 1: 2 × 3 × 10, 2 × 5 × 6 and 3 × 4 × 5.',
     'Their sums are 15, 13 and 12. Only 3, 4, 5 add to 12, so the largest is 5.'],
    'To be sure the list is complete, start from the smallest factor: it can only be 2 or 3, because 4 × 5 × 6 is already more than 60.',
    'Use the multiplication clue to make a short complete list, then apply the addition clue.')
B['LOGIC-02', 'transfer', 4] = P('A square whose reverse is prime',
    'A two-digit number is a perfect square. When its digits are reversed, the result is a prime number. What is the two-digit number?', 16,
    ['The two-digit squares are 16, 25, 36, 49, 64 and 81. Reversed they are 61, 52, 63, 94, 46 and 18.',
     '52, 94, 46 and 18 are even and 63 = 7 × 9. Only 61 is prime, so the number is 16.'],
    'Check that 61 is prime: it is not divisible by 2, 3, 5 or 7, and 11 × 11 is already more than 61.',
    'Start from the clue that gives the shortest list.')
B['LOGIC-02', 'try', 5] = P('Every three neighbours add to twenty',
    'Five numbers are written in a row. Every three neighbouring numbers add to 20. The first number is 7 and the fifth number is 4. What is the middle number?', 9,
    ['Compare numbers 1, 2, 3 with numbers 2, 3, 4: both sets add to 20 and share two numbers, so the 4th number equals the 1st: 7.',
     'In the same way the 5th number equals the 2nd, so the 2nd number is 4.',
     'The first three numbers are 7, 4 and the middle number, so the middle number is 20 − 7 − 4 = 9.'],
    'The row is 7, 4, 9, 7, 4, and each neighbouring three add to 20.',
    'Overlapping conditions can force numbers to repeat.')
B['LOGIC-02', 'transfer', 5] = P('Exactly one false statement',
    'A whole number from 1 to 10 is hidden. Four statements are made about it: "It is even." "It is greater than 6." "It is a multiple of 4." "It is less than 9." Exactly one of the four statements is false. What is the hidden number?', 4,
    ['Suppose "even" is the false one. Then the number is odd, yet a multiple of 4: impossible.',
     'Suppose "a multiple of 4" is the false one. Then the number is even, greater than 6 and less than 9, so it is 8, but 8 is a multiple of 4: impossible. Suppose "less than 9" is false. Then it is 9 or 10 and a multiple of 4: impossible.',
     'So "greater than 6" is the false statement. The number is a multiple of 4 that is at most 6: it is 4.'],
    'Check 4: even (true), greater than 6 (false), multiple of 4 (true), less than 9 (true).',
    'When exactly one statement is false, test each statement in turn as the false one.')
B['LOGIC-02', 'try', 6] = P('Three linked secret numbers',
    'Ali, Bo and Cy each choose a different whole number from 1 to 9. Ali\'s number is the sum of the other two. Bo\'s number is three times Cy\'s. The three numbers add to more than 10. What is Ali\'s number?', 8,
    ['If Cy chooses c, then Bo has 3c and Ali has 4c. Since 4c is at most 9, c is 1 or 2.',
     'The numbers are 1, 3, 4 (total 8) or 2, 6, 8 (total 16). Only the second total is more than 10, so Ali has 8.'],
    'Check: 8 = 6 + 2, and 6 = 3 × 2.',
    'Express every unknown using one of them; the allowed range then leaves very few cases.')
B['LOGIC-02', 'transfer', 6] = P('Four weights in four bags',
    'Weights of 1 kg, 2 kg, 3 kg and 4 kg are placed one each in bags P, Q, R and S. Bags P and Q together weigh the same as bags R and S together. Bag P is heavier than bag S, and bag Q is heavier than bag P. How heavy is bag R, in kg?', 4,
    ['The total is 10 kg, so each pair weighs 5 kg. The pairs are 1 with 4, and 2 with 3.',
     'If P and Q are 1 and 4, then Q heavier than P gives P = 1, but P must be heavier than S: impossible.',
     'So P and Q are 2 and 3 with P = 2 and Q = 3. Then S is lighter than 2, so S = 1 and R = 4.'],
    'Check: 2 + 3 = 4 + 1, P (2) is heavier than S (1), and Q (3) is heavier than P (2).',
    'An equal-sum clue with a known total fixes the possible pairs immediately.')
B['LOGIC-02', 'try', 7] = P('A year divisible by eleven',
    'A year from 2001 to 2099 is a multiple of 11, and its four digits add to 12. Which year is it?', 2046,
    ['Write the year as 20AB. The digit sum gives A + B = 10.',
     'A number is a multiple of 11 when its alternating digit sum is a multiple of 11: 2 − 0 + A − B, so A − B = −2 (A − B = 9 would need A = 9, B = 0, which does not add to 10).',
     'A + B = 10 and B − A = 2 give A = 4 and B = 6: the year 2046.'],
    'Check: 2046 = 11 × 186 and 2 + 0 + 4 + 6 = 12.',
    'Translate each clue into a relation between the unknown digits.')
B['LOGIC-02', 'transfer', 7] = P('Crack the three-digit code',
    'A secret code has three different digits. Four guesses are tested. Guess 435: exactly one digit is correct and in the correct position. Guess 795: exactly one digit is correct but in the wrong position. Guess 962: no digit is correct. Guess 261: exactly one digit is correct and in the correct position. In every guess, any digit not mentioned as correct does not appear in the code. What is the code?', 471,
    ['From 962, the digits 9, 6 and 2 are not in the code. Then guess 261 shows that 1 is the third digit.',
     'In guess 435 the 5 is in the third position, which is taken by 1, so 5 is not the correctly placed digit, and then 5 is not in the code at all. From guess 795, with 9 and 5 excluded, 7 is in the code but not first, so 7 is the second digit.',
     'In guess 435 the 3 cannot be second, so the correctly placed digit is 4, in first position. The code is 471.'],
    'Check 471 against each guess: 435 (4 placed), 795 (7 misplaced), 962 (none), 261 (1 placed).',
    'Begin with the guess that eliminates the most, and carry each deduction into the other clues.')

# ---------------------------------------------------------------- FRAC-02
B['FRAC-02', 'try', 2] = P('Concrete in three parts',
    'A concrete mix uses sand, gravel and cement in the ratio 4 : 3 : 1 by weight. A batch weighs 56 kg. How many more kilograms of sand than cement does it contain?', 21,
    ['There are 4 + 3 + 1 = 8 equal parts, so one part is 56 ÷ 8 = 7 kg.',
     'Sand is 3 parts more than cement: 3 × 7 = 21 kg.'],
    'Check: 28 kg sand, 21 kg gravel and 7 kg cement total 56 kg.',
    'A difference between ingredients is a number of parts; you do not need each amount separately.')
B['FRAC-02', 'transfer', 2] = P('Linking two ratios',
    'Three friends share 93 cards. The ratio of Amy\'s cards to Ben\'s is 3 : 4, and the ratio of Ben\'s cards to Cal\'s is 6 : 5. How many cards does Amy have?', 27,
    ['Ben appears as 4 parts in one ratio and 6 in the other. Rewrite both with Ben as 12: Amy : Ben = 9 : 12 and Ben : Cal = 12 : 10.',
     'So Amy : Ben : Cal = 9 : 12 : 10, which is 31 parts. One part is 93 ÷ 31 = 3 cards.',
     'Amy has 9 × 3 = 27 cards.'],
    'Check: 27, 36 and 30 total 93; 27 : 36 = 3 : 4 and 36 : 30 = 6 : 5.',
    'Two ratios can be joined only after the shared quantity is given the same number of parts.')
B['FRAC-02', 'try', 3] = P('Distance from a map',
    'A map has scale 1 : 50 000. Two towns are 8 cm apart on the map. How far apart are they really, in kilometres?', 4,
    ['Every 1 cm on the map is 50 000 cm in reality, so 8 cm represents 400 000 cm.',
     '400 000 cm = 4000 m = 4 km.'],
    'A quicker route: 50 000 cm is half a kilometre, so each map centimetre is 0.5 km.',
    'A scale is a ratio of lengths in the same unit; convert units only at the end.')
B['FRAC-02', 'transfer', 3] = P('Paint for an enlarged logo',
    'A logo painted on a wall needed 40 mL of paint. The same logo is to be painted with every length 3 times as long, using paint at the same thickness. How many millilitres of paint are needed?', 360,
    ['Paint covers area. When every length is multiplied by 3, both the width and the height of each part triple, so areas are multiplied by 3 × 3 = 9.',
     'The paint needed is 40 × 9 = 360 mL.'],
    'Test with a 1 by 1 square: enlarged it is 3 by 3, which is 9 unit squares, not 3.',
    'A scale factor for lengths is squared for areas.')
B['FRAC-02', 'try', 4] = P('A gift that makes them equal',
    'Ava and Ben have stickers in the ratio 5 : 3. After Ava gives Ben 8 stickers, they have the same number. How many stickers did Ava have at first?', 40,
    ['At first Ava is 2 parts ahead of Ben. A gift of 8 lowers Ava by 8 and raises Ben by 8, closing a gap of 16.',
     'So 2 parts are 16 stickers and one part is 8. Ava had 5 × 8 = 40.'],
    'Check: 40 and 24 become 32 and 32.',
    'Giving moves the gap by twice the gift.')
B['FRAC-02', 'transfer', 4] = P('An age ratio that changes',
    'The ratio of Tom\'s age to his mother\'s age is 1 : 4. In 6 years the ratio will be 2 : 5. How old is Tom\'s mother now?', 24,
    ['The age gap never changes. Now the gap is 3 of today\'s parts; in 6 years it is 3 of the later parts (5 − 2).',
     'So a part is the same size at both times. Tom goes from 1 part to 2 parts in 6 years, so one part is 6 years.',
     'Tom\'s mother is 4 × 6 = 24 now.'],
    'Check: now 6 and 24 (1 : 4); in 6 years 12 and 30 (2 : 5).',
    'When two quantities grow by the same amount, their difference is the fixed thing to compare.')
B['FRAC-02', 'try', 5] = P('The ingredient that runs out first',
    'A biscuit recipe uses flour, sugar and butter in the ratio 6 : 2 : 3 by weight. Kai has 900 g of flour, 250 g of sugar and 480 g of butter. What is the greatest total weight of mixture he can make, in grams, keeping to the recipe?', 1375,
    ['Find how big one part could be for each ingredient: flour 900 ÷ 6 = 150 g, sugar 250 ÷ 2 = 125 g, butter 480 ÷ 3 = 160 g.',
     'Sugar allows the smallest part, 125 g, so it runs out first. The mixture has 6 + 2 + 3 = 11 parts: 11 × 125 = 1375 g.'],
    'Check the amounts used: 750 g flour, 250 g sugar and 375 g butter, all available.',
    'In a fixed ratio, the scarcest ingredient decides the size of one part.')
B['FRAC-02', 'transfer', 5] = P('Two gears in mesh',
    'Gear A has 24 teeth and meshes with gear B, which has 40 teeth. When gear A makes 35 complete turns, how many complete turns does gear B make?', 21,
    ['Meshed gears pass the same number of teeth. Gear A passes 24 × 35 = 840 teeth.',
     'Gear B needs 40 teeth for each turn, so it makes 840 ÷ 40 = 21 turns.'],
    'The larger gear turns fewer times: the turns are in the ratio 40 : 24 = 5 : 3 the other way round, and 35 : 21 = 5 : 3.',
    'Some quantities are in inverse ratio: more teeth means fewer turns.')
B['FRAC-02', 'try', 6] = P('A tower measured by its shadow',
    'A vertical pole 2 m tall casts a shadow 3 m long. At the same moment a tower casts a shadow 27 m long on the same level ground. How tall is the tower, in metres?', 18,
    ['The sun\'s rays make the same angle for both, so height : shadow is the same ratio, 2 : 3.',
     'The tower\'s shadow is 27 ÷ 3 = 9 times as long as the pole\'s, so the tower is 9 × 2 = 18 m tall.'],
    'Check the ratio: 18 : 27 = 2 : 3.',
    'Shapes with the same angles are scaled copies; one scale factor links every pair of matching lengths.')
B['FRAC-02', 'transfer', 6] = P('Two jugs of the same shape',
    'Two jugs have exactly the same shape. The smaller is 10 cm tall and holds 300 mL. The larger is 20 cm tall. How many millilitres does the larger jug hold?', 2400,
    ['Every length of the larger jug is 2 times the matching length of the smaller one.',
     'Volume depends on three lengths multiplied together, so the volume is multiplied by 2 × 2 × 2 = 8: 300 × 8 = 2400 mL.'],
    'Test with cubes: a cube of side 2 contains 8 unit cubes, not 2.',
    'A scale factor for lengths is cubed for volumes.')
B['FRAC-02', 'try', 7] = P('Mixing two jugs of cordial',
    'Jug A holds 3 litres of drink mixed in the ratio cordial : water = 1 : 2. Jug B holds 4 litres mixed in the ratio cordial : water = 3 : 1. Both jugs are poured into a large bowl. How many litres of water must be added to the bowl so that cordial and water are in the ratio 1 : 1?', 1,
    ['Jug A has 1 litre of cordial and 2 litres of water. Jug B has 3 litres of cordial and 1 litre of water.',
     'The bowl has 4 litres of cordial and 3 litres of water. One more litre of water makes them equal.'],
    'You cannot average the ratios 1 : 2 and 3 : 1 directly, because the jugs are different sizes; work with actual amounts.',
    'Convert each ratio into real quantities before combining mixtures.')
B['FRAC-02', 'transfer', 7] = P('A choir whose ratio shifts',
    'In a choir the ratio of boys to girls is 3 : 5. After 6 boys join and 6 girls leave, the ratio becomes 3 : 4. How many children were in the choir at first?', 112,
    ['The total number of children does not change, so compare using the total. At first boys are 3/8 of the choir; afterwards they are 3/7.',
     'Use a total that both 8 and 7 divide: 56 parts. Boys go from 21 parts to 24 parts, a gain of 3 parts, which is the 6 boys who joined. One part is 2 children.',
     'The choir has 56 × 2 = 112 children.'],
    'Check: 42 boys and 70 girls (3 : 5) become 48 and 64 (3 : 4).',
    'When the total stays fixed, rewrite both ratios with the same total number of parts.')

# ---------------------------------------------------------------- COUNT-01
B['COUNT-01', 'try', 2] = P('Digits with product twenty-four',
    'How many three-digit numbers have digits whose product is 24?', 21,
    ['Find the sets of three digits with product 24: {1, 3, 8}, {1, 4, 6}, {2, 2, 6} and {2, 3, 4}.',
     'Three different digits can be arranged in 6 orders; {2, 2, 6} has only 3 orders. Total 6 + 6 + 3 + 6 = 21.'],
    'To be sure no set is missing, go through the smallest digit in order: 1 (then 3 × 8 or 4 × 6), 2 (then 2 × 6 or 3 × 4); a smallest digit of 3 would need a product of at least 27.',
    'First list the unordered sets in a fixed order, then count the arrangements of each.')
B['COUNT-01', 'transfer', 2] = P('Triangles with perimeter fifteen',
    'Two triangles count as the same if they have the same three side lengths. How many different triangles have whole-number side lengths, in centimetres, and perimeter 15 cm?', 7,
    ['The longest side must be less than the sum of the other two, so it is less than half the perimeter: at most 7. It is also at least 5, since the sides average 5.',
     'Longest side 7: the others add to 8 and are at most 7: (1, 7), (2, 6), (3, 5), (4, 4), giving 4 triangles. Longest side 6: the others add to 9 and are at most 6: (3, 6), (4, 5), giving 2. Longest side 5: (5, 5), giving 1.',
     'Total 4 + 2 + 1 = 7.'],
    'Each case obeys the triangle rule automatically, because the two shorter sides add to more than the longest.',
    'Organise the list by the largest side, and use the triangle rule to limit it.')
B['COUNT-01', 'try', 3] = P('Pairs adding to a multiple of five',
    'Two different numbers are chosen from 1, 2, 3, …, 10, and the order in which they are chosen does not matter. In how many ways can this be done so that their sum is a multiple of 5?', 9,
    ['The sum is between 3 and 19, so it must be 5, 10 or 15.',
     'Sum 5: 1 + 4, 2 + 3. Sum 10: 1 + 9, 2 + 8, 3 + 7, 4 + 6. Sum 15: 5 + 10, 6 + 9, 7 + 8.',
     'That is 2 + 4 + 3 = 9 pairs.'],
    '5 + 5 is not allowed because the numbers must be different.',
    'Split by the possible totals, and list each case from the smallest first number upwards.')
B['COUNT-01', 'transfer', 3] = P('Even numbers with rising digits',
    'A four-digit number uses four different digits from 1, 2, 3, 4, 5, 6, written in increasing order from left to right. How many such numbers are even?', 11,
    ['The last digit is the largest of the four and must be even. It cannot be 2, since three smaller digits would be needed.',
     'Last digit 4: the other digits must be 1, 2, 3, giving 1 number. Last digit 6: choose any 3 of the digits 1 to 5, and there are 10 ways to do that.',
     'Total 1 + 10 = 11.'],
    'The 10 choices are easiest to count as the 10 ways to leave out 2 of the 5 digits.',
    'Once the order is forced, counting numbers becomes counting sets of digits.')
B['COUNT-01', 'try', 4] = P('Three dice totalling ten',
    'Three ordinary dice are rolled and the numbers showing add to 10. Counting 1, 3, 6 as the same set as 6, 3, 1, how many different sets of three numbers are possible?', 6,
    ['List the sets from the smallest number upwards. Smallest 1: 1, 3, 6 and 1, 4, 5. Smallest 2: 2, 2, 6; 2, 3, 5; 2, 4, 4. Smallest 3: 3, 3, 4.',
     'The smallest number cannot be 4, since 4 + 4 + 4 is more than 10. That gives 2 + 3 + 1 = 6 sets.'],
    'No number may exceed 6, which is why 1, 2, 7 and 1, 1, 8 are not listed.',
    'Write each set in increasing order so that no set is listed twice.')
B['COUNT-01', 'transfer', 4] = P('A middle digit equal to a sum',
    'How many three-digit numbers have a middle digit equal to the sum of the first and last digits?', 45,
    ['Choose the first digit a (1 to 9) and last digit c (0 to 9). The middle digit a + c must be at most 9.',
     'For a = 1 there are 9 choices of c (0 to 8); for a = 2 there are 8; and so on down to 1 choice for a = 9.',
     'Total 9 + 8 + … + 1 = 45.'],
    'Each allowed pair a, c gives exactly one number, such as 396 or 110.',
    'Choose the free digits and count how the restriction limits them case by case.')
B['COUNT-01', 'try', 5] = P('A four-stripe flag',
    'A flag has 4 horizontal stripes. Each stripe is red, white or blue. Stripes that touch must be different colours, and the top and bottom stripes must also be different from each other. How many flags are possible?', 18,
    ['Ignoring the top-and-bottom rule, choose the stripes from the top: 3 × 2 × 2 × 2 = 24 flags.',
     'Now count those where the top and bottom match. Choose the top (3 ways) and the second stripe (2 ways). The third stripe must differ from the second and from the bottom, which equals the top: only 1 way. That is 6 flags.',
     'Allowed flags: 24 − 6 = 18.'],
    'Direct check with a red top stripe: RWRW, RWRB, RWBW, RBRB, RBRW and RBWB, which is 6 flags. The same holds for each top colour, and 3 × 6 = 18.',
    'Count without the awkward rule, then subtract the arrangements that break it.')
B['COUNT-01', 'transfer', 5] = P('Three primes adding to thirty',
    'If the order of the primes does not matter, in how many ways can 30 be written as the sum of three different prime numbers?', 2,
    ['Three odd numbers have an odd sum, but 30 is even. So one of the primes must be 2, the only even prime.',
     'The other two primes are different and add to 28: 5 + 23 and 11 + 17 work (3 + 25 and 7 + 21 fail, and 13 + 15 fails).',
     'There are 2 ways: 2 + 5 + 23 and 2 + 11 + 17.'],
    'Check the candidates below 14 in order: 3, 5, 7, 11, 13 pair with 25, 23, 21, 17, 15.',
    'A parity argument can remove almost every case before any listing starts.')
B['COUNT-01', 'try', 6] = P('Digit sum nine up to two hundred',
    'How many whole numbers from 1 to 200 have digits that add to 9?', 19,
    ['One-digit: only 9. Two-digit: 18, 27, 36, 45, 54, 63, 72, 81, 90, which is 9 numbers.',
     'From 100 to 199 the last two digits must add to 8: 108, 117, …, 180, which is 9 numbers. The number 200 does not work.',
     'Total 1 + 9 + 9 = 19.'],
    'These are also the multiples of 9 with digit sum exactly 9; 99, 189 and 198 are multiples of 9 with digit sum 18, so they are not counted.',
    'Break the range into blocks with the same number of digits and count each block.')
B['COUNT-01', 'transfer', 6] = P('Climbing with steps of two and three',
    'A staircase has 10 steps. Zoe climbs it taking either 2 steps or 3 steps with each stride, and lands exactly on the top step. In how many different orders of strides can she do this?', 7,
    ['Try each possible number of 3-step strides. With no 3s she needs five 2s: 1 order. With two 3s she needs two 2s, making 4 strides.',
     'One 3 or three 3s leave an odd number of steps, which 2s cannot fill. With two 3s and two 2s, choose which 2 of the 4 strides are the 3s: 6 orders.',
     'Total 1 + 6 = 7.'],
    'The six orders are 3322, 3232, 3223, 2332, 2323 and 2233.',
    'Split by how many of one kind are used, then count the orders within each case.')

def curate2(skill, role, visit, original):
    """Return the reauthored problem for this (skill, role, visit), or the original."""
    return B.get((skill, role, visit), original)
