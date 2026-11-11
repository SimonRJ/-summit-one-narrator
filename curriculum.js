// Explicit instruction and small checks. These are teaching exercises, not unseen exam items.
export const METHOD_VERSION = "2026-11-11";
const rows = [
['DIG-01','T11.1','Split a number into place-value parts before calculating. Use a nearby round number, then compensate for the change.','A rounded answer is a check, not an exact answer.'],
['DIG-02','T11.1','Choose the leading digit first: zero cannot start a multi-digit number. Then count the choices remaining at each position.','Treating zero like every other leading digit adds invalid numbers.'],
['DIG-03','T11.3','Decide whether you are counting numbers or occurrences of a digit. Count each place separately so a repeated digit can contribute twice.','A number such as 11 contains two copies of the digit 1.'],
['DIG-04','T11.1','Write a repeated-digit number using place value. In a palindrome, choosing the first half determines the reflected half.','A leading zero changes the number of digits.'],
['DIG-05','T11.2','Work column by column and name the carry. A carry is a constraint linking adjacent columns, not an extra mystery digit.','Check that different letters really have different digits.'],
['DIV-01','T04.2','Build the prime factorisation. A divisor chooses how many copies of each prime to keep, from zero up to the available exponent.','The exponents are increased by one before multiplying the choice counts.'],
['DIV-02','T03.2','A common multiple is a shared landing point on two number tracks. The least common multiple uses each prime to the larger required exponent.','The first event and the repeat interval need not be the same.'],
['DIV-03','T03.1','Write a number as divisor × whole-number quotient + remainder. The remainder is at least zero and smaller than the divisor.','A remainder equal to the divisor is not finished.'],
['DIV-04','T02.1','Track just odd or even. Adding an odd number switches parity; adding an even number preserves it. An invariant can rule out a target.','An impossibility argument must cover every allowed move.'],
['DIV-05','T03.1','List a cycle until the original state returns. Reduce the position modulo the cycle length; remainder zero means the final position in the cycle.','Do not confuse position zero with the first item.'],
['FRAC-01','T09.1','Name the whole at every step. A fraction of what remains multiplies the remaining fraction, not the original whole.','Two successive fractions generally cannot be subtracted from the original total.'],
['FRAC-02','T16.1','A ratio describes equal-sized parts. Find the value of one part from a known total or difference, then rebuild the requested quantity.','A ratio of 2:3 means 2 out of 5 parts in the first group.'],
['FRAC-03','T09.1','Percent means out of one hundred. Convert each change into a multiplier and keep track of which amount is the base.','A 20% rise followed by a 20% fall does not undo itself.'],
['FRAC-04','T09.1','Use a common unit for the whole. For a fraction of a group, multiply the group size by that fraction before combining groups.','Averaging fractions without weighting by group size can mislead.'],
['RATE-01','T16.2','Convert to one common unit before multiplying. For repeated events, count the intervals, not just the event labels.','There are one fewer gaps than fence posts in a straight row.'],
['RATE-02','T16.2','Turn each completion time into work done per minute. Add the rates when workers act together, then invert the combined rate.','Never average the two completion times.'],
['RATE-03','T16.2','Keep distance, speed and time in compatible units. Distance equals speed multiplied by time; sketch the journey if speeds change.','Minutes must be converted when speed is per hour.'],
['RATE-04','T16.2','Watch how quickly the gap changes. Approaching speeds add; chasing speeds subtract when both travel in the same direction.','Add speeds only when the separation is closing at their sum.'],
['ALG-01','T09.3','Give the unknown a meaning. Translate the relationship, undo equal operations on both sides, and substitute into the original story.','An equation is useful only if its quantities keep their meaning.'],
['ALG-02','T02.E','Use the total and the difference together. Remove the extra amount to create two equal parts, then halve.','Halving the total alone ignores the difference.'],
['ALG-03','T02.E','Compare two collections that share an unknown quantity. Subtract the collections so the shared part cancels.','Subtract every term, not just the one you want to remove.'],
['ALG-04','T02.2','Start with the result and undo the last operation first. Reverse both the operation and the order; finally check forwards.','Reverse the order as well as the operation.'],
['ALG-05','T02.3','Separate the total from the winning margin. A transfer changes a gap by twice the amount moved because one side loses what the other gains.','Changing one quantity and transferring between two quantities affect the gap differently.'],
['SEQ-01','T10.1','For a constant step, the nth term is the first term plus n−1 steps. Pair the first and last terms to find a sum.','There are n−1 jumps from the first term to the nth.'],
['SEQ-02','T10.1','Repeated multiplication gives geometric growth. For a doubling sum, compare the sum with twice itself so the middle terms cancel.','A doubling pattern must be justified by the situation.'],
['SEQ-03','T10.1','Classify the final step. If the final move is one or two steps, every route comes from exactly one of two smaller route sets.','A recurrence needs starting values.'],
['SEQ-04','T10.2','Write down enough state to determine the next move. Once exactly the same state returns, all future states repeat.','A repeated output alone need not mean the full state repeats.'],
['COUNT-01','T05.2','Choose an organising rule, such as the smallest number first. Make a list in that order and explain why nothing can sit between adjacent cases.','An unordered pair should not be counted in both orders.'],
['COUNT-02','T05.1','Multiply choices for successive decisions. If order does not matter, count how many ordered descriptions describe the same outcome.','Divide only after proving the same overcount applies to every outcome.'],
['COUNT-03','T05.2','Let the restriction organise the count. For neighbours, a block or the gaps between objects often exposes the valid choices.','A block can still have different internal orders.'],
['COUNT-04','T05.2','Count the whole set and remove unwanted cases, or add sets and subtract their overlap once. Draw labelled regions if needed.','Subtracting the overlap twice loses valid outcomes.'],
['COUNT-05','T06.1','Count incidences in two ways. For handshakes, each person counts their own partners, so every handshake appears twice.','The two counting methods must count the same collection.'],
['COUNT-06','T05.2','Split outcomes into disjoint cases using a feature every outcome has. Solve each case, then add.','Cases must cover all possibilities without overlapping.'],
['LOGIC-01','T17.2','Try one truth assignment and follow its consequences. A liar makes a false statement, so negate the entire claim carefully.','The opposite of “all” is “at least one is not”.'],
['LOGIC-02','T17.3','Combine all constraints. Each condition removes candidates; check the remaining candidate against every original condition.','A candidate satisfying one clue may fail another.'],
['LOGIC-03','T06.1','Compare totals that count the same entries. In a rectangular grid, adding row totals and adding column totals must agree.','An attractive pattern is not a rule unless the conditions force it.'],
['LOGIC-04','T17.1','Proving uniqueness has two jobs: construct one solution and show no other solution works. A bounded list can be a complete proof.','Finding a solution does not prove it is the only one.'],
['GEO-01','T13.2','Trace the outside boundary. When shapes join, their shared edge disappears from both perimeters.','Subtract each shared edge twice.'],
['GEO-02','T13.1','Split a shape into known regions or subtract it from a simple outer shape. A triangle is half a parallelogram with the same base and perpendicular height.','A sloping side is not automatically the perpendicular height.'],
['GEO-03','T12.1','Start with reliable facts: a straight angle is 180°, a full turn 360°, and triangle angles sum to 180°. State the reason for every step.','Do not measure an angle from an unscaled diagram.'],
['GEO-04','T15.1','Name a transformation precisely: reflection, rotation or translation. A symmetry maps the whole shape onto itself, including any labels or colours.','A shape’s outline can have more symmetries than its colouring.'],
['GEO-05','T07.3','To prove an optimum, establish a bound and build an example attaining it. With a fixed rectangle perimeter, moving unequal sides closer increases area.','A good-looking example alone does not prove a maximum.'],
['SOLID-01','T13.3','Count one layer at a time, including cubes hidden behind others. A complete cuboid has length × width × height unit cubes.','A picture usually shows only some of the cubes.'],
['SOLID-02','T13.3','Classify cubes by their position: corners, edges, face interiors and the hidden interior. Each class has a different number of painted faces.','For an n-cube edge, only n−2 cubes lie away from its corners.'],
['SOLID-03','T13.3','Distinguish volume from surface area. Volume counts unit cubes; surface area counts exposed unit-square faces. Match opposite faces in a net.','Six face areas must be counted, including faces hidden in a view.'],
['SPATIAL-01','T14.1','At each point, add the route counts from the allowed predecessor points. Start the initial point with one route: the empty route.','Adding counts is valid only when the last-step cases do not overlap.'],
['SPATIAL-02','T12.3','Label coordinates and count intervals between grid lines. A rectangle is determined by choosing two vertical and two horizontal boundary lines.','A grid with n cells across has n+1 boundary lines.'],
['SPATIAL-03','T15.3','Use a colouring or area invariant to test a tiling. If each domino covers one black and one white square, the board must have equal counts.','Equal colour counts are necessary but do not alone guarantee a tiling.'],
['SPATIAL-04','T14.2','Record legal connections as a network. A route using every edge once has either zero or two odd-degree vertices in a connected graph.','A route through every vertex is a different problem from a route along every edge.'],
['DATA-01','T08.1','List equally likely elementary outcomes. Probability is favourable outcomes divided by all outcomes only when the elementary outcomes are equally likely.','Different-looking totals may have different numbers of ways to occur.'],
['DATA-02','T16.3','Recover the total by multiplying mean by count. Combine totals and counts before finding a new mean.','A mean of two means needs equal group sizes.'],
['DATA-03','T01.2','Read the axis labels, scale and units before using a graph or table. Describe what each entry measures and what comparison is requested.','A graph need not begin at zero or use intervals of one.']
];
export const methods=Object.fromEntries(rows.map(([id,video,idea,trap])=>[id,{id,video,idea,trap}]));
export function skillFor(session,taxonomy){return taxonomy.categories.flatMap(c=>c.subskills).find(s=>s.name===session.focus)?.id||null;}
const factorial=n=>n<2?1:n*factorial(n-1);
const choose=(n,k)=>factorial(n)/(factorial(k)*factorial(n-k));
export function exercise(id,seed=0){
 const n=2+Math.abs(seed)%7, a=n+3, b=n+5;
 let prompt, value, reason;
 switch(id){
 case 'DIG-01':prompt=`Find ${n*100+97} + 38 exactly.`;value=n*100+135;reason=`Add 40, then subtract 2: ${n*100+97} + 40 − 2 = ${value}.`;break;
 case 'DIG-02':prompt=`How many three-digit numbers use three different digits from 0, 1, 2, …, ${n}?`;value=n*n*(n-1);reason=`There are ${n} nonzero leading choices, ${n} remaining middle choices and ${n-1} final choices: ${value}.`;break;
 case 'DIG-03':prompt=`How many times is the digit 1 written in the numbers 1 to ${n*10+9}?`;value=n+11;reason=`The units column contributes ${n+1} copies (1, 11, …, ${n*10+1}); 10–19 contribute ten in the tens column. Total ${value}.`;break;
 case 'DIG-04':prompt=`A three-digit palindrome has first digit ${n}. How many different such numbers are possible?`;value=10;reason=`The last digit must also be ${n}. The middle digit can be any of 0–9: ten choices.`;break;
 case 'DIG-05':prompt=`In the addition ${n}A + ${n}A = ${20*n+10}, A is one digit. Find A.`;value=5;reason=`Twice (${10*n}+A) is ${20*n+10}. Thus 2A=10 and A=5; the units column carries 1.`;break;
 case 'DIV-01':prompt=`How many positive divisors does 2^${n} × 3² have?`;value=(n+1)*3;reason=`Choose the exponent of 2 in ${n+1} ways (0 to ${n}) and of 3 in 3 ways (0 to 2). Multiply to get ${value}.`;break;
 case 'DIV-02':prompt=`Two lights flash together now. One flashes every ${n*4} seconds, the other every ${n*6}. In how many seconds do they next flash together?`;value=12*n;reason=`The least common multiple of 4 and 6 is 12. Scaling both intervals by ${n} gives ${value} seconds.`;break;
 case 'DIV-03':prompt=`What is the remainder when ${7*n+5} is divided by 7?`;value=5;reason=`${7*n+5} = 7 × ${n} + 5, and 0 ≤ 5 < 7.`;break;
 case 'DIV-04':prompt=`Start with an even number. Add 3 exactly ${n} times. Is the result odd or even?`;value=n%2?'odd':'even';reason=`Each addition of 3 switches parity. After ${n} switches, the result is ${value}.`;break;
 case 'DIV-05':prompt=`What is the last digit of 2^${n+7}?`;value=[6,2,4,8][(n+7)%4];reason=`The last digits cycle 2,4,8,6. Exponent ${n+7} leaves remainder ${(n+7)%4} on division by 4, giving ${value}.`;break;
 case 'FRAC-01':prompt=`A box has ${12*n} counters. Half are removed, then one third of those remaining are removed. How many remain?`;value=4*n;reason=`Half leaves ${6*n}; keeping two thirds of that leaves ${4*n}.`;break;
 case 'FRAC-02':prompt=`Red : blue counters = 2 : 3. There are ${5*n} counters. How many are blue?`;value=3*n;reason=`Five equal parts total ${5*n}, so a part is ${n}. Blue has three parts: ${value}.`;break;
 case 'FRAC-03':prompt=`A $${100*n} price rises 20%, then falls 20%. What is the final price in dollars?`;value=96*n;reason=`Multiply by 1.2 then 0.8. The final multiplier is 0.96, so the price is $${value}.`;break;
 case 'FRAC-04':prompt=`One third of ${6*n} children and one half of ${4*n} adults wear hats. How many people wear hats altogether?`;value=4*n;reason=`Children contribute ${2*n}, adults ${2*n}; together ${value}.`;break;
 case 'RATE-01':prompt=`A bell rings ${n+2} times, with 5 seconds between rings. How many seconds pass from the first ring to the last?`;value=5*(n+1);reason=`${n+2} rings have ${n+1} gaps. Multiply the gaps by 5 seconds.`;break;
 case 'RATE-02':prompt=`One tap fills a tank in ${3*n} minutes, another in ${6*n}. Working together, how many minutes do they take?`;value=2*n;reason=`In ${6*n} minutes the first fills two tanks and the second one. Three tanks per ${6*n} minutes means one tank per ${2*n} minutes.`;break;
 case 'RATE-03':prompt=`A cyclist travels at ${6*n} km/h for 20 minutes. How far does the cyclist travel in kilometres?`;value=2*n;reason=`20 minutes is one third of an hour. Distance = ${6*n} × 1/3 = ${value} km.`;break;
 case 'RATE-04':prompt=`Two walkers are ${6*n} km apart. They walk towards each other at 4 km/h and 2 km/h. After how many hours do they meet?`;value=n;reason=`The gap closes at 6 km/h. Time = ${6*n} ÷ 6 = ${n} hours.`;break;
 case 'ALG-01':prompt=`Three identical notebooks and a $4 pen cost $${3*n+4}. What is the price of one notebook in dollars?`;value=n;reason=`Remove the pen: ${3*n+4}−4=${3*n}. Divide by three notebooks to get $${n}.`;break;
 case 'ALG-02':prompt=`Two piles total ${6*n+4} counters. The larger has ${2*n} more than the smaller. How many are in the smaller pile?`;value=2*n+2;reason=`Remove the extra ${2*n}, then halve: (${6*n+4}−${2*n})÷2=${value}.`;break;
 case 'ALG-03':prompt=`Two pens and a book cost $${2*n+7}. Five identical pens and the same book cost $${5*n+7}. What does a pen cost in dollars?`;value=n;reason=`The second purchase adds three pens for $${3*n}. Divide by 3 to get $${n}.`;break;
 case 'ALG-04':prompt=`A number is multiplied by 4, then 3 is added. The result is ${4*n+3}. Find the starting number.`;value=n;reason=`Undo the last move first: (${4*n+3}−3)÷4=${n}. Check: 4×${n}+3=${4*n+3}.`;break;
 case 'ALG-05':prompt=`A has ${4*n} counters and B has ${2*n}. How many counters must A give B to make the piles equal?`;value=n;reason=`The gap is ${2*n}. Each transferred counter reduces it by 2, so transfer ${n}. Both then have ${3*n}.`;break;
 case 'SEQ-01':prompt=`A sequence starts at 5 and increases by 3 each time. Find term ${n+4}.`;value=5+3*(n+3);reason=`There are ${n+3} steps after the first term. 5+3×${n+3}=${value}.`;break;
 case 'SEQ-02':prompt=`Find the sum 1 + 2 + 4 + … + ${2**n}.`;value=2**(n+1)-1;reason=`Twice the sum minus the original sum leaves ${2**(n+1)}−1=${value}.`;break;
 case 'SEQ-03':{const f=[1,1];for(let i=2;i<=n+2;i++)f[i]=f[i-1]+f[i-2];prompt=`A staircase has ${n+2} steps. You may climb one or two steps each move. How many different sequences of moves reach the top?`;value=f[n+2];reason=`Let f(0)=f(1)=1. Split by the last move: f(k)=f(k−1)+f(k−2). Counts to step ${n+2}: ${f.join(', ')}.`;break;}
 case 'SEQ-04':prompt=`A pointer starts facing north. Each move turns it 90° clockwise. Which direction does it face after ${n+7} moves?`;value=['north','east','south','west'][(n+7)%4];reason=`The four-state cycle is north, east, south, west. ${(n+7)%4} extra turns after full cycles gives ${value}.`;break;
 case 'COUNT-01':prompt=`How many unordered pairs of different positive whole numbers add to ${2*n+1}?`;value=n;reason=`The smaller number can be 1 to ${n}. Each determines its partner. The next choice would repeat a pair backwards.`;break;
 case 'COUNT-02':prompt=`A team of two is chosen from ${n+3} children. How many different teams are possible?`;value=choose(n+3,2);reason=`There are ${n+3}×${n+2} ordered choices. Each team is counted twice, so divide by 2: ${value}.`;break;
 case 'COUNT-03':prompt=`${n+2} different books are arranged in a row. Two particular books must be neighbours. How many arrangements are possible?`;value=2*factorial(n+1);reason=`Treat the pair as one block. Arrange ${n+1} objects in ${(n+1)}! ways, then choose either order inside the block. Total ${value}.`;break;
 case 'COUNT-04':prompt=`In a class, ${3*n} play chess, ${2*n} play music, and ${n} do both. How many do at least one of these activities?`;value=4*n;reason=`Add the group sizes and subtract the overlap once: ${3*n}+${2*n}−${n}=${value}.`;break;
 case 'COUNT-05':prompt=`At a meeting of ${n+3} people, each pair shakes hands once. How many handshakes occur?`;value=choose(n+3,2);reason=`Each of ${n+3} people counts ${n+2} partners. Each handshake was counted twice, so the total is ${value}.`;break;
 case 'COUNT-06':prompt=`How many two-digit numbers using only digits 1 to ${n}, with repetition allowed, have at least one digit equal to 1?`;value=2*n-1;reason=`Case 1: tens digit 1 gives ${n} numbers. Case 2: tens not 1 and units 1 gives ${n-1}. Disjoint total ${value}.`;break;
 case 'LOGIC-01':prompt=`${2*n+1} people stand in a line. Each except the last says “The next person is a liar.” Everyone always lies or always tells the truth. What is the largest possible number of liars?`;value=n+1;reason=`Adjacent people have opposite types. Alternating liar, truthful, …, liar gives ${n+1} liars; the other possible pattern has ${n}.`;break;
 case 'LOGIC-02':prompt=`A whole number is greater than ${6*n}, less than ${6*n+6}, divisible by 3 and odd. What is it?`;value=6*n+3;reason=`The only multiple of 3 strictly between the bounds is ${value}. It is odd, so every clue is satisfied.`;break;
 case 'LOGIC-03':prompt=`A 2-by-2 grid has row totals ${n+8} and ${n+12}. Its first column totals ${n+5}. What is the second column total?`;value=n+15;reason=`Both rows sum to ${2*n+20}. Subtract the first column total ${n+5} to obtain ${value}.`;break;
 case 'LOGIC-04':prompt=`Two positive whole numbers have sum ${2*n+1}. Their difference is 1. What is the larger number?`;value=n+1;reason=`They must be x and x+1. Then 2x+1=${2*n+1}, forcing x=${n}. The pair ${n}, ${n+1} works and the equation leaves no other pair.`;break;
 case 'GEO-01':prompt=`Two squares of side ${n} cm join along one full side. What is the perimeter of the resulting rectangle in cm?`;value=6*n;reason=`Separate perimeters total ${8*n}. The shared ${n}-cm edge was counted twice, so subtract ${2*n}, leaving ${value}.`;break;
 case 'GEO-02':prompt=`A rectangle is ${2*n} cm by ${n+3} cm. A triangle with the same base and height is removed. What area remains, in square cm?`;value=n*(n+3);reason=`The triangle is half the rectangle. The remaining area is (${2*n}×${n+3})÷2=${value}.`;break;
 case 'GEO-03':prompt=`A triangle has angles ${10*n}° and ${n+25}°. What is its third angle in degrees?`;value=155-11*n;reason=`Triangle angles total 180°. Subtract the two given angles: 180−${10*n}−${n+25}=${value}.`;break;
 case 'GEO-04':prompt=`A regular ${n+2}-sided polygon has no labels or colours. How many rotations of less than 360°, including 0°, map it onto itself?`;value=n+2;reason=`Each rotation taking a vertex to a vertex works. There are ${n+2} such turns, including the zero turn.`;break;
 case 'GEO-05':prompt=`A rectangle has whole-number side lengths and perimeter ${4*n} cm. What is its largest possible area in square cm?`;value=n*n;reason=`The sides sum to ${2*n}. Write them n−d and n+d: area n²−d² ≤ n². The ${n}-by-${n} square attains ${value}.`;break;
 case 'SOLID-01':prompt=`A solid block is ${n} cubes wide, ${n+1} deep and 3 high. How many unit cubes does it contain?`;value=3*n*(n+1);reason=`Each layer has ${n*(n+1)} cubes and there are 3 layers, including hidden cubes: ${value}.`;break;
 case 'SOLID-02':prompt=`An ${n+2}-by-${n+2}-by-${n+2} cube is painted on all six outer faces, then separated into unit cubes. How many have no paint?`;value=n**3;reason=`Remove one outer layer on each side. The unpainted core is ${n}×${n}×${n}=${value}.`;break;
 case 'SOLID-03':prompt=`A closed cuboid has side lengths 2 cm, 3 cm and ${n} cm. What is its surface area in square cm?`;value=12+10*n;reason=`Three pairs of equal faces give 2(2×3 + 2×${n} + 3×${n})=${value}.`;break;
 case 'SPATIAL-01':prompt=`To reach a point, a robot must move ${n} steps right and 2 steps up, in any order. How many shortest routes are there?`;value=choose(n+2,2);reason=`Choose the two up-step positions among ${n+2} moves. That is (${n+2}×${n+1})÷2=${value}.`;break;
 case 'SPATIAL-02':prompt=`A grid has ${n} vertical lines and 3 horizontal lines. How many rectangles have sides on these lines?`;value=choose(n,2)*3;reason=`Choose two vertical boundaries in ${choose(n,2)} ways and two horizontal boundaries in 3 ways. Multiply: ${value}.`;break;
 case 'SPATIAL-03':prompt=`A checkerboard has ${2*n} rows and ${2*n} columns. Remove two opposite corner squares. Can the rest be tiled with 1-by-2 dominoes? Answer yes or no.`;value='no';reason=`Opposite corners on an even-sided checkerboard have the same colour. Removing them leaves unequal colour counts; every domino covers one of each colour.`;break;
 case 'SPATIAL-04':prompt=`A connected network has ${n+1} edges meeting only at one central hub; the outer endpoints are all different. Can one continuous trail use every edge exactly once without repeating an edge? Answer yes or no.`;value='no';reason=`There are ${n+1} degree-one outer vertices, already more than two odd-degree vertices. Such a trail is impossible.`;break;
 case 'DATA-01':prompt=`A bag has ${n} red and 3 blue counters. One counter is chosen uniformly. What is the probability of red? Give a fraction.`;value=`${n}/${n+3}`;reason=`${n} of the ${n+3} equally likely counters are red, so the probability is ${value}.`;break;
 case 'DATA-02':prompt=`The mean of ${n} numbers is 8. One more number, 14, is added. What is the new mean? Give an exact fraction if needed.`;value=`${8*n+14}/${n+1}`;reason=`The old total is ${8*n}. Add 14 and divide by the new count ${n+1}: ${value}.`;break;
 case 'DATA-03':prompt=`A table records Monday: ${3*n} books, Tuesday: ${4*n} books, Wednesday: ${2*n} books. How many more books were recorded on Tuesday than Wednesday?`;value=2*n;reason=`Read the two relevant entries, then subtract ${4*n}−${2*n}=${value} books.`;break;
 default:throw new Error('Missing exercise for '+id);
 }
 return {id,seed,prompt,value,reason};
}
export function numericValue(value){
 const s=String(value??'').trim().replace(/−/g,'-');
 if(/^[+-]?(?:\d+(?:\.\d+)?|\.\d+)$/.test(s))return Number(s);
 const m=s.match(/^([+-]?\d+)\s*\/\s*(\d+)$/);return m&&Number(m[2])!==0?Number(m[1])/Number(m[2]):null;
}
export function checkAnswer(expected,response){
 const a=numericValue(expected),b=numericValue(response);
 return a!==null&&b!==null?Math.abs(a-b)<1e-10:String(expected).trim().toLowerCase()===String(response).trim().toLowerCase();
}
export function evidenceFor(records,id){
 return records.flatMap(r=>Object.values(r.evidence||{}).filter(e=>e.skill_id===id&&e.kind==='retrieval').map(e=>({...e,session:r.session_number}))).sort((a,b)=>a.session-b.session);
}
export function recallState(records,id){
 const ev=evidenceFor(records,id),last=ev.at(-1),wins=ev.filter(e=>e.correct&&e.independent);
 const retained=wins.some(a=>wins.some(b=>b.session-a.session>=4&&b.seed!==a.seed));
 return {last,retained:retained&&last?.correct===true,wins:wins.length,due:last?last.session+(last.correct?last.independent?7:3:2):null};
}
export function dueSkills(records,slot,currentId){
 const taught=[...new Set(records.flatMap(r=>r.summary?.skill_id?[r.summary.skill_id]:[]))];
 return taught.filter(id=>methods[id]&&id!==currentId).map(id=>({id,...recallState(records,id)})).filter(x=>x.due===null||x.due<=slot).sort((a,b)=>(a.due??0)-(b.due??0)).slice(0,2).map(x=>x.id);
}
