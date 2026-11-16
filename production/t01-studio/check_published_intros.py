"""Verify the live Pages movies, chapter links and app module revision."""

from hashlib import sha256
from html.parser import HTMLParser
import json
import re
import sys
import time
from urllib.error import URLError
from urllib.parse import urljoin, urlsplit
from urllib.request import Request, urlopen

from publish_intro_batch import ROOT, VERSION, read_plan, watch_page


class WatchPage(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.links = []
        self.sources = []
        self.chapters = 0
        self.player = False
        self.feed(source)

    def handle_starttag(self, tag, items):
        attrs = dict(items)
        if tag == "a":
            self.links.append(attrs.get("href", ""))
        if tag == "source" and attrs.get("type") == "video/mp4":
            self.sources.append(attrs.get("src"))
        if tag == "button" and "data-time" in attrs:
            self.chapters += 1
        if tag == "video":
            self.player = "controls" in attrs and "playsinline" in attrs


def read(site, path, byte_range=None):
    headers = {"User-Agent": "Summit-One-introduction-check/1.0"}
    if byte_range:
        headers["Range"] = byte_range
    with urlopen(Request(urljoin(site, path), headers=headers), timeout=30) as handle:
        return handle.status, handle.headers.get_content_type(), handle.read()


def check(site):
    lessons = read_plan()["lessons"]
    tag = f"?v={VERSION}"
    root = read(site, "index.html" + tag)[2].decode()
    app = read(site, "app-main.js" + tag)[2].decode()
    menu = read(site, "course-menu-ui.js" + tag)[2].decode()
    if not re.search(r"app-main\.js\?v=lesson-intros-v[0-9]+", root) or "lessonIntroId(s.slot)" not in app or "lesson-introduction-videos.html" not in menu:
        raise ValueError("The revised lesson modules are waiting for deployment")
    published = sorted(path.name[:4] for path in (ROOT / "review").glob("S[0-9][0-9][0-9]-Intro-qa.json"))
    index = WatchPage(read(site, "lesson-introduction-videos.html" + tag)[2].decode())
    if [link for link in index.links if link.startswith("watch-intro-")] != list(map(watch_page, published)):
        raise ValueError("The introduction index does not yet match the release")
    for lesson in lessons:
        position = published.index(lesson)
        name = f"media/{lesson}-Intro"
        page = WatchPage(read(site, watch_page(lesson) + tag)[2].decode())
        if len(page.sources) != 1 or page.chapters != 7 or not page.player:
            raise ValueError(f"{lesson}: watch page has an incomplete player")
        mp4 = page.sources[0]
        media = urlsplit(mp4)
        if media.scheme or media.netloc or media.path != name + ".mp4":
            raise ValueError(f"{lesson}: watch page points to a different movie")
        if position + 1 < len(published) and watch_page(published[position + 1]) not in page.links:
            raise ValueError(f"{lesson}: next lesson link is missing")
        _, mime, payload = read(site, mp4)
        report = json.loads((ROOT / f"review/{lesson}-Intro-qa.json").read_text())
        if mime != "video/mp4" or sha256(payload).hexdigest() != report["sha256"]:
            raise ValueError(f"{lesson}: Published MP4 differs from the verified render")
        status, _, start = read(site, mp4, "bytes=0-1023")
        if status != 206 or start != payload[:1024]:
            raise ValueError(f"{lesson}: HTTP byte range needed for inline playback did not work")
        print(f"{lesson}: watch page, chapters, exact MP4 and inline range playback verified.", flush=True)


if __name__ == "__main__":
    for attempt in range(35):
        try:
            check(sys.argv[1])
            break
        except (URLError, TimeoutError, ValueError) as problem:
            if attempt == 34:
                raise
            print(f"Waiting for Pages — {problem}", flush=True)
            time.sleep(12)
