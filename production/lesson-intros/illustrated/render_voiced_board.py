"""Draw each animation cue from the measured words. Blend caption weight without changing the word's position."""
import argparse,json,hashlib,subprocess
from pathlib import Path
from math import ceil
from bisect import bisect_right
from importlib import import_module
from functools import lru_cache
from PIL import Image,ImageDraw
from captioned_film import Canvas,ease,font
from visuals import Cues
ROOT=Path(__file__).resolve().parents[3]
MODULES={'S024':'bead_scale_trays','S036':'forced_dominoes','S083':'mirror_mosaics','S041':'shop_comparison'}
PAPER='#172336';INK='#f6f1e6'
def groups(timeline):
    words=[word for scene in timeline['scenes'] for word in scene['words']]
    result=[];i=0
    for caption in timeline['captions']:
        tokens=caption['text'].split();w=words[i:i+len(tokens)]
        assert [item['text'] for item in w]==tokens
        result.append((caption,w));i+=len(tokens)
    assert i==len(words)
    return result
@lru_cache(maxsize=24)
def typeset(text,scale):
    tokens=text.split();width=round(1280*scale);height=round(100*scale);size=round(34*scale)
    while True:
        face=font(size,False);heavy=font(size,True);space=max(4,round(heavy.getlength(' ')))
        lengths=[ceil(heavy.getlength(t))+1 for t in tokens]
        if sum(lengths)+space*(len(tokens)-1)<width-55*scale:break
        size-=1
        if size<round(23*scale):raise ValueError('Caption is too long: '+text)
    blank=Image.new('RGB',(width,height),PAPER);items=[]
    x=(width-(sum(lengths)+space*(len(tokens)-1)))//2
    for token,w in zip(tokens,lengths):
        normal=Image.new('RGB',(w,height),PAPER)
        bold=normal.copy()
        for im,weight in [(normal,face),(bold,heavy)]:
            ImageDraw.Draw(im).text((w/2,height*.47),token,font=weight,fill=INK,anchor='mm')
        blank.paste(normal,(x,0));items.append((x,normal,bold));x+=w+space
    return blank,items
def spoken_caption(group,time,scale):
    c,words=group;base,boxes=typeset(c['text'],scale);out=base.copy()
    for w,(x,normal,bold) in zip(words,boxes):
        if w['start']-.08<time<w['end']+.08:
            emphasis=min(ease((time-w['start']+.08)/.14),ease((w['end']+.08-time)/.14))
            out.paste(Image.blend(normal,bold,emphasis),(x,0))
    fade=min(ease((time-c['start'])/.10),ease((c['end']-time)/.10))
    return out if fade>=1 else Image.blend(Image.new('RGB',out.size,PAPER),out,fade)
class Movie:
    def __init__(self,id,timeline,scale):
        self.lesson=import_module(MODULES[id]);self.lesson.verify();self.scale=scale
        script=json.loads((ROOT/'production/scripts'/(id+'.json')).read_text())
        self.scenes=timeline['scenes'];self.starts=[s['start'] for s in self.scenes]
        assert len(script['scenes'])==len(self.scenes)==11
        for authored,aligned in zip(script['scenes'],self.scenes):
            assert authored['n']==aligned['n'] and authored['narration'].split()==[w['text'] for w in aligned['words']]
        self.caps=groups(timeline);self.capstarts=[c['start'] for c,w in self.caps]
    def frame(self,t,captions=True):
        i=bisect_right(self.starts,t)-1
        c=Canvas(self.scale,self.lesson.PAPER)
        self.lesson.SCENES[i](c,Cues(self.scenes[i],t))
        im=Image.new('RGB',(round(1280*self.scale),round(720*self.scale)),PAPER);im.paste(c.image,(0,0))
        k=bisect_right(self.capstarts,t)-1
        if captions and k>=0 and t<self.caps[k][0]['end']:im.paste(spoken_caption(self.caps[k],t,self.scale),(0,round(620*self.scale)))
        return im
def render(id,audio,out):
    out.mkdir(parents=True,exist_ok=True);m=json.loads((audio/'timeline.json').read_text())
    assert m['id']==id and m['narration_reference']=='0f3304a393ee504e9fa22537267ac03f150569a5fab0859616f261d009513362'
    assert m['mean_match_percent']>=90 and min(s['match_percent'] for s in m['scenes'])>=80
    film=Movie(id,m,1.5);duration=m['duration']
    dest=out/(id+'-Intro-Illustrated.mp4')
    args=['ffmpeg','-nostdin','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','30','-i','pipe:0','-i',str(audio/'narration.wav'),'-map','0:v','-map','1:a','-c:v','libx264','-pix_fmt','yuv420p','-threads','3','-crf','19','-preset','fast','-profile:v','high','-level:v','4.1','-c:a','aac','-b:a','160k','-movflags','+faststart',str(dest)]
    with subprocess.Popen(args,stdin=subprocess.PIPE) as encoder:
        try:
            for frame in range(ceil(duration*30)):encoder.stdin.write(film.frame(frame/30).tobytes())
        finally:encoder.stdin.close()
        if encoder.wait():raise ValueError('render failed')
    stats=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(dest)]))
    video,voice=stats['streams'];sec=float(stats['format']['duration'])
    assert (video['codec_name'],video['width'],video['height'],voice['codec_name'])==('h264',1920,1080,'aac') and abs(sec-duration)<.06
    subprocess.run(['ffmpeg','-nostdin','-v','error','-xerror','-i',str(dest),'-f','null','-'],check=True)
    film.frame(m['scenes'][8]['speech_end']-.1,False).save(out/(id+'-Intro-Illustrated-poster.jpg'),quality=94)
    report={'id':id,'seconds':sec,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'audio_original_wav_sha256':hashlib.sha256((audio/'narration.wav').read_bytes()).hexdigest(),'mean_speech_match':m['mean_match_percent'],'scene_matches':[s['match_percent'] for s in m['scenes']]}
    (out/(id+'-qa.json')).write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('id',choices=MODULES);p.add_argument('--audio',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();render(a.id,a.audio,a.out)
