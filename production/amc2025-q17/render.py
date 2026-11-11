"""Original mathematical animation. Black canvas, cyan objects, gold emphasis.
All narrative actions use word timestamps from the completed synthetic speech.
"""
import argparse,functools,json,math,re,subprocess,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from solution_design import load_question,source_colour,diagram_surface
QUESTION=load_question(Path(__file__).with_name('question.json'))
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
 if a<=0:return
 d=ImageDraw.Draw(im,'RGBA');r=SIZE/2
 rect=[round(z*S) for z in [x-r,y-r,x+r,y+r]]
 if fill:d.rectangle(rect,fill=(*rgb(fill),round(a*.12*255)))
 d.rectangle(rect,outline=(*rgb(color),round(a*255)),width=round(1.3*S))
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

def left_text(im,s,x,y,size=27,color=WHITE):
 ImageDraw.Draw(im).text((round(x*S),round(y*S)),s,font=font(size),fill=color,anchor='lm')
def dot(im,x,y,r=10,color=BLUE,a=1):
 if a<=0:return
 ImageDraw.Draw(im,'RGBA').ellipse(tuple(round(z*S) for z in [x-r,y-r,x+r,y+r]),fill=(*rgb(color),round(255*a)))
def opening(im,t):
 # The exact source wording, all choices, and faithful blank grid are present from frame one.
 text(im,'2025 AMC UPPER PRIMARY  ·  QUESTION 17',640,61,16,DIM,'sans')
 text(im,'Xian’s number pyramid',640,111,37,WHITE)
 question_cue=cue(0,'What is the largest')
 for j,v in enumerate(QUESTION['question_lines']):
  left_text(im,v,62,193+43*j,27,GOLD if j>=7 and t>=question_cue else WHITE)
 # Match the 5 / 3 / 1 square arrangement and the three arrows in the source diagram.
 xs=[875,950,1025,1100,1175];ys=[399,324,249];d=ImageDraw.Draw(im)
 surface=diagram_surface(QUESTION)
 d.rectangle([round(830*S),round(195*S),round(1230*S),round(445*S)],fill=surface)
 for yy,inds in [(399,range(5)),(324,range(1,4)),(249,[2])]:
  for k in inds:
   x=xs[k];d.rectangle([round(v*S) for v in [x-37.5,yy-37.5,x+37.5,yy+37.5]],outline=WHITE,width=2)
 colour=source_colour(QUESTION,'arrows')
 # The arrow geometry is instructional, not an answer hint.
 for start in [(875,385),(950,385),(1025,385)]:
  end=(950,335);line(im,[start,end],colour,3)
  angle=math.atan2(end[1]-start[1],end[0]-start[0]);length=12
  line(im,[(end[0]-length*math.cos(angle-.5),end[1]-length*math.sin(angle-.5)),end,(end[0]-length*math.cos(angle+.5),end[1]-length*math.sin(angle+.5))],colour,3)
 for j in range(5):
  text(im,str(j+1),875+75*j,491,32,BLUE,a=anim(t,cue(0,'one to five'),.6))
 text(im,'Use each number once',1025,534,16,DIM,'sans',anim(t,cue(0,'one to five'),.6))
 for x,v in zip([140,390,640,890,1140],QUESTION['choices']):text(im,v,x,650,28,WHITE)

