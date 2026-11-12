"""Reviewed original paper authoring. Source paper imports remain private."""
import json,math,random,re,hashlib
from fractions import Fraction as F
from itertools import permutations,combinations,product
from pathlib import Path

def svg(body,w=420,h=240,label='Mathematical diagram'):
 from html import escape
 return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(label)}"><title>{escape(label)}</title><rect width="{w}" height="{h}" fill="white"/><g fill="#18344c" stroke="#18344c" stroke-width="2" font-family="Arial,sans-serif">{body}</g></svg>'
def text(x,y,value,size=17):
 from html import escape
 return f'<text x="{x}" y="{y}" font-size="{size}" stroke="none" text-anchor="middle">{escape(str(value))}</text>'
def grid(cols,rows,shaded=(),labels=None):
 size=min(45,330/max(cols,rows));x0=35;y0=30;body=''
 for y in range(rows):
  for x in range(cols):body+=f'<rect x="{x0+x*size}" y="{y0+y*size}" width="{size}" height="{size}" fill="'+('#86c9c4' if (x,y) in shaded else '#fff')+'"/>'
 for (x,y),v in (labels or {}).items():body+=text(x0+(x+.5)*size,y0+(y+.65)*size,v)
 return svg(body,x0*2+cols*size,y0*2+rows*size,'Grid with labelled or shaded cells')
def polygon(points,labels=(),fill='#d9ebe8',extra=''):
 body=f'<polygon points="'+ ' '.join(f'{x},{y}' for x,y in points)+f'" fill="{fill}"/>'
 for x,y,t in labels:body+=text(x,y,t)
 return svg(body+extra,max(420,max(x for x,y in points)+35,max((x for x,y,t in labels),default=0)+35),max(240,max(y for x,y in points)+35,max((y for x,y,t in labels),default=0)+25))
def bars(values,names,step=1):
 hi=max(values);body='';scale=130/hi
 for i,(v,name) in enumerate(zip(values,names)):
  x=65+i*65;body+=f'<rect x="{x}" y="{180-v*scale}" width="38" height="{v*scale}" fill="#86c9c4"/>'+text(x+19,205,name,14)+text(x+19,170-v*scale,v,14)
 return svg(body,label='Bar chart; values labelled above bars')
def cuboid(w,d,h):
 body='<path d="M95,75L260,75L315,35L150,35Z" fill="#c4e5df"/><path d="M95,75L260,75L260,185L95,185Z" fill="#91c7c2"/><path d="M260,75L315,35L315,145L260,185Z" fill="#5f9faa"/>'
 body+=text(175,213,f'width {w}')+text(341,100,f'{d}',15)+text(60,137,f'{h}',15)+text(45,157,'height',13)+text(344,120,'depth',13)
 return svg(body,label=f'Cuboid: width {w}, depth {d}, height {h}. Not to scale.')
def number_line(values):
 body='<path d="M35,100H385"/>'
 for i,v in enumerate(values):
  x=40+340*i/(len(values)-1);body+=f'<path d="M{x},93V107"/>'+text(x,133,v)
 return svg(body,h=170,label='Equally spaced labelled number line')
def routes(a,b,blocked=()):
 body='';scale=min(52,300/max(a,b));x0=40;y0=35
 for x in range(a+1):body+=f'<path d="M{x0+x*scale},{y0}V{y0+b*scale}" stroke="#8099a8"/>'
 for y in range(b+1):body+=f'<path d="M{x0},{y0+y*scale}H{x0+a*scale}" stroke="#8099a8"/>'
 for x,y,label in [(0,0,'S'),(a,b,'T')]+[(x,y,'×') for x,y in blocked]:body+=text(x0+x*scale,y0+(b-y)*scale+6,label,22)
 return svg(body,x0*2+a*scale,y0*2+b*scale,'Route grid. S is bottom left; T is top right. Crosses are forbidden vertices.')
