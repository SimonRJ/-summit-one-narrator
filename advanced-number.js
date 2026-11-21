/* Original, unassessed advanced enrichment, number/algebra families. */
export const advancedNumber = [
 [
  "DIG-01",
  "Difference of squares",
  "The same middle number appears in both factors. How far away on either side are they?",
  "Calculate 998 × 1002 mentally.",
  [
   "Write it as (1000 − 2)(1000 + 2).",
   "The middle terms cancel: (a − b)(a + b) = a² − b².",
   "So 998 × 1002 = 1000² − 2² = 999996."
  ],
  "Look for factors equally far from a convenient middle number.",
  "Which is larger, 48 × 52 or 49 × 51, and by how much?",
  "Both products sit just below 50². The first is 2500 − 4 and the second is 2500 − 1, so 49 × 51 is larger by 3."
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
  "Pick the most restricted position first. A leading zero and a zero in the middle play different roles.",
  "How many of the four-digit numbers in the example contain a zero?",
  "All 60 that end in zero qualify. If the last digit is 5, the first has four choices, zero has two middle positions and the final free digit has three choices. That adds 24, giving 84."
 ],
 [
  "DIG-03",
  "A digit-position invariant",
  "Long digit-counting tasks become short when each place is equally balanced.",
  "How many 7s occur in the integers from 1 to 999?",
  [
   "Imagine all strings from 000 to 999; padding with zeroes adds no 7s.",
   "A 7 in the units column leaves 10 × 10 choices for the other two digits, giving 100 appearances. The same count works for tens and hundreds.",
   "The total is 100 + 100 + 100 = 300. The number 777 counts three times."
  ],
  "Count a digit by position and check the final incomplete block.",
  "Pages 1 to 275 are numbered. How many times must the printer use the digit 7?",
  "There are 27 sevens in the units column, from 7 to 267. The tens column has ten each in 70–79 and 170–179, then six in 270–275. The total is 27 + 20 + 6 = 53."
 ],
 [
  "DIG-04",
  "Repunits and divisibility by 11",
  "Since 10 leaves remainder −1 on division by 11, successive place values alternate between remainders +1 and −1.",
  "Explain why 111111 is divisible by 11 without dividing.",
  [
   "For divisibility by 11, alternate plus and minus signs between successive digits.",
   "Here the alternating sum is 1 − 1 + 1 − 1 + 1 − 1 = 0.",
   "Therefore 11 divides 111111. Every repunit with an even number of digits has this property."
  ],
  "A missing digit often turns a divisibility test into a short equation.",
  "In the four-digit number 6□48, which digit makes the number divisible by 11?",
  "The alternating sum is 6 − □ + 4 − 8 = 2 − □. As the digit runs from 0 to 9, the only attainable multiple of 11 is zero. The missing digit is 2."
 ],
 [
  "DIG-05",
  "Cryptarithms become algebra",
  "When a letter stands for a digit, its place gives the coefficient.",
  "AB and BA are two-digit numbers written with nonzero, different digits. Find every ordered pair (A, B) for which AB + BA = 99.",
  [
   "By place value, AB = 10A + B and BA = 10B + A.",
   "So AB + BA = 11(A + B) = 99, hence A + B = 9.",
   "The valid pairs are (1,8), (2,7), (3,6), (4,5) and their reversals: 8 in total."
  ],
  "Write down the value of each place before combining letters that appear more than once.",
  "The three-digit numbers ABA and BAB differ by 273, with ABA larger. Their two different digits add to 11. What is ABA?",
  "Subtracting the place values gives 91 × (A − B) = 273. The digits differ by 3 and add to 11, so A = 7 and B = 4. Check that 747 − 474 = 273."
 ],
 [
  "DIV-01",
  "Divisors as choices of prime powers",
  "Prime factorisation can count all divisors without listing them.",
  "How many positive divisors does 360 have? How many of them are even?",
  [
   "Factor 360 = 2³ × 3² × 5.",
   "A divisor chooses the exponent of 2 in 4 ways, of 3 in 3 ways and of 5 in 2 ways: 4 × 3 × 2 = 24.",
   "For an even divisor, the power of 2 cannot be zero: 3 × 3 × 2 = 18."
  ],
  "A restriction on the divisor usually becomes a restriction on one or more prime exponents.",
  "How many positive divisors of 360 are perfect squares?",
  "Each prime needs an even exponent. For 2 choose 0 or 2, for 3 choose 0 or 2, and for 5 choose 0. The four square divisors are 1, 4, 9 and 36."
 ],
 [
  "DIV-02",
  "Synchronising several repeating events",
  "Two repeating events can have a common repeat interval.",
  "Two lights flash together at 0 seconds, then every 12 and 18 seconds respectively. How many more times do they flash together up to and including 180 seconds?",
  [
   "LCM(12,18) = 36 seconds.",
   "Common flash times are 36, 72, 108, 144 and 180 seconds.",
   "There are 5 such times; starting time 0 is excluded."
  ],
  "Find one shared moment before using the repeat interval when the starting times differ.",
  "One light starts at 0 seconds and flashes every 12 seconds. Another starts at 6 seconds and flashes every 18 seconds. When do they flash together in the first 100 seconds?",
  "The second light flashes at 6, 24, 42, 60, 78 and 96 seconds. Of these, 24, 60 and 96 are multiples of 12. The spacing is still 36 seconds, although the first coincidence is at 24."
 ],
 [
  "DIV-03",
  "Combining two remainder clues",
  "Each remainder clue gives a list. A solution belongs to both lists.",
  "Find the smallest positive integer leaving remainder 2 on division by 5 and remainder 1 on division by 3.",
  [
   "The first condition gives numbers 2, 7, 12, 17, 22, ...",
   "Check the second: 2 leaves remainder 2; 7 leaves remainder 1.",
   "The smallest is 7. Solutions repeat every LCM(5,3) = 15: 7, 22, 37, ..."
  ],
  "Keep the whole sequence of solutions until every clue has been applied.",
  "Which numbers between 100 and 200 satisfy both remainder clues and are also multiples of 4?",
  "The candidates start at 112 and rise by 15. Adding 15 changes the remainder modulo 4 by 3, so it takes four steps to return to a multiple of 4. The only answers are 112 and 172."
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
  "A colour imbalance can rule out a tiling even when the area divides exactly.",
  "A 5 by 5 board loses the square immediately to the right of its top-left corner. Can twelve dominoes cover the rest?",
  "Colour the top-left corner black. There are initially 13 black and 12 white squares. The removed square is white, leaving 13 black and 11 white. Twelve dominoes would need 12 of each."
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
  "You can add or multiply the final digits after reducing very large exponents to positions in a cycle.",
  "What is the units digit of 7²⁰²⁷ + 7²⁰²⁸?",
  "The first power ends in 3. Multiplying by 7 gives the next power a final digit of 1. The sum ends in 4."
 ],
 [
  "FRAC-01",
  "The whole changes when a fraction is taken",
  "A second fraction often refers to what is left, not the original amount.",
  "A tank starts full. A third of its water is poured away, then a quarter of what remains is used. What fraction of the full tank is left?",
  [
   "After the first action, 2/3 remains.",
   "Keeping 3/4 of that leaves (2/3) × (3/4).",
   "The remaining fraction of the original tank is 1/2."
  ],
  "Label the amount that each fraction acts on before going forwards or backwards.",
  "After a third of the water is poured away and a quarter of the remainder is used, 18 litres remain. How much water was there at first?",
  "The 18 litres are three quarters of the middle amount, so there were 24 litres after the first pour. That was two thirds of the starting amount, which was 36 litres."
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
  "Choose a convenient starting square when only a percentage or ratio is given.",
  "The area of a square grows by 69%. By what percentage does its side length grow?",
  "A square of area 100 has side 10. An area of 169 gives side 13. The side grows by 3 out of 10, or 30%."
 ],
 [
  "FRAC-03",
  "Compare nearby fractions without decimals",
  "Putting fractions over the same positive denominator preserves their order.",
  "Which is greater: 17/29 or 23/39?",
  [
   "Use 29 × 39 as the common denominator. Compare the two new numerators.",
   "17 × 39 = 663, while 23 × 29 = 667.",
   "Because 663 < 667, 17/29 < 23/39."
  ],
  "Check strict inequalities exactly whenever two rounded values look identical.",
  "Find a fraction strictly between 17/29 and 23/39 without using decimals.",
  "Add the numerators and add the denominators to get 40/68 = 10/17. Check both sides exactly. The first cross-products are 289 and 290, and the second are 390 and 391."
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
  "Recover the total from each mean before combining or removing a group.",
  "Two students join the combined group in the example. The mean of all 32 is now 75 points. What is the mean of the two newcomers?",
  "The new total is 32 × 75 = 2400 points. The original students contributed 2200 points. The two newcomers contributed 200 between them, so their mean is 100."
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
  "Draw the start and finish positions of the same point on a moving object.",
  "A 120-metre train travels at 72 km/h. How long passes between its front reaching a 180-metre bridge and its last carriage clearing it?",
  "The front travels 180 + 120 = 300 metres before the rear clears the bridge. At 20 metres per second, this takes 15 seconds."
 ],
 [
  "RATE-02",
  "Combined work rates add",
  "The time to finish and the fraction finished per hour are not the same thing.",
  "Two pipes fill an empty tank at constant rates. On its own, one takes 6 hours and the other takes 4 hours. How long do they take together?",
  [
   "Hourly filling rates are 1/6 and 1/4 of a tank.",
   "Together the rate is 1/6 + 1/4 = 5/12 tanks per hour.",
   "Time is 1 ÷ (5/12) = 12/5 hours = 2 hours 24 minutes."
  ],
  "Decide whether the amount grows or shrinks before dividing by the net rate.",
  "The tank starts half full. One pipe can fill a tank in 6 hours and a drain can empty it in 4 hours. Both are open at their constant rates. When does the tank become empty?",
  "Each hour the tank loses 1/4 − 1/6 = 1/12 of its full capacity. Half a tank is six twelfths, so it empties in 6 hours."
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
  "Convert the target average into a time budget for the whole trip.",
  "A cyclist rides the first half of a route at 24 km/h. What speed on the second half would give an overall average of 36 km/h?",
  "Use 72 km for each half. A 144 km trip at an average of 36 km/h must take 4 hours. The first half uses 3 hours, leaving 1 hour for 72 km. The required speed is 72 km/h."
 ],
 [
  "RATE-04",
  "Measure the closing speed",
  "Two moving objects may be replaced by one closing-rate calculation.",
  "Two trains travel towards each other at constant speeds of 70 and 50 km/h. Their fronts start 180 km apart. When do their fronts meet?",
  [
   "The gap shrinks at 70 + 50 = 120 km/h.",
   "Time = distance ÷ closing speed = 180/120 hours.",
   "They meet after 1.5 hours."
  ],
  "Choose a pair of matching points and ask how their separation changes each hour.",
  "Two trains travel in the same direction at 70 and 50 km/h. The faster train starts 12 km behind. How many minutes until their fronts are level?",
  "The faster train gains 20 km each hour. It needs 12/20 of an hour to close the gap, which is 36 minutes."
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
  "A symmetric list has its mean at the centre.",
  "Five consecutive odd numbers add to 155. What is the smallest?",
  "The middle number is the mean, 155 ÷ 5 = 31. Two steps of size 2 to its left give 27. The five numbers are 27, 29, 31, 33 and 35."
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
  "Pretend every item is the cheaper kind and count how much one replacement adds.",
  "Ten tickets are sold for a total of $46. Child tickets cost $3 and adult tickets cost $7. How many adult tickets were sold?",
  "Ten child tickets would bring in $30. Each replacement with an adult ticket adds $4. The extra $16 needs four replacements, so four adults bought tickets."
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
  "Look for a collection shared by two measurements and work out its value once.",
  "Two apples and one pear weigh 17 units. One apple and two pears weigh 19 units. All apples have the same weight and all pears have the same weight. How heavy is each?",
  "Combining both weighings gives three of each fruit weighing 36 units, so one apple and one pear weigh 12. Remove that pair from each weighing. An apple weighs 5 units and a pear weighs 7."
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
  "Undo one entire pass before undoing another.",
  "A machine doubles its input and subtracts 1. After the same number passes through twice, the output is 29. What was the starting number?",
  "To undo one pass, add 1 and divide by 2. The first undoing gives 15 and the second gives 8. Sending 8 through twice gives 15, then 29."
 ],
 [
  "ALG-05",
  "A total and a margin give two equations",
  "Winner-margin problems hide a sum and a difference.",
  "Two players score 63 points altogether. One finishes 7 points ahead. What are their scores?",
  [
   "Call the scores H and L: H + L = 63 and H − L = 7.",
   "Adding the equations gives 2H = 70 and H = 35.",
   "So L = 28. The difference is indeed 7."
  ],
  "A transferred point changes the gap on both sides while leaving the total fixed.",
  "The players have scores of 35 and 28. Two points are transferred from the leader to the other player. What is the new winning margin?",
  "The new scores are 33 and 30, a margin of 3. Moving two points across removes two from one score and adds two to the other, so the old margin of 7 shrinks by 4."
 ]
];
