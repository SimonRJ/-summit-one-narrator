"""Check the schedules, coloured pack totals and closest HCF/LCM pair."""
from math import gcd,lcm
assert lcm(6,9)==18
assert [x for x in range(1,19) if x%6==0 and x%9==0]==[18]
assert gcd(24,36)==12 and 12*2==24 and 12*3==36
pairs=[]
for a in range(1,181):
 for b in range(a,181):
  if gcd(a,b)==6 and lcm(a,b)==180:pairs.append((a,b))
assert pairs and min(pairs,key=lambda p:p[1]-p[0])==(30,36)
scaled=[(a//6,b//6) for a,b in pairs]
assert set(scaled)=={(1,30),(2,15),(3,10),(5,6)}
assert all(gcd(a,b)==1 and a*b==30 for a,b in scaled)
print('S013: meeting time, exact pack contents and closest original pair verified')
