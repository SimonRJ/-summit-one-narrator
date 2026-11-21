import { mountRouteModel } from './route-model.js?v=paths-20261121';
import { mountDominoModel } from './domino-model.js?v=github-20261121';
import { modelClaims, mountClaimChallenge } from './model-claims.js?v=reasoning-20261121';

// Each investigation is a separate worked example. It never reads or records a learner's answers.
const investigations = [
  { skill: 'SOLID-01', slots: [6, 72, 87, 163, 254, 286, 345], title: 'Explore cube layers and views', build: buildStacks },
  { skill: 'SPATIAL-02', slots: [17, 82, 94, 118, 359], title: 'Explore rectangles around a cell', build: buildRectangles },
  { skill: 'GEO-05', slots: [53, 85, 122, 213, 370], title: 'Explore a fixed length of fencing', build: buildFencing },
];

export function mountLessonModel(container, lesson) {
  if (!container) return false;
  container.replaceChildren();
  const model = investigations.find(entry => entry.slots.includes(lesson?.slot) && (lesson.skill == null || entry.skill === lesson.skill));
  if (!model) return mountDominoModel(container, lesson) || mountRouteModel(container, lesson);
  const details = document.createElement('details');
  details.className = 'lesson-model';
  const summary = document.createElement('summary');
  summary.textContent = model.title;
  const body = document.createElement('div');
  body.className = 'lesson-model-body';
  details.append(summary, body);
  container.append(details);
  const readExample = model.build(body);
  mountClaimChallenge(body, modelClaims[model.skill], readExample, model.slots.indexOf(lesson.slot));
  return true;
}

function slider(label, key, value, max) {
  return `<label class="lm-slider"><span>${label} <b data-value="${key}">${value}</b></span>
    <input data-key="${key}" type="range" min="1" max="${max}" step="1" value="${value}"></label>`;
}

function outputArea() {
  return '<div class="lm-drawing"></div><p class="lm-result" role="status" aria-live="polite" aria-atomic="true"></p>';
}

function graphic(width, height, description, drawing) {
  return `<svg viewBox="0 0 ${width} ${height}" role="img" aria-label="${description}" focusable="false">${drawing}</svg>`;
}

function label(x, y, value, className = 'lm-caption', anchor = 'middle') {
  return `<text x="${x}" y="${y}" class="${className}" text-anchor="${anchor}">${value}</text>`;
}

function connectControls(body, draw) {
  let example;
  const update = () => {
    const state = {};
    for (const control of body.querySelectorAll('[data-key]')) {
      state[control.dataset.key] = Number(control.value);
      const display = body.querySelector(`[data-value="${control.dataset.key}"]`);
      if (display) display.textContent = control.value;
    }
    example = draw(state, body.querySelector('.lm-drawing'), body.querySelector('.lm-result'));
  };
  body.querySelector('.lm-controls').addEventListener('input', update);
  update();
  return () => example;
}

