import assert from 'node:assert/strict';
import fs from 'node:fs';
import {checkAnswer,skillFor} from '../curriculum.js';
import {mixedFlashDeck} from '../flash-cards.js';
import {practice} from '../transfer-practice.js';
import {workshopStudies} from '../workshop-studies.js';

const read = file => JSON.parse(fs.readFileSync(new URL('../data/'+file,import.meta.url)));
const course = read('sessions-372.json').sessions;
const taxonomy = read('taxonomy-52.json');
const range = n => Array.from({length:n},(_,i)=>i);
const sum = values => values.reduce((a,b)=>a+b,0);
const pairs = values => values.flatMap((a,i)=>values.slice(i+1).map(b=>[a,b]));
const permutations = values => values.length ? values.flatMap((v,i)=>permutations(values.filter((_,j)=>j!==i)).map(t=>[v,...t])) : [[]];
const triples = (values) => values.flatMap((a,i)=>pairs(values.slice(i+1)).map(([b,c])=>[a,b,c]));
const paths = (x,y,blocked) => x<0||y<0||blocked?.[0]===x&&blocked?.[1]===y ? 0 : x+y===0 ? 1 : paths(x-1,y,blocked)+paths(x,y-1,blocked);
const cubes = (x,y,z) => range(x).flatMap(a=>range(y).flatMap(b=>range(z).map(c=>[a,b,c])));
const boundaryCount = (p,shape) => p.filter((n,i)=>n===0||n===shape[i]-1).length;
const routeTilings = (length,sizes,blocked) => length<0||length===blocked ? 0 : length===0 ? 1 : sum(sizes.map(n=>routeTilings(length-n,sizes,blocked)));
function flips() {
 const goal=0b100001, seen=new Set([0]);let states=[0];
 for(let n=1;n<=5;n++){
  const next=[];
  for(const state of states)for(const i of range(5)){
   const moved=state^(3<<i);if(moved===goal)return n;
   if(!seen.has(moved)){next.push(moved);seen.add(moved)}
  }
  states=next;
 }
}
function cubeTunnelArea(){
 const cells=cubes(3,3,3).filter(([x,y])=>x!==1||y!==1);
 const solid=new Set(cells.map(p=>p.join(',')));
 return sum(cells.map(p=>sum([0,1,2].flatMap(k=>[-1,1].map(d=>{
  const q=p.slice();q[k]+=d;return Number(!solid.has(q.join(',')));
 })))));
}
function inspectionCircuit(){
 // Uniform-cost search on (junction, set of paths already walked).
 const edges=[['A','B',3],['B','C',4],['C','D',3],['D','A',4],['A','C',5]];
 const queue=[[0,'B',0]],seen=new Set();
 while(queue.length){
  queue.sort((a,b)=>b[0]-a[0]);
  const [cost,v,mask]=queue.pop(),key=v+','+mask;
  if(seen.has(key))continue;seen.add(key);
  if(v==='B' && mask===31)return cost;
  edges.forEach(([a,b,length],i)=>{if(v===a||v===b)queue.push([cost+length,v===a?b:a,mask|(1<<i)])});
 }
}
function possibleDominoes(n,holes){
 // Dynamic programming over the used cells in each row.
 const blocked=Array.from({length:n},(_,y)=>sum(holes.filter(p=>p[1]===y).map(p=>1<<p[0])));
 let active=new Map([[0,0]]);
 for(let y=0;y<n;y++){
  const next=new Map();
  function visit(mask,below,count){
   const x=range(n).find(x=>(mask&(1<<x))===0);
   if(x===undefined){next.set(below,Math.max(next.get(below)??0,count));return}
   visit(mask|(1<<x),below,count);
   if(x+1<n&&!(mask&(1<<(x+1))))visit(mask|(3<<x),below,count+1);
   if(y+1<n&&!(blocked[y+1]&(1<<x)))visit(mask|(1<<x),below|(1<<x),count+1);
  }
  for(const [above,count] of active)visit(above|blocked[y],0,count);
  active=next;
 }
 return active.get(0);
}
const allDice = range(6).flatMap(b=>range(6).map(r=>[r+1,b+1]));
const larger = allDice.filter(([r,b])=>r>b);
const transfer = new Map([
 [16,range(61).find(t=>t>=2&&(t-2)%6===0&&(t-1)%5===0)],
 [32,range(100).find(x=>Number.isInteger(x*3/8)&&x*3/8+14===x*5/8)],
 [48,20],[64,triples(range(11).map(i=>2*i+1)).filter(t=>sum(t)===21).length],
 [80,Math.max(...range(13).slice(3).map(i=>(i-2)*(15-i-2)))],
 [96,cubes(5,4,3).filter(p=>boundaryCount(p,[5,4,3])===2).length],
 [111,paths(4,2,[2,1])],[128,4],
 [136,pairs(range(6)).filter(([a,b])=>b-a!==1&&b-a!==5).length],
 [144,range(150).find(x=>150*.2===(150-x)*.25)],
 [160,flips()],[176,routeTilings(8,[1,3],4)],
 [184,range(11).slice(1).find(lap=>Number.isInteger(lap*4/6))],
 [192,range(81).slice(1).filter(v=>(v%4===0)!==(v%6===0)).length],
 [208,Math.abs(63*(7-2)/9)],[212,range(201).find(l=>l/8===(l+135)/23)],
 [225,range(6).slice(1).find(v=>[v<4,v%2===1,v===5].filter(Boolean).length===1)],
 [236,range(101).slice(1).map(x=>x*x).find(x=>x%18===0&&x%20===0)],
 [240,range(5).flatMap(bell=>pairs(range(5).filter(p=>p!==bell)).map(rope=>[bell,...rope])).filter(team=>team.includes(0)).length],
 [256,range(151).slice(1).filter(n=>[...String(n)].filter(d=>d==='1').length>=2).length],
 [264,300/11],[272,larger.filter(([r,b])=>r===b+1).length/larger.length],
 [288,range(51).find(n=>6*12+20*n===(6+n)*17)],[292,possibleDominoes(5,[[0,0],[4,4]])],
 [304,range(85).find(n=>(84-n+6)===2*(n-6))],
 [316,sum([1,3,6,18,36])],[320,permutations([...'PQRST']).filter(p=>['P','Q'].every(c=>p.indexOf(c)<p.indexOf('R'))&&p.indexOf('S')<p.indexOf('T')).length],
 [328,['north','east','south','west'][sum(range(19))%4]],
 [337,range(1000).slice(100).filter(n=>{const [a,b,c]=[...String(n)].map(Number);return a<b&&b<c&&c<=6&&c%2===0}).length],
 [340,range(201).slice(1).find(d=>Math.abs(d/18+d/36+1/6-d/10)<1e-10)],
 [344,cubeTunnelArea()],[352,range(1000).slice(1).find(n=>[2*n+1,3*n+1].every(x=>Number.isInteger(Math.sqrt(x))))],
 [356,range(10000).slice(1000).filter(n=>n%9===0&&[...String(n)].reverse().join('')===String(n)).length],
 [363,52],[369,range(16).find(d=>d*2+(15-d)*3===38)],[372,inspectionCircuit()]
]);
assert.deepEqual(pairs([11,15,20]).map(sum).sort((a,b)=>a-b),[26,31,35]);
assert.deepEqual([4,6,8,10].map(n=>28-n).sort((a,b)=>a-b),[18,20,22,24]);
assert(Math.abs((6-.5)*transfer.get(264)-60-90)<1e-10);
assert.equal(2*(12+8)+(4+3+4-3)+(2+2+2-2),transfer.get(363));

