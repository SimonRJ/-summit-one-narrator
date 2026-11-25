import json,re,subprocess,pathlib,numpy as np
from faster_whisper import WhisperModel
root=pathlib.Path('/workspace/scratch/2fdd119b5e17/s015-render-audit-20261125')
model=WhisperModel('/workspace/scratch/d5cfe38d5338/model',device='cpu',compute_type='int8',cpu_threads=2)
eot=model.hf_tokenizer.token_to_id('<|endoftext|>')
blocked=[i for token,i in model.hf_tokenizer.get_vocab().items() if i<eot and re.search('[0-9]',token)]
report={'source_movie_sha256':'f4bb4b7e43d5d0037680d07ff8b65a375fd552f865406657d7e2b259604eca52','method':'Existing local base.en recognizer on decoded MP4 scene audio, numeral tokens suppressed to measure spoken words; no synthesis or media change.','scenes':[]}
for scene,start,end in [(2,17.4,40.08),(3,40.08,63.11)]:
 b=subprocess.check_output(['ffmpeg','-hide_banner','-loglevel','error','-ss',str(start),'-t',str(end-start),'-i',str(root/'S015.mp4'),'-vn','-ar','16000','-ac','1','-f','f32le','pipe:1'])
 audio=np.frombuffer(b,dtype=np.float32)
 segments,info=model.transcribe(audio,language='en',beam_size=5,word_timestamps=True,condition_on_previous_text=False,suppress_tokens=[-1,*blocked])
 words=[]
 for segment in segments:
  for w in segment.words:
   words.append({'text':w.word.strip(),'start':round(start+w.start,4),'end':round(start+w.end,4),'probability':round(w.probability,5)})
 print(json.dumps({'scene':scene,'recognized':' '.join(w['text'] for w in words)},ensure_ascii=False),flush=True)
 report['scenes'].append({'scene':scene,'crop_start':start,'crop_end':end,'words':words})
(root/'number-word-onsets.json').write_text(json.dumps(report,indent=2)+'\n')
for s in report['scenes']:
 for a,b in ([(26.8,33.6)] if s['scene']==2 else [(47.5,53.0)]):
  print(json.dumps({'scene':s['scene'],'target_words':[w for w in s['words'] if a<=w['start']<=b]},indent=2),flush=True)
