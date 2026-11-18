"""Compare a delivered caption-preserving film with the approved recording and the author's timed drawings."""
import argparse
import hashlib
import importlib
import json
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image

from captioned_film import drawing, verify_audio


def probe(movie):
    raw = subprocess.check_output(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(movie)])
    return json.loads(raw)


def samples(movie, filters, pixel_format, shape):
    command = ['ffmpeg', '-nostdin', '-v', 'error', '-xerror', '-threads', '2', '-i', str(movie),
               '-an', '-filter_threads', '1', '-vf', filters, '-vsync', '0', '-pix_fmt', pixel_format, '-f', 'rawvideo', '-']
    pixels = subprocess.check_output(command)
    return np.frombuffer(pixels, dtype=np.uint8).reshape((-1,) + shape)


def check(spec, original, delivery):
    spec.verify()
    source_hash = hashlib.sha256(original.read_bytes()).hexdigest()
    if source_hash != spec.ORIGINAL:
        raise ValueError('The original recording differs from the artwork source')
    data = probe(delivery)
    video, audio = data['streams']
    frames = int(video['nb_frames'])
    old_video = probe(original)['streams'][0]
    if (video['width'], video['height'], video['avg_frame_rate'], video['codec_name'], audio['codec_name']) != (1920, 1080, '30/1', 'h264', 'aac'):
        raise ValueError('Unrecognised delivery format')
    if frames != int(old_video['nb_frames']):
        raise ValueError('The timed recording has a different number of frames')
    packet_hash = verify_audio(original, delivery)
    stripe_filter = 'crop=1920:150:0:930,scale=384:30:flags=area,format=gray'
    before = samples(original, stripe_filter, 'gray', (30, 384))
    after = samples(delivery, stripe_filter, 'gray', (30, 384))
    if len(before) != frames or len(after) != frames:
        raise ValueError('A caption frame is missing')
    caption_errors = []
    for i in range(0, frames, 120):
        delta = np.abs(before[i:i+120].astype(np.int16) - after[i:i+120])
        caption_errors.extend(delta.mean(axis=(1, 2)).tolist())
    children = "select='not(mod(n,15))',crop=1920:930:0:0,scale=192:93:flags=area,format=rgb24"
    body = samples(delivery, children, 'rgb24', (93, 192, 3))
    if len(body) != (frames + 14) // 15:
        raise ValueError('A sampled drawing is missing')
    picture_errors = []
    local_errors = []
    for j, delivered in enumerate(body):
        expected = drawing(spec, j / 2, 1.5).resize((192, 93), Image.Resampling.BOX)
        error = np.abs(np.asarray(expected).astype(np.int16) - delivered)
        picture_errors.append(float(error.mean()))
        # A single label, counter or angle can occupy only a small part of a frame.
        # Compare 16-by-15-pixel tiles as well as the entire drawing.
        tiles = error[:90].reshape(6, 15, 12, 16, 3).mean(axis=(1, 3, 4))
        local_errors.append(float(tiles.max()))
    metrics = {'caption_peak_mean_luma': max(caption_errors), 'picture_peak_mean_rgb': max(picture_errors),
               'picture_peak_tile_rgb': max(local_errors)}
    # YouTube-style platform transcoding is outside this comparison. These limits are for
    # the course's H.264 export using its source drawing, caption stripe, and audio packets.
    if metrics['caption_peak_mean_luma'] > 3.5 or metrics['picture_peak_mean_rgb'] > 5 or metrics['picture_peak_tile_rgb'] > 18:
        raise ValueError(f'Timeline differs from the approved source: {metrics}')
    return {'id': spec.ID, 'sha256': hashlib.sha256(delivery.read_bytes()).hexdigest(), 'legacy_sha256': source_hash,
            'frames': frames, 'audio_packets': packet_hash, 'caption_frames_checked': len(after),
            'drawings_checked': len(body), 'drawing_interval_seconds': .5, **{k: round(v, 3) for k, v in metrics.items()}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('module')
    parser.add_argument('original', type=Path)
    parser.add_argument('delivery', type=Path)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    result = check(importlib.import_module(args.module), args.original, args.delivery)
    encoded = json.dumps(result, indent=2) + '\n'
    if args.report:
        args.report.write_text(encoded)
    print(encoded, end='')
