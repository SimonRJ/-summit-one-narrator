"""Replace one faulty explanation in each of two pinned, previously reviewed films."""
import argparse
import copy
from hashlib import sha256
import json
import math
from pathlib import Path
import subprocess
import sys
from urllib.request import urlopen
from zipfile import ZipFile

import numpy as np
from PIL import Image
import soundfile as sf
from render_recorded import Board, background, caption
from stage import Moment
from prepare_audio import align, caption_cues, load_recording, stamp, transcribe
from synth import MODEL_REVISION, RATE, ROOT, VOICE_SHA

BASE = 'https://github.com/SimonRJ/-summit-one-narrator/releases/download/lesson-introductions/'
EDITIONS = {
    'S019': (5, 'c08c020ccb192987a2339e27a328248cb43b8b00753ba3fdf6d6c83cbdedc086',
             BASE + 'S019-distinct-audio-timeline-20261116-v3.zip', 'd2210cc4cabf6e52e87b5ac53b8fc881460b0444206983db12a75cb98ffed3ec'),
    'S020': (9, '393ec2fbd79e93259b2cdf512eeeea947644745b4078069f977b301360be62bc',
             'https://raw.githubusercontent.com/SimonRJ/-summit-one-narrator/7760eeaa80cb4ff198fe0e806afce12cb0fedeea/production/lesson-intros/illustrated/S020.json',
             '579c9c7bc043e7b448141d94e2a8cd462bad82d31d686b42b367ba231fc920b5'),
}
FPS = 30


def fetch(url, out, digest):
    if not out.exists():
        with urlopen(url, timeout=90) as source:
            out.write_bytes(source.read())
    assert sha256(out.read_bytes()).hexdigest() == digest, out


def capture(args):
    return subprocess.check_output(['ffmpeg','-nostdin','-v','error','-xerror','-threads','2',*map(str,args)])


def waveform(path):
    return np.frombuffer(capture(['-i',path,'-vn','-ac','1','-ar',RATE,'-f','f32le','pipe:1']), '<f4')


def draw(lesson, scene, cues, second, scale):
    board = Board(background(*(('#332837','#231d34') if lesson=='S019' else ('#142c3c','#102030')),scale),scale)
    c = Moment(scene, second)
    white, blue, gold = '#f6f1e9', '#85b5e6', '#edc175'
    if lesson=='S019':
        board.label('Cross out the leftmost pair',76,86,46,white,bold=True)
        board.line([(76,127),(1200,127)],'#938794',2)
        crossed = c.reveal('cross out the two squares',.85)
        for row in range(4):
            for col in range(4):
                x,y=169+86*col,188+86*row
                board.box(x,y,82,82,radius=0,fill=blue if (row+col)%2==0 else gold)
                if row==0 and col<2:
                    board.box(x,y,82,82,radius=0,fill='#332837',opacity=crossed)
                    board.line([(x+10,y+11),(x+72,y+71)],'#ffb4c3',4,crossed)
                    board.line([(x+10,y+71),(x+72,y+11)],'#ffb4c3',4,crossed)
        board.label('Top row, columns 1 and 2',625,245,36,white,crossed,bold=True)
        board.label('Can dominoes cover the rest?',625,382,34,gold,c.reveal('Can dominoes cover'),bold=True)
        board.label('Each domino uses one shared edge.',625,473,27,white,c.reveal('sharing an edge'))
    else:
        board.label('Exponent 49, position one',76,86,46,white,bold=True)
        board.line([(76,127),(1200,127)],'#7496a8',2)
        board.label('12 full blocks use exponents 1 to 48',88,193,37,white,c.reveal('twelve full blocks'),bold=True)
        start=c.reveal('next exponent is forty-nine')
        board.label('Exponent',90,313,33,white,start,bold=True)
        board.label('Cycle position',90,390,33,white,c.reveal('position one'),bold=True)
        board.label('Last digit',90,467,33,white,c.reveal('digits to add'),bold=True)
        for i,(exp,pos,last,when) in enumerate([(49,1,3,'next exponent is forty-nine'),(50,2,9,'digits to add'),(51,3,7,'digits to add')]):
            x=565+i*205
            board.text(str(exp),x,313,42,blue,opacity=c.reveal(when),bold=True)
            board.text(str(pos),x,390,40,gold,opacity=min(c.reveal('position one'),c.reveal(when)),bold=True)
            board.text(str(last),x,467,40,white,opacity=c.reveal('digits to add'),bold=True)
        board.label('3 + 9 + 7 = 19',505,550,40,gold,c.reveal('sum is nineteen'),bold=True)
    for cue in cues:
        if cue['start'] <= second < cue['end']:
            # Both conditions retain their cue times with one stable glyph layer.
            # S020 uses Stage directly; S019 uses the shared stable caption helper.
            if lesson == 'S020':
                board.caption(cue, second)
            else:
                caption(board,cue,scene['words'],second)
            break
    return board.image


