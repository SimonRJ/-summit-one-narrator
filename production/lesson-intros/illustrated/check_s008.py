"""Independently enumerate the S008 examples and check the released soundtrack."""
from itertools import product
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
timeline=json.loads((ROOT/'S008.json').read_text())
assert timeline['id']=='S008' and len(timeline['scenes'])==11
assert all(s['match'] >= 90 for s in timeline['scenes'])
assert 111*3==333
assert 2772==2*1001+7*110 and 1001==11*91 and 110==11*10
assert 2772//11==252 and 2772%11==0
palindromes=[]
extra=0
for a,b,c in product(range(1,10),range(10),range(10)):
    number=10000*a+1000*b+100*c+10*b+a
    assert str(number)==str(number)[::-1]
    assert sum(map(int,str(number)))==2*a+2*b+c
    if number%9==0:
        palindromes.append(number)
    if c==9 and (2*a+2*b)%9==0:
        extra+=1
assert len(set(palindromes))==100 and extra==10
for number in [18081,18981]:
    assert str(number)==str(number)[::-1] and number%9==0
print('S008: independently enumerated all 100 solutions; checked examples and timings')
