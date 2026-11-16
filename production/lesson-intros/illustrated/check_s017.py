"""Enumerate grid crossings and all boundary-defined S017 rectangles."""
from itertools import combinations
assert (3+1)*(2+1)==12
assert len(list(combinations(range(5),2)))*len(list(combinations(range(4),2)))==60
# In a 6x5 grid, cell (column,row) lies between line coordinates (c-1,c) and (r-1,r).
A=(2,3);B=(5,3)
rects=[(l,r,b,t) for l,r in combinations(range(7),2) for b,t in combinations(range(6),2)]
def contains(rect,cell):
 l,r,b,t=rect;c,row=cell
 return l<=c-1 and c<=r and b<=row-1 and row<=t
contains_a=[rect for rect in rects if contains(rect,A)]
contains_both=[rect for rect in contains_a if contains(rect,B)]
only_a=[rect for rect in contains_a if not contains(rect,B)]
assert (len(contains_a),len(contains_both),len(only_a))==(90,36,54)
assert contains((1,4,2,4),A) and not contains((1,4,2,4),B)
assert contains((1,5,2,4),A) and contains((1,5,2,4),B)
assert 2*5*3*3==90 and 2*2*3*3==36 and 90-36==54
print('S017: grid dimensions, marked cell locations, boundaries and 54 rectangles verified')
