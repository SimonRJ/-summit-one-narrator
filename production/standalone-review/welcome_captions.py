"""Retain the approved complete words in spoken mathematical phrases."""
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
root=Path('build/amc-introduction')
script=json.loads((HERE/'welcome-script.json').read_text())
original=json.loads((root/'words.json').read_text())['words']
groups=(HERE/'welcome-captions.txt').read_text().splitlines()
scenes=json.loads((root/'timing.json').read_text())['segments']
captions=[]
for i,(group,segment,scene) in enumerate(zip(groups,script['segments'],scenes,strict=True)):
    assert group.replace('|',' ')==segment,(i,group)
    words=[w for w in original if w['segment']==i+1]
    assert ' '.join(w['text'] for w in words)==segment
    pos=0
    for chunk in group.split('|'):
        items=words[pos:pos+len(chunk.split())]
        pos+=len(items)
        following=words[pos]['start'] if pos<len(words) else scene['start_seconds']+scene['duration_seconds']
        start=items[0]['start'];end=min(following,max(start+.7,items[-1]['end']+.08))
        if end<=start:raise ValueError(f'Empty caption at {chunk}')
        captions.append({'start':start,'end':end,'text':chunk.replace('A M C','AMC')})
def stamp(s):
    ms=round(s*1000)
    return f'{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d}.{ms%1000:03d}'
(root/'captions.json').write_text(json.dumps(captions,indent=2)+'\n')
(root/'AMCIntroduction.vtt').write_text('WEBVTT\n\n'+'\n\n'.join(
    f"{stamp(x['start'])} --> {stamp(x['end'])}\n{x['text']}" for x in captions)+'\n')
