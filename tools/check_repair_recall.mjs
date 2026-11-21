import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import {methods,exercise,checkAnswer} from '../curriculum.js';
import {practice} from '../transfer-practice.js';

// Use the production selector without importing browser-only authentication into Node.
const source=fs.readFileSync(new URL('../learning-support.js',import.meta.url),'utf8')
 .replace(/^import .*;$/gm,'').replace(/export /g,'');
const context={methods,exercise,checkAnswer,practice};
vm.runInNewContext(source,context);
const choose=context.chooseRepairQuestion;
for(const skill_id of Object.keys(methods)){
 for(let i=0;i<52;i++){
  const row={id:'repair-'+i,skill_id,stage:1};
  const history=[];
  const first=choose(row,history);
  history.push({question_id:first.prompt,correct:true,used_help:true,response:String(first.value)});
  row.stage=2;
  const second=choose(row,history);
  assert.notEqual(second.prompt,first.prompt);
  history.push({prompt:second.prompt,correct:true,used_help:false,response:String(second.value)});
  row.stage=3;
  const delayed=choose(row,history);
  assert.notEqual(delayed.prompt,first.prompt);
  assert.notEqual(delayed.prompt,second.prompt);
  const pending={stage:3,source:delayed.source,seed:delayed.seed};
  assert.equal(choose(row,history,pending).prompt,delayed.prompt);
 }
}
const row={id:'digits',skill_id:'DIG-05',stage:2};
const history=[{prompt:practice('DIG-05',2).prompt,correct:true,used_help:true,response:'8'}];
// The original practice generator has different numbers but the answer is always eight.
assert.notEqual(choose(row,history).value,8);
row.skill_id='GEO-03';
const pool=[...Array.from({length:52},(_,i)=>practice(row.skill_id,i)),...Array.from({length:7},(_,i)=>exercise(row.skill_id,i))];
const unique=[...new Map(pool.map(q=>[q.prompt,q])).values()];
const exhausted=unique.map(q=>({prompt:q.prompt,response:String(q.value),correct:true,used_help:false}));
exhausted[1].used_help=true;
assert.equal(choose(row,exhausted).prompt,exhausted[1].prompt);
assert.equal(choose(row,[{correct:true}]).prompt.length>0,true);
console.log('Passed changed and delayed examples for all 52 techniques, saved variant recovery and reuse after exhausting a finite bank.');
