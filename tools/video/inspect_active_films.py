"""Decode each distinct lesson MP4 and save a labelled frame from every chapter for editorial review."""
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import tempfile
from collections import defaultdict
from pathlib import Path
from urllib.request import urlopen

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
SITE = 'https://simonrj.github.io/-summit-one-narrator/'
LEGACY = 'https://github.com/SimonRJ/-summit-one-narrator/releases/download/lesson-introductions/'


def read(path):
    return json.loads(path.read_text())


def editions(catalogue):
    data = ROOT / 'data'
    remote = {e['id']: e for e in read(catalogue / 'lesson-intros-live.json')['entries']}
    recorded = read(data / 'recorded-studies.json')
    assigned = defaultdict(list)
    for name in ('read-watch-practise', 'read-watch-practise-later'):
        for lesson in read(data / (name + '.json'))['lessons']:
            assigned[lesson['videoId']].append(lesson)
    for identifier, lessons in sorted(assigned.items()):
        if identifier in recorded['lessons']:
            guide = recorded['lessons'][identifier]
            url = (guide.get('release') or recorded['release']) + identifier + '.mp4'
            duration, chapters, digest = guide['seconds'], guide['chapters'], guide.get('sha256')
        elif int(identifier[1:]) <= 6:
            page = (ROOT / ('watch-intro-' + identifier.lower() + '.html')).read_text()
            chapter_times = re.findall(r'data-time="([0-9.]+)"[^>]*>([^<]+)', page)
            chapters = [dict(start=float(t), title=label.strip()) for t, label in chapter_times]
            qa = read(ROOT / 'review' / (identifier + '-Intro-qa.json'))
            duration, digest = qa['duration_seconds'], qa['sha256']
            url = SITE + 'media/' + identifier + '-Intro.mp4'
        else:
            entry = remote[identifier]
            assert entry['status'] == 'verified', identifier
            edition = '-Illustrated-v2' if entry.get('illustration') == 2 or entry.get('illustratedRevision') == 2 else '-Illustrated' if entry.get('illustration') == 1 else ''
            suffix = '-Illustrated' if entry.get('detailsEdition') == 1 else ''
            guide = read(catalogue / 'lesson-intros' / (identifier + suffix + '.json'))
            duration, digest, chapters = entry['seconds'], entry['sha256'], guide['chapters']
            url = LEGACY + identifier + '-Intro' + edition + '.mp4'
        assigned_urls = {l['movie'] for l in lessons if l.get('filmUse')}
        assert not assigned_urls or assigned_urls == {url}, (identifier, assigned_urls)
        assert chapters and len(chapters) >= 2, identifier
        yield identifier, url, digest, duration, chapters, [l['slot'] for l in lessons]


def inspect(item, out, tmp):
    identifier, url, expected, seconds, chapters, slots = item
    movie = tmp / (identifier + '.mp4')
    subprocess.run(['curl', '--fail', '--location', '--retry', '3', '--silent', '--show-error',
                    '--max-time', '180', '-o', str(movie), url], check=True)
    with movie.open('rb') as f:
        digest = hashlib.file_digest(f, 'sha256').hexdigest()
    probe = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_streams',
                    '-show_format', '-of', 'json', str(movie)]))
    streams = probe['streams']
    video = next(s for s in streams if s['codec_type'] == 'video')
    duration = float(probe['format']['duration'])
    assert video['codec_name'] == 'h264' and sum(s['codec_type'] == 'audio' for s in streams) == 1
    assert abs(duration - seconds) < 0.35, (duration, seconds)
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-xerror', '-threads', '2',
                    '-i', str(movie), '-map', '0:v:0', '-map', '0:a:0', '-f', 'null', '-'], check=True)
    cols, w, h = 3, 360, 202
    sheet = Image.new('RGB', (cols*w, ((len(chapters)+cols-1)//cols)*(h+26)), '#f2f1ed')
    draw = ImageDraw.Draw(sheet)
    for i, chapter in enumerate(chapters):
        start = chapter['start']
        end = chapters[i+1]['start'] if i+1 < len(chapters) else duration
        assert 0 <= start < end <= duration + .01, chapter
        sample = start + .65*(end-start)
        frame = tmp / 'sample.jpg'
        subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-ss', f'{sample:.3f}', '-i',
                        str(movie), '-frames:v', '1', '-vf', f'scale={w}:{h}:force_original_aspect_ratio=decrease',
                        str(frame)], check=True)
        x, y = (i%cols)*w, (i//cols)*(h+26)
        with Image.open(frame) as im:
            sheet.paste(im, (x+(w-im.width)//2, y))
        draw.text((x+4, y+h+3), f"{identifier}  {sample:.1f}s   {chapter['title'][:42]}", fill='black')
    sheet.save(out / (identifier+'.jpg'), quality=83)
    movie.unlink()
    return dict(id=identifier, seconds=duration, slots=slots, chapters=len(chapters), sha256=digest,
                expected_sha256=expected, matches_register=(digest==expected) if expected else None)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--catalogue',type=Path,required=True)
    p.add_argument('--shard',type=int,required=True)
    p.add_argument('--shards',type=int,default=8)
    p.add_argument('--out',type=Path,required=True)
    args=p.parse_args()
    args.out.mkdir(parents=True,exist_ok=True)
    selected=list(editions(args.catalogue))[args.shard::args.shards]
    rows=[]
    with tempfile.TemporaryDirectory() as temp:
        for item in selected:
            try:
                row=inspect(item,args.out,Path(temp))
            except Exception as error:
                row=dict(id=item[0],error=str(error))
            rows.append(row)
            print(row['id'], row.get('error') or 'decoded', flush=True)
            (args.out/'results.json').write_text(json.dumps(rows,indent=2)+'\n')
    if any('error' in row or row.get('matches_register') is False for row in rows):
        raise SystemExit('See the film-specific results and frame sheets.')


if __name__ == '__main__':
    main()
