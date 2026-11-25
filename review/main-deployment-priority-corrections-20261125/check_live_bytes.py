"""Compare deployed public bytes with the frozen priority-corrections source.

Preparation is offline: --plan-only writes the expected manifest without HTTP.
Run the live comparison only after the parent confirms the matching Pages build.
All requests are ordinary public GETs with the query versions used by the site.
No browser, account, learner state, synthesis, or publication is involved.
"""

import argparse
import concurrent.futures
import datetime
import hashlib
import json
from pathlib import Path
import re
import subprocess
import urllib.request


ROOT = Path(__file__).resolve().parents[2]
SOURCE_COMMIT = 'e287b9102574b8a6cbc29beba97ccc9a7dc569fe'
SOURCE_TREE = 'de6b0b43b98bba31a2a6ec3cf633210c1c2b3bdf'
BASE = 'https://simonrj.github.io/-summit-one-narrator/'
APP_VERSION = 'priority-corrections-20261125'
FONT_VERSION = 'local-fonts-20261125'
WELCOME_VERSION = 'course-films-target-clock-20261125'

PLAIN_APP = [
    'index.html', 'sw.js', 'lesson-introduction-videos.html',
    'watch-lesson-intro.html', 'offline-reader.html',
]
VERSIONED_APP = [
    'app-main.js', 'course-menu-ui.js', 'lesson-introduction-media.js',
    'lesson-introduction-library.js', 'offline-reader.js',
    'data/read-watch-practise.json', 'data/read-watch-practise-later.json',
    'data/recorded-studies.json', 'data/teaching-72.json',
]
STANDALONE = [
    ('welcome.html', None), ('welcome.js', WELCOME_VERSION),
    ('welcome.css', 'chapter-navigation-20261122'),
    ('watch-amc-2025-q17.html', None), ('watch-t18-1.html', None),
    ('teaching-videos.html', None),
    ('lesson-video-chapters.js', 'chapter-seek-20261122'),
    ('lesson-video-chapters.js', 'seek-1'),
    ('media/AMCIntroduction.mp4', WELCOME_VERSION),
    ('media/AMCIntroduction-poster.jpg', WELCOME_VERSION),
    ('media/AMCIntroduction.vtt', None),
    ('media/AMCIntroduction-transcript.txt', None),
    ('review/AMCIntroduction-qa.json', WELCOME_VERSION),
    ('media/AMC2025Q17-voice-c.mp4', WELCOME_VERSION),
    ('media/AMC2025Q17-voice-c-poster.jpg', WELCOME_VERSION),
    ('media/AMC2025Q17-voice-c.vtt', WELCOME_VERSION),
    ('review/AMC2025Q17-voice-c.json', None),
    ('media/T18.1.mp4', 'thirteen-search'),
    ('media/T18.1-studio-poster.jpg', 'thirteen-search'),
    ('media/T18.1.vtt', None), ('review/T18.1-studio-qa.json', None),
]
MOVIE_PINS = {
    'media/AMCIntroduction.mp4': '5373ccb4f27d875cbd2f05ce8aa4d5d57de25643529c2a434f58ef3e602bb9f5',
    'media/AMC2025Q17-voice-c.mp4': '10c454496ef92f044a50841ebffc0f7711afc5432997386f577560cf4737950d',
    'media/T18.1.mp4': '3527d02410e4b1158af7d42a5d8abce16cb6fed702947b8fa864af25590635ce',
}
FILMS = {
    'S009': ('carry-reversal-reviewed-20261125-bcbd31159202',
             '39d28fec11fe4cc1b1d1b840d01ab8d8b3ae3ccb6d184bf37c1ccf4e37c16ef6', [9, 228], 'retained'),
    'S010': ('carry-reversal-reviewed-20261125-bcbd31159202',
             'e8e2e6f697b00cd9401479a603bf6992c2538a107b3fbd519cac0e0b9b7f9a71', [10, 319], 'retained'),
    'S012': ('s012-missing-rung-20261125-b46d28d6d374',
             '87e71ca9ae8e3355f9f092f05a7e4c0678313aa569bbc3b4cc63a200ff2cedd7', [12, 248], 'retained'),
    'S015': ('s015-numeral-timing-20261125-41b7922d37ed',
             '19765de3ce9c28259d244c41d370cb3073513bc928124167e58cc21497098c89', [15, 260], 'new'),
    'S020': ('s020-stable-captions-20261125-0dfec081086f',
             '5308674d7d66dee6545d05699311a192b13e2fce2d48b6d2f560ec35ce1e57f3', [20, 283], 'new'),
    'S102': ('s102-tens-units-20261125-a84046b06450',
             'f08e10363f675d7cb9e46fd31e5f766fdbbacd248af3ddded95b2a06eb40f6e1', [102, 296], 'new'),
}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def source(path):
    return subprocess.check_output(['git', 'show', SOURCE_COMMIT + ':' + path], cwd=ROOT)


