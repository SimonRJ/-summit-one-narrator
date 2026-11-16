"""Independent checks of the published S001 narration and its animated examples."""
from pathlib import Path
import json

d=json.loads((Path(__file__).parent/'S001.json').read_text())
assert d['id']=='S001' and len(d['scenes'])==9
assert all(a['end'] <= b['start'] for a,b in zip(d['captions'],d['captions'][1:]))
assert 2473%3==1 and sum(map(int,str(2473)))==16
assert 1739==6*289+5
shapes=['triangle','square','circle','star','diamond','hexagon']
assert shapes[(1739-1)%6]=='diamond' and shapes[(1740-1)%6]=='hexagon'
valid=[n for n in range(100,1000) if n%5==4 and n%7==6 and n%9==0]
assert valid[0]==279 and [35*k%9 for k in range(1,9)]==[8,7,6,5,4,3,2,1]
print('S001: digit-sum, cycle indexing and all three conditions verified')
