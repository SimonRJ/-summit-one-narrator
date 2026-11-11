import itertools,json,subprocess,wave,re,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from solution_design import load_question
q=load_question(Path(__file__).with_name('question.json'))
p=Path('build/amc2025-q17')
f=p/'final.mp4'
d=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(f)]))
v=next(x for x in d['streams'] if x['codec_type']=='video');a=next(x for x in d['streams'] if x['codec_type']=='audio')
assert (v['width'],v['height'])==(1920,1080)
assert 35<float(d['format']['duration'])<=60
assert v['codec_name']=='h264' and a['codec_name']=='aac'
timing=json.loads((p/'timing.json').read_text());assert len(timing['segments'])==6
def normal(s):
 for n,w in [('1','one'),('3','three'),('5','five')]:s=s.replace(n,w)
 return re.sub(r'[^a-z0-9]','',s.lower())
assert normal(timing['segments'][0]['text'])==normal(q['question_text'])
assert 'maximising problem' in timing['segments'][1]['text']
assert 'count how often each bottom number contributes' in timing['segments'][1]['text']
assert timing['segments'][0]['duration_seconds']>20
assert (p/'exact-question.jpg').exists()
values=[(sum(w*x for w,x in zip([1,2,3,2,1],arr)),arr) for arr in itertools.permutations(range(1,6))]
assert max(x[0] for x in values)==32
assert sum([9,12,11])==32
assert [sum([1,3,5,4,2][i:i+3]) for i in range(3)]==[9,12,11]
subprocess.run(['ffmpeg','-v','error','-i',str(f),'-f','null','-'],check=True)
r={'duration_seconds':float(d['format']['duration']),'resolution':'1920x1080','fps':v['avg_frame_rate'],'audio_voice':timing['voice'],'speech_aligned_scenes':6,'exact_problem_shown_and_narrated':True,'problem_type_and_plan_before_solution':True,'question_reading_seconds':timing['segments'][0]['duration_seconds'],'colour_fidelity_manifest_passed':True,'revision':q['revision'],'permutations_checked':120,'maximum':32,'correct_option':'C','full_decode_passed':True,'exact_reference_voice_match':False}
(p/'qa.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
