"""Per-problem lesson content and difficulty assessments from the Upper Primary audit."""
import json
from functools import lru_cache
from pathlib import Path

REVIEWED_DIR = Path(__file__).with_name('reviewed')
ATTEMPTED = {'O001T', 'O001X', 'O002T', 'O002X'}


@lru_cache(maxsize=1)
def reviewed_lessons():
    reviewed = {}
    for path in sorted(REVIEWED_DIR.glob('*.json')):
        for row in json.loads(path.read_text()):
            pid = row['id']
            if pid in reviewed:
                raise ValueError(f'Duplicate reviewed lesson problem: {pid}')
            reviewed[pid] = row
    return reviewed
