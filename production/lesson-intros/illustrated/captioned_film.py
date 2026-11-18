"""Composite original voice and burned-in captions with an individually drawn lesson."""
from bisect import bisect_right
from functools import lru_cache
import hashlib,json,subprocess
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from math import ceil

W,H=1280,620

def ease(x):
    x=max(0,min(1,x))
    return x*x*(3-2*x)

def cue(t,start,length=.8):
    return ease((t-start)/length)

def mix(a,b,p):
    return a+(b-a)*p

@lru_cache(maxsize=220)
def font(size,bold=False):
    return ImageFont.truetype('DejaVuSans'+('-Bold' if bold else '')+'.ttf',size)

@lru_cache(maxsize=6)
def paper(scale,background):
    return Image.new('RGB',(round(W*scale),round(H*scale)),background)

class Canvas:
    def __init__(self,scale,background):
        self.scale=scale
        self.image=paper(scale,background).copy()
        self.draw=ImageDraw.Draw(self.image)
    def xy(self,p):return tuple(round(v*self.scale) for v in p)
    def line(self,points,ink,w=2):
        self.draw.line([self.xy(p) for p in points],fill=ink,width=max(1,round(w*self.scale)),joint='curve')
    def poly(self,points,fill,edge,w=2):
        self.draw.polygon([self.xy(p) for p in points],fill=fill)
        if edge:self.line([*points,points[0]],edge,w)
    def text(self,s,x,y,size,ink,anchor='mm',bold=False):
        self.draw.text(self.xy((x,y)),str(s),font=font(round(size*self.scale),bold),fill=ink,anchor=anchor,stroke_width=0)
    def rect(self,x,y,w,h,fill,edge=None,stroke=2):
        self.draw.rectangle(self.xy((x,y,x+w,y+h)),fill=fill,outline=edge,width=max(1,round(stroke*self.scale)))
    def dot(self,x,y,r,fill):
        self.draw.ellipse(self.xy((x-r,y-r,x+r,y+r)),fill=fill)

def drawing(module,t,scale):
    c=Canvas(scale,module.PAPER)
    scene=bisect_right(module.START,t)-1
    module.SCENES[scene](c,t)
    return c.image

def verify_audio(src,out):
    def audio_hash(file):
        return subprocess.check_output(['ffmpeg','-v','error','-i',str(file),'-map','0:a:0','-c:a','copy','-f','hash','-hash','sha256','-'],text=True).strip()
    digest=audio_hash(src)
    assert audio_hash(out)==digest
    return digest

def render(module,src,out):
    out.mkdir(parents=True,exist_ok=True)
    assert hashlib.sha256(src.read_bytes()).hexdigest()==module.ORIGINAL
    module.verify()
    stats=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_streams','-of','json',str(src)]))['streams'][0]
    assert (stats['width'],stats['height'],stats['avg_frame_rate'])==(1920,1080,'30/1')
    count=int(stats['nb_frames'])
    movie=out/(module.ID+'-Intro-Illustrated.mp4')
    cmd=['ffmpeg','-nostdin','-v','error','-y','-threads','2','-i',str(src),'-f','rawvideo','-pix_fmt','rgb24','-s','1920x930','-framerate','30','-i','pipe:0',
         '-filter_complex_threads','2','-filter_complex','[0:v]crop=1920:150:0:930[caption];[1:v][caption]vstack=inputs=2[v]','-map','[v]','-map','0:a:0','-c:a','copy',
         '-c:v','libx264','-pix_fmt','yuv420p','-threads','3','-crf','19','-preset','fast','-profile:v','high','-level:v','4.1','-movflags','+faststart',str(movie)]
    with subprocess.Popen(cmd,stdin=subprocess.PIPE) as encoder:
        try:
            for frame in range(count):
                encoder.stdin.write(drawing(module,frame/30,1.5).tobytes())
        finally:encoder.stdin.close()
        if encoder.wait():raise RuntimeError('Film composite failed')
    final=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(movie)]))
    v,a=final['streams'];assert int(v['nb_frames'])==count and v['width']==1920 and v['height']==1080 and a['codec_name']=='aac'
    voice=verify_audio(src,movie)
    subprocess.run(['ffmpeg','-nostdin','-v','error','-xerror','-i',str(movie),'-f','null','-'],check=True)
    poster=Image.new('RGB',(1920,1080),module.PAPER);poster.paste(drawing(module,module.POSTER,1.5),(0,75));poster.save(out/(module.ID+'-Intro-Illustrated-poster.jpg'),quality=94)
    report={'id':module.ID,'sha256':hashlib.sha256(movie.read_bytes()).hexdigest(),'legacy_sha256':module.ORIGINAL,'seconds':float(final['format']['duration']),'audio_packets':voice,'original_captions':True,'frames':count}
    (out/(module.ID+'-qa.json')).write_text(json.dumps(report,indent=2)+'\n')
    return report
