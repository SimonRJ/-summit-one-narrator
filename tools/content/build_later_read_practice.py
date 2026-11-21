"""Compile the private S069–S370 lesson drafts for the course and protected grader."""
import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EDITION = 'read-watch-practise-2'
REVISED_FILM_BRIDGES = {
    ('S086', 197): "Pause when the leak opens at minute three. How much water is already in the tank, and what rate applies to the nine units still needed?",
    ('S074', 74): "Watch the rectangle grow from 8 by 14 to 9 by 15. What proves that every other positive integer width misses the target area?",
    ('S074', 158): "As the shorter side increases by one, watch what happens to the longer side and the area. Why can the target be reached only once?",
    ('S074', 249): "In the rectangle example, the shorter side determines its partner. In the pair puzzle, look for how naming the smaller number avoids listing a pair twice.",
}
FIELDS = ('id', 'source_type', 'source_label', 'category', 'difficulty', 'title',
          'prompt', 'answer', 'unit', 'solution_text', 'spoken_script', 'rights')


def read(path):
    return json.loads(path.read_text())


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def digest(rows):
    def value(row, name):
        return json.dumps(row[name], ensure_ascii=False) if name == 'answer' else str(row[name])
    pieces = [hashlib.md5(chr(31).join(value(row, name) for name in FIELDS).encode()).hexdigest()
              for row in rows]
    return hashlib.md5(''.join(pieces).encode()).hexdigest()


