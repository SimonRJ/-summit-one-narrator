"""Progressive cinematic maths animation, synced to measured VoxCPM voice-C segments."""
import argparse,json,math,re,subprocess,hashlib
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
P=argparse.ArgumentParser();P.add_argument("--lesson",required=True,choices=["S001","S002"]);args=P.parse_args()
ID=args.lesson;ROOT=Path("build/lesson-intros")/ID;ROOT.mkdir(parents=True,exist_ok=True)
DOC=json.loads((Path("production/lesson-intros")/(ID+".json")).read_text())
TIMER=json.loads((ROOT/"timing.json").read_text());CAPS=json.loads((ROOT/"captions.json").read_text())
W,H,S,FPS=1920,1080,1.5,24
WHITE="#eff5f9";CYAN="#77d8ea";GOLD="#f6c76e";FAINT="#adc0d1";BG="#06101c";NAVY="#172739";GREEN="#a8dfc4";RED="#ef9f9a";PURPLE="#bcb9f5"
import functools
@functools.lru_cache(maxsize=90)
def font(n,bold=False):
 name="DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
 return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/"+name,max(12,round(n*S)))
def clamp(x):return max(0,min(1,x))
def ease(x):x=clamp(x);return x*x*(3-2*x)
def color(s,a=1):
 v=tuple(int(s[j:j+2],16) for j in [1,3,5])
 return tuple(round(x*clamp(a)+int(BG[j:j+2],16)*(1-clamp(a))) for x,j in zip(v,[1,3,5]))
def xy(x,y):return round(x*S),round(y*S)
def rect(im,x,y,w,h,fill=NAVY,stroke="#2e4c65",rad=16,a=1):
 ImageDraw.Draw(im).rounded_rectangle((round((x-w/2)*S),round((y-h/2)*S),round((x+w/2)*S),round((y+h/2)*S)),radius=round(rad*S),fill=color(fill,a),outline=color(stroke,a),width=round(1.5*S))
def line(im,points,c=CYAN,width=2,a=1):
 if len(points)>1:ImageDraw.Draw(im).line([xy(x,y) for x,y in points],fill=color(c,a),width=max(1,round(width*S)),joint="curve")
def dot(im,x,y,r=8,c=CYAN,a=1):
 d=ImageDraw.Draw(im);d.ellipse((round((x-r)*S),round((y-r)*S),round((x+r)*S),round((y+r)*S)),fill=color(c,a))
def circ(im,x,y,r,c=CYAN,width=2,a=1):
 d=ImageDraw.Draw(im);d.ellipse((round((x-r)*S),round((y-r)*S),round((x+r)*S),round((y+r)*S)),outline=color(c,a),width=max(1,round(width*S)))
def txt(im,s,x,y,n=28,c=WHITE,bold=False,a=1,limit=1100):
 s=str(s);n0=n
 while font(n,bold).getlength(s)>limit*S and n>14:n-=1
 if a>.005:ImageDraw.Draw(im).text(xy(x,y),s,font=font(n,bold),fill=color(c,a),anchor="mm")
def bar(im,x,y,w,h,c=CYAN,a=1):rect(im,x,y,w,h,c,c,4,a)
def poly(im,coords,c=CYAN,a=1):
 ImageDraw.Draw(im).polygon([xy(x,y) for x,y in coords],fill=color(c,a))
def arrow(im,x0,y0,x1,y1,c=CYAN,a=1):
 line(im,[(x0,y0),(x1,y1)],c,2.5,a)
 theta=math.atan2(y1-y0,x1-x0)
 for ang in [theta+2.6,theta-2.6]:line(im,[(x1,y1),(x1+13*math.cos(ang),y1+13*math.sin(ang))],c,2.5,a)
def cube(im,cx,cy,r,rot=0,c=CYAN,a=1):
 v=[]
 for x,y,z in [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]:
  xx=x*math.cos(rot)+z*math.sin(rot);zz=-x*math.sin(rot)+z*math.cos(rot)
  yy=y*.84-zz*.52;depth=y*.52+zz*.84;v.append((cx+xx*r,cy+yy*r,depth))
 faces=[(0,1,2,3),(4,7,6,5),(0,4,5,1),(3,2,6,7),(1,5,6,2),(0,3,7,4)]
 for j,f in enumerate(sorted(faces,key=lambda f:sum(v[k][2] for k in f))):
  pts=[(v[k][0],v[k][1]) for k in f]
  poly(im,pts,"#1d3d51",a*.8);line(im,pts+[pts[0]],c,1.8,a*(.5+j*.07))
