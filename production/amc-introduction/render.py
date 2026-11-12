"""AMC introduction: original mathematical motion, aligned to completed voice C narration."""
import argparse, functools, json, math, re, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ROOT=Path('build/amc-introduction'); SRC=Path(__file__).parent
W,H,S,FPS=1920,1080,1.5,30
BLACK='#03080d';WHITE='#f7f7f7';CYAN='#28bbee';GOLD='#ffd36a';DIM='#9baab5';DARK='#183442'
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
    text(im,chapter.upper(),640,48,15,CYAN);text(im,title,640,108,38,WHITE,'math')
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

def polygon(im,pts,c,a=1):
    ImageDraw.Draw(im).polygon([(round(x*S),round(y*S)) for x,y in pts],fill=col(c,a))

def equation(im,s,y=550,c=GOLD,a=1,n=40):text(im,s,640,y,n,c,'math',a)

def grid(im,x,y,cols,rows,cell=65,a=1):
    for r in range(rows+1):line(im,[(x,y+r*cell),(x+cols*cell,y+r*cell)],DIM,1.5,a)
    for c in range(cols+1):line(im,[(x+c*cell,y),(x+c*cell,y+rows*cell)],DIM,1.5,a)

def selected_rect(im,x,y,cell,hpair,vpair,a=1):
    top,bottom=hpair;left,right=vpair
    polygon(im,[(x+left*cell,y+top*cell),(x+right*cell,y+top*cell),(x+right*cell,y+bottom*cell),(x+left*cell,y+bottom*cell)],CYAN,.12*a)
    for r in hpair:line(im,[(x,y+r*cell),(x+4*cell,y+r*cell)],GOLD,4,a)
    for c in vpair:line(im,[(x+c*cell,y),(x+c*cell,y+3*cell)],CYAN,4,a)
    for r in hpair:
        for c in vpair:dot(im,x+c*cell,y+r*cell,5,WHITE,a)

def cycle(im,i,t,y=350,highlight=False):
    for j,(x,v) in enumerate(zip([340,540,740,940],[3,9,7,1])):
        if i==6:
            words=['repeat three','nine','seven','seven one'];a=anim(t,cue(i,words[j]),.45)
        else:a=1
        ring(im,x,y,48,CYAN,2,a);text(im,v,x,y,44,WHITE,'math',a)
        text(im,['1st','2nd','3rd','4th'][j],x,y+80,21,DIM,a=a)
        if j:arrow(im,(x-143,y),(x-58,y),CYAN,a)
    a=anim(t,cue(i,'Four positions'),.6) if i==6 else 1
    trace(im,[(940,y-60),(940,y-100),(340,y-100),(340,y-60)],a,CYAN,2)
    if highlight:
        a=anim(t,cue(i,'third position'),.5);ring(im,740,y,54,GOLD,4,a);text(im,7,740,y,44,GOLD,'math',a)

