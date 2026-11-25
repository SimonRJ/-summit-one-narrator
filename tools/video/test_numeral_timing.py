"""Measured numeral repairs must be local, exact and independent of recording."""

from copy import deepcopy
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'production/t01-studio'))
import prepare_audio as timing


def heard(*items):
    return [SimpleNamespace(word=text, start=start, end=end) for text, start, end in items]


class NumeralTimingTests(unittest.TestCase):
    def frame_example(self):
        # Exact S017 scene-4 intervals, relative to the 60-second fixture origin.
        script = 'Compare counts. Twenty four rectangles contain A.'
        primary = heard(('Compare', 5.2, 5.7), ('counts.', 5.7, 6.02),
                        ('24', 7.14, 7.14), ('rectangles', 7.14, 7.78),
                        ('contain', 7.78, 8.10), ('A.', 8.10, 8.48))
        alternate = heard(('Compare', 5.2, 5.7), ('counts.', 5.7, 6.02),
                          ('Twenty', 6.68, 6.88), ('four', 6.88, 7.22),
                          ('rectangles', 7.22, 7.76), ('contain', 7.76, 8.14),
                          ('A.', 8.14, 8.48))
        words, match = timing.align(script, primary, 60, 69)
        return script, primary, words, alternate, match

    def test_measured_number_and_overlapping_neighbor_only_are_replaced(self):
        script, primary, words, alternate, match = self.frame_example()
        original = deepcopy(words)
        repaired, reports = timing.repair_collapsed_numerals(
            script, primary, words, alternate, 60, 69, match)
        self.assertEqual(words, original)
        self.assertEqual(repaired[:2], words[:2])
        self.assertEqual(repaired[5:], words[5:])
        self.assertAlmostEqual(repaired[2]['start'], 66.68)
        self.assertAlmostEqual(repaired[3]['end'], 67.22)
        self.assertAlmostEqual(repaired[4]['start'], 67.22)
        self.assertEqual(reports[0]['replaced_word_indices'], [2, 3, 4])
        self.assertEqual(reports[0]['adjoining_words'], ['rectangles'])
        self.assertFalse(any(a['end'] > b['start'] for a, b in zip(repaired, repaired[1:])))
        self.assertAlmostEqual(timing.caption_cues(repaired)[1]['start'], 66.68)

    def test_all_terms_of_a_compound_must_match(self):
        prefix = 'Inspect the written parcel labels carefully before choosing the next number'
        script = prefix + ' three hundred and forty-four now.'
        primary = heard(*[(word, i * .2, (i + 1) * .2)
                          for i, word in enumerate(prefix.split())],
                        ('344', 3.2, 3.2), ('now.', 4.0, 4.3))
        alternate = heard(*[(word, i * .2, (i + 1) * .2)
                            for i, word in enumerate(prefix.split())],
                          ('three', 2.6, 2.8), ('hundred', 2.8, 3.0),
                          ('and', 3.0, 3.1), ('forty', 3.1, 3.3),
                          ('five', 3.3, 3.7), ('now.', 4.0, 4.3))
        words, _ = timing.align(script, primary, 0, 5)
        original = deepcopy(words)
        with self.assertRaisesRegex(ValueError, 'unmatched term'):
            timing.repair_collapsed_numerals(script, primary, words, alternate, 0, 5, 90)
        self.assertEqual(words, original)

    def test_existing_positive_numbers_and_nonnumeric_zero_do_not_trigger_a_pass(self):
        script = 'Check twenty four rectangles.'
        primary = heard(('Check', 0, 0), ('24', .2, .6), ('rectangles.', .6, 1.2))
        words, match = timing.align(script, primary, 0, 2)
        with patch.object(timing, 'transcribe') as transcribe:
            result, reports = timing.repair_numeral_timing(
                object(), np.zeros(12), script, primary, words, match, 0, 2)
        transcribe.assert_not_called()
        self.assertIs(result, words)
        self.assertEqual(reports, [])

    def test_reviewed_positive_number_extends_a_truncated_caption(self):
        script = 'Labels include three hundred and twenty four, then pause.'
        primary = heard(('Labels', 0, .3), ('include', .3, .6),
                        ('324,', .6, 1.2), ('then', 2.4, 2.6), ('pause.', 2.6, 3))
        alternate = heard(('Labels', 0, .3), ('include', .3, .6),
                          ('three', .6, .8), ('hundred', .8, 1.1),
                          ('and', 1.1, 1.2), ('twenty', 1.2, 1.4),
                          ('four,', 1.4, 1.9), ('then', 2.4, 2.6), ('pause.', 2.6, 3))
        words, match = timing.align(script, primary, 0, 4)
        repaired, reports = timing.repair_measured_numeral_groups(
            script, words, alternate, 0, 4, match, [(2, 7)])
        self.assertEqual(repaired[:2], words[:2])
        self.assertEqual(repaired[7:], words[7:])
        self.assertEqual(repaired[6]['end'], 1.9)
        self.assertEqual(reports[0]['original_end'], 1.2)
        self.assertEqual(timing.collapsed_numeral_groups(words, primary, 0), [])

    def test_reviewed_group_cannot_replace_ordinary_prose(self):
        script, primary, words, alternate, match = self.frame_example()
        with self.assertRaisesRegex(ValueError, 'not a numeral'):
            timing.repair_measured_numeral_groups(script, words, alternate, 60, 69, match, [(0, 2)])

    def test_compound_number_is_not_split_across_caption_phrases(self):
        text = ('The four labels are three hundred and twenty four, three hundred and forty four, '
                'three hundred and fifty four, and three hundred and eighty four.')
        words = [{'text': word, 'start': index*.2, 'end': (index+1)*.2}
                 for index, word in enumerate(text.split())]
        cues = timing.caption_cues(words)
        self.assertEqual(' '.join(c['text'] for c in cues), text)
        for number in ('three hundred and twenty four,', 'three hundred and forty four,',
                       'three hundred and fifty four,', 'three hundred and eighty four.'):
            self.assertEqual(sum(number in cue['text'] for cue in cues), 1)

    def test_numeral_repair_cannot_choose_a_distant_occurrence(self):
        script, primary, words, alternate, match = self.frame_example()
        alternate[2].start, alternate[2].end = 6.1, 6.3
        alternate[3].start, alternate[3].end = 6.3, 6.5
        with self.assertRaisesRegex(ValueError, 'original collapsed anchor'):
            timing.repair_collapsed_numerals(script, primary, words, alternate, 60, 69, match)

    def test_context_expansion_is_bounded_and_failure_leaves_input_intact(self):
        script = 'Count twenty four red blue green shapes now.'
        primary = heard(('Count', 0, .5), ('24', 2, 2), ('red', 2, 2.1),
                        ('blue', 2.1, 2.2), ('green', 2.2, 2.3),
                        ('shapes', 3.5, 4), ('now.', 4, 4.5))
        alternate = heard(('Count', 0, .5), ('twenty', 1.3, 1.7),
                          ('four', 1.7, 2.2), ('red', 2.2, 2.5),
                          ('blue', 2.5, 2.8), ('green', 2.8, 3.1),
                          ('shapes', 3.5, 4), ('now.', 4, 4.5))
        words, match = timing.align(script, primary, 0, 5)
        original = deepcopy(words)
        with self.assertRaisesRegex(ValueError, 'right context bound'):
            timing.repair_collapsed_numerals(script, primary, words, alternate, 0, 5, match)
        self.assertEqual(words, original)

    def test_uncertain_word_form_pass_fails_closed(self):
        script, primary, words, alternate, match = self.frame_example()
        alternate[-1].word = 'something else entirely'
        with self.assertRaisesRegex(ValueError, 'recognition needs review'):
            timing.repair_collapsed_numerals(script, primary, words, alternate, 60, 69, match)

    def test_lexical_mask_preserves_default_timestamp_and_control_tokens(self):
        tokenizer = SimpleNamespace(token_to_id=lambda word: 100,
            get_vocab=lambda: {'one': 1, '24': 2, ' 344': 3, '<|endoftext|>': 100,
                              '<|speaker_1|>': 101, '<|0.00|>': 102})
        self.assertEqual(timing.numeral_suppression_tokens(tokenizer), [-1, 2, 3])

    def test_one_secondary_pass_preserves_waveform_and_requests_no_recording(self):
        script, primary, words, alternate, match = self.frame_example()
        waveform = np.linspace(-.1, .1, 30, dtype=np.float32)
        original = waveform.copy()
        model = object()
        with patch.object(timing, 'transcribe', return_value=alternate) as transcribe, \
                patch.object(timing.sf, 'write', side_effect=AssertionError('Must not write audio')):
            timing.repair_numeral_timing(model, waveform, script, primary, words, match, 60, 69)
        transcribe.assert_called_once_with(model, waveform, number_words=True)
        np.testing.assert_array_equal(waveform, original)


if __name__ == '__main__':
    unittest.main()
