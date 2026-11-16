"""Independently check the S002 arithmetic and dimensions used in the animation."""
from pathlib import Path
import json
import math

d=json.loads((Path(__file__).parent/'S002.json').read_text())
assert d['id']=='S002' and len(d['scenes'])==9
assert all(a['end']<=b['start'] for a,b in zip(d['captions'],d['captions'][1:]))
assert 398+207==605
assert 57*100==5700 and 57*2==114 and 57*98==5586
assert 49996*50004==50000**2-16
assert 49996*50004-(50000**2-17)==1
for n,delta in [(8,2),(10,3),(50000,4)]:
    assert (n-delta)*(n+delta)==n*n-delta*delta
assert math.isclose(100/57,(100*5.6)/(57*5.6),rel_tol=1e-12)
print('S002: place-value examples, rectangle proportions and difference of squares verified')
