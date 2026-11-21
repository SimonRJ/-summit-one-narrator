-- Supplementary teaching for a frozen solution after the usual attempt check.
create table public.solution_clarifications (
    problem_id text not null references public.content_problems(id),
    revision integer not null check (revision > 0),
    note text not null check (length(trim(note)) > 0),
    primary key (problem_id, revision)
);
alter table public.solution_clarifications enable row level security;
revoke all on table public.solution_clarifications from public, anon, authenticated, service_role;
grant select on table public.solution_clarifications to service_role;
