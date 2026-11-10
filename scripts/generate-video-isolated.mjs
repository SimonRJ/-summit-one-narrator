import fs from "node:fs/promises";
import path from "node:path";
import { spawn } from "node:child_process";
import { promisify } from "node:util";
import { execFile } from "node:child_process";
const execFileP=promisify(execFile);

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
const silence=path.join(work,"silence.wav");
await execFileP("ffmpeg",["-y","-v","error","-f","lavfi","-i","anullsrc=r=24000:cl=mono","-t","0.22","-c:a","pcm_s16le",silence]);
const list=[];
for(let i=0;i<video.chunks.length;i++){
 list.push(`file '${path.resolve(path.join(work,`chunk-${String(i+1).padStart(2,"0")}.wav`)).replaceAll("'","'\\''")}'`);
 if(i<video.chunks.length-1) list.push(`file '${path.resolve(silence).replaceAll("'","'\\''")}'`);
}
const concat=path.join(work,"concat.txt"); await fs.writeFile(concat,list.join("\n")+"\n");
const target=path.join(outDir,`${videoId}_narration.wav`);
await execFileP("ffmpeg",["-y","-v","error","-f","concat","-safe","0","-i",concat,"-ar","24000","-ac","1","-c:a","pcm_s16le",target]);
const st=await fs.stat(target); if(st.size<1000) throw new Error("Final WAV too small");
await fs.writeFile(path.join(outDir,"manifest.json"),JSON.stringify({video_id:videoId,title:video.title,word_count:video.word_count,chunks:video.chunks.length,voice:"af_heart",speed:0.88,bytes:st.size},null,2));
console.log(`Complete ${videoId}: ${(st.size/1048576).toFixed(2)} MB`);
