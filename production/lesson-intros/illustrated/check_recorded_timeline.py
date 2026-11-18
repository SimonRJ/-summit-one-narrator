"""Check the delivered caption frames, diagrams and audio against a word-aligned Voice C master."""
import argparse
from bisect import bisect_right
import hashlib
import json
from pathlib import Path
import subprocess

import numpy as np
from PIL import Image

from check_encoded_timeline import probe, samples
from render_voiced_board import Movie, PAPER, spoken_caption


def pcm(path):
    command = ['ffmpeg', '-nostdin', '-v', 'error', '-i', str(path), '-map', '0:a:0',
               '-ar', '16000', '-ac', '1', '-f', 'f32le', '-']
    return np.frombuffer(subprocess.check_output(command), dtype=np.float32)


def check(lesson, folder, delivery):
    timing = json.loads((folder / 'timeline.json').read_text())
    film = Movie(lesson, timing, 1.5)
    data = probe(delivery)
    video, audio = data['streams']
    if (video['width'], video['height'], video['avg_frame_rate'], video['codec_name'], audio['codec_name']) != (1920, 1080, '30/1', 'h264', 'aac'):
        raise ValueError('Unexpected media format')
    frames = int(video['nb_frames'])
    if abs(frames / 30 - timing['duration']) >= .06:
        raise ValueError('The movie and the recording have different durations')
    reference, result = pcm(folder / 'narration.wav'), pcm(delivery)
    if abs(len(reference) - len(result)) >= 1600:
        raise ValueError('The public audio and the session master have different lengths')
    correlations = []
    for scene in timing['scenes']:
        a, b = int(scene['start'] * 16000), int(scene['speech_end'] * 16000)
        u, v = reference[a:b], result[a:b]
        correlations.append(float(np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))))
    if min(correlations) <= .985:
        raise ValueError('A spoken scene differs from its authored voice master')
    strip = samples(delivery, 'crop=1920:150:0:930,scale=384:30:flags=area,format=gray', 'gray', (30, 384))
    if len(strip) != frames:
        raise ValueError('A caption frame is missing')
    blank = Image.new('RGB', (1920, 150), PAPER)
    cap_errors = []
    for n, delivered in enumerate(strip):
        t = n / 30
        k = bisect_right(film.capstarts, t) - 1
        image = spoken_caption(film.caps[k], t, 1.5) if k >= 0 and t < film.caps[k][0]['end'] else blank
        expected = np.asarray(image.resize((384, 30), Image.Resampling.BOX).convert('L'), dtype=np.int16)
        cap_errors.append(float(np.abs(expected - delivered).mean()))
    body = samples(delivery, "select='not(mod(n,15))',crop=1920:930:0:0,scale=192:93:flags=area,format=rgb24",
                   'rgb24', (93, 192, 3))
    if len(body) != (frames + 14) // 15:
        raise ValueError('A sampled picture is missing')
    image_errors, tile_errors = [], []
    for i, delivered in enumerate(body):
        expected = film.frame(i / 2, False).crop((0, 0, 1920, 930)).resize((192, 93), Image.Resampling.BOX)
        err = np.abs(np.asarray(expected, dtype=np.int16) - delivered)
        image_errors.append(float(err.mean()))
        tile_errors.append(float(err[:90].reshape(6, 15, 12, 16, 3).mean(axis=(1, 3, 4)).max()))
    metrics = dict(caption_peak_mean_luma=max(cap_errors), picture_peak_mean_rgb=max(image_errors),
                   picture_peak_tile_rgb=max(tile_errors))
    if metrics['caption_peak_mean_luma'] > 4 or metrics['picture_peak_mean_rgb'] > 5 or metrics['picture_peak_tile_rgb'] > 18:
        raise ValueError(f'The delivered timeline differs from its word-aligned drawing: {metrics}')
    return {'id': lesson, 'sha256': hashlib.sha256(delivery.read_bytes()).hexdigest(),
            'caption_frames_checked': frames, 'drawings_checked': len(body), 'drawing_interval_seconds': .5,
            'spoken_words_checked': sum(len(s['words']) for s in timing['scenes']),
            'minimum_scene_audio_correlation': round(min(correlations), 5),
            **{k: round(v, 3) for k,v in metrics.items()}}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('lesson')
    p.add_argument('recording', type=Path)
    p.add_argument('delivery', type=Path)
    p.add_argument('--report', type=Path)
    args = p.parse_args()
    result = json.dumps(check(args.lesson, args.recording, args.delivery), indent=2) + '\n'
    if args.report:
        args.report.write_text(result)
    print(result, end='')
