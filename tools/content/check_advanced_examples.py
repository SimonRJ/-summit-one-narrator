"""Check the worked mathematics and transfer problems for all 52 optional techniques."""
import json
from fractions import Fraction as F
from itertools import combinations, permutations, product
from math import comb, isqrt
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
cards = {}
for group in ['number', 'counting', 'geometry']:
    source = (ROOT / f'advanced-{group}.js').read_text().split(' = ', 1)[1].strip().removesuffix(';')
    cards.update({row[0]: row for row in json.loads(source)})
checked = set()


def check(skill, maths, text):
    assert skill not in checked and maths, skill
    assert text in cards[skill][7], (skill, text)
    checked.add(skill)


check('DIG-01', 998 * 1002 == 999996 and 49 * 51 - 48 * 52 == 3, 'larger by 3')
digits = [str(n) for n in range(1000, 10000, 5) if set(str(n)) <= set('012345') and len(set(str(n))) == 4]
check('DIG-02', len(digits) == 108 and sum('0' in n for n in digits) == 84, 'giving 84')
sevens = lambda n: sum(str(i).count('7') for i in range(1, n + 1))
check('DIG-03', sevens(999) == 300 and sevens(275) == 53, '= 53')
check('DIG-04', 111111 % 11 == 0 and [i for i in range(10) if (6048 + 100*i) % 11 == 0] == [2], 'digit is 2')
pairs = list(permutations(range(1,10), 2))
check('DIG-05', sum(10*a+b+10*b+a == 99 for a,b in pairs) == 8 and
      [101*a+10*b for a,b in pairs if a+b == 11 and 101*a+10*b-(101*b+10*a) == 273] == [747], '747 − 474 = 273')
divisors = [d for d in range(1, 361) if 360 % d == 0]
check('DIV-01', len(divisors) == 24 and sum(d%2 == 0 for d in divisors) == 18 and
      [d for d in divisors if isqrt(d)**2 == d] == [1,4,9,36], '1, 4, 9 and 36')
check('DIV-02', sum(t%12 == t%18 == 0 for t in range(1,181)) == 5 and
      [t for t in range(6,101,18) if t%12 == 0] == [24,60,96], '24, 60 and 96')
remainders = [n for n in range(1,200) if n%5 == 2 and n%3 == 1]
check('DIV-03', remainders[0] == 7 and [n for n in remainders if n>100 and n%4 == 0] == [112,172], '112 and 172')
def colours(n, removed):
    board = [(x+y)%2 for x,y in product(range(n), repeat=2) if (x,y) not in removed]
    return sorted([board.count(0), board.count(1)])
check('DIV-04', colours(8,{(0,0),(7,7)}) == [30,32] and colours(5,{(1,0)}) == [11,13], '13 black and 11 white')
check('DIV-05', pow(7,2027,10) == 3 and (pow(7,2027,10)+pow(7,2028,10))%10 == 4, 'ends in 4')
check('FRAC-01', F(2,3)*F(3,4) == F(1,2) and 36*F(2,3)*F(3,4) == 18, '36 litres')
check('FRAC-02', F(3,5)**2 == F(9,25) and F(13,10)**2 == F(169,100), '30%')
check('FRAC-03', F(17,29)<F(10,17)<F(23,39) and F(40,68)==F(10,17), '10/17')
check('FRAC-04', F(10*60+20*80,30) == F(220,3) and (10*60+20*80+2*100) == 32*75, 'mean is 100')
check('RATE-01', F(72*1000,3600)==20 and F(120+180,20)==15, '15 seconds')
check('RATE-02', 1/(F(1,6)+F(1,4))==F(12,5) and F(1,2)+6*(F(1,6)-F(1,4))==0, '6 hours')
check('RATE-03', F(120,2+1)==40 and 144/(F(72,24)+F(72,72))==36, '72 km/h')
check('RATE-04', F(180,70+50)==F(3,2) and F(36,60)*(70-50)==12, '36 minutes')
check('ALG-01', sum(range(32,35))==99 and list(range(27,36,2))==[27,29,31,33,35] and sum(range(27,36,2))==155, '27, 29, 31, 33 and 35')
check('ALG-02', [n for n in range(13) if 4*n+2*(12-n)==34]==[5] and [n for n in range(11) if 7*n+3*(10-n)==46]==[4], 'four adults')
check('ALG-03', (29+21,29-21)==(50,8) and (2*5+7,5+2*7)==(17,19), '5 units and a pear weighs 7')
check('ALG-04', F(3*9-5,2)==11 and 2*(2*8-1)-1==29, 'gives 8')
check('ALG-05', (35+28,35-28)==(63,7) and (35-2)-(28+2)==3, 'margin of 3')
check('SEQ-01', sum(range(1,101))==5050 and sum(range(21,60,2))==800, 'sum is 800')
check('SEQ-02', sum(2**k for k in range(11))==2047 and sum(2**k for k in range(7))==127 and sum(2**k for k in range(8))==255, 'Day eight')
def tilings(n):
    if n==0:
        yield ()
    for length in (1,2):
        if length<=n:
            yield from ((length,)+rest for rest in tilings(n-length))
