"""Validate the pair counts, parity invariant and all merge orders in S018."""
from functools import lru_cache
assert 13==6*2+1 and 18==9*2 and 13+18==31
assert all((13+2*k)%2==1 for k in range(-20,21)) and 18%2==0
@lru_cache(None)
def finals(values):
 if len(values)==1:return {values[0]}
 found=set()
 for i in range(len(values)):
  for j in range(i+1,len(values)):
   rest=[v for k,v in enumerate(values) if k not in (i,j)]
   found |= finals(tuple(sorted(rest+[values[i]+values[j]+1])))
 return found
initial=(3,7,9,14,19)
assert sum(initial)==52 and finals(initial)=={56}
assert [3+7+1,11+9+1,21+14+1,36+19+1]==[11,21,36,56]
assert 7+9+1==17 and 3+17+1==21
print('S018: exact paired counters, even-move invariant and all merge orders verified')
