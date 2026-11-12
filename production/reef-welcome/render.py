"""Reef's welcome: original geometry animated from completed narration timestamps."""
import argparse, functools, json, math, re, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ROOT=Path('build/reef-welcome'); SRC=Path(__file__).parent
W,H,S,FPS=1920,1080,1.5,30
BLACK='#000000';WHITE='#f7f7f7';CYAN='#28bbee';GOLD='#ffd36a';DIM='#9baab5';DARK='#183442'
TIMING=None;WORDS=None;CAPS=None
@functools.lru_cache(100)
def font(n,style='sans'):
    family='DejaVuSerif' if style=='math' else 'DejaVuSans'
    return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/'+family+('-Bold' if style=='bold' else '')+'.ttf',round(n*S))
def clamp(v):return min(1,max(0,v))
def ease(v):v=clamp(v);return v*v*(3-2*v)
def anim(t,a,d=.8):return ease((t-a)/d)
def mix(a,b,u):return a+(b-a)*u
def col(c,a=1):return tuple(round(int(c[k:k+2],16)*clamp(a)) for k in (1,3,5))
def text(im,s,x,y,n=30,c=WHITE,style='sans',a=1):
    if a>0:
        f=font(n,style);assert f.getlength(str(s))<=W-84*S,f'Text too wide: {s}'
        ImageDraw.Draw(im).text((round(x*S),round(y*S)),str(s),font=f,fill=col(c,a),anchor='mm')
def line(im,pts,c=CYAN,width=2,a=1):
    if a>0:ImageDraw.Draw(im).line([(round(x*S),round(y*S)) for x,y in pts],fill=col(c,a),width=max(1,round(width*S)),joint='curve')
def dot(im,x,y,r=8,c=CYAN,a=1):
    if a>0:ImageDraw.Draw(im).ellipse([round(v*S) for v in (x-r,y-r,x+r,y+r)],fill=col(c,a))
def ring(im,x,y,r=30,c=CYAN,width=2,a=1):
    if a>0:ImageDraw.Draw(im).ellipse([round(v*S) for v in (x-r,y-r,x+r,y+r)],outline=col(c,a),width=max(1,round(width*S)))
def rect(im,x,y,w,h,c=DARK,outline=CYAN,a=1,r=12):
    if a>0:ImageDraw.Draw(im).rounded_rectangle([round(v*S) for v in (x-w/2,y-h/2,x+w/2,y+h/2)],radius=round(r*S),fill=col(c,a),outline=col(outline,a),width=round(1.5*S))
def travel(p,q,u,lift=30):return (mix(p[0],q[0],u),mix(p[1],q[1],u)-4*u*(1-u)*lift)
def trace(im,pts,u,c=CYAN,width=3,a=1):
    lengths=[math.dist(p,q) for p,q in zip(pts,pts[1:])];left=sum(lengths)*clamp(u);done=[pts[0]]
    for p,q,l in zip(pts,pts[1:],lengths):
        if left>=l:done.append(q);left-=l
        else:done.append((mix(p[0],q[0],left/l),mix(p[1],q[1],left/l)));break
    line(im,done,c,width,a)
def norm(s):return re.sub('[^a-z0-9]','',s.lower())
@functools.lru_cache(150)
def cue(i,phrase):
    ws=[w for w in WORDS if w['segment']==i+1];got=[norm(w['text']) for w in ws];want=[norm(w) for w in phrase.split()]
    for j in range(len(got)-len(want)+1):
        if got[j:j+len(want)]==want:return ws[j]['start']
    raise ValueError(f'Missing spoken cue: {i+1}: {phrase}')
def heading(im,title,chapter):
    text(im,chapter.upper(),640,53,14,DIM);text(im,title,640,112,39,WHITE,'math')
def arrow(im,p,q,c=CYAN,a=1):
    line(im,[p,q],c,2,a);v=math.atan2(q[1]-p[1],q[0]-p[0]);l=11
    line(im,[(q[0]-l*math.cos(v-.5),q[1]-l*math.sin(v-.5)),q,(q[0]-l*math.cos(v+.5),q[1]-l*math.sin(v+.5))],c,2,a)