function buildStacks(body) {
  body.innerHTML = `<p>Look from the front of this four-stack building. Predict how tall the back-left stack must grow before the outline changes. On the plan, the numbers are heights. Shading marks stacks that reach your chosen layer.</p>
    <div class="lm-controls">${slider('Back-left stack height', 'height', 1, 5)}${slider('Layer to inspect', 'layer', 2, 5)}<label>View<select data-key="side"><option value="0">From the front</option><option value="1">From the right</option></select></label></div>${outputArea()}`;

  return connectControls(body, ({ height, layer, side }, canvas, result) => {
    // Each row in the plan runs from left to right. The back row is drawn first.
    const back = [height, 4];
    const front = [3, 2];
    const stacks = [...back, ...front];
    const outline = side ? [Math.max(...front), Math.max(...back)] : [Math.max(front[0], back[0]), Math.max(front[1], back[1])];
    const sides = side ? ['front', 'back'] : ['left', 'right'];
    const occupied = stacks.filter(h => h >= layer).length;
    let plan = label(74, 15, 'Plan from above') + label(74, 127, 'Front', 'lm-small');
    stacks.forEach((h, i) => {
      const x = 35 + (i % 2) * 39;
      const y = 31 + Math.floor(i / 2) * 39;
      plan += `<rect x="${x}" y="${y}" width="39" height="39" class="${h >= layer ? 'lm-present' : 'lm-empty'}"/>`;
      plan += label(x + 19.5, y + 25, h, h >= layer ? 'lm-active-number' : 'lm-number');
    });
    const words = ['back left', 'back right', 'front left', 'front right'];
    let elevation = label(207, 15, side ? 'Right-side outline' : 'Front outline');
    outline.forEach((h, col) => {
      for (let level = 1; level <= h; level++) {
        elevation += `<rect x="${188 + col * 19}" y="${114 - level * 19}" width="19" height="19" class="${level === layer ? 'lm-present' : 'lm-cube'}"/>`;
      }
    });
    elevation += label(207, 129, sides.join(' · '), 'lm-small');
    const description = `Plan heights are ${back.join(' and ')} in the back row and 3 and 2 in the front row. The ${side ? 'right-side' : 'front'} view shows ${outline.join(' and ')} from ${sides[0]} to ${sides[1]}.`;
    canvas.innerHTML = graphic(280, 137, description, plan + elevation);
    const locations = words.filter((word, i) => stacks[i] >= layer).join(', ');
    result.textContent = `The ${side ? 'right-side' : 'front'} outline shows ${outline[0]} cubes (${sides[0]}) and ${outline[1]} (${sides[1]}). Layer ${layer} has ${occupied} of the four positions filled${occupied ? ' (' + locations + ')' : ''}. The full building has ${stacks.reduce((sum, h) => sum + h, 0)} cubes.`;
    return { height, rightHeight: Math.max(front[1], back[1]),
      second: stacks.filter(h => h >= 2).length, third: stacks.filter(h => h >= 3).length };
  });
}

function framesAround(column, row) {
  const frames = [];
  for (let left = 0; left <= column; left++) {
    for (let right = column + 1; right <= 4; right++) {
      for (let bottom = 0; bottom <= row; bottom++) {
        for (let top = row + 1; top <= 3; top++) frames.push({ left, right, bottom, top });
      }
    }
  }
  return frames;
}

function buildRectangles(body) {
  const columns = 'ABCD';
  const options = Array.from({ length: 12 }, (_, i) =>
    `<option value="${i}">${columns[i % 4]}${Math.floor(i / 4) + 1}</option>`).join('');
  body.innerHTML = `<p>Each rectangle must contain the marked cell. Predict whether the corner A1 or the middle cell B2 belongs to more rectangles. Then inspect their outlines.</p>
    <div class="lm-controls"><label>Marked cell<select data-key="cell">${options}</select></label>
    ${slider('Outline to inspect', 'frame', 1, 12)}</div>${outputArea()}`;
  const control = body.querySelector('[data-key="frame"]');
  let lastCell = null;
  return connectControls(body, ({ cell }, canvas, result) => {
    const column = cell % 4;
    const row = Math.floor(cell / 4);
    const frames = framesAround(column, row);
    control.max = frames.length;
    if (cell !== lastCell) control.value = 1;
    lastCell = cell;
    const number = Number(control.value);
    body.querySelector('[data-value="frame"]').textContent = `${number} of ${frames.length}`;
    control.setAttribute('aria-valuetext', `Outline ${number} of ${frames.length}`);
    const { left, right, bottom, top } = frames[number - 1];
    const x = edge => 76 + 34 * edge;
    const y = edge => 117 - 34 * edge;
    let drawing = `<rect x="${x(column)}" y="${y(row + 1)}" width="34" height="34" class="lm-present"/>`;
    for (let i = 0; i <= 4; i++) drawing += `<path d="M${x(i)} ${y(0)} V${y(3)}" class="lm-grid"/>`;
    for (let j = 0; j <= 3; j++) drawing += `<path d="M${x(0)} ${y(j)} H${x(4)}" class="lm-grid"/>`;
    for (let i = 0; i < 4; i++) drawing += label(x(i) + 17, 135, columns[i], 'lm-caption');
    for (let j = 0; j < 3; j++) drawing += label(61, y(j) - 13, j + 1, 'lm-caption');
    drawing += `<rect x="${x(left)}" y="${y(top)}" width="${x(right) - x(left)}" height="${y(bottom) - y(top)}" class="lm-outline"/>`;
    drawing += `<circle cx="${x(column) + 17}" cy="${y(row) - 17}" r="4" class="lm-dot"/>`;
    const cellName = columns[column] + (row + 1);
    const lowCell = columns[left] + (bottom + 1);
    const highCell = columns[right - 1] + top;
    const description = `A four-column, three-row grid. The marked cell is ${cellName}. The outline runs from cell ${lowCell} at the bottom left to cell ${highCell} at the top right.`;
    canvas.innerHTML = graphic(280, 143, description, drawing);
    result.textContent = `For ${cellName}, there are ${column + 1} left, ${4 - column} right, ${row + 1} bottom and ${3 - row} top edge choices. That makes ${column + 1} × ${4 - column} × ${row + 1} × ${3 - row} = ${frames.length} rectangles. This outline spans cells ${lowCell} to ${highCell}.`;
    const partner = columns[3-column] + (3-row);
    return { cell: cellName, frame: number, width: right-left, height: top-bottom, count: frames.length,
      partner, partnerCount: framesAround(3-column, 2-row).length };
  });
}