def prepare():
    actual_commit = subprocess.check_output(['git', 'rev-parse', SOURCE_COMMIT + '^{commit}'], cwd=ROOT).decode().strip()
    actual_tree = subprocess.check_output(['git', 'rev-parse', SOURCE_COMMIT + '^{tree}'], cwd=ROOT).decode().strip()
    assert actual_commit == SOURCE_COMMIT and actual_tree == SOURCE_TREE
    font_manifest = json.loads(source('fonts/sources.json'))
    fonts = font_manifest['fonts']
    assert len(fonts) == 28 and len({f['filename'] for f in fonts}) == 28
    css = source('design-system.css').decode()
    css_fonts = set(re.findall(r'url\((fonts/[^)]+\.woff2)\)', css))
    assert css_fonts == {'fonts/' + f['filename'] for f in fonts}
    entries = [(p, None, 'app') for p in PLAIN_APP]
    entries += [(p, APP_VERSION, 'app') for p in VERSIONED_APP]
    assert len(entries) == 14
    entries += [(p, FONT_VERSION, 'font-stylesheet') for p in ('design-system.css', 'public-study-theme.css')]
    entries += [('fonts/sources.json', None, 'font-manifest')]
    entries += [('fonts/' + f['filename'], None, 'font') for f in fonts]
    entries += [(p, version, 'standalone') for p, version in STANDALONE]
    expected = {}
    manifest = []
    for path, version, category in entries:
        if path not in expected:
            expected[path] = source(path)
        data = expected[path]
        relative_url = path + ('?v=' + version if version else '')
        manifest.append({'path': path, 'url': BASE + relative_url, 'category': category,
                         'query_version': version, 'expected_bytes': len(data), 'expected_sha256': digest(data)})
    assert len({m['url'] for m in manifest}) == len(manifest)
    for f in fonts:
        data = expected['fonts/' + f['filename']]
        assert digest(data) == f['sha256'] and len(data) == f['bytes']
    for path, pin in MOVIE_PINS.items():
        assert digest(expected[path]) == pin, 'Frozen source differs from verified returned movie: ' + path
    declarations = check_declarations(expected)
    assert declarations['all_routes_match'] and declarations['all_page_declarations_match'], declarations
    return manifest, expected, declarations


