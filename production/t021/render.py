#!/usr/bin/env python3
"""Original animated mathematical explainer for Summit One T02.1.
Renders clean 1280x720 H.264 video with no baked subtitles; subtitle pass is separate.
Only Pillow, NumPy and ffmpeg required. Visuals are synchronized to narration timing.json.
"""
from __future__ import annotations
import argparse, functools, json, math, os, subprocess
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W,H=1280,720
INK=(234,244,255); MUTED=(146,163,189); GOLD=(255,192,88); AQUA=(83,220,218); PINK=(249,117,145); VIOLET=(177,156,255); GREEN=(132,233,167)
BG=(7,16,31); ACCENT=(65,99,150)
FONT_REG=next((x for x in ['/usr/share/fonts/opentype/inter/Inter-Regular.otf','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'] if os.path.isfile(x)), None)
FONT_BOLD=next((x for x in ['/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'] if os.path.isfile(x)),None)
FONT_MED=next((x for x in ['/usr/share/fonts/opentype/inter/Inter-Medium.otf',FONT_REG] if x and os.path.isfile(x)),None)

@functools.lru_cache(maxsize=50)
def font(sz,weight='reg'):
    return ImageFont.truetype(FONT_BOLD if weight=='bold' else FONT_MED if weight=='med' else FONT_REG,sz)

def clamp(x,lo=0.0,hi=1.0):return max(lo,min(hi,x))
def ease(x):x=clamp(x);return x*x*(3-2*x)
def out(x):x=clamp(x);return 1-(1-x)**3

def rgba(c,a=255):return tuple(c[:3])+(int(clamp(a/255)*255),)

def text(d,x,y,s,sz=32,c=INK,weight='reg',anchor='mm',opacity=255):
    d.text((int(x),int(y)),s,font=font(sz,weight),fill=rgba(c,opacity),anchor=anchor,stroke_width=0)

def line(d,xy,c=MUTED,width=2,opacity=255,joint='curve'):
    d.line(xy,fill=rgba(c,opacity),width=width,joint=joint)

def pill(d,x,y,s,c=GOLD,w=None,alpha=245):
    w=w or max(105,len(s)*10+40)
    d.rounded_rectangle((x-w/2,y-19,x+w/2,y+20),radius=18,fill=(15,32,54,alpha),outline=rgba(c,120),width=2)
    text(d,x,y,s,17,c,'bold')

def panel(d,xy,fill=(14,31,52,230),outline=(54,82,120),r=25,width=2):
    d.rounded_rectangle(xy,radius=r,fill=fill,outline=outline,width=width)

def circle(d,x,y,r,c,op=255,stroke=False):
    if stroke:
        d.ellipse((x-r,y-r,x+r,y+r),outline=rgba(c,op),width=3)
    else:
        d.ellipse((x-r,y-r,x+r,y+r),fill=rgba(c,op))

@functools.lru_cache(maxsize=8)
def background():
    Y,X=np.mgrid[0:H,0:W]
    radial=np.exp(-(((X-660)/880)**2+((Y-250)/680)**2)*1.8)
    glow1=np.exp(-(((X-300)/480)**2+((Y-420)/390)**2)*2.5)
    glow2=np.exp(-(((X-1030)/410)**2+((Y-190)/380)**2)*2.6)
    ar=np.empty((H,W,4),np.uint8)
    ar[:,:,0]=np.clip(6+6*radial+4*glow1+1*glow2,0,255)
    ar[:,:,1]=np.clip(15+10*radial+5*glow1+6*glow2,0,255)
    ar[:,:,2]=np.clip(31+17*radial+14*glow1+14*glow2,0,255)
    ar[:,:,3]=255
    im=Image.fromarray(ar,'RGBA')
    d=ImageDraw.Draw(im,'RGBA')
    for gx in range(64,W,64):line(d,[(gx,95),(gx,586)],(62,87,132),1,20)
    for gy in range(115,585,64):line(d,[(0,gy),(W,gy)],(62,87,132),1,15)
    line(d,[(40,88),(1240,88)],(91,119,162),2,70)
    text(d,42,44,'SUMMIT  ONE',19,INK,'bold',anchor='lm')
    text(d,210,46,'// THE 135 MISSION',16,MUTED,anchor='lm')
    text(d,1238,46,'02  /  MATHEMATICAL INVARIANTS',15,AQUA,'med',anchor='rm')
    d.rectangle((0,598,W,720),fill=(5,12,25,248))
    line(d,[(0,598),(W,598)],(70,108,150),2,135)
    return im


