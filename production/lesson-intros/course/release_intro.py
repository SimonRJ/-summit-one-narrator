"""Upload and verify individual films without redeploying the whole application."""

import argparse
import base64
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[3]
REPO = "SimonRJ/-summit-one-narrator"
SITE = "https://simonrj.github.io/-summit-one-narrator/"
TAG = "lesson-introductions"
BRANCH = "lesson-intro-catalog"
CATALOGUE = "data/lesson-intros-live.json"
LEGACY = {f"S{slot:03}" for slot in range(1, 7)}
VOICE_C = "0f3304a393ee504e9fa22537267ac03f150569a5fab0859616f261d009513362"
ART_REVISION = 2
ASSET_ROOT = f"https://github.com/{REPO}/releases/download/{TAG}/"
RAW_ROOT = f"https://raw.githubusercontent.com/{REPO}/refs/heads/{BRANCH}/"


def course():
    data = json.loads((ROOT / "data/sessions-372.json").read_text())
    return {f"S{row['slot']:03}": row["focus"] for row in data["sessions"] if row["type"] == "LESSON"}


def assets(lesson):
    assert re.fullmatch(r"S[0-9]{3}", lesson)
    prefix = lesson + "-Intro"
    return prefix + ".mp4", prefix + "-poster.jpg", prefix + ".json"


def api(path, payload=None):
    cmd = ["gh", "api", "repos/" + REPO + "/" + path]
    if payload is not None:
        cmd += ["--method", "PUT", "--input", "-"]
    return json.loads(subprocess.check_output(
        cmd, text=True, input=json.dumps(payload) if payload is not None else None,
    ))


def get_file(path):
    result = api(f"contents/{path}?ref={BRANCH}")
    return result["sha"], json.loads(base64.b64decode(result["content"]))


def put_file(path, obj, message, previous=None):
    text = json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "\n"
    data = {"branch": BRANCH, "message": message, "content": base64.b64encode(text.encode()).decode()}
    if previous:
        data["sha"] = previous
    return api(f"contents/{path}", data)


def get_catalogue():
    previous, data = get_file(CATALOGUE)
    assert data["version"] == 1 and isinstance(data["entries"], list)
    return previous, data


