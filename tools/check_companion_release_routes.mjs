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
const resolverFor = catalogue => {
  const context = vm.createContext({teaching: catalogue});
  vm.runInContext(app.slice(start, end), context);
  return id => vm.runInContext(`finalVideoUrl(${JSON.stringify(id)})`, context);
};
const movieFor = resolverFor(teaching);

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

// The queued native-chapter and notebook installers publish new catalogue tokens.
// Exercise a complete edition rollover, including the seven legacy blank rows.
const nextEdition = teaching.map(film => ({...film,
  video_url: `media/${film.id}.mp4?v=chapters-a1b2c3d4e5f6`}));
const nextMovieFor = resolverFor(nextEdition);
for (const film of nextEdition) {
  assert.equal(nextMovieFor(film.id), film.video_url,
    `${film.id}: a newly published catalogue edition was ignored`);
}

const rejected = [
  'https://example.com/media/T16.3.mp4?v=next',
  'https://simonrj.github.io/-summit-one-narrator/media/T16.3.mp4?v=next',
  '//example.com/media/T16.3.mp4?v=next',
  '/media/T16.3.mp4?v=next',
  'media/T05.1.mp4?v=next',
  'media/../media/T16.3.mp4?v=next',
  'media/%54%31%36%2e%33.mp4?v=next',
  'media/T16.3.mp4?v=%2e%2e%2fother',
  'media/T16.3.mp4?v=next&url=https://example.com',
  'media/T16.3.mp4?v=next#fragment',
  'media/T16.3.mp4?v=',
  'media/T16.3.mp4?v=next ',
  {url: 'media/T16.3.mp4?v=next'},
  1,
];
for (const video_url of rejected) {
  const catalogue = teaching.map(film => film.id === 'T16.3' ? {...film, video_url} : film);
  assert.equal(resolverFor(catalogue)('T16.3'), '',
    `Unsafe or mismatched catalogue URL accepted: ${JSON.stringify(video_url)}`);
}

for (const id of ['A001', 'K001', 'N1.26', 'S001', 'T00.1', 'T19.1', 'T99.1', 'T16.4', '', null]) {
  assert.equal(movieFor(id), '', `${id}: unpublished or protected film exposed by public resolver`);
  const catalogue = [...teaching, {id, video_url: `media/${id}.mp4?v=next`}];
  assert.equal(resolverFor(catalogue)(id), '', `${id}: an extra catalogue row bypassed the public ID boundary`);
}
console.log('PASS: all 72 companion routes agree, all 72 accept a safe catalogue edition rollover, and unsafe URLs plus unpublished/protected IDs are rejected.');
