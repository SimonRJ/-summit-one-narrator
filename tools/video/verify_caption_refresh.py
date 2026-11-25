"""Check known bad caption transitions in an exact recording's picture-only refresh."""

import argparse
import json
from pathlib import Path
import subprocess
import sys

import numpy as np
from PIL import Image

from preserve_encoded_audio import packets
from restore_recorded_candidate import ROOT, digest, validate_bundle

sys.path.insert(0, str(ROOT / 'production/lesson-films'))
from render_recorded import frames_for

CAPTION_TOP = 945
CAPTION_BOTTOM = 1050
MAX_CAPTION_GLYPH_ERROR = 12
MAX_ARTWORK_ERROR = 5


def decoded_frames(movie, numbers):
    expression = '+'.join(f'eq(n,{number})' for number in numbers)
    raw = subprocess.check_output([
        'ffmpeg', '-nostdin', '-v', 'error', '-xerror', '-threads', '2',
        '-filter_threads', '1', '-i', str(movie), '-an',
        '-vf', "select='" + expression + "',format=rgb24", '-fps_mode', 'vfr',
        '-f', 'rawvideo', 'pipe:1'])
    data = np.frombuffer(raw, dtype=np.uint8)
    assert len(data) == len(numbers) * 1920 * 1080 * 3, 'Missing exact decoded frame'
    return dict(zip(numbers, data.reshape(-1, 1080, 1920, 3)))


def mean_error(actual, expected, mask=None):
    delta = np.abs(actual.astype('int16') - expected.astype('int16'))
    if mask is not None:
        delta = delta[mask]
    return float(delta.mean())


def verify(manifest, lesson, source, output, source_only=False):
    spec = manifest['lessons'][lesson]
    assets = {name: (source / 'assets' / name).read_bytes() for name in spec['assets']}
    provenance = {
        name: (source / 'provenance' / name).read_bytes()
        for name in spec['source'].get('provenance_artifact', {}).get('files', {})
    }
    recording = validate_bundle(manifest, spec, assets, provenance)
    for name, data in recording.items():
        assert (source / 'recording' / name).read_bytes() == data, name + ': recording changed'
    timeline, script, _, draw = frames_for(lesson, source / 'recording')
    numbers = sorted({item['frame'] for item in spec['caption_transition_frames']})
    assert numbers and len(numbers) == len(spec['caption_transition_frames'])
    original = source / 'assets' / (lesson + '.mp4')
    before = decoded_frames(original, numbers)
    after = None
    audio_evidence = None
    movie = ROOT / 'media/lesson-films' / (lesson + '.mp4')
    if not source_only:
        after = decoded_frames(movie, numbers)
        guide = json.loads((ROOT / 'production/lesson-films' / lesson / 'guide.json').read_text())
        original_guide = json.loads(assets[lesson + '-guide.json'])
        assert guide['sha256'] == digest(movie.read_bytes())
        assert {key: value for key, value in guide.items() if key != 'sha256'} == {
            key: value for key, value in original_guide.items() if key != 'sha256'
        }, 'Refresh changed teaching metadata'
        original_audio = packets(original, 'a:0')
        candidate_audio = packets(movie, 'a:0')
        assert original_audio and candidate_audio == original_audio, 'AAC packets or timing changed'
        audio_evidence = {
            'aac_packets': len(original_audio),
            'aac_packet_records_sha256': digest(json.dumps(original_audio, sort_keys=True).encode()),
            'aac_bytes_and_timestamps_identical': True,
        }
    output.mkdir(parents=True, exist_ok=True)
    reports = []
    for number in numbers:
        second = number / 30
        expected_image = draw(second, 1.5)
        expected = np.asarray(expected_image)
        assert expected.shape == (1080, 1920, 3)
        caption = expected[CAPTION_TOP:CAPTION_BOTTOM]
        # Restrict the error to visible letters; a mostly empty caption band can
        # otherwise hide the doubled outlines in a small whole-frame average.
        glyphs = caption.mean(axis=2) > 120
        assert int(glyphs.sum()) > 1000, 'Chosen transition does not show a full phrase'
        body_error = mean_error(before[number][:930], expected[:930])
        legacy_error = mean_error(before[number][CAPTION_TOP:CAPTION_BOTTOM], caption, glyphs)
        assert body_error <= MAX_ARTWORK_ERROR, 'Pinned source artwork changed'
        assert legacy_error > MAX_CAPTION_GLYPH_ERROR, 'Known held caption no longer demonstrates its defect'
        old_name = f'{lesson}-frame-{number}-original.png'
        reference_name = f'{lesson}-frame-{number}-reference.png'
        Image.fromarray(before[number]).save(output / old_name)
        expected_image.save(output / reference_name)
        item = {
            'frame': number, 'decoded_seconds': second,
            'glyph_pixels_checked': int(glyphs.sum()),
            'source_artwork_mean_error': round(body_error, 4),
            'held_caption_glyph_mean_error': round(legacy_error, 4),
            'maximum_candidate_caption_glyph_error': MAX_CAPTION_GLYPH_ERROR,
            'original_image': old_name, 'source_reference_image': reference_name,
        }
        if after is not None:
            caption_error = mean_error(after[number][CAPTION_TOP:CAPTION_BOTTOM], caption, glyphs)
            artwork_error = mean_error(after[number][:930], expected[:930])
            assert caption_error <= MAX_CAPTION_GLYPH_ERROR, (
                lesson, number, 'Encoded caption does not match its stable glyph layer', caption_error)
            assert artwork_error <= MAX_ARTWORK_ERROR, 'Refreshed artwork changed'
            candidate_name = f'{lesson}-frame-{number}-candidate.png'
            Image.fromarray(after[number]).save(output / candidate_name)
            item.update(candidate_caption_glyph_mean_error=round(caption_error, 4),
                        candidate_artwork_mean_error=round(artwork_error, 4),
                        candidate_image=candidate_name)
        reports.append(item)
    return {
        'lesson': lesson, 'mode': 'held source and drawing reference only' if source_only else 'actual encoded caption refresh',
        'source_movie_sha256': spec['assets'][lesson + '.mp4']['sha256'],
        'candidate_movie_sha256': None if source_only else digest(movie.read_bytes()),
        'frames': reports, 'audio': audio_evidence,
        'recording_members_unchanged': True,
        'candidate_encoded_acceptance': not source_only,
        'final_editorial_credit': False,
    }


if __name__ == '__main__':
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--manifest', required=True, type=Path)
    cli.add_argument('--lesson', required=True)
    cli.add_argument('--source', required=True, type=Path)
    cli.add_argument('--output', required=True, type=Path)
    cli.add_argument('--source-only', action='store_true', help='Check the held source without encoding a replacement')
    args = cli.parse_args()
    result = verify(json.loads(args.manifest.read_text()), args.lesson, args.source, args.output, args.source_only)
    (args.output / 'caption-refresh-proof.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
