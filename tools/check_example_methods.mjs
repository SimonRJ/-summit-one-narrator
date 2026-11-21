import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {exampleMethods} from '../example-methods.js';
import {readCard} from '../reviewed-lesson.js';

const editions = ['read-watch-practise', 'read-watch-practise-later'].map(name =>
  JSON.parse(readFileSync(new URL(`../data/${name}.json`, import.meta.url), 'utf8')).lessons);
const labels = ['A', 'B', 'C'].flatMap(first => ['A', 'B', 'C'].map(last => first + last));
const commonLengths = Array.from({length: 12}, (_, i) => i + 1).filter(n => 12 % n === 0 && 20 % n === 0);
const possibleJar = Array.from({length: 25}, (_, i) => i).find(n => (3 + 7 + 8 + n) / 4 === 6);
const ratePerMinute = 1 / 6 + 1 / 3;
const fourTerms = [4, 8, 16, 32];
const redChance = (1 / 2) * (2 / 2) + (1 / 2) * (1 / 2);
// Calculate each result independently of the explanation and match the answer in the rendered alternative.
const solutions = new Map([
  [2, `to get ${31 * 8}.`],
  [13, `greatest length is ${Math.max(...commonLengths)} cm`],
  [26, `must already hold ${possibleJar}.`],
  [43, `sum is ${2 * (4 * 4) - 2 * 4} cm`],
  [62, `= ${labels.filter(label => label.includes('A')).length}.`],
  [86, `1/${1 / ratePerMinute} of a batch`],
  [142, `= ${(18 - 18 / 3) / 2} rolls`],
  [179, `${4 / (1 + 0.5) * 3}/3 km/h`],
  [298, `extra ${2 * fourTerms.at(-1) - fourTerms.reduce((sum, n) => sum + n, 0)}.`],
  [332, `${redChance * 4}/4.`]
]);

const seen = new Set();
for (const lessons of editions) {
  let count = 0;
  for (const lesson of lessons) {
    const card = readCard(lesson);
    const expected = solutions.get(lesson.slot);
    const method = exampleMethods.get(lesson.example.prompt);
    assert.equal(Boolean(method), Boolean(expected), `Unexpected match at lesson ${lesson.slot}`);
    if (!expected) {
      assert.ok(!card.includes('rwl-second-method'));
      continue;
    }
    assert.ok(!seen.has(lesson.example.prompt), `Duplicate example at ${lesson.slot}`);
    seen.add(lesson.example.prompt);
    count++;
    assert.ok(method.working.includes(expected), `Result at lesson ${lesson.slot} should contain ${expected}`);
    const alternate = card.indexOf('<details class="rwl-second-method">');
    const full = card.indexOf('class="rwl-full-example">');
    assert.ok(full > card.indexOf('</details>') && alternate > card.indexOf('</ol>', full));
    assert.ok(alternate < card.indexOf('</details>', full), 'Alternative must be nested in the closed full example');
    assert.ok(card.indexOf(method.working) > alternate && card.indexOf(method.comparison) > alternate);
    const changed = {...lesson, example: {...lesson.example, prompt: lesson.example.prompt + ' (revised)'}};
    assert.ok(!readCard(changed).includes('rwl-second-method'), 'Revised example must not reuse old reasoning');
  }
  assert.ok(count > 0, 'Both editions should include comparisons');
}
assert.equal(seen.size, solutions.size);
assert.equal(seen.size, exampleMethods.size);
console.log(`Verified ${seen.size} optional method comparisons across ${editions.flat().length} lessons.`);
