"""Restore a pinned complete recording for a picture-only caption refresh.

Sources are immutable public release assets or one successful, pinned Actions
renderer. This module never aligns, synthesizes, dispatches or cancels anything.
It validates every byte before writing and refuses to replace different files.
"""

import argparse
import hashlib
from io import BytesIO
import json
from pathlib import Path
import subprocess
import urllib.request
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[2]
RECORDING_MEMBERS = {'script.json', 'timeline.json', 'captions.vtt', 'narration.flac'}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def checked_bytes(data, expected, label):
    assert len(data) == expected['bytes'], f'{label}: byte count changed'
    assert digest(data) == expected['sha256'], f'{label}: SHA-256 changed'
    return data


def checked_archive(data, expected, label):
    with ZipFile(BytesIO(data)) as archive:
        names = archive.namelist()
        assert len(names) == len(expected) and set(names) == set(expected), (
            label, 'unexpected or duplicate archive members', names)
        assert all(Path(name).name == name and '\\' not in name for name in names)
        return {
            name: checked_bytes(archive.read(name), expected[name], label + '/' + name)
            for name in sorted(names)
        }


def api(path):
    return json.loads(subprocess.check_output(['gh', 'api', path]))


def verify_actions_source(repository, source):
    run = api(f"repos/{repository}/actions/runs/{source['run']}")
    assert run['head_sha'] == source['commit'], 'Unexpected recording source commit'
    assert run['head_branch'] == source['branch'], 'Unexpected recording source branch'
    assert run['path'] == source['workflow'] and run['event'] == 'push'
    assert run['repository']['full_name'] == repository
    assert run['head_repository']['full_name'] == repository, 'Forked source is not accepted'
    job = api(f"repos/{repository}/actions/jobs/{source['render_job']}")
    assert job['run_id'] == source['run'] and job['head_sha'] == source['commit']
    assert job['name'] == 'render'
    assert job['status'] == 'completed' and job['conclusion'] == 'success', (
        'The source renderer has not succeeded', job['status'], job['conclusion'])
    for key in ('candidate_artifact', 'provenance_artifact'):
        expected = source[key]
        actual = api(f"repos/{repository}/actions/artifacts/{expected['id']}")
        assert actual['id'] == expected['id'] and actual['name'] == expected['name']
        assert not actual['expired'], 'Pinned recording artifact expired'
        assert actual['digest'] == 'sha256:' + expected['sha256']
        assert actual['size_in_bytes'] == expected['bytes']
        assert actual['workflow_run']['id'] == source['run']
        assert actual['workflow_run']['head_sha'] == source['commit']
        assert actual['workflow_run']['head_branch'] == source['branch']


def read_sources(repository, spec, local_source=None):
    source = spec['source']
    provenance = {}
    if source['kind'] == 'actions_artifact':
        if local_source is None:
            verify_actions_source(repository, source)
        archives = {}
        for key in ('candidate_artifact', 'provenance_artifact'):
            expected = source[key]
            if local_source is None:
                data = subprocess.check_output([
                    'gh', 'api', f"repos/{repository}/actions/artifacts/{expected['id']}/zip"])
            else:
                data = (local_source / expected['archive_name']).read_bytes()
            archives[key] = checked_bytes(data, expected, expected['archive_name'])
        assets = checked_archive(archives['candidate_artifact'], spec['assets'], 'candidate')
        provenance = checked_archive(
            archives['provenance_artifact'], source['provenance_artifact']['files'], 'provenance')
    elif source['kind'] == 'public_release':
        assets = {}
        for name, expected in spec['assets'].items():
            assert expected['url'] == (
                f"https://github.com/{repository}/releases/download/{source['tag']}/{name}")
            if local_source is None:
                with urllib.request.urlopen(expected['url'], timeout=60) as response:
                    data = response.read(expected['bytes'] + 1)
            else:
                data = (local_source / name).read_bytes()
            assets[name] = checked_bytes(data, expected, name)
    else:
        raise ValueError('Unknown pinned recording source')
    return assets, provenance


