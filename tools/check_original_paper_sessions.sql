-- Test installed practice papers through the production answer-saving and grading
-- functions. Run from an administrative SQL session. Every synthetic learner,
-- answer, repair and result is rolled back. The output contains aggregate counts.
begin;
set local statement_timeout = '90s';
set local lock_timeout = '3s';

create temporary table verified_papers (
  paper_id text primary key,
  question_count integer,
  maximum_score integer
) on commit drop;

do $review$
declare
  paper public.exam_catalog%rowtype;
  learner uuid;
  sitting uuid;
  keys jsonb;
  result jsonb;
  number integer;
  first_number integer;
  last_number integer;
  last_marks integer;
  omit_last boolean;
  expected_score integer;
  rejected boolean;
begin
  for paper in
    select * from public.exam_catalog
    where active and (source_type = 'summit_amc_split_original'
      or id like 'summit-rossmoyne-practice-v2-%' or id = 'rossmoyne-original-sample-v2')
    order by id
  loop
    select jsonb_object_agg(question_number,
      case when jsonb_typeof(answer) = 'object'
        then coalesce(answer->>'choice', answer->>'value', answer->>'answer')
        else answer#>>'{}' end),
      min(question_number), max(question_number)
      into keys, first_number, last_number
      from public.exam_questions where exam_id = paper.id;
    select marks into strict last_marks from public.exam_questions
      where exam_id = paper.id and question_number = last_number;

    foreach omit_last in array array[false, true] loop
      begin
        learner := gen_random_uuid();
        insert into auth.users(id) values (learner);
        insert into public.profiles(id) values (learner) on conflict (id) do nothing;
        perform set_config('request.jwt.claim.sub', learner::text, true);
        perform set_config('request.jwt.claims',
          jsonb_build_object('sub', learner, 'role', 'authenticated')::text, true);

        execute 'set local role authenticated';
        insert into public.exam_sittings(user_id, exam_id, started_at, expires_at)
          values (learner, paper.id, now(), now())
          returning id into sitting;
        if not exists (select 1 from public.exam_sittings where id = sitting
          and expires_at - started_at = make_interval(mins => paper.duration_minutes)) then
          raise exception 'Timer mismatch for %', paper.id;
        end if;

        for number in select question_number from public.exam_questions_student
          where exam_id = paper.id order by question_number
        loop
          if not omit_last or number <> last_number then
            perform public.save_exam_response(sitting, number, keys->>number::text);
          end if;
        end loop;

        execute 'reset role';
        execute 'set local role service_role';
        result := public.seal_exam_result(sitting, learner, false);
        expected_score := paper.max_score - (case when omit_last then last_marks else 0 end);
        if (result->>'score')::integer is distinct from expected_score
          or jsonb_array_length(result->'rows') is distinct from paper.question_count
          or exists (select 1 from jsonb_array_elements(result->'rows') item
            where coalesce(item->>'explanation','') = '') then
          raise exception 'Score or worked report mismatch for %', paper.id;
        end if;
        if public.seal_exam_result(sitting, learner, false) is distinct from result then
          raise exception 'Result changed on a second request for %', paper.id;
        end if;

        execute 'reset role';
        execute 'set local role authenticated';
        rejected := false;
        begin
          perform public.save_exam_response(sitting, first_number, 'A');
        exception when raise_exception then
          if sqlerrm <> 'This attempt is not open for answers' then raise; end if;
          rejected := true;
        end;
        if not rejected then raise exception 'Closed answer was editable for %', paper.id; end if;

        if not paper.repeatable then
          rejected := false;
          begin
            insert into public.exam_sittings(user_id, exam_id, started_at, expires_at)
              values (learner, paper.id, now(), now());
          exception when raise_exception then
            if sqlerrm not like '%one attempt%' then raise; end if;
            rejected := true;
          end;
          if not rejected then raise exception 'Second attempt allowed for %', paper.id; end if;
        end if;
        execute 'reset role';
        raise exception using errcode = 'ZX901', message = 'Discard the verified fixture';
      exception when sqlstate 'ZX901' then null;
      end;
      if exists (select 1 from auth.users where id = learner)
        or exists (select 1 from public.exam_sittings where user_id = learner) then
        raise exception 'Synthetic fixture survived for %', paper.id;
      end if;
    end loop;
    insert into verified_papers values (paper.id, paper.question_count, paper.max_score);
  end loop;
end $review$;
select count(*) as papers, sum(question_count)::integer as questions,
  2 * count(*) as graded_synthetic_attempts from verified_papers;
rollback;
