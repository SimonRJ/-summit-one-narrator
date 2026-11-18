"""Replace the two algebra diagrams in the reviewed T02.3 print, keeping its recorded audio and captions."""
import argparse
from hashlib import sha256
import json
from math import ceil
from pathlib import Path
import subprocess
from stage import Stage,between
from order_bars import double_sum,compare_orders

ORIGINAL='e333eb08cb10786a6f1debe9013a400b92d411bbdf8d15ce928dd2ec1699a725'
# Measured cue groups in the published T02.3 caption track, in seconds.
A={'adding five makes a bar':49.07,'doubling makes two copies':53.23,
   'collect its parts':55.95,'two x plus ten':59.62}
B={'that gives two copies':63.81,'add five once':65.87,'pair those matching pieces':72.37,'the extra five':74.19}
class Cues:
    def __init__(self,t):
        self.t=t
        self.start,self.times=(45.69,A) if t<61.53 else (61.53,B)
    def at(self,phrase):return self.times[phrase]
    def reveal(self,phrase,duration=.55):return between(self.t,self.at(phrase),duration)

def draw(t,scale=1.5):
    stage=Stage(scale)
    (double_sum if t<61.53 else compare_orders)(stage,Cues(t))
    return stage.image

def audio_hash(path):
    return subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0','-c:a','copy','-f','hash','-hash','sha256','-'],text=True).strip()

def render(source,out):
    assert sha256(source.read_bytes()).hexdigest()==ORIGINAL
    out.mkdir(parents=True,exist_ok=True)
    file=out/'T02.3.mp4'
    start,end=ceil(45.69*30),ceil(77.84*30)
    # The bottom 100 logical pixels, including the original caption, stay on the base track.
    graph=f'[1:v]setpts=PTS+{start}/(30*TB)[art];[0:v][art]overlay=x=0:y=0:eof_action=pass:repeatlast=0[v]'
    cmd=['ffmpeg','-nostdin','-v','error','-y','-threads','2','-i',str(source),'-f','rawvideo','-pix_fmt','rgb24','-s','1920x930','-framerate','30','-i','pipe:0','-filter_complex_threads','2','-filter_complex',graph,'-map','[v]','-map','0:a:0','-c:a','copy','-c:v','libx264','-threads','3','-crf','17','-preset','fast','-profile:v','high','-level:v','4.1','-pix_fmt','yuv420p','-movflags','+faststart',str(file)]
    with subprocess.Popen(cmd,stdin=subprocess.PIPE) as enc:
        try:
            for f in range(start,end):
                enc.stdin.write(draw(f/30).crop((0,0,1920,930)).tobytes())
        finally:enc.stdin.close()
        if enc.wait():raise RuntimeError('T02.3 composite failed')
    draw(76).save(out/'T02.3-studio-poster.jpg',quality=93)
    info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(file)]))
    v=info['streams'][0];assert v['width']==1920 and v['height']==1080 and v['avg_frame_rate']=='30/1' and int(v['nb_frames'])==4122
    assert audio_hash(file)==audio_hash(source)
    subprocess.run(['ffmpeg','-nostdin','-v','error','-xerror','-i',str(file),'-f','null','-'],check=True)
    for x in (-7,0,2.5,3,8,19):
        assert 2*(x+5)-(2*x+5)==5
        assert (-2*x+5)-(-2*(x+5))==15
        assert (3*x-4)-3*(x-4)==8
    print(sha256(file.read_bytes()).hexdigest(),flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('out',type=Path);args=p.parse_args();render(args.source,args.out)
