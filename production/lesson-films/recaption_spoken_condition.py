"""Refresh one pinned spoken-condition scene, retaining approved audio and timing.

The default remains the original S020 candidate. S019 explicitly selects its
exact returned public edition; no new recording, ASR or timeline alignment runs.
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
POLICIES = {
    'S020': {'scene_number': 9, 'source_sha256': SOURCE_SHA, 'assets': SOURCE_ASSETS},
    'S019': {
        'scene_number': 5,
        'source_sha256': '51545b1baf76d155f052fdcedc6bfde126e45c63845e97468166c0e069bc365f',
        'assets': {
            'S019.mp4': '51545b1baf76d155f052fdcedc6bfde126e45c63845e97468166c0e069bc365f',
            'S019-guide.json': 'e072bbcb020b381720a7ebb5f23476b22d3070dd1beb413264228455a86c9639',
            'S019-poster.jpg': 'e51125931fcc24dcb1577ec7ad1cf05fc1e3803a632685f5c3e8524d30faf822',
            'S019-qa.json': '2c6f54543d62bcd5dcb8ac021501008e8c7c4b16a41effe41802f6abd444eb5b',
            'S019-recording.zip': 'b1ad8709874843e26d52dd0cb104008c85010ff96e443b200b02c243c44d8abd',
            'S019.vtt': '92f0c39344a9dc9729bf1f34db93b2f5c3047f5bde22cbcc419a8d09c46a3c41',
        },
    },
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


def probe(movie):
    return json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_streams',
        '-show_format', '-of', 'json', str(movie)]))


def packet_records(movie, stream):
    return json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', stream,
        '-show_packets', '-show_entries', 'packet=pts,dts,duration,size,data_hash',
        '-show_data_hash', 'sha256', '-of', 'json', str(movie)]))['packets']


def check_stream_identity(before, after):
    """Use actual stream lengths, not rounded container duration (S019 has a short video tail)."""
    assert abs(float(before['format']['duration']) - float(after['format']['duration'])) < .001
    for kind in ('video', 'audio'):
        a = next(s for s in before['streams'] if s['codec_type'] == kind)
        b = next(s for s in after['streams'] if s['codec_type'] == kind)
        fields = ('codec_name', 'time_base', 'start_time', 'duration', 'nb_frames')
        if kind == 'video':
            fields += ('width', 'height', 'r_frame_rate', 'pix_fmt')
        else:
            fields += ('sample_rate', 'channels')
        assert {key: a.get(key) for key in fields} == {key: b.get(key) for key in fields}, (kind, a, b)


def selected_scene(lesson, timeline, script):
    assert timeline['id'] == script['id'] == lesson
    assert timeline['narration_reference'] == '0f3304a393ee504e9fa22537267ac03f150569a5fab0859616f261d009513362'
    assert len(timeline['scenes']) == len(script['scenes'])
    for scene, part in zip(timeline['scenes'], script['scenes']):
        assert ' '.join(word['text'] for word in scene['words']) == part['narration']
    index = POLICIES[lesson]['scene_number'] - 1
    scene = timeline['scenes'][index]
    assert scene['n'] == index + 1
    first, stop = [round(scene[key] * FPS) for key in ('start', 'end')]
    assert abs(scene['start'] - first/FPS) < 1e-7
    assert abs(scene['end'] - stop/FPS) < 1e-7
    narration = script['scenes'][index]['narration']
    if lesson == 'S020':
        assert 'The next exponent is forty-nine.' in narration
        assert [pow(3, n, 10) for n in (49, 50, 51)] == [3, 9, 7]
        assert sum(pow(3, n, 10) for n in range(1, 52)) % 10 == 9
    else:
        assert len(timeline['scenes']) == 11
        assert 'In the top row, cross out the two squares farthest to the left.' in narration
        remaining = {(row, col) for row in range(4) for col in range(4)} - {(0, 0), (0, 1)}
        dominoes = [((0, 2), (0, 3)), *[((row, col), (row, col+1))
            for row in range(1, 4) for col in (0, 2)]]
        covered = [cell for pair in dominoes for cell in pair]
        assert len(dominoes) == 7 and len(covered) == len(set(covered)) == 14
        assert set(covered) == remaining
        assert all(abs(a[0]-b[0]) + abs(a[1]-b[1]) == 1 for a, b in dominoes)
        assert sum((row+col) % 2 == 0 for row, col in remaining) == 7
    return scene, first, stop


def rebuild(source, output, lesson='S020'):
    policy = POLICIES[lesson]
    source = source.resolve()
    output = output.resolve()
    assert source != output, 'Keep the original candidate immutable'
    for name, expected in policy['assets'].items():
        assert digest(source/name) == expected, f'Unexpected source asset: {name}'
    original = source / f'{lesson}.mp4'
    assert digest(original) == policy['source_sha256'], 'Unexpected source candidate'
    guide = json.loads((source / f'{lesson}-guide.json').read_text())
    assert guide['sha256'] == policy['source_sha256']
    with ZipFile(source / f'{lesson}-recording.zip') as archive:
        timeline = json.loads(archive.read('timeline.json'))
        script = json.loads(archive.read('script.json'))
    scene, first, stop = selected_scene(lesson, timeline, script)
    original_info = probe(original)
    original_audio_packets = packet_records(original, 'a:0')
    original_video_packets = packet_records(original, 'v:0')
    cues = [cue for cue in timeline['captions'] if scene['start'] <= cue['start'] < scene['end']]
    output.mkdir(parents=True, exist_ok=True)
    insert = output / f'.scene{scene["n"]}.mp4'
    command = ['ffmpeg', '-nostdin', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
        '-s', '1920x1080', '-r', str(FPS), '-i', 'pipe:0', '-c:v', 'libx264', '-crf', '18',
        '-preset', 'veryfast', '-threads', '2', '-pix_fmt', 'yuv420p', str(insert)]
    with subprocess.Popen(command, stdin=subprocess.PIPE) as encoder:
        for n in range(stop-first):
            encoder.stdin.write(draw(lesson, scene, cues, (first+n)/FPS, 1.5).tobytes())
        encoder.stdin.close()
        assert encoder.wait() == 0, 'Correction scene did not encode'
    graph = f'[0:v]split=2[left][right];[left]trim=end_frame={first},setpts=PTS-STARTPTS[v0];[right]trim=start_frame={stop},setpts=PTS-STARTPTS[v2];[v0][1:v][v2]concat=n=3:v=1:a=0[out]'
    movie = output / f'{lesson}.mp4'
    ffmpeg('-y', '-i', original, '-i', insert, '-filter_complex_threads', '2', '-filter_complex', graph,
        '-map', '[out]', '-map', '0:a:0', '-c:v', 'libx264', '-crf', '17', '-preset', 'veryfast',
        '-threads', '2', '-pix_fmt', 'yuv420p', '-r', str(FPS), '-fps_mode', 'cfr',
        '-video_track_timescale', '15360', '-c:a', 'copy', '-movflags', '+faststart', movie)
    ffmpeg('-xerror', '-i', movie, '-f', 'null', '-')
    assert packets(movie) == packets(original), 'Narration packets changed'
    info = probe(movie)
    check_stream_identity(original_info, info)
    assert packet_records(movie, 'a:0') == original_audio_packets, 'AAC bytes or timestamps changed'
    new_video_packets = packet_records(movie, 'v:0')
    assert sorted((p['pts'], p['duration']) for p in new_video_packets) == sorted(
        (p['pts'], p['duration']) for p in original_video_packets), 'Video presentation times changed'
    assert [p['dts'] for p in new_video_packets] == [p['dts'] for p in original_video_packets], 'Video decode times changed'
    video = next(s for s in info['streams'] if s['codec_type'] == 'video')
    assert [video['width'], video['height'], video['r_frame_rate']] == [1920, 1080, '30/1']
    duration = float(info['format']['duration'])
    assert abs(duration - guide['seconds']) < .001
    before, after = frames(original), frames(movie)
    assert before.shape == after.shape
    errors = []
    original_scene_errors = []
    corrected_scene_errors = []
    for second, actual in enumerate(after):
        intended = (np.asarray(draw(lesson, scene, cues, second, 1.5).resize((320,180), Image.Resampling.BOX))
                    if scene['start'] <= second < scene['end'] else before[second])
        diff = abs(actual.astype('int16') - intended.astype('int16'))
        errors.append([float(diff[:153].mean()), float(diff[153:].mean())])
        (corrected_scene_errors if scene['start'] <= second < scene['end'] else original_scene_errors).append(errors[-1])
    worst = np.max(errors, axis=0).tolist()
    assert max(worst) < 5, worst
    guide['sha256'] = digest(movie)
    guide['seconds'] = duration
    (output / f'{lesson}-guide.json').write_text(json.dumps(guide, ensure_ascii=False, indent=2)+'\n')
    for name in (f'{lesson}.vtt', f'{lesson}-recording.zip'):
        shutil.copyfile(source / name, output / name)
        assert digest(source / name) == digest(output / name)
    draw(lesson, scene, [], scene['speech_end'], 1.5).save(output / f'{lesson}-poster.jpg', quality=92)
    qa = json.loads((source / f'{lesson}-qa.json').read_text())
    qa.update(sha256=guide['sha256'], prior_candidate_sha256=policy['source_sha256'],
        caption_treatment=f'One stable bold phrase; no regular/bold glyph cross-fade in scene {scene["n"]}',
        audio_packets_identical=True, timeline_and_vtt_identical=True,
        caption_repair_reference_comparisons=len(after), caption_repair_largest_mean_picture_difference=worst,
        caption_repair_scene=scene['n'], other_scenes_retained=len(timeline['scenes'])-1,
        original_other_scene_comparisons=len(original_scene_errors),
        original_other_scene_maximum_difference=np.max(original_scene_errors, axis=0).tolist(),
        corrected_scene_comparisons=len(corrected_scene_errors),
        original_video_frames=int(video['nb_frames']), source_aac_packets=len(original_audio_packets),
        audio_packet_bytes_and_timestamps_identical=True, stream_times_and_video_frame_count_identical=True,
        video_presentation_and_decode_timestamps_identical=True,
        timeline_vtt_script_lossless_recording_archive_identical=True, new_synthesis=False, new_recognition=False,
        final_editorial_credit=False)
    (output / f'{lesson}-qa.json').write_text(json.dumps(qa, ensure_ascii=False, indent=2)+'\n')
    insert.unlink()
    print(json.dumps({'id':lesson, 'scene':scene['n'], 'sha256':guide['sha256'], 'duration':duration, 'audio_packets_identical':True, 'comparisons':len(after), 'largest_picture_difference':worst}), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--lesson', choices=tuple(POLICIES), default='S020')
    args = parser.parse_args()
    rebuild(args.source, args.output, args.lesson)
