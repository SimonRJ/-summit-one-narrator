"""Original mathematical animation. Black canvas, cyan objects, gold emphasis.
All narrative actions use word timestamps from the completed synthetic speech.
"""
import argparse,functools,json,math,re,subprocess
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path('build/amc2025-q17');W,H=1920,1080;S=1.5;FPS=30
WHITE='#f7f7f7';BLUE='#28bbee';GOLD='#ffd36a';DIM='#657079';BLACK='#000000'
X=[380,510,640,770,900];Y=[510,380,250];SIZE=130
TIMING=None;WORDS=None
@functools.lru_cache(150)
def font(size,style='math'):
 p='/usr/share/fonts/truetype/dejavu/DejaVuSerif'+('-Italic' if style=='italic' else '')+'.ttf'
 if style=='sans':p='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
 return ImageFont.truetype(p,round(size*S))
def clamp(x):return max(0,min(1,x))
def smooth(x):x=clamp(x);return x*x*(3-2*x)
def anim(t,a,d=.55):return smooth((t-a)/d)
def lerp(a,b,u):return a+(b-a)*u
def rgb(c,a=1):return tuple(round(int(c[j:j+2],16)*a) for j in [1,3,5])
def text(im,s,x,y,size=36,color=WHITE,style='math',a=1):
 if a<=0:return
 d=ImageDraw.Draw(im);d.text((round(x*S),round(y*S)),str(s),font=font(size,style),fill=rgb(color,a),anchor='mm',stroke_width=0)
def line(im,pts,color=WHITE,width=1.4,a=1):
 if a>0:ImageDraw.Draw(im).line([(round(x*S),round(y*S)) for x,y in pts],fill=rgb(color,a),width=max(1,round(width*S)),joint='curve')
def box(im,x,y,v='',color=WHITE,a=1,fill=None):
 d=ImageDraw.Draw(im);r=SIZE/2
 rect=[round(z*S) for z in [x-r,y-r,x+r,y+r]]
 if fill:d.rectangle(rect,fill=rgb(fill,a*.12))
 d.rectangle(rect,outline=rgb(color,a),width=round(1.3*S))
 if v!='':text(im,v,x,y,44,color,a=a)
def bezier(p0,p1,u,lift=30):
 return (lerp(p0[0],p1[0],u),lerp(p0[1],p1[1],u)-4*u*(1-u)*lift)
def flight(im,v,p0,p1,u,color=BLUE,size=38,lift=30,a=1):
 x,y=bezier(p0,p1,u,lift);text(im,v,x,y,size,color,a=a)
def ray(im,p0,p1,u,color=BLUE):
 pts=[bezier(p0,p1,k/40,10) for k in range(max(1,int(40*u))+1)]
 line(im,pts,color,1.5,a=.7)
def norm(s):return re.sub('[^a-z0-9]','',s.lower())
@functools.lru_cache(100)
def cue(i,phrase):
 ws=[w for w in WORDS if w['segment']==i+1];got=[norm(w['text']) for w in ws];want=[norm(x) for x in phrase.split()]
 for j in range(len(got)-len(want)+1):
  if got[j:j+len(want)]==want:return ws[j]['start']
 raise ValueError(f'Unmatched cue {i}: {phrase}')
def base(im,bottom=None,middle=None,top='?',letters=False,highlight=(),fade=1):
 bottom=bottom or ['']*5;middle=middle or ['']*3
 for k,x in enumerate(X):box(im,x,Y[0],bottom[k],BLUE if k in highlight else WHITE,fade)
 for k,x in enumerate(X[1:4]):box(im,x,Y[1],middle[k],WHITE,fade)
 box(im,640,Y[2],top,GOLD if str(top)=='32' else WHITE,fade)
def weights(im,values=[1,2,3,2,1],alpha=None):
 for k,(x,v) in enumerate(zip(X,values)):text(im,'×'+str(v),x,611,32,GOLD,a=alpha[k] if alpha else 1)
def heading(im,title):
 text(im,'2025 AMC  ·  QUESTION 17',640,40,13,DIM,'sans')
 text(im,title,640,103,38,WHITE)
