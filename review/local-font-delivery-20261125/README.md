# Local font delivery check

The same official Source Sans 3, Source Serif 4, Source Code Pro and STIX Two Math WOFF2 files are now served from the site. Their bytes and all upstream family/style/weight/Unicode-range declarations are unchanged. The source and license hashes are in `../../fonts/sources.json`.

The lesson gallery was checked in desktop Chromium and iPhone WebKit emulation with both Google font domains blocked. All 13 requested weight/style combinations loaded successfully from the local site, neither profile requested an external font, and horizontal overflow was zero. The screenshots retain the deliberate blocked-backend fallback catalogue; this check establishes font delivery and layout, not live backend availability.

Desktop Chromium then installed the service worker and verified that all 28 public font files were cached. With browser networking disabled, a fresh document loaded the offline reader, its opening lesson and all 13 font combinations. The reader remained light, with no horizontal overflow. The two JSON result files and the gallery/reader screenshots record these actual outcomes.

The earlier deployed S012 navigation trace in `external-font-navigation-trace.json` measured 39.999 seconds to DOM readiness: the public HTML took about 19.7 seconds and the imported Google Fonts stylesheet added about 18.7 seconds. Removing that external import eliminates this particular dependency. The trace is environment-specific and is not a general production benchmark.

`tools/check_local_fonts.py` is the reusable browser check. This run used the existing pinned Chromium/WebKit executables and the workspace proxy certificate accommodation. It does not constitute physical iPhone testing. Actual Supabase requests were blocked, and no learner records were used or changed.

Public HTML references and both page generators now request the same versioned local design/theme stylesheets. The shared service-worker revision includes the immutable, hash-named font files. Deployed byte verification remains a separate gate after publication.
