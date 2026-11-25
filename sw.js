const scope = new URL(self.registration.scope);
const CACHE="summit-one-priority-corrections-20261125b";
const cachePrefix = scope.pathname + ':summit-one-';
const cacheName = scope.pathname + ':' + CACHE;
const reader = new URL('offline-reader.html', scope).href;
const staticFiles = [
  "./fonts/stix-two-math-normal-all-8b2a6834cf.woff2",
  "./fonts/source-code-pro-normal-cyrillic-ext-dd503d60c3.woff2",
  "./fonts/source-code-pro-normal-cyrillic-fd7699ecbd.woff2",
  "./fonts/source-code-pro-normal-greek-ext-01e467c83c.woff2",
  "./fonts/source-code-pro-normal-greek-34dfcd3f61.woff2",
  "./fonts/source-code-pro-normal-vietnamese-d8a28d78c1.woff2",
  "./fonts/source-code-pro-normal-latin-ext-ab316ee7e4.woff2",
  "./fonts/source-code-pro-normal-latin-8b774aaa51.woff2",
  "./fonts/source-sans-3-italic-cyrillic-ext-9f9b2a3d40.woff2",
  "./fonts/source-sans-3-italic-cyrillic-747ba5266e.woff2",
  "./fonts/source-sans-3-italic-greek-ext-eed2194fd9.woff2",
  "./fonts/source-sans-3-italic-greek-7ebcf40b8c.woff2",
  "./fonts/source-sans-3-italic-vietnamese-aa44d57632.woff2",
  "./fonts/source-sans-3-italic-latin-ext-6fe10a66ec.woff2",
  "./fonts/source-sans-3-italic-latin-5fbc14d56c.woff2",
  "./fonts/source-sans-3-normal-cyrillic-ext-c6e007862d.woff2",
  "./fonts/source-sans-3-normal-cyrillic-b6b721e08d.woff2",
  "./fonts/source-sans-3-normal-greek-ext-67fbab24bd.woff2",
  "./fonts/source-sans-3-normal-greek-dd6ec3878c.woff2",
  "./fonts/source-sans-3-normal-vietnamese-a91edbcdcb.woff2",
  "./fonts/source-sans-3-normal-latin-ext-a85a7459bd.woff2",
  "./fonts/source-sans-3-normal-latin-19143dca07.woff2",
  "./fonts/source-serif-4-normal-cyrillic-ext-da49e14ae1.woff2",
  "./fonts/source-serif-4-normal-cyrillic-a81082707b.woff2",
  "./fonts/source-serif-4-normal-greek-54c4728aa0.woff2",
  "./fonts/source-serif-4-normal-vietnamese-c3de01b514.woff2",
  "./fonts/source-serif-4-normal-latin-ext-d10ccbbd0d.woff2",
  "./fonts/source-serif-4-normal-latin-382475f382.woff2",
  "./figures/read-practice/S094.svg",
  "./figures/read-practice/S209.svg",
  "./exam-flags.js?v=deeper-20261121",
  "./figure-viewer.js?v=deeper-20261121",
  "./figure-viewer.css?v=deeper-20261121",
  "./route-model.js?v=paths-20261121",
  "./route-model.css?v=paths-20261121",
  "./offline-reader.html",
  "./public-study-theme.css?v=local-fonts-20261125",
  "./notebook-challenges.js",
  "./offline-reader.js?v=priority-corrections-20261125b",
  "./domino-model.js?v=github-20261121",
  "./domino-model.css?v=github-20261121",
  "./model-claims.js?v=powers-20261122",
  "./example-methods.js?v=course-review-20261122-a",
  "./lesson-models.js?v=powers-20261122",
  "./lesson-models.css?v=deeper-20261121",
  "./data/read-watch-practise-later.json?v=priority-corrections-20261125b",
  "./figures/read-practice/S002.svg",
  "./figures/read-practice/S003.svg",
  "./figures/read-practice/S006.svg",
  "./figures/read-practice/S008.svg",
  "./figures/read-practice/S017.svg",
  "./figures/read-practice/S019.svg",
  "./figures/read-practice/S024.svg",
  "./figures/read-practice/S036.svg",
  "./figures/read-practice/S043.svg",
  "./figures/read-practice/S046.svg",
  "./figures/read-practice/S053.svg",
  "./figures/read-practice/S061.svg",
  "./figures/read-practice/S075.svg",
  "./figures/read-practice/S086.svg",
  "./figures/read-practice/S095.svg",
  "./figures/read-practice/S104.svg",
  "./figures/read-practice/S106.svg",
  "./figures/read-practice/S124.svg",
  "./figures/read-practice/S125.svg",
  "./figures/read-practice/S129.svg",
  "./figures/read-practice/S141.svg",
  "./figures/read-practice/S173.svg",
  "./figures/read-practice/S232.svg",
  "./figures/read-practice/S323.svg",
  "./figures/read-practice/S355.svg",
  "./figures/read-practice/S362.svg",
  "./figures/read-practice/S368.svg",
  "./reviewed-lesson.js?v=full-lessons-20261125",
  "./data/read-watch-practise.json?v=priority-corrections-20261125b",
  "./read-practice.css?v=tablet-readings-20261125",
  "./coverage.html",
  "./coverage.js?v=topic-label-20261122",
  "./data/amc-coverage.json?v=recognition-20261113",
  "./recognition.js?v=recognition-20261113",
  "./exam-diagnostics.js?v=recognition-20261113",
  "./welcome.html",
  "./lesson-video-chapters.js?v=chapter-seek-20261122",
  "./welcome.js?v=course-films-target-clock-20261125",
  "./welcome.css?v=chapter-navigation-20261122",
  "./transfer-practice.js?v=github-20261121",
  "./learning-support.js?v=github-20261121",
  "./exam-rules.js?v=split-20261113",
  "./flash-cards.js?v=standalone-cards-20261122",
  "./flash-ui.js?v=standalone-cards-20261122",
  "./original-learning.js?v=upper-primary-audit-20261114",
  "./data/lesson-challenges.json?v=upper-primary-audit-20261114",
  "./",
  "./index.html",
  "./teaching-videos.html",
  "./lesson-introduction-videos.html",
  "./watch-lesson-intro.html",
  "./lesson-introduction-library.js?v=priority-corrections-20261125b",
  "./lesson-introduction-watch.js?v=lesson-intros-v7",
  "./boot-loader.js?v=identity-math-20261113",
  "./boot-loader.css?v=cinematic-20261113",
  "./main.css?v=worked-films-20261122",
  "./summit-polish.css?v=craft-20261121",
  "./app-main.js?v=priority-corrections-20261125b",
  "./workshop-studies.js?v=workshops-20261122",
  "./course-menu.js?v=menu-20261113",
  "./course-menu-ui.js?v=priority-corrections-20261125b",
  "./data/recorded-studies.json?v=priority-corrections-20261125b",
  "./lesson-introduction-media.js?v=priority-corrections-20261125b",
  "./lesson-pager.js?v=responsive-20261113",
  "./lesson-screenflow.js?v=data-audit-20261114",
  "./lesson-player.js",
  "./advanced-connections.js?v=technique-transfers-20261121",
  "./advanced-number.js?v=technique-transfers-20261121",
  "./advanced-counting.js?v=technique-transfers-20261121",
  "./advanced-geometry.js?v=technique-transfers-20261121",
  "./curriculum.js?v=recognition-20261113",
  "./learning-ui.js?v=study-pace-20261122",
  "./session-intros.js?v=mawa-visits-20261121",
  "./lesson-journeys.js?v=recognition-20261113",
  "./problem-figures.js",
  "./login.html",
  "./login.js?v=accessible-form-20261122",
  "./supabase-client.js?v=auth-20261112",
  "./tests.html",
  "./tests.js?v=full-marks-20261122",
  "./exam.css?v=deeper-20261121",
  "./manifest.webmanifest",
  "./icon.svg",
  "./summit-mark.svg",
  "./design-system.css?v=local-fonts-20261125",
  "./math-typography.js?v=advanced-20261113",
  "./robots.txt",
  "./data/skill-session-links.json?v=review-20261113",
  "./data/sessions-372.json",
  "./data/teaching-72.json?v=priority-corrections-20261125b",
  "./data/mawa-investigations-20.json?v=mawa-visits-20261121",
  "./data/rossmoyne-h23.json",
  "./data/taxonomy-52.json",
  "./data/amc-awards.json",
  "./data/milestones.json"
].map(path => new URL(path, scope).href);
const allowed = new Set(staticFiles);

