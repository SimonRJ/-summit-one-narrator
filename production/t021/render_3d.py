#!/usr/bin/env python3
"""Summit One T02.1 — original spatial mathematical animation, locked to existing audio.

Everything is drawn anew as a 3D world (perspective camera, lit solids, ground plane,
particle trajectories and parallax). Audio segment boundaries and word alignment
are read from the already-approved narration; nothing here generates speech.
The 120px caption strip is intentionally empty of new text.
"""
from __future__ import annotations
import argparse, functools, hashlib, json, math, os, re, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np

W,H=1280,720
BG=(5,12,27); WHITE=(239,248,255); MUTED=(157,176,195)
TEAL=(92,228,217); BLUE=(89,161,255); GOLD=(255,195,105)
MINT=(126,236,182); RED=(255,117,150); LILAC=(181,158,255)
FPS=24
FONT_REG=next((p for p in ['/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf','/usr/share/fonts/opentype/inter/Inter-Regular.otf'] if os.path.exists(p)),None)
FONT_BOLD=next((p for p in ['/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf','/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf'] if os.path.exists(p)),None)
if not FONT_REG or not FONT_BOLD: raise RuntimeError('Fonts unavailable')
@functools.lru_cache(100)
def F(size,bold=False):return ImageFont.truetype(FONT_BOLD if bold else FONT_REG,size)
def clip(x,a=0,b=1):return max(a,min(b,x))
def ease(x):
    x=clip(x);return x*x*(3-2*x)
def out(x):x=clip(x);return 1-(1-x)**3
def lerp(a,b,k):return a+(b-a)*k
def mix(a,b,k):return tuple(int(lerp(p,q,k)) for p,q in zip(a,b))
def rgba(rgb,a=255):return tuple(int(v) for v in rgb)+(int(clip(a/255)*255),)
def tx(d,x,y,s,size=24,color=WHITE,bold=False,anchor='mm',opacity=255,stroke=0):
    if opacity<=0:return
    d.text((int(x),int(y)),str(s),font=F(size,bold),fill=rgba(color,opacity),anchor=anchor,stroke_width=stroke,stroke_fill=(2,9,20,255))
def text_r(d,x,y,s,size=24,color=WHITE,bold=False,opacity=255):tx(d,x,y,s,size,color,bold,'rm',opacity)
def ln(d,pts,c=TEAL,width=2,a=255):d.line([(int(x),int(y)) for x,y in pts],fill=rgba(c,a),width=width,joint='curve')
def circ(d,x,y,r,c,a=255,outline=False,width=2):
    box=(int(x-r),int(y-r),int(x+r),int(y+r))
    if outline:d.ellipse(box,outline=rgba(c,a),width=width)
    else:d.ellipse(box,fill=rgba(c,a))
def glow(d,x,y,r,c,intensity=1):
    for mul,op in [(3.2,7),(2.35,15),(1.55,25)]:circ(d,x,y,r*mul,c,int(op*intensity))
def glow_line(d,p0,p1,col=TEAL,width=3,opacity=235):
    ln(d,[p0,p1],col,width+9,int(opacity*.08));ln(d,[p0,p1],col,width+4,int(opacity*.16));ln(d,[p0,p1],col,width,opacity)

def norm(s):return re.sub('[^a-z0-9]','',s.lower())

@functools.lru_cache(2)
def bg():
    ys,xs=np.ogrid[:H,:W]
    r1=np.exp(-(((xs-470)/720)**2 + ((ys-325)/560)**2)*1.4)
    r2=np.exp(-(((xs-1070)/550)**2 + ((ys-235)/500)**2)*2.1)
    vign=1-.23*(((xs-W/2)/(W/2))**2+((ys-H/2)/(H/2))**2)
    img=np.zeros((H,W,4),dtype=np.uint8)
    img[:,:,0]=np.clip((4+4*r1+2*r2)*vign,0,255).astype('uint8')
    img[:,:,1]=np.clip((12+12*r1+5*r2)*vign,0,255).astype('uint8')
    img[:,:,2]=np.clip((26+24*r1+16*r2)*vign,0,255).astype('uint8')
    img[:,:,3]=255
    im=Image.fromarray(img,'RGBA');d=ImageDraw.Draw(im,'RGBA')
    for i in range(140):
        x=(i*173+37)%W;y=85+(i*97)%470
        circ(d,x,y,1,WHITE,14 if i%4 else 28)
    d.rectangle((0,592,W,H),fill=(2,8,18,244))
    ln(d,[(0,592),(W,592)],(48,89,116),2,95)
    return im

