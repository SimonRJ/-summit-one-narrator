"""Recompute the Upper Primary audit answers using finite models and exact arithmetic."""
import argparse
import hashlib
import json
import os
import sys
import tempfile
from fractions import Fraction
from itertools import accumulate, combinations, combinations_with_replacement, permutations, product
from math import gcd, isqrt, lcm, prod
from pathlib import Path
from statistics import mean, median

from audit_all_lessons import map_course
from build_original_lessons import PRIVATE_SOURCE_ENV, build, private_solutions
from review_helpers import (
    chains, count_in_cuboid, cube_surface, digits, divisors, domino_possible,
    flips_3x3, grid_perimeter, iterate, last_under_digit_budget,
    last_under_print_budget, line_flips_3x3, only, paint_count, pals, prime,
    prob, reachable, rect, reflections, rotations, shift, small_angle,
    surface, switched_states, trail_ends, triangle_area, up_paths, yn,
)
from reviewed_lessons import reviewed_lessons
from check_curated_batch2 import C as BATCH2_ANSWERS
from curated_spatial import RECTANGLES, TILINGS
from curated_data import DATA_REVISITS


def calculated_answers():
    answers = {}
    # ALG-01
    answers.update({
        'O038T': only(n for n in range(37) if 9+4*n==37),
        'O038X': only(n for n in range(12) if 9*n+5*(11-n)==67),
        'O170T': only(n for n in range(30) if 6+2*n==3*n),
        'O170X': only(a for a in range(12) if 9*a+6*(11-a)==84),
        'O202T': only((fee+2)+4*5 for fee in range(32) if fee+4*5==31),
        'O202X': only(n for n in range(30) if 5*min(n,5)+3*max(n-5,0)==43),
        'O261T': min(12*b+3*(13-5*b) for b in range(3)),
        'O261X': only(b for a,b,c in product(range(15),repeat=3) if a+b+c==14 and c==2 and 5*a+10*b+20*c==135),
        'O293T': next(n for n in range(60) if 7*n>=48+3*n),
        'O293X': only(b2+w2 for b2,w1,w2 in product(range(19),repeat=3) if 6+b2+w1+w2==18 and w2==b2+2 and 9*(6+b2)+5*(w1+w2)==130),
    })
    # ALG-02
    answers.update({
        'O040T': only(n for n in range(1,29) if n+n+9==29),
        'O040X': only(a for a,b in combinations(range(1,43),2) if a+b==42 and b-8==a+6),
    })
    # ALG-03
    answers.update({
        'O041T': only(Fraction(l,2) for l in range(2,91) for b in range(2,91) if 2*b+3*l==90 and 2*b+5*l==118),
        'O041X': only(m+b for m,b in product(range(1,38),repeat=2) if 2*m+3*b==37 and 3*m+2*b==33),
        'O050T': only(s for a,s in product(range(1,18),repeat=2) if 2*a+s==17 and a+s==11),
        'O050X': only(t+b for t,b in product(range(1,46),repeat=2) if 3*t+b==36 and 2*t+3*b==45),
        'O193T': only(n for l,m,n in product(range(29),repeat=3) if l+m==21 and m+n==25 and l+n==28),
        'O193X': only(r for s,r in product(range(1,46),repeat=2) if 4*s+3*r==45 and 5*s+2*r==44),
        'O284T': only(s+d for s,d in product(range(1,32),repeat=2) if 3*s+2*d==31 and s+2*d==17),
        'O284X': only(p for a,p,l in product(range(1,16),repeat=3) if a+p+l==13 and 2*a+p==14 and 2*p+l==15),
        'O362T': only(g+h for g,h in product(range(1,39),repeat=2) if 4*g+2*h==38 and 3*g+2*h==31),
        'O362X': only(6*b//r for r,b in product(range(1,49),repeat=2) if 3*r+2*b==48 and 3*r+5*b==84 and (6*b)%r==0),
    })
    # ALG-04
    answers.update({
        'O003T': only(n for n in range(55) if 2*(2*n-9)==54),
        'O003X': only(n for n in range(100) if n%2==0 and (n//2-3)%2==0 and (n//2-3)//2-2+5==12),
        'O044T': only(n for n in range(55) if 2*(2*(n+5)+5)==54),
        'O044X': only(2*n+7 for n in range(50) if 2*n+7==3*n-2),
        'O143T': only(2*h for h in range(10,60) if h-5+h-9==28),
        'O143X': only(n for n in (53,54,55) if (n-4)%3==0),
        'O234T': only(n for n in range(1,58) if 3*(3*n-6)-6==57),
        'O234X': only(n for n in range(1,100) if iterate(Fraction(n),3,lambda v:Fraction(3,2)*v-6)==39),
        'O325T': only(n for n in range(1,20) if (n*n-7)**2-7==74),
        'O325X': only(n for n in range(60) if 3*(2*n-5)-(5*n+2)==11),
    })
    # ALG-05
    answers.update({
        'O046T': only(n for n in range(51) if 30+n==50-n+10),
        'O046X': only(Fraction(k,3) for k in range(147) if 49-Fraction(k,3)==2*(21+Fraction(k,3))),
        'O125T': only(m for m in range(36) if 35-m==17+m),
        'O125X': only(m for m in range(39) if 16+m==2*(38-m)),
        'O216T': only(m for m in range(22) if 26-7+m==14+7-m),
        'O216X': only(a for a in range(41,81) if a-6==80-a+6),
        'O275T': only(a for a in range(27,53) if a-6==52-a),
        'O275X': sum(max(0,n-54//3) for n in (8,17,29)),
        'O307T': only(m for m in range(46) if (25+m)-(45-m)==8),
        'O307X': only(s for s in range(1,74) if 73-s+8==2*(s+5-8)),
    })
    # COUNT-01
    answers.update({
        'O057T': sum(a+b==15 and a%2==1 for a,b in combinations(range(1,15),2)),
        'O057X': sum(a+b+c==15 and c-a<=3 for a,b,c in combinations_with_replacement(range(1,16),3)),
    })
    # COUNT-02
    answers.update({
        'O058T': sum(set((a,b)).isdisjoint(p) for a,b in permutations(range(7),2) for p in combinations(range(7),2)),
        'O058X': sum(d!=0 or 0 in pair for pair in combinations(range(7),2) for d in range(3)),
        'O069T': len(list(product(range(5),combinations(range(3),2)))),
        'O069X': sum(p[0]<4 and sum(v>=4 for v in p)==1 for p in permutations(range(6),3)),
        'O130T': sum(len(set(p)&{0,1})==1 for p in combinations(range(6),2)),
        'O130X': sum(bool(set(p)&{0,1}) and r not in p for p in combinations(range(7),2) for r in range(7)),
        'O221T': len(list(product((0,1),repeat=len(list(combinations(range(4),2)))))),
        'O221X': sum(sum(p)==7 and len(set(p))==2 for p in product(range(1,5),repeat=3)),
        'O312T': sum(a<b for a,b in permutations(range(6),2)),
        'O312X': len({min(p,p[::-1]) for p in permutations(range(7),4) if p[0]<3 and p[-1]<3 and p[1]>=3 and p[2]>=3}),
    })
    # COUNT-03
    answers.update({
        'O023T': sum(abs(p.index('A')-p.index('B'))>1 for p in permutations('ABCDE')),
        'O023X': sum(b-a>1 and sum(abs(w-x)==1 for x in (a,b))==1 for a,b in combinations(range(1,6),2) for w in range(1,6) if w not in (a,b)),
        'O060T': sum(a in (1,8) and b not in (1,8) and abs(a-b)>1 for a,b in permutations(range(1,9),2)),
        'O060X': sum(p.index('E')+3==len(p)-1-p[::-1].index('E') for p in set(permutations('ABCDFEE'))),
        'O088T': sum(p[2]=='C' and set(p[::4])=={'A','B'} for p in permutations('ABCDE')),
        'O088X': sum((b-a) not in (1,5) for a,b in combinations(range(6),2)),
        'O171T': sum(b-a==4 for a,b in combinations(range(1,10),2)),
        'O171X': sum(p[0]==p[-1]=='G' and 'GG' not in ''.join(p) for p in set(permutations('GGGWWWW'))),
        'O262T': sum(abs(p.index('A')-p.index('B')) in (1,4) for p in permutations('ABCDE')),
        'O262X': sum(all(b-a>1 for a,b in zip(c,c[1:])) for c in combinations([1,2,3,5,6,7,8],3)),
        'O353T': sum(all(b-a>1 for a,b in zip(c,c[1:])) for c in combinations(range(7),3)),
        'O353X': sum(p[0]=='R' and p.count('G')==2 and all(a!=b for a,b in zip(p,p[1:])) for p in product('RBG',repeat=5)),
    })
    # COUNT-04
    answers.update({
        'O062T': 42-len(set(range(21))|set(range(14,28))),
        'O062X': sum((n%2==0)!=(n%3==0) for n in range(1,43)),
        'O121T': only(b for b in range(36) if 20+18-b+6==35),
        'O121X': sum(n%4!=0 and n%6!=0 for n in range(1,61)),
        'O153T': only(40-b for b in range(41) if 23+19-b==40),
        'O153X': only(n for n in range(29) if (28-n-1)+2*n+3==12+11+10),
        'O244T': sum(all(n%d for d in (2,3,5)) for n in range(1,61)),
        'O244X': min(b for b in range(18) if 30-(17+19-b)>=3),
        'O303T': only(s for s in range(41) if s+s+5+15==40),
        'O303X': sum(n%5==0 and '5' in str(n) for n in range(1,121)),
        'O335T': 22+18-2*8,
        'O335X': only(b for b in range(29) if (24+5)+28-b==55-13),
    })
    # COUNT-05
    answers.update({
        'O065T': len(set(tuple(sorted((a,(a+d)%14))) for a in range(14) for d in (-1,1,7))),
        'O065X': only(n for n in range(1,43) if 6*n==2*21),
        'O162T': len(list(range(0,9*2+4,2))),
        'O162X': only(n for n in range(25) if 6*n==24*3),
        'O194T': sum(abs(x-a)+abs(y-b)==1 for (x,y),(a,b) in combinations(rect(3,2),2)),
        'O194X': 18-(2*3+2*3-3),
        'O253T': only(n for n in range(8) if 4*3+n==7*2),
        'O253X': 6*10-2*11,
        'O285T': len(list(combinations(range(1,8),2)))+3,
        'O285X': 18*2-3*9+1,
    })
    # COUNT-06
    answers.update({
        'O067T': sum(p.count(1)==1 for p in product(range(1,8),repeat=2)),
        'O067X': sum(p[0]>=4 and len(set(p))==2 for p in product(range(1,6),repeat=3)),
        'O079T': sum(p.count('S')==1 for p in product('SRB',repeat=3)),
        'O079X': sum(p.count(3)==1 and p[-1]>2 for p in product(range(1,5),repeat=4)),
        'O235T': sum((p[0]==0)!=(p[-1]==0) for p in product(range(3),repeat=4)),
        'O235X': sum(sum(p[:3])==10 and p[1]==max(p[:3]) and p[3:] == tuple(sorted(p[3:]))
                     for p in permutations(range(1,7))),
        'O326T': sum((a+b)%2==1 for a,b in product((1,2),(3,4))),
        'O326X': sum(len(set(str(n)))==3 and sum(int(c)%2==0 for c in str(n))==2 for n in range(100,400)),
        'O361T': sum(a*b%10==0 for a,b in combinations(range(1,7),2)),
        'O361X': sum(n%3==0 for n in digits(range(6),2)),
    })
    # DATA-01
    answers.update({
        'O101T': prob(combinations('BBBBBBBGGG',2),lambda p:p.count('G')==2),
        'O101X': prob(range(3,43,3),lambda n:n%2==0),
        'O150T': prob(permutations('GGGSS',2),lambda p:p[1]=='S'),
        'O150X': prob((p for p in product(range(1,7),repeat=2) if sum(p)==9),lambda p:p[0]>4),
        'O241T': prob(combinations(range(1,6),2),lambda p:max(p)==4),
        'O241X': prob(product('RRBBB',repeat=2),lambda p:p[0]==p[1]),
        'O332T': prob((p for p in product('HT',repeat=3) if 'H' in p),lambda p:p.count('H')==2),
        'O332X': prob(combinations(range(1,8),2),lambda p:sum(p)%2==0 and prod(p)%2==1),
    })
    # DATA-02
    answers.update({
        'O026T': mean([12]*7+[20]*3),
        'O026X': Fraction(14*7-19+9,7),
        'O092T': only(n for n in range(61) if (44+n)/5==12),
        'O092X': Fraction(5*15-12+8-17+21,5),
        'O103T': Fraction(sum([16]*3+[8]*5),8),
        'O103X': only(n for n in range(79) if Fraction(78-n,5)==13),
        'O132T': mean(range(7,32,6)),
        'O132X': Fraction(6*12-2*18,4),
        'O191T': mean([8+2,10,13,17-2]),
        'O191X': only(n for n in range(31) if 42+30-n==5*12),
        'O223T': 4*15-8-21,
        'O223X': only(n for n in range(100) if n==2*Fraction(72+n,5)),
        'O282T': abs(mean((11,15,18,21,25))-mean((15,18,21))),
        'O282X': only(set(a+b for a,b in product(range(5,10),range(11,23)) if 4+a+10+b+23==60)),
        'O314T': Fraction(9*20-3*14-3*26,3),
        'O314X': only(Fraction(5*n-4,4) for n in range(30) if 2*n+3==27),
    })
    # DATA-03
    answers.update({
        'O045T': 9*6-(7*6+3),
        'O045X': sum([35+8,35+13]),
    })
    # DIG-01
    answers.update({
        'O002T': sum([99]*7+[37]),
        'O002X': sum([53]+[198]*7),
        'O123T': 4*97+3*104,
        'O123X': 420-2*48-8*20+48+8*19,
        'O214T': only(2*k for k in range(20) if 48*k+52*k==900),
        'O214X': only(n for n in (97,98,99,101,102,103) if sum(x for x in (97,98,99,101,102,103) if x!=n)==498),
        'O305T': only(b for b in range(13) if 51*b+49*(12-b)==606),
        'O305X': only((a+2)*(b-2) for a,b in combinations(range(1,100),2) if a+b==100 and a*b==2419),
    })
    # DIG-02
    answers.update({
        'O004T': sum(n>300 and n%2==0 for n in digits((0,2,4,7),3)),
        'O004X': sum(n%4==0 and n//100%2==1 for n in digits((0,1,2,4,6),3)),
        'O164T': sum(a<b<c and c==5 for a,b,c in permutations(range(1,7),3)),
        'O164X': sum(n%2==0 and str(n)[1]==max(str(n)) for n in digits((0,1,3,5,6),3)),
        'O255T': sum(245<n<300 for n in digits((0,2,3,6,8),3)),
        'O255X': sum(n%5==0 and '23' in str(n) for n in digits(range(1,6),4)),
        'O346T': sum(int(str(n)[0])%2==0 and n%2==1 and '0' in str(n) for n in digits(range(5),4)),
        'O346X': sum(sum(x>y for x,y in zip(p,p[1:]))==1 for p in permutations(range(1,6))),
    })
    # DIG-03
    answers.update({
        'O005T': sum(str(n).count('2') for n in range(320,360)),
        'O005X': sum(len(str(n)) for n in [*range(96,108),*range(996,1004)]),
        'O102T': sum('3' in str(n) for n in range(20,80)),
        'O102X': sum(str(n).count('2') for n in range(2,121,2)),
        'O114T': sum(len(set(str(n)))==len(str(n)) for n in range(80,116)),
        'O114X': last_under_print_budget(40,4,9),
        'O146T': abs(sum(len(str(n)) for n in range(1,26))-sum(len(str(n)) for n in range(90,107))),
        'O146X': sum(f'{n:03d}'.count('0') for n in range(85,124)),
        'O205T': abs(''.join(map(str,range(65,96))).count('7')-''.join(map(str,range(65,96))).count('8')),
        'O205X': last_under_digit_budget(range(1,300,2),149),
        'O237T': sum((n//100==7) != (n%10==7) for n in range(100,1000)),
        'O237X': min(sum(len(str(n))>p and n//10**p%2==1 for n in range(1,231)) for p in range(3)),
        'O296T': sum(str(n).count('3')==2 for n in range(300,350)),
        'O296X': sum(str(n).count('4') for n in range(10,45) if n%10<5 and n//10%2!=n%2),
    })
    # DIG-04
    answers.update({
        'O008T': sum(sum(map(int,str(n)))==12 for n in pals(4)),
        'O008X': min(n for n in pals(4) if n>1411),
        'O055T': only(n for n in pals(4) if n//1000==3 and (n//10%10)*(n//100%10)==49),
        'O055X': sum(n%7==0 for n in pals(3) if 200<=n<=399),
        'O155T': min(n for n in pals(3) if n>593)-max(n for n in pals(3) if n<593),
        'O155X': sum(n//1000%2==1 and sum(map(int,str(n)))%5==0 for n in pals(4)),
        'O187T': only(n for n in pals(3) if 400<n<500 and str(n+11)==str(n+11)[::-1]),
        'O187X': sum(str(a+b)==str(a+b)[::-1] for a,b in combinations([n for n in pals(3) if n//100==4],2)),
        'O246T': min(n for n in pals(3) if isqrt(n)**2==n),
        'O246X': sum(str(b-a)==str(b-a)[::-1] for a,b in zip(pals(3),[*(pals(3)[1:]),1001])),
        'O278T': sum(set(str(n))<=set('258') and len(set(str(n)))==2 for n in pals(4)),
        'O278X': sum(b-a==110 for a,b in combinations(pals(4),2)),
    })
    # DIG-05
    answers.update({
        'O009T': only(a for a in range(10) if (50+a)+(50+a)==114),
        'O009X': only(a for a in range(1,10) if 10*a+7+70+a==132),
        'O010T': only(a for a in range(10) if 82-(40+a)==35),
        'O010X': only(11*a for a,b in permutations(range(10),2) if a and 11*a+30+b==104),
        'O137T': only(11*a for a in range(1,10) if 11*a+17==83),
        'O137X': only(10*b for a,b in permutations(range(1,10),2) if 10*a+6+20+a==10*b),
        'O228T': only(a for a in range(11,100) if a%10 and a-int(str(a)[::-1])==27 and sum(map(int,str(a)))==11),
        'O228X': only(a for a in range(10) if 195<6*(30+a)<215 and 6*(30+a)%10==a),
        'O319T': only(n for n in range(17,100,10) if 100<=3*n<200 and (3*n)//10%10==n//10),
        'O319X': sum(a-c==4 and a+b+c==12 for a,b,c in permutations(range(1,10),3)),
    })
    # DIV-01
    answers.update({
        'O011T': sum(60%k==0 for k in range(2,60)),
        'O011X': max(k for k in range(10) if 8*k+9*k+12*k<=72),
        'O178T': next(k for k in range(30) if (87+k)%6==(87+k)%8==0),
        'O178X': only(n for n in range(21,50) if n%9==0 and len(divisors(n))==6),
        'O269T': min((60+84)//k for k in range(1,61) if 60%k==84%k==0),
        'O269X': sum(30<a*b<70 and a*b%11==0 for a,b in combinations([n for n in range(2,71) if prime(n)],2)),
        'O360T': 150-max(n*n for n in range(20) if n*n<=150),
        'O360X': sum(a*b==90 and (a<10)!=(b<10) for a,b in combinations(range(2,91),2)),
    })
    # DIV-02
    answers.update({
        'O013T': sum(t%14==0 and t%21==0 for t in range(1,127)),
        'O013X': next(t for t in range(16,100) if (t-3)%6==(t-7)%8==0),
        'O219T': sum((t%8==0)!=(t%12==0) for t in range(1,61)),
        'O219X': next(t for t in range(5,100) if (t-1)%4==0 and (t-4)%5==0),
        'O251T': only(t for t in range(1,61) if len(range(t,61,t))==7 and 7*t==56),
        'O251X': yn(any(t%6==t%10==0 and (t-10)%15==0 for t in range(10,70))),
        'O310T': sum(t%10!=0 for t in range(6,91,6)),
        'O310X': sum((t-4)%7==(t-1)%9==0 for t in range(4,150)),
        'O342T': sum(t%5==0 or t%7==0 for t in range(1,71)),
        'O342X': sum(i for i in range(13,30) if lcm(12,i)==60),
    })
    # DIV-03
    answers.update({
        'O001T': (-53)%7,
        'O001X': only({(n*n+4)%7 for n in range(3,200,7)}),
        'O015T': next(i for i in range(8) if (118+i)%8==3),
        'O015X': only(n for n in range(51,90) if n%6==n%7==2),
        'O066T': max(n for n in range(1,59) if (n-4)%7==0),
        'O066X': [k for k in range(1,45) if (4*k)%11==0][1],
        'O110T': (86-86%7+25)%7,
        'O110X': sum((d-1)%7==5 and d%2==0 for d in range(1,32)),
        'O169T': sum(all(t%10 for t in (i,i+1)) for i in range(1,95,2)),
        'O169X': max(n for n in range(100,160) if n%12==5 and n%9==2),
        'O201T': (90-5)%12,
        'O201X': sum(i//8==96//8 for i in range(97,131) if i%8==7),
        'O260T': (83-14)%6,
        'O260X': sum((n*n)%15==4 for n in range(1,101)),
        'O351T': next(n for n in range(100,120) if (n-5)%8==0),
        'O351X': sum(n%12==n*n%12 for n in range(1,201)),
    })
    # DIV-04
    answers.update({
        'O018T': yn(0 in switched_states(6,3,7)),
        'O018X': yn((44-22)%gcd(6,9)==0),
        'O019T': yn((27-9)%gcd(8,12)==0),
        'O019X': yn(any(n.bit_count()==5 for n in switched_states(9,2,4))),
        'O151T': yn(sum((1,3,5,6,8,9))%2==1),
        'O151X': min(x for x in reachable(30,(9,-6),7) if x>40),
        'O242T': max(sum((x+y)%2==0 for x,y in rect(5,4)-set(p)) for p in combinations([q for q in rect(5,4) if sum(q)%2==0],2)),
        'O242X': yn(any(14+8*(2*k-7)==0 for k in range(8))),
        'O333T': min(abs(48-2*n) for n in range(49) if (n-18)%4==0),
        'O333X': yn(any(mask==1<<4 for mask in line_flips_3x3())),
        'O367T': sum(sum(p)>0 and sum(p)%2==0 for k in range(5) for p in combinations((3,5,7,9),k)),
        'O367X': yn(sum(1<<n for n in (0,2,6,8)) in flips_3x3()),
    })
    # DIV-05
    answers.update({
        'O020T': (pow(3,15,10)+2)%10,
        'O020X': next(n for n in range(1,10) if pow(7,n,10)==pow(3,n,10)),
        'O283T': prod(range(1,20,2))%10,
        'O283X': sum(pow(2,n,10)==pow(8,n,10) for n in range(1,101)),
    })
    # FRAC-01
    answers.update({
        'O022T': 84*Fraction(2,3)*Fraction(3,4),
        'O022X': only(n for n in range(1,200) if n%6==0 and n*Fraction(1,2)*Fraction(2,3)==30),
        'O142T': (Fraction(2,3)*90+15)/90,
        'O142X': only(n for n in range(1,301) if n%5==0 and (n-n//5)%3==0 and (n-n//5)//3-n//5==12),
        'O174T': only(n for n in range(13,100) if Fraction(n-12,2)==15),
        'O174X': only(n for n in range(1,200) if Fraction(3,4)*n-Fraction(1,3)*n==25),
        'O233T': len(range(18,36))-len(range(18,36,3)),
        'O233X': only(n for n in range(1,200) if n-Fraction(2,5)*n+Fraction(1,4)*Fraction(2,5)*n==63),
        'O265T': 80*Fraction(3,4)*Fraction(1,2)*Fraction(4,5),
        'O265X': only(n for n in range(1,150) if Fraction(n,3)-6==13),
        'O324T': only(n for n in range(1,200) if Fraction(2,3)*n+12==Fraction(3,4)*n),
        'O324X': only(Fraction(n,2)-12 for n in range(1,100) if Fraction(n-12,2)==18),
    })
    # FRAC-02
    answers.update({
        'O024T': only(8*n for n in range(1,20) if 5*n-3*n==14),
        'O024X': only(m for n,m in product(range(1,50),repeat=2) if 2*n==14 and 2*n+m==5*n),
    })
    # FRAC-03
    answers.update({
        'O025T': 140*Fraction(75,100)+7,
        'O025X': 100*Fraction(70-56,70),
        'O029T': 49-60*Fraction(80,100),
        'O029X': only(p for p in range(1,100) if p*Fraction(3,4)*Fraction(6,5)==54),
        'O165T': 100*Fraction(80-68,80),
        'O165X': abs(48*Fraction(5,4)-72*Fraction(3,4)),
        'O347T': only(p for p in range(1,101) if Fraction(9,10)*p==Fraction(3,4)*72),
        'O347X': only(p for p in range(1,200) if Fraction(7,10)*p==Fraction(4,5)*p-6),
    })
    # FRAC-04
    answers.update({
        'O027T': sum(n-n//k for n,k in ((42,3),(28,2))),
        'O027X': Fraction(sum(n-n//k for n,k in ((21,3),(14,2))),35),
        'O115T': Fraction(sum(n//k for n,k in ((8,2),(12,3),(16,4))),8+12+16),
        'O115X': only(2*n for n in range(1,80) if n%12==0 and Fraction(3,4)*n+Fraction(1,3)*n==13),
        'O206T': only(6+(40-a)//2 for a in range(41) if a%4==0 and a//4==6),
        'O206X': Fraction(4+6,4+16+6),
        'O297T': only(k for k in range(30) if Fraction(16,24+k)==Fraction(1,2)),
        'O297X': only(c for c in range(49) if Fraction(48-c,3)+Fraction(3*c,4)==26),
    })
    # GEO-01
    answers.update({
        'O043T': grid_perimeter(rect(9,3)|shift(rect(6,4),9,0)),
        'O043X': grid_perimeter(rect(13,9)-shift(rect(2,3),5,0)),
        'O076T': grid_perimeter(rect(12,8)-shift(rect(5,3),7,0)),
        'O076X': grid_perimeter(rect(3,3)-{(1,1)}|{(3,0)}),
        'O108T': grid_perimeter(rect(3,3)|shift(rect(4,4),3,0)|shift(rect(5,5),7,0)),
        'O108X': grid_perimeter(rect(14,9)-shift(rect(2,3),2,0)-shift(rect(2,4),9,5)),
        'O199T': grid_perimeter(rect(10,10)-set().union(*(shift(rect(2,2),x,y) for x in (0,8) for y in (0,8)))),
        'O199X': only(k for k in range(1,6) if 2*(7+5+4+3)-2*k==34),
        'O290T': grid_perimeter(rect(13,13)-shift(rect(4,4),4,4)),
        'O290X': only(a for a,b,c in product(range(1,15),repeat=3) if a+b+c==15 and a==c and 2*(b+12)==34),
    })
    # GEO-02
    answers.update({
        'O061T': 14*9-triangle_area(((0,0),(14,0),(5,9))),
        'O061X': triangle_area(((0,0),(14,0),(4,6)))-triangle_area(((0,0),(14,0),(4,3))),
        'O078T': triangle_area(((0,0),(8,0),(4,Fraction(7,2)))),
        'O078X': only(a for a in range(1,20) if 6*a+6*(a+5)==102),
        'O149T': max(triangle_area(t) for t in [((0,0),(3,0),(2,12)),((3,0),(9,0),(2,12))]),
        'O149X': triangle_area(((6,0),(12,2),(0,8))),
        'O181T': triangle_area(((2,0),(5,0),(0,12))),
        'O181X': triangle_area(((0,0),(16,0),(3,8)))-triangle_area(((0,0),(8,0),(Fraction(3,2),4))),
        'O331T': Fraction(13*7,2)-Fraction(13*4,2),
        'O331X': only(b for b,h in product(range(1,85),range(4,85)) if b*h==84 and b*(h-3)==48),
        'O365T': triangle_area(((4,0),(12,0),(5,5))) + triangle_area(((12,0),(Fraction(29,2),Fraction(5,2)),(5,5))),
        'O365X': triangle_area(((0,0),(30,0),(30,6)))/(30*18),
    })
    # GEO-03
    answers.update({
        'O081T': only(a for a in range(180) if 2*a+66==180),
        'O081X': only(a for a in range(180) if a+38+(180-113)==180),
        'O131T': only(a for a in range(90) if (90-a)-a==18),
        'O131X': min(58,89,only(a for a in range(1,180) if 58+89+2*a+a==360)),
        'O190T': next(a for a in range(360) if (47-28+a)%360==180),
        'O190X': small_angle(6*30,Fraction(30)*(3+Fraction(30,60))),
        'O222T': only(b for a,b in combinations(range(1,90),2) if a+b==90 and b-a==14),
        'O222X': only(180-c for c in range(1,180) if (180-132)+(180-114)+c==180),
        'O281T': only(a+36 for a in range(1,145) if a+a+a+36==180),
        'O281X': only(a for a in range(1,181) if a+3*a+3*a-16==180 and a<3*a-16<3*a),
        'O313T': only(a for a in range(1,180) if 5*a+a==180),
        'O313X': min(180-36-x for x,y in permutations(range(1,109),2) if x+y==108 and x-y==18 for x in (x,y)),
    })
    # GEO-04
    answers.update({
        'O083T': len(rotations('bg'*7)),
        'O083X': len(reflections('rr'+'b'*12)),
        'O172T': len(rotations('x...x...')),
        'O172X': len(reflections('rbbr')),
        'O263T': len(rotations('sd.sd.')),
        'O263X': len(reflections('xx..')),
        'O354T': len(rotations('rwb'*4)),
        'O354X': len(rotations('sdodldld'))+len(reflections('sdodldld'))-1,
    })
    # GEO-05
    answers.update({
        'O053T': max(x*y for x,y in product(range(1,29),repeat=2) if 2*x+y==28),
        'O053X': min(2*(a+b) for a,b in product(divisors(195),repeat=2) if a*b==195),
        'O085T': max(a*b for a,b in product(range(1,12),repeat=2) if 2*(a+b)==24),
        'O085X': min(2*a+b for a,b in combinations(range(4,97),2) if a%2==0 and a*b==96),
        'O122T': max(2*a for a,b in combinations(range(1,15),2) if a+b==15 and b>2),
        'O122X': max(a*b for a,b in combinations(range(1,18),2) if a+b==18 and b>=2*a),
        'O213T': max(a for a,b in combinations(range(2,46),2) if a*b==45),
        'O213X': max(s*l for s,l in product(range(1,36),repeat=2) if s<=l and 3*s+2*l==35),
        'O370T': only(a for a,b in combinations(range(1,20),2) if a+b==20 and (a+2)*(b-2)-a*b==12),
        'O370X': only(a for a,b in combinations(range(1,18),2) if 2*(a+b)==36 and a*b==9*9-16),
    })
    # LOGIC-01
    answers.update({
        'O033T': only(code for code in range(10) for a,b in product((False,True),repeat=2) if a==(not a and not b) and b==(code==7)),
        'O033X': only(n for n in (7,8,9) if sum((n!=7,n==7,n!=8))==1),
        'O068T': only(c for c in ('red','blue','green') if c!='blue' and not(c!='green')),
        'O068X': only(n for n in range(1,5) if sum((n%2==1,n>2,n==2))==2),
        'O099T': only(n for n in range(1,4) if len(set((n!=1,n!=2,n==3)))==1),
        'O099X': only(n for n in range(1,5) if sum((n in (1,2),n in (2,3),n in (3,4),n==2))==3),
        'O185T': only(n for n in (4,6,8,10) if sum((n<8,n>4,n in (8,10)))==1),
        'O185X': only(name for name in ('Ana','Ben','Cleo') if (name=='Ana',name=='Ben',name=='Cleo')==(name=='Ben',name=='Ana',name=='Cleo')),
        'O276T': only(n for n in range(1,6) if n%2 and n>2 and n%3==0),
        'O276X': only(n for n in range(1,6) if n in (2,5) and sum((n%2==0,n>2,n in (2,5),n<4))==2),
    })
    # LOGIC-02
    answers.update({
        'O071T': only(n for n in range(1,25) if sum(range(n-1,n+2))==24),
        'O071X': only(n for n in (24,30,36,42) if n%4==0 and len(divisors(n))==9),
    })
    # LOGIC-03
    answers.update({
        'O073T': sum((12,17,15))-sum((11,16)),
        'O073X': 70-49+6,
        'O117T': 15+19-16,
        'O117X': only(n for n in range(19) if 22+2*n==36),
        'O267T': (17+21-14)-14,
        'O267X': sum([25,20,20]+[20,25,20]),
        'O299T': only(set(c for a,b,c,d,e in product(range(1,16),repeat=5) if a+b+c==27 and c+d+e==32 and a+b+c+d+e==48)),
        'O299X': 20+25-14-7-10,
        'O358T': sum((15,21,18,26))//4,
        'O358X': 127-2*48-2*6,
    })
    # LOGIC-04
    answers.update({
        'O074T': only(a for a,b in combinations(range(1,41),2) if a*b==40 and b-a==3),
        'O074X': max(a for a,b in combinations(range(2,15,2),2) if a+b==14),
        'O158T': min(b for a,b in combinations(range(1,121),2) if a*b==120 and a%3==0 and b%5==0),
        'O158X': only({b for a,b in combinations(range(1,50),2) if b>4 and a*b==2*a*(b-4)}),
        'O249T': sum(3*a+5*b==24 for a,b in product(range(1,9),repeat=2)),
        'O249X': only(a+b for a,b in combinations(range(2,145,2),2) if a*b==144 and a+b<40 and b==4*a),
    })
    # RATE-01
    answers.update({
        'O030T': Fraction(sum(6 for n in range(1,8)),18),
        'O030X': range(0,9*8,8)[-1]-range(0,7*8,8)[-1],
        'O156T': Fraction(sum([12,12,12,8,8]),13),
        'O156X': len(range(0,(13-1)*5+1,4)),
        'O188T': len(range(0,29,2)),
        'O188X': 24+sum(2 for x in range(2,7)),
        'O247T': sum(n%3!=0 for n in range(1,len(range(0,49,4)))),
        'O247X': (lambda t:t[2]-t[0])([n for n in range(3,160) if n%7==0 and (n-3)%5==0]),
        'O279T': only((17-9)*p for p in range(1,40) if (7-1)*p==30),
        'O279X': sum(i%4==0 and (22-i)%3==0 for i in range(1,22)),
        'O338T': only(d for d in range(1,106) if (9-2)*d==21*5),
        'O338X': sorted(set(range(0,121,6))|set(range(3,120,12)))[24],
    })
    # RATE-02
    answers.update({
        'O031T': 1/(Fraction(1,42)-Fraction(1,84)),
        'O031X': only(h for h in range(1,85) if h*(42-14)==84),
        'O086T': 18*12//6+20*12//5,
        'O086X': only(t for t in range(20) if 24+15*t-3*t==120),
        'O106T': sum(6+(4 if t>=3 else 0) for t in range(10)),
        'O106X': only(t for t in range(40) if 4*t+3*max(0,t-5)==62),
        'O138T': only(t for t in range(30) if 10*t==32+6*t),
        'O138X': 12*Fraction(1,3)+Fraction(2,3)/(Fraction(1,12)+Fraction(1,18)),
        'O197T': Fraction(80,5)-Fraction(80,8),
        'O197X': only(m for m,a in product(range(21),repeat=2) if (m+a)*8==120 and (m+2*a)*6==120),
        'O229T': only(t for t in range(30) if 12*t-2*min(t,3)==90),
        'O229X': only(95//(a+b+c) for a,b,c in product(range(1,16),repeat=3) if a+b==10 and a+c==13 and b+c==15),
    })
    # RATE-03
    answers.update({
        'O034T': Fraction(15*28+10*0+30*14,60),
        'O034X': Fraction(2*14)/(Fraction(14,7)+Fraction(14,14)),
        'O039T': Fraction(20*36+10*48,60),
        'O039X': Fraction(24)/(Fraction(12,12)+Fraction(12,18)),
        'O179T': Fraction(5*60,18+6+12),
        'O179X': 20/(Fraction(30,15)-Fraction(10,12)),
        'O270T': abs(Fraction(24*60,12)-(Fraction(24*60,16)+20)),
        'O270X': only(abs(a-b) for a,b in product(range(37),repeat=2) if a+b==36 and a==36//3),
        'O368T': only(d for d in range(9,70) if Fraction(d-8,2)==Fraction(36*15,60)),
        'O368X': only(v for v in range(1,100) if Fraction(20*15+30*v,50)==18),
    })
    # RATE-04
    answers.update({
        'O037T': only(t for t in range(25) if 5*t==21+2*t),
        'O037X': [t for t in range(1,43) if (2*t+4*t)%42==0][2],
        'O129T': only(t for t in range(30) if 3*t==63-4*t),
        'O129X': only(t for t in (Fraction(k,7) for k in range(50,150)) if 3*t+4*(t-2)==70),
        'O220T': next(t for t in range(1,121) if (5*t-3*t)%120==0),
        'O220X': only(t for t in range(40) if abs(6*t-4*t)==14),
        'O311T': only(t for t in range(30) if 9*t==4*(t+5)),
        'O311X': Fraction(180-72)/(Fraction(72,1)/Fraction(180,36)),
    })
    # SEQ-01
    answers.update({
        'O047T': sum(list(accumulate([7]+[3]*7))),
        'O047X': only(k for k,v in enumerate(accumulate([7]+[4]*10),1) if v==31),
        'O134T': list(accumulate([5]+[4]*4))[4]-list(accumulate([5]+[4]*4))[1],
        'O134X': only(sum(a+k*d for k in range(7)) for a,d in product(range(1,31),repeat=2) if a+2*d==18 and a+5*d==30),
        'O166T': only(6+2*d for d in range(1,16) if sum(6+i*d for i in range(3))==27),
        'O166X': next(k for k in range(40) if 7+5*k>30+3*k),
        'O257T': only(n for n in range(1,30) if 3*n-(n-1)==19),
        'O257X': only(sum(a+3*k for k in range(12)) for a in range(1,88) if sum(a+3*k for k in range(6))==87),
        'O348T': next(i+1 for i,s in enumerate(accumulate(range(4,100,3))) if s>100),
        'O348X': sum(list(accumulate([2]+[4]*14))[::2]),
    })
    # SEQ-02
    answers.update({
        'O051T': iterate(7,5,lambda n:n*2),
        'O051X': next(i for i,n in enumerate(accumulate(7*2**k for k in range(12)),1) if n>441),
        'O059T': len(list(product((0,1),repeat=3))),
        'O059X': next(k for k in range(10) if Fraction(96,2**k)<5),
        'O116T': iterate(3,3,lambda n:n+n+1),
        'O116X': next(d for d in range(1,20) if 4*2**d>19+7*d),
        'O207T': len(list(product(range(3),repeat=4)))-len(list(product(range(3),repeat=2))),
        'O207X': only(a*2**5 for a in (Fraction(i,2) for i in range(40)) if a*2**3==24+12*3),
        'O298T': sum(3*2**k for k in range(2,6)),
        'O298X': only(16*n for n in range(1,60) if 16*n-11==5*(n+11)),
    })
    # SEQ-03
    answers.update({
        'O012T': sum(not any(a and b for a,b in zip(p,p[1:])) for p in product((0,1),repeat=5)),
        'O012X': len(chains(7,(1,3))),
        'O052T': sum(p.count(2)==1 for p in chains(5,(1,2))),
        'O052X': sum(sum(p)==9 and p.count(3)==2 for p in product((1,2,3),repeat=4)),
        'O157T': sum(p[0]==2 for p in chains(6,(1,2))),
        'O157X': sum(4 not in list(accumulate(p)) for p in chains(7,(1,2))),
        'O248T': sum('AA' not in ''.join(p) and p[-2:]==('B','B') for p in product('AB',repeat=4)),
        'O248X': sum(p.count(2)==2 and p[::-1].index(2)+p.index(2)<=len(p)-4 for p in chains(8,(1,2))),
        'O339T': sum(6 in list(accumulate(p)) for p in chains(12,(2,3))),
        'O339X': sum(all((a,b)!=(3,3) for a,b in zip(p,p[1:])) for p in chains(11,(2,3))),
    })
    # SEQ-04
    answers.update({
        'O054T': sum(([1,1,0,-1]*6)[:23]),
        'O054X': ([1,2,3]*15)[43],
    })
    # SOLID-01
    answers.update({
        'O006T': sum(len(rect(w,h)) for w,h in ((7,5),(6,4),(5,3))),
        'O006X': sum(not (y==2 and z in (1,2)) for x,y,z in product(range(7),range(6),range(4))),
        'O072T': len(set(product(range(4),range(4),range(3)))-{(0,0,z) for z in range(3)}),
        'O072X': only(n for n in range(1,16) if len(list(product(range(n),range(1),range(3))))==15),
        'O087T': sum(len(rect(w,h)) for w,h in ((6,3),(6,3),(4,3),(2,3))),
        'O087X': sum(not (z==2 and (x==2 or y==2)) for x,y,z in product(range(5),repeat=3)),
        'O163T': sum(len(range(1,h)) for h in (3,1,2,4,1,3)),
        'O163X': only(n+1 for n in range(10) if 20*n+11==91),
        'O195T': sum(not ((z==2 and x<2 and y<2) or (z==0 and x==0 and y<3)) for x,y,z in product(range(6),range(4),range(3))),
        'O195X': sum(x>=4 and y>=2 for x,y,z in product(range(6),range(4),range(5))),
        'O254T': only(h for h in range(1,13) if 2*sum([1,2,3,h])==24),
        'O254X': len(set(product(range(3),range(3),range(5)))|set(product(range(3),range(5),range(3)))),
        'O286T': sum((16,16,16,16,8))//9,
        'O286X': sum(not (z%2==0 and x in (0,3) and y in (0,3)) for x,y,z in product(range(4),range(4),range(6))),
        'O345T': sum(1 for h in (1,4,3,2,4,1) for z in range(h,4)),
        'O345X': only(h for h in range(1,21) if 2*len(rect(4,5))+h*len(rect(2,2))==3*len(rect(6,4))),
    })
    # SOLID-02
    answers.update({
        'O089T': paint_count((5,6,7),range(6),2),
        'O089X': sum(paint_count((5,6,7),(4,5),n) for n in (1,2)),
        'O113T': paint_count((4,5,6),(2,5),2),
        'O113X': sum(x==2 and 0<y<3 and 0<z<2 for x,y,z in product(range(3),range(4),range(3))),
        'O145T': paint_count((4,5,6),range(6),0),
        'O145X': only(n for n in range(3,20) if paint_count((n,4,5),range(6),0)==24),
        'O204T': paint_count((5,4,2),(0,1,2,3),1),
        'O204X': count_in_cuboid((5,5,5),range(6),1,lambda x,y,z:(x,y)!=(2,2)),
        'O295T': count_in_cuboid((3,4,5),(4,5),0,lambda x,y,z:z!=2),
        'O295X': only(n for n in range(3,20) if paint_count((n,3,3),range(6),2)==3*paint_count((n,3,3),range(6),3)),
        'O327T': sum(sum((x+dx,y+dy,z+dz) in set(product(range(1,5),range(1,4),range(1,3))) for dx,dy,dz in ((1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)))>0 for x,y,z in set(product(range(6),range(5),range(4)))-set(product(range(1,5),range(1,4),range(1,3)))),
        'O327X': sum((x in (0,4))+(y in (0,4))==2 and z not in (0,4) for x,y,z in product(range(5),repeat=3)),
    })
    # SOLID-03
    answers.update({
        'O090T': surface((7,4,3))-7*4,
        'O090X': 2*surface((7,7,Fraction(7,2))),
        'O186T': surface((9,4,3))-9*4,
        'O186X': 2*surface((4,4,4))-surface((8,4,4)),
        'O277T': surface((4,6,5))+surface((5,6,5))-surface((9,6,5)),
        'O277X': cube_surface(set(product(range(4),repeat=3))-{(0,0,0),(3,2,2)}),
    })
    # SPATIAL-01
    answers.update({
        'O093T': sum((1,1) in p for p in up_paths(6,2)),
        'O093X': sum(not any(e in list(zip(p,p[1:])) for e in (((2,0),(2,1)),((2,1),(2,2)))) for p in up_paths(4,2)),
        'O227T': sum(p[0]=='U' for p in set(permutations('RRRRUU'))),
        'O227X': sum(((1,2) in p)!=((3,1) in p) for p in up_paths(4,3)),
        'O318T': sum('UU' not in ''.join(p) for p in set(permutations('RRRRUU'))),
        'O318X': sum(p[0]=='R' and p[1]=='U' and sum(a!=b for a,b in zip(p,p[1:]))==3 for p in set(permutations('RRRRUUUU'))),
        'O366T': sum(p[0]=='U' and sum(a!=b for a,b in zip(p,p[1:]))==3 for p in set(permutations('RRRRRUU'))),
        'O366X': sum((1,1) not in p and (3,2) not in p for p in up_paths(4,3)),
    })
    # SPATIAL-02
    answers.update({
        'O017T': sum(a==0 for a,b in combinations(range(7),2) for c,d in combinations(range(4),2)),
        'O017X': len(list(combinations(range(8),2)))*6-len(list(combinations(range(7),2)))*6,
    })
    # SPATIAL-03
    answers.update({
        'O036T': (3*3)%2+(2*6)%2,
        'O036X': yn(sum((-1)**(x+y) for x,y in rect(14,2)-{(0,0),(13,1)})==0),
    })
    # SPATIAL-04
    answers.update({
        'O100T': yn(any(x!='A' for x in trail_ends(('AB','BC','CD','DE','EF','FG','GA','AD'),'A'))),
        'O100X': yn('A' in trail_ends(('AB','BC','CD','DE','EF','FG','GA','AH','HI','IJ','JK','KL','LM','MN','NA'),'A')),
        'O109T': only(set(trail_ends(('AB','BC','CD','DA','AC'),'A'))),
        'O109X': min(n for n in (0,1) if 'A' in trail_ends(('AB','BC','CD','DA','EA')+('EA',)*n,'A')),
        'O200T': only(n for n in 'ABCDE' if 'E' in trail_ends(('AB','BC','CA','CD','DE'),n)),
        'O200X': len(list(trail_ends(('AB','BC','CA','AD','DE','EF','FA'),'A'))),
        'O291T': sum('A' in trail_ends(tuple(e for e in ('AB','BC','CD','DA','BD') if e!=rem),'A') for rem in ('AB','BC','CD','DA','BD')),
        'O291X': sum(n=='B' for n in trail_ends(('AB','BC','CA','BD','DA'),'A')),
    })
    answers.update({
        'O120X': only(16*n for n in range(1,50) if 8*(n+5)==18*n),
        'O139T': (5*2026)%12,
        'O167T': only(n for n in (18,22,27,34) if max({18,22,27,34}-{n})-min({18,22,27,34}-{n})==12),
        'O209T': sum(b-a==d-c for a,b in combinations((0,1,3,4,7),2)
                     for c,d in combinations((0,1,3,4),2)),
        'O226T': only(order[1] for order in permutations(('Bugs','Clouds','Rivers','Stars'))
                      if order.index('Bugs') < order.index('Clouds') < order.index('Stars')
                      and order.index('Rivers') < order.index('Clouds')
                      and order.index('Stars') - order.index('Bugs') == 2),
        'O243X': only(t+f for t,f in product(range(97),range(20)) if 10*t+50*f==960 and t==f+6),
        'O302X': only(4*c+3*b for c,b in product(range(1,21),repeat=2) if c+b==21 and 4*c+3*b==2*c+8*b),
        'O321X': sum(range(1,101))%7,
        'O334T': only(d for a,b,c,d in product(range(28),repeat=4) if a+b==22 and b+c==27 and c+d==24 and c==2*a),
    })
    return answers


def normal(value):
    try:
        return Fraction(str(value)).limit_denominator(10000)
    except ValueError:
        return str(value).lower()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--solutions', default=os.environ.get(PRIVATE_SOURCE_ENV))
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    with tempfile.TemporaryDirectory() as tmp:
        directory = Path(tmp)
        build(map_course(), directory, public_only=True)
        rows = {p['id']: p for p in json.loads((directory / 'lesson-prompts.json').read_text())}
        manifest = json.loads((directory / 'lesson-manifest.json').read_text())
    published = json.loads((root / 'data/lesson-challenges.json').read_text())
    assert manifest == published, 'Regenerate the public lesson manifest from the current generator'
    checked = calculated_answers()
    assert checked.keys() == reviewed_lessons().keys(), 'A reviewed problem is missing its calculation'
    retained = {}
    for item in manifest['items']:
        pid = item['id']
        if pid in checked:
            continue
        skill, visit, role = item['skill'], item['visit'], item['role']
        if (skill, role, visit) in BATCH2_ANSWERS:
            answer = BATCH2_ANSWERS[skill, role, visit]()
        else:
            catalogue = {'SPATIAL-02': RECTANGLES, 'SPATIAL-03': TILINGS, 'DATA-03': DATA_REVISITS}
            answer = catalogue[skill][visit, role]['answer']
        retained[pid] = answer
    checked.update(retained)
    assert checked.keys() == rows.keys(), 'A canonical lesson is missing its calculation'

    # Pin the stems independently of the public content audit. If a problem is
    # reworded, check it again against the private answers before refreshing this list.
    approved_stems = json.loads((root / 'tools/content/reviewed_stem_signatures.json').read_text())
    assert approved_stems == {pid: hashlib.sha256(row['prompt'].encode()).hexdigest()
                             for pid, row in rows.items()}, 'A checked prompt has changed'

    if args.solutions:
        solutions = private_solutions(args.solutions)
        assert checked.keys() == solutions.keys(), 'The private answer source has different lesson IDs'
        for pid, value in checked.items():
            actual = solutions[pid]['answer']
            assert normal(actual) == normal(value), f'{pid}: authored answer differs from the calculation'
        print(f'PASS: verified {len(checked)} private keys against the answer checks.')
    print(f'PASS: recomputed answers and matched checked stems and the public manifest for {len(checked)} lessons.')


if __name__ == '__main__':
    main()
