"""Prepare one immutable illustrated edition and its catalogue row after its editorial review."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from datetime import datetime,timezone
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
from urllib.request import Request,urlopen

from PIL import Image
from prepare import RAW, RELEASE, REGISTER, MANIFEST, digest, file_name, head, lesson_id, need, read_remote, sequential_scope, write_files


def public_digest(asset,sha):
    req=Request(RELEASE+asset+'?reviewed_sha='+sha,headers={'User-Agent':'Summit-One-video-review'})
    with urlopen(req,timeout=90) as resp:
        need(resp.status==200,'Release asset missing: '+asset)
        found=hashlib.file_digest(resp,'sha256').hexdigest()
    need(found==sha,'Staged release has different bytes: '+asset)


def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))


def audio_hash(path):
    return subprocess.check_output(['ffmpeg','-nostdin','-v','error','-i',str(path),'-map','0:a:0','-c:a','copy','-f','hash','-hash','sha256','-'],text=True).strip()


def preserved(source,qa,original,movie,seconds):
    need(digest(original)==source['sha256']==qa['legacy_sha256'] and original.resolve()!=movie.resolve(),'Different baseline for retained narration')
    packet_hash=audio_hash(movie)
    need(re.fullmatch(r'SHA256=[0-9a-f]{64}',packet_hash) and packet_hash==audio_hash(original)==qa['audio_packets'],'Audio packets differ from original')
    need(abs(seconds-source['duration_seconds'])<.06 and qa['frames']==qa['caption_frames_checked'] and qa['caption_peak_mean_luma']<=3.5,'Original duration or caption frame mismatch')
    details=deepcopy(source)
    details['audio_packet_hash']=packet_hash.partition('=')[2]
    return details


def revoiced(source,qa,script_path,recording,seconds):
    script=json.loads(script_path.read_text()); clock=json.loads((recording/'timeline.json').read_text())
    need(script['id']==clock['id']==source['id'] and 'voice c' in script['voice'].lower(),'Different recording or script')
    need(clock['narration_reference']==source['reference_sha256'] and clock['model_revision']==source['model_revision'],'Narration source changed')
    need(abs(clock['duration']-seconds)<.06 and qa['minimum_scene_audio_correlation']>.985 and qa['caption_peak_mean_luma']<=4,'Timeline or spoken recording mismatch')
    scenes=clock['scenes']; need(len(scenes)==len(script['scenes'])==11 and clock['mean_match_percent']>=90,'Recorded scene structure differs')
    for i,(s,w) in enumerate(zip(script['scenes'],scenes),1):
        need(s['n']==w['n']==i and s['narration'].split()==[t['text'] for t in w['words']],'Script and recording word alignment differ')
        need(w['match_percent']>=80 and w['start']<=w['speech_end']<=w['end']<=seconds+.06,'Invalid scene timing')
        need(w['start']==0 if i==1 else w['start']>=scenes[i-2]['speech_end'],'Scene overlap')
    need(sum(len(s['words']) for s in scenes)==qa['spoken_words_checked'],'Incomplete spoken word review')
    details=deepcopy(source);details.update(title=script['title'],match_percent=clock['mean_match_percent'],script_sha256=digest(script_path),
           transcript=[s['narration'] for s in script['scenes']],scenes=[{'number':s['n'],'start':s['start'],'match_percent':s['match_percent']} for s in scenes])
    for i,chapter in zip((1,2,3,5,7,10,11),details['chapters'],strict=True):chapter['start']=scenes[i-1]['start']
    return details


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('lesson',type=lesson_id)
    p.add_argument('--movie',type=Path,required=True);p.add_argument('--poster',type=Path,required=True)
    p.add_argument('--timeline',type=Path,required=True,help='Final delivery check, generated against the encoded movie')
    p.add_argument('--edition',choices=[1,2],type=int,required=True);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--expected-catalog',required=True,help='Current checked catalog SHA to lease')
    source_group=p.add_mutually_exclusive_group(required=True)
    source_group.add_argument('--original',type=Path,help='Existing movie with unchanged recording and caption track')
    source_group.add_argument('--recording',type=Path,help='New measured recording folder with timeline.json')
    p.add_argument('--script',type=Path,help='Exact script that produced new recording')
    p.add_argument('--chapter-titles',type=Path,help='Optional JSON array of seven individual chapter titles')
    a=p.parse_args();lesson=a.lesson;lease=a.expected_catalog
    need(bool(a.recording)==bool(a.script),'Specify --script only for a new recording')
    need(head('lesson-intro-catalog')==lease,'Concurrent catalog update; refresh lease before preparing')
    baseline=head('main');sequential_scope(read_remote(RAW+baseline+'/'+REGISTER),lesson)
    origin=RAW+lease+'/'
    catalog=json.loads(read_remote(origin+MANIFEST));updated=deepcopy(catalog)
    row,=[r for r in updated['entries'] if r['id']==lesson]
    need(row.get('status')=='verified','Original catalogue entry unavailable')
    previous=row['sha256'];current_edition=row.get('illustratedRevision',1) if row.get('illustration') else 0
    need(a.edition>current_edition,'Selected publicly active media would be overwritten')
    source=json.loads(read_remote(origin+f'data/lesson-intros/{lesson}.json'))
    need(source['id']==lesson and source['sha256']==row.get('legacy_sha256',previous),'Baseline origin changed')
    qa=json.loads(a.timeline.read_text());movie_sha=digest(a.movie);poster_sha=digest(a.poster)
    need(qa['id']==lesson and qa['sha256']==movie_sha and movie_sha!=previous,'Incorrect reviewed delivery')
    stats=probe(a.movie);video,audio=stats['streams'];seconds=float(stats['format']['duration']);frames=int(video['nb_frames'])
    need((video['codec_name'],video['width'],video['height'],Fraction(video['avg_frame_rate']),audio['codec_name'])==('h264',1920,1080,30,'aac'),'Incorrect delivery streams')
    need(abs(seconds-float(audio['duration']))<.1 and abs(seconds-frames/30)<.06,'Incomplete audio or video duration')
    need(qa['caption_frames_checked']==frames and qa['drawing_interval_seconds']==.5 and qa['drawings_checked']==math.ceil(frames/15),'Insufficient coverage of encoded frames')
    need(qa['picture_peak_mean_rgb']<=5 and qa['picture_peak_tile_rgb']<=18,'Drawing comparison failed')
    with Image.open(a.poster) as poster:
        need(poster.format=='JPEG' and poster.size==(1920,1080),'Poster dimensions disagree with video');poster.verify()
    details=(preserved(source,qa,a.original,a.movie,seconds) if a.original else revoiced(source,qa,a.script,a.recording,seconds))
    if a.chapter_titles:
        titles=json.loads(a.chapter_titles.read_text());need(isinstance(titles,list) and len(titles)==7 and all(isinstance(t,str) and t.strip() for t in titles),'Supply seven chapter titles')
        for chapter,title in zip(details['chapters'],titles,strict=True):chapter['title']=title
    need(len(details['chapters'])==7 and len(details['scenes'])==len(details['transcript'])==11 and details['chapters'][0]['start']==0,'Incomplete lesson details')
    need([c['start'] for c in details['chapters']]==[details['scenes'][i-1]['start'] for i in (1,2,3,5,7,10,11)],'Unmatched chapter timings')
    details.update(seconds=seconds,duration_seconds=seconds,sha256=movie_sha,art_revision=3,legacy_sha256=previous,illustrated_revision=a.edition)
    asset=file_name(lesson,a.edition);poster_asset=asset[:-4]+'-poster.jpg'
    with ThreadPoolExecutor(max_workers=2) as ex:
        for task in [ex.submit(public_digest,asset,movie_sha), ex.submit(public_digest,poster_asset,poster_sha)]:task.result()
    row.update(sha256=movie_sha,legacy_sha256=source['sha256'],seconds=seconds,title=details['title'],illustration=1,detailsEdition=1,illustrated_at=datetime.now(timezone.utc).isoformat())
    if a.edition==2:row['illustratedRevision']=2
    if current_edition:row['previous_illustrated_sha256']=previous
    need([x['id'] for x,y in zip(catalog['entries'],updated['entries'],strict=True) if x!=y]==[lesson],'Unexpected catalog scope')
    need(head('lesson-intro-catalog')==lease and head('main')==baseline,'Remote refs changed during preparation; retry against current snapshot')
    values={MANIFEST:updated,f'data/lesson-intros/{lesson}-Illustrated.json':details}
    write_files(a.output,{key:json.dumps(value,ensure_ascii=False,separators=(',',':'))+'\n' for key,value in values.items()},lease,'catalog')
    print(json.dumps({'id':lesson,'lease':lease,'files':list(values),'sha256':movie_sha,'poster_sha256':poster_sha,'seconds':seconds}))


if __name__=='__main__':main()
