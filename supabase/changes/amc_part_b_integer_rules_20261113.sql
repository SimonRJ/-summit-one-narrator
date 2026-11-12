-- 0–999 limits for AMC numerical responses, preserving server snapshots and authentication.
begin;
CREATE OR REPLACE FUNCTION public.save_exam_response(p_sitting_id uuid, p_question integer, p_response text)
 RETURNS exam_sittings
 LANGUAGE plpgsql
 SET search_path TO ''
AS $function$
declare s public.exam_sittings%rowtype; e public.exam_catalog%rowtype; question_kind text; option_count integer;
begin
 select * into s from public.exam_sittings where id=p_sitting_id and user_id=auth.uid() for update;
 if not found or s.completed or clock_timestamp()>=s.expires_at then raise exception 'This attempt is not open for answers'; end if;
 select * into e from public.exam_catalog where id=s.exam_id;
 select question_type,jsonb_array_length(choices) into question_kind,option_count from public.exam_questions_student where exam_id=s.exam_id and question_number=p_question;
 if not found then raise exception 'Question not found'; end if;
 if p_response is not null then
  if question_kind='multiple_choice' and not(p_response ~ '^[A-Z]$' and ascii(p_response)-64 between 1 and option_count) then raise exception 'Choose a listed option'; end if;
  if question_kind='integer' and not(p_response ~ (case when e.max_score=135 or e.metadata->>'amc_part' in ('speed','depth') then '^[0-9]{1,3}$' else '^[0-9]{1,6}$' end)) then raise exception 'Enter a valid whole-number answer'; end if;
 end if;
 update public.exam_sittings set responses=case when p_response is null then responses-p_question::text else jsonb_set(responses,array[p_question::text],to_jsonb(p_response),true) end,
 integer_save_times=case when p_response is null then integer_save_times-p_question::text when question_kind='integer' then jsonb_set(integer_save_times,array[p_question::text],to_jsonb(clock_timestamp()),true) else integer_save_times end
 where id=s.id returning * into s;
 return s;
end;
$function$
;

CREATE OR REPLACE FUNCTION public.seal_exam_result(p_sitting_id uuid, p_user_id uuid, p_auto boolean DEFAULT false)
 RETURNS jsonb
 LANGUAGE plpgsql
 SET search_path TO ''
AS $function$
declare s public.exam_sittings%rowtype; e public.exam_catalog%rowtype; q public.exam_questions%rowtype;
 result jsonb; rows jsonb='[]'::jsonb; response text; expected text; ok boolean; earned integer;
 total integer=0; n integer=0; award text; estimated boolean; student_year integer; cuts jsonb;
 finish_time timestamptz; duration_seconds integer; version text; skill text; done integer=0;