def circle_symbols(im,t,highlight=None):
 labels=["TRIANGLE","SQUARE","CIRCLE","STAR","DIAMOND","HEXAGON"]
 n=6;cx,cy,r=640,368,175
 circ(im,cx,cy,r,"#3b637a",1.5)
 for j,label in enumerate(labels):
  ang=-math.pi/2+j*math.pi*2/n;px=cx+r*math.cos(ang);py=cy+r*math.sin(ang)
  active=highlight==j
  rect(im,px,py,124,82,fill="#314051" if active else "#0e2132",stroke=GOLD if active else "#43748b",rad=15)
  txt(im,str(j+1),px,py-20,20,GOLD if active else CYAN,True)
  txt(im,label,px,py+14,13,WHITE,True,limit=115)
def grid(im,x,y,w,h,cols,rows):
 for k in range(cols+1):line(im,[(x+k*w/cols,y),(x+k*w/cols,y+h)],"#4b697b",1)
 for k in range(rows+1):line(im,[(x,y+k*h/rows),(x+w,y+k*h/rows)],"#4b697b",1)
def caption(im,t):
 active=next((q for q in CAPS if q["start"]<=t<=q["end"]),None)
 if active is None:return
 d=ImageDraw.Draw(im)
 d.rounded_rectangle((round(64*S),round(617*S),round(1216*S),round(700*S)),radius=round(12*S),fill="#101d2d")
 sentence=active["text"].strip()
 parts=[""]
 for word in sentence.split():
  potential=(parts[-1]+" "+word).strip()
  if font(21).getlength(potential)>(1020*S):parts.append(word)
  else:parts[-1]=potential
 parts=parts[:2]
 for j,x in enumerate(parts):txt(im,x,640,645+j*27,21,WHITE,False)
def base(i,tag,title):
 image=Image.new("RGB",(W,H),BG);d=ImageDraw.Draw(image)
 # Subtle mathematically structured perspective lines; not decorative stars.
 for j in range(7):
  x=70+j*196
  line(image,[(x+math.sin(i+j)*12,116),(x-130,607)],"#0d2331",1.0)
 txt(image,"SUMMIT ONE  /  LEARNING",180,44,16,FAINT,True)
 txt(image,DOC["title"].upper(),640,72,15,CYAN,True,limit=1110)
 txt(image,title,640,125,34,WHITE,True,limit=1110)
 txt(image,tag.upper(),1098,44,16,GOLD,True)
 for j in range(len(DOC["segments"])):
  bar(image,387+j*57,590,43,3,CYAN if j<=i else "#264456",1)
 return image
