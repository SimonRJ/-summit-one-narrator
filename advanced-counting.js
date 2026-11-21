/* Original, read-only mathematical enrichment: sequences, counting, logic. */
export const advancedCounting = [
 [
  "SEQ-01",
  "Pairing a sequence creates a formula",
  "A fixed-increment pattern has a useful symmetry from beginning to end.",
  "Find 1 + 2 + 3 + ... + 100 without long addition.",
  [
   "Pair the first and last: 1 + 100 = 101.",
   "Every pair gives 101, and there are 50 pairs.",
   "The sum is 50 × 101 = 5050. In general, 1 + ... + n = n(n+1)/2."
  ],
  "Count both endpoints before pairing the first and last terms.",
  "What is the sum of the odd numbers from 21 through 59?",
  "There are 20 terms. Pair 21 with 59, 23 with 57, and continue inwards. Ten pairs each total 80, so the sum is 800."
 ],
 [
  "SEQ-02",
  "Doubling series can telescope",
  "Repeated doubling looks enormous but has a surprising short total.",
  "Find 1 + 2 + 4 + 8 + ... + 1024.",
  [
   "Call the total S. Doubling makes 2S = 2 + 4 + ... + 2048.",
   "Subtract the original S; all middle powers cancel.",
   "S = 2048 − 1 = 2047."
  ],
  "Distinguish the latest term from everything accumulated so far.",
  "On day one a collection gains one token. Each day it gains twice as many as the day before. At the end of which day does the total first exceed 200?",
  "Seven days give 1 + 2 + … + 64 = 127. On day eight another 128 arrive, taking the total to 255. Day eight is the first."
 ],
 [
  "SEQ-03",
  "Fibonacci numbers can count tiled paths",
  "Recurrences turn a large counting problem into a few smaller ones.",
  "How many ways can a 1 by 5 strip be covered with 1 by 1 and 1 by 2 tiles?",
  [
   "Every tiling ends with either a square or a domino.",
   "If T(n) is the number of length-n tilings, T(n) = T(n−1) + T(n−2).",
   "Starting T(1)=1 and T(2)=2, the next counts are 3, 5, 8. So T(5)=8."
  ],
  "When the number of long tiles is fixed, count the order of the tiles themselves.",
  "How many tilings of a strip of length 6 use exactly two dominoes and only unit squares for the rest?",
  "Two dominoes occupy four cells. The other two cells need two unit squares. Arrange the four tiles by choosing two of their four positions for dominoes. There are six choices."
 ],
 [
  "SEQ-04",
  "Finite transformations eventually cycle",
  "If the same rule always gives the next state, returning to a previous state starts a repeat.",
  "Starting at 1, keep doubling and taking the remainder after division by 5. Where are you after 2027 operations?",
  [
   "The states are 1 → 2 → 4 → 3 → 1, a cycle of four.",
   "2027 leaves remainder 3 after division by 4.",
   "Three moves after 1 lands on 3."
  ],
  "Write the starting state next to move zero so that the cycle index is clear.",
  "Start with 0. At each move, double the number, add 1, then take the remainder on division by 7. Where are you after 100 moves?",
  "The states are 0 → 1 → 3 → 0. After 99 moves there have been 33 complete cycles. The next move gives 1."
 ],
 [
  "COUNT-01",
  "Organised lists grow into integer partitions",
  "Ordering cases prevents you from accidentally counting rearrangements several times.",
  "How many positive integer triples x ≤ y ≤ z satisfy x+y+z=10?",
  [
   "If x=1, the pairs (y,z) are (1,8),(2,7),(3,6),(4,5): 4.",
   "If x=2, use (2,6),(3,5),(4,4): 3. If x=3, use (3,4): 1.",
   "x≥4 is impossible. Total 4+3+1=8 triples."
  ],
  "Sorting removes rearrangements, but an equal pair can still appear at either end.",
  "Among the positive triples in the example, how many have exactly two equal numbers?",
  "The triples are (1,1,8), (2,2,6), (2,4,4) and (3,3,4). Equal numbers can occupy either the first two or the last two positions in a sorted triple. There are four."
 ],
 [
  "COUNT-02",
  "Choosing a team introduces combinations",
  "When order does not matter, ordered selections overcount the same group.",
  "How many different three-person teams can be chosen from eight people?",
  [
   "There are 8 × 7 × 6 = 336 ordered selections.",
   "Every team appears 3 × 2 × 1 = 6 times in different orders.",
   "Divide: 336/6 = 56. This is written C(8,3)."
  ],
  "When a restriction excludes only a few choices, count the excluded groups directly.",
  "Eight people can form 56 three-person teams. How many teams are allowed if two particular people cannot serve together?",
  "For a forbidden team, include the two specified people and choose one of the other six. Remove those six teams from 56 to get 50."
 ],
 [
  "COUNT-03",
  "Treat neighbours as a block",
  "Restricted arrangements become easier when two items must stay together.",
  "Five people stand in a line. How many orders have A and B adjacent?",
  [
   "Treat A and B as one block, giving four objects to arrange.",
   "The objects have 4! = 24 orders.",
   "AB or BA are both possible inside the block, so 24 × 2 = 48."
  ],
  "Translate a spacing condition into possible places before arranging the people.",
  "Five people line up. In how many arrangements is there exactly one person between A and B?",
  "The two positions can be first and third, second and fourth, or third and fifth. A and B can swap within each pair of positions. The other three people have six orders. The count is 3 × 2 × 6 = 36."
 ],
 [
  "COUNT-04",
  "Overlapping sets require subtraction",
  "When two groups overlap, simply adding their sizes counts their shared members twice.",
  "How many integers from 1 to 100 are multiples of 2 or 3?",
  [
   "There are 50 multiples of 2 and 33 multiples of 3.",
   "The 16 multiples of 6 were included in both counts.",
   "Subtract the overlap: 50+33−16=67."
  ],
  "Decide how many times the overlap is supposed to count in the final answer.",
  "From 1 to 100 inclusive, how many numbers are divisible by exactly one of 2 and 3?",
  "There are 50 even numbers and 33 multiples of 3. The 16 multiples of 6 appear in both lists and must appear in neither final group. Subtract twice 16 to get 51."
 ],
 [
  "COUNT-05",
  "Count a handshake from both ends",
  "The same connection can be counted at each of its two endpoints.",
  "Nine people meet. Each pair shakes hands once. How many handshakes take place?",
  [
   "Every person reports eight handshakes, giving 9 × 8 = 72 reports.",
   "Each actual handshake was reported twice.",
   "Divide by two: 72/2 = 36 handshakes."
  ],
  "An odd total can disprove a set of reports without identifying who made a mistake.",
  "At a gathering of seven people, six report four handshakes each and one reports three. Can all the reports be correct?",
  "The reports total 6 × 4 + 3 = 27. Each handshake adds two reports, so the total has to be even. At least one report is mistaken."
 ],
 [
  "COUNT-06",
  "Split into complete, non-overlapping cases",
  "A strong counting solution covers every possibility without counting any possibility twice.",
  "Using digits 1 to 5 exactly once, how many five-digit numbers are odd?",
  [
   "The final digit must be 1, 3 or 5: three disjoint cases.",
   "For each ending, arrange the other four digits in 4! = 24 ways.",
   "The total is 3 × 24 = 72 odd numbers."
  ],
  "Start with the position that decides the size and then reconsider the remaining endings.",
  "Use each of 1, 2, 3, 4 and 5 once. How many of the resulting numbers are both even and greater than 40,000?",
  "If the first digit is 4, the last must be 2. This gives six middle orders. If the first is 5, the last can be 2 or 4, giving twelve more orders. The total is 18."
 ],
 [
  "LOGIC-01",
  "Contradiction can identify a liar",
  "A statement that defeats its own truth assumption gives surprisingly strong information.",
  "Each of A and B either always tells the truth or always lies. A says, “Both of us are liars.” Which one tells the truth?",
  [
   "If A were telling the truth, A would be a liar: contradiction.",
   "Therefore A is lying and the whole statement is false.",
   "Because A already is a liar, B must be truthful."
  ],
  "Keep every assignment that satisfies all of the statements, even if a puzzle sounds as though it has one solution.",
  "A says that B always lies. B says that A always lies. Each always lies or always tells the truth. Can you identify the truthful speaker?",
  "Exactly one is truthful. A truthful A with a lying B fits both statements. A lying A with a truthful B also fits both. The statements do not distinguish these two possibilities."
 ],
 [
  "LOGIC-02",
  "Before-and-after rules form a directed graph",
  "Some puzzles give only constraints on order, not exact positions.",
  "Three tasks must be completed once each. A comes before C, and C before B. How many orders satisfy both rules?",
  [
   "The first rule forces A earlier than C.",
   "The second forces C earlier than B.",
   "Together they give the unique order A, C, B."
  ],
  "Temporarily remove an unrestricted item, solve the smaller ordering puzzle and insert it again.",
  "Task A must come before both B and C. Task D can go anywhere. How many orders of the four tasks work?",
  "First arrange A, B and C. The possibilities are ABC and ACB. For each, insert D in one of four gaps, including the two ends. That gives eight orders."
 ],
 [
  "LOGIC-03",
  "Magic squares hide a centre invariant",
  "Rather than trial and error, equal line totals produce equations.",
  "A 3 by 3 magic square uses 1 through 9. Every row, column and diagonal sums to the same number. What is its centre?",
  [
   "The numbers sum to 45, so each row totals 15.",
   "The four lines through the centre total 60; together they count all nine cells once and the centre three extra times.",
   "So 60 = 45 + 3c, giving centre c = 5."
  ],
  "An operation applied to every entry can preserve equal sums and transport a known result.",
  "Double every entry of a 3 by 3 magic square containing 1 to 9. What is the new centre and what do two opposite outer cells add to?",
  "The original centre is 5 and opposite outer cells sum to 10. Doubling every entry preserves equal line sums and doubles both quantities. The centre becomes 10 and opposite cells sum to 20."
 ],
 [
  "LOGIC-04",
  "A proof shows you found every answer",
  "Finding examples is different from showing no other answers exist.",
  "Find all real numbers x satisfying x²=x.",
  [
   "Rearrange to x²−x=0.",
   "Factor: x(x−1)=0.",
   "At least one factor is zero, so x=0 or x=1. Both work."
  ],
  "Before dividing by an expression containing the unknown, check when that expression is zero.",
  "Find all real numbers satisfying x(x − 2) = 3(x − 2).",
  "Moving all terms to the left gives (x − 2)(x − 3) = 0. Both 2 and 3 work. Dividing by x − 2 at the start would lose the solution 2."
 ]
];
