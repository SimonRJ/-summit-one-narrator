"""Assemble and align the actual Voice C recordings without changing their speed."""

import argparse
from difflib import SequenceMatcher
import hashlib
import json
import re
import subprocess

import numpy as np
import soundfile as sf
from num2words import num2words

from synth import BUILD, IDS, MODEL_REVISION, RATE, ROOT, VOICE_SHA


PAUSES = {
    "T01.1": {3: 2.4, 7: 2.3, 9: 5.0},
    "T01.2": {3: 2.4, 6: 1.0, 9: 5.0},
    "T01.3": {3: 3.5, 8: 5.0},
    "T01.E": {1: 3.5, 6: 2.6, 8: 5.0},
    "T02.3": {3: 3.5, 8: 5.0},
    "T02.E": {1: 3.5, 6: 5.0},
    "T03.1": {3: 3.5, 8: 5.0},
    "T03.2": {3: 3.5, 7: 5.0},
    "T03.3": {3: 3.5, 7: 5.0},
    "T03.E": {1: 3.5, 6: 5.0},
    "T04.1": {3: 3.5, 7: 5.0},
    "T04.2": {3: 3.5, 7: 5.0},
    "T04.3": {3: 3.5, 8: 5.0},
    "T04.E": {1: 3.5, 6: 5.0},
}
SPOKEN_FORMS = {
    "centimetre": "centimeter",
    "centimetres": "centimeters",
    "metre": "meter",
    "metres": "meters",
    "cm": "centimeters",
    "m": "meters",
    "it's": "its",
    "cue": "queue",
    "headcount": "head count",
    "endpoints": "end points",
    "reread": "re read",
    "o'clock": "o clock",
    "oh": "o",
    "ex": "x",
    "factorisation": "factorization",
    "factorise": "factorize",
    "factorises": "factorizes",
    "colour": "color",
    "colours": "colors",
    "colouring": "coloring",
    "centre": "center",
    "centres": "centers",
    "neighbour": "neighbor",
    "neighbours": "neighbors",
    "neighbouring": "neighboring",
    "leftover": "left over",
    "kilogram": "kilograms",
    "kg": "kilograms",
    "nought": "zero",
    "weigh": "way",
    "weighs": "ways",
    "route": "root",
    "routes": "roots",
    "along": "a long",
}


def clock_words(match):
    hour, minute = map(int, match.groups())
    if minute == 0:
        return f"{hour} o'clock"
    if minute < 10:
        return f"{hour} oh {minute}"
    return f"{hour} {minute}"


def fraction_words(match):
    numerator, denominator = map(int, match.groups())
    if denominator < 2:
        return match.group()
    base = {2: "half", 4: "quarter"}.get(denominator, num2words(denominator, to="ordinal"))
    if numerator != 1:
        base = "halves" if denominator == 2 else base + "s"
    return f"{numerator} {base}"


def tokens(text):
    text = text.lower().replace("’", "'")
    text = re.sub(r"\$(\d+(?:,\d{3})*)", r"\1 dollars", text)
    text = re.sub(r"(?<!\d)(\d{1,2}):([0-5]\d)(?!\d)", clock_words, text)
    text = re.sub(r"\b([1-9]\d*)\.5\b", r"\1 and a half", text)
    text = re.sub(r"\b(\d+)\.(\d+)\b", lambda m: f"{m[1]} point {' '.join(m[2])}", text)
    text = re.sub(r"\b(\d+)\s*/\s*(\d+)\b", fraction_words, text)
    text = re.sub(r"\b40s\b", "forties", text)
    text = re.sub(r"(?<=\d)\s*[×x*]\s*(?=\d)", " times ", text)
    text = text.replace("×", " times ").replace("÷", " divided by ").replace("+", " plus ")
    text = text.replace("=", " equals ").replace("−", " minus ")
    parts = re.findall(r"[a-z]+(?:'[a-z]+)?|\d+(?:,\d{3})*(?:st|nd|rd|th)?s?", text)
    result = []
    for part in parts:
        if part[0].isdigit():
            plural = part.endswith("s")
            numeral = part[:-1] if plural else part
            ordinal = numeral[-2:] in ("st", "nd", "rd", "th")
            numeral = numeral[:-2] if ordinal else numeral
            expanded = num2words(int(numeral.replace(",", "")), to="ordinal" if ordinal else "cardinal")
            terms = re.findall("[a-z]+", expanded)
            if plural:
                terms[-1] += "s"
            result.extend(terms)
        else:
            result.extend(SPOKEN_FORMS.get(part, part).split())
    return result


