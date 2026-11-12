"""Import the private, user-supplied sample transcription. Never bundle source data publicly."""
from core import *
from rossmoyne_01_03 import strip
import argparse,base64

def plain(value):
 s=str(value).replace('\\\\','\\').replace('\\textquotesingle s',"'s").replace('``','"')
 s=re.sub(r'(?<!\\)\$', '',s)
 s=s.replace('\\$','$').replace('\\%','%').replace('\\times','×').replace('\\operatorname{lcm}','lcm')
 s=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'(\1/\2)',s)
 s=re.sub(r'\\frac(\d)\{([^{}]+)\}',r'(\1/\2)',s)
 s=re.sub(r'\\frac\{([^{}]+)\}(\d)',r'(\1/\2)',s)
 s=re.sub(r'\\frac(\d)(\d)',r'\1/\2',s)
 s=re.sub(r'\^\{([^}]+)\}',r'^\1',s)
 s=s.replace('\\lceil','ceiling(').replace('\\rceil',')').replace('\\{','{').replace('\\}','}')
 return s

def build(bank,figures):
 source=json.loads(Path(bank).read_text())['exams'][0]
 skills=['DIG-01','COUNT-01','RATE-01','COUNT-04','SEQ-02','LOGIC-03','COUNT-03','DIV-05','ALG-04','RATE-02','DIV-05','RATE-01','GEO-01','ALG-03','ALG-05','GEO-02','GEO-01','DIG-04','FRAC-04','DIV-02','DIG-05','SOLID-02','FRAC-01']
 qs=[];eid='rossmoyne-original-sample-v2'
 for q,skill in zip(source,skills):
  n=q['no'];choices=[plain(v) for v in q['options']] if q['options'] else []
  expected=plain(q['answer']);stem=plain(q['stem']);explanation=plain(q['explanation'])
  figure=''
  if n in [6,21]:
   filename='original_animal_grid.webp' if n==6 else 'original_symbol_subtraction.webp'
   b64=base64.b64encode((Path(figures)/filename).read_bytes()).decode()
   alt='Animal symbol grid and row and column totals' if n==6 else 'Picture subtraction ABRA − BCBR = RCBB'
   figure=f'<img src="data:image/webp;base64,{b64}" alt="{alt}" style="max-width:100%;height:auto"/>'
  if n==5:
   stem=stem.replace('one cookie','one cupcake')
   explanation='The seven boxes hold 1+2+4+8+16+32+64=127 cupcakes. Add the three eaten to obtain 130. The source used “cookie” once; that typographical error is corrected in this transcription.'
  if n==16:figure=strip(5,4,1)
  if n==17:
   figure=svg('<path d="M25,100H95V175H165V35H250V100H375" fill="none" stroke-width="4"/><path d="M25,100H375" stroke-dasharray="4 5" stroke="#a9afb8"/><path d="M25,205H375"/>'+text(200,230,'x')+text(70,145,'4 cm')+text(280,70,'7 cm'),label='Bent wire: horizontal segments all move right. Downward detour 4 cm and upward detour 7 cm.')
  if n==18:explanation='Subtracting gives 11111111107777777778. The result has nine 1s, one 0, nine 7s and a final 8. The digit sum is 9+0+63+8=80. Check by adding the ten-digit 3333333333 back to recover the twenty 1s.'
  if n==20:
   stem='Consider the words MAGIC RECTANGLE SQUARE TRIANGLE. Each second, the last letter of each word moves to the front of that word. After one second they read CMAGI ERECTANGL ESQUAR ETRIANGL. What is the smallest positive number of seconds before all the original words appear together again?'
  if n==21:
   explanation='Let apple=A, bee=B, rabbit=R and cherries=C. The subtraction is ABRA−BCBR=RCBB. A units-column borrow would require A−R+10=B; with distinct digits 1,2,4,6, the only possible difference of −4 uses A=2,R=6 and would repeat B=6, so no units borrow is possible. Thus A=R+B, forcing A=6 and {R,B}={4,2}. The tens column requires R−B, allowing a borrow if needed, to equal B. Only R=4,B=2 works. The remaining C=1. Check the complete subtraction: 6246−2124=4122.'
  if n==22:figure=cuboid(4,6,5)
  answer=chr(65+choices.index(expected)) if choices else expected
  assert not re.search(r'\\[a-zA-Z]',stem+explanation+''.join(choices)),(n,stem,explanation)
  qs.append({'exam_id':eid,'question_number':n,'question_type':'multiple_choice' if choices else 'integer','stem':stem,'choices':choices,'answer':answer,'explanation':explanation,'marks':q['marks'],'image_ref':None,'figure_svg':figure,'category':skill,'metadata':{'skill_id':skill,'source':'user-supplied-official-sample-transcription','source_question_number':n,'version':'20261112-v2','expected_value':expected,'source_note':'Transcribed from the user-supplied sample; diagrams recovered from the supplied archive. Q5 source typo corrected.'}})
 assert len(qs)==23 and sum(q['marks'] for q in qs)==100
 return {'exam':{'id':eid,'title':'Rossmoyne original sample','year':2028,'division':'Honours Mathematics','student_year':6,'duration_minutes':60,'max_score':100,'source_type':'user_supplied_original_sample','source_rights':'user_supplied_private_study','active':True,'repeatable':False,'session_slot':None,'question_count':23,'metadata':{'version':'20261112-v2','section':'rossmoyne','original_sample':True,'transcription':True,'timing_note':'60 minutes is a home-practice setting; no official timing is claimed.','source_note':'Recovered from the uploaded sample transcription and source illustrations. Not an official 2028 paper.'}},'questions':qs}

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('bank');ap.add_argument('figures');ap.add_argument('output');a=ap.parse_args()
 write_papers([build(a.bank,a.figures)],a.output)
