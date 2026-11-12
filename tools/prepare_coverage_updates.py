"""Prepare private, guarded data updates; never put generated SQL on Pages.

Inputs: the private full teaching map, the generated original-paper directory,
and a private output directory. This tool does not connect to a database.
"""
import json,sys
from pathlib import Path

def literal(value):
 return "'"+json.dumps(value,ensure_ascii=False).replace("'","''")+"'::jsonb"

def prepare(mapping,papers,out):
 rows=json.loads(Path(mapping).read_text());assert len(rows)==570
 target=Path(out);target.mkdir(parents=True,exist_ok=True)
 for year in range(2007,2026):
  selected=[r for r in rows if r['exam_id']==f'amc-up-{year}'];assert len(selected)==30
  data=literal(selected)
  sql=f"""begin;
with source as (select * from jsonb_to_recordset({data}) as x(exam_id text,question_number integer,skill_id text,learning_map jsonb)), changed as (
update public.exam_questions q set category=s.skill_id, metadata=coalesce(q.metadata,'{{}}'::jsonb)||jsonb_build_object('skill_id',s.skill_id,'learning_map',s.learning_map)
from source s where q.exam_id=s.exam_id and q.question_number=s.question_number returning q.question_number)
select count(*) as mapped_questions from changed;
commit;
select count(*) as mapped_questions from public.exam_questions where exam_id='amc-up-{year}' and metadata->'learning_map'->>'version'='recognition-20261113';
"""
  (target/f'map-{year}.sql').write_text(sql)
 for path in sorted(Path(papers).glob('summit-amc-practice-v2-*.json')):
  p=json.loads(path.read_text());e=p['exam'];q=p['questions'];assert len(q)==30 and sum(x['marks'] for x in q)==135
  cols=['question_type','stem','choices','answer','explanation','marks','image_ref','figure_svg','category','metadata']
  sql=f"""begin;
lock table public.exam_sittings in share row exclusive mode;
do $$ begin
 if exists(select 1 from public.exam_sittings where exam_id='{e['id']}') then raise exception 'Paper has attempts: publish a new version instead'; end if;
 if (select count(*) from public.exam_questions where exam_id='{e['id']}')<>30 then raise exception 'Unexpected paper size'; end if;
end $$;
with source as (select * from jsonb_populate_recordset(null::public.exam_questions,{literal(q)}))
update public.exam_questions q set {','.join(c+'=s.'+c for c in cols)} from source s where q.exam_id=s.exam_id and q.question_number=s.question_number;
update public.exam_catalog set metadata=metadata||{literal(e['metadata'])} where id='{e['id']}';
commit;
select count(*) as revised_questions,sum(marks) as marks from public.exam_questions where exam_id='{e['id']}' and metadata->>'version'='20261113-coverage';
"""
  (target/(e['id']+'.sql')).write_text(sql)
 print('Prepared 19 mapping updates and 10 guarded mock updates.')
if __name__=='__main__':prepare(*sys.argv[1:])
