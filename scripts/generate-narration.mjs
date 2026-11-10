import fs from "node:fs/promises";
import path from "node:path";
import crypto from "node:crypto";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { KokoroTTS } from "kokoro-js";

const execFileP = promisify(execFile);
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
const tempRoot = path.join(outDir, "_chunks");
await fs.mkdir(tempRoot, { recursive: true });
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

async function generateChunkToFile(text, label, filename) {
  let last;
  for (let attempt = 1; attempt <= 3; attempt++) {
    try {
      const r = await tts.generate(text, { voice: VOICE, speed: SPEED });
      if (!r || typeof r.save !== "function") {
        throw new Error(`Kokoro returned unsupported audio object: ${r?.constructor?.name || typeof r}`);
      }
      await r.save(filename);
      const st = await fs.stat(filename);
      if (st.size < 1000) throw new Error(`Saved WAV too small: ${st.size} bytes`);
      return;
    } catch (e) {
      last = e;
      console.error(`${label} attempt ${attempt} failed: ${e.message}`);
      try { await fs.rm(filename, { force: true }); } catch {}
      await new Promise(r => setTimeout(r, attempt * 2000));
    }
  }
  throw last;
}

async function probeDuration(filename) {
  const { stdout } = await execFileP("ffprobe", [
    "-v","error","-show_entries","format=duration","-of","default=nw=1:nk=1",filename
  ]);
  return Number(stdout.trim());
}

const manifest = {
  schema_version: "summit-one-kokoro-cloud-v2",
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

for (let vi = 0; vi < queue.length; vi++) {
  const v = queue[vi];
  console.log(`[${vi + 1}/${queue.length}] ${v.video_id} — ${v.title} (${v.chunks.length} chunks)`);
  const workDir = path.join(tempRoot, v.video_id.replace(/[^A-Za-z0-9._-]/g, "_"));
  await fs.mkdir(workDir, { recursive: true });
  const chunkFiles = [];

  for (let ci = 0; ci < v.chunks.length; ci++) {
    const c = v.chunks[ci];
    const chunkPath = path.join(workDir, `chunk-${String(ci + 1).padStart(2, "0")}.wav`);
    console.log(`  chunk ${ci + 1}/${v.chunks.length}: ${c.chunk_id} (${c.word_count} words)`);
    await generateChunkToFile(c.text, c.chunk_id, chunkPath);
    chunkFiles.push(chunkPath);
  }

  const silencePath = path.join(workDir, "silence.wav");
  await execFileP("ffmpeg", [
    "-y","-v","error","-f","lavfi","-i","anullsrc=r=24000:cl=mono",
    "-t",String(GAP_SECONDS),"-c:a","pcm_s16le",silencePath
  ]);

  const concatPath = path.join(workDir, "concat.txt");
  const list = [];
  for (let i = 0; i < chunkFiles.length; i++) {
    list.push(`file '${path.resolve(chunkFiles[i]).replaceAll("'", "'\\''")}'`);
    if (i < chunkFiles.length - 1) {
      list.push(`file '${path.resolve(silencePath).replaceAll("'", "'\\''")}'`);
    }
  }
  await fs.writeFile(concatPath, list.join("\n") + "\n");

  const filename = `${v.video_id}_narration.wav`;
  const finalPath = path.join(outDir, filename);
  await execFileP("ffmpeg", [
    "-y","-v","error","-f","concat","-safe","0","-i",concatPath,
    "-ar","24000","-ac","1","-c:a","pcm_s16le",finalPath
  ]);

  const wav = await fs.readFile(finalPath);
  const sha256 = crypto.createHash("sha256").update(wav).digest("hex");
  const duration = await probeDuration(finalPath);

  manifest.videos.push({
    video_id: v.video_id,
    title: v.title,
    type: v.type,
    source: v.source,
    held_in_iphone_app: Boolean(v.held),
    chunk_count: v.chunks.length,
    word_count: v.word_count,
    duration_seconds: Number(duration.toFixed(3)),
    sample_rate: 24000,
    filename,
    bytes: wav.length,
    sha256
  });

  console.log(`  saved ${filename} — ${duration.toFixed(1)} s — ${(wav.length / 1048576).toFixed(1)} MB`);
  await fs.writeFile(path.join(outDir, "manifest.json"), JSON.stringify(manifest, null, 2));
  await fs.rm(workDir, { recursive: true, force: true });
}

await fs.rm(tempRoot, { recursive: true, force: true });
await fs.writeFile(path.join(outDir, "manifest.json"), JSON.stringify(manifest, null, 2));
console.log(`Completed ${manifest.videos.length} videos from ${queuePath}.`);
