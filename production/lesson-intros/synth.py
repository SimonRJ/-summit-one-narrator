"""Generate lesson opening films with the student's approved synthetic VoxCPM2 voice C."""
import argparse,hashlib,json,subprocess
from pathlib import Path
import numpy as np
import soundfile as sf
parser=argparse.ArgumentParser()
parser.add_argument("--lesson",required=True,choices=("S001","S002"))
parser.add_argument("--segment",type=int)
args=parser.parse_args()
root=Path("build/lesson-intros")/args.lesson
root.mkdir(parents=True,exist_ok=True)
doc=json.loads((Path("production/lesson-intros")/(args.lesson+".json")).read_text())
ref=Path("media/voice-audition/vox-australian-male-c.mp3")
if args.segment is not None:
 import torch
 from huggingface_hub import snapshot_download
 from voxcpm import VoxCPM
 torch.set_num_threads(2);torch.set_num_interop_threads(1)
 subprocess.run(["ffmpeg","-v","error","-y","-i",str(ref),"-ac","1","-ar","48000",str(root/"reference.wav")],check=True)
 model=VoxCPM.from_pretrained(snapshot_download("openbmb/VoxCPM2",revision="7936080b41163874f38610f46f438e2c0757f9fd",allow_patterns=["*.json","*.safetensors","audiovae.pth","*.model","*.txt"]),load_denoiser=False,optimize=False,device="cpu")
 prompt=json.loads(Path("production/voice-audition/brief.json").read_text())["text"]
 n=args.segment
 if not 0<=n<len(doc["segments"]):raise ValueError("Invalid segment")
 words=doc["segments"][n]
 wav=np.asarray(model.generate(text=words,prompt_wav_path=str(root/"reference.wav"),reference_wav_path=str(root/"reference.wav"),prompt_text=prompt,seed=406+20*int(args.lesson[-1])+n,cfg_value=2.0,inference_timesteps=10,normalize=False,denoise=False,max_len=650,retry_badcase=True,retry_badcase_max_times=1),dtype=np.float32).reshape(-1)
 assert np.isfinite(wav).all() and 2<len(wav)/48000<48 and np.sqrt(np.mean(wav**2))>.005, "Audio must be natural, non-silent and bounded"
 sf.write(root/f"speech-{n:02d}.wav",wav,48000)
 print(json.dumps({"lesson":args.lesson,"segment":n,"seconds":round(len(wav)/48000,3)}),flush=True)
else:
 chunks=[];segments=[];cursor=0
 for i,words in enumerate(doc["segments"]):
  sound,rate=sf.read(root/f"speech-{i:02d}.wav");assert rate==48000
  pause=doc["pause_seconds"][i]
  chunks.extend([sound,np.zeros(round(pause*rate),dtype=np.float32)])
  segments.append({"index":i+1,"text":words,"start_seconds":cursor,"duration_seconds":len(sound)/rate,"pause_after":pause})
  cursor+=len(sound)/rate+pause
 assert 110<cursor<420,f"Unexpected narration length {cursor}"
 sf.write(root/"raw-narration.wav",np.concatenate(chunks),48000)
 subprocess.run(["ffmpeg","-v","error","-y","-i",str(root/"raw-narration.wav"),"-af","loudnorm=I=-18:TP=-2:LRA=9","-ar","48000",str(root/"narration.wav")],check=True)
 (root/"timing.json").write_text(json.dumps({"id":args.lesson,"title":doc["title"],"voice":"VoxCPM2 — approved voice C","duration_seconds":cursor,"segments":segments,"reference_sha256":hashlib.sha256(ref.read_bytes()).hexdigest(),"old_audio_used":False},indent=2))
 print(json.dumps({"lesson":args.lesson,"segments":len(segments),"seconds":round(cursor,2)}),flush=True)
