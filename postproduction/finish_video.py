#!/usr/bin/env python3
import argparse, json, math, os, re, subprocess, hashlib, shlex, sys
from pathlib import Path


def run(cmd, capture=True, check=True):
    p=subprocess.run(cmd,stdout=subprocess.PIPE if capture else None,stderr=subprocess.PIPE if capture else None,text=True)
    if check and p.returncode!=0:
        raise RuntimeError(f"command failed ({p.returncode}): {' '.join(map(str,cmd))}\n{(p.stderr or '')[-4000:]}")
    return p

def ffprobe(path):
    p=run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)])
    return json.loads(p.stdout)

def duration(info):
    try:return float(info['format']['duration'])
    except:return 0.0

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

def fmt_vtt(t):
    t=max(0,float(t)); h=int(t//3600); t-=h*3600; m=int(t//60); s=t-m*60
    return f"{h:02d}:{m:02d}:{s:06.3f}"

def estimate_words(text,dur):
    words=text.split()
    if not words:return []
    weights=[]
    for w in words:
        clean=re.sub(r'[^A-Za-z0-9]+','',w)
        weights.append(max(0.65, min(2.5, len(clean or w)**0.55)))
    total=sum(weights); t=0.0; out=[]
    for w,wt in zip(words,weights):
        d=dur*wt/total
        out.append({'text':w,'start':t,'end':t+d,'estimated':True})
        t+=d
    out[-1]['end']=dur
    return out

def scaled_words(item,audio_d):
    wt=item.get('wordTimings') or []
    if wt and float(wt[-1].get('end') or 0)>0:
        base=float(wt[-1]['end']); scale=audio_d/base
        return [dict(w, start=float(w['start'])*scale, end=float(w['end'])*scale, estimated=w.get('estimated',False) or abs(scale-1)>0.005) for w in wt], 'scaled-registry-word-timing', scale
    return estimate_words(item.get('transcript') or '',audio_d), 'duration-weighted-estimate', None

def cues_from_words(words):
    cues=[]; cur=[]; start=None
    for i,w in enumerate(words):
        if start is None:start=w['start']
        cur.append(w)
        text=' '.join(x['text'] for x in cur)
        elapsed=w['end']-start
        punct=bool(re.search(r'[.!?][\"”’\']?$',w['text']))
        if (punct and len(cur)>=4) or len(cur)>=9 or elapsed>=3.4 or i==len(words)-1:
            cues.append((start,w['end'],text)); cur=[]; start=None
    return cues

def write_vtt(path,words):
    cues=cues_from_words(words)
    with open(path,'w',encoding='utf-8') as f:
        f.write('WEBVTT\n\n')
        for i,(a,b,text) in enumerate(cues,1):
            f.write(f"{i}\n{fmt_vtt(a)} --> {fmt_vtt(max(b,a+0.08))}\n{text}\n\n")
    return len(cues)

def audio_level(path):
    p=run(['ffmpeg','-hide_banner','-nostats','-i',str(path),'-af','volumedetect','-f','null','-'],check=False)
    s=(p.stderr or '')
    m=re.search(r'mean_volume:\s*(-?inf|[-0-9.]+) dB',s)
    return None if not m else (-999.0 if m.group(1)=='-inf' else float(m.group(1)))

def find_item(registry,video_id):
    vids=registry.get('videos',[])
    for v in vids:
        if v.get('id')==video_id or v.get('video_id')==video_id:return v
    raise KeyError(video_id)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--video-id',required=True)
    ap.add_argument('--visual',required=True)
    ap.add_argument('--audio',required=True)
    ap.add_argument('--registry',required=True)
    ap.add_argument('--out-dir',required=True)
    ap.add_argument('--force-extreme-retime',action='store_true')
    args=ap.parse_args()
    out=Path(args.out_dir);out.mkdir(parents=True,exist_ok=True)
    registry=json.load(open(args.registry,encoding='utf-8')); item=find_item(registry,args.video_id)
    vi=ffprobe(args.visual); ai=ffprobe(args.audio); vd=duration(vi); ad=duration(ai)
    if vd<=0 or ad<=0:raise RuntimeError(f'invalid duration visual={vd} audio={ad}')
    ratio=ad/vd; deviation=abs(ratio-1)
    if deviation<=0.012: action='preserve_timing'
    elif 0.80<=ratio<=1.25: action='linear_retime'
    else:
        action='extreme_retime_review'
        if not args.force_extreme_retime: raise RuntimeError(f'retime ratio {ratio:.4f} outside automatic safety range 0.80–1.25')
    words, timing_method, timing_scale=scaled_words(item,ad)
    vtt=out/f'{args.video_id}.vtt'; cue_count=write_vtt(vtt,words)
    final=out/f'{args.video_id}.mp4'
    if action=='preserve_timing': vf='tpad=stop_mode=clone:stop_duration=0.35'
    else: vf=f'setpts={ratio:.10f}*PTS,tpad=stop_mode=clone:stop_duration=0.35'
    cmd=['ffmpeg','-y','-hide_banner','-loglevel','error','-i',args.visual,'-i',args.audio,
         '-map','0:v:0','-map','1:a:0','-vf',vf,
         '-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p',
         '-c:a','aac','-b:a','160k','-ar','48000','-ac','1','-movflags','+faststart','-shortest',str(final)]
    run(cmd)
    fi=ffprobe(final); fd=duration(fi)
    streams=fi.get('streams',[]); vs=next((s for s in streams if s.get('codec_type')=='video'),{}); aus=next((s for s in streams if s.get('codec_type')=='audio'),{})
    mean_db=audio_level(final)
    delta=fd-ad
    qa={
      'schema_version':'summit-one-final-video-qa-v1','video_id':args.video_id,
      'visual_source':str(args.visual),'audio_source':str(args.audio),'final_file':final.name,
      'visual_duration_seconds':round(vd,3),'audio_duration_seconds':round(ad,3),'final_duration_seconds':round(fd,3),
      'audio_visual_ratio':round(ratio,6),'retime_action':action,'retime_percent':round((ratio-1)*100,3),
      'final_audio_delta_seconds':round(delta,3),'caption_timing_method':timing_method,'caption_scale':timing_scale,
      'word_count':len(words),'caption_cues':cue_count,
      'video_codec':vs.get('codec_name'),'width':vs.get('width'),'height':vs.get('height'),'pix_fmt':vs.get('pix_fmt'),
      'audio_codec':aus.get('codec_name'),'audio_sample_rate':aus.get('sample_rate'),'audio_channels':aus.get('channels'),
      'mean_volume_db':mean_db,'sha256':sha256(final),
      'passes_duration_sync':abs(delta)<=0.20,'passes_video_codec':vs.get('codec_name')=='h264',
      'passes_audio':aus.get('codec_name')=='aac' and mean_db is not None and mean_db>-60,
      'requires_manual_review':action=='extreme_retime_review' or abs((ratio-1)*100)>12
    }
    qa['passed_integrity']=qa['passes_duration_sync'] and qa['passes_video_codec'] and qa['passes_audio']
    json.dump(qa,open(out/f'{args.video_id}.qa.json','w'),indent=2)
    print(json.dumps(qa,indent=2))
    if not qa['passed_integrity']: sys.exit(2)
if __name__=='__main__':main()