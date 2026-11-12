-- One permanent sitting per pupil and paper. Existing sittings are retained.
create unique index if not exists exam_sittings_one_attempt
  on public.exam_sittings(user_id,exam_id);

alter table public.exam_sittings enable row level security;
-- This older permissive ALL policy allowed any member to affect any sitting.
drop policy if exists exams_member_only on public.exam_sittings;
drop policy if exists exams_insert_own on public.exam_sittings;
create policy exams_insert_own on public.exam_sittings for insert to authenticated
  with check ((select auth.uid())=user_id and completed=false and score is null and submitted_at is null);
drop policy if exists exams_update_own_open on public.exam_sittings;
create policy exams_update_own_open on public.exam_sittings for update to authenticated
  using ((select auth.uid())=user_id and completed=false and expires_at>now())
  with check ((select auth.uid())=user_id and completed=false and score is null and submitted_at is null);
-- Keep exams_select_own: finished papers remain readable without an age limit.
revoke all on public.exam_sittings from anon;
revoke delete,truncate,references,trigger on public.exam_sittings from authenticated;

create or replace function public.prevent_completed_exam_mutation()
returns trigger language plpgsql security invoker set search_path='' as $$
declare paper public.exam_catalog%rowtype;
begin
  if tg_op='INSERT' then
    if current_user='authenticated' then
      if new.user_id is distinct from auth.uid() then
        raise exception 'You can only start your own exam attempt';
      end if;
      select * into paper from public.exam_catalog where id=new.exam_id and active=true;
      if not found then raise exception 'This paper is not available'; end if;
      if new.completed or new.score is not null or new.submitted_at is not null then
        raise exception 'A new attempt must be unsubmitted';
      end if;
      new.started_at=clock_timestamp();
      new.expires_at=new.started_at+make_interval(mins=>paper.duration_minutes);
      new.created_at=new.started_at;
      new.exam_year=paper.year;
      new.max_score=paper.max_score;
      new.responses='{}'::jsonb;
      new.integer_save_times='{}'::jsonb;
    end if;
    return new;
  end if;
  if old.completed then raise exception 'Completed exam sittings are immutable'; end if;
  if current_user='authenticated' then
    if clock_timestamp()>=old.expires_at then raise exception 'This exam has ended. Saved answers are locked'; end if;
    if (to_jsonb(new)-array['responses','integer_save_times']) is distinct from
       (to_jsonb(old)-array['responses','integer_save_times']) then
      raise exception 'Only answers can be changed during an open exam attempt';
    end if;
  end if;
  return new;
end;
$$;
drop trigger if exists trg_prevent_completed_exam_mutation on public.exam_sittings;
create trigger trg_prevent_completed_exam_mutation before insert or update on public.exam_sittings
for each row execute function public.prevent_completed_exam_mutation();
revoke execute on function public.prevent_completed_exam_mutation() from public,anon,authenticated;