self.addEventListener('install', event => {
  event.waitUntil((async () => {
    const cache = await caches.open(cacheName);
    // addAll is atomic. A failed download must leave the previous worker active.
    await cache.addAll(staticFiles.map(url => new Request(url, {cache: 'reload', credentials: 'omit'})));
    await self.skipWaiting();
  })());
});

self.addEventListener('activate', event => {
  event.waitUntil((async () => {
    const legacyNames = scope.pathname === '/-summit-one-narrator/'
      ? ['summit-one-guided-20261121', 'summit-one-reasoning-20261121'] : [];
    const keys = await caches.keys();
    await Promise.all(keys.filter(key => key !== cacheName && (
      key.startsWith(cachePrefix) || legacyNames.includes(key)
    )).map(key => caches.delete(key)));
    await self.clients.claim();
  })());
});

self.addEventListener('message', event => {
  if (event.data?.type === 'summit-reader-status') {
    event.waitUntil((async () => {
      const ready = Boolean(await caches.match(reader, {cacheName}));
      event.source?.postMessage({type: 'summit-reader-status-result', ready});
    })());
  }
});

self.addEventListener('fetch', event => {
  const request = event.request;
  const url = new URL(request.url);
  if (request.method !== 'GET' || url.origin !== scope.origin ||
      !url.pathname.startsWith(scope.pathname) || request.headers.has('authorization')) return;
  if (request.mode === 'navigate') {
    event.respondWith((async () => {
      try { return await fetch(request, {cache: 'no-store'}); } catch {
        if (url.pathname !== new URL(reader).pathname) return Response.redirect(reader, 302);
        const cache = await caches.open(cacheName);
        return await cache.match(reader) || Response.error();
      }
    })());
    return;
  }
  // Only the explicit public assets enter this cache. Movies and protected requests use the network.
  if (!allowed.has(url.href)) return;
  event.respondWith((async () => {
    const cache = await caches.open(cacheName);
    // Unversioned releases and catalogue data should reflect a successful online update.
    if (!url.search) {
      try { const fresh = await fetch(request); if (fresh.ok) return fresh; } catch {}
    }
    return await cache.match(request) || fetch(request);
  })());
});