class P3:
    """Actual rotating 3D perspective camera, not flat isometric cutouts."""
    def __init__(self,t,index=0,scale=99,cx=640,cy=452):
        self.yaw=.29+.19*math.sin(t*.30+index*.71)
        self.elev=.50+.07*math.sin(t*.23+index*.37)
        self.scale=scale;self.cx=cx;self.cy=cy
        self.c=math.cos(self.yaw);self.s=math.sin(self.yaw)
        self.ce=math.cos(self.elev);self.se=math.sin(self.elev)
    def p(self,x,y,z):
        X=self.c*x+self.s*z
        Z=-self.s*x+self.c*z
        Y=self.ce*y-self.se*Z
        D=self.se*y+self.ce*Z
        f=11.5/(11.5+D)
        return self.cx+X*self.scale*f,self.cy-Y*self.scale*f

def poly(d,proj,coords,color,alpha=240,outline=None):
    points=[proj.p(*pt) for pt in coords]
    d.polygon(points,fill=rgba(color,alpha))
    if outline:d.line(points+[points[0]],fill=rgba(outline,alpha),width=1,joint='curve')

def box3(d,P,x,y,z,size_x,size_y,size_z,col,opacity=250):
    # Front/right/top facets are physically projected, giving depth and changing
    # silhouettes as the camera moves.
    x0,x1=x-size_x/2,x+size_x/2
    z0,z1=z-size_z/2,z+size_z/2
    y0,y1=y,y+size_y
    front=[(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)]
    side=[(x1,y0,z0),(x1,y0,z1),(x1,y1,z1),(x1,y1,z0)]
    top=[(x0,y1,z0),(x1,y1,z0),(x1,y1,z1),(x0,y1,z1)]
    edge=mix(col,WHITE,.38)
    poly(d,P,front,mix(col,BG,.24),opacity)
    poly(d,P,side,mix(col,BG,.44),opacity)
    poly(d,P,top,mix(col,WHITE,.16),opacity,outline=edge)
    pp=P.p(x,y+size_y,z)
    if opacity>=200:circ(d,*pp,1.1,WHITE,75)

def plane(d,P,x=0,z=0,sx=3.3,sz=3.15,col=(19,53,71),outline=(56,121,142)):
    poly(d,P,[(x-sx/2,-.13,z-sz/2),(x+sx/2,-.13,z-sz/2),(x+sx/2,-.13,z+sz/2),(x-sx/2,-.13,z+sz/2)],col,244,outline)
    box3(d,P,x,-.28,z,sx,.16,sz,mix(col,BG,.35),225)

def grid(d,P,t):
    for i in range(-8,9):
        a=38 if i%2 else 57
        ln(d,[P.p(-9,-.55,i),P.p(9,-.55,i)],(60,127,150),1,a)
        ln(d,[P.p(i,-.55,-9),P.p(i,-.55,9)],(60,127,150),1,a)
    # translucent outer orbital markers reinforce depth, but never distract
    for k in range(8):
        x=5*math.cos(k*math.pi/4+t*.018)
        z=4*math.sin(k*math.pi/4+t*.018)
        px,py=P.p(x,-.49,z)
        circ(d,px,py,2.0,BLUE,95)

def particle(d,P,x,y,z,color=TEAL,r=8,a=255):
    px,py=P.p(x,y,z)
    glow(d,px,py,r,color,a/255)
    circ(d,px,py,r,color,a)
    circ(d,px-r*.24,py-r*.28,r*.21,WHITE,int(a*.80))

def positions(n,x):
    # Fixed physical grid slots: count maps to distinct 3D lattice sites.
    # Arrange back to front for convincing occlusion.
    cols=5
    pts=[]
    for i in range(n):
        row=i//cols
        col=i%cols
        pts.append((x+(col-2)*.49,.04,-.95+row*.52))
    return pts

