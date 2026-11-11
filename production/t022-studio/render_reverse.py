#!/usr/bin/env python3
"""T02.2: a studio lesson about reversing a process. Reuses the approved art system."""
import argparse,functools,importlib.util,json,math,re,subprocess
from pathlib import Path
from PIL import Image,ImageDraw

ROOT=Path(__file__).resolve().parent
BASE=next(p for p in [ROOT.parent/'t021-studio/render_studio.py',ROOT.parent/'t021/render_studio.py'] if p.exists())
sp=importlib.util.spec_from_file_location('studio',BASE);B=importlib.util.module_from_spec(sp);sp.loader.exec_module(B)
WHITE,MUTED,DIM,GOLD,BLUE,MINT,RED=B.WHITE,B.MUTED,B.DIM,B.GOLD,B.BLUE,B.MINT,B.RED
text,rr,coin,line,eq,pill=B.text,B.rr,B.coin,B.line,B.eq,B.pill
smooth,anim,lerp,clamp=B.smooth,B.anim,B.lerp,B.clamp
TIMING=None;WORDS=None;CAPTIONS=None;DURATION=0
def norm(s):return re.sub('[^a-z0-9]','',s.lower())
@functools.lru_cache(200)
def cue(i,phrase,end=False):
 ws=[w for w in WORDS if w['segment']==i+1];got=[norm(w['text']) for w in ws];wanted=[norm(x) for x in phrase.split()]
 for j in range(len(got)-len(wanted)+1):
  if got[j:j+len(wanted)]==wanted:return ws[j+len(wanted)-1]['end'] if end else ws[j]['start']
 raise ValueError(f'Unmatched cue in scene {i+1}: {phrase}')
def rise(i,t,phrase,d=.65,delay=0):return anim(t,cue(i,phrase)+delay,cue(i,phrase)+delay+d)
def title(im,s,sub=None):
 text(im,s,640,151,38,WHITE,'bold')
 if sub:text(im,sub,640,207,20,MUTED)
def card(im,x,y,value,color=WHITE,w=198,h=128,a=1,active=False):
 if a<=0:return
 layer=Image.new('RGBA',im.size)
 rr(layer,(x-w/2,y-h/2+7,x+w/2,y+h/2+7),'#080c12',22)
 rr(layer,(x-w/2,y-h/2,x+w/2,y+h/2),'#22302e' if active else '#1e2732',22,outline='#427562' if active else '#2b3743')
 sz=60 if len(str(value))<5 else 38
 text(layer,value,x,y,sz,color,'light')
 if a<.999:layer.putalpha(layer.getchannel('A').point(lambda v:int(v*a)))
 im.alpha_composite(layer)
def arrow(im,x1,x2,y,color=DIM,progress=1):
 x=lerp(x1,x2,progress);line(im,[(x1,y),(x,y)],color,2)
 if progress>.97:
  sign=1 if x2>x1 else -1;line(im,[(x-8*sign,y-6),(x,y),(x-8*sign,y+6)],color,2)
def pipeline(im,values,ops,reverse=False,colors=None,reveals=None,active=-1,y=355):
 n=len(values);xs=[280,640,1000] if n==3 else [205,495,785,1075]
 width=208 if n==3 else 177
 colors=colors or [GOLD]+[WHITE]*(n-2)+[BLUE]
 for j,(x,v) in enumerate(zip(xs,values)):card(im,x,y,v,colors[j],w=width,a=reveals[j] if reveals else 1,active=j==active)
 for j,op in enumerate(ops):
  a,b=xs[j]+width/2+13,xs[j+1]-width/2-13
  if reverse:a,b=b,a
  arrow(im,a,b,y,MINT if reverse else MUTED)
  text(im,op,(xs[j]+xs[j+1])/2,y-47,18 if len(op)>6 else 25,MINT if reverse else MUTED,'math')
 return xs
