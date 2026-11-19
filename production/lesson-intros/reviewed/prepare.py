"""Prepare one reviewed introduction's register and watch list against live, immutable Git snapshots."""
import argparse
import csv
import hashlib
import html
import io
import json
from pathlib import Path
import re
import subprocess
from urllib.request import Request, urlopen

REPO = 'SimonRJ/-summit-one-narrator'
RAW = f'https://raw.githubusercontent.com/{REPO}/'
SITE = 'https://simonrj.github.io/-summit-one-narrator/'
RELEASE = f'https://github.com/{REPO}/releases/download/lesson-introductions/'
COMPLETE = 'final editorial review complete'
REGISTER = 'docs/lesson-introduction-review-register-20261116.csv'
LIST = 'lesson-video-review-list.html'
MANIFEST = 'data/lesson-intros-live.json'
ORIENTATIONS = {(e,o) for e in ('chrome','webkit') for o in ('portrait','landscape')}


def need(ok,reason):
    if not ok:
        raise ValueError(reason)


def lesson_id(value):
    if not re.fullmatch(r'S[0-9]{3}',value):
        raise argparse.ArgumentTypeError('Supply one lesson ID such as S067')
    return value


def watch_url(lesson):
    return SITE + f'watch-lesson-intro.html?slot={int(lesson[1:])}'


def read_remote(url):
    req = Request(url,headers={'User-Agent':'Summit-One-video-review'})
    with urlopen(req,timeout=60) as response:
        return response.read().decode('utf-8')


def head(branch):
    ref = 'refs/heads/' + branch
    result = subprocess.check_output(['git','ls-remote','--exit-code',f'https://github.com/{REPO}.git',ref],text=True,timeout=50)
    sha,resolved = result.strip().split()
    need(resolved==ref and re.fullmatch(r'[0-9a-f]{40}',sha), 'Unexpected Git reference')
    return sha


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream,'sha256').hexdigest()


def replace_once(text,old,new):
    need(text.count(old)==1, 'Changed source context: '+old[:100])
    return text.replace(old,new,1)


def sequential_scope(text,lesson):
    rows = list(csv.DictReader(io.StringIO(text)))
    ids = [r['id'] for r in rows]
    completed = {r['id'] for r in rows if r['individual_review']==COMPLETE}
    need(len(ids)==len(set(ids)) and ids==sorted(ids), 'Unexpected introduction register order')
    next_id = next((i for i in ids if i not in completed),None)
    need(lesson==next_id, f'Expected {next_id} as the single active introduction, received {lesson}')
    return rows,completed


def file_name(lesson,edition):
    need(edition in (1,2),'Unsupported player edition')
    return f'{lesson}-Intro-Illustrated' + ('-v2' if edition==2 else '') + '.mp4'


def read_phone(directory,lesson,asset,checksum,seconds,byte_count):
    source_url = RELEASE + asset
    checks = set()
    streamed = set()
    for path in directory.rglob(lesson+'-*.json'):
        r = json.loads(path.read_text()); need(r['id']==lesson,'Different film in current phone reports')
        for name in ['source','courseSource'] if 'orientation' in r else ['source']:
            need(r[name].split('?')[0]==source_url,'Wrong release media in phone player')
        if path.name.endswith('-public-digest.json'):
            engine = path.name.split('-')[1]
            need(r['sha256']==checksum and r['bytes']==byte_count and r['asset']==asset and engine not in streamed,'Streamed public bytes differ or repeat')
            streamed.add(engine)
        else:
            pair = (r['engine'],r['orientation'])
            need(pair in ORIENTATIONS and pair not in checks,'Invalid phone result')
            need(r['page'].split('&')[0]==watch_url(lesson) and r['method']=='chapter button' and not r['error'] and not r['overflow'],'Wrong watch page or failed chapter control')
            need(0 < r['target'] < r['time'] < r['target']+10 and abs(r['seconds']-seconds)<.2,'Playback did not resume at chapter')
            checks.add(pair)
    need(checks==ORIENTATIONS and streamed=={'chrome','webkit'},'Missing public mobile playback evidence')


