"""Generate reproducible, original male voice auditions using official VoxCPM2."""
import gc, json, os, subprocess, time
from pathlib import Path
import numpy as np
import soundfile as sf
import torch
from huggingface_hub import HfApi, snapshot_download
from voxcpm import VoxCPM

ROOT=Path('build/voice-audition');ROOT.mkdir(parents=True,exist_ok=True)
brief=json.loads(Path('production/voice-audition/brief.json').read_text())
torch.set_num_threads(min(4,os.cpu_count() or 2));torch.set_num_interop_threads(1)
info=HfApi().model_info(brief['model'])
print('Loading official model revision',info.sha,flush=True)
path=snapshot_download(brief['model'],revision=info.sha,allow_patterns=['*.json','*.safetensors','audiovae.pth','*.model','*.txt'])
started=time.monotonic()
model=VoxCPM.from_pretrained(path,load_denoiser=False,optimize=False,device='cpu')
print('Model loaded in',round(time.monotonic()-started,1),'seconds',flush=True)
report={'model':brief['model'],'model_revision':info.sha,'code_revision':brief['code_revision'],'mode':'original voice design','reference_audio':None,'device':'cpu','sample_rate':model.tts_model.sample_rate,'text':brief['display_text'],'voices':[]}
for voice in brief['voices']:
    print('Generating',voice['id'],voice['label'],flush=True);start=time.monotonic()
    wav=model.generate(text='('+voice['description']+')'+brief['text'],cfg_value=2.0,inference_timesteps=10,seed=voice['seed'],max_len=350,normalize=False,denoise=False,retry_badcase=True,retry_badcase_max_times=2)
    wav=np.asarray(wav,dtype=np.float32).reshape(-1);rate=model.tts_model.sample_rate
    assert np.isfinite(wav).all() and 8<len(wav)/rate<55,'Invalid or runaway output'
    assert np.sqrt(np.mean(wav**2))>.005,'Output is silent'
    out=ROOT/('vox-australian-male-'+voice['id']+'.wav');sf.write(out,wav,rate,subtype='PCM_16')
    mp3=out.with_suffix('.mp3')
    subprocess.run(['ffmpeg','-v','error','-y','-i',str(out),'-af','loudnorm=I=-18:TP=-2:LRA=9','-ar','48000','-c:a','libmp3lame','-b:a','192k',str(mp3)],check=True)
    entry={**voice,'duration_seconds':round(len(wav)/rate,3),'generation_seconds':round(time.monotonic()-start,2),'file':mp3.name,'peak':round(float(np.max(np.abs(wav))),4),'rms':round(float(np.sqrt(np.mean(wav**2))),4)}
    report['voices'].append(entry);(ROOT/'manifest.json').write_text(json.dumps(report,indent=2));print(json.dumps(entry),flush=True)
    del wav;gc.collect()
del model;gc.collect()
# Independent speech recognition checks the actual output, not only the requested text.
from faster_whisper import WhisperModel
asr=WhisperModel('base.en',device='cpu',compute_type='int8',cpu_threads=2)
for v in report['voices']:
    segments,_=asr.transcribe(str(ROOT/v['file']),beam_size=5,language='en')
    v['heard_text']=' '.join(s.text.strip() for s in segments)
    print('HEARD',v['id'],v['heard_text'],flush=True)
    assert all(k in v['heard_text'].lower() for k in ['summit','seven','pattern']),'Sample omitted key content'
(ROOT/'manifest.json').write_text(json.dumps(report,indent=2))
print('Auditions complete. Accent preference requires listening review.',flush=True)
