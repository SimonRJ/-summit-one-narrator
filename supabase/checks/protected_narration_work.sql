-- Run as the project administrator. Raises on an unexpected production access grant or broken source link.
do $$
declare
  name text;
  role_name text;
  column_name text;
begin
  foreach name in array array['protected_narration_work','protected_film_visual_plans'] loop
    assert (select relrowsecurity from pg_class where oid=format('public.%I',name)::regclass),
      format('Row security is required on %I',name);
    foreach role_name in array array['anon','authenticated'] loop
      for column_name in select attname from pg_attribute
        where attrelid=format('public.%I',name)::regclass and attnum>0 and not attisdropped loop
        assert not has_column_privilege(role_name,format('public.%I',name),column_name,'SELECT,INSERT,UPDATE'),
          format('Unexpected learner permission on %I.%I',name,column_name);
      end loop;
    end loop;
  end loop;
  assert not has_column_privilege('service_role','public.protected_narration_work','source_problem_id','SELECT,UPDATE');
  assert not has_column_privilege('service_role','public.protected_narration_work','narration','UPDATE');
  assert not has_column_privilege('service_role','public.protected_narration_work','audio_flac','SELECT');
  assert has_column_privilege('service_role','public.protected_narration_work','audio_flac','UPDATE');
  assert not has_table_privilege('service_role','public.protected_film_visual_plans','SELECT,INSERT,UPDATE');
  assert not exists (select 1 from public.protected_narration_work n left join public.content_problems p
    on p.id=n.source_problem_id where n.source_problem_id is not null and p.id is null);
end $$;
