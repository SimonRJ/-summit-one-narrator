"""Independent arithmetic checks of S011's primes, divisors and square."""
from math import isqrt
from itertools import product
assert all(37%d for d in range(2,isqrt(37)+1))
assert 60==2**2*3*5
shown={2**a*3**b*5**c for a,b,c in product(range(3),range(2),range(2))}
actual={n for n in range(1,61) if 60%n==0}
assert shown==actual and len(actual)==12
assert 2016==2**5*3**2*7
assert all(isqrt(2016*n)**2!=2016*n for n in range(1,14))
assert 2016*14==168**2==28224
assert 2*2*2*3*7==168
assert len([n for n in range(1,2) if 1%n==0])==1
print('S011: primality, 12 divisors and smallest square multiplier verified')
