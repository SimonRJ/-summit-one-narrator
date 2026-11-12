-- Additive protections: preserve existing data, grants, policies and triggers.
create unique index if not exists exam_sittings_one_attempt on public.exam_sittings(user_id,exam_id);
alter table public.exam_sittings enable row level security;
create policy exam_owner_guard on public.exam_sittings as restrictive for all to authenticated
  using ((select auth.uid())=user_id) with check ((select auth.uid())=user_id);
create policy exam_insert_guard on public.exam_sittings as restrictive for insert to authenticated
  with check (completed=false and score is null and submitted_at is null);
create policy exam_update_guard on public.exam_sittings as restrictive for update to authenticated
  using (completed=false and expires_at>now())
  with check (completed=false and score is null and submitted_at is null);
create policy exam_delete_guard on public.exam_sittings as restrictive for delete to authenticated
  using (false);
create or replace function public.guard_exam_attempt()
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
create trigger exam_attempt_guard before insert or update on public.exam_sittings
for each row execute function public.guard_exam_attempt();
