"""Package the checked movie chapters and generate both players from their measured recordings."""
from collections import Counter
import hashlib
import html
import itertools
import json
from pathlib import Path
import re
import subprocess

ROOT=Path.cwd()
HERE=Path(__file__).resolve().parent
MEDIA=ROOT/'media'
REVIEW=ROOT/'review'
BUILD=ROOT/'build/amc-introduction'
REV='course-films-20261125'
PYRAMID_CHAPTERS=[(0,'Read the problem'),(23.22,'Choose a maximising strategy'),
                  (29.05,'Trace the position weights'),(34.09,'Place the five numbers'),
                  (39.82,'Test the swap argument'),(43.74,'Add the three middle squares')]
WELCOME_CHAPTERS=[(0,'Welcome'),(1,'How the AMC works'),(2,'Question formats'),(3,'How marks add up'),
                 (4,'Using your time'),(5,'Mathematical topics'),(6,'The last digit of a power'),
                 (7,'Use the remainder'),(8,'Counters in a ratio'),(9,'Rectangles in a grid'),
                 (10,'Work backwards'),(11,'Two-dice probability'),(12,'Odd and even'),
                 (13,'Read the example'),(14,'Watch the diagram'),(15,'Practise on paper'),
                 (16,'Part A and Part B'),(17,'Your first move')]


def digest(path):
    with path.open('rb') as stream: return hashlib.file_digest(stream,'sha256').hexdigest()


def clock(sec):
    return f'{int(sec)//60}:{int(sec)%60:02d}'


def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_chapters','-show_streams','-of','json',str(path)]))


def streams(path):
    return subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-map','0:v:0','-map','0:a:0','-c','copy','-f','streamhash','-hash','sha256','-']).decode().splitlines()


def chapter_movie(path, output, chapters):
    data=probe(path); end=round(float(data['format']['duration'])*1000)
    starts=[round(t*1000) for t,_ in chapters]+[end]
    assert sorted(set(starts))==starts and starts[0]==0
    metadata=BUILD/(path.stem+'-chapters.ffmeta')
    metadata.write_text(';FFMETADATA1\n'+''.join(f'[CHAPTER]\nTIMEBASE=1/1000\nSTART={starts[i]}\nEND={starts[i+1]}\ntitle={title}\n' for i,(_,title) in enumerate(chapters)))
    temp=output.with_suffix('.chaptered.mp4')
    subprocess.run(['ffmpeg','-v','error','-y','-i',str(path),'-i',str(metadata),'-map','0:v:0','-map','0:a:0','-map_metadata','0','-map_chapters','1','-c','copy','-movflags','+faststart',str(temp)],check=True)
    assert streams(path)==streams(temp),'Audio/video changed during chapter packaging'
    probe2=probe(temp)
    assert [round(float(c['start_time'])*1000) for c in probe2['chapters']]==starts[:-1]
    assert [c['tags']['title'] for c in probe2['chapters']]==[t for _,t in chapters]
    subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(temp),'-f','null','-'],check=True)
    temp.replace(output)
    return {'sha256':digest(output),'source_stream_hashes':streams(output),'duration_seconds':float(probe2['format']['duration']),'chapters':[{'start':t,'title':s} for t,s in chapters]}


def nav(chapters,label):
    return f'<nav class="intro-chapters" aria-label="{label}">\n'+''.join(f'  <button type="button" data-time="{t:.3f}"><span>{clock(t)}</span> {html.escape(title)}</button>\n' for t,title in chapters)+'</nav>'


