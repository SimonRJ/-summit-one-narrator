"""Mathematically distinct revisits for the most repetitive original lesson families.

Only visits >=2 are replaced. First encounters and four previously attempted
problems retain their original identities and statement. No past-exam content.
Each replacement independently checks its answer against the original key.
"""
from fractions import Fraction

def curate(skill, role, visit, original):
    if visit <= 1 or skill not in ('DIV-03','ALG-04','DATA-02'): return original
    a=Fraction(str(original['answer']))
    x=visit+6
    def q(title,prompt,steps,check,insight,result):
        assert Fraction(str(result))==a,(skill,role,visit,result,original['answer'])
        assert prompt.endswith('?'),(skill,role,visit,prompt)
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
          5:('A laboratory reports three more results',f'A laboratory collects {x} measurements with mean {m}. It then records {p}, {t} and {last}. Find the new mean of all {x+3} measurements as an exact fraction. What value do you get?'),
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
    return original
