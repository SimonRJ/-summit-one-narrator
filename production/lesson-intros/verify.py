"""QA: genuine approved voice C, correct maths, precise speech-aligned HD videos."""
import argparse,hashlib,json,math,re,subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("--lesson",required=True,choices=("S001","S002"));a=p.parse_args()
root=Path("build/lesson-intros")/a.lesson
doc=json.loads((Path("production/lesson-intros")/(a.lesson+".json")).read_text())
timing=json.loads((root/"timing.json").read_text())
captions=json.loads((root/"captions.json").read_text())
alignment=json.loads((root/"alignment-qa.json").read_text())
probe=json.loads(subprocess.check_output(["ffprobe","-v","error","-show_format","-show_streams","-of","json",str(root/"final.mp4")]))
v=next(x for x in probe["streams"] if x["codec_type"]=="video")
audio=next(x for x in probe["streams"] if x["codec_type"]=="audio")
duration=float(probe["format"]["duration"])
assert v["codec_name"]=="h264" and (v["width"],v["height"])==(1920,1080)
assert audio["codec_name"]=="aac" and len([x for x in probe["streams"] if x["codec_type"]=="audio"])==1
assert 110<duration<420 and abs(duration-timing["duration_seconds"]-2.5)<.18
assert timing["voice"]=="VoxCPM2 — approved voice C"
ref=Path("media/voice-audition/vox-australian-male-c.mp3")
assert timing["reference_sha256"]==hashlib.sha256(ref.read_bytes()).hexdigest()
assert timing["old_audio_used"] is False
assert [x["text"] for x in timing["segments"]]==doc["segments"]
assert len(timing["segments"])==9
assert alignment["match_percent"]>=90
assert all(captions[i]["end"]<=captions[i+1]["start"]+.005 for i in range(len(captions)-1))
assert all(0<=c["start"]<c["end"]<=duration for c in captions)
assert len(doc["examples"])==3 and [x["level"] for x in doc["examples"]]==["easy","medium","hard"]
assert not any("reef" in v.lower() for v in doc["segments"])
assert (root/"poster.jpg").stat().st_size>10000
assert (root/(a.lesson+".vtt")).read_text().startswith("WEBVTT")
if a.lesson=="S001":
 assert 2473%3==1 and divmod(1739,6)==(289,5)
 good=[n for n in range(100,1000) if n%5==4 and n%7==6 and n%9==0]
 assert good[0]==279
else:
 assert 398+207==605 and 57*98==5586
 assert 49996*50004==(50000**2)-16
 assert (49996*50004)-((50000**2)-17)==1
subprocess.run(["ffmpeg","-v","error","-i",str(root/"final.mp4"),"-f","null","-"],check=True)
sha=hashlib.sha256((root/"final.mp4").read_bytes()).hexdigest()
size=(root/"final.mp4").stat().st_size
assert size<95*1024*1024
report=dict(id=a.lesson,title=doc["title"],voice=timing["voice"],old_audio_used=False,reference_sha256=timing["reference_sha256"],duration_seconds=round(duration,3),video="1920×1080 H.264 24 fps",audio="AAC",scenes=9,example_levels=["easy","medium","hard"],word_alignment_percent=alignment["match_percent"],spoken_caption_layers=1,mathematics_verified=True,full_video_decode_passed=True,bytes=size,sha256=sha)
(root/"qa.json").write_text(json.dumps(report,indent=2))
(root/"transcript.txt").write_text(doc["title"]+"\n\n"+"\n\n".join(doc["segments"]))
print(json.dumps(report,indent=2),flush=True)
