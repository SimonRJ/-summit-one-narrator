"""Apply the reviewed positive twenty-four timing to its exact saved S017 take.

This source-specific step uses archived scene-relative measurements. It does
not run a recognizer, alter audio, broaden automatic repair or shift a scene.
"""

import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'production/t01-studio'))
from prepare_audio import repair_measured_numeral_groups


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def refine(directory, report_path):
    plan_path = Path(__file__).with_name('s017-number-timing.json')
    plan_bytes = plan_path.read_bytes()
    plan = json.loads(plan_bytes)
    script_bytes = (ROOT / 'production/scripts/S017.json').read_bytes()
    if sha256(script_bytes) != plan['script_sha256']:
        raise ValueError('S017 reviewed timing belongs to a different authored script')
    script = json.loads(script_bytes)
    part = next(scene for scene in script['scenes'] if scene['n'] == plan['scene'])
    if sha256(part['narration'].encode()) != plan['narration_sha256']:
        raise ValueError('S017 reviewed scene narration differs')
    raw = directory.parent / f"S017-{plan['scene']:02}.wav"
    if sha256(raw.read_bytes()) != plan['source_wav_sha256']:
        raise ValueError('S017 reviewed timing requires the exact preserved raw take')
    metadata = json.loads(raw.with_suffix('.json').read_text())
    if (metadata['narration_sha256'] != plan['narration_sha256']
            or metadata['sample_rate_hz'] != plan['source_rate_hz']
            or abs(metadata['duration_seconds'] - plan['source_duration_seconds']) > 1e-6):
        raise ValueError('S017 raw take metadata differs from the reviewed source')

    path = directory / 'timeline.json'
    timeline = json.loads(path.read_text())
    before = deepcopy(timeline)
    if timeline['id'] != 'S017':
        raise ValueError('This measured correction is only for S017')
    scene = next(scene for scene in timeline['scenes'] if scene['n'] == plan['scene'])
    words = scene['words']
    if ' '.join(word['text'] for word in words) != part['narration']:
        raise ValueError('S017 timed words differ from the complete authored scene')
    start, end = scene['start'], scene['speech_end']
    if abs(end - start - plan['source_duration_seconds']) > 1e-6:
        raise ValueError('S017 scene has been stretched or replaced')
    for (first, stop), text in zip(plan['groups'], plan['expected_group_text']):
        if ' '.join(word['text'] for word in words[first:stop]) != text:
            raise ValueError('S017 reviewed numeral indices no longer identify the same words')
    alternate = [SimpleNamespace(**word) for word in plan['word_forms']]
    repaired, reports = repair_measured_numeral_groups(
        part['narration'], words, alternate, start, end,
        scene['match_percent'], [tuple(group) for group in plan['groups']])
    cue = next(cue for cue in timeline['captions'] if cue['text'] == plan['reviewed_caption_text'])
    for first, stop in plan['groups']:
        if not cue['start'] <= repaired[first]['start'] < repaired[stop-1]['end'] <= cue['end']:
            raise ValueError('S017 measured compound is not fully inside its retained phrase cue')
    changed = [index for index, (old, new) in enumerate(zip(words, repaired)) if old != new]
    scene['words'] = repaired
    scene['reviewed_numeral_timing'] = {
        'source_wav_sha256': plan['source_wav_sha256'],
        'plan_sha256': sha256(plan_bytes),
        'method': 'source-bound archived word-form measurements',
        'repairs': reports,
    }
    if timeline['captions'] != before['captions']:
        raise ValueError('S017 phrase cues must remain unchanged')
    for old, new in zip(before['scenes'], timeline['scenes']):
        if old['n'] != plan['scene'] and old != new:
            raise ValueError('S017 refinement changed an unrelated scene')
    audit = {
        'lesson': 'S017', 'scene': plan['scene'], 'plan_sha256': sha256(plan_bytes),
        'source_wav_sha256': plan['source_wav_sha256'], 'repairs': reports,
        'changed_word_indices': changed, 'caption_cues_unchanged': True,
        'vtt_unchanged': True, 'audio_unchanged': True,
        'automatic_repair_rule_unchanged': True, 'final_editorial_credit': False,
    }
    # Only timing and its audit are written, after all source/overlap checks pass.
    path.write_text(json.dumps(timeline, indent=2) + '\n')
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(audit, indent=2) + '\n')
    return audit


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    parser.add_argument('--report', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(refine(args.directory, args.report), indent=2))
