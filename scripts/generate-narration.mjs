import fs from "node:fs/promises";
import path from "node:path";
import crypto from "node:crypto";
import { KokoroTTS } from "kokoro-js";

const queuePath = process.argv[2];
const outDir = process.argv[3] || "narration-out";
if (!queuePath) throw new Error("Usage: node generate-narration.mjs <queue.json> [outDir]");

const VOICE = "af_heart";
const SPEED = 0.88;
const MODEL_ID = "onnx-community/Kokoro-82M-v1.0-ONNX";
const DTYPE = "q8";
const DEVICE = "cpu";
const GAP_SECONDS = 0.22;

await fs.mkdir(outDir, { recursive: true });
const queue = JSON.parse(await fs.readFile(queuePath, "utf8"));

console.log(`Loading Kokoro ${DTYPE}/${DEVICE} for ${queuePath}…`);
const tts = await KokoroTTS.from_pretrained(MODEL_ID, {
  dtype: DTYPE,
  device: DEVICE,
  progress_callback: (x) => {
    if (x?.status === "progress" && x?.file) {
      const pct = Number(x.progress || 0).toFixed(1);
      process.stdout.write(`\rmodel ${pct}% ${x.file}   `);
    }
  },
});
console.log("\nModel ready.");

function concatFloat(arrays, rate, gap=GAP_SECONDS) {
  const gapN = Math.floor(rate * gap);
  const total = arrays.reduce((n,a)=>n+a.length,0) + Math.max(0, arrays.length-1)*gapN;
  const out = new Float32Array(total);
  let pos = 0;
  arrays.forEach((a,i)=>{
    out.set(a,pos);
    pos += a.length;
    if (i < arrays.length-1) pos += gapN;
  });
  return out;
}

function wavBuffer(samples, rate=24000) {
  const b = Buffer.allocUnsafe(44 + samples.length*2);
  b.write("RIFF",0);
  b.writeUInt32LE(36 + samples.length*2,4);
  b.write("WAVE",8);
  b.write("fmt ",12);
  b.writeUInt32LE(16,16);
  b.writeUInt16LE(1,20);
  b.writeUInt16LE(1,22);
  b.writeUInt32LE(rate,24);
  b.writeUInt32LE(rate*2,28);
  b.writeUInt16LE(2,32);
  b.writeUInt16LE(16,34);
  b.write("data",36);
  b.writeUInt32LE(samples.length*2,40);
  let o=44;
  for (let i=0;i<samples.length;i++,o+=2) {
    const x=Math.max(-1,Math.min(1,samples[i]));
    b.writeInt16LE(Math.round(x < 0 ? x*32768 : x*32767),o);
  }
  return b;
}

async function generateChunk(text, label) {
  let last;
  for (let attempt=1; attempt<=3; attempt++) {
    try {
      const r = await tts.generate(text, { voice: VOICE, speed: SPEED });
      if (!r?.data?.length) throw new Error("Kokoro returned no waveform data");
      return { data: r.data, rate: r.sampling_rate || 24000 };
    } catch (e) {
      last=e;
      console.error(`\n${label} attempt ${attempt} failed: ${e.message}`);
      await new Promise(r=>setTimeout(r, attempt*2000));
    }
  }
  throw last;
}

const manifest = {
  schema_version: "summit-one-kokoro-cloud-v1",
  generated_at: new Date().toISOString(),
  queue_file: path.basename(queuePath),
  model: MODEL_ID,
  dtype: DTYPE,
  device: DEVICE,
  voice: VOICE,
  speed: SPEED,
  gap_seconds: GAP_SECONDS,
  videos: []
};

for (let vi=0; vi<queue.length; vi++) {
  const v=queue[vi];
  console.log(`[${vi+1}/${queue.length}] ${v.video_id} — ${v.title} (${v.chunks.length} chunks)`);
  const parts=[];
  let rate=24000;
  for (let ci=0; ci<v.chunks.length; ci++) {
    const c=v.chunks[ci];
    console.log(`  chunk ${ci+1}/${v.chunks.length}: ${c.chunk_id} (${c.word_count} words)`);
    const r=await generateChunk(c.text, c.chunk_id);
    parts.push(r.data);
    rate=r.rate;
  }
  const pcm=concatFloat(parts, rate);
  const wav=wavBuffer(pcm, rate);
  const filename=`${v.video_id}_narration.wav`;
  await fs.writeFile(path.join(outDir,filename),wav);
  const sha256=crypto.createHash("sha256").update(wav).digest("hex");
  const duration=pcm.length/rate;
  manifest.videos.push({
    video_id:v.video_id,
    title:v.title,
    type:v.type,
    source:v.source,
    held_in_iphone_app:Boolean(v.held),
    chunk_count:v.chunks.length,
    word_count:v.word_count,
    duration_seconds:Number(duration.toFixed(3)),
    sample_rate:rate,
    filename,
    bytes:wav.length,
    sha256
  });
  console.log(`  saved ${filename} — ${duration.toFixed(1)} s — ${(wav.length/1048576).toFixed(1)} MB`);
  await fs.writeFile(path.join(outDir,"manifest.json"),JSON.stringify(manifest,null,2));
}

await fs.writeFile(path.join(outDir,"manifest.json"),JSON.stringify(manifest,null,2));
console.log(`Completed ${manifest.videos.length} videos from ${queuePath}.`);
