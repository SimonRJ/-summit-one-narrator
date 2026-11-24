"""Recover one completed lesson from pinned takes in an unfinished voice matrix.

This downloads existing audio only. It never starts, cancels or reruns a job and
never synthesizes speech. Alignment still uses prepare_audio.py's recording and
word-matching checks. The manifest pins each complete artifact, including audio.
"""

import argparse
import hashlib
from io import BytesIO
import json
from pathlib import Path
import subprocess
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[2]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def api(path):
    return json.loads(subprocess.check_output(['gh', 'api', path]))


def verify_source(spec):
    """Require this lesson's successful jobs, not its unrelated matrix siblings."""
    repo = spec['repository']
    run = api(f"repos/{repo}/actions/runs/{spec['voice_run']}")
    assert run['head_sha'] == spec['voice_commit'], 'Unexpected voice source commit'
    assert run['head_branch'] == spec['voice_branch'], 'Unexpected voice branch'
    assert run['path'] == spec['voice_workflow'], 'Unexpected voice workflow'
    assert run['event'] == 'push', 'Unexpected voice event'
    assert run['repository']['full_name'] == repo, 'Unexpected voice repository'
    assert run['head_repository']['full_name'] == repo, 'Forked audio is not accepted'
    old = api(f"repos/{repo}/actions/runs/{spec['original_render_run']}")
    assert old['head_sha'] == spec['original_render_commit']
    assert old['path'] == spec['original_render_workflow']
    assert old['status'] == 'completed' and old['conclusion'] in ('failure', 'cancelled'), (
        'The original renderer is active or succeeded; do not duplicate it',
        old['status'], old['conclusion'])
    jobs = api(f"repos/{repo}/actions/runs/{spec['voice_run']}/jobs?per_page=100")
    assert jobs['total_count'] <= 100, 'Paginate before accepting a larger source run'
    ready = {job['name'] for job in jobs['jobs']
             if job['status'] == 'completed' and job['conclusion'] == 'success'}
    expected = {f"voice ({spec['lesson']}, {a['scene']})" for a in spec['artifacts']}
    assert expected <= ready, f'Missing successful voice jobs: {sorted(expected - ready)}'
    available = api(f"repos/{repo}/actions/runs/{spec['voice_run']}/artifacts?per_page=100")
    assert available['total_count'] <= 100, 'Paginate before accepting a larger artifact list'
    by_id = {a['id']: a for a in available['artifacts']}
    for item in spec['artifacts']:
        actual = by_id[item['id']]
        assert actual['name'] == item['name'] and not actual['expired']
        assert actual['digest'] == 'sha256:' + item['sha256'], 'Artifact digest changed'
        assert actual['workflow_run']['id'] == spec['voice_run']


def checked_take(spec, item, archive, narration):
    assert digest(archive) == item['sha256'], f"{item['name']}: archive digest changed"
    stem = f"{spec['lesson']}-{item['scene']:02}"
    names = {stem + '.json', stem + '.wav'}
    with ZipFile(BytesIO(archive)) as z:
        assert len(z.namelist()) == 2 and set(z.namelist()) == names, (
            item['name'], 'unexpected archive members', z.namelist())
        files = {name: z.read(name) for name in names}
    meta = json.loads(files[stem + '.json'])
    assert meta['lesson'] == spec['lesson'] and meta['scene'] == item['scene']
    assert meta['narration_sha256'] == digest(narration.encode()), 'Script/take mismatch'
    assert meta['reference_sha256'] == spec['voice_reference'], 'Wrong narration voice'
    assert meta['model_revision'] == spec['model_revision'], 'Wrong voice model revision'
    assert meta['natural_speed'] is True and meta['sample_rate_hz'] == 48000
    assert 0 < meta['duration_seconds'] < 180
    return files


def recover(spec, output, archives=None):
    script = json.loads((ROOT / 'production/scripts' / (spec['lesson'] + '.json')).read_text())
    parts = {scene['n']: scene['narration'] for scene in script['scenes']}
    assert script['id'] == spec['lesson']
    assert set(parts) == {item['scene'] for item in spec['artifacts']}
    assert len(parts) == len(spec['artifacts']), 'Duplicate take in pinned manifest'
    if archives is None:
        verify_source(spec)
    recovered = {}
    for item in spec['artifacts']:
        if archives is None:
            data = subprocess.check_output([
                'gh', 'api',
                f"repos/{spec['repository']}/actions/artifacts/{item['id']}/zip"])
        else:
            data = (archives / (item['name'] + '.zip')).read_bytes()
        recovered.update(checked_take(spec, item, data, parts[item['scene']]))
    # Validate the entire set before writing; never overwrite another recording.
    output.mkdir(parents=True, exist_ok=True)
    for name, data in recovered.items():
        target = output / name
        if target.exists():
            assert target.read_bytes() == data, f'Refusing to replace {target}'
    for name, data in recovered.items():
        (output / name).write_bytes(data)
    return {'lesson': spec['lesson'], 'takes': len(parts), 'source_run': spec['voice_run'],
            'mode': 'local archive verification' if archives else 'pinned GitHub recovery',
            'files': {name: digest(data) for name, data in sorted(recovered.items())}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--archives', type=Path, help='Verify already downloaded ZIPs without network or job lookup')
    args = parser.parse_args()
    print(json.dumps(recover(json.loads(args.manifest.read_text()), args.output, args.archives), indent=2))
