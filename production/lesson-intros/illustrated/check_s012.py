"""Check the narrated sequences and enumerate the broken-rung routes."""
seq=[5]
for _ in range(3):seq.append(seq[-1]+3)
assert seq==[5,8,11,14]
readings=[3]
for _ in range(4):readings.append(2*readings[-1]-1)
assert readings==[3,5,9,17,33]
assert [x-1 for x in readings]==[2,4,8,16,32]
ways=[0]*9;ways[0]=1
for rung in range(1,9):
 if rung!=3:ways[rung]=ways[rung-1]+(ways[rung-2] if rung>=2 else 0)
assert ways==[1,1,2,0,2,2,4,6,10]
paths=[]
def enumerate_routes(pos,path):
 if pos==8:paths.append(path);return
 for step in (1,2):
  target=pos+step
  if target<=8 and target!=3:enumerate_routes(target,path+[step])
enumerate_routes(0,[])
assert len(paths)==10 and sum(p[-1]==1 for p in paths)==6 and sum(p[-1]==2 for p in paths)==4
assert any(2 in p and p[:3]==[1,1,2] for p in paths)
print('S012: both sequences, broken-rung table and ten routes verified')
