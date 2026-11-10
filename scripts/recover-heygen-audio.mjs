import fs from "node:fs/promises";
import path from "node:path";
import crypto from "node:crypto";

const src=process.argv[2]||"heygen-89-audio-manifest.json";
const outDir=process.argv[3]||"heygen-audio";
await fs.mkdir(outDir,{recursive:true});
const data=JSON.parse(await fs.readFile(src,"utf8"));
const results=[];

async function fetchWithRetry(url,label){
  let last;
  for(let i=1;i<=4;i++){
    try{
      const r=await fetch(url,{redirect:"follow",headers:{"User-Agent":"SummitOneNarrationRecovery/1.0"}});
      if(!r.ok) throw new Error(`HTTP ${r.status} ${r.statusText}`);
      const ab=await r.arrayBuffer();
      if(ab.byteLength<1000) throw new Error(`Unexpectedly small response: ${ab.byteLength} bytes`);
      return Buffer.from(ab);
    }catch(e){
      last=e;
      console.error(`${label} attempt ${i} failed: ${e.message}`);
      await new Promise(r=>setTimeout(r,i*2500));
    }
  }
  throw last;
}

for(let i=0;i<data.items.length;i++){
  const x=data.items[i];
  console.log(`[${i+1}/${data.items.length}] ${x.video_id} — ${x.title}`);
  try{
    const buf=await fetchWithRetry(x.audio_url,x.video_id);
    const file=`${x.video_id}_narration.wav`;
    await fs.writeFile(path.join(outDir,file),buf);
    results.push({
      ...x,
      file,
      bytes:buf.length,
      sha256:crypto.createHash("sha256").update(buf).digest("hex"),
      recovered:true
    });
    console.log(`  saved ${file} ${(buf.length/1048576).toFixed(2)} MB`);
  }catch(e){
    results.push({...x,recovered:false,error:e.message});
    console.error(`  FAILED ${x.video_id}: ${e.message}`);
  }
  await fs.writeFile(path.join(outDir,"recovery-manifest.json"),JSON.stringify({count:results.length,results},null,2));
}

const failed=results.filter(x=>!x.recovered);
console.log(`Recovered ${results.length-failed.length}/${results.length}`);
if(failed.length){
  console.error("Failed IDs:",failed.map(x=>x.video_id).join(", "));
  process.exitCode=2;
}
