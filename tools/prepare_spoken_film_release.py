"""Prepare S019/S020/S102 changes only from successful, public releases.

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
        'run': 45524933207,
        'commit': 'ac244dec713654fa7fb47693c8c179d9fb436479',
        'workflow': '.github/workflows/s019-caption-stability.yml',
        'tag': 's019-stable-captions-20261125-ac244dec7136',
        'sha256': '5455c0c0119bedd897ddda6feb41002cf215575c8f8839565661674c42ad712c',
        'slots': [19, 333],
        'source_sha256': '51545b1baf76d155f052fdcedc6bfde126e45c63845e97468166c0e069bc365f',
        'held_sha256': [
            '51545b1baf76d155f052fdcedc6bfde126e45c63845e97468166c0e069bc365f',
            '4a549a8cdb160102a38b9e9e63c409188f41406c300c05f2041694a3348d7a16',
        ],
        'recording_sha256': 'b1ad8709874843e26d52dd0cb104008c85010ff96e443b200b02c243c44d8abd',
        'vtt_sha256': '92f0c39344a9dc9729bf1f34db93b2f5c3047f5bde22cbcc419a8d09c46a3c41',
    },
    'S020': {
        'run': 45503875492,
        'commit': '0dfec081086f153023e2ab74861717d75dbaa779',
        'workflow': '.github/workflows/s020-caption-stability.yml',
        'tag': 's020-stable-captions-20261125-0dfec081086f',
        'sha256': '5308674d7d66dee6545d05699311a192b13e2fce2d48b6d2f560ec35ce1e57f3',
        'slots': [20, 283],
        'held_sha256': 'fa00a38665821402f0a2060c40b4aa7ae4b89632609862a80607f39a4cc5006f',
    },
    'S102': {
        'run': 45518273975,
        'commit': 'a84046b0645063f273951ce85d938aa71fffa9ee',
        'workflow': '.github/workflows/s102-digit-swap.yml',
        'tag': 's102-tens-units-20261125-a84046b06450',
        'slots': [102, 296],
        'recording_sha256': '4582dcd016527a350da681f165b53e32ade863c7e3ea011aa5863e892cb8593b',
        'source_sha256': '538f9142a5113e5d14d3a35b6a7851e8dd331e16aba7d98224a7d0c294601612',
        'held_sha256': [
            'dad309128905a96c6b3784b63eb12df2b6545ffe9fc930b7cf7ded0c89b9cec4',
            'c0bc373168fb2221642b660339d0cbf948d9019d283ad88dc002126a716e5c49',
        ],
        'canonical_bridge': ('Keep the hundreds digit fixed and swap tens and units: 153 becomes 135. '
                             'Count the printed threes in each column separately.'),
        'consumer_bridge': ('For the multiples-of-nine count, keep hundreds fixed and swap tens and units: '
                            '153 becomes 135. Which digit choices force the missing digit?'),
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
    require(not policy.get('hold_reason'), policy.get('hold_reason'))
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
        require(movie_digest not in policy['held_sha256'],
                'Held or unpublished S019 candidate rejected')
        require(movie_digest == policy['sha256'], 'This is not the final S019 CI edition')
        require(qa.get('prior_candidate_sha256') == policy['source_sha256'],
                'S019 caption repair does not identify its pinned source')
        require(identity['S019-recording.zip'] == policy['recording_sha256']
                and identity['S019.vtt'] == policy['vtt_sha256'],
                'S019 original recording archive or VTT changed')
        require(all(qa.get(key) is True for key in (
            'audio_packets_identical', 'timeline_and_vtt_identical',
            'audio_packet_bytes_and_timestamps_identical',
            'stream_times_and_video_frame_count_identical',
            'video_presentation_and_decode_timestamps_identical',
            'timeline_vtt_script_lossless_recording_archive_identical')),
            'S019 original audio, timeline or caption preservation is unverified')
        require(qa.get('new_synthesis') is False and qa.get('new_recognition') is False
                and qa.get('original_video_frames') == 4269
                and qa.get('source_aac_packets') == 6673,
                'S019 saved-take or exact stream-length evidence differs')
        require(qa.get('scene_replaced') == qa.get('caption_repair_scene') == 5
                and qa.get('other_scenes_retained') == 10,
                'S019 no longer describes the scoped scene-five caption repair')
        require(qa.get('picture_comparison_period_seconds') == 1
                and qa.get('decoded_reference_comparisons') == 143
                and qa.get('caption_repair_reference_comparisons') == 143
                and qa.get('original_other_scene_comparisons') == 129
                and qa.get('corrected_scene_comparisons') == 14,
                'S019 lacks complete encoded-picture comparisons')
        for key in ('caption_repair_largest_mean_picture_difference',
                    'original_other_scene_maximum_difference'):
            differences = qa.get(key, [])
            require(isinstance(differences, list) and len(differences) == 2
                    and all(isinstance(value, (int, float)) and 0 <= value < 5
                            for value in differences),
                    'S019 encoded-picture differences exceed the checked bounds')
    elif lesson == 'S020':
        require(movie_digest != policy['held_sha256'], 'Held doubled-caption edition rejected')
        require(movie_digest == policy['sha256'], 'This is not the final S020 CI edition')
        require(qa.get('prior_candidate_sha256') == policy['held_sha256'],
                'Caption repair does not identify its pinned source candidate')
        require(qa.get('audio_packets_identical') is True
                and qa.get('timeline_and_vtt_identical') is True,
                'Approved audio or caption timing preservation is unverified')
        require(qa.get('caption_repair_reference_comparisons', 0) >= 190,
                'Final caption repair lacks encoded-picture comparison evidence')
    else:
        require(movie_digest not in policy['held_sha256'], 'Held S102 numeral-timing edition rejected')
        require(qa.get('input_recording_sha256') == policy['recording_sha256'],
                'S102 does not use the one preserved Voice C take')
        require(qa.get('source_sha256') == policy['source_sha256']
                and qa.get('scene_replaced') == 8
                and qa.get('preserved_source_scenes') == [1, 2, 3, 4, 5, 6, 7, 9, 10, 11],
                'S102 no longer describes the scoped scene-eight repair')
        require(qa.get('mathematical_check') == {
            'range': [100, 599], 'divisor': 9,
            'pairs': [[153, 135], [243, 234], [333, 333], [423, 432], [513, 531]],
            'ones': 5, 'tens': 5, 'hundreds': 11, 'total': 21,
        }, 'S102 digit pairing or count differs from the checked correction')
        matches = qa.get('corrected_passage_match_percent', [])
        require(len(matches) == 4 and min(matches) >= 95,
                'S102 lacks all four measured spoken-number passages')
        require(qa.get('decoded_reference_comparisons', 0) >= 216,
                'S102 lacks complete encoded-picture comparisons')
        require(guide['bridge'] == policy['canonical_bridge'],
                'S102 released guide still has old or unreviewed bridge wording')

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
        bridge = guide['bridge'] if canonical else row['bridge']
        if lesson == 'S019':
            # The existing canonical and technique cues are already correct.
            # A caption-only release must not rewrite either lesson's bridge.
            if canonical:
                require(guide['bridge'] == row['bridge'],
                        'S019 released guide would change the existing lesson bridge')
            bridge = row['bridge']
        if lesson == 'S102' and not canonical:
            bridge = policy['consumer_bridge']
        changes.append({
            'file': 'data/' + filename,
            'slot': row['slot'],
            'expected_current_movie': row['movie'],
            'expected_current_video_id': lesson,
            'set': {'movie': base + lesson + '.mp4', 'videoTitle': guide['title'],
                    'filmUse': 'dedicated' if canonical else 'technique',
                    'bridge': bridge},
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
        'additional_opening_bridges': ([{
            'file': 'tools/content/practice-revisions-20261121.json',
            'key': 'S296', 'bridge': policy['consumer_bridge'],
        }] if lesson == 'S102' else []),
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