function recallAnswer(id,seed){
 const n=3+seed%13,k=2+seed%4;
 switch(id){
  case 'DIG-01':return sum(Array(n).fill(99));
  case 'DIG-02':return range(1000).slice(100).filter(x=>{const d=[...String(x)].map(Number);return d.every(digit=>digit<=k+2)&&d[0]%2===0&&new Set(d).size===3}).length;
  case 'DIG-03':return sum(range(100).map(v=>[...String(100*n+v).slice(-2)].filter(c=>c==='7').length));
  case 'DIG-04':return range(10000).slice(1000).filter(v=>{const s=String(v);return [...s].every(d=>+d<=k+3)&&s===[...s].reverse().join('')}).length;
  case 'DIG-05':return range(10).find(a=>3*(10*k+a)===3*(10*k+8));
  case 'DIV-01':{const num=2**k*25;return range(num+1).slice(1).filter(d=>d%2===0&&num%d===0).length}
  case 'DIV-02':return range(48*n+1).slice(1).filter(m=>m%(4*n)===0&&m%(6*n)===0).length;
  case 'DIV-03':return ((7*3+k)**2+4)%7;
  case 'DIV-04':return 'no'; // Toggling a pair preserves parity of the lit count.
  case 'DIV-05':return ['red','blue','green','gold'][(4*n+k-1)%4];
  case 'FRAC-01':return 18*n*(1-1/3)*(1-1/4);
  case 'FRAC-02':return range(251).find(t=>t*5/8-t*3/8===2*n);
  case 'FRAC-03':return 80*n*5/4;
  case 'FRAC-04':return (2/3*(3*n)+.5*(2*n))/(5*n);
  case 'RATE-01':return 6*n/((n+1)-1);
  case 'RATE-02':return 1/(1/(3*n)-1/(6*n));
  case 'RATE-03':return 3*n/(2*n/6+n/3);
  case 'RATE-04':return range(100).find(t=>5*t===2*n+3*t);
  case 'ALG-01':return range(100).find(x=>5*x+7===5*n+7);
  case 'ALG-02':return range(101).find(x=>x+(x-2*n)===8*n+6);
  case 'ALG-03':return range(101).find(x=>7*x+2*(4*n+9-4*x)===7*n+18);
  case 'ALG-04':return range(101).find(x=>(x-5)*2+9===2*n+9);
  case 'ALG-05':return range(101).find(t=>5*n-t===2*(n+t));
  case 'SEQ-01':{const seats=range(n+3).map(i=>n+i);return seats[0]+seats.at(-1)}
  case 'SEQ-02':return sum(range(5).map(i=>n*2**i));
  case 'SEQ-03':return routeTilings(k+3,[1,2]);
  case 'SEQ-04':return range(10*n+2).reduce(state=>(state+3)%10,k);
  case 'COUNT-01':return pairs(range(2*n+2).slice(1)).filter(p=>sum(p)===2*n+2).length;
  case 'COUNT-02':return range(n+2).flatMap(a=>range(n+2).filter(b=>a!==b)).length;
  case 'COUNT-03':return permutations(range(k+2)).filter(p=>Math.abs(p.indexOf(0)-p.indexOf(1))>1).length;
  case 'COUNT-04':return (6*n+5*n)-10*n;
  case 'COUNT-05':return 2*pairs(range(n+3)).length;
  case 'COUNT-06':return range(100).slice(10).filter(v=>{const d=[...String(v)].map(Number);return d.every(i=>i>=1&&i<=k+2)&&d.filter(i=>i===1).length===1}).length;
  case 'LOGIC-01':return range(n+10).filter(x=>(x>n)!==(x>n+3)).length;
  case 'LOGIC-02':return range(12*n+12).slice(12*n+1).find(x=>x%2===0&&x%3===0&&x%4!==0);
  case 'LOGIC-03':return sum([n+2,n+5,n+8])-sum([n+1,n+4]);
  case 'LOGIC-04':return range(n*(n+2)+1).find(x=>x*(x+2)===n*(n+2));
  case 'GEO-01':return 4*(n+2)+4*n-2*n;
  case 'GEO-02':return (2*n)*(2*k)/2-(2*n)*k/2;
  case 'GEO-03':return (180-20-10*k)/2;
  case 'GEO-04':return range(2*n).filter(shift=>range(2*n).every(i=>(i+shift)%2===i%2)).length;
  case 'GEO-05':return Math.max(...range(2*n+2).map(a=>a*(2*n+1-a)));
  case 'SOLID-01':return cubes(n,4,3).filter(([x,y])=>x!==0||y!==0).length;
  case 'SOLID-02':{const side=k+3;return cubes(side,side,side).filter(p=>boundaryCount(p,[side,side,side])===2).length}
  case 'SOLID-03':return n*(n+2)+2*(n*3)+2*((n+2)*3);
  case 'SPATIAL-01':return paths(k,2)-paths(k,2,[1,1]);
  case 'SPATIAL-02':return 2*pairs(range(k+1)).length;
  case 'SPATIAL-03':{const board=range(2*k).flatMap(x=>range(2*k).map(y=>[x,y])).filter(([x,y])=>!(x===y&&(x===0||x===2*k-1)));assert.notEqual(board.filter(([x,y])=>(x+y)%2===0).length*2,board.length);return 'no'}
  case 'SPATIAL-04':return (2*(n+3)>2)?'no':'yes';
  case 'DATA-01':return 1/(k+2);
  case 'DATA-02':return (12*n-3)/(n-1);
  case 'DATA-03':return (2*n+3*n)/2;
  default:throw Error('Unverified technique '+id);
 }
}
const slots=course.filter(s=>s.type==='MIXED').map(s=>s.slot);
assert.deepEqual([...workshopStudies.keys()],slots);
assert.deepEqual([...transfer.keys()],slots);
const prompts=new Set(),techniques=new Set(),titles=new Set();
for(const [slot,study] of workshopStudies){
 const taught=new Set(course.filter(s=>s.slot<slot&&s.type==='LESSON').map(s=>skillFor(s,taxonomy)));
 const skills=[...study.recall.map(([id])=>id),study.id];
 assert.equal(new Set(skills).size,6);
 assert(skills.every(id=>taught.has(id)),slot);
 assert(!titles.has(study.title));titles.add(study.title);
 const flash=mixedFlashDeck(skills,slot);assert.equal(flash.length,5);assert.equal(new Set(flash.map(card=>card.q)).size,5);
 for(const card of flash)assert(card.why && card.options[card.answer]===card.yes);
 const expected=transfer.get(slot);
 assert(checkAnswer(study.value,String(expected)),slot+' transfer');
 for(const [id,seed] of study.recall){
  techniques.add(id);const q=practice(id,seed),v=recallAnswer(id,seed);
  assert(checkAnswer(q.value,String(v)),slot+' '+id+' '+q.value+' '+v);
  assert(!prompts.has(q.prompt));prompts.add(q.prompt);
 }
 assert(study.steps.length>=3 && study.contrast && study.hint && !prompts.has(study.prompt));prompts.add(study.prompt);
}
assert.equal(techniques.size,52);assert.equal(prompts.size,216);
console.log('Passed 36 workshops, 216 different prompts, independent answers, taught prerequisites, 52 recall techniques and 180 flash decisions.');
