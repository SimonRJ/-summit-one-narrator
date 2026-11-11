#!/usr/bin/env python3
"""T02.1 studio edition. Deterministic animation using the existing audio timeline.

No generated speech, no camera orbit, no decorative grids. Rendered ceramic
counters retain identity through transfers. Coordinates are authored at 1280x720
and rasterised at 1920x1080. Timing comes from the published narration's VTT.
"""
import argparse, functools, json, math, os, re, subprocess
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT=Path(__file__).resolve().parent
S=1.5; W=1920; H=1080; FPS=30; DURATION=212.926
WHITE='#f2f1ed'; MUTED='#a5adb7'; DIM='#65717e'; GOLD='#eeb765'; BLUE='#7eb5f3'; MINT='#9cdbbc'; RED='#f39299'
FONTDIR='/usr/share/fonts/truetype/open-sans'
def clamp(v):return max(0,min(1,v))
def smooth(v):
 v=clamp(v);return v*v*v*(v*(v*6-15)+10)
def anim(t,a,b):return smooth((t-a)/(b-a))
def lerp(a,b,u):return a+(b-a)*u
def rgb(c):return tuple(int(c[i:i+2],16) for i in (1,3,5)) if isinstance(c,str) else c
@functools.lru_cache(200)
def font(size,weight='regular'):
 p=f'{FONTDIR}/OpenSans-'+{'regular':'Regular','light':'Light','bold':'Semibold','heavy':'Bold'}.get(weight,'Regular')+'.ttf'
 if weight=='math':p='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
 return ImageFont.truetype(p,round(size*S))
@functools.lru_cache(1800)
def label(s,size,color=WHITE,weight='regular'):
 f=font(size,'math' if '→' in str(s) else weight);box=f.getbbox(str(s));w=round(f.getlength(str(s)))+12;h=box[3]-box[1]+12
 im=Image.new('RGBA',(max(1,w),max(1,h)))
 ImageDraw.Draw(im).text((6,6-box[1]),str(s),font=f,fill=rgb(color)+(255,))
 return im