def pile(d,P,count,x,color,intro=1.0,extra=0,move=None,ghost=False):
    # Draw cubes ordered in depth; never recreate a fixed 2D diagram.
    pts=positions(count,x)
    for k,(px,py,pz) in enumerate(pts):
        opacity=int(228*clip(intro*4-k*.10))
        if ghost:opacity=int(opacity*.32)
        if opacity<6:continue
        box3(d,P,px,py,pz,.40,.33,.40,color,opacity)
        if k%4==0:
            hx,hy=P.p(px,py+.33,pz)
            circ(d,hx,hy,1.3,WHITE,int(opacity*.23))

def pilestage(d,P,nL,nR,left=GOLD,right=TEAL,opL=1,opR=1,labels=('LEFT','RIGHT'),show_total=True):
    plane(d,P,-2.85,0,3.20,3.2,col=(15,43,62),outline=(57,103,130))
    plane(d,P,2.85,0,3.20,3.2,col=(13,44,58),outline=(60,108,115))
    pile(d,P,nL,-2.85,left,opL)
    pile(d,P,nR,2.85,right,opR)
    tx(d,354,520,f'{labels[0]}    {nL}',25,left,True)
    tx(d,914,520,f'{labels[1]}    {nR}',25,right,True)
    if show_total:
        tx(d,640,516,f'{nL} + {nR} = {nL+nR}',27,WHITE,True)

def mathtext(d,s,y=230,sz=55,col=WHITE,frac=1):
    tx(d,640,y,s,sz,col,True,opacity=int(255*ease(frac)))

def chapter(d,i,label,progress):
    tx(d,56,45,'SUMMIT ONE',17,WHITE,True,'lm')
    tx(d,208,45,'/  VISUAL MATHEMATICS',12,MUTED,False,'lm')
    text_r(d,1224,45,'T02.1   •   INVARIANTS',16,TEAL,True)
    ln(d,[(56,73),(1224,73)],(52,91,120),1,80)
    tx(d,69,106,f'{i+1:02d}',13,TEAL,True,'lm')
    tx(d,103,106,label.upper(),14,MUTED,True,'lm')
    d.rounded_rectangle((57,573,1223,576),radius=2,fill=(41,57,79,230))
    d.rounded_rectangle((57,573,57+int(1166*clip(progress)),576),radius=2,fill=rgba(TEAL,225))

def announce(d,headline,sub=None,size=43,x=640,y=159):
    tx(d,x,y,headline,size,WHITE,True)
    if sub:tx(d,x,y+47,sub,20,MUTED)

def arrow(d,p1,p2,col=TEAL,k=1):
    k=ease(k);x=lerp(p1[0],p2[0],k);y=lerp(p1[1],p2[1],k)
    glow_line(d,p1,(x,y),col,3)
    if k>.9:
        a=math.atan2(p2[1]-p1[1],p2[0]-p1[0]);l=13
        ln(d,[(x,y),(x-l*math.cos(a-.5),y-l*math.sin(a-.5))],col,4)
        ln(d,[(x,y),(x-l*math.cos(a+.5),y-l*math.sin(a+.5))],col,4)

class Story:
    def __init__(self,timing,words):
        self.seg=timing['segments'];self.words=words.get('words',words) if words else []
        self.spans=[]
        for i,s in enumerate(self.seg):
            st=float(s['start_seconds']);end=st+float(s['duration_seconds'])+float(s.get('pause_after',0))
            self.spans.append((st,end))
        self.total=max(x[1] for x in self.spans)
        self.byseg={i:[] for i in range(21)}
        for w in self.words:
            j=int(w.get('segment',w.get('index',1)))-1
            if 0<=j<21:self.byseg[j].append(w)
    def at(self,t):
        for i,(a,b) in enumerate(self.spans):
            if t < b or i==20:return i,clip((t-a)/(b-a))
        return 20,1.0
    def cue(self,i,phrase,default=.30):
        ws=self.byseg.get(i,[])
        wanted=[norm(x) for x in phrase.split() if norm(x)]
        got=[norm(w['text']) for w in ws]
        for j in range(len(got)-len(wanted)+1):
            if got[j:j+len(wanted)]==wanted:
                return float(ws[j]['start'])
        # Transcript relative position is still linked to this exact speech segment.
        base=[norm(w) for w in self.seg[i]['text'].split()]
        for j in range(len(base)-len(wanted)+1):
            if base[j:j+len(wanted)]==wanted:
                return self.spans[i][0]+(self.spans[i][1]-self.spans[i][0])*(j/max(1,len(base)))
        return self.spans[i][0]+(self.spans[i][1]-self.spans[i][0])*default
    def rise(self,i,t,phrase,seconds=.8,default=.3):return ease((t-self.cue(i,phrase,default))/seconds)

