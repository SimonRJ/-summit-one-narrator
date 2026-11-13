begin;
-- One assessment sitting only: completed papers are immutable and can be reviewed forever.
update public.exam_catalog set repeatable=false,
 metadata=coalesce(metadata,'{}'::jsonb)||'{"attempt_policy":"single_attempt_per_paper","post_submit":"review_only","target_set_count":30}'::jsonb
where metadata->>'amc_part' in ('speed','depth') and active=true;

-- Reused full-mock questions do NOT satisfy the new unseen-original requirement.
-- Retire from new exam selection while retaining all catalog/question/sitting records.
update public.exam_catalog as e set active=false,
 metadata=coalesce(e.metadata,'{}'::jsonb)||'{"retired_reason":"reused_prior_full_mock_not_new_original","review_only":true}'::jsonb
where e.source_type='summit_amc_split_familiarisation'
and not exists(select 1 from public.exam_sittings s where s.exam_id=e.id and s.completed=false);

-- Old complete AMC mocks also cease appearing in the new AMC workflow, without deletion.
update public.exam_catalog as e set active=false,
 metadata=coalesce(e.metadata,'{}'::jsonb)||'{"retired_reason":"part_A_part_B_and_real_only","review_only":true}'::jsonb
where e.source_type='original_authored_mock' and e.max_score=135
and not exists(select 1 from public.exam_sittings s where s.exam_id=e.id and s.completed=false);

-- Independently authored splits are only available once; preserve existing attempts.
update public.exam_catalog set repeatable=false where source_type='summit_amc_split_original' and active;
commit;