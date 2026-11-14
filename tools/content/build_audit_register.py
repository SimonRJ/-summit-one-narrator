"""Build the ID, verification method and difficulty register for the lesson bank."""
import csv
import hashlib
import json
import tempfile
from collections import Counter
from pathlib import Path

from audit_all_lessons import map_course, numeric_skeleton
from build_original_lessons import build
from curated_batch2 import B as BATCH2
from curated_data import data_revisit
from curated_spatial import spatial_revisit
from reviewed_lessons import ATTEMPTED, reviewed_lessons

ROOT = Path(__file__).resolve().parents[2]
FIGURES = ('spatialDiagram', 'dataDisplay', 'geometryDiagram', 'cuboidDiagram', 'pictogram')
EARLIER_LATE_BAND = {
    'O097X', 'O127X', 'O159X', 'O209T', 'O211X', 'O218T', 'O230X', 'O250X',
    'O289X', 'O309X', 'O321X', 'O334X', 'O349X', 'O359T', 'O359X',
}
EARLIER_MIDDLE_BAND = {
    'O075T', 'O082T', 'O082X', 'O094T', 'O095T', 'O104T', 'O107T', 'O107X',
    'O120T', 'O124T', 'O127T', 'O135T', 'O139T', 'O141T', 'O141X', 'O148T',
    'O167T', 'O173X', 'O180T', 'O183T', 'O198T', 'O211T', 'O215X', 'O226T',
    'O230T', 'O232T', 'O232X', 'O258T', 'O274T', 'O289T', 'O317T', 'O321T',
    'O323T', 'O323X', 'O330T', 'O355T',
}


def main():
    reviewed = reviewed_lessons()
    with tempfile.TemporaryDirectory() as temporary:
        directory = Path(temporary)
        build(map_course(), directory, public_only=True)
        rows = json.loads((directory / 'lesson-prompts.json').read_text())
        manifest = json.loads((directory / 'lesson-manifest.json').read_text())['items']
    entries = {item['id']: item for item in manifest}
    shapes = Counter(numeric_skeleton(row['prompt']) for row in rows)
    register = []
    for row in rows:
        pid = row['id']
        item = entries[pid]
        skill, role, visit = item['skill'], item['role'], item['visit']
        if pid in reviewed:
            check = 'check_reviewed_lessons.py'
            band = reviewed[pid]['band']
        else:
            if spatial_revisit(skill, visit, role):
                check = 'check_curated_spatial.py'
            elif data_revisit(skill, visit, role):
                check = 'check_curated_data.py'
            elif (skill, role, visit) in BATCH2:
                check = 'check_curated_batch2.py'
            else:
                raise ValueError(f'{pid} has no independent check')
            if pid in EARLIER_LATE_BAND:
                band = '26–30'
            elif pid in EARLIER_MIDDLE_BAND:
                band = '11–20'
            else:
                band = '21–25'

        if pid in ATTEMPTED:
            action = 'Retained saved version'
        elif pid in reviewed:
            action = 'Revised in full-bank audit'
        else:
            action = 'Retained after earlier audit'
        register.append({
            'id': pid, 'session': item['session'], 'technique': skill, 'role': role, 'visit': visit,
            'difficulty': row['difficulty'],
            'upper_primary_band': band,
            'content_fingerprint': hashlib.md5(row['prompt'].encode()).hexdigest()[:10],
            'assurance_level': 'independent', 'verification_method': check,
            'same_structure_elsewhere': shapes[numeric_skeleton(row['prompt'])] - 1,
            'individually_reviewed': 'yes', 'has_recorded_attempts': 'yes - frozen' if pid in ATTEMPTED else 'no',
            'diagram': 'phone-width fixture' if any(key in item for key in FIGURES) else 'text only',
            'status': action,
        })

    assert len(register) == len(shapes) == 566
    path = ROOT / 'docs/content-audit-register.csv'
    with path.open('w', encoding='utf-8', newline='') as output:
        writer = csv.DictWriter(output, fieldnames=list(register[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(register)
    print(json.dumps({
        'problems': len(register),
        'distinct_number_normalised_stems': len(shapes),
        'status': Counter(item['status'] for item in register),
        'estimated_upper_primary_bands': Counter(item['upper_primary_band'] for item in register),
        'figures': sum(item['diagram'] != 'text only' for item in register),
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