check('SEQ-03', len(list(tilings(5)))==8 and sum(t.count(2)==2 for t in tilings(6))==6, 'six choices')
def orbit(value, steps, update):
    for _ in range(steps):
        value = update(value)
    return value
check('SEQ-04', orbit(1,2027,lambda n:2*n%5)==3 and orbit(0,100,lambda n:(2*n+1)%7)==1, 'next move gives 1')
triples=[(x,y,z) for x,y,z in product(range(1,11),repeat=3) if x<=y<=z and x+y+z==10]
check('COUNT-01', len(triples)==8 and sum(len(set(t))==2 for t in triples)==4, 'There are four')
teams=list(combinations(range(8),3))
check('COUNT-02',len(teams)==56 and sum(not {0,1}<=set(t) for t in teams)==50,'to get 50')
orders=list(permutations('ABCDE'))
check('COUNT-03',sum(abs(p.index('A')-p.index('B'))==1 for p in orders)==48 and
      sum(abs(p.index('A')-p.index('B'))==2 for p in orders)==36,'= 36')
evens=set(range(2,101,2)); thirds=set(range(3,101,3))
check('COUNT-04',len(evens|thirds)==67 and len(evens^thirds)==51,'get 51')
check('COUNT-05',len(list(combinations(range(9),2)))==36 and (6*4+3)%2==1,'= 27')
numbers=[int(''.join(t)) for t in permutations('12345')]
check('COUNT-06',sum(n%2 for n in numbers)==72 and sum(n>40000 and n%2==0 for n in numbers)==18,'is 18')
roles=list(product((True,False), repeat=2))
check('LOGIC-01',[(a,b) for a,b in roles if a==((not a) and (not b))]==[(False,True)] and
      {(a,b) for a,b in roles if a==(not b) and b==(not a)}=={(False,True),(True,False)},'two possibilities')
check('LOGIC-02',sum(p.index('A')<p.index('C')<p.index('B') for p in permutations('ABC'))==1 and
      sum(p.index('A')<min(p.index('B'),p.index('C')) for p in permutations('ABCD'))==8,'eight orders')
# Any complete magic square is covered by checking all 9! arrangements.
magic=[]
lines=((0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6))
for p in permutations(range(1,10)):
    if all(p[a]+p[b]+p[c]==15 for a,b,c in lines):
        magic.append(p)
check('LOGIC-03',len(magic)==8 and all(p[4]==5 and all(2*(p[i]+p[8-i])==20 for i in range(4)) for p in magic),'centre becomes 10')
# Algebraic identities establish the real roots; the assertions check each coefficient and substitution.
check('LOGIC-04', all(x*x-x==x*(x-1) and x*(x-2)-3*(x-2)==(x-2)*(x-3) for x in (-3,0,1,2,3,F(1,7)))
      and all(x*(x-2)==3*(x-2) for x in (2,3)), 'Both 2 and 3')
def perimeter(cells):
    return sum((x+dx,y+dy) not in cells for x,y in cells for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)))
