// Run alongside the browser checks with Playwright installed.
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { createRequire } from 'node:module';
const { chromium } = createRequire(import.meta.url)('playwright');
const root = new URL('../', import.meta.url);
const read = path => readFile(new URL(path, root), 'utf8');
const manifests = await Promise.all(['data/read-watch-practise.json', 'data/read-watch-practise-later.json'].map(read));
const lessons = manifests.flatMap(json => JSON.parse(json).lessons.map(({slot, skill}) => ({slot, skill})));
const fixture = '<meta name="viewport" content="width=device-width, initial-scale=1"><link rel="stylesheet" href="/lesson-models.css"><main></main>';
const resources = {
  '/': [fixture, 'text/html'],
  '/domino-model.js': [await read('domino-model.js'), 'text/javascript'],
  '/domino-model.css': [await read('domino-model.css'), 'text/css'],
  '/model-claims.js': [await read('model-claims.js'), 'text/javascript'],
  '/lesson-models.js': [await read('lesson-models.js'), 'text/javascript'],
  '/lesson-models.css': [await read('lesson-models.css'), 'text/css'],
};
const browser = await chromium.launch({executablePath: process.env.CHROMIUM_PATH || undefined});
try {
  const page = await browser.newPage({viewport: {width: 320, height: 667}});
  await page.route('http://lesson.test/**', route => {
    const resource = resources[new URL(route.request().url()).pathname];
    return resource ? route.fulfill({body: resource[0], contentType: resource[1]}) : route.fulfill({status: 404});
  });
  await page.goto('http://lesson.test/');
  const actual = await page.evaluate(async lessons => {
    const { mountLessonModel } = await import('/lesson-models.js');
    const main = document.querySelector('main');
    window.showModel = lesson => mountLessonModel(main, lesson);
    return lessons.filter(lesson => window.showModel(lesson)).map(lesson => lesson.slot);
  }, lessons);
  assert.deepEqual(actual, [6,17,19,36,53,72,82,85,87,94,97,118,122,127,151,159,163,213,218,254,286,309,333,341,345,359,370]);
  const open = async slot => {
    await page.evaluate(lesson => window.showModel(lesson), lessons.find(lesson => lesson.slot === slot));
    assert.equal(await page.locator('.lesson-model').getAttribute('open'), null);
    await page.locator('.lesson-model > summary').focus();
    await page.keyboard.press('Enter');
    assert.equal(await page.locator('.lesson-model').getAttribute('open'), '');
  };
  await open(87);
  const slider = page.locator('[data-key=height]');
  await slider.focus();
  await page.keyboard.press('ArrowRight');
  assert.equal(await slider.inputValue(), '2');
  const stackStates = await page.evaluate(() => {
    window.setControl = (key, value) => {
      const control = document.querySelector(`[data-key="${key}"]`);
      control.value = value;
      control.dispatchEvent(new Event('input', {bubbles:true}));
    };
    let checked = 0;
    for (let h = 1; h <= 5; h++) for (let level = 1; level <= 5; level++) for (const side of [0,1]) {
      window.setControl('height',h); window.setControl('layer',level); window.setControl('side',side);
      const cubes = [h,4,3,2].flatMap((n, i) => Array.from({length:n}, (_, k) =>
        ({row: Math.floor(i/2), col: i%2, z: k+1})));
      const occupied = cubes.filter(c => c.z === level).length;
      const first = cubes.filter(c => side ? c.row === 1 : c.col === 0);
      const other = cubes.filter(c => side ? c.row === 0 : c.col === 1);
      const visible = [first,other].map(column => new Set(column.map(c => c.z)).size);
      const summary = document.querySelector('.lm-result').textContent;
      const drawing = document.querySelector('.lm-drawing svg');
      const drawnCubes = [...drawing.querySelectorAll('rect')].slice(4);
      if (!summary.includes(`Layer ${level} has ${occupied}`) || !summary.includes(`${cubes.length} cubes.`) ||
          !drawing.getAttribute('aria-label').includes(`shows ${visible.join(' and ')}`) ||
          drawnCubes.length !== visible[0]+visible[1] ||
          drawnCubes.some(block => block.getAttribute('width') !== block.getAttribute('height'))) {
        throw Error('Cube model failed at '+[h,level,side]);
      }
      checked++;
    }
    return checked;
  });
  assert.equal(stackStates,50);
  await open(17);
  const frames = await page.evaluate(() => {
    let total = 0;
    for (let i = 0; i < 12; i++) {
      window.setControl('cell',i);
      const col = i%4, row = Math.floor(i/4);
      const expected = new Set();
      // Enumerate dimensions and translations independently of the edge-choice implementation.
      for (let width=1; width<=4; width++) for(let height=1; height<=3; height++)
        for(let x=0; x+width<=4; x++) for(let y=0; y+height<=3; y++)
          if (x<=col && col<x+width && y<=row && row<y+height) expected.add([x,y,width,height].join(','));
      const range = document.querySelector('[data-key=frame]');
      if (Number(range.max) !== expected.size) throw Error('Wrong count for cell '+i);
      const seen = new Set();
      for(let n=1;n<=expected.size;n++) {
        window.setControl('frame',n);
        const rect = document.querySelector('.lm-outline');
        const width = rect.width.baseVal.value / 34, height = rect.height.baseVal.value / 34;
        const left = (rect.x.baseVal.value - 76)/34;
        const bottom = (117-rect.y.baseVal.value)/34-height;
        const key = [left,bottom,width,height].join(',');
        if (!expected.has(key) || seen.has(key)) throw Error('Incorrect or repeated outline '+key);
        seen.add(key); total++;
      }
    }
    return total;
  });
  assert.equal(frames, 200);
  await open(85);
  const fences = await page.evaluate(() => {
    let checked=0;
    for (const wall of [0,1]) for(let depth=1; depth<=11; depth++) {
      window.setControl('wall',wall); window.setControl('depth',depth);
      const candidateWidths = Array.from({length:24}, (_,j)=>j+1).filter(w =>
        2*depth + (wall ? w : 2*w) === 24);
      const [width] = candidateWidths;
      const text = document.querySelector('.lm-result').textContent;
      const grid = document.querySelector('.lm-pen');
      if(candidateWidths.length!==1 || !text.includes(`= ${width*depth} m²`) ||
         grid.width.baseVal.value !== 9*width || grid.height.baseVal.value !== 9*depth ||
         Boolean(document.querySelector('.lm-wall')) !== Boolean(wall)) throw Error('Fence case '+[wall,depth]);
      checked++;
    }
    return checked;
  });
  assert.equal(fences,22);
  // Use the learner controls so the example, classification and graph share the same live state.
  await open(6);
  const challenge = page.locator('.lm-claims');
  const openChallenge = async () => {
    assert.equal(await challenge.getAttribute('open'), null);
    await challenge.locator(':scope > summary').press('Enter');
    assert.equal(await challenge.getAttribute('open'), '');
  };
  await openChallenge();
  const saveCase = challenge.getByRole('button', {name: 'Use this example'});
  const cases = challenge.locator('.lm-cases li');
  const verdict = challenge.getByRole('status', {includeHidden: true});
  const sometimes = challenge.getByRole('button', {name: 'Sometimes', exact: true});
  await sometimes.press('Enter');
  assert.match(await verdict.innerText(), /example.*counterexample/i);
  await saveCase.press('Space');
  assert.equal(await cases.count(), 1);
  assert.match(await cases.first().innerText(), /Claim holds.*Back left: 1/s);
  // Saving a different supporting example replaces the first one; it cannot count as a counterexample.
  await slider.press('ArrowRight');
  await slider.press('ArrowRight');
  await saveCase.press('Enter');
  assert.equal(await cases.count(), 1);
  assert.match(await cases.first().innerText(), /Claim holds.*Back left: 3/s);
  await slider.press('ArrowRight');
  await saveCase.press('Enter');
  assert.equal(await cases.count(), 2);
  assert.match(await cases.last().innerText(), /Counterexample.*Back left: 4/s);
  await sometimes.press('Enter');
  assert.match(await verdict.innerText(), /^Sometimes\./);

  await challenge.getByRole('combobox').selectOption({label: 'The right column'});
  assert.equal(await cases.count(), 0);
  assert.equal(await verdict.innerText(), '');
  await challenge.getByRole('button', {name: 'Never', exact: true}).press('Enter');
  assert.match(await verdict.innerText(), /right column/i);
  await challenge.getByRole('button', {name: 'Always', exact: true}).press('Enter');
  assert.match(await verdict.innerText(), /^Always\./);

  for (const width of [320,390,768]) {
    await page.setViewportSize({width,height:716});
    for (const slot of [87,17,85]) {
      await open(slot);
      await openChallenge();
      await saveCase.click();
      assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), true);
      assert.equal(await page.evaluate(() => [...document.querySelectorAll('summary,input,select,button')].every(el => {
        const box = el.getBoundingClientRect();
        const labelled = el.matches('input,select') ? el.labels.length > 0 : Boolean(el.textContent.trim());
        return box.height >= 44 && box.left >= 0 && box.right <= innerWidth && labelled;
      })), true);
    }
  }
  assert.equal(await page.evaluate(() => {
    if (!window.showModel({slot:87}) || !document.querySelector('.lesson-model')) return false;
    const result = window.showModel({slot:87,skill:'different'});
    return result === false && !document.querySelector('main').firstChild;
  }),true);
  console.log('Passed 27 course mappings, 50 stack views, 200 grid outlines, 22 fencing configurations, claim evidence and reset, keyboard controls and three viewport widths.');
} finally {
  await browser.close();
}
