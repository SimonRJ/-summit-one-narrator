-- Transactional fixtures: no learner attempt or progress survives this check.
begin;
select set_config('qa.user_id',(select id::text from public.profiles order by created_at limit 1),true);
insert into public.exam_catalog(id,title,year,division,student_year,duration_minutes,max_score,source_type,source_rights,active,repeatable,question_count)
values ('_qa_repeat_20261112','Temporary repeatable fixture',2027,'Upper Primary',5,60,135,'qa_fixture','qa_fixture',true,true,2),('_qa_once_20261112','Temporary single-attempt fixture',2027,'Upper Primary',5,60,135,'qa_fixture','qa_fixture',true,false,2);
insert into public.exam_questions(exam_id,question_number,question_type,stem,choices,answer,explanation,marks,category,metadata)
select e.id,q.n,q.kind,q.stem,q.choices,q.answer,'Fixture explanation for checking atomic marking and review.',q.marks,'ALG-01','{"skill_id":"ALG-01"}'::jsonb from public.exam_catalog e cross join (values (1,'multiple_choice','Temporary fixture question one','["one","two","three","four","five"]'::jsonb,'"B"'::jsonb,3),(26,'integer','Temporary fixture question twenty six','[]'::jsonb,'"12"'::jsonb,6))q(n,kind,stem,choices,answer,marks) where e.id in ('_qa_repeat_20261112','_qa_once_20261112');
select set_config('request.jwt.claim.sub',current_setting('qa.user_id'),true);
set local role authenticated;
with s as (insert into public.exam_sittings(user_id,exam_id,completed,responses,metadata) values(auth.uid(),'_qa_repeat_20261112',false,'{}','{}') returning id) select set_config('qa.sitting',id::text,true) from s;
do $$ begin
 if has_column_privilege('authenticated','public.exam_questions','answer','SELECT') then raise exception 'Answer keys exposed';end if;
 if has_function_privilege('authenticated','public.seal_exam_result(uuid,uuid,boolean)','EXECUTE') then raise exception 'Grader callable directly';end if;
 begin
  insert into public.exam_sittings(user_id,exam_id,completed) values(auth.uid(),'_qa_repeat_20261112',false);
  raise exception 'QA unexpected duplicate open attempt accepted';
 exception when others then if sqlerrm like 'QA unexpected%' then raise;end if; end;
 perform public.save_exam_response(current_setting('qa.sitting')::uuid,1,'B');
 perform public.save_exam_response(current_setting('qa.sitting')::uuid,26,'012');
 begin
  perform public.save_exam_response(current_setting('qa.sitting')::uuid,26,'12abc');raise exception 'QA unexpected invalid number accepted';
 exception when others then if sqlerrm like 'QA unexpected%' then raise;end if;end;
end $$;
set local role service_role;
do $$ declare r jsonb;r2 jsonb;begin
 r=public.seal_exam_result(current_setting('qa.sitting')::uuid,current_setting('qa.user_id')::uuid,false);
 if (r->>'score')::integer<>9 or jsonb_array_length(r->'rows')<>2 then raise exception 'Marking fixture failed: %',r;end if;
 r2=public.seal_exam_result(current_setting('qa.sitting')::uuid,current_setting('qa.user_id')::uuid,false);
 if r<>r2 then raise exception 'Snapshot is not idempotent';end if;
end $$;
set local role authenticated;
do $$ begin
 begin perform public.save_exam_response(current_setting('qa.sitting')::uuid,1,'A');raise exception 'QA unexpected sealed update accepted';exception when others then if sqlerrm like 'QA unexpected%' then raise;end if;end;
end $$;
with s as (insert into public.exam_sittings(user_id,exam_id,completed) values(auth.uid(),'_qa_repeat_20261112',false) returning id,attempt_number) select set_config('qa.repeat_number',attempt_number::text,true) from s;
with s as (insert into public.exam_sittings(user_id,exam_id,completed) values(auth.uid(),'_qa_once_20261112',false) returning id) select set_config('qa.once',id::text,true) from s;
set local role service_role;
select public.seal_exam_result(current_setting('qa.once')::uuid,current_setting('qa.user_id')::uuid,false)->>'score';
set local role authenticated;
do $$ begin
 if current_setting('qa.repeat_number')<>'2' then raise exception 'Repeat sequence failed';end if;
 begin insert into public.exam_sittings(user_id,exam_id,completed) values(auth.uid(),'_qa_once_20261112',false);raise exception 'QA unexpected second attempt allowed';exception when others then if sqlerrm like 'QA unexpected%' then raise;end if;end;
end $$;
select set_config('request.jwt.claim.sub','00000000-0000-0000-0000-000000000001',true);
do $$ begin
 if exists(select 1 from public.exam_sittings where id=current_setting('qa.sitting')::uuid) then raise exception 'Cross-account attempt exposed';end if;
 if exists(select 1 from public.learning_repairs where user_id=current_setting('qa.user_id')::uuid) then raise exception 'Cross-account repairs exposed';end if;
end $$;
reset role;
rollback;
select 'PASS: repeat attempts, single-attempt lock, per-question saving, strict numeric answers, atomic grading, idempotent snapshots, hidden keys and owner access' as validation;
