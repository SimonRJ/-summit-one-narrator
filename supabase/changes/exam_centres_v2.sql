-- Separate repeatable practice from one-attempt assessment; preserve every existing sitting.
alter table public.exam_catalog add column if not exists repeatable boolean not null default false;
alter table public.exam_sittings add column if not exists attempt_number integer not null default 1;
drop index if exists public.exam_sittings_one_attempt;
create unique index if not exists exam_sittings_one_open_attempt on public.exam_sittings(user_id,exam_id) where completed=false;
create unique index if not exists exam_sittings_attempt_sequence on public.exam_sittings(user_id,exam_id,attempt_number);

create table if not exists public.exam_result_snapshots (
 sitting_id uuid primary key references public.exam_sittings(id),
 user_id uuid not null references auth.users(id),
 result jsonb not null,
 created_at timestamptz not null default now()
);
alter table public.exam_result_snapshots enable row level security;
revoke all on public.exam_result_snapshots from anon,authenticated;
grant all on public.exam_result_snapshots to service_role;

create table if not exists public.learning_repairs (
 id uuid primary key default gen_random_uuid(), user_id uuid not null references auth.users(id),
 source_type text not null, source_ref text not null, source_label text not null,
 skill_id text not null, classification text, stage integer not null default 0 check(stage between 0 and 4),
 due_after_session integer not null default 0, evidence jsonb not null default '{}'::jsonb,
 created_at timestamptz not null default now(), updated_at timestamptz not null default now(),
 unique(user_id,source_type,source_ref,skill_id)
);
alter table public.learning_repairs enable row level security;
grant select,insert,update on public.learning_repairs to authenticated;
grant all on public.learning_repairs to service_role;
create policy repair_owner_select on public.learning_repairs for select to authenticated using ((select auth.uid())=user_id);
create policy repair_owner_insert on public.learning_repairs for insert to authenticated with check ((select auth.uid())=user_id);
create policy repair_owner_update on public.learning_repairs for update to authenticated using ((select auth.uid())=user_id) with check ((select auth.uid())=user_id);
create index if not exists learning_repairs_owner_due on public.learning_repairs(user_id,stage,due_after_session);

create table if not exists public.investigation_reviews (
 id uuid primary key default gen_random_uuid(), user_id uuid not null references auth.users(id),
 session_number integer not null, reviewer_name text not null,
 reviewer_role text not null check(reviewer_role in ('parent','tutor')),
 rubric jsonb not null, notes text not null default '',
 reviewed_at timestamptz not null default now()
);
alter table public.investigation_reviews enable row level security;
grant select,insert on public.investigation_reviews to authenticated;
grant all on public.investigation_reviews to service_role;
create policy investigation_review_owner_read on public.investigation_reviews for select to authenticated using ((select auth.uid())=user_id);
create policy investigation_review_owner_add on public.investigation_reviews for insert to authenticated with check ((select auth.uid())=user_id);
create index if not exists investigation_reviews_owner on public.investigation_reviews(user_id,session_number);

create or replace function public.guard_exam_attempt()
returns trigger language plpgsql security invoker set search_path='' as $$
declare paper public.exam_catalog%rowtype; previous_count integer;
begin
 if tg_op='INSERT' then
  if current_user='authenticated' and new.user_id is distinct from auth.uid() then raise exception 'You can only start your own exam attempt'; end if;
  select * into paper from public.exam_catalog where id=new.exam_id and active=true;
  if not found then raise exception 'This paper is not available'; end if;
  -- Serialise concurrent starts for one learner and paper.
  perform pg_advisory_xact_lock(hashtextextended(new.user_id::text||':'||new.exam_id,0));
  select count(*) into previous_count from public.exam_sittings where user_id=new.user_id and exam_id=new.exam_id;
  if previous_count>0 and not paper.repeatable then raise exception 'This paper has one attempt. Open the saved sitting to review or resume.'; end if;
  if exists(select 1 from public.exam_sittings where user_id=new.user_id and exam_id=new.exam_id and completed=false) then raise exception 'Resume the open attempt before starting another.'; end if;
  if new.completed or new.score is not null or new.submitted_at is not null then raise exception 'A new attempt must be unsubmitted'; end if;
  new.attempt_number=previous_count+1;
  new.started_at=clock_timestamp(); new.expires_at=new.started_at+make_interval(mins=>paper.duration_minutes);
  new.created_at=new.started_at; new.exam_year=paper.year; new.max_score=paper.max_score;
  new.responses='{}'::jsonb;new.integer_save_times='{}'::jsonb;
  new.metadata=coalesce(new.metadata,'{}'::jsonb)||jsonb_build_object('title',paper.title,'repeatable',paper.repeatable,'question_version',coalesce(paper.metadata->>'version','legacy'),'attempt_number',new.attempt_number);
  return new;
 end if;
 if old.completed then raise exception 'Completed exam sittings are immutable'; end if;
 if current_user='authenticated' then
  if clock_timestamp()>=old.expires_at then raise exception 'This exam has ended. Saved answers are locked'; end if;
  if (to_jsonb(new)-array['responses','integer_save_times']) is distinct from (to_jsonb(old)-array['responses','integer_save_times']) then raise exception 'Only answers can be changed during an open exam attempt'; end if;
 end if;
 return new;
