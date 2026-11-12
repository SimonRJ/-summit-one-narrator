import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import {profiles,wordingCards} from '../recognition.js';
import {flashDeck,mixedFlashDeck} from '../flash-cards.js';
import {skillFor} from '../curriculum.js';
const read=p=>JSON.parse(fs.readFileSync(p));
const sessions=read('data/sessions-372.json').sessions,taxonomy=read('data/taxonomy-52.json');
assert.deepEqual(profiles,read('data/recognition-profiles.json'));
assert.equal(Object.keys(profiles).length,52);assert.equal(wordingCards.length,10);
let prior=[],count=0;
for(const s of sessions){
 let deck;
 if(s.type==='LESSON'){const id=skillFor(s,taxonomy);prior.push(id);deck=flashDeck(id,1,s.slot);}
 else if(s.type==='MAWA')deck=flashDeck('M'+String((Math.floor(s.slot/7)-1)%20+1).padStart(2,'0'),1,s.slot,true);
 else deck=mixedFlashDeck([...new Set(prior)].slice(-4),s.slot);
 assert.equal(deck.length,5);assert(deck.every(c=>c.q&&c.options.length===2&&c.options[0]!==c.options[1]&&c.why));
 assert([2,3].includes(deck.filter(c=>c.answer===0).length));count++;
}
const d=read('data/amc-coverage.json');assert.equal(d.questions,570);assert.equal(d.papers,19);
assert.equal(d.topics.reduce((n,x)=>n+x.questions,0),570);
for(const [b,n] of Object.entries({'Q1–10':190,'Q11–20':190,'Q21–25':95,'Q26–30':95}))assert.equal(d.topics.reduce((sum,t)=>sum+(t.bands[b]||0),0),n);
assert.equal(d.skills.reduce((n,x)=>n+x.questions,0),570);
const src=fs.readFileSync('exam-diagnostics.js','utf8').replace(/^import .*;\n/gm,'').replace(/export /g,'');
const context={profiles};vm.createContext(context);vm.runInContext(src,context);
const groups=context.diagnosticGroups([{category:'ALG-01',correct:true,earned:3,marks:3},{category:'ALG-01',correct:false,earned:0,marks:7},{category:'GEO-02',correct:false,earned:0,marks:4}]);
assert.equal(groups[0].total,2);assert.equal(groups[0].correct,1);assert.equal(groups[0].marks,10);assert.equal(groups[0].earned,3);
assert.equal(groups.reduce((n,g)=>n+g.marks,0),14);
console.log(`PASS: ${count} five-card session decks, 52 recognition profiles, full 570-question aggregates and lost-mark diagnostic grouping.`);