def validate_bundle(manifest, spec, assets, provenance, root=ROOT):
    lesson = spec['id']
    expected_names = {lesson + ending for ending in (
        '.mp4', '-poster.jpg', '-guide.json', '-qa.json', '.vtt', '-recording.zip')}
    assert set(assets) == set(spec['assets']) == expected_names
    for name, data in assets.items():
        checked_bytes(data, spec['assets'][name], name)
    assert set(spec['recording_files']) == RECORDING_MEMBERS
    recording = checked_archive(
        assets[lesson + '-recording.zip'], spec['recording_files'], 'recording')
    for name, expected_digest in manifest['implementation_files'].items():
        assert digest((root / name).read_bytes()) == expected_digest, name + ': implementation changed'
    assert digest((root / spec['artwork_file']).read_bytes()) == spec['artwork_sha256']
    assert recording['script.json'] == (root / 'production/scripts' / (lesson + '.json')).read_bytes()
    script = json.loads(recording['script.json'])
    timeline = json.loads(recording['timeline.json'])
    guide = json.loads(assets[lesson + '-guide.json'])
    qa = json.loads(assets[lesson + '-qa.json'])
    assert script['id'] == timeline['id'] == guide['id'] == lesson
    assert len(script['scenes']) == len(timeline['scenes']) == spec['scenes']
    assert timeline['narration_reference'] == spec['voice_reference']
    assert timeline['model_revision'] == spec['model_revision']
    assert timeline['duration'] == spec['duration']
    assert len(timeline['captions']) == spec['caption_phrases']
    assert sum(len(scene['words']) for scene in timeline['scenes']) == spec['spoken_words']
    for scene, part in zip(timeline['scenes'], script['scenes']):
        assert ' '.join(word['text'] for word in scene['words']) == part['narration']
    assert ' '.join(part['narration'] for part in script['scenes']) == (
        ' '.join(cue['text'] for cue in timeline['captions']))
    assert assets[lesson + '.vtt'] == recording['captions.vtt']
    assert guide['sha256'] == qa['sha256'] == spec['assets'][lesson + '.mp4']['sha256']
    assert qa['source_voice_reference_sha256'] == spec['voice_reference']
    assert qa['recorded_scenes_checked'] == spec['scenes']
    assert abs(guide['seconds'] - spec['duration']) < .12
    if 'take_provenance' in spec:
        assert json.loads(provenance['build-take-recovery.json']) == spec['take_provenance']
        assert digest((root / 'tools/video' / (lesson.lower() + '-recorded-takes.json')).read_bytes()) == (
            spec['source_takes_manifest_sha256'])
        for number, words in spec['retained_numeric_intervals'].items():
            actual = timeline['scenes'][int(number) - 1]['words']
            assert all(word in actual for word in words), 'Measured numeral intervals changed'
    return recording


def write_verified(output, files):
    # Complete preflight prevents partial replacement when an existing file differs.
    for name, data in files.items():
        target = output / name
        if target.exists():
            assert target.is_file() and target.read_bytes() == data, (
                f'Refusing to replace different existing file: {target}')
    for name, data in files.items():
        target = output / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)


def restore(manifest, lesson, output, local_source=None, root=ROOT):
    assert manifest['schema_version'] == 1 and manifest['final_editorial_credit'] is False
    spec = manifest['lessons'][lesson]
    assert spec['id'] == lesson
    assets, provenance = read_sources(manifest['repository'], spec, local_source)
    recording = validate_bundle(manifest, spec, assets, provenance, root)
    files = {**{'assets/' + name: data for name, data in assets.items()},
             **{'recording/' + name: data for name, data in recording.items()},
             **{'provenance/' + name: data for name, data in provenance.items()}}
    write_verified(output, files)
    return {
        'lesson': lesson, 'source_kind': spec['source']['kind'],
        'mode': 'verified local bytes' if local_source else 'verified remote bytes',
        'source_movie_sha256': spec['assets'][lesson + '.mp4']['sha256'],
        'files': {name: digest(data) for name, data in sorted(files.items())},
        'script_unchanged': True, 'timeline_unchanged': True, 'vtt_unchanged': True,
        'recording_audio_unchanged': True, 'alignment_run': False,
        'speech_generation_run': False, 'final_editorial_credit': False,
    }


if __name__ == '__main__':
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--manifest', required=True, type=Path)
    cli.add_argument('--lesson', required=True)
    cli.add_argument('--output', required=True, type=Path)
    cli.add_argument('--local-source', type=Path, help='Validate saved source assets without network')
    args = cli.parse_args()
    print(json.dumps(restore(
        json.loads(args.manifest.read_text()), args.lesson, args.output, args.local_source), indent=2))
