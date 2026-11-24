"""Replace a text-only notebook prompt with a measured drawing, keeping the public AAC and caption band."""

import argparse
from bisect import bisect_right
import hashlib
import json
from math import ceil
from pathlib import Path
from tempfile import TemporaryDirectory
from PIL import Image, ImageDraw, ImageFont
import re
import shutil
import subprocess
import sys
from companion_notebooks import ART, picture
from finish_tickets import caption_time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "production/t01-studio"))
import publish


def digest(path):
    with path.open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def audio_hash(path):
    return subprocess.check_output(
        [
            "ffmpeg",
            "-v",
            "error",
            "-i",
            str(path),
            "-map",
            "0:a",
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


def frames(path):
    value = subprocess.check_output(
        [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_entries",
            "stream=nb_frames",
            "-of",
            "csv=p=0",
            str(path),
        ],
        text=True,
    )
    return int(value.strip())


def probe_frame(path, t, y=0, height=1080):
    return subprocess.check_output(
        [
            "ffmpeg",
            "-v",
            "error",
            "-nostdin",
            "-ss",
            str(t),
            "-i",
            str(path),
            "-frames:v",
            "1",
            "-vf",
            f"crop=1920:{height}:0:{y},scale=320:-1,format=gray",
            "-f",
            "rawvideo",
            "-",
        ]
    )


def byte_error(a, b):
    assert len(a) == len(b) and a
    return sum(abs(u - v) for u, v in zip(a, b)) / len(a)


def timing(source, qa):
    cues = []
    for block in re.split(r"\n\s*\n", source.read_text().strip())[1:]:
        span, *text = block.splitlines()
        a, b = map(caption_time, span.split(" --> "))
        cues.append((a, b, " ".join(text)))
    closing = qa["scenes"][-1]["start"]
    index = next(
        (
            i
            for i, (a, b, s) in enumerate(cues)
            if a >= closing
            and re.search(r"notebook challenge|rebuild this|rebuild the", s, re.I)
        ),
        None,
    )
    if index is None:
        raise ValueError("Could not locate the recorded notebook prompt")
    first = cues[index][0]
    last = cues[-1][1]
    assert closing <= first < last < qa["duration_seconds"]
    return first, last


# Measured against the released Voice C recording using two separate speech passes.
PERIMETER_CAPTIONS = (
    ("00:01:16.640", "00:01:19.180", "Their perimeters are fifty, twenty-eight,"),
    ("00:01:19.220", "00:01:20.700", "twenty-two and twenty."),
    ("00:01:21.260", "00:01:22.640", "It is four by six."),
)
OLD_T18_VTT = "2f1802e8251f4f2103e289e5e2af13e806b4bb5f6a243a448097c0ca9112736c"


def repair_perimeter_captions(source, vtt, out, scratch):
    assert digest(vtt) == OLD_T18_VTT
    old = "00:01:22.972 --> 00:01:23.110\nIt is four by six."
    text = vtt.read_text()
    assert text.count(old) == 1
    corrected = text.replace(
        old, "\n\n".join(f"{a} --> {b}\n{line}" for a, b, line in PERIMETER_CAPTIONS)
    )
    transcript = json.loads((ROOT / "production/scripts/T18.1.json").read_text())
    tokenize = lambda words: re.findall(r"[a-z]+", words.lower())
    caption_words = " ".join(
        line
        for line in corrected.splitlines()
        if line and "-->" not in line and line != "WEBVTT"
    )
    assert tokenize(caption_words) == tokenize(
        " ".join(scene["narration"] for scene in transcript["scenes"])
    )
    (out / vtt.name).write_text(corrected)

    raw = subprocess.check_output(
        [
            "ffmpeg",
            "-v",
            "error",
            "-ss",
            "76.4",
            "-i",
            str(source),
            "-frames:v",
            "1",
            "-vf",
            "crop=1920:146:0:934,format=rgb24",
            "-f",
            "rawvideo",
            "-",
        ]
    )
    empty = Image.frombytes("RGB", (1920, 146), raw)
    layers = [(76.37, 83.20, "")]
    layers.extend(
        (caption_time(a), caption_time(b), words) for a, b, words in PERIMETER_CAPTIONS
    )
    inputs, filters = [], []
    face = Path("/usr/share/fonts/truetype/open-sans/OpenSans-Bold.ttf")
    font = ImageFont.truetype(str(face) if face.exists() else "DejaVuSans-Bold.ttf", 51)
    for i, (start, end, words) in enumerate(layers):
        im = empty.copy()
        if words:
            draw = ImageDraw.Draw(im)
            bounds = draw.textbbox((960, 67), words, font=font, anchor="mm")
            draw.rounded_rectangle(
                (bounds[0] - 31, 20, bounds[2] + 31, 110), radius=19, fill="#101720"
            )
            draw.text((960, 67), words, font=font, fill="#f2f1ed", anchor="mm")
        png = scratch / f"caption-{i}.png"
        im.save(png)
        stream = f"{i + 2}:v"
        if words:
            length = end - start
            inputs.extend(
                [
                    "-loop",
                    "1",
                    "-framerate",
                    "30",
                    "-t",
                    f"{length:.3f}",
                    "-i",
                    str(png),
                ]
            )
            filters.append(
                f"[{stream}]format=rgba,fade=t=in:st=0:d=0.12:alpha=1,fade=t=out:st={length - 0.14:.3f}:d=0.14:alpha=1,setpts=PTS-STARTPTS+{start:.3f}/TB[faded{i}];"
            )
            stream = f"faded{i}"
        else:
            inputs.extend(["-i", str(png)])
        previous = "0:v" if i == 0 else f"caption{i - 1}"
        filters.append(
            f"[{previous}][{stream}]overlay=0:934:enable='between(t,{start},{end})':eof_action=repeat[caption{i}];"
        )
    return inputs, "".join(filters), f"caption{len(layers) - 1}"


def build(k, out):
    out.mkdir(parents=True, exist_ok=True)
    qa = json.loads((ROOT / "review" / (k + "-studio-qa.json")).read_text())
    source = ROOT / "media" / (k + ".mp4")
    expected = json.loads(
        Path(__file__).with_name("notebook-source-hashes.json").read_text()
    )
    assert digest(source) == qa["sha256"] == expected[k]
    vtt = ROOT / "media" / (k + ".vtt")
    start, end = timing(vtt, qa)
    duration = qa["duration_seconds"]
    nframes = frames(source)
    assert (qa["width"], qa["height"], qa["fps"]) == (1920, 1080, 30) and abs(
        nframes / 30 - duration
    ) < 0.04
    target = out / (k + ".mp4")
    scratch = TemporaryDirectory()
    inputs, filters, base = [], "", "0:v"
    if k == "T18.1":
        inputs, filters, base = repair_perimeter_captions(
            source, vtt, out, Path(scratch.name)
        )
    descriptor = (
        filters
        + f"[1:v]setpts=PTS-STARTPTS+{start:.6f}/TB[board];[{base}][board]overlay=0:0:enable='gte(t,{start:.6f})':eof_action=repeat,format=yuv420p[film]"
    )
    cmd = [
        "ffmpeg",
        "-v",
        "error",
        "-nostdin",
        "-y",
        "-threads",
        "2",
        "-i",
        str(source),
        "-f",
        "rawvideo",
        "-pix_fmt",
        "rgb24",
        "-s",
        "1920x930",
        "-r",
        "15",
        "-i",
        "-",
        *inputs,
        "-filter_complex_threads",
        "2",
        "-filter_complex",
        descriptor,
        "-map",
        "[film]",
        "-map",
        "0:a:0",
        "-frames:v",
        str(nframes),
        "-c:v",
        "libx264",
        "-threads",
        "3",
        "-preset",
        "veryfast",
        "-crf",
        "17",
        "-c:a",
        "copy",
        "-movflags",
        "+faststart",
        str(target),
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for n in range(ceil((duration - start) * 15)):
        proc.stdin.write(picture(k, n / 15, end - start, duration - end).tobytes())
    proc.stdin.close()
    if proc.wait():
        raise RuntimeError("Encoding failed")
    scratch.cleanup()
    assert frames(target) == nframes
    speech = audio_hash(source)
    assert audio_hash(target) == speech
    subprocess.run(
        ["ffmpeg", "-v", "error", "-xerror", "-i", str(target), "-f", "null", "-"],
        check=True,
    )
    prefix_checks = [
        round(byte_error(probe_frame(source, t), probe_frame(target, t)), 4)
        for t in (1, closing_time(qa), max(0, start - 1))
    ]
    caption_checks = [
        round(
            byte_error(
                probe_frame(source, t, 934, 146), probe_frame(target, t, 934, 146)
            ),
            4,
        )
        for t in (start + 0.5, (start + end) / 2, end - 0.4)
    ]
    changed = byte_error(
        probe_frame(source, duration - 0.5, 0, 928),
        probe_frame(target, duration - 0.5, 0, 928),
    )
    if max(prefix_checks + caption_checks) > 3.0 or changed < 20:
        raise ValueError(
            f"Pixel checks failed for {k}: {prefix_checks} {caption_checks} {changed}"
        )
    if k == "T18.1":
        samples = (77.5, 79.65, 81.98)
        body = [
            round(
                byte_error(
                    probe_frame(source, t, 0, 930), probe_frame(target, t, 0, 930)
                ),
                4,
            )
            for t in samples
        ]
        subtitle = [
            round(
                byte_error(
                    probe_frame(source, t, 934, 146), probe_frame(target, t, 934, 146)
                ),
                4,
            )
            for t in samples
        ]
        assert max(body) < 3 and min(subtitle) > 2, (body, subtitle)
        qa["perimeter_caption_repair"] = {
            "cues": [
                {"start": a, "end": b, "text": words}
                for a, b, words in PERIMETER_CAPTIONS
            ],
            "source_vtt_sha256": OLD_T18_VTT,
            "vtt_sha256": digest(out / vtt.name),
            "caption_transcript_matches_authored_narration": True,
            "spoken_first_sentence_seconds": [76.64, 80.50],
            "spoken_solution_seconds": [81.30, 82.54],
            "body_mean_error": body,
            "caption_band_mean_change": subtitle,
        }
    qa.update(
        source_sha256=qa["sha256"],
        sha256=digest(target),
        version=ART[k][0],
        frames=nframes,
        decoded_successfully=True,
        audio_packet_sha256=speech,
        notebook_art_source="production/lesson-films/companion_notebooks.py",
        notebook_start_seconds=start,
        prompt_ends_seconds=end,
        earlier_frame_mean_errors=prefix_checks,
        caption_band_mean_errors=caption_checks,
        closing_frame_mean_change=round(changed, 3),
    )
    (out / (k + "-studio-qa.json")).write_text(
        json.dumps(qa, indent=2, ensure_ascii=False) + "\n"
    )


def closing_time(qa):
    return max(1, qa["scenes"][-1]["start"] - 0.8)


def install(folder):
    generator = ROOT / "production/t01-studio/publish.py"
    content = generator.read_text()
    catalogue = ROOT / "data/teaching-72.json"
    catalogue_data = json.loads(catalogue.read_text())
    catalogue_rows = {row["id"]: row for row in catalogue_data["items"]}
    patch = []
    for k, (version, _) in ART.items():
        path = folder / (k + "-studio-qa.json")
        qa = json.loads(path.read_text())
        movie = folder / (k + ".mp4")
        assert digest(movie) == qa["sha256"] and qa["version"] == version
        assert digest(ROOT / "media" / (k + ".mp4")) == qa["source_sha256"]
        assert k not in publish.REVISED_MEDIA
        catalogue_rows[k]["video_url"] = f"media/{k}.mp4?v={version}"
        publish.REVISED_MEDIA[k] = version
        patch.append(f'    "{k}": "{version}",')
        if k == "T18.1":
            caption = folder / (k + ".vtt")
            assert digest(caption) == qa["perimeter_caption_repair"]["vtt_sha256"]
            assert digest(ROOT / "media" / caption.name) == OLD_T18_VTT
            shutil.copyfile(caption, ROOT / "media" / caption.name)
        shutil.copyfile(movie, ROOT / "media" / movie.name)
        shutil.copyfile(path, ROOT / "review" / path.name)
        script = json.loads((ROOT / "production/scripts" / (k + ".json")).read_text())
        route = ROOT / ("watch-" + k.lower().replace(".", "-") + ".html")
        route.write_text(
            publish.make_watch_page(k, script, qa, available=publish.TEACHING_SEQUENCE)
        )
    catalogue.write_text(
        json.dumps(catalogue_data, indent=2, ensure_ascii=False) + "\n"
    )
    mark = "REVISED_MEDIA = {\n"
    assert content.count(mark) == 1
    generator.write_text(content.replace(mark, mark + "\n".join(patch) + "\n"))


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("lesson", choices=[*ART, "install"])
    cli.add_argument("output", type=Path)
    args = cli.parse_args()
    install(args.output) if args.lesson == "install" else build(
        args.lesson, args.output
    )
