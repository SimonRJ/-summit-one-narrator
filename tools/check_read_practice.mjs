import assert from 'node:assert/strict';
import fs from 'node:fs';
import {edition,questionOrder,readCard,phaseFor} from '../reviewed-lesson.js';
const read = p=>JSON.parse(fs.readFileSync(new URL('../data/'+p,import.meta.url),'utf8'));
const course=read('sessions-372.json').sessions;
const bank=read('lesson-challenges.json').items;
const release=read('read-watch-practise.json');
const recorded=read('recorded-studies.json');
function checkFilm(lesson) {
 const id = lesson.videoId;
 const guide = recorded.lessons[id];
 assert(/^https:\/\//.test(lesson.movie));
 if (!guide) {
  assert(lesson.videoTitle && lesson.movie.includes(id+'-Intro'));
  return;
 }
 assert.equal(lesson.movie,(guide.release || recorded.release)+id+'.mp4');
 assert.equal(lesson.videoTitle,guide.title);
 if (Number(id.slice(1)) === lesson.slot) {
  assert.equal(lesson.filmUse,'dedicated');
  assert.equal(lesson.bridge,guide.bridge);
 }
 assert.equal(guide.chapters.length,guide.transcript.length);
 assert(guide.chapters.length >= 7);
 assert.equal(guide.chapters[0].start,0);
 assert(guide.chapters.every((ch,i) => ch.start < guide.seconds && (!i || ch.start > guide.chapters[i-1].start)));
}
assert.equal(release.edition,edition);
assert.deepEqual(release.lessons.map(l=>l.slot),course.filter(s=>s.slot<=68&&s.type==='LESSON').map(s=>s.slot));
let count=0,retained=0;const ids=new Set(),stems=new Set();
for(const l of release.lessons){
 const slot=String(l.slot).padStart(3,'0'), video='S'+slot;
 assert.equal(l.videoId,video);checkFilm(l);
 assert(l.example.steps.length>=2 && l.example.steps.every(x=>x.trim()));assert(l.intro&&l.bridge&&l.recap&&l.headline);
 const order=questionOrder(l,bank,bank);
 assert.equal(order.length,l.retained.length+4);assert.equal(order.at(-1).id,'RWL1-'+slot+'-D');
 assert.deepEqual(l.questions.map(q=>q.id),'ABCD'.split('').map(a=>'RWL1-'+slot+'-'+a));
 for(const q of l.questions){
  assert.deepEqual(Object.keys(q).sort(),['hint','id','prompt','title']);assert(q.hint&&q.title&&q.prompt);
  const s=q.prompt.toLowerCase().replace(/\W/g,'');assert(!stems.has(s));stems.add(s);assert(!ids.has(q.id));ids.add(q.id);count++;
 }
 if(l.example.figure){ const fig=l.example.figure;assert(fig.alt&&/^figures\/read-practice\/S\d{3}\.svg$/.test(fig.src));assert(fs.existsSync(new URL('../'+fig.src,import.meta.url)));assert(readCard(l).includes('alt='));}
 assert(readCard(l).includes('A small example'));retained+=l.retained.length;
}
assert.equal(count,220);assert.equal(phaseFor(0),'Read');assert.equal(phaseFor(1),'Watch');assert.equal(phaseFor(2),'Practise');
console.log('PASS: '+release.lessons.length+' lessons, '+count+' new problems, '+retained+' retained; read/watch/practise order and answer protection.');

const later = read('read-watch-practise-later.json');
const startingQuestions = new Set();
for (const lesson of [...release.lessons, ...later.lessons]) {
 const cue = lesson.example.prediction;
 assert(cue?.endsWith('?'), 'Missing starting question in lesson ' + lesson.slot);
 assert(!startingQuestions.has(cue), 'Repeated starting question in lesson ' + lesson.slot);
 startingQuestions.add(cue);
}
assert.equal(startingQuestions.size, 283);
const openingEdits=JSON.parse(fs.readFileSync(new URL('../tools/content/practice-revisions-20261121.json',import.meta.url))).openings;
for(const [id,edit] of Object.entries(openingEdits)){
 const lesson=[...release.lessons,...later.lessons].find(item=>item.slot===Number(id.slice(1)));
 assert(lesson,id);
 for(const [field,value] of Object.entries(edit.example || {})) {
  assert.deepEqual(lesson.example[field],value,id+' example '+field);
 }
 for (const field of ['headline','intro','bridge','recap']) {
  if (field in edit) assert.equal(lesson[field],edit[field],id+' '+field);
 }
}
const laterSlots = course.filter(s => s.type === 'LESSON' && s.slot > 68).map(s => s.slot);
const skills = new Map(bank.map(q => [q.session,q.skill]));
assert.equal(later.edition,'read-watch-practise-2');
assert.deepEqual(later.lessons.map(l => l.slot),laterSlots);
const filmUse = {dedicated:0,technique:0};
let laterQuestions = 0;
for(const lesson of later.lessons){
 const tag = String(lesson.slot).padStart(3,'0');
 const sourceSlot = Number(lesson.videoId.slice(1));
 assert.equal(lesson.skill,skills.get(lesson.slot));
 assert.equal(lesson.skill,skills.get(sourceSlot));
 checkFilm(lesson);
 assert.equal(lesson.filmUse,sourceSlot===lesson.slot?'dedicated':'technique');
 assert(sourceSlot <= lesson.slot);
 filmUse[lesson.filmUse]++;
 assert(lesson.headline && lesson.intro && lesson.bridge && lesson.recap && lesson.example.steps.length>=2);
 const order = questionOrder(lesson,bank,bank);
 assert.equal(order.length,4+lesson.retained.length);
 assert.deepEqual(lesson.questions.map(q => q.id),Array.from('ABCD',k => 'RWL2-'+tag+'-'+k));
 assert.equal(order.at(-1).id,'RWL2-'+tag+'-D');
 for(const question of lesson.questions){
  const allowed=['family','hint','id','prompt','title'];
  if(question.figure){
   allowed.push('figure');
   assert(question.figure.alt && /^figures\/read-practice\/S\d{3}-[ABCD]\.svg$/.test(question.figure.src));
   assert(fs.existsSync(new URL('../'+question.figure.src,import.meta.url)));
  }
  assert.deepEqual(Object.keys(question).sort(),allowed.sort());
  assert(question.hint && question.family.startsWith(lesson.skill+':'));
  const stem = question.prompt.toLowerCase().replace(/\W/g,'');
  assert(!stems.has(stem),'Duplicate practice prompt: '+question.id);
  stems.add(stem);
  laterQuestions++;
 }
 const figure=lesson.example.figure;
 if(figure){
  assert(figure.alt && /^figures\/read-practice\/S\d{3}\.svg$/.test(figure.src));
  assert(fs.existsSync(new URL('../'+figure.src,import.meta.url)));
 }
}
assert.equal(laterQuestions,912);
// The 58 original own-introduction rows are listed in docs/LATER_LESSONS.md
// at 04d2032d585c020a0e44ab4b1d468680198a77f7. A recorded replacement for
// one of those films (for example S102) does not add a dedicated assignment.
const originalDedicatedSlots = new Set([
 69,71,72,73,74,75,76,78,79,81,82,83,85,86,87,88,89,90,92,93,
 94,95,97,99,100,101,102,103,104,106,107,108,109,110,113,114,
 115,116,117,118,120,121,122,123,124,125,127,129,130,131,132,
 134,135,139,142,143,145,146,
]);
assert.equal(originalDedicatedSlots.size,58);
const expectedDedicatedSlots = new Set([
 ...originalDedicatedSlots,
 ...Object.keys(recorded.lessons).map(id=>Number(id.slice(1))).filter(slot=>slot>68),
]);
assert([...expectedDedicatedSlots].every(slot=>laterSlots.includes(slot)),
 'A dedicated film is assigned outside the later teaching lessons');
assert.deepEqual(
 later.lessons.filter(lesson=>lesson.filmUse==='dedicated').map(lesson=>lesson.slot).sort((a,b)=>a-b),
 [...expectedDedicatedSlots].sort((a,b)=>a-b),
 'Dedicated assignments must match the original films and recorded additions',
);
assert.deepEqual(filmUse,{
 dedicated:expectedDedicatedSlots.size,
 technique:laterSlots.length-expectedDedicatedSlots.size,
});
const allLessons = [...release.lessons,...later.lessons];
for (const id of Object.keys(recorded.lessons))
 assert(allLessons.some(lesson=>lesson.videoId===id && lesson.slot===Number(id.slice(1))));
console.log('PASS: all 228 later lessons, 912 protected questions and their skill-matched films.');

// Catch questions that only swap numbers or rename the same participants.
// Only title-case words observed inside a sentence can be treated as names;
// repeated names retain their identities within a particular puzzle.
const practice = [...release.lessons, ...later.lessons].flatMap(lesson => lesson.questions);
const possibleNames = new Set();
for (const {prompt} of practice) {
  for (const match of prompt.matchAll(/\b[A-Z][a-z]+\b/g)) {
    const prefix = prompt.slice(0, match.index).trimEnd();
    if (prefix && !/[.!?]$/.test(prefix)) possibleNames.add(match[0]);
  }
}
function promptPattern(prompt) {
  const names = new Map();
  const numbers = new Map();
  return prompt.replace(/\b(?:[A-Z][a-z]+|\d+)\b/g, token => {
    const numeric = /^\d+$/.test(token);
    if (!numeric && !possibleNames.has(token)) return token;
    const values = numeric ? numbers : names;
    if (!values.has(token)) values.set(token, values.size + 1);
    return (numeric ? '{number' : '{name') + values.get(token) + '}';
  }).toLowerCase().replace(/\s+/g, ' ').trim();
}
const byPattern = new Map();
for (const question of practice) {
  const pattern = promptPattern(question.prompt);
  assert(!byPattern.has(pattern),
    'Practice prompts differ only in labels or values: ' + byPattern.get(pattern) + ' and ' + question.id);
  byPattern.set(pattern, question.id);
}
console.log('PASS: ' + practice.length + ' practice prompts screened across both editions for renamed or renumbered copies.');