def cube(im,center,angle,size=90):
    vs=[]
    for x,y,z in [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]:
        xx=x*math.cos(angle)+z*math.sin(angle);zz=-x*math.sin(angle)+z*math.cos(angle)
        yy=y*.85-zz*.48;zz2=y*.48+zz*.85;vs.append((center[0]+xx*size,center[1]+yy*size,zz2))
    faces=[(0,1,2,3),(4,7,6,5),(0,4,5,1),(3,2,6,7),(1,5,6,2),(0,3,7,4)];faces.sort(key=lambda f:sum(vs[k][2] for k in f));d=ImageDraw.Draw(im)
    for j,f in enumerate(faces):
        pts=[(round(vs[k][0]*S),round(vs[k][1]*S)) for k in f];d.polygon(pts,fill=col(CYAN,.1+j*.025));d.line(pts+[pts[0]],fill=col(CYAN,.55+j*.08),width=3)
def captions(im,t):
    active=next((c for c in CAPS if c['start']<=t<=c['end']),None)
    if not active:return
    lines=['']
    for w in active['text'].split():
        test=(lines[-1]+' '+w).strip()
        if font(23).getlength(test)>1100*S:lines.append(w)
        else:lines[-1]=test
    assert len(lines)<=2
    for j,s in enumerate(lines):text(im,s,640,650+j*31,23,WHITE)
