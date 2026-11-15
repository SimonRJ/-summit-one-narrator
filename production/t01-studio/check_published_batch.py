"""Verify the live index, watch routes and exact MP4 delivered by GitHub Pages."""

import argparse
import hashlib
from html.parser import HTMLParser
import json
import time
from urllib.error import URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen

from publish import COURSE_VERSION, ROOT, TEACHING_SEQUENCE, watch_path


class Page(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.links = []
        self.sources = []
        self.chapter_buttons = 0
        self.inline_player = False
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a" and "href" in attrs:
            self.links.append(attrs["href"])
        if tag == "source" and attrs.get("type") == "video/mp4":
            self.sources.append(attrs.get("src"))
        if tag == "video" and "controls" in attrs and "playsinline" in attrs:
            self.inline_player = True
        if tag == "button" and "data-time" in attrs:
            self.chapter_buttons += 1


def read_live(site, path):
    request = Request(urljoin(site, path), headers={"User-Agent": "Summit-One-release-check/1.0"})
    with urlopen(request, timeout=30) as response:
        return response.headers.get_content_type(), response.read()


def check(site, plan):
    expected_count = 16 + min(56, plan["batch"] * 5)
    revision = f"?batch={plan['batch']}"
    html = Page(read_live(site, "teaching-videos.html" + revision)[1].decode())
    expected = [watch_path(lesson) for lesson in TEACHING_SEQUENCE[:expected_count]]
    found = [href for href in html.links if href.startswith("watch-")]
    if found != expected:
        raise ValueError(f"Live list contains {len(found)} of {expected_count} expected watch pages")
    previous = TEACHING_SEQUENCE[expected_count - len(plan["lessons"]) - 1]
    if expected[expected_count - len(plan["lessons"])] not in Page(
            read_live(site, watch_path(previous) + revision)[1].decode()).links:
        raise ValueError(f"{previous} does not yet link to the new batch")

    for index, lesson in enumerate(plan["lessons"]):
        page = Page(read_live(site, watch_path(lesson) + revision)[1].decode())
        source = f"media/{lesson}.mp4?v={COURSE_VERSION}"
        if page.sources != [source] or not page.inline_player or page.chapter_buttons < 5:
            raise ValueError(f"{lesson}: incomplete watch page")
        if index + 1 < len(plan["lessons"]) and watch_path(plan["lessons"][index + 1]) not in page.links:
            raise ValueError(f"{lesson}: the next watch link does not match the lesson order")
        report = json.loads((ROOT / f"review/{lesson}-studio-qa.json").read_text())
        mime, media = read_live(site, source)
        if mime != "video/mp4" or hashlib.sha256(media).hexdigest() != report["sha256"]:
            raise ValueError(f"{lesson}: the live MP4 differs from the verified export")
        print(f"{lesson}: watch page and verified {len(media):,}-byte MP4 online", flush=True)
    print(f"{expected_count} of {len(TEACHING_SEQUENCE)} teaching films are online", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("site")
    args = parser.parse_args()
    plan = json.loads((ROOT / "production/t01-studio/release_plan.json").read_text())
    for attempt in range(1, 36):
        try:
            check(args.site, plan)
            return
        except (URLError, TimeoutError, ValueError) as error:
            if attempt == 35:
                raise
            print(f"Waiting for the Pages release ({attempt}) — {error}", flush=True)
            time.sleep(12)


if __name__ == "__main__":
    main()
