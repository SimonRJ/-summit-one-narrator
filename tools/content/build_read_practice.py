"""Rebuild the answer-free course edition and its private, insert-only grading rows.

  python tools/content/build_read_practice.py PRIVATE_EDITION_DIRECTORY
See docs/READ_WATCH_PRACTISE.md. The private directory contains drafts/ and sources/.
No answer key or worked solution for a scored question is written inside the repo.
"""
import argparse, hashlib, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EDITION = 'read-watch-practise-1'
# The original bank and attempts are immutable. These IDs no longer form part of
# this edition's route: a different technique, a near-copy of the film, or a
# different application better left for a later lesson.
OMIT = set('O005X O010T O011X O018X O019T O019X O033T O036T O036X O038X O045T O045X O046X O054T O059T O059X O060T O066X'.split())
def read(p): return json.loads(p.read_text())
def write(p,data): p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def build(private):
    private=private.resolve()
    revisions=read(ROOT/'tools/content/practice-revisions-20261121.json')['questions']
    if private.is_relative_to(ROOT): raise ValueError('The private answer source must be outside the public repository')
    course=read(ROOT/'data/sessions-372.json')['sessions']
    targets=[s['slot'] for s in course if s['type']=='LESSON' and s['slot']<=68]
    assert len(targets)==55 and sorted(int(f.stem[1:]) for f in (private/'drafts').glob('S*.json'))==targets
    old={q['id']:q for q in read(ROOT/'data/lesson-challenges.json')['items']}
    figures=read(ROOT/'figures/read-practice/openings.json')
    opening_revisions=read(ROOT/'tools/content/practice-revisions-20261121.json')['openings']
    public=[]; grading=[]; stems=set()
    for n in targets:
        key=f'S{n:03}'; src=read(private/'sources'/f'{key}.json'); d=read(private/'drafts'/f'{key}.json')
        assert src['id']==key and d['slot']==n and len(d['questions'])==4
        assert d['intro'] and d['bridge'] and d['recap'] and d['example']['steps']
        retained=[f'O{n:03}{s}' for s in 'TX' if f'O{n:03}{s}' not in OMIT]
        assert all(old[k]['session']==n for k in retained)
        lesson={k:d[k] for k in ('slot','headline','intro','example','bridge','recap')}
        revised=opening_revisions.get(key,{})
        lesson['example']={**lesson['example'],**revised.get('example',{})}
        for field in ('headline', 'intro', 'bridge', 'recap'):
            if field in revised:
                lesson[field] = revised[field]
        if key in figures: lesson['example']={**lesson['example'],'figure':figures[key]}
        lesson.update(skill=src['skill'],videoId=key,videoTitle=src['videoTitle'],movie=src['videoUrl'],retained=retained,questions=[])
        for i,q in enumerate(d['questions']):
            pid=f'RWL1-{n:03}-{"ABCD"[i]}'
            q={**q, **revisions.get(pid, {})}
            stem=re.sub(r'\W','',q['prompt']).casefold()
            assert stem not in stems and q['hint'] and q['solution'] and q['answer'] is not None, pid
            stems.add(stem)
            lesson['questions'].append(dict(id=pid,**{k:q[k] for k in ('title','prompt','hint')}))
            grading.append(dict(id=pid,source_type='original_lesson_practice',source_label='Summit One lesson practice: '+key,category=src['skill'],difficulty=(2,3,4,5)[i],title=q['title'],prompt=q['prompt'],answer=q['answer'],unit='',solution_text=q['solution'],spoken_script='',rights='original_authored_for_summit_one'))
        public.append(lesson)
    assert len(grading)==220 and OMIT <= old.keys()
    write(ROOT/'data/read-watch-practise.json',dict(edition=EDITION,lessons=public))
    write(private/'grading.json',grading)
    # Stable, portable parity check against the protected and public fields in production.
    fields=('id','source_type','source_label','category','difficulty','title','prompt','answer','unit','solution_text','spoken_script','rights')
    def value(row,k): return json.dumps(row[k],ensure_ascii=False,separators=(',',':')) if k=='answer' else str(row[k])
    digest=hashlib.md5(''.join(hashlib.md5(chr(31).join(value(r,k) for k in fields).encode()).hexdigest() for r in grading).encode()).hexdigest()
    colsql=', '.join(k+'::text' if k in ('answer','difficulty') else k for k in fields)
    (private/'verify_live.sql').write_text(f"SELECT count(*) AS question_count, md5(string_agg(md5(concat_ws(chr(31), {colsql})), '' ORDER BY id)) AS edition_fingerprint FROM public.content_problems WHERE id LIKE 'RWL1-%';")
    (private/'fingerprint.txt').write_text(digest+'\n')
    print(f'{len(public)} lessons, {len(grading)} new questions, {sum(len(l["retained"]) for l in public)} retained. Fingerprint: {digest}')
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('private',type=Path); build(p.parse_args().private)
