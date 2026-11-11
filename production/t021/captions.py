#!/usr/bin/env python3
"""Clean, single-layer speech captions for T02.1.
Word positions are aligned to the generated narration (faster-whisper), while the
on-screen text always comes from the approved written narration—not ASR guesses.
One ASS dialogue is visible at any instant: no doubled subtitles.
"""
import argparse, difflib, json, math, re
from pathlib import Path

def wordnorm(s):return re.sub(r'[^a-z0-9]','',s.lower())
def tim(t):
    h=int(t//3600);m=int(t//60)%60;s=t%60
    return f'{h:02d}:{m:02d}:{s:06.3f}'
def ast(t):
    h=int(t//3600);m=int(t//60)%60;s=t%60
    return f'{h}:{m:02d}:{s:05.2f}'
def ass_esc(s):return s.replace('\\','\\\\').replace('{','\\{').replace('}','\\}')

def make_base_words(data):
    words=[]
    for seg in data['segments']:
        tokens=seg['text'].split()
        length=[max(1,len(wordnorm(w))**.7) + (.55 if w.endswith(('.', '?','!')) else 0) for w in tokens]
        total=sum(length)
        unit=seg['duration_seconds']/total
        t=seg['start_seconds']
        for w,n in zip(tokens,length):
            dur=n*unit
            words.append({'text':w,'start':t,'end':t+dur,'segment':seg['index']})
            t+=dur
    return words

def align(words,audio):
    try:
        from faster_whisper import WhisperModel
        model=WhisperModel('base.en',device='cpu',compute_type='int8',cpu_threads=2)
        pieces,meta=model.transcribe(audio,beam_size=2,word_timestamps=True,vad_filter=False,condition_on_previous_text=False)
        heard=[]
        for seg in pieces:
            for w in seg.words or []:
                if wordnorm(w.word):heard.append({'text':w.word.strip(),'start':float(w.start),'end':float(w.end)})
        target=[wordnorm(w['text']) for w in words]
        recognized=[wordnorm(w['text']) for w in heard]
        sm=difflib.SequenceMatcher(None,target,recognized,autojunk=False)
        matched=0
        for tag,i0,i1,j0,j1 in sm.get_opcodes():
            if tag!='equal':continue
            for i,j in zip(range(i0,i1),range(j0,j1)):
                # Avoid moving a valid segment's timestamp outside its synthesis window.
                if abs(words[i]['start']-heard[j]['start'])<2.7:
                    words[i]['start']=heard[j]['start'];words[i]['end']=heard[j]['end'];words[i]['aligned']=True;matched+=1
        # Reposition unaligned tokens evenly between adjacent matched anchors within segment.
        byseg={}
        for i,w in enumerate(words):byseg.setdefault(w['segment'],[]).append(i)
        for inds in byseg.values():
            for pos,idx in enumerate(inds):
                if words[idx].get('aligned'):continue
                left=next((j for j in reversed(inds[:pos]) if words[j].get('aligned')),None)
                right=next((j for j in inds[pos+1:] if words[j].get('aligned')),None)
                if left is not None and right is not None:
                    dist=right-left; r=(idx-left)/dist
                    nextstart=words[left]['end']+(words[right]['start']-words[left]['end'])*r
                    words[idx]['start']=nextstart
                    words[idx]['end']=min(words[right]['start'],nextstart+.15)
        return {'method':'faster-whisper base.en + transcript alignment','recognized_words':len(heard),'matched_original_words':matched,'match_percent':round(100*matched/max(1,len(words)),1)}
    except Exception as e:
        return {'method':'speech-segment-duration fallback','error':str(e),'matched_original_words':0,'match_percent':0}

def phrase_groups(words):
    # Make sentence-aware, breath-length captions; don't strand articles at
    # line ends and don't force children to read two unrelated sentences at once.
    groups=[];cur=[];currentseg=None
    unhelpful_end={'a','an','the','to','in','with','from','and','or','of','for','but','is'}
    for i,w in enumerate(words):
        maybe=' '.join(words[k]['text'] for k in cur+[i])
        if cur and (w['segment']!=currentseg or len(maybe)>55 or len(cur)>=10):
            carry=[]
            if w['segment']==currentseg and len(cur)>2 and wordnorm(words[cur[-1]]['text']) in unhelpful_end:
                carry=[cur.pop()]
            if cur:groups.append(cur)
            cur=carry
        cur.append(i);currentseg=w['segment']
        if len(cur)>=3 and w['text'].endswith(('.', '?', '!')):
            groups.append(cur);cur=[]
    if cur:groups.append(cur)
    return groups

def make_ass(words,groups,out):
    # Semi-transparent base text with one brighter, softly scaled spoken word.
    ass='''[Script Info]
Title: T02.1 single speech-aligned caption track
ScriptType: v4.00+
PlayResX: 1280
PlayResY: 720
ScaledBorderAndShadow: yes
WrapStyle: 2
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Base,Inter,30,&H00CCDBE7,&H00CCDBE7,&H00112233,&H00112233,0,0,0,0,100,100,0,0,1,1.5,0,2,50,50,29,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
    for g in groups:
        begin=words[g[0]]['start']
        end=words[g[-1]]['end']
        # Keep text visible to phrase end; but never let it overlap the next phrase.
        follow_index=g[-1]+1
        if follow_index<len(words):end=min(end+.06,words[follow_index]['start'])
        for k,idx in enumerate(g):
            w=words[idx]
            st=max(begin,w['start']); en=words[g[k+1]]['start'] if k+1<len(g) else end
            en=max(st+.06,min(en,end))
            # Only one caption event renders at once. Highlight the active original word,
            # without a second subtitle track or overlapping duplicate lettering.
            parts=[]
            for wi in g:
                txt=ass_esc(words[wi]['text'])
                if wi==idx:
                    parts.append('{\\b1\\1c&H00FFFFFF&\\fscx100\\fscy100\\t(0,85,\\fscx105\\fscy105)\\t(130,280,\\fscx100\\fscy100)}'+txt+'{\\rBase}')
                else:parts.append(txt)
            phrase=' '.join(parts)
            ass+=f'Dialogue: 0,{ast(st)},{ast(en)},Base,,0,0,0,,{phrase}\n'
    Path(out).write_text(ass,encoding='utf-8')

def make_vtt(words,groups,out):
    outtext='WEBVTT\n\n'
    for g in groups:
        st=words[g[0]]['start'];end=words[g[-1]]['end']
        outtext+=f'{tim(st)} --> {tim(end)}\n'+ ' '.join(words[i]['text'] for i in g)+'\n\n'
    Path(out).write_text(outtext,encoding='utf-8')

def main():
    p=argparse.ArgumentParser()
    for name in ['timing','audio','ass','vtt','qa']:p.add_argument('--'+name,required=True)
    p.add_argument('--words',default=None)
    a=p.parse_args();data=json.load(open(a.timing))
    words=make_base_words(data)
    qa=align(words,a.audio)
    if a.words:
        Path(a.words).write_text(json.dumps({'video_id':data['id'],'audio_locked':True,'words':words,'alignment':qa},indent=2),encoding='utf-8')
    groups=phrase_groups(words)
    make_ass(words,groups,a.ass);make_vtt(words,groups,a.vtt)
    qa.update({'caption_events':len(words),'caption_groups':len(groups),'single_layer':True,'burned_in_original_subtitles':False,'voice':data['voice'],'speed':data['speed']})
    Path(a.qa).write_text(json.dumps(qa,indent=2))
    print(json.dumps(qa,indent=2))
if __name__=='__main__':main()