def text(im,s,x,y,size=28,color=WHITE,weight='regular',a=1,align='center'):
 if a<=0:return
 l=label(str(s),size,color,weight)
 if a<.998:l=l.copy();l.putalpha(l.getchannel('A').point(lambda p:int(p*clamp(a))))
 px=round(x*S);py=round(y*S)
 if align=='center':px-=l.width//2
 elif align=='right':px-=l.width
 im.alpha_composite(l,(px,py-l.height//2))
def rr(im,box,fill,r=18,outline=None,width=1):
 ImageDraw.Draw(im).rounded_rectangle(tuple(round(x*S) for x in box),radius=round(r*S),fill=rgb(fill),outline=rgb(outline) if outline else None,width=round(width*S))
def line(im,pts,color,width=2):ImageDraw.Draw(im).line([(round(x*S),round(y*S)) for x,y in pts],fill=rgb(color),width=round(width*S),joint='curve')
def pill(im,s,x,y,color=MINT,size=18,a=1):
 l=label(s,size,color,'bold');w=l.width/S+32
 if a<1:
  layer=Image.new('RGBA',im.size);rr(layer,(x-w/2,y-23,x+w/2,y+23),'#1d2c28',23);text(layer,s,x,y,size,color,'bold');layer.putalpha(layer.getchannel('A').point(lambda p:int(p*a)));im.alpha_composite(layer)
 else:rr(im,(x-w/2,y-23,x+w/2,y+23),'#1d2c28',23);text(im,s,x,y,size,color,'bold')
@functools.lru_cache(1)
def background():
 yy,xx=np.mgrid[0:H,0:W];g=np.exp(-(((xx-W*.52)/(W*.7))**2+((yy-H*.44)/(H*.62))**2)*3)
 arr=np.zeros((H,W,4),dtype=np.uint8)
 for k,(a,b) in enumerate([(13,7),(18,9),(25,11)]):arr[:,:,k]=(a+b*g).astype('uint8')
 arr[:,:,3]=255
 return Image.fromarray(arr,'RGBA')
@functools.lru_cache(256)
def coin_asset(color,size):
 src=Image.open(ROOT/'assets'/f'{color}.png').convert('RGBA');bbox=src.getbbox();src=src.crop((bbox[0]-3,bbox[1]-3,bbox[2]+3,bbox[3]+3))
 side=round(size*S);src.thumbnail((side,side),Image.Resampling.LANCZOS)
 pad=round(12*S);out=Image.new('RGBA',(src.width+2*pad,src.height+2*pad))
 sh=Image.new('RGBA',out.size);d=ImageDraw.Draw(sh);d.ellipse((pad+3,pad+src.height*.45,pad+src.width-3,pad+src.height+8*S),fill=(0,0,0,110));sh=sh.filter(ImageFilter.GaussianBlur(6*S));out.alpha_composite(sh);out.alpha_composite(src,(pad,pad));return out
def coin(im,x,y,col='gold',size=54,a=1,lift=0):
 if a<=0:return
 spr=coin_asset(col,round(size))
 if a<.998:spr=spr.copy();spr.putalpha(spr.getchannel('A').point(lambda v:int(v*a)))
 im.alpha_composite(spr,(round(x*S-spr.width/2),round((y-lift)*S-spr.height/2)))
def positions(n,cx,cy=354,spacing=55):
 # Stable slots ensure that adding/removing counters never rearranges existing ones.
 return [(cx+(j%5-2)*spacing,cy+(j//5)*55) for j in range(n)]
def group(im,n,cx,col,cy=354,colors=None,a=1,size=54):
 for j,(x,y) in enumerate(positions(n,cx,cy)):coin(im,x,y,colors[j] if colors else col,size,a)
def title(im,s,sub=None,a=1):
 text(im,s,640,154,39,WHITE,'bold',a)
 if sub:text(im,sub,640,207,20,MUTED,'regular',a)
def quantities(im,left,right,y=485):
 text(im,left,350,y,49,GOLD,'light');text(im,right,930,y,49,BLUE,'light')
 text(im,'LEFT PILE',350,y+43,13,MUTED,'bold');text(im,'RIGHT PILE',930,y+43,13,MUTED,'bold')
def total(im,n=12,y=350,a=1):
 text(im,'TOTAL',640,y-32,13,MUTED,'bold',a);text(im,n,640,y+7,58,MINT,'light',a)
def eq(im,parts,y=340,size=58,a=1):
 widths=[label(s,size,c,'math').width/S for s,c in parts];x=640-sum(widths)/2
 for (s,c),w in zip(parts,widths):text(im,s,x+w/2,y,size,c,'math',a);x+=w
def lanes(im,n1,n2,step=0,y=330,size=48,gap=50,start=350,addition=None,show_gap=True):
 text(im,str(n1),238,y,46,GOLD,'light');text(im,str(n2),238,y+92,46,BLUE,'light')
 for row,n,col in [(0,n1,'gold'),(1,n2,'blue')]:
  for j in range(n):coin(im,start+j*gap,y+row*92,col,size)
 if addition:
  old1,old2,u=addition
  for row,old,col in [(0,old1,'gold'),(1,old2,'blue')]:
   for j in range(2):coin(im,start+(old+j)*gap,y+row*92,col,size,a=clamp(u*3),lift=65*(1-u))
 if show_gap:
  # This single bracket describes the unmatched counters, not the background.
  x0=start+n1*gap-gap*.38;x1=start+(n2-1)*gap+gap*.38
  if n2>n1:line(im,[(x0,y+128),(x0,y+137),(x1,y+137),(x1,y+128)],MINT,1.5)
  pill(im,f'GAP  {n2-n1}',1080,y+46)

def scene(im,i,t):
 if i==0:
  title(im,'Find what stays the same.')
  # Twelve persistent objects shift from a circular arrangement to two rows.
  u=anim(t,1.6,7.8)
  for j in range(12):
   ang=j*math.tau/12-math.pi/2
   x0,y0=640+230*math.cos(ang),380+122*math.sin(ang)
   x1,y1=475+(j%6)*66,350+(j//6)*78
   coin(im,lerp(x0,x1,u),lerp(y0,y1,u),'gold' if j<6 else 'blue',54)
  text(im,'INVARIANT',640,268,19,MINT,'bold',anim(t,3.8,4.6))
  pill(im,'12 counters. Every arrangement.',640,524,a=anim(t,5.5,7.0))
  for j,(s,a) in enumerate([('A total',10.04),('A difference',11.64),('A remainder',13.42)]):text(im,s,340+j*300,575,19,MUTED,a=anim(t,a,a+.35))
 elif i==1:
  title(im,'You don’t need to try every move.')
  for j,(a,b) in enumerate([(5,7),(7,5),(6,6)]):
   u=anim(t,18+j*.95,18.6+j*.95);cx=330+j*310
   text(im,f'{a} + {b}',cx,332,51,WHITE,'light',u)
   text(im,'12',cx,408,38,MINT,'bold',u)
  text(im,'Different routes. The same total.',640,493,24,MUTED,a=anim(t,23,24))
  pill(im,'10 + 10 = 20   is out of reach',640,558,RED,a=anim(t,28.25,29.3))
 elif i==2:
  title(im,'A small move. A powerful proof.')
  cards=[('01','MOVE','Watch the counters',32.7),('02','NOTICE','Find what stays fixed',35.52),('03','PROVE','Explain why it works',40.7),('04','APPLY','Try a new puzzle',43.32)]
  for j,(num,word,desc,a) in enumerate(cards):
   u=anim(t,a,a+.65);x=178+j*308
   layer=Image.new('RGBA',im.size);rr(layer,(x-130,285,x+130,480),'#1c252e',20)
   text(layer,num,x-98,320,16,MINT,'bold',align='left');text(layer,word,x,378,27,WHITE,'bold');text(layer,desc,x,432,15,MUTED)
   layer.putalpha(layer.getchannel('A').point(lambda p:int(p*u)));im.alpha_composite(layer)
 elif i in (3,4,5,6,8):
  heads={3:'Two piles. One simple rule.',4:'What can no legal move change?',5:'Follow the same two counters.',6:'What leaves must arrive.',8:'The arrangement changes. The total stays.'}
  title(im,heads[i], 'Transfer counters between the piles.' if i==3 else None)
  moved=i in (6,8)
  u=anim(t,67.1,69.3) if i==5 else (1 if moved else 0)
  group(im,5,350,'gold');group(im,5,930,'blue')
  for j in range(2):
   fr=positions(7,930)[5+j];to=positions(7,350)[5+j]
   v=anim(t,67.1+j*.2,69.1+j*.2) if i==5 else u
   coin(im,lerp(fr[0],to[0],v),lerp(fr[1],to[1],v)-125*math.sin(v*math.pi),'blue',54)
  lcount=7 if u>=.999 else 5;rCount=5 if u>.001 else 7
  quantities(im,lcount,rCount)
  if i==3:
   text(im,'TARGET',640,290,13,MUTED,'bold',anim(t,56,56.5));text(im,'10 + 10 ?',640,330,31,WHITE,'bold',anim(t,56,56.5))
  elif i==4:total(im,12,a=anim(t,63.08,64.4))
  elif i==5:
   total(im,12,a=anim(t,66.1,66.8))
   if .001<u<.999:text(im,'2 in transit',640,470,16,BLUE)
   pill(im,'The total is still twelve',640,564,a=anim(t,74.5,75.5))
  elif i==6:
   eq(im,[('−t',BLUE),(' + ',MUTED),('t',GOLD),(' = 0',MINT)],265,38,a=anim(t,77,78.2));total(im,12)
   text(im,'Nothing created. Nothing lost.',640,567,22,MUTED,a=anim(t,82.1,83))
  else:total(im,12);pill(im,'This is an invariant.',640,565,a=anim(t,96,98))
 elif i==7:
  title(im,'An impossibility proof')
  rr(im,(145,278,600,516),'#2b2128',24);rr(im,(680,278,1135,516),'#1b2b28',24)
  text(im,'10 + 10 = 20',372,337,38,WHITE,'light');text(im,'20 ≠ 12',372,407,44,RED,'math');text(im,'IMPOSSIBLE',372,475,16,RED,'bold')
  a=anim(t,90.5,91.2);text(im,'6 + 6 = 12',908,337,38,WHITE,'light',a);text(im,'12 = 12',908,407,44,MINT,'math',a);text(im,'POSSIBLE',908,475,16,MINT,'bold',a)
 elif i==9:
  title(im,'New rule. New invariant.','Add two new counters to each pile.')
  u=anim(t,105.6,107.6);group(im,5,350,'gold');group(im,7,930,'blue')
  for n,x,col in [(5,350,'gold'),(7,930,'blue')]:
   for j,(xx,yy) in enumerate(positions(n+2,x)[n:]):coin(im,xx,yy,col,54,clamp(u*3),75*(1-u))
  quantities(im,7 if u>.999 else 5,9 if u>.999 else 7)
  text(im,'+2',350,277,32,GOLD,'bold',u);text(im,'+2',930,277,32,BLUE,'bold',u)
  total(im,16 if u>.999 else 12)
 elif i==10:
  title(im,'The total grows. The gap stays.')
  u=anim(t,110.808,112.15)
  for n,cx,col,row in [(7,350,'gold',0),(9,930,'blue',1)]:
   for j,(x,y) in enumerate(positions(n,cx)):
    coin(im,lerp(x,350+j*53,u),lerp(y,330+row*92,u),col,lerp(54,48,u))
   text(im,str(n),238,330+row*92,46,GOLD if row==0 else BLUE,'light',u)
  if t>=116.6:
   line(im,[(700,458),(700,467),(795,467),(795,458)],MINT,1.5)
   pill(im,'GAP  2',1080,376,a=anim(t,116.6,117.3))
  text(im,'TOTAL',444,526,14,MUTED,'bold');text(im,'12 → 16',444,565,34,RED,'light',anim(t,111,112))
  text(im,'DIFFERENCE',844,526,14,MUTED,'bold',anim(t,116.6,117.2));text(im,'9 − 7 = 2',844,565,34,MINT,'math',anim(t,116.6,117.2))
 elif i==11:
  title(im,'Equal additions keep the gap fixed.')
  u1=anim(t,122.48,123.8);u2=anim(t,124.94,126.5)
  step=2 if u2>=.999 else 1 if u1>=.999 else 0;n1,n2=5+2*step,7+2*step
  add=(n1,n2,u2 if step else u1) if (0<u2<.999 or 0<u1<.999) else None
  lanes(im,n1,n2,start=330,gap=51,size=47,addition=add)
  text(im,'+2 to both piles',640,522,26,MUTED)
  pill(im,'The gap is always 2',640,569,a=anim(t,127.76,128.5))
 elif i==12:
  title(im,'From a pattern to a proof.')
  a=anim(t,132.46,133.4)
  rr(im,(265,292,535,440),'#302a23',24);rr(im,(745,292,1015,440),'#202c3b',24)
  text(im,'A',400,361,72,GOLD,'math',a);text(im,'B',880,361,72,BLUE,'math',a)
  u=anim(t,134.78,137.3)
  text(im,'A + 2',400,505,45,GOLD,'math',u);text(im,'B + 2',880,505,45,BLUE,'math',u)
 elif i==13:
  title(im,'The equal changes cancel.')
  if t<140.265:
   eq(im,[('(A + 2)',GOLD),(' − ',MUTED),('(B + 2)',BLUE)],350,58)
   text(im,'Subtract the new pile sizes',640,476,22,MUTED)
  else:
   k=anim(t,142.0,143.55);u=anim(t,143.59,144.6)
   # Distribute the minus first. Only then cancel +2 with −2.
   text(im,'A',lerp(370,556,u),350,62,GOLD,'math');text(im,'−',lerp(640,640,u),350,62,WHITE,'math');text(im,'B',lerp(765,724,u),350,62,BLUE,'math')
   text(im,'+2',lerp(500,585,k),350+72*k,54,MINT,'math',1-k)
   text(im,'−2',lerp(910,695,k),350+72*k,54,MINT,'math',1-k)
   text(im,'+2 − 2 = 0',640,492,30,MINT,'math',anim(t,140.4,141.2)*(1-u))
   pill(im,'A − B is unchanged',640,497,a=anim(t,144.1,145.0))
 elif i==14:
  title(im,'Transfers preserve the total.')
  if t<153.0:
   text(im,'A − t',400,350,63,GOLD,'math',anim(t,150.1,151.3));text(im,'B + t',880,350,63,BLUE,'math',anim(t,151.9,153))
   text(im,'LOSES t',400,449,16,MUTED,'bold',anim(t,150.1,151.3));text(im,'GAINS t',880,449,16,MUTED,'bold',anim(t,151.9,153))
  elif t<156.65:eq(im,[('(A − t)',GOLD),(' + ',WHITE),('(B + t)',BLUE)],350,56)
  else:
   k=anim(t,156.65,158.0);text(im,'A',lerp(365,555,k),350,63,GOLD,'math');text(im,'+',640,350,63,WHITE,'math');text(im,'B',lerp(770,725,k),350,63,BLUE,'math')
   text(im,'−t',lerp(500,580,k),350+70*k,55,MINT,'math',1-k);text(im,'+t',lerp(910,700,k),350+70*k,55,MINT,'math',1-k)
   pill(im,'A + B is unchanged',640,497,a=anim(t,157.8,158.6))
 elif i==15:
  title(im,'Always check the actual rule.')
  rr(im,(115,267,620,551),'#202932',22);rr(im,(660,267,1165,551),'#202932',22)
  text(im,'TRANSFER',367,311,18,BLUE,'bold');text(im,'ADD EQUALLY',912,311,18,GOLD,'bold')
  text(im,'5 + 7  →  6 + 6',367,373,29,WHITE,'light',anim(t,161.1,162.1));text(im,'Total stays 12',367,434,28,MINT,'bold',anim(t,161.1,162.1));text(im,'Gap: 2 → 0',367,493,24,MUTED,a=anim(t,164,165))
  text(im,'5 + 7  →  7 + 9',912,373,29,WHITE,'light',anim(t,165.1,166));text(im,'Gap stays 2',912,434,28,MINT,'bold',anim(t,166,167));text(im,'Total: 12 → 16',912,493,24,MUTED,a=anim(t,167.6,168.4))
 elif i==16:
  title(im,'Your turn. Can you reach the target?','Each move adds 2 to both piles.')
  lanes(im,4,9,start=350,gap=53,show_gap=False)
  text(im,'START',238,259,14,MUTED,'bold')
  text(im,'TARGET',640,515,14,MUTED,'bold',anim(t,177.44,177.9));text(im,'18  and  23',640,562,40,WHITE,'light',anim(t,177.44,177.9))
 elif i==17:
  title(im,'Seven moves reach both targets.')
  raw=clamp((t-182.9)/3.05)*7;k=min(7,int(raw))
  n1,n2=4+2*k,9+2*k;u=smooth(raw-k)
  addition=(n1,n2,u) if k<7 and raw>0 else None
  lanes(im,n1,n2,start=325,gap=29,size=29,show_gap=True,addition=addition)
  text(im,f'{k} / 7 moves',640,266,22,MUTED,a=anim(t,182.9,183.25))
  eq(im,[('7 × 2',WHITE),(' = 14',MINT)],526,40,a=anim(t,182.9,184))
  text(im,'4 + 14 = 18        9 + 14 = 23',640,579,25,WHITE,'math',anim(t,186.3,187.2))
 elif i==18:
  title(im,'A different target breaks the rule.')
  text(im,'START',360,285,15,MUTED,'bold');text(im,'9 − 4',360,352,48,WHITE,'math');text(im,'5',360,437,67,MINT,'light')
  text(im,'TARGET',920,285,15,MUTED,'bold');text(im,'22 − 18',920,352,48,WHITE,'math');text(im,'4',920,437,67,RED,'light',anim(t,190.64,191.6))
  text(im,'≠',640,426,52,RED,'math',anim(t,191,192));pill(im,'Impossible: the gap would change.',640,556,RED,a=anim(t,193.74,194.5))
 elif i==19:
  title(im,'One move can tell the whole story.')
  for j,(word,sub,a) in enumerate([('INSPECT','one legal move',200.96),('CANCEL','the equal changes',202.0),('CONCLUDE','what always stays fixed',204.0)]):
   u=anim(t,a,a+.5);x=300+j*340
   text(im,f'0{j+1}',x,317,18,MINT,'bold',u);text(im,word,x,382,29,WHITE,'bold',u);text(im,sub,x,439,19,MUTED,a=u)
  eq(im,[('+2',GOLD),(' − 2',BLUE),(' = 0',MINT)],540,38,a=anim(t,198.3,199.5))
 else:
  text(im,'MAKE THE IDEA YOURS',640,192,16,MINT,'bold')
  text(im,'One move.',640,300,56,WHITE,'light')
  text(im,'One equation.',640,381,56,WHITE,'light',anim(t,208.6,209.4))
  text(im,'Your proof.',640,462,56,MINT,'bold',anim(t,210.0,210.8))
  text(im,'Pause and try it in your notebook.',640,560,23,MUTED,a=anim(t,207,207.6))

TIMES=[0,16.255,31.384,47.059,59.669,66.075,76.599,85.3,93.738,102.71,110.808,119.552,129.617,138.419,147.931,159.296,170.021,179.605,188.465,196.415,206.925,DURATION]
def parse_vtt(path):
 entries=[]
 def seconds(s):
  a,b,c=map(float,s.split(':'));return 3600*a+60*b+c
 for block in Path(path).read_text().split('\n\n'):
  ls=block.splitlines()
  if ls and '-->' in ls[0]:
   a,b=ls[0].split(' --> ');entries.append((seconds(a),seconds(b),' '.join(ls[1:])))
 return entries
CAPTIONS=[]
def caption(im,t):
 for a,b,s in CAPTIONS:
  if a<=t<b:
   # Preserve measured phrase timing; no invented word timing/highlighting.
   op=min(anim(t,a,a+.09),1-anim(t,max(a,b-.08),b))
   text(im,s,640,663,23,WHITE,'regular',op);return
def chapter(t):
 for start,name in [(196,'THE TAKEAWAY'),(170,'TRY IT'),(129.6,'THE PROOF'),(102.7,'THE DIFFERENCE'),(47,'THE TOTAL'),(0,'INVARIANTS')]:
  if t>=start:return name
def frame(t):
 i=next((j for j in range(21) if t<TIMES[j+1]),20)
 im=background().copy();scene(im,i,t)
 # Short editorial dissolves, never perpetual camera movement.
 if i>0 and t<TIMES[i]+.30:
  prev=background().copy();scene(prev,i-1,TIMES[i]-.001);im=Image.blend(prev,im,anim(t,TIMES[i],TIMES[i]+.30))
 text(im,'SUMMIT ONE',62,48,13,WHITE,'bold',align='left')
 text(im,'T02.1  /  '+chapter(t),1218,48,12,MUTED,'regular',align='right')
 caption(im,t)
 return im.convert('RGB')
def main():
 global CAPTIONS,S,W,H
 p=argparse.ArgumentParser();p.add_argument('--vtt',default=str(ROOT/'source/T02.1.vtt'));p.add_argument('--out',default=str(ROOT/'T02.1_studio_visual.mp4'));p.add_argument('--preview',action='store_true');p.add_argument('--start',type=float,default=0);p.add_argument('--end',type=float,default=DURATION);p.add_argument('--fps',type=int,default=FPS);p.add_argument('--scale',type=float,default=1.5);a=p.parse_args()
 S=a.scale;W=round(1280*S);H=round(720*S);CAPTIONS=parse_vtt(a.vtt)
 if a.preview:
  out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
  ts=[8,27,44,57.5,64.8,68.2,74.5,83,92.4,99.4,107.8,118,128.4,137.6,140.8,144.9,158.5,168.8,178.3,187.7,194.9,205.3,211.8]
  for j,t in enumerate(ts):frame(t).save(out/f'{j:02d}_{t:.1f}.jpg',quality=93)
  print('Previewed',len(ts),'key states',flush=True);return
 out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True)
 proc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(a.fps),'-i','pipe:0','-an','-c:v','libx264','-threads','3','-preset','fast','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],stdin=subprocess.PIPE)
 count=math.ceil((a.end-a.start)*a.fps)
 for n in range(count):
  proc.stdin.write(frame(a.start+n/a.fps).tobytes())
  if n%(a.fps*10)==0:print(f'{a.start+n/a.fps:.1f}s / {a.end:.1f}s',flush=True)
 proc.stdin.close();assert proc.wait()==0
if __name__=='__main__':main()
