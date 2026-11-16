"""Independent enumeration of the reversal and carry examples in S010."""
assert [a for a in range(10) if a+a==8]==[4]
reversal=[(a,b) for a in range(1,10) for b in range(1,10)
          if a!=b and a+b==8 and 10*a+b+36==10*b+a]
assert reversal==[(2,6)] and 26+36==62
assert all((10*b+a)-(10*a+b)==9*(b-a) for a in range(1,10) for b in range(1,10))
solutions=[]
for a in range(1,10):
 for b in range(1,10):
  for c in range(10):
   for d in range(10):
    if len({a,b,c,d})==4 and (10*a+b)+(10*a+c)==100*b+10*d:
     solutions.append((10*a+b,a,b,c,d))
assert solutions and min(solutions)==(61,6,1,9,3)
assert 51+59==110 and 61+69==130
print('S010: reversal identity, digit sum, rejected candidate and minimum carry solution verified')
