#!/usr/bin/env python3
import argparse, concurrent.futures as cf, hashlib, json, os, re, shutil, subprocess, sys
from pathlib import Path

PROTECTED_RE=re.compile(r'^(?:A\d{3}|K\d{3}|N[1-4]\.(?:26|27|28|29|30))$')

def run(cmd):
    p=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    if p.returncode: raise RuntimeError(p.stderr[-4000:])
    return p.stdout

def probe(p):
    return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))

def sha256(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

def duration(info): return float(info['format']['duration'])

def encode_one(src,outdir,crf,preset):
    vid=src.stem
    dst=outdir/f'{vid}.mp4'; tmp=outdir/f'.{vid}.tmp.mp4'
    outdir.mkdir(parents=True,exist_ok=True)
    # Never upscale. A001's 1080p approved visual gets a 720p delivery copy; archived master stays 1080p.
    vf="scale=w='min(iw,1280)':h='min(ih,720)':force_original_aspect_ratio=decrease:force_divisible_by=2"
    run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(src),'-map','0:v:0','-map','0:a:0',
         '-vf',vf,'-c:v','libx264','-preset',preset,'-crf',str(crf),'-pix_fmt','yuv420p',
         '-c:a','aac','-b:a','96k','-ar','48000','-ac','1','-movflags','+faststart',str(tmp)])
    os.replace(tmp,dst)
    a,b=probe(src),probe(dst)
    vs=[s for s in b['streams'] if s['codec_type']=='video']; aud=[s for s in b['streams'] if s['codec_type']=='audio']
    if not vs or vs[0].get('codec_name')!='h264': raise RuntimeError(f'{vid}: delivery video is not H.264')
    if not aud or aud[0].get('codec_name')!='aac': raise RuntimeError(f'{vid}: delivery audio is not AAC')
    if int(vs[0].get('width',9999))>1280 or int(vs[0].get('height',9999))>720: raise RuntimeError(f'{vid}: delivery resolution too large')
    delta=abs(duration(a)-duration(b))
    if delta>0.25: raise RuntimeError(f'{vid}: duration changed by {delta:.3f}s')
    q={'video_id':vid,'source_bytes':src.stat().st_size,'delivery_bytes':dst.stat().st_size,
       'compression_ratio':round(dst.stat().st_size/src.stat().st_size,4),'duration_delta_seconds':round(delta,4),
       'width':int(vs[0]['width']),'height':int(vs[0]['height']),'video_codec':'h264','audio_codec':'aac',
       'crf':crf,'preset':preset,'audio_bitrate_kbps':96,'sha256':sha256(dst),'passed':True}
    (outdir/f'{vid}.delivery.qa.json').write_text(json.dumps(q,indent=2))
    return q

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--final-root',required=True)
    ap.add_argument('--out-root',required=True)
    ap.add_argument('--workers',type=int,default=4)
    ap.add_argument('--crf',type=float,default=23)
    ap.add_argument('--preset',default='veryfast')
    ap.add_argument('--max-total-mib',type=float,default=900)
    a=ap.parse_args()
    root=Path(a.final_root); out=Path(a.out_root)
    out.mkdir(parents=True,exist_ok=True)
    files=[]
    for p in root.glob('*/*.mp4'):
        if PROTECTED_RE.fullmatch(p.stem): files.append(p)
    if len(files)!=194: raise SystemExit(f'Expected 194 protected challenge finals, found {len(files)}')
    results=[]; failures=[]
    with cf.ThreadPoolExecutor(max_workers=max(1,a.workers)) as ex:
        fut={ex.submit(encode_one,p,out,a.crf,a.preset):p.stem for p in files}
        for i,f in enumerate(cf.as_completed(fut),1):
            vid=fut[f]
            try:
                q=f.result();results.append(q);print(f'PROGRESS {i}/194 {vid} ratio={q["compression_ratio"]}',flush=True)
            except Exception as e:
                failures.append({'video_id':vid,'error':str(e)});print(f'FAILED {vid}: {e}',flush=True)
    total=sum(x['delivery_bytes'] for x in results); max_bytes=int(a.max_total_mib*1024*1024)
    summary={'expected':194,'completed':len(results),'failed':failures,'total_bytes':total,'total_mib':round(total/1024/1024,2),
             'max_total_mib':a.max_total_mib,'within_storage_safety_ceiling':total<=max_bytes,
             'average_compression_ratio':round(sum(x['compression_ratio'] for x in results)/len(results),4) if results else None,
             'crf':a.crf,'preset':a.preset,'audio_bitrate_kbps':96}
    (out/'PROTECTED_DELIVERY_SUMMARY.json').write_text(json.dumps(summary,indent=2))
    (out/'PROTECTED_DELIVERY_MANIFEST.json').write_text(json.dumps({'schema_version':'summit-one-protected-delivery-v1','items':sorted(results,key=lambda x:x['video_id'])},indent=2))
    print(json.dumps(summary,indent=2))
    if failures or len(results)!=194 or total>max_bytes: raise SystemExit(1)

if __name__=='__main__': main()