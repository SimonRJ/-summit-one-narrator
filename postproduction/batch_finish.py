#!/usr/bin/env python3
import argparse, csv, json, os, re, subprocess, sys
from pathlib import Path

def video_id_from_name(name):
    stem=Path(name).stem
    m=re.match(r'^(T\d{2}[.-][123E]|K\d{3}|N[1-4][.-](?:26|27|28|29|30)|A\d{3})',stem,re.I)
    if not m:return None
    s=m.group(1).upper().replace('-', '.') if m.group(1).upper().startswith(('T','N')) else m.group(1).upper()
    return s

def index_files(root,exts):
    out={}
    for p in Path(root).rglob('*'):
        if p.is_file() and p.suffix.lower() in exts:
            vid=video_id_from_name(p.name)
            if vid: out.setdefault(vid,[]).append(p)
    return out

def pick(paths,prefer=None):
    if not paths:return None
    if prefer:
        for p in paths:
            if prefer.lower() in p.name.lower():return p
    return sorted(paths,key=lambda p:(len(p.name),p.name))[0]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--visual-root',required=True)
    ap.add_argument('--audio-root',required=True)
    ap.add_argument('--registry',required=True)
    ap.add_argument('--out-root',required=True)
    ap.add_argument('--finish-script',default=str(Path(__file__).with_name('finish_video.py')))
    ap.add_argument('--overrides',help='JSON map video_id -> visual path')
    ap.add_argument('--ids',nargs='*')
    ap.add_argument('--force',action='store_true')
    ap.add_argument('--force-extreme-retime',action='store_true')
    args=ap.parse_args()
    visuals=index_files(args.visual_root,{'.mp4','.mov','.m4v'})
    audio=index_files(args.audio_root,{'.wav','.mp3','.m4a','.aac','.flac'})
    overrides=json.load(open(args.overrides)) if args.overrides else {}
    ids=set(args.ids or audio.keys())
    rows=[]; failures=[]
    outroot=Path(args.out_root);outroot.mkdir(parents=True,exist_ok=True)
    for i,vid in enumerate(sorted(ids),1):
        a=pick(audio.get(vid),prefer='.wav')
        v=Path(overrides[vid]) if vid in overrides else pick(visuals.get(vid),prefer='visual_master')
        row={'video_id':vid,'audio':str(a) if a else None,'visual':str(v) if v else None}
        if not a or not v or not v.exists():
            row.update(status='missing-input'); failures.append(row); rows.append(row); continue
        target=outroot/vid
        qa=target/f'{vid}.qa.json'
        if qa.exists() and not args.force:
            data=json.load(open(qa)); row.update(status='existing',**{k:data.get(k) for k in ('retime_action','retime_percent','final_duration_seconds','passed_integrity','requires_manual_review')}); rows.append(row); continue
        cmd=[sys.executable,args.finish_script,'--video-id',vid,'--visual',str(v),'--audio',str(a),'--registry',args.registry,'--out-dir',str(target)]
        if args.force_extreme_retime:cmd.append('--force-extreme-retime')
        print(f'[{i}/{len(ids)}] {vid}',flush=True)
        p=subprocess.run(cmd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        if p.returncode:
            row.update(status='failed',error=p.stdout[-3000:]);failures.append(row)
        else:
            data=json.load(open(qa));row.update(status='complete',**{k:data.get(k) for k in ('retime_action','retime_percent','final_duration_seconds','passed_integrity','requires_manual_review')})
        rows.append(row)
    with open(outroot/'FINAL_VIDEO_QA.csv','w',newline='',encoding='utf-8') as f:
        cols=['video_id','status','retime_action','retime_percent','final_duration_seconds','passed_integrity','requires_manual_review','visual','audio','error']
        w=csv.DictWriter(f,fieldnames=cols,extrasaction='ignore');w.writeheader();w.writerows(rows)
    summary={'requested':len(ids),'complete':sum(r['status'] in ('complete','existing') and r.get('passed_integrity',True) for r in rows),'failures':len(failures),'manual_review':sum(bool(r.get('requires_manual_review')) for r in rows),'missing_inputs':[r['video_id'] for r in rows if r['status']=='missing-input'],'failed_ids':[r['video_id'] for r in rows if r['status']=='failed']}
    json.dump(summary,open(outroot/'FINAL_VIDEO_SUMMARY.json','w'),indent=2)
    print(json.dumps(summary,indent=2))
    if failures:sys.exit(2)
if __name__=='__main__':main()