"""Verify the rendered introduction, narration, captions and mathematical examples."""
import hashlib,itertools,json,math,re,subprocess,wave
from pathlib import Path
import numpy as np
p=Path('build/amc-introduction');src=Path('production/amc-introduction')
script=json.loads((src/'narration.json').read_text());timing=json.loads((p/'timing.json').read_text());alignment=json.loads((p/'alignment-qa.json').read_text());caps=json.loads((p/'captions.json').read_text())
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p/'final.mp4')]))
v=next(s for s in probe['streams'] if s['codec_type']=='video');a=next(s for s in probe['streams'] if s['codec_type']=='audio');duration=float(probe['format']['duration'])
assert (v['width'],v['height'],v['codec_name'],a['codec_name'])==(1920,1080,'h264','aac')
assert 180<duration<420
assert abs(duration-timing['duration_seconds']-2.8)<.15
assert len(timing['segments'])==18 and timing['voice']=='VoxCPM2 — approved voice C'
assert [s['text'] for s in timing['segments']]==script['segments']
assert alignment['match_percent']>=90
assert all(c['start']<c['end'] for c in caps)
assert all(caps[i]['end']<=caps[i+1]['start']+.001 for i in range(len(caps)-1))
assert all(c['end']<=duration for c in caps)
assert timing['old_audio_used'] is False
assert len([s for s in probe['streams'] if s['codec_type']=='audio'])==1
heard=json.loads((p/'heard-words.json').read_text())
assert not re.search(r'\breef\b', ' '.join(w['text'] for w in heard),re.I),'Name found in generated speech'
for f in ['narration.json','render.py']:
 assert not re.search(r'\breef\b',(src/f).read_text(),re.I)
with wave.open(str(p/'narration.wav')) as f:
 data=np.frombuffer(f.readframes(f.getnframes()),dtype=np.int16).astype(float)/32768
assert np.sqrt(np.mean(data**2))>.01
assert np.max(np.abs(data))<1
# Verify each exact demonstration, including by enumeration where useful.
assert 10*3+10*4+5*5+sum(range(6,11))==135
assert pow(3,123,10)==7 and divmod(123,4)==(30,3)
assert [pow(3,k,10) for k in range(1,5)]==[3,9,7,1]
assert (5-3)*6==12 and (3+5)*6==48
rectangles=[(a,b,c,d) for a,b in itertools.combinations(range(4),2) for c,d in itertools.combinations(range(5),2)]
assert len(rectangles)==60 and len(list(itertools.combinations(range(4),2)))==6 and len(list(itertools.combinations(range(5),2)))==10
assert (17-5)*2+7==31 and ((31-7)//2)+5==17
outcomes=list(itertools.product(range(1,7),repeat=2));wins=[p for p in outcomes if sum(p)==7]
assert len(outcomes)==36 and len(wins)==6
assert 15%2==1 and 7+7+1==15
subprocess.run(['ffmpeg','-v','error','-i',str(p/'final.mp4'),'-f','null','-'],check=True)
report={'revision':script['revision'],'title':script['title'],'duration_seconds':duration,'resolution':'1920x1080','fps':v['avg_frame_rate'],'voice':timing['voice'],'voice_reference_sha256':timing['reference_sha256'],'old_audio_used':False,'name_removed_from_script_visuals_and_recognised_speech':True,'scenes':18,'word_alignment_percent':alignment['match_percent'],'caption_layers':1,'mathematics_checked':True,'full_decode_passed':True,'audio_stream_count':1,'audio_rms':round(float(np.sqrt(np.mean(data**2))),4),'script_words':sum(len(s.split()) for s in script['segments']),'sources':'production/amc-introduction/sources.json','file_bytes':(p/'final.mp4').stat().st_size,'sha256':hashlib.sha256((p/'final.mp4').read_bytes()).hexdigest()}
assert report['file_bytes']<95*1024*1024
(p/'qa.json').write_text(json.dumps(report,indent=2));(p/'transcript.txt').write_text(script['title']+'\n\n'+'\n\n'.join(s.replace('A M C','AMC') for s in script['segments']))
print(json.dumps(report,indent=2))