def band(d,y,value,label,col=TEAL,w=520,gl=0):
    x=640
    ln(d,[(x-w/2,y+27),(x+w/2,y+27)],col,2,120)
    tx(d,640,y,value,51,col,True)
    tx(d,640,y+54,label,18,MUTED)

def orbit(d,P,t,quantity=12,k=1):
    # Rotating 3D toroidal geometry; note truly projected x,y,z, not a planar orbit.
    for j in range(quantity):
        a=j*2*math.pi/quantity+t*.16
        x=2.9*math.cos(a);z=2.5*math.sin(a)
        y=.6+.56*math.sin(a*2+t*.12)
        particle(d,P,x,y,z,TEAL if j%2 else GOLD,7,220)
    for ring in [-.5,.5]:
        pts=[]
        for j in range(79):
            a=j*math.pi/39
            pts.append(P.p(2.94*math.cos(a),.55+ring,2.55*math.sin(a)))
        ln(d,pts,TEAL,2,80)

def stream(d,P,fr,to,col,k,height=1.75):
    if k<=0:return
    n=30
    pts=[]
    for j in range(n+1):
        u=j/n
        if u>k:break
        x=lerp(fr[0],to[0],u)
        z=lerp(fr[2],to[2],u)
        y=lerp(fr[1],to[1],u)+height*4*u*(1-u)
        pts.append(P.p(x,y,z))
    if len(pts)>1:ln(d,pts,col,3,155)
    u=k
    x=lerp(fr[0],to[0],u);z=lerp(fr[2],to[2],u);y=lerp(fr[1],to[1],u)+height*4*u*(1-u)
    particle(d,P,x,y,z,col,9,245)

