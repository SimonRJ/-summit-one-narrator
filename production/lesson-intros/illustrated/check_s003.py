"""Independently check the three examples in lesson 3."""
from pathlib import Path
import json

d=json.loads((Path(__file__).parent/'S003.json').read_text())
assert d['id']=='S003' and len(d['scenes'])==11
assert all(a['end']<=b['start'] for a,b in zip(d['captions'],d['captions'][1:]))
assert 6*4+7==31 and (31-7)//4==6
assert 27-27//3+7==25 and (25-7)//2*3==27
def reverse(n): return (n+2)*2
def forward(n): return n//2-2
assert [reverse(x) for x in (5,14,32)]==[14,32,68]
assert [forward(x) for x in (68,32,14)]==[32,14,5]
assert forward(12)==4
print('S003: machine, stamp parts and all three stations verified')
