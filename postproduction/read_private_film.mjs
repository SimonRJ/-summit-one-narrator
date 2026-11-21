import {createHash} from 'node:crypto';

const digest = bytes => createHash('sha256').update(bytes).digest('hex');
const challengeId = /^(?:A\d{3}|K\d{3}|N[1-4]\.(?:26|27|28|29|30))$/;

export function assemblePrivateFilm(parts, expectedHash){
  if(!/^[a-f0-9]{64}$/.test(expectedHash)) throw Error('Invalid expected media hash.');
  if(!parts.length || parts.length>512) throw Error('Incomplete staged film.');
  const decoded = parts.map((row,index)=>{
    if(row.part_number!==index || row.part_count!==parts.length ||
       typeof row.bytes!=='string' || !/^\\x(?:[a-f0-9]{2})+$/.test(row.bytes) ||
       row.bytes.length>2+2*98304) throw Error('Missing or invalid staged film part.');
    return Buffer.from(row.bytes.slice(2),'hex');
  });
  const film = Buffer.concat(decoded);
  if(digest(film)!==expectedHash) throw Error('Staged media does not match the reviewed export.');
  return film;
}

export async function importPrivateFilm(client,bucket,filmId,mediaHash){
  if(!challengeId.test(filmId) || !/^[a-f0-9]{64}$/.test(mediaHash)) throw Error('Invalid film reference.');
  const source=()=>client.from('protected_film_parts');
  const parts=[];
  for(let from=0;from<512;from+=4){
    const {data,error}=await source().select('part_number,part_count,bytes')
      .eq('film_id',filmId).eq('media_sha256',mediaHash).order('part_number').range(from,from+3);
    if(error) throw Error('Unable to read private production data.');
    parts.push(...data);
    if(data.length<4 || parts.length===parts[0]?.part_count) break;
  }
  const name=filmId+'.mp4', storage=client.storage.from(bucket);
  // A retry after a completed transfer needs only the readback check.
  if(parts.length){
    const film=assemblePrivateFilm(parts,mediaHash);
    await storage.upload(name,film,{contentType:'video/mp4',cacheControl:'3600',upsert:false});
  }
  const readback=await storage.download(name);
  if(readback.error || !readback.data) throw Error('Private storage readback failed. Source retained.');
  const remote=Buffer.from(await readback.data.arrayBuffer());
  if(digest(remote)!==mediaHash) throw Error('Private storage contains a different edition. Source retained.');
  const {error}=await source().delete().eq('film_id',filmId).eq('media_sha256',mediaHash);
  if(error) throw Error('Verified media stored. Removing its staged copy needs a retry.');
  console.log(`Private media verified for ${filmId} (${remote.length} bytes).`);
}
