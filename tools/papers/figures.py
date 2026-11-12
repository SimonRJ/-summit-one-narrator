"""Question diagrams: only stated data; no embedded solutions."""
from core import *
def rectangle(w,h,extra='',fill='white'):
 return polygon([(65,45),(350,45),(350,185),(65,185)],[(205,28,str(w)),(385,120,str(h))],fill=fill,extra=extra)
def square(side):
 return svg('<rect x="120" y="30" width="170" height="170" fill="#dcece9"/>'+text(205,225,side),label='Square with its given side length')
def squares(a,b):
 aa=float(re.search(r'[0-9.]+',a)[0]);bb=float(re.search(r'[0-9.]+',b)[0]);scale=130/max(aa,bb);wa=aa*scale;wb=bb*scale
 return svg(f'<rect x="{100-wa/2}" y="{185-wa}" width="{wa}" height="{wa}" fill="#dcece9"/><rect x="{300-wb/2}" y="{185-wb}" width="{wb}" height="{wb}" fill="#dcece9"/>'+text(100,215,a)+text(300,215,b),label='Two separate squares with given side lengths')
def triangle(labels):return polygon([(55,185),(355,185),(205,35)],labels,fill='white')
def extras(index):
 return {
 4:{4:svg('<circle cx="210" cy="120" r="90" fill="white"/>'+''.join(f'<path d="M210,120L{210+90*math.cos(i*math.pi/3)},{120+90*math.sin(i*math.pi/3)}"/>' for i in range(6)),label='A full turn split into six equal angles'),14:squares('4 cm','6 cm'),28:rectangle('18 cm','12 cm',extra=''.join(f'<rect x="{x}" y="{y}" width="34" height="34" fill="#d5e8e5"/>' for x in [65,316] for y in [45,151])+text(84,92,'x')+text(335,137,'x'))},
 5:{9:triangle([(100,108,'9 cm'),(310,108,'9 cm'),(205,215,'6 cm')]),13:rectangle('14 m','6 m'),17:rectangle('3 × width','width'),23:svg('<rect x="30" y="50" width="130" height="130" fill="white"/><path d="M230,180H400L315,33Z" fill="white"/>'+text(95,115,'81 cm²')+text(315,212,'equal perimeters'),label='Square and equilateral triangle with equal perimeters; square area 81 square centimetres')},
 6:{7:square('11 cm'),13:rectangle('16 cm','? cm',text(205,220,'perimeter 50 cm')),21:rectangle('8 cm','5 cm',text(205,220,'Add the same amount to both dimensions.'))},
 7:{12:rectangle('20 m','15 m',extra='<rect x="65" y="45" width="65" height="65" fill="#8bc1d4"/>'+text(98,80,'5 m')),18:triangle([(108,105,'5 cm'),(308,105,'9 cm'),(205,215,'whole-number length')]),25:rectangle('18 cm','8 cm',text(205,220,'Same area as the square.'))},
 8:{4:polygon([(65,185),(350,185),(65,35)],[(95,164,'90°'),(310,174,'35°'),(88,74,'?')],fill='white'),7:svg('<path d="M90,80H260V205H90ZM90,80L150,30H320V155L260,205M260,80L320,30" fill="none"/><path d="M90,205L150,155H320M150,30V155" fill="none" stroke-dasharray="5 4"/>',label='Cube with hidden edges dashed'),15:svg('<rect x="120" y="30" width="170" height="170" fill="white"/><rect x="154" y="64" width="102" height="102" fill="#d5e8e5"/>'+text(205,225,'10 cm square')+text(205,120,'6 cm'),label='Square of side 10 cm containing a square of side 6 cm'),19:rectangle('18 cm','10 cm',extra='<path d="M207.5,45V185" stroke-dasharray="6 5"/>'+text(205,220,'Fold the short sides together.')),26:rectangle('longer side < 2 × shorter','',extra=text(205,120,'area 144 cm²'))},
 9:{12:rectangle('35 cm','24 cm',extra='<rect x="90" y="70" width="235" height="90" fill="#d5e8e5"/>'+text(205,120,'2 cm border all around')),17:svg('<rect x="120" y="30" width="170" height="170" fill="white"/><path d="M120,115H290"/>'+text(205,225,'8 cm square'),label='Square of side 8 cm divided into two equal rectangles')},
 10:{7:squares('5 cm','3 cm'),12:rectangle('length ?','6 cm',extra=text(205,220,'Same perimeter as a square of area 64 cm²')),19:triangle([(205,68,'100°'),(110,120,'equal'),(307,120,'equal')])}
 }.get(index,{})
