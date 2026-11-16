"""Independent enumeration of every numeric claim in lesson S009."""
assert [a for a in range(10) if a+a==6]==[3]
medium=[(a,b) for a in range(1,10) for b in range(10)
        if a!=b and 2*(10*a+5)==70+b]
assert medium==[(3,0)] and 35+35==70
solutions=[]
for a in range(1,10):
 for b in range(1,10):
  for c in range(10):
   for d in range(10):
    if len({a,b,c,d})==4 and 2*(10*a+b)==100*b+10*c+d:
     solutions.append((10*a+b,a,b,c,d))
assert solutions and min(solutions)==(51,5,1,0,2)
assert all(s[2]==1 and s[4]==2 and s[1]>=5 for s in solutions)
assert 51+51==102
print('S009: simple and medium equations and minimum distinct-digit solution verified')