def check_declarations(responses):
    results = {'routes': [], 'pages': [], 'errors': []}
    try:
        catalogue = json.loads(responses['data/recorded-studies.json'])
        lessons = {}
        for path in ('data/read-watch-practise.json', 'data/read-watch-practise-later.json'):
            lessons.update({row['slot']: row for row in json.loads(responses[path])['lessons']})
        for film, (tag, pin, slots, group) in FILMS.items():
            expected_movie = 'https://github.com/SimonRJ/-summit-one-narrator/releases/download/' + tag + '/' + film + '.mp4'
            guide = catalogue['lessons'][film]
            guide_movie = (guide.get('release') or catalogue['release']) + film + '.mp4'
            for slot in slots:
                row = lessons[slot]
                canonical = slot == int(film[1:])
                checks = {
                    'film_identity': row['videoId'] == film,
                    'movie_and_catalogue': row['movie'] == guide_movie == expected_movie,
                    'guide_movie_sha256': guide['sha256'] == pin,
                    'title': row['videoTitle'] == guide['title'],
                    'film_use': row['filmUse'] == ('dedicated' if canonical else 'technique'),
                    'bridge': bool(row['bridge']) and (not canonical or row['bridge'] == guide['bridge']),
                }
                if film == 'S102':
                    checks['corrected_bridge'] = '153 becomes 135' in row['bridge'] and 'incorrect here' not in row['bridge']
                results['routes'].append({'slot': slot, 'film': film, 'group': group, 'movie': row['movie'],
                    'guide_movie_sha256': guide['sha256'], 'bridge': row['bridge'], 'checks': checks,
                    'match': all(checks.values())})
    except Exception as error:
        results['errors'].append('Route declarations: ' + type(error).__name__ + ': ' + str(error))
    try:
        text = {p: b.decode() for p, b in responses.items() if b is not None and p.endswith(('.html', '.js', '.css', '.json'))}
        required = {
            'index.html': ['app-main.js?v=' + APP_VERSION, 'design-system.css?v=' + FONT_VERSION],
            'sw.js': ['summit-one-' + APP_VERSION] + [p + '?v=' + APP_VERSION for p in VERSIONED_APP],
            'public-study-theme.css': ['design-system.css?v=' + FONT_VERSION],
            'welcome.html': ['welcome.js?v=' + WELCOME_VERSION, 'media/AMCIntroduction.mp4?v=' + WELCOME_VERSION,
                             'media/AMCIntroduction-poster.jpg?v=' + WELCOME_VERSION],
            'welcome.js': ['review/AMCIntroduction-qa.json?v=' + WELCOME_VERSION],
            'watch-amc-2025-q17.html': ['media/AMC2025Q17-voice-c.mp4?v=' + WELCOME_VERSION,
                'media/AMC2025Q17-voice-c-poster.jpg?v=' + WELCOME_VERSION,
                'media/AMC2025Q17-voice-c.vtt?v=' + WELCOME_VERSION,
                'lesson-video-chapters.js?v=chapter-seek-20261122'],
            'watch-t18-1.html': ['media/T18.1.mp4?v=thirteen-search',
                'media/T18.1-studio-poster.jpg?v=thirteen-search', 'lesson-video-chapters.js?v=seek-1'],
            'teaching-videos.html': ['href="watch-t18-1.html"'],
            'lesson-introduction-library.js': ['"S102-Intro.mp4": "Correction: keep the hundreds digit fixed'],
        }
        for path, strings in required.items():
            missing = [s for s in strings if s not in text[path]]
            results['pages'].append({'path': path, 'required_declarations': strings, 'missing': missing, 'match': not missing})
        teaching = json.loads(responses['data/teaching-72.json'])
        t18 = next(item for item in teaching['items'] if item['id'] == 'T18.1')
        results['pages'].append({'path': 'data/teaching-72.json', 'film': 'T18.1', 'movie': t18['video_url'],
                                 'match': t18['video_url'] == 'media/T18.1.mp4?v=thirteen-search'})
        welcome_qa = json.loads(responses['review/AMCIntroduction-qa.json'])
        t18_qa = json.loads(responses['review/T18.1-studio-qa.json'])
        results['pages'].append({'path': 'review/AMCIntroduction-qa.json', 'sha256': welcome_qa['sha256'],
                                 'match': welcome_qa['sha256'] == MOVIE_PINS['media/AMCIntroduction.mp4']})
        results['pages'].append({'path': 'review/T18.1-studio-qa.json', 'sha256': t18_qa['sha256'],
                                 'match': t18_qa['sha256'] == MOVIE_PINS['media/T18.1.mp4']})
    except Exception as error:
        results['errors'].append('Page declarations: ' + type(error).__name__ + ': ' + str(error))
    results['all_routes_match'] = len(results['routes']) == 12 and all(r['match'] for r in results['routes'])
    results['all_six_new_routes_match'] = len([r for r in results['routes'] if r['group'] == 'new']) == 6 and all(r['match'] for r in results['routes'] if r['group'] == 'new')
    results['all_six_retained_routes_match'] = len([r for r in results['routes'] if r['group'] == 'retained']) == 6 and all(r['match'] for r in results['routes'] if r['group'] == 'retained')
    results['all_page_declarations_match'] = len(results['pages']) == 12 and all(r['match'] for r in results['pages']) and not results['errors']
    return results


