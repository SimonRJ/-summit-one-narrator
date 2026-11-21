"""Independent finite calculations for the numbered investigations in schedule order."""
import itertools as it
from collections import Counter,deque
from fractions import Fraction
from hashlib import sha256
from math import comb,factorial,prod,gcd,lcm
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[2]
data=json.loads((ROOT/'data/mawa-investigations-20.json').read_text())
def perms(n): return it.permutations(range(1,n+1))
def tri(n): return n*(n+1)//2
def tris(a,b): return comb(a+b,3)-comb(a,3)-comb(b,3)
def routes(m,n):
 for us in it.combinations(range(m+n),n):
  p=[(0,0)]
  for t in range(m+n):
   x,y=p[-1]; p.append((x+(t not in us),y+(t in us)))
  yield p
def tile(n,m,removed=(),bar=2):
 cells={(i,j) for i in range(n) for j in range(m)}-set(removed)
 def f(left):
  if not left:return 1
  i,j=min(left);ans=0
  for di,dj in [(1,0),(0,1)]:
   s={(i+di*k,j+dj*k) for k in range(bar)}
   if s<=left: ans+=f(left-s)
  return ans
 return f(cells)
def queens(n):
 return [p for p in perms(n) if len({i-v for i,v in enumerate(p)})==len({i+v for i,v in enumerate(p)})==n]
def payments(n,values):
 return [(a,n-a-c,c,sum(t*d for t,d in zip((a,n-a-c,c),values))) for a in range(n+1) for c in range(n-a+1)]
def rails(n,occupancy):
 states={tuple(occupancy)}
 todo=deque(states)
 while todo:
  state=todo.popleft(); i=state.index('_')
  for j in [(i-1)%n,(i+1)%n]:
   target=list(state);target[i],target[j]=target[j],target[i];t=tuple(target)
   if t not in states:states.add(t);todo.append(t)
 return states
def moved(nums,n,goal):
 todo=deque([(tuple(nums),0)]);seen={tuple(nums)}
 while todo:
  state,c=todo.popleft()
  if state==tuple(goal):return c
  for x in state:
   for dest in (x-1,x+1):
    if dest in state or not 1<=dest<=n:continue
    nx=tuple(sorted(set(state)-{x}|{dest}))
    if nx not in seen:seen.add(nx);todo.append((nx,c+1))
def winners(k,last_loses,through):
 win=[bool(last_loses)]
 for n in range(1,through+1):win.append(any(not win[n-step] for step in range(1,min(k,n)+1)))
 return win
def ring(n):
 a=tuple(chr(65+i) for i in range(n-1))+('_',);return {s for s in rails(n,a) if s[-1]=='_'}
def same(o,e):
 if o!=e:raise AssertionError((o,e))