def recognized_terms(words, index):
    """Keep the time of each recognised word when Whisper splits a written number."""
    text = words[index].word.strip()
    previous = words[index - 1].word.strip() if index else ""
    following = words[index + 1].word.strip() if index + 1 < len(words) else ""
    if text.lower() == "x" and previous.isdigit() and following.isdigit():
        return ["times"]
    decimal = re.fullmatch(r"\.(\d+)[,.;]?", text)
    if decimal and previous.isdigit():
        return ["point", *[num2words(int(digit)) for digit in decimal[1]]]
    tail = re.fullmatch(r"(\d+)[,.;]?", text)
    if tail and re.fullmatch(r"\.\d+,", previous):
        return [num2words(int(digit)) for digit in tail[1]]
    if previous.isdigit() and re.fullmatch(r",000ths?[,.]?", text):
        return ["thousandths"]
    return tokens(text)


def align(script, recognized, start, end):
    expected = script.split()
    target = [(token, k) for k, word in enumerate(expected) for token in tokens(word)]
    heard = []
    for word_index, word in enumerate(recognized):
        terms = recognized_terms(recognized, word_index)
        for index, term in enumerate(terms):
            span = (word.end - word.start) / len(terms)
            heard.append((term, start + word.start + index * span, start + word.start + (index + 1) * span))

    matched = [[] for _ in expected]
    compare = SequenceMatcher(None, [x[0] for x in target], [x[0] for x in heard], autojunk=False)
    for match in compare.get_matching_blocks():
        for offset in range(match.size):
            matched[target[match.a + offset][1]].append(heard[match.b + offset][1:])
    words = [
        {"text": text, "start": min(t[0] for t in pairs), "end": max(t[1] for t in pairs), "matched": True}
        if pairs else {"text": text, "matched": False}
        for text, pairs in zip(expected, matched)
    ]

    cursor = 0
    while cursor < len(words):
        if words[cursor]["matched"]:
            cursor += 1
            continue
        stop = cursor
        while stop < len(words) and not words[stop]["matched"]:
            stop += 1
        left = words[cursor - 1]["end"] if cursor else start
        right = words[stop]["start"] if stop < len(words) else end
        width = max(0.0, right - left) / (stop - cursor)
        for k in range(cursor, stop):
            words[k].update(start=left + (k - cursor) * width, end=left + (k - cursor + 1) * width)
        cursor = stop

    last = start
    for word in words:
        word["start"] = min(end, max(last, word["start"]))
        word["end"] = min(end, max(word["start"], word["end"]))
        last = word["end"]
    return words, round(compare.ratio() * 100, 2)


def caption_cues(words):
    groups = []
    sentence = []
    for word in words:
        sentence.append(word)
        if word["text"].endswith((".", "?", "!")):
            groups.extend(caption_phrases(sentence))
            sentence = []
    if sentence:
        groups.extend(caption_phrases(sentence))

    cues = []
    for i, group in enumerate(groups):
        start = group[0]["start"]
        end = group[-1]["end"] + 0.13
        if i + 1 < len(groups):
            end = min(end, groups[i + 1][0]["start"])
        if end - start >= 0.12:
            cues.append({"start": start, "end": end, "text": " ".join(w["text"] for w in group)})
    return cues


def caption_phrases(sentence):
    while len(" ".join(word["text"] for word in sentence)) > 56:
        length = 0
        end = 0
        for word in sentence:
            length += len(word["text"]) + (1 if end else 0)
            if length > 56:
                break
            end += 1
        # Leave a complete phrase at the end of a sentence and prefer a nearby clause break.
        end = max(1, min(end, len(sentence) - 3))
        for index in range(end, max(2, end - 3), -1):
            if sentence[index - 1]["text"].endswith((",", ":")):
                end = index
                break
        yield sentence[:end]
        sentence = sentence[end:]
    if sentence:
        yield sentence