def base(sidx,t,whole_progress):
    im=background().copy()
    d=ImageDraw.Draw(im,'RGBA')
    text(d,42,113,f'CHAPTER 02    •    INSIGHT {sidx+1:02d} / 18',13,AQUA,'bold',anchor='lm')
    d.rounded_rectangle((43,574,1237,578),radius=2,fill=(44,62,88,160))
    d.rounded_rectangle((43,574,43+int(1194*clamp(whole_progress)),578),radius=2,fill=rgba(AQUA,225))
    # decorative active waveform, subtle and never competing with the proof
    for i in range(29):
        y=542+8*math.sin(t*.55+i*.4)*math.sin(i*.3)
        circle(d,90+i*7,y,1.4,AQUA,19)
    return im,d


def heading(d,big,sub='',tag='THE QUESTION'):
    pill(d,640,146,tag,AQUA,w=max(150,len(tag)*11+44))
    text(d,640,207,big,47,INK,'bold')
    if sub:text(d,640,251,sub,21,MUTED,'med')


def centers(n,x,y=393):
    if n==0:return []
    cols=4 if n>8 else (3 if n>5 else 3)
    rows=math.ceil(n/cols)
    gap=43 if n>12 else 47
    width=(cols-1)*gap
    startx=x-width/2
    starty=y-(rows-1)*gap/2
    return [(startx+(i%cols)*gap,starty+(i//cols)*gap) for i in range(n)]


def counter(d,x,y,color,opacity=255,r=14,glow=True):
    if glow:
        circle(d,x,y,r+7,color,int(opacity*.12))
        circle(d,x,y,r+3,color,int(opacity*.26))
    circle(d,x,y,r,color,opacity)
    circle(d,x-4,y-5,2,(255,255,255),int(opacity*.65))

def pile(d,x,n,color,label,y=386,value=None,opacity=255):
    text(d,x,286,label,19,color,'bold',opacity=opacity)
    for px,py in centers(n,x,y):counter(d,px,py,color,opacity)
    text(d,x,506,str(n if value is None else value),52,color,'bold',opacity=opacity)


def small_math(d,tokens,y=303,size=50):
    f=font(size,'bold')
    widths=[d.textlength(s,font=f) for s,c in tokens]
    x=640-(sum(widths))/2
    for (s,c),wid in zip(tokens,widths):
        text(d,x,y,s,size,c,'bold',anchor='lm'); x+=wid


def underline(d,x0,x1,y,c,stage=1):line(d,[(x0,y),(x0+(x1-x0)*ease(stage),y)],c,4,230)


def arc(d,p0,p1,col,stage,raise_y=100):
    n=max(1,int(35*ease(stage)))
    for i in range(n):
        tt=i/34
        x=(1-tt)*p0[0]+tt*p1[0]
        y=(1-tt)*p0[1]+tt*p1[1]-raise_y*4*tt*(1-tt)
        circle(d,x,y,2.7,col,int(60+140*tt))

def bez(p0,p1,tt,h=95):
    return (p0[0]+(p1[0]-p0[0])*tt,p0[1]+(p1[1]-p0[1])*tt-h*4*tt*(1-tt))


def draw_scene(im,d,idx,p,elapsed):
    x1,x2=353,927
    if idx in (0,1):
        heading(d,'Can we make 10 + 10?', 'A move may TRANSFER counters; it may not create any.', 'THE PUZZLE')
        panel(d,(145,290,560,551));panel(d,(720,290,1135,551))
        pile(d,x1,5,GOLD,'LEFT PILE',y=397);pile(d,x2,7,AQUA,'RIGHT PILE',y=397)
        if idx==1:
            text(d,640,443,'5  +  7  =  12',37,INK,'bold')
            underline(d,520,760,470,AQUA,p*.85)
            pill(d,640,529,'LOOK FOR WHAT CANNOT CHANGE',VIOLET,w=380)
        else:
            text(d,640,534,'Can the total ever be 20?',22,PINK,'med')

    elif idx==2:
        heading(d,'Watch one move', 'Two counters travel from right to left.', 'ONE LEGAL MOVE')
        panel(d,(145,291,560,551));panel(d,(720,291,1135,551))
        k=ease((p-.15)/.6)
        left=centers(7,x1,398);right=centers(7,x2,398)
        for a,b in left[:5]:counter(d,a,b,GOLD)
        for a,b in right[:5]:counter(d,a,b,AQUA)
        for j in range(2):
            st=right[5+j];end=left[5+j]
            if k<.01:xy=st
            elif k>.99:xy=end
            else:xy=bez(st,end,k,110+j*36)
            arc(d,st,end,AQUA,k,110+j*36)
            counter(d,*xy,AQUA)
        text(d,x1,502,str(5+round(2*k)),52,GOLD,'bold')
        text(d,x2,502,str(7-round(2*k)),52,AQUA,'bold')
        text(d,640,440,'TOTAL = 12',30,INK,'bold')
        pill(d,640,520,'STILL TWELVE',GREEN,w=188)

    elif idx==3:
        heading(d,'Nothing appears. Nothing vanishes.', 'Moving t counters changes the piles in opposite directions.', 'WHY IT WORKS')
        panel(d,(122,287,1158,526))
        pile(d,328,7,GOLD,'A − t',y=389);pile(d,953,5,AQUA,'B + t',y=389)
        # equal-and-opposite change arrows
        line(d,[(432,399),(849,399)],MUTED,3,170)
        if p>.15:arc(d,(849,396),(433,396),GOLD,(p-.15)/.65,96)
        pill(d,641,505,'− t     + t  =  0',GREEN,w=285)

    elif idx==4:
        heading(d,'An impossibility proof', 'We only have twelve counters in total.', 'THE ANSWER')
        panel(d,(132,284,608,545));panel(d,(674,284,1148,545))
        text(d,370,331,'10 + 10 = 20',39,PINK,'bold')
        text(d,907,331,'6 + 6 = 12',39,GREEN,'bold')
        text(d,370,413,'IMPOSSIBLE',24,PINK,'bold')
        text(d,907,413,'POSSIBLE',24,GREEN,'bold')
        if p>.2:
            line(d,[(230,355),(512,468)],PINK,6,int(235*ease((p-.2)/.45)))
            line(d,[(230,468),(512,355)],PINK,6,int(235*ease((p-.2)/.45)))
            line(d,[(840,444),(884,482),(978,365)],GREEN,9,int(225*ease((p-.22)/.5)))
        text(d,640,545,'The invariant rules out a target without testing every path.',17,MUTED)

    elif idx==5:
        text(d,640,206,'INVARIANT',75,AQUA,'bold')
        underline(d,415,865,254,GOLD,(p-.16)/.62)
        panel(d,(240,295,1040,476),fill=(17,36,57,220),outline=(49,104,127))
        text(d,640,349,'Something that stays unchanged',30,INK,'med')
        text(d,640,409,'after every permitted move.',30,INK,'med')
        pill(d,640,518,'TOTAL = 12',GOLD,w=170)

    elif idx==6:
        heading(d,'Change the rule', 'Every move ADDS TWO NEW counters to BOTH piles.', 'NEW EXPERIMENT')
        panel(d,(145,291,560,550));panel(d,(720,291,1135,550))
        k=ease((p-.2)/.52)
        l=centers(7,x1,397);r=centers(9,x2,397)
        for a,b in l[:5]:counter(d,a,b,GOLD)
        for a,b in r[:7]:counter(d,a,b,AQUA)
        for a,b in l[5:]:counter(d,a,b-75*(1-k),GOLD,int(255*k))
        for a,b in r[7:]:counter(d,a,b-75*(1-k),AQUA,int(255*k))
        text(d,x1,509,f'{5+round(2*k)}',52,GOLD,'bold')
        text(d,x2,509,f'{7+round(2*k)}',52,AQUA,'bold')
        pill(d,640,502,'+ 2      + 2',GREEN,w=250)

    elif idx==7:
        heading(d,'The total grows…', '…but look what happens to the GAP.', 'FIND A DIFFERENT INVARIANT')
        panel(d,(140,281,1140,532))
        row=[('5 + 7 = 12', GOLD),('7 + 9 = 16', AQUA),('9 + 11 = 20', VIOLET)]
        for i,(s,c) in enumerate(row):
            yy=345+i*69
            text(d,270,yy,s,33,c,'bold',anchor='lm',opacity=int(255*clamp(p*5-i*.35)))
            text(d,920,yy,f'GAP = 2',29,GREEN,'bold',opacity=int(255*clamp(p*5-i*.35)))
        line(d,[(746,301),(746,503)],(53,91,126),2,145)

    elif idx==8:
        heading(d,'Watch the gap', 'Equal additions push both piles upwards together.', 'SEE THE PATTERN')
        stage=min(2,int(p*3));fraction=clamp((p-stage/3)*3)
        if stage==0:na,nb=5,7
        elif stage==1:na,nb=7,9
        else:na,nb=9,11
        panel(d,(145,290,560,552));panel(d,(720,290,1135,552))
        pile(d,x1,na,GOLD,'A',y=398);pile(d,x2,nb,AQUA,'B',y=398)
        text(d,640,425,'GAP',23,MUTED,'bold')
        text(d,640,469,'2',56,GREEN,'bold')
        if p>.15:arc(d,(530,388),(747,388),GREEN,fraction,68)

    elif idx==9:
        heading(d,'Prove it for any pile sizes', 'Call the starting sizes A and B.', 'THE ALGEBRA')
        panel(d,(155,292,1125,529))
        small_math(d,[('BEFORE:  ',MUTED),('A',GOLD),('   and   ',INK),('B',AQUA)],350,37)
        small_math(d,[('AFTER:   ',MUTED),('A + 2',GOLD),('   and   ',INK),('B + 2',AQUA)],437,39)
        underline(d,432,848,485,GREEN,(p-.2)/.58)

    elif idx==10:
        heading(d,'The changes cancel', 'Equal additions preserve the difference.', 'THE ONE-MOVE PROOF')
        panel(d,(128,281,1152,544))
        small_math(d,[('(A + ',INK),('2',GOLD),(') − (B + ',INK),('2',AQUA),(')',INK)],355,48)
        if p>.18:
            small_math(d,[('=  A − B + ',INK),('2',GOLD),(' − ',INK),('2',AQUA)],424,45)
        if p>.52:
            small_math(d,[('=  A − B',GREEN)],505,49)
            pill(d,1016,492,'SAME GAP',GREEN,w=170)

    elif idx==11:
        heading(d,'Transfer: the total cancels', 'What leaves the first pile reaches the second.', 'A DIFFERENT PROOF')
        panel(d,(126,289,1154,538))
        small_math(d,[('(A − ',INK),('t',GOLD),(') + (B + ',INK),('t',AQUA),(')',INK)],367,50)
        if p>.24:
            small_math(d,[('=  A + B  ',INK),('− t + t',PINK)],443,47)
        if p>.56:
            small_math(d,[('=  A + B',GREEN)],523,49)
            pill(d,1054,518,'SAME TOTAL',GREEN,w=150)

    elif idx==12:
        heading(d,'Same piles. Two different rules.', 'Do not confuse a preserved total with a preserved gap.', 'THE COMMON TRAP')
        panel(d,(112,290,623,550),outline=(127,90,54))
        panel(d,(656,290,1167,550),outline=(57,127,120))
        text(d,365,335,'TRANSFER',30,GOLD,'bold')
        text(d,913,335,'ADD TO BOTH',30,AQUA,'bold')
        text(d,365,416,'Total fixed',35,GREEN,'bold')
        text(d,913,416,'Difference fixed',35,GREEN,'bold')
        text(d,365,475,'Gap can change',23,MUTED,'med')
        text(d,913,475,'Total can change',23,MUTED,'med')
        underline(d,238,496,510,GOLD,p)
        underline(d,785,1042,510,AQUA,p)

    elif idx==13:
        heading(d,'A new challenge', 'Both piles gain TWO counters per move.', 'TEST YOUR INSIGHT')
        panel(d,(126,286,570,536));panel(d,(710,286,1154,536))
        text(d,346,334,'START',19,MUTED,'bold')
        text(d,933,334,'TARGET?',19,MUTED,'bold')
        text(d,347,412,'4   &   9',54,INK,'bold')
        text(d,934,412,'18   &   23',54,INK,'bold')
        pill(d,347,493,'GAP = 5',GREEN,w=175)
        pill(d,936,493,'GAP = 5',GREEN,w=175)
        arc(d,(581,404),(710,404),AQUA,p,40)

    elif idx==14:
        heading(d,'Yes—seven moves do it', 'Each pile increases by fourteen.', 'CHECK THE TARGET')
        panel(d,(155,279,1125,543))
        small_math(d,[('4 + ',INK),('7 × 2',GOLD),(' = 18',GREEN)],365,50)
        small_math(d,[('9 + ',INK),('7 × 2',AQUA),(' = 23',GREEN)],457,50)
        pill(d,640,522,'BOTH EQUATIONS WORK',GREEN,w=288)

    elif idx==15:
        heading(d,'And this one is impossible', 'The target gap would change from five to four.', 'RULE IT OUT')
        panel(d,(136,288,1144,533))
        text(d,342,367,'4   &   9',50,INK,'bold')
        text(d,932,367,'18   &   22',50,INK,'bold')
        pill(d,342,448,'GAP = 5',GREEN,w=167)
        pill(d,932,448,'GAP = 4',PINK,w=167)
        line(d,[(613,382),(680,382)],PINK,5,int(210*ease(p)))
        text(d,640,521,'NOT REACHABLE',26,PINK,'bold')

    elif idx==16:
        heading(d,'The invariant method', 'One short proof can replace a hundred attempted moves.', 'THE SUPERPOWER')
        steps=[('01','INSPECT ONE MOVE','What changes?'),('02','FIND CANCELLATION','What stays fixed?'),('03','USE THE INVARIANT','What is impossible?')]
        for j,(number,a,b) in enumerate(steps):
            x=83+j*405
            panel(d,(x,306,x+375,513),outline=(56+17*j,115+5*j,129))
            text(d,x+43,347,number,23,AQUA,'bold',anchor='lm')
            text(d,x+187,418,a,25,INK,'bold')
            text(d,x+187,466,b,20,MUTED)
            if j<2:line(d,[(x+373,408),(x+410,408)],AQUA,4,int(200*clamp(p*3-j)))

    elif idx==17:
        heading(d,'Your turn', 'Pause the lesson and draw one legal move.', 'THINK LIKE A MATHEMATICIAN')
        panel(d,(208,273,1072,540))
        for j in range(4):
            line(d,[(283,337+j*51),(1000,337+j*51)],(78,107,150),2,120)
        text(d,640,353,'What quantity survives every move?',29,AQUA,'bold')
        text(d,640,454,'Show why with a single equation.',26,INK,'med')
        pill(d,640,519,'REMEMBER • DISCOVER • TRY',GOLD,w=320)
    return im


def render_frame(idx,p,elapsed,whole_progress):
    im,d=base(idx,elapsed,whole_progress)
    return draw_scene(im,d,idx,p,elapsed)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--timing',required=True)
    ap.add_argument('--out',default='T02.1_visual.mp4')
    ap.add_argument('--fps',type=int,default=24)
    ap.add_argument('--preview',action='store_true')
    args=ap.parse_args()
    dat=json.load(open(args.timing))
    segments=dat['segments']
    # Segment durations are the actual speech durations + the pause after each segment.
    begins=[]; total=0
    for s in segments:
        begins.append(total)
        total+=float(s['duration_seconds'])+float(s.get('pause_after',0.0))
    if len(segments)!=18:raise ValueError('T02.1 must have eighteen narration segments')
    if args.preview:
        out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
        for i in range(18):
            fr=render_frame(i,.72,begins[i]+.72*segments[i]['duration_seconds'],(begins[i]+.7*segments[i]['duration_seconds'])/total)
            fr.convert('RGB').save(out/f'scene-{i+1:02d}.png')
        print(f'Wrote {len(segments)} storyboard frames to {out}')
        return
    command=['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pixel_format','rgb24','-video_size',f'{W}x{H}','-framerate',str(args.fps),'-i','-','-an','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(args.out)]
    ff=subprocess.Popen(command,stdin=subprocess.PIPE)
    count=0
    for idx,s in enumerate(segments):
        duration=float(s['duration_seconds'])+float(s.get('pause_after',0))
        frames=round(duration*args.fps)
        for fi in range(frames):
            p=(fi+.5)/max(1,frames)
            elapsed=begins[idx]+p*duration
            frame=render_frame(idx,p,elapsed,elapsed/total)
            # Fade through background instead of double-burning any captions.
            k=min(1.0,(p*duration)/.40)
            if idx>0 and k<1:
                prior=render_frame(idx-1,1.0,elapsed,elapsed/total)
                frame=Image.blend(prior,frame,ease(k))
            try:ff.stdin.write(frame.convert('RGB').tobytes())
            except BrokenPipeError:raise RuntimeError('ffmpeg closed video input')
            count+=1
        if idx%3==0:print(f'Rendered {idx+1}/{len(segments)} segments, {count/args.fps:.1f} seconds',flush=True)
    ff.stdin.close()
    if ff.wait()!=0:raise RuntimeError(f'ffmpeg failed {ff.returncode}')
    print('Written:',args.out,'frames',count,'seconds',count/args.fps)

if __name__=='__main__':main()