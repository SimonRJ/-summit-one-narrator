import assert from 'node:assert/strict';
import {exactValue, numericResponse as response} from '../supabase/functions/submit-problem-attempt/answer-value.js';

for (const form of ['3/2', '6⁄4', '1.50', '1 1/2', '1½']) assert.equal(response('3/2',form).correct,true);
for (const form of ['−1½','-1 1/2','-1.5']) assert.equal(response('-3/2',form).correct,true);
for (const form of ['1,234', '1 234', '1234.0']) assert.equal(response(1234,form).correct,true);
for (const form of ['2/0','1 or 2','12,34','0.5x','−½½','1/2/3','1 3/2']) assert.equal(exactValue(form),null);
assert.equal(response('1/3','0.3333333333333').correct,false);
assert.equal(response(1,'1.0000000000000001').correct,false);
assert.equal(response(12,'12 or 13').correct,null);
assert.equal(response(25,'25%','By what percentage did it grow?').correct,true);
assert.equal(response(25,'25%','A price changes. What sale percentage did the shop use?').correct,true);
assert.equal(response('1/4','25%','What is the probability of blue?').correct,true);
assert.equal(response(1,'100%','How many cubes are there?').correct,null);
assert.equal(response('2/5','4/10','Enter a fraction in simplest form.').correct,null);
assert.equal(response('2/5','2/5','Enter a fraction in simplest form.').correct,true);
assert.equal(response('yes','yes'),null);
console.log('Exact equivalence, mixed numbers, fraction glyphs, percentages, question-specific forms and recoverable input checked.');

import vm from 'node:vm';
import fs from 'node:fs';
import {stripTypeScriptTypes} from 'node:module';
const functionSource = fs.readFileSync(new URL('../supabase/functions/submit-problem-attempt/index.ts', import.meta.url), 'utf8')
  .replace(/^import .*;\n/gm,'').replace(/export /g,'');
let handler;
const writes = [];
const lessonRow={id:'RWL2-999-A',answer:'3/2',prompt:'Give the exact amount.',source_type:'original_lesson_practice'};
function client() {
  return {
    auth:{getUser:async()=>({data:{user:{id:'fixture'}}})},
    from(name) {
      const builder = {
        select:()=>builder,eq:()=>builder,limit:async()=>({data:[]}),
        maybeSingle:async()=>({data:{id:'fixture'}}),single:async()=>({data:lessonRow}),
        insert:async row=>{assert.equal(name,'problem_attempts');writes.push(row);return {error:null};},
      };
      return builder;
    },
  };
}
const context = {Deno:{env:{get:()=>''},serve:fn=>{handler=fn;}},createClient:client,numericResponse:response,Response,console};
vm.runInNewContext(stripTypeScriptTypes(functionSource),context);
async function submit(value) {
  return handler(new Request('https://example.test/check',{
    method:'POST',headers:{authorization:'Bearer fixture','content-type':'application/json'},
    body:JSON.stringify({problem_id:lessonRow.id,session_number:5,answer_text:value})
  }));
}
const bad = await submit('1/0');
assert.equal(bad.status,422);
assert.equal((await bad.json()).code,'answer_format');
assert.equal(writes.length,0);
const good=await submit('1½');
assert.equal(good.status,200);
assert.equal((await good.json()).correct,true);
assert.equal(writes.length,1);
assert.equal(writes[0].independent_credit,true);
console.log('An unreadable entry leaves the saved first attempt available. A valid answer records it once.');
