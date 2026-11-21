"""Topic film chapter menus and transcripts share the measured narration scene starts."""
from html import escape

# Keys are one-based narration scene numbers, also used in the sound alignment reports.
CHAPTERS = {
    "T01.1": {
        1: "Label packets, counters and loose pieces", 3: "Open Mia’s four packets",
        6: "Add ribbon lengths in centimetres", 7: "Count every nine on pages 95–105",
        9: "Find the pencils that still work",
    },
    "T01.2": {
        1: "Choose a line, table or sketch", 3: "Place posts along a straight fence",
        5: "Join the ends of the fence", 6: "Count Sam once in the queue",
        7: "Compare the price per pencil", 8: "Trace the outside edges of two mats",
        9: "Plant trees at both ends of a path",
    },
    "T01.3": {
        1: "Predict the units and size of an answer", 3: "Estimate seats for 130 students",
        4: "Fill buses in groups of forty", 6: "Show why three buses fall short",
        7: "Count only the completely full buses", 8: "Pack 100 eggs into boxes of twelve",
    },
    "T01.E": {
        1: "Locate the two ends of the ribbon", 3: "Count centimetre gaps from 2 to 9",
        4: "Subtract the starting mark", 5: "Slide both ends back to zero and seven",
        6: "Time a film from 7:15 to 9:05", 8: "Measure a recording across noon",
    },
    "T02.1": {
        1: "Find a quantity one move preserves", 4: "Transfer counters between two piles",
        10: "Add two counters to each pile", 13: "Prove the changes cancel",
        17: "Test two targets from four and nine", 20: "Write an equation for one move",
    },
    "T02.2": {
        1: "Undo the last operation first", 3: "Recover the machine’s input from 23",
        6: "Check the reversed steps forwards", 8: "Rebuild the pile from eight counters",
        12: "Check that each pile contains whole counters", 16: "Trace the route back from 17",
    },
    "T02.3": {
        1: "Swap addition and doubling", 3: "Predict which rule gives more",
        4: "Make two copies of the whole bar", 5: "Pair the matching parts",
        6: "Compare the rules with a negative multiplier", 7: "Decide which steps can swap",
        8: "Compare tripling before and after subtraction",
    },
    "T02.E": {
        1: "Try both rules with one starting number", 2: "Make four copies of the sum",
        4: "Cancel the matching tiles", 5: "Test the gap at zero and at ten",
        6: "Draw the two add-and-scale rules",
    },
    "T03.1": {
        1: "Group seventeen counters in fives", 3: "Mark the four-bead cycle",
        4: "Locate bead 50", 5: "Place bead 48 at remainder zero",
        6: "Subtract two numbers with the same remainder", 7: "Filter a list by two remainders",
        8: "Move 100 days beyond Tuesday",
    },
    "T03.2": {
        1: "Compare the four- and six-second lights", 3: "Start both lights at zero",
        4: "Find the gap between shared flashes", 5: "Give the second light a two-second delay",
        6: "Use parity to rule out a meeting", 7: "Find the next shared bus departure",
    },
    "T03.3": {
        1: "Fit four counters into three boxes", 3: "Delay a matching pair of socks",
        5: "Sort four numbers into remainder boxes", 6: "Pair the numbers that sum to eleven",
        7: "Force two birthdays into one month",
    },
    "T03.E": {
        1: "Find a multiple-of-three difference", 2: "Give each number a remainder box",
        4: "Subtract numbers from the same box", 5: "Test four numbers and then three",
        6: "Find the guarantee for divisor ten",
    },
    "T04.1": {
        1: "Split 60 into 6 and 10", 2: "Start again with 4 and 15",
        3: "Choose primes to test against 91", 4: "Find the factor that divides 91",
        5: "Decide when the search for a factor of 97 ends",
        6: "Share the prime factors of 66 among three numbers", 7: "Build a factor tree for 84",
    },
    "T04.2": {
        1: "Pair the positive factors of twelve", 3: "Choose the twos and threes in a factor",
        4: "Find 1 and 12 in the choices grid", 5: "Extend the count from 72 to 360",
        6: "Find the unpaired factor of 36", 7: "Count the factors of 200",
    },
    "T04.3": {
        1: "Line up the prime copies in 12 and 18", 3: "Compare a shared factor with a shared multiple",
        4: "Take the smaller count in each prime column", 5: "Cover both rows with the larger counts",
        6: "Check why the two products agree", 7: "Give the lone three in 48 a partner",
        8: "Find the HCF and LCM of 20 and 30",
    },
    "T04.E": {
        1: "Turn 90 into a square", 2: "Find the two primes without partners",
        3: "Supply one more two and one more five", 4: "Split 900 into matching groups",
        5: "Show that every valid multiplier is a multiple of ten", 6: "Find the least multiplier for 60",
    },
    "T05.1": {
        1: "Swap two runners on a podium and on a team", 2: "Check what a swap changes",
        3: "Compare both selections from Ava, Ben and Cal", 4: "Assign first place and second place",
        5: "Merge two orders that pick the same team", 6: "Count the six orders of each group of three",
        7: "Assign captain, scorer and timekeeper", 8: "Choose captains or equipment carriers",
    },
    "T05.2": {
        1: "Choose cases that cover every outcome once", 2: "Find the choice that changes the branch size",
        3: "Build an even number from five available digits", 4: "Separate a zero ending from a 2 or 4",
        5: "Count the legal hundreds and tens digits", 6: "Combine the two last-digit counts",
        7: "Remove the forbidden switch setting", 8: "Count two-digit numbers with distinct digits",
    },
    "T05.3": {
        1: "Match each result to the choices that made it", 2: "Check for missing or repeated rows",
        3: "Seat five students with two kept apart", 4: "Arrange three students to create four gaps",
        5: "Fill two different gaps in order", 6: "Read the choices back from a finished row",
        7: "Subtract rows with the two students together", 8: "Keep two named books apart on a shelf",
    },
    "T05.E": {
        1: "Choose a sandwich and a fruit", 2: "Sort the lunches by sandwich",
        3: "List the fruits allowed with cheese", 4: "Add the lunches with a bean sandwich",
        5: "Remove cheese with plum from the full menu", 6: "Exclude the red-and-orange outfits",
    },
    "T06.1": {
        1: "Trace a handshake to its two people", 2: "Connect the reports to the objects counted",
        3: "Arrange handshakes among six people", 4: "Add the six reports of five handshakes",
        5: "Pair the two reports of each handshake", 6: "Test seven people making three handshakes each",
        7: "Count a cube’s edges from its faces", 8: "Count the games in an eight-team tournament",
    },
    "T06.2": {
        1: "Weigh three boxes two at a time", 2: "Find their combined weight first",
        3: "Record the three pair weights", 4: "Count each box twice in the total of 36 kg",
        5: "Recover each box from the other pair", 6: "Check all three weights on the scales",
        7: "Distinguish triangle corners from edge middles", 8: "Recover three numbers from their pair sums",
    },
    "T06.3": {
        1: "Form groups from twelve tokens", 2: "Distinguish a ceiling from an achievable maximum",
        3: "Plan partnerships for five club members", 4: "Count the ten available partnerships",
        5: "Fit all ten pairs into five days", 6: "Test whether three groups of three can fit",
        7: "Schedule a six-player chess tournament",
    },
    "T06.E": {
        1: "Join four tiles into a square", 2: "Count the edges before the tiles touch",
        3: "Locate the four internal joins", 4: "Remove both edge reports at every join",
        5: "Rearrange the square into a row", 6: "Trace the boundary of a two-by-three rectangle",
    },
    "T07.1": {
        1: "Find a limit every placement must respect", 2: "Test what one arrangement proves",
        3: "Place separated counters in eight cells", 4: "Pair the eight cells from left to right",
        5: "Fill the odd-numbered cells", 6: "Handle the ninth unpaired cell",
        7: "Cover eight cells with the fewest counters", 8: "Find the largest placement in eleven cells",
    },
    "T07.2": {
        1: "Compare rectangles with the same fence", 2: "Separate a pattern from a proof",
        3: "Split twelve into two whole-number parts", 4: "Compare the six possible products",
        5: "Identify the missing square of side d", 6: "Keep the two parts different",
        7: "Compare three fours with four threes", 8: "Find the greatest area with 22 cm of fence",
    },
    "T07.3": {
        1: "Work back from equality in a bound", 2: "Use a tight bound to choose a layout",
        3: "Fill a four-by-four board under two rules", 4: "Get a limit from the four rows",
        5: "Check the columns of a full-row arrangement", 6: "Build two diagonal blocks of four",
        7: "Inspect every row and column", 8: "Place three counters on a three-by-three board",
    },
    "T07.E": {
        1: "Pack seven red and four blue counters", 2: "Estimate the trays from eleven places",
        3: "Limit red counters to two per tray", 4: "Build a legal four-tray packing",
        5: "Compare the two capacity bounds", 6: "Pack nine reds with three blues",
    },
    "T08.1": {
        1: "Decide which outcomes have equal chances", 2: "Distinguish a colour from an individual counter",
        3: "Test the three proposed head counts", 4: "Distinguish the first toss from the second",
        5: "Identify both routes to exactly one head", 6: "Compare dice totals using ordered pairs",
        7: "Find the chance of matching dice",
    },
    "T08.2": {
        1: "Follow a draw without replacement", 2: "Recount the bag after removing one counter",
        3: "Try drawing two reds from four counters", 4: "Set the chance of the first red",
        5: "Follow the red branch a second time", 6: "Check all four colour routes sum to one",
        7: "Combine red–blue and blue–red", 8: "Draw from three reds and one blue",
    },
    "T08.3": {
        1: "Cross out outcomes the clue rules out", 2: "Find the total after filtering the list",
        3: "Roll an even number on a fair die", 4: "Keep only the even faces",
        5: "Count faces above three in the reduced list", 6: "List the dice pairs that total eight",
        7: "Check whether the survivors are equally likely", 8: "Use the clue that a roll exceeded two",
    },
    "T08.E": {
        1: "Compare two heads with at least one head", 2: "Label the two coins and list four results",
        3: "Remove the outcome with two tails", 4: "Find two heads among the surviving results",
        5: "Change the clue to a head on the first coin", 6: "Condition on the coins showing different faces",
    },
    "T09.1": {
        1: "Find a half before and after cutting the bar", 2: "Change the whole between steps",
        3: "Name the whole for each person’s marbles", 4: "Remove a quarter of the original forty",
        5: "Take a third of the remaining thirty", 6: "Model two thirds of three quarters",
        7: "Raise and lower a price by ten percent", 8: "Track the remaining water in a tank",
    },
    "T09.2": {
        1: "Express a decimal in thousandths", 2: "Link a stopping decimal to a power of ten",
        3: "Decide whether three fortieths terminates", 4: "Turn a denominator of 40 into 1000",
        5: "Explain why one sixth keeps repeating", 6: "Reduce six fifteenths before testing",
        7: "Make a decimal into a whole number", 8: "Test the denominators 20, 12 and 75",
    },
    "T09.3": {
        1: "Undo the same move on both pans", 2: "Preserve every possible solution",
        3: "Balance the pouches and loose counters", 4: "Remove one pouch from each side",
        5: "Clear five loose counters from each pan", 6: "Substitute seven into the original balance",
        7: "Clear a half in an equation", 8: "Check zero before dividing by the unknown",
        9: "Solve the balance with three pouches",
    },
    "T09.E": {
        1: "Share 21 counters across three trays", 2: "Find the total on each tray",
        3: "Separate five counters inside the pouch", 4: "Write the tray story as an equation",
        5: "Remove all six loose counters first", 6: "Find the marbles inside each of four boxes",
    },
    "T10.1": {
        1: "Build a large count from smaller cases", 2: "Tile ten cells without listing 89 patterns",
        3: "Predict the count for five cells", 4: "Sort tilings by their last tile",
        5: "Add the length-four and length-three counts", 6: "Continue the tiling counts to ten cells",
        7: "Match the last tile to the last stair step", 8: "Count the tilings of seven cells",
    },
    "T10.2": {
        1: "Decide what a state must remember", 2: "Use a cycle to reach a distant term",
        3: "Double 3 and track the last digit", 4: "Find where the cycle begins",
        5: "Locate the 50th term after the initial 3", 6: "Remember two digits for a sum recurrence",
        7: "Track a robot’s previous direction", 8: "Triple 7 and find the 30th last digit",
    },
    "T10.3": {
        1: "Label a game from its smallest positions", 2: "Use a label to find a winning move",
        3: "Choose who starts with ten counters", 4: "Compare piles of one, two and three",
        5: "Decide when every move helps the opponent", 6: "Leave nine and complete pairs of moves",
        7: "Allow a third counter on each turn", 8: "Plan a winning first move from fourteen",
    },
    "T10.E": {
        1: "Grow a three-by-three dot square", 2: "Add a bottom row of four dots",
        3: "Count the corner only once", 4: "Check the increase from nine to sixteen",
        5: "Grow a square of side n", 6: "Find the next border for twenty rows",
    },
    "T11.1": {
        1: "Compare the value of 4 in 42 and 24", 2: "Write a two-digit number using place value",
        3: "Reverse a number to gain 27", 4: "Express both digit orders with A and B",
        5: "Factor the difference between the numbers", 6: "List and check the possible originals",
        7: "Add a number to its reverse", 8: "Use the limits on each digit",
        9: "Find numbers four times their digit sum",
    },
    "T11.2": {
        1: "Compare each place value with a multiple of 9", 2: "Use digit sums after rearranging digits",
        3: "Test 4725 for divisibility by 9", 4: "Remove groups of nine from each place",
        5: "Explain why a digit sum of 18 works", 6: "Find the remainder when 583 is divided by 9",
        7: "Rearrange 1, 2 and 6 and test for 3", 8: "Fill the missing digit between 5 and 8",
        9: "Choose the missing digit in 73□4",
    },
    "T11.3": {
        1: "Count the twos in 22", 2: "Separate a digit count into columns",
        3: "Look for sevens from 1 to 100", 4: "Count sevens in the units column",
        5: "Count sevens in the tens column", 6: "Count the numbers containing a seven",
        7: "Count the digits on pages 1 to 99", 8: "Count every three written up to 50",
    },
    "T11.E": {
        1: "Explain each carry in 58 + 67", 2: "Exchange ten units for one ten",
        3: "Exchange ten tens for one hundred", 4: "Read the new hundreds digit",
        5: "Check 125 by rounding and regrouping", 6: "Explain both carries in 76 + 89",
    },
    "T12.1": {
        1: "Link facts about a straight line and a turn", 2: "Justify an angle without measuring",
        3: "Locate the marked angle below the 65° crossing", 4: "Match corresponding angles",
        5: "Use a straight line to get the marked angle", 6: "Draw a parallel through a triangle’s vertex",
        7: "Split the angles opposite equal sides", 8: "Find the third angle from two 55° angles",
    },
    "T12.2": {
        1: "Divide a clock face into twelve gaps", 2: "Compare a view from the centre with one from the rim",
        3: "Trace the arc from twelve to four", 4: "Count four gaps across five hour marks",
        5: "View the same arc from eight o’clock", 6: "Use two equal-radius triangles to prove the angle rule",
        7: "Put one side of a triangle on a diameter", 8: "Find the smaller centre angle from two to seven",
    },
    "T12.3": {
        1: "Choose an extra line with a purpose", 2: "Recognise three useful kinds of line",
        3: "Examine a bent path between parallel lines", 4: "Draw a parallel through the bend",
        5: "Combine the 35° and 45° angles", 6: "Box in a tilted square on a grid",
        7: "Drop a height to form right angles", 8: "Find the tilted area from a two-by-one step",
    },
    "T12.E": {
        1: "Locate the exterior angle at C", 2: "Find the inside angle using 48° and 67°",
        3: "Follow the extension from B through C", 4: "Compare the exterior angle with the two far angles",
        5: "Test the shortcut with 60° and 55°", 6: "Use 35° and 80° to find the exterior angle",
    },
}


