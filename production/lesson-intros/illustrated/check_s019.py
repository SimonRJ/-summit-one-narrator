"""Verify exact parity and the missing-corner domino obstruction."""
assert 15==7*2+1 and 20==10*2 and 15+20==35
assert all((15+2*k)%2==1 for k in range(-30,31)) and 20%2==0
board={(r,c) for r in range(4) for c in range(4)}
holes={(0,0),(3,3)}
assert all((r+c)%2==0 for r,c in holes)
assert len(board-holes)==14
assert sum((r+c)%2==0 for r,c in board-holes)==6
assert sum((r+c)%2==1 for r,c in board-holes)==8
for r,c in board:
 for dr,dc in ((1,0),(0,1)):
  if (r+dr,c+dc) in board:
   assert (r+c)%2 != (r+dr+c+dc)%2
# Each domino requires one of each colour; 7 dominoes would require 7 of each.
assert 14//2==7 and 6!=7 and 8!=7
print('S019: exact missing corners, 6/8 colour balance and domino obstruction verified')
