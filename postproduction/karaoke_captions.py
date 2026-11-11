#!/usr/bin/env python3
import argparse, json, re
from difflib import SequenceMatcher
from pathlib import Path

def norm(s):
    return re.sub(r"[^a-z0-9]+", "", s.lower())

def ass_escape(s):
    return s.replace("\\", r"\\").replace("{", r"\{").replace("}", r"\}")

def ass_time(sec):
    sec=max(0.0,float(sec))
    h=int(sec//3600); sec-=h*3600
    m=int(sec//60); sec-=m*60
    return f"{h}:{m:02d}:{sec:05.2f}"

def find_transcript(obj, video_id):
    if isinstance(obj, dict):
        if obj.get("id")==video_id and obj.get("transcript"):
            return obj["transcript"]
        for v in obj.values():
            r=find_transcript(v, video_id)
            if r:
                return r
    elif isinstance(obj, list):
        for v in obj:
            r=find_transcript(v, video_id)
            if r:
                return r
    return None

def load_transcript(path, video_id):
    data=json.loads(Path(path).read_text(encoding="utf-8"))
    out=find_transcript(data, video_id)
    if not out:
        raise SystemExit(f"Could not find transcript for {video_id}")
    return out.strip()

def tokenize(text):
    return re.findall(r"\S+", text)

def transcribe(audio, prompt, model_name):
    from faster_whisper import WhisperModel
    model=WhisperModel(model_name, device="cpu", compute_type="int8")
    segments, _=model.transcribe(
        audio,
        language="en",
        beam_size=5,
        word_timestamps=True,
        vad_filter=False,
        condition_on_previous_text=True,
        initial_prompt=prompt[:2200],
    )
    words=[]
    for seg in segments:
        for w in (seg.words or []):
            token=w.word.strip()
            if token and w.start is not None and w.end is not None:
                words.append({
                    "text": token,
                    "start": float(w.start),
                    "end": float(w.end),
                    "norm": norm(token),
                })
    return words

def align(transcript_tokens, heard):
    tnorm=[norm(t) for t in transcript_tokens]
    hnorm=[w["norm"] for w in heard]
    sm=SequenceMatcher(a=tnorm,b=hnorm,autojunk=False)
    mapped=[None]*len(transcript_tokens)
    direct=0
    for block in sm.get_matching_blocks():
        for k in range(block.size):
            ti=block.a+k
            hi=block.b+k
            mapped[ti]=(heard[hi]["start"],heard[hi]["end"])
            direct+=1

    aligned_idx=[i for i,x in enumerate(mapped) if x]
    if not aligned_idx:
        raise SystemExit("No transcript words aligned to the audio.")

    # Fill unmatched transcript words between reliable audio anchors.
    for left_pos in range(len(aligned_idx)-1):
        left=aligned_idx[left_pos]
        right=aligned_idx[left_pos+1]
        if right-left <= 1:
            continue
        a=mapped[left][1]
        b=max(a+0.05,mapped[right][0])
        run=list(range(left+1,right))
        weights=[max(1,len(norm(transcript_tokens[j]))) for j in run]
        total=sum(weights)
        cursor=a
        for j,wgt in zip(run,weights):
            dur=(b-a)*(wgt/total)
            mapped[j]=(cursor,cursor+dur)
            cursor+=dur

    first=aligned_idx[0]
    for i in range(first-1,-1,-1):
        dur=max(0.10,0.05*max(1,len(norm(transcript_tokens[i]))))
        end=max(0.0,mapped[i+1][0])
        mapped[i]=(max(0.0,end-dur),end)

    last=aligned_idx[-1]
    for i in range(last+1,len(mapped)):
        dur=max(0.10,0.05*max(1,len(norm(transcript_tokens[i]))))
        start=mapped[i-1][1]
        mapped[i]=(start,start+dur)

    cleaned=[]
    previous_end=0.0
    for tok,pair in zip(transcript_tokens,mapped):
        s,e=pair
        s=max(previous_end,s)
        e=max(s+0.055,e)
        cleaned.append({"text":tok,"start":s,"end":e})
        previous_end=e
    return cleaned,direct

def make_groups(words, max_words=8, max_chars=58):
    groups=[]
    cur=[]
    for w in words:
        projected=" ".join(x["text"] for x in cur+[w])
        if cur and (len(cur)>=max_words or len(projected)>max_chars):
            groups.append(cur)
            cur=[]
        cur.append(w)
        if re.search(r"[.!?]$",w["text"]) and len(cur)>=4:
            groups.append(cur)
            cur=[]
    if cur:
        groups.append(cur)
    return groups

def char_pulse(word, event_start):
    text=word["text"]
    glyphs=[c for c in text if not c.isspace()]
    n=max(1,len(glyphs))
    duration=max(0.09,word["end"]-word["start"])
    slot=duration/n

    # Intentionally overlap neighbouring letters. At normal speech speed,
    # roughly 2-4 letters are thickening/fading at once.
    half=max(0.075,min(0.19,slot*2.35))
    out=[]
    rank=0
    for ch in text:
        if ch.isspace():
            out.append(ch)
            continue
        center=word["start"] + duration*((rank+0.5)/n)
        rise=max(word["start"],center-half)
        peak=max(rise+0.025,center)
        fall=min(word["end"]+0.11,center+half)

        a=max(0,int(round((rise-event_start)*1000)))
        b=max(a+20,int(round((peak-event_start)*1000)))
        c=max(b+30,int(round((fall-event_start)*1000)))

        # A same-colour outline grows then shrinks. This creates a genuinely smooth
        # perceived font-weight transition rather than a binary bold on/off switch.
        out.append(
            r"{\bord0\blur0.22"
            + fr"\t({a},{b},\bord1.45\blur0.02)"
            + fr"\t({b},{c},\bord0\blur0.22)"
            + "}"
            + ass_escape(ch)
        )
        rank+=1
    return "".join(out)

def write_ass(groups, out_path):
    header="""[Script Info]
ScriptType: v4.00+
PlayResX: 1280
PlayResY: 720
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Caption,DejaVu Sans,36,&H00E8EEF4,&H00E8EEF4,&H00E8EEF4,&H00071525,0,0,0,0,100,100,0,0,1,0,0,2,72,72,28,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""
    lines=[header]
    for group in groups:
        event_start=max(0.0,group[0]["start"]-0.14)
        event_end=group[-1]["end"]+0.18
        body=[]
        for i,w in enumerate(group):
            if i:
                body.append(" ")
            body.append(char_pulse(w,event_start))
        lines.append(
            f"Dialogue: 0,{ass_time(event_start)},{ass_time(event_end)},"
            f"Caption,,0,0,0,,{''.join(body)}\n"
        )
    Path(out_path).write_text("".join(lines),encoding="utf-8")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--audio",required=True)
    ap.add_argument("--transcript-json",required=True)
    ap.add_argument("--video-id",default="T01.2")
    ap.add_argument("--ass-out",required=True)
    ap.add_argument("--qa-out",required=True)
    ap.add_argument("--model",default="base.en")
    args=ap.parse_args()

    transcript=load_transcript(args.transcript_json,args.video_id)
    transcript_tokens=tokenize(transcript)
    heard=transcribe(args.audio,transcript,args.model)
    aligned,direct=align(transcript_tokens,heard)

    ratio=direct/max(1,len(transcript_tokens))
    if ratio < 0.80:
        raise SystemExit(f"Alignment quality too low: {ratio:.3f}")

    groups=make_groups(aligned)
    write_ass(groups,args.ass_out)

    qa={
        "video_id":args.video_id,
        "alignment_source":"finished bm_george 0.88 audio",
        "alignment_model":args.model,
        "transcript_words":len(transcript_tokens),
        "recognized_words":len(heard),
        "direct_word_matches":direct,
        "direct_match_ratio":round(ratio,4),
        "qa_note":"Unmatched display tokens are interpolated only between neighbouring recognized speech anchors.",
        "caption_groups":len(groups),
        "first_word":aligned[0],
        "last_word":aligned[-1],
        "highlight_style":"smooth overlapping per-letter weight pulse; no hard word switch"
    }
    Path(args.qa_out).write_text(json.dumps(qa,indent=2),encoding="utf-8")
    print(json.dumps(qa,indent=2))

if __name__=="__main__":
    main()
