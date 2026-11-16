"""Upload and verify individual films without redeploying the whole application."""

import argparse
import base64
from datetime import datetime, timezone
from functools import lru_cache
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


@lru_cache(maxsize=None)
def lesson_script_sha256(lesson):
    from compile_intros import compile_lesson, lessons

    plan = next(item for item in lessons() if item.id == lesson)
    compile_lesson(plan)
    script_file = ROOT / "production/scripts" / (lesson + ".json")
    return sha256(script_file.read_bytes()).hexdigest()


def current_candidate(lesson):
    try:
        report = asset_entry(lesson)
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError):
        return None
    if (report.get("art_revision") == ART_REVISION
            and report.get("script_sha256") == lesson_script_sha256(lesson)):
        return report
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
    if existing and existing["status"] in {"checking", "verified"}:
        # Keep the bytes stable once a watch page serves this film.
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


def failed_productions():
    run = os.environ.get("GITHUB_RUN_ID")
    attempt = os.environ.get("GITHUB_RUN_ATTEMPT")
    if not run or not attempt:
        return set()
    try:
        jobs = api(f"actions/runs/{run}/attempts/{attempt}/jobs?per_page=100")["jobs"]
    except subprocess.CalledProcessError:
        return set()
    return {
        job["name"].removeprefix("produce (").removesuffix(")")
        for job in jobs
        if job["name"].startswith("produce (") and job["status"] == "completed"
        and job["conclusion"] in {"failure", "cancelled", "timed_out"}
    }


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


def contains_publications(data, reports, status):
    entries = {row["id"]: row for row in data["entries"]}
    allowed = {"checking", "verified"} if status == "checking" else {status}
    return all(entries.get(lesson, {}).get("sha256") == report["sha256"]
               and entries[lesson]["status"] in allowed for lesson, report in reports.items())


def mark(reports, status):
    label = ", ".join(reports)
    for attempt in range(3):
        previous, catalogue = get_catalogue()
        rows = {item["id"]: item for item in catalogue["entries"]}
        for lesson, report in reports.items():
            row = rows.get(lesson, {})
            if row.get("status") == "verified":
                assert row["sha256"] == report["sha256"]
                continue
            rows[lesson] = {
                "id": lesson, "title": report["title"], "seconds": report["seconds"],
                "sha256": report["sha256"], "status": status,
                **({"verified_at": datetime.now(timezone.utc).isoformat()} if status == "verified" else {}),
            }
        new = {"version": 1, "entries": [rows[id] for id in sorted(rows)]}
        if catalogue == new:
            return new
        try:
            put_file(CATALOGUE, new, f"{status.title()} Summit One introductions {label}", previous)
        except subprocess.CalledProcessError:
            if attempt == 2 or get_catalogue()[0] == previous:
                raise
        else:
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


def available_reports(lessons, titles):
    try:
        uploaded = list_uploaded()
    except subprocess.CalledProcessError:
        return {}
    reports = {}
    for lesson in lessons:
        if not set(assets(lesson)) <= uploaded:
            continue
        report = current_candidate(lesson)
        if report:
            verified_report(report, lesson)
            assert report["title"] == titles[lesson]
            reports[lesson] = report
    return reports


def ready_window(lessons, deadline):
    titles = course()
    while True:
        reports = available_reports(lessons, titles)
        if reports:
            return reports
        pending = ", ".join(lessons)
        if time.monotonic() > deadline:
            raise TimeoutError(f"Waiting for these lessons to finish rendering: {pending}")
        if set(lessons) <= failed_productions():
            raise RuntimeError(f"These lessons need another recording or upload attempt: {pending}")
        time.sleep(30)


def prepare_watch_page(lesson, report):
    examine_download(lesson, report)
    detail = "data/lesson-intros/" + lesson + ".json"
    try:
        detail_sha, existing = get_file(detail)
    except subprocess.CalledProcessError:
        detail_sha, existing = None, None
    if existing != report:
        put_file(detail, report, f"Save the chapters and transcript for {lesson}", detail_sha)


def verified_lessons(catalogue):
    return LEGACY | {item["id"] for item in catalogue["entries"] if item["status"] == "verified"}


def report_progress(catalogue):
    titles = course()
    count = len(titles.keys() & verified_lessons(catalogue))
    counts = f"videos complete : {count}\nvideos to go: {len(titles)-count}"
    print(counts, flush=True)
    if "GITHUB_STEP_SUMMARY" in os.environ:
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as stream:
            print(counts + "\n", file=stream)


def publish_reports(reports):
    for lesson, report in reports.items():
        prepare_watch_page(lesson, report)
    mark(reports, "checking")
    wait_for_raw(CATALOGUE, lambda data: contains_publications(data, reports, "checking"))
    for lesson, report in reports.items():
        confirm_player(lesson)
        report_progress(mark({lesson: report}, "verified"))


def publish(lessons, max_wait_minutes):
    deadline = time.monotonic() + max_wait_minutes * 60
    _, catalogue = get_catalogue()
    verified = verified_lessons(catalogue)
    remaining = [lesson for lesson in lessons if lesson not in verified]
    last_window = {}
    while remaining:
        reports = ready_window(remaining, deadline)
        publish_reports(reports)
        remaining = [lesson for lesson in remaining if lesson not in reports]
        last_window = reports
    if last_window:
        wait_for_raw(CATALOGUE, lambda data: contains_publications(data, last_window, "verified"))


def follow_production(run_id, minutes):
    """Publish ready films while the production run uses its render slots."""
    titles = course()
    deadline = time.monotonic() + minutes * 60
    completed_at = None
    while True:
        _, catalogue = get_catalogue()
        remaining = sorted(titles.keys() - verified_lessons(catalogue))
        if not remaining:
            wait_for_raw(CATALOGUE, lambda data: titles.keys() <= verified_lessons(data))
            report_progress(catalogue)
            return False
        if time.monotonic() >= deadline:
            return True
        reports = available_reports(remaining, titles)
        if reports:
            publish_reports(reports)
            continue
        if completed_at is None:
            state = api(f"actions/runs/{run_id}")
            if state["status"] == "completed":
                completed_at = time.monotonic()
        elif time.monotonic() - completed_at >= 7 * 60:
            report_progress(catalogue)
            return False
        time.sleep(30)


def select(max_items):
    from compile_intros import lessons, ready

    _, cat = get_catalogue()
    archived = verified_lessons(cat)
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
    follow = parts.add_parser("follow")
    follow.add_argument("producer_run", type=int)
    follow.add_argument("--minutes", type=int, default=150)
    args = parser.parse_args()
    if args.cmd == "prepare":
        create_release()
    elif args.cmd == "select":
        print(json.dumps(select(args.limit), separators=(",", ":")))
    elif args.cmd == "stage":
        stage(args.lesson)
    elif args.cmd == "publish":
        publish(args.lessons, args.wait_minutes)
    else:
        again = follow_production(args.producer_run, args.minutes)
        with open(os.environ["GITHUB_OUTPUT"], "a") as output:
            print("again=" + ("true" if again else "false"), file=output)
