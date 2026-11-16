"""Reuse only unchanged worked-example audio from the actual published S022 film."""
from hashlib import sha256
import json
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
REFERENCE='0f3304a393ee504e9fa22537267ac03f150569a5fab0859616f261d009513362'
MODEL='7936080b41163874f38610f46f438e2c0757f9fd'
UNCHANGED=range(3,10)


def extract(source):
    timeline=json.loads((HERE/'S022.json').read_text())
    script=json.loads((ROOT/'production/scripts/S022.json').read_text())
    source_hash=sha256(source.read_bytes()).hexdigest()
    if source_hash!=timeline['legacy_sha256']:
        raise ValueError('The source film is not the reviewed original')
    build=ROOT/'build/t01-studio';build.mkdir(parents=True,exist_ok=True)
    for n in UNCHANGED:
        scene=timeline['scenes'][n-1];authored=script['scenes'][n-1]['narration']
        if authored.split()!=[word['text'] for word in scene['words']]:
            raise ValueError(f'S022 scene {n}: narration was changed and cannot be reused')
        start=max(scene['start'],scene['words'][0]['start']-.12)
        end=min(scene['end'],scene['words'][-1]['end']+.16)
        if not 1<end-start<50:raise ValueError(f'S022 scene {n}: unexpected speech duration')
        wav=build/f'S022-{n:02}.wav'
        subprocess.run(['ffmpeg','-v','error','-y','-i',str(source),'-ss',str(start),'-t',str(end-start),
                        '-ac','1','-ar','48000','-c:a','pcm_s16le',str(wav)],check=True)
        duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration',
                      '-of','default=noprint_wrappers=1:nokey=1',str(wav)],text=True))
        meta={'lesson':'S022','scene':n,'narration_sha256':sha256(authored.encode()).hexdigest(),
              'reference_sha256':REFERENCE,'model_revision':MODEL,'natural_speed':True,'sample_rate_hz':48000,
              'duration_seconds':duration,'source':'unchanged audio extracted from the published original',
              'source_video_sha256':source_hash,'source_start_seconds':start,'source_end_seconds':end}
        (build/f'S022-{n:02}.json').write_text(json.dumps(meta)+'\n')
        print(f'S022 scene {n}: reused {duration:.2f}s of its verified original soundtrack')


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('source',type=Path);extract(p.parse_args().source)
