"""Build and validate the teaching-video production scripts.

Source: production/scripts/src/*.txt (plain text, one block per video).
Output: production/scripts/<ID>.json (one file per video) and production/scripts/INDEX.md.

Each script follows docs/VIDEO_TEACHING_STANDARD.md: insight, why it matters,
puzzle, development, variation or trap, recap with a notebook exercise. Scenes
carry a visual direction (V) and the narration to be spoken (N). No audio or
animation is produced here; timings must come from the final recorded narration.

Run: python tools/video/build_scripts.py          (validate and write)
     python tools/video/build_scripts.py --check  (validate only)
"""
import json, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'production/scripts/src'
OUT = ROOT / 'production/scripts'
STAGES = ('INSIGHT', 'WHY', 'PUZZLE', 'DEVELOP', 'VARIATION', 'RECAP')
APPROVED = {'T02.1': 'Approved studio edition already published (media/T02.1.mp4). Keep its audio unchanged.',
            'T02.2': 'Approved studio edition already published (media/T02.2.mp4). Keep its audio unchanged.'}
WPM = 150  # planning estimate only

def parse():
    scripts = {}
    for f in sorted(SRC.glob('*.txt')):
        for block in re.split(r'^@@ ', f.read_text(), flags=re.M)[1:]:
            lines = block.strip().split('\n')
            vid = lines[0].strip()
            assert vid not in scripts, f'duplicate {vid}'
            s = dict(id=vid, goal='', scenes=[], exercise='', exercise_answer='', source=f.name)
            cur = None
            for ln in lines[1:]:
                if not ln.strip():
                    continue
                if ln.startswith('GOAL: '): s['goal'] = ln[6:].strip()
                elif ln.startswith('TRY: '): s['exercise'] = ln[5:].strip()
                elif ln.startswith('ANS: '): s['exercise_answer'] = ln[5:].strip()
                elif re.match(r'^\[([A-Z]+)\]$', ln):
                    cur = dict(stage=ln[1:-1], visual='', narration=''); s['scenes'].append(cur)
                elif ln.startswith('V: '): cur['visual'] = ln[3:].strip()
                elif ln.startswith('N: '): cur['narration'] = ln[3:].strip()
                else: raise AssertionError(f'{vid}: unrecognised line: {ln[:60]}')
            scripts[vid] = s
    return scripts

def validate(scripts, items):
    by_id = {i['id']: i for i in items}
    problems = []
    for vid, s in scripts.items():
        def bad(msg): problems.append(f'{vid}: {msg}')
        if vid not in by_id: bad('not in data/teaching-72.json'); continue
        if vid in APPROVED: bad('already approved; do not rescript')
        kind = by_id[vid]['type']
        stages = [c['stage'] for c in s['scenes']]
        if any(x not in STAGES for x in stages): bad(f'unknown stage in {stages}')
        if not s['goal'] or not s['exercise'] or not s['exercise_answer']: bad('missing goal, exercise or answer')
        if stages[-1:] != ['RECAP']: bad('must end with RECAP')
        need = ('INSIGHT', 'WHY', 'PUZZLE', 'DEVELOP', 'VARIATION', 'RECAP') if kind == 'concept' else ('PUZZLE', 'DEVELOP', 'VARIATION', 'RECAP')
        for x in need:
            if x not in stages: bad(f'missing stage {x}')
        if kind == 'concept' and stages[:2] != ['INSIGHT', 'WHY']: bad('concept videos open with INSIGHT then WHY, before the puzzle')
        for n, c in enumerate(s['scenes'], 1):
            if not c['visual'] or not c['narration']: bad(f'scene {n} lacks visual or narration')
            if re.search(r'\bA\d{3}\b|\bN\d\.\d+\b', c['narration'] + c['visual']): bad(f'scene {n} refers to an archive item')
            if re.search(r'[=×÷+^]|\d\s*/\s*\d|\bx\s+\d', c['narration']): bad(f'scene {n} narration contains symbols; spell maths out for speech')
        words = sum(len(c['narration'].split()) for c in s['scenes'])
        lo, hi = (240, 620) if kind == 'concept' else (160, 420)
        if not lo <= words <= hi: bad(f'narration is {words} words; expected {lo}-{hi} for a {kind}')
        s['narration_words'] = words
        s['estimated_minutes'] = round(words / WPM, 1)
    return problems

def main():
    items = json.loads((ROOT / 'data/teaching-72.json').read_text())['items']
    scripts = parse()
    problems = validate(scripts, items)
    missing = [i['id'] for i in items if i['id'] not in scripts and i['id'] not in APPROVED]
    if problems:
        print('\n'.join(problems)); raise SystemExit(f'{len(problems)} script problems')
    if '--check' not in sys.argv:
        for old in OUT.glob('T*.json'): old.unlink()
        rows = []
        for i in items:
            vid = i['id']
            if vid in APPROVED:
                rows.append(f'| {vid} | {i["title"]} | {i["type"]} | approved video | | {APPROVED[vid]} |'); continue
            if vid not in scripts:
                rows.append(f'| {vid} | {i["title"]} | {i["type"]} | not yet scripted | | |'); continue
            s = scripts[vid]
            doc = dict(id=vid, title=i['title'], chapter=i['chapter'], type=i['type'], status='script_ready_not_recorded',
                       voice='Voice C (VoxCPM2), natural speed (see docs/VIDEO_PRODUCTION.md)', goal=s['goal'],
                       narration_words=s['narration_words'], estimated_minutes=s['estimated_minutes'],
                       scenes=[dict(n=k, **c) for k, c in enumerate(s['scenes'], 1)],
                       notebook_exercise=s['exercise'], notebook_answer=s['exercise_answer'])
            (OUT / f'{vid}.json').write_text(json.dumps(doc, ensure_ascii=False, indent=1) + '\n')
            rows.append(f'| {vid} | {i["title"]} | {i["type"]} | script ready | {s["narration_words"]} words, about {s["estimated_minutes"]} min | [{vid}.json]({vid}.json) |')
        head = ('# Teaching-video scripts\n\nGenerated by `python tools/video/build_scripts.py` from `src/*.txt`. Do not edit the JSON files by hand.\n\n'
                'Status meanings: **script ready** = narration and visual directions written and validated, nothing recorded or animated; '
                '**approved video** = a finished video already exists and is not to be rescripted.\n\n'
                f'Scripts ready: {len(scripts)} of {len(items)}. Approved videos: {len(APPROVED)}. Not yet scripted: {len(missing)}.\n\n'
                '| ID | Title | Type | Status | Length | File |\n|---|---|---|---|---|---|\n')
        (OUT / 'INDEX.md').write_text(head + '\n'.join(rows) + '\n')
    print(f'PASS: {len(scripts)} scripts valid; {len(APPROVED)} approved videos untouched; {len(missing)} not yet scripted{": " + ", ".join(missing[:8]) if missing else ""}.')

if __name__ == '__main__':
    main()