def content(i,t):
    im=Image.new('RGB',(W,H),BLACK);st=TIMING['segments'][i]['start_seconds'];u=t-st
    if i==0:
        text(im,'SUMMIT ONE',640,65,16,DIM);trace(im,[(485,325),(640,185),(795,325),(485,325)],anim(u,.2,2),CYAN,2.5);dot(im,640,185,5,GOLD,anim(u,1.3))
        text(im,'Hi, Reef.',640,400,69,WHITE,'math',anim(u,.15));text(im,'Your next discovery starts here.',640,485,27,GOLD,a=anim(t,cue(i,'Get curious')))
        for k in range(5):dot(im,540+k*50,557,4,CYAN,anim(t,cue(i,'one small step')+.12*k,.4))
    elif i==1:
        heading(im,'Three destinations. A world of ideas.','Your journey');xs=[265,640,1015];trace(im,[(265,320),(640,320),(1015,320)],anim(u,1,3),DARK,2)
        for k,(x,title,sub,word) in enumerate(zip(xs,['AMC','MAWA','Rossmoyne'],['Creative problems','Explain your thinking','Honours Mathematics'],['Australian','Problem Solving',"Rossmoyne's"])):
            a=anim(t,cue(i,word),.65);ring(im,x,320,78,CYAN if k<2 else GOLD,2,a);text(im,['?','','△'][k],x,320,60,CYAN if k<2 else GOLD,'math',a);text(im,title,x,450,34,WHITE,'math',a);text(im,sub,x,503,19,DIM,a=a)
            if k==1:
                for dx,dy in [(0,-20),(-21,19),(21,19)]:dot(im,x+dx,320+dy,6,CYAN,a)
    elif i==2:
        heading(im,'A long tradition of curious thinkers','Did you know?');trace(im,[(260,330),(1020,330)],anim(u,.4,1.7),CYAN,2)
        for x,date,label,word in zip([260,640,1020],['1978','2002','You'],['First national AMC','Primary divisions join','The next chapter'],['nineteen','Primary','joining']):
            a=anim(t,cue(i,word),.6);dot(im,x,330,7,GOLD,a);text(im,date,x,252,63,GOLD,'math',a);text(im,label,x,408,21,WHITE,a=a)
        text(im,'Australian Mathematics Competition',640,533,22,DIM,a=anim(u,1))
    elif i==3:
        heading(im,'Look beneath the story','The problem solver’s eye');a=anim(t,cue(i,'notice'),1.3);pts=[(360,280),(560,280),(360,460)];d=ImageDraw.Draw(im)
        d.polygon([(x*S,y*S) for x,y in pts],fill=col(CYAN,.22));line(im,pts+[pts[0]],CYAN,3)
        coords=[travel(p,q,a,35) for p,q in zip([(760,290),(960,470),(760,470)],[(560,280),(560,460),(360,460)])]
        d.polygon([(round(x*S),round(y*S)) for x,y in coords],fill=col(GOLD,.2));line(im,coords+[coords[0]],GOLD,3)
        text(im,'Different pieces',860,260,26,DIM,a=1-a);text(im,'One useful structure',825,370,33,GOLD,'math',a);text(im,'A good picture can reveal the next step.',640,551,24,WHITE,a=anim(u,1))
    elif i==4:
        heading(im,'A sum you can see','One small aha moment')
        for j,(word,n) in enumerate([('One dot',1),('three',2),('five',3),('seven',4)]):
            a=anim(t,cue(i,word),.95);cells=[(x,y) for y in range(n) for x in range(n) if x==n-1 or y==n-1]
            for k,(x,y) in enumerate(cells):dot(im,*travel((175+k*34,530),(535+x*70,240+y*70),a,70),14,CYAN if j%2==0 else GOLD,anim(t,cue(i,word),.2))
        a=anim(t,cue(i,'four-by-four'),.65);trace(im,[(500,205),(780,205),(780,485),(500,485),(500,205)],a,WHITE,1.4);text(im,'1 + 3 + 5 + 7',640,547,34,WHITE,'math');text(im,'4 × 4 = 16',1000,348,39,GOLD,'math',a)
    elif i==5:
        heading(im,'MAWA · Problem Solving Program','Explore and explain');a=anim(t,cue(i,'nineteen'),.8);text(im,'1992',360,320,103,GOLD,'math',a);text(im,'The programme begins',360,421,20,DIM,a=a)
        rect(im,880,345,360,250,c='#081c25',outline=CYAN);text(im,'WHY?',880,320,61,CYAN,'math');text(im,'Make your reasoning visible',880,413,18,WHITE,a=anim(t,cue(i,'Explaining')));text(im,'Mathematical Association of Western Australia',640,542,23,WHITE)
    elif i==6:
        heading(im,'Notice. Test. Explain.','The investigation mindset')
        for n,x,word in [(2,275,'patterns'),(3,640,'small cases'),(4,1005,'explanations')]:
            a=anim(t,cue(i,word),.7)
            for row in range(n):
                for j in range(row+1):dot(im,x+(j-row/2)*35,270+row*35,9,CYAN if row<n-1 else GOLD,a)
            text(im,['Notice a pattern','Test another case','Explain the rule'][n-2],x,453,22,WHITE,a=a)
        text(im,'Does this always work?',640,550,34,GOLD,'math',anim(t,cue(i,'Does this always')))
    elif i==7:
        heading(im,'Rossmoyne · Honours Mathematics','Go beyond the familiar');cube(im,(360,365),u*.12,103);a=anim(t,cue(i,'Fermat Club'),.7)
        text(im,'The Fermat Club',895,303,38,GOLD,'math',a);text(im,'Curiosity + collaboration',895,367,23,WHITE,a=a)
        for j,x in enumerate([810,895,980]):
            aa=anim(t,cue(i,'together')+j*.14,.6);ring(im,x,460,20,CYAN,2,aa)
            if j:line(im,[(x-65,460),(x-20,460)],CYAN,2,aa)
        text(im,'Explore mathematics beyond the usual curriculum.',640,558,23,DIM)
    elif i==8:
        heading(im,'Build a toolkit that travels with you','Flexible thinking')
        for k,(x,label,word) in enumerate(zip([265,640,1015],['Draw a diagram','Work backwards','Break it into parts'],['Draw a diagram','Work backwards','Break a big'])):
            a=anim(t,cue(i,word),.8)
            if k==0:trace(im,[(x-75,400),(x,245),(x+75,400),(x-75,400)],a,CYAN,3);line(im,[(x,245),(x,400)],GOLD,2,a)
            elif k==1:
                for j,v in enumerate(['?','× 3','24']):text(im,v,x-100+j*100,330,35,WHITE,'math',a)
                arrow(im,(x+90,395),(x-90,395),GOLD,a)
            else:
                rect(im,x,280,66,66,c='#071c25',a=a)
                for dx in [-75,0,75]:arrow(im,(x,320),(x+dx,365),CYAN,a);rect(im,x+dx,404,45,45,c='#071c25',a=a)
            text(im,label,x,490,24,WHITE,a=a)
    elif i==9:
        heading(im,'Understand it. Try it. Make it yours.','Inside a lesson')
        for k,(label,word) in enumerate([('Meet the idea','introduces'),('See it work','shows'),('Try it','try it')]):
            x=300+340*k;a=anim(t,cue(i,word),.6);dot(im,x,245,6,GOLD,a);text(im,label,x,292,23,WHITE,a=a)
            if k:line(im,[(x-334,245),(x-6,245)],CYAN,2,a)
        a=anim(t,cue(i,'Quick choices'),.6);text(im,'2, 4, 6, …',640,385,42,CYAN,'math',a)
        for x,s in [(495,'A   8'),(785,'B   9')]:rect(im,x,474,200,76,c='#071c25',outline=CYAN,a=a);text(im,s,x,474,30,WHITE,'math',a)
        q=anim(t,cue(i,'before deeper'),.55);rect(im,495,474,200,76,c='#233321',outline=GOLD,a=q);text(im,'A   8',495,474,30,GOLD,'math',q);text(im,'Quick decisions → deeper reasoning',640,563,22,DIM,a=a)
    elif i==10:
        heading(im,'New story. A useful idea you recognise.','Transfer your learning');a=anim(t,cue(i,'numbers'),1.3)
        for j in range(12):dot(im,*travel((340+(j%3)*65,245+(j//3)*65),(780+(j%6)*50,320+(j//6)*65),a,80),13,CYAN if j<6 else GOLD)
        text(im,'4 groups of 3',415,548,28,WHITE,'math',1-a);text(im,'2 groups of 6',910,548,28,WHITE,'math',a);text(im,'12',640,232,57,GOLD,'math');text(im,'Regrouping keeps the total unchanged.',640,592,21,DIM,a=anim(u,1))
    elif i==11:
        heading(im,'Stuck? You have a next move.','Confidence grows through practice')
        for k,(x,title,word) in enumerate(zip([270,640,1010],['Try a small case','Make a sketch','Check a clue'],['smaller example','Make a sketch','Check a clue'])):
            a=anim(t,cue(i,word),.7);ring(im,x,330,73,CYAN,2,a)
            if k==0:
                for dx in [-17,17]:
                    for dy in [-17,17]:dot(im,x+dx,330+dy,7,GOLD,a)
            if k==1:trace(im,[(x-40,360),(x-8,300),(x+40,360)],a,GOLD,3)
            if k==2:trace(im,[(x-32,330),(x-7,354),(x+38,307)],a,GOLD,4)
            text(im,title,x,454,25,WHITE,a=a)
        text(im,'A careful attempt is useful information.',640,555,27,GOLD,'math',anim(t,cue(i,'Every careful attempt')))
    elif i==12:
        heading(im,'Rehearse. Review. Improve.','Practice papers');rect(im,370,360,300,330,c='#071016',outline=DIM)
        for k in range(4):
            y=250+k*62;a=anim(u,.3+k*.65,.6);text(im,str(k+1),267,y,18,DIM,a=a);trace(im,[(300,y),(465,y)],a,CYAN,2)
            if k<3:trace(im,[(485,y),(493,y+7),(506,y-11)],a,GOLD,2)
        ring(im,800,300,62,CYAN,2);line(im,[(800,258),(800,300),(835,317)],GOLD,3);text(im,'Read · Plan · Check',870,417,25,WHITE)
        a=anim(t,cue(i,'Afterwards'),.7);arrow(im,(565,474),(700,474),GOLD,a);text(im,'Understand the solution',897,505,25,GOLD,'math',a);text(im,'Choose one thing to improve',897,550,21,DIM,a=a)
    elif i==13:
        heading(im,'One thoughtful step at a time','On exam day');ring(im,280,357,72+8*math.sin(u*.65),CYAN,2);text(im,'Breathe',280,357,29,WHITE,'math')
        for k,(label,word) in enumerate([('Start with what you know','Start with'),('Move on and return','move on'),('Aim high. Think carefully.','Aim high')]):
            a=anim(t,cue(i,word),.7);dot(im,515,270+k*92,5,GOLD,a);text(im,label,850,270+k*92,29,WHITE,'math',a)
    else:
        text(im,'SUMMIT ONE',640,62,16,DIM);text(im,'Your next discovery starts here.',640,152,43,WHITE,'math');pts=[(325,460),(445,390),(540,408),(665,295),(760,318),(920,220)];trace(im,pts,anim(u,.3,3),CYAN,3)
        for k,p in enumerate(pts):dot(im,*p,5,GOLD,anim(u,.5+k*.45,.5))
        text(im,'Curiosity',340,526,24,CYAN,a=anim(t,cue(i,'curiosity')));text(im,'Practice',640,526,24,CYAN,a=anim(t,cue(i,'toolkit')));text(im,'Discovery',940,526,24,GOLD,a=anim(t,cue(i,'aha moments')));text(im,'Let’s begin, Reef.',640,596,30,GOLD,'math',anim(t,cue(i,'Your next discovery')))
    return im

def frame(t):
    i=max(j for j,s in enumerate(TIMING['segments']) if s['start_seconds']<=t);im=content(i,t);st=TIMING['segments'][i]['start_seconds']
    if i and t-st<.38:im=Image.blend(content(i-1,st-.01),im,ease((t-st)/.38))
    captions(im,t);return im

def main():
    global TIMING,WORDS,CAPS
    p=argparse.ArgumentParser();p.add_argument('--preview',action='store_true');p.add_argument('--layout-preview',action='store_true');args=p.parse_args();ROOT.mkdir(parents=True,exist_ok=True)
    if args.layout_preview:
        # For layout inspection only. The actual render requires completed audio alignment.
        doc=json.loads((SRC/'narration.json').read_text());segs=[];WORDS=[];cursor=0
        for i,s in enumerate(doc['segments']):
            ws=s.split();dur=len(ws)*.45;segs.append({'start_seconds':cursor,'duration_seconds':dur});WORDS.extend({'text':w,'segment':i+1,'start':cursor+j*.45,'end':cursor+(j+1)*.45} for j,w in enumerate(ws));cursor+=dur+.7
        TIMING={'segments':segs,'duration_seconds':cursor};CAPS=[]
    else:TIMING=json.loads((ROOT/'timing.json').read_text());WORDS=json.loads((ROOT/'words.json').read_text())['words'];CAPS=json.loads((ROOT/'captions.json').read_text())
    duration=TIMING['duration_seconds']+2.8;shots=[];(ROOT/'storyboard').mkdir(exist_ok=True)
    for i,seg in enumerate(TIMING['segments']):
        for f in [.25,.66,.94]:
            shot=frame(seg['start_seconds']+seg['duration_seconds']*f);shot.save(ROOT/'storyboard'/f'{i+1:02d}-{f:.2f}.jpg',quality=90)
            if f==.94:shots.append(shot)
    contact=Image.new('RGB',(1278,240*math.ceil(len(shots)/3)),BLACK)
    for k,shot in enumerate(shots):contact.paste(shot.resize((426,240)),((k%3)*426,(k//3)*240))
    contact.save(ROOT/'contact.jpg',quality=94)
    poster=Image.new('RGB',(W,H),BLACK);text(poster,'SUMMIT ONE',640,105,19,DIM);text(poster,'Hi, Reef.',640,280,80,WHITE,'math');text(poster,'Your next discovery starts here.',640,399,36,GOLD,'math');trace(poster,[(410,568),(530,480),(640,523),(780,470),(870,500)],1,CYAN,3);poster.save(ROOT/'poster.jpg',quality=95)
    if args.preview or args.layout_preview:return
    proc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-vcodec','rawvideo','-s',f'{W}x{H}','-pix_fmt','rgb24','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(ROOT/'visual.mp4')],stdin=subprocess.PIPE)
    for k in range(math.ceil(duration*FPS)):
        proc.stdin.write(frame(k/FPS).tobytes())
        if k%600==0:print(f'Rendering {k}/{math.ceil(duration*FPS)} frames',flush=True)
    proc.stdin.close();assert proc.wait()==0
if __name__=='__main__':main()