def expression(im,terms,x,y,highlight='c',a=1):
 values=[]
 for i,term in enumerate(terms):
  if i:values.append(('+',WHITE))
  values.append((term,BLUE if term==highlight else WHITE))
 size=22;width=sum(font(size,'italic' if v.isalpha() else 'math').getlength(v)/S for v,c in values)+6*(len(values)-1)
 start=x-width/2
 for v,c in values:
  style='italic' if v.isalpha() else 'math';ww=font(size,style).getlength(v)/S
  text(im,v,start+ww/2,y,size,c,style,a);start+=ww+6

def frame(t):
 im=Image.new('RGB',(W,H),BLACK)
 i=max(j for j,s in enumerate(TIMING['segments']) if s['start_seconds']<=t)
 st=TIMING['segments'][i]['start_seconds'];en=st+TIMING['segments'][i]['duration_seconds'];u=clamp((t-st)/(en-st))
 if i==0:
  heading(im,'How large can the top be?')
  base(im,fade=anim(t,0,.7))
  for j in range(5):text(im,j+1,X[j],650,42,BLUE,a=anim(t,.4+j*.11,.5))
 elif i==1:
  heading(im,'Add the three closest boxes.')
  base(im)
  for j in range(5):text(im,j+1,X[j],650,40,BLUE)
  a=anim(t,cue(i,'Each box'),.4)
  for j in range(3):
   box(im,X[j],510,'',BLUE,a,BLUE)
   tt=anim(t,cue(i,'three closest')+j*.12,.85)
   if 0<tt<1:flight(im,'•',(X[j],510),(510,380),tt,BLUE,34)
  box(im,510,380,'+',BLUE,a)
  text(im,'Use 1, 2, 3, 4, 5 once each',640,691,16,DIM,'sans')
 elif i==2:
  heading(im,'Follow the centre number.')
  base(im,list('abcde'),highlight=(2,))
  for j in [0,1,3,4]:box(im,X[j],510,'',WHITE);text(im,'abcde'[j],X[j],510,38,DIM,'italic')
  box(im,640,510,'',BLUE,fill=BLUE);text(im,'c',640,510,44,BLUE,'italic')
  a=cue(i,'It appears');d=max(.9,(en-a)*.5)
  for j in range(3):
   q=anim(t,a+j*.18,d)
   if q>0:
    ray(im,(640,470),(X[j+1],405),q,BLUE)
    flight(im,'c',(640,510),(X[j+1],380),q,BLUE,34,lift=20)
  text(im,'One centre number. Three middle sums.',640,644,26,WHITE,a=anim(t,a+.5,.6))
 elif i==3:
  heading(im,'The centre contributes three times.')
  base(im,list('abcde'),top='',highlight=(2,))
  for j in range(3):
   expression(im,[['a','b','c'],['b','c','d'],['c','d','e']][j],X[j+1],380,a=.65)
   q=anim(t,st+.05+j*.13,max(.6,(en-st)*.45))
   if q<1:flight(im,'c',(X[j+1],380),(640+(j-1)*30,250),q,BLUE,27,lift=10)
  q=anim(t,cue(i,'three times'),.4)
  expression(im,['c','c','c'],640,250,a=1-q)
  text(im,'3c',640,250,44,GOLD,'italic',q)
  weights(im,alpha=[0,0,q,0,0])
 elif i==4:
  heading(im,'Count every position’s contributions.')
  base(im,list('abcde'))
  a=anim(t,cue(i,'neighbours'),.55);b=anim(t,cue(i,'Each end'),.55)
  weights(im,alpha=[b,a,1,a,b])
  for j in [1,3]:box(im,X[j],510,'abcde'[j],BLUE,a)
  for j in [0,4]:box(im,X[j],510,'abcde'[j],BLUE,b)
  text(im,'1     :     2     :     3     :     2     :     1',640,674,19,DIM)
 elif i==5:
  heading(im,'Give the biggest number the biggest weight.')
  base(im,top='');weights(im)
  # Digit, initial bank position, target cell, spoken action.
  moves=[(5,4,2,'five'),(3,2,1,'three'),(4,3,3,'four'),(1,0,0,'one'),(2,1,4,'two')]
  for v,source,target,word in moves:
   q=anim(t,cue(i,word),.85)
   flight(im,str(v),(X[source],680),(X[target],510),q,BLUE,44,lift=42)
 elif i==6:
  heading(im,'Larger number. More copies. Larger total.')
  # A concrete swap shows why putting the larger number at the higher weight helps.
  text(im,'end',480,245,22,DIM,'sans');text(im,'centre',800,245,22,DIM,'sans')
  box(im,480,345);box(im,800,345)
  text(im,'×1',480,445,38,GOLD);text(im,'×3',800,445,38,GOLD)
  q=anim(t,cue(i,'in a position'),1.4)
  flight(im,'5',(480,345),(800,345),q,BLUE,54,lift=90)
  flight(im,'1',(800,345),(480,345),q,BLUE,54,lift=-90)
  text(im,'5 × 1 + 1 × 3 = 8',640,555,38,WHITE,a=1-q)
  text(im,'1 × 1 + 5 × 3 = 16',640,555,38,WHITE,a=q)
  text(im,'Same two numbers. A larger total.',640,638,27,GOLD,a=anim(t,cue(i,'That is why'),.6))
 elif i==7:
  heading(im,'Now add upwards.')
  base(im,['1','3','5','4','2'],top='',highlight=range(5));weights(im)
  for j,(v,word) in enumerate([(9,'nine'),(12,'twelve'),(11,'eleven')]):
   q=anim(t,cue(i,word),.4);text(im,str(v),X[j+1],380,43,BLUE,a=q)
  q=anim(t,cue(i,'Add them'),.8)
  for j,v in enumerate([9,12,11]):
   if 0<q<1:flight(im,str(v),(X[j+1],380),(640,250),q,GOLD,26,lift=20,a=math.sin(q*math.pi))
  a=anim(t,cue(i,'thirty-two'),.35)
  text(im,'32',640,250,48,GOLD,a=a)
 elif i==8:
  heading(im,'Count how often each number contributes.')
  base(im,['1','3','5','4','2'],[9,12,11],'32',highlight=range(5));weights(im)
  text(im,'Answer C  ·  32',640,684,27,GOLD,a=anim(t,st,.4))
 return im

