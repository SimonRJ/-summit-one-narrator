import assert from 'node:assert/strict';
import {analyseRoute,countRouteFinishes} from '../route-model.js';

// Independently choose two up-step positions among five, then classify the resulting ten whole walks.
const walks=[];
for(let first=0;first<5;first++) for(let second=first+1;second<5;second++) {
  const word=Array.from({length:5},(_,i)=>i===first||i===second?'U':'R').join('');
  const points=['A1'];
  let col=0,row=1;
  for(const step of word) {
    if(step==='R') col++;
    else row++;
    points.push('ABCD'[col]+row);
  }
  walks.push({word,points});
}
const eligible={
  open: () => true,
  checkpoint: walk=>walk.points.includes('B2'),
  point: walk=>!walk.points.includes('B2'),
  edge: walk=>!walk.points.some((v,i)=>v==='B2'&&walk.points[i-1]==='A2'),
  history: walk=>!walk.word.includes('UU')
};
const expectedTotals=[10,6,4,7,6], rules=Object.keys(eligible);
let checked=0;
for(const [index,rule] of rules.entries()) {
  const legal=walks.filter(eligible[rule]);
  assert.equal(legal.length,expectedTotals[index]);
  assert.equal(countRouteFinishes(rule),expectedTotals[index]);
  for(const walk of walks) assert.equal(Boolean(analyseRoute(rule,walk.word).accepted),legal.includes(walk));
  // Includes impossible prefixes, paths already completed, and right/up prefixes which can still be repaired.
  for(let len=0;len<=5;len++) for(let bits=0;bits<2**len;bits++) {
    const prefix=Array.from({length:len},(_,i)=>bits&(1<<i)?'U':'R').join('');
    assert.equal(countRouteFinishes(rule,prefix),legal.filter(w=>w.word.startsWith(prefix)).length,rule+' '+prefix);
    checked++;
  }
}
assert.equal(analyseRoute('checkpoint','RRRUU').accepted,false);
assert.equal(analyseRoute('checkpoint','RURRU').accepted,true);
assert.match(analyseRoute('point','RU').error,/junction/);
assert.equal(analyseRoute('edge','RU').state.viaB2,true);
assert.match(analyseRoute('edge','UR').error,/street/);
assert.match(analyseRoute('history','RUU').error,/Two up/);
assert.equal(analyseRoute('history','URU').state.y,2);
assert.equal(countRouteFinishes('history','RU'),2);
assert.equal(countRouteFinishes('history','UR'),3);
console.log('Passed 50 whole-route classifications and '+checked+' prefix-completion counts on five route rules.');
