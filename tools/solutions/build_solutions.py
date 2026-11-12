"""Build reviewed solution updates without redistributing question images/text."""
import importlib,json,sys
from pathlib import Path

def build():
 rows=[]
 for year in range(2009,2023):
  mod=importlib.import_module(f'y{year}')
  assert set(mod.SOLUTIONS)==set(range(1,31 if year==2017 else 26)),year
  for n,(skill,solution) in mod.SOLUTIONS.items():
   assert len(solution)>30,(year,n)
   rows.append({'exam_id':f'amc-up-{year}','question_number':n,'skill_id':skill,'explanation':solution,'answer_correction':getattr(mod,'ANSWER_CORRECTIONS',{}).get(n)})
 assert len(rows)==355
 return rows
if __name__=='__main__':
 out=Path(sys.argv[1] if len(sys.argv)>1 else '/tmp/summit-written-solutions.json');out.write_text(json.dumps(build(),ensure_ascii=False,indent=2));print(f'Wrote 355 reviewed explanations to {out}')
