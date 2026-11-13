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
  "Pairing leads to triangular numbers and algebraic summation proofs.",
  "What is the sum from 101 to 200?",
  "There are 100 numbers with average 150.5, so the sum is 15050."
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
  "This is the beginning of geometric series and exponential growth.",
  "Why does the answer fall exactly one below the next power of 2?",
  "Because doubling the sum shifts each term and all intermediate terms cancel."
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
  "This links patterns to dynamic programming and route counting.",
  "How many tilings does a 1 by 6 strip have?",
  "T(6) = 8 + 5 = 13."
 ],
 [
  "SEQ-04",
  "Finite transformations eventually cycle",
  "Repeated operations on a small set of states must revisit an earlier state.",
  "Starting at 1, keep doubling and taking the remainder after division by 5. Where are you after 2027 operations?",
  [
   "The states are 1 → 2 → 4 → 3 → 1, a cycle of four.",
   "2027 leaves remainder 3 after division by 4.",
   "Three moves after 1 lands on 3."
  ],
  "This is the start of finite-state mathematics and modular dynamics.",
  "What happens after 2028 operations?",
  "A multiple of four moves returns to 1."
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
  "Partitions of integers are a recurring theme in deeper counting competitions.",
  "Why insist x ≤ y ≤ z?",
  "It picks one order for each group so permutations are not counted repeatedly."
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
  "Combinations lead to Pascal's triangle and binomial coefficients.",
  "How many four-person teams can be chosen?",
  "C(8,4) = 70."
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
  "Advanced permutation problems can combine adjacency with forbidden positions.",
  "How many orders keep A and B apart?",
  "5! − 48 = 120 − 48 = 72."
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
  "Inclusion–exclusion extends to three or more sets and probability.",
  "Why subtract multiples of 6?",
  "They are precisely the numbers counted twice."
 ],
 [
  "COUNT-05",
  "Count a handshake from both ends",
  "The same connection can be counted at each of its two endpoints.",
  "Nine people shake hands exactly once with every other person. How many handshakes?",
  [
   "Every person reports eight handshakes, giving 9 × 8 = 72 reports.",
   "Each actual handshake was reported twice.",
   "Divide by two: 72/2 = 36 handshakes."
  ],
  "This is the beginning of graph theory and the handshake lemma.",
  "Can an odd number of people each shake hands an odd number of times?",
  "No. The sum of everyone's handshake counts is even, so the number of odd counts must be even."
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
  "Case partitions are essential in olympiad counting and probability.",
  "How many of these numbers are even?",
  "There are two even endings, each with 4! arrangements: 48."
 ],
 [
  "LOGIC-01",
  "Contradiction can identify a liar",
  "A statement that defeats its own truth assumption gives surprisingly strong information.",
  "A and B are always truthful or always lying. A says, 'Both of us are liars.' What follows?",
  [
   "If A were telling the truth, A would be a liar: contradiction.",
   "Therefore A is lying and the whole statement is false.",
   "Because A already is a liar, B must be truthful."
  ],
  "Reasoning by contradiction is a central olympiad proof technique.",
  "Could both of them be liars?",
  "No. Then A's statement would be true, impossible for a liar."
 ],
 [
  "LOGIC-02",
  "Before-and-after rules form a directed graph",
  "Some puzzles give only constraints on order, not exact positions.",
  "Three tasks A, B and C must follow A before C and C before B. How many orders are allowed?",
  [
   "The first rule forces A earlier than C.",
   "The second forces C earlier than B.",
   "Together they give the unique order A, C, B."
  ],
  "Longer precedence puzzles lead to directed graphs and topological sorting.",
  "If only A before B were required, how many orders of A, B and C would be allowed?",
  "There are 3! = 6 total orders, exactly half with A before B: 3."
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
  "This combines symmetry, equations and double counting.",
  "What do two opposite outer cells add to?",
  "Each opposite pair plus the centre totals 15, so the pair sums to 10."
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
  "Factorisation is a useful way to prove a list of solutions is complete.",
  "Does x²=1 have only x=1?",
  "No. It also has x=−1."
 ]
];
