"""Verify and install both counting-workshop films on the checked-out review branch."""

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

from counting_workshops import ROOT, EDITIONS

sys.path.insert(0, str(ROOT / "production/t01-studio"))
import publish


def digest(path):
    with path.open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def audio_digest(path):
    return subprocess.check_output(
        [
            "ffmpeg",
            "-v",
            "error",
            "-i",
            str(path),
            "-map",
            "0:a:0",
            "-c:a",
            "copy",
            "-f",
            "hash",
            "-hash",
            "sha256",
            "-",
        ],
        text=True,
    ).strip()


def media_streams(path):
    raw = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_streams", "-of", "json", str(path)]
    )
    return json.loads(raw)["streams"]


def install(
    folder,
    editions=EDITIONS,
    art_source="production/lesson-films/counting_workshops.py",
):
    change = {}
    for lesson, (version, source_hash) in editions.items():
        current = ROOT / "media" / (lesson + ".mp4")
        film = folder / (lesson + ".mp4")
        report_path = ROOT / "review" / (lesson + "-studio-qa.json")
        report = json.loads(report_path.read_text())
        assert digest(current) == report["sha256"] == source_hash
        before, after = media_streams(current), media_streams(film)
        assert [s["codec_name"] for s in after] == ["h264", "aac"]
        assert (after[0]["width"], after[0]["height"], after[0]["r_frame_rate"]) == (
            1920,
            1080,
            "30/1",
        )
        assert before[0]["nb_frames"] == after[0]["nb_frames"]
        assert abs(float(before[0]["duration"]) - float(after[0]["duration"])) < 0.04
        old_audio, new_audio = audio_digest(current), audio_digest(film)
        assert old_audio == new_audio, (lesson, old_audio, new_audio)
        subprocess.run(
            [
                "ffmpeg",
                "-v",
                "error",
                "-nostdin",
                "-xerror",
                "-i",
                str(film),
                "-f",
                "null",
                "-",
            ],
            check=True,
        )
        change[lesson] = dict(
            version=version,
            sha256=digest(film),
            frames=int(after[0]["nb_frames"]),
            audio_packet_sha256=new_audio,
        )
    generator = ROOT / "production/t01-studio/publish.py"
    source = generator.read_text()
    for lesson, values in change.items():
        old = publish.REVISED_MEDIA[lesson]
        match = f'"{lesson}": "{old}"'
        assert source.count(match) == 1
        source = source.replace(match, f'"{lesson}": "{values["version"]}"')
        publish.REVISED_MEDIA[lesson] = values["version"]
        path = ROOT / "review" / (lesson + "-studio-qa.json")
        report = json.loads(path.read_text())
        for field in ("legacy_sha256", "compared_frames", "compared_scenes"):
            report.pop(field, None)
        report.update(
            **values,
            source_sha256=editions[lesson][1],
            art_source=art_source,
            decoded_successfully=True,
        )
        path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
        for suffix in (".mp4", "-studio-poster.jpg"):
            shutil.copyfile(
                folder / (lesson + suffix), ROOT / "media" / (lesson + suffix)
            )
        script = json.loads(
            (ROOT / "production/scripts" / (lesson + ".json")).read_text()
        )
        route = ROOT / ("watch-" + lesson.lower().replace(".", "-") + ".html")
        route.write_text(
            publish.make_watch_page(
                lesson, script, report, available=publish.TEACHING_SEQUENCE
            )
        )
    generator.write_text(source)


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("folder", type=Path)
    cli.add_argument(
        "--incidence",
        action="store_true",
        help="Install the check-in and fixture-room films.",
    )
    args = cli.parse_args()
    if args.incidence:
        from incidence_workshops import CHECKS

        install(args.folder, CHECKS, "production/lesson-films/incidence_workshops.py")
    else:
        install(args.folder)
