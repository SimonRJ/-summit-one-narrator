const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const fs = require('node:fs/promises');
const {spawnSync} = require('node:child_process');

// A branch commit and its public CDN response can become visible at different times.
async function awaitCatalogueEdition(target) {
  const url = 'https://raw.githubusercontent.com/SimonRJ/-summit-one-narrator/refs/heads/lesson-intro-catalog/data/lesson-intros-live.json';
  const deadline = Date.now() + 6 * 60_000;
  while (Date.now() < deadline) {
    const response = await fetch(url + '?v=' + Math.floor(Date.now() / 20000), {signal: AbortSignal.timeout(15_000)});
    if (response.ok) {
      const entry = (await response.json()).entries.find(row => row.id === target.id);
      if (entry?.status === 'verified' && entry.sha256 === target.sha256) return;
    }
    await new Promise(resolve => setTimeout(resolve, 15_000));
  }
  throw new Error(`The public catalogue has not yet served the reviewed ${target.id} edition`);
}

async function awaitCourseAssignment(target) {
  if (!target.assignedSlots?.length) return;
  const site = 'https://simonrj.github.io/-summit-one-narrator/';
  const asset = 'https://github.com/SimonRJ/-summit-one-narrator/releases/download/lesson-introductions/' + target.asset;
  const deadline = Date.now() + 6 * 60_000;
  while (Date.now() < deadline) {
    const home = await fetch(site, {signal: AbortSignal.timeout(15000)});
    const script = (await home.text()).match(/src="(app-main\.js\?v=[^"]+)"/)?.[1];
    if (home.ok && script) {
      const module = await fetch(new URL(script, site), {signal: AbortSignal.timeout(15000)});
      const data = (await module.text()).match(/fetch\("(data\/read-watch-practise-later\.json\?v=[^"]+)"/)?.[1];
      if (module.ok && data) {
        const response = await fetch(new URL(data, site), {signal: AbortSignal.timeout(15000)});
        if (response.ok) {
          const lessons = (await response.json()).lessons.filter(l => l.videoId === target.id);
          if (target.assignedSlots.every(slot => lessons.some(l => l.slot === slot))
              && lessons.every(l => l.movie === asset)) return;
        }
      }
    }
    await new Promise(resolve => setTimeout(resolve, 15000));
  }
  throw new Error('The deployed Read-Watch-Practise lessons still select an earlier film.');
}

async function check() {
  const target = JSON.parse(await fs.readFile('production/lesson-intros/phone-review-target.json', 'utf8'));
  assert.match(target.id, /^S\d{3}$/);
  assert.match(target.sha256, /^[0-9a-f]{64}$/);
  assert.ok(target.asset.startsWith(target.id + '-Intro') && /^[\w.-]+\.mp4$/.test(target.asset));
  assert.ok(['chrome', 'webkit'].includes(process.env.ENGINE));
  if (target.chapterPlayerSha256) {
    assert.match(target.chapterPlayerSha256, /^[a-f0-9]{64}$/);
    process.env.CHAPTER_PLAYER_SHA256 = target.chapterPlayerSha256;
  }
  await Promise.all([awaitCatalogueEdition(target), awaitCourseAssignment(target)]);
  const runner = spawnSync(process.execPath, ['tools/review-public-video-players.cjs',target.id], {stdio:'inherit'});
  if (runner.error) throw runner.error;
  assert.equal(runner.status, 0, 'The public phone player failed its playback or chapter seek.');
  let publicSource;
  for (const orientation of ['portrait','landscape']) {
    const file = `build/phone/${target.id}-${process.env.ENGINE}-${orientation}.json`;
    const evidence = JSON.parse(await fs.readFile(file,'utf8'));
    assert.equal(evidence.id, target.id);
    assert.equal(evidence.engine, process.env.ENGINE);
    assert.equal(evidence.orientation, orientation);
    assert.equal(evidence.courseSource, evidence.source);
    assert.equal(new URL(evidence.source).pathname.split('/').pop(), target.asset);
    if (publicSource) assert.equal(evidence.source, publicSource);
    publicSource = evidence.source;
  }
  const catalogue = new URL('https://raw.githubusercontent.com/SimonRJ/-summit-one-narrator/refs/heads/lesson-intro-catalog/data/lesson-intros-live.json');
  catalogue.searchParams.set('verified_sha',target.sha256);
  const manifest = await fetch(catalogue, {signal:AbortSignal.timeout(30000)});
  assert.ok(manifest.ok, `Live catalogue returned ${manifest.status}`);
  const row = (await manifest.json()).entries.find(row => row.id === target.id);
  assert.equal(row?.status, 'verified');
  assert.equal(row.sha256, target.sha256);
  const response = await fetch(publicSource, {signal:AbortSignal.timeout(180000)});
  assert.ok(response.ok, `Live media returned ${response.status}`);
  const hash = crypto.createHash('sha256');
  let bytes = 0;
  for await (const chunk of response.body) {hash.update(chunk); bytes += chunk.length;}
  assert.equal(hash.digest('hex'), target.sha256, 'The player resolved to different media bytes from the reviewed film.');
  await fs.writeFile(`build/phone/${target.id}-${process.env.ENGINE}-public-digest.json`,JSON.stringify({id:target.id,asset:target.asset,source:publicSource,sha256:target.sha256,bytes},null,2));
}
check().catch(error => {console.error(error);process.exitCode=1});
