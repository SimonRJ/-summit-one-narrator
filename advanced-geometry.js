/* Original, read-only advanced enrichment: geometry, spatial and data families. */
export const advancedGeometry = [
 [
  "GEO-01",
  "Shared edges reveal a perimeter formula",
  "When unit squares join, each shared edge removes two exposed sides.",
  "A row has n unit squares. Find its perimeter using n.",
  [
   "Separate squares have a total of 4n sides.",
   "There are n−1 joins, each hiding two sides.",
   "The outer perimeter is 4n−2(n−1)=2n+2."
  ],
  "Boundary arguments lead to polyomino perimeter bounds and geometric invariants.",
  "Why can two shapes of equal area have different perimeters?",
  "Their counts of shared internal edges may differ."
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
  "Dissection and complement methods also work with triangles, circles and overlapping regions.",
  "Why was 'disjoint' important?",
  "If the removed pieces overlapped, subtracting their full areas would double-count the overlap."
 ],
 [
  "GEO-03",
  "Triangulation proves polygon angle sums",
  "One simple drawing explains a whole family of polygon rules.",
  "Find the interior-angle sum of a pentagon.",
  [
   "Draw diagonals from one vertex to divide the convex pentagon into 3 triangles.",
   "Every triangle has interior-angle sum 180 degrees.",
   "Thus the pentagon's sum is 3 × 180 = 540 degrees. For n sides the sum is (n−2) × 180."
  ],
  "Triangulation is useful in geometry proof and polygon dissections.",
  "What is each angle of a regular pentagon?",
  "All five angles are equal: 540/5 = 108 degrees."
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
  "This is a glimpse of group theory, which studies symmetry and transformation rules.",
  "How many rotations preserve a non-square rectangle?",
  "Only 0 and 180 degrees."
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
  "Inequality arguments are a common step from computation to proof in olympiad geometry.",
  "Why is finding a 5 by 5 rectangle not a complete proof by itself?",
  "It gives one area but does not rule out a different rectangle with greater area."
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
  "3D layers lead to volume formulae and counting cubes with several visibility conditions.",
  "How many are hidden in a 6 by 6 by 6 solid?",
  "The inner dimensions are 4 by 4 by 4, so 4³=64."
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
  "This technique extends to all surface configurations and other solids.",
  "How many small cubes have no paint?",
  "The interior is 3 by 3 by 3: there are 27."
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
  "Dimensional scaling leads to optimisation and geometric similarity.",
  "Why does volume grow faster than surface area?",
  "Volume contains three length factors; surface area contains only two."
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
  "This combines paths, combinations and inclusion–exclusion in Junior/Intermediate competition problems.",
  "Why multiply 3 by 6?",
  "Each route through the point has a unique beginning and ending segment."
 ],
 [
  "SPATIAL-02",
  "A rectangle is a choice of four boundary lines",
  "Grid counting becomes simple when each rectangle is represented uniquely.",
  "How many rectangles are in a grid with 3 rows and 4 columns?",
  [
   "There are 4 horizontal grid lines and 5 vertical lines.",
   "Choose two horizontals: C(4,2)=6. Choose two verticals: C(5,2)=10.",
   "Every pair of choices determines one rectangle: 6 × 10 = 60."
  ],
  "Selecting boundaries extends to 3D cuboids and more challenging grid restrictions.",
  "How many unit squares are in that grid?",
  "3 × 4 = 12."
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
  "This is an introduction to proof by construction and mathematical induction.",
  "Why does the method handle any location for the missing square?",
  "Only the quadrant containing it matters; the central piece fills one square in each other quadrant."
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
  "Euler trails are a first look at graph theory and network problem solving.",
  "Can you trace all five edges and return to your starting corner?",
  "No. A closed edge-once route needs every vertex to have even degree."
 ],
 [
  "DATA-01",
  "The opposite event may be easier to count",
  "'At least one' often becomes simple by counting 'none' first.",
  "Two fair dice are rolled. What is the probability of at least one six?",
  [
   "The probability a die is not six is 5/6.",
   "The probability neither die is six is (5/6)²=25/36.",
   "The opposite event, at least one six, has probability 1−25/36=11/36."
  ],
  "Complements are useful in multi-step probability, especially with restrictions.",
  "Why is 2 × 1/6 not correct?",
  "That addition counts the double-six outcome twice."
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
  "This is an early step towards weighted averages and unknown distributions.",
  "Why cannot you assume the missing score is 25?",
  "The mean is a property of all scores together, not one score."
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
  "Data interpretation in competitions often involves percentages, rates and misleading scales.",
  "What should you look at before comparing two bars?",
  "The vertical-axis origin, tick spacing, units and labels."
 ]
];
