import assert from 'node:assert/strict';
import {countDominoTilings, dominoBoards} from '../domino-model.js';

// Independent calculation: assign each dark square a distinct neighbouring light square.
function matchings(board, free) {
  const left = [], right = [];
  for (const i of free) {
    const row = Math.floor(i / board.width), column = i % board.width;
    ((row + column) % 2 === 0 ? left : right).push({row, column});
  }
  if (left.length !== right.length) return 0;
  function count(index, available) {
    if (index === left.length) return 1;
    let total = 0;
    for (const light of available) {
      const distance = Math.abs(left[index].row - light.row) + Math.abs(left[index].column - light.column);
      if (distance === 1) total += count(index + 1, available.filter(other => other !== light));
    }
    return total;
  }
  return count(0, right);
}

assert.deepEqual(dominoBoards.map(board => countDominoTilings(board)), [3, 0, 0]);
let checked = 0;
for (const board of dominoBoards) {
  const all = Array.from({length: board.width * board.height}, (_, i) => i).filter(n => !board.holes.includes(n));
  for (let mask = 0; mask < (1 << all.length); mask++) {
    const free = all.filter((id, index) => mask & (1 << index));
    const covered = all.filter((id, index) => !(mask & (1 << index)));
    assert.equal(countDominoTilings(board, [covered]), matchings(board, free), board.name + ' ' + mask);
    checked++;
  }
}
// Placing A1-B1 and B2-C2 on the first board leaves A2 and C1 on opposite colours but too far apart.
assert.equal(countDominoTilings(dominoBoards[0], [[0, 1], [4, 5]]), 0);
assert.equal(countDominoTilings(dominoBoards[0], [[0, 3], [1, 4], [2, 5]]), 1);
assert.equal(checked, 1344);
console.log('Passed exact domino tiling checks for all 1,344 free-square patterns on three boards.');