def load_recording(lesson, index, text):
    stem = f"{lesson}-{index:02}"
    meta = json.loads((BUILD / f"{stem}.json").read_text())
    if meta["reference_sha256"] != VOICE_SHA or meta["model_revision"] != MODEL_REVISION:
        raise ValueError(f"{stem}: incorrect narrator reference")
    if not meta["natural_speed"] or meta["narration_sha256"] != hashlib.sha256(text.encode()).hexdigest():
        raise ValueError(f"{stem}: recording does not match the current script")
    waveform, rate = sf.read(BUILD / f"{stem}.wav", dtype="float32")
    if rate != RATE or waveform.ndim != 1 or abs(len(waveform) / rate - meta["duration_seconds"]) > 0.02:
        raise ValueError(f"{stem}: unexpected audio format or duration")
    return waveform


def stamp(seconds):
    ms = round(seconds * 1000)
    return f"{ms // 3600000:02}:{ms // 60000 % 60:02}:{ms // 1000 % 60:02}.{ms % 1000:03}"


def prepare(lesson):
    from faster_whisper import WhisperModel

    script = json.loads((ROOT / f"production/scripts/{lesson}.json").read_text())
    build = BUILD / lesson
    build.mkdir(parents=True, exist_ok=True)
    model = WhisperModel("base.en", device="cpu", compute_type="int8", cpu_threads=2)
    audio = [np.zeros(round(0.6 * RATE), dtype="float32")]
    cursor = len(audio[0])
    scenes = []
    captions = []
    for scene in script["scenes"]:
        index = scene["n"]
        waveform = load_recording(lesson, index, scene["narration"])
        start = cursor / RATE
        end = (cursor + len(waveform)) / RATE
        pause = PAUSES.get(lesson, {}).get(index, {"PUZZLE": 3.5, "RECAP": 5.0}.get(scene["stage"], 0.65))
        gap = np.zeros(round(pause * RATE), dtype="float32")
        decoded, _ = model.transcribe(
            waveform[::3],
            word_timestamps=True,
            beam_size=5,
            condition_on_previous_text=False,
            language="en",
        )
        spoken = [word for segment in decoded for word in segment.words or []]
        words, match = align(scene["narration"], spoken, start, end)
        print(f"{lesson} scene {index}: {match:.2f}% aligned, speech {start:.2f}–{end:.2f}s", flush=True)
        scenes.append({
            "n": index,
            "start": 0.0 if index == 1 else start,
            "end": end + len(gap) / RATE,
            "speech_end": end,
            "words": words,
            "recognized_speech": " ".join(word.word.strip() for word in spoken),
            "match_percent": match,
        })
        captions.extend(caption_cues(words))
        audio.extend([waveform, gap])
        cursor += len(waveform) + len(gap)

    average = sum(scene["match_percent"] for scene in scenes) / len(scenes)
    if average < 90 or min(scene["match_percent"] for scene in scenes) < 80:
        for scene in scenes:
            if scene["match_percent"] < 90:
                print(f"Review scene {scene['n']} ({scene['match_percent']:.2f}%): {scene['recognized_speech']}")
        raise ValueError(f"{lesson}: review the narration before publishing ({average:.2f}% mean alignment)")

    raw = build / "voice-c-raw.wav"
    sf.write(raw, np.concatenate(audio), RATE, subtype="PCM_24")
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-i", str(raw), "-af", "loudnorm=I=-18:TP=-2:LRA=9",
         "-ar", str(RATE), "-c:a", "pcm_s24le", str(build / "narration.wav")],
        check=True,
    )
    duration = cursor / RATE
    (build / "timeline.json").write_text(json.dumps({
        "id": lesson,
        "duration": duration,
        "narration_reference": VOICE_SHA,
        "model_revision": MODEL_REVISION,
        "mean_match_percent": round(average, 2),
        "scenes": scenes,
        "captions": captions,
    }, indent=2) + "\n")
    (build / "captions.vtt").write_text("WEBVTT\n\n" + "\n\n".join(
        f"{stamp(cue['start'])} --> {stamp(cue['end'])}\n{cue['text']}" for cue in captions
    ) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("lesson", choices=IDS)
    prepare(parser.parse_args().lesson)
