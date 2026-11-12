-- Run ONLY inside a transaction that is rolled back, after exam_single_attempt.sql.
-- Uses one existing profile and paper; no fixture sitting is retained.
do $$ declare pupil uuid; begin
  select id into pupil from public.profiles limit 1;
  if pupil is null then raise exception 'Verification needs an existing profile'; end if;
  perform set_config('request.jwt.claim.sub',pupil::text,true);
  perform set_config('request.jwt.claims',jsonb_build_object('sub',pupil,'role','authenticated')::text,true);
end $$;
set local role authenticated;
do $$ declare row public.exam_sittings%rowtype; blocked boolean; begin
  insert into public.exam_sittings(user_id,exam_id,started_at,expires_at)
  values(auth.uid(),'amc-up-2025','2000-01-01','2099-01-01') returning * into row;
  if abs(extract(epoch from row.started_at-clock_timestamp()))>5 or row.expires_at-row.started_at<>interval '60 minutes' then
    raise exception 'Server must own start and expiry times';
  end if;
  update public.exam_sittings set responses='{"1":"A"}' where id=row.id;
  blocked=false;
  begin
    insert into public.exam_sittings(user_id,exam_id,started_at,expires_at)
    values(auth.uid(),'amc-up-2025',now(),now()+interval '60 minutes');
  exception when unique_violation then blocked=true; end;
  if not blocked then raise exception 'Duplicate open attempt allowed'; end if;
  blocked=false;
  begin update public.exam_sittings set expires_at=now()+interval '2 hours' where id=row.id;
  exception when raise_exception or insufficient_privilege then blocked=true; end;
  if not blocked then raise exception 'Timer reset allowed'; end if;
  blocked=false;
  begin update public.exam_sittings set completed=true,score=135 where id=row.id;
  exception when raise_exception or insufficient_privilege then blocked=true; end;
  if not blocked then raise exception 'Student self-grading allowed'; end if;
  blocked=false;
  begin insert into public.exam_sittings(user_id,exam_id,started_at,expires_at)
    values(gen_random_uuid(),'amc-up-2025',now(),now()+interval '1 hour');
  exception when raise_exception or insufficient_privilege then blocked=true; end;
  if not blocked then raise exception 'Student can create another pupil attempt'; end if;
end $$;
reset role;
update public.exam_sittings set expires_at=now()-interval '1 second'
where user_id=auth.uid() and exam_id='amc-up-2025';
set local role authenticated;
do $$ declare affected integer; begin
  update public.exam_sittings set responses='{"1":"B"}' where user_id=auth.uid() and exam_id='amc-up-2025';
  get diagnostics affected=row_count;
  if affected<>0 then raise exception 'Expired answers can still change'; end if;
end $$;
reset role;
update public.exam_sittings set completed=true,score=3,submitted_at=now()
where user_id=auth.uid() and exam_id='amc-up-2025';
set local role authenticated;
do $$ declare affected integer; blocked boolean=false; begin
  update public.exam_sittings set responses='{"1":"B"}' where user_id=auth.uid() and exam_id='amc-up-2025';
  get diagnostics affected=row_count;
  if affected<>0 then raise exception 'Completed answers can still change'; end if;
  begin insert into public.exam_sittings(user_id,exam_id,started_at,expires_at)
    values(auth.uid(),'amc-up-2025',now(),now()+interval '1 hour');
  exception when unique_violation then blocked=true; end;
  if not blocked then raise exception 'Retake after submission allowed'; end if;
  if (select count(*) from public.exam_sittings where user_id=auth.uid() and exam_id='amc-up-2025' and completed)<>1 then
    raise exception 'Completed review no longer accessible';
  end if;
end $$;
reset role;
