import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {stripTypeScriptTypes} from 'node:module';
import vm from 'node:vm';

const filename = new URL('../supabase/functions/get-problem-solution/index.ts', import.meta.url);
const source = readFileSync(filename, 'utf8').replace(/^import .*?;\n/, '');

async function request({signedIn = true, member = true, attempt = true, note = null, noteError = false} = {}) {
  const reads = [], writes = [];
  const original = 'Original checked reasoning.';
  const student = {id: 'test-learner'};
  const problem = {id:'test-problem', title:'Test problem', solution_text:original};
  const from = table => {
    const filters = [];
    const data = () => {
      reads.push(table);
      switch (table) {
        case 'profiles':
          assert(filters.some(([k,v]) => k === 'id' && v === student.id));
          return member ? student : null;
        case 'problem_attempts':
          assert(filters.some(([k,v]) => k === 'user_id' && v === student.id));
          assert(filters.some(([k,v]) => k === 'problem_id' && v === problem.id));
          assert(filters.some(([k,v]) => k === 'evidence_level' && v.join(',') === 'independent,guided'));
          assert(filters.some(([k,v]) => k === 'answer_text' && v === 'not null'));
          assert(filters.some(([k,v]) => k === 'answer_text' && v === 'nonempty'));
          return attempt ? {id:'test-attempt'} : null;
        case 'content_problems':
        case 'solution_clarifications':
          assert(filters.some(([k,v]) => v === problem.id && k === (table==='content_problems'?'id':'problem_id')));
          if (table === 'solution_clarifications') {
            assert(filters.some(([k,v]) => k === 'order' && v === 'latest revision'));
            assert(filters.some(([k,v]) => k === 'limit' && v === 1));
          }
          return table === 'content_problems' ? problem : note && !noteError ? {note} : null;
        default: throw Error('Unexpected table '+table);
      }
    };
    const chain = {
      select(){return chain;}, eq(k,v){filters.push([k,v]);return chain;},
      in(k,v){filters.push([k,v]);return chain;}, limit(n){filters.push(['limit',n]);return chain;},
      order(k,options){assert(k==='revision' && options.ascending===false);filters.push(['order','latest revision']);return chain;},
      not(k,op,v){assert(op==='is' && v===null);filters.push([k,'not null']);return chain;},
      neq(k,v){assert(v==='');filters.push([k,'nonempty']);return chain;},
      async single(){return {data:data()};},
      async maybeSingle(){return {data:data(),error:noteError && table==='solution_clarifications' ? {message:'unavailable'} : null};},
      async insert(row){writes.push([table,row.user_id]);},
    };
    return chain;
  };
  let handler;
  const client = {auth:{getUser:async()=>({data:{user:student}})},from,
    storage:{from:()=>({createSignedUrl:async()=>({data:null,error:null})})}};
  vm.runInNewContext(stripTypeScriptTypes(source), {Deno:{env:{get:()=>''},serve:fn=>{handler=fn;}},createClient:()=>client,Response,console});
  const response = await handler(new Request('http://example.test', {method:'POST',
    headers:signedIn ? {Authorization:'Bearer test-token'} : {},
    body:JSON.stringify({problem_id:problem.id})}));
  return {status:response.status,output:await response.json(),reads,writes,original};
}

for (const options of [{signedIn:false},{member:false},{attempt:false}]) {
  const check = await request({...options,note:'Private test note'});
  assert.equal(check.status, options.signedIn===false ? 401 : 403);
  assert(!check.reads.includes('content_problems') && !check.reads.includes('solution_clarifications'));
  assert.equal(check.writes.length,0);
}
for (const options of [{},{note:'Private test note'},{note:'Private test note',noteError:true}]) {
  const check=await request(options);
  assert.equal(check.status,200);
  assert(check.reads.indexOf('problem_attempts') < check.reads.indexOf('solution_clarifications'));
  const expected=options.note && !options.noteError ? check.original+'\n\nAnother way to see it\n'+options.note : check.original;
  assert.equal(check.output.solution_text, expected);
  assert.deepEqual(check.writes,[['problem_attempts','test-learner']]);
}
console.log('Verified attempt-gated clarifications and original explanations.');
