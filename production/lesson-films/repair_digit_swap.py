"""Replace only S102 scene 8, reusing ten performances from the pinned public film.

The saved Voice C take is used directly; this command never synthesises narration.
The older public film did not retain a word timeline. Its saved recovery therefore
uses measured ASR word timing and the published scene starts. Embedded captions in
the other ten scenes remain in their original pictures.
"""
import argparse
from hashlib import sha256
import json
import math
from pathlib import Path
import shutil
import subprocess
from zipfile import ZipFile

import numpy as np
from PIL import Image
import soundfile as sf

from digit_swap_scene import check_maths, draw, motion
from repair_spoken_condition import capture, fetch, shift_scene, waveform, write
from prepare_audio import align, caption_cues, load_recording, stamp, transcribe
from synth import MODEL_REVISION, RATE, ROOT, VOICE_SHA

LESSON = 'S102'
FPS = 30
SOURCE_SHA = '538f9142a5113e5d14d3a35b6a7851e8dd331e16aba7d98224a7d0c294601612'
GUIDE_SHA = '4ff0df3427a7f09492a68252f931a1c2b39dcf98aaa4ea3af60b99b086c38b94'
TIMELINE_SHA = '81837aeb40efb9e7d5c6f1fed5994a504d0e939c29b20e36c201a8e63af5244e'
BASE = 'https://github.com/SimonRJ/-summit-one-narrator/releases/download/lesson-introductions/'


def saved_recording():
    stem = ROOT / 'production/lesson-films/voice-c-repairs/S102-tens-units'
    if not stem.with_suffix('.flac').exists():
        # A workflow recording is already restored to build/t01-studio. The same
        # voice, natural-speed and narration-hash checks below apply to that take.
        return
    metadata = json.loads(stem.with_suffix('.json').read_text())
    assert sha256(stem.with_suffix('.flac').read_bytes()).hexdigest() == metadata['recording_sha256']
    destination = ROOT / 'build/t01-studio'
    destination.mkdir(parents=True, exist_ok=True)
    samples, rate = sf.read(stem.with_suffix('.flac'), dtype='int16')
    assert rate == RATE and samples.ndim == 1
    sf.write(destination / 'S102-08.wav', samples, rate, subtype='PCM_16')
    write(destination / 'S102-08.json', metadata)


def cache_recording():
    """Save the finished take losslessly, so later renders never need a retake."""
    line = json.loads((ROOT/'production/scripts/S102.json').read_text())['scenes'][7]['narration']
    load_recording(LESSON, 8, line)
    take = ROOT/'build/t01-studio/S102-08'
    samples, rate = sf.read(take.with_suffix('.wav'), dtype='int16')
    stem = ROOT/'production/lesson-films/voice-c-repairs/S102-tens-units'
    stem.parent.mkdir(parents=True, exist_ok=True)
    if stem.with_suffix('.flac').exists():
        existing, existing_rate = sf.read(stem.with_suffix('.flac'), dtype='int16')
        assert existing_rate == rate and np.array_equal(existing, samples), 'Saved take is immutable'
    else:
        sf.write(stem.with_suffix('.flac'), samples, rate, subtype='PCM_16')
    metadata = json.loads(take.with_suffix('.json').read_text())
    metadata['recording_sha256'] = sha256(stem.with_suffix('.flac').read_bytes()).hexdigest()
    write(stem.with_suffix('.json'), metadata)
    return metadata


def compare_pictures(movie, original, scene, cues, first, stop, nframes):
    def decode(path, selection):
        return np.frombuffer(capture(['-i', path, '-an', '-vf',
            selection + ',scale=320:180:flags=area,format=rgb24', '-fps_mode', 'vfr',
            '-f', 'rawvideo', 'pipe:1']), np.uint8).reshape(-1, 180, 320, 3)
    actual = decode(movie, "select='not(mod(n,30))'")
    delta_frames = nframes - (stop - first)
    source_count = int(subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
        '-show_entries', 'stream=nb_frames', '-of', 'csv=p=0', str(original)], text=True))
    selected = [n for n in range(source_count)
                if (n < first and n % FPS == 0) or (n >= stop and (n + delta_frames) % FPS == 0)]
    selection = (f"select='lt(n,{first})*not(mod(n,{FPS}))+"
                 f"gte(n,{stop})*not(mod(n+({delta_frames}),{FPS}))'")
    source = decode(original, selection)
    assert len(selected) == len(source)
    reference = dict(zip(selected, source))
    errors = []
    for second, picture in enumerate(actual):
        if scene['start'] <= second < scene['end']:
            expected = np.asarray(draw(scene, cues, second).resize((320, 180), Image.Resampling.BOX))
        else:
            frame = second * FPS if second < scene['start'] else second * FPS - delta_frames
            expected = reference[frame]
        diff = abs(picture.astype('int16') - expected.astype('int16'))
        errors.append([float(diff[:153].mean()), float(diff[153:].mean())])
    worst = np.max(errors, axis=0).tolist()
    assert max(worst) < 5, worst
    return len(actual), worst


