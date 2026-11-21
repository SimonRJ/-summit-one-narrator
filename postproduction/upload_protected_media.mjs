import fs from 'node:fs';
import path from 'node:path';
import {importPrivateFilm} from './read_private_film.mjs';
import { createClient } from '@supabase/supabase-js';

const root=process.argv[2];
if(!root) throw new Error('Usage: node upload_protected_media.mjs <protected_challenge_dir>');
const url=process.env.SUPABASE_URL, key=process.env.SUPABASE_SERVICE_ROLE_KEY;
if(!url||!key) throw new Error('SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are required');
const bucket=process.env.PROTECTED_VIDEO_BUCKET||'summit-one-protected-video';
const sb=createClient(url,key,{auth:{persistSession:false,autoRefreshToken:false}});
const {data:destination,error:bucketError}=await sb.storage.getBucket(bucket);
if(bucketError || !destination || destination.public)throw new Error('A private destination bucket is required.');
if(root==='--staged'){
  await importPrivateFilm(sb,bucket,process.argv[3]||'',process.argv[4]||'');
  process.exit(0);
}
const ids=fs.readdirSync(root).filter(f=>f.endsWith('.mp4')).map(f=>f.replace(/\.mp4$/,''));
if(!ids.length) throw new Error('No protected challenge MP4s found');
const challengeId = /^(?:A\d{3}|K\d{3}|N[1-4]\.(?:26|27|28|29|30))$/;
for(const id of ids){
  if(!challengeId.test(id))throw new Error(`Unrecognised protected challenge: ${id}`);
}
let ok=0;
for(const id of ids.sort()){
  const p=path.join(root,`${id}.mp4`), bytes=fs.readFileSync(p);
  const {error}=await sb.storage.from(bucket).upload(`${id}.mp4`,bytes,{contentType:'video/mp4',upsert:true,cacheControl:'3600'});
  if(error)throw new Error(`${id}: ${error.message}`);
  ok++; console.log(`Uploaded ${id} (${bytes.length} bytes)`);
}
console.log(JSON.stringify({bucket,uploaded:ok,ids},null,2));