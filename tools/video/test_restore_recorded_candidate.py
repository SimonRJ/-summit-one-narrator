"""Narrow provenance and nonreplacement guards for archived recording refreshes."""

from io import BytesIO
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from zipfile import ZipFile

import restore_recorded_candidate as restore


class RecordingRestoreGuards(unittest.TestCase):
    def setUp(self):
        manifest = json.loads((Path(__file__).parent / 'stable-caption-refresh-20261125.json').read_text())
        self.repository = manifest['repository']
        self.source = manifest['lessons']['S017']['source']
        self.run = {
            'head_sha': self.source['commit'], 'head_branch': self.source['branch'],
            'path': self.source['workflow'], 'event': 'push',
            'repository': {'full_name': self.repository}, 'head_repository': {'full_name': self.repository},
        }
        self.job = {'run_id': self.source['run'], 'head_sha': self.source['commit'],
                    'name': 'render', 'status': 'completed', 'conclusion': 'success'}
        self.artifacts = [{
            'id': self.source[key]['id'], 'name': self.source[key]['name'], 'expired': False,
            'digest': 'sha256:' + self.source[key]['sha256'],
            'size_in_bytes': self.source[key]['bytes'],
            'workflow_run': {'id': self.source['run'], 'head_sha': self.source['commit'],
                             'head_branch': self.source['branch']},
        } for key in ('candidate_artifact', 'provenance_artifact')]

    def test_wrong_bytes_are_rejected(self):
        expected = {'bytes': 3, 'sha256': restore.digest(b'old')}
        for data in (b'bad', b'long'):
            with self.assertRaises(AssertionError):
                restore.checked_bytes(data, expected, 'saved recording')

    def test_archive_must_contain_only_exact_named_members(self):
        stream = BytesIO()
        with ZipFile(stream, 'w') as archive:
            archive.writestr('timeline.json', b'{}')
            archive.writestr('../unexpected', b'not a member')
        expected = {'timeline.json': {'bytes': 2, 'sha256': restore.digest(b'{}')}}
        with self.assertRaises(AssertionError):
            restore.checked_archive(stream.getvalue(), expected, 'recording')

    def test_wrong_source_branch_stops_before_job_or_artifact_fetch(self):
        self.run['head_branch'] = 'different-production-branch'
        with patch.object(restore, 'api', return_value=self.run) as request:
            with self.assertRaises(AssertionError):
                restore.verify_actions_source(self.repository, self.source)
        self.assertEqual(request.call_count, 1)

    def test_unfinished_source_renderer_is_rejected(self):
        self.job.update(status='in_progress', conclusion=None)
        with patch.object(restore, 'api', side_effect=[self.run, self.job]) as request:
            with self.assertRaises(AssertionError):
                restore.verify_actions_source(self.repository, self.source)
        self.assertEqual(request.call_count, 2)

    def test_wrong_artifact_digest_is_rejected(self):
        self.artifacts[0]['digest'] = 'sha256:' + '0' * 64
        with patch.object(restore, 'api', side_effect=[self.run, self.job, *self.artifacts]):
            with self.assertRaises(AssertionError):
                restore.verify_actions_source(self.repository, self.source)

    def test_exact_successful_source_accepts_the_two_pinned_artifacts(self):
        with patch.object(restore, 'api', side_effect=[self.run, self.job, *self.artifacts]) as request:
            restore.verify_actions_source(self.repository, self.source)
        self.assertEqual(request.call_count, 4)

    def test_wrong_public_release_path_is_rejected_before_read(self):
        spec = {'source': {'kind': 'public_release', 'tag': 'pinned'},
                'assets': {'S017.mp4': {'url': 'https://example.invalid/other.mp4'}}}
        with self.assertRaises(AssertionError):
            restore.read_sources(self.repository, spec, Path('/does-not-exist'))

    def test_existing_different_file_prevents_any_new_write(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            (output / 'saved').write_bytes(b'keep')
            with self.assertRaises(AssertionError):
                restore.write_verified(output, {'new': b'not written', 'saved': b'changed'})
            self.assertFalse((output / 'new').exists())
            self.assertEqual((output / 'saved').read_bytes(), b'keep')


if __name__ == '__main__':
    unittest.main()
