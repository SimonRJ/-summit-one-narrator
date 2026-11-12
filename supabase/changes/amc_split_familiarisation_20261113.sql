-- Summit One: first split-exam familiarisation set (2026-11-13).
-- Reuses the TEN already-authored full mocks. These are NOT additional original questions.
-- No authentic past-paper text is duplicated. Original papers and historical sittings are untouched.
begin;
do $check$
begin
 if (select count(*) from public.exam_catalog
     where id ~ '^summit-amc-practice-v2-[0-9]{2}$' and active and repeatable) <> 10
 then raise exception 'Expected ten active, repeatable authored AMC mocks'; end if;
 if exists (
   select 1 from public.exam_catalog e
   where e.id ~ '^summit-amc-practice-v2-[0-9]{2}$' and e.active
     and (e.question_count<>30 or e.max_score<>135
       or (select count(*) from public.exam_questions q where q.exam_id=e.id)<>30
       or (select sum(q.marks) from public.exam_questions q where q.exam_id=e.id)<>135)
 ) then raise exception 'A source authored mock is incomplete'; end if;
end $check$;

insert into public.exam_catalog
(id,title,year,division,student_year,duration_minutes,max_score,source_type,award_cutoffs,source_rights,active,session_slot,question_count,metadata,repeatable)
select
 case when parts.part='speed' then 'summit-amc-speed-intro-' else 'summit-amc-depth-intro-' end || right(e.id,2),
 case when parts.part='speed' then 'Fluency ' else 'Challenge ' end || right(e.id,2) ||
 case when parts.part='speed' then ' · Q1–20' else ' · Q21–30' end,
 e.year,e.division,e.student_year,
 case when parts.part='speed' then 20 else 40 end,
 case when parts.part='speed' then 70 else 65 end,
 'summit_amc_split_familiarisation',null,
 'Summit One authored full-mock questions shown as split training; no new-original claim',
 true,null,
 case when parts.part='speed' then 20 else 10 end,
 jsonb_build_object(
  'amc_part',parts.part,'paper_family','amc_upper_primary','bank','familiarisation',
  'source_paper_id',e.id,'originality','reused_from_existing_full_mock',
  'timer_mode','elapsed','target_minutes',case when parts.part='speed' then 20 else 40 end,
  'version','split-intro-20261113',
  'card_summary','Familiarisation from an existing authored full AMC mock. Same problems as that full mock; use your first attempt to judge unseen ability.'
 ),true
from public.exam_catalog e
cross join (values ('speed'),('depth')) as parts(part)
where e.id ~ '^summit-amc-practice-v2-[0-9]{2}$' and e.active
on conflict(id) do nothing;

insert into public.exam_questions
(exam_id,question_number,question_type,stem,choices,answer,explanation,marks,image_ref,figure_svg,category,metadata)
select p.id,q.question_number,q.question_type,q.stem,q.choices,q.answer,q.explanation,q.marks,q.image_ref,q.figure_svg,q.category,
 coalesce(q.metadata,'{}'::jsonb)||jsonb_build_object('reused_from',q.exam_id)
from public.exam_catalog p
join public.exam_catalog source on source.id=p.metadata->>'source_paper_id'
join public.exam_questions q on q.exam_id=source.id
where p.source_type='summit_amc_split_familiarisation'
 and ((p.metadata->>'amc_part'='speed' and q.question_number between 1 and 20)
  or (p.metadata->>'amc_part'='depth' and q.question_number between 21 and 30))
on conflict(exam_id,question_number) do nothing;

do $verify$
begin
 if (select count(*) from public.exam_catalog where source_type='summit_amc_split_familiarisation')<>20
 then raise exception 'Expected twenty split familiarisation sets'; end if;
 if exists (
  select 1 from public.exam_catalog e
  where e.source_type='summit_amc_split_familiarisation'
    and ((select count(*) from public.exam_questions q where q.exam_id=e.id)<>e.question_count
       or (select coalesce(sum(q.marks),0) from public.exam_questions q where q.exam_id=e.id)<>e.max_score
       or exists(select 1 from public.exam_questions q where q.exam_id=e.id
                  and (q.answer is null or coalesce(length(q.explanation),0)<40))
       or (e.max_score=70 and exists(select 1 from public.exam_questions q where q.exam_id=e.id
                                     and (q.question_number>20 or q.question_type<>'multiple_choice')))
       or (e.max_score=65 and (select count(*) from public.exam_questions q where q.exam_id=e.id
                               and q.question_type='integer')<>5))
 ) then raise exception 'Split familiarisation validation failed'; end if;
end $verify$;
commit;