def content(i,t):
    im=Image.new('RGB',(W,H),BLACK);st=TIMING['segments'][i]['start_seconds'];u=t-st
    C=lambda phrase: cue(i,phrase)
    A=lambda phrase,d=.7: anim(t,C(phrase),d)
    if i==0:
        text(im,'SUMMIT ONE',640,53,17,DIM)
        text(im,'Think your way through.',640,144,51,WHITE,'math',anim(u,.1,1))
        a=A('huge number');text(im,'3¹²³',285,350,78,CYAN,'math',a)
        text(im,'Number',285,472,23,DIM,a=a)
        a=A('hidden pattern')
        for k in range(4):
            ang=-math.pi/2+k*math.pi/2+.08*u
            dot(im,640+65*math.cos(ang),350+65*math.sin(ang),10,GOLD,a)
        ring(im,640,350,65,GOLD,1.5,a);text(im,'Pattern',640,472,23,DIM,a=a)
        a=A('puzzling shape')
        if a: cube(im,(1000,350),u*.1,64)
        text(im,'Shape',1000,472,23,DIM,a=a)
        text(im,'Your introduction to AMC Upper Primary',640,564,28,GOLD,a=A('Australian Mathematics'))
    elif i==1:
        heading(im,'One hour. Thirty opportunities.','How the exam works')
        text(im,'UPPER PRIMARY · YEARS 5–6',640,181,22,DIM,a=A('Years Five'))
        a=A('sixty minutes');ring(im,330,372,126,CYAN,3,a)
        for k in range(12):
            angle=k*math.pi/6-math.pi/2
            line(im,[(330+111*math.cos(angle),372+111*math.sin(angle)),(330+119*math.cos(angle),372+119*math.sin(angle))],DIM,2,a)
        text(im,'60',330,349,90,WHITE,'math',a);text(im,'minutes',330,421,24,CYAN,a=a)
        q=A('thirty questions',1.3)
        for n in range(30):
            x=735+(n%6)*53;y=269+(n//6)*48
            b=clamp(q*30-n);rect(im,x,y,36,31,c=DARK,outline=CYAN if n<25 else GOLD,a=b,r=5)
            text(im,n+1,x,y,15,WHITE,a=b)
        text(im,'30 questions',867,522,32,WHITE,'math',q)
        text(im,'Online or paper · a growing challenge',640,590,24,DIM,a=A('on paper'))
    elif i==2:
        heading(im,'Two ways to give your answer','The question formats')
        a=A('multiple choice');text(im,'Questions 1–25',350,230,29,CYAN,'math',a)
        text(im,'Choose one answer',350,286,25,WHITE,a=a)
        for j,l in enumerate('ABCDE'):
            x=174+j*88;ring(im,x,387,34,CYAN if j!=2 else GOLD,2,a);text(im,l,x,387,28,WHITE,a=a)
        text(im,'A · B · C · D · E',350,497,26,DIM,a=a)
        a=A('final five');text(im,'Questions 26–30',930,230,29,GOLD,'math',a)
        text(im,'Supply a whole number',930,286,25,WHITE,a=a)
        for j,l in enumerate('146'):
            x=845+j*85;rect(im,x,387,68,86,c=DARK,outline=GOLD,a=a);text(im,l,x,387,45,WHITE,'math',a)
        text(im,'Illustrative answer entry',930,461,18,DIM,a=a)
        text(im,'0–999 inclusive',930,524,30,GOLD,'math',A('zero'))
    elif i==3:
        heading(im,'Every part of the paper counts','135 marks available')
        blocks=[(200,'1–10','10 × 3','30','three each'),(485,'11–20','10 × 4','40','four for'),(770,'21–25','5 × 5','25','then five'),(1055,'26–30','6+7+8+9+10','40','worth six')]
        for x,qs,expr,total,phrase in blocks:
            a=A(phrase);text(im,'Q'+qs,x,237,25,DIM,a=a);rect(im,x,359,246,150,c=DARK,outline=CYAN if x<1000 else GOLD,a=a)
            text(im,expr,x,330,29 if x<1000 else 24,WHITE,'math',a);text(im,total+' marks',x,390,27,CYAN if x<1000 else GOLD,'math',a)
        equation(im,'30 + 40 + 25 + 40 = 135',548,GOLD,A('one hundred'),40)
    elif i==4:
        heading(im,'Use your time thoughtfully','A calm exam strategy')
        for k,(label,phrase) in enumerate([('No marks deducted for wrong answers','Wrong answers'),('Solve what you can; return to tougher ones','Start with'),('Check unanswered questions','Leave time')]):
            a=A(phrase);y=258+k*96;trace(im,[(104,y),(117,y+12),(139,y-16)],a,CYAN,3);text(im,label,480,y,25,WHITE,a=a)
        a=A('pocket or scientific');rect(im,1045,353,165,234,c=DARK,outline=GOLD,a=a)
        rect(im,1045,284,120,47,c=BLACK,outline=DIM,a=a,r=5);text(im,'12 × 4',1045,284,19,CYAN,a=a)
        for row in range(3):
            for c in range(3):rect(im,1005+c*40,345+row*43,27,28,c=DARK,outline=DIM,a=a,r=4)
        text(im,'Calculator permitted',1045,517,20,GOLD,a=a);text(im,'Current Upper Primary rules',1045,550,16,DIM,a=a)
        text(im,'Read carefully. Plan. Solve. Check.',640,594,26,GOLD,a=A('Careful reasoning'))
    elif i==5:
        heading(im,'Many topics. A connected toolkit.','The kinds of problems you will meet')
        tiles=[('Number','3¹²³','number',CYAN),('Fractions & ratios','3 : 5','fractions',GOLD),('Algebra','2x + 7','algebra',CYAN),('Geometry & measure','△  □','geometry',GOLD),('Data & chance','1 / 6','statistics',CYAN),('Counting & logic','1, 2, 3, …','counting',GOLD)]
        for k,(label,symbol,phrase,c) in enumerate(tiles):
            x=260+k%3*380;y=285+k//3*200;a=A(phrase)
            rect(im,x,y,330,154,c='#09131c',outline=DARK,a=a);text(im,symbol,x,y-21,40,c,'math',a);text(im,label,x,y+42,24,WHITE,a=a)
        text(im,'Spot the structure beneath the story.',640,605,25,GOLD,a=A('mathematical structure'))
    elif i==6:
        heading(im,'Find the last digit of 3¹²³','Number patterns · cycles')
        text(im,'One huge power. Just four last digits.',640,178,23,DIM,a=A('final digit'))
        cycle(im,i,t,365)
        text(im,'3¹ → 3      3² → 9      3³ → 7      3⁴ → 1',640,520,30,WHITE,'math',A('Four positions'))
        text(im,'The pattern repeats every 4 powers.',640,591,26,GOLD,a=A('Four positions'))
    elif i==7:
        heading(im,'123 powers → a remainder of 3','Number patterns · choose the position')
        equation(im,'123 = 30 × 4 + 3',209,WHITE,A('thirty groups'),44)
        cycle(im,i,t,385,True)
        text(im,'30 complete cycles',406,546,27,DIM,a=A('thirty groups'))
        text(im,'3 more positions',879,546,27,GOLD,a=A('three left'))
        text(im,'Last digit: 7',640,603,34,GOLD,'math',A('position seven'))
    elif i==8:
        heading(im,'Blue : gold = 3 : 5. Gold has 12 more.','Ratios · equal parts')
        text(im,'How many counters altogether?',640,177,25,WHITE)
        left,cell,y1,y2=315,125,300,411
        text(im,'Blue',204,y1,27,CYAN,a=A('Blue and gold'));text(im,'Gold',204,y2,27,GOLD,a=A('Blue and gold'))
        a=A('ratio three to five')
        for r,n,c in [(y1,3,CYAN),(y2,5,GOLD)]:
            for j in range(n):
                rect(im,left+j*cell,r,116,66,c=c,outline=c,a=.75*a,r=5)
                text(im,'6',left+j*cell,r,29,WHITE,'math',A('each part is six'))
        a=A('twelve more');trace(im,[(left+3*cell-54,458),(left+3*cell-54,478),(left+4*cell+54,478),(left+4*cell+54,458)],a,GOLD,2)
        text(im,'2 parts = 12',left+3.5*cell,513,25,GOLD,'math',a)
        equation(im,'1 part = 6     →     8 parts = 48',584,WHITE,A('Altogether'),34)
    elif i==9:
        heading(im,'How many rectangles in a 3 × 4 grid?','Geometry · organised counting')
        x,y,cell=172,260,80;grid(im,x,y,4,3,cell)
        hchoices=[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)];vchoices=[(0,1),(0,2),(0,3),(0,4),(1,2),(1,3),(1,4),(2,3),(2,4),(3,4)]
        ht=A('four horizontal');vt=A('five vertical')
        if ht:
            h=hchoices[min(5,int(max(0,t-C('four horizontal'))/.7))]
            for r in h:line(im,[(x,y+r*cell),(x+4*cell,y+r*cell)],GOLD,4,ht)
        else:h=(0,1)
        if vt:
            v=vchoices[min(9,int(max(0,t-C('five vertical'))/.65))]
            selected_rect(im,x,y,cell,h,v,vt)
        text(im,'4 horizontal lines',332,211,23,GOLD,a=ht);text(im,'5 vertical lines',332,547,23,CYAN,a=vt)
        text(im,'Choose 2 horizontal',887,274,29,GOLD,a=ht);text(im,'Choose 2 vertical',887,354,29,CYAN,a=vt)
        text(im,'6 × 10 = 60',887,460,48,WHITE,'math',A('Six choices'))
        text(im,'Include rectangles of every size.',640,604,26,DIM,a=A('sixty rectangles'))
    elif i==10:
        heading(im,'Subtract 5, double, add 7 → 31','Algebra · work backwards')
        text(im,'What was the starting number?',640,176,25,WHITE)
        xs=[190,490,790,1090];labels=['?','− 5','× 2','+ 7']
        phases=['Five is subtracted','Five is subtracted','is doubled','seven is added']
        # Forward transformation: number → after subtracting 5 → after doubling → 31.
        for j,x in enumerate(xs):
            a=A(phases[j]);rect(im,x,297,126,83,c=DARK,outline=CYAN,a=a)
            val=['x','x − 5','2(x − 5)','31'][j];text(im,val,x,297,26 if j in [1,2] else 38,WHITE,'math',a)
            if j:
                arrow(im,(xs[j-1]+75,297),(x-75,297),CYAN,a);text(im,labels[j],x-150,246,25,CYAN,a=a)
        phrases=['starting number','then add five','halve','subtract seven']
        inverse=[17,12,24,31]
        for j in [3,2,1,0]:
            x=xs[j];phrase=['then add five','halve','subtract seven','Undo the steps'][j];a=A(phrase)
            text(im,inverse[j],x,465,49,GOLD,'math',a)
            if j<3:
                arrow(im,(xs[j+1]-70,465),(x+70,465),GOLD,a);text(im,['+ 5','÷ 2','− 7'][j],x+150,408,26,GOLD,a=a)
        equation(im,'Check: 2 × (17 − 5) + 7 = 31',584,WHITE,A('seventeen'),33)
    elif i==11:
        heading(im,'Two fair dice: what is P(total = 7)?','Probability · count organised cases')
        x,y,cell=192,246,47;grid(im,x,y,6,6,cell,A('two fair'))
        for r in range(6):
            text(im,r+1,x-26,y+(r+.5)*cell,20,DIM,a=A('two fair'))
            text(im,r+1,x+(r+.5)*cell,y-25,20,DIM,a=A('two fair'))
            for c in range(6):
                a=A('Six ordered',1.5)
                if r+c==5:
                    aa=clamp(a*6-r);rect(im,x+(c+.5)*cell,y+(r+.5)*cell,cell-4,cell-4,c=GOLD,outline=GOLD,a=.75*aa,r=2);text(im,'7',x+(c+.5)*cell,y+(r+.5)*cell,22,WHITE,a=aa)
                else:dot(im,x+(c+.5)*cell,y+(r+.5)*cell,2,DARK,A('two fair'))
        text(im,'Die 1',333,563,22,DIM,a=A('two fair'));text(im,'Die 2',117,378,21,DIM,a=A('two fair'))
        text(im,'6 outcomes total 7',870,285,29,GOLD,a=A('Six ordered'))
        text(im,'36 equally likely outcomes',870,371,25,WHITE,a=A('thirty-six'))
        text(im,'6 / 36 = 1 / 6',870,477,43,CYAN,'math',A('one sixth'))
        text(im,'(1, 6) and (6, 1) are different ordered outcomes.',640,610,23,DIM,a=A('exactly once'))
    elif i==12:
        heading(im,'Can 15 counters form two equal groups?','Logic · parity and impossibility')
        text(im,'Whole counters only',640,181,24,DIM)
        q=A('Pair them',1.4)
        for k in range(15):
            p=(310+(k%5)*160,270+(k//5)*100)
            dest=(280+(k%7)*120,310 if k<7 else 445) if k<14 else (1000,567)
            pos=travel(p,dest,q,22);dot(im,*pos,21,CYAN if k<7 else GOLD)
        a=A('one is left');ring(im,1000,567,32,GOLD,2,a);text(im,'1 left over',1130,567,21,GOLD,a=a)
        text(im,'7 + 7 + 1 = 15',640,574,36,WHITE,'math',a)
        text(im,'An odd total cannot split equally into two whole-number groups.',640,611,22,DIM,a=A('This is parity'))
    elif i==13:
        heading(im,'An idea before a challenge','How you will learn')
        for k,(x,label,phrase,sub) in enumerate([(270,'What does it solve?','what it solves','Meet the idea'),(640,'Why does it help?','why it helps','See the reason'),(1010,'When can I use it?','when to use','Spot the clue')]):
            a=A(phrase);ring(im,x,320,67,CYAN if k!=1 else GOLD,2,a);text(im,['?','→','!'][k],x,320,56,WHITE,'math',a);text(im,label,x,434,26,WHITE,a=a);text(im,sub,x,487,23,DIM,a=a)
        text(im,'Small worked example → a growing challenge',640,586,29,GOLD,'math',A('small worked example'))
    elif i==14:
        heading(im,'Practise choosing the next move','Five quick A / B decisions')
        for k in range(5):dot(im,560+k*40,180,6,GOLD if k==0 else DARK)
        grid(im,160,297,4,3,65)
        text(im,'Count every rectangle.',290,246,24,WHITE)
        a=A('count squares');rect(im,869,307,564,83,c=DARK,outline=DIM,a=a)
        text(im,'A   Count only the squares',869,307,25,WHITE,a=a)
        a=A('choose pairs');rect(im,869,438,564,105,c=DARK,outline=CYAN,a=a)
        text(im,'B   Choose boundary-line pairs',869,438,25,WHITE,a=a)
        a=A('Choose the lines');rect(im,869,438,564,105,c='#143b45',outline=GOLD,a=a);text(im,'B   Choose boundary-line pairs',869,438,25,GOLD,a=a)
        selected_rect(im,160,297,65,(0,2),(1,4),a)
        text(im,'Choose a method. Explain why it fits.',640,590,27,GOLD,a=A('recognise the next move'))
    elif i==15:
        heading(im,'Make the method your own','From support to independence')
        items=[('With support','with support'),('On your own','independently'),('A new setting','different-looking'),('Explain & check','Explain your plan')]
        for k,(label,phrase) in enumerate(items):
            x=205+k*290;a=A(phrase)
            if k:arrow(im,(x-202,350),(x-90,350),CYAN,a)
            ring(im,x,350,64,CYAN if k<3 else GOLD,2,a);text(im,k+1,x,350,43,WHITE,'math',a);text(im,label,x,466,25,WHITE,a=a)
        text(im,'New numbers · new diagrams · new stories',640,557,28,GOLD,a=A('numbers and stories'))
        text(im,'A method you can recognise and use again.',640,606,23,DIM,a=A('unseen questions'))
    elif i==16:
        heading(im,'Practise. Review. Repair. Return.','Turn an exam into useful feedback')
        a=A('under a timer');ring(im,270,331,83,CYAN,2,a);text(im,'60:00',270,331,37,WHITE,'math',a)
        text(im,'Mock exam',270,466,24,DIM,a=a)
        a=A('Afterwards');arrow(im,(380,331),(495,331),CYAN,a)
        for k,(label,phrase) in enumerate([('Reading','reading'),('Method','choosing a method'),('Calculating','calculating'),('Checking','checking')]):
            y=234+k*74;a=A(phrase);rect(im,713,y,300,56,c=DARK,outline=CYAN if k!=1 else GOLD,a=a,r=6);text(im,label,713,y,23,WHITE,a=a)
        a=A('Repair that skill');arrow(im,(925,331),(1000,331),GOLD,a);ring(im,1100,331,53,GOLD,2,a);trace(im,[(1074,333),(1094,351),(1130,309)],a,GOLD,3)
        text(im,'Targeted practice',1086,450,23,GOLD,a=a);text(im,'Revisit later',1086,496,23,DIM,a=A('revisit it later'))
        text(im,'Worked solutions help you understand the next step.',640,589,25,WHITE,a=A('worked solutions'))
    else:
        text(im,'SUMMIT ONE',640,58,17,DIM)
        text(im,'Curiosity. Method. Confidence.',640,162,46,WHITE,'math',anim(u,.1,1))
        pts=[(245,461),(395,385),(545,406),(695,307),(845,333),(1035,237)]
        trace(im,pts,anim(u,1,6),CYAN,3)
        for j,p in enumerate(pts):dot(im,*p,6,GOLD,anim(u,1+j*.9,.7))
        for x,label,phrase in [(280,'Find a clue','a clue'),(640,'Try a small case','small case'),(1000,'Build your toolkit','your toolkit')]:text(im,label,x,541,25,CYAN,a=A(phrase))
        text(im,'Let’s begin.',640,610,34,GOLD,'math',A("Let's begin"))
    return im

def frame(t):
    i=max(j for j,s in enumerate(TIMING['segments']) if s['start_seconds']<=t)
    im=content(i,t);st=TIMING['segments'][i]['start_seconds']
    if i and t-st<.38:im=Image.blend(content(i-1,st-.01),im,ease((t-st)/.38))
    # A single caption layer, with a separate dark safe area below the diagram.
    captions(im,t)
    line(im,[(0,718),(1280*min(1,t/(TIMING['duration_seconds']+2.8)),718)],CYAN,2,.7)
    return im

def main():
    global TIMING,WORDS,CAPS
    p=argparse.ArgumentParser();p.add_argument('--preview',action='store_true');p.add_argument('--layout-preview',action='store_true');args=p.parse_args();ROOT.mkdir(parents=True,exist_ok=True)
    if args.layout_preview:
        doc=json.loads((SRC/'narration.json').read_text());segs=[];WORDS=[];cursor=0
        for i,s in enumerate(doc['segments']):
            ws=s.split();dur=len(ws)*.42;segs.append({'start_seconds':cursor,'duration_seconds':dur});WORDS.extend({'text':w,'segment':i+1,'start':cursor+j*.42,'end':cursor+(j+1)*.42} for j,w in enumerate(ws));cursor+=dur+doc['pause_seconds'][i]
        TIMING={'segments':segs,'duration_seconds':cursor};CAPS=[]
    else:TIMING=json.loads((ROOT/'timing.json').read_text());WORDS=json.loads((ROOT/'words.json').read_text())['words'];CAPS=json.loads((ROOT/'captions.json').read_text())
    duration=TIMING['duration_seconds']+2.8;shots=[];(ROOT/'storyboard').mkdir(exist_ok=True)
    for i,seg in enumerate(TIMING['segments']):
        for f in [.25,.66,.94]:
            shot=frame(seg['start_seconds']+seg['duration_seconds']*f);shot.save(ROOT/'storyboard'/f'{i+1:02d}-{f:.2f}.jpg',quality=90)
            if f==.94:shots.append(shot)
    contact=Image.new('RGB',(1280,240*math.ceil(len(shots)/3)),BLACK)
    for k,shot in enumerate(shots):contact.paste(shot.resize((426,240)),((k%3)*426,(k//3)*240))
    contact.save(ROOT/'contact.jpg',quality=94)
    poster=Image.new('RGB',(W,H),BLACK)
    text(poster,'SUMMIT ONE',640,87,21,DIM);text(poster,'Think your way through.',640,221,56,WHITE,'math')
    text(poster,'Your AMC introduction',640,304,32,GOLD)
    text(poster,'3¹²³',305,455,70,CYAN,'math');grid(poster,565,384,3,2,52);cube(poster,(1010,444),.45,55)
    text(poster,'The exam · The ideas · Your learning journey',640,605,28,WHITE)
    poster.save(ROOT/'poster.jpg',quality=95)
    if args.preview or args.layout_preview:return
    proc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-vcodec','rawvideo','-s',f'{W}x{H}','-pix_fmt','rgb24','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(ROOT/'visual.mp4')],stdin=subprocess.PIPE)
    for k in range(math.ceil(duration*FPS)):
        proc.stdin.write(frame(k/FPS).tobytes())
        if k%600==0:print(f'Rendering {k}/{math.ceil(duration*FPS)} frames',flush=True)
    proc.stdin.close();assert proc.wait()==0
if __name__=='__main__':main()