def one_scene(d,P,S,i,t,p):
    # Intentional animation beats occur at matched *spoken words* from the
    # original final audio, never at arbitrary slide-timing intervals.
    q=lambda phrase,seconds=.8,default=.3:S.rise(i,t,phrase,seconds,default)
    if i==0: # 1. What is an invariant?
        announce(d,'What stays the same?', 'When a problem changes, look for what does not.',40)
        orbit(d,P,t,12)
        mathtext(d,'INVARIANT',307,49,TEAL,q('an invariant',.55))
        tx(d,640,386,'A quantity that stays fixed',27,MINT,True,opacity=int(245*q('stays fixed',.8)))
        tx(d,640,530,'A total     •     A difference     •     A remainder',20,MUTED,opacity=int(255*q('Sometimes',.6)))
    elif i==1: # Why this is useful
        announce(d,'Too many possible moves?', 'Find one rule that every route must obey.',40)
        start=P.p(-3.7,.12,0)
        particle(d,P,-3.7,.14,0,GOLD,16)
        for j in range(5):
            z=(j-2)*.73
            path=[P.p(-3.6+v*.13,.15+.16*math.sin(j*2+v),z*v/25) for v in range(26)]
            reveal=q('so many legal moves',2.4)
            n=max(1,int(25*reveal))
            ln(d,[start]+path[:n],LILAC,2,125)
            if reveal>.35:
                particle(d,P,.0,.10,z,LILAC,4,150)
        text_r(d,1060,390,'ONE',25,MINT,True,opacity=int(240*q('one mathematical fact')))
        text_r(d,1060,433,'INVARIANT',37,MINT,True,opacity=int(240*q('one mathematical fact')))
        mathtext(d,'Impossible?',518,39,RED,q('impossible'))
    elif i==2: # plan
        announce(d,'See it. Prove it. Use it.', 'We will follow a single mathematical thread.',40)
        steps=[('PUZZLE',GOLD),('ONE MOVE',TEAL),('EXAMPLES',LILAC),('PROOF',MINT)]
        for j,(name,col) in enumerate(steps):
            x=-3.65+j*2.45
            show=ease((p-j*.15)/.45)
            if show==0:continue
            box3(d,P,x,0,0,1.18,1.0,.90,col,int(230*show))
            xx,yy=P.p(x,1.4,0)
            tx(d,xx,yy,name,19,col,True,opacity=int(255*show))
            if j<3:
                arrow(d,P.p(x+.7,.7,0),P.p(x+1.8,.7,0),WHITE,show)
        tx(d,640,539,'Then you will try one for yourself.',22,MINT,opacity=int(255*q('try',.9)))
    elif i==3: # puzzle
        announce(d,'A counter-moving puzzle', 'Only transfers are legal: no new counters.',40)
        pilestage(d,P,5,7)
        val=q('ten counters in each pile',.9)
        tx(d,640,290,'GOAL',16,MUTED,True,opacity=int(255*val))
        tx(d,640,330,'10  +  10  =  20',33,RED,True,opacity=int(255*val))
        if val>.2:glow_line(d,(544,328),(730,328),RED,2,int(155*val))
    elif i==4: # better question
        announce(d,'Before calculating…', 'Is there something every move preserves?',39)
        pilestage(d,P,5,7)
        tx(d,640,301,'?',91,WHITE,True,opacity=int(255*q('ask a better question',1.4)))
        tx(d,640,379,'5  +  7  =  12',37,MINT,True,opacity=int(255*q('something',.8)))
    elif i==5: # move 2 blue right to left
        announce(d,'Watch a single legal move', 'Two counters travel. None are created.',39)
        k=q('Move two blue',2.2)
        plane(d,P,-2.85,0,3.2,3.2);plane(d,P,2.85,0,3.2,3.2)
        pile(d,P,5,-2.85,GOLD);pile(d,P,5,2.85,TEAL)
        start=positions(7,2.85)[5:7];end=positions(7,-2.85)[5:7]
        for j,(fr,to) in enumerate(zip(start,end)):
            u=clip((k-j*.07)/.93)
            # The moving pieces are the same two objects throughout.
            if u<=.01:box3(d,P,*fr,.4,.33,.4,TEAL,240)
            elif u>=.99:box3(d,P,*to,.4,.33,.4,TEAL,240)
            else:stream(d,P,(fr[0],.25,fr[2]),(to[0],.25,to[2]),TEAL,u,1.50+j*.16)
        tx(d,354,522,f'LEFT   {5 if q("Now there are seven",.15)<.5 else 7}',26,GOLD,True)
        tx(d,914,522,f'RIGHT   {7 if q("Now there are seven",.15)<.5 else 5}',26,TEAL,True)
        tx(d,640,337,'TOTAL  =  12',36,MINT,True,opacity=int(255*q('total is still twelve',.75)))
    elif i==6: # transfer preserves total
        announce(d,'Nothing appears. Nothing vanishes.', 'What leaves one pile arrives in the other.',37)
        pilestage(d,P,7,5,show_total=False)
        k=q('takes some counters away',1.4)
        arrow(d,P.p(1.55,1.0,.6),P.p(-1.45,1.0,.6),TEAL,k)
        tx(d,640,331,'−t       +t',42,WHITE,True,opacity=int(255*k))
        tx(d,640,391,'−t  +  t  =  0',34,MINT,True,opacity=int(255*q('Nothing is created',1.0)))
    elif i==7: # impossible vs possible
        announce(d,'An impossibility proof', 'A legal move cannot turn twelve into twenty.',41)
        if q('twenty counters',1.0)>.1:
            tx(d,374,344,'10 + 10',50,RED,True)
            tx(d,906,344,'6 + 6',50,MINT,True)
            tx(d,374,421,'20 ≠ 12',33,RED,True)
            tx(d,906,421,'12 = 12',33,MINT,True)
            glow_line(d,(250,301),(494,460),RED,6,180)
            tx(d,374,505,'IMPOSSIBLE',22,RED,True)
            tx(d,906,505,'POSSIBLE',22,MINT,True)
        else:pilestage(d,P,5,7)
    elif i==8: # invariant name
        announce(d,'An invariant', 'One quantity stays fixed through every legal move.',44)
        orbit(d,P,t,12)
        mathtext(d,'A + B = 12',341,55,MINT,q('total number',.8))
        tx(d,640,514,'CHANGE THE ARRANGEMENT. NOT THE TOTAL.',20,TEAL,True)
    elif i==9: # add new 2 both
        announce(d,'Change the rule', 'Now both piles receive two new counters.',42)
        k=q('adds two brand-new counters',1.5)
        plane(d,P,-2.85,0,3.2,3.2);plane(d,P,2.85,0,3.2,3.2)
        pile(d,P,5,-2.85,GOLD);pile(d,P,7,2.85,TEAL)
        for x,col,old in [(-2.85,GOLD,5),(2.85,TEAL,7)]:
            new=positions(old+2,x)[old:old+2]
            for j,(px,py,pz) in enumerate(new):
                fall=ease((k-j*.17)/.83)
                box3(d,P,px,py+2.4*(1-fall),pz,.40,.33,.40,col,int(255*fall))
        tx(d,354,520,f'{5 if k<.72 else 7}  LEFT',25,GOLD,True)
        tx(d,914,520,f'{7 if k<.72 else 9}  RIGHT',25,TEAL,True)
        tx(d,640,340,'+2     +2',39,MINT,True,opacity=int(255*k))
    elif i==10: # growth total, diff fixed
        announce(d,'What is actually preserved?', 'The total grows, but the difference does not.',41)
        k=q('total is growing',.8)
        pilestage(d,P,7,9,show_total=False)
        tx(d,355,321,'TOTAL',19,MUTED,True)
        tx(d,355,373,'12 → 16',37,RED,True,opacity=int(255*k))
        tx(d,918,321,'DIFFERENCE',19,MUTED,True)
        tx(d,918,373,'7 − 5 = 2',37,MINT,True,opacity=int(255*q('difference between',.8)))
        tx(d,640,539,'EQUAL ADDITIONS KEEP THE GAP UNCHANGED.',18,MINT,True)
    elif i==11: # 5+7 /7+9/9+11 step transforms
        announce(d,'The gap survives every addition', 'New blocks arrive in pairs. Watch both piles grow.',39)
        v1=q('Add two to each',1.05)
        v2=q('Add two again',1.05)
        shown=0 if v1<.90 else 1 if v2<.90 else 2
        nL,nR=5+shown*2,7+shown*2
        pilestage(d,P,nL,nR,show_total=False)
        mathtext(d,f'{nL}   and   {nR}',325,39,WHITE)
        tx(d,640,400,f'GAP = {nR-nL}',38,MINT,True)
        for j in range(2):
            # Raised 3D rails make the preserved separation visible.
            z=-1.8+j*.23
            ln(d,[P.p(-1.75,.30,z),P.p(1.75,.30,z)],MINT,2,100)
    elif i==12: # algebra A,B, both +2
        announce(d,'A proof for any starting values', 'Call the pile sizes A and B.',39)
        plane(d,P,-2.85,0,3.2,3.2);plane(d,P,2.85,0,3.2,3.2)
        for x,col,num in [(-2.85,GOLD,6),(2.85,TEAL,9)]:
            pile(d,P,num,x,col)
            k=q('plus two',1.05)
            for px,py,pz in positions(num+2,x)[num:num+2]:
                box3(d,P,px,py+2*(1-k),pz,.42,.32,.42,MINT,int(220*k))
        mathtext(d,'A    and    B',298,37,WHITE,q('A and B'))
        tx(d,640,377,'A + 2     and     B + 2',34,MINT,True,opacity=int(255*q('A plus two',.9)))
        tx(d,640,536,'Same addition to both amounts',18,MUTED)
    elif i==13: # cancellations visual
        announce(d,'Watch the +2 terms cancel', 'Two equal changes disappear when we subtract.',40)
        k=q('cancel perfectly',1.25)
        mathtext(d,'(A + 2) − (B + 2)',318,49,WHITE)
        l=lerp(445,608,k);r=lerp(836,671,k)
        for x,col in [(l,GOLD),(r,TEAL)]:
            # 3D glowing terms physically converge, then fade.
            xx=(x-640)/90
            box3(d,P,xx,1.60,.8,.50,.43,.50,col,int(250*(1-k)))
        if k>.65:
            circ(d,640,402,26,MINT,int(215*k))
            tx(d,640,471,'A − B',55,MINT,True,opacity=int(255*ease((k-.65)/.35)))
        else:tx(d,640,476,'+2             −2',35,GOLD,True)
    elif i==14: # transfer proof
        announce(d,'Transfers conserve the total', 'What leaves here is added there.',42)
        plane(d,P,-2.85,0,3.2,3.2);plane(d,P,2.85,0,3.2,3.2)
        pile(d,P,6,-2.85,GOLD);pile(d,P,6,2.85,TEAL)
        k=q('loses t',1.25)
        stream(d,P,(-1.6,.3,0),(1.5,.3,0),GOLD,k,1.9)
        tx(d,640,325,'(A − t) + (B + t)',43,WHITE,True,opacity=int(255*k))
        tx(d,640,389,'−t + t = 0',37,GOLD,True,opacity=int(255*q('changes cancel',.65)))
        tx(d,640,462,'TOTAL = A + B',37,MINT,True,opacity=int(255*q('changes cancel',.65)))
    elif i==15: # trap
        announce(d,'Two rules. Two different invariants.', 'Always inspect the actual legal move.',37)
        split=640
        ln(d,[(split,268),(split,533)],(83,118,144),2,130)
        # left: moving physical block from group to other
        for z in [-.65,-.20,.25]:
            box3(d,P,-4.0,.2,z,.43,.45,.45,GOLD)
            box3(d,P,-2.75,.2,z,.43,.45,.45,TEAL)
        for z in [-.65,-.20,.25]:
            box3(d,P,2.5,.2,z,.43,.45,.45,GOLD)
            box3(d,P,3.8,.2,z,.43,.45,.45,TEAL)
        k=q('preserves the total',.8)
        arrow(d,(344,326),(490,326),GOLD,k)
        arrow(d,(870,310),(870,365),TEAL,q('Adding the same number',.8))
        tx(d,359,454,'TRANSFER',25,GOLD,True)
        tx(d,920,454,'ADD TO BOTH',25,TEAL,True)
        tx(d,359,504,'TOTAL fixed',25,MINT,True,opacity=int(255*k))
        tx(d,920,504,'GAP fixed',25,MINT,True,opacity=int(255*q('difference',.6)))
    elif i==16: # challenge 4 and 9 -> 18 23
        announce(d,'Try one yourself', 'Both piles gain two with every move.',42)
        pilestage(d,P,4,9,show_total=False)
        k=q('eighteen and twenty-three',.8)
        tx(d,640,303,'TARGET',20,MUTED,True,opacity=int(255*k))
        tx(d,640,352,'18   and   23',39,WHITE,True,opacity=int(255*k))
        tx(d,640,427,'STARTING GAP  =  5',29,MINT,True)
    elif i==17: # seven moves yes
        announce(d,'Seven moves make the target', 'Both piles gain fourteen counters.',40)
        k=q('Exactly seven moves',2.5)
        step=int(clip(k)*7)
        pilestage(d,P,4+2*step,9+2*step,show_total=False)
        tx(d,640,291,'7 × 2 = 14',46,GOLD,True,opacity=int(255*k))
        tx(d,640,364,'4 + 14 = 18',34,WHITE,True,opacity=int(255*q('Both target',.6)))
        tx(d,640,414,'9 + 14 = 23',34,MINT,True,opacity=int(255*q('Both target',.6)))
    elif i==18: # contrast no
        announce(d,'This target breaks the rule', 'The gap would have to change from five to four.',39)
        pilestage(d,P,18,22,show_total=False)
        tx(d,353,331,'START',20,MUTED,True)
        tx(d,353,385,'9 − 4 = 5',38,MINT,True)
        tx(d,912,331,'TARGET',20,MUTED,True)
        tx(d,912,385,'22 − 18 = 4',35,RED,True)
        tx(d,640,482,'IMPOSSIBLE',33,RED,True,opacity=int(255*q('No',.8)))
        if q('rules that out',.8)>.25:
            ln(d,[(760,401),(1080,401)],RED,4,220)
    elif i==19: # summary
        announce(d,'One move can tell the whole story', 'Instead of testing every possible path.',38)
        orbit(d,P,t,12)
        seq=[('EXAMINE A MOVE','Examine one move'),('FIND WHAT CANCELS','identify what cancels'),('APPLY THE RULE','reason about every move')]
        for j,(s,phrase) in enumerate(seq):
            k=q(phrase,.7)
            tx(d,640,341+j*62,s,25,[GOLD,TEAL,MINT][j],True,opacity=int(255*k))
        tx(d,640,549,'A PROOF — NOT JUST A PATTERN',18,MUTED,True)
    elif i==20: # notebook
        announce(d,'Now make the idea yours', 'Explain the invariant, not just the answer.',40)
        # 3D writing surface tilted in space, with a line being drawn as spoken.
        box3(d,P,0,-.1,0,6.4,.09,3.4,(135,165,191),180)
        poly(d,P,[(-2.8,.015,-1.35),(2.8,.015,-1.35),(2.8,.015,1.35),(-2.8,.015,1.35)],(33,58,77),245,(103,165,184))
        for k in range(4):
            linepts=[P.p(-2.45,.035,-.95+k*.62),P.p(2.45,.035,-.95+k*.62)]
            ln(d,linepts,(103,155,171),2,95)
        k=q('write a single equation',1.1)
        px,py=P.p(lerp(-2.25,1.9,k),.09,.18)
        glow(d,px,py,6,TEAL)
        tx(d,640,362,'What never changed?',30,MINT,True,opacity=int(255*q('Draw one move',.9)))
        tx(d,640,516,'SHOW IT WITH ONE EQUATION',21,WHITE,True,opacity=int(255*k))


