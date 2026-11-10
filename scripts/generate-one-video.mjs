import fs from "node:fs/promises";
import path from "node:path";
import { KokoroTTS } from "kokoro-js";

const queueFile=process.argv[2];
const videoId=process.argv[3];
const outDir=process.argv[4]||"out";
if(!queueFile||!videoId) throw new Error("Usage: node generate-one-video.mjs <queue.json> <video_id> [out]");

const queue=JSON.parse(await fs.readFile(queueFile,"utf8"));
const video=queue.find(v=>v.video_id===videoId);
if(!video) throw new Error(`Video ${videoId} not found in ${queueFile}`);
await fs.mkdir(outDir,{recursive:true});

const text=video.chunks.map(c=>c.text.trim()).join(" ");
console.log(`Generating ${videoId}: ${video.title} · ${video.word_count} words · one isolated synthesis call`);

const tts=await KokoroTTS.from_pretrained("onnx-community/Kokoro-82M-v1.0-ONNX",{
  dtype:"q8",
  device:"cpu",
  progress_callback:(x)=>{
    if(x?.status==="progress"&&x?.file){
      process.stdout.write(`\rmodel ${Number(x.progress||0).toFixed(1)}% ${x.file}   `);
    }
  }
});
console.log("\nModel ready");
const audio=await tts.generate(text,{voice:"af_heart",speed:0.88});
const target=path.join(outDir,`${videoId}_narration.wav`);
await audio.save(target);
const st=await fs.stat(target);
if(st.size<1000) throw new Error("Generated WAV unexpectedly small");
await fs.writeFile(path.join(outDir,"manifest.json"),JSON.stringify({
  video_id:videoId,
  title:video.title,
  word_count:video.word_count,
  voice:"af_heart",
  speed:0.88,
  model:"onnx-community/Kokoro-82M-v1.0-ONNX",
  bytes:st.size,
  generated_at:new Date().toISOString()
},null,2));
console.log(`Saved ${target} · ${(st.size/1048576).toFixed(2)} MB`);
