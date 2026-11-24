"""Rebuild the reviewed course welcome from its immutable performances and timing.

Run from the repository root after downloading the release files to the supplied
directory. The generated sound and picture are checked against the signed-off film
before that edition's identical public bytes are restored to their same-origin paths.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
from zipfile import ZipFile
import numpy as np

ROOT=Path.cwd()
SOURCE=ROOT/'production/amc-introduction'
GUIDES=ROOT/'production/standalone-review'
BUILD=ROOT/'build/amc-introduction'


def digest(path):
    with path.open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()


def checked_audio(movie):
    raw=subprocess.check_output(['ffmpeg','-v','error','-xerror','-threads','2','-i',str(movie),'-vn','-ar','8000','-ac','1','-f','f32le','pipe:1'])
    return np.frombuffer(raw,dtype='<f4')


def checked_frames(movie):
    raw=subprocess.check_output(['ffmpeg','-v','error','-xerror','-threads','2','-i',str(movie),'-an','-vf','fps=1,scale=320:180:flags=area,format=rgb24','-f','rawvideo','pipe:1'])
    return np.frombuffer(raw,dtype='uint8').reshape(-1,180,320,3)


def rebuild(downloads):
    manifest=json.loads((SOURCE/'approved-master.json').read_text())
    studio=downloads/'welcome-studio.zip'
    reviewed=downloads/'AMCIntroduction.mp4'
    previous=json.loads((downloads/'AMCIntroduction-qa.json').read_text())
    assert digest(reviewed)==previous['sha256']==manifest['movie_sha256']
    assert digest(SOURCE/'narration.json')==manifest['script_sha256'],'Record the revised passages before changing the approved master'
    BUILD.mkdir(exist_ok=True,parents=True)
    with ZipFile(studio) as archive:
        for name in [*(f'speech-{i:02d}.wav' for i in range(18)),'timing.json','words.json','heard-words.json']:
            with archive.open(name) as source, (BUILD/name).open('wb') as file:shutil.copyfileobj(source,file)
            assert digest(BUILD/name)==manifest['studio_members_sha256'][name],name
    approved=json.loads((BUILD/'timing.json').read_text())
    assert approved['reference_sha256']==manifest['reference_sha256']
    script=json.loads((SOURCE/'narration.json').read_text())['segments']
    assert [s['text'] for s in approved['segments']]==script
    subprocess.run([sys.executable,str(SOURCE/'synth.py')],check=True)
    timing=json.loads((BUILD/'timing.json').read_text())
    assert timing['segments']==approved['segments'] and timing['duration_seconds']==approved['duration_seconds']
    words=json.loads((BUILD/'words.json').read_text())
    (BUILD/'alignment-qa.json').write_text(json.dumps(words['alignment'],indent=2))
    for i,line in enumerate(script,1):
        assert ' '.join(w['text'] for w in words['words'] if w['segment']==i)==line
    subprocess.run([sys.executable,str(GUIDES/'welcome_captions.py')],check=True)
    subprocess.run([sys.executable,str(SOURCE/'render.py')],check=True)
    candidate=BUILD/'final.mp4'
    subprocess.run(['ffmpeg','-v','error','-y','-i',str(BUILD/'visual.mp4'),'-i',str(BUILD/'narration.wav'),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k','-af','apad','-shortest','-movflags','+faststart',str(candidate)],check=True)
    subprocess.run([sys.executable,str(SOURCE/'verify.py')],check=True)
    subprocess.run([sys.executable,str(GUIDES/'publish_guides.py'),'welcome'],check=True)
    candidate=ROOT/'media/AMCIntroduction.mp4';qa=json.loads((ROOT/'review/AMCIntroduction-qa.json').read_text())
    assert abs(qa['duration_seconds']-previous['duration_seconds'])<.06 and qa['chapters']==previous['chapters']
    orig=checked_audio(reviewed);new=checked_audio(candidate);assert abs(len(orig)-len(new))<800
    correlations=[]
    for scene in approved['segments']:
        start=round(scene['start_seconds']*8000);end=round((scene['start_seconds']+scene['duration_seconds'])*8000)
        correlations.append(float(np.corrcoef(orig[start:end],new[start:end])[0,1]))
    assert min(correlations)>.994,correlations
    old_frames=checked_frames(reviewed);new_frames=checked_frames(candidate);assert old_frames.shape==new_frames.shape
    means=np.abs(old_frames.astype('int16')-new_frames.astype('int16')).mean(axis=(1,2,3));assert max(means)<3.5,float(max(means))
    for label,out in [('transcript.txt','AMCIntroduction-transcript.txt'),('AMCIntroduction.vtt','AMCIntroduction.vtt')]:
        assert (BUILD/label).read_bytes()==(downloads/out).read_bytes()
        shutil.copyfile(downloads/out,ROOT/'media'/out)
    shutil.copyfile(BUILD/'poster.jpg',ROOT/'media/AMCIntroduction-poster.jpg')
    shutil.copyfile(reviewed,candidate)
    # Use the reviewed QA findings, with the source filename of this canonical build.
    previous['sources']='production/amc-introduction/sources.json'
    (ROOT/'review/AMCIntroduction-qa.json').write_text(json.dumps(previous,indent=2)+'\n')
    shutil.copyfile(BUILD/'alignment-qa.json',ROOT/'review/AMCIntroduction-alignment-qa.json')
    evidence={'release':manifest['release'],'sha256':digest(candidate),'compared_seconds':len(means),
              'maximum_frame_mean_absolute_error':float(max(means)),'minimum_scene_audio_correlation':min(correlations),'checked_scenes':18}
    (BUILD/'rebuild-qa.json').write_text(json.dumps(evidence,indent=2)+'\n')
    print(json.dumps(evidence))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('downloads',type=Path)
    rebuild(p.parse_args().downloads)
