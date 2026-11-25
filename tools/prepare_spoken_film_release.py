"""Prepare S019/S020 catalogue changes only from successful, public releases.

Pass unmodified GitHub workflow-run and release API JSON plus the downloaded
public release package. This writes a reviewable plan to a new output file;
it never edits learner routes, review counts, the database or the source tree.
"""
import argparse
import hashlib
import json
from pathlib import Path


REPOSITORY = 'SimonRJ/-summit-one-narrator'
ROOT = Path(__file__).resolve().parents[1]
POLICY = {
    'S019': {
        'run': 45491819969,
        'commit': '3d94f6856b475eb160c11bf7b6334ff13e9c61b6',
        'workflow': '.github/workflows/s019-domino-condition.yml',
        'tag': 's019-domino-condition-20261125-3d94f6856b47',
        'sha256': '51545b1baf76d155f052fdcedc6bfde126e45c63845e97468166c0e069bc365f',
        'slots': [19, 333],
    },
    'S020': {
        'run': 45503875492,
        'commit': '0dfec081086f153023e2ab74861717d75dbaa779',
        'workflow': '.github/workflows/s020-caption-stability.yml',
        'tag': 's020-stable-captions-20261125-0dfec081086f',
        'slots': [20, 283],
        'held_sha256': 'fa00a38665821402f0a2060c40b4aa7ae4b89632609862a80607f39a4cc5006f',
    },
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha256(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def prepare(lesson, run, release, package, root=ROOT):
    policy = POLICY[lesson]
    require(run.get('id') == policy['run'], 'Wrong production workflow run')
    require(run.get('head_sha') == policy['commit'], 'Wrong production source commit')
    require(run.get('path') == policy['workflow'], 'Wrong production workflow path')
    require(run.get('status') == 'completed' and run.get('conclusion') == 'success',
            'Production render, playback and release gates have not all succeeded')
    require(release.get('tag_name') == policy['tag'], 'Wrong immutable release tag')
    require(release.get('draft') is False and release.get('published_at'),
            'The immutable release is not public')
    require(release.get('target_commitish') == policy['commit'], 'Release source commit differs')

    base = f'https://github.com/{REPOSITORY}/releases/download/{policy["tag"]}/'
    names = [lesson + suffix for suffix in
             ('.mp4', '.vtt', '-guide.json', '-qa.json', '-poster.jpg', '-recording.zip')]
    assets = release.get('assets', [])
    identity = {}
    for name in names:
        matches = [asset for asset in assets if asset.get('name') == name]
        require(len(matches) == 1, f'Missing or ambiguous public asset: {name}')
        asset = matches[0]
        require(asset.get('state') == 'uploaded', f'Incomplete public asset: {name}')
        require(asset.get('browser_download_url') == base + name,
                f'Unexpected public asset location: {name}')
        local = package / name
        require(local.is_file(), f'Missing downloaded public asset: {name}')
        require(local.stat().st_size == asset.get('size'), f'Asset length differs: {name}')
        digest = sha256(local)
        require(asset.get('digest') == 'sha256:' + digest,
                f'Public GitHub digest does not match downloaded asset: {name}')
        identity[name] = digest

    guide = json.loads((package / f'{lesson}-guide.json').read_text())
    qa = json.loads((package / f'{lesson}-qa.json').read_text())
    movie_digest = identity[f'{lesson}.mp4']
    require(guide.get('sha256') == qa.get('sha256') == movie_digest,
            'Guide, QA and delivered movie identities differ')
    require(guide.get('title') and guide.get('bridge') and guide.get('transcript'),
            'The released guide is incomplete')
    require(abs(guide['seconds'] - qa['full_duration_seconds']) < .001,
            'Guide and QA durations differ')
    starts = [chapter['start'] for chapter in guide['chapters']]
    require(starts and starts[0] == 0 and starts == sorted(set(starts))
            and starts[-1] < guide['seconds'], 'Invalid measured chapters')
    if lesson == 'S019':
        require(movie_digest == policy['sha256'], 'This is not the final S019 CI edition')
    else:
        require(movie_digest != policy['held_sha256'], 'Held doubled-caption edition rejected')
        require(qa.get('prior_candidate_sha256') == policy['held_sha256'],
                'Caption repair does not identify its pinned source candidate')
        require(qa.get('audio_packets_identical') is True
                and qa.get('timeline_and_vtt_identical') is True,
                'Approved audio or caption timing preservation is unverified')
        require(qa.get('caption_repair_reference_comparisons', 0) >= 190,
                'Final caption repair lacks encoded-picture comparison evidence')

    rows = []
    for filename in ('read-watch-practise.json', 'read-watch-practise-later.json'):
        for row in json.loads((root / 'data' / filename).read_text())['lessons']:
            if row.get('videoId') == lesson:
                rows.append((filename, row))
    require(sorted(row['slot'] for _, row in rows) == policy['slots'],
            'Film consumers changed; review new assignments before integrating')
    changes = []
    for filename, row in rows:
        canonical = row['slot'] == int(lesson[1:])
        require(canonical or row.get('filmUse') == 'technique',
                'A later lesson now has its own dedicated film; do not overwrite it')
        changes.append({
            'file': 'data/' + filename,
            'slot': row['slot'],
            'expected_current_movie': row['movie'],
            'expected_current_video_id': lesson,
            'set': {'movie': base + lesson + '.mp4', 'videoTitle': guide['title'],
                    'filmUse': 'dedicated' if canonical else 'technique',
                    'bridge': guide['bridge'] if canonical else row['bridge']},
        })
    return {
        'lesson': lesson,
        'production_run': policy['run'],
        'production_commit': policy['commit'],
        'release_tag': policy['tag'],
        'released_asset_sha256': identity,
        'catalogue_file': 'data/recorded-studies.json',
        'catalogue_entry': {**guide, 'release': base},
        'route_changes': changes,
        'canonical_opening_bridge': {'file': 'tools/content/practice-revisions-20261121.json',
                                     'key': lesson, 'bridge': guide['bridge']},
        'remaining_release_steps': [
            'Apply only the listed fields, retaining all worked examples, practice IDs and grading editions.',
            'Refresh the catalogue query and matching app/service-worker cache versions in the combined release.',
            'Run the recorded-study and read/practice checks, then check the exact public learner routes.',
            'Keep final editorial credit pending until that independent acceptance is complete.',
        ],
        'source_tree_modified': False,
        'editorial_completion_awarded': False,
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lesson', choices=POLICY, required=True)
    parser.add_argument('--run-report', type=Path, required=True)
    parser.add_argument('--release-report', type=Path, required=True)
    parser.add_argument('--package', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    try:
        require(not args.output.resolve().is_relative_to(ROOT.resolve()),
                'Write the staging plan outside the repository')
        plan = prepare(args.lesson, json.loads(args.run_report.read_text()),
                       json.loads(args.release_report.read_text()), args.package)
        with args.output.open('x') as stream:
            stream.write(json.dumps(plan, ensure_ascii=False, indent=2) + '\n')
    except (ValueError, KeyError, FileNotFoundError) as error:
        parser.exit(1, f'No integration plan written: {error}\n')
    print(f'Prepared {args.lesson} from its successful public release; source tree and completion counts unchanged.')