def fetch(entry, expected):
    result = dict(entry)
    request = urllib.request.Request(entry['url'], headers={'User-Agent': 'AMC-public-deployment-byte-verification'})
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            data = response.read()
            result.update(status=response.status, final_url=response.geturl(), actual_bytes=len(data),
                          actual_sha256=digest(data), exact_match=data == expected[entry['path']],
                          headers={k: response.headers.get(k) for k in ('ETag', 'Last-Modified', 'Cache-Control', 'Content-Type')})
        return result, data
    except Exception as error:
        result.update(exact_match=False, error=type(error).__name__ + ': ' + str(error))
        return result, None


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--output', type=Path, required=True)
    cli.add_argument('--plan-only', action='store_true')
    cli.add_argument('--deployment-commit', help='Exact main commit whose identical source tree passed Pages')
    cli.add_argument('--pages-run-id', type=int)
    args = cli.parse_args()
    if args.output.exists():
        cli.error('Output already exists; preserve prior observations and choose a new path')
    if not args.plan_only and not re.fullmatch(r'[0-9a-f]{40}', args.deployment_commit or ''):
        cli.error('Supply the exact deployment commit only after Pages success is confirmed')
    manifest, expected, local_declarations = prepare()
    report = {'source_commit': SOURCE_COMMIT, 'source_tree': SOURCE_TREE, 'deployment_commit': args.deployment_commit,
              'pages_run_id': args.pages_run_id, 'site': BASE,
              'checked_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'scope': 'Public HTTP response bytes and declared routes; no browser or learner-state operations.',
              'http_concurrency': 4, 'invented_cache_bypass_queries': False, 'final_editorial_credit': False,
              'browser_playback_checked': False}
    if args.plan_only:
        report.update(mode='OFFLINE_EXPECTED_MANIFEST_ONLY', files=manifest,
                      immutable_source_declarations=local_declarations, live_requests_made=False)
        passed = True
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            checked = list(pool.map(lambda entry: fetch(entry, expected), manifest))
        responses = {entry['path']: data for entry, (_, data) in zip(manifest, checked)}
        report.update(mode='LIVE_PUBLIC_BYTES', files=[row for row, _ in checked], live_requests_made=True,
                      declarations=check_declarations(responses))
        report['all_bytes_match'] = all(row['exact_match'] for row, _ in checked)
        report['font_files_verified'] = sum(row['exact_match'] for row, _ in checked if row['category'] == 'font')
        report['standalone_movie_pins_match'] = all(responses.get(path) is not None and digest(responses[path]) == pin for path, pin in MOVIE_PINS.items())
        passed = (report['all_bytes_match'] and report['font_files_verified'] == 28 and report['standalone_movie_pins_match']
                  and report['declarations']['all_routes_match'] and report['declarations']['all_page_declarations_match'])
        report['passed'] = passed
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x') as stream:
        stream.write(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'report': str(args.output), 'mode': report['mode'], 'requests': 0 if args.plan_only else len(manifest),
                      'expected_resources': len(manifest), 'passed': passed,
                      'failed_files': [r['path'] for r in report['files'] if r.get('exact_match') is False]}, indent=2))
    return 0 if passed else 1


if __name__ == '__main__':
    raise SystemExit(main())