def build(private):
    private = private.resolve()
    if private.is_relative_to(ROOT):
        raise ValueError('Keep the private authoring source outside the public repository.')
    course = read(ROOT / 'data/sessions-372.json')['sessions']
    slots = [s['slot'] for s in course if s['type'] == 'LESSON' and s['slot'] > 68]
    manifest = read(ROOT / 'data/lesson-challenges.json')['items']
    skills = {q['session']: q['skill'] for q in manifest}
    original_ids = {q['id']: q['session'] for q in manifest}
    assert len(slots) == 228 and sorted(int(f.stem[1:]) for f in (private/'drafts').glob('S*.json')) == slots
    revisions = read(ROOT/'tools/content/practice-revisions-20261121.json')
    # Already updated drafts can be rebuilt directly. An older private archive
    # gets the worked solutions for its revised questions from the private overlay.
    overlay_path = private/'practice-revision-solutions.json'
    solution_overlay = read(overlay_path) if overlay_path.exists() else {}
    lessons, rows = [], []
    recorded = read(ROOT/'data/recorded-studies.json')
    existing = read(ROOT/'data/read-watch-practise.json')['lessons']
    normalise = lambda s: re.sub(r'[^a-z0-9]', '', s.casefold())
    stems = {normalise(q['prompt']) for l in existing for q in l['questions']}
    for slot in slots:
        tag = f'S{slot:03}'
        draft = read(private/'drafts'/f'{tag}.json')
        src = read(private/'sources'/f'{tag}.json')
        assert draft['slot'] == src['slot'] == slot
        assert skills[slot] == src['skill'] == skills[int(src['videoId'][1:])]
        assert src['videoId'] in src['videoUrl'] and len(src['transcript']) > 1
        assert bool(draft['intro'] and draft['bridge'] and draft['recap'] and draft['headline'])
        assert draft['example']['prompt'] and len(draft['example']['steps']) >= 2
        retained = draft['retained']
        assert len(retained) == len(set(retained)) and all(original_ids[id] == slot for id in retained)
        example = {k: draft['example'][k] for k in ('prompt', 'steps')}
        diagram = private/'figures'/f'{tag}.svg'
        if diagram.exists():
            alt = draft['example'].get('figureAlt') or draft.get('figureAlt')
            assert alt, tag
            public_path = Path('figures/read-practice') / f'{tag}.svg'
            (ROOT/public_path).write_bytes(diagram.read_bytes())
            example['figure'] = {'src': str(public_path), 'alt': alt}
        lesson = {k: draft[k] for k in ('slot', 'headline', 'intro', 'bridge', 'recap')}
        revised = revisions['openings'].get(tag, {})
        example.update(revised.get('example', {}))
        if 'intro' in revised:
            lesson['intro'] = revised['intro']
        if (src['videoId'], slot) in REVISED_FILM_BRIDGES:
            lesson['bridge'] = REVISED_FILM_BRIDGES[src['videoId'], slot]
        movie = src['videoUrl']
        # The illustrated releases retain the recording used to write each lesson bridge.
        if src['videoId'] in {'S069', 'S071', 'S072', 'S073', 'S074', 'S075', 'S076', 'S079', 'S082', 'S085', 'S086', 'S087', 'S088', 'S092', 'S093', 'S094'} and movie.endswith(src['videoId'] + '-Intro.mp4'):
            movie = movie.removesuffix('.mp4') + '-Illustrated.mp4'
        lesson.update(example=example, skill=src['skill'], videoId=src['videoId'],
                      videoTitle=src['videoTitle'], movie=movie, filmUse=src['mode'],
                      retained=retained, questions=[])
        if tag in recorded['lessons']:
            guide = recorded['lessons'][tag]
            release = guide.get('release') or recorded['release']
            lesson.update(videoId=tag, videoTitle=guide['title'], movie=release + tag + '.mp4',
                          filmUse='dedicated', bridge=guide['bridge'])
        assert len(draft['questions']) == 4, tag
        for i, q in enumerate(draft['questions']):
            id = f'RWL2-{slot:03}-{"ABCD"[i]}'
            if id in revisions['questions']:
                q.update(revisions['questions'][id])
                expected_digest = revisions['solutionHashes'].get(id)
                if expected_digest:
                    solution = solution_overlay.get(id, q['solution'])
                    if hashlib.sha256(solution.encode()).hexdigest() != expected_digest:
                        raise ValueError(f'{id}: refresh the private solution overlay as described in docs/LATER_LESSONS.md')
                    q['solution'] = solution
            assert all(isinstance(q[k], str) and q[k].strip() for k in ('title','prompt','hint','solution')), id
            assert isinstance(q['answer'], (int, float, str)) and not isinstance(q['answer'], bool), id
            if isinstance(q['answer'], str):
                answer = q['answer'].strip()
                numeric = re.fullmatch(r'[+-]?(?:\d+(?:\.\d+)?|\.\d+|\d+\s*/\s*[1-9]\d*)', answer)
                short_text = len(answer) <= 12 and re.fullmatch(r'[a-z .+-]+', answer, re.I)
                assert numeric or short_text, f'{id}: answer cannot be marked by the protected grader'
            stem = normalise(q['prompt'])
            assert stem not in stems, f'Duplicate prompt at {id}'
            stems.add(stem)
            # A repeat visit with the same technique and problem role is familiar for
            # progress reporting, even when the figures or story have changed.
            family = f"{src['skill']}:continuation:{'ABCD'[i]}"
            lesson['questions'].append(dict(id=id, family=family, **{k:q[k] for k in ('title','prompt','hint')}))
            question_diagram = private/'figures'/f'{tag}-{"ABCD"[i]}.svg'
            if question_diagram.exists():
                alt = q.get('figureAlt')
                assert alt, id
                public_path = Path('figures/read-practice') / question_diagram.name
                (ROOT/public_path).write_bytes(question_diagram.read_bytes())
                lesson['questions'][-1]['figure']={'src':str(public_path),'alt':alt}
            rows.append(dict(id=id, source_type='original_lesson_practice',
                source_label='Summit One lesson practice: '+tag, category=src['skill'],
                difficulty=(2,3,4,5)[i], title=q['title'], prompt=q['prompt'], answer=q['answer'],
                unit='', solution_text=q['solution'], spoken_script='', rights='original_authored_for_summit_one'))
        lessons.append(lesson)
    write(ROOT/'data/read-watch-practise-later.json', {'edition':EDITION, 'lessons':lessons})
    write(private/'grading.json', rows)
    (private/'fingerprint.txt').write_text(digest(rows)+'\n')
    columns = ', '.join(k+'::text' if k in ('answer','difficulty') else k for k in FIELDS)
    (private/'verify_live.sql').write_text(
        "SELECT count(*) AS question_count, md5(string_agg(md5(concat_ws(chr(31), " + columns +
        ")), '' ORDER BY id)) AS edition_fingerprint FROM public.content_problems WHERE id LIKE 'RWL2-%';")
    retained = sum(len(l['retained']) for l in lessons)
    print(f'{len(lessons)} lessons, {len(rows)} new problems, {retained} retained. Grading fingerprint {digest(rows)}.')


if __name__ == '__main__':
    args = argparse.ArgumentParser(description=__doc__)
    args.add_argument('private', type=Path)
    build(args.parse_args().private)