def draw(i,t):
 seg=TIMER["segments"][i]
 u=clamp((t-seg["start_seconds"])/max(.01,seg["duration_seconds"]))
 E=lambda p,d=.1:ease((u-p)/d)
 step=i
 if ID=="S001":
  titles=["Remainders: a hidden shortcut","EASY · The divisibility question","Why adding digits works","MEDIUM · One repeating cycle","The remainder gives the position","HARD · Three simultaneous conditions","Simplify before calculating","Find and check the code","Your turn on new problems"]
  tags=["the idea","easy","easy","medium","medium","hard","hard","hard","next"]
 else:
  titles=["Take numbers apart intelligently","EASY · Estimate first","Compensate to make it exact","MEDIUM · Think in rectangles","Subtract the small strip","One reusable habit","HARD · Two enormous expressions","A difference-of-squares identity","Now solve new problems"]
  tags=["the idea","easy","easy","medium","medium","method","hard","hard","next"]
 im=base(i,tags[i],titles[i])
 if ID=="S001":
  if i==0:
   for j,(x,v) in enumerate([(360,"BIG NUMBER"),(640,"SMALL REMAINDER"),(920,"USEFUL CLUE")]):
    rect(im,x,328,230,150,fill=NAVY,stroke=CYAN if j==1 else "#43637b",a=E(.08+j*.12))
    txt(im,v,x,315,19,CYAN if j==1 else WHITE,True,a=E(.08+j*.12))
    txt(im,["2473","R = 1","WHY?"][j],x,366,42,GOLD if j==1 else WHITE,True,a=E(.08+j*.12))
   txt(im,"Easy → Medium → Hard",640,518,28,DIM if False else FAINT,a=E(.55))
  elif i==1:
   txt(im,"2,473",640,296,88,WHITE,True,a=E(.08))
   txt(im,"divisible by 3 ?",640,410,36,CYAN,True,a=E(.33))
   for j,v in enumerate([2,4,7,3]):
    rect(im,475+j*110,512,72,66,stroke="#4a6d84",a=E(.48+j*.07));txt(im,v,475+j*110,512,37,GOLD,True,a=E(.48+j*.07))
  elif i==2:
   txt(im,"10 ≡ 1   (mod 3)",640,223,33,CYAN,True,a=E(.03))
   for j,v in enumerate([2,4,7,3]):
    txt(im,v,407+j*157,330,55,WHITE,True,a=E(.12+j*.09))
    if j<3:txt(im,"+",486+j*157,330,35,CYAN,True,a=E(.2+j*.09))
   txt(im,"= 16",955,330,50,GOLD,True,a=E(.51))
   arrow(im,640,372,640,446,a=E(.62))
   txt(im,"16 = 3 × 5 + 1",640,490,41,GOLD,True,a=E(.64))
   txt(im,"remainder 1 · not divisible",640,546,24,GREEN,a=E(.83))
  elif i==3:
   circle_symbols(im,t)
   txt(im,"Position 1,739 ?",640,562,33,GOLD,True,a=E(.55))
  elif i==4:
   circle_symbols(im,t,highlight=4 if u>.62 else None)
   txt(im,"1,739 = 6 × 289 + 5",640,237,41,GOLD,True,a=E(.20))
   txt(im,"289 full cycles · fifth symbol",640,546,25,GREEN,True,a=E(.70))
  elif i==5:
   rect(im,640,350,780,370,stroke="#42617c",a=E(.03))
   txt(im,"Find the smallest THREE-DIGIT N",640,244,31,WHITE,True,a=E(.08))
   for j,v in enumerate(["N leaves 4 when divided by 5","N leaves 6 when divided by 7","N is divisible by 9"]):
    txt(im,v,640,323+j*68,29,GOLD if j==2 else CYAN,a=E(.23+j*.18))
  elif i==6:
   for j,(value,y) in enumerate([("N + 1 is divisible by 5",270),("N + 1 is divisible by 7",350),("N + 1 = 35k",442)]):
    txt(im,value,640,y,37,GOLD if j==2 else WHITE,True,a=E(.13+j*.22))
   txt(im,"N = 35k − 1",640,531,33,GREEN,True,a=E(.80))
  elif i==7:
   txt(im,"35k ≡ 1 (mod 9)",640,225,38,CYAN,True,a=E(.04))
   txt(im,"8k ≡ 1  →  k ≡ 8 (mod 9)",640,317,33,WHITE,True,a=E(.27))
   txt(im,"N = 35 × 8 − 1 = 279",640,418,44,GOLD,True,a=E(.54))
   txt(im,"279 ÷ 5 → 4 left   |   279 ÷ 7 → 6 left",640,497,23,GREEN,True,a=E(.78))
   txt(im,"2 + 7 + 9 = 18 : divisible by 9",640,542,21,FAINT,a=E(.87))
  elif i==8:
   for j,(x,v) in enumerate([(360,"DIGIT SUM"),(640,"REPEATING CYCLE"),(920,"SHARED REMAINDERS")]):
    rect(im,x,335,236,124,stroke=CYAN if j==1 else "#52708b",a=E(.10+j*.12))
    txt(im,v,x,335,19,WHITE,True,a=E(.13+j*.12),limit=230)
   txt(im,"Now solve the new lesson problems.",640,506,33,GOLD,True,a=E(.65))
 else:
  if i==0:
   txt(im,"CLOSE TO A ROUND NUMBER",640,232,30,CYAN,True,a=E(.04))
   for j,(value,x) in enumerate([("398",320),("≈ 400",640),("− 2",960)]):
    rect(im,x,359,224,125,stroke="#467c91",a=E(.13+j*.17))
    txt(im,value,x,359,49,GOLD if j==1 else WHITE,True,a=E(.13+j*.17))
   txt(im,"Estimate → Decompose → Check",640,527,30,FAINT,a=E(.65))
  elif i==1:
   txt(im,"398  +  207",640,260,70,WHITE,True,a=E(.06))
   txt(im,"400  +  200",640,386,58,CYAN,True,a=E(.38))
   txt(im,"≈ 600",640,510,51,GOLD,True,a=E(.70))
  elif i==2:
   txt(im,"398 = 400 − 2",640,218,41,CYAN,True,a=E(.08))
   txt(im,"207 = 200 + 7",640,311,41,CYAN,True,a=E(.31))
   txt(im,"600 − 2 + 7 = 600 + 5",640,423,39,WHITE,True,a=E(.55))
   txt(im,"605",640,528,70,GOLD,True,a=E(.76))
  elif i==3:
   txt(im,"57 × 98",640,223,53,WHITE,True,a=E(.03))
   rx,ry,w,h=330,305,600,205
   rect(im,630,406,600,205,"#102838",CYAN,a=E(.13),rad=1)
   # show 98 of 100 units as the kept area, 2 of 100 as a strip
   bar(im,rx+(w*98/100)/2,ry+h/2,w*98/100,h,"#1d657b",a=E(.24))
   bar(im,rx+w*99/100,ry+h/2,w*2/100,h,GOLD,a=E(.45))
   txt(im,"98 kept",597,423,27,WHITE,True,a=E(.55))
   txt(im,"2 removed",1005,423,24,GOLD,True,a=E(.63))
   txt(im,"57 units high",219,406,19,CYAN,a=E(.70))
  elif i==4:
   for j,(value,y) in enumerate([("57 × 100 = 5,700",250),("57 × 2 = 114",358),("5,700 − 114 = 5,586",479)]):
    txt(im,value,640,y,44 if j==2 else 38,GOLD if j==2 else WHITE,True,a=E(.12+j*.24))
   txt(im,"Exact and close to the estimate",640,551,24,GREEN,a=E(.84))
  elif i==5:
   for j,(value,y) in enumerate([("1. Find a convenient round number",248),("2. Replace the awkward part",349),("3. Keep the correction visible",450)]):
    rect(im,640,y,770,77,stroke="#46677f",a=E(.1+j*.23))
    txt(im,value,640,y,27,WHITE if j!=2 else GOLD,True,a=E(.10+j*.23))
  elif i==6:
   txt(im,"Which expression is larger?",640,235,32,WHITE,True,a=E(.02))
   rect(im,640,344,790,100,stroke=CYAN,a=E(.20))
   txt(im,"49,996 × 50,004",640,345,51,CYAN,True,a=E(.22))
   txt(im,"versus",640,426,23,FAINT,a=E(.45))
   rect(im,640,513,790,100,stroke=GOLD,a=E(.51))
   txt(im,"50,000² − 17",640,512,48,GOLD,True,a=E(.55))
  elif i==7:
   txt(im,"(N − 4)(N + 4)",640,221,46,CYAN,True,a=E(.04))
   txt(im,"= N² − 4²",640,309,52,WHITE,True,a=E(.30))
   txt(im,"= N² − 16",640,420,60,GOLD,True,a=E(.55))
   txt(im,"No long multiplication needed",640,523,25,GREEN,a=E(.76))
  elif i==8:
   txt(im,"N² − 16",437,298,51,CYAN,True,a=E(.05))
   txt(im,">",640,300,51,WHITE,True,a=E(.30))
   txt(im,"N² − 17",845,298,51,GOLD,True,a=E(.32))
   txt(im,"Larger by exactly ONE",640,409,41,GREEN,True,a=E(.55))
   txt(im,"Your turn: new problems, same useful idea.",640,526,26,WHITE,a=E(.76))
 caption(im,t)
 return im
