import assert from 'node:assert/strict';
import { modelClaims } from '../model-claims.js';

// A saved example must report the same quantities and named cells that established its verdict.
function checkExamples(claims, state, expected, displayed, totals) {
  for (const [i, claim] of claims.entries()) {
    const where = claim.name + ' ' + JSON.stringify(state);
    assert.equal(claim.test(state), expected[i], where);
    const tokens = claim.example(state).match(/\b[A-D][1-3]\b|\d+/g) || [];
    assert.deepEqual(tokens, displayed[i].map(String), where + ' saved example');
    if (expected[i]) totals[i]++;
  }
}

function checkVerdicts(claims, observed, configurations, expectedTrue) {
  assert.deepEqual(observed, expectedTrue);
  for (const [i, n] of observed.entries()) {
    const verdict = n === 0 ? 'Never' : n === configurations ? 'Always' : 'Sometimes';
    assert.equal(claims[i].verdict, verdict, claims[i].name);
  }
}

const cubeClaims = modelClaims['SOLID-01'];
const cubeTotals = [0, 0, 0];
for (let height = 1; height <= 5; height++) {
  const cubes = [];
  for (const [x, y, stack] of [[0, 0, 3], [1, 0, 2], [0, 1, height], [1, 1, 4]]) {
    for (let z = 1; z <= stack; z++) cubes.push({ x, y, z });
  }
  const hidden = cubes.filter(c => c.x === 0 && c.y === 1)
    .every(c => cubes.some(other => other.x === c.x && other.y === 0 && other.z === c.z));
  const rightHeight = new Set(cubes.filter(c => c.x === 1).map(c => c.z)).size;
  const second = cubes.filter(c => c.z === 2).length;
  const third = cubes.filter(c => c.z === 3).length;
  checkExamples(cubeClaims, { height, rightHeight, second, third },
    [hidden, rightHeight === 4, third > second],
    [[3, height], [height, rightHeight], [height, 2, second, 3, third]], cubeTotals);
}
checkVerdicts(cubeClaims, cubeTotals, 5, [3, 5, 0]);

const rectangleClaims = modelClaims['SPATIAL-02'];
const grid = [];
const cellName = (x, y) => 'ABCD'[x] + (y + 1);
for (let width = 1; width <= 4; width++) {
  for (let height = 1; height <= 3; height++) {
    for (let left = 0; left + width <= 4; left++) {
      for (let bottom = 0; bottom + height <= 3; bottom++) {
        const cells = new Set();
        for (let x = left; x < left + width; x++) {
          for (let y = bottom; y < bottom + height; y++) cells.add(cellName(x, y));
        }
        grid.push({ left, bottom, width, height, cells });
      }
    }
  }
}
assert.equal(grid.length, 60);
const rectTotals = [0, 0, 0];
let outlines = 0;
for (let x = 0; x < 4; x++) {
  for (let y = 0; y < 3; y++) {
    const cell = cellName(x, y);
    const partner = cellName(3 - x, 2 - y);
    const partnerCount = grid.filter(r => r.cells.has(partner)).length;
    const enclosing = grid.filter(r => r.cells.has(cell));
    // The inspection slider sorts by its left, right, bottom, then top boundary.
    enclosing.sort((a, b) => a.left - b.left || a.width - b.width ||
      a.bottom - b.bottom || a.height - b.height);
    for (const [i, rectangle] of enclosing.entries()) {
      const { width, height, left, bottom } = rectangle;
      const perimeter = 2 * width + 2 * height;
      const rotated = grid.find(r => r.left === 4 - left - width &&
        r.bottom === 3 - bottom - height && r.width === width && r.height === height);
      assert(rotated?.cells.has(partner), 'The rotated outline must enclose the partner cell');
      const frame = i + 1;
      const count = enclosing.length;
      checkExamples(rectangleClaims, { cell, frame, width, height, count, partner, partnerCount },
        [width === height, count === partnerCount, perimeter === 7],
        [[cell, frame, width, height], [cell, count, partner, partnerCount], [width, height, perimeter]], rectTotals);
      outlines++;
    }
  }
}
assert.equal(outlines, 200);
checkVerdicts(rectangleClaims, rectTotals, outlines, [54, 200, 0]);

const penClaims = modelClaims['GEO-05'];
const penTotals = [0, 0, 0];
let pens = 0;
for (let depth = 1; depth <= 11; depth++) {
  const widths = [[], []];
  for (let w = 1; w <= 24; w++) {
    if (depth + w + depth + w === 24) widths[0].push(w);
    if (depth + w + depth === 24) widths[1].push(w);
  }
  assert.deepEqual(widths.map(row => row.length), [1, 1]);
  const [[closedWidth], [wallWidth]] = widths;
  const closedArea = depth * closedWidth;
  const wallArea = depth * wallWidth;
  for (const [wall, [width]] of widths.entries()) {
    const state = { wall, width, depth, closedWidth, wallWidth };
    checkExamples(penClaims, state,
      [width > depth, wallArea === 2 * closedArea, Math.min(width, depth) > 8],
      [[width, depth], [depth, closedArea, wallArea], [width, depth, 24]], penTotals);
    assert(penClaims[0].example(state).includes(wall ? 'With a wall' : 'With four fenced sides'));
    pens++;
  }
}
assert.equal(pens, 22);
checkVerdicts(penClaims, penTotals, pens, [12, 22, 0]);
const digitClaims = modelClaims['DIV-05'];
const powerTotals = [0, 0, 0];
for (let base = 1; base < 10; base++) {
  const last = n => Number(BigInt(base) ** BigInt(n) % 10n);
  for (let exponent = 1; exponent <= 12; exponent++) {
    const digit = last(exponent), next = last(exponent + 1), afterFour = last(exponent + 4);
    checkExamples(digitClaims, {base, exponent, digit, next, afterFour},
      [true, digit !== next, false],
      [[base, exponent, exponent + 4, digit, afterFour], [base, digit, next], [base, exponent, digit]], powerTotals);
  }
}
checkVerdicts(digitClaims, powerTotals, 108, [108, 72, 0]);
console.log('PASS: 12 claims, classifications and saved example quantities across 108 powers, 5 stacks, 200 marked outlines and 22 pens.');