def reading_sections(lesson, starts, paragraphs):
    headings = CHAPTERS[lesson]
    if len(starts) != len(paragraphs) or max(headings) > len(starts) or starts[0] != 0:
        raise ValueError(f"{lesson}: chapter map no longer matches the recorded narration")
    buttons, transcript = [], []
    for number, (start, paragraph) in enumerate(zip(starts, paragraphs), 1):
        if number in headings:
            seconds = int(start + 0.5)
            clock = f"{seconds // 60}:{seconds % 60:02}"
            title = escape(headings[number])
            buttons.append(
                f'<button type="button" data-time="{start:.3f}">'
                f'<span class="chapter-clock">{clock}</span> {title}</button>'
            )
            transcript.append(f'<h2><span class="chapter-clock">{clock}</span> {title}</h2>')
        transcript.append(f'<p>{escape(paragraph)}</p>')
        if lesson == "T05.1" and number == 2:
            transcript.append(
                '<aside class="reading-note" aria-label="Written clarification">'
                '<strong>Why two orders?</strong> In the opening example, two distinct players can exchange places. '
                'There are two orders for that pair. For three distinct players there are 3 × 2 × 1 = 6 orders, '
                'so an unordered group of three needs a different divisor.</aside>'
            )
    return "\n".join(buttons), "\n".join(transcript)