def shift_scene(scene, delta):
    scene=copy.deepcopy(scene)
    for key in ('start','end','speech_end'):
        scene[key]+=delta
    for word in scene['words']:
        word['start']+=delta
        word['end']+=delta
    return scene


def write(path, data):
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')


def make(lesson, out):
    from faster_whisper import WhisperModel
    out.mkdir(exist_ok=True,parents=True)
    working=out.parent/('repair-'+lesson)
    working.mkdir(exist_ok=True,parents=True)
    nth, sha, time_url, time_sha=EDITIONS[lesson]
    original=working/'original.mp4'
    time_file=working/('timing.zip' if lesson=='S019' else 'timing.json')
    fetch(BASE+lesson+'-Intro-Illustrated.mp4',original,sha)
    fetch(time_url,time_file,time_sha)
    if lesson=='S019':
        with ZipFile(time_file) as z:
            before=json.loads(z.read('timeline.json'))
    else:
        before=json.loads(time_file.read_text())
    source_audio=waveform(original)
    script=json.loads((ROOT/'production/scripts'/f'{lesson}.json').read_text())
    scenes=before['scenes']
    for s,part in zip(scenes,script['scenes']):
        if s['n']!=nth:
            assert ' '.join(w['text'] for w in s['words'])==part['narration']
    src=scenes[nth-1]
    # Both splice points lie on exact frame boundaries. Preserve the original timing
    # everywhere else and pad only the newly recorded scene to a complete final frame.
    first=round(src['start']*FPS); stop=round(src['end']*FPS)
    begin,end=first/FPS,stop/FPS
    a,b=round(begin*RATE),round(end*RATE)
    line=script['scenes'][nth-1]['narration']
    fresh=load_recording(lesson,nth,line)
    model=WhisperModel('base.en',device='cpu',compute_type='int8',cpu_threads=2)
    heard=transcribe(model,fresh)
    words,match=align(line,heard,begin+0.22,begin+0.22+len(fresh)/RATE)
    assert match>=88, (lesson,match,[w.word for w in heard])
    # Match the established release's integrated level while keeping Voice C at natural speed.
    normalized=working/'normalized.wav'
    subprocess.run(['ffmpeg','-nostdin','-v','error','-y','-i',ROOT/'build/t01-studio'/f'{lesson}-{nth:02}.wav','-af','loudnorm=I=-18:TP=-2:LRA=9','-ar',str(RATE),normalized],check=True)
    fresh=waveform(normalized)
    nframes=math.ceil((.22+len(fresh)/RATE+.80)*FPS)
    sample_count=nframes*(RATE//FPS)
    insert=np.zeros(sample_count,dtype=np.float32)
    lead=round(.22*RATE)
    insert[lead:lead+len(fresh)]=fresh
    delta=nframes/FPS-(end-begin)
    audio=np.concatenate((source_audio[:a],insert,source_audio[b:]))
    master=working/'narration.flac'
    sf.write(master,audio,RATE,subtype='PCM_24')
    replacement=dict(n=nth,start=begin,end=begin+nframes/FPS,speech_end=begin+.22+len(fresh)/RATE,words=words,match_percent=match,recognized_speech=' '.join(w.word.strip() for w in heard))
    new_scenes=[s if s['n']<nth else replacement if s['n']==nth else shift_scene(s,delta) for s in scenes]
    new_scenes[nth-2]['end']=begin
    new_scenes[nth]['start']=replacement['end']
    rep_cues=caption_cues(words)
    new_cues=[c for c in before['captions'] if c['end']<=begin+.03]+rep_cues+[
        dict(c,start=c['start']+delta,end=c['end']+delta) for c in before['captions'] if c['start']>=end-.03]
    assert ' '.join(s['narration'] for s in script['scenes'])==' '.join(c['text'] for c in new_cues)
    assert all(a['end']<=b['start']+.001 for a,b in zip(new_cues,new_cues[1:]))
    assert sum(3**e for e in range(1,52))%10==9 and [pow(3,e,10) for e in (49,50,51)]==[3,9,7]
    assert sum(1 for r in range(4) for k in range(4) if (r,k) not in ((0,0),(0,1)))==14
    # Draw only the correction. The rest comes from the pinned public film.
    new_scene=working/'insert.mp4'
    enc=['ffmpeg','-nostdin','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','30','-i','pipe:0','-c:v','libx264','-crf','18','-preset','veryfast','-threads','2','-pix_fmt','yuv420p',new_scene]
    with subprocess.Popen(enc,stdin=subprocess.PIPE) as p:
        for n in range(nframes):
            p.stdin.write(draw(lesson,replacement,rep_cues,begin+n/FPS,1.5).tobytes())
        p.stdin.close()
        if p.wait():raise ValueError('New scene failed to encode')
    cutfilter=f'[0:v]split=2[left][right];[left]trim=end_frame={first},setpts=PTS-STARTPTS[v0];[right]trim=start_frame={stop},setpts=PTS-STARTPTS[v2];[v0][1:v][v2]concat=n=3:v=1:a=0[out]'
    movie=out/f'{lesson}.mp4'
    subprocess.run(['ffmpeg','-nostdin','-v','error','-y','-threads','2','-i',original,'-i',new_scene,'-i',master,'-filter_complex_threads','2','-filter_complex',cutfilter,'-map','[out]','-map','2:a','-c:v','libx264','-crf','17','-preset','veryfast','-threads','2','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',movie],check=True)
    duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',movie],text=True))
    assert abs(duration-len(audio)/RATE)<.15
    digest=sha256(movie.read_bytes()).hexdigest()
    bridge=next(l['bridge'] for l in json.loads((ROOT/'data/read-watch-practise.json').read_text())['lessons'] if l['slot']==int(lesson[1:]))
    guide=dict(title=script['title'],seconds=duration,chapters=[dict(title=p['heading'],start=round(s['start'],3)) for p,s in zip(script['scenes'],new_scenes)],transcript=[p['narration'] for p in script['scenes']],bridge=bridge,sha256=digest)
    text='WEBVTT\n\n'+'\n\n'.join(f"{stamp(c['start'])} --> {stamp(c['end'])}\n{c['text']}" for c in new_cues)+'\n'
    (out/f'{lesson}.vtt').write_text(text)
    write(out/f'{lesson}-guide.json',guide)
    draw(lesson,replacement,[],replacement['speech_end'],1.5).save(out/f'{lesson}-poster.jpg',quality=92)
    timeline=dict(id=lesson,duration=duration,narration_reference=VOICE_SHA,model_revision=MODEL_REVISION,scenes=new_scenes,captions=new_cues)
    with ZipFile(out/f'{lesson}-recording.zip','w') as z:
        z.writestr('script.json',json.dumps(script,ensure_ascii=False))
        z.writestr('timeline.json',json.dumps(timeline,ensure_ascii=False))
        z.writestr('captions.vtt',text)
        z.write(master,'narration.flac')
    encoded=waveform(movie); rates=[]
    for scene in new_scenes:
        x=round(scene['start']*RATE);y=min(round(scene['end']*RATE),len(audio),len(encoded))
        # The codec may alter ultrasonic content; the student-facing signal must track the source.
        rate=float(np.corrcoef(audio[x:y:6],encoded[x:y:6])[0,1]); assert rate>=.985,(scene['n'],rate)
        rates.append(round(rate,6))
    # Independently compare the completed movie to the intended original or redrawn
    # source, including every chapter and the captions area, once per second.
    def frames(path):
        return np.frombuffer(capture(['-i',path,'-an','-vf',"select='not(mod(n,30))',scale=320:180:flags=area,format=rgb24",'-fps_mode','vfr','-f','rawvideo','pipe:1']),np.uint8).reshape(-1,180,320,3)
    actual=frames(movie); errs=[]
    # Retain only the referenced source frames. Source and target frame numbers
    # differ by an integer after the splice, so the two periodic selections are exact.
    delta_frames=nframes-(stop-first)
    selected=[k for k in range(round(len(source_audio)/RATE*FPS)+2)
              if (k<first and k%FPS==0) or (k>=stop and (k+delta_frames)%FPS==0)]
    select=f"select='lt(n,{first})*not(mod(n,{FPS}))+gte(n,{stop})*not(mod(n+({delta_frames}),{FPS}))',scale=320:180:flags=area,format=rgb24"
    snapshot=np.frombuffer(capture(['-i',original,'-an','-vf',select,'-fps_mode','vfr','-f','rawvideo','pipe:1']),np.uint8).reshape(-1,180,320,3)
    assert abs(len(selected)-len(snapshot))<=1
    raw=dict(zip(selected,snapshot))
    for sec,frame in enumerate(actual):
        if begin<=sec<begin+nframes/FPS:
            target=np.asarray(draw(lesson,replacement,rep_cues,sec,1.5).resize((320,180),Image.Resampling.BOX))
        else:
            index=sec*FPS if sec<begin else round((sec-delta)*FPS)
            target=raw[index]
        vals=abs(frame.astype('int16')-target.astype('int16'))
        errs.append([float(vals[:153].mean()),float(vals[153:].mean())])
    worst=np.max(errs,axis=0).tolist();assert max(worst)<5,(lesson,worst)
    write(out/f'{lesson}-qa.json',dict(sha256=digest,source_sha256=sha,scene_replaced=nth,corrected_scene_recognition=replacement['recognized_speech'],corrected_match_percent=match,scene_audio_correlations=rates,full_duration_seconds=duration,picture_comparison_period_seconds=1,decoded_reference_comparisons=len(actual),largest_mean_picture_difference=worst,caption_count=len(new_cues)))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('lesson',choices=EDITIONS);parser.add_argument('out',type=Path)
    args=parser.parse_args();make(args.lesson,args.out)