def update_register(text,lesson,details,note):
    rows,completed = sequential_scope(text,lesson)
    row = next(r for r in rows if r['id']==lesson)
    old = next(line for line in text.splitlines() if line.startswith(lesson+','))
    row.update(title=details['title'],availability='verified',individual_review=COMPLETE,narration_source=details.get('narration',row['narration_source']),observation=note)
    out = io.StringIO(newline=''); csv.DictWriter(out,fieldnames=list(row),lineterminator='\n').writerow(row)
    result = replace_once(text,old+'\n',out.getvalue())
    need(list(csv.DictReader(io.StringIO(result)))==rows,'Register updates differ from selected row')
    return result,completed,len(rows)


def update_watch_list(text,lesson,details,completed,total):
    tag = '<section aria-labelledby="revised-lesson-introductions">'
    prefix,section=text.split(tag); section,suffix=section.split('</section>',1)
    old_ids = re.findall(r'<th scope="row">(S\d{3})</th>',section)
    need(sorted(completed)==old_ids,'Watch list differs from completion register')
    seconds=round(details['seconds']); n=len(completed)
    row=(f'<tr><th scope="row">{lesson}</th><td><a href="{watch_url(lesson)}">{html.escape(details["title"])}</a>'
         f'</td><td>{seconds//60}:{seconds%60:02d}</td></tr>')
    after = next((x for x in old_ids if x>lesson),None)
    anchor = f'<tr><th scope="row">{after}</th>' if after else '</tbody>'
    section=replace_once(section,anchor,row+'\n'+anchor)
    section=replace_once(section,f'{n} of {total} lesson introductions', f'{n+1} of {total} lesson introductions')
    prefix=replace_once(prefix,f'>{n} lesson introductions</a>',f'>{n+1} lesson introductions</a>')
    return prefix+tag+section+'</section>'+suffix


def write_files(output,files,lease,branch):
    for name,body in files.items():
        path=output/'files'/name
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(body)
    (output/('expected-'+branch+'.txt')).write_text(lease+'\n')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('lesson',type=lesson_id)
    parser.add_argument('--timeline',type=Path,required=True,help='Final encoded-timeline report')
    parser.add_argument('--movie',type=Path,required=True)
    parser.add_argument('--phone-root',type=Path,required=True)
    parser.add_argument('--notes',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args(); lesson=args.lesson
    baseline=head('main'); catalog=head('lesson-intro-catalog')
    source=RAW+baseline+'/'; media=RAW+catalog+'/'
    entry,=[row for row in json.loads(read_remote(media+MANIFEST))['entries'] if row['id']==lesson]
    need((entry.get('status'),entry.get('illustration'),entry.get('detailsEdition'))==('verified',1,1),'Current illustrated edition is not live')
    details=json.loads(read_remote(media+f'data/lesson-intros/{lesson}-Illustrated.json'))
    qa=json.loads(args.timeline.read_text()); checksum=digest(args.movie); duration=details['seconds']
    need(qa['id']==details['id']==lesson and checksum==qa['sha256']==details['sha256']==entry['sha256'],'Public edition, reviewed movie and final report differ')
    need(len(details['scenes'])==11 and abs(qa['caption_frames_checked']-duration*details['fps'])<2 and abs(qa['drawings_checked']*qa['drawing_interval_seconds']-duration)<=qa['drawing_interval_seconds'],'Incomplete timeline review')
    asset=file_name(lesson,entry.get('illustratedRevision',1))
    read_phone(args.phone_root,lesson,asset,checksum,duration,args.movie.stat().st_size)
    note=args.notes.read_text().strip();need(note and '\n' not in note,'Provide an individual editorial observation paragraph')
    note += f' Full review covered all {len(details["scenes"])} scenes. The revised public player resumed after a chapter seek in Chrome and WebKit in portrait and landscape. Reviewed file: {asset}, SHA-256 {checksum}.'
    register,completed,total=update_register(read_remote(source+REGISTER),lesson,details,note)
    watch=update_watch_list(read_remote(source+LIST),lesson,details,completed,total)
    need(head('main')==baseline and head('lesson-intro-catalog')==catalog,'Remote state changed during preparation; retry')
    write_files(args.output,{REGISTER:register,LIST:watch},baseline,'main')
    print(f'{lesson}: {len(completed)+1} complete, {total-len(completed)-1} to go. Main lease {baseline}')


if __name__=='__main__':
    main()
