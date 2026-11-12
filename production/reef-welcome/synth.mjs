import fs from "node:fs";
import path from "node:path";
import { KokoroTTS } from "kokoro-js";
import { phonemize } from "./kokoro-phonemize.mjs";

const INPUT = process.argv[2] ?? "production/t021/narration.json";
const OUT = process.argv[3] ?? "build/t021";
const doc = JSON.parse(fs.readFileSync(INPUT, "utf8"));
const voice = doc.voice || "af_heart";
const speed = Number(doc.speed || 1.02);

fs.mkdirSync(OUT,{recursive:true});
const tts=await KokoroTTS.from_pretrained("onnx-community/Kokoro-82M-v1.0-ONNX",{dtype:"q8",device:"cpu"});
const RATE=24000;
function asWav(samples,rate=RATE){
  const b=Buffer.alloc(44+samples.length*2);
  b.write('RIFF',0);b.writeUInt32LE(36+samples.length*2,4);b.write('WAVE',8);b.write('fmt ',12);b.writeUInt32LE(16,16);b.writeUInt16LE(1,20);b.writeUInt16LE(1,22);b.writeUInt32LE(rate,24);b.writeUInt32LE(rate*2,28);b.writeUInt16LE(2,32);b.writeUInt16LE(16,34);b.write('data',36);b.writeUInt32LE(samples.length*2,40);
  for(let i=0;i<samples.length;i++){const v=Math.max(-1,Math.min(1,samples[i]));b.writeInt16LE(Math.round(v<0?v*32768:v*32767),44+i*2)}return b;
}
function trimSilence(arr){
  // Keep breathing space around phrases. Remove only model padding, not natural within-sentence pauses.
  const window=Math.round(RATE*.008),threshold=.0017;
  const active=k=>{const stop=Math.min(arr.length,k+window);let acc=0;for(let j=k;j<stop;j++)acc+=arr[j]*arr[j];return Math.sqrt(acc/(stop-k||1))>threshold};
  let start=0,end=arr.length;
  while(start<arr.length-window&&!active(start))start+=window;
  while(end>start+window&&!active(end-window))end-=window;
  start=Math.max(0,start-Math.round(RATE*.08));end=Math.min(arr.length,end+Math.round(RATE*.14));
  return arr.subarray(start,end);
}
const chunks=[];const timings=[];const pronunciation=[];let cursor=0;
async function synthesise(speech,index){
  if(!/\bMAWA(?:'s)?\b/.test(speech))return tts.generate(speech,{voice,speed});
  const parts=speech.split(/(\bMAWA(?:'s)?\b)/g),phones=[];
  for(const part of parts){
    if(!part)continue;
    if(/^MAWA/.test(part)){
      const p="mˈɑːwə"+(part.endsWith("'s")?"z":"");
      phones.push(p);pronunciation.push({segment:index+1,word:part,phonemes:p,spoken_as:"one two-syllable word"});
    }else phones.push(await phonemize(part,'b'));
  }
  const phonemes=phones.join(' ').replace(/ +([,.;!?])/g,'$1');
  const {input_ids}=tts.tokenizer(phonemes,{truncation:false});
  if(input_ids.dims.at(-1)>510)throw Error('Narration chunk exceeds safe phoneme length');
  return tts.generate_from_ids(input_ids,{voice,speed});
}
for(let i=0;i<doc.segments.length;i++){
  const speech=doc.segments[i];
  console.log(`[${i+1}/${doc.segments.length}] Generating coherent speech chunk: ${speech.length} characters`);
  const res=await synthesise(speech,i);
  if((res.sampling_rate??RATE)!==RATE)throw new Error('Unexpected Kokoro sample rate');
  const wav=res.audio??res.data;
  if(!wav?.length)throw new Error(`Kokoro returned empty waveform for segment ${i+1}`);
  const audio=trimSilence(wav instanceof Float32Array?wav:Float32Array.from(wav));
  const seconds=audio.length/RATE;
  // Narrative breathing depends on syntax and a conceptual beat, not a uniform fixed silence.
  const pause=i===doc.segments.length-1?0:(doc.pause_seconds?.[i]??.4);
  timings.push({index:i+1,text:speech,start_seconds:+cursor.toFixed(4),duration_seconds:+seconds.toFixed(4),pause_after:pause});
  chunks.push(audio);
  if(pause>0)chunks.push(new Float32Array(Math.round(RATE*pause)));
  fs.writeFileSync(path.join(OUT,`speech-${String(i+1).padStart(2,'0')}.wav`),asWav(audio));
  cursor+=seconds+pause;
}
if(pronunciation.length!==2)throw Error('Expected both MAWA occurrences to use the word pronunciation');
fs.writeFileSync(path.join(OUT,'pronunciation-qa.json'),JSON.stringify({voice,entries:pronunciation},null,2));
const combined=new Float32Array(chunks.reduce((n,a)=>n+a.length,0));
let offset=0;for(const c of chunks){combined.set(c,offset);offset+=c.length}
fs.writeFileSync(path.join(OUT,'narration.wav'),asWav(combined));
fs.writeFileSync(path.join(OUT,'timing.json'),JSON.stringify({id:doc.id,title:doc.title,voice,speed,duration_seconds:combined.length/RATE,segments:timings},null,2));
console.log(`DONE ${doc.id}: ${timings.length} continuous narration phrases, ${ (combined.length/RATE).toFixed(2)}s, ${voice} @ ${speed} speed.`);
