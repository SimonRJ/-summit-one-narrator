import assert from 'node:assert/strict';
import fs from 'node:fs';
import {methods,checkAnswer} from '../curriculum.js';
import {practice,bridgeHTML} from '../transfer-practice.js';
for(const id of Object.keys(methods))for(let seed=0;seed<52;seed++){
 const q=practice(id,seed);assert(q.prompt.length>20&&q.steps.length===3);assert(q.steps.every(s=>s.length>15));assert(!/undefined|NaN/.test(JSON.stringify(q)),id);assert(checkAnswer(q.value,String(q.value)));assert(!checkAnswer(q.value,'maybe '+q.value));assert(!/undefined|NaN/.test(bridgeHTML(id,seed+1)));
 const n=3+seed%13,k=2+seed%4;
 if(id==='DIG-02'){let count=0;for(let a=1;a<=k+2;a++)for(let b=0;b<=k+2;b++)for(let c=0;c<=k+2;c++)if(a%2===0&&new Set([a,b,c]).size===3)count++;assert.equal(q.value,count)}
 if(id==='DIV-01'){let count=0,N=2**k*25;for(let d=2;d<=N;d+=2)if(N%d===0)count++;assert.equal(q.value,count)}
 if(id==='DIV-03')for(let a=0;a<10;a++)assert.equal(((7*a+k)**2+4)%7,q.value);
 if(id==='GEO-05'){let best=0;for(let a=1;a<2*n+1;a++)best=Math.max(best,a*(2*n+1-a));assert.equal(q.value,best)}
 if(id==='SOLID-02'){let count=0,N=k+3;for(let x=0;x<N;x++)for(let y=0;y<N;y++)for(let z=0;z<N;z++)if(Number(x===0||x===N-1)+Number(y===0||y===N-1)+Number(z===0||z===N-1)===2)count++;assert.equal(q.value,count)}
 if(id==='SPATIAL-01'){const routes=(x,y)=>x===0||y===0?1:routes(x-1,y)+routes(x,y-1);assert.equal(q.value,routes(1,1)*routes(k-1,1))}
}
const s=JSON.parse(fs.readFileSync(new URL('../data/sessions-372.json',import.meta.url))).sessions;
assert.equal(s.filter(x=>x.type==='MIXED').length,36);assert(!s.some(x=>/MOCK/.test(x.type)));assert.equal(s.filter(x=>x.type==='MAWA').length,53);
for(const f of ['app-main.js','tests.js','supabase/functions/grade-exam/index.ts'])assert(!/star[345]_correct|increment_timed_star_correct/.test(fs.readFileSync(new URL('../'+f,import.meta.url),'utf8')));
console.log('PASS: 2,704 technique-practice variants; independent digit, factor, remainder, geometry and route checks; 36 workshops; no star feature.');
