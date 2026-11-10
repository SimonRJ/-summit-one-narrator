import fs from "node:fs";
import { execFileSync } from "node:child_process";

const queue=[];
for(let i=1;i<=10;i++){const p=`queue-${String(i).padStart(2,"0")}.json`;if(fs.existsSync(p))queue.push(...JSON.parse(fs.readFileSync(p,"utf8")))}
if(fs.existsSync("queue-special.json"))queue.push(...JSON.parse(fs.readFileSync("queue-special.json","utf8")));
const byId=new Map(queue.map(x=>[x.video_id,x]));

function show(ref,path){try{return JSON.parse(execFileSync("git",["show",`${ref}:${path}`],{encoding:"utf8",maxBuffer:50*1024*1024}))}catch{return {items:[]}}}
const historical=[
 ...show("24734d0fa7142d2157ce53f5e25f85fb8209c347","data/challenges-amc-001-040.json").items,
 ...show("fe6f32430e546c6c797e51916d195590569f85b0","data/challenges-amc-041-080.json").items,
 ...show("1684f38ca03e8f12ede272044d70f0d8520033d8","data/challenges-amc-081-120.json").items,
 ...show("0b6453c67e50baae8567f465158584d79cda185a","data/challenges-amc-121-152.json").items,
 ...show("8aa4dd54ad20f49ac863718f37dfb4ff93b17ebb","data/challenges-original-42.json").items
];
const hist=new Map(historical.map(x=>[x.id,x]));
const teaching=JSON.parse(fs.readFileSync("data/teaching-72.json","utf8")).items;
const items=[];
for(const t of teaching){
 const q=byId.get(t.id);
 items.push({id:t.id,title:t.title,type:t.type,category:t.chapter,accent:"cyan",segments:q?.chunks?.map(c=>c.text)||t.chunks.map(c=>c.text)});
}
for(const h of historical){
 const q=byId.get(h.id);
 const segments=q?.chunks?.map(c=>c.text) || (h.spoken_script?String(h.spoken_script).split(/\n\n+/):( [h.prompt,...(h.solution_steps||[])] ));
 items.push({id:h.id,title:h.title,type:h.type||h.kind||"challenge",category:h.category||h.related_teaching||"reasoning",accent:"gold",segments:segments.filter(Boolean)});
}
const unique=[...new Map(items.map(x=>[x.id,x])).values()].sort((a,b)=>a.id.localeCompare(b.id,undefined,{numeric:true}));
if(unique.length!==266)throw new Error(`Expected 266 render records, got ${unique.length}`);
fs.mkdirSync("render",{recursive:true});fs.writeFileSync("render/manifest.json",JSON.stringify({count:unique.length,items:unique},null,2));
console.log("Render manifest:",unique.length);
