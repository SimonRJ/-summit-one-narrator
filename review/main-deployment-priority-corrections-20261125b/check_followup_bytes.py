"""Check only 14 b-batch HTTP resources; retain the verified other 52 offline.

Prepare with --plan-only after the final source is frozen. Live mode additionally
requires the exact deployment SHA and successful Pages run supplied by the owner.
No movies, posters, font files, browser sessions or learner endpoints are fetched.
"""
import argparse
import concurrent.futures
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
BASE = "https://simonrj.github.io/-summit-one-narrator/"
RELEASE_BASE = "https://github.com/SimonRJ/-summit-one-narrator/releases/download/"
FIRST_SOURCE = "d51e1382373a03aa0a3a828cfffa0a2a6c6a0198"
FIRST_PREPARED_SOURCE = "e287b9102574b8a6cbc29beba97ccc9a7dc569fe"
VERSION = "priority-corrections-20261125b"
PLAIN = ["index.html", "sw.js", "lesson-introduction-videos.html", "watch-lesson-intro.html", "offline-reader.html"]
VERSIONED = ["app-main.js", "course-menu-ui.js", "lesson-introduction-media.js",
             "lesson-introduction-library.js", "offline-reader.js", "data/read-watch-practise.json",
             "data/read-watch-practise-later.json", "data/recorded-studies.json", "data/teaching-72.json"]
TAG_FOUR = "stable-captions-20261125-2cde68c0f046"
FILMS = {
    "S009": (TAG_FOUR, "999aba1a891fffeafe82e3c3b9e537d0b261a0332d507e967a199890f0a3d123", (9,228)),
    "S010": (TAG_FOUR, "5369c10e51e6ac79a925d04566ebe6780735de2069fb10f20d6242b4137a1a8a", (10,319)),
    "S012": (TAG_FOUR, "d36d6c733066f0e27d195e0268548cc0c8c3ce68bfd0cfac7348ac8529be2dd6", (12,248)),
    "S015": ("s015-numeral-timing-20261125-41b7922d37ed", "19765de3ce9c28259d244c41d370cb3073513bc928124167e58cc21497098c89", (15,260)),
    "S017": (TAG_FOUR, "7a2493a89821faca46c686fed5d4d003b27e6a4fe5779670202b6ae3ff5edfe4", (17,300)),
    "S019": ("s019-stable-captions-20261125-ac244dec7136", "5455c0c0119bedd897ddda6feb41002cf215575c8f8839565661674c42ad712c", (19,333)),
    "S020": ("s020-stable-captions-20261125-0dfec081086f", "5308674d7d66dee6545d05699311a192b13e2fce2d48b6d2f560ec35ce1e57f3", (20,283)),
    "S102": ("s102-tens-units-20261125-a84046b06450", "f08e10363f675d7cb9e46fd31e5f766fdbbacd248af3ddded95b2a06eb40f6e1", (102,296)),
}


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT,
                                   env={**os.environ, "GIT_NO_LAZY_FETCH":"1"})


def source(commit, path):
    return git("show", commit+":"+path)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def rows_from(files):
    rows=[]
    for path in ("data/read-watch-practise.json", "data/read-watch-practise-later.json"):
        rows.extend(json.loads(files[path])["lessons"])
    assert len({r["slot"] for r in rows})==len(rows), "Duplicate declared lesson slot"
    return {r["slot"]:r for r in rows}


def declarations(files, previous_rows):
    catalogue=json.loads(files["data/recorded-studies.json"])
    lessons=rows_from(files)
    routes=[]
    for film,(tag,pin,slots) in FILMS.items():
        guide=catalogue["lessons"][film]
        movie=RELEASE_BASE+tag+"/"+film+".mp4"
        declared_slots=sorted(slot for slot,row in lessons.items() if row["videoId"]==film)
        for slot in slots:
            row=lessons[slot]
            canonical=slot==int(film[1:])
            checks={"exact_two_slots":declared_slots==list(slots), "film_identity":row["videoId"]==film,
                    "movie_and_catalogue":row["movie"]==(guide.get("release") or catalogue["release"])+film+".mp4"==movie,
                    "guide_sha256":guide["sha256"]==pin, "title":row["videoTitle"]==guide["title"],
                    "film_use":row["filmUse"]==("dedicated" if canonical else "technique"),
                    "bridge_preserved":bool(row["bridge"]) and row["bridge"]==previous_rows[slot]["bridge"],
                    "canonical_bridge":not canonical or row["bridge"]==guide["bridge"]}
            if film=="S102":
                checks["corrected_digit_swap"]="153 becomes 135" in row["bridge"] and "incorrect here" not in row["bridge"]
            routes.append(dict(slot=slot,film=film,role="canonical" if canonical else "consumer",
                               movie=row["movie"],guide_sha256=guide["sha256"],bridge=row["bridge"],checks=checks,
                               passed=all(checks.values())))
    required={
        "index.html":["app-main.js?v="+VERSION],
        "sw.js":["summit-one-"+VERSION]+[path+"?v="+VERSION for path in VERSIONED],
        "lesson-introduction-videos.html":["lesson-introduction-library.js?v="+VERSION],
        "watch-lesson-intro.html":["lesson-introduction-library.js?v="+VERSION],
        "offline-reader.html":["offline-reader.js?v="+VERSION],
        "app-main.js":["course-menu-ui.js?v="+VERSION,"lesson-introduction-media.js?v="+VERSION,
                       "data/read-watch-practise.json?v="+VERSION,"data/read-watch-practise-later.json?v="+VERSION,
                       "data/teaching-72.json?v="+VERSION],
        "course-menu-ui.js":["lesson-introduction-media.js?v="+VERSION],
        "lesson-introduction-library.js":["lesson-introduction-media.js?v="+VERSION],
        "lesson-introduction-media.js":["data/recorded-studies.json?v="+VERSION],
        "offline-reader.js":["data/read-watch-practise.json?v="+VERSION,"data/read-watch-practise-later.json?v="+VERSION],
    }
    references=[dict(path=path,missing=[text for text in strings if text not in files[path].decode()])
                for path,strings in required.items()]
    return dict(routes=routes,cache_references=references,
                passed=len(routes)==16 and all(r["passed"] for r in routes) and not any(r["missing"] for r in references))