# M01–M20, initial visit.
same([abs(n-int(str(n)[::-1])) for n in [741,502,811]],[594,297,693])
for n in range(100,1000):
 x=abs(n-int(str(n)[::-1]));same(x//10%10,9 if n//100!=n%10 else 0)
same(len([n for n in range(11,100) if n%10 and abs(n-int(str(n)[::-1]))==27]),12)
same(sum(range(1,32,2)),256)
for n in range(1,35): a=list(range(n*n-n+1,n*n+n,2));same((len(a),sum(a)),(n,n**3));same((n+2)**2-n*n,4*n+4)
same((lcm(4,6,9),lcm(4,6,8)),(36,24))
same([i for i in range(9,61) if (i-5)%6==(i-9)%8==0],[17,41])
arr=list(it.permutations('ABCDE'))
same(Counter(p.index('C') for p in arr if p.index('C') in [1,2,3] and abs(p.index('A')-p.index('B'))!=1),Counter({1:16,2:16,3:16}))
same(sum(p[0]=='C' and abs(p.index('A')-p.index('B'))==1 for p in arr),12)
same((tris(5,4),tris(3,6),tris(3,5)),(70,63,45))
same(Counter((2,1) in p for p in routes(4,3)),Counter({True:18,False:17}))
same(Counter((1,2) in p for p in routes(3,3)),Counter({True:9,False:11}))
same((comb(5,2)*3,comb(4,2)),(30,6))
# Round-ended and notched windows, pair (straight coefficient, pi coefficient).
same((8*2,2*8,10*2-16),(16,16,4));same((12*6,(6//2)**2,2*12,6),(72,9,24,6))
same((4**2,Fraction(2**2,4),4*4-2*2,Fraction(2,2)),(16,1,12,1))
same((8*4-6,Fraction(3,2),Fraction(9,4)),(26,Fraction(3,2),Fraction(9,4)))
def discs():
 start=frozenset([1,3,5,7]);end=frozenset([0,2,6,8]);seen={start};todo=deque([(start,0)])
 while todo:
  pos,n=todo.popleft()
  if pos==end:return n
  for a in pos:
   for b in range(9):
    if b in pos or abs(a%3-b%3)+abs(a//3-b//3)!=1:continue
    ns=pos-{a}|{b}
    if ns not in seen:seen.add(ns);todo.append((ns,n+1))
same(discs(),4);same(len(list(routes(1,1))),2)
def fivepaint(w,d,h):return Counter(int(x in (0,w-1))+int(y in (0,d-1))+int(z==h-1) for x,y,z in it.product(range(w),range(d),range(h)))
same(fivepaint(4,5,3),Counter({0:12,1:26,2:18,3:4}))
same(Counter(z in (0,3) for _,_,z in it.product(range(3),range(3),range(4))),Counter({0:18,1:18}))
same(tile(4,4,[(0,0),(3,3)]),0);assert tile(4,4,[(0,0),(3,0)]) and tile(3,6,[(0,0),(0,5)])
abc=[p for p in it.permutations(range(1,6),3) if p[0]+p[1]==7 and p[1]+p[2]==5];same(abc,[(3,4,1),(4,3,2),(5,2,3)])
same([p for p in abc if 2*p[0]+p[2]==10],[(4,3,2)])
abc=[p for p in it.permutations(range(1,10),3) if p[0]+p[1]==9 and p[1]+p[2]==7];same(len(abc),6);same([p for p in abc if p[0]+p[2]==8],[(5,4,3)])
grid=[8,1,6,3,5,7,4,9,2]
lines=[(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
same({sum(grid[k] for k in g) for g in lines},{15});same({sum(grid[k]+4 for k in g) for g in lines},{27})
same({p[:3] for p in payments(6,(1,2,5)) if p[3]==14},{(1,4,1),(4,0,2)})
assert all(p[3]!=24 for p in payments(5,(1,2,5)))
same({p[:3] for p in payments(5,(1,3,4)) if p[3]==13},{(1,4,0),(2,1,2)})
edges=['AB','AC','AD','BE','CE'];same(Counter(''.join(edges)),Counter(A=3,B=2,C=2,D=1,E=2));assert sum([3,2,2,1,3])%2 and sum([3,2,2,2])%2
same(queens(4),[(2,4,1,3),(3,1,4,2)]);same(queens(3),[])
same(max(a*(12-a) for a in range(1,12)),36);same(max(w*(24-2*w) for w in range(1,12)),72)
for k in [2,3]:same(winners(k,False,45),[bool(n%(k+1)) for n in range(46)])
same((2*240+14*12+9,240+8*12+7,4*240+3*12+4),(657,343,1000))
same((2*120+11*8+6,120+7*8+5,4*120+4*8+3),(334,181,515))
# M01–M20, second visit.
larger=[n for n in range(11,100) if n%10 and n-int(str(n)[::-1])==36]
same([n for n in larger if n+int(str(n)[::-1])==110],[73]);same([n+int(str(n)[::-1]) for n in larger],[66,88,110,132,154])
for n in range(2,150):same(sum(range(n+1)),tri(n));same(tri(n)+tri(n-1),n*n)
same(tri(24),300)
two=[t for t in range(4,700) if (t-2)%6==(t-4)%8==0];same(two[:4],[20,44,68,92]);same([i for i in two if (i-2)%5==0][:3],[92,212,332]);same([i for i in range(3,27) if (i-2)%6==(i-3)%8==0],[])
circle=[('A',)+s for s in it.permutations('BCDEF')];adj=lambda p,a,b:(p.index(a)-p.index(b))%6 in (1,5)
same(sum(p[3]=='B' and adj(p,'C','D') for p in circle),8);same(sum(not adj(p,'A','B') and adj(p,'C','D') for p in circle),24)
for n in range(2,14):
 pairs=list(it.combinations(range(n),2));quads=list(it.product(pairs,repeat=2));pg=[(a,b) for a,b in quads if a[1]-a[0]==b[1]-b[0]]
 same(len(pg),sum(i*i for i in range(1,n)))
 if n==5:same((len(quads),len(pg),sum(a!=b for a,b in pg)),(100,30,20))
same(sum(not ({(1,1),(2,2)}&set(p)) for p in routes(3,3)),4)
same(sum(not ({(1,2),(2,1)}&set(p)) for p in routes(3,3)),2)
same(sum(comb(n,2) for n in (6,4,4)),27);same(comb(6,2)-comb(4,2),9)
same((2*18,2*4,2*(4+1.5),2*1.5),(36,8,11.0,3.0))
same((1*4**2,4*2**2),(16,16));same((48-2*4,Fraction(4,2),48-4*2*2,Fraction(4*2,2)),(40,2,32,4))
same(moved((1,3,5),7,(3,5,7)),6);same(moved((1,4,7),7,(2,5,6)),3)
fits=[]
for a,b,c in it.combinations_with_replacement(range(3,15),3):
 face=Counter(sum((p in (0,s-1)) for p,s in zip((x,y,z),(a,b,c))) for x,y,z in it.product(range(a),range(b),range(c)))
 if face[0]==12 and face[2]==32:fits.append(((a,b,c),face[1]))
same(fits,[((3,5,6),38)])
same(tile(4,6,[(0,0),(1,2),(2,1)],3),0);assert tile(4,6,[(0,0),(0,1),(0,2)],3)>0
abc=[p for p in it.permutations(range(1,10),3) if p[0]+p[1]==2*p[2] and sum(p)==15]
same(len(abc),8);same([p for p in abc if p[0]-p[1]==4],[(7,3,5)]);same([p for p in abc if p[0]>p[1] and sum(x in {2,3,5,7} for x in p[:2])==1],[(8,2,5)])
power=[2**p for p in grid];same({prod(power[k] for k in g) for g in lines},{32768});same(power[4],32)
double=[p*(2 if i in (0,4,8) else 1) for i,p in enumerate(power)];same([prod(double[k] for k in g)//32768 for g in lines],[2,2,2,2,2,2,8,2])
tok=payments(5,(2,5,8));same(sorted({p[-1] for p in tok}),list(range(10,41,3)));same({p[:3] for p in tok if p[-1]==22},{(1,4,0),(2,2,1),(3,0,2)});same(min({p[-1] for p in payments(6,(2,5,8))},key=lambda x:abs(26-x)),27)
walk='ECDABCA';same(sorted(''.join(sorted(s)) for s in zip(walk,walk[1:])),sorted(['CE','CD','AD','AB','BC','AC']))
for n,v in [(3,2),(4,9)]:same(len([p for p in perms(n) if all(i!=x for i,x in enumerate(p,1))]),v)
for sides,answer in [(3,96),(4,72)]:same(max(w*l for w,l in it.product(range(1,25),repeat=2) if sides*w+2*l==48),answer)
for k in [2,3]:same(winners(k,True,54)[1:],[n%(k+1)!=1 for n in range(1,55)])
units=lambda v,p,m,d:210*v+30*p+5*m+d
same(units(3,1,0,2)-units(1,5,4,4),units(1,2,1,3));same(units(1,2,3,3),4*units(0,2,2,2))
# M01–M13, final visit.
for n in range(100,1000):
 a,b,c=map(int,str(n))
 if a!=c:
  delta=abs(n-int(str(n)[::-1]));same(delta+int(str(delta).zfill(3)[::-1]),1089)
for a,b,d in it.product(range(1,10),range(10),range(10)):
 if a!=d:
  n=1000*a+110*b+d;delta=abs(n-int(str(n)[::-1]));same(delta+int(str(delta).zfill(4)[::-1]),10989)
for n in range(1,12):
 counts=Counter(sum(i==n for i in cell) for cell in it.product(range(n+1),repeat=3))
 same([counts[i] for i in range(4)],[n**3,3*n*n,3*n,1])
same(7**3-5**3,218)
for b in range(12):
 meetings=[t for t in range(1,15) if 2*t%12==(b-t)%12]
 if b==3:same(meetings[:3],[1,5,9])
 same(bool(meetings),b%3==0)
orders=list(it.permutations('ABCDEF'))
same(sum(p.index('A')<p.index('B') and p.index('C')<p.index('D') for p in orders),180);same(sum(p.index('A')<p.index('B')<p.index('C') and p.index('D')<p.index('E') for p in orders),60)
same(max(tris(a,12-a) for a in range(1,12)),180);same(max(tris(a,11-a) for a in range(1,11)),135)
paths=[p for p in routes(4,4) if all(y<=x for x,y in p)];same(len(paths),14);same(sum((2,2) in p for p in paths),4);same(sum(all(y<x for x,y in p[1:-1]) for p in paths),5)
same([(r,h) for r,h in it.product(range(2,31),range(1,21)) if comb(r,2)==15 and r*h==18],[(6,3)]);same(4*comb(7,2),84)
same((12*10,2*10,12,Fraction(6**2-3**2,2),2*10+12-6,6+3),(120,20,12,Fraction(27,2),26,9))
same(sum(r*r for r in (1,2,3,4))-4*Fraction(5,2)**2,5)
for rad in it.product(range(1,18),repeat=4):
 if sum(rad)==20:assert sum(Fraction(r,2)**2 for r in rad)>=25
for n in range(4,8):same(len(ring(n)),n-1)
s=rails(4,'ABC_');assert tuple('BCA_') in s and tuple('BAC_') not in s
for n in range(2,12):
 counts=Counter(sum(x==0 for x in p) for p in it.product(range(n),repeat=3))
 same([counts[i] for i in range(4)],[(n-1)**3,3*(n-1)**2,3*(n-1),1])
same(sum(y==0 and x in (0,3) and z!=0 for x,y,z in it.product(range(4),repeat=3)),6)
same([tile(2,n) for n in range(7)],[1,1,2,3,5,8,13]);same((tile(2,3)**2,tile(2,2)**2),(9,4))
abcs=list(it.permutations(range(1,10),3));sums=[(a,b,c) for a,b,c in abcs if (10*a+b)+(10*b+a)==11*c];same(len(sums),32);same([sum(t[2]==c for t in sums) for c in range(3,10)],[2,2,4,4,6,6,8]);same([p for a,b,c in abcs if (10*a+b)-(10*b+a)==11*c],[])
# Link the verified problem text to its slot. No answers from any scored bank are exposed.
records=[]
for i in range(53):
 base=data['items'][i%20];item={**base,**base['visits'][i//20]}
 digest=sha256(json.dumps([item[k] for k in ('prompt','solution','transfer_prompt','transfer_solution')],ensure_ascii=False).encode()).hexdigest()
 records.append(dict(slot=(i+1)*7,title=item['title'],verified_problem_text=digest))
assert len(records) == 53 and len({record['slot'] for record in records}) == 53
print('PASS: independent numerical and combinatorial checks for 53 investigations and 53 extensions.')
