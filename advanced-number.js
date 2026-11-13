/* Original, unassessed advanced enrichment, number/algebra families. */
export const advancedNumber = [
 [
  "DIG-01",
  "Difference of squares",
  "Compensating around 100 is the seed of an algebraic identity.",
  "Calculate 998 × 1002 mentally.",
  [
   "Write it as (1000 − 2)(1000 + 2).",
   "The middle terms cancel: (a − b)(a + b) = a² − b².",
   "So 998 × 1002 = 1000² − 2² = 999996."
  ],
  "This pattern later helps with factorisation, large-number comparisons and Junior AMC algebra.",
  "Can you calculate 997 × 1003 the same way?",
  "It is 1000² − 3² = 999991."
 ],
 [
  "DIG-02",
  "Count under two digit restrictions",
  "Position rules can be combined with divisibility and no repetition.",
  "How many four-digit numbers use four different digits from 0 to 5 and are divisible by 5?",
  [
   "They must end with 0 or 5, so separate two non-overlapping cases.",
   "Ending 0: 5 choices for the first digit, then 4 and 3; total 60.",
   "Ending 5: 4 choices for the first digit, then 4 and 3; total 48. Answer 108."
  ],
  "This case method appears in restricted permutations and olympiad counting.",
  "What changes if digits may repeat?",
  "Each ending has 5 × 6 × 6 = 180 possibilities, so total 360."
 ],
 [
  "DIG-03",
  "A digit-position invariant",
  "Long digit-counting tasks become short when each place is equally balanced.",
  "How many 7s occur in the integers from 1 to 999?",
  [
   "Imagine all strings from 000 to 999; padding with zeroes adds no 7s.",
   "A 7 appears in the units place 100 times; exactly the same applies to tens and hundreds.",
   "The total is 100 + 100 + 100 = 300. The number 777 counts three times."
  ],
  "This leads to digit-sum identities and expected values in probability.",
  "What is the average count of 7s in one random three-digit string?",
  "Three positions each have probability 1/10 of holding 7, so the average count is 3/10."
 ],
 [
  "DIG-04",
  "Repunits and divisibility by 11",
  "A string of repeated 1s hides a useful alternating remainder pattern.",
  "Explain why 111111 is divisible by 11 without dividing.",
  [
   "For divisibility by 11, alternate plus and minus signs between successive digits.",
   "Here the alternating sum is 1 − 1 + 1 − 1 + 1 − 1 = 0.",
   "Therefore 11 divides 111111. Every repunit with an even number of digits has this property."
  ],
  "This opens the door to modular arithmetic and repeating decimal arguments.",
  "Does the same test succeed for 11111?",
  "No: its alternating sum is 1, which is not divisible by 11."
 ],
 [
  "DIG-05",
  "Cryptarithms become algebra",
  "When a letter stands for a digit, its place gives the coefficient.",
  "Find all ordered nonzero distinct digits A and B satisfying AB + BA = 99.",
  [
   "By place value, AB = 10A + B and BA = 10B + A.",
   "So AB + BA = 11(A + B) = 99, hence A + B = 9.",
   "The valid pairs are (1,8), (2,7), (3,6), (4,5) and their reversals: 8 in total."
  ],
  "Harder letter puzzles combine algebra, carrying and unique-digit constraints.",
  "What if the target sum were 88?",
  "A + B = 8 gives 6 nonzero distinct ordered pairs."
 ],
 [
  "DIV-01",
  "Divisors as choices of prime powers",
  "Prime factorisation can count all divisors without listing them.",
  "How many divisors does 360 have, and how many are even?",
  [
   "Factor 360 = 2³ × 3² × 5.",
   "A divisor chooses the exponent of 2 in 4 ways, of 3 in 3 ways and of 5 in 2 ways: 4 × 3 × 2 = 24.",
   "For an even divisor, the power of 2 cannot be zero: 3 × 3 × 2 = 18."
  ],
  "This technique appears in number-theory problems involving perfect squares and divisor counts.",
  "How many divisors of 360 are odd?",
  "There are 24 − 18 = 6; equivalently choose no factor of 2."
 ],
 [
  "DIV-02",
  "Synchronising several repeating events",
  "A repeating situation can itself have a repeating pattern governed by the LCM.",
  "Lights flash every 12 and 18 seconds. How many simultaneous flashes occur after time 0 up to 180 seconds?",
  [
   "LCM(12,18) = 36 seconds.",
   "Common flash times are 36, 72, 108, 144 and 180 seconds.",
   "There are 5 such times; starting time 0 is excluded."
  ],
  "Later you can combine unequal remainder conditions, not just matching cycles.",
  "What if a third light flashes every 15 seconds?",
  "The first time all three coincide is LCM(12,18,15) = 180 seconds."
 ],
 [
  "DIV-03",
  "Combining two remainder clues",
  "Congruence clues can locate a number that ordinary arithmetic seems unable to pin down.",
  "Find the smallest positive integer leaving remainder 2 on division by 5 and remainder 1 on division by 3.",
  [
   "The first condition gives numbers 2, 7, 12, 17, 22, ...",
   "Check the second: 2 leaves remainder 2; 7 leaves remainder 1.",
   "The smallest is 7. Solutions repeat every LCM(5,3) = 15: 7, 22, 37, ..."
  ],
  "Combining congruences develops into the Chinese remainder theorem in advanced number theory.",
  "Find the smallest solution greater than 100.",
  "The pattern is 7 + 15k; the first above 100 is 112."
 ],
 [
  "DIV-04",
  "Colouring can prove impossibility",
  "Even and odd are simple invariants; more powerful invariants use a coloured board.",
  "Can an 8 by 8 chessboard, with opposite corner squares removed, be tiled with 1 by 2 dominoes?",
  [
   "A chessboard has 32 black and 32 white squares.",
   "Opposite corners share one colour, so removal leaves counts 30 and 32.",
   "Every domino covers one black and one white square, so tiling is impossible."
  ],
  "Colouring invariants are common in WAJO-style non-routine proofs.",
  "Why is checking only that 62 squares remain insufficient?",
  "62 is even, but parity of area misses the unequal colours."
 ],
 [
  "DIV-05",
  "The final digit of an enormous power",
  "Powers repeat their final digits in short cycles.",
  "What is the last digit of 7^2027?",
  [
   "The powers of 7 end in 7, 9, 3, 1, then repeat every four exponents.",
   "Since 2027 = 4 × 506 + 3, choose the third position.",
   "The final digit is 3, without computing the power."
  ],
  "This is modular arithmetic with a finite cycle, useful in difficult number problems.",
  "What is the last digit of 7^2028?",
  "Exponent 2028 is divisible by 4, so the final digit is 1."
 ],
 [
  "FRAC-01",
  "The whole changes when a fraction is taken",
  "A second fraction often refers to what is left, not the original amount.",
  "A third of a tank is emptied, then a quarter of what remains is used. What fraction is left?",
  [
   "After the first action, 2/3 remains.",
   "Keeping 3/4 of that leaves (2/3) × (3/4).",
   "The remaining fraction of the original tank is 1/2."
  ],
  "Changing reference wholes underlies compound percentages and conditional probability.",
  "What if half the remainder were used?",
  "Then (2/3) × (1/2) = 1/3 of the original would remain."
 ],
 [
  "FRAC-02",
  "Scale factors are squared for area",
  "A length ratio and an area ratio are different objects.",
  "Two similar squares have side ratio 3:5. Find their area ratio.",
  [
   "Use representative side lengths 3 and 5.",
   "Their areas are 3² = 9 and 5² = 25.",
   "The area ratio is 9:25 because area multiplies two lengths."
  ],
  "Similarity leads to geometry problems involving area and volume scaling.",
  "What is the volume ratio for similar cubes with side ratio 3:5?",
  "3³:5³ = 27:125."
 ],
 [
  "FRAC-03",
  "Compare nearby fractions without decimals",
  "Multiplying across denominators avoids dangerous rounding.",
  "Which is greater: 17/29 or 23/39?",
  [
   "Both denominators are positive, so compare cross-products.",
   "17 × 39 = 663, while 23 × 29 = 667.",
   "Because 663 < 667, 17/29 < 23/39."
  ],
  "Exact comparisons matter when olympiad bounds are extremely close.",
  "Why avoid rounding both to two decimal places?",
  "They might appear equal after rounding even though they are not."
 ],
 [
  "FRAC-04",
  "Averages need weights",
  "Combining the means of differently sized groups requires the groups' totals.",
  "Ten students average 60 points; twenty average 80. What is the overall mean?",
  [
   "Group totals are 10 × 60 = 600 and 20 × 80 = 1600.",
   "The combined total is 2200 among 30 students.",
   "The mean is 2200/30 = 73 and 1/3, not the unweighted average 70."
  ],
  "Weighted means appear in mixture problems and expected-value puzzles.",
  "When would averaging 60 and 80 directly work?",
  "When both groups have the same number of students."
 ],
 [
  "RATE-01",
  "Rates can be rewritten in new units",
  "A distance per hour can become a distance per second through exact unit cancellation.",
  "Convert 72 km/h into metres per second.",
  [
   "One kilometre is 1000 metres; one hour is 3600 seconds.",
   "Convert: 72 × 1000/3600 m/s.",
   "The answer is 20 m/s."
  ],
  "Rates with changing units lead to more advanced time-distance problems.",
  "How far does 20 m/s cover in 45 seconds?",
  "20 × 45 = 900 metres."
 ],
 [
  "RATE-02",
  "Combined work rates add",
  "The time to finish and the fraction finished per hour are not the same thing.",
  "One pipe fills a tank in 6 hours, another in 4. How long together?",
  [
   "Hourly filling rates are 1/6 and 1/4 of a tank.",
   "Together the rate is 1/6 + 1/4 = 5/12 tanks per hour.",
   "Time is 1 ÷ (5/12) = 12/5 hours = 2 hours 24 minutes."
  ],
  "The same reasoning applies to teams, machines and emptying tanks.",
  "What changes if the second pipe drains the tank?",
  "Subtract its rate rather than adding it."
 ],
 [
  "RATE-03",
  "Average speed is total distance over total time",
  "For equal-distance legs, the ordinary average of speeds is misleading.",
  "A cyclist travels out at 30 km/h and back the same distance at 60 km/h. Find average speed.",
  [
   "Choose 60 km each way: 2 hours out and 1 hour back.",
   "Total distance is 120 km over 3 hours.",
   "The average speed is 40 km/h, not 45 km/h."
  ],
  "This points towards the harmonic mean in later competition mathematics.",
  "Why is 40 closer to the slower speed?",
  "More time was spent travelling at 30 km/h."
 ],
 [
  "RATE-04",
  "Think about the gap, not the trains",
  "Two moving objects may be replaced by one closing-rate calculation.",
  "Trains approach each other at 70 and 50 km/h, starting 180 km apart. When do they meet?",
  [
   "The gap shrinks at 70 + 50 = 120 km/h.",
   "Time = distance ÷ closing speed = 180/120 hours.",
   "They meet after 1.5 hours."
  ],
  "Relative motion later introduces delayed starts and changing directions.",
  "If both travel the same way, what is the relative speed?",
  "Use the difference 70 − 50 = 20 km/h."
 ],
 [
  "ALG-01",
  "A letter can prove something about every example",
  "Expressing consecutive numbers algebraically reveals a general pattern.",
  "Three consecutive integers have sum 99. Find them.",
  [
   "Write them as x, x + 1 and x + 2.",
   "Then 3x + 3 = 99, giving x = 32.",
   "The integers are 32, 33, 34."
  ],
  "The same method can prove general facts about consecutive-number sums.",
  "Why is the sum of any three consecutive integers divisible by 3?",
  "Their total is 3(x + 1)."
 ],
 [
  "ALG-02",
  "Two totals reveal two hidden types",
  "A head count and a leg count give two simultaneous constraints.",
  "There are 12 hens and rabbits with 34 legs. How many rabbits?",
  [
   "If all were hens, there would be 2 × 12 = 24 legs.",
   "Each rabbit replaces a hen and adds two more legs.",
   "There are 34 − 24 = 10 extra legs, hence 5 rabbits."
  ],
  "This is a visual introduction to solving simultaneous equations.",
  "How many hens are there?",
  "12 − 5 = 7 hens."
 ],
 [
  "ALG-03",
  "Elimination removes one unknown",
  "A sum and a difference can be combined without guessing either number.",
  "The sum of two numbers is 50 and their difference is 8. Find both.",
  [
   "Write x + y = 50 and x − y = 8.",
   "Add them to cancel y: 2x = 58, so x = 29.",
   "Then y = 21. Both constraints check."
  ],
  "This is the starting point for systems of linear equations.",
  "What parity must the sum and difference have for integer answers?",
  "Both must be even or both odd."
 ],
 [
  "ALG-04",
  "Undo a function machine in reverse order",
  "An operation chain can be reversed by undoing its steps from the end.",
  "A machine triples a number, subtracts 5, then halves the result. Output is 11. Find the input.",
  [
   "Undo halving: double 11 to get 22.",
   "Undo subtracting 5: add 5 to get 27.",
   "Undo tripling: divide by 3 to find 9."
  ],
  "This opens the door to inverse functions and reversible transformations.",
  "Can squaring always be reversed uniquely?",
  "Not over all real numbers: 3 and −3 both square to 9."
 ],
 [
  "ALG-05",
  "A total and a margin give two equations",
  "Winner-margin problems hide a sum and a difference.",
  "Two players score 63 altogether; one beats the other by 7. What are the scores?",
  [
   "Call the scores H and L: H + L = 63 and H − L = 7.",
   "Adding the equations gives 2H = 70 and H = 35.",
   "So L = 28. The difference is indeed 7."
  ],
  "This reasoning appears in vote counts, sports scores and more involved linear puzzles.",
  "Why can a total 64 with difference 7 not give whole-number scores?",
  "They have opposite parity, so the calculated scores would contain halves."
 ]
];