def main():
 DURATION=float(TIMER["duration_seconds"])+2.5
 nframes=round(DURATION*FPS)
 cmd=["ffmpeg","-hide_banner","-loglevel","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s","1920x1080","-r",str(FPS),"-i","-","-c:v","libx264","-preset","veryfast","-crf","21","-pix_fmt","yuv420p","-movflags","+faststart",str(ROOT/"visual.mp4")]
 proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
 starts=[seg["start_seconds"] for seg in TIMER["segments"]]
 try:
  for idx in range(nframes):
   t=idx/FPS
   index=max(0,min(len(starts)-1,next((j for j in range(len(starts)-1,-1,-1) if starts[j]<=t),0)))
   im=draw(index,min(t,float(TIMER["duration_seconds"])-.01))
   proc.stdin.write(im.tobytes())
   if idx%240==0:print(f"{ID}: {idx}/{nframes} frames",flush=True)
  proc.stdin.close()
  err=proc.stderr.read();status=proc.wait()
  if status:raise RuntimeError(err.decode(errors="replace")[-3000:])
 except Exception:
  proc.kill();raise
 # Poster at a first fully drawn mathematics frame, not a still title card.
 frame=draw(1,TIMER["segments"][1]["start_seconds"]+.45*TIMER["segments"][1]["duration_seconds"])
 frame.save(ROOT/"poster.jpg",quality=90,optimize=True)
 print(f"Rendered {ID} at 1920×1080 / {FPS} fps, {nframes} frames.",flush=True)
if __name__=="__main__":main()
