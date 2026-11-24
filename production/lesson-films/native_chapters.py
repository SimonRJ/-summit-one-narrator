"""Add the watch page's teaching chapters to an existing H.264/AAC film.

The chapter track works in a compatible native player or a downloaded MP4.
The camera and microphone packet checks include timing and encoded payloads.
"""

import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import shutil
import subprocess
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[2]
FROZEN = {"T02.1", "T02.2"}


class ChapterButtons(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows = []
        self.start = None
        self.words = []

    def handle_starttag(self, tag, attrs):
        if tag == "button" and "data-time" in dict(attrs):
            self.start = round(float(dict(attrs)["data-time"]) * 1000)
            self.words = []

    def handle_data(self, data):
        if self.start is not None:
            self.words.append(data)

    def handle_endtag(self, tag):
        if tag == "button" and self.start is not None:
            label = re.sub(
                r"^\d+:\d{2}\s*(?:[·•]\s*)?", "", "".join(self.words).strip()
            )
            assert label and "\n" not in label
            self.rows.append((self.start, label))
            self.start = None


def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def inspect(path):
    raw = subprocess.check_output(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_streams",
            "-show_chapters",
            "-of",
            "json",
            str(path),
        ]
    )
    return json.loads(raw)


def packet_hash(path, track):
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        track,
        "-show_packets",
        "-show_data_hash",
        "sha256",
        "-show_entries",
        "packet=pts_time,dts_time,duration_time,size,flags,data_hash",
        "-of",
        "compact=p=0:nk=0",
        str(path),
    ]
    return hashlib.sha256(subprocess.check_output(cmd)).hexdigest()


def source_editions():
    return json.loads(
        Path(__file__).with_name("native-chapter-sources.json").read_text()
    )


def ids():
    return list(source_editions())


def chapter_text(rows):
    lines = [";FFMETADATA1"]
    for start, end, title in rows:
        escaped = re.sub(r"([\\=;#])", r"\\\1", title)
        lines.extend(
            (
                "[CHAPTER]",
                "TIMEBASE=1/1000",
                f"START={start}",
                f"END={end}",
                f"title={escaped}",
            )
        )
    return "\n".join(lines) + "\n"


def mux(k, movie, page, qa, destination, picture_source=None):
    if (
        k in FROZEN
        or sha(movie) != qa["sha256"]
        or qa["sha256"] != source_editions()[k]
    ):
        raise ValueError(f"{k}: unexpected or protected source")
    before = inspect(movie)
    assert [v["codec_name"] for v in before["streams"]] == [
        "h264",
        "aac",
    ] and not before["chapters"]
    parser = ChapterButtons()
    parser.feed(page.read_text())
    edges = [n for n, _ in parser.rows]
    assert len(edges) > 1 and edges[0] == 0 and sorted(set(edges)) == edges
    final = round(float(before["streams"][0]["duration"]) * 1000)
    rows = [
        (n, end, label) for (n, label), end in zip(parser.rows, [*edges[1:], final])
    ]
    assert all(n < end for n, end, _ in rows)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory() as scratch:
        meta = Path(scratch) / "chapters.ffmeta"
        meta.write_text(chapter_text(rows))
        subprocess.run(
            [
                "ffmpeg",
                "-v",
                "error",
                "-nostdin",
                "-y",
                "-i",
                str(picture_source or movie),
                "-f",
                "ffmetadata",
                "-i",
                str(meta),
                "-map",
                "0:v:0",
                "-map",
                "0:a:0",
                "-map_metadata",
                "0",
                "-map_chapters",
                "1",
                "-c",
                "copy",
                "-movflags",
                "+faststart",
                str(destination),
            ],
            check=True,
        )
    after = inspect(destination)
    assert [v["codec_name"] for v in after["streams"][:2]] == ["h264", "aac"]
    actual = [
        (
            round(float(c["start_time"]) * 1000),
            round(float(c["end_time"]) * 1000),
            c["tags"]["title"],
        )
        for c in after["chapters"]
    ]
    assert rows == actual, (k, rows, actual)
    hashes = {}
    for track in ("v:0", "a:0"):
        baseline = picture_source if track == "v:0" and picture_source else movie
        old, new = packet_hash(baseline, track), packet_hash(destination, track)
        assert old == new, (k, track, old, new)
        hashes[track] = new
    return {
        "prior_mp4_sha256": qa["sha256"],
        "sha256": sha(destination),
        "packet_timing_and_payload_sha256": hashes,
        "chapters": [{"start_ms": s, "end_ms": e, "title": n} for s, e, n in rows],
    }


def one(k, out):
    page = ROOT / ("watch-" + k.lower().replace(".", "-") + ".html")
    movie = ROOT / "media" / (k + ".mp4")
    qa = json.loads((ROOT / "review" / (k + "-studio-qa.json")).read_text())
    if k == "T01.1":
        from ribbon_transition import render

        with TemporaryDirectory() as temp:
            repaired = Path(temp) / "ribbon.mp4"
            change = render(movie, repaired)
            result = mux(k, movie, page, qa, out / movie.name, picture_source=repaired)
            result["picture_revision"] = change
    else:
        result = mux(k, movie, page, qa, out / movie.name)
    (out / (k + ".json")).write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    )
    return result


def install(out):
    catalogue = ROOT / "data/teaching-72.json"
    data = json.loads(catalogue.read_text())
    by_id = {entry["id"]: entry for entry in data["items"]}
    for k in ids():
        movie = ROOT / "media" / (k + ".mp4")
        replacement = out / movie.name
        report = json.loads((out / (k + ".json")).read_text())
        assert sha(movie) == report["prior_mp4_sha256"] == source_editions()[k]
        assert sha(replacement) == report["sha256"]
        page = ROOT / ("watch-" + k.lower().replace(".", "-") + ".html")
        qa_path = ROOT / "review" / (k + "-studio-qa.json")
        qa = json.loads(qa_path.read_text())
        assert qa["sha256"] == report["prior_mp4_sha256"]
        version = "chapters-" + report["sha256"][:12]
        new_url = f"media/{k}.mp4?v={version}"
        new_page, count = re.subn(
            re.escape("media/" + k + ".mp4") + r"(?:\?v=[^\"'<> ]+)?",
            new_url,
            page.read_text(),
        )
        assert count == 2, (k, count)
        page.write_text(new_page)
        by_id[k]["video_url"] = new_url
        qa["native_chapters"] = report
        qa["sha256"] = report["sha256"]
        qa_path.write_text(json.dumps(qa, indent=2, ensure_ascii=False) + "\n")
        shutil.copyfile(replacement, movie)
    catalogue.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("film")
    ap.add_argument("out", type=Path)
    args = ap.parse_args()
    if args.film == "install":
        install(args.out)
        raise SystemExit(0)
    work = ids() if args.film == "all" else [args.film]
    for k in work:
        print(k, len(one(k, args.out)["chapters"]), flush=True)
