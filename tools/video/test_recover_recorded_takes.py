"""Provenance and independence gates for recovery of an existing recording."""

from copy import deepcopy
from io import BytesIO
import json
from pathlib import Path
import unittest
from unittest.mock import patch
from zipfile import ZipFile

import recover_recorded_takes as recovery


class RecordedTakeRecoveryTests(unittest.TestCase):
    def setUp(self):
        self.spec = json.loads(Path(__file__).with_name('s015-recorded-takes.json').read_text())
        s = self.spec
        self.voice = {'head_sha': s['voice_commit'], 'head_branch': s['voice_branch'],
                      'path': s['voice_workflow'], 'event': 'push', 'status': 'in_progress',
                      'conclusion': None, 'repository': {'full_name': s['repository']},
                      'head_repository': {'full_name': s['repository']}}
        self.old = {'head_sha': s['original_render_commit'], 'path': s['original_render_workflow'],
                    'status': 'completed', 'conclusion': 'failure'}
        self.jobs = {'total_count': 10, 'jobs': [
            {'name': f"voice (S015, {n})", 'status': 'completed', 'conclusion': 'success'}
            for n in range(1, 9)] + [
            {'name': f"voice (S017, {n})", 'status': 'queued', 'conclusion': None} for n in (7, 8)]}
        self.artifacts = {'total_count': 8, 'artifacts': [
            {'id': a['id'], 'name': a['name'], 'expired': False,
             'digest': 'sha256:' + a['sha256'], 'workflow_run': {'id': s['voice_run']}}
            for a in s['artifacts']]}

    def check_source(self):
        responses = [self.voice, self.old, self.jobs, self.artifacts]
        with patch.object(recovery, 'api', side_effect=responses):
            recovery.verify_source(self.spec)

    def test_completed_lesson_does_not_wait_for_queued_sibling(self):
        self.check_source()

    def test_incomplete_own_scene_is_rejected(self):
        self.jobs['jobs'][7].update(status='queued', conclusion=None)
        with self.assertRaisesRegex(AssertionError, 'Missing successful voice jobs'):
            self.check_source()

    def test_active_original_renderer_is_rejected(self):
        self.old.update(status='in_progress', conclusion=None)
        with self.assertRaisesRegex(AssertionError, 'do not duplicate'):
            self.check_source()

    def test_wrong_commit_and_expired_artifact_are_rejected(self):
        self.voice['head_sha'] = '0' * 40
        with self.assertRaisesRegex(AssertionError, 'source commit'):
            self.check_source()
        self.voice['head_sha'] = self.spec['voice_commit']
        self.artifacts['artifacts'][0]['expired'] = True
        with self.assertRaises(AssertionError):
            self.check_source()

    def archive(self, *, voice=None, extra=False):
        narration = 'Four parcels fit in a bundle.'
        item = deepcopy(self.spec['artifacts'][0])
        meta = {'lesson': 'S015', 'scene': 1, 'narration_sha256': recovery.digest(narration.encode()),
                'reference_sha256': voice or self.spec['voice_reference'],
                'model_revision': self.spec['model_revision'], 'natural_speed': True,
                'sample_rate_hz': 48000, 'duration_seconds': 5}
        buf = BytesIO()
        with ZipFile(buf, 'w') as z:
            z.writestr('S015-01.json', json.dumps(meta))
            z.writestr('S015-01.wav', b'fixture audio payload')
            if extra:
                z.writestr('../unexpected.txt', 'must not be extracted')
        data = buf.getvalue()
        item['sha256'] = recovery.digest(data)
        return item, data, narration

    def test_archive_bytes_and_script_are_bound(self):
        item, data, narration = self.archive()
        self.assertEqual(set(recovery.checked_take(self.spec, item, data, narration)),
                         {'S015-01.json', 'S015-01.wav'})
        with self.assertRaisesRegex(AssertionError, 'archive digest'):
            recovery.checked_take(self.spec, item, data + b'changed', narration)
        with self.assertRaisesRegex(AssertionError, 'Script/take mismatch'):
            recovery.checked_take(self.spec, item, data, narration + ' Changed.')

    def test_wrong_voice_and_extra_archive_members_are_rejected(self):
        item, data, narration = self.archive(voice='wrong voice')
        with self.assertRaisesRegex(AssertionError, 'Wrong narration voice'):
            recovery.checked_take(self.spec, item, data, narration)
        item, data, narration = self.archive(extra=True)
        with self.assertRaisesRegex(AssertionError, 'unexpected archive members'):
            recovery.checked_take(self.spec, item, data, narration)


if __name__ == '__main__':
    unittest.main()