def catalogue_url():
    return RAW_ROOT + CATALOGUE + "?v=" + str(int(time.time() // 20))


def public(url, byte_range=None):
    headers = {"User-Agent": "Summit-One-introduction-release"}
    if byte_range:
        headers["Range"] = byte_range
    with urlopen(Request(url, headers=headers), timeout=28) as response:
        return response.status, response.headers.get_content_type(), response.read()


def asset_entry(lesson):
    return json.loads(public(ASSET_ROOT + assets(lesson)[2])[2])


def current_candidate(lesson):
    try:
        report = asset_entry(lesson)
        if report.get("art_revision") == ART_REVISION:
            return report
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError):
        pass
    return None


def verified_report(report, lesson):
    assert report["id"] == lesson and report["decoded_successfully"]
    assert report["reference_sha256"] == VOICE_C and report["narration_speed_changed"] is False
    assert report["audio_streams"] == 1 and report["caption_layers"] == 1
    assert (report["width"], report["height"], report["fps"]) == (1920, 1080, 30)
    assert len(report["chapters"]) == 7 and report["match_percent"] >= 90


def list_uploaded():
    raw = subprocess.check_output(
        ["gh", "release", "view", TAG, "--repo", REPO, "--json", "assets"], text=True,
    )
    return {entry["name"] for entry in json.loads(raw)["assets"]}


def create_release():
    if subprocess.run(["gh", "release", "view", TAG, "--repo", REPO], stdout=subprocess.DEVNULL).returncode:
        subprocess.run(["gh", "release", "create", TAG, "--repo", REPO, "--target", "main",
                        "--title", "Summit One lesson introductions", "--latest=false",
                        "--notes", "Narrated introduction videos for Summit One lessons."], check=True)


def stage(lesson):
    folder = ROOT / "build/t01-studio" / lesson
    report = json.loads((folder / "qa.json").read_text())
    script_file = ROOT / "production/scripts" / (lesson + ".json")
    script = json.loads(script_file.read_text())
    assert script["title"] == course()[lesson]
    verified_report(report, lesson)
    movie, poster, metadata = assets(lesson)
    assert sha256((folder / "final.mp4").read_bytes()).hexdigest() == report["sha256"]
    sha, catalogue = get_catalogue()
    existing = next((item for item in catalogue["entries"] if item["id"] == lesson), None)
    if existing and existing["status"] == "verified":
        # A retry must never replace the public bytes of an already verified film.
        return
    prepared = {
        **report, "title": script["title"], "seconds": report["duration_seconds"],
        "art_revision": ART_REVISION,
        "script_sha256": sha256(script_file.read_bytes()).hexdigest(),
        "transcript": [item["narration"] for item in script["scenes"]],
    }
    for here, dest in (("final.mp4", movie), ("poster.jpg", poster)):
        shutil.copyfile(folder / here, folder / dest)
    (folder / metadata).write_text(json.dumps(prepared, ensure_ascii=False) + "\n")
    # Publish metadata last so it can serve as a ready marker for the complete upload.
    for name in (movie, poster, metadata):
        command = ["gh", "release", "upload", TAG, str(folder / name), "--repo", REPO, "--clobber"]
        for attempt in range(3):
            uploaded = subprocess.run(command)
            if uploaded.returncode == 0:
                break
            if attempt == 2:
                uploaded.check_returncode()
            time.sleep(12 * (attempt + 1))


def failed_production(lesson):
    run = os.environ.get("GITHUB_RUN_ID")
    attempt = os.environ.get("GITHUB_RUN_ATTEMPT")
    if not run or not attempt:
        return False
    try:
        jobs = api(f"actions/runs/{run}/attempts/{attempt}/jobs?per_page=100")["jobs"]
    except subprocess.CalledProcessError:
        return False
    return any(job["name"] == f"produce ({lesson})" and job["status"] == "completed"
               and job["conclusion"] in {"failure", "cancelled", "timed_out"} for job in jobs)


def wait_for_candidate(lesson, deadline):
    while True:
        report = current_candidate(lesson)
        if report:
            verified_report(report, lesson)
            assert report["title"] == course()[lesson]
            return report
        if time.monotonic() > deadline:
            raise TimeoutError(f"Waiting for {lesson} to finish rendering")
        if failed_production(lesson):
            raise RuntimeError(f"{lesson} needs another recording or upload attempt")
        time.sleep(30)


def examine_download(lesson, report):
    movie, poster, _ = assets(lesson)
    code, mime, payload = public(ASSET_ROOT + movie)
    assert code == 200 and mime in ("video/mp4", "application/octet-stream")
    assert sha256(payload).hexdigest() == report["sha256"]
    code, _, start = public(ASSET_ROOT + movie, "bytes=0-1023")
    assert code == 206 and start == payload[:1024], f"{lesson}: HTTPS seeking failed"
    code, _, image = public(ASSET_ROOT + poster)
    assert code == 200 and image[:2] == b"\xff\xd8" and len(image) > 1000


def read_raw(path):
    return json.loads(public(RAW_ROOT + path + "?v=" + str(int(time.time() // 20)))[2])


def wait_for_raw(path, condition):
    for _ in range(36):
        try:
            if condition(read_raw(path)):
                return
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError):
            pass
        time.sleep(12)
    raise TimeoutError("The live catalogue has not caught up")


def mark(lesson, report, status):
    previous, catalogue = get_catalogue()
    rows = {item["id"]: item for item in catalogue["entries"]}
    row = rows.get(lesson, {})
    if row.get("status") == "verified":
        assert row["sha256"] == report["sha256"]
        return catalogue
    updated = {
        "id": lesson, "title": report["title"], "seconds": report["seconds"],
        "sha256": report["sha256"], "status": status,
    }
    if status == "verified":
        updated["verified_at"] = datetime.now(timezone.utc).isoformat()
    rows[lesson] = updated
    new = {"version": 1, "entries": [rows[id] for id in sorted(rows)]}
    if row != updated:
        put_file(CATALOGUE, new, f"{status.title()} Summit One introduction {lesson}", previous)
    wait_for_raw(CATALOGUE, lambda data: any(
        item["id"] == lesson and item["sha256"] == report["sha256"] and item["status"] == status
        for item in data["entries"]
    ))
    return new


def confirm_player(lesson):
    command = ["node", str(ROOT / "tools/check_live_intro_player.mjs"), lesson]
    deadline = time.monotonic() + 8 * 60
    while True:
        result = subprocess.run(command)
        if result.returncode == 0:
            return
        if time.monotonic() >= deadline:
            result.check_returncode()
        time.sleep(25)


def publish(lessons, max_wait_minutes):
    deadline = time.monotonic() + max_wait_minutes * 60
    for lesson in lessons:
        _, current = get_catalogue()
        if any(item["id"] == lesson and item["status"] == "verified" for item in current["entries"]):
            continue
        report = wait_for_candidate(lesson, deadline)
        examine_download(lesson, report)
        detail = "data/lesson-intros/" + lesson + ".json"
        try:
            detail_sha, existing = get_file(detail)
        except subprocess.CalledProcessError:
            detail_sha, existing = None, None
        if existing != report:
            put_file(detail, report, f"Save the chapters and transcript for {lesson}", detail_sha)
        wait_for_raw(detail, lambda data: data["sha256"] == report["sha256"])
        mark(lesson, report, "checking")
        confirm_player(lesson)
        final = mark(lesson, report, "verified")
        count = len(LEGACY) + sum(item["status"] == "verified" for item in final["entries"])
        counts = f"videos complete : {count}\nvideos to go: {len(course())-count}"
        print(counts, flush=True)
        if "GITHUB_STEP_SUMMARY" in os.environ:
            with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as stream:
                print(counts + "\n", file=stream)


def select(max_items):
    from compile_intros import lessons, ready

    _, cat = get_catalogue()
    archived = LEGACY | {item["id"] for item in cat["entries"] if item["status"] == "verified"}
    selected = []
    for lesson in lessons():
        if lesson.id in archived:
            continue
        if not ready(lesson):
            break
        selected.append(lesson.id)
        if len(selected) == max_items:
            break
    return selected


def missing_candidates(lessons):
    uploaded = list_uploaded()
    return [lesson for lesson in lessons
            if not set(assets(lesson)) <= uploaded or not current_candidate(lesson)]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parts = parser.add_subparsers(dest="cmd", required=True)
    parts.add_parser("prepare")
    choose = parts.add_parser("select")
    choose.add_argument("limit", type=int)
    upload = parts.add_parser("stage")
    upload.add_argument("lesson")
    check = parts.add_parser("publish")
    check.add_argument("lessons", nargs="+")
    check.add_argument("--wait-minutes", type=int, default=290)
    args = parser.parse_args()
    if args.cmd == "prepare":
        create_release()
    elif args.cmd == "select":
        print(json.dumps(select(args.limit), separators=(",", ":")))
    elif args.cmd == "stage":
        stage(args.lesson)
    else:
        publish(args.lessons, args.wait_minutes)
