const assert = require('node:assert/strict');
const {createHash} = require('node:crypto');
const {readFile, writeFile} = require('node:fs/promises');
const {execFileSync} = require('node:child_process');
const {setTimeout: delay} = require('node:timers/promises');

const site = 'https://simonrj.github.io/-summit-one-narrator/';
async function read(url) {
  const response = await fetch(url, {signal: AbortSignal.timeout(60000)});
  assert.ok(response.ok, response.status + ' ' + url);
  return response;
}

async function verify(film) {
  const {id, revision, sha256} = film;
  const url = new URL('media/' + id + '.mp4?v=' + revision, site).href;
  const route = 'watch-' + id.toLowerCase().replace('.', '-') + '.html';
  const page = await (await read(site + route)).text();
  assert.ok(page.includes('src="media/' + id + '.mp4?v=' + revision + '"'), route);
  const qa = await (await read(site + 'review/' + id + '-studio-qa.json?v=' + revision)).json();
  assert.equal(qa.sha256, sha256);
  const movie = Buffer.from(await (await read(url)).arrayBuffer());
  assert.equal(createHash('sha256').update(movie).digest('hex'), sha256);
  return {id, source: url, sha256, bytes: movie.length};
}

(async () => {
  const films = JSON.parse(await readFile('production/reviewed-teaching-editions.json', 'utf8'));
  let receipts;
  for (let attempt = 1; attempt <= 35; attempt++) {
    try {
      receipts = await Promise.all(films.map(verify));
      break;
    } catch (error) {
      if (attempt === 35) throw error;
      console.log('Waiting for the selected Pages editions.', error.message);
      await delay(10000);
    }
  }
  execFileSync(process.execPath, ['tools/review-public-video-players.cjs', ...films.map(f => f.id)], {stdio: 'inherit'});
  for (const receipt of receipts) {
    const prefix = 'build/phone/' + receipt.id + '-' + process.env.ENGINE;
    for (const orientation of ['portrait', 'landscape']) {
      const report = JSON.parse(await readFile(prefix + '-' + orientation + '.json', 'utf8'));
      assert.equal(report.courseSource, receipt.source);
      assert.equal(report.source, receipt.source);
      assert.equal(report.method, 'chapter button');
      assert.ok(report.time > report.target);
    }
    await writeFile(prefix + '-public-digest.json', JSON.stringify(receipt, null, 2) + '\n');
  }
})().catch(error => {console.error(error); process.exitCode = 1;});
