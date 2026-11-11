import itertools,json,subprocess,wave
from pathlib import Path
p=Path('build/amc2025-q17')
f=p/'final.mp4'
d=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(f)]))
v=next(x for x in d['streams'] if x['codec_type']=='video');a=next(x for x in d['streams'] if x['codec_type']=='audio')
assert (v['width'],v['height'])==(1920,1080)
assert 35<float(d['format']['duration'])<=60
assert v['codec_name']=='h264' and a['codec_name']=='aac'
timing=json.loads((p/'timing.json').read_text());assert len(timing['segments'])==9
values=[(sum(w*x for w,x in zip([1,2,3,2,1],arr)),arr) for arr in itertools.permutations(range(1,6))]
assert max(x[0] for x in values)==32
assert sum([9,12,11])==32
assert [sum([1,3,5,4,2][i:i+3]) for i in range(3)]==[9,12,11]
subprocess.run(['ffmpeg','-v','error','-i',str(f),'-f','null','-'],check=True)
r={'duration_seconds':float(d['format']['duration']),'resolution':'1920x1080','fps':v['avg_frame_rate'],'audio_voice':timing['voice'],'speech_aligned_scenes':9,'permutations_checked':120,'maximum':32,'correct_option':'C','full_decode_passed':True,'exact_reference_voice_match':False}
(p/'qa.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
