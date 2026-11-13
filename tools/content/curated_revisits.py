"""Mathematically distinct revisits for the most repetitive original lesson families.

Only visits >=2 are replaced. First encounters and four previously attempted
problems retain their original identities and statement. No past-exam content.
Each replacement independently checks its answer against the original key.
"""
from fractions import Fraction

def curate(skill, role, visit, original):
    if visit <= 1: return original
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
                'A positive integer N has remainder 4 on division by 7. Find the remainder of (N−1)(N+1)+2 upon division by 7.',
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
    return original
