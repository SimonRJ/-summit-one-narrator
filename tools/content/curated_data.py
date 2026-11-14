"""Original DATA-03 revisits. The table and chart values are givens."""
from curated_spatial import problem


def table(columns, rows, caption):
    return dict(kind='table', columns=columns, rows=rows, caption=caption)


def bars(labels, values, ticks, caption):
    return dict(kind='bars', labels=labels, values=values, ticks=ticks, caption=caption)


DATA_REVISITS = {
    (2, 'try'): problem('Two values between the ticks',
        'The chart shows the lengths of two toy boats. Each tick is 4 cm above the previous tick. The top of each bar is halfway between neighbouring ticks. What is the total length, in centimetres, of the two boats?',
        56, 'Read the value at the top of each bar.', [
            'The axis starts at 20 cm. The first bar ends halfway between 20 and 24, so the first boat is 22 cm long.',
            'The second bar ends halfway between 32 and 36, so the second boat is 34 cm long. Their total length is 22 + 34 = 56 cm.'
        ], 'The bars extend 2 cm and 14 cm above the drawn baseline. Those heights are not the boats’ full lengths.',
        bars(('Boat A', 'Boat B'), (22, 34), (20, 24, 28, 32, 36), 'Boat lengths (cm). Boat A ends halfway between 20 and 24. Boat B ends halfway between 32 and 36.')),
    (2, 'transfer'): problem('Reading the two keys',
        'Two clubs use different keys in their book donation records. Their counts of full and half symbols are shown below. What is the difference between the numbers of books they collected?',
        9, 'Convert each display using its own key.', [
            'Cedar uses a key of 6 books per symbol. Its four full symbols and one half give 24 + 3 = 27 books.',
            'Banksia uses a key of 8 books per symbol. Its four full symbols and one half give 32 + 4 = 36 books.'
        ], 'Banksia collected 36 − 27 = 9 more books.',
        table(('Club', 'Full', 'Half', 'Books per full symbol'), (('Cedar', 4, 1, 6), ('Banksia', 4, 1, 8)), 'Symbols in each club’s record.')),
    (3, 'try'): problem('Finding Thursday’s count',
        'The table gives the numbers of birds counted each day. There were 80 birds counted in total over the five days. How many were counted on Thursday?',
        18, 'Add the four known counts, then compare with the total.', [
            'The four known counts add to 16 + 12 + 20 + 14 = 62.',
            'The total includes Thursday, so Thursday’s count was 80 − 62 = 18.'
        ], 'Putting 18 in the gap brings the five-day total to 80.',
        table(('Day', 'Birds'), (('Mon', 16), ('Tue', 12), ('Wed', 20), ('Thu', '?'), ('Fri', 14)), 'Bird counts by day.')),
    (3, 'transfer'): problem('Two bars with the same height',
        'Two charts show the scores of teams A and B. Both have tick marks 5 points apart. Team A’s chart starts at 20 points and Team B’s starts at 35 points. Each bar rises 10 points above its own baseline. How many more points did the higher-scoring team earn?',
        15, 'The scale is the same, but the baselines are different.', [
            'Team A’s score was 20 + 10 = 30. Team B’s was 35 + 10 = 45.',
            'The difference is 45 − 30 = 15 points. Since the rises are equal, the same difference is visible in their baselines: 35 − 20 = 15.'
        ], 'Equal bar heights across two charts only imply equal values if the baselines and scales also agree.',
        table(('Team', 'Axis starts at', 'Bar rises by'), (('A', 20, 10), ('B', 35, 10)), 'Axis positions and bar rises in points.')),
    (4, 'try'): problem('How many people chose one fruit?',
        'Each of 30 people chose apple, pear, or both. The display gives the total number choosing each fruit. How many people chose exactly one of the two fruits?',
        20, 'People who chose both are counted in both bars.', [
            'The bars count 24 apple choices and 16 pear choices, making 40 choices by 30 people.',
            'Every person made one choice, and those who chose both made one extra choice. The 10 extra choices mean 10 people chose both. Therefore 30 − 10 = 20 chose exactly one.'
        ], 'There were 14 apple-only and 6 pear-only voters.',
        bars(('Apple', 'Pear'), (24, 16), (0, 8, 16, 24, 32), 'Apple reaches 24 votes. Pear reaches 16 votes.')),
    (4, 'transfer'): problem('Which turn had the greater increase?',
        'The table records the total distance travelled by a cart, measured from the start. During which numbered turn did the cart travel the farthest? Enter the turn number.',
        3, 'Find the gain between readings for each turn.', [
            'In turns 1 and 2, the gains were 9 − 0 = 9 m and 13 − 9 = 4 m.',
            'In turns 3 and 4, the gains were 25 − 13 = 12 m and 30 − 25 = 5 m. The greatest gain was in turn 3.'
        ], 'The final reading is the greatest total distance from the start. The largest change occurred one turn earlier.',
        table(('After turn', 'Total (m)'), ((0, 0), (1, 9), (2, 13), (3, 25), (4, 30)), 'Cumulative distance from the start.')),
    (5, 'try'): problem('Minutes represented by each mark',
        'A swimming log uses the same key for every row. A half symbol stands for half the value of a full one. The two sessions together lasted 70 minutes. How many minutes does one full symbol represent?',
        10, 'Combine the symbols first, then use the total to find the key.', [
            'There are 2 + 4 = 6 full symbols. The two half symbols make one more full symbol.',
            'Seven full symbols stand for 70 minutes, so each full symbol stands for 10 minutes.'
        ], 'The two sessions lasted 25 and 45 minutes, which add to 70.',
        table(('Session', 'Full symbols', 'Half symbols'), (('Monday', 2, 1), ('Friday', 4, 1)), 'Symbols in the swimming log.')),
    (5, 'transfer'): problem('Replace one incorrect reading',
        'A class measured rainfall on four days. One reading was entered as 14 mm instead of 8 mm. After the correction, how many millimetres was the mean daily rainfall?',
        10, 'Correct the total, then divide by the same number of days.', [
            'The displayed readings add to 7 + 14 + 15 + 10 = 46 mm. Replacing 14 with 8 reduces the total by 6 mm.',
            'The corrected total is 40 mm, so the mean over four days is 40 ÷ 4 = 10 mm.'
        ], 'Adding the corrected readings directly also gives 7 + 8 + 15 + 10 = 40.',
        table(('Day', 'Recorded (mm)'), ((1, 7), (2, 14), (3, 15), (4, 10)), 'Rainfall as it was first entered.')),
    (6, 'try'): problem('Choosing bars with the same total',
        'The chart shows how many stickers were collected by each of four houses. How many different pairs of houses collected exactly as many stickers as the other two houses combined? Count each pair of houses once.',
        2, 'Any pair that matches the remaining pair must account for half the total.', [
            'The four counts are 6, 4, 7 and 5. Together they make 22, so a matching pair must total 11.',
            'Six goes with five, and four goes with seven. The other pair sums are 9, 10, 12 and 13, so there are exactly two pairs.'
        ], 'There is one way to split the houses into matching groups, but two pairs satisfy the question.',
        bars(('Red', 'Blue', 'Gold', 'Green'), (6, 4, 7, 5), (0, 2, 4, 6, 8), 'Red reaches 6, Blue 4, Gold 7 and Green 5.')),
    (6, 'transfer'): problem('Find the middle score',
        'The table shows how many pupils earned each score. What was the median score among all pupils?',
        6, 'Use the frequencies to locate the middle pupils in score order.', [
            'There are 3 + 5 + 1 + 3 = 12 pupils. The middle two are sixth and seventh in score order.',
            'The first three scored 4. Pupils in positions 4 through 8 scored 6. So the sixth and seventh both scored 6, giving a median of 6.'
        ], 'Each pupil contributes one score. The four distinct score labels alone do not represent the class.',
        table(('Score', 'Pupils'), ((4, 3), (6, 5), (8, 1), (10, 3)), 'Frequency of each score.')),
    (7, 'try'): problem('Read the two map scales',
        'The two maps show different parks. On both maps the drawn path is 5 cm long. The table gives the actual distance represented by each centimetre. How many metres longer is the real path shown on Map B?',
        60, 'Compare the two scales per centimetre, then apply the length of the paths.', [
            'One centimetre on Map B represents 32 − 20 = 12 more metres than one centimetre on Map A.',
            'The drawn paths are each 5 cm long, so the difference in real lengths is 5 × 12 = 60 metres.'
        ], 'The actual lengths are 100 m and 160 m.',
        table(('Map', 'Metres per cm'), (('A', 20), ('B', 32)), 'Distance scales printed on the maps.')),
    (7, 'transfer'): problem('What the broken axis exaggerates',
        'The chart shows the heights of two seedlings, measured in centimetres. A student says, “The bar for B is three times as tall, so the seedling is three times as tall.” How many times as tall as A is seedling B? Give an exact fraction.',
        '6/5', 'A comparison of real heights must use both values measured from zero.', [
            'The chart starts at 18 cm. A reaches 20 cm and B reaches 24 cm.',
            'The ratio of the actual heights is 24 ÷ 20 = 6/5. The bars rise by 2 and 6 cm above the drawn baseline, which explains the student’s ratio of three.'
        ], 'The ratio 6/5 is only a little bigger than one, which agrees with a height difference of 4 cm.',
        bars(('A', 'B'), (20, 24), (18, 20, 22, 24, 26), 'Seedling height (cm). Axis begins at 18. A reaches 20, and B reaches 24.')),
}


def data_revisit(skill, visit, role):
    if skill == 'DATA-03':
        return DATA_REVISITS.get((visit, role))
    return None
