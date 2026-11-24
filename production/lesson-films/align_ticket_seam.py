"""Time the ticket and domino workshops’ authored captions against their recorded Voice C speech."""
import argparse
import json
from pathlib import Path
import re
import subprocess
import sys

from pocketsphinx import Decoder

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 't01-studio'))
from prepare_audio import stamp


def heard_words(path, words):
    pcm = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', str(path), '-ar', '16000',
                                   '-ac', '1', '-f', 's16le', 'pipe:1'])
    decoder = Decoder(loglevel='ERROR')
    terms = [re.sub(r'[^a-z]', '', word.lower()) for word in words]
    pronunciation={'tiling':'T AY L IH NG','tilings':'T AY L IH NG Z','neighbouring':'N EY B ER IH NG','colour':'K AH L ER'}
    for term,sound in pronunciation.items():
        if not decoder.lookup_word(term): decoder.add_word(term,sound)
    decoder.set_align_text(' '.join(terms))
    decoder.start_utt()
    decoder.process_raw(pcm, False, True)
    decoder.end_utt()
    segments = [s for s in decoder.seg() if not s.word.startswith(('<', '['))]
    names = [re.sub(r'\(\d+\)$', '', s.word) for s in segments]
    if names != terms:
        raise ValueError(f'{path.name}: forced alignment did not cover the authored words')
    return [(s.start_frame / 100, (s.end_frame + 1) / 100) for s in segments]


def prepare(film, source, build):
    timeline = json.loads((build / 'timeline.json').read_text())
    script = json.loads((build / 'script.json').read_text())
    groups = json.loads((HERE / 'ticket_seam_captions.json').read_text())[film]
    captions = []
    for scene, part, chapter in zip(timeline['scenes'], script['scenes'], groups, strict=True):
        words = part['narration'].split()
        if ' '.join(chapter.split('|')) != part['narration']:
            raise ValueError(f"{film} scene {scene['n']}: caption text differs from narration")
        origin = 0.6 if scene['n'] == 1 else scene['start']
        intervals = heard_words(source / f"{film}-{scene['n']:02}.wav", words)
        for (start, end), word, text in zip(intervals, scene['words'], words, strict=True):
            assert word['text'] == text and end > start
            word.update(start=round(origin+start, 3), end=round(origin+end, 3))
        cursor = 0
        for line in chapter.split('|'):
            count = len(line.split()); phrase = scene['words'][cursor:cursor+count]; cursor += count
            start = phrase[0]['start']; end = phrase[-1]['end']
            following = scene['words'][cursor]['start'] if cursor < len(words) else scene['end']-.06
            stop = min(following, max(end+.08, start+.85))
            if stop <= start:
                raise ValueError(f'{film}: empty caption for {line}')
            captions.append(dict(start=start, end=round(stop, 3), text=line))
    timeline['captions'] = captions
    timeline['word_timing_method'] = 'PocketSphinx transcript-constrained alignment of the checked 48 kHz Voice C scene takes'
    (build / 'timeline.json').write_text(json.dumps(timeline, indent=2)+'\n')
    (build / 'captions.vtt').write_text('WEBVTT\n\n'+'\n\n'.join(
        f"{stamp(c['start'])} --> {stamp(c['end'])}\n{c['text']}" for c in captions)+'\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('film', choices=('S095','S097'))
    parser.add_argument('scenes', type=Path)
    parser.add_argument('build', type=Path)
    args = parser.parse_args()
    prepare(args.film, args.scenes, args.build)
