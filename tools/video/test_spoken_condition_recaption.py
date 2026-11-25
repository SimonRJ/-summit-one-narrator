"""Pins and stream geometry for caption-only refreshes of existing recordings."""

from copy import deepcopy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'production/lesson-films'))
import recaption_spoken_condition as recaption


class SpokenConditionCaptionTests(unittest.TestCase):
    def recording(self, lesson, narration):
        number = recaption.POLICIES[lesson]['scene_number']
        scenes = [dict(n=n, start=(n-1)*10, end=n*10, words=[{'text': 'Earlier.'}])
                  for n in range(1, 12)]
        parts = [dict(n=n, narration='Earlier.') for n in range(1, 12)]
        parts[number-1]['narration'] = narration
        scenes[number-1]['words'] = [{'text': word} for word in narration.split()]
        return ({'id': lesson, 'narration_reference':
                 '0f3304a393ee504e9fa22537267ac03f150569a5fab0859616f261d009513362',
                 'scenes': scenes}, {'id': lesson, 'scenes': parts})

    def test_s019_only_selects_the_approved_leftmost_pair_scene(self):
        narration = 'In the top row, cross out the two squares farthest to the left.'
        timeline, script = self.recording('S019', narration)
        scene, first, stop = recaption.selected_scene('S019', timeline, script)
        self.assertEqual((scene['n'], first, stop), (5, 1200, 1500))
        timeline, script = self.recording('S019', narration.replace('farthest to the left', 'in the middle'))
        with self.assertRaises(AssertionError):
            recaption.selected_scene('S019', timeline, script)

    def test_original_s020_policy_and_ninth_scene_remain_available(self):
        self.assertEqual(recaption.rebuild.__defaults__, ('S020',))
        self.assertEqual(recaption.POLICIES['S020']['source_sha256'],
                         'fa00a38665821402f0a2060c40b4aa7ae4b89632609862a80607f39a4cc5006f')
        timeline, script = self.recording('S020', 'The next exponent is forty-nine.')
        scene, first, stop = recaption.selected_scene('S020', timeline, script)
        self.assertEqual((scene['n'], first, stop), (9, 2400, 2700))

    def stream_fixture(self):
        return {'format': {'duration': '142.330000'}, 'streams': [
            {'codec_type': 'video', 'codec_name': 'h264', 'time_base': '1/15360',
             'start_time': '0.000000', 'duration': '142.300000', 'nb_frames': '4269',
             'width': 1920, 'height': 1080, 'r_frame_rate': '30/1', 'pix_fmt': 'yuv420p'},
            {'codec_type': 'audio', 'codec_name': 'aac', 'time_base': '1/48000',
             'start_time': '0.000000', 'duration': '142.330000', 'nb_frames': '6673',
             'sample_rate': '48000', 'channels': 1}]}

    def test_video_tail_is_preserved_without_rounding_audio_duration(self):
        source = self.stream_fixture()
        recaption.check_stream_identity(source, deepcopy(source))
        changed = deepcopy(source)
        changed['streams'][0].update(nb_frames='4270', duration='142.333333')
        with self.assertRaises(AssertionError):
            recaption.check_stream_identity(source, changed)

    def test_audio_offset_or_time_base_change_is_rejected(self):
        source = self.stream_fixture()
        for key, value in [('start_time', '0.021333'), ('time_base', '1/44100')]:
            changed = deepcopy(source)
            changed['streams'][1][key] = value
            with self.assertRaises(AssertionError):
                recaption.check_stream_identity(source, changed)


if __name__ == '__main__':
    unittest.main()
