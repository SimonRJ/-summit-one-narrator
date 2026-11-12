"""Breadth and placement changes for the previously unattempted AMC set.

Keep the authored difficulty progression in small bands; change topic positions
between papers. Never shuffle a sitting or an already attempted paper at runtime.
"""
from core import *
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from build_learning_map import teaching_map

def apply_coverage(p):
 if p['exam']['max_score']!=135:return p
 index=int(p['exam']['id'][-2:]);raw=[]
 for q in p['questions']:
  value=q['metadata']['expected_value']
  raw.append(item(q['stem'],value,q['explanation'],q['category'],[x for x in q['choices'] if x!=value] if q['choices'] else None,figure=q['figure_svg']))
 for slot,skill in {3:{28:'COUNT-04'},5:{28:'DIV-03'},8:{27:'SEQ-03'},10:{30:'COUNT-06'}}.get(index,{}).items():raw[slot-1]['category']=skill
 if index==10:
  raw[0]=item('Which number is closest to 49 × 21?',1000,'Estimate with 50×20=1000. The exact product is 49×(20+1)=980+49=1029. Its distances from 800, 900, 1000, 1100 and 1200 are 229, 129, 29, 71 and 171, so 1000 is closest.','DIG-01',[800,900,1100,1200],check=min([800,900,1000,1100,1200],key=lambda x:abs(x-49*21)))
 if index==2:
  triples=[(a,b,c) for a in range(1,24) for b in range(a,24) for c in range(b,24) if a+b+c==24 and a*b+a*c+b*c==176]
  raw[28]=item('A closed rectangular box has positive whole-number side lengths. The total length of its twelve edges is 96 cm, and its surface area is 352 cm². What is the greatest possible volume of the box, in cubic centimetres?',384,'Call the lengths a ≤ b ≤ c. The twelve edges give a+b+c=24, and the six faces give ab+ac+bc=176. The shortest side a is at most 8. For a=1 through 8, the required products bc are 153,132,113,96,81,68,57,48; the required sums b+c are 23,22,21,20,19,18,17,16. List the factor pairs of each product and keep only pairs with the required sum and b≥a. Only a=4,b=8,c=12 survives. (The pair 4,12 when a=8 is the same box, with sides out of order.) Its volume is 4×8×12=384. Check: the edge total is 4×24=96 and the surface area is 2×(32+48+96)=352.', 'GEO-05',check=max(a*b*c for a,b,c in triples),figure=cuboid('a','b','c'))
 if index==3:
  # Two overlapping perpendicular strips; derive their common width first.
  raw[28]=item('A 24 m by 18 m rectangular garden has two straight paths of the same whole-number width. One runs from left to right across the full garden; the other runs from top to bottom. Their intersection is counted only once. Together the paths cover 117 m². The paths separate the remaining garden into four rectangles. What is the sum of the perimeters of those four rectangles, in metres?',144,'Let the path width be w. Adding strip areas counts their square intersection twice, so 24w+18w−w²=117. Among whole-number widths from 1 to 18, the covered area increases as w increases: w=2 gives 80, w=3 gives 117, and w=4 gives 152. Thus w=3. The two remaining horizontal lengths together are 24−3=21; the two remaining vertical lengths together are 18−3=15. In the sum of the four rectangle perimeters, each of these lengths is counted four times. The sum is 4×(21+15)=144 metres. This works wherever the two paths cross inside the garden, even if they are not centred.','GEO-02',check=4*(24+18-2*3),figure=svg('<rect x="45" y="35" width="300" height="180" fill="#d9ebe8"/><rect x="45" y="110" width="300" height="30" fill="#efce83"/><rect x="165" y="35" width="38" height="180" fill="#efce83"/>'+text(190,25,'24 m')+text(385,130,'18 m')+text(275,100,'same width',14),h=245,label='Two perpendicular paths of equal width inside a 24 m by 18 m garden. Not to scale.'))
 if index==5:
  raw[29]=item('Three jars A, B and C contain 288 counters altogether. First, one third of the counters in A are moved to B. Next, one quarter of the counters now in B are moved to C. Finally, one fifth of the counters now in C are moved to A. All three jars then contain the same number of counters. How many counters were in A at the start?',108,'The total stays 288, so each final jar has 96. Undo the last transfer: C retained four fifths of its previous amount, so it previously held 120 and sent 24 to A. Just before that move, the amounts were A=72, B=96, C=120. Undo the second: B retained three quarters, so it previously held 128 and sent 32 to C; the amounts were 72,128,88. Undo the first: A retained two thirds, so it started with 108 and sent 36 to B. Initial amounts were 108,92,88. Check forward: 72,128,88 → 72,96,120 → 96,96,96.','ALG-04',check=F(96-F(96,4),F(2,3)))
 if index==6:
  raw[28]=item('A courier cycles from Harbour to Hill at a constant 12 km/h. Another courier leaves Harbour 30 minutes later and follows the same route at 18 km/h. They reach Hill at the same instant. The second courier immediately returns to Harbour at 9 km/h. How many minutes after the first courier originally left does the second courier arrive back at Harbour?',210,'The first courier has a 12×1/2=6 km head start. The second closes the gap at 18−12=6 km/h, so catches the first after one hour of cycling. Hill is therefore 18 km from Harbour. The first leg ends 90 minutes after the first departure. The return takes 18÷9=2 hours=120 minutes. The requested total is 90+120=210 minutes. Check the outward times: 18/12=1.5 hours and 18/18=1 hour, a difference of 30 minutes.','RATE-04',check=F(18,12)*60+F(18,9)*60)
 if index==7:
  cubes={(x,y,z) for x in range(5) for y in range(5) for z in range(5) if not (x==2 and y==2)}
  faces=lambda p:sum((p[0]+dx,p[1]+dy,p[2]+dz) not in cubes for dx,dy,dz in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)])
  count=sum(faces(p)==2 for p in cubes)
  raw[29]=item('A 5-by-5-by-5 cube of unit cubes has its central vertical column of five cubes removed, leaving a square tunnel open at the top and bottom. Every exposed face is painted, including the four walls of the tunnel. How many remaining unit cubes have exactly two painted faces?',44,'Separate the outside from the tunnel. Along the twelve outside edges, omit the eight corners; each edge contributes 3 cubes with exactly two painted faces, giving 36. The four cubes immediately beside the tunnel on the top face each have one top face and one tunnel face painted. The bottom contributes four more. Cubes beside the tunnel at the three middle levels have only one painted face, and no cube touches two tunnel walls. Total: 36+4+4=44. Check that the removed column contains no outside edge cubes.','SOLID-02',check=count,figure=svg('<rect x="85" y="30" width="250" height="175" fill="#a9d6c9"/><rect x="185" y="100" width="50" height="35" fill="white"/>'+''.join(f'<path d="M{85+50*i},30V205M85,{30+35*i}H335" stroke="#375e67"/>' for i in range(1,5))+text(210,232,'Top view: centre column removed',15),h=250,label='Top view of a 5-by-5 array with the central square removed. The same square tunnel continues through all five layers.'))
 # Shuffle only nearby positions of comparable intended difficulty. The final
 # two retain their editorial order, while their domains now vary across papers.
 rng=random.Random(20261113+index)
 order=[]
 for lo,hi in [(0,5),(5,10),(10,15),(15,20),(20,25),(25,28),(28,30)]:
  segment=list(range(lo,hi))
  if lo<28:rng.shuffle(segment)
  order+=segment
 result=paper('amc',index,[raw[i] for i in order])
 result['exam']['metadata'].update(version='20261113-coverage',difficulty_note='Editorially calibrated in bands; not empirically equated to an official paper.',topic_order='Varies between papers, fixed within each saved paper.')
 for q,original in zip(result['questions'],order):
  q['metadata'].update(version='20261113-coverage',authoring_slot=original+1,learning_map=teaching_map(q,False))
 return result
