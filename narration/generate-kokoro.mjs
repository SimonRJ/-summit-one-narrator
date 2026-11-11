import fs from "node:fs";
import path from "node:path";
import { KokoroTTS } from "kokoro-js";

const MODEL_ID = "onnx-community/Kokoro-82M-v1.0-ONNX";
const VOICE = "af_heart";
const SPEED = 0.88;
const DTYPE = "q8";
const DEVICE = "cpu";
const GAP_SECONDS = 0.22;

const queueFile = process.env.QUEUE_FILE;
if (!queueFile) throw new Error("QUEUE_FILE is required");
const outDir = process.env.OUT_DIR || "output";
const heldMode = process.env.PROCESS_HELD || "exclude"; // exclude | only | include

fs.mkdirSync(outDir, { recursive: true });
const queue = JSON.parse(fs.readFileSync(queueFile, "utf8"));
let selected = queue;
if (heldMode === "exclude") selected = queue.filter(x => !x.held);
if (heldMode === "only") selected = queue.filter(x => x.held);

console.log(`Loading Kokoro model ${MODEL_ID} (${DTYPE}/${DEVICE})...`);
const tts = await KokoroTTS.from_pretrained(MODEL_ID, { dtype: DTYPE, device: DEVICE });
console.log(`Loaded. Generating ${selected.length} video narrations with ${VOICE} at speed ${SPEED}.`);

function safeName(s) {
  return String(s).replace(/[^A-Za-z0-9._-]+/g, "_");
}
function concatWithGap(arrays, rate, gapSeconds = GAP_SECONDS) {
  const gapN = Math.floor(rate * gapSeconds);
  const total = arrays.reduce((n,a)=>n+a.length,0) + Math.max(0, arrays.length - 1) * gapN;
  const out = new Float32Array(total);
  let p = 0;
  arrays.forEach((a,i) => {
    out.set(a,p); p += a.length;
    if (i < arrays.length - 1) p += gapN;
  });
  return out;
}
function wavBuffer(samples, rate = 24000) {
  const b = Buffer.alloc(44 + samples.length * 2);
  b.write("RIFF", 0, 4, "ascii");
  b.writeUInt32LE(36 + samples.length * 2, 4);
  b.write("WAVE", 8, 4, "ascii");
  b.write("fmt ", 12, 4, "ascii");
  b.writeUInt32LE(16, 16);
  b.writeUInt16LE(1, 20);
  b.writeUInt16LE(1, 22);
  b.writeUInt32LE(rate, 24);
  b.writeUInt32LE(rate * 2, 28);
  b.writeUInt16LE(2, 32);
  b.writeUInt16LE(16, 34);
  b.write("data", 36, 4, "ascii");
  b.writeUInt32LE(samples.length * 2, 40);
  let o = 44;
  for (let i=0;i<samples.length;i++) {
    const x = Math.max(-1, Math.min(1, samples[i]));
    b.writeInt16LE(Math.round(x < 0 ? x * 32768 : x * 32767), o);
    o += 2;
  }
  return b;
}
async function generateChunk(text, label) {
  let last;
  for (let attempt=1; attempt<=2; attempt++) {
    try {
      const r = await tts.generate(text, { voice: VOICE, speed: SPEED });
      const samples = r.audio ?? r.data;
      if (!samples?.length) throw new Error("Kokoro returned no waveform");
      return { samples: samples instanceof Float32Array ? samples : Float32Array.from(samples), rate: r.sampling_rate || 24000 };
    } catch (e) {
      last = e;
      console.warn(`${label}: attempt ${attempt} failed: ${e.message}`);
    }
  }
  throw last;
}

const manifest = {
  generated_at: new Date().toISOString(),
  model: MODEL_ID,
  voice: VOICE,
  speed: SPEED,
  dtype: DTYPE,
  device: DEVICE,
  gap_seconds: GAP_SECONDS,
  queue_file: queueFile,
  held_mode: heldMode,
  videos: [],
  failures: []
};

for (let i=0;i<selected.length;i++) {
  const item = selected[i];
  console.log(`[${i+1}/${selected.length}] ${item.video_id} — ${item.title}`);
  try {
    const parts = [];
    let rate = 24000;
    const chunkMeta = [];
    for (let c=0;c<item.chunks.length;c++) {
      const ch = item.chunks[c];
      const r = await generateChunk(ch.text, ch.chunk_id);
      if (parts.length && r.rate !== rate) throw new Error(`sample-rate mismatch ${rate} vs ${r.rate}`);
      rate = r.rate;
      parts.push(r.samples);
      chunkMeta.push({
        chunk_id: ch.chunk_id,
        sequence: ch.sequence,
        words: ch.word_count,
        duration_seconds: Number((r.samples.length / rate).toFixed(3))
      });
    }
    const joined = concatWithGap(parts, rate);
    const filename = safeName(item.video_id) + ".wav";
    fs.writeFileSync(path.join(outDir, filename), wavBuffer(joined, rate));
    const duration = joined.length / rate;
    const estimate = Number(item.estimated_seconds || 0);
    manifest.videos.push({
      video_id: item.video_id,
      title: item.title,
      type: item.type,
      held: !!item.held,
      filename,
      sample_rate: rate,
      duration_seconds: Number(duration.toFixed(3)),
      estimated_seconds: estimate || null,
      duration_ratio_vs_estimate: estimate ? Number((duration / estimate).toFixed(4)) : null,
      chunks: chunkMeta
    });
  } catch (e) {
    console.error(`${item.video_id} FAILED: ${e.stack || e.message}`);
    manifest.failures.push({ video_id: item.video_id, error: e.message });
  }
}

fs.writeFileSync(path.join(outDir, "manifest.json"), JSON.stringify(manifest, null, 2));
fs.writeFileSync(path.join(outDir, "README.txt"),
  `Summit One Kokoro narration production\nModel: ${MODEL_ID}\nVoice: ${VOICE}\nSpeed: ${SPEED}\nDtype: ${DTYPE}\nGenerated videos: ${manifest.videos.length}\nFailures: ${manifest.failures.length}\n`
);
if (manifest.failures.length) {
  console.error(`${manifest.failures.length} narration(s) failed.`);
  process.exitCode = 1;
} else {
  console.log(`Completed ${manifest.videos.length} narration(s).`);
}
