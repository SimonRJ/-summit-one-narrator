"""Enumerate every legal number and ending used by lesson 4."""
from itertools import permutations
from pathlib import Path
import json

d=json.loads((Path(__file__).parent/'S004.json').read_text())
assert d['id']=='S004' and len(d['scenes'])==12
assert all(a['end']<=b['start'] for a,b in zip(d['captions'],d['captions'][1:]))
assert min(int(''.join(p)) for p in permutations('047') if p[0]!='0')==407
even=sorted(int(''.join(p)) for p in permutations('025') if p[0]!='0' and int(p[-1])%2==0)
assert even==[250,502,520]
valid=[int(''.join(p)) for p in permutations('01246') if p[0]!='0' and int(''.join(p))>40000 and int(''.join(p))%4==0]
assert len(valid)==18 and 61204 in valid
assert sum(n//10000==4 for n in valid)==8 and sum(n//10000==6 for n in valid)==10
endings=['20','40','60','12','04','24','64','16']
assert all(int(x)%4==0 and len(set(x))==2 for x in endings)
assert sum('4' not in x for x in endings)==4 and sum('6' not in x for x in endings)==5
print('S004: smallest number, even cases and all 18 five-digit numbers verified')
