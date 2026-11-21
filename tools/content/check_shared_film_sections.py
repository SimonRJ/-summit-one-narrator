"""Compare complete spoken sections in lesson guides before independently crediting films."""
import argparse
from collections import defaultdict
from itertools import combinations
import json
from pathlib import Path
import re


def overlaps(guides):
    sections = defaultdict(dict)
    for guide in guides:
        film = guide['id']
        for i, paragraph in enumerate(guide['transcript'], start=1):
            tokens = tuple(re.findall(r"[^\W_]+", paragraph.casefold()))
            if len(tokens) >= 16:
                sections[tokens][film] = i
    pairs = defaultdict(list)
    for locations in sections.values():
        for left, right in combinations(sorted(locations), 2):
            pairs[left, right].append((locations[left], locations[right]))
    return {pair: sorted(matches) for pair, matches in pairs.items() if len(matches) >= 2}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('guides', nargs='+', type=Path)
    args = parser.parse_args()
    guides = [json.loads(p.read_text()) for p in args.guides]
    if len({g['id'] for g in guides}) != len(guides) or len(guides) < 2:
        parser.error('Supply guides for at least two different lessons')
    repeated = overlaps(guides)
    for (a, b), matches in repeated.items():
        print(f'{a} and {b} share {len(matches)} long spoken sections: {matches}')
    if repeated:
        raise SystemExit(1)
    print(f'Checked {len(guides)} lesson transcripts for repeated sections.')
