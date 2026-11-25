"""S102: a reversible tens/units swap, with the hundreds place held fixed."""
import math

from render_recorded import Board, background
from stage import Moment

BACKGROUND = ('#172b38', '#101e2c')
WHITE, BLUE, GOLD, MINT = '#f5f1e9', '#85b5e6', '#edc175', '#9cdbbc'
PAIRS = ((153, 135), (243, 234), (333, 333), (423, 432), (513, 531))


def swap_tens_units(number):
    hundreds, tail = divmod(number, 100)
    tens, units = divmod(tail, 10)
    return 100 * hundreds + 10 * units + tens


def check_maths():
    allowed = [n for n in range(100, 600) if n % 9 == 0]
    ones = [n for n in allowed if n % 10 == 3]
    tens = [n for n in allowed if n // 10 % 10 == 3]
    assert ones == [a for a, _ in PAIRS]
    assert tens == sorted(b for _, b in PAIRS)
    assert {swap_tens_units(n) for n in ones} == set(tens)
    for n in allowed:
        partner = swap_tens_units(n)
        assert partner in allowed and partner // 100 == n // 100
        assert sum(map(int, str(partner))) == sum(map(int, str(n)))
        assert swap_tens_units(partner) == n
    assert swap_tens_units(153) == 135 and swap_tens_units(333) == 333
    assert [sum(str(n)[i] == '3' for n in allowed) for i in (2, 1, 0)] == [5, 5, 11]
    assert sum(str(n).count('3') for n in allowed) == 21
    return {'range': [100, 599], 'divisor': 9, 'pairs': PAIRS,
            'ones': 5, 'tens': 5, 'hundreds': 11, 'total': 21}


def motion(scene, second):
    cue = Moment(scene, second)
    forward = cue.reveal('swap the tens and units digits', 1.4)
    backward = cue.reveal('Swapping back recovers the original', 1.4)
    progress = max(0, forward - backward)
    return {'hundreds': (746, 325),
            'tens': (938 + 166 * progress, 325 - 52 * math.sin(math.pi * progress)),
            'units': (1104 - 166 * progress, 325 + 52 * math.sin(math.pi * progress)),
            'progress': progress}


def draw(scene, cues, second, scale=1.5):
    board = Board(background(*BACKGROUND, scale), scale)
    cue = Moment(scene, second)
    board.label('Keep the hundreds digit fixed', 64, 74, 44, WHITE, bold=True)
    board.label('Multiples of 9  ·  100 through 599', 64, 124, 25, BLUE)
    board.line([(64, 155), (1216, 155)], '#496174', 2)

    board.box(60, 182, 546, 416, fill='#203343')
    board.text('Ones digit 3', 194, 215, 28, GOLD, bold=True)
    shown = cue.reveal('swap the tens and units digits', 1.4)
    board.text('Tens digit 3', 468, 215, 28, BLUE, bold=True, opacity=shown)
    repeated = cue.reveal('Three hundred and thirty-three', .6)
    for index, (before, after) in enumerate(PAIRS):
        y = 271 + 56 * index
        visible = cue.reveal('For hundreds digits one through five', .4, index * .34)
        if before == 333:
            board.box(79, y - 25, 508, 49, fill='#405252', edge=MINT, opacity=repeated)
        for j, digit in enumerate(str(before)):
            board.text(digit, 160 + j * 34, y, 37, GOLD if j == 2 else WHITE,
                       bold=True, opacity=visible)
        board.text('↔', 332, y, 32, MINT, opacity=min(visible, shown))
        for j, digit in enumerate(str(after)):
            board.text(digit, 434 + j * 34, y, 37, BLUE if j == 1 else WHITE,
                       bold=True, opacity=min(visible, shown))
    total = cue.reveal('The ones and tens columns contribute five each')
    board.text('5 occurrences', 194, 569, 27, GOLD, bold=True, opacity=total)
    board.text('5 occurrences', 468, 569, 27, BLUE, bold=True, opacity=total)

    for x, label in ((746, 'Hundreds'), (938, 'Tens'), (1104, 'Units')):
        board.text(label, x, 215, 25, MINT if label == 'Hundreds' else WHITE, bold=True)
        board.box(x - 54, 271, 108, 108, edge=MINT if label == 'Hundreds' else '#496174',
                  fill='#203343', stroke=3)
    positions = motion(scene, second)
    board.text('1', *positions['hundreds'], 66, MINT, bold=True)
    board.text('5', *positions['tens'], 66, BLUE, bold=True)
    board.text('3', *positions['units'], 66, GOLD, bold=True)
    fixed = cue.reveal('keep the hundreds digit fixed')
    board.text('stays 1', 746, 410, 25, MINT, bold=True, opacity=fixed)
    board.text('153 ↔ 135', 1008, 439, 38, WHITE, bold=True, opacity=shown)
    unchanged = cue.reveal('The digit sum and hundreds range are unchanged')
    board.text('1 + 5 + 3 = 1 + 3 + 5 = 9', 928, 497, 29, GOLD, opacity=unchanged)
    board.text('Both stay in the same hundred.', 928, 541, 26, WHITE, opacity=unchanged)
    board.text('333: one match in each column', 928, 583, 25, MINT,
               bold=True, opacity=repeated)
    for cap in cues:
        if cap['start'] <= second < cap['end']:
            # Keep one stable glyph layer throughout; no regular/bold cross-fade.
            board.caption(cap, second)
            break
    return board.image
