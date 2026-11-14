"""Enumerate the spatial revisits from their stated geometry and tiling rules."""
from functools import lru_cache
from itertools import combinations, product
from pathlib import Path
import json
import tempfile

from audit_all_lessons import map_course
from build_original_lessons import build
from curated_spatial import RECTANGLES, TILINGS


def cells(width, height):
    return frozenset(product(range(width), range(height)))


def rectangles(width, height):
    for l, r in combinations(range(width + 1), 2):
        for t, b in combinations(range(height + 1), 2):
            yield (l, r, t, b), frozenset(product(range(l, r), range(t, b)))


def placements(board, shapes):
    return {piece for x, y in board for shape in shapes
            if (piece := frozenset((x + dx, y + dy) for dx, dy in shape)) <= board}


def exact_covers(board, pieces):
    if not board:
        yield ()
        return
    first = min(board)
    for piece in pieces:
        if first in piece and piece <= board:
            for tail in exact_covers(board - piece, pieces):
                yield (piece, *tail)


def packing(board, pieces):
    @lru_cache(None)
    def best(left):
        if not left:
            return 0
        first = min(left)
        return max([best(left - {first})] + [1 + best(left - piece) for piece in pieces
                    if first in piece and piece <= left])
    return best(board)


def through_center():
    candidates = [area for _, area in rectangles(3, 3) if (1, 1) in area]
    return sum(a & b == {(1, 1)} for a, b in combinations(candidates, 2))


def uneven_squares():
    x, y = (0, 1, 3, 4, 7), (0, 1, 3, 4)
    return sum(x[r] - x[l] == y[b] - y[t] for (l, r, t, b), _ in rectangles(4, 3))


def missing_edge():
    x, y = 1, 1
    return sum(not (l <= x < r and y in (t, b)) for (l, r, t, b), _ in rectangles(4, 3))


def straight(n):
    return [tuple((i, 0) for i in range(n)), tuple((0, i) for i in range(n))]


DOMINO = straight(2)
SQUARE = [tuple(cells(2, 2))]
BENT = [tuple(shape) for shape in combinations(cells(2, 2), 3)]


def tile_count(board, shapes=DOMINO):
    return sum(1 for _ in exact_covers(board, placements(board, shapes)))


def one_removed():
    board = cells(5, 5)
    return sum(tile_count(board - {cell}) > 0 for cell in board)


def max_upright():
    board = cells(6, 5)
    shapes = [tuple(cells(2, 3)), tuple(cells(3, 2))]
    return max(sum(len({y for _, y in p}) == 3 for p in cover)
               for cover in exact_covers(board, placements(board, shapes)))


def stripe_counts():
    board = cells(6, 6)
    stripe = frozenset((x, y) for x, y in board if x in (2, 3))
    return {sum(len(p & stripe) == 1 for p in cover)
            for cover in exact_covers(board, placements(board, DOMINO))
            if sum(p <= stripe for p in cover) == 4}