begin
 if current_user<>'service_role' then raise exception 'Service role required'; end if;
 select * into s from public.exam_sittings where id=p_sitting_id and user_id=p_user_id for update;
 if not found then raise exception 'Sitting not found'; end if;
 select r.result into result from public.exam_result_snapshots r where r.sitting_id=s.id and r.user_id=p_user_id;
 if found then return result; end if;
 select * into e from public.exam_catalog where id=s.exam_id;
 if not found then raise exception 'Exam not found'; end if;
 select coalesce(completed_sessions,0) into done from public.progress_state where user_id=p_user_id;
 done=coalesce(done,0);
 for q in select * from public.exam_questions where exam_id=e.id order by question_number loop
  n=n+1; response=s.responses->>q.question_number::text;
  expected=case when jsonb_typeof(q.answer)='object' then coalesce(q.answer->>'choice',q.answer->>'value',q.answer->>'answer') else q.answer#>>'{}' end;
  if q.question_type='multiple_choice' then ok=coalesce(upper(trim(response))=upper(trim(expected)),false);
  else ok=coalesce(response ~ (case when e.max_score=135 or e.metadata->>'amc_part' in ('speed','depth') then '^[0-9]{1,3}$' else '^[0-9]{1,6}$' end),false);
   if ok then ok=response::numeric=expected::numeric; end if;
  end if;
  earned=case when ok then q.marks else 0 end; total=total+earned;
  rows=rows||jsonb_build_array(jsonb_build_object('question_number',q.question_number,'question_type',q.question_type,'stem',q.stem,'choices',q.choices,'response',response,'correct',ok,'earned',earned,'marks',q.marks,'correct_answer',expected,'explanation',q.explanation,'image_ref',q.image_ref,'figure_svg',q.figure_svg,'metadata',q.metadata,'category',q.category));
  skill=coalesce(q.metadata->>'skill_id',case when q.category ~ '^[A-Z]+-[0-9]{2}$' then q.category else null end);
  if not ok and skill is not null and not s.completed then
   insert into public.learning_repairs(user_id,source_type,source_ref,source_label,skill_id,due_after_session)
   values(p_user_id,'exam',s.id::text||':'||q.question_number,e.title||' · Q'||q.question_number,skill,done)
   on conflict(user_id,source_type,source_ref,skill_id) do nothing;
  end if;
 end loop;
 if n<>e.question_count then raise exception 'Exam question set is incomplete'; end if;
 if e.metadata->>'amc_part' in ('speed','depth') then
  if (e.metadata->>'amc_part'='speed' and (e.question_count<>20 or e.duration_minutes<>20 or e.max_score<>70))
     or (e.metadata->>'amc_part'='depth' and (e.question_count<>10 or e.duration_minutes<>40 or e.max_score<>65))
  then raise exception 'Invalid AMC training paper format'; end if;
 end if;
 student_year=case when s.metadata->>'student_year'='6' then 6 else 5 end;
 estimated=e.award_cutoffs is null;
 cuts=coalesce(e.award_cutoffs,case when student_year=6 then '{"proficiency":32,"credit":58,"distinction":73,"high_distinction":92,"prize":118}'::jsonb else '{"proficiency":32,"credit":49,"distinction":64,"high_distinction":83,"prize":106}'::jsonb end);
 award=case when e.max_score<>135 then null when total=135 then 'Perfect practice score' when total>=coalesce((cuts->>'prize')::integer,999) then 'Prize range' when total>=coalesce((cuts->>'high_distinction')::integer,999) then 'High Distinction' when total>=coalesce((cuts->>'distinction')::integer,999) then 'Distinction' when total>=coalesce((cuts->>'credit')::integer,999) then 'Credit' when total>=coalesce((cuts->>'proficiency')::integer,32) then 'Proficiency' else 'Participation' end;
 finish_time=coalesce(s.submitted_at,clock_timestamp());
 duration_seconds=greatest(0,least(e.duration_minutes*60,extract(epoch from least(finish_time,s.expires_at)-s.started_at)::integer));
 version=coalesce(e.metadata->>'version','legacy-with-errata-20261112');
 result=jsonb_build_object('ok',true,'exam',to_jsonb(e)-'source_rights','score',total,'max_score',e.max_score,'award',jsonb_build_object('label',award,'estimated',estimated,'student_year',student_year),'rows',rows,'attempt_number',s.attempt_number,'submitted_at',finish_time,'time_used_seconds',duration_seconds,'question_version',version,'original_score',case when s.completed then s.score else total end,'review_corrected',s.completed and s.score is distinct from total);
 if not s.completed then
  update public.exam_sittings set score=total,completed=true,submitted_at=finish_time,metadata=coalesce(metadata,'{}'::jsonb)||jsonb_build_object('auto_submitted',p_auto or finish_time>=s.expires_at,'award',award,'award_estimated',estimated,'award_student_year',student_year,'time_used_seconds',duration_seconds,'question_version',version) where id=s.id;
 end if;
 insert into public.exam_result_snapshots(sitting_id,user_id,result) values(s.id,p_user_id,result);
 return result;
end;
$function$
;
commit;