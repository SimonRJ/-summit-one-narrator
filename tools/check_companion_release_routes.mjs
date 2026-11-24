// Keep the learner's companion player on the edition offered by its public page.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import {fileURLToPath} from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const read = name => fs.readFileSync(path.join(root, name), 'utf8');
const teaching = JSON.parse(read('data/teaching-72.json')).items;
const app = read('app-main.js');
const start = app.indexOf('const openingFilmIds=');
const end = app.indexOf('function markSolutionPlayback', start);
assert(start >= 0 && end > start, 'Companion URL resolver could not be located');
const context = vm.createContext({teaching});
vm.runInContext(app.slice(start, end), context);
const movieFor = id => vm.runInContext(`finalVideoUrl(${JSON.stringify(id)})`, context);

assert.equal(teaching.length, 72, 'Expected the complete public companion catalogue');
for (const film of teaching) {
  const page = read(`watch-${film.id.toLowerCase().replace('.', '-')}.html`);
  const sources = [...page.matchAll(/<source\b[^>]*\bsrc="([^"]+)"/g)];
  assert.equal(sources.length, 1, `${film.id}: expected one public movie source`);
  const publicMovie = sources[0][1];
  assert.equal(movieFor(film.id), publicMovie,
    `${film.id}: active/completed lesson player differs from the public watch page`);
  if (film.video_url) {
    assert.equal(film.video_url, publicMovie,
      `${film.id}: catalogue and public watch page offer different editions`);
  }
}

for (const id of ['A001', 'K001', 'N1.26', 'S001', 'T99.1', 'T16.4', '', null]) {
  assert.equal(movieFor(id), '', `${id}: unpublished or protected film exposed by public resolver`);
}
console.log('PASS: all 72 companion watch pages and learner-player URLs agree; unpublished and protected IDs remain excluded.');
