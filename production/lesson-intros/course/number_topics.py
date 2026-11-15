"""Number structure, positional constraints and repeating patterns."""

from itertools import product
from math import gcd, isqrt, lcm

from story import Example, Topic, bars, chain, grid, say, spoken_list, table, tiles


def repunits(lesson):
    v = lesson.visit
    digits = 3 + v % 3
    ones = int("1" * digits)
    multiplier = 3 + v
    repdigit = ones * multiplier
    a,b = 2+v, 7-v
    palindrome = 1001*a + 110*b
    limit = (9, 5, 4, 6, 3, 8)[v]
    pairs = [(j,k) for j in range(1,limit+1) for k in range(10) if (j+k)%9 == 0]
    regular = 10 * limit
    answer = regular + len(pairs)
    assert answer == sum((2*j+2*k+c)%9 == 0 for j,k,c in product(range(1,limit+1),range(10),range(10)))
    assert str(palindrome) == str(palindrome)[::-1] and palindrome%11 == 0

    return Topic(
        (
            ("A palindrome reads the same from either end. Matching digits sit in paired places on either side of its centre.", "Mirror the digits about the centre."),
            ("A repunit is made entirely of ones. Place value lets us build a repeated digit with one multiplication.", "A repunit has a one in every place."),
        ),
        (
            ("In AMC Upper Primary practice, watch for numbers that read the same when reversed, or a long row of repeated digits.", "AMC Upper Primary · repeated digits"),
            ("In a Rossmoyne style puzzle, add a divisibility rule. Use the mirror structure to leave fewer free choices.", "Rossmoyne-style · add a divisibility clue"),
        ),
        (
            Example("Build a repeated digit", (
                (f"Take the repunit {say(ones)} and multiply by {say(multiplier)}. What number will you get?", f"{ones:,} × {multiplier}"),
                ("Picture multiplying each place separately. Look for any place that would need a carry.", "Can any column make a carry?"),
            ), (
                (f"Each one becomes a {say(multiplier)}. The product in every column is below ten, so no digit has to move into the next place.", f"Every 1 becomes {multiplier}"),
                (f"The answer is {say(repdigit)}. You can view it as one copy of that digit in every position.", f"{ones:,} × {multiplier} = {repdigit:,}"),
            ), tiles(*str(ones)), worked_art=tiles(*str(repdigit))),
            Example("Spot a factor in a palindrome", (
                (f"The four-digit number {say(palindrome)} reads the same both ways. Divide it by eleven.", f"{palindrome:,} ÷ 11"),
                ("Can you find the quotient by splitting the outer and inner pairs of digits?", "Separate the outside and inside digits."),
            ), (
                (f"The two outer copies of {say(a)} contribute {say(1001*a)}. The two inner copies of {say(b)} contribute {say(110*b)}.", f"{palindrome:,} = {a} × 1,001 + {b} × 110"),
                ("One thousand and one is eleven times ninety-one. One hundred and ten is eleven times ten. Both pairs share a factor of eleven.", "1,001 = 11 × 91  •  110 = 11 × 10"),
                (f"Now add ninety-one times {say(a)} and ten times {say(b)}. The quotient is {say(palindrome//11)}.", f"91 × {a} + 10 × {b} = {palindrome//11}"),
            ), tiles(a,b,b,a,highlight=(0,3))),
            Example("Count palindromes that pass a test", (
                (f"Count the five-digit palindromes divisible by nine whose first digit is at most {say(limit)}.", f"Five digits, first digit 1–{limit}"),
                ("The first and last digits match. So do the second and fourth. The centre can be any single digit allowed by the divisibility test.", "Five places: A, B, C, B, A"),
            ), (
                ("A five-digit palindrome is fixed once we choose its first two digits and the centre. Call them A, B and C. The digit sum is twice A plus twice B plus C.", "Digit sum = 2A + 2B + C"),
                ("For each outer pair choose C to make the sum a multiple of nine. There is always a choice from zero through eight, since those digits give all nine remainders.", f"{limit} × 10 = {regular} choices with C from 0 to 8"),
                ("Nine is a second choice precisely when zero already worked. That happens when A plus B is itself divisible by nine.", "C = 9 adds one case when 9 divides A + B."),
            ), tiles("A","B","C","B","A",highlight=(2,)), proof=(
                (f"The pair can sum to nine, with one partner from zero to eight for each allowed first digit." +
                 (" The pair nine and nine also sums to eighteen." if limit==9 else " A sum of eighteen is outside our permitted range."), f"Extra middle digits: {len(pairs)}"),
                (f"Add {say(regular)} and {say(len(pairs))}. The answer is {say(answer)}, with each number counted once by its three free positions.", f"{regular} + {len(pairs)} = {answer}"),
            ), proof_art=table(("A","Possible B"),*((x,y) for x,y in pairs[:4]),("…","…"))),
        ),
        (
            ("Starting with zero would give fewer than five written digits. Only the centre and the second digit may start from zero in this count.", "Allow zero in the first place", "First digit comes from 1–9"),
            ("When the required remainder is zero, both zero and nine work as centre digits. Test those two endpoints before you count.", "Forget the middle digit 9", "C = 0 and C = 9 have the same remainder"),
        ),
        (
            ("Write only the independent digits first. Use the mirror pairs to copy the other positions.", "Mark the free digits", "The last two digits are determined by the first two."),
            ("Use the divisibility test on the resulting digit sum. Check whether the residue allows two single digits.", "Test the centre", "Remainder zero can mean 0 or 9."),
        ), cover=tiles("A","B","C","B","A",highlight=(2,)),
    )


