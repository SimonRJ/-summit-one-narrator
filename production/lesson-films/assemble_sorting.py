"""Combine the seven original sorting performances with their new transfer and caption each take."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

import numpy as np
from faster_whisper import WhisperModel
from pocketsphinx import Decoder

HERE = Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'t01-studio'))
from prepare_audio import align, load_recording, stamp, transcribe

RATE = 48000
CONFIG = HERE/'sorting-edition'


def pcm(path, rate):
    raw = subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0','-ac','1','-ar',str(rate),'-f','s16le','pipe:1'])
    return np.frombuffer(raw,dtype='<i2')


def align_words(samples, text):
    decoder = Decoder(loglevel='ERROR')
    for token,sounds in {'labelled':'L EY B AH L D','unlabelled':'AH N L EY B AH L D','inclusively':'IH N K L UW S IH V L IY'}.items():
        if not decoder.lookup_word(token): decoder.add_word(token,sounds)
    # A hyphenated numeral stays one displayed word while both spoken parts are aligned.
    parts=[re.findall(r"[a-z]+(?:'[a-z]+)?",w.lower()) for w in text.split()]
    terms=[term for word in parts for term in word]
    decoder.set_align_text(' '.join(terms))
    decoder.start_utt();decoder.process_raw(samples.tobytes(),False,True);decoder.end_utt()
    aligned=[s for s in decoder.seg() if not s.word.startswith(('<','['))]
    assert [re.sub(r'\(\d+\)$','',s.word) for s in aligned]==terms
    index=0;result=[]
    for token,components in zip(text.split(),parts,strict=True):
        spans=aligned[index:index+len(components)];index+=len(components)
        result.append({'text':token,'start':spans[0].start_frame/100,'end':(spans[-1].end_frame+1)/100})
    return result


def prepare(source, take, output):
    meta=json.loads((CONFIG/'source.json').read_text())
    with source.open('rb') as stream: assert hashlib.file_digest(stream,'sha256').hexdigest()==meta['original_sha256']
    script=json.loads((HERE.parent/'scripts/S057.json').read_text())
    chapters=(CONFIG/'captions.txt').read_text().splitlines()
    bounds=meta['source_starts']
    original=pcm(source,RATE)
    # Keep each original sample across the seven contiguous teaching chapters, including their natural pauses.
    saved=[original[round(a*RATE):round(b*RATE)] for a,b in zip(bounds,bounds[1:])]
    saved_16k=pcm(source,16000)
    clips=[saved_16k[round(a*16000):round(b*16000)] for a,b in zip(bounds,bounds[1:])]
    new_text=script['scenes'][7]['narration']
    fresh=load_recording('S057',8,new_text)
    model=WhisperModel('base.en',device='cpu',compute_type='int8',cpu_threads=2)
    heard=transcribe(model,fresh)
    _,score=align(new_text,heard,0,len(fresh)/RATE)
    if score<92: raise ValueError(f'Check transfer narration ({score:.2f}%): '+''.join(w.word for w in heard))
    # Match the course loudness for the replacement take without changing its pace.
    new_bytes=subprocess.check_output(['ffmpeg','-v','error','-i',str(take),'-af','loudnorm=I=-18:TP=-2:LRA=9','-ar',str(RATE),'-ac','1','-f','s16le','pipe:1'])
    saved.append(np.concatenate([np.frombuffer(new_bytes,dtype='<i2'),np.zeros(4*RATE,dtype='<i2')]))
    clips.append(pcm(take,16000))
    output.mkdir(parents=True,exist_ok=True)
    audio=np.concatenate(saved)
    subprocess.run(['ffmpeg','-v','error','-y','-f','s16le','-ar',str(RATE),'-ac','1','-i','pipe:0','-c:a','flac',str(output/'narration.flac')],input=audio.tobytes(),check=True)
    scenes=[];captions=[];cursor=0
    scores=[*meta['source_scene_match_percent'],score]
    for i,(part,group,clip,sound,match) in enumerate(zip(script['scenes'],chapters,clips,saved,scores,strict=True)):
        assert group.replace('|',' ')==part['narration']
        start=cursor/RATE;cursor+=len(sound);end=cursor/RATE
        words=align_words(clip,part['narration'])
        for w in words:
            w['start']=round(start+w['start'],3);w['end']=min(round(end,3),round(start+w['end'],3))
            assert w['end']>w['start']
        scenes.append({'n':i+1,'start':round(start,3),'end':round(end,3),'speech_end':words[-1]['end'],'words':words,'match_percent':match})
        at=0
        for phrase in group.split('|'):
            phrase_words=words[at:at+len(phrase.split())];at+=len(phrase_words)
            following=words[at]['start'] if at<len(words) else end-.04
            onset=phrase_words[0]['start'];stop=min(following,max(phrase_words[-1]['end']+.1,onset+.8))
            assert onset<stop,phrase
            captions.append({'start':onset,'end':round(stop,3),'text':phrase})
    timeline={'id':'S057','duration':len(audio)/RATE,'narration_reference':meta['narration_reference'],'model_revision':meta['model_revision'],
              'source_movie_sha256':meta['original_sha256'],'original_contiguous_interval':[bounds[0],bounds[-1]],
              'transfer_source_sha256':hashlib.sha256(take.read_bytes()).hexdigest(),'transfer_independent_transcription':''.join(w.word for w in heard).strip(),
              'mean_match_percent':round(sum(scores)/len(scores),2),'word_timing_method':'PocketSphinx transcript-constrained alignment against each checked performance',
              'scenes':scenes,'captions':captions}
    (output/'timeline.json').write_text(json.dumps(timeline,indent=2)+'\n')
    (output/'script.json').write_text(json.dumps(script,indent=2)+'\n')
    (output/'captions.vtt').write_text('WEBVTT\n\n'+'\n\n'.join(f"{stamp(c['start'])} --> {stamp(c['end'])}\n{c['text']}" for c in captions)+'\n')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source',type=Path)
    parser.add_argument('transfer',type=Path)
    parser.add_argument('output',type=Path)
    args=parser.parse_args()
    prepare(args.source,args.transfer,args.output)