def main():
    stepped = cells(4, 3) - {(2, 2), (3, 2)}
    cross = frozenset((x, y) for x, y in cells(5, 5) if x == 2 or y == 2)
    opposite_corners = cells(4, 4) - {(0, 0), (3, 3)}
    missing_pair = cells(4, 4) - {(0, 0), (1, 0)}
    t_shapes = [((0, 0), (1, 0), (2, 0), (1, 1)), ((0, 1), (1, 1), (2, 1), (1, 0)),
                ((0, 0), (0, 1), (0, 2), (1, 1)), ((1, 0), (1, 1), (1, 2), (0, 1))]
    panels = cells(3, 2) | frozenset((x + 4, y) for x, y in cells(2, 2))
    clipped = cells(4, 4) - cells(2, 2)
    rims = frozenset((x, y) for x, y in cells(5, 5) if x in (0, 4) or y in (0, 4))
    horizontal = [DOMINO[0]]
    rect = {
        (2, 'try'): sum(r-l == b-t for (l,r,t,b), _ in rectangles(4,3)),
        (2, 'transfer'): sum(len(a) == 6 for _, a in rectangles(5,4)),
        (3, 'try'): sum(a <= stepped for _, a in rectangles(4,3)),
        (3, 'transfer'): missing_edge(),
        (4, 'try'): sum({(1,1),(3,1)} <= a for _, a in rectangles(5,3)),
        (4, 'transfer'): sum(len(a & {(1,0),(3,2)}) == 1 for _, a in rectangles(5,3)),
        (5, 'try'): sum(a == {(3-x,y) for x,y in a} for _, a in rectangles(4,3)),
        (5, 'transfer'): sum(all(1 <= x <= 3 and 1 <= y <= 2 for x,y in a) for _, a in rectangles(5,4)),
        (6, 'try'): uneven_squares(),
        (6, 'transfer'): sum(2 * (r-l+b-t) == 14 for (l,r,t,b), _ in rectangles(5,4)),
        (7, 'try'): sum(all(x != y for x,y in a) for _, a in rectangles(4,4)),
        (7, 'transfer'): sum(sum((-1)**(x+y) for x,y in a) == 0 for _, a in rectangles(4,3)),
        (8, 'try'): sum(r-l == 2*(b-t) for (l,r,t,b), _ in rectangles(5,3)),
        (8, 'transfer'): sum(a <= cross for _, a in rectangles(5,5)),
        (9, 'try'): next(n for n in range(2,9) if sum(r-l == 2 for (l,r,_,_), _ in rectangles(n,n)) == 60),
        (9, 'transfer'): through_center(),
    }
    stripe = stripe_counts()
    assert len(stripe) == 1, stripe
    tiling = {
        (2, 'try'): packing(opposite_corners, placements(opposite_corners, DOMINO)),
        (2, 'transfer'): one_removed(),
        (3, 'try'): 'yes' if tile_count(missing_pair) else 'no',
        (3, 'transfer'): 'yes' if tile_count(cells(6, 6), straight(4)) else 'no',
        (4, 'try'): min(sum(rows[y] != cols[x] for x, y in cells(3, 3))
                       for rows in product((False, True), repeat=3)
                       for cols in product((False, True), repeat=3) if len(set(rows + cols)) > 1),
        (4, 'transfer'): 'yes' if tile_count(cells(6, 6), t_shapes) else 'no',
        (5, 'try'): 'yes' if tile_count(cells(4,4)-{(0,0),(0,3),(3,0),(3,3)}, BENT) else 'no',
        (5, 'transfer'): sum(tile_count(cells(6,4)-p, horizontal) > 0 for p in placements(cells(6,4), SQUARE)),
        (6, 'try'): stripe.pop(),
        (6, 'transfer'): max_upright(),
        (7, 'try'): tile_count(panels),
        (7, 'transfer'): packing(clipped, placements(clipped, straight(4))),
        (8, 'try'): packing(cells(5,5), placements(cells(5,5), SQUARE)),
        (8, 'transfer'): tile_count(rims),
    }
    assert rect == {key: q['answer'] for key, q in RECTANGLES.items()}, rect
    assert tiling == {key: q['answer'] for key, q in TILINGS.items()}, tiling
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp)
        build(map_course(), out, public_only=True)
        manifest = json.loads((out / 'lesson-manifest.json').read_text())['items']
        published = json.loads((Path(__file__).resolve().parents[2] / 'data/lesson-challenges.json').read_text())['items']
        spatial = [m for m in manifest if m['skill'] in ('SPATIAL-02', 'SPATIAL-03')]
        assert [m for m in published if m['skill'] in ('SPATIAL-02', 'SPATIAL-03')] == spatial
    print(f'PASS: independently enumerated {len(rect) + len(tiling)} spatial answers and matched the published diagram manifest.')


if __name__ == '__main__':
    main()
