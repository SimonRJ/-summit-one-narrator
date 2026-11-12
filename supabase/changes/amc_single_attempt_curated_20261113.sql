-- Summit One, November 2026: protect single-sitting A/B exam integrity.
-- Retain every historical question, answer, sitting, snapshot and review, including retired content.
begin;
update public.exam_catalog
   set repeatable=false,
       metadata=metadata||'{"exam_attempt_policy":"single_scored_attempt","review_after_submit":true}'::jsonb
 where metadata->>'amc_part' in ('speed','depth');
-- The ten earlier full-length authored AMC mocks are now archival and may be viewed only
-- through historical results; they have no separate AMC exam-library entry.
update public.exam_catalog
   set active=false,metadata=metadata||'{"retired_reason":"full_mock_category_removed_20261113"}'::jsonb
 where source_type='original_authored_mock' and max_score=135;
-- Old full-mock excerpts were not fresh problems, and several are not appropriately calibrated.
-- Keep their old record/snapshots but do NOT count these as new 30-set practice content.
update public.exam_catalog
   set active=false,metadata=metadata||'{"retired_reason":"reused_full_mock_questions_not_fresh_20261113"}'::jsonb
 where source_type='summit_amc_split_familiarisation';
-- The original, independently authored and solution-bearing papers remain in the 30-slot roadmap.
update public.exam_catalog set title='AMC Part A · Set 01',metadata=metadata||'{"plan_index":1,"exam_series":"part_a_30","quality_gate":"reviewed"}'::jsonb where id='summit-amc-speed-original-pilot-01';
update public.exam_catalog set title='AMC Part A · Set 02',metadata=metadata||'{"plan_index":2,"exam_series":"part_a_30","quality_gate":"reviewed"}'::jsonb where id='summit-amc-speed-original-01';
update public.exam_catalog set title='AMC Part B · Set 01',metadata=metadata||'{"plan_index":1,"exam_series":"part_b_30","quality_gate":"reviewed"}'::jsonb where id='summit-amc-depth-original-01';
do $check$
begin
 if (select count(*) from public.exam_catalog where active and metadata->>'amc_part'='speed') <> 2 then raise exception 'Expected two reviewed Part A sets'; end if;
 if (select count(*) from public.exam_catalog where active and metadata->>'amc_part'='depth') <> 1 then raise exception 'Expected one reviewed Part B set'; end if;
 if exists (select 1 from public.exam_catalog where active and metadata->>'amc_part' in ('speed','depth') and repeatable) then raise exception 'Practice paper must lock after first attempt'; end if;
 if exists (select 1 from public.exam_catalog e where e.active and e.metadata->>'amc_part' in ('speed','depth')
   and ((select count(*) from public.exam_questions q where q.exam_id=e.id)<>e.question_count
     or (select sum(marks) from public.exam_questions q where q.exam_id=e.id)<>e.max_score
     or exists(select 1 from public.exam_questions q where q.exam_id=e.id and (q.category is null or length(coalesce(q.explanation,''))<85))
   )) then raise exception 'Incomplete source questions or solution review'; end if;
end $check$;
commit;
