"""Final difficulty, technique-tag and figure review of the new paper set."""
from core import *
from figures import extras

def refine(p):
 kind='amc' if p['exam']['max_score']==135 else 'rossmoyne';index=int(p['exam']['id'][-2:]);raw=[]
 for q in p['questions']:
  answer=q['metadata']['expected_value'];wrong=[v for v in q['choices'] if v!=answer] if q['choices'] else None
  raw.append(item(q['stem'],answer,q['explanation'],q['category'],wrong,figure=q['figure_svg']))
 if kind=='amc' and index==2:
  raw[22]=item('At a meeting, each person shakes hands once with every other person. Three new people arrive and shake hands with everyone, including one another. This adds 24 handshakes. How many people were at the meeting before they arrived?',7,'If n people were already there, each of the three newcomers makes n handshakes with them: 3n. The newcomers also make 3 handshakes among themselves. Thus 3n+3=24, so n=7. Check: seven initial people have 21 handshakes; ten people have 45; the increase is 24.','COUNT-05',[6,8,9,10],check=(24-3)//3)
  raw[23]=item('A cuboid is 4 cubes wide, 3 cubes deep and 5 cubes high. Its top face and all four vertical faces are painted, but its bottom is not. How many unit cubes have exactly two painted faces?',22,'The four vertical edges contribute 4×(5−1)=16 cubes with two side faces painted; omit the top corners, which have three faces. Along the top perimeter away from corners, there are 2×(4−2)+2×(3−2)=6 cubes with one top and one side face. Total 16+6=22.','SOLID-02',[8,16,20,28],figure=cuboid(4,3,5),check=sum((x in [0,3])+(y in [0,2])+(z==4)==2 for x in range(4) for y in range(3) for z in range(5)))
 if kind=='amc' and index==4:
  raw[29]=item('A 30 cm by 20 cm rectangle has A at the bottom left, B at the bottom right, C at the top right and D at the top left. AB = 30 cm and AD = 20 cm. P is one third of the way from D to C, and Q is halfway from A to B. Lines AP and DQ meet at X. What is the area of triangle ABX, in square centimetres?',180,'Let the distance from X to the left edge AD be w. Along AP, the height above AB is 2w because P is 10 cm across and 20 cm high. Along DQ, the height is 20−(4/3)w because Q is 15 cm across. Equate: 2w=20−4w/3, so w=6 and the height is 12. Triangle ABX has base 30 and perpendicular height 12, hence area 30×12/2=180. A ratio route gives the same result: the crossing divides the 20 cm height in the ratio AQ:DP=15:10, so the lower height is 12.','GEO-02',figure=svg('<path d="M45,190H345V30H45Z" fill="none"/><path d="M45,190L145,30M45,30L195,190"/><circle cx="105" cy="94" r="3"/>'+text(35,210,'A')+text(355,210,'B')+text(355,25,'C')+text(35,25,'D')+text(145,22,'P')+text(195,210,'Q')+text(118,90,'X')+text(275,225,'AB = 30 cm')+text(260,55,'AD = 20 cm'),h=250,label='Rectangle ABCD, P on DC with DP:PC=1:2, Q midpoint of AB, AP and DQ meet at X. Not to scale.'),check=F(30*12,2))
 if kind=='amc' and index==6:
  raw[24]=item('A rectangle is enlarged so that its length increases by 50% and its width decreases by 20%. The new area is 72 cm². What was its original area?', '60 cm²','The length multiplier is 1.5 and the width multiplier is 0.8. Their product is 1.2, so the new area is 120% of the old. Divide 72 by 1.2 to get 60 cm². The two percentage changes act on different lengths, so subtracting their percentages is not valid.','FRAC-03',['54 cm²','57.6 cm²','86.4 cm²','90 cm²'])
 if kind=='amc' and index==9:
  vals=[v for v in range(700,800) if v%4==0 and sum(map(int,str(v)))==14 and len(set(str(v)))==3]
  assert vals==[716,752]
  raw[23]=item('A three-digit number uses three different digits and is divisible by 4. Its hundreds digit is 7 and its digit sum is 14. How many such numbers are there?',2,'Write the number as 7ab, so a+b=7. The last two digits represent 10a+b=9a+7. Divisibility by 4 requires a+3 to be a multiple of 4, so a=1,5 or 9. The last would make b negative. The surviving numbers are 716 and 752, giving 2.','DIG-02',[1,3,4,5],check=len(vals))
 if kind=='amc' and index==10:
  raw[23]=item('A container starts one third full. After 12 litres are added, it is half full. Then one quarter of the water now in it is removed. How many litres of water remain?',27,'Adding 12 litres increases the fill by 1/2−1/3=1/6, so the capacity is 72 litres. At half full it contains 36 litres. Keeping three quarters of those 36 litres leaves 27 litres. The removed fraction refers to the water present, not the capacity.','FRAC-01',[18,24,30,54],check=72*F(1,2)*F(3,4))
 # Map each question to the method actually taught by that identifier.
 for q in raw:
  t=q['stem'].lower();old=q['category']
  if old in ['SPATIAL-02','SPATIAL-03'] and any(w in t for w in ['compass','fold','clockwise','reflect','rotat']):q['category']='GEO-04'
  if old=='SEQ-02' and any(w in t for w in ['repeats','repeating','pattern repeats']):q['category']='DIV-05'
  if old=='SEQ-03' and 'consecutive' in t:q['category']='SEQ-01'
  if old=='COUNT-03' and 'stair' in t:q['category']='SEQ-03'
  if old=='DIG-04' and 'divisible' in t:q['category']='DIV-03'
  if old=='LOGIC-03' and any(w in t for w in ['guarantee','without looking']):q['category']='COUNT-06'
  if old=='LOGIC-05':q['category']='SEQ-04'
 if kind=='rossmoyne':
  if index==1:raw[9]=item('Three taps can separately fill a tank in 10, 15 and 30 hours. Their rates are constant. How many hours do they take together?',5,'In 30 hours the taps would fill 3, 2 and 1 tanks respectively. Together they fill 6 tanks in 30 hours, or one tank in 5 hours. Equivalently, the rates sum to 1/10+1/15+1/30=1/5 tank per hour.','RATE-02',[4,6,10,15],check=1/(F(1,10)+F(1,15)+F(1,30)))
  # Source-style diagrams support the actual relationships, with all dimensions stated.
  for q in raw:
   t=q['stem']
   if not q['figure_svg'] and re.search(r'(block|cake|cuboid) is (\d+) (?:unit )?cubes wide, (\d+)(?: cubes)? deep and (\d+)',t,re.I):
    z=re.search(r'(block|cake|cuboid) is (\d+) (?:unit )?cubes wide, (\d+)(?: cubes)? deep and (\d+)',t,re.I);q['figure_svg']=cuboid(*map(int,z.groups()[1:]))
  # All nine get a diagrammatic relationship rather than a decorative picture.
  n=4 if index==4 else 5
  if not raw[n]['figure_svg']:
   descriptions={2:[['3 triangles','2 squares'],['1 square','6 circles']],3:[['2 apples + 1 pear','340 g'],['1 apple + 2 pears','380 g']],4:[['triangle + circle','13'],['circle + square','17'],['triangle + square','20']],5:[['1 large parcel','2 small + 3 kg'],['3 large parcels','33 kg']],6:[['2 circles + triangle','23'],['circle + 2 triangles','25']],7:[['red + blue','19 g'],['2 red + 3 blue','48 g']],8:[['3 red + 2 blue','31 points'],['red + 2 blue','17 points']],9:[['4 mugs + plate','$33'],['2 mugs + plate','$21']]}
   if index in descriptions:raw[n]['figure_svg']=wide_table(descriptions[index])
  if index in [2,5,6,8] and not raw[15]['figure_svg']:
   fig={2:polygon([(50,35),(350,35),(350,195),(50,195)],[(200,25,'12 cm'),(395,120,'8 cm')],fill='#bcded7',extra='<path d="M50,35H125L50,115Z M350,195H275L350,115Z" fill="white"/>'+text(88,60,'3')+text(65,92,'4')+text(312,182,'3')+text(338,146,'4')),
    5:svg('<rect x="30" y="40" width="130" height="130" fill="white"/><path d="M30,40L160,170M30,170L160,40"/><path d="M30,40H160L95,105Z" fill="#85bdb5"/><rect x="240" y="40" width="130" height="130" fill="white"/><path d="M240,40H305V170H240Z" fill="#85bdb5"/>',label='Two equal squares; one has one diagonal quarter shaded; one has half shaded.'),
    6:polygon([(45,40),(355,40),(355,190),(45,190)],[(200,25,'8 m'),(395,120,'5 m')],fill='white'),
    8:polygon([(60,195),(350,195),(60,35)],[(205,224,'12 cm'),(35,120,'9 cm')],fill='#bcded7',extra='<path d="M60,195H157L60,142Z" fill="white"/>'+text(110,181,'4 cm')+text(95,150,'3 cm'))}[index];raw[15]['figure_svg']=fig
  if index in [1,2,3,5,6,7,8,9] and not raw[16]['figure_svg']:
   # A schematic equation displays only quantities already supplied, never the answer.
   notes={1:['Total wire 120 cm','Detour depths: 5 cm and 8 cm'],2:['Total wire 160 cm','Vertical total 32 cm; leftward total 9 cm'],3:['Frame: 30 cm × 20 cm','Two horizontal braces, each 30 cm'],5:['Rectangle: 24 cm × 18 cm','Route: top → right side → bottom'],6:['Wire: perimeter of 9 cm × 7 cm','New shape: equilateral triangle'],7:['333333','Multiply by 3, then add 1'],8:['One wire, two shapes','Square side 18 cm; rectangle length = 3 × width'],9:['Wire length 96 cm','Rectangle length = 3 × width']}
   raw[16]['figure_svg']=svg(text(210,75,notes[index][0],16)+text(210,125,notes[index][1],14),label='Given measurements and relationships')
 if kind=='amc':
  for number,figure in extras(index).items():
   if not raw[number-1]['figure_svg']:raw[number-1]['figure_svg']=figure
 result=paper(kind,index,raw)
 if kind=='rossmoyne':result['exam']['metadata']['timing_note']='60 minutes is a home-practice setting; official timing is unconfirmed.'
 return result

def wide_table(rows):
 body=''
 for j,row in enumerate(rows):
  for i,value in enumerate(row):body+=f'<rect x="{15+205*i}" y="{20+j*48}" width="205" height="48" fill="white"/>'+text(117+205*i,50+j*48,value,14)
 return svg(body,440,40+48*len(rows),'Balance or equation relationships given in the question')
