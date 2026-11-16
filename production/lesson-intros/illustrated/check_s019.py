"""Independently verify every board and covering in the new lesson."""
from functools import lru_cache

small={(r,c) for r in range(3) for c in range(3)}
assert len(small)==9
assert sum((r+c)%2==0 for r,c in small)==5
assert sum((r+c)%2==1 for r,c in small)==4

@lru_cache(None)
def can_tile(cells):
    if not cells:return True
    first=min(cells);r,c=first
    for neighbour in ((r+1,c),(r-1,c),(r,c+1),(r,c-1)):
        if neighbour in cells and can_tile(frozenset(cells-{first,neighbour})):
            return True
    return False

board={(r,c) for r in range(4) for c in range(4)}
adjacent_holes={(0,0),(0,1)}
available=board-adjacent_holes
pieces=[{(0,2),(0,3)}]+[{(r,c),(r,c+1)} for r in (1,2,3) for c in (0,2)]
assert len(pieces)==7 and set().union(*pieces)==available
assert sum(len(piece) for piece in pieces)==len(available)==14
assert all(len(piece)==2 and len({(r+c)%2 for r,c in piece})==2 for piece in pieces)
assert can_tile(frozenset(available))

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
assert not can_tile(frozenset(board-holes))
# Balanced colours are not enough: two isolated opposite-colour cells cannot form a domino.
isolated={(0,0),(0,3)}
assert len({(r+c)%2 for r,c in isolated})==2 and not can_tile(frozenset(isolated))
print('S019: 3×3 count, explicit seven-domino covering, impossible board and counterexample verified')
