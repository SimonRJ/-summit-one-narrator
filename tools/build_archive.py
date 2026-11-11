import fitz,json,re,pathlib,base64,io,hashlib
import numpy as np
from PIL import Image,ImageDraw
root=pathlib.Path('/workspace/scratch/2c6b7aa92624');out=root/'archive-build';doc=fitz.open(root/'upload/AMC upper Exams(1).pdf');bank=json.loads((root/'summit-audit/private-content-audit.json').read_text())
ranges={2009:(19,28),2010:(30,38),2011:(40,47),2012:(49,57),2013:(60,68),2014:(68,77),2015:(78,87),2016:(87,93),2017:(94,102),2018:(102,109),2019:(110,119),2020:(121,131),2021:(134,143),2022:(146,154)}
keys={}
for pi,first in [(156,2007),(157,2015)]:
 tokens=doc[pi].get_text().split(); start=tokens.index(str(first+7))+1; tokens=tokens[start:]
 for i in range(30):
  row=tokens[i*9:(i+1)*9]; assert row[0]==str(i+1),(pi,i,row)
  for j,v in enumerate(row[1:]): keys.setdefault(first+j,[]).append(v)
for year,ks in keys.items(): assert len(ks)==30 and all(v in 'ABCDE' for v in ks[:25]) and all(v.isdigit() for v in ks[25:])
(out/'answer-keys.json').write_text(json.dumps(keys,indent=2))
reviews=[]
page_ink={}
def boundary(pi,top):
 if pi not in page_ink:
  pm=doc[pi].get_pixmap(matrix=fitz.Matrix(2,2),colorspace=fitz.csGRAY)
  ar=np.frombuffer(pm.samples,dtype=np.uint8).reshape(pm.height,pm.width)
  page_ink[pi]=(ar[:,64:-48]<205).sum(axis=1)
 ink=page_ink[pi];hi=int((top-2)*2);lo=max(0,hi-180)
 for y in range(hi,lo,-1):
  if max(ink[max(0,y-3):y+1],default=999)<=1:return y/2
 return top-20