def table_diagram(rows,headers=None):
 rr=([headers] if headers else [])+rows;w=90*max(map(len,rr))+40;body=''
 for j,row in enumerate(rr):
  for i,v in enumerate(row):body+=f'<rect x="{20+90*i}" y="{20+38*j}" width="90" height="38" fill="'+('#dcebe9' if headers and j==0 else 'white')+'"/>'+text(65+90*i,45+38*j,v,16)
 return svg(body,w,40+38*len(rr),'Table with labelled rows and columns')
def count_routes(a,b,blocked=()):
 dp={(0,0):1}
 for y in range(b+1):
  for x in range(a+1):
   if (x,y)==(0,0):continue
   dp[x,y]=0 if (x,y) in blocked else dp.get((x-1,y),0)+dp.get((x,y-1),0)
 return dp[a,b]
def divisors(n):return [d for d in range(1,n+1) if n%d==0]
def item(stem,answer,solution,skill,wrong=None,check=None,figure=''):
 if check is not None:
  try: equal=F(str(answer))==F(str(check))
  except (ValueError,ZeroDivisionError): equal=str(answer)==str(check)
  assert equal,(stem,answer,check)
 assert len(stem)>15 and len(solution)>40 and re.fullmatch(r'[A-Z]+-\d\d',skill)
 return dict(stem=stem,value=str(answer),explanation=solution,category=skill,wrong=[str(x) for x in wrong] if wrong is not None else None,figure_svg=figure)
def paper(kind,index,items):
 expected=30 if kind=='amc' else 23;mc=25 if kind=='amc' else 18
 assert len(items)==expected,(kind,index,len(items))
 rng=random.Random(62026+index+(0 if kind=='amc' else 200))
 places=([0,1,2,3,4]*5)[:mc];rng.shuffle(places)
 qs=[]
 for n,q0 in enumerate(items,1):
  q=q0.copy();value=q.pop('value');wrong=q.pop('wrong');slot=places[n-1] if n<=mc else None
  if n<=mc:
   assert wrong is not None and len(wrong)==4,(kind,index,n,'four distractors required')
   assert len(set(wrong+[value]))==5,(kind,index,n,value,wrong)
   choices=wrong[:];rng.shuffle(choices);choices.insert(slot,value);answer=chr(65+slot)
  else:
   assert value.isdigit() and int(value)<(1000 if kind=='amc' else 1000000),(kind,index,n,value)
   choices=[];answer=value
  marks=(3 if n<=10 else 4 if n<=20 else 5 if n<=25 else n-20) if kind=='amc' else (3 if n<=7 else 4 if n<=13 else 5 if n<=18 else 6)
  qs.append(dict(**q,exam_id=f'summit-{kind}-practice-v2-{index:02}',question_number=n,question_type='multiple_choice' if n<=mc else 'integer',choices=choices,answer=answer,marks=marks,image_ref=None,metadata={'skill_id':q['category'],'version':'20261112-v2','original_authored':True,'expected_value':value,'solution_verified':True}))
 assert sum(q['marks'] for q in qs)==(135 if kind=='amc' else 100)
 return {'exam':{'id':qs[0]['exam_id'],'title':f'AMC Practice {index:02}' if kind=='amc' else f'Rossmoyne Honours Practice {index:02}','year':2027 if kind=='amc' else 2028,'division':'Upper Primary' if kind=='amc' else 'Honours Mathematics','student_year':6,'duration_minutes':60,'max_score':135 if kind=='amc' else 100,'source_type':'original_authored_mock','source_rights':'original_authored_for_summit_one','active':True,'repeatable':kind=='amc','session_slot':None,'question_count':expected,'metadata':{'version':'20261112-v2','section':kind,'card_summary':'Original problems, complete written solutions and saved attempt history.','difficulty_basis':'AMC Upper Primary 2007–2025' if kind=='amc' else 'User-supplied 23-question Rossmoyne sample; four-section 100-mark blueprint','independent_of_organiser':True}},'questions':qs}
def write_papers(papers,out):
 Path(out).mkdir(parents=True,exist_ok=True)
 for p in papers:(Path(out)/(p['exam']['id']+'.json')).write_text(json.dumps(p,ensure_ascii=False,indent=2))
