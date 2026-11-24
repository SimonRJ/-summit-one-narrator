"""Cut the unique examples from the checked public Voice C masters and time their new illustrations."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

import numpy as np
from pocketsphinx import Decoder

HERE=Path(__file__).resolve().parent
CONFIG=HERE/'pair-editions'
PRONUNCIATIONS={"pair's":'P EH R Z','leftmost':'L EH F T M OW S T','tiling':'T AY L IH NG','tilings':'T AY L IH NG Z'}
RATE=48000


def stamp(time):
    ms=round(time*1000)
    return f'{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d}.{ms%1000:03d}'


def words_in_recording(samples, words):
    decoder=Decoder(loglevel='ERROR')
    for term,sounds in PRONUNCIATIONS.items():
        if not decoder.lookup_word(term): decoder.add_word(term,sounds)
    # Join the component pronunciations of written hyphenated numbers back into the same displayed word.
    parts=[re.findall(r"[a-z]+(?:'[a-z]+)?",w.lower()) for w in words]
    terms=[term for word in parts for term in word]
    decoder.set_align_text(' '.join(terms))
    decoder.start_utt();decoder.process_raw(samples.tobytes(),False,True);decoder.end_utt()
    aligned=[s for s in decoder.seg() if not s.word.startswith(('<','['))]
    assert [re.sub(r'\(\d+\)$','',s.word) for s in aligned]==terms
    index=0;out=[]
    for token,components in zip(words,parts,strict=True):
        spans=aligned[index:index+len(components)];index+=len(components)
        out.append({'text':token,'start':spans[0].start_frame/100,'end':(spans[-1].end_frame+1)/100})
    return out


def pcm(path,rate):
    raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0','-ac','1','-ar',str(rate),'-f','s16le','pipe:1'])
    return np.frombuffer(raw,dtype='<i2')


def prepare(id,source,output):
    meta=json.loads((CONFIG/'source.json').read_text())[id]
    with source.open('rb') as incoming: assert hashlib.file_digest(incoming,'sha256').hexdigest()==meta['original_sha256']
    script=json.loads((HERE.parent/'scripts'/f'{id}.json').read_text())
    chapters=(CONFIG/f'{id}-captions.txt').read_text().splitlines()
    origin=meta['source_starts'][0];duration=round(meta['source_starts'][-1]-origin,3)
    points=meta['source_starts'];actual=pcm(source,RATE);recognition=pcm(source,16000)
    output.mkdir(parents=True,exist_ok=True)
    audio=actual[round(origin*RATE):round(points[-1]*RATE)]
    subprocess.run(['ffmpeg','-v','error','-y','-f','s16le','-ar',str(RATE),'-ac','1','-i','pipe:0','-c:a','flac',str(output/'narration.flac')],input=audio.tobytes(),check=True)
    scenes=[];captions=[]
    for i,(scene,cues,a,b) in enumerate(zip(script['scenes'],chapters,points[:-1],points[1:],strict=True)):
        assert cues.replace('|',' ')==scene['narration']
        words=words_in_recording(recognition[round(a*16000):round(b*16000)],scene['narration'].split())
        for w in words:
            w['start']=round(a-origin+w['start'],3);w['end']=min(round(b-origin,3),round(a-origin+w['end'],3))
            assert w['end']>w['start']
        scenes.append({'n':i+1,'start':round(a-origin,3),'end':round(b-origin,3),'speech_end':words[-1]['end'],'words':words})
        pos=0
        for phrase in cues.split('|'):
            chunk=words[pos:pos+len(phrase.split())];pos+=len(chunk)
            next_start=words[pos]['start'] if pos<len(words) else b-origin-.04
            start=chunk[0]['start'];end=min(next_start,max(chunk[-1]['end']+.1,start+.8))
            assert start<end,(id,phrase)
            captions.append({'start':start,'end':round(end,3),'text':phrase})
    timeline={'id':id,'duration':duration,'narration_reference':meta['narration_reference'],'model_revision':meta['model_revision'],
              'source_movie_sha256':meta['original_sha256'],'original_contiguous_interval':[points[0],points[-1]],
              'mean_match_percent':round(sum(meta['source_scene_match_percent'])/len(scenes),2),
              'word_timing_method':'Transcript-constrained alignment of the exact retained recording',
              'scenes':scenes,'captions':captions}
    (output/'script.json').write_text(json.dumps(script,indent=2)+'\n')
    (output/'timeline.json').write_text(json.dumps(timeline,indent=2)+'\n')
    (output/'captions.vtt').write_text('WEBVTT\n\n'+'\n\n'.join(f"{stamp(x['start'])} --> {stamp(x['end'])}\n{x['text']}" for x in captions)+'\n')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('id',choices=['S095','S097']);p.add_argument('source',type=Path);p.add_argument('output',type=Path)
    a=p.parse_args();prepare(a.id,a.source,a.output)
