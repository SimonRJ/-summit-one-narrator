"""Recorded phrases must not double their glyphs while the active word changes."""

from pathlib import Path
import sys
import unittest

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'production/lesson-films'))
from render_recorded import Board, caption


class StableCaptionTests(unittest.TestCase):
    def setUp(self):
        self.background = Image.new('RGB', (1280, 720), '#28313a')
        self.cue = {'text': 'Fifty four fails.', 'start': 0, 'end': 3}
        self.words = [dict(text=word, start=start, end=end) for word, start, end in (
            ('Fifty', .2, .8), ('four', .8, 1.5), ('fails.', 1.5, 2.5))]

    def draw(self, second):
        board = Board(self.background, 1)
        caption(board, self.cue, self.words, second)
        return board.image.tobytes()

    def test_phrase_pixels_do_not_morph_at_word_transitions(self):
        expected = self.draw(.5)
        self.assertNotEqual(expected, self.background.tobytes())
        for second in (.78, .85, 1.10, 1.49, 1.55, 2.2):
            self.assertEqual(self.draw(second), expected)

    def test_whole_phrase_is_hidden_outside_the_cue(self):
        for second in (-.1, 0, 3, 3.1):
            self.assertEqual(self.draw(second), self.background.tobytes())


if __name__ == '__main__':
    unittest.main()
