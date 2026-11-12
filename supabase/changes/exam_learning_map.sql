-- Teaching guidance is available only to the owner of a submitted sitting.
-- Keep answer-bearing metadata out of exam_questions_student.
create or replace function public.get_exam_learning_map(p_sitting_id uuid)
returns table(question_number integer, category text, metadata jsonb)
language sql stable security definer set search_path = ''
as $$
  select q.question_number, q.category,
    jsonb_build_object('skill_id', q.category,
      'learning_map', q.metadata -> 'learning_map')
  from public.exam_sittings s
  join public.exam_questions q on q.exam_id = s.exam_id
  where s.id = p_sitting_id and s.user_id = (select auth.uid())
    and s.completed is true and s.submitted_at is not null
  order by q.question_number;
$$;
revoke all on function public.get_exam_learning_map(uuid) from public, anon;
grant execute on function public.get_exam_learning_map(uuid) to authenticated;
comment on function public.get_exam_learning_map(uuid) is
  'Owner-only post-submission teaching map. Does not return answers or solution metadata.';
