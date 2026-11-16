"""Check the actual clock example and each power-sum claim independently."""
from math import cos,pi,sin

cycle=[pow(3,n,10) for n in range(1,5)]
assert cycle==[3,9,7,1]
assert all(pow(3,n,10)==cycle[(n-1)%4] for n in range(1,101))
assert divmod(37,4)==(9,1) and pow(3,37,10)==3
assert divmod(51,4)==(12,3)
assert sum(cycle)==20 and sum(cycle[:3])==19
assert sum(pow(3,n,10) for n in range(1,52))==259
assert sum(3**n for n in range(1,52))%10==9

assert (9+17)%12==2 and (9+12)%12==9
angle=lambda hour:-pi/2+2*pi*hour/12
assert abs(cos(angle(9))+1)<1e-9 and abs(sin(angle(9)))<1e-9
assert cos(angle(26))>0 and sin(angle(26))<0  # two is upper-right
assert cycle[3]==1 and sum(cycle)%10==0
print('S020: exact clock turn, power cycle, remainder-zero and 51-term sum verified')
