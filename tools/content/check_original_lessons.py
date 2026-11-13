"""Independent finite/arithmetical checks for the new content families and capstones."""
from build_original_lessons import family,capstone
from fractions import Fraction as F
from itertools import combinations,permutations,product
import math

def eq(k,n,role,v):
    q=family(k,n,role);a=q['answer']
    assert (F(str(a))==F(str(v)) if str(a) not in ['yes','no','north','east','south','west'] else a==v),(k,n,role,a,v)

def paths(a,b,blocked=()):
    d={}
    for i in range(a+1):
        for j in range(b+1):d[i,j]=0 if (i,j) in blocked else 1 if i==j==0 else d.get((i-1,j),0)+d.get((i,j-1),0)
    return d[a,b]
for n in range(3,12):
    x=n+4
    eq('DIG-01',n,'transfer',198*x+53)
    # Enumerate divisors and square multipliers instead of using exponent formulas.
    N=2**(n-1)*15
    eq('DIV-01',n,'try',sum(N%d==0 for d in range(2,N)))
    N=2**(n-1)*27
    eq('DIV-01',n,'transfer',next(m for m in range(1,100) if math.isqrt(N*m)**2==N*m))
    eq('DIV-02',n,'transfer',next(t for t in range(n+13,n+100) if (t-n)%6==0 and (t-n-4)%8==0))
    eq('DIV-03',n,'transfer',((7*13+3+n%3)**2+n+1)%7)
    eq('DIV-05',n,'try',(3**(4*n+3)+2)%10)
    eq('FRAC-01',2*n,'transfer',next(v for v in range(1,1000) if F(v,2)*F(2,3)==3*(2*n+4)))
    eq('FRAC-02',n,'transfer',next(v for v in range(1,1000) if F(2*x+v,5*x)==1))
    eq('FRAC-03',n,'transfer',100*F(10*x-8*x,10*x))
    eq('FRAC-04',n,'transfer',F(3*x*F(2,3)+2*x*F(1,2),5*x))
    eq('RATE-02',n,'try',1/(F(1,6*x)-F(1,12*x)))
    eq('RATE-03',n,'transfer',F(4*x,1)/(F(2*x,x)+F(2*x,2*x)))
    eq('RATE-04',n,'transfer',F(3*6*x,2+4))
    eq('ALG-01',n,'transfer',next(a for a in range(x+5) if 9*a+5*(x+4-a)==5*(x+4)+12))
    eq('ALG-02',n,'try',next(a for a in range(3*x+9) if a-(3*x+8-a)==x+2))
    eq('ALG-03',n,'transfer',next(b for b in range(100) if (3*x+2*(x+4)-2*b)*2+5*b==6*x+5*(x+4)))
    eq('ALG-04',n,'transfer',next(v for v in range(1,200) if F(v-6,2)+5==x+5))
    nn=2*n;xx=nn+4
    eq('ALG-05',nn,'try',next(v for v in range(5*xx+1) if 3*xx+v-(5*xx-v)==xx))
    eq('ALG-05',n,'transfer',F(7*x-2*3*x,3))
    eq('SEQ-01',n,'try',sum(x+3*i for i in range(8)))
    eq('SEQ-02',n,'transfer',next(k for k in range(1,15) if sum(x*2**i for i in range(k))>x*(2**(n%4+3)-1)))
    L=n+2
    eq('SEQ-03',n,'try',sum('11' not in ''.join(map(str,b)) for b in product([0,1],repeat=L)))
    counts=[0]*(L+1);counts[0]=1
    for i in range(1,L+1):counts[i]=counts[i-1]+(counts[i-3] if i>=3 else 0)
    eq('SEQ-03',n,'transfer',counts[L])
    moves=[1,1,0,-1];eq('SEQ-04',n,'try',sum(moves[i%4] for i in range(6*n+5)))
    eq('COUNT-02',n,'try',sum(1 for cap in range(x) for dep in range(x) if cap!=dep for pair in combinations([i for i in range(x) if i not in [cap,dep]],2)))
    L=n%3+5
    eq('COUNT-03',n,'try',sum(abs(p.index(0)-p.index(1))!=1 and (n<6 or p[0]==2) and (n<9 or p[-1]==3) for p in permutations(range(L))))
    eq('COUNT-04',n,'transfer',sum((i%2==0)!=(i%3==0) for i in range(1,6*x+1)))
    d=n%5+4;eq('COUNT-06',n,'transfer',sum(z.count(2)==1 for z in product(range(1,d+1),repeat=3)))
    eq('LOGIC-01',n,'transfer',next(box for box in [x,x+1,x+2] if sum([box!=x,box==x,box!=x+1])==1))
    eq('LOGIC-04',n,'transfer',max(a for a in range(2,2*x,2) if a<2*x-a and (2*x-a)%2==0))
    # Polygon reflection action: vertex i maps to c-i modulo 2x.
    N=2*x;red={0,1};eq('GEO-04',n,'transfer',sum({(c-i)%N for i in red}==red for c in range(N)))
    eq('GEO-05',n,'try',max(w*(4*x-2*w) for w in range(1,2*x)))
    A=4*x*x-1;eq('GEO-05',n,'transfer',min(2*(a+A//a) for a in range(1,A+1) if A%a==0))
    a=n+2;b=a+1;c=a+2
    counts={j:0 for j in range(4)}
    for i,j,k in product(range(a),range(b),range(c)):
        painted=sum([i==0,i==a-1,j==0,j==b-1,k==0,k==c-1]);counts[painted]=counts.get(painted,0)+1
    eq('SOLID-02',n,'try',counts[2])
    eq('SOLID-02',n,'transfer',sum((k==0)+(k==c-1)==1 for i,j,k in product(range(a),range(b),range(c))))
    a=n%4+3;eq('SPATIAL-01',n,'transfer',paths(a,2,[(1,1)]));eq('SPATIAL-01',n,'try',paths(a,2)-paths(a,2,[(1,1)]))
    eq('SPATIAL-02',n,'transfer',(math.comb(x+1,2)-math.comb(x,2))*math.comb(4,2))
    tokens=['b']*x+['g']*3;eq('DATA-01',n,'try',F(sum(a=='g' and b=='g' for i,a in enumerate(tokens) for j,b in enumerate(tokens) if i!=j),len(tokens)*(len(tokens)-1)))
    eq('DATA-02',n,'transfer',F(sum([14]*x)-19+9,x))
assert capstone(361)['answer']==sum((10*a+b)%3==0 for a,b in permutations(range(6),2) if a)
assert capstone(366)['answer']==paths(4,3,[(1,1),(3,2)])
assert capstone(370)['answer']==max(a*(17-a) for a in range(1,17))

# Content/editorial invariants: every standard lesson grades the final answer
# without prompting students to type an essay or justify their method.
import inspect
from build_original_lessons import build
assert 'In your working:' not in inspect.getsource(build)
assert 'Transfer reflection:' not in inspect.getsource(build)
for method in ('DIG-01','DIG-02','DIG-03','DIG-05','DIV-03','ALG-04','SEQ-04'):
    for n in range(3,12):
        for role in ('try','transfer'):
            problem=family(method,n,role)
            prompt=problem['prompt']
            assert 'In your working' not in prompt,(method,n,role)
            assert 'A meter should add' not in prompt,(method,n,role)
            assert 'A robot spends' not in prompt,(method,n,role)
            assert prompt.strip().endswith('?'),(method,n,role,prompt)
for slot in (367,370):
    assert 'Prove' not in capstone(slot)['prompt']
print('PASS: original problem contexts are concrete, question-only, and answer-first.')

print('PASS: independent enumeration, rational arithmetic, route DP, geometric bounds, probability and capstone checks across all nine supported visits.')
