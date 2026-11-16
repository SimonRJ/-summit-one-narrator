"""Switch a lesson to its verified illustrated asset after checking the public upload."""
import argparse
import base64
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import time
from urllib.request import Request, urlopen

from render import HERE, MOVIES, RELEASE, REPOSITORY


BRANCH = "lesson-intro-catalog"
CATALOGUE = "data/lesson-intros-live.json"


def gh(*args, payload=None):
    return subprocess.check_output(
        ["gh", *args], text=True, input=json.dumps(payload) if payload is not None else None,
    )


def api(path, payload=None):
    cmd = ["api", f"repos/{REPOSITORY}/{path}"]
    if payload is not None:
        cmd.extend(("--method", "PUT", "--input", "-"))
    return json.loads(gh(*cmd,payload=payload))


def get_catalogue():
    item = api(f"contents/{CATALOGUE}?ref={BRANCH}")
    return item["sha"], json.loads(base64.b64decode(item["content"]))


def fetch(name, head=False):
    headers={"User-Agent":"Summit-One-illustrated-publication"}
    if head:
        headers["Range"]="bytes=0-1023"
    request=Request(RELEASE+name+"?v="+str(int(time.time()//30)),headers=headers)
    with urlopen(request,timeout=35) as response:
        return response.status,response.read()


def check_upload(filename, digest):
    def read():
        status,data=fetch(filename)
        assert status==200 and sha256(data).hexdigest()==digest,f"{filename}: checksum mismatch"
        if filename.endswith(".mp4"):
            ranged,opening=fetch(filename,head=True)
            assert ranged==206 and opening==data[:1024],f"{filename}: byte seeking unavailable"

    for attempt in range(5):
        try:
            read()
        except (OSError,AssertionError):
            if attempt==4:
                raise
            time.sleep(12)
        else:
            return


def publish(id, out):
    timeline=json.loads((HERE/f"{id}.json").read_text())
    report=json.loads((out/f"{id}-qa.json").read_text())
    _,catalogue=get_catalogue()
    row=next(item for item in catalogue["entries"] if item["id"]==id)
    assert row["status"]=="verified" and row["seconds"]==report["seconds"]
    assert row.get("legacy_sha256",row["sha256"])==timeline["legacy_sha256"]
    movie=out/f"{id}-Intro-Illustrated.mp4"
    poster=out/f"{id}-Intro-Illustrated-poster.jpg"
    assert report["sha256"]==sha256(movie.read_bytes()).hexdigest()
    assets=json.loads(gh("release","view","lesson-introductions","--repo",REPOSITORY,"--json","assets"))["assets"]
    present={item["name"] for item in assets}
    for src in (movie,poster):
        if src.name not in present:
            gh("release","upload","lesson-introductions",str(src),"--repo",REPOSITORY)
        check_upload(src.name,sha256(src.read_bytes()).hexdigest())

    # Jobs can finish together. The content API rejects a concurrent change to the branch.
    for attempt in range(8):
        previous,catalogue=get_catalogue()
        row=next(item for item in catalogue["entries"] if item["id"]==id)
        if row.get("illustration")==1:
            assert row["sha256"]==report["sha256"]
            return
        assert row["sha256"]==timeline["legacy_sha256"]
        row.update(sha256=report["sha256"], legacy_sha256=timeline["legacy_sha256"], illustration=1,
                   illustrated_at=datetime.now(timezone.utc).isoformat())
        content=json.dumps(catalogue,ensure_ascii=False,separators=(",",":"))+"\n"
        try:
            api(f"contents/{CATALOGUE}",{
                "branch":BRANCH,"sha":previous,"message":f"Publish the illustrated Lesson {int(id[1:])} introduction",
                "content":base64.b64encode(content.encode()).decode(),
            })
        except subprocess.CalledProcessError:
            if attempt==7:
                raise
            time.sleep(3)
        else:
            print(f"{id}: illustrated release and HTTP range playback verified",flush=True)
            return


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("lesson",choices=MOVIES)
    parser.add_argument("--out",type=Path,required=True)
    args=parser.parse_args()
    publish(args.lesson,args.out)
