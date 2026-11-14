"""Original spatial revisits. Diagram specifications contain only the givens."""


def problem(title, prompt, answer, clue, steps, check, diagram=None):
    return dict(title=title, prompt=prompt, answer=answer, clue=clue,
                steps=steps, check=check, diagram=diagram)


def board(*cells, description, widths=None, heights=None):
    return dict(cells=cells, description=description, widths=widths, heights=heights)


RECTANGLES = {
    (2, 'try'): problem('Squares on a pinboard',
        'A pinboard is divided into 3 rows of 4 equal squares. How many squares of all sizes have all four sides along the drawn lines?',
        20, 'Count each size separately.', [
            'There are 12 single squares. A 2-by-2 square can start in either of the first two rows and in any of the first three columns, giving 6.',
            'A 3-by-3 square can start in column A or B, giving 2 more. The total is 12 + 6 + 2 = 20.'
        ], 'A square cannot be taller than the three rows.',
        board('....', '....', '....', description='Three rows of four equal squares.')),
    (2, 'transfer'): problem('Six-square rectangles',
        'The grid has 4 rows of 5 unit squares. How many rectangles along the grid lines have area exactly 6 square units?',
        17, 'Use the area to find the possible widths and heights.', [
            'Neither side can have length 6. The only dimensions that fit are 2 wide and 3 high, or 3 wide and 2 high.',
            'There are 4 × 2 = 8 placements of the first kind and 3 × 3 = 9 of the second kind. The total is 17.'
        ], 'Each placement has exactly one top-left cell.',
        board('.....', '.....', '.....', '.....', description='Four rows of five equal squares.')),
    (3, 'try'): problem('Rectangles in a stepped floor',
        'A tiled floor has 3 rows. The top two rows have 4 tiles each. The bottom row has only its two leftmost tiles. How many rectangles of any size can be made from whole tiles in this floor?',
        39, 'Choose the consecutive rows first, then the columns they share.', [
            'Using only the top two rows gives three choices of row span: row 1, row 2, or both. Each has four available columns. There are 4 + 3 + 2 + 1 = 10 column spans for each row span.',
            'The three row spans ending in row 3 each have only two available columns. Each gives 2 + 1 = 3 column spans. The total is 3 × 10 + 3 × 3 = 39.'
        ], 'Every rectangle either reaches row 3 or stays within the top two rows.',
        board('....', '....', '..  ', description='A stepped floor. The bottom row contains only A3 and B3.')),
    (3, 'transfer'): problem('The missing grid segment',
        'A grid has 3 rows of 4 unit squares. The horizontal line segment between cells B1 and B2 is erased. How many rectangles of any size still have all four sides drawn?',
        42, 'Start with the complete grid, then count rectangles whose boundary uses the missing segment.', [
            'The complete grid has 5 choices of vertical boundary lines taken two at a time and 4 horizontal lines taken two at a time. That gives 10 × 6 = 60 rectangles.',
            'To use the erased segment, the left side can be on either of the two lines at or left of column B’s left edge. The right side can be on any of the three lines at or right of its right edge. The erased segment is on one horizontal boundary and the other can be any of the three other horizontal lines. So 2 × 3 × 3 = 18 rectangles are lost.'
        ], 'A rectangle whose inside crosses the erased segment still counts. Only its outside edges need to be drawn.',
        dict(board('....', '....', '....', description='The horizontal segment between B1 and B2 is missing.'), gap=(1, 1))),
    (4, 'try'): problem('One frame around two stamps',
        'On the 3-row, 5-column grid, stamps fill cells B2 and D2. How many rectangles made from whole cells contain both stamps?',
        16, 'A rectangle contains both stamps exactly when it contains the strip from B2 to D2.', [
            'Its first column can be A or B and its last column can be D or E.',
            'Its first row can be 1 or 2 and its last row can be 2 or 3. These four choices are independent, so there are 2 × 2 × 2 × 2 = 16 rectangles.'
        ], 'Even the smallest rectangle, the three cells B2 through D2, is included.',
        board('.....', '.X.X.', '.....', description='Stamps in cells B2 and D2.')),
    (4, 'transfer'): problem('Exactly one ink mark',
        'A 3-row, 5-column grid has ink marks in cells B1 and D3. How many rectangles made from whole cells contain exactly one ink mark?',
        40, 'Count the rectangles through each mark. Remove the ones through both from both counts.', [
            'For B1 there are 2 choices of first column, 4 of last column and 3 of last row. The first row is 1. This gives 24. For D3, the choices are 4 first columns, 2 last columns and 3 first rows, also 24.',
            'A rectangle through both must span all three rows, start at A or B and end at D or E. There are 4 such rectangles. Subtract them twice: 24 + 24 − 4 − 4 = 40.'
        ], 'A rectangle containing both marks was counted once with each mark.',
        board('.X...', '.....', '...X.', description='Ink marks in cells B1 and D3.')),
    (5, 'try'): problem('Fold along the middle line',
        'A grid of 3 rows and 4 columns is folded so column A lies on D and column B lies on C. How many rectangles made from whole cells have left and right halves that match exactly when folded along this crease?',
        12, 'A rectangle centred on the crease uses equally many columns on each side.', [
            'The column span is either B through C or A through D.',
            'The row span can be any one row, either pair of consecutive rows, or all three rows. There are 6 choices, giving 2 × 6 = 12 rectangles.'
        ], 'Folding changes the columns but keeps every row in place.',
        dict(board('....', '....', '....', description='A dashed vertical crease between columns B and C.'), crease=2)),
    (5, 'transfer'): problem('Clear of the border',
        'A 4-row, 5-column grid is printed on a card. The outermost row at the top and bottom and the outermost column at each side are shaded. How many rectangles made from whole cells use only unshaded cells?',
        18, 'The four border strips leave one smaller rectangular grid.', [
            'The unshaded part consists of rows 2 and 3 and columns B through D.',
            'Two rows give 2 + 1 = 3 row spans. Three columns give 3 + 2 + 1 = 6 column spans. The total is 3 × 6 = 18.'
        ], 'A rectangle may touch the line between shaded and unshaded cells while using only unshaded cells.',
        board('#####', '#...#', '#...#', '#####', description='The shaded cells form the outer border.')),
    (6, 'try'): problem('Squares on an uneven grid',
        'The four column widths of a grid are 1, 2, 1 and 3 cm from left to right. Its three row heights are 1, 2 and 1 cm from top to bottom. How many squares of all sizes have all four sides along the grid lines?',
        13, 'A square pairs a column span and a row span of equal length.', [
            'For side lengths 1, 2, 3 and 4 cm, the numbers of matching column spans are 2, 1, 3 and 2. The numbers of matching row spans are 2, 1, 2 and 1.',
            'Multiply within each size and add: 2 × 2 + 1 × 1 + 3 × 2 + 2 × 1 = 13.'
        ], 'The full height is 4 cm, so no longer column span can form a square.',
        board('....', '....', '....', description='Column widths 1, 2, 1 and 3 cm. Row heights 1, 2 and 1 cm.', widths=(1, 2, 1, 3), heights=(1, 2, 1))),
    (6, 'transfer'): problem('Fourteen metres of edging',
        'A 4-row, 5-column grid divides a garden into square beds of side length 1 metre. How many rectangles made from whole beds have perimeter exactly 14 metres?',
        10, 'The width and height add to 7 metres.', [
            'The dimensions that fit are 3 wide and 4 high, 4 wide and 3 high, or 5 wide and 2 high.',
            'There are 3 × 1, 2 × 2 and 1 × 3 placements respectively. The sum is 3 + 4 + 3 = 10.'
        ], 'A square has equal whole-number sides and its perimeter is a multiple of four, so none of these rectangles is a square.',
        board('.....', '.....', '.....', '.....', description='Four rows of five one-metre beds.')),
    (7, 'try'): problem('Avoid the diagonal',
        'In a 4-by-4 grid the squares A1, B2, C3 and D4 are shaded. How many rectangles made from whole cells contain no shaded square?',
        30, 'A rectangle that avoids the diagonal lies completely above it or completely below it.', [
            'Above the diagonal, if the bottom row is row 1, there are 6 column spans in B through D. If the bottom row is row 2, there are 2 possible top rows and 3 column spans in C through D. If it is row 3, there are 3 top rows and only column D.',
            'This gives 6 + 6 + 3 = 15 above the diagonal. Reflection gives 15 below it, for 30 altogether.'
        ], 'A rectangle includes every crossing of its chosen rows and columns. If the row and column numbers overlap, it includes a diagonal square.',
        board('#...', '.#..', '..#.', '...#', description='A1, B2, C3 and D4 are shaded.')),
    (7, 'transfer'): problem('Balanced checkerboard rectangles',
        'A board of 3 rows and 4 columns is coloured like a chessboard. How many rectangles made from whole cells contain equal numbers of light and dark squares?',
        36, 'A checkerboard rectangle is balanced exactly when its width or height is even.', [
            'An even side lets you pair neighbours of opposite colours. If both sides are odd, the area is odd, so the two colour counts cannot be equal.',
            'There are 10 column spans and 6 row spans, for 60 rectangles. Odd widths have 4 + 2 = 6 placements. Odd heights have 3 + 1 = 4 placements. Subtract 6 × 4 = 24 to get 36.'
        ], 'Subtracting only odd-by-odd rectangles keeps every rectangle with two even sides exactly once.',
        board('d.d.', '.d.d', 'd.d.', description='A 3-row, 4-column checkerboard with A1 dark.')),
    (8, 'try'): problem('Twice as wide as tall',
        'A grid has 3 rows and 5 columns of unit squares. How many rectangles along its lines are exactly twice as wide as they are tall?',
        16, 'List the heights for which twice the height still fits.', [
            'A 2-by-1 rectangle has 4 choices of starting column and 3 choices of row, giving 12.',
            'A 4-by-2 rectangle has 2 choices of starting column and 2 of starting row, giving 4 more. The total is 16.'
        ], 'A height of 3 would require 6 columns. A tall, narrow rectangle does not meet the stated width condition.',
        board('.....', '.....', '.....', description='Three rows of five equal squares.')),
    (8, 'transfer'): problem('Rectangles in a narrow cross',
        'A cross is made of unit squares. Its middle row has 5 squares and its middle column has 5 squares. The row and column share their centre square. How many rectangles of all sizes can be made from whole squares of the cross?',
        29, 'Any rectangle wider than one square and taller than one square would need a 2-by-2 block.', [
            'The cross has no 2-by-2 block. Every rectangle therefore lies in the middle row or the middle column.',
            'Each strip of five squares gives 5 + 4 + 3 + 2 + 1 = 15 intervals. The centre square is counted in both strips, so the total is 15 + 15 − 1 = 29.'
        ], 'Only the single centre square belongs to both strips.',
        board('  .  ', '  .  ', '.....', '  .  ', '  .  ', description='The middle row and middle column are five squares long.')),
    (9, 'try'): problem('Rebuild the square grid',
        'A square grid has exactly 60 rectangles that are two unit squares wide. The rectangles can have any height and must follow the grid lines. How many rows does the grid have?',
        5, 'For a square grid, count the possible two-column spans and the possible row spans.', [
            'A 4-by-4 grid gives 3 × (4 + 3 + 2 + 1) = 30. A 5-by-5 grid gives 4 × (5 + 4 + 3 + 2 + 1) = 60.',
            'Starting at two rows, each added row and column adds both a new two-column span and new row spans. The number strictly increases, so only five rows give 60.'
        ], 'A grid with one row and one column has no two-column spans.'),
    (9, 'transfer'): problem('Meeting only in the centre',
        'The centre square of a 3-by-3 grid is marked. How many pairs of different rectangles made from whole cells overlap in exactly that centre square? Count each pair once.',
        40, 'Temporarily call the rectangles A and B. Both must cover the centre square.', [
            'For each of the four directions from the centre, choose whether neither rectangle extends one cell, only A extends, or only B extends. Both cannot extend in the same direction, or they would share a neighbouring square.',
            'These independent choices give 3 × 3 × 3 × 3 = 81 ordered possibilities. Exclude the one in which both are the centre square. The remaining 80 count each pair twice, so the answer is 40.'
        ], 'When the rectangles extend in different directions, their shared row span and shared column span both have length one.',
        board('...', '.X.', '...', description='The centre square B2 is marked.')),
}