def cryptarithms(lesson):
    v=lesson.visit
    use_reverse=v%2==1
    digit=3+v
    ua,ub=((3,5),(3,6),(4,6),(3,7),(2,8))[v]
    total=2*(10*ua+ub)
    last=total%10
    assert ua!=last and total<100
    basic=Example("One letter, one digit", (
        (f"The same digit A is added to itself and the result is {say(2*digit)}. Which digit is A?", f"A + A = {2*digit}"),
        ("Keep both copies of A the same while you solve the number sentence.", "Repeated letters must match."),
    ), (
        ("The left side is twice the digit A. Dividing the whole result by two keeps the equality balanced.", f"2A = {2*digit}"),
        (f"Half of {say(2*digit)} is {say(digit)}. Substitute the digit in both places to check the original addition.", f"A = {digit}  •  {digit} + {digit} = {2*digit}"),
    ), tiles("A","A",2*digit,highlight=(0,1)))
    if use_reverse:
        left,right=(2+v//2,6+v//2)
        move=9*(right-left)
        summ=left+right
        medium=Example("Reverse two digits", (
            (f"A and B are distinct digits with sum {say(summ)}. Adding {say(move)} to the two-digit number A B reverses its digits.", f"AB + {move} = BA"),
            ("Both numbers have two digits. Which digits fit the sum and the reversal together?", f"A + B = {summ}"),
        ), (
            ("A B means ten A plus B. B A means ten B plus A. Subtract them. The difference is nine times B minus A, with the digit difference taken first.", "BA − AB = 9(B − A)"),
            (f"The difference in the two digits is four, because {say(move)} divided by nine is four. Subtract that from the given sum and split the remainder in half.", f"A + B = {summ}, B − A = 4"),
            (f"A is {say(left)} and B is {say(right)}. Check the two-digit numbers in the original order.", f"{10*left+right} + {move} = {10*right+left}"),
        ), tiles("AB","+ "+str(move),"BA"))
    else:
        medium=Example("Follow a carry", (
            (f"The two-digit number A {say(ub)} is added to itself. The answer has tens digit {say(total//10)} and units digit B.", f"A{ub} + A{ub} = {total//10}B"),
            ("A and B are distinct digits. Where does the carry come from and what are the two digits?", "Find A and B."),
        ), (
            (f"The units give {say(ub)} plus {say(ub)}, which is {say(2*ub)}. Write {say(last)} in the units and carry one ten.", f"B = {last}, with one ten carried"),
            (f"Now twice A plus one equals {say(total//10)}. Subtract one from the tens total, then halve it.", f"2A + 1 = {total//10}"),
            (f"A is {say(ua)} and B is {say(last)}. Adding the two finished numbers checks both columns.", f"{10*ua+ub} + {10*ua+ub} = {total}"),
        ), grid(("A",ub),("A",ub),(total//10,"B"),highlight=((0,1),(1,1))))
    values=[]
    for a,b,c,d in product(range(10),repeat=4):
        if a*b == 0 or len({a,b,c,d})!=4:
            continue
        if use_reverse:
            first, second, result = 10*a+b, 10*a+c, 100*b+10*d
        else:
            first, second, result = 10*a+b, 10*a+b, 100*b+10*c+d
        if first+second==result:
            values.append((first,second,result,a,b,c,d))
    small=v<2
    first,second,result,a,b,c,d=(min(values) if small else max(values))
    target="smallest" if small else "largest"
    if use_reverse:
        hard=Example("Use the hundreds and units clues", (
            ("A B plus A C gives B D zero. A, B, C and D are four distinct digits and A and B are nonzero.", "AB + AC = BD0"),
            (f"Find the {target} possible two-digit number A B. Start with the fact that a carry creates the hundreds digit.", f"Find the {target} possible AB."),
        ), (
            ("Adding two two-digit numbers can carry just one hundred. Therefore B is one.", "B = 1"),
            ("The units add to a number ending in zero. One plus C can only make ten, so C is nine and one ten carries.", "1 + C = 10, so C = 9"),
            ("The tens then give twice A plus one. It must reach ten, and the units of that calculation give D.", "2A + 1 = 10 + D"),
        ), grid(("A","B"),("A","C"),("B","D","0")), proof=(
            (("Try A equals five. It makes D one, already used by B. Six works."
              if small else "Nine is already used by C. Eight gives D seven, which is available.") +
             " The tens rule and distinct digits rule give the first allowable choice in the required order.", f"A = {a}, D = {d}"),
            (f"The required number is {say(first)}. Add {say(first)} and {say(second)} to verify the result {say(result)}.", f"{first} + {second} = {result}"),
        ), proof_art=tiles(first,second,result,highlight=(2,)))
    else:
        hard=Example("Force a leading digit before searching", (
            ("A B plus A B gives B C D. All four letters stand for distinct digits. The leading digits A and B are nonzero.", "AB + AB = BCD"),
            (f"Find the {target} such number A B. Use the carry into hundreds before you try possible tens digits.", f"Find the {target} possible AB."),
        ), (
            ("The largest possible sum of two two-digit numbers is below two hundred, so the hundreds digit B is one.", "B = 1"),
            ("Now the units are one plus one. That gives D equals two, with no carry into the tens.", "D = 2"),
            ("The tens double A and must reach ten. That means A is at least five. Check distinct digits as you choose A.", "A ≥ 5 and C = 2A − 10"),
        ), grid(("A","B"),("A","B"),("B","C","D")), proof=(
            ((f"Start at five. Five gives C equals zero, distinct from the other letters."
              if small else "Start at nine. Nine gives C equals eight, distinct from the other letters.") +
             " This endpoint of the possible tens digits already works.", f"A = {a}, C = {c}"),
            (f"So A B is {say(first)}. Its double is {say(result)}, with the required repeated digit at the front of the answer.", f"{first} + {second} = {result}"),
        ), proof_art=tiles(first,second,result,highlight=(2,)))
    if v == 4:
        choices=tuple(row[0] for row in values)
        hard=Example("Count every valid assignment", (
            ("A B plus A B gives B C D. A and B are nonzero, and all four letters represent different digits.", "AB + AB = BCD"),
            ("How many values of A B work? Sort the possible tens digits and examine the carries.", "Count all valid values of AB."),
        ), (
            ("The hundreds carry is one, so B is one. The units give two with no carry, so D is two.", "B = 1 and D = 2"),
            ("Twice A must produce a hundreds carry. A can be five through nine. The tens digit C is twice A minus ten.", "A = 5–9, C = 2A − 10"),
            ("For A equals six, C would equal two, repeating D. The other four candidates assign four different digits, and each addition checks.", "Exclude A = 6 because C = D = 2."),
        ), grid(("A","B"),("A","B"),("B","C","D")), proof=(
            (f"The surviving numbers are {spoken_list(choices)}. Every possible A has been tested, so no other value is missing.", f"Valid AB: {', '.join(map(str,choices))}"),
            ("Test any of the doubles in the original pattern. For example, doubling seventy-one gives one hundred and forty-two.", f"{len(choices)} solutions"),
        ), proof_art=tiles(*choices))
    return Topic(
        (
            ("In a cryptarithm, a letter stands for one digit wherever it appears. Different letters use different digits when the question says so.", "One letter keeps one value."),
            ("Work by place value. A carry is an extra clue linking one column to the next.", "Use carries to connect columns."),
        ),
        (
            ("An AMC number puzzle may replace digits with letters or boxes. Check whether repeated symbols are required to have the same value.", "AMC Upper Primary · missing digits"),
            ("In a Rossmoyne style puzzle, a leading digit or the size of the answer can cut down the possible carries first.", "Rossmoyne-style · use the answer size"),
        ),
        (basic,medium,hard),
        (
            ("Treat A B as a two-digit number. A is worth ten times as much in the tens place as it would be in the units.", "Read AB as A × B", "AB represents 10A + B"),
            ("Look for a leading zero and a repeated value assigned to different letters. Check every symbol after the arithmetic works.", "Check arithmetic only", "Check leading and distinct digits too"),
        ),
        (
            ("Write the columns and mark the possible carries. Use the very first digit of a three-digit sum to narrow your options.", "Use the strongest column", "Check the hundreds digit and then the units."),
            ("After solving, put each value back into the original expression. An equality and a legal assignment are both required.", "Substitute every digit", "Verify the sum and the digit rules."),
        ), cover=grid(("A","B"),("A","B"),("B","C","D")),
    )


def primes(lesson):
    v=lesson.visit
    n=(37,39,41,49)[v]
    trial=[p for p in (2,3,5,7,11,13) if p <= isqrt(n)]
    factor=next((p for p in trial if n%p==0),None)
    a,b=2+v%2,1+v//2
    m=(2**a)*(3**b)*5
    count=(a+1)*(b+1)*2
    p,q,r=(5,3,5,3)[v],(2,4,2,4)[v],(1,1,3,3)[v]
    hard_n=(2**p)*(3**q)*(7**r)
    least=2*7
    root=isqrt(hard_n*least)
    assert root**2==hard_n*least and all(isqrt(hard_n*k)**2 != hard_n*k for k in range(1,least))
    assert count == sum(m%d==0 for d in range(1,m+1))
    return Topic(
        (
            ("Prime numbers are the building blocks of multiplication. A prime has exactly two positive factors, one and itself.", "Primes have two positive factors."),
            ("Prime factorisation keeps a record of how often each prime appears. Read those counts as information about all the divisors.", "Factorisation records the prime powers."),
        ),
        (
            ("In AMC practice, factor clues may appear in a number search, a question about possible rectangles, or a problem about perfect squares.", "AMC Upper Primary · factor clues"),
            ("In Rossmoyne style reasoning, use prime powers to explain why your list is complete or why a proposed multiplier is smallest.", "Rossmoyne-style · justify every choice"),
        ),
        (
            Example("Test a candidate for primality", (
                (f"Is {say(n)} a prime number? Think about how far you need to look for a possible small factor.", f"Is {n} prime?"),
                ("A factor pair always has a member at or below the square root of the number.", "Check small prime divisors."),
            ), (
                (f"The prime divisors to test are {spoken_list(trial)}. If no prime this small divides, then there cannot be a larger factor pair either.", f"Try {', '.join(map(str,trial))}"),
                ((f"{say(factor)} times {say(n//factor)} is {say(n)}, so it is composite."
                  if factor else f"None divides {say(n)} evenly, so {say(n)} is prime.")+" The small-factor test decides the question.", f"{n} = {factor} × {n//factor}" if factor else f"{n} is prime."),
            ), tiles(*trial)),
            Example("Count factors without listing them", (
                (f"How many positive divisors does {say(m)} have? Its prime factors are just two, three and five.", f"Count the positive divisors of {m}."),
                ("Imagine choosing the number of copies of each prime in a divisor.", "Choose exponents independently."),
            ), (
                (f"The prime factorisation is two to the power {say(a)}, times three to the power {say(b)}, times five.", f"{m} = 2^{a} × 3^{b} × 5"),
                (f"There are {say(a+1)} choices for the exponent of two, {say(b+1)} for three and two for five. Zero copies is also a choice.", f"{a+1} choices  ×  {b+1} choices  ×  2 choices"),
                (f"Multiply the independent choices to get {say(count)} divisors. Different exponent choices make different products.", f"{a+1} × {b+1} × 2 = {count} divisors"),
            ), table(("Prime","2","3","5"),("Copies",f"0–{a}",f"0–{b}","0–1"))),
            Example("Make a perfect square", (
                (f"What is the smallest positive whole number that turns {say(hard_n)} into a perfect square when you multiply them?", f"Smallest m such that {hard_n:,} × m is a square"),
                (f"The factorisation uses two to the power {say(p)}, three to the power {say(q)} and seven to the power {say(r)}. Think in pairs of identical factors.", f"{hard_n:,} = 2^{p} × 3^{q} × 7^{r}"),
            ), (
                ("A square has even exponents, since the two identical factors each contribute the same number of every prime.", "Square exponents come in pairs."),
                (f"The exponents {say(p)} and {say(r)} are odd. Add one copy of two and one copy of seven. The exponent of three is already even.", f"Add one 2 and one 7."),
                ("Two times seven is fourteen. Both primes are required and adding any more would only make the multiplier larger.", "Smallest multiplier = 2 × 7 = 14"),
            ), table(("Prime",2,3,7),("Copies",p,q,r),highlight=((1,1),(1,3))), proof=(
                (f"With the extra primes the exponents become {spoken_list((p+1,q,r+1))}. Halve every exponent to get the factorisation of the square root.", f"New exponents: {p+1}, {q}, {r+1}"),
                (f"That square root is {say(root)}. Squaring it gives {say(root*root)}, which is exactly fourteen times the starting number.", f"{root:,}² = {root*root:,}"),
            ), proof_art=tiles(2**((p+1)//2),3**(q//2),7**((r+1)//2))),
        ),
        (
            ("One has only one positive factor, so keep it out of a prime factorisation. The empty choice of primes, however, does give the divisor one.", "Treat 1 as prime", "1 is a divisor from zero copies."),
            ("An exponent of three permits zero, one, two or three copies. Count all four choices when finding the number of divisors.", "Count three choices for exponent 3", "Count 0, 1, 2 and 3"),
        ),
        (
            ("Split a difficult factor into primes. Keep the copies of the same prime together.", "Write prime powers", "Group identical prime factors."),
            ("Match the task to the exponent rule. Use choices to count divisors, or even exponents to make a square.", "Use the right test", "Check the final product with the original factors."),
        ), cover=tiles(2,2,3,5),
    )


def multiples(lesson):
    v=lesson.visit
    first,second=(6+2*v,9+3*v)
    meet=lcm(first,second)
    red,blue=(24+12*v,36+12*v)
    groups=gcd(red,blue)
    scale=6+v
    shape=(30,42,70,66,105)[v]
    pairs=[(a,shape//a) for a in range(1,isqrt(shape)+1) if shape%a==0 and gcd(a,shape//a)==1]
    near,far=min(pairs,key=lambda pair:pair[1]-pair[0])
    minimum=(scale*near,scale*far)
    assert gcd(*minimum)==scale and lcm(*minimum)==scale*shape
    return Topic(
        (
            ("The highest common factor is the largest number that divides both quantities. The lowest common multiple is the first positive number they both divide into.", "HCF divides both. LCM is a multiple of both."),
            ("Listen for the job: equal grouping uses a common factor, and meeting schedules use a common multiple.", "Grouping and repeating have different tests."),
        ),
        (
            ("In AMC practice, identical packs or repeating events can signal a common factor or multiple. Write what each clue requires the answer to divide.", "AMC Upper Primary · groups or repeat times"),
            ("A Rossmoyne style problem can give the H C F and L C M as clues to find the original pair.", "Rossmoyne-style · reconstruct a number pair"),
        ),
        (
            Example("Find the first shared multiple", (
                (f"Two activities restart every {say(first)} minutes and every {say(second)} minutes. They start together at time zero.", f"Repeat every {first} and {second} minutes."),
                ("After the start, how many minutes until they first start together again?", "Find the first positive match."),
            ), (
                (f"The first schedule goes {spoken_list(range(first,meet+1,first))}. The second goes {spoken_list(range(second,meet+1,second))}.", f"List multiples up to {meet}."),
                (f"They first match at {say(meet)} minutes. That is the least positive number divisible by both periods.", f"LCM({first}, {second}) = {meet}"),
            ), table(("Period", "1st","2nd","3rd"),(first,first,2*first,3*first),
                         (second,second,2*second,3*second),highlight=((1,3),(2,2)))),
            Example("Make the greatest number of equal packs", (
                (f"A kit has {say(red)} red markers and {say(blue)} blue markers. Make as many identical packs as possible with none left over.", f"{red} red and {blue} blue markers"),
                ("How many packs can you make? Find a number of packs that divides both totals.", "Every pack gets the same colour counts."),
            ), (
                (f"The pack count divides both {say(red)} and {say(blue)}. It also divides their difference, which is {say(blue-red)}.", f"Common divisors also divide {blue} − {red} = {blue-red}."),
                (f"Both totals are multiples of {say(groups)}. Since the difference is {say(groups)}, no larger count can divide both.", f"HCF({red}, {blue}) = {groups}"),
                (f"Make {say(groups)} packs. Each contains {say(red//groups)} reds and {say(blue//groups)} blues.", f"{groups} packs of {red//groups} red and {blue//groups} blue"),
            ), bars(("Red",((red,red),)),("Blue",((red,red),(blue-red,blue-red))))),
            Example("Reconstruct a pair from its HCF and LCM", (
                (f"Two positive integers have highest common factor {say(scale)} and lowest common multiple {say(scale*shape)}.", f"HCF = {scale}  •  LCM = {scale*shape}"),
                ("Find the pair whose difference is as small as possible. Start by dividing each number by their common factor.", "Find the pair with the smallest gap."),
            ), (
                (f"Divide both by {say(scale)}. The new pair is coprime, meaning it shares no prime factors. Its lowest common multiple is {say(shape)}.", f"After scaling: HCF = 1, LCM = {shape}"),
                (f"Coprime numbers have lowest common multiple equal to their product, so the two scaled values multiply to {say(shape)}. List the factor pairs.", f"A × B = {shape}, with HCF(A,B) = 1"),
                (f"The closest legal scaled pair is {say(near)} and {say(far)}. Their difference is {say(far-near)}, smaller than that of the other pairs.", f"Closest scaled pair: {near}, {far}"),
            ), tiles(scale,scale*shape), worked_art=table(("A","B"),*pairs), proof=(
                (f"Scale by {say(scale)} to recover {say(minimum[0])} and {say(minimum[1])}. Their gap is {say(minimum[1]-minimum[0])}. Multiplying all gaps by the same positive number keeps their order.", f"Original pair: {minimum[0]}, {minimum[1]}"),
                (f"Their common factor is {say(scale)}, and their least common multiple is {say(scale*shape)}. These are the two original clues.", f"Check both: {scale} and {scale*shape}"),
            ), proof_art=tiles(*minimum)),
        ),
        (
            ("The answer to an equal packing problem divides the totals. A repeat time has to be a multiple of both periods.", "Use the LCM for the number of packs", "The pack count is a common factor"),
            ("After scaling by the full common factor, make sure the residual pair is coprime. A shared prime would make the common factor larger.", "Use any factor pair after scaling", "Reject pairs sharing a prime"),
        ),
        (
            ("Write what has to divide what. Find the factor or multiple that satisfies that direction.", "Choose HCF or LCM", "Check the divisibility direction."),
            ("For an unknown pair, remove the greatest common factor first. Multiply back and verify both conditions.", "Scale, solve, and check", "A coprime pair has product equal to its LCM."),
        ), cover=tiles("HCF","LCM"),
    )


def divisibility(lesson):
    v=lesson.visit
    first,second=((4,6),(5,8),(6,9),(9,12),(6,14),(8,10),(12,15))[v-1]
    step=lcm(first,second)
    low,high=49+7*v,200+11*v
    shifted=tuple(n for n in range(low+1,high+2) if n%step==0)
    solutions=tuple(n-1 for n in shifted)
    assert solutions == tuple(n for n in range(low,high+1) if n%first==first-1 and n%second==second-1)
    groups,base,extra=6+v,4+v,1+v%3
    n=groups*base+extra
    h,t=2+v, 2+2*v%8
    digit=next(d for d in (0,4,8) if (h+t+d)%3==0)
    number=100*h+10*t+digit
    assert number%12==0 and all((100*h+10*t+d)%12!=0 for d in range(10) if d!=digit)
    return Topic(
        (
            ("A remainder measures how far a number is past a multiple. A remainder just one below the divisor tells you the number is one step before the next multiple.", "Remainder one below the divisor → add one."),
            ("That one step can turn several awkward remainders into a single common multiples problem.", "Work with the next multiple instead."),
        ),
        (
            ("In AMC practice, read almost full groups and one short of a multiple as clues about a remainder.", "AMC Upper Primary · translate the wording"),
            ("In a Rossmoyne style search, combine more than one remainder and use the interval to finish the argument.", "Rossmoyne-style · combine the conditions"),
        ),
        (
            Example("Locate the leftover amount", (
                (f"Group {say(n)} counters into packets of {say(base)}. How many counters remain outside full packets?", f"{n} counters in groups of {base}"),
                ("Identify the last multiple of the packet size that fits. Then count the ungrouped counters.", "Find the last complete group."),
            ), (
                (f"{say(groups)} packets use {say(groups*base)} counters. The next packet would bring the used total above {say(n)}.", f"{groups} × {base} = {groups*base}"),
                (f"Subtract to get {say(extra)}. The leftover amount is less than the group size, as a valid remainder must be.", f"{n} = {groups} × {base} + {extra}"),
            ), chain(groups*base,n)),
            Example("Use two divisibility rules", (
                (f"Find the last digit of the three-digit number beginning with {say(h)} and {say(t)} if the number is divisible by four and three.", f"{h}{t}□ must be divisible by 4 and 3."),
                ("Use the last two digits for one test and the digit sum for the other.", "Which last digit passes both?"),
            ), (
                (f"The possible endings divisible by four are {spoken_list((10*t,10*t+4,10*t+8))}, so the last digit is zero, four or eight.", f"Possible final digits: 0, 4, 8"),
                (f"The fixed digits sum to {say(h+t)}. Of those three last digits, only {say(digit)} makes a multiple of three.", f"{h} + {t} + {digit} = {h+t+digit}"),
                (f"The number is {say(number)}. Its ending and its digit sum pass the two requested tests.", f"{number} is divisible by both 4 and 3."),
            ), tiles(h,t,"□"), worked_art=tiles(0,4,8,highlight=((0,4,8).index(digit),))),
            Example("Turn two remainders into common multiples", (
                (f"Count the numbers from {say(low)} through {say(high)} whose remainder is {say(first-1)} on division by {say(first)}.", f"{low}–{high} inclusive, remainder {first-1} ÷ {first}"),
                (f"The same numbers must give remainder {say(second-1)} on division by {say(second)}. What happens to both remainders if you add one?", f"Also remainder {second-1} ÷ {second}"),
            ), (
                (f"Adding one to N makes it divisible by {say(first)} and {say(second)}. Their least common multiple is {say(step)}.", f"N + 1 is a multiple of {step}."),
                (f"The shifted interval starts at {say(low+1)} and ends at {say(high+1)}. Find the first and last multiples of {say(step)} in that interval.", f"Shift both endpoints: {low+1}–{high+1}"),
                (f"They start at {say(shifted[0])} and finish at {say(shifted[-1])}. Step by {say(step)}, including both ends.", f"{shifted[0]}, {shifted[0]+step}, …, {shifted[-1]}"),
            ), tiles(first-1,first,second-1,second), worked_art=chain(low, low+1, shifted[0]), proof=(
                (f"There are {say((shifted[-1]-shifted[0])//step)} steps between the endpoints. Include the first multiple to get {say(len(solutions))} numbers.", f"({shifted[-1]} − {shifted[0]}) ÷ {step} + 1 = {len(solutions)}"),
                (f"Subtract one from each multiple to recover the original numbers. For example, the first is {say(solutions[0])} and gives both required remainders.", f"First original match: {solutions[0]}"),
            ), proof_art=tiles(*solutions[:8])),
        ),
        (
            ("A remainder can be zero, but it must always be smaller than the divisor. Once there are enough leftovers for a complete group, make that group.", "Leave a full packet as a remainder", "Remainder < divisor"),
            ("When you shift the number in a bounded search, shift the endpoints by the same amount. Pull each answer back to the original interval.", "Keep the old bounds for N + 1", "Shift the whole interval"),
        ),
        (
            ("Name the divisor and the remainder together. Check whether adding or subtracting a small amount lands on a multiple.", "Look for a nearby multiple", "A one-step shift may simplify two clues."),
            ("Check the first and last values against every condition. If you counted gaps, include the first valid value.", "Check the bounds and remainders", "Count values, including legal endpoints."),
        ), cover=chain(f"{first-1} left","+1",f"multiple of {first}"),
    )


def parity(lesson):
    v=lesson.visit
    first, second=13+2*v,18+2*v
    if v%2 == 0:
        values=(3+v,7+v,9+v,14+v,19+v)
        combined=sum(values)+len(values)-1
        hard=Example("Track the effect of every merge", (
            (f"Start with the numbers {spoken_list(values)}. A move replaces any two numbers by their sum plus one.", "Merge a and b into a + b + 1."),
            ("Keep going until only one number remains. Is that final number odd or even? Does the choice of partners matter?", "What is the final parity?"),
        ), (
            (f"The original sum is {say(sum(values))}. Replacing two entries by their sum plus one adds exactly one to the total, whatever pair you choose.", f"Starting total = {sum(values)}  •  each move adds 1"),
            ("Every move decreases the number of entries by one. Five entries need exactly four moves to make a single entry.", "5 → 4 → 3 → 2 → 1"),
            (f"Add four to the original total. The last number is {say(combined)}, so it is {'odd' if combined%2 else 'even'} regardless of how you merge.", f"{sum(values)} + 4 = {combined} ({'odd' if combined%2 else 'even'})"),
        ), tiles(*values), worked_art=chain(5,4,3,2,1), proof=(
            ("Check by merging from left to right. Then think about swapping the first pair. The order changes the intermediate values, but each move adds one to the total.", "Changing the order keeps the same total change."),
            ("In a longer version, a list of n entries takes n minus one moves. This lets you answer even when drawing every move would take too long.", "Final total = starting total + (n − 1)"),
        ), proof_art=tiles(sum(values),"+4",combined))
    else:
        size=4+2*(v//2)
        same=(0,0),(size-1,size-1)
        rows=[["□" if (i+j)%2==0 else "■" for j in range(size)] for i in range(size)]
        rows[0][0]=rows[-1][-1]="×"
        hard=Example("Use parity as a colouring argument", (
            (f"A {say(size)} by {say(size)} square grid has its top left and bottom right corners removed.", f"{size} × {size} grid, remove opposite corners."),
            ("Can you cover every remaining square with dominoes, each covering two adjacent squares? No overlap is allowed.", "Can dominoes tile the rest?"),
        ), (
            ("Colour the grid like a chessboard. A domino always covers one square of each colour, because adjacent squares have opposite colours.", "Every domino covers one of each colour."),
            (f"The grid began with {say(size*size//2)} squares of each colour. The opposite corners in this even-sized grid have the same colour.", f"Initially {size*size//2} of each."),
            (f"Removing both corners gives {say(size*size//2-2)} of one colour and {say(size*size//2)} of the other. Dominoes cannot balance these counts.", f"{size*size//2-2} versus {size*size//2} → impossible"),
        ), grid(*rows,highlight=same), proof=(
            ("There are an even number of remaining cells, so a total cell count alone would allow a whole number of dominoes.", f"{size*size-2} cells is even."),
            ("The stronger test is the split by colouring. Rotating a domino does not change its need for one square of each colour.", "The counts by colour decide the puzzle."),
        ), proof_art=bars(("First colour",((size*size//2-2,size*size//2-2),)),("Second colour",((size*size//2,size*size//2),))))
    return Topic(
        (
            ("Parity tells us whether a whole number is odd or even. Think of an even number as pairs, and an odd number as pairs with one left over.", "Even = pairs. Odd = pairs plus one."),
            ("Look for a move or arrangement that must preserve parity. One quick check can rule out a long search.", "Track what happens to the extra one."),
        ),
        (
            ("AMC practice may hide odd and even structure in jumps, paired objects, or a game where each move changes some pieces.", "AMC Upper Primary · recognise pairs"),
            ("A Rossmoyne style proof can use parity or a two-colour pattern to explain why a proposed arrangement is impossible.", "Rossmoyne-style · use an invariant"),
        ),
        (
            Example("Decide parity from the parts", (
                (f"Is the sum of {say(first)} and {say(second)} odd or even? Try to decide by pairing.", f"{first} + {second}"),
                ("Think about how many unpaired counters each addend would have.", "Combine complete pairs and the leftovers."),
            ), (
                (f"{say(first)} has one extra counter after pairing. {say(second)} is fully paired, so it contributes no extra counter.", "Odd contributes 1. Even contributes 0."),
                (f"The total has one extra and is odd. The exact sum is {say(first+second)}, which confirms the pairing argument.", f"{first+second} is odd."),
            ), tiles(first,second)),
            Example("Follow a rule that preserves parity", (
                (f"A counter starts at {say(first)} on a number line. Each move adds or subtracts an even number of steps.", f"Start at {first}. Make even jumps."),
                (f"Can it ever reach {say(second)}? The length and direction may change on each move.", f"Can it land on {second}?"),
            ), (
                ("Adding an even number is adding entire pairs. Subtracting an even number also removes entire pairs. Neither change affects the leftover one.", "An even jump keeps the same parity."),
                (f"The counter starts at odd {say(first)}, and every later position must remain odd. The target {say(second)} is even, so it is unreachable.", f"{first} is odd. {second} is even."),
            ), chain(first,first+2,first+4,first+6)),
            hard,
        ),
        (
            ("Try a parity question before calculating a big total. Label each value odd or even and see how the labels combine.", "Do all the arithmetic", "Track odd and even first"),
            ("A matching parity does not prove that every move is allowed. Use a construction as well whenever the question asks what can be achieved.", "Use matching parity as proof of reachability", "Show a valid construction too"),
        ),
        (
            ("Mark what one move does to parity. Decide whether the leftover changes, stays fixed, or follows a pattern.", "Analyse one move", "Identify exactly what is preserved."),
            ("Check whether the target has the required parity or colour balance. Write one sentence explaining why every legal move obeys that rule.", "Explain the obstruction", "Show why all cases obey the same test."),
        ), cover=tiles("pair","pair","+1",highlight=(2,)),
    )


def cycles(lesson):
    v=lesson.visit
    start=9+2*v
    hours=17+7*v
    finish=(start+hours-1)%12+1
    base=(3,7)[v]
    length=(37,64)[v]
    count=(51,63)[v]
    cycle=tuple(pow(base,j,10) for j in range(1,5))
    single=pow(base,length,10)
    blocks, tail=divmod(count,4)
    total=blocks*sum(cycle)+sum(cycle[:tail])
    assert total%10==sum(pow(base,n,10) for n in range(1,count+1))%10
    edge=length%4 or 4
    return Topic(
        (
            ("A cycle brings the same states back in the same order. Track where a full cycle ends and how many extra steps you take.", "Full cycles + a short tail"),
            ("When all you need is a last digit, you can multiply last digits and leave the rest of the number behind.", "Keep the last digit at each step."),
        ),
        (
            ("AMC Upper Primary practice can use a repeating picture, a clock or the last digit of a large power. Write a small first cycle.", "AMC Upper Primary · spot repeating states"),
            ("A Mawa style investigation can change the base or the number of steps. Check whether the cycle length stays the same.", "MAWA-style · vary the rule"),
        ),
        (
            Example("Move around a twelve-hour clock", (
                (f"It is {say(start)} o'clock on a twelve-hour clock. What number will the hour hand point to after {say(hours)} hours?", f"{start}:00 + {hours} hours"),
                ("Start by removing any whole turns that bring you back to the same place.", "How many hours remain after a full turn?"),
            ), (
                (f"Every twelve hours returns to the starting number. The {say(hours)} hours leave {say(hours%12)} extra hours after full turns.", f"{hours} leaves a remainder of {hours%12} on division by 12."),
                (f"Step {say(hours%12)} hours ahead. Wrap past twelve if needed, so the hour hand points to {say(finish)}.", f"The hour hand points to {finish}."),
            ), chain(start,"+ "+str(hours%12),finish)),
            Example("Find the last digit of a large power", (
                (f"What is the units digit of {say(base)} to the power {say(length)}? Work with just the units digits of its first few powers.", f"Units digit of {base}^{length}"),
                ("Watch for the first repeat. A remainder of zero will need a careful interpretation.", "Write one complete cycle."),
            ), (
                (f"The first four units digits are {spoken_list(cycle)}. The next digit repeats the first, and the same multiplication rule gives the same later digits.", "Cycle: " + " → ".join(map(str,cycle))),
                (f"The exponent {say(length)} leaves a remainder of {say(length%4)} on division by four. Use position {say(edge)} in the cycle.", f"Cycle position = {edge}"),
                (f"The digit at that position is {say(single)}. If the remainder is zero, the fourth position sits at the end of the last full cycle.", f"Units digit = {single}"),
            ), tiles(*cycle,highlight=(edge-1,))),
            Example("Find the units digit of a sum of powers", (
                (f"Add the first {say(count)} positive powers of {say(base)}, starting with exponent one. What is the units digit of the sum?", f"{base}¹ + {base}² + … + {base}^{count}"),
                ("You already know the cycle of the last digits. Work out what one whole block contributes to the sum.", "Use the sum of a full four-term cycle."),
            ), (
                (f"One full cycle has units digits {spoken_list(cycle)}. Their sum is {say(sum(cycle))}, with units digit zero.", " + ".join(map(str,cycle))+f" = {sum(cycle)}"),
                (f"There are {say(blocks)} full cycles and {say(tail)} terms left. Every completed block contributes zero to the units digit.", f"{count} = {blocks} × 4 + {tail}"),
                (f"Add the first {say(tail)} digits of the cycle. Their sum is {say(sum(cycle[:tail]))}, so the final units digit is {say(total%10)}.", f"Tail sum: {' + '.join(map(str,cycle[:tail]))} = {sum(cycle[:tail])}"),
            ), chain(*cycle), proof=(
                ("The units digit of a sum depends only on the units digits of the addends. Tens contributed by any full cycle cannot change it.", "Discard whole tens, keep the remainder."),
                (f"The answer is {say(total%10)}. Check that the tail starts at exponent one of a new cycle, because the last completed block ended at a multiple of four.", f"Units digit = {total%10}"),
            ), proof_art=tiles(*cycle[:tail],highlight=tuple(range(tail)))),
        ),
        (
            ("If the step count is a multiple of the cycle length, land on the last listed item when the cycle was numbered from one.", "Treat remainder 0 as item 1", "Use the last item of a one-based cycle"),
            ("For a sum, add the contributions of the earlier terms as well as the final term. Check the total contributed by each full cycle.", "Use only the final term", "Separate complete blocks and the tail"),
        ),
        (
            ("Record states in order. Find the first state you can recognise again, and count the length from one occurrence to the next.", "Write one cycle", "Check where your numbering begins."),
            ("Divide by the cycle length and use the remainder. When the task asks for a sum, work out what the full cycles contribute.", "Reduce, then interpret", "Keep the tail in its original order."),
        ), cover=chain(*cycle),
    )


def arithmetic_sequence(lesson):
    v=lesson.visit
    a,d=4+v,3+v%3
    terms=[a+i*d for i in range(4)]
    index=14+3*v
    answer=a+(index-1)*d
    count=12+2*v
    last=a+(count-1)*d
    total=count*(a+last)//2
    assert total==sum(a+i*d for i in range(count))
    return Topic(
        (("In an arithmetic sequence each new term adds the same difference. The term number counts entries, but the changes happen in the gaps between entries.", "Term n is n−1 jumps from the start."),
         ("For a total of several terms, pair values from the two ends. Their sums are equal.", "Pair first with last, then second with second-last.")),
        (("AMC practice can hide a fixed increment in a seating plan, a stack or a pattern of growing figures. Check whether the differences are constant.", "AMC Upper Primary · find the common difference"),
         ("A Rossmoyne style question may need a total without listing every term. Pairing gives a short calculation and a reason.", "Rossmoyne-style · sum the pattern")),
        (
            Example("Build the first few terms", (
                (f"A list starts at {say(a)} and increases by {say(d)} each time. What are the first four terms?", f"Start {a}, add {d} each time."),
                ("Count the starting number as the first term.", "How many jumps reach the fourth term?")),
                ((f"Add {say(d)} three times after the starting value. That produces {spoken_list(terms)}.", " → ".join(map(str,terms))),
                 ("There are four terms but only three gaps. The fixed step is the size of each gap.", "Four terms → three jumps")), chain(a,f"+{d}","…")),
            Example("Jump to a distant position", (
                (f"A sequence has first term {say(a)} and common difference {say(d)}. What is term {say(index)}?", f"Find term {index}."),
                ("Work out how many gaps separate that term from the first.", f"Use the start and the repeated step.")),
                ((f"Term {say(index)} is {say(index-1)} steps beyond term one. The total increase is that number of steps times {say(d)}.", f"{index-1} × {d} = {(index-1)*d}"),
                 (f"Add the first term. The requested term is {say(answer)}. Check the rule would give {say(a)} at term one.", f"{a} + {index-1} × {d} = {answer}")), chain("Term 1",f"{index-1} jumps",f"Term {index}")),
            Example("Pair opposite ends to sum a growing pattern", (
                (f"A theatre section starts with {say(a)} seats in its first row. Each new row contains {say(d)} more than the row before it.", f"First row {a}. Each next row adds {d} seats."),
                (f"There are {say(count)} rows. Find the total number of seats.", f"Total for {count} rows?")),
                ((f"The last row contains {say(last)}, after {say(count-1)} increases. Pair the first row with the last.", f"Last row: {a} + ({count}−1) × {d} = {last}"),
                 (f"Every pair totals {say(a+last)}. Moving inward adds {say(d)} to one end and removes {say(d)} from the other.", f"Each pair = {a} + {last} = {a+last}"),
                 (f"There are {say(count//2)} pairs. Multiply by the common pair total to get {say(total)} seats.", f"{count//2} × {a+last} = {total} seats")),
                tiles(a,a+d,a+2*d,"…",last-d,last,highlight=(0,5)),proof=(
                    ("A check is to imagine the rows redistributed evenly. The mean of the first and last values is the mean row length.", f"Mean row length = ({a}+{last})/2"),
                    (f"Multiplying that mean by all {say(count)} rows gives the same total, {say(total)} seats.", f"{count} × ({a}+{last})/2 = {total}"))),
        ),
        (("The starting value occupies term one. A later position needs one fewer step than its term number.", "Use n jumps to find term n", "Use n−1 jumps"),
         ("If the step changes, arithmetic-sequence formulas no longer apply. Check the first few differences before summing.", "Use the same formula for any growing list", "Check the fixed difference")),
        (("Write the first term and common difference. For a particular term, count the gaps before multiplying.", "Record start and step", "Translate term number into jumps."),
         ("For a sum, check the last term and whether there is an unpaired centre. Pair opposite ends to verify the total.", "Pair the ends", "The downward change cancels the upward one.")),
        cover=chain(*terms),
    )


def doubling(lesson):
    v=lesson.visit
    first,start=2+v,3+v
    days=4+v
    last=first*2**(days-1)
    length=5+v
    series=2**length-1
    target=start*(2**(length+1)-1)+start*(2**(length-1))
    allowed=length+1
    spent=start*(2**allowed-1)
    left=target-spent
    assert spent<=target<start*(2**(allowed+1)-1)
    return Topic(
        (("A doubling pattern multiplies the current amount by two each time. Compare it with adding a fixed amount: its increases get larger as the terms grow.", "Each new amount is twice the previous one."),
         ("To sum a doubling sequence, double the whole sum and align the common terms. Subtract to leave only the two ends.", "Double the sum, align, subtract.")),
        (("An AMC problem may use objects that double each day or a prize that grows by a fixed multiplier. Mark whether it asks for one term or a total.", "AMC Upper Primary · term or total?"),
         ("In a Mawa style investigation, compare the total with the next term. Changing the starting number scales both.", "MAWA-style · generalise the sum")),
        (
            Example("Track a doubling amount", (
                (f"A display begins with {say(first)} lights on day one. The number doubles each day. How many are on at day {say(days)}?", f"Day 1: {first}. Double each day. Find day {days}."),
                ("Count how many doublings happen after the first day.", "Day 1 already has a value.")),
                ((f"There are {say(days-1)} doublings. Each one multiplies the current number by two, so use that power of two.", f"{days-1} doublings → multiply by 2^{days-1}"),
                 (f"Multiply the starting amount by that power. Day {say(days)} has {say(last)} lights.", f"{first} × 2^{days-1} = {last}")), chain(first,2*first,4*first,"…",last)),
            Example("Sum doubling terms by matching them", (
                (f"Find the sum of the first {say(length)} terms of the sequence one, two, four, eight and so on.", f"S = 1 + 2 + 4 + … + {2**(length-1)}"),
                ("What stays after you double the sum and subtract the original?", "Align S and 2S.")),
                ((f"Let the whole sum be S. Doubling every term begins at two and ends at {say(2**length)}.", f"2S = 2 + 4 + … + {2**length}"),
                 ("Subtract S. Every term shared by the two rows cancels. Only the last term of the doubled row and the first term of the original remain.", "2S − S = last doubled term − 1"),
                 (f"So the sum is {say(2**length)} minus one, or {say(series)}.", f"S = {2**length} − 1 = {series}")), table(("S","1","2","4","…",2**(length-1)),("2S","","2","4","…",2**length))),
            Example("Check how long a doubling budget lasts", (
                (f"A project uses {say(start)} tokens on day one. Each day's requirement doubles. There are {say(target)} tokens in the whole budget.", f"Day 1 uses {start}; double daily. Budget {target}."),
                ("How many complete days can it run? A day counts only if all of its tokens are available.", "Find the greatest affordable number of days.")),
                ((f"The total through day n is {say(start)} times two to the power n minus one, with the minus one inside the multiplier.", f"After n days: {start}(2ⁿ − 1)"),
                 (f"The total for {say(allowed)} days is {say(spent)}, which fits the budget. The next total would be {say(start*(2**(allowed+1)-1))}.", f"{allowed} days: {spent}. {allowed+1} days: {start*(2**(allowed+1)-1)}."),
                 (f"The next total is over budget, so there are {say(allowed)} complete days. The unused balance is {say(left)} tokens.", f"{allowed} days, with {left} tokens left.")),
                chain(start,start*2,start*4,"…","Budget"),proof=(
                    (f"After day {say(allowed)}, the amount needed for the next single day is {say(start*2**allowed)} tokens. It exceeds the balance.", f"Next day costs {start*2**allowed} > {left}."),
                    ("Every additional day uses positive tokens, so no later stopping point can be cheaper. The two consecutive totals prove the bound.", "One affordable day count, then the next is too expensive."))),
        ),
        (("The value on a day and the amount used across all days are different quantities. Check whether the problem says on or through.", "Use the last term as the running total", "Add all elapsed terms"),
         ("Keep the first term when indexing the powers. There are zero doublings at the start.", "Power n gives the day n value", "Day n has n−1 doublings")),
        (("Find the first term and the repeated multiplier. Mark whether you are calculating a term or a sum.", "Choose term or sum", "Check the first one or two values."),
         ("For a budget limit, show the last affordable total and the next one. They prove where you must stop.", "Verify both sides of the boundary", "Check consecutive totals.")),
        cover=chain(1,2,4,8,16),
    )


def finite_state(lesson):
    v=lesson.visit
    past=11+5*v
    finish=("North","East","South","West")[past%4]
    order=(2+v%2,3+v)
    period=lcm(*order)
    states=tuple(range(1,7+v%3))
    stem=1+v%3
    total=51+7*v
    loop=states[stem:]
    state=loop[(total-stem)%len(loop)]
    mapping=dict(zip(states,(*states[1:],states[stem])))
    direct=states[0]
    for _ in range(total):
        direct=mapping[direct]
    assert direct==state
    return Topic(
        (("A finite-state rule has only a limited set of possible situations. Once the same full state occurs again, the same rule repeats everything that follows.", "Same full state + same rule → same future."),
         ("Sometimes there is a short starting path before a loop. Count that path separately from the repeating part.", "Separate the lead-in and the loop.")),
        (("In AMC practice, a repeating transformation might turn a pointer, change a colour or move a mark. Record the complete state between steps.", "AMC Upper Primary · track a state"),
         ("A Mawa style investigation can compare loops from different starting states. Ask which states repeat and which appear only once.", "MAWA-style · inspect the lead-in")),
        (
            Example("Turn a pointer by whole quarter turns", (
                (f"A pointer begins facing north. Turn it clockwise by a quarter turn {say(past)} times. Where does it point?", f"North at start. Turn clockwise {past} times."),
                ("Count how many quarter turns bring it back to north.", "Remove complete revolutions.")),
                ((f"Four turns make one complete revolution. Dividing {say(past)} by four leaves {say(past%4)} extra turns.", f"{past} leaves remainder {past%4} when divided by 4."),
                 (f"Apply those extra turns from north. The pointer ends facing {finish.lower()}.", f"Final direction: {finish}")), chain("N","E","S","W","N")),
            Example("Wait for two settings to reset together", (
                (f"On each press, one dial moves to its next position in a cycle of {say(order[0])}. A second dial moves in a cycle of {say(order[1])}.", f"Two dials: cycles of {order[0]} and {order[1]}."),
                ("After how many presses is the full starting pair first restored?", "Both dial positions must return.")),
                ((f"The first dial resets at multiples of {say(order[0])}, and the second at multiples of {say(order[1])}.", "Match their reset steps."),
                 (f"The first positive common reset occurs after {say(period)} presses. The state consists of both dials, not just one.", f"Full period = LCM({order[0]}, {order[1]}) = {period}")), tiles(*order,period)),
            Example("Find a late state after a lead-in", (
                (f"A machine starts at state one. It moves up through the numbered states until {say(states[-1])}. From there its next state is {say(states[stem])}, and it follows the same rule forever.", f"1 → 2 → … → {states[-1]} → {states[stem]}"),
                (f"The starting state is at step zero. Where is it after {say(total)} moves?", f"Find state at step {total}.")),
                ((f"At step {say(stem)} the machine first reaches {say(loop[0])}, the first state of the loop. The earlier states do not recur.", f"Lead-in: {stem} moves"),
                 (f"The loop has {say(len(loop))} states. From the loop entry, there are {say(total-stem)} more moves to make.", f"Remaining loop moves: {total} − {stem}"),
                 (f"Divide by the loop length. The remainder is {say((total-stem)%len(loop))}. Move that far from the first loop state to reach {say(state)}.", f"Remainder {(total-stem)%len(loop)} → state {state}")),
                chain(*states,"↩ "+str(states[stem])),worked_art=chain(*loop),proof=(
                    ("When counting from the entry time, a remainder of zero means no extra move. That puts the machine at the entry state again.", "Index the entry state at offset zero."),
                    (f"The last state in the loop points back to {say(loop[0])}, so the calculation never returns to the earlier lead-in states.", "Check the arrow that closes the loop."))),
        ),
        (("A displayed position may not capture the full situation. Include any second dial or change in the rule that affects the next move.", "Match one visible detail", "Match the full state"),
         ("The lead-in happens only once. Subtract its length before dividing by the size of the loop.", "Use the loop from step zero automatically", "Find where the loop really begins")),
        (("List the first few complete states and name the next-step rule. Stop when a full state repeats.", "Find the first repeat", "Record the two occurrences as step numbers."),
         ("Separate the first visit to the loop from later laps. Check whether your indexing is by moves from zero or by states from one.", "Count the remaining moves", "Use the loop remainder from the correct entry.")),
        cover=chain("Start","Entry","Loop","Entry"),
    )