function buildFencing(body) {
  body.innerHTML = `<p>You have 24 metres of fencing. Predict the depth that gives the largest area, then move the fence to test your idea. Try again with a wall along the back.</p>
    <div class="lm-controls"><label>Boundary<select data-key="wall"><option value="0">Fence on all four sides</option><option value="1">Wall along the back</option></select></label>
    ${slider('Depth in metres', 'depth', 2, 11)}</div>${outputArea()}`;
  return connectControls(body, ({ wall, depth }, canvas, result) => {
    const width = wall ? 24 - 2 * depth : 12 - depth;
    const area = width * depth;
    // Equal units on both axes, with a 1 m grid clipped by the pen endpoints.
    const scale = 9;
    const x = 34, base = 117, top = base - depth * scale, right = x + width * scale;
    let drawing = `<rect x="${x}" y="${top}" width="${width * scale}" height="${depth * scale}" class="lm-pen"/>`;
    for (let col = 1; col < width; col++) drawing += `<path d="M${x + col * scale} ${top} V${base}" class="lm-unit"/>`;
    for (let row = 1; row < depth; row++) drawing += `<path d="M${x} ${base - row * scale} H${right}" class="lm-unit"/>`;
    drawing += `<path d="M${x} ${top} V${base} H${right} V${top}" class="lm-fence"/>`;
    drawing += `<path d="M${x} ${top} H${right}" class="${wall ? 'lm-wall' : 'lm-fence'}"/>`;
    drawing += label((x + right) / 2, base + 19, `${width} m`, 'lm-caption');
    drawing += label(right + 9, (top + base) / 2 + 4, `${depth} m`, 'lm-caption', 'start');
    const description = `Rectangular pen ${width} metres across and ${depth} metres deep. ${wall ? 'A dashed line marks the wall at the back. Three sides are fenced.' : 'All four sides are fenced.'}`;
    canvas.innerHTML = graphic(280, 144, description, drawing);
    const fence = wall ? `${width} + 2 × ${depth}` : `2 × ${width} + 2 × ${depth}`;
    result.textContent = `${wall ? 'The dashed back wall uses no fencing. ' : ''}The fence measures ${fence} = 24 m. The area is ${width} × ${depth} = ${area} m².`;
    return { wall, width, depth, closedWidth: 12-depth, wallWidth: 24-2*depth };
  });
}
