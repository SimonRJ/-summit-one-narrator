const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const fs = require('node:fs/promises');
const { devices, webkit } = require('playwright');

const site = 'https://simonrj.github.io/-summit-one-narrator/';
const watchPage = site + 'watch-lesson-intro.html?slot=67';
const scriptUrl = new URL('lesson-introduction-watch.js', site);
const movie = 'https://github.com/SimonRJ/-summit-one-narrator/releases/download/lesson-introductions/S067-Intro-Illustrated.mp4';
const expectedDigest = '061c4f6aa16e9230936deb9ca832fce167367158e771729d251217c3b19033cf';
const candidate = 'tools/player-candidates/lesson-introduction-watch.js';
const evidenceDir = 'build/s067-player-candidate';

async function verifyPublicMedia() {
  const catalog = new URL('https://raw.githubusercontent.com/SimonRJ/-summit-one-narrator/refs/heads/lesson-intro-catalog/data/lesson-intros-live.json');
  catalog.searchParams.set('check', Date.now());
  const manifest = await fetch(catalog, { signal: AbortSignal.timeout(30000) });
  assert.ok(manifest.ok, 'Public catalogue HTTP ' + manifest.status);
  const entry = (await manifest.json()).entries.find(entry => entry.id === 'S067');
  assert.equal(entry?.sha256, expectedDigest);
  assert.equal(entry.status, 'verified');
  const response = await fetch(movie, { signal: AbortSignal.timeout(180000) });
  assert.ok(response.ok, 'Public media HTTP ' + response.status);
  const hash = crypto.createHash('sha256');
  let bytes = 0;
  for await (const chunk of response.body) {
    hash.update(chunk);
    bytes += chunk.length;
  }
  const sha256 = hash.digest('hex');
  assert.equal(sha256, expectedDigest);
  return { movie, bytes, sha256 };
}

async function checkProgress(page, target) {
  // Mere assignment to currentTime can report the target even while a new request is pending.
  // Observe a decoded frame past the target, then independently watch playback advance there.
  const settled = await page.waitForFunction(target => {
    const video = document.querySelector('#introFilm');
    return !video.paused && !video.seeking && video.readyState >= 2 &&
      video.currentTime >= target + 0.3 && video.currentTime < target + 8 && video.currentTime;
  }, target, { timeout: 30000 });
  const start = await settled.jsonValue();
  const advanced = await page.waitForFunction(({ start, target }) => {
    const video = document.querySelector('#introFilm');
    return !video.paused && !video.seeking && video.readyState >= 2 &&
      video.currentTime >= start + 1.2 && video.currentTime < target + 12 && video.currentTime;
  }, { start, target }, { timeout: 16000 });
  return { target, start, advanced: await advanced.jsonValue() };
}

async function checkCase(browser, spec, script) {
  const { name, orientation, warm } = spec;
  const viewport = orientation === 'landscape' ? { width: 844, height: 390 } : { width: 390, height: 844 };
  const context = await browser.newContext({
    ...devices['iPhone 13'], defaultBrowserType: undefined, viewport, screen: viewport,
    deviceScaleFactor: 2, serviceWorkers: 'block'
  });
  const page = await context.newPage();
  const result = { name, orientation, warm, substituted: [], checks: [] };
  try {
    await page.route(url => url.origin === scriptUrl.origin && url.pathname === scriptUrl.pathname, async route => {
      assert.equal(route.request().resourceType(), 'script');
      result.substituted.push(route.request().url());
      await route.fulfill({ contentType: 'application/javascript', body: script });
    });
    await page.addInitScript(() => {
      window.playerEvents = [];
      for (const event of ['click', 'loadedmetadata', 'play', 'playing', 'pause', 'seeking', 'seeked', 'error', 'waiting', 'timeupdate']) {
        document.addEventListener(event, e => {
          const v = document.getElementById('introFilm');
          if (v && (e.target === v || e.target.closest?.('[data-time]'))) {
            window.playerEvents.push([event, performance.now(), v.currentTime, v.readyState, v.seeking, v.paused]);
            if (window.playerEvents.length > 150) window.playerEvents.shift();
          }
        }, true);
      }
    });
    await page.goto(watchPage, { waitUntil: 'domcontentloaded', timeout: 60000 });
    const film = page.locator('#introFilm');
    const chapters = page.locator('#introChapters button[data-time]');
    const challenge = chapters.filter({ hasText: /challenge/i });
    await challenge.waitFor({ timeout: 30000 });
    const target = Number(await challenge.getAttribute('data-time'));
    assert.ok(Math.abs(target - 88.07) < 0.1, 'Incorrect hard problem chapter at ' + target);
    if (warm) {
      await film.evaluate(v => { v.muted = true; return v.play(); });
      await page.waitForFunction(() => document.querySelector('#introFilm').currentTime > .15, null, { timeout: 30000 });
    }
    // On cold runs this is the first tap, without any wait for video readiness.
    await challenge.tap();
    result.checks.push(await checkProgress(page, target));
    const medium = chapters.filter({ hasText: /medium/i });
    const recap = chapters.last();
    const recapTime = Number(await recap.getAttribute('data-time'));
    assert.ok(recapTime > target);
    // The learner changes their mind before the previous chapter has had time to play.
    await medium.tap();
    await challenge.tap();
    await recap.tap();
    result.checks.push(await checkProgress(page, recapTime));
    await challenge.tap();
    result.checks.push(await checkProgress(page, target));
    result.video = await film.evaluate(v => ({
      source: v.currentSrc, width: v.videoWidth, height: v.videoHeight,
      duration: v.duration, error: v.error?.message || '', landscape: innerWidth > innerHeight
    }));
    assert.equal(result.video.source, movie);
    assert.equal(result.video.error, '');
    assert.equal(result.video.landscape, orientation === 'landscape');
    assert.deepEqual([result.video.width, result.video.height], [1920, 1080]);
    assert.equal(result.substituted.length, 1, 'The page must load exactly one candidate chapter script');
    console.log(name, result.checks);
  } catch (error) {
    result.failure = String(error);
    console.error(name, String(error));
    throw error;
  } finally {
    result.events = await page.evaluate(() => window.playerEvents).catch(() => []);
    await fs.writeFile(evidenceDir + '/' + name + '.json', JSON.stringify(result, null, 2));
    await context.close();
  }
}

async function main() {
  await fs.mkdir(evidenceDir, { recursive: true });
  const script = await fs.readFile(candidate);
  const media = await verifyPublicMedia();
  await fs.writeFile(evidenceDir + '/edition.json', JSON.stringify({
    ...media, watchPage, candidateSha256: crypto.createHash('sha256').update(script).digest('hex')
  }, null, 2));
  const browser = await webkit.launch();
  try {
    let failures = 0;
    for (const test of [
      { name: 'landscape-cold-1', orientation: 'landscape', warm: false },
      { name: 'landscape-playing', orientation: 'landscape', warm: true },
      { name: 'landscape-cold-2', orientation: 'landscape', warm: false },
      { name: 'portrait-cold', orientation: 'portrait', warm: false },
      { name: 'portrait-playing', orientation: 'portrait', warm: true }
    ]) {
      try { await checkCase(browser, test, script); }
      catch { failures++; }
    }
    assert.equal(failures, 0, 'Every cold and playing chapter test must pass.');
  } finally {
    await browser.close();
  }
}

main().catch(error => { console.error(error); process.exitCode = 1; });