def pyramid():
    movie=MEDIA/'AMC2025Q17-voice-c.mp4'
    assert digest(movie)=='a3e6d7165d8142d562605c5718bb4d3d9fbd9c4918ade776f0f2d010cf4f0fdd'
    rows=list(itertools.permutations(range(1,6)))
    def top(row): return sum(sum(row[k:k+3]) for k in range(3))
    assert all(top(row)==sum(x*w for x,w in zip(row,(1,2,3,2,1))) for row in rows)
    counts=Counter(map(top,rows)); winners=[row for row in rows if top(row)==max(counts)]
    assert winners==[(1,3,5,4,2),(1,4,5,3,2),(2,3,5,4,1),(2,4,5,3,1)]
    assert len(rows)==120 and max(counts)==32 and counts[32]==4
    assert [sum(winners[0][k:k+3]) for k in range(3)]==[9,12,11]
    report=chapter_movie(movie,movie,PYRAMID_CHAPTERS)
    report.update(arrangements_checked=len(rows),maximising_rows=winners,top_counts=dict(sorted(counts.items())),middle_row_for_example=[9,12,11],correct_option='C')
    (REVIEW/'AMC2025Q17-edition.json').write_text(json.dumps(report,indent=2)+'\n')
    file=ROOT/'watch-amc-2025-q17.html';page=file.read_text().replace('v=voice-c-1','v='+REV)
    chip_css='\n'.join(s for s in (ROOT/'welcome.css').read_text().splitlines() if s.startswith('.intro-chapters'))
    page=page.replace('</style>',chip_css+'\n</style>',1)
    page=page.replace('<div class="links">',nav(PYRAMID_CHAPTERS,'Replay the pyramid solution')+'<div class="links">',1)
    question=json.loads((ROOT/'production/amc2025-q17/question.json').read_text())
    transcript=json.loads((ROOT/'production/amc2025-q17/narration.json').read_text())['segments']
    captions=(HERE/'pyramid-captions.vtt').read_text()
    caption_words=' '.join(' '.join(block.splitlines()[1:]) for block in captions.strip().split('\n\n')[1:])
    assert caption_words==' '.join(transcript)
    (MEDIA/'AMC2025Q17-voice-c.vtt').write_text(captions)
    page=page.replace('<details><summary>Read the solution',
            '<details><summary>Read the question and narration</summary><p>'+html.escape(question['question_text'])+'</p><p>'
            +' · '.join(html.escape(q) for q in question['choices'])+'</p>'
            +''.join('<p>'+html.escape(s)+'</p>' for s in transcript[1:])+'</details><details><summary>Read the solution',1)
    page=page.replace('</main></body>', '</main><script defer src="lesson-video-chapters.js?v=chapter-seek-20261122"></script></body>')
    file.write_text(page)


def welcome():
    script=json.loads((HERE/'welcome-script.json').read_text())
    times=json.loads((BUILD/'timing.json').read_text())
    chapters=[(round(times['segments'][i]['start_seconds'],3),title) for i,title in WELCOME_CHAPTERS]
    report=chapter_movie(BUILD/'final.mp4',MEDIA/'AMCIntroduction.mp4',chapters)
    qa=json.loads((BUILD/'qa.json').read_text())
    qa.pop('old_audio_used',None)
    qa.update(other_voice_used=False,sha256=report['sha256'],file_bytes=(MEDIA/'AMCIntroduction.mp4').stat().st_size,chapters=report['chapters'],
              previous_approved_performances_retained=14,revised_approved_performances=4,sources='production/standalone-review/welcome-sources.json')
    (REVIEW/'AMCIntroduction-qa.json').write_text(json.dumps(qa,indent=2)+'\n')
    file=ROOT/'welcome.html'; page=file.read_text().replace('amc-intro-20261113',REV)
    nav_block=nav(chapters,'Jump to a chapter'); page=re.sub(r'<nav class="intro-chapters".*?</nav>',lambda m:nav_block,page,count=1,flags=re.S)
    paragraphs=''.join('<p>'+html.escape(s.replace('A M C','AMC'))+'</p>\n' for s in script['segments'])
    page=re.sub(r'<div class="transcript">.*?</div></details>',lambda m:'<div class="transcript">'+paragraphs+'</div></details>',page,count=1,flags=re.S)
    source=json.loads((HERE/'welcome-sources.json').read_text())['sources'][2]
    page=page.replace('https://imath.com.au/download/AMC/Y5-6/2021%20AMC%20Y5-6.pdf',source['url'])
    page=page.replace('(hosted by iMath)','(2024 bilingual edition)')
    page=page.replace('welcome.js?v=chapter-navigation-20261122','welcome.js?v='+REV)
    file.write_text(page)
    js=ROOT/'welcome.js';js.write_text(js.read_text().replace('amc-intro-20261113',REV))
    tests=ROOT/'tools/welcome-check.mjs'
    s=tests.read_text().replace('assert.equal(await chapters.count(), 5);','assert.equal(await chapters.count(), 18);')
    s=s.replace('v.textTracks[0].mode',"[...v.textTracks].find(track=>track.kind==='captions').mode")
    s=s.replace("document.querySelector('video').textTracks[0].cues","[...document.querySelector('video').textTracks].find(track=>track.kind==='captions')?.cues")
    tests.write_text(s)


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('film',choices=['welcome','pyramid','both'])
    args=parser.parse_args()
    BUILD.mkdir(parents=True,exist_ok=True)
    if args.film in ('pyramid','both'): pyramid()
    if args.film in ('welcome','both'): welcome()