TILINGS = {
    (2, 'try'): problem('The most dominoes that fit',
        'Two opposite corners, A1 and D4, are removed from a 4-by-4 checkerboard. Dominoes each cover two edge-adjacent squares. What is the greatest number of dominoes that can be placed without overlaps?',
        6, 'Count the squares of the colour that is now less common.', [
            'The two missing corners are the same colour. Six squares of that colour remain. Each domino needs one, so at most six dominoes can fit.',
            'Place dominoes on B1–C1, A2–B2, C2–D2, A3–B3, C3–D3 and B4–C4. The pairs are edge-adjacent and use twelve different available cells.'
        ], 'The bound and the construction agree, so six is the maximum.',
        board(' .d.', '.d.d', 'd.d.', '.d. ', description='The checkerboard is missing the corners A1 and D4.')),
    (2, 'transfer'): problem('A square to remove',
        'One square is removed from a 5-by-5 checkerboard with dark corners. How many choices of the removed square allow the rest of the board to be covered exactly with dominoes? Each domino covers two edge-adjacent squares.',
        13, 'The removal must leave equal numbers of light and dark squares.', [
            'The original board has 13 dark squares and 12 light squares. Every domino uses one of each, so only the 13 dark squares are candidates.',
            'If the removed square is in row 1, 3 or 5, its column is A, C or E. Pair the remaining squares of that row horizontally on either side of the hole. The rows above and below come in pairs, so fill them vertically.',
            'The other dark squares are B2, D2, B4 and D4. For any of these, take the 3-by-3 block with the missing square at its centre. Its eight surrounding squares make a rim that can be paired in order. The two remaining rows across the board can be tiled vertically. The two remaining columns beside the block can be tiled horizontally.'
        ], 'Both cases give a full tiling, so all 13 dark squares work.',
        board('d.d.d', '.d.d.', 'd.d.d', '.d.d.', 'd.d.d', description='A 5-by-5 checkerboard with A1 dark.')),
    (3, 'try'): problem('Two neighbouring squares removed',
        'Squares A1 and B1 are removed from a 4-by-4 board. Can dominoes, each covering two edge-adjacent squares, cover the entire remaining board? Answer yes or no.',
        'yes', 'A tiling can be proved by building one.', [
            'The two remaining squares in row 1, C1 and D1, are neighbours. Cover them with a horizontal domino.',
            'Each of rows 2, 3 and 4 has four squares, so use two horizontal dominoes in each of these rows.'
        ], 'One domino and three pairs cover all 14 squares.',
        board('  ..', '....', '....', '....', description='The top row is missing A1 and B1.')),
    (3, 'transfer'): problem('Can long tiles cover the board?',
        'Can a 6-by-6 board be covered by nine straight tiles that each cover four consecutive squares in a row or column? Answer yes or no.',
        'no', 'Colour whole 2-by-2 blocks to get a pattern that matches the length of the tiles.', [
            'Divide the board into nine 2-by-2 blocks. Colour those blocks alternately dark and light, starting dark at the top left. There are 20 dark squares and 16 light squares.',
            'In any row or column the colours repeat in pairs. Four consecutive squares therefore include exactly two of each colour. Nine tiles would cover 18 of each, which cannot match the board.'
        ], 'The area is 36 squares. The contradiction comes from the colour balance.',
        board(*(['......'] * 6), description='A plain 6-by-6 board. The worked solution describes the colouring.')),
    (4, 'try'): problem('Switching rows and columns',
        'Nine lamps in a 3-by-3 array are all off. One move flips every lamp in a single row or a single column. After some moves, at least one lamp is on. What is the smallest possible number of lamps that are on?',
        3, 'Look at the corners of any rectangle formed by two rows and two columns.', [
            'Each move flips two of those four lamps or none. Since all begin off, every such rectangle always has an even number of lit corner lamps.',
            'If just one lamp is on, choose any rectangle having it as a corner. If exactly two are on, choose two rows and two columns to include one of them and avoid the other. In both cases a rectangle would have one lit corner, which is impossible.',
            'Flipping one row lights exactly three lamps.'
        ], 'To avoid the second lamp, use the third row if the lamps are on different rows, or the third column if they share a row.',
        board('...', '...', '...', description='Nine lamps in a square array, all initially off.')),
    (4, 'transfer'): problem('Nine T-shaped tiles',
        'A T-shaped tile has three squares in a row and one more attached to the middle square. The tiles may be turned. Can nine of these tiles cover a 6-by-6 board exactly? Answer yes or no.',
        'no', 'Colour the board like a chessboard and count how one tile divides between the colours.', [
            'The middle square of a T and its three edge-neighbours have opposite colours. So each tile covers either one dark square or three dark squares.',
            'Nine odd numbers add to an odd number. But the board has 18 dark squares, which is even. A tiling is impossible.'
        ], 'Each tile uses four squares, so area alone would allow nine tiles.',
        board(*(['......'] * 6), description='A plain 6-by-6 board. Each tile consists of three squares in a row and one attached to the middle.')),
    (5, 'try'): problem('Four corners cut away',
        'All four corner squares of a 4-by-4 board are removed. Can the board be tiled with L-shaped pieces that each cover three of the four squares of a 2-by-2 block? The pieces may be turned. Answer yes or no.',
        'yes', 'Find a way to divide the board into sections that match the tiles.', [
            'Divide the original board into four 2-by-2 blocks.',
            'Each block loses its outside corner and has exactly three squares left in an L shape. Cover each of the four blocks with one turned tile.'
        ], 'The four pieces use disjoint blocks and cover all 12 remaining squares.',
        board(' .. ', '....', '....', ' .. ', description='The four outer corner squares are missing.')),
    (5, 'transfer'): problem('Fit one square tile among dominoes',
        'A board has 4 rows and 6 columns. One tile covers a 2-by-2 block. All the other tiles are horizontal dominoes. In how many different positions can the 2-by-2 tile go if every square of the board must be covered?',
        9, 'Check the lengths of the two gaps in each row through the square tile.', [
            'Both gaps must have even length to be filled by horizontal dominoes. Starting the square tile in column A, C or E leaves gaps of lengths 0 and 4, 2 and 2, or 4 and 0.',
            'The first row of the tile can be row 1, 2 or 3. All other rows are six squares long and can be paired horizontally. Thus there are 3 × 3 = 9 positions.'
        ], 'Starting in B or D leaves an odd gap on both sides.',
        board('......', '......', '......', '......', description='Four rows of six squares.')),
    (6, 'try'): problem('Dominoes crossing a stripe',
        'A board of 6 rows and 6 columns is completely covered by dominoes. The two middle columns form a shaded stripe. Exactly four dominoes lie entirely inside the stripe. How many dominoes cover one shaded and one unshaded square?',
        4, 'Count the squares of the stripe according to how each domino meets it.', [
            'The stripe has 6 × 2 = 12 squares. The four dominoes entirely inside it cover eight of those squares.',
            'Each remaining shaded square belongs to a domino with exactly one square outside the stripe. There are 12 − 8 = 4 such dominoes.'
        ], 'For example, fill four rows with horizontal dominoes in pairs AB, CD and EF. In the other two rows, use BC and DE, and fill columns A and F with vertical dominoes across those two rows.',
        board(*(['..##..'] * 6), description='The two middle columns, C and D, are shaded.')),
    (6, 'transfer'): problem('The most upright tiles',
        'A board of 5 rows and 6 columns is completely tiled with rectangles measuring 2 by 3 unit squares. A tile is called upright if it is 3 squares high. What is the greatest possible number of upright tiles?',
        3, 'Every upright tile crosses the same middle row.', [
            'An upright tile can start in row 1, 2 or 3. In every case it covers two squares of row 3. Since that row has only six squares, at most three upright tiles fit.',
            'Place three upright tiles side by side in rows 1–3. Tile the bottom two rows with two tiles turned sideways, each three columns wide.'
        ], 'The five tiles cover 5 × 6 = 30 squares, and the upper bound is attained.',
        board('......', '......', '......', '......', '......', description='Five rows of six squares.')),
    (7, 'try'): problem('Two separate tiled panels',
        'A frame holds two separate panels. The first has 2 rows of 3 squares and the second has 2 rows of 2 squares. How many ways can both panels be tiled with dominoes? A domino cannot cross the gap between panels.',
        6, 'Count the tilings of each panel and combine the independent choices.', [
            'The first panel can have three vertical dominoes, or a pair of horizontal dominoes beside one vertical domino. That vertical domino can be at either end, giving three tilings.',
            'The second panel can be tiled with two horizontal dominoes or two vertical ones. There are 3 × 2 = 6 combinations.'
        ], 'The panels are separate positions in the frame. A choice for one imposes no restriction on the other.',
        board('... ..', '... ..', description='A 2-by-3 panel and a 2-by-2 panel separated by a gap.')),
    (7, 'transfer'): problem('Long strips on a clipped board',
        'The top-left 2-by-2 block is cut out of a 4-by-4 board. What is the greatest number of straight four-square strips that can fit on the remaining board without overlap? Some squares may be left uncovered.',
        2, 'A strip of length four must fill a whole row or a whole column.', [
            'Only rows 3 and 4 are complete, and only columns C and D are complete. Every complete row crosses every complete column.',
            'Mixing the orientations would make two strips overlap. Two strips can fit in the two complete rows, or in the two complete columns. Three cannot fit.'
        ], 'The clipped board has room by area for three strips, but their shape prevents that placement.',
        board('  ..', '  ..', '....', '....', description='The top-left 2-by-2 block is missing.')),
    (8, 'try'): problem('Pack the largest number of square tiles',
        'On a 5-by-5 board, each tile covers a 2-by-2 block of whole squares. What is the greatest number of these tiles that can be placed without overlap?',
        4, 'Mark B2, D2, B4 and D4 to find an upper bound.', [
            'Each pair of consecutive columns includes B or D. Each pair of consecutive rows includes row 2 or 4. Thus every tile covers exactly one of the four marked squares.',
            'No two tiles can use the same marked square. Four tiles can fit by dividing the top-left 4-by-4 block into four 2-by-2 blocks.'
        ], 'The four marks give a stricter bound than dividing 25 by 4.',
        board('.....', '.....', '.....', '.....', '.....', description='Five rows of five unit squares.')),
    (8, 'transfer'): problem('Dominoes around the rim',
        'The central 3-by-3 block is removed from a 5-by-5 board. In how many ways can dominoes cover the one-square-wide rim? Each domino covers two edge-adjacent squares.',
        2, 'The remaining squares form one closed chain.', [
            'Pick the top-left square. Its domino must pair it with the next square along the top or the next square down the left side.',
            'Once this pair is chosen, the remaining squares are a single chain of 14. Starting at one end forces every pair in turn. Both choices therefore give a complete tiling, for two tilings altogether.'
        ], 'Squares across the central hole do not share an edge and cannot be paired.',
        board('.....', '.   .', '.   .', '.   .', '.....', description='Only the outer rim of the 5-by-5 board remains.')),
}


def spatial_revisit(skill, visit, role):
    problems = {'SPATIAL-02': RECTANGLES, 'SPATIAL-03': TILINGS}.get(skill, {})
    return problems.get((visit, role))