def make(out, source=None, whisper_model='base.en'):
    from faster_whisper import WhisperModel
    maths = check_maths()
    out.mkdir(parents=True, exist_ok=True)
    work = out.parent / 'repair-S102'
    work.mkdir(parents=True, exist_ok=True)
    original = work / 'original.mp4'
    if source:
        assert sha256(source.read_bytes()).hexdigest() == SOURCE_SHA
        if not original.exists():
            shutil.copyfile(source, original)
    fetch(BASE + 'S102-Intro.mp4', original, SOURCE_SHA)
    guide_file = work / 'source-guide.json'
    fetch(BASE + 'S102-Intro.json', guide_file, GUIDE_SHA)
    source_guide = json.loads(guide_file.read_text())
    timing_file = ROOT / 'production/lesson-films/source-timelines/S102-public.json'
    assert sha256(timing_file.read_bytes()).hexdigest() == TIMELINE_SHA
    before = json.loads(timing_file.read_text())
    script = json.loads((ROOT / 'production/scripts/S102.json').read_text())
    assert before['source_sha256'] == SOURCE_SHA and before['source_guide_sha256'] == GUIDE_SHA
    assert before['narration_reference'] == VOICE_SHA and before['model_revision'] == MODEL_REVISION
    assert len(before['scenes']) == len(script['scenes']) == 11
    for i, (scene, part) in enumerate(zip(before['scenes'], script['scenes'])):
        assert scene['start'] == source_guide['scenes'][i]['start']
        assert ' '.join(w['text'] for w in scene['words']) == source_guide['transcript'][i]
        if scene['n'] != 8:
            assert part['narration'] == source_guide['transcript'][i]
    line = script['scenes'][7]['narration']
    assert 'keep the hundreds digit fixed and swap the tens and units digits' in line
    assert 'One hundred and fifty-three becomes one hundred and thirty-five.' in line
    assert 'Swapping back recovers the original' in line
    saved_recording()
    fresh = load_recording(LESSON, 8, line)
    source_audio = waveform(original)
    old = before['scenes'][7]
    # The original renderer switches at the first frame at/after a scene start.
    first, stop = [math.ceil(old[k] * FPS - 1e-7) for k in ('start', 'end')]
    begin, end = first / FPS, stop / FPS
    boundaries = []
    for boundary in (begin, end):
        quiet = source_audio[round((boundary - .04) * RATE):round(boundary * RATE)]
        peak = float(np.max(abs(quiet)))
        assert peak < .005, ('Splice would cut speech', boundary, peak)
        boundaries.append(peak)
    recognizer = WhisperModel(whisper_model, device='cpu', compute_type='int8', cpu_threads=2)
    heard = transcribe(recognizer, fresh)
    words, match = align(line, heard, begin + .22, begin + .22 + len(fresh) / RATE)
    assert match >= 90, (match, [w.word for w in heard])
    normalized = work / 'normalized.wav'
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', ROOT / 'build/t01-studio/S102-08.wav',
        '-af', 'loudnorm=I=-18:TP=-2:LRA=9', '-ar', str(RATE), normalized], check=True)
    normalized_samples = waveform(normalized)
    assert len(normalized_samples) == len(fresh), 'Loudness matching changed the recording length'
    fresh = normalized_samples
    nframes = math.ceil((.22 + len(fresh) / RATE + .8) * FPS)
    insert = np.zeros(nframes * (RATE // FPS), dtype=np.float32)
    insert[round(.22 * RATE):round(.22 * RATE) + len(fresh)] = fresh
    delta = nframes / FPS - (end - begin)
    audio = np.concatenate((source_audio[:round(begin * RATE)], insert, source_audio[round(end * RATE):]))
    master = work / 'narration.flac'
    sf.write(master, audio, RATE, subtype='PCM_24')
    replacement = dict(n=8, start=begin, end=begin + nframes / FPS,
        speech_end=begin + .22 + len(fresh) / RATE, words=words, match_percent=match,
        recognized_speech=' '.join(w.word.strip() for w in heard))
    scenes = [s if s['n'] < 8 else replacement if s['n'] == 8 else shift_scene(s, delta)
              for s in before['scenes']]
    scenes[6]['end'] = begin
    scenes[8]['start'] = replacement['end']
    scenes[8]['words'][0]['start'] = max(scenes[8]['words'][0]['start'], replacement['end'])
    rep_cues = caption_cues(words)
    cues = [c for c in before['captions'] if c['end'] <= begin] + rep_cues + [
        dict(c, start=max(c['start'] + delta, replacement['end']), end=c['end'] + delta)
        for c in before['captions'] if c['start'] >= old['end'] - 1e-6]
    assert ' '.join(p['narration'] for p in script['scenes']) == ' '.join(c['text'] for c in cues)
    assert all(a['end'] <= b['start'] + .001 for a, b in zip(cues, cues[1:]))
    assert all(motion(replacement, begin + n/FPS)['hundreds'] == (746, 325) for n in range(nframes))
    new_scene = work / 'insert.mp4'
    command = ['ffmpeg', '-nostdin', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
        '-s', '1920x1080', '-r', str(FPS), '-i', 'pipe:0', '-c:v', 'libx264', '-crf', '18',
        '-preset', 'veryfast', '-threads', '2', '-pix_fmt', 'yuv420p', str(new_scene)]
    with subprocess.Popen(command, stdin=subprocess.PIPE) as encoder:
        for n in range(nframes):
            encoder.stdin.write(draw(replacement, rep_cues, begin + n/FPS).tobytes())
        encoder.stdin.close()
        assert encoder.wait() == 0, 'Correction scene failed to encode'
    graph = (f'[0:v]split=2[left][right];[left]trim=end_frame={first},setpts=PTS-STARTPTS[v0];'
        f'[right]trim=start_frame={stop},setpts=PTS-STARTPTS[v2];'
        '[v0][1:v][v2]concat=n=3:v=1:a=0[out]')
    movie = out / 'S102.mp4'
    capture(['-y', '-i', original, '-i', new_scene, '-i', master, '-filter_complex_threads', '2',
        '-filter_complex', graph, '-map', '[out]', '-map', '2:a', '-c:v', 'libx264', '-crf', '17',
        '-preset', 'veryfast', '-threads', '2', '-pix_fmt', 'yuv420p', '-r', str(FPS),
        '-fps_mode', 'cfr', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', movie])
    capture(['-i', movie, '-f', 'null', '-'])
    info = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_streams',
        '-show_format', '-of', 'json', str(movie)]))
    video = next(s for s in info['streams'] if s['codec_type'] == 'video')
    assert (video['width'], video['height'], video['r_frame_rate']) == (1920, 1080, '30/1')
    duration = float(info['format']['duration'])
    assert abs(duration - len(audio)/RATE) < .15
    digest = sha256(movie.read_bytes()).hexdigest()
    rows = [row for name in ('read-watch-practise.json', 'read-watch-practise-later.json')
            for row in json.loads((ROOT/'data'/name).read_text())['lessons'] if row.get('videoId') == LESSON]
    assert sorted(row['slot'] for row in rows) == [102, 296]
    bridge = next(row['bridge'] for row in rows if row['slot'] == 102)
    guide = dict(title=script['title'], seconds=duration, sha256=digest, bridge=bridge,
        chapters=[dict(title=p['heading'], start=round(s['start'], 3)) for p, s in zip(script['scenes'], scenes)],
        transcript=[p['narration'] for p in script['scenes']])
    vtt = 'WEBVTT\n\n' + '\n\n'.join(f"{stamp(c['start'])} --> {stamp(c['end'])}\n{c['text']}" for c in cues) + '\n'
    (out/'S102.vtt').write_text(vtt)
    write(out/'S102-guide.json', guide)
    draw(replacement, [], replacement['speech_end']).save(out/'S102-poster.jpg', quality=92)
    timeline = dict(id=LESSON, duration=duration, narration_reference=VOICE_SHA, model_revision=MODEL_REVISION,
        source_sha256=SOURCE_SHA, source_timing_method=before['timing_method'], scenes=scenes, captions=cues)
    with ZipFile(out/'S102-recording.zip', 'w') as archive:
        archive.writestr('script.json', json.dumps(script, ensure_ascii=False))
        archive.writestr('timeline.json', json.dumps(timeline, ensure_ascii=False))
        archive.writestr('captions.vtt', vtt)
        archive.write(master, 'narration.flac')
    encoded = waveform(movie)
    correlations = []
    for scene in scenes:
        start = round(scene['start'] * RATE)
        finish = min(round(scene['end'] * RATE), len(audio), len(encoded))
        rate = float(np.corrcoef(audio[start:finish:6], encoded[start:finish:6])[0, 1])
        assert rate >= .985, (scene['n'], rate)
        correlations.append(round(rate, 6))
    comparisons, worst = compare_pictures(movie, original, replacement, rep_cues, first, stop, nframes)
    qa = dict(sha256=digest, source_sha256=SOURCE_SHA, scene_replaced=8,
        corrected_scene_recognition=replacement['recognized_speech'], corrected_match_percent=match,
        scene_audio_correlations=correlations, full_duration_seconds=duration,
        picture_comparison_period_seconds=1, decoded_reference_comparisons=comparisons,
        largest_mean_picture_difference=worst, caption_count=len(cues), mathematical_check=maths,
        splice_frame_numbers=[first, stop], source_splice_maximum_amplitudes=boundaries,
        preserved_source_scenes=[n for n in range(1, 12) if n != 8],
        source_timing_method=before['timing_method'], caption_treatment='One stable phrase glyph layer in scene 8',
        editorial_acceptance='Pending full listen/watch and exact production device gates; this is a scoped correctness repair.')
    write(out/'S102-qa.json', qa)
    print(json.dumps(qa), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    parser.add_argument('--source', type=Path, help='Optional local copy of the pinned original movie')
    parser.add_argument('--whisper-model', default='base.en')
    args = parser.parse_args()
    make(args.output, args.source, args.whisper_model)
