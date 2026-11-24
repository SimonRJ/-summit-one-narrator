"""Put the seven reviewed chapter marks in each of the six introductory MP4s."""
import hashlib
import itertools
import json
import os
import subprocess
import tempfile
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class Chapters(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows=[]
        self.parts=None
        self.inside_time=False

    def handle_starttag(self,tag,attrs):
        attributes=dict(attrs)
        if tag=='button' and 'data-time' in attributes:
            self.start=round(1000*float(attributes['data-time']))
            self.parts=[]
        if tag=='span' and self.parts is not None:
            self.inside_time=True

    def handle_endtag(self,tag):
        if tag=='span':self.inside_time=False
        if tag=='button' and self.parts is not None:
            self.rows.append((self.start,''.join(self.parts).strip()))
            self.parts=None

    def handle_data(self,text):
        if self.parts is not None and not self.inside_time:self.parts.append(text)


def verify_math():
    assert sum(map(int,'2473'))==16 and divmod(1739,6)==(289,5)
    assert next(n for n in range(100,1000) if n%5==4 and n%7==6 and n%9==0)==279
    assert 398+207==605 and 57*98==5586 and (50000**2-15)-(49996*50004)==1
    assert (31-7)//4==6 and [2*(n+2) for n in (5,14,32)]==[14,32,68]
    numbers=[int(''.join(p)) for p in itertools.permutations('01246') if p[0]!='0']
    assert len([n for n in numbers if n>40000 and n%4==0])==18
    assert ''.join(map(str,range(1,66))).count('4')==17
    assert ''.join(map(str,range(9,251,9))).count('2')==10
    solid=set(itertools.product(range(4),range(4),range(3)))
    tunnel={(x,1,1) for x in range(4)}
    shaft={(1,1,z) for z in range(3)}
    assert len(solid-(tunnel|shaft))==42


def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format',
                              '-show_chapters','-of','json',str(path)]))


def packet_hashes(path):
    return subprocess.check_output(['ffmpeg','-nostdin','-v','error','-i',str(path),
                  '-map','0:v:0','-map','0:a:0','-c','copy','-f','streamhash','-hash','sha256','-'],text=True)


def digest(path):
    with path.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()


def embed(sid):
    movie=ROOT/'media'/(sid+'-Intro.mp4')
    qa=ROOT/'review'/(sid+'-Intro-qa.json')
    evidence=json.loads(qa.read_text()); assert evidence['sha256']==digest(movie)
    parser=Chapters();parser.feed((ROOT/('watch-intro-'+sid.lower()+'.html')).read_text())
    rows=parser.rows
    assert len(rows)==7 and rows[0][0]==0 and all(a[0]<b[0] for a,b in zip(rows,rows[1:]))
    original=probe(movie)
    previous=[c['tags'].get('title') for c in original['chapters']]
    if previous==[name for _,name in rows]:return
    assert not previous
    end=round(1000*float(original['format']['duration']))
    def escaped(s):return ''.join('\\'+c if c in '\\=;#' else c for c in s)
    with tempfile.TemporaryDirectory(dir=movie.parent) as folder:
        work=Path(folder);out=work/'chaptered.mp4';meta=work/'chapters'
        meta.write_text(';FFMETADATA1\n'+''.join(
            f'[CHAPTER]\nTIMEBASE=1/1000\nSTART={start}\nEND={rows[i+1][0] if i+1<len(rows) else end}\ntitle={escaped(title)}\n'
            for i,(start,title) in enumerate(rows)))
        subprocess.run(['ffmpeg','-nostdin','-v','error','-y','-i',str(movie),'-f','ffmetadata',
            '-i',str(meta),'-map','0:v:0','-map','0:a:0','-map_chapters','1','-map_metadata','0',
            '-c','copy','-movflags','+faststart',str(out)],check=True)
        embedded=probe(out)['chapters']
        assert [(round(float(c['start_time'])*1000),c['tags']['title']) for c in embedded]==rows
        before=packet_hashes(movie);assert before==packet_hashes(out)
        evidence.update(previous_container_sha256=evidence['sha256'],sha256=digest(out),
            native_chapters=len(rows),chapter_source='watch-intro-'+sid.lower()+'.html',
            encoded_stream_hashes=before.splitlines())
        os.replace(out,movie);qa.write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n')
    print(sid,len(rows),'chapters; original encoded video and voice verified')


if __name__=='__main__':
    verify_math()
    for i in range(1,7):embed(f'S{i:03}')