# These written checks accompany the recorded notebook prompts.
NOTEBOOK_CHECKS = {
    "T04.1": "Split 84 into 12 × 7. Then 12 = 3 × 4 and 4 = 2 × 2. The leaves are all prime, so 84 = 2² × 3 × 7. Multiplying them gives 4 × 21 = 84.",
    "T04.2": "Since 200 = 2³ × 5², a factor uses 0, 1, 2 or 3 twos and 0, 1 or 2 fives. That gives 4 × 3 = 12 positive factors, including 1 when both counts are zero. Each pair of exponents gives a different prime factorisation.",
    "T04.3": "Write 20 = 2² × 5 and 30 = 2 × 3 × 5. Both supply one 2 and one 5, giving a highest common factor of 10. To cover both numbers, take two twos, a three and a five. The lowest common multiple is 2² × 3 × 5 = 60.",
    "T04.E": "In 60 = 2² × 3 × 5, the two twos already form a pair. Any multiplier that makes a square must supply at least one 3 and one 5, so it is a multiple of 15. The first positive choice works because 60 × 15 = 900 = 30².",
    "T05.2": "The tens digit has 9 choices, from 1 to 9. For each one, the units digit can be any of the ten digits except the tens digit, leaving 9 choices. This gives 9 × 9 = 81 numbers. As a check, remove the nine doubles, 11 through 99, from the 90 two-digit numbers.",
    "T06.1": "Each of the eight teams plays seven opponents. The 8 × 7 = 56 team appearances include both teams in every game. Pair the appearances to get 56 ÷ 2 = 28 games.",
    "T06.2": "The readings add to 17 + 20 + 23 = 60. Each number appears twice, so the three numbers add to 30. Subtract each pair sum from 30 to get the missing numbers 13, 10 and 7. Their pair sums are 7 + 10 = 17, 7 + 13 = 20 and 10 + 13 = 23.",
    "T06.E": "Six separate tiles contribute 24 unit edges. Each of the two rows has two joins, and three more joins run between the rows. These seven joins each hide two edges, leaving 24 − 2 × 7 = 10 units of perimeter. Tracing the outside gives 3 + 2 + 3 + 2 = 10.",
}
