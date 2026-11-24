-- Source identity stays private and is not granted to the recording worker.
alter table public.protected_narration_work add column if not exists source_problem_id text references public.content_problems(id);

create table if not exists public.protected_film_visual_plans (
  source_problem_id text not null references public.content_problems(id),
  source_script_sha256 text not null check (source_script_sha256 ~ '^[a-f0-9]{64}$'),
  visual_direction text not null check (length(visual_direction) between 20 and 6000),
  direction_sha256 text not null check (direction_sha256 = encode(sha256(convert_to(visual_direction,'UTF8')),'hex')),
  renderer_sha256 text check (renderer_sha256 ~ '^[a-f0-9]{64}$'),
  primary key (source_problem_id, source_script_sha256)
);
alter table public.protected_film_visual_plans enable row level security;
revoke all on public.protected_film_visual_plans from public, anon, authenticated, service_role;