for year,(lo,hi) in ranges.items():
 anchors=[]
 for pi in range(lo,hi):
  ws=json.loads((out/f'ocr-{pi}.json').read_text())['words'] if year==2014 else doc[pi].get_text('words')
  for w in ws:
   m=(re.match(r'^(\d{1,2})[.,](?:[A-Za-z]|$)',w[4]) if year==2014 else re.fullmatch(r'(\d{1,2})\.',w[4]))
   if m and w[0]<115 and w[1]<790 and 1<=int(m[1])<=30:anchors.append((int(m[1]),pi,w[1]))
 anchors.sort(key=lambda z:(z[1],z[2])); assert [x[0] for x in anchors]==list(range(1,28 if year==2014 else 31)),(year,anchors)
 qs=[]
 for idx,(q,pi,top) in enumerate(anchors):
  nexta=anchors[idx+1] if idx+1<len(anchors) and anchors[idx+1][1]==pi else (q+1,pi,785)
  crops=[];raw=[];rects=[]
  for pageid in range(pi,nexta[1]+1):
   y0=boundary(pi,top) if pageid==pi else 45
   y1=boundary(pageid,nexta[2]) if nexta[2]!=785 else 785
   if y1-y0<15:continue
   page=doc[pageid];rect=fitz.Rect(32,y0,page.rect.width-24,min(y1,785));pix=page.get_pixmap(matrix=fitz.Matrix(1.7,1.7),clip=rect)
   crops.append(Image.open(io.BytesIO(pix.tobytes('png'))).convert('RGB'));raw.append(page.get_text(clip=rect));rects.append([pageid+1,*list(rect)])
  width=max(x.width for x in crops);im=Image.new('RGB',(width,sum(x.height for x in crops)+16*(len(crops)-1)),'white');y=0
  for c in crops: im.paste(c,(0,y));y+=c.height+16
  imagepath=out/f'{year}-{q:02}.webp';im.save(imagepath,format='WEBP',quality=92,method=6)
  data=base64.b64encode(imagepath.read_bytes()).decode();image=f'<img class="source-question" alt="Original {year} AMC Upper Primary question {q}, including all diagrams and answer choices" src="data:image/webp;base64,{data}">'
  known=next((p for p in bank if f'{year} Upper Primary Q{q}' in p['source_label'].split(' / ')),None)
  if known:assert str(known['answer'])==keys[year][q-1],(year,q,known['answer'],keys[year][q-1])
  qs.append({'exam_id':f'amc-up-{year}','question_number':q,'question_type':'multiple_choice' if q<=25 else 'integer','stem':f'{year} AMC Upper Primary · Question {q}. Read the original question and choices below.','choices':['Option A','Option B','Option C','Option D','Option E'] if q<=25 else [],'answer':keys[year][q-1],'explanation':known['solution_text'] if known else None,'marks':3 if q<=10 else 4 if q<=20 else 5 if q<=25 else q-20,'image_ref':image,'category':known['category'] if known else 'archive','metadata':{'source_pages':[r[0] for r in rects],'source_rects':rects,'source_text':'\n'.join(raw) if year!=2014 else '', 'explanation_status':'worked_solution' if known else 'answer_key_only','source_fidelity':'original_question_crop','image_sha256':hashlib.sha256(imagepath.read_bytes()).hexdigest()}})
  reviews.append({'year':year,'question':q,'file':str(imagepath),'rects':rects})
 if year==2014:
  for q in [28,29,30]:
   known=next(p for p in bank if p['source_label']==f'2014 Upper Primary Q{q}');assert str(known['answer'])==keys[year][q-1]
   qs.append({'exam_id':'amc-up-2014','question_number':q,'question_type':'integer','stem':known['prompt'],'choices':[],'answer':keys[year][q-1],'explanation':known['solution_text'],'marks':q-20,'image_ref':None,'category':known['category'],'metadata':{'source_fidelity':'existing_authenticated_archive_transcription','source_problem':known['id'],'explanation_status':'worked_solution'}})
 exam={'id':f'amc-up-{year}','title':f'{year} AMC Upper Primary','year':year,'division':'Upper Primary','student_year':None,'duration_minutes':60,'max_score':135,'source_type':'authentic_amc_past_paper','source_rights':'user_supplied_past_paper','question_count':30,'metadata':{'source':'User supplied AMC upper Exams PDF (2007–2022)','source_sha256':hashlib.sha256((root/'upload/AMC upper Exams(1).pdf').read_bytes()).hexdigest(),'answer_key':'Archive table, PDF pages 157–158','fidelity_audit':'Question crops retain original diagrams and options; all 30 keys checked against source table','special_note':'Q28–30 recovered from existing authenticated archive transcriptions; supplied scan ends at Q27' if year==2014 else None,'solutions_note':'Worked explanations included where available; remaining questions have verified source answer keys only.','fidelity_audit_date':'2026-11-11'}}
 assert len(qs)==30 and sum(q['marks'] for q in qs)==135
 (out/f'import-{year}.json').write_text(json.dumps({'exam':exam,'questions':qs},ensure_ascii=False))
 print(year,len(qs),(out/f'import-{year}.json').stat().st_size,flush=True)
(out/'crop-manifest.json').write_text(json.dumps(reviews,indent=2))
# Contact sheets make all crop boundaries reviewable without re-typesetting a question.
for year in ranges:
 files=sorted(out.glob(f'{year}-*.webp'));thumbs=[]
 for f in files:
  im=Image.open(f);im.thumbnail((255,330));t=Image.new('RGB',(270,360),'#dae1e8');t.paste(im,(7,25));ImageDraw.Draw(t).text((8,5),f.stem,fill='black');thumbs.append(t)
 for offset in range(0,len(thumbs),12):
  page=Image.new('RGB',(1080,1080),'white')
  for j,t in enumerate(thumbs[offset:offset+12]):page.paste(t,((j%4)*270,(j//4)*360))
  page.save(out/f'review-{year}-{offset//12}.jpg',quality=88)
