"""Recover unchanged spoken passages from the exact released film, and remove surplus trailing silence."""
import argparse,hashlib,json,subprocess,wave
from pathlib import Path
from urllib.request import urlopen
import numpy as np
ROOT=Path(__file__).resolve().parents[3]
REFERENCE='0f3304a393ee504e9fa22537267ac03f150569a5fab0859616f261d009513362'
MODEL='7936080b41163874f38610f46f438e2c0757f9fd'

def recover(id,old,source,sha):
    meta=json.loads(old.read_text());script=json.loads((ROOT/'production/scripts'/(id+'.json')).read_text())
    assert meta['id']==script['id']==id and len(script['scenes'])==len(meta['scenes'])==len(meta['transcript'])
    assert meta['sha256']==sha==hashlib.sha256(source.read_bytes()).hexdigest()
    assert meta['reference_sha256']==REFERENCE and meta['model_revision']==MODEL
    build=ROOT/'build/t01-studio';build.mkdir(parents=True,exist_ok=True)
    raw=subprocess.check_output(['ffmpeg','-nostdin','-v','error','-i',str(source),'-map','0:a:0','-ac','1','-ar','48000','-f','s16le','-'])
    audio=np.frombuffer(raw,dtype='<i2');starts=[v['start'] for v in meta['scenes']]+[meta['duration_seconds']]
    reused=[]
    for row,narr,a,b in zip(script['scenes'],meta['transcript'],starts,starts[1:]):
        if row['narration']!=narr:continue
        n=row['n'];clip=audio[round(a*48000):round(b*48000)]
        size=960;blocks=clip[:len(clip)//size*size].reshape(-1,size).astype('float32')/32768
        rms=np.sqrt((blocks**2).mean(axis=1));audible=np.flatnonzero(rms>max(.0018,rms.max()*.006))
        assert len(audible)>20
        end=min(len(clip),int(audible[-1]+1)*size+int(.24*48000))
        assert len(clip)-(audible[-1]+1)*size>.14*48000,(id,n,'no silent boundary after passage')
        # Keep the waveform from its recorded beginning. Remove only redundant silence after the speech.
        part=clip[:end];path=build/f'{id}-{n:02}.wav'
        with wave.open(str(path),'wb') as writer:
            writer.setparams((1,2,48000,0,'NONE','not compressed'));writer.writeframes(part.tobytes())
        info=dict(lesson=id,scene=n,narration_sha256=hashlib.sha256(narr.encode()).hexdigest(),reference_sha256=REFERENCE,model_revision=MODEL,natural_speed=True,sample_rate_hz=48000,duration_seconds=len(part)/48000,source_video_sha256=sha,source_start_seconds=a,source_end_seconds=a+len(part)/48000)
        path.with_suffix('.json').write_text(json.dumps(info)+'\n');reused.append(n)
    return reused
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('id');p.add_argument('sha');p.add_argument('--meta',type=Path);p.add_argument('--source',type=Path);a=p.parse_args()
    build=ROOT/'build';build.mkdir(exist_ok=True);id=a.id
    assert len(id)==4 and id[0]=='S' and id[1:].isdigit()
    meta=a.meta or build/(id+'-catalogue.json');source=a.source or build/(id+'-source.mp4')
    if not a.meta:meta.write_bytes(urlopen('https://raw.githubusercontent.com/SimonRJ/-summit-one-narrator/refs/heads/lesson-intro-catalog/data/lesson-intros/'+id+'.json',timeout=90).read())
    if not a.source:source.write_bytes(urlopen('https://github.com/SimonRJ/-summit-one-narrator/releases/download/lesson-introductions/'+id+'-Intro.mp4',timeout=90).read())
    print(id,'reused original spoken passages',recover(id,meta,source,a.sha))
