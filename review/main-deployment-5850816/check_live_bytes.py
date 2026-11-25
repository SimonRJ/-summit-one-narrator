"""Read-only verification of the deployed priority-film source and route declarations.

Run from the repository root after the 5850816 Pages deployment succeeds:
    python review/main-deployment-5850816/check_live_bytes.py

This checks HTTP response bytes and declared mappings. It does not exercise a
learner account, play media, or confer editorial acceptance.
"""

import concurrent.futures
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import urllib.request


ROOT = Path(__file__).resolve().parents[2]
REF = "585081646578fe8b0020d2dee831a8f853eb3bca"
BASE = "https://simonrj.github.io/-summit-one-narrator/"
VERSION = "priority-films-20261125"
PLAIN = [
    "index.html", "sw.js", "lesson-introduction-videos.html",
    "watch-lesson-intro.html", "offline-reader.html",
]
VERSIONED = [
    "app-main.js", "course-menu-ui.js", "lesson-introduction-media.js",
    "lesson-introduction-library.js", "offline-reader.js",
    "data/read-watch-practise.json", "data/read-watch-practise-later.json",
    "data/recorded-studies.json", "data/teaching-72.json",
]
FILMS = {
    "S009": {
        "tag": "carry-reversal-reviewed-20261125-bcbd31159202",
        "sha256": "39d28fec11fe4cc1b1d1b840d01ab8d8b3ae3ccb6d184bf37c1ccf4e37c16ef6",
        "slots": [9, 228],
    },
    "S010": {
        "tag": "carry-reversal-reviewed-20261125-bcbd31159202",
        "sha256": "e8e2e6f697b00cd9401479a603bf6992c2538a107b3fbd519cac0e0b9b7f9a71",
        "slots": [10, 319],
    },
    "S012": {
        "tag": "s012-missing-rung-20261125-b46d28d6d374",
        "sha256": "87e71ca9ae8e3355f9f092f05a7e4c0678313aa569bbc3b4cc63a200ff2cedd7",
        "slots": [12, 248],
    },
}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def check_file(path):
    expected = subprocess.check_output(["git", "show", f"{REF}:{path}"], cwd=ROOT)
    url = BASE + path + (f"?v={VERSION}" if path in VERSIONED else "")
    request = urllib.request.Request(url, headers={
        "Cache-Control": "no-cache", "User-Agent": "AMC-release-byte-audit",
    })
    result = {"path": path, "url": url, "expected_bytes": len(expected),
              "expected_sha256": digest(expected)}
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            actual = response.read()
            result.update(status=response.status, actual_bytes=len(actual),
                          actual_sha256=digest(actual), exact_match=actual == expected,
                          headers={key: response.headers.get(key) for key in
                                   ("ETag", "Last-Modified", "Cache-Control")})
        return result, actual
    except Exception as exc:
        result.update(exact_match=False, error=f"{type(exc).__name__}: {exc}")
        return result, None


def main():
    paths = PLAIN + VERSIONED
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        checked = list(pool.map(check_file, paths))
    responses = {path: data for path, (_, data) in zip(paths, checked)}
    report = {
        "source_commit": REF,
        "checked_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "scope": "Live HTTP bytes and route declarations only; no browser or learner-state action.",
        "files": [row for row, _ in checked],
        "routes": [],
    }
    try:
        catalogue = json.loads(responses["data/recorded-studies.json"])
        lessons = {}
        for path in ("data/read-watch-practise.json", "data/read-watch-practise-later.json"):
            lessons.update({row["slot"]: row for row in json.loads(responses[path])["lessons"]})
        for film, specification in FILMS.items():
            expected_movie = ("https://github.com/SimonRJ/-summit-one-narrator/releases/download/"
                              + specification["tag"] + "/" + film + ".mp4")
            guide = catalogue["lessons"][film]
            guide_movie = (guide.get("release") or catalogue["release"]) + film + ".mp4"
            for slot in specification["slots"]:
                lesson = lessons[slot]
                report["routes"].append({
                    "slot": slot, "film": film, "movie": lesson["movie"],
                    "video_title": lesson["videoTitle"], "bridge": lesson["bridge"],
                    "guide_movie": guide_movie, "guide_movie_sha256": guide["sha256"],
                    "match": lesson["movie"] == expected_movie == guide_movie
                             and guide["sha256"] == specification["sha256"],
                })
    except Exception as exc:
        report["route_error"] = f"{type(exc).__name__}: {exc}"
    report["all_bytes_match"] = all(row["exact_match"] for row, _ in checked)
    report["all_six_routes_match"] = len(report["routes"]) == 6 and all(
        row["match"] for row in report["routes"])
    output = Path(__file__).with_name("live-byte-comparison.json")
    output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"report": str(output), "all_bytes_match": report["all_bytes_match"],
                      "all_six_routes_match": report["all_six_routes_match"]}))
    return 0 if report["all_bytes_match"] and report["all_six_routes_match"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
