import fs from "node:fs";
import { KokoroTTS } from "kokoro-js";

const MODEL_ID="onnx-community/Kokoro-82M-v1.0-ONNX";
const VOICE=process.env.VOICE||"am_michael";
const SPEED=Number(process.env.SPEED||"0.88");
const OUT=process.env.OUT_FILE||`voice-sample-${VOICE}.wav`;
const TEXT="Choose a representation that exposes the relationship. A line is useful for order, ranks and intervals. When counting objects between two endpoints, distinguish the objects from the gaps separating them.";

function wavBuffer(samples, rate=24000){
  const b=Buffer.alloc(44+samples.length*2);
  b.write("RIFF",0,4,"ascii"); b.writeUInt32LE(36+samples.length*2,4);
  b.write("WAVE",8,4,"ascii"); b.write("fmt ",12,4,"ascii"); b.writeUInt32LE(16,16);
  b.writeUInt16LE(1,20); b.writeUInt16LE(1,22); b.writeUInt32LE(rate,24); b.writeUInt32LE(rate*2,28);
  b.writeUInt16LE(2,32); b.writeUInt16LE(16,34); b.write("data",36,4,"ascii"); b.writeUInt32LE(samples.length*2,40);
  let o=44; for(const s of samples){const x=Math.max(-1,Math.min(1,s)); b.writeInt16LE(Math.round(x<0?x*32768:x*32767),o); o+=2}
  return b;
}
const tts=await KokoroTTS.from_pretrained(MODEL_ID,{dtype:"q8",device:"cpu"});
const r=await tts.generate(TEXT,{voice:VOICE,speed:SPEED});
const samples=r.audio??r.data;
if(!samples?.length) throw new Error("No waveform");
fs.writeFileSync(OUT,wavBuffer(samples instanceof Float32Array?samples:Float32Array.from(samples),r.sampling_rate||24000));
console.log(JSON.stringify({voice:VOICE,speed:SPEED,duration_seconds:samples.length/(r.sampling_rate||24000),out:OUT}));
