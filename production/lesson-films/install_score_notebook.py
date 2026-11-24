"""Build the score-notebook review package with the two approved recordings."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "production/t01-studio"))
from publish import make_watch_page, TEACHING_SEQUENCE

LESSON = "T16.3"
KEYS = ("T16.3-four-values", "T16.3-median-recap")


def install(render, voices, output):
    out = lambda p: output / p
    for directory in ("media", "review", "production/scripts/src", "production/t01-studio", "production/lesson-films/voice-c-repairs"):
        out(directory).mkdir(exist_ok=True, parents=True)
    measured = json.loads((render / "measured.json").read_text())
    qa_file = Path("review/T16.3-studio-qa.json")
    qa = json.loads((ROOT / qa_file).read_text())
    assert measured["source_sha256"] == qa["sha256"] and measured["version"] == "score-notebook"
    media = render / (LESSON + ".mp4")
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-xerror", "-i", str(media), "-f", "null", "-"], check=True)
    assert hashlib.file_digest(media.open("rb"), "sha256").hexdigest() == measured["sha256"]
    starts = measured["scene_starts"]
    assert len(starts) == len(qa["scenes"]) == len(qa["chapters"]) == 8
    for index, start in enumerate(starts):
        qa["scenes"][index]["start"] = start
        qa["chapters"][index]["start"] = start
    qa["chapters"][6]["title"] = "Find the median with one or two middle positions"
    qa.update({k: measured[k] for k in ("sha256","source_sha256","duration_seconds","frames","version")})
    qa.update(diagram_source="production/lesson-films/score_notebook.py",
              spoken_edit="Two Voice C passages now work through the odd and even cases. The original notebook challenge follows the new summary.",
              corrected_passages_matched_before_encoding=True)
    qa.pop("match_percent",None)
    for scene in qa["scenes"]:
        scene.pop("match_percent",None)
    stream = subprocess.check_output(["ffmpeg","-v","error","-i",str(media),"-map","0:a","-c:a","copy","-f","hash","-hash","sha256","-"],text=True).strip()
    qa["audio_packet_sha256"] = stream
    out(qa_file).write_text(json.dumps(qa, indent=2) + "\n")
    for item in (media, render / "T16.3.vtt", render / "T16.3-studio-poster.jpg"):
        shutil.copyfile(item, out("media")/item.name)
    for key in KEYS:
        for extension in (".wav", ".json"):
            name = key + extension
            shutil.copyfile(voices / name, out("production/lesson-films/voice-c-repairs") / name)
    requests = {r["id"]:r["text"] for r in json.loads((ROOT/"production/lesson-films/voice-c-repairs/requests.json").read_text())}
    source_path = Path("production/scripts/T16.3.json")
    text_path = Path("production/scripts/src/chapters-15-18.txt")
    source = json.loads((ROOT/source_path).read_text())
    original = (ROOT/text_path).read_text()
    for i, key, visual in [(6, KEYS[0], "Five score cards are sorted. Remove the five, bracket the two middle cards, then average three and nine."), (7, KEYS[1], "Open the score notebook to the odd and even rules. Recover the missing score from the two totals.")]:
        scene = source["scenes"][i]
        notebook = re.search(r" Notebook challenge:.*",scene["narration"])
        new = requests[key] + (notebook.group() if notebook else "")
        for field, value in (("visual",visual),("narration",new)):
            old = scene[field]
            assert original.count(old) == 1
            original = original.replace(old, value)
            scene[field] = value
    words = sum(len(s["narration"].split()) for s in source["scenes"])
    source.update(narration_words=words,estimated_minutes=round(words/150,1))
    out(text_path).write_text(original)
    out(source_path).write_text(json.dumps(source, ensure_ascii=False, indent=1) + "\n")
    import publish
    publish.REVISED_MEDIA[LESSON] = measured["version"]
    out("watch-t16-3.html").write_text(make_watch_page(LESSON, source, qa, available=TEACHING_SEQUENCE))
    # Keep future static-site builds on the measured edition as well.
    generator = Path("production/t01-studio/publish.py")
    text = (ROOT/generator).read_text()
    anchor = 'REVISED_MEDIA = {\n'
    assert text.count(anchor) == 1
    out(generator).write_text(text.replace(anchor,anchor+'    "T16.3": "score-notebook",\n'))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("render","voices","output"):
        parser.add_argument(name,type=Path)
    args = parser.parse_args()
    install(args.render,args.voices,args.output)
