-- An administrator stages reviewed media; the service reads and removes it after verified delivery.
begin;
create table if not exists public.protected_film_parts (
  film_id text not null check (film_id ~ '^(A[0-9]{3}|K[0-9]{3}|N[1-4][.](26|27|28|29|30))$'),
  media_sha256 text not null check (media_sha256 ~ '^[a-f0-9]{64}$'),
  part_count smallint not null check (part_count between 1 and 512),
  part_number smallint not null check (part_number >= 0 and part_number < part_count),
  bytes bytea not null check (octet_length(bytes) between 1 and 98304),
  primary key (film_id, media_sha256, part_number)
);
alter table public.protected_film_parts enable row level security;
revoke all on table public.protected_film_parts from public, anon, authenticated, service_role;
grant select, delete on table public.protected_film_parts to service_role;
commit;
