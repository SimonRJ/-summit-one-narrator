"""Rebuild S020's corrected scene from its pinned recording, retaining AAC packets.

The input is the exact S020-reviewed-candidate artifact from run 45491820136.
No voice synthesis, audio stretching, script change or timeline realignment occurs.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
from zipfile import ZipFile

import numpy as np
from PIL import Image

from repair_spoken_condition import draw

SOURCE_SHA = 'fa00a38665821402f0a2060c40b4aa7ae4b89632609862a80607f39a4cc5006f'
SOURCE_ASSETS = {
    'S020.mp4': SOURCE_SHA,
    'S020-guide.json': '80d6e410c94507343d5e64bc453be1523587d46391924b4aa7ae4f466b0c7a89',
    'S020-poster.jpg': 'fef51caf206f8ba7551db5bb2e518dfd80c6315f07959c7c5e5024ae30f0f6d0',
    'S020-qa.json': 'f1e8bc1c82bbab84d5e2f87c5986bb3ca3fd3fed7998052c33302af97e7ae653',
    'S020-recording.zip': '72a341a6ea59e73738f444e7ff81b89d381c6dd04f7a9e65ead43d474308405f',
    'S020.vtt': '7a22be8ae311bffa0561f49e91cb547132a6e6ed44e86e751763341c579a0fe3',
}
FPS = 30


def digest(path):
    with path.open('rb') as handle:
        return hashlib.file_digest(handle, 'sha256').hexdigest()


def ffmpeg(*args):
    return subprocess.check_output(['ffmpeg', '-nostdin', '-v', 'error', '-threads', '2', *map(str, args)])


def packets(movie):
    return ffmpeg('-i', movie, '-map', '0:a:0', '-c:a', 'copy', '-f', 'adts', 'pipe:1')


def frames(movie):
    return np.frombuffer(ffmpeg('-i', movie, '-an', '-vf',
        "select='not(mod(n,30))',scale=320:180:flags=area,format=rgb24",
        '-fps_mode', 'vfr', '-f', 'rawvideo', 'pipe:1'), np.uint8).reshape(-1, 180, 320, 3)


def rebuild(source, output):
    source = source.resolve()
    output = output.resolve()
    assert source != output, 'Keep the original candidate immutable'
    for name, expected in SOURCE_ASSETS.items():
        assert digest(source/name) == expected, f'Unexpected source asset: {name}'
    original = source / 'S020.mp4'
    assert digest(original) == SOURCE_SHA, 'Unexpected source candidate'
    guide = json.loads((source / 'S020-guide.json').read_text())
    assert guide['sha256'] == SOURCE_SHA
    with ZipFile(source / 'S020-recording.zip') as archive:
        timeline = json.loads(archive.read('timeline.json'))
        script = json.loads(archive.read('script.json'))
    assert timeline['id'] == script['id'] == 'S020'
    assert timeline['narration_reference'] == '0f3304a393ee504e9fa22537267ac03f150569a5fab0859616f261d009513362'
    for scene, part in zip(timeline['scenes'], script['scenes']):
        assert ' '.join(word['text'] for word in scene['words']) == part['narration']
    scene = timeline['scenes'][8]
    first, stop = [round(scene[key] * FPS) for key in ('start', 'end')]
    assert abs(scene['start'] - first/FPS) < 1e-7
    assert abs(scene['end'] - stop/FPS) < 1e-7
    assert 'The next exponent is forty-nine.' in script['scenes'][8]['narration']
    assert [pow(3, n, 10) for n in (49, 50, 51)] == [3, 9, 7]
    assert sum(pow(3, n, 10) for n in range(1, 52)) % 10 == 9
    cues = [cue for cue in timeline['captions'] if scene['start'] <= cue['start'] < scene['end']]
    output.mkdir(parents=True, exist_ok=True)
    insert = output / '.scene9.mp4'
    command = ['ffmpeg', '-nostdin', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
        '-s', '1920x1080', '-r', str(FPS), '-i', 'pipe:0', '-c:v', 'libx264', '-crf', '18',
        '-preset', 'veryfast', '-threads', '2', '-pix_fmt', 'yuv420p', str(insert)]
    with subprocess.Popen(command, stdin=subprocess.PIPE) as encoder:
        for n in range(stop-first):
            encoder.stdin.write(draw('S020', scene, cues, (first+n)/FPS, 1.5).tobytes())
        encoder.stdin.close()
        assert encoder.wait() == 0, 'Correction scene did not encode'
    graph = f'[0:v]split=2[left][right];[left]trim=end_frame={first},setpts=PTS-STARTPTS[v0];[right]trim=start_frame={stop},setpts=PTS-STARTPTS[v2];[v0][1:v][v2]concat=n=3:v=1:a=0[out]'
    movie = output / 'S020.mp4'
    ffmpeg('-y', '-i', original, '-i', insert, '-filter_complex_threads', '2', '-filter_complex', graph,
        '-map', '[out]', '-map', '0:a:0', '-c:v', 'libx264', '-crf', '17', '-preset', 'veryfast',
        '-threads', '2', '-pix_fmt', 'yuv420p', '-r', str(FPS), '-fps_mode', 'cfr',
        '-video_track_timescale', '15360', '-c:a', 'copy', '-movflags', '+faststart', movie)
    ffmpeg('-xerror', '-i', movie, '-f', 'null', '-')
    assert packets(movie) == packets(original), 'Narration packets changed'
    info = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(movie)]))
    video = next(s for s in info['streams'] if s['codec_type'] == 'video')
    assert [video['width'], video['height'], video['r_frame_rate']] == [1920, 1080, '30/1']
    duration = float(info['format']['duration'])
    assert abs(duration - guide['seconds']) < .001
    assert int(video['nb_frames']) == round(guide['seconds'] * FPS)
    before, after = frames(original), frames(movie)
    assert before.shape == after.shape
    errors = []
    for second, actual in enumerate(after):
        intended = (np.asarray(draw('S020', scene, cues, second, 1.5).resize((320,180), Image.Resampling.BOX))
                    if scene['start'] <= second < scene['end'] else before[second])
        diff = abs(actual.astype('int16') - intended.astype('int16'))
        errors.append([float(diff[:153].mean()), float(diff[153:].mean())])
    worst = np.max(errors, axis=0).tolist()
    assert max(worst) < 5, worst
    guide['sha256'] = digest(movie)
    guide['seconds'] = duration
    (output / 'S020-guide.json').write_text(json.dumps(guide, ensure_ascii=False, indent=2)+'\n')
    for name in ('S020.vtt', 'S020-recording.zip'):
        shutil.copyfile(source / name, output / name)
        assert digest(source / name) == digest(output / name)
    draw('S020', scene, [], scene['speech_end'], 1.5).save(output / 'S020-poster.jpg', quality=92)
    qa = json.loads((source / 'S020-qa.json').read_text())
    qa.update(sha256=guide['sha256'], prior_candidate_sha256=SOURCE_SHA,
        caption_treatment='One stable bold phrase; no regular/bold glyph cross-fade in scene 9',
        audio_packets_identical=True, timeline_and_vtt_identical=True,
        caption_repair_reference_comparisons=len(after), caption_repair_largest_mean_picture_difference=worst)
    (output / 'S020-qa.json').write_text(json.dumps(qa, ensure_ascii=False, indent=2)+'\n')
    insert.unlink()
    print(json.dumps({'sha256':guide['sha256'], 'duration':duration, 'audio_packets_identical':True, 'comparisons':len(after), 'largest_picture_difference':worst}), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    rebuild(args.source, args.output)