check('GEO-01',perimeter(set(product(range(6),range(1))))-perimeter(set(product(range(3),range(2))))==4,'4 units')
check('GEO-02',100-4*2*3==76 and sum(x>=2 and y>=2 for x,y in product(range(8),range(6)))==24,'24 square centimetres')
check('GEO-03',(5-2)*180==540 and [n for n in range(3,361) if (n-2)*180==150*n]==[12],'12 sides')
corners=[(-1,-1),(1,-1),(1,1),(-1,1)]; marks={corners[0],corners[2]}
def sym(p,k,flip):
    x,y=p
    if flip:x=-x
    for _ in range(k):x,y=-y,x
    return x,y
symmetries={tuple(sym(p,k,flip) for p in corners) for k,flip in product(range(4),(False,True))}
check('GEO-04',len(symmetries)==8 and sum({s[0],s[2]}==marks for s in symmetries)==4,'Four symmetries')
check('GEO-05',F(10,2)**2==25 and max(i*(13-i) for i in range(1,13))==42,'42 square centimetres')
def boundary(shape):
    return [sum(n in (0,limit-1) for n,limit in zip(p,shape)) for p in product(*(range(k) for k in shape))]
check('SOLID-01',boundary((4,4,4)).count(0)==8 and boundary((5,6,7)).count(0)==60,'= 60 cubes')
check('SOLID-02',boundary((5,5,5)).count(2)==36 and boundary((4,4,4)).count(1)==24,'24 little cubes')
check('SOLID-03',6**3==8*3**3 and 6*6**2==4*(6*3**2) and 8*(6*3**2)==2*6*6**2,'twice the original')
routes=[]
for up in combinations(range(7),3):
    x=y=0; path=[]
    for step in range(7):
        if step in up:y+=1
        else:x+=1
        path.append((x,y))
    if (2,1) not in path:routes.append(path)
check('SPATIAL-01',len(routes)==17 and sum(p[0]==(1,0) for p in routes)==8,'leave 8')
rectangles=[(x2-x1,y2-y1) for x1,x2 in combinations(range(5),2) for y1,y2 in combinations(range(4),2)]
check('SPATIAL-02',len(rectangles)==60 and sum(w!=h for w,h in rectangles)==40,'40 rectangles')
def cover(size, origin, missing):
    if size==1:return []
    half=size//2
    x,y=origin
    origins=[(x+i*half,y+j*half) for i,j in product(range(2),repeat=2)]
    middle=[(x+half-1+i,y+half-1+j) for i,j in product(range(2),repeat=2)]
    quadrant=(2 if missing[0]>=x+half else 0)+(1 if missing[1]>=y+half else 0)
    centre=set(middle)-{middle[quadrant]}
    placements=[centre]
    for i,start in enumerate(origins):
        placements+=cover(half,start,missing if i==quadrant else middle[i])
    return placements
for size in (4,8):
    board=set(product(range(size),repeat=2))
    for missing in board:
        tiles=cover(size,(0,0),missing)
        assert all(len(t)==3 and len({x for x,y in t})==len({y for x,y in t})==2 for t in tiles)
        assert len(tiles)==(size**2-1)//3 and set.union(*tiles)==board-{missing}
check('SPATIAL-03',(4**2-1)//3==5 and (8**2-1)//3==21,'= 21')
edges=[(0,1),(1,2),(2,3),(3,0),(0,2)]
def odd(edges):return {n for n in range(4) if sum(n in e for e in edges)%2}
check('SPATIAL-04',odd(edges)=={0,2} and odd(edges+[(1,3)])==set(range(4)), 'four corners')
dice=list(product(range(1,7),repeat=2)); six=[x for x in dice if 6 in x]
check('DATA-01',F(len(six),len(dice))==F(11,36) and F(six.count((6,6)),len(six))==F(1,11),'1/11')
check('DATA-02',4*25-(10+20+30)==40 and F(4*25-31+19,4)==22,'mean of 22')
check('DATA-03',round((100/95-1)*100,1)==5.3 and [b for b in range(70) if 80-b==3*(70-b)]==[65],'From 65 to 80')
assert checked==set(cards) and len(checked)==52
print('Verified 52 worked examples and their 52 transfer problems.')
