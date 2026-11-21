"""Compare whole scene transcripts from the same public guides the introduction player selects."""
import argparse
import csv
import json
import subprocess
import sys
from collections import defaultdict
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def catalogue_json(ref, name):
    raw = subprocess.check_output(['git', 'show', f'{ref}:data/{name}'], cwd=ROOT)
    return json.loads(raw)


def load_guides(ref, recorded_studies):
    guides = {}
    for item in catalogue_json(ref, 'lesson-intros-live.json')['entries']:
        if item['status'] not in ('checking', 'verified'):
            continue
        identifier = item['id']
        suffix = '-Illustrated' if item.get('detailsEdition') == 1 else ''
        guide = catalogue_json(ref, f'lesson-intros/{identifier}{suffix}.json')
        guides[identifier] = item['status'], guide['transcript']
    for identifier, guide in recorded_studies['lessons'].items():
        guides[identifier] = 'recorded study', guide['transcript']
    return guides


def shared_scenes(guides):
    occurrences = defaultdict(lambda: defaultdict(list))
    for identifier, (_, script) in sorted(guides.items()):
        for index, scene in enumerate(script, start=1):
            text = ' '.join(scene.split())
            if len(text.split()) >= 20:
                occurrences[text][identifier].append(index)
    pairs = defaultdict(list)
    for text, locations in occurrences.items():
        for left, right in combinations(sorted(locations), 2):
            pairs[left, right].append((locations[left], locations[right], len(text.split())))
    for (left, right), matches in sorted(pairs.items()):
        if len(matches) < 2:
            continue
        matches.sort()
        left_numbers = ' '.join(str(i) for group, _, _ in matches for i in group)
        right_numbers = ' '.join(str(i) for _, group, _ in matches for i in group)
        yield (left, right, guides[left][0], guides[right][0], len(matches), left_numbers,
               right_numbers, sum(words for _, _, words in matches))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('catalog_ref', help='Revision of the public lesson-intro-catalog branch')
    parser.add_argument('--recorded', type=Path, default=ROOT / 'data/recorded-studies.json')
    args = parser.parse_args()
    guides = load_guides(args.catalog_ref, json.loads(args.recorded.read_text()))
    writer = csv.writer(sys.stdout, lineterminator='\n')
    writer.writerow(('left', 'right', 'left_source_status', 'right_source_status', 'shared_sections',
                     'left_scene_numbers', 'right_scene_numbers', 'shared_word_count'))
    writer.writerows(shared_scenes(guides))


if __name__ == '__main__':
    main()
