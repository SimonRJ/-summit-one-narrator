"""Select checked-in scripts for a named edition and partition its Voice C recording sessions."""
import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def plan(ref):
    match = re.fullmatch(r'production/(voice|film)/([a-z0-9]+(?:-[a-z0-9]+)*)', ref)
    if not match:
        raise ValueError('Run on a named production/voice or production/film edition branch')
    phase, edition = match.groups()
    metadata = json.loads((ROOT / f'production/lesson-films/editions/{edition}.json').read_text())
    voices, films, used = [], [], set()
    for item in metadata['lessons']:
        slot, tag = item['id'], item['tag']
        if not re.fullmatch(r'S\d{3}', slot) or not re.fullmatch(r'[A-Za-z0-9-]+', tag) or slot in used:
            raise ValueError('Invalid or repeated edition entry')
        used.add(slot)
        script = json.loads((ROOT / f'production/scripts/{slot}.json').read_text())
        numbers = [scene['n'] for scene in script['scenes']]
        if not numbers or numbers != list(range(1, len(numbers) + 1)):
            raise ValueError(f'Invalid authored scene order for {slot}')
        for first in range(1, len(numbers) + 1, 3):
            voices.append({'slot': slot, 'first': first, 'last': min(first + 2, len(numbers))})
        films.append({'slot': slot, 'tag': tag, 'title': script['title']})
    run = metadata.get('recording_run', 0)
    if not films or (phase == 'film' and not (isinstance(run, int) and run > 0)):
        raise ValueError('The film phase needs its successful source recording run')
    return {'phase':phase,'recording_run':str(run),'voices':json.dumps(voices),'films':json.dumps(films)}


if __name__ == '__main__':
    with open(os.environ['GITHUB_OUTPUT'],'a') as output:
        for name,value in plan(os.environ['GITHUB_REF_NAME']).items():
            print(f'{name}={value}',file=output)
