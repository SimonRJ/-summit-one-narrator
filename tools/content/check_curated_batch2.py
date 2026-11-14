"""Independent recomputation of every answer in curated_batch2.py.

Each check below solves the problem again by brute-force search or direct
simulation, written separately from the worked solution. It also confirms that
problems claiming a unique answer really have exactly one.
Run: python tools/content/check_curated_batch2.py
"""
import sys
from fractions import Fraction as F
from itertools import permutations, product, combinations, combinations_with_replacement
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from curated_batch2 import B, SKILLS

def one(values):
    values = list(values)
    assert len(set(values)) == 1, ('not unique', values[:6])
    return values[0]

R = range
isprime = lambda n: n > 1 and all(n % d for d in R(2, int(n ** .5) + 1))
dsum = lambda n: sum(map(int, str(n)))
C = {}

# ALG-02
C['ALG-02', 'try', 2] = lambda: one(c for a in R(1, 65) for b in R(1, 65) for c in R(1, 65) if a + b + c == 64 and b == 2 * a and c == b + 4)
C['ALG-02', 'transfer', 2] = lambda: one(max(t) for t in product(R(1, 39), repeat=3) if t[0] <= t[1] <= t[2] and sorted([t[0] + t[1], t[0] + t[2], t[1] + t[2]]) == [31, 35, 38])
C['ALG-02', 'try', 3] = lambda: one(c for c in R(24) if 4 * c + 2 * (23 - c) == 74)
C['ALG-02', 'transfer', 3] = lambda: one(c for c in R(41) if 12 * (40 - c) + 7 * c == 365)
C['ALG-02', 'try', 4] = lambda: one(m for m in R(7, 200) for l in R(7, 200) if m - 6 == l + 6 and m + 6 == 3 * (l - 6))
C['ALG-02', 'transfer', 4] = lambda: one(l * w for l in R(1, 29) for w in R(1, 29) if 2 * (l + w) == 58 and l - 5 == w + 2)
C['ALG-02', 'try', 5] = lambda: one(p + 3 for p in R(1, 41) if 4 * (p + 3) + 3 * p == 40)
C['ALG-02', 'transfer', 5] = lambda: one(m for a in R(1, 16) for b in R(1, 16) for m in R(1, 16) if 2 * a + b + m == 13 and a + 2 * b + m == 12 and a + b + 2 * m == 15)
C['ALG-02', 'try', 6] = lambda: one(f for f in R(1, 67) if f + 4 == 2 * ((66 - f) + 8))
C['ALG-02', 'transfer', 6] = lambda: one(t + f for t in R(97) for f in R(20) if 10 * t + 50 * f == 960 and t == f + 6)
C['ALG-02', 'try', 7] = lambda: one(b + c for a in R(91) for d in R(91) for b in [0] for c in [90 - a - d] if c >= 0 and a + b + c == 61 and b + c + d == 70)
C['ALG-02', 'transfer', 7] = lambda: one(x for x in R(1, 500) for y in R(1, x) if x + y == 5 * (x - y) and x == y + 12)
C['ALG-02', 'try', 8] = lambda: one(c for c in R(21) if 5 * c - 2 * (20 - c) == 58)
C['ALG-02', 'transfer', 8] = lambda: one(t for u in R(21) for b in R(21) for t in R(21) if u + b + t == 20 and u + 2 * b + 3 * t == 44 and b == 2 * u)

# SEQ-04
def seq(start, step, n):
    x = start
    for _ in R(n - 1):
        x = step(x)
    return x
