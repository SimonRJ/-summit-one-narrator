"""Align the written script to its final audio; preserve the approved caption text."""
import argparse,difflib,json,re,subprocess
from pathlib import Path
import numpy as np
from faster_whisper import WhisperModel
def norm(s):
 s=re.sub('[^a-z0-9]','',s.lower())
 return {'ex':'x','24':'twentyfour','4':'four','3':'three','2':'two','1':'one','0':'zero','8':'eight','7':'seven','5':'five','6':'six','12':'twelve','17':'seventeen','23':'twentythree','32':'thirtytwo','9':'nine','11':'eleven','20':'twenty','22':'twentytwo','30':'thirty','42':'fortytwo'}.get(s,s)
def stamp(t):
 return f'{int(t//3600):02d}:{int(t//60)%60:02d}:{t%60:06.3f}'
def main():
 p=argparse.ArgumentParser();p.add_argument('--audio',required=True);p.add_argument('--timing',required=True);p.add_argument('--out',required=True);a=p.parse_args()
 timing=json.load(open(a.timing));out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
 samples=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',a.audio,'-ac','1','-ar','16000','-f','f32le','-']),dtype=np.float32)
 model=WhisperModel('base.en',device='cpu',compute_type='int8',cpu_threads=2)
 words=[];heard=[];seg_reports=[]
 for seg in timing['segments']:
  st=seg['start_seconds'];en=st+seg['duration_seconds']
  pieces,_=model.transcribe(samples[int(st*16000):int(en*16000)],word_timestamps=True,beam_size=5,condition_on_previous_text=False)
  hw=[{'text':w.word.strip(),'start':float(w.start)+st,'end':float(w.end)+st} for piece in pieces for w in piece.words or []]
  heard.extend(hw);target=seg['text'].split();ws=[{'text':x,'segment':seg['index']} for x in target]
  sm=difflib.SequenceMatcher(None,[norm(x) for x in target],[norm(x['text']) for x in hw],autojunk=False)
  for tag,i0,i1,j0,j1 in sm.get_opcodes():
   if tag=='equal':
    for i,j in zip(range(i0,i1),range(j0,j1)):ws[i].update(start=hw[j]['start'],end=hw[j]['end'],aligned=True)
  k=0
  while k<len(ws):
   if 'start' in ws[k]:k+=1;continue
   z=k
   while z<len(ws) and 'start' not in ws[z]:z+=1
   lo=ws[k-1]['end'] if k else st;hi=ws[z]['start'] if z<len(ws) else en
   for j in range(k,z):ws[j].update(start=lo+(hi-lo)*(j-k)/(z-k),end=lo+(hi-lo)*(j-k+1)/(z-k),aligned=False)
   k=z
  for j,w in enumerate(ws):
   w['start']=max(st,min(en,w['start']));w['end']=max(w['start'],min(en,w['end']))
  seg_reports.append({'segment':seg['index'],'words':len(ws),'matched':sum(w['aligned'] for w in ws)})
  words.extend(ws)
 groups=[];cur=[]
 for w in words:
  if cur and (w['segment']!=cur[-1]['segment'] or len(' '.join(v['text'] for v in cur+[w]))>62 or len(cur)>=11):groups.append(cur);cur=[]
  cur.append(w)
  if len(cur)>=3 and w['text'].endswith(('.', '?','!')):groups.append(cur);cur=[]
 if cur:groups.append(cur)
 caps=[{'start':g[0]['start'],'end':g[-1]['end'],'text':' '.join(x['text'] for x in g)} for g in groups]
 for i,c in enumerate(caps[:-1]):c['end']=min(c['end']+.06,caps[i+1]['start'])
 pct=100*sum(w['aligned'] for w in words)/len(words)
 report={'match_percent':round(pct,2),'segments':seg_reports,'words':len(words),'caption_layers':1,'method':'per-sentence audio alignment; unmatched words bounded by matched neighbours'}
 (out/'heard-words.json').write_text(json.dumps(heard,indent=2))
 assert pct>=90,report
 (out/'words.json').write_text(json.dumps({'words':words,'alignment':report},indent=2))
 (out/'captions.json').write_text(json.dumps(caps,indent=2))
 (out/'alignment-qa.json').write_text(json.dumps(report,indent=2))
 (out/'ReefWelcome.vtt').write_text('WEBVTT\n\n'+''.join(f"{stamp(c['start'])} --> {stamp(c['end'])}\n{c['text']}\n\n" for c in caps))
 print(json.dumps(report,indent=2))
if __name__=='__main__':main()
