-- Read-only fingerprint of the frozen authentic AMC subsystem and of recorded learner attempts.
-- Run before and after any content or schema work and compare with docs/AUTHENTIC_AMC_FREEZE.md.
-- This query never writes and never starts an exam sitting.
select 'authentic exam catalog' as item, count(*) as n,
       md5(string_agg(md5(id||'|'||coalesce(title,'')||'|'||coalesce(active::text,'')||'|'||coalesce(metadata::text,'')||'|'||coalesce(question_count::text,'')||'|'||coalesce(duration_minutes::text,'')||'|'||coalesce(repeatable::text,'')), '' order by id)) as fingerprint
  from exam_catalog where source_type = 'authentic_amc_past_paper'
union all
select 'authentic exam questions', count(*),
       md5(string_agg(md5(q.exam_id||'|'||q.question_number||'|'||coalesce(q.stem,'')||'|'||coalesce(q.choices::text,'')||'|'||coalesce(q.answer::text,'')||'|'||coalesce(q.explanation,'')||'|'||coalesce(q.image_ref,'')||'|'||coalesce(q.figure_svg,'')||'|'||coalesce(q.metadata::text,'')||'|'||coalesce(q.marks::text,'')), '' order by q.exam_id, q.question_number))
  from exam_questions q join exam_catalog c on c.id = q.exam_id where c.source_type = 'authentic_amc_past_paper'
union all
select 'authentic-linked content problems', count(*),
       md5(string_agg(md5(coalesce(id,'')||'|'||coalesce(title,'')||'|'||coalesce(prompt,'')||'|'||coalesce(answer::text,'')||'|'||coalesce(solution_text,'')||'|'||coalesce(spoken_script,'')||'|'||coalesce(category,'')||'|'||coalesce(difficulty::text,'')), '' order by id))
  from content_problems where source_type = 'authentic_amc'
union all
select 'problem attempts', count(*),
       md5(string_agg(id::text||problem_id||answer_text||coalesce(is_correct::text,''), '' order by id))
  from problem_attempts;