C['SEQ-04', 'try', 2] = lambda: seq(3, lambda x: 3 * x % 10, 50)
C['SEQ-04', 'transfer', 2] = lambda: sum('rrbgb'[i % 5] == 'b' for i in R(73))
C['SEQ-04', 'try', 3] = lambda: seq(0, lambda x: (x + 5) % 12, 2027)
C['SEQ-04', 'transfer', 3] = lambda: sum([1, 1, 0][(t - 1) % 3] and [1, 0, 0, 1][(t - 1) % 4] for t in R(1, 61))
C['SEQ-04', 'try', 4] = lambda: seq(20, lambda x: x // 2 if x % 2 == 0 else x + 7, 100)
def _seventh():
    digits, r = [], 1
    for _ in R(40):
        r *= 10; digits.append(r // 7); r %= 7
    assert digits[:6] == [1, 4, 2, 8, 5, 7]
    return sum(digits)
C['SEQ-04', 'transfer', 4] = _seventh
def _cups():
    cups = [1, 0, 0, 0]
    for k in R(20):
        i = k % 3
        cups[i], cups[i + 1] = cups[i + 1], cups[i]
    return cups.index(1) + 1
C['SEQ-04', 'try', 5] = _cups
C['SEQ-04', 'transfer', 5] = lambda: sum(2 ** k for k in R(1, 51)) % 10
def _fib_even():
    a, b, n = 1, 1, 0
    for _ in R(60):
        n += a % 2 == 0; a, b = b, a + b
    return n
C['SEQ-04', 'try', 6] = _fib_even
def _chain():
    a, b = 1, 3
    for _ in R(98):
        a, b = b, (a + b) % 10
    return b
C['SEQ-04', 'transfer', 6] = _chain
C['SEQ-04', 'try', 7] = lambda: sum([1, 1, 0, 0, 0, 1, 0, 0, 0, 0][(t - 1) % 10] for t in R(1, 338))
C['SEQ-04', 'transfer', 7] = lambda: sum(R(1, 101)) % 7

# LOGIC-02
C['LOGIC-02', 'try', 2] = lambda: one(n for n in R(61, 80) if n % 2 and dsum(n) == 11)
def _race():
    out = []
    for p in permutations(R(1, 6)):
        a, b, c, d, e = p
        if b == a + 2 and c == b + 1 and e > d and d != 1:
            out.append(d)
    return one(out)
C['LOGIC-02', 'transfer', 2] = _race
C['LOGIC-02', 'try', 3] = lambda: one(n for n in R(101, 200) if n % 7 == 0 and n % 2 == 0 and dsum(n) == 11)
C['LOGIC-02', 'transfer', 3] = lambda: one(p[0] for p in permutations([10, 20, 30, 40]) if p[0] > p[1] and p[2] == p[3] + 10 and p[1] != 10)
C['LOGIC-02', 'try', 4] = lambda: one(t[2] for t in combinations(R(2, 61), 3) if t[0] * t[1] * t[2] == 60 and sum(t) == 12)
C['LOGIC-02', 'transfer', 4] = lambda: one(n for n in R(10, 100) if int(n ** .5) ** 2 == n and isprime(int(str(n)[::-1])))
C['LOGIC-02', 'try', 5] = lambda: one(t[2] for t in product(R(0, 21), repeat=3) for t in [(7, t[0], t[1], t[2], 4)] if all(sum(t[i:i + 3]) == 20 for i in R(3)))
C['LOGIC-02', 'transfer', 5] = lambda: one(n for n in R(1, 11) if [n % 2 == 0, n > 6, n % 4 == 0, n < 9].count(False) == 1)
C['LOGIC-02', 'try', 6] = lambda: one(a for a, b, c in permutations(R(1, 10), 3) if a == b + c and b == 3 * c and a + b + c > 10)
C['LOGIC-02', 'transfer', 6] = lambda: one(r for p, q, r, s in permutations([1, 2, 3, 4]) if p + q == r + s and p > s and q > p)
C['LOGIC-02', 'try', 7] = lambda: one(y for y in R(2001, 2100) if y % 11 == 0 and dsum(y) == 12)
def _code():
    def fb(g, c):
        place = sum(x == y for x, y in zip(g, c))
        return place, sum(x in c for x in g) - place
    clues = [((4, 3, 5), (1, 0)), ((7, 9, 5), (0, 1)), ((9, 6, 2), (0, 0)), ((2, 6, 1), (1, 0))]
    sols = [c for c in permutations(R(10), 3) if all(fb(g, c) == f for g, f in clues)]
    return one(100 * c[0] + 10 * c[1] + c[2] for c in sols)
C['LOGIC-02', 'transfer', 7] = _code

# FRAC-02
C['FRAC-02', 'try', 2] = lambda: F(56, 8) * 4 - F(56, 8)
C['FRAC-02', 'transfer', 2] = lambda: one(a for a in R(1, 94) for b in R(1, 94) for c in [93 - a - b] if c > 0 and 4 * a == 3 * b and 5 * b == 6 * c)
C['FRAC-02', 'try', 3] = lambda: F(8 * 50000, 100 * 1000)
C['FRAC-02', 'transfer', 3] = lambda: 40 * 3 ** 2
C['FRAC-02', 'try', 4] = lambda: one(a for a in R(9, 500) for b in R(1, 500) if 3 * a == 5 * b and a - 8 == b + 8)
C['FRAC-02', 'transfer', 4] = lambda: one(m for t in R(1, 100) for m in [4 * t] if 5 * (t + 6) == 2 * (m + 6))
C['FRAC-02', 'try', 5] = lambda: 11 * min(F(900, 6), F(250, 2), F(480, 3))
C['FRAC-02', 'transfer', 5] = lambda: F(24 * 35, 40)
C['FRAC-02', 'try', 6] = lambda: F(2, 3) * 27
C['FRAC-02', 'transfer', 6] = lambda: 300 * F(20, 10) ** 3
C['FRAC-02', 'try', 7] = lambda: (F(3, 3) * 1 + F(4, 4) * 3) - (F(3, 3) * 2 + F(4, 4) * 1)
C['FRAC-02', 'transfer', 7] = lambda: one(b + g for b in R(1, 300) for g in R(7, 300) if 5 * b == 3 * g and 4 * (b + 6) == 3 * (g - 6))

# COUNT-01
def dprod(n):
    p = 1
    for ch in str(n):
        p *= int(ch)
    return p
C['COUNT-01', 'try', 2] = lambda: sum(dprod(n) == 24 for n in R(100, 1000))
C['COUNT-01', 'transfer', 2] = lambda: sum(a + b > c for a, b, c in combinations_with_replacement(R(1, 15), 3) if a + b + c == 15)
C['COUNT-01', 'try', 3] = lambda: sum((a + b) % 5 == 0 for a, b in combinations(R(1, 11), 2))
C['COUNT-01', 'transfer', 3] = lambda: sum(t[3] % 2 == 0 for t in combinations(R(1, 7), 4))
C['COUNT-01', 'try', 4] = lambda: sum(sum(t) == 10 for t in combinations_with_replacement(R(1, 7), 3))
C['COUNT-01', 'transfer', 4] = lambda: sum(int(str(n)[1]) == int(str(n)[0]) + int(str(n)[2]) for n in R(100, 1000))
C['COUNT-01', 'try', 5] = lambda: sum(all(f[i] != f[i + 1] for i in R(3)) and f[0] != f[3] for f in product('RWB', repeat=4))
C['COUNT-01', 'transfer', 5] = lambda: sum(sum(t) == 30 for t in combinations([p for p in R(2, 30) if isprime(p)], 3))
C['COUNT-01', 'try', 6] = lambda: sum(dsum(n) == 9 for n in R(1, 201))
def _strides(n=10):
    w = [1] + [0] * n
    for i in R(1, n + 1):
        w[i] = (w[i - 2] if i >= 2 else 0) + (w[i - 3] if i >= 3 else 0)
    return w[n]
C['COUNT-01', 'transfer', 6] = _strides

def main():
    assert set(C) == set(B), (set(B) ^ set(C))
    skeleton = lambda s: __import__('re').sub(r'[0-9]+(?:[.,][0-9]+)?', 'N', s.lower())
    for key, problem in B.items():
        got = C[key]()
        assert F(got) == F(problem['answer']), (key, 'stored', problem['answer'], 'recomputed', got)
        assert isinstance(problem['answer'], int), key
        assert problem['prompt'].endswith('?') and 35 < len(problem['prompt']) < 1150, key
        assert len(problem['steps']) >= 2 and problem['check'] and problem['clue'], key
        text = ' '.join([problem['prompt'], problem['check'], problem['clue']] + problem['steps'])
        assert 'PLACEHOLDER' not in text and '...' not in text, key
        assert not __import__('re').search(r'explain your|show your reasoning|in your working', text, __import__('re').I), key
    for skill in SKILLS:
        items = [v for k, v in B.items() if k[0] == skill]
        assert len({v['title'] for v in items}) == len(items), (skill, 'duplicate titles')
        assert len({skeleton(v['prompt']) for v in items}) == len(items), (skill, 'repeated structure')
    print(f'PASS: {len(B)} reauthored problems in {len(SKILLS)} families independently recomputed; answers unique where uniqueness is claimed.')

if __name__ == '__main__':
    main()
