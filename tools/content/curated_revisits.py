"""Mathematically distinct revisits for the most repetitive original lesson families.

Only visits >=2 are replaced. First encounters and four previously attempted
problems retain their original identities and statement. No past-exam content.
Each replacement independently checks its answer against the original key.
"""
from fractions import Fraction

def curate(skill, role, visit, original):
    if visit <= 1 or skill not in ('DIV-03','ALG-04','DATA-02','DIG-03','SOLID-01'): return original
    a=Fraction(str(original['answer']))
    x=visit+6
    def q(title,prompt,steps,check,insight,result):
        assert Fraction(str(result))==a,(skill,role,visit,result,original['answer'])
        assert prompt.endswith(('?','.')) and '?' in prompt,(skill,role,visit,prompt)
        return dict(title=title,prompt=prompt,answer=original['answer'],steps=steps,check=check,clue=insight)

    if skill=='DIV-03' and role=='try':
        if visit==2:
            return q('Reach the next multiple of seven',
                'The number 61 is written on a board. What is the smallest positive whole number that must be added to make it a multiple of 7?',
                ['The nearest multiple of 7 above 61 is 63, because 7 × 9 = 63.',
                 'The difference 63 − 61 = 2 is the smallest positive addition.'],
                '61 + 2 = 63 is divisible by 7, while 61 + 1 = 62 is not.',
                'The question asks for the distance to the next multiple, not the remainder.',2)
        if visit==3:
            return q('Next checkpoint in a seven-step pattern',
                'A counter starts at 69 and advances one number at a time. How many advances are needed before its display first shows a multiple of 7?',
                ['Since 7 × 9 = 63, the next multiple is 7 × 10 = 70.',
                 'One advance changes 69 into 70.'], 
                'There is no multiple of 7 strictly between 69 and 70.',
                'Locate the next multiple rather than listing every possible count.',1)
        if visit==4:
            return q('A missing digit in a multiple of seven',
                'A three-digit number is written as 12□. What digit replaces the box so the number is divisible by 7?',
                ['The three-digit candidates run from 120 to 129. Only 126 is divisible by 7: 7 × 18 = 126.',
                 'The missing units digit is 6.'],
                '120 + 6 = 126; the next multiple of 7 is 133, outside the range.',
                'Use the remainder to narrow down an unknown digit.',6)
        if visit==5:
            return q('The digit that completes a divisible number',
                'A number has the form 3□0. Which digit belongs in the box if the entire number must be divisible by 7?',
                ['Look at multiples of 7 between 300 and 390 that end in 0.',
                 '350 = 7 × 50. It is the only matching multiple in this range. The digit is 5.'],
                'The closest matching multiples with a final zero are 280 and 420.',
                'Divisibility and a fixed units digit restrict the tens digit.',5)
        if visit==6:
            return q('Complete a multiple of nine',
                'A card shows 23. What is the smallest positive number to add so that the new number is divisible by 9?',
                ['The next multiple of 9 is 27, because 9 × 3 = 27.',
                 'Add 27 − 23 = 4.'],
                '23 + 4 = 27. Adding 1, 2 or 3 does not reach a multiple of 9.',
                'The distance-to-next-multiple idea works for moduli other than 7.',4)
        if visit==7:
            return q('Remainder from a length of ribbon',
                'A 52 cm ribbon is cut into as many whole 7 cm pieces as possible. What length of ribbon is left over, in centimetres?',
                ['Seven pieces use 7 × 7 = 49 cm of ribbon.',
                 'The unused part measures 52 − 49 = 3 cm.'],
                'The leftover 3 cm is smaller than 7 cm, so no further full piece fits.',
                'A remainder measures what is left, not what is needed to fill a box.',3)
        if visit==8:
            return q('Minutes until the next bell',
                'A bell rings at 0 minutes and every 9 minutes after that. At 43 minutes, how many minutes are left until the next ring?',
                ['The bell rings at 36 minutes and then at 45 minutes.',
                 'From 43 to 45 minutes is 2 minutes.'],
                '43 lies between two consecutive multiples of 9: 36 and 45.',
                'A repeating schedule is the same mathematical idea as modular arithmetic.',2)

    if skill=='DIV-03' and role=='transfer':
        r=3+(visit+2)%3
        if visit==2:
            return q('A product of consecutive remainders',
                'A whole number N leaves remainder 4 when divided by 7. What remainder does N(N+1)+1 leave when divided by 7?',
                ['Replace N by its remainder 4 when finding a remainder after division by 7.',
                 'Compute 4 × 5 + 1 = 21. Its remainder on division by 7 is 0.'],
                'The factors of 7 in the difference between N and 4 do not change the result.',
                'A polynomial can be evaluated using only a remainder class.',0)
        if visit==3:
            return q('Square the difference before dividing',
                'A whole number N leaves remainder 5 when divided by 7. What is the remainder when (N−2)²+1 is divided by 7?',
                ['N−2 has remainder 3 after division by 7.',
                 'Then (N−2)²+1 has the same remainder as 3²+1 = 10, namely 3.'],
                'Try N=5 and N=12: both give remainder 3.',
                'Taking powers preserves congruence when done before reducing the result.',3)
        if visit==4:
            return q('Double a remainder and add three',
                'When an integer N is divided by 7, the remainder is 3. What remainder does 2N+3 have when divided by 7?',
                ['Use N=7k+3 to express all possible integers with that remainder.',
                 'Then 2N+3=14k+9. Since 9=7+2, the remainder is 2.'],
                'The 14k part contributes no remainder after dividing by 7.',
                'Use congruences to simplify an entire family of unknown numbers.',2)
        if visit==5:
            return q('Multiply two neighbouring expressions',
                'A positive integer N has remainder 4 on division by 7. What remainder does (N−1)(N+1)+2 leave upon division by 7?',
                ['Replace N by remainder 4: the product is congruent to 3 × 5 + 2.',
                 'That is 17, which leaves remainder 3 when divided by 7.'],
                'Expanding gives N²+1; using N=4 gives 17 as a quick independent check.',
                'Related factors can be used without finding the unknown number itself.',3)
        if visit==6:
            return q('A negative result inside a remainder question',
                'An integer N leaves remainder 5 on division by 7. What remainder does 3N−2 leave when divided by 7?',
                ['Compute with the remainder first: 3 × 5 − 2 = 13.',
                 'The number 13 is one less than 14, so it leaves remainder 6 on division by 7.'],
                'Replacing N by N+7 increases 3N−2 by 21, a multiple of 7.',
                'Subtracting does not break the repeating pattern of remainders.',6)
        if visit==7:
            return q('A cubic expression without huge arithmetic',
                'An integer N leaves remainder 3 when divided by 7. What is the remainder of N³−1 on division by 7?',
                ['The remainder can be found from 3³−1=27−1=26.',
                 '26=7 × 3+5, so the remainder is 5.'],
                'No actual value for N is needed; adding a multiple of 7 cannot change the remainder.',
                'The power may be enormous, yet only one small representative matters.',5)
        if visit==8:
            return q('A shifted square in modular arithmetic',
                'A whole number N has remainder 4 when divided by 7. What remainder does (N+1)²+2 leave when divided by 7?',
                ['N+1 leaves remainder 5.',
                 'Then 5²+2=27. Dividing by 7 leaves remainder 6.'],
                '27=7 × 3+6, which is between 0 and 6 as required for a remainder.',
                'First change the number, then square it, and finally reduce the result.',6)

    if skill=='ALG-04' and role=='try':
        v=int(a)
        if visit==2:
            y=(5*v-12)//4
            return q('Reverse three arithmetic operations',
                f'A number is multiplied by 5, then 12 is subtracted, and the result is divided by 4. The final output is {y}. What was the number?',
                [f'Reverse dividing by 4: {y} × 4 = {4*y}.',
                 f'Add back 12, then divide by 5: ({4*y}+12) ÷ 5 = {v}.'],
                f'The original sequence gives (5 × {v} − 12) ÷ 4 = {y}.',
                'Inverting the operations in reverse order prevents incorrect shortcuts.',v)
        if visit==3:
            y=2*(v-3)+7
            return q('Work backwards through a rule',
                f'A machine subtracts 3 from a number, doubles the result, then adds 7. Its output is {y}. What number went in?',
                [f'Remove the final 7: {y} − 7 = {y-7}.',
                 f'Undo doubling and subtracting 3: {y-7} ÷ 2 + 3 = {v}.'],
                f'({v} − 3) × 2 + 7 = {y}, confirming the input.',
                'Each step must be undone in the opposite order from which it was performed.',v)
        if visit==4:
            y=(v-18)**2
            return q('An inverse square with a condition',
                f'A number greater than 18 is reduced by 18 and then squared. The result is {y}. What was the original number?',
                [f'The squared difference is {y}, so the difference has magnitude {int(y**0.5)}.',
                 f'Because the starting number is greater than 18, use the positive difference: 18 + {int(y**0.5)} = {v}.'],
                f'({v} − 18)² = {y}; the extra condition removes the other square-root possibility.',
                'Squaring loses the sign, so a constraint is sometimes necessary for a unique inverse.',v)
        if visit==5:
            y=3*(2*v+3)-5
            return q('Undo a four-operation machine',
                f'A machine doubles a number, adds 3, multiplies the result by 3, then subtracts 5. Its display reads {y}. What was the input?',
                [f'Add 5 to the display and divide by 3: ({y} + 5) ÷ 3 = {2*v+3}.',
                 f'Subtract 3 and divide by 2: ({2*v+3} − 3) ÷ 2 = {v}.'],
                f'Starting with {v} produces {y} when the four operations are followed in order.',
                'Working backwards through several operations is an early form of solving a composed equation.',v)

    if skill=='ALG-04' and role=='transfer':
        v=int(a)
        if visit==2:
            y=(v-4)//2+1
            return q('Recover the original donation',
                f'A charity has some tokens. It gives away 4, puts half of those remaining in a box, then puts one more token in the box. The box contains {y} tokens. How many tokens did the charity start with?',
                [f'The box had {y-1} before the extra token was added.',
                 f'This was half of {2*(y-1)} remaining tokens. Adding back the 4 donated tokens gives {v}.'],
                f'({v} − 4) ÷ 2 + 1 = {y}.',
                'The final extra token is not part of the half that was boxed.',v)
        if visit==3:
            y=4*(v+3)-9
            return q('Find an input hidden in fourfold growth',
                f'An integer is increased by 3, multiplied by 4, and then reduced by 9. The result is {y}. What was the integer?',
                [f'Undo subtracting 9: {y} + 9 = {y+9}.',
                 f'Divide by 4 and subtract 3: {y+9} ÷ 4 − 3 = {v}.'],
                f'({v}+3) × 4 − 9 = {y}.',
                'Group operations carefully: the addition occurs before multiplication.',v)
        if visit==4:
            y=(2*v-7)//3
            return q('An unknown number behind an exact division',
                f'A number is doubled. Seven is subtracted, and the result is split into three equal whole-number parts. Each part is {y}. What was the original number?',
                [f'Three equal parts total 3 × {y} = {3*y}.',
                 f'Add 7 and halve: ({3*y} + 7) ÷ 2 = {v}.'],
                f'2 × {v} − 7 = {3*y}, which divides exactly into three parts.',
                'The equal-parts condition and subtraction order both matter.',v)
        if visit==5:
            y=3*(v-2)//2
            return q('Undo a scaled sequence',
                f'An unknown even number is reduced by 2, multiplied by 3, and then halved. Its final value is {y}. What was the starting number?',
                [f'Double the output and divide by 3: 2 × {y} ÷ 3 = {v-2}.',
                 f'Add back 2 to recover the original number {v}.'],
                f'({v} − 2) × 3 ÷ 2 = {y}, and {v} is even as required.',
                'A divisibility condition can confirm the order of operations was respected.',v)

    if skill=='DATA-02' and role=='try':
        # Revisit problems use new individual observations, not repeated team means.
        m={2:13,3:11,4:10,5:14,6:15,7:16,8:9}[visit]
        p,t={2:(15,17),3:(21,22),4:(24,26),5:(11,12),
             6:(6,8),7:(1,2),8:(30,34)}[visit]
        last=12*x+60-m*x-p-t
        assert last>0
        result=Fraction(m*x+p+t+last,x+3)
        contexts={
          2:('Update a class average',f'A class of {x} students has an average test score of {m} points. Three more students join with scores {p}, {t} and {last}. What is the average for all {x+3} students? Give an exact fraction if necessary.'),
          3:('A chess season with three new games',f'Across {x} chess matches a player averages {m} points per game. The next three matches give {p}, {t} and {last} points. What is the average per match over all {x+3} matches? Give an exact fraction if needed.'),
          4:('Add new observations to a data set',f'A survey has {x} readings with mean {m}. Three further readings are {p}, {t} and {last}. What is the mean of the expanded data set? Give an exact fraction if needed.'),
          5:('A laboratory reports three more results',f'A laboratory collects {x} measurements with mean {m}. It then records {p}, {t} and {last}. What is the new mean of all {x+3} measurements, expressed as an exact fraction if necessary?'),
          6:('Three additional results change the mean',f'The mean of {x} quiz results is {m}. The final three students score {p}, {t} and {last}. What is the mean of all {x+3} results? Give an exact fraction if needed.'),
          7:('Very low scores join a data set',f'A set of {x} scores has mean {m}. Three further scores are {p}, {t} and {last}. What is the mean when the scores are combined? Give an exact fraction if needed.'),
          8:('A tournament average after bonus rounds',f'An athlete earns a mean of {m} points over {x} rounds. In three bonus rounds the athlete earns {p}, {t} and {last}. What is the mean points per round over all {x+3} rounds? Give an exact fraction if needed.')
        }
        title,prompt=contexts[visit]
        return q(title,prompt,
            [f'The original {x} observations total {x} × {m} = {x*m}.',
             f'The three new observations contribute {p} + {t} + {last} = {p+t+last}. All {x+3} observations sum to {12*x+60}.',
             f'Divide the combined total by the number of observations: ({12*x+60}) ÷ {x+3} = {result}.'],
            f'The new total is {x*m}+{p+t+last}={12*x+60}, and the denominator is {x+3}, not {x}.',
            'Averages must be combined through their totals and their numbers of observations.',result)

    if skill=='DATA-02' and role=='transfer':
        recorded_mean={2:13,3:12,4:15,5:13,6:12,7:15,8:13}[visit]
        recorded={2:20,3:10,4:30,5:20,6:10,7:30,8:20}[visit]
        actual= x+10 if visit in (2,5,8) else (2*x if visit in (3,6) else 20-x)
        corrected=recorded_mean*x-recorded+actual
        result=Fraction(corrected,x)
        contexts={
          2:('Repair an incorrect science average',f'The mean of {x} science measurements is reported as {recorded_mean}. One reading was entered as {recorded} but should have been {actual}. What is the corrected mean? Give an exact fraction if needed.'),
          3:('Correct a running-club data entry',f'A running club calculates a mean time of {recorded_mean} minutes from {x} recorded times. One time was entered as {recorded} minutes instead of {actual} minutes. What is the corrected mean time? Give an exact fraction if needed.'),
          4:('Find the true average temperature',f'The mean of {x} daily temperatures is reported as {recorded_mean} degrees. A faulty sensor logged {recorded} degrees on one day, but the actual temperature was {actual} degrees. What is the corrected mean? Give an exact fraction if needed.'),
          5:('Correct one missing mark on a score sheet',f'After {x} quiz scores were recorded, the mean was {recorded_mean}. One score marked {recorded} should have been {actual}. What is the corrected mean? Give an exact fraction if needed.'),
          6:('An incorrect assembly count',f'The mean number of parts assembled in {x} sessions was entered as {recorded_mean}. One session was recorded as {recorded} parts rather than the actual {actual}. What should the mean be? Give an exact fraction if needed.'),
          7:('Spot a faulty weather observation',f'A weather station reports an average of {recorded_mean} degrees from {x} days. One temperature of {recorded} degrees should have been {actual} degrees. What is the corrected average? Give an exact fraction if needed.'),
          8:('Fix the club tournament average',f'A club records {x} tournament scores with mean {recorded_mean}. An entry of {recorded} points is corrected to {actual} points. What is the new average score? Give an exact fraction if needed.')
        }
        title,prompt=contexts[visit]
        return q(title,prompt,
            [f'The recorded total is {x} × {recorded_mean} = {x*recorded_mean}.',
             f'Replace the incorrect {recorded} with {actual}. The total becomes {x*recorded_mean} − {recorded} + {actual} = {corrected}.',
             f'There are still {x} values, so the corrected mean is {corrected} ÷ {x} = {result}.'],
            f'The number of observations does not change. The total changes by {actual-recorded}.',
            'Correct the total first; do not change the divisor when one value is replaced.',result)

    if skill=='DIG-03' and role=='try':
        if visit==2:
            return q('Count numbers containing a digit',
                'From 19 to 63 inclusive, how many whole numbers contain the digit 2 at least once?',
                ['The ten numbers 20 to 29 all contain a 2.',
                 'Four more numbers, 32, 42, 52 and 62, also contain a 2. The total is 10 + 4 = 14.'],
                '22 is one number despite containing two copies of the digit 2.',
                'Counting numbers that contain a digit differs from counting individual occurrences of that digit.',14)
        if visit==3:
            return q('Which numbers repeat a digit?',
                'How many whole numbers from 1 to 112 inclusive have at least one digit appearing twice or more?',
                ['The two-digit numbers that repeat a digit are 11, 22, 33, 44, 55, 66, 77, 88 and 99: nine numbers.',
                 'From 100 to 112, the repeated-digit numbers are 100, 101, 110, 111 and 112: five more. The answer is 14.'],
                'The number 111 qualifies once, not three times, because the objects counted are whole numbers.',
                'Keep a complete list of cases and avoid counting one number several times.',14)
        if visit==4:
            return q('Count the characters in a sequence of labels',
                'A small exhibition labels its displays with every whole number from 4 to 13. How many printed digits are used altogether?',
                ['There are six one-digit labels from 4 to 9, using 6 digits.',
                 'There are four two-digit labels from 10 to 13, using 8 digits. Total 6 + 8 = 14.'],
                'There are ten displays, but the number of printed digits is 14.',
                'Count each label according to its length rather than treating all numbers as the same size.',14)
        if visit==5:
            return q('Count every appearance of the number seven',
                'A ticket roll is numbered from 70 to 109 inclusive. How many times is the digit 7 printed?',
                ['The tens position contributes a 7 in every number from 70 to 79, for 10 occurrences.',
                 'The units position contributes another at 77, 87, 97 and 107. Total 10 + 4 = 14.'],
                'The ticket 77 contributes two occurrences, one from each digit position.',
                'When counting occurrences, different positions contribute separately.',14)
        if visit==6:
            return q('Count a repeated units digit',
                'A scoreboard lists all whole numbers from 10 to 49 inclusive. How many copies of the digit 1 appear in those numbers?',
                ['The tens position contributes 10 copies of 1 in the numbers 10 through 19.',
                 'The units position contributes 1 at 11, 21, 31 and 41. So the total is 14.'],
                '11 contributes two copies because both of its digits are 1.',
                'Separate contributions by digit position before combining them.',14)
        if visit==7:
            return q('Count labels containing at least one three',
                'A museum labels its cases with consecutive numbers from 29 to 73. How many labels contain the digit 3 at least once?',
                ['The ten labels 30 through 39 contain a 3 in the tens place.',
                 'The labels 43, 53, 63 and 73 also contain 3. This gives 10 + 4 = 14 labels.'],
                'The label 33 is counted once because this question counts labels, not printed copies of the digit.',
                'The phrase at least once changes the mathematical object being counted.',14)

    if skill=='DIG-03' and role=='transfer':
        if visit==2:
            return q('Digits across the one-digit boundary',
                'A library prints shelf labels 9, 10, 11, and every consecutive integer through 49. How many individual digit characters does it print?',
                ['The label 9 has one digit.',
                 'The forty labels from 10 through 49 each have two digits: 40 × 2 = 80. Total 1 + 80 = 81.'],
                'There are 41 labels but 81 digits, because one label has a different length.',
                'A change from one-digit to two-digit labels changes the number of characters per label.',81)
        if visit==3:
            return q('Count digits on inclusive numbered cards',
                'Cards are numbered consecutively from 7 to 55, including both ends. How many digits are printed on all the cards?',
                ['The three cards 7, 8 and 9 need one digit each.',
                 'The forty-six cards from 10 to 55 need two digits each. Total 3 + 46 × 2 = 95.'],
                '55 − 10 + 1 = 46 includes both ends of the two-digit range.',
                'Always split across a change in number length and count endpoints explicitly.',95)
        if visit==4:
            return q('Digit characters in a numbered strip',
                'A strip prints every integer from 6 through 61, in order. How many individual digits appear on the strip?',
                ['Four labels, 6 to 9, each use one digit.',
                 'The remaining fifty-two labels, 10 to 61, each use two. The total is 4 + 52 × 2 = 108.'],
                '61 − 10 + 1 = 52, so no endpoint is omitted.',
                'Count lengths of individual labels, not only the number of labels.',108)
        if visit==5:
            return q('A page-number printing budget',
                'A booklet prints the page numbers from 2 through 59. How many digit characters are needed to print all those page numbers?',
                ['The eight page numbers 2 to 9 are one digit each.',
                 'The fifty page numbers 10 to 59 are two digits each. Total 8 + 50 × 2 = 108.'],
                'Fifty-eight pages are numbered, but many numbers need two characters.',
                'A digit-counting budget depends on the number of numerals at each length.',108)
        if visit==6:
            return q('Two sizes of membership labels',
                'A club prints 20 different three-digit badges and 12 different four-digit badges. Leading zeroes are printed wherever needed. How many digit characters are used in total?',
                ['The twenty three-digit badges require 20 × 3 = 60 characters.',
                 'The twelve four-digit badges require 12 × 4 = 48 more. Together they require 108 characters.'],
                '60 + 48 = 108, independently of the individual numbers printed on the badges.',
                'When label length is specified, multiply quantity by digits per label before adding.',108)
        if visit==7:
            return q('A mixed batch of number plates',
                'A workshop prints 30 three-digit identification labels and 9 two-digit labels. How many digits will be printed across all 39 labels?',
                ['Thirty labels of length 3 use 30 × 3 = 90 digit characters.',
                 'Nine labels of length 2 use 9 × 2 = 18 more. The combined total is 108.'],
                '90 + 18 = 108 digits even though there are only 39 separate labels.',
                'The requested count is printed digits, not the number of identification labels.',108)

    if skill=='SOLID-01' and role=='try':
        v=x
        if visit==2:
            return q('Remove a corner notch from a cuboid',
                f'A solid cuboid contains {v} × 3 × 4 unit cubes. A 5 × 2 × 1 rectangular piece is removed from one corner. How many unit cubes remain?',
                [f'The complete solid contains {v} × 3 × 4 = {12*v} cubes.',
                 f'The removed piece contains 5 × 2 × 1 = 10 cubes, leaving {12*v}-10 = {12*v-10}.'],
                'The rectangular piece fits inside the original dimensions and the missing cubes are counted once.',
                'A difference of volumes is more reliable than counting the visible faces.',12*v-10)
        if visit==3:
            return q('Count cubes in an attached arm',
                f'A model joins a {v} × 2 × 5 cuboid to a separate {v-5} × 2 × 1 cuboid along a face, without overlap. How many unit cubes make up the model?',
                [f'The larger component contains {10*v} cubes.',
                 f'The attached arm has {v-5} × 2 × 1 = {2*(v-5)} cubes. Together that is {10*v+2*(v-5)}.'],
                'Every cube belongs to exactly one component because the pieces touch but do not overlap.',
                'Count disjoint three-dimensional components and add their volumes.',12*v-10)
        if visit==4:
            return q('A tower with one incomplete shelf',
                f'A display has {v} shelves of unit cubes. Every shelf except the last has exactly 12 cubes, while the last has only 2. How many unit cubes are in the display?',
                [f'There are {v-1} complete shelves containing {12*(v-1)} cubes.',
                 f'The incomplete shelf adds 2, giving {12*(v-1)} + 2 = {12*v-10}.'],
                'Multiplying all shelves by 12 would count ten cubes that are not actually present.',
                'Handle an exceptional layer separately instead of pretending every layer is complete.',12*v-10)
        if visit==5:
            return q('A ten-cube groove in a solid wall',
                f'A solid block is {v} cubes long, 4 cubes wide and 3 cubes high. A straight run of 10 cubes along one outer edge is removed. How many unit cubes remain?',
                [f'Before removing any cubes there are {v} × 4 × 3 = {12*v}.',
                 f'Ten distinct cubes are taken away from one edge. The remaining count is {12*v} − 10 = {12*v-10}.'],
                'The length is at least 10, so the specified run fits completely along the block.',
                'A run removed from a solid affects its total volume even when the remaining object is irregular.',12*v-10)
        if visit==6:
            return q('Two missing bars from a long block',
                f'A cuboid contains {v} × 2 × 6 unit cubes. Two separate, non-overlapping bars, each 5 cubes long and one cube thick, are removed. How many unit cubes remain?',
                [f'Originally the block contains {v} × 2 × 6 = {12*v} cubes.',
                 f'Each bar contains 5 cubes, so two bars remove 10. The remainder is {12*v-10}.'],
                'The bars fit and do not overlap; otherwise subtracting ten would overcount missing cubes.',
                'Disjoint missing pieces can be counted independently and subtracted from the whole.',12*v-10)
        if visit==7:
            return q('Three rectangular pieces build one model',
                f'A model uses three separate solid pieces with dimensions {v} × 1 × 3, {v} × 1 × 4, and {v-2} × 1 × 5 unit cubes. They are joined without overlapping. How many unit cubes are used?',
                [f'The first two pieces contain 3 × {v} = {3*v} and 4 × {v} = {4*v} cubes.',
                 f'The third contains 5 × {v-2} = {5*(v-2)} cubes. Together: {3*v}+{4*v}+{5*(v-2)} = {12*v-10}.'],
                'All three pieces are disjoint before joining, so no cube is counted twice.',
                'The total of several different rectangular solids can be simplified using the distributive law.',12*v-10)
        if visit==8:
            return q('A mosaic with one shortened row',
                f'A mosaic is built from 12 rows, each designed to hold {v} unit cubes. Ten positions in the final row are deliberately left empty. How many cubes are present?',
                [f'Twelve full rows would contain 12 × {v} = {12*v} cubes.',
                 f'The ten unfilled positions reduce the count to {12*v}-10 = {12*v-10}.'],
                'The incomplete last row is still counted once; its ten empty positions must not be counted as cubes.',
                'A repeated shape with a known exception is counted by subtracting the missing pieces.',12*v-10)

    if skill=='SOLID-01' and role=='transfer':
        v=x
        if visit==2:
            return q('Remove the top layer of a block',
                f'A solid array of unit cubes is {v} long, 11 wide and 3 high. The entire top layer is removed. How many cubes are left?',
                [f'The complete array has {v} × 11 × 3 = {33*v} cubes.',
                 f'The removed top layer has {v} × 11 = {11*v} cubes. The remaining two layers contain {22*v}.'],
                'The number remaining also equals 2 × 11 × '+str(v)+' = '+str(22*v)+'.',
                'Removing a whole layer is different from removing a narrow tunnel.',22*v)
        if visit==3:
            return q('Two cuboids joined edge to edge',
                f'A model is assembled from two non-overlapping cuboids of dimensions {v} × 3 × 4 and {v} × 2 × 5 unit cubes. What is the combined number of unit cubes?',
                [f'The first cuboid has {v} × 3 × 4 = {12*v} cubes.',
                 f'The second has {v} × 2 × 5 = {10*v} cubes. Together there are {12*v}+{10*v} = {22*v}.'],
                'The touching faces are not extra cubes, and no interiors overlap.',
                'Joining solids along a face does not change the number of cubes in either piece.',22*v)
        if visit==4:
            return q('A full-length groove along a corner',
                f'A block is {v} cubes long, 6 wide and 4 high. A groove 1 cube wide and 2 cubes deep is cut along its entire length at a corner. How many unit cubes remain?',
                [f'The original block contains {v} × 6 × 4 = {24*v} cubes.',
                 f'The groove removes {v} × 1 × 2 = {2*v} cubes. The remainder is {24*v}-{2*v} = {22*v}.'],
                'The cut runs along an outside corner; it removes a fixed 1-by-2 cross-section at every position.',
                'Multiply the cross-section area by the length to find a volume removed.',22*v)
        if visit==5:
            return q('A trench carved across every layer',
                f'A large block is {v} cubes long, 5 wide and 5 high. A straight 3-by-1 channel runs its full length. How many unit cubes remain after the channel is removed?',
                [f'The original solid contains {v} × 5 × 5 = {25*v} cubes.',
                 f'The channel removes 3 × 1 × {v} = {3*v} cubes. The remainder is {25*v}-{3*v} = {22*v}.'],
                'Every cross-section of the block loses three of its twenty-five cubes.',
                'Count the volume removed from repeated cross-sections rather than trying to count hidden faces.',22*v)
        if visit==6:
            return q('A repeating layer with two gaps',
                f'A tower has {v} identical layers. Each layer is a 4-by-6 arrangement of cubes with two different corner positions empty. How many unit cubes make up the complete tower?',
                [f'A full layer would have 4 × 6 = 24 cubes, but two corner positions are missing.',
                 f'Each actual layer has 22 cubes. With {v} such layers, the total is 22 × {v} = {22*v}.'],
                'Each layer has the same two missing positions, so the stack never fills those gaps.',
                'An invariant cross-section can be multiplied by the number of layers.',22*v)
        if visit==7:
            return q('Two vertical towers with different bases',
                f'Two solid towers are each {v} cubes high. Their rectangular bases are 5-by-2 and 3-by-4 unit squares. They do not overlap. How many unit cubes are in both towers?',
                [f'The first base contains 5 × 2 = 10 cubes per layer, making {10*v} cubes.',
                 f'The second base has 3 × 4 = 12 cubes per layer, making {12*v}. Together there are {22*v}.'],
                'The towers have equal height but different base areas, and neither overlaps the other.',
                'A solid volume is base area multiplied by height; add the distinct volumes.',22*v)
        if visit==8:
            return q('An array with an attached square patch',
                f'A model has {v} separate rows. Each row contains a 3-by-6 unit-cube rectangle and a separate 2-by-2 square patch of cubes, without overlap. How many unit cubes are used?',
                [f'Each row contains 3 × 6 + 2 × 2 = 18 + 4 = 22 unit cubes.',
                 f'With {v} identical rows, the model contains 22 × {v} = {22*v} cubes.'],
                'The two shapes within one row do not overlap, so both contribute their full counts.',
                'Breaking a solid into repeated non-overlapping units is a direct alternative to subtraction.',22*v)
    return original
