"""Match new instructional art to the exact, naturally paced public Voice C edition."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from urllib.request import urlopen

import numpy as np
import soundfile as sf
from faster_whisper import WhisperModel

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'production/t01-studio'))
from prepare_audio import align,caption_cues,stamp,transcribe
from synth import MODEL_REVISION,RATE,VOICE_SHA

SOURCE_GUIDE='https://raw.githubusercontent.com/SimonRJ/-summit-one-narrator/a576b43f9d17f16a134445973b5c2445123b4984/data/lesson-intros/'
SOURCE_MOVIE='https://github.com/SimonRJ/-summit-one-narrator/releases/download/lesson-introductions/'
DIGESTS={'S101':'cd71dd989f84ceb2efa01d435f593347b7df557d55d9f16daa99e2f92fd00352',
         'S123':'d46d13dda004c68338c11f6cee0e2b6f8e1a3b328ddf079a8d4b9d60e7cea09b'}

def prepare(lesson,out,source,model_name):
    out.mkdir(parents=True,exist_ok=True);source.mkdir(parents=True,exist_ok=True)
    film=source/'original.mp4';guide_file=source/'guide.json'
    if not film.exists():
        with urlopen(SOURCE_MOVIE+lesson+'-Intro.mp4',timeout=100) as r:film.write_bytes(r.read())
    if not guide_file.exists():
        with urlopen(SOURCE_GUIDE+lesson+'.json',timeout=60) as r:guide_file.write_bytes(r.read())
    guide=json.loads(guide_file.read_text())
    script_file=ROOT/'production/scripts'/(lesson+'.json');script=json.loads(script_file.read_text())
    assert hashlib.sha256(film.read_bytes()).hexdigest()==guide['sha256']==DIGESTS[lesson]
    assert guide['reference_sha256']==VOICE_SHA and guide['model_revision']==MODEL_REVISION
    assert guide['narration_speed_changed'] is False and guide['transcript']==[s['narration'] for s in script['scenes']]
    raw=subprocess.check_output(['ffmpeg','-nostdin','-v','error','-xerror','-i',film,'-vn','-ac','1','-ar',str(RATE),'-f','f32le','pipe:1'])
    samples=np.frombuffer(raw,np.float32);duration=len(samples)/RATE
    assert abs(duration-guide['seconds'])<.15
    model=WhisperModel(model_name,device='cpu',compute_type='int8',cpu_threads=2)
    starts=[s['start'] for s in guide['scenes']]+[duration]
    scenes=[];captions=[]
    for part,start,end in zip(script['scenes'],starts,starts[1:]):
        n=part['n'];line=part['narration'];segment=samples[round(start*RATE):round(end*RATE)]
        speech=transcribe(model,segment)
        words,match=align(line,speech,start,end)
        if match<90:
            extra=transcribe(model,segment,use_vad=True)
            again,score=align(line,extra,start,end)
            if score>match:speech,words,match=extra,again,score
        assert match>=80,(lesson,n,match,' '.join(w.word for w in speech))
        cues=caption_cues(words)
        assert ' '.join(c['text'] for c in cues)==line,(lesson,n)
        for cue in cues:cue['end']=min(cue['end'],end)
        captions.extend(cues)
        scenes.append(dict(n=n,start=start,end=end,speech_end=words[-1]['end'],words=words,recognized_speech=' '.join(w.word.strip() for w in speech),match_percent=match))
        print(n,match,scenes[-1]['recognized_speech'],flush=True)
    average=sum(s['match_percent'] for s in scenes)/len(scenes)
    assert average>=90 and all(x['end']<=y['start']+.001 for x,y in zip(captions,captions[1:]))
    sf.write(out/'narration.flac',samples,RATE,subtype='PCM_24')
    (out/'script.json').write_bytes(script_file.read_bytes())
    timeline=dict(id=lesson,duration=duration,source_published_sha256=DIGESTS[lesson],narration_reference=VOICE_SHA,model_revision=MODEL_REVISION,mean_match_percent=round(average,2),scenes=scenes,captions=captions)
    (out/'timeline.json').write_text(json.dumps(timeline,indent=2)+'\n')
    (out/'captions.vtt').write_text('WEBVTT\n\n'+'\n\n'.join(f"{stamp(c['start'])} --> {stamp(c['end'])}\n{c['text']}" for c in captions)+'\n')

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('lesson',choices=DIGESTS);ap.add_argument('out',type=Path);ap.add_argument('source',type=Path);ap.add_argument('--model',default='base.en');args=ap.parse_args()
    prepare(args.lesson,args.out,args.source,args.model)