def main():
 global TIMING,WORDS
 p=argparse.ArgumentParser();p.add_argument('--preview',action='store_true');args=p.parse_args()
 TIMING=json.loads((ROOT/'timing.json').read_text());WORDS=json.loads((ROOT/'words.json').read_text())['words']
 duration=TIMING['duration_seconds']+1.6
 assert duration<=60,f'Too long: {duration}'
 # Check every semantic cue before spending time on full render.
 samples=[]
 for j,s in enumerate(TIMING['segments']):
  for frac in [.2,.6,.9]:samples.append((j,s['start_seconds']+s['duration_seconds']*frac))
 previews=ROOT/'storyboard';previews.mkdir(exist_ok=True,parents=True)
 for j,t in samples:frame(t).save(previews/f'scene-{j+1}-{t:.2f}.jpg',quality=92)
 frame(TIMING['segments'][8]['start_seconds']+1).save(ROOT/'poster.jpg',quality=94)
 contact=Image.new('RGB',(960,540*math.ceil(len(samples)/3)),BLACK)
 for k,(j,t) in enumerate(samples):
  shot=frame(t);shot.thumbnail((320,180));contact.paste(shot,((k%3)*320,(k//3)*180))
 # Crop contact to compact 3-column storyboard.
 contact.crop((0,0,960,180*math.ceil(len(samples)/3))).save(ROOT/'contact.jpg',quality=94)
 if args.preview:return
 process=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-vcodec','rawvideo','-s',f'{W}x{H}','-pix_fmt','rgb24','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','fast','-crf','17','-pix_fmt','yuv420p','-movflags','+faststart',str(ROOT/'visual.mp4')],stdin=subprocess.PIPE)
 for f in range(math.ceil(duration*FPS)):
  process.stdin.write(frame(f/FPS).tobytes())
  if f%300==0:print(f'Frame {f}/{math.ceil(duration*FPS)}',flush=True)
 process.stdin.close();assert process.wait()==0
if __name__=='__main__':main()
