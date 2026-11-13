"""Independent static QA for all generated AMC and Honours mock papers.

Not a substitute for human review of mathematical claims or render inspection.
Validates question completeness, answer-key mapping, figure XML/semantics and
mathematical typography basics. Called after build_all.py in release QA.
"""
import json,re,sys,collections
from pathlib import Path
from xml.etree import ElementTree as ET

def fail(msg):raise AssertionError(msg)
def numeric_shape(text):
 return re.sub(r'[0-9]+(?:[.,][0-9]+)?','N',text.lower())

def check_svg(markup,tag):
 if '<script' in markup.lower() or 'onload=' in markup.lower() or '<foreignobject' in markup.lower():
  fail(f'{tag} unsafe SVG markup')
 try:root=ET.fromstring(markup)
 except ET.ParseError as e:fail(f'{tag} cannot parse SVG: {e}')
 if not root.tag.endswith('svg'):fail(f'{tag} not an SVG root')
 if root.get('role')!='img' or not root.get('aria-label'):
  fail(f'{tag} missing image semantics')
 view=root.get('viewBox')
 if not view or len(view.split())!=4:fail(f'{tag} missing viewBox')
 x,y,w,h=map(float,view.split())
 if w<=0 or h<=0:fail(f'{tag} bad viewBox dimensions')
 if w>1300 or h>900:fail(f'{tag} oversized visual layout')
 # Avoid clipping numerical labels or accidentally placing rectangles off-canvas.
 warnings=[]
 for node in root.iter():
  name=node.tag.split('}')[-1]
  if name=='rect':
   try:
    rx=float(node.get('x','0'));ry=float(node.get('y','0'))
    rw=float(node.get('width','0'));rh=float(node.get('height','0'))
    if rx<x-3 or ry<y-3 or rx+rw>x+w+3 or ry+rh>y+h+3:
     warnings.append('rectangle touches outside viewBox')
   except ValueError:pass
  if name=='text':
   try:
    tx=float(node.get('x','0'));ty=float(node.get('y','0'))
    if tx<x or tx>x+w or ty<y or ty>y+h: warnings.append('text anchor outside viewBox')
   except ValueError:pass
 return warnings

def main():
 folder=Path(sys.argv[1]);files=sorted(folder.glob('*.json'))
 if not files:fail('No mock paper JSON created')
 papers=[json.loads(path.read_text()) for path in files]
 errors=[];warnings=[];titles=collections.Counter();allstems=collections.Counter();figures=0;keys=0;question_count=0
 for doc in papers:
  exam=doc['exam'];qs=doc['questions']
  tag=exam['id'];is_amc='-amc-' in tag;want=30 if is_amc else 23
  if len(qs)!=want:errors.append(f'{tag} has {len(qs)} questions, expected {want}')
  expected_mc=25 if is_amc else 18
  if len({x['question_number'] for x in qs})!=len(qs):errors.append(f'{tag} repeated question numbers')
  if [x['question_number'] for x in qs]!=list(range(1,want+1)):errors.append(f'{tag} questions are out of order')
  if sum(x['marks'] for x in qs)!=(135 if is_amc else 100):errors.append(f'{tag} total marks incorrect')
  for q in qs:
   question_count+=1;n=q['question_number'];where=f'{tag}:{n}'
   stem=q['stem'].strip();sol=q['explanation'].strip()
   titles[numeric_shape(stem)]+=1;allstems[stem]+=1
   if len(stem)<9 or len(stem)>1250:errors.append(f'{where} stem length outside reasonable range')
   if len(sol)<45 or len(sol)>5000:errors.append(f'{where} worked solution length')
   if not re.search(r'[?.]$',stem):warnings.append(f'{where} missing final punctuation')
   if re.search(r'(in your working|explain your method|tell me why|the answer is given|PLACEHOLDER|TODO)',stem,re.I):
    errors.append(f'{where} inappropriate guidance / placeholder in exam question')
   if q['question_type']=='multiple_choice':
    if n>expected_mc:errors.append(f'{where} wrong choice question position')
    choices=q.get('choices')
    if not isinstance(choices,list) or len(choices)!=5 or len(set(map(str,choices)))!=5:
     errors.append(f'{where} options not five unique choices')
     continue
    if q.get('answer') not in list('ABCDE'):errors.append(f'{where} incorrect answer key type')
    else:
     keyed=choices[ord(q['answer'])-65]
     value=q.get('metadata',{}).get('expected_value')
     if value is not None and str(keyed)!=str(value):errors.append(f'{where} answer letter points to wrong value')
    keys+=1
   else:
    if n<=expected_mc:errors.append(f'{where} numerical question in multiple-choice slot')
    if q['question_type']!='integer':errors.append(f'{where} unexpected question_type')
    if is_amc and not re.fullmatch(r'\d{1,3}',str(q['answer'])):
     errors.append(f'{where} AMC integer answer outside 0–999')
    value=q.get('metadata',{}).get('expected_value')
    if value is not None and str(q.get('answer'))!=str(value):
     errors.append(f'{where} answer not expected_value')
   fig=q.get('figure_svg') or ''
   if fig:
    figures+=1
    try:warnings+= [f'{where}: {msg}' for msg in check_svg(fig,where)]
    except AssertionError as e:errors.append(str(e))
 if len(papers)!=19 or question_count!=507:errors.append(f'expected 19 papers and 507 questions, got {len(papers)}, {question_count}')
 duplicated=sum(n-1 for n in allstems.values() if n>1)
 repeated_shapes={k:n for k,n in titles.items() if n>=3}
 print(json.dumps({'papers':len(papers),'questions':question_count,'validated_multiple_choice':keys,
   'svg_diagrams':figures,'exact_duplicated_questions':duplicated,
   'repeated_numeric_skeletons':len(repeated_shapes),'most_repeated_skeletons':sorted(repeated_shapes.items(),key=lambda x:-x[1])[:12],
   'visual_warnings':len(warnings),'sample_warnings':warnings[:20],'errors':errors[:30]},indent=2))
 if errors:raise AssertionError(f'{len(errors)} problems in generated mock bank')
 print('PASS: all generated mock questions, option mappings, numeric keys and SVG structures verified.')

if __name__=='__main__':main()
