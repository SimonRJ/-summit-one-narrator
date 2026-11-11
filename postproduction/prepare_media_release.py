#!/usr/bin/env python3
import argparse, csv, hashlib, json, os, re, shutil, sys
from pathlib import Path

PUBLIC_PATTERNS=(re.compile(r'^T\d{2}\.(?:1|2|3|E)

def classify(vid):
    if any(p.fullmatch(vid) for p in PROTECTED_PATTERNS): return 'protected_challenge'
    if any(p.fullmatch(vid) for p in PUBLIC_PATTERNS): return 'public_safe'
    return 'unknown'

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

def link_or_copy(src,dst):
    dst.parent.mkdir(parents=True,exist_ok=True)
    if dst.exists(): dst.unlink()
    try: os.link(src,dst)
    except OSError: shutil.copy2(src,dst)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--final-root',required=True)
    ap.add_argument('--out-root',required=True)
    ap.add_argument('--release-tag',default='summit-one-video-v1')
    ap.add_argument('--repo',default='SimonRJ/-summit-one-narrator')
    ap.add_argument('--expected-total',type=int,default=None)
    args=ap.parse_args()
    root=Path(args.final_root); out=Path(args.out_root)
    pub=out/'public_release'; prot=out/'protected_challenge'
    if out.exists(): shutil.rmtree(out)
    pub.mkdir(parents=True); prot.mkdir(parents=True)
    rows=[]; unknown=[]
    for qa in sorted(root.rglob('*.qa.json')):
        vid=qa.name[:-8]
        cls=classify(vid)
        if cls=='unknown': unknown.append(vid); continue
        mp4=qa.with_name(f'{vid}.mp4')
        if not mp4.exists():
            alt=qa.with_name(f'{vid}_final.mp4')
            if alt.exists(): mp4=alt
            else: raise SystemExit(f'Missing final MP4 for {vid}')
        vtt=qa.with_name(f'{vid}.vtt')
        q=json.load(open(qa,encoding='utf-8'))
        checks={
            'passed_integrity':bool(q.get('passed_integrity')),
            'passes_duration_sync':bool(q.get('passes_duration_sync')),
            'passes_video_codec':bool(q.get('passes_video_codec')),
            'passes_audio':bool(q.get('passes_audio')),
        }
        if not all(checks.values()): raise SystemExit(f'QA failed for {vid}: {checks}')
        if q.get('requires_manual_review'):
            raise SystemExit(f'Manual review required before release: {vid}')
        destdir=pub if cls=='public_safe' else prot
        destmp4=destdir/f'{vid}.mp4'
        link_or_copy(mp4,destmp4)
        if vtt.exists(): link_or_copy(vtt,destdir/f'{vid}.vtt')
        digest=sha256(destmp4)
        (destdir/f'{vid}.sha256').write_text(f'{digest}  {vid}.mp4\n',encoding='utf-8')
        url=(f'https://github.com/{args.repo}/releases/download/{args.release_tag}/{vid}.mp4' if cls=='public_safe' else None)
        rows.append({
            'video_id':vid,'media_class':cls,'mp4':destmp4.name,'sha256':digest,
            'duration_seconds':q.get('final_duration_seconds'),
            'video_url':url,'release_tag':args.release_tag if url else None,
            'protected':cls=='protected_challenge'
        })
    if unknown: raise SystemExit('Unknown video IDs: '+', '.join(unknown))
    ids=[r['video_id'] for r in rows]
    if len(ids)!=len(set(ids)): raise SystemExit('Duplicate final video IDs')
    if args.expected_total is not None and len(ids)!=args.expected_total:
        raise SystemExit(f'Expected {args.expected_total} finals, found {len(ids)}')
    public=[r for r in rows if r['media_class']=='public_safe']
    protected=[r for r in rows if r['media_class']=='protected_amc']
    app={r['video_id']:{
        'video_id':r['video_id'],
        'media_access':'public_release' if not r['protected'] else 'protected_authenticated',
        'video_url':r['video_url'],
        'sha256':r['sha256'],
        'duration_seconds':r['duration_seconds']
    } for r in rows}
    (out/'PUBLIC_RELEASE_MANIFEST.json').write_text(json.dumps({'schema_version':'summit-one-public-video-release-v1','count':len(public),'items':public},indent=2),encoding='utf-8')
    (out/'PROTECTED_AMC_MANIFEST.json').write_text(json.dumps({'schema_version':'summit-one-protected-challenge-media-v1','count':len(protected),'items':protected},indent=2),encoding='utf-8')
    (out/'APP_MEDIA_REGISTRY.json').write_text(json.dumps({'schema_version':'summit-one-app-media-v1','count':len(rows),'by_id':app},indent=2),encoding='utf-8')
    with open(out/'MEDIA_PACKAGE_QA.csv','w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=['video_id','media_class','duration_seconds','sha256','video_url']);w.writeheader();w.writerows([{k:r.get(k) for k in w.fieldnames} for r in rows])
    (out/'PUBLIC_RELEASE_FILES.txt').write_text('\n'.join(sorted(p.name for p in pub.iterdir() if p.is_file()))+'\n',encoding='utf-8')
    summary={
        'total_final_videos':len(rows),'public_safe':len(public),'protected_challenge':len(protected),
        'unknown':0,'duplicates':0,'public_contains_challenge':any(any(p.fullmatch(r['video_id']) for p in PROTECTED_PATTERNS) for r in public),
        'release_tag':args.release_tag
    }
    if summary['public_contains_challenge']: raise SystemExit('SAFETY FAILURE: challenge media entered public bundle')
    (out/'MEDIA_PACKAGE_SUMMARY.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps(summary,indent=2))

if __name__=='__main__': main()),)
PROTECTED_PATTERNS=(
    re.compile(r'^A\d{3}

def classify(vid):
    if PROTECTED_PATTERN.fullmatch(vid): return 'protected_amc'
    if any(p.fullmatch(vid) for p in PUBLIC_PATTERNS): return 'public_safe'
    return 'unknown'

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

def link_or_copy(src,dst):
    dst.parent.mkdir(parents=True,exist_ok=True)
    if dst.exists(): dst.unlink()
    try: os.link(src,dst)
    except OSError: shutil.copy2(src,dst)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--final-root',required=True)
    ap.add_argument('--out-root',required=True)
    ap.add_argument('--release-tag',default='summit-one-video-v1')
    ap.add_argument('--repo',default='SimonRJ/-summit-one-narrator')
    ap.add_argument('--expected-total',type=int,default=None)
    args=ap.parse_args()
    root=Path(args.final_root); out=Path(args.out_root)
    pub=out/'public_release'; prot=out/'protected_amc'
    if out.exists(): shutil.rmtree(out)
    pub.mkdir(parents=True); prot.mkdir(parents=True)
    rows=[]; unknown=[]
    for qa in sorted(root.rglob('*.qa.json')):
        vid=qa.name[:-8]
        cls=classify(vid)
        if cls=='unknown': unknown.append(vid); continue
        mp4=qa.with_name(f'{vid}.mp4')
        if not mp4.exists():
            alt=qa.with_name(f'{vid}_final.mp4')
            if alt.exists(): mp4=alt
            else: raise SystemExit(f'Missing final MP4 for {vid}')
        vtt=qa.with_name(f'{vid}.vtt')
        q=json.load(open(qa,encoding='utf-8'))
        checks={
            'passed_integrity':bool(q.get('passed_integrity')),
            'passes_duration_sync':bool(q.get('passes_duration_sync')),
            'passes_video_codec':bool(q.get('passes_video_codec')),
            'passes_audio':bool(q.get('passes_audio')),
        }
        if not all(checks.values()): raise SystemExit(f'QA failed for {vid}: {checks}')
        if q.get('requires_manual_review'):
            raise SystemExit(f'Manual review required before release: {vid}')
        destdir=pub if cls=='public_safe' else prot
        destmp4=destdir/f'{vid}.mp4'
        link_or_copy(mp4,destmp4)
        if vtt.exists(): link_or_copy(vtt,destdir/f'{vid}.vtt')
        digest=sha256(destmp4)
        (destdir/f'{vid}.sha256').write_text(f'{digest}  {vid}.mp4\n',encoding='utf-8')
        url=(f'https://github.com/{args.repo}/releases/download/{args.release_tag}/{vid}.mp4' if cls=='public_safe' else None)
        rows.append({
            'video_id':vid,'media_class':cls,'mp4':destmp4.name,'sha256':digest,
            'duration_seconds':q.get('final_duration_seconds'),
            'video_url':url,'release_tag':args.release_tag if url else None,
            'protected':cls=='protected_amc'
        })
    if unknown: raise SystemExit('Unknown video IDs: '+', '.join(unknown))
    ids=[r['video_id'] for r in rows]
    if len(ids)!=len(set(ids)): raise SystemExit('Duplicate final video IDs')
    if args.expected_total is not None and len(ids)!=args.expected_total:
        raise SystemExit(f'Expected {args.expected_total} finals, found {len(ids)}')
    public=[r for r in rows if r['media_class']=='public_safe']
    protected=[r for r in rows if r['media_class']=='protected_amc']
    app={r['video_id']:{
        'video_id':r['video_id'],
        'media_access':'public_release' if not r['protected'] else 'protected_authenticated',
        'video_url':r['video_url'],
        'sha256':r['sha256'],
        'duration_seconds':r['duration_seconds']
    } for r in rows}
    (out/'PUBLIC_RELEASE_MANIFEST.json').write_text(json.dumps({'schema_version':'summit-one-public-video-release-v1','count':len(public),'items':public},indent=2),encoding='utf-8')
    (out/'PROTECTED_AMC_MANIFEST.json').write_text(json.dumps({'schema_version':'summit-one-protected-amc-media-v1','count':len(protected),'items':protected},indent=2),encoding='utf-8')
    (out/'APP_MEDIA_REGISTRY.json').write_text(json.dumps({'schema_version':'summit-one-app-media-v1','count':len(rows),'by_id':app},indent=2),encoding='utf-8')
    with open(out/'MEDIA_PACKAGE_QA.csv','w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=['video_id','media_class','duration_seconds','sha256','video_url']);w.writeheader();w.writerows([{k:r.get(k) for k in w.fieldnames} for r in rows])
    (out/'PUBLIC_RELEASE_FILES.txt').write_text('\n'.join(sorted(p.name for p in pub.iterdir() if p.is_file()))+'\n',encoding='utf-8')
    summary={
        'total_final_videos':len(rows),'public_safe':len(public),'protected_amc':len(protected),
        'unknown':0,'duplicates':0,'public_contains_amc':any(PROTECTED_PATTERN.fullmatch(r['video_id']) for r in public),
        'release_tag':args.release_tag
    }
    if summary['public_contains_amc']: raise SystemExit('SAFETY FAILURE: AMC media entered public bundle')
    (out/'MEDIA_PACKAGE_SUMMARY.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps(summary,indent=2))

if __name__=='__main__': main()),
    re.compile(r'^K\d{3}

def classify(vid):
    if PROTECTED_PATTERN.fullmatch(vid): return 'protected_amc'
    if any(p.fullmatch(vid) for p in PUBLIC_PATTERNS): return 'public_safe'
    return 'unknown'

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

def link_or_copy(src,dst):
    dst.parent.mkdir(parents=True,exist_ok=True)
    if dst.exists(): dst.unlink()
    try: os.link(src,dst)
    except OSError: shutil.copy2(src,dst)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--final-root',required=True)
    ap.add_argument('--out-root',required=True)
    ap.add_argument('--release-tag',default='summit-one-video-v1')
    ap.add_argument('--repo',default='SimonRJ/-summit-one-narrator')
    ap.add_argument('--expected-total',type=int,default=None)
    args=ap.parse_args()
    root=Path(args.final_root); out=Path(args.out_root)
    pub=out/'public_release'; prot=out/'protected_amc'
    if out.exists(): shutil.rmtree(out)
    pub.mkdir(parents=True); prot.mkdir(parents=True)
    rows=[]; unknown=[]
    for qa in sorted(root.rglob('*.qa.json')):
        vid=qa.name[:-8]
        cls=classify(vid)
        if cls=='unknown': unknown.append(vid); continue
        mp4=qa.with_name(f'{vid}.mp4')
        if not mp4.exists():
            alt=qa.with_name(f'{vid}_final.mp4')
            if alt.exists(): mp4=alt
            else: raise SystemExit(f'Missing final MP4 for {vid}')
        vtt=qa.with_name(f'{vid}.vtt')
        q=json.load(open(qa,encoding='utf-8'))
        checks={
            'passed_integrity':bool(q.get('passed_integrity')),
            'passes_duration_sync':bool(q.get('passes_duration_sync')),
            'passes_video_codec':bool(q.get('passes_video_codec')),
            'passes_audio':bool(q.get('passes_audio')),
        }
        if not all(checks.values()): raise SystemExit(f'QA failed for {vid}: {checks}')
        if q.get('requires_manual_review'):
            raise SystemExit(f'Manual review required before release: {vid}')
        destdir=pub if cls=='public_safe' else prot
        destmp4=destdir/f'{vid}.mp4'
        link_or_copy(mp4,destmp4)
        if vtt.exists(): link_or_copy(vtt,destdir/f'{vid}.vtt')
        digest=sha256(destmp4)
        (destdir/f'{vid}.sha256').write_text(f'{digest}  {vid}.mp4\n',encoding='utf-8')
        url=(f'https://github.com/{args.repo}/releases/download/{args.release_tag}/{vid}.mp4' if cls=='public_safe' else None)
        rows.append({
            'video_id':vid,'media_class':cls,'mp4':destmp4.name,'sha256':digest,
            'duration_seconds':q.get('final_duration_seconds'),
            'video_url':url,'release_tag':args.release_tag if url else None,
            'protected':cls=='protected_amc'
        })
    if unknown: raise SystemExit('Unknown video IDs: '+', '.join(unknown))
    ids=[r['video_id'] for r in rows]
    if len(ids)!=len(set(ids)): raise SystemExit('Duplicate final video IDs')
    if args.expected_total is not None and len(ids)!=args.expected_total:
        raise SystemExit(f'Expected {args.expected_total} finals, found {len(ids)}')
    public=[r for r in rows if r['media_class']=='public_safe']
    protected=[r for r in rows if r['media_class']=='protected_amc']
    app={r['video_id']:{
        'video_id':r['video_id'],
        'media_access':'public_release' if not r['protected'] else 'protected_authenticated',
        'video_url':r['video_url'],
        'sha256':r['sha256'],
        'duration_seconds':r['duration_seconds']
    } for r in rows}
    (out/'PUBLIC_RELEASE_MANIFEST.json').write_text(json.dumps({'schema_version':'summit-one-public-video-release-v1','count':len(public),'items':public},indent=2),encoding='utf-8')
    (out/'PROTECTED_AMC_MANIFEST.json').write_text(json.dumps({'schema_version':'summit-one-protected-amc-media-v1','count':len(protected),'items':protected},indent=2),encoding='utf-8')
    (out/'APP_MEDIA_REGISTRY.json').write_text(json.dumps({'schema_version':'summit-one-app-media-v1','count':len(rows),'by_id':app},indent=2),encoding='utf-8')
    with open(out/'MEDIA_PACKAGE_QA.csv','w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=['video_id','media_class','duration_seconds','sha256','video_url']);w.writeheader();w.writerows([{k:r.get(k) for k in w.fieldnames} for r in rows])
    (out/'PUBLIC_RELEASE_FILES.txt').write_text('\n'.join(sorted(p.name for p in pub.iterdir() if p.is_file()))+'\n',encoding='utf-8')
    summary={
        'total_final_videos':len(rows),'public_safe':len(public),'protected_amc':len(protected),
        'unknown':0,'duplicates':0,'public_contains_amc':any(PROTECTED_PATTERN.fullmatch(r['video_id']) for r in public),
        'release_tag':args.release_tag
    }
    if summary['public_contains_amc']: raise SystemExit('SAFETY FAILURE: AMC media entered public bundle')
    (out/'MEDIA_PACKAGE_SUMMARY.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps(summary,indent=2))

if __name__=='__main__': main()),
    re.compile(r'^N[1-4]\.(?:26|27|28|29|30)

def classify(vid):
    if PROTECTED_PATTERN.fullmatch(vid): return 'protected_amc'
    if any(p.fullmatch(vid) for p in PUBLIC_PATTERNS): return 'public_safe'
    return 'unknown'

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

def link_or_copy(src,dst):
    dst.parent.mkdir(parents=True,exist_ok=True)
    if dst.exists(): dst.unlink()
    try: os.link(src,dst)
    except OSError: shutil.copy2(src,dst)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--final-root',required=True)
    ap.add_argument('--out-root',required=True)
    ap.add_argument('--release-tag',default='summit-one-video-v1')
    ap.add_argument('--repo',default='SimonRJ/-summit-one-narrator')
    ap.add_argument('--expected-total',type=int,default=None)
    args=ap.parse_args()
    root=Path(args.final_root); out=Path(args.out_root)
    pub=out/'public_release'; prot=out/'protected_amc'
    if out.exists(): shutil.rmtree(out)
    pub.mkdir(parents=True); prot.mkdir(parents=True)
    rows=[]; unknown=[]
    for qa in sorted(root.rglob('*.qa.json')):
        vid=qa.name[:-8]
        cls=classify(vid)
        if cls=='unknown': unknown.append(vid); continue
        mp4=qa.with_name(f'{vid}.mp4')
        if not mp4.exists():
            alt=qa.with_name(f'{vid}_final.mp4')
            if alt.exists(): mp4=alt
            else: raise SystemExit(f'Missing final MP4 for {vid}')
        vtt=qa.with_name(f'{vid}.vtt')
        q=json.load(open(qa,encoding='utf-8'))
        checks={
            'passed_integrity':bool(q.get('passed_integrity')),
            'passes_duration_sync':bool(q.get('passes_duration_sync')),
            'passes_video_codec':bool(q.get('passes_video_codec')),
            'passes_audio':bool(q.get('passes_audio')),
        }
        if not all(checks.values()): raise SystemExit(f'QA failed for {vid}: {checks}')
        if q.get('requires_manual_review'):
            raise SystemExit(f'Manual review required before release: {vid}')
        destdir=pub if cls=='public_safe' else prot
        destmp4=destdir/f'{vid}.mp4'
        link_or_copy(mp4,destmp4)
        if vtt.exists(): link_or_copy(vtt,destdir/f'{vid}.vtt')
        digest=sha256(destmp4)
        (destdir/f'{vid}.sha256').write_text(f'{digest}  {vid}.mp4\n',encoding='utf-8')
        url=(f'https://github.com/{args.repo}/releases/download/{args.release_tag}/{vid}.mp4' if cls=='public_safe' else None)
        rows.append({
            'video_id':vid,'media_class':cls,'mp4':destmp4.name,'sha256':digest,
            'duration_seconds':q.get('final_duration_seconds'),
            'video_url':url,'release_tag':args.release_tag if url else None,
            'protected':cls=='protected_amc'
        })
    if unknown: raise SystemExit('Unknown video IDs: '+', '.join(unknown))
    ids=[r['video_id'] for r in rows]
    if len(ids)!=len(set(ids)): raise SystemExit('Duplicate final video IDs')
    if args.expected_total is not None and len(ids)!=args.expected_total:
        raise SystemExit(f'Expected {args.expected_total} finals, found {len(ids)}')
    public=[r for r in rows if r['media_class']=='public_safe']
    protected=[r for r in rows if r['media_class']=='protected_amc']
    app={r['video_id']:{
        'video_id':r['video_id'],
        'media_access':'public_release' if not r['protected'] else 'protected_authenticated',
        'video_url':r['video_url'],
        'sha256':r['sha256'],
        'duration_seconds':r['duration_seconds']
    } for r in rows}
    (out/'PUBLIC_RELEASE_MANIFEST.json').write_text(json.dumps({'schema_version':'summit-one-public-video-release-v1','count':len(public),'items':public},indent=2),encoding='utf-8')
    (out/'PROTECTED_AMC_MANIFEST.json').write_text(json.dumps({'schema_version':'summit-one-protected-amc-media-v1','count':len(protected),'items':protected},indent=2),encoding='utf-8')
    (out/'APP_MEDIA_REGISTRY.json').write_text(json.dumps({'schema_version':'summit-one-app-media-v1','count':len(rows),'by_id':app},indent=2),encoding='utf-8')
    with open(out/'MEDIA_PACKAGE_QA.csv','w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=['video_id','media_class','duration_seconds','sha256','video_url']);w.writeheader();w.writerows([{k:r.get(k) for k in w.fieldnames} for r in rows])
    (out/'PUBLIC_RELEASE_FILES.txt').write_text('\n'.join(sorted(p.name for p in pub.iterdir() if p.is_file()))+'\n',encoding='utf-8')
    summary={
        'total_final_videos':len(rows),'public_safe':len(public),'protected_amc':len(protected),
        'unknown':0,'duplicates':0,'public_contains_amc':any(PROTECTED_PATTERN.fullmatch(r['video_id']) for r in public),
        'release_tag':args.release_tag
    }
    if summary['public_contains_amc']: raise SystemExit('SAFETY FAILURE: AMC media entered public bundle')
    (out/'MEDIA_PACKAGE_SUMMARY.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps(summary,indent=2))

if __name__=='__main__': main()),
)

def classify(vid):
    if PROTECTED_PATTERN.fullmatch(vid): return 'protected_amc'
    if any(p.fullmatch(vid) for p in PUBLIC_PATTERNS): return 'public_safe'
    return 'unknown'

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

def link_or_copy(src,dst):
    dst.parent.mkdir(parents=True,exist_ok=True)
    if dst.exists(): dst.unlink()
    try: os.link(src,dst)
    except OSError: shutil.copy2(src,dst)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--final-root',required=True)
    ap.add_argument('--out-root',required=True)
    ap.add_argument('--release-tag',default='summit-one-video-v1')
    ap.add_argument('--repo',default='SimonRJ/-summit-one-narrator')
    ap.add_argument('--expected-total',type=int,default=None)
    args=ap.parse_args()
    root=Path(args.final_root); out=Path(args.out_root)
    pub=out/'public_release'; prot=out/'protected_amc'
    if out.exists(): shutil.rmtree(out)
    pub.mkdir(parents=True); prot.mkdir(parents=True)
    rows=[]; unknown=[]
    for qa in sorted(root.rglob('*.qa.json')):
        vid=qa.name[:-8]
        cls=classify(vid)
        if cls=='unknown': unknown.append(vid); continue
        mp4=qa.with_name(f'{vid}.mp4')
        if not mp4.exists():
            alt=qa.with_name(f'{vid}_final.mp4')
            if alt.exists(): mp4=alt
            else: raise SystemExit(f'Missing final MP4 for {vid}')
        vtt=qa.with_name(f'{vid}.vtt')
        q=json.load(open(qa,encoding='utf-8'))
        checks={
            'passed_integrity':bool(q.get('passed_integrity')),
            'passes_duration_sync':bool(q.get('passes_duration_sync')),
            'passes_video_codec':bool(q.get('passes_video_codec')),
            'passes_audio':bool(q.get('passes_audio')),
        }
        if not all(checks.values()): raise SystemExit(f'QA failed for {vid}: {checks}')
        if q.get('requires_manual_review'):
            raise SystemExit(f'Manual review required before release: {vid}')
        destdir=pub if cls=='public_safe' else prot
        destmp4=destdir/f'{vid}.mp4'
        link_or_copy(mp4,destmp4)
        if vtt.exists(): link_or_copy(vtt,destdir/f'{vid}.vtt')
        digest=sha256(destmp4)
        (destdir/f'{vid}.sha256').write_text(f'{digest}  {vid}.mp4\n',encoding='utf-8')
        url=(f'https://github.com/{args.repo}/releases/download/{args.release_tag}/{vid}.mp4' if cls=='public_safe' else None)
        rows.append({
            'video_id':vid,'media_class':cls,'mp4':destmp4.name,'sha256':digest,
            'duration_seconds':q.get('final_duration_seconds'),
            'video_url':url,'release_tag':args.release_tag if url else None,
            'protected':cls=='protected_amc'
        })
    if unknown: raise SystemExit('Unknown video IDs: '+', '.join(unknown))
    ids=[r['video_id'] for r in rows]
    if len(ids)!=len(set(ids)): raise SystemExit('Duplicate final video IDs')
    if args.expected_total is not None and len(ids)!=args.expected_total:
        raise SystemExit(f'Expected {args.expected_total} finals, found {len(ids)}')
    public=[r for r in rows if r['media_class']=='public_safe']
    protected=[r for r in rows if r['media_class']=='protected_amc']
    app={r['video_id']:{
        'video_id':r['video_id'],
        'media_access':'public_release' if not r['protected'] else 'protected_authenticated',
        'video_url':r['video_url'],
        'sha256':r['sha256'],
        'duration_seconds':r['duration_seconds']
    } for r in rows}
    (out/'PUBLIC_RELEASE_MANIFEST.json').write_text(json.dumps({'schema_version':'summit-one-public-video-release-v1','count':len(public),'items':public},indent=2),encoding='utf-8')
    (out/'PROTECTED_AMC_MANIFEST.json').write_text(json.dumps({'schema_version':'summit-one-protected-amc-media-v1','count':len(protected),'items':protected},indent=2),encoding='utf-8')
    (out/'APP_MEDIA_REGISTRY.json').write_text(json.dumps({'schema_version':'summit-one-app-media-v1','count':len(rows),'by_id':app},indent=2),encoding='utf-8')
    with open(out/'MEDIA_PACKAGE_QA.csv','w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=['video_id','media_class','duration_seconds','sha256','video_url']);w.writeheader();w.writerows([{k:r.get(k) for k in w.fieldnames} for r in rows])
    (out/'PUBLIC_RELEASE_FILES.txt').write_text('\n'.join(sorted(p.name for p in pub.iterdir() if p.is_file()))+'\n',encoding='utf-8')
    summary={
        'total_final_videos':len(rows),'public_safe':len(public),'protected_amc':len(protected),
        'unknown':0,'duplicates':0,'public_contains_amc':any(PROTECTED_PATTERN.fullmatch(r['video_id']) for r in public),
        'release_tag':args.release_tag
    }
    if summary['public_contains_amc']: raise SystemExit('SAFETY FAILURE: AMC media entered public bundle')
    (out/'MEDIA_PACKAGE_SUMMARY.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps(summary,indent=2))

if __name__=='__main__': main()