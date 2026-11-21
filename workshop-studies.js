// The five recall prompts are pinned to their authored technique and variant.
// The final problem on each visit asks for a new application without naming a method.
export const workshopEdition = "original-workshops-1";
export const workshopStudies = new Map([
  [16, {
    title: "The two signal flags",
    id: "DIV-03",
    prompt: "A blue flag rises at minute 2 and every 6 minutes after that. A gold flag rises at minute 1 and every 5 minutes after that. At which minute do both rise for the first time?",
    value: 26,
    hint: "Write the first few times for just one flag. Test them against the other flag’s starting time.",
    steps: [
      "The blue flag rises at minutes 2, 8, 14, 20 and 26.",
      "For the gold flag, subtract 1 from each candidate. The first difference divisible by 5 is 26 − 1 = 25.",
      "Minute 26 is four blue intervals after 2 and five gold intervals after 1."
    ],
    contrast: "The repeat interval tells you how far apart coincidences are. The initial offsets determine the first coincidence.",
    figure: "",
    recall: [["DIG-04",16],["SEQ-03",21],["ALG-04",26],["SOLID-01",31],["DIG-05",36]]
  }],
  [32, {
    title: "The paint that changed colour",
    id: "FRAC-02",
    prompt: "A tin contains blue and white paint in the ratio 3 to 5 by volume. A painter adds 14 mL of blue paint. The tin now holds equal volumes of blue and white. How many millilitres did it contain before the addition?",
    value: 56,
    hint: "Which colour has the same volume before and after the addition?",
    steps: [
      "The white paint initially exceeded the blue by two equal parts.",
      "Adding 14 mL closes that gap, so one original part was 14 ÷ 2 = 7 mL.",
      "There were eight parts before the addition, giving 8 × 7 = 56 mL. The new mixture contains 35 mL of each colour."
    ],
    contrast: "The requested volume belongs to the original mixture.",
    figure: "",
    recall: [["DIV-04",32],["COUNT-03",37],["DATA-02",42],["RATE-01",47],["DIG-01",0]]
  }],
  [48, {
    title: "Three readings on one scale",
    id: "ALG-03",
    prompt: "Three parcels are weighed two at a time. The three pair readings are 26 kg, 31 kg and 35 kg. What is the mass of the heaviest parcel in kilograms?",
    value: 20,
    hint: "What does adding all three readings count twice?",
    steps: [
      "The pair totals add to 92 kg. Each parcel appears on the scale twice, so the three parcels together weigh 46 kg.",
      "The pair weighing 26 kg leaves the greatest mass off the scale.",
      "That missing parcel weighs 46 − 26 = 20 kg. The other two weigh 15 kg and 11 kg, which reproduce all three readings."
    ],
    contrast: "The largest reading is a pair mass. The smallest pair omits the heaviest parcel.",
    figure: "",
    recall: [["FRAC-04",48],["RATE-02",1],["LOGIC-01",6],["SPATIAL-03",11],["GEO-01",16]]
  }],
  [64, {
    title: "Three different odd lengths",
    id: "COUNT-01",
    prompt: "Three rods have different positive odd lengths in centimetres. Their total length is 21 cm. How many different sets of three lengths are possible?",
    value: 7,
    hint: "Sort the lengths, then hold the shortest rod fixed.",
    steps: [
      "If the shortest is 1, the other pairs are (3,17), (5,15), (7,13) and (9,11).",
      "If it is 3, the pairs are (5,13) and (7,11). If it is 5, only (7,9) works.",
      "A shortest rod of at least 7 needs a total of at least 7 + 9 + 11 = 27. The count is 4 + 2 + 1 = 7 sets."
    ],
    contrast: "Rearranging the same three rods gives the same set.",
    figure: "",
    recall: [["FRAC-02",12],["RATE-03",17],["ALG-01",22],["DATA-03",27],["SEQ-01",32]]
  }],
  [80, {
    title: "A frame around the garden",
    id: "GEO-05",
    prompt: "A rectangular garden has perimeter 30 m and positive whole-number side lengths. A path 1 m wide runs along the inside of all four edges. What is the largest possible planting area in square metres?",
    value: 30,
    hint: "How does the path change each of the garden’s two dimensions?",
    steps: [
      "The outside length and width add to 15 m. Removing the path subtracts 2 m from each dimension, so the inside dimensions add to 11 m.",
      "For a fixed sum, moving one unit from the longer side to the shorter side increases the product whenever the sides differ by at least two.",
      "The closest whole numbers with sum 11 are 5 and 6. An outside garden of 7 m by 8 m achieves 30 square metres of planting area."
    ],
    contrast: "The path occupies both ends of each dimension.",
    figure: "",
    recall: [["DIV-02",28],["SPATIAL-02",33],["FRAC-01",38],["RATE-04",43],["ALG-02",48]]
  }],
  [96, {
    title: "Paint along three kinds of edge",
    id: "SOLID-02",
    prompt: "A solid block of 5 by 4 by 3 unit cubes is painted over its entire outside. The block is taken apart. How many little cubes have exactly two painted faces?",
    value: 24,
    hint: "Locate a cube with two painted faces. Can it be at a corner?",
    steps: [
      "Exactly two painted faces occur in the interiors of edges. Corners have three painted faces.",
      "Four edges of length 5 contribute three cubes each. Four edges of length 4 contribute two each. Four edges of length 3 contribute one each.",
      "The edge interiors are separate, so the total is 4 × (3 + 2 + 1) = 24."
    ],
    contrast: "A cuboid can have three different edge lengths. Count all three groups.",
    figure: "",
    recall: [["DIG-03",44],["DIV-01",49],["FRAC-03",2],["ALG-03",7],["SEQ-02",12]]
  }],
  [111, {
    title: "A closed crossing",
    id: "SPATIAL-01",
    prompt: "A walker goes from (0,0) to (4,2), moving one unit right or up each time. The crossing at (2,1) is closed. How many routes reach the destination?",
    value: 6,
    hint: "First count unrestricted routes. Then count exactly those that pass through the closed crossing.",
    steps: [
      "The full journey has six moves. Choosing two positions for the up moves gives 15 routes.",
      "To reach (2,1) takes two right moves and one up move, in three possible orders. The remainder has the same move counts and three orders.",
      "Nine routes use the crossing. Subtract them once from 15 to get 6 open routes."
    ],
    contrast: "Every forbidden route has one prefix and one suffix meeting at the closed crossing.",
    figure: "",
    recall: [["GEO-03",7],["SOLID-02",12],["DATA-01",17],["DIV-03",22],["DIG-02",27]]
  }],
  [128, {
    title: "The missing crate",
    id: "DATA-02",
    prompt: "Four crates are weighed in groups of three, leaving out a different crate each time. The four readings are 18, 20, 22 and 24 kg. How heavy is the lightest crate in kilograms?",
    value: 4,
    hint: "Count how many weighing groups contain any one crate.",
    steps: [
      "Every crate occurs in three readings. Their sum, 84 kg, is three times the combined mass.",
      "The four crates therefore weigh 28 kg together. Omitting the lightest gives the largest reading, 24 kg.",
      "The omitted crate weighs 28 − 24 = 4 kg. The other omitted masses are 6, 8 and 10 kg, which sum with 4 to 28."
    ],
    contrast: "Choose the heaviest group to find the lightest item left out.",
    figure: "",
    recall: [["ALG-05",24],["GEO-05",29],["SEQ-04",34],["COUNT-01",39],["LOGIC-02",44]]
  }],
  [136, {
    title: "Two empty seats at a round table",
    id: "COUNT-03",
    prompt: "Six seats around a table are numbered 1 through 6 in order. Exactly two seats must stay empty, and the empty seats must not be neighbours. How many pairs of seats could be empty?",
    value: 9,
    hint: "Count every pair first. Remember which seat is next to seat 1 on the other side.",
    steps: [
      "There are 6 × 5 ÷ 2 = 15 unordered pairs of seats.",
      "The circular table has six neighbouring pairs, including seats 6 and 1.",
      "Removing those six pairs leaves 9 possible pairs of empty seats."
    ],
    contrast: "The numbers distinguish positions even when the same arrangement could be rotated onto another.",
    figure: "",
    recall: [["GEO-02",32],["LOGIC-03",37],["SOLID-03",42],["SPATIAL-01",47],["DIV-05",0]]
  }],
  [144, {
    title: "Concentrating the syrup",
    id: "FRAC-03",
    prompt: "A 150 g syrup mixture is 20% sugar by mass. Only water evaporates. When sugar makes up 25% of the new mixture, how many grams of water have evaporated?",
    value: 30,
    hint: "Identify the mass that stays constant while the percentages change.",
    steps: [
      "The sugar weighs one fifth of 150 g, or 30 g.",
      "That same 30 g is now one quarter of the remaining mixture, so the mixture now weighs 120 g.",
      "The loss is 150 − 120 = 30 g, all of it water."
    ],
    contrast: "The two percentages refer to mixtures with different total masses.",
    figure: "",
    recall: [["COUNT-02",40],["LOGIC-04",45],["GEO-04",50],["SPATIAL-04",3],["ALG-04",8]]
  }],
  [160, {
    title: "Flip the two end tiles",
    id: "DIV-04",
    prompt: "Six white tiles stand in a row. A move turns over two neighbouring tiles, changing white to black or black to white. What is the fewest moves needed to leave just the two end tiles black?",
    value: 5,
    hint: "Number the five gaps. Which gap must be used to change tile 1?",
    steps: [
      "The first gap must be used an odd number of times. For tile 2 to finish white, the second gap must then also be used an odd number of times.",
      "Continue along the row. Each of the five gaps must be used at least once, so fewer than five moves cannot work.",
      "Use each gap once. The two end tiles change once each and every inside tile changes twice. Five moves realise the target."
    ],
    contrast: "Even colour totals tell you the target might be reachable. A shortest route needs both a lower bound and an example.",
    figure: "",
    recall: [["COUNT-04",4],["SOLID-01",9],["DIG-04",14],["SEQ-03",19],["DATA-02",24]]
  }],
  [176, {
    title: "The broken fourth step",
    id: "SEQ-03",
    prompt: "Starting at ground level, a climber can move up one step or three steps at a time. Landing on step 4 is forbidden, but jumping over it is allowed. How many different routes land on step 8?",
    value: 4,
    hint: "For each landing, which two steps could the last move have come from?",
    steps: [
      "There is one empty route at step 0. The counts at steps 1, 2 and 3 are 1, 1 and 2.",
      "Give step 4 a count of zero. At steps 5, 6 and 7, adding the counts one and three steps earlier gives 1, 3 and 3.",
      "Step 8 can be reached from step 7 or step 5. Their counts give 3 + 1 = 4 routes."
    ],
    contrast: "A forbidden landing has zero routes, even though a jump can cross it.",
    figure: "",
    recall: [["COUNT-05",20],["DIG-05",25],["DIV-04",30],["RATE-01",35],["FRAC-04",40]]
  }],
  [184, {
    title: "Meeting at the beacon again",
    id: "RATE-04",
    prompt: "Two boats leave a beacon together and travel in the same direction around a 150 m circuit. Their steady speeds are 4 m/s and 6 m/s. How many laps has the faster boat completed when it first catches the slower one?",
    value: 3,
    hint: "How far must the faster boat gain before the two are level again?",
    steps: [
      "The faster boat gains 6 − 4 = 2 metres each second.",
      "A full lap of gain is 150 m, taking 75 seconds. Before that, its gain is strictly between zero and one lap.",
      "The faster boat travels 6 × 75 = 450 m, or 3 laps. The slower boat has completed 2 laps."
    ],
    contrast: "The distance gained is one lap. The distance travelled by the faster boat is greater.",
    figure: "",
    recall: [["COUNT-06",28],["DIG-01",33],["SPATIAL-03",38],["GEO-01",43],["LOGIC-01",48]]
  }],
  [192, {
    title: "Exactly one bell",
    id: "COUNT-04",
    prompt: "A red bell rings at every positive multiple of 4 minutes and a blue bell at every positive multiple of 6 minutes. From minute 1 to minute 80 inclusive, at how many times does exactly one bell ring?",
    value: 21,
    hint: "Sort the times into red only, blue only and both.",
    steps: [
      "Red rings 20 times and blue 13 times. Both ring at multiples of 12, of which there are 6.",
      "The red-only count is 20 − 6 = 14 and the blue-only count is 13 − 6 = 7.",
      "Together these give 21 times when exactly one bell rings."
    ],
    contrast: "A shared ringing time was counted in both lists and belongs to neither final group.",
    figure: "",
    recall: [["RATE-02",36],["FRAC-02",41],["ALG-01",46],["DATA-03",51],["SEQ-01",4]]
  }],
  [208, {
    title: "Splitting the sail",
    id: "GEO-02",
    prompt: "A triangular sail has area 63 square metres. A point on its base divides the base lengths in the ratio 2 to 7. A seam joins that point to the opposite corner. By how many square metres do the two pieces differ?",
    value: 35,
    hint: "Draw the height from the shared corner to the base line.",
    steps: [
      "Both triangles have the same perpendicular height. Their areas have the same ratio as their bases, 2 to 7.",
      "Nine equal area parts share 63 square metres. One part is 7 square metres, giving pieces of 14 and 49.",
      "The difference is 49 − 14 = 35 square metres."
    ],
    contrast: "The seam length has no role in the shared-height calculation.",
    figure: "",
    recall: [["COUNT-03",0],["RATE-03",5],["DIV-02",10],["SPATIAL-02",15],["FRAC-01",20]]
  }],
  [212, {
    title: "A train clears a platform",
    id: "RATE-01",
    prompt: "At a constant speed, a train takes 8 seconds to pass a post and 23 seconds to pass a 135 m platform. Both times begin when the front first reaches the object and end when the rear clears it. How long is the train in metres?",
    value: 72,
    hint: "Compare the two distances travelled by the front of the train.",
    steps: [
      "Passing the post requires one train length of travel. Passing the platform requires one train length plus 135 m.",
      "The extra 135 m takes 23 − 8 = 15 seconds, so the train travels 9 metres each second.",
      "In the 8 seconds needed to clear the post, the train travels 72 m. This is its length."
    ],
    contrast: "Measure from the front first arriving until the rear leaves in both cases.",
    figure: "",
    recall: [["ALG-02",4],["DIG-03",9],["DIV-01",14],["FRAC-03",19],["SEQ-02",24]]
  }],
  [225, {
    title: "Only one drawer label is true",
    id: "LOGIC-01",
    prompt: "A key is in one of five drawers numbered 1 to 5. Three clues say “below 4”, “an odd number” and “drawer 5”. Exactly one clue is true. Which drawer contains the key?",
    value: 2,
    hint: "Try each drawer and count how many clues it satisfies.",
    steps: [
      "Drawers 1 and 3 each make the first two clues true.",
      "Drawer 4 makes none true. Drawer 5 makes both the odd-number clue and the drawer-5 clue true.",
      "Drawer 2 makes only “below 4” true. It is the unique answer."
    ],
    contrast: "Two true clues disqualify a drawer just as surely as zero true clues.",
    figure: "",
    recall: [["RATE-04",18],["ALG-03",22],["GEO-03",28],["SOLID-02",33],["DATA-01",38]]
  }],
  [236, {
    title: "A square that packs in both trays",
    id: "DIV-01",
    prompt: "A positive number of counters can fill rows of 18 with none left, or rows of 20 with none left. The counters can also form a filled square. What is the smallest possible number of counters?",
    value: 900,
    hint: "First find the least common multiple, then examine its prime exponents.",
    steps: [
      "The least common multiple of 18 and 20 is 180 = 2² × 3² × 5.",
      "A square needs an even exponent for each prime. Another factor of 5 gives 2² × 3² × 5².",
      "The smallest square multiple is therefore 900 = 30². It has 50 rows of 18 or 45 rows of 20."
    ],
    contrast: "Meeting both divisibility conditions is only the first requirement.",
    figure: "",
    recall: [["DIG-02",28],["ALG-05",33],["GEO-05",38],["SEQ-04",43],["COUNT-01",48]]
  }],
  [240, {
    title: "One bell and two rope holders",
    id: "COUNT-02",
    prompt: "Five students include Ali. One student rings a bell and two others hold identical ends of a rope. How many teams with assigned jobs include Ali? Swapping the rope holders counts as the same assignment.",
    value: 18,
    hint: "Separate the cases according to Ali’s job.",
    steps: [
      "If Ali rings the bell, choose two rope holders from the four other students in six ways.",
      "If Ali holds the rope, choose one of four others to ring the bell, then one of the remaining three to share the rope. That gives 12 ways.",
      "The two cases cannot overlap. Altogether there are 6 + 12 = 18 assignments."
    ],
    contrast: "The bell is a named role. The two positions on the rope are interchangeable.",
    figure: "",
    recall: [["DIV-03",32],["LOGIC-02",37],["GEO-02",42],["SOLID-03",47],["SPATIAL-01",0]]
  }],
  [256, {
    title: "A printer short of ones",
    id: "DIG-03",
    prompt: "Page numbers run from 1 to 150. On how many pages does the digit 1 occur at least twice?",
    value: 15,
    hint: "Separate the page numbers below 100 from those beginning with a 1.",
    steps: [
      "Below 100 only page 11 works. Between 100 and 150 the hundreds digit already supplies one 1.",
      "Pages 110 through 119 all work. Outside that block, the numbers with a units digit of 1 are 101, 121, 131 and 141.",
      "The total is 1 + 10 + 4 = 15 pages."
    ],
    contrast: "Page 111 qualifies once. The question counts pages rather than occurrences of a digit.",
    figure: "",
    recall: [["DIV-05",48],["LOGIC-03",1],["COUNT-02",6],["GEO-04",12],["SPATIAL-04",17]]
  }],
  [264, {
    title: "A right angle after two",
    id: "GEO-03",
    prompt: "The hands of a clock point to 2 o’clock exactly. How many minutes pass before the smaller angle between the hands first equals 90 degrees? Give an exact answer.",
    value: "300/11",
    hint: "At the start, the minute hand is 60 degrees behind the hour hand.",
    steps: [
      "Each minute the minute hand turns 6 degrees and the hour hand turns half a degree. The minute hand gains 11/2 degrees per minute.",
      "Their initial 60-degree gap shrinks to zero before the minute hand moves 90 degrees ahead. The required gain is 150 degrees.",
      "Time is 150 ÷ (11/2) = 300/11 minutes. The smaller angle stayed below 90 degrees on the way to the first meeting."
    ],
    contrast: "The hour hand moves during the calculation, including after the hands meet.",
    figure: "",
    recall: [["LOGIC-04",4],["COUNT-04",9],["ALG-04",14],["SOLID-01",19],["DIG-04",25]]
  }],
  [272, {
    title: "The taller die",
    id: "DATA-01",
    prompt: "A red die and a blue die are fair six-sided dice rolled independently. You learn that the red die shows more than the blue die. Given that clue, what is the probability that the red die shows exactly one more?",
    value: "1/3",
    hint: "List pairs in order, keeping only those with red larger.",
    steps: [
      "If blue shows 1 through 5, the allowed numbers of red results are 5, 4, 3, 2 and 1. This leaves 15 equally likely pairs.",
      "Exactly five pairs differ by one, from red 2 with blue 1 through red 6 with blue 5.",
      "The conditional probability is 5/15 = 1/3."
    ],
    contrast: "The clue removes all ties and every outcome with the blue die larger.",
    figure: "",
    recall: [["COUNT-05",12],["SEQ-03",18],["DIG-05",22],["DIV-04",27],["FRAC-04",32]]
  }],
  [288, {
    title: "The mean of the joined groups",
    id: "FRAC-04",
    prompt: "Six runners in one group average 12 laps. A second group averages 20 laps. When all the runners are counted together the mean is 17 laps. How many runners are in the second group?",
    value: 10,
    hint: "Compare each group’s total against 17 laps per runner.",
    steps: [
      "The first group contributes 6 × (17 − 12) = 30 laps less than the combined target for its six runners.",
      "Each runner in the second group contributes an average surplus of 20 − 17 = 3 laps.",
      "Ten such runners balance the 30-lap deficit. Check that (72 + 200) ÷ 16 = 17."
    ],
    contrast: "The balance uses group totals even when individual runners made different numbers of laps.",
    figure: "",
    recall: [["COUNT-06",29],["DATA-02",33],["RATE-01",38],["SPATIAL-03",44],["GEO-01",48]]
  }],
  [292, {
    title: "A board with two missing corners",
    id: "SPATIAL-03",
    prompt: "The top-left and bottom-right cells are removed from a 5 by 5 board. A domino covers two edge-neighbouring cells. What is the greatest possible number of dominoes that can be placed without overlap?",
    value: 11,
    hint: "You need a ceiling on the count and a placement that reaches it.",
    steps: [
      "Only 23 cells remain, so twelve dominoes would need too much space. Eleven is an upper bound.",
      "Lay two horizontal dominoes in each of the top and bottom rows. Fill rows 2 and 3 with five vertical dominoes. Put two horizontal dominoes in row 4.",
      "These 2 + 2 + 5 + 2 = 11 dominoes fit, with one cell unused. This proves the maximum."
    ],
    contrast: "An area bound alone does not prove that the proposed maximum fits.",
    figure: "",
    recall: [["LOGIC-01",33],["DIG-01",37],["RATE-02",42],["ALG-01",47],["DATA-03",0]]
  }],
  [304, {
    title: "Passing tokens backwards",
    id: "ALG-05",
    prompt: "Mira and Jay have 84 tokens altogether. Mira gives Jay 6 tokens. Jay now has twice as many tokens as Mira. How many did Mira have before the transfer?",
    value: 34,
    hint: "Recover their two final amounts before undoing the move.",
    steps: [
      "The transfer keeps the total at 84. The final amounts are one part for Mira and two for Jay.",
      "Each part is 84 ÷ 3 = 28. Mira ends with 28 and Jay with 56.",
      "Mira had 28 + 6 = 34 before giving six away. Jay started with 50 and finishes with 56."
    ],
    contrast: "Apply the ratio to the moment it describes.",
    figure: "",
    recall: [["FRAC-02",44],["SEQ-01",49],["DIV-02",3],["SPATIAL-02",8],["COUNT-03",14]]
  }],
  [316, {
    title: "An alternating family tree",
    id: "SEQ-02",
    prompt: "A branching tree starts with one node in row 1. Every node in row 1 has three children, every node in row 2 has two, and the same three-then-two rule repeats. How many nodes are in the first five rows altogether?",
    value: 64,
    hint: "Write the number of nodes in each row before adding.",
    steps: [
      "The first row has 1 node. Its three children make row 2, then each has two children to give 6 nodes in row 3.",
      "Row 4 has 6 × 3 = 18 nodes. Row 5 has 18 × 2 = 36.",
      "Counting all five rows gives 1 + 3 + 6 + 18 + 36 = 64."
    ],
    contrast: "Each new row multiplies the last row. The total requires an addition as well.",
    figure: "",
    recall: [["FRAC-01",4],["RATE-03",9],["DIG-03",14],["DIV-01",19],["ALG-02",24]]
  }],
  [320, {
    title: "Weaving two delivery lists",
    id: "LOGIC-02",
    prompt: "Five parcels P, Q, R, S and T are delivered once each. Both P and Q must come before R. S must come before T. How many delivery orders are allowed?",
    value: 20,
    hint: "First choose which three of the five positions belong to P, Q and R.",
    steps: [
      "The three positions for P, Q and R can be chosen in 10 ways.",
      "In those positions R must be last, leaving two possible orders for P and Q. The remaining two positions must contain S then T.",
      "Each choice gives a different valid order, for 10 × 2 = 20 orders."
    ],
    contrast: "The relative order of S and T is fixed even when the two parcels are separated.",
    figure: "",
    recall: [["FRAC-03",8],["SEQ-02",13],["GEO-03",18],["SOLID-02",23],["DATA-01",28]]
  }],
  [328, {
    title: "The turning compass",
    id: "SEQ-04",
    prompt: "A compass pointer begins facing north. On move 1 it turns one quarter-turn clockwise, on move 2 it turns two quarter-turns clockwise, and so on. Which direction does it face after move 18?",
    value: "west",
    hint: "Four quarter-turns restore the original direction. Count all the turns made.",
    steps: [
      "The total count is 1 + 2 + … + 18. Pairing the ends gives 9 × 19 = 171 quarter-turns.",
      "Remove 42 full revolutions, or 168 quarter-turns. Three quarter-turns remain.",
      "Starting at north, those three clockwise turns lead to east, south and then west."
    ],
    contrast: "The turn on move 18 is only the last contribution to the pointer’s final direction.",
    figure: "",
    recall: [["RATE-04",16],["ALG-03",21],["COUNT-01",27],["DIG-02",33],["GEO-05",36]]
  }],
  [337, {
    title: "Climbing digits with an even finish",
    id: "COUNT-06",
    prompt: "A three-digit number uses digits from 0 to 6. Its digits strictly increase from left to right and its final digit is even. How many such numbers exist?",
    value: 13,
    hint: "Fix the final digit and choose the two smaller digits that precede it.",
    steps: [
      "Zero cannot occur. It would have to be first, and the result would no longer be a three-digit number.",
      "Ending in 2 leaves too few smaller positive digits. Ending in 4 gives three pairs from 1, 2 and 3. Ending in 6 gives ten pairs from 1 through 5.",
      "Each pair has just one increasing order. The count is 0 + 3 + 10 = 13."
    ],
    contrast: "An increasing arrangement fixes the order automatically once its digits are chosen.",
    figure: "",
    recall: [["ALG-05",25],["SEQ-04",30],["GEO-02",35],["LOGIC-02",40],["SOLID-03",45]]
  }],
  [340, {
    title: "The stop inside the average",
    id: "RATE-03",
    prompt: "A rider travels half a route at 9 km/h and half at 18 km/h. A ten-minute stop is included in the total journey time. The overall average is 10 km/h. How long is the route in kilometres?",
    value: 10,
    hint: "Find the moving time for an 18 km route first, with 9 km in each half.",
    steps: [
      "The first 9 km would take 1 hour and the next 9 km half an hour. The moving average is therefore 18 ÷ 1.5 = 12 km/h for any route with these equal-distance halves.",
      "For each kilometre, moving takes 5 minutes. At the stated overall average, each kilometre allows 6 minutes of elapsed time.",
      "That extra minute per kilometre accounts for the ten-minute stop, so the route is 10 km."
    ],
    contrast: "A stop adds time to the denominator while adding no distance to the numerator.",
    figure: "",
    recall: [["SPATIAL-01",29],["DIV-03",33],["COUNT-02",38],["LOGIC-03",43],["GEO-04",48]]
  }],
  [344, {
    title: "A tunnel through the cube",
    id: "SOLID-03",
    prompt: "A solid 3 cm cube is built from unit cubes. Remove the central column of three unit cubes from the top face straight through to the bottom. What is the total surface area left, including the tunnel walls, in square centimetres?",
    value: 64,
    hint: "Track the surfaces that disappear and the new ones exposed inside.",
    steps: [
      "The original outside has area 6 × 3² = 54 square centimetres.",
      "The openings remove one square centimetre from the top and one from the bottom. The tunnel exposes four walls, each 3 cm by 1 cm.",
      "The new total area is 54 − 2 + 12 = 64 square centimetres."
    ],
    contrast: "The two ends of the tunnel are openings. Only its four side walls add new area.",
    figure: "",
    recall: [["SPATIAL-04",32],["DIV-05",37],["COUNT-04",42],["LOGIC-04",47],["ALG-04",2]]
  }],
  [352, {
    title: "Two square readouts",
    id: "LOGIC-04",
    prompt: "Find the smallest positive whole number n for which both 2n + 1 and 3n + 1 are perfect squares.",
    value: 40,
    hint: "The first expression is always odd. Test the odd squares in increasing order.",
    steps: [
      "The first odd squares above 1 are 9, 25, 49 and 81. Solving 2n + 1 for each gives n = 4, 12, 24 and 40.",
      "The second readout is then 13, 37, 73 or 121. The first three lie strictly between consecutive squares, while 121 = 11².",
      "At n = 40 the first readout is 81 = 9², so both tests pass. The ordered search rules out every smaller positive n."
    ],
    contrast: "Testing a candidate proves existence. Testing every earlier possible first square proves minimality.",
    figure: "",
    recall: [["COUNT-05",40],["SOLID-01",46],["DIG-04",51],["DIV-04",3],["FRAC-04",8]]
  }],
  [356, {
    title: "Mirror numbers divisible by nine",
    id: "DIG-04",
    prompt: "How many four-digit palindromes are divisible by 9?",
    value: 10,
    hint: "Write the digits as ABBA. Which values of A + B are possible?",
    steps: [
      "The digit sum is 2(A + B). For divisibility by 9, A + B must itself be a multiple of 9.",
      "A is from 1 to 9 and B is from 0 to 9. A + B = 9 gives one B for each of nine choices of A. A + B = 18 gives only A = B = 9.",
      "There are 9 + 1 = 10 such palindromes. The number 9999 belongs to the second case."
    ],
    contrast: "The middle digit may be zero, and the two chosen digits are allowed to coincide.",
    figure: "",
    recall: [["COUNT-06",46],["SEQ-03",0],["DATA-02",2],["RATE-01",7],["SPATIAL-03",13]]
  }],
  [363, {
    title: "Changing the fence line",
    id: "GEO-01",
    prompt: "A rectangular yard is 12 m by 8 m. A notch 3 m wide and 4 m deep is cut into the middle of a 12 m side. Outside a different side, a 2 m square pen is attached along one whole side of the pen. What is the new outside perimeter in metres?",
    value: 52,
    hint: "Trace what replaces the straight edge at each alteration.",
    steps: [
      "The original perimeter is 2 × (12 + 8) = 40 m. At the notch, the 3 m edge is replaced by 4 + 3 + 4 m, a gain of 8 m.",
      "The pen replaces 2 m of the fence line with three sides of 2 m each, a gain of 4 m.",
      "The new outside perimeter is 40 + 8 + 4 = 52 m."
    ],
    contrast: "The far edge of the notch replaces an edge of the same length. Its depth controls the increase.",
    figure: "",
    recall: [["DIG-05",51],["RATE-02",4],["LOGIC-01",10],["ALG-01",14],["DATA-03",19]]
  }],
  [369, {
    title: "Where did the points go?",
    id: "ALG-03",
    prompt: "Six teams play each other once. A win gives the winner 3 points and the loser 0. In a draw each team gets 1 point. The final table contains 38 points altogether. How many matches were draws?",
    value: 7,
    hint: "Find the total points the tournament would have awarded if every match had a winner.",
    steps: [
      "There are 6 × 5 ÷ 2 = 15 matches. With winners in every match, the table would contain 45 points.",
      "A draw awards only two points in total, one fewer than a decisive match.",
      "The shortfall is 45 − 38 = 7 points, so seven matches were draws. Eight wins and seven draws give 24 + 14 = 38 points."
    ],
    contrast: "Count points awarded per match before trying to reconstruct any individual team’s results.",
    figure: "",
    recall: [["GEO-01",5],["DIG-01",10],["DIV-02",17],["SPATIAL-02",22],["COUNT-03",27]]
  }],
  [372, {
    title: "The shortest inspection circuit",
    id: "SPATIAL-04",
    prompt: "Four paths form a rectangle ABCD in that order. AB and CD are each 3 km, BC and DA are each 4 km, and a fifth path AC is 5 km. An inspector starts at B, walks every path at least once and returns to B. What is the shortest total distance in kilometres?",
    value: 24,
    hint: "Which junctions have an odd number of incident paths before any path is repeated?",
    steps: [
      "The five paths total 19 km. A and C are the two odd junctions. On a closed walk arrivals match departures, so the repeated paths must connect A to C.",
      "The shortest A-to-C connection is the 5 km diagonal. Travelling via B or D costs 7 km. At least 19 + 5 = 24 km is needed.",
      "The walk B–A–C–D–A–C–B uses each side once and the diagonal twice. Its length is 24 km, so the bound is attainable."
    ],
    contrast: "Showing which junctions must be paired gives a lower bound. A full closed walk shows that you can attain it.",
    figure: "",
    recall: [["FRAC-02",8],["SEQ-01",13],["DIG-03",19],["DIV-01",24],["RATE-03",28]]
  }]
]);
