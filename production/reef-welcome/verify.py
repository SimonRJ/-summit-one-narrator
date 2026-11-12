import json,math,subprocess,wave
from pathlib import Path
import numpy as np
p=Path('build/reef-welcome');script=json.loads(Path('production/reef-welcome/narration.json').read_text());timing=json.loads((p/'timing.json').read_text());alignment=json.loads((p/'alignment-qa.json').read_text());caps=json.loads((p/'captions.json').read_text())
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p/'final.mp4')]))
v=next(s for s in probe['streams'] if s['codec_type']=='video');a=next(s for s in probe['streams'] if s['codec_type']=='audio');duration=float(probe['format']['duration'])
assert (v['width'],v['height'],v['codec_name'],a['codec_name'])==(1920,1080,'h264','aac')
assert 100<duration<300,(duration,'Unexpected intro length')
assert abs(duration-timing['duration_seconds']-2.8)<.15
assert len(timing['segments'])==15 and timing['voice']=='bm_george'
assert [s['text'] for s in timing['segments']]==script['segments']
assert alignment['match_percent']>=90
assert all(c['start']<c['end'] for c in caps)
assert all(caps[i]['end']<=caps[i+1]['start']+.001 for i in range(len(caps)-1))
with wave.open(str(p/'narration.wav')) as f:
    data=np.frombuffer(f.readframes(f.getnframes()),dtype=np.int16).astype(float)/32768
assert np.sqrt(np.mean(data**2))>.01
assert pow(7,2027,10)==3 and divmod(2027,4)==(506,3)
assert [pow(7,k,10) for k in range(1,5)]==[7,9,3,1]
board={(r,c) for r in range(6) for c in range(8)}-{(0,0),(5,7)}
assert len(board)==46==23*2
assert sum((r+c)%2==0 for r,c in board)==22
assert sum((r+c)%2==1 for r,c in board)==24
assert all((r+c)%2!=(r+dr+c+dc)%2 for r,c in board for dr,dc in [(1,0),(0,1)] if (r+dr,c+dc) in board)
assert [k*(k+1) for k in range(1,7)]==[2,6,12,20,30,42]
pronunciation=json.loads((p/'pronunciation-qa.json').read_text())
assert pronunciation['voice']=='bm_george' and len(pronunciation['entries'])==2
assert all(x['phonemes'] in ['mˈɑːwə','mˈɑːwəz'] for x in pronunciation['entries'])
assert all('M A W A' not in t for t in script['segments'])
subprocess.run(['ffmpeg','-v','error','-i',str(p/'final.mp4'),'-f','null','-'],check=True)
report={'revision':script['revision'],'pronunciation':pronunciation,'title':script['title'],'duration_seconds':duration,'resolution':'1920x1080','fps':v['avg_frame_rate'],'voice':timing['voice'],'speed':timing['speed'],'scenes':15,'word_alignment_percent':alignment['match_percent'],'caption_layers':1,'mathematics_checked':True,'full_decode_passed':True,'audio_rms':round(float(np.sqrt(np.mean(data**2))),4),'script_words':sum(len(s.split()) for s in script['segments']),'sources':'production/reef-welcome/sources.json','file_bytes':(p/'final.mp4').stat().st_size}
assert report['file_bytes']<95*1024*1024
(p/'qa.json').write_text(json.dumps(report,indent=2));(p/'transcript.txt').write_text(script['title']+'\n\n'+'\n\n'.join(script['segments']))
print(json.dumps(report,indent=2))
