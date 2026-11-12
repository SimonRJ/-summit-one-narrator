-- Run only once the corresponding frontend release is available.
-- Keep retired papers and every historic sitting for permanent review.
begin;
do $$
declare papers integer; questions integer;
begin
 select count(*),sum(question_count) into papers,questions from public.exam_catalog
 where id ~ '^summit-(amc|rossmoyne)-practice-v2-[0-9]{2}$' or id='rossmoyne-original-sample-v2';
 if papers<>20 or questions<>530 then raise exception 'Expected 20 complete replacement papers'; end if;
 if exists(select 1 from public.exam_catalog e where (e.id ~ '^summit-(amc|rossmoyne)-practice-v2-[0-9]{2}$' or e.id='rossmoyne-original-sample-v2') and
  ((select count(*) from public.exam_questions q where q.exam_id=e.id)<>e.question_count or
   (select sum(marks) from public.exam_questions q where q.exam_id=e.id)<>e.max_score or
   exists(select 1 from public.exam_questions q where q.exam_id=e.id and (length(coalesce(explanation,''))<40 or answer is null))))
 then raise exception 'Incomplete paper or solution set'; end if;
end $$;
update public.exam_catalog set active=false,session_slot=null,
 metadata=metadata||'{"retired_by":"exam-centres-v2","retired_at":"2026-11-12"}'::jsonb
where id ~ '^summit-(amc|rossmoyne)-mock-[0-9]{2}$';
update public.exam_catalog set active=true,session_slot=null
where id ~ '^summit-(amc|rossmoyne)-practice-v2-[0-9]{2}$' or id='rossmoyne-original-sample-v2';
commit;
select source_type,count(*) papers,sum(question_count) questions from public.exam_catalog where active group by source_type;
