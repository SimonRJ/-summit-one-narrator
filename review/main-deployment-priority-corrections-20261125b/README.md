# Narrow b-batch delivery verification

Prepared for `priority-corrections-20261125b`. The owner supplies the frozen source SHA, then the exact deployed SHA and successful Pages run before live mode is run.

The verifier compares the other **52 previously verified resource entries** against the published first deployment `d51e1382373a03aa0a3a828cfffa0a2a6c6a0198` using Git blob identities entirely offline. It confirms that deployment has the same tree as prepared source `e287b9102574b8a6cbc29beba97ccc9a7dc569fe`. These represent 51 distinct paths because the chapter script was verified under two query versions. The baseline records the earlier successful 66-resource public comparison and its report hash. The published commit makes the check reproducible without access to the original local-only preparation commit.

Live mode performs exactly **14 public GETs**: five unversioned entry pages/service-worker resources and nine app/catalogue resources using the new token. The downloaded catalogues are also checked for all **16 declared mappings**: canonical and consumer slots for S009, S010, S012, S015, S017, S019, S020 and S102. The expected release tags and film hashes are pinned, titles and film-use roles must agree, and bridge text is preserved.

There are no repeated movie, poster or font downloads, no browser/session actions, no learner endpoints, and no acceptance credit. Changed bytes or declarations fail the check; earlier delivery evidence is reused only when the corresponding source blob is unchanged.

## Final deployment result

All checks passed for deployed commit `900035e645847900726a85eb59e3a3104a6bca66`, published from frozen local source `48a2b77359c2b555e26a7a77e20a25c13d2c78c3` with identical tree `1f0b2371c192b193ece555fbebbf66d9a67028b3`.

`offline-preflight-48a2b77-20261125.json` preserves the original pre-publication result: zero HTTP requests, all 52 retained entries unchanged, and all 16 source declarations and cache references valid. It is unchanged from that first offline observation.

After the parent confirmed Pages run **45530708173** succeeded at **02:09:12 UTC on 25 November 2026**, the verifier made its 14 public GETs. Every response returned HTTP 200 and matched the final source bytes exactly. The fetched catalogues also passed all 16 pinned canonical/consumer mappings, bridge-preservation checks, title/role checks and b cache references. `live-byte-comparison-900035e-20261125.json` records these results and the identical retained-resource comparison.

No media or font download was repeated, and no product, main-ref, learner or editorial-acceptance change was made by this verification. This final runtime evidence is preserved separately from the deployed main source.
