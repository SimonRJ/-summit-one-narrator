"""Check completed speech without regenerating valid audio."""
import difflib,json,re,subprocess
from pathlib import Path
import numpy as np
import soundfile as sf
from faster_whisper import WhisperModel

p=Path('build/voice-audition');report=json.loads((p/'manifest.json').read_text())
def words(s):
    s=s.lower().replace('ross moyne','rossmoyne')
    s=re.sub(r'\b(marwa|maua)\b','mawa',s)
    s=re.sub(r'\b2027\b','two thousand and twenty seven',s)
    s=re.sub(r'\b7\b','seven',s)
    return re.sub('[^a-z0-9 ]',' ',s).split()
expected=words(report['text'])
asr=WhisperModel('base.en',device='cpu',compute_type='int8',cpu_threads=2)
for v in report['voices']:
    wav,rate=sf.read(p/v['file'].replace('.mp3','.wav'))
    assert rate==48000 and np.isfinite(wav).all()
    assert 8<len(wav)/rate<55 and np.sqrt(np.mean(wav**2))>.005
    subprocess.run(['ffmpeg','-v','error','-i',str(p/v['file']),'-f','null','-'],check=True)
    segs,_=asr.transcribe(str(p/v['file']),beam_size=5,language='en')
    v['heard_text']=' '.join(s.text.strip() for s in segs)
    got=words(v['heard_text']);matched=sum(m.size for m in difflib.SequenceMatcher(None,expected,got,autojunk=False).get_matching_blocks())
    v['script_word_coverage']=round(matched/len(expected),4)
    v['full_decode_passed']=True
    (p/'manifest.json').write_text(json.dumps(report,indent=2))
    print(v['id'],v['heard_text'],v['script_word_coverage'],flush=True)
    assert v['script_word_coverage']>=.9 and .9<=len(got)/len(expected)<=1.1,'Transcript differs materially'
    assert all(x in got for x in ['seven','power','thousand','twenty','pattern','careful','thinking'])
report['qa_status']='passed'
report['verification_note']='ASR numerals are expanded to words; spelling variants of MAWA and Rossmoyne are normalised for matching. Accent naturalness requires listening review.'
(p/'manifest.json').write_text(json.dumps(report,indent=2))
