"""Reuse the user-approved synthetic voice C as reference; never mix old speech."""
import argparse,gc,hashlib,json,os,subprocess
from pathlib import Path
import numpy as np
import soundfile as sf
p=argparse.ArgumentParser();p.add_argument('--segment',type=int);a=p.parse_args()
root=Path('build/reef-welcome');root.mkdir(parents=True,exist_ok=True)
doc=json.loads(Path('production/reef-welcome/narration.json').read_text())
ref=Path('media/voice-audition/vox-australian-male-c.mp3')
if a.segment is not None:
 import torch
 from huggingface_hub import snapshot_download
 from voxcpm import VoxCPM
 torch.set_num_threads(2);torch.set_num_interop_threads(1)
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(ref),'-ar','48000','-ac','1',str(root/'reference.wav')],check=True)
 model=VoxCPM.from_pretrained(snapshot_download('openbmb/VoxCPM2',revision='7936080b41163874f38610f46f438e2c0757f9fd',allow_patterns=['*.json','*.safetensors','audiovae.pth','*.model','*.txt']),load_denoiser=False,optimize=False,device='cpu')
 prompt=json.loads(Path('production/voice-audition/brief.json').read_text())['text']
 i=a.segment
 wav=np.asarray(model.generate(text=doc['segments'][i].replace('MAWA', 'Mawa'),prompt_wav_path=str(root/'reference.wav'),reference_wav_path=str(root/'reference.wav'),prompt_text=prompt,seed=126+i,cfg_value=2.0,inference_timesteps=10,normalize=False,denoise=False,max_len=650,retry_badcase=True,retry_badcase_max_times=1),dtype=np.float32).reshape(-1)
 assert np.isfinite(wav).all() and 1<len(wav)/48000<45 and np.sqrt(np.mean(wav**2))>.005
 sf.write(root/f'speech-{i:02d}.wav',wav,48000)
 print(json.dumps({'segment':i,'duration':len(wav)/48000}),flush=True)
else:
 chunks=[];segments=[];cursor=0
 for i,text in enumerate(doc['segments']):
  wav,rate=sf.read(root/f'speech-{i:02d}.wav');assert rate==48000
  pause=doc['pause_seconds'][i] if i<14 else 0
  segments.append(dict(index=i+1,text=text,start_seconds=cursor,duration_seconds=len(wav)/rate,pause_after=pause))
  chunks.extend([wav,np.zeros(round(pause*rate))]);cursor+=len(wav)/rate+pause
 assert 100<cursor+2.8<300,f'Unexpected introduction duration: {cursor}'
 sf.write(root/'raw-narration.wav',np.concatenate(chunks),48000)
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(root/'raw-narration.wav'),'-af','loudnorm=I=-18:TP=-2:LRA=9','-ar','48000',str(root/'narration.wav')],check=True)
 (root/'timing.json').write_text(json.dumps(dict(id=doc['id'],title=doc['title'],voice='VoxCPM2 — approved voice C',speed=1.0,duration_seconds=cursor,segments=segments,reference_sha256=hashlib.sha256(ref.read_bytes()).hexdigest(),old_audio_used=False),indent=2))
