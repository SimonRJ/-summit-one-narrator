"""Independent counts of the solids and their overlapping cuts in S006."""
from itertools import product
simple=set(product(range(3),range(2),range(2)))
assert len(simple)==12 and len({(x,y) for x,y,z in simple if z==0})==6
front=[1,3,2];back=[4,1,3]
heights=front+back
assert sum(heights)==14
assert [sum(h>=level for h in heights) for level in range(1,5)]==[6,4,3,1]
solid=set(product(range(4),range(4),range(3)))
column={(1,1,z) for z in range(3)}
tunnel={(x,1,1) for x in range(4)}
assert len(solid)==48 and len(column)==3 and len(tunnel)==4
assert len(column & tunnel)==1 and len(column | tunnel)==6
remaining=solid-(column|tunnel)
assert [sum(z==i for x,y,z in remaining) for i in range(3)]==[15,12,15]
assert len(remaining)==42
print('S006: dimensions, stacks, layer counts and shared cut verified')