end;
$$;

-- Safe question view has diagrams, but never keys or explanations.
create or replace view public.exam_questions_student with (security_invoker=true) as
select exam_id,question_number,question_type,stem,choices,marks,image_ref,figure_svg,category from public.exam_questions;
grant select(figure_svg,category) on public.exam_questions to authenticated;
grant select on public.exam_questions_student to authenticated;

create or replace function public.save_exam_response(p_sitting_id uuid,p_question integer,p_response text)
returns public.exam_sittings language plpgsql security invoker set search_path='' as $$
declare s public.exam_sittings%rowtype; e public.exam_catalog%rowtype; question_kind text; option_count integer;
begin
 select * into s from public.exam_sittings where id=p_sitting_id and user_id=auth.uid() for update;
 if not found or s.completed or clock_timestamp()>=s.expires_at then raise exception 'This attempt is not open for answers'; end if;
 select * into e from public.exam_catalog where id=s.exam_id;
 select question_type,jsonb_array_length(choices) into question_kind,option_count from public.exam_questions_student where exam_id=s.exam_id and question_number=p_question;
 if not found then raise exception 'Question not found'; end if;
 if p_response is not null then
  if question_kind='multiple_choice' and not(p_response ~ '^[A-Z]$' and ascii(p_response)-64 between 1 and option_count) then raise exception 'Choose a listed option'; end if;
  if question_kind='integer' and not(p_response ~ (case when e.max_score=135 then '^[0-9]{1,3}$' else '^[0-9]{1,6}$' end)) then raise exception 'Enter a valid whole-number answer'; end if;
 end if;
 update public.exam_sittings set responses=case when p_response is null then responses-p_question::text else jsonb_set(responses,array[p_question::text],to_jsonb(p_response),true) end,
 integer_save_times=case when p_response is null then integer_save_times-p_question::text when question_kind='integer' then jsonb_set(integer_save_times,array[p_question::text],to_jsonb(clock_timestamp()),true) else integer_save_times end
 where id=s.id returning * into s;
 return s;
end;
$$;
revoke all on function public.save_exam_response(uuid,integer,text) from public,anon;
grant execute on function public.save_exam_response(uuid,integer,text) to authenticated;

-- Invoker RPC: only the authenticated Edge Function's service role can execute it.
-- The row lock covers reading answers, grading, sealing and the immutable snapshot.
create or replace function public.seal_exam_result(p_sitting_id uuid,p_user_id uuid,p_auto boolean default false)
returns jsonb language plpgsql security invoker set search_path='' as $$
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
  else ok=coalesce(response ~ (case when e.max_score=135 then '^[0-9]{1,3}$' else '^[0-9]{1,6}$' end),false);
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
$$;
revoke all on function public.seal_exam_result(uuid,uuid,boolean) from public,anon,authenticated;
grant execute on function public.seal_exam_result(uuid,uuid,boolean) to service_role;

-- Retire the old star-award action. Historical counters are inert archival data.
drop function if exists public.increment_timed_star_correct(uuid,integer,integer,integer);
revoke all on public.learning_repairs,public.investigation_reviews from anon;
