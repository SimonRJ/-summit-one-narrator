import fs from "node:fs/promises";
import path from "node:path";
import { spawn } from "node:child_process";

const [queueFile,videoId,outDir="out"]=process.argv.slice(2);
const queue=JSON.parse(await fs.readFile(queueFile,"utf8"));
const video=queue.find(v=>v.video_id===videoId);
if(!video) throw new Error("Video not found");
await fs.mkdir(outDir,{recursive:true});
const work=path.join(outDir,"chunks");
await fs.mkdir(work,{recursive:true});

function runNode(args){
 return new Promise((resolve,reject)=>{
   const p=spawn(process.execPath,args,{stdio:"inherit"});
   p.on("exit",code=>code===0?resolve():reject(new Error(`child exited ${code}`)));
 });
}
for(let i=0;i<video.chunks.length;i++){
 await runNode(["scripts/generate-single-chunk.mjs",queueFile,videoId,String(i),work]);
}

function parseWav(buf){
 if(buf.toString("ascii",0,4)!=="RIFF"||buf.toString("ascii",8,12)!=="WAVE")throw new Error("Invalid WAV");
 const format=buf.readUInt16LE(20),channels=buf.readUInt16LE(22),rate=buf.readUInt32LE(24),bits=buf.readUInt16LE(34);
 let pos=12,dataStart=-1,dataSize=0;
 while(pos+8<=buf.length){
   const id=buf.toString("ascii",pos,pos+4),size=buf.readUInt32LE(pos+4);
   if(id==="data"){dataStart=pos+8;dataSize=size;break}
   pos+=8+size+(size%2);
 }
 if(dataStart<0)throw new Error("WAV data chunk missing");
 return {format,channels,rate,bits,data:buf.subarray(dataStart,Math.min(buf.length,dataStart+dataSize))};
}
function wavHeader(dataBytes,{format,channels,rate,bits}){
 const blockAlign=channels*bits/8,byteRate=rate*blockAlign,b=Buffer.alloc(44);
 b.write("RIFF",0);b.writeUInt32LE(36+dataBytes,4);b.write("WAVE",8);b.write("fmt ",12);b.writeUInt32LE(16,16);
 b.writeUInt16LE(format,20);b.writeUInt16LE(channels,22);b.writeUInt32LE(rate,24);b.writeUInt32LE(byteRate,28);b.writeUInt16LE(blockAlign,32);b.writeUInt16LE(bits,34);
 b.write("data",36);b.writeUInt32LE(dataBytes,40);return b;
}
const parsed=[];
for(let i=0;i<video.chunks.length;i++) parsed.push(parseWav(await fs.readFile(path.join(work,`chunk-${String(i+1).padStart(2,"0")}.wav`))));
const spec=parsed[0];
for(const p of parsed)if(p.format!==spec.format||p.channels!==spec.channels||p.rate!==spec.rate||p.bits!==spec.bits)throw new Error("Chunk WAV formats differ");
const gapFrames=Math.round(spec.rate*0.22),gapBytes=gapFrames*spec.channels*spec.bits/8;
const pieces=[];
parsed.forEach((p,i)=>{pieces.push(p.data);if(i<parsed.length-1)pieces.push(Buffer.alloc(gapBytes))});
const body=Buffer.concat(pieces),target=path.join(outDir,`${videoId}_narration.wav`);
await fs.writeFile(target,Buffer.concat([wavHeader(body.length,spec),body]));
const st=await fs.stat(target);if(st.size<1000)throw new Error("Final WAV too small");
await fs.writeFile(path.join(outDir,"manifest.json"),JSON.stringify({video_id:videoId,title:video.title,word_count:video.word_count,chunks:video.chunks.length,voice:"af_heart",speed:0.88,bytes:st.size,sample_rate:spec.rate,format:spec.format,bits:spec.bits},null,2));
console.log(`Complete ${videoId}: ${(st.size/1048576).toFixed(2)} MB`);
