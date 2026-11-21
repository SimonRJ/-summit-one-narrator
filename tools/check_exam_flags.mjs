import assert from 'node:assert/strict';
import {createExamFlags} from '../exam-flags.js';

const values = new Map();
const store = {
  getItem: key => values.get(key) ?? null,
  setItem: (key, value) => values.set(key, value),
  removeItem: key => values.delete(key)
};
const open = (learner, sitting) => createExamFlags(learner, sitting, [21, 26], store);
const first = open('one', 'test');
first.toggle(21);
assert.ok(first.has(21));
assert.ok(open('one', 'test').has(21));
assert.equal(open('one', 'again').has(21), false);
const other = open('two', 'test');
assert.equal(other.has(21), false);
other.toggle(26);
const secondTab = open('one', 'test');
secondTab.toggle(26);
const ownSecond = Array.from(values.keys()).find(key => key.includes(':one:test:26'));
assert.ok(first.sync({key: ownSecond, storageArea: store, newValue: '1'}));
assert.ok(first.has(26));
first.toggle(21);
assert.equal(open('one', 'test').has(21), false);
first.toggle(99);
assert.equal(first.has(99), false);
first.clear();
assert.equal(open('two', 'test').has(26), true);
assert.equal(open('one', 'test').has(26), false);
const unavailable = createExamFlags('three', 'test', [21], {
  getItem() { throw Error('Storage unavailable'); },
  setItem() { throw Error('Storage unavailable'); },
  removeItem() { throw Error('Storage unavailable'); }
});
unavailable.toggle(21);
assert.ok(unavailable.has(21));
unavailable.clear();
assert.equal(unavailable.has(21), false);
console.log('PASS: marks survive reopen, are isolated by learner and sitting, and work in memory without storage.');
