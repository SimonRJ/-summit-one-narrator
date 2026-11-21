import assert from 'node:assert/strict';
import fs from 'node:fs';
import {edition,questionOrder,readCard,phaseFor} from '../reviewed-lesson.js';
const read = p=>JSON.parse(fs.readFileSync(new URL('../data/'+p,import.meta.url),'utf8'));
const course=read('sessions-372.json').sessions;
const bank=read('lesson-challenges.json').items;
const release=read('read-watch-practise.json');
assert.equal(release.edition,edition);
assert.deepEqual(release.lessons.map(l=>l.slot),course.filter(s=>s.slot<=68&&s.type==='LESSON').map(s=>s.slot));
let count=0,retained=0;const ids=new Set(),stems=new Set();
for(const l of release.lessons){
 const slot=String(l.slot).padStart(3,'0'), video='S'+slot;
 assert.equal(l.videoId,video);assert(l.movie.includes(video+'-Intro'));assert(/^https:\/\//.test(l.movie));
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
const openingEdits=JSON.parse(fs.readFileSync(new URL('../tools/content/practice-revisions-20261121.json',import.meta.url))).openings;
for(const [id,edit] of Object.entries(openingEdits)){
 const lesson=[...release.lessons,...later.lessons].find(item=>item.slot===Number(id.slice(1)));
 assert(lesson,id);
 assert.equal(lesson.example.prompt,edit.example.prompt,id);
 assert.deepEqual(lesson.example.steps,edit.example.steps,id);
 if(edit.intro)assert.equal(lesson.intro,edit.intro,id);
}
const laterSlots = course.filter(s => s.type === 'LESSON' && s.slot > 68).map(s => s.slot);
const skills = new Map(bank.map(q => [q.session,q.skill]));
assert.equal(later.edition,'read-watch-practise-2');
assert.deepEqual(later.lessons.map(l => l.slot),laterSlots);
const recorded = read('recorded-studies.json');
const filmUse = {dedicated:0,technique:0};
let laterQuestions = 0;
for(const lesson of later.lessons){
 const tag = String(lesson.slot).padStart(3,'0');
 const sourceSlot = Number(lesson.videoId.slice(1));
 assert.equal(lesson.skill,skills.get(lesson.slot));
 assert.equal(lesson.skill,skills.get(sourceSlot));
 const guide = recorded.lessons[lesson.videoId];
 if (guide) {
  assert.equal(lesson.movie, recorded.release + lesson.videoId + '.mp4');
  assert.equal(lesson.slot, sourceSlot);
  assert.equal(lesson.videoTitle,guide.title);
  assert.equal(lesson.bridge,guide.bridge);
  assert.equal(guide.chapters.length,guide.transcript.length);
  assert(guide.chapters.length >= 7);
  assert.equal(guide.chapters[0].start,0);
  assert(guide.chapters.every((ch,i) => ch.start < guide.seconds && (!i || ch.start > guide.chapters[i-1].start)));
 } else {
  assert(lesson.videoTitle && lesson.movie.includes(lesson.videoId+'-Intro'));
 }
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
const studyCount = Object.keys(recorded.lessons).length;
assert.deepEqual(filmUse,{dedicated:58+studyCount,technique:170-studyCount});
for (const id of Object.keys(recorded.lessons))
 assert(later.lessons.some(lesson=>lesson.videoId===id && lesson.filmUse==='dedicated'));
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