def gridpos(n,cx,cy,cols=5,gap=47):return [(cx+(j%cols-(cols-1)/2)*gap,cy+j//cols*gap) for j in range(n)]
def coins(im,n,cx,cy,col='blue',cols=5,gap=47,size=43,a=1):
 for x,y in gridpos(n,cx,cy,cols,gap):coin(im,x,y,col,size,a)
def panelgroup(im,cx,cy,n=5,a=1,highlight=False,size=40):
 rr(im,(cx-95,cy-78,cx+95,cy+72),'#21332e' if highlight else '#1b252f',20)
 for x,y in gridpos(n,cx,cy-34,3,48):coin(im,x,y,'blue',size,a)
def fraction_group(im,cx,cy,count=4,a=1,col='blue',ghost=False):
 rr(im,(cx-100,cy-77,cx+100,cy+101),'#1b2530',18)
 if ghost:text(im,'?',cx,cy,48,DIM,'light',a)
 else:coins(im,count,cx,cy-32,col,2,55,48,a)
 text(im,str(count) if not ghost else 'one third',cx,cy+75,24,MUTED,'light',a)
def fraction_bars(im,cx,y,unit,good=True,a=1):
 for j in range(3):
  x=cx+(j-1)*82;rr(im,(x-36,y-35,x+36,y+35),'#284764' if j<2 else '#242a32',12)
  text(im,str(unit),x,y,29,BLUE if j<2 else DIM,'light',a)
 text(im,'Keep 2 of 3 equal groups',cx,y+67,16,MUTED,a=a)

def draw(im,i,t):
 q=lambda phrase,d=.65,delay=0:rise(i,t,phrase,d,delay)
 start=TIMING['segments'][i]['start_seconds'];elapsed=t-start
 if i==0:
  title(im,'The finish can reveal the start.')
  rev=t>=cue(i,'undo the last move first')
  pipeline(im,['START','?','FINISH'],['first move','last move'] if not rev else ['undo move 1','undo move 2'],reverse=rev)
  text(im,'WORK BACKWARDS',640,540,20,MINT,'bold',q('Working backwards'))
  if rev:
   u=anim(t,cue(i,'undo the last move first'),cue(i,'undo the last move first')+2)
   coin(im,lerp(1000,280,u),477,'gold',35)
 elif i==1:
  title(im,'A route back. Then a forward check.')
  pipeline(im,['START','MIDDLE','FINISH'],['undo','undo'],True)
  u=q('follow a clear route',2.3)
  if 0<u<1:coin(im,lerp(1000,280,u),474,'gold',34)
  f=q('travelling forwards again',1.5)
  if f>0:
   arrow(im,280,1000,535,MINT,f);text(im,'CHECK FORWARDS',640,578,17,MINT,'bold',f)
 elif i==2:
  title(im,'A secret number goes into a machine.')
  u=q('twenty-three',.18)
  pipeline(im,['?','?','23' if u>.5 else '?'],['×4','+3'])
  text(im,'START',280,472,14,MUTED,'bold');text(im,'FINISH',1000,472,14,MUTED,'bold')
  pill(im,'Which operation happened last?',640,558,a=q('What number went in'))
 elif i==3:
  title(im,'Undo the last move first.','Reverse +3 with −3.')
  u=anim(t,cue(i,'minus three'),cue(i,'is twenty',True))
  # The exact three added counters leave the collection.
  for j,(x,y) in enumerate(gridpos(23,890,295,5,47)):
   if j<20:coin(im,x,y,'blue',43)
   else:coin(im,x+48*u,y-155*u,'gold',43,1-u)
  text(im,'23 − 3',335,341,53,WHITE,'math');text(im,'= 20',335,429,64,MINT,'light',q('is twenty',.65))
  text(im,'BEFORE THE ADDITION',890,535,15,MUTED,'bold',q('is twenty',.65))
 elif i==4:
  title(im,'Now undo the multiplication.')
  centers=[280,520,760,1000];u=q('Twenty divided by four',1.05)
  forward=anim(t,cue(i,'five times four'),cue(i,'is twenty',True));plus=anim(t,cue(i,'twenty plus three'),cue(i,'is twenty-three',True))
  for j,cx in enumerate(centers):
   active=(j==0 and t>=cue(i,'is five') and forward<.99)
   rr(im,(cx-101,282,cx+101,444),'#21332e' if active else '#1b252f',19)
  for j,cx in enumerate(centers):
   active=(j==0 and t>=cue(i,'is five') and forward<.99)
   aa=1 if t<cue(i,'is five') else lerp(1 if j==0 else .20,1,forward)
   for k,(x,y) in enumerate(gridpos(5,cx,319,3,48)):
    # Twenty counters visibly regroup into four piles of five.
    sx,sy=gridpos(20,640,310,10,48)[j*5+k]
    coin(im,lerp(sx,x,u),lerp(sy,y,u),'blue',42,aa)
   text(im,'5' if t>=cue(i,'is five') else 'one group',cx,469,30 if t>=cue(i,'is five') else 15,MINT if active else MUTED,'light')
  if plus>0:
   for j in range(3):coin(im,584+j*56,533,'gold',42,plus,lift=40*(1-plus))
   text(im,'20 + 3 = 23',640,584,29,MINT,'math',plus)
  elif forward>0:text(im,'5 × 4 = 20',640,555,42,MINT,'math',forward)
  else:text(im,'20 ÷ 4 = 5',640,555,45,MINT,'math',q('is five'))
 elif i==5:
  title(im,'The inverse steps need the right order.')
  a=q('five point seven five',.35);b=q('two point seven five',.35)
  pipeline(im,['23','5.75' if a>.5 else '?','2.75' if b>.5 else '?'],['÷4','−3'],colors=[BLUE,WHITE,RED])
  text(im,'WRONG ORDER',640,252,16,RED,'bold')
  text(im,'2.75 × 4 + 3 = 14 ≠ 23',640,534,32,RED,'math',q('That is not five'))
  text(im,'It misses the target.',640,582,21,MUTED,a=q('The order is part'))
 elif i==6:
  zero=q('Multiplying by zero',.7)
  if zero<.95:
   title(im,'Peel away the outside operation first.')
   add=q('four x plus three',.6);remove=q('Subtracting three',1.0);divide=q('Dividing by four',1.0)
   for j in [1,2,3,0]:
    shift=q('Dividing by four',.7,.3)
    x=lerp(330,640,shift) if j==0 else 330+j*160
    card(im,x,351,'x',BLUE,w=122,h=122,a=(1-divide if j else 1)*q('Call the start x'))
   for j in range(3):coin(im,962+j*51,351-85*remove,'gold',45,add*(1-remove))
   if divide>.01: text(im,'4x ÷ 4 = x',640,525,42,MINT,'math',divide)
   elif remove>.01:text(im,'4x + 3 − 3 = 4x',640,525,42,MINT,'math',remove)
   else:text(im,'4x + 3',640,525,42,WHITE,'math',add)
  else:
   title(im,'Some moves lose information.')
   text(im,'2 × 0 = 0',350,350,49,WHITE,'math');text(im,'5 × 0 = 0',930,350,49,WHITE,'math')
   pill(im,'Same finish. Different possible starts.',640,508,RED,a=q('lose the starting information'))
 elif i==7:
  title(im,'Fractions of what remains')
  pipeline(im,['?','?','8' if q('eight counters')>.5 else '?'],['keep ½','keep ⅔'])
  text(im,'ORIGINAL',280,469,14,MUTED,'bold');text(im,'REMAINDER',640,469,14,MUTED,'bold');text(im,'FINISH',1000,469,14,MUTED,'bold')
  pill(im,'How many counters were there at the start?',640,556,a=q('How many'))
 elif i==8:
  title(im,'Restore the missing third.')
  split=q('Split them into two equal groups',1.1);restore=q('Restore the missing third',1.0)
  for cx in [380,640]:rr(im,(cx-100,278,cx+100,458),'#1b2530',20)
  for j,cx in enumerate([380,640]):
   for k,(x,y) in enumerate(gridpos(4,cx,316,2,55)):
    source_index=(k//2)*4+j*2+k%2
    sx,sy=gridpos(8,510,316,4,55)[source_index];coin(im,lerp(sx,x,split),lerp(sy,y,split),'blue',48)
   text(im,'4',cx,432,27,MUTED,'light',split)
  fraction_group(im,900,355,4,restore,'gold')
  if restore<.01:text(im,'?',900,345,48,DIM,'light')
  pill(im,'One third = 4',640,519,a=q('groups of four'))
  text(im,'8 + 4 = 12',640,579,36,MINT,'math',q('previous pile had twelve'))
 elif i==9:
  title(im,'Now undo keeping half.')
  double=q('Double it',1.1);half=q('Half of twenty-four',.85);twothirds=q('Two thirds of twelve',.85)
  for side,cx in enumerate([390,890]):
   for j in range(12):
    group=j//4;k=j%4;x=cx+(group-1)*105+(k%2-.5)*45;y=324+(k//2)*48
    aa=(1 if side==0 else double)*(1-half if side==1 else 1)
    if side==0 and group==2:aa*=1-twothirds
    coin(im,x,y,'blue' if side==0 else 'gold',42,aa,lift=(55*(1-double) if side else 0))
  if half<=.01:
   text(im,'12',390,447,40,BLUE,'light');text(im,'12',890,447,40,GOLD,'light',double);text(im,'12 × 2 = 24',640,550,43,MINT,'math',double)
  elif twothirds<=.01:text(im,'½ of 24 = 12',640,532,43,MINT,'math',half)
  else:text(im,'⅔ of 12 = 8',640,532,43,MINT,'math',twothirds)
 elif i==10:
  title(im,'Use the current whole.')
  text(im,'CURRENT PILE',350,276,15,MINT,'bold');text(im,'ORIGINAL PILE',930,276,15,MUTED,'bold')
  fraction_bars(im,350,354,4);fraction_bars(im,930,354,8,False)
  text(im,'⅔ of 12 = 8',350,485,34,MINT,'math');text(im,'⅔ of 24 = 16',930,485,34,MUTED,'math')
  pill(im,'This is the amount we keep.',350,559,a=q('two thirds of twelve'))
  text(im,'Wrong whole for the second step.',930,559,18,RED,'bold',q('not two thirds'))
 elif i==11:
  title(im,'Every intermediate pile must be whole.')
  pipeline(im,['?','?','?','7' if q('Could the final pile',.25)>.5 else '?'],['½','+1','×2'])
  pill(im,'Whole counters only',640,552,a=q('Suppose a rule'))
 elif i==12:
  title(im,'A whole-number start is not enough.')
  u1=q('three point five',.4);u2=q('two point five',.4);u3=q('get five',.4)
  pipeline(im,['5' if u3>.5 else '?','2.5' if u2>.5 else '?','3.5' if u1>.5 else '?','7'],['×2','−1','÷2'],True,colors=[MINT,RED,RED,BLUE])
  text(im,'WHOLE',205,474,15,MINT,'bold',u3);text(im,'NOT WHOLE',495,474,15,RED,'bold',u2);text(im,'NOT WHOLE',785,474,15,RED,'bold',u1)
  pill(im,'The intermediate piles break the rule.',640,565,RED,a=q('but the intermediate piles'))
 elif i==13:
  title(im,'Check a legal candidate both ways.')
  reverse=t<cue(i,'Forwards');xs=[205,495,785,1075]
  if reverse:
   u=q('eight becomes four',1);v=q('then three',.5);w=q('then six',.5)
   vals=['6' if w>.5 else '?','3' if v>.5 else '?','4' if u>.5 else '?','8']
   active=3 if u<.5 else 2 if v<.5 else 1 if w<.5 else 0
  else:
   vals=['6','3','4','8'];active=0
   for j,phrase in [(1,'six becomes three'),(2,'then four'),(3,'then eight')]:
    if t>=cue(i,phrase):active=j
  pipeline(im,vals,['×2','−1','÷2'] if reverse else ['½','+1','×2'],reverse,colors=[MINT]*4,active=active)
  if not reverse:
   for x,n in zip(xs,[6,3,4,8]):coins(im,n,x,487,'blue',4,26,24)
  pill(im,'Every pile is whole. Every move is legal.',640,574,a=q('Every pile is whole'))
 elif i==14:
  title(im,'A candidate becomes a checked solution.')
  for j,(word,sub,phrase) in enumerate([('REVERSE','the order','Reverse the order'),('UNDO','each operation','Undo each operation'),('CHECK','every state','Check every intermediate'),('VERIFY','the forward journey','Then check')]):
   x=175+j*310;u=q(phrase,.45);layer=Image.new('RGBA',im.size)
   rr(layer,(x-133,290,x+133,484),'#1e2732',20);text(layer,f'0{j+1}',x-99,325,16,MINT,'bold',align='left');text(layer,word,x,385,27,WHITE,'bold');text(layer,sub,x,445,16,MUTED)
   layer.putalpha(layer.getchannel('A').point(lambda v:int(v*u)));im.alpha_composite(layer)
  text(im,'The checks establish that it really works.',640,560,22,MUTED,a=q('the checks show'))
 else:
  title(im,'Your turn. Recover the hidden start.')
  pipeline(im,['?','?','17'],['×3','−4'])
  pill(im,'Work backwards, then prove it forwards.',640,549,a=q('Pause here'))
  text(im,'Pause and draw the journey in your notebook.',640,593,19,MUTED,a=q('draw the forward journey'))

def scene_index(t):
 for i,s in enumerate(TIMING['segments']):
  if i==len(TIMING['segments'])-1 or t<TIMING['segments'][i+1]['start_seconds']:return i
def chapter(i):
 return 'WORK BACKWARDS' if i<2 else 'THE NUMBER MACHINE' if i<7 else 'THE CHANGING WHOLE' if i<11 else 'CHECK THE RULES' if i<14 else 'MAKE IT YOURS'
def frame(t):
 i=scene_index(t);im=B.background().copy();draw(im,i,t);st=TIMING['segments'][i]['start_seconds']
 if i>0 and t<st+.28:
  prev=B.background().copy();draw(prev,i-1,st-.001);im=Image.blend(prev,im,anim(t,st,st+.28))
 text(im,'SUMMIT ONE',62,48,13,WHITE,'bold',align='left');text(im,'T02.2  /  '+chapter(i),1218,48,12,MUTED,align='right')
 for c in CAPTIONS:
  if c['start']<=t<c['end']:
   op=min(anim(t,c['start'],c['start']+.08),1-anim(t,max(c['start'],c['end']-.07),c['end']))
   text(im,c['text'],640,663,23,WHITE,'regular',op);break
 return im.convert('RGB')
def load_data(folder):
 global TIMING,WORDS,CAPTIONS,DURATION
 folder=Path(folder);TIMING=json.load(open(folder/'timing.json'));WORDS=json.load(open(folder/'words.json'))['words'];CAPTIONS=json.load(open(folder/'captions.json'));DURATION=TIMING['duration_seconds']
def main():
 p=argparse.ArgumentParser();p.add_argument('--data',default=str(ROOT));p.add_argument('--out',required=True);p.add_argument('--preview',action='store_true');p.add_argument('--start',type=float,default=0);p.add_argument('--end',type=float);a=p.parse_args();load_data(a.data)
 # Render multiple states in every scene, verifying all phrase cue lookups.
 if a.preview:
  out=Path(a.out);out.mkdir(parents=True,exist_ok=True);manifest=[]
  for i,s in enumerate(TIMING['segments']):
   for j,u in enumerate([.12,.5,.87]):
    t=s['start_seconds']+s['duration_seconds']*u;name=f'{i:02d}_{j}_{t:.2f}.jpg';frame(t).save(out/name,quality=93);manifest.append({'file':name,'time':t,'scene':i+1})
  (out/'frames.json').write_text(json.dumps(manifest,indent=2));print('Verified and previewed',len(manifest),'states.');return
 end=a.end or DURATION
 proc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','30','-i','pipe:0','-an','-c:v','libx264','-threads','3','-preset','fast','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',a.out],stdin=subprocess.PIPE)
 for n in range(math.ceil((end-a.start)*30)):
  t=a.start+n/30;proc.stdin.write(frame(t).tobytes())
  if n%300==0:print(f'{t:.1f}s / {end:.1f}s',flush=True)
 proc.stdin.close();assert proc.wait()==0
if __name__=='__main__':main()
