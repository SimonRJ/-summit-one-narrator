"""Apply the reviewed S015 timing patch to its exact held CI recording, without ASR or synthesis."""

import argparse
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[2]
RECORDING_NAMES = {'script.json', 'timeline.json', 'captions.vtt', 'narration.flac'}


def digest(data):
    return sha256(data).hexdigest()


def checked_files(archive, root=ROOT):
    proof = json.loads((root / 'review/S015-numeral-timing-correction-20261125.json').read_text())
    for name, expected in proof['source_hashes'].items():
        assert digest((root / name).read_bytes()) == expected, f'Reviewed drawing/timing source changed: {name}'
    data = archive.read_bytes()
    assert digest(data) == proof['source_candidate_archive_sha256'], 'Wrong source candidate archive'
    with ZipFile(BytesIO(data)) as candidate:
        movie = candidate.read('S015.mp4')
        recording = candidate.read('S015-recording.zip')
    assert digest(movie) == proof['source_master_sha256'], 'Wrong held movie'
    assert digest(recording) == proof['source_recording_archive_sha256'], 'Wrong archived recording'
    with ZipFile(BytesIO(recording)) as source:
        assert set(source.namelist()) == RECORDING_NAMES, 'Unexpected recording members'
        files = {name: source.read(name) for name in RECORDING_NAMES}
    assert {name: digest(data) for name, data in files.items()} == proof['source_recording_files']
    assert files['script.json'] == (root / 'production/scripts/S015.json').read_bytes(), 'Script changed'
    old = json.loads(files['timeline.json'])
    saved = root / 'production/lesson-films/voice-c-repairs'
    files['timeline.json'] = (saved / 'S015-numeral-timeline.json').read_bytes()
    files['captions.vtt'] = (saved / 'S015-numeral-captions.vtt').read_bytes()
    assert {name: digest(data) for name, data in files.items()} == proof['corrected_recording_files']
    new = json.loads(files['timeline.json'])
    assert {k: v for k, v in old.items() if k not in ('scenes', 'captions')} == {
        k: v for k, v in new.items() if k not in ('scenes', 'captions')}, 'Timeline identity changed'
    assert len(old['scenes']) == len(new['scenes']) == 8
    evidence = {scene['scene']: scene for scene in proof['affected_scenes']}
    for before, after in zip(old['scenes'], new['scenes']):
        assert {k: v for k, v in before.items() if k != 'words'} == {
            k: v for k, v in after.items() if k not in ('words', 'numeral_timing_repairs')}
        assert len(before['words']) == len(after['words'])
        observed = []
        for index, (a, b) in enumerate(zip(before['words'], after['words'])):
            assert {k: v for k, v in a.items() if k not in ('start', 'end')} == {
                k: v for k, v in b.items() if k not in ('start', 'end')}, 'Spoken text or match status changed'
            assert 0 <= b['start'] <= b['end'] <= after['speech_end']
            if a != b:
                observed.append({'word_index': index, 'text': a['text'], 'before': a, 'after': b})
        assert observed == evidence.get(before['n'], {}).get('changed_words', []), 'Unreviewed word timing'
        assert all(a['end'] <= b['start'] + 1e-6 for a, b in zip(after['words'], after['words'][1:]))
    script = json.loads(files['script.json'])
    assert ' '.join(c['text'] for c in new['captions']) == ' '.join(s['narration'] for s in script['scenes'])
    assert all(c['start'] < c['end'] for c in new['captions'])
    assert all(a['end'] <= b['start'] + 1e-6 for a, b in zip(new['captions'], new['captions'][1:]))
    assert digest(files['narration.flac']) == proof['source_recording_files']['narration.flac']
    return files, movie, proof


def apply(archive, output, audio_source):
    files, movie, proof = checked_files(archive)
    targets = {output / name: data for name, data in files.items()}
    targets[audio_source] = movie
    # Check everything before writing; a repeated invocation is idempotent.
    for path, data in targets.items():
        assert not path.exists() or path.read_bytes() == data, f'Refusing to replace {path}'
    for path, data in targets.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    return {'id': 'S015', 'source_master_sha256': proof['source_master_sha256'],
            'source_candidate_archive_sha256': proof['source_candidate_archive_sha256'],
            'corrected_recording_files': proof['corrected_recording_files'],
            'reviewed_scenes': sorted(s['scene'] for s in proof['affected_scenes']),
            'changed_word_timings': sum(len(s['changed_words']) for s in proof['affected_scenes']),
            'lossless_audio_preserved': True, 'new_recognition': False, 'new_synthesis': False}


if __name__ == '__main__':
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--candidate', required=True, type=Path)
    cli.add_argument('--output', required=True, type=Path)
    cli.add_argument('--audio-source', required=True, type=Path)
    args = cli.parse_args()
    print(json.dumps(apply(args.candidate, args.output, args.audio_source), indent=2))
