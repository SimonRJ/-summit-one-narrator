const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const fs = require('node:fs/promises');
const {spawnSync} = require('node:child_process');

async function check() {
  const target = JSON.parse(await fs.readFile('production/lesson-intros/phone-review-target.json', 'utf8'));
  assert.match(target.id, /^S\d{3}$/);
  assert.match(target.sha256, /^[0-9a-f]{64}$/);
  assert.ok(target.asset.startsWith(target.id + '-Intro') && /^[\w.-]+\.mp4$/.test(target.asset));
  assert.ok(['chrome', 'webkit'].includes(process.env.ENGINE));
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