def prepare(commit):
    assert re.fullmatch("[0-9a-f]{40}",commit)
    baseline=json.loads(Path(__file__).with_name("baseline-resources.json").read_text())
    assert baseline["passed"] and baseline["source_commit"]==FIRST_PREPARED_SOURCE and len(baseline["resources"])==66
    assert baseline["deployment_commit"]==FIRST_SOURCE
    assert git("rev-parse",FIRST_SOURCE+"^{tree}").decode().strip()==baseline["source_tree"]
    retained=[r for r in baseline["resources"] if r["category"]!="app"]
    assert len(retained)==52
    comparisons=[]
    for row in retained:
        old=git("rev-parse",FIRST_SOURCE+":"+row["path"]).decode().strip()
        new=git("rev-parse",commit+":"+row["path"]).decode().strip()
        comparisons.append(dict(path=row["path"],url=row["url"],first_source_blob=old,
                                followup_blob=new,match=old==new==row["first_source_blob_sha"],
                                prior_public_sha256=row["expected_sha256"],http_repeated=False))
    assert all(r["match"] for r in comparisons), "Previously verified resource changed; do not reuse its old delivery result"
    files={path:source(commit,path) for path in PLAIN+VERSIONED}
    prior=rows_from({path:source(FIRST_SOURCE,path) for path in
                    ("data/read-watch-practise.json","data/read-watch-practise-later.json")})
    manifest=[dict(path=path,url=BASE+path+("?v="+VERSION if path in VERSIONED else ""),
                   bytes=len(data),sha256=sha(data)) for path,data in files.items()]
    assert len(manifest)==14 and len({r["url"] for r in manifest})==14
    local=declarations(files,prior)
    assert local["passed"], "Frozen source declarations fail the expected mappings or cache references"
    return manifest,files,prior,comparisons,local


def fetch(entry,expected):
    result=dict(entry)
    request=urllib.request.Request(entry["url"],headers={"User-Agent":"AMC-public-followup-byte-verification"},method="GET")
    try:
        with urllib.request.urlopen(request,timeout=45) as response:
            data=response.read()
            result.update(status=response.status,final_url=response.geturl(),actual_bytes=len(data),
                          actual_sha256=sha(data),match=response.status==200 and data==expected,
                          headers={k:response.headers.get(k) for k in ("ETag","Last-Modified","Cache-Control","Content-Type")})
        return result,data
    except Exception as error:
        result.update(match=False,error=type(error).__name__+": "+str(error))
        return result,None


def main():
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--source-commit",required=True)
    cli.add_argument("--output",required=True,type=Path)
    cli.add_argument("--plan-only",action="store_true")
    cli.add_argument("--deployment-commit")
    cli.add_argument("--pages-run",type=int)
    args=cli.parse_args()
    if args.output.exists():cli.error("Preserve previous observations; choose a new output path")
    if not args.plan_only and (not re.fullmatch("[0-9a-f]{40}",args.deployment_commit or "") or not args.pages_run):
        cli.error("Live mode requires the deployment SHA and successful Pages run supplied by the owner")
    manifest,expected,prior,comparisons,local=prepare(args.source_commit)
    report=dict(source_commit=args.source_commit,source_tree=git("rev-parse",args.source_commit+"^{tree}").decode().strip(),
                first_source=FIRST_SOURCE,deployment_commit=args.deployment_commit,pages_run=args.pages_run,
                checked_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),version=VERSION,
                offline_reuse=comparisons,offline_52_match=True,source_declarations=local,
                repeated_media_or_font_downloads=False,learner_operations=False,editorial_credit=False)
    if args.plan_only:
        report.update(mode="offline-plan",http_requests=0,files=manifest,passed=True)
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            checked=list(pool.map(lambda row:fetch(row,expected[row["path"]]),manifest))
        responses={entry["path"]:data for entry,(_,data) in zip(manifest,checked)}
        try:
            live_declarations=declarations(responses,prior) if all(data is not None for data in responses.values()) else dict(passed=False,error="A required response was unavailable")
        except Exception as error:
            live_declarations=dict(passed=False,error=type(error).__name__+": "+str(error))
        report.update(mode="live-public-get",http_requests=14,files=[row for row,_ in checked],declarations=live_declarations,
                      passed=all(row["match"] for row,_ in checked) and live_declarations["passed"])
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open("x") as stream:stream.write(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(dict(output=str(args.output),mode=report["mode"],passed=report["passed"],
                          http_requests=report["http_requests"],offline_resource_entries=52,declared_mappings=16)))
    return 0 if report["passed"] else 1


if __name__=="__main__":
    raise SystemExit(main())