def frame(S,t):
    i,p=S.at(t)
    im=bg().copy();d=ImageDraw.Draw(im,'RGBA')
    P=P3(t,i)
    grid(d,P,t)
    tags=['THE IDEA','THE VALUE','THE JOURNEY','THE PUZZLE','THE INSIGHT','ONE LEGAL MOVE',
          'WHY IT WORKS','A PROOF','THE DEFINITION','CHANGE THE RULE','FIND THE GAP',
          'TEST THE PATTERN','GENERALISE','CANCEL THE CHANGE','PROVE A TRANSFER','COMPARE',
          'YOU TRY','CHECK THE TARGET','RULE IT OUT','RECALL THE METHOD','IN YOUR NOTEBOOK']
    one_scene(d,P,S,i,t,p)
    chapter(d,i,tags[i],t/S.total)
    # Scene changes use a subtle dark breathing transition; the audio is never retimed.
    opening=ease(p*19)
    if opening<1:
        veil=Image.new('RGBA',(W,592),(BG[0],BG[1],BG[2],int(215*(1-opening))))
        im.alpha_composite(veil,(0,0))
    return im.convert('RGB')

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--timing',required=True)
    ap.add_argument('--words',default=None)
    ap.add_argument('--out',default='build/t021/new_visual.mp4')
    ap.add_argument('--fps',type=int,default=24)
    ap.add_argument('--preview',action='store_true')
    ap.add_argument('--limit',type=int,default=0)
    a=ap.parse_args()
    S=Story(json.load(open(a.timing)),json.load(open(a.words)) if a.words and os.path.exists(a.words) else {})
    if len(S.seg)!=21:raise ValueError(f'Expected 21 locked narration segments; found {len(S.seg)}')
    if a.preview:
        out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
        for i,(start,end) in enumerate(S.spans):
            tt=lerp(start,end,.64)
            frame(S,tt).save(out/f'{i+1:02d}.png',optimize=True)
        print('Created 21 perspective-rendered scene thumbnails at',out)
        return
    Path(a.out).parent.mkdir(parents=True,exist_ok=True)
    frames=math.ceil(S.total*a.fps)+a.fps//2
    cmd=['ffmpeg','-y','-hide_banner','-loglevel','error','-f','rawvideo','-pixel_format','rgb24',
         '-video_size',f'{W}x{H}','-framerate',str(a.fps),'-i','-', '-an','-c:v','libx264',
         '-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',a.out]
    ff=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    for n in range(frames if not a.limit else min(frames,a.limit)):
        t=n/a.fps
        try:ff.stdin.write(frame(S,t).tobytes())
        except BrokenPipeError:raise RuntimeError('FFmpeg video encoder stopped unexpectedly')
        if n%720==0:print(f'3D render {n}/{frames} frames, {t:.1f}/{S.total:.1f}s',flush=True)
    ff.stdin.close()
    if ff.wait()!=0:raise RuntimeError(f'ffmpeg returned {ff.returncode}')
    print('Rendered',a.out,'duration',S.total,'frames',frames)

if __name__=='__main__':main()