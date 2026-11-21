/* Original, read-only advanced enrichment: geometry, spatial and data families. */
export const advancedGeometry = [
 [
  "GEO-01",
  "Shared edges reveal a perimeter formula",
  "When unit squares join, each shared edge removes two exposed sides.",
  "A straight row contains n unit squares joined edge to edge. What is the perimeter in terms of n?",
  [
   "Separate squares have a total of 4n sides.",
   "There are n−1 joins, each hiding two sides.",
   "The outer perimeter is 4n−2(n−1)=2n+2."
  ],
  "Two shapes made from the same squares can expose different numbers of edges.",
  "Six unit squares make a row. They are rearranged into a 2 by 3 rectangle. By how much does the perimeter decrease?",
  "The row is 1 by 6 with perimeter 14. The rectangle has perimeter 10. Its two extra shared edges hide four exposed sides, so the decrease is 4 units."
 ],
 [
  "GEO-02",
  "Subtract the pieces you do not want",
  "A complex shaded region can be simpler as a large shape minus a few non-overlapping pieces.",
  "A 10 by 10 square has four disjoint 2 by 3 rectangles removed from its corners. What area remains?",
  [
   "The square has area 10 × 10 = 100.",
   "Each missing rectangle has area 2 × 3 = 6.",
   "Remaining area = 100 − 4 × 6 = 76 square units."
  ],
  "Trace the shared part before subtracting several pieces from one shape.",
  "A sheet is 8 cm wide and 6 cm high. Remove the top strip 2 cm tall and the left strip 2 cm wide, counting their shared corner only once. What area remains?",
  "The strips cover 16 and 12 square centimetres with an overlap of 4. The area left is 48 − (16 + 12 − 4) = 24 square centimetres. The remaining 6 by 4 rectangle confirms it."
 ],
 [
  "GEO-03",
  "Triangulation proves polygon angle sums",
  "One simple drawing explains a whole family of polygon rules.",
  "What is the sum of the interior angles of a convex pentagon?",
  [
   "Draw diagonals from one vertex to divide the convex pentagon into 3 triangles.",
   "Every triangle has interior-angle sum 180 degrees.",
   "Thus the pentagon's sum is 3 × 180 = 540 degrees. For n sides the sum is (n−2) × 180."
  ],
  "When individual interior angles are known, the turn at each corner can be easier to use.",
  "Every interior angle of a regular polygon is 150°. How many sides does it have?",
  "Walking around the edge turns you through 180° − 150° = 30° at each corner. One circuit makes 360°, so there are 360 ÷ 30 = 12 corners and 12 sides."
 ],
 [
  "GEO-04",
  "Square symmetries form a system",
  "Rotations and reflections are not merely pictures: they can be combined like operations.",
  "How many different symmetries does a square have?",
  [
   "It has 4 rotational symmetries: 0, 90, 180 and 270 degrees.",
   "It has 4 reflection symmetries: two through midpoints and two through opposite vertices.",
   "Altogether there are 8 transformations that preserve the square."
  ],
  "Test every transformation against the marks as well as the outline.",
  "Two opposite corners of a square are marked with identical dots. How many of its original eight symmetries preserve the dots?",
  "Doing nothing and rotating by 180° both work. Reflection in either diagonal also preserves the marked pair. The two other rotations and the two midline reflections move the dots to unmarked corners. Four symmetries remain."
 ],
 [
  "GEO-05",
  "Prove a maximum, not just an example",
  "An optimisation solution needs both a construction and proof that nothing better exists.",
  "A rectangle has perimeter 20 units. What is its largest possible area?",
  [
   "If its sides are a and b, then a+b=10.",
   "Because (a−b)²≥0, we have (a+b)²≥4ab.",
   "So 100≥4ab and area ab≤25. Equality occurs for the 5 by 5 square."
  ],
  "For a fixed sum, balance the two factors as closely as the allowed numbers permit.",
  "A rectangle with whole-number side lengths has perimeter 26 cm. What is its greatest possible area?",
  "The side lengths sum to 13. Moving one unit from a longer side to a shorter side increases the area whenever they differ by at least two. The closest pair is 6 and 7, giving 42 square centimetres."
 ],
 [
  "SOLID-01",
  "Hidden cubes grow in three dimensions",
  "Count what is inside a solid by removing the visible boundary layers.",
  "How many cubes in a solid 4 by 4 by 4 unit-cube structure touch none of its outside faces?",
  [
   "A hidden cube cannot lie on any of the six outside faces.",
   "Removing one layer on every side leaves a 2 by 2 by 2 inner cube.",
   "The hidden count is 2³=8."
  ],
  "Find the interior dimensions directly when boundary layers overlap.",
  "A solid block is 5 by 6 by 7 unit cubes. How many little cubes touch none of its outside faces?",
  "The interior is two units shorter in every direction, giving 3 × 4 × 5 = 60 cubes. The six boundary layers meet at edges, so subtracting six entire faces separately would count some cubes twice."
 ],
 [
  "SOLID-02",
  "Classify painted cubes by their positions",
  "The corners, edge interiors and face interiors behave differently after a cube is cut.",
  "A 5 by 5 by 5 cube is painted outside and cut into unit cubes. How many have exactly two painted faces?",
  [
   "Only edge-interior cubes have exactly two painted faces.",
   "Each of the 12 edges has 5−2=3 non-corner cubes.",
   "So the number is 12 × 3 = 36."
  ],
  "Sort cubes by whether they lie inside a face, along an edge or at a corner.",
  "A 4 by 4 by 4 cube is painted on the outside and cut into unit cubes. How many little cubes have paint on exactly one face?",
  "On each large face, remove its edge rows and columns. A 2 by 2 patch of four remains. The six patches are disjoint, giving 24 little cubes."
 ],
 [
  "SOLID-03",
  "Area and volume have different scaling laws",
  "Doubling an object's size does not merely double everything.",
  "A cube with edge length 3 is enlarged to edge length 6. Compare its area and volume.",
  [
   "Original surface area 6 × 3² = 54; new surface area 6 × 6² = 216.",
   "Area has multiplied by 216/54 = 4.",
   "Original volume 3³=27; new volume 6³=216. Volume multiplied by 8."
  ],
  "Cutting preserves volume while exposing faces that used to be inside.",
  "A cube is cut into eight equal smaller cubes. All eight are separated. How does their total surface area compare with the original surface area?",
  "A child cube has half the edge length and one quarter the surface area. Eight times one quarter is two. The separated pieces have twice the original surface area."
 ],
 [
  "SPATIAL-01",
  "A blocked route invites complement counting",
  "Count all shortest paths, then remove those that pass through the forbidden point.",
  "How many right/up shortest routes from (0,0) to (4,3) avoid the point (2,1)?",
  [
   "Choose positions for three up moves among seven moves: C(7,3)=35 total routes.",
   "To reach (2,1), choose one up position among three: C(3,1)=3; from there to (4,3), choose two up positions among four: C(4,2)=6.",
   "Routes through the point: 3 × 6 = 18, so routes avoiding it: 35−18=17."
  ],
  "Apply a fixed first move before counting the remaining paths.",
  "On the grid in the example, start with a rightward step. How many shortest routes to (4,3) now avoid (2,1)?",
  "From (1,0) there are 20 routes to the finish, with three up moves in six steps. Two prefixes reach (2,1), then six endings reach the finish. Remove 2 × 6 forbidden routes from 20 to leave 8."
 ],
 [
  "SPATIAL-02",
  "A rectangle is a choice of four boundary lines",
  "Grid counting becomes simple when each rectangle is represented uniquely.",
  "How many rectangles have all four sides along the lines of a grid with 3 rows and 4 columns?",
  [
   "There are 4 horizontal grid lines and 5 vertical lines.",
   "Choose two horizontals: C(4,2)=6. Choose two verticals: C(5,2)=10.",
   "Every pair of choices determines one rectangle: 6 × 10 = 60."
  ],
  "Count squares by side length when a grid question requires rectangles with unequal sides.",
  "How many rectangles in the 3-row, 4-column grid are not squares?",
  "Of the 60 rectangles, 12 are unit squares, 6 are 2 by 2 squares and 2 are 3 by 3 squares. Removing all 20 squares leaves 40 rectangles with unequal side lengths."
 ],
 [
  "SPATIAL-03",
  "One missing square can enable a recursive tiling",
  "A constructive proof can solve every arrangement of a certain type, not just one board.",
  "Can any 4 by 4 square board with one square removed be tiled using L-shaped three-square pieces?",
  [
   "Split the 4 by 4 board into four 2 by 2 quadrants.",
   "The missing square lies in one quadrant. Cover one central square in each of the other three quadrants with one L-piece.",
   "Each quadrant now has exactly one square missing, so its remaining three squares form another L. Together the five pieces cover the board."
  ],
  "To extend a construction, make each smaller region look like the puzzle you already solved.",
  "An 8 by 8 board loses one square. Can the same L-shaped pieces always cover the rest, and how many are needed?",
  "Split the board into four 4 by 4 quadrants. Place a central L in the three quadrants that did not lose a square. Each quadrant now has a single unavailable cell and needs five pieces by the smaller construction. The total is 1 + 4 × 5 = 21."
 ],
 [
  "SPATIAL-04",
  "Odd-degree vertices decide whether a trail exists",
  "A route that uses every edge exactly once is controlled by a parity condition.",
  "A square has its four edges plus one diagonal. Can you trace all five edges exactly once without lifting your pencil?",
  [
   "The diagonal endpoints each touch three edges, making them odd-degree vertices.",
   "The other two corners each touch two edges, making them even-degree vertices.",
   "A connected network with exactly two odd vertices has an edge-once trail starting at one odd vertex and ending at the other. So yes."
  ],
  "State whether a crossing is a junction before counting the degrees.",
  "Add the second diagonal to the square. The crossing is a bridge, so you cannot change direction there. Can every edge now be traced exactly once in one continuous trail?",
  "All four corners now have three incident edges. Each odd corner needs to be an endpoint, but a single trail has only two ends. Such a trail is impossible."
 ],
 [
  "DATA-01",
  "The opposite event may be easier to count",
  "'At least one' often becomes simple by counting 'none' first.",
  "Two fair six-sided dice are rolled independently. What is the probability of at least one six?",
  [
   "The probability a die is not six is 5/6.",
   "The dice are independent, so the probability that neither shows six is (5/6)² = 25/36.",
   "The opposite event, at least one six, has probability 1−25/36=11/36."
  ],
  "When given a clue about a result, rebuild the set of possible outcomes before taking a fraction.",
  "You learn that at least one of the two dice showed a six. What is the probability that both showed six?",
  "Eleven equally likely ordered outcomes contain a six. Only (6,6) has two sixes. Among the eleven outcomes left by the clue, the probability is 1/11."
 ],
 [
  "DATA-02",
  "An average contains a hidden total",
  "Work backwards from the mean to find a missing value.",
  "Four scores average 25. Three scores are 10, 20 and 30. What is the fourth?",
  [
   "The total must be 4 × 25 = 100.",
   "Known scores total 10 + 20 + 30 = 60.",
   "The fourth score is 100−60=40."
  ],
  "A correction changes the total first. Divide that change among all observations to see its effect on the mean.",
  "Four recorded scores have a mean of 25. One score was entered as 31 instead of 19. What is the corrected mean?",
  "The recorded total is 100. Replacing 31 with 19 lowers it by 12, so the true total is 88. Dividing by four gives a corrected mean of 22."
 ],
 [
  "DATA-03",
  "Axes can distort the impression of a change",
  "The scale of a graph matters more than how dramatic the bars look.",
  "A bar chart shows values 95 and 100, but the vertical axis begins at 90. Has the quantity almost doubled?",
  [
   "Read the actual values rather than just the visible bar heights.",
   "The change is 100−95=5.",
   "Relative to 95, the change is 5/95, about 5.3%, not a doubling."
  ],
  "Compare differences in the original units before interpreting the ratio of two drawn lengths.",
  "A chart shows values of 70 and 80. It is cropped so the second drawn bar is three times the height of the first. At what value does the visible axis begin?",
  "The difference of 10 units equals two short-bar heights. The short bar must therefore rise 5 units, from 65 to 70. From 65 to 80 is 15 units, which is three times 5."
 ]
];
