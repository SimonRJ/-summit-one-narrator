"""Render the new S019 storyboard using its independently aligned Voice C audio.

This produces a candidate only. It deliberately contains no publication step.
"""
import argparse
from hashlib import sha256
import json
from math import ceil
from pathlib import Path
import subprocess

import domino_story
import render

ROOT=Path(__file__).resolve().parents[3]
VOICE_SHA='0f3304a393ee504e9fa22537267ac03f150569a5fab0859616f261d009513362'


def read_checked(audio_dir):
    script=json.loads((ROOT/'production/scripts/S019.json').read_text())
    timeline=json.loads((audio_dir/'timeline.json').read_text())
    assert timeline['id']=='S019' and timeline['narration_reference']==VOICE_SHA
    assert len(script['scenes'])==len(timeline['scenes'])==11
    assert timeline['mean_match_percent']>=90
    assert all(scene['match_percent']>=80 for scene in timeline['scenes'])
    for authored,aligned in zip(script['scenes'],timeline['scenes']):
        assert authored['n']==aligned['n']
        assert authored['narration'].split()==[word['text'] for word in aligned['words']]
    assert all(a['end']<=b['start'] for a,b in zip(timeline['captions'],timeline['captions'][1:]))
    duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration',
                                          '-of','default=noprint_wrappers=1:nokey=1',str(audio_dir/'narration.wav')],text=True))
    assert abs(duration-timeline['duration'])<.03
    return script,timeline


def main(audio_dir,out,preview=False):
    script,timeline=read_checked(audio_dir)
    # The prepared timeline contains measured speech boundaries, not estimated timestamps.
    render.load=lambda lesson:{'scenes':timeline['scenes'],'captions':timeline['captions']}
    render.MOVIES['S019']=(domino_story,'fraction')
    lesson=render.Lesson('S019',1 if preview else 1.5)
    out.mkdir(parents=True,exist_ok=True)
    lesson.preview(out)
    if preview:return
    movie=out/'S019-Intro-Illustrated.mp4'
    command=['ffmpeg','-nostdin','-v','error','-y','-f','rawvideo','-pixel_format','rgb24',
             '-video_size','1920x1080','-framerate','30','-i','pipe:0','-i',str(audio_dir/'narration.wav'),
             '-map','0:v:0','-map','1:a:0','-c:v','libx264','-crf','20','-preset','fast',
             '-threads','3','-pix_fmt','yuv420p','-profile:v','high','-level:v','4.1',
             '-c:a','aac','-b:a','192k','-movflags','+faststart','-shortest',str(movie)]
    with subprocess.Popen(command,stdin=subprocess.PIPE) as encoder:
        try:
            for frame in range(ceil(timeline['duration']*30)):
                encoder.stdin.write(lesson.frame(frame/30).tobytes())
                if frame and frame%900==0:print(f'S019: {frame//30}s rendered',flush=True)
        finally:encoder.stdin.close()
        if encoder.wait():raise RuntimeError('Video encoding failed')
    chosen=timeline['scenes'][7]
    lesson.frame(chosen['speech_end']-.1,False).save(out/'S019-Intro-Illustrated-poster.jpg',quality=95)
    info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(movie)],text=True))
    video,audio=info['streams']
    assert (video['codec_name'],video['width'],video['height'],video['pix_fmt'],video['avg_frame_rate'])==('h264',1920,1080,'yuv420p','30/1')
    assert audio['codec_name']=='aac' and abs(float(info['format']['duration'])-timeline['duration'])<.08
    subprocess.run(['ffmpeg','-nostdin','-v','error','-xerror','-i',str(movie),'-f','null','-'],check=True)
    qa={'id':'S019','candidate_sha256':sha256(movie.read_bytes()).hexdigest(),
        'source_narration_sha256':sha256((audio_dir/'narration.wav').read_bytes()).hexdigest(),
        'script_sha256':sha256((ROOT/'production/scripts/S019.json').read_bytes()).hexdigest(),
        'voice_reference_sha256':VOICE_SHA,'seconds':float(info['format']['duration']),
        'mean_alignment_percent':timeline['mean_match_percent'],
        'scene_alignment_percent':[s['match_percent'] for s in timeline['scenes']],
        'full_audiovisual_review':False,'iphone_review':False}
    (out/'S019-distinct-qa.json').write_text(json.dumps(qa,indent=2)+'\n')
    print(json.dumps(qa,indent=2),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--audio',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--preview',action='store_true')
    args=parser.parse_args()
    main(args.audio,args.out,args.preview)
