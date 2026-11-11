import fs from 'node:fs';
import path from 'node:path';
import { createClient } from '@supabase/supabase-js';

const root=process.argv[2];
if(!root) throw new Error('Usage: node upload_protected_media.mjs <protected_amc_dir>');
const url=process.env.SUPABASE_URL, key=process.env.SUPABASE_SERVICE_ROLE_KEY;
if(!url||!key) throw new Error('SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are required');
const bucket=process.env.PROTECTED_VIDEO_BUCKET||'summit-one-protected-video';
const ids=fs.readdirSync(root).filter(f=>f.endsWith('.mp4')).map(f=>f.replace(/\.mp4$/,''));
if(!ids.length) throw new Error('No protected AMC MP4s found');
for(const id of ids){if(!/^A\d{3}$/.test(id))throw new Error(`SAFETY: non-AMC file in protected upload set: ${id}`)}
const sb=createClient(url,key,{auth:{persistSession:false,autoRefreshToken:false}});
let ok=0;
for(const id of ids.sort()){
  const p=path.join(root,`${id}.mp4`), bytes=fs.readFileSync(p);
  const {error}=await sb.storage.from(bucket).upload(`${id}.mp4`,bytes,{contentType:'video/mp4',upsert:true,cacheControl:'3600'});
  if(error)throw new Error(`${id}: ${error.message}`);
  ok++; console.log(`Uploaded ${id} (${bytes.length} bytes)`);
}
console.log(JSON.stringify({bucket,uploaded:ok,ids},null,2));