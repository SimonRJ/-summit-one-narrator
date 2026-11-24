begin;
create table if not exists public.protected_narration_work (
  batch_id uuid not null,
  slot smallint not null check (slot between 1 and 32),
  scene_number smallint not null check (scene_number between 1 and 32),
  narration text not null check (length(narration) between 1 and 3000),
  narration_sha256 text not null check (narration_sha256 = encode(sha256(convert_to(narration,'UTF8')),'hex')),
  audio_flac bytea,
  audio_sha256 text,
  voice_evidence jsonb,
  primary key (batch_id, slot),
  check ((audio_flac is null and audio_sha256 is null and voice_evidence is null)
    or (audio_flac is not null and audio_sha256 is not null and voice_evidence is not null
      and octet_length(audio_flac) between 1024 and 5000000
      and substring(audio_flac from 1 for 4) = decode('664c6143','hex')
      and audio_sha256 = encode(sha256(audio_flac),'hex')))
);
alter table public.protected_narration_work enable row level security;
revoke all on public.protected_narration_work from public, anon, authenticated, service_role;
grant select (batch_id, slot, scene_number, narration, narration_sha256, audio_sha256)
  on public.protected_narration_work to service_role;
grant update (audio_flac, audio_sha256, voice_evidence) on public.protected_narration_work to service_role;
commit;