def frame(t):
 im=Image.new('RGB',(W,H),BLACK)
 i=max(j for j,s in enumerate(TIMING['segments']) if s['start_seconds']<=t)
 st=TIMING['segments'][i]['start_seconds'];en=st+TIMING['segments'][i]['duration_seconds']
 if i==0:
  opening(im,t)
 elif i==1:
  heading(im,'What kind of problem is this?')
  text(im,'MAXIMISING',640,260,50,BLUE)
  text(im,'Make the top as large as possible.',640,329,29,WHITE)
  a=anim(t,cue(i,'We will count'),.4)
  text(im,'THE PLAN',640,429,17,GOLD,'sans',a)
  text(im,'Count how often each position contributes.',640,485,28,WHITE,a=a)
  text(im,'Put larger numbers where they count more.',640,539,28,WHITE,a=a)
 elif i==2:
  heading(im,'How often does each position count?')
  base(im,top='')
  centre=cue(i,'centre');three=cue(i,'three times');neighbours=cue(i,'neighbours');ends=cue(i,'ends')
  dot(im,640,510,11)
  for j in range(3):
   q=anim(t,centre,.65);r=anim(t,three,.7)
   p=bezier((640,510),(X[j+1],380),q,18)
   if r>0:p=bezier((X[j+1],380),(640+(j-1)*30,250),r,12)
   dot(im,*p,9)
  aa=[anim(t,ends,.35),anim(t,neighbours,.35),anim(t,three,.35),anim(t,neighbours,.35),anim(t,ends,.35)]
  weights(im,alpha=aa)
  for j in [1,3]:
   box(im,X[j],510,'',BLUE,aa[j])
   if neighbours<=t<ends:
    for k in ([0,1] if j==1 else [1,2]):line(im,[(X[j],470),(X[k+1],405)],BLUE,1.5,a=.7)
  for j in [0,4]:
   box(im,X[j],510,'',BLUE,aa[j])
   if ends<=t<ends+.7:line(im,[(X[j],470),(X[1 if j==0 else 3],405)],BLUE,1.5,a=.7)
 elif i==3:
  heading(im,'Give the biggest number the biggest weight.')
  base(im,top='');weights(im)
  for v,source,target,word in [(5,4,2,'five'),(3,2,1,'three'),(4,3,3,'four'),(1,0,0,'one'),(2,1,4,'two')]:
   q=anim(t,cue(i,word),.65)
   flight(im,str(v),(X[source],680),(X[target],510),q,BLUE,44,lift=42)
 elif i==4:
  heading(im,'Why does this give the maximum?')
  text(im,'end',480,245,22,DIM,'sans');text(im,'centre',800,245,22,DIM,'sans')
  box(im,480,345);box(im,800,345)
  text(im,'×1',480,445,38,GOLD);text(im,'×3',800,445,38,GOLD)
  q=anim(t,cue(i,'more-counted'),.95)
  flight(im,'5',(480,345),(800,345),q,BLUE,54,lift=90)
  flight(im,'1',(800,345),(480,345),q,BLUE,54,lift=-90)
  text(im,'5 × 1 + 1 × 3 = 8',640,555,38,WHITE,a=max(0,1-2*q))
  text(im,'1 × 1 + 5 × 3 = 16',640,555,38,WHITE,a=max(0,2*q-1))
  text(im,'Same numbers. A larger total.',640,638,27,GOLD,a=anim(t,cue(i,'larger total'),.3))
 elif i==5:
  heading(im,'Now add upwards.')
  base(im,['1','3','5','4','2'],top='',highlight=range(5));weights(im)
  for j,(v,word) in enumerate([(9,'nine'),(12,'twelve'),(11,'eleven')]):text(im,str(v),X[j+1],380,43,BLUE,a=anim(t,cue(i,word),.3))
  q=anim(t,cue(i,'The maximum'),.7)
  for j,v in enumerate([9,12,11]):
   if 0<q<1:flight(im,str(v),(X[j+1],380),(640,250),q,GOLD,26,lift=20,a=math.sin(q*math.pi))
  text(im,'32',640,250,48,GOLD,a=anim(t,cue(i,'thirty-two'),.3))
  text(im,'Answer C  ·  32',640,684,27,GOLD,a=anim(t,cue(i,'answer C'),.3))
 return im

def main():
 global TIMING,WORDS
 p=argparse.ArgumentParser();p.add_argument('--preview',action='store_true');args=p.parse_args()
 TIMING=json.loads((ROOT/'timing.json').read_text());WORDS=json.loads((ROOT/'words.json').read_text())['words']
 duration=TIMING['duration_seconds']+1.6
 assert duration<=60,f'Too long: {duration}'
 # Check every semantic cue before spending time on full render.
 samples=[]
 frame(0).save(ROOT/'exact-question.jpg',quality=95)
 for j,s in enumerate(TIMING['segments']):
  for frac in [.2,.6,.9]:samples.append((j,s['start_seconds']+s['duration_seconds']*frac))
 previews=ROOT/'storyboard';previews.mkdir(exist_ok=True,parents=True)
 for j,t in samples:frame(t).save(previews/f'scene-{j+1}-{t:.2f}.jpg',quality=92)
 frame(TIMING['duration_seconds']+1).save(ROOT/'poster.jpg',quality=94)
 contact=Image.new('RGB',(960,180*math.ceil(len(samples)/3)),BLACK)
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
