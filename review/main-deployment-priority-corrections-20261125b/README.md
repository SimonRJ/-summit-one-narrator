# Narrow b-batch delivery verification

Prepared for `priority-corrections-20261125b`. The owner supplies the frozen source SHA, then the exact deployed SHA and successful Pages run before live mode is run.

The verifier compares the other **52 previously verified resource entries** against the published first deployment `d51e1382373a03aa0a3a828cfffa0a2a6c6a0198` using Git blob identities entirely offline. It confirms that deployment has the same tree as prepared source `e287b9102574b8a6cbc29beba97ccc9a7dc569fe`. These represent 51 distinct paths because the chapter script was verified under two query versions. The baseline records the earlier successful 66-resource public comparison and its report hash. The published commit makes the check reproducible without access to the original local-only preparation commit.

Live mode performs exactly **14 public GETs**: five unversioned entry pages/service-worker resources and nine app/catalogue resources using the new token. The downloaded catalogues are also checked for all **16 declared mappings**: canonical and consumer slots for S009, S010, S012, S015, S017, S019, S020 and S102. The expected release tags and film hashes are pinned, titles and film-use roles must agree, and bridge text is preserved.

There are no repeated movie, poster or font downloads, no browser/session actions, no learner endpoints, and no acceptance credit. Changed bytes or declarations fail the check; earlier delivery evidence is reused only when the corresponding source blob is unchanged.
