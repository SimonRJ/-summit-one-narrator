// Original ungraded investigations. Coordinates run left to right, with row 1 at the top.
export const dominoBoards = [
  {
    name: 'The six-square mat', width: 3, height: 2, holes: [],
    clue: 'Start at A1. Try covering it with the square below, then try the square to its right.',
    proof: 'Stand one domino in each of the three columns. That covers every square exactly once. Can you find the two other tilings?'
  },
  {
    name: 'Two missing squares', width: 4, height: 3, holes: [0, 10],
    clue: 'Show the colours. What does every domino take away, whichever way you turn it?',
    proof: 'A1 and C3 were both dark. That leaves four dark and six light squares. Each domino covers one of each, so two light squares would be left over.'
  },
  {
    name: 'Two corners, one neighbour', width: 4, height: 3, holes: [1, 2, 9, 10],
    clue: 'Which square would A1 need as a partner? Which square would A3 need?',
    proof: 'There are four dark and four light squares. But A1 and A3 can each pair only with A2. Two dominoes cannot use A2 at once, so this board cannot be tiled.'
  }
];

const slotBoards = new Map([
  [19, ['DIV-04', 1]], [36, ['SPATIAL-03', 0]], [97, ['SPATIAL-03', 0]],
  [127, ['SPATIAL-03', 0]], [151, ['DIV-04', 0]], [159, ['SPATIAL-03', 1]],
  [218, ['SPATIAL-03', 1]], [309, ['SPATIAL-03', 0]], [333, ['DIV-04', 2]],
  [341, ['SPATIAL-03', 2]]
]);

function nameOf(board, cell) {
  return String.fromCharCode(65 + cell % board.width) + (1 + Math.floor(cell / board.width));
}

function dark(board, cell) {
  return (cell % board.width + Math.floor(cell / board.width)) % 2 === 0;
}

function neighbours(board, a, b) {
  return Math.abs(a % board.width - b % board.width)
    + Math.abs(Math.floor(a / board.width) - Math.floor(b / board.width)) === 1;
}

function freeCells(board, pairs) {
  const taken = new Set([...board.holes, ...pairs.flat()]);
  return Array.from({length: board.width * board.height}, (_, i) => i).filter(cell => !taken.has(cell));
}

// Pick the first free square. Every complete tiling pairs it with exactly one neighbour.
export function countDominoTilings(board, pairs = []) {
  const free = freeCells(board, pairs);
  const memo = new Map([[0, 1]]);
  function count(mask) {
    if (memo.has(mask)) return memo.get(mask);
    const first = free.find(cell => mask & (1 << cell));
    const rest = mask ^ (1 << first);
    let total = 0;
    for (const next of free) {
      if ((rest & (1 << next)) && neighbours(board, first, next)) {
        total += count(rest ^ (1 << next));
      }
    }
    memo.set(mask, total);
    return total;
  }
  return count(free.reduce((mask, cell) => mask | (1 << cell), 0));
}

export function mountDominoModel(container, lesson) {
  const mapping = slotBoards.get(lesson?.slot);
  if (!container || !mapping || (lesson.skill != null && lesson.skill !== mapping[0])) return false;
  const panel = document.createElement('details');
  panel.className = 'lesson-model domino-model';
  panel.innerHTML = `<summary>Explore domino tilings</summary>
    <div class="lesson-model-body">
      <label class="dm-board-label">Choose a board<select></select></label>
      <p>Can you cover every square with dominoes? Choose two squares that share an edge to place one domino.</p>
      <div class="dm-board" role="group"></div>
      <label class="dm-colours"><input type="checkbox"> Show checkerboard colours</label>
      <p class="dm-count" hidden></p>
      <div class="dm-actions"><button type="button" data-action="undo">Undo last domino</button><button type="button" data-action="reset">Start over</button></div>
      <fieldset><legend>Could the starting board be tiled?</legend>
        <button type="button" data-action="possible">Yes</button> <button type="button" data-action="impossible">No</button>
      </fieldset>
      <p class="dm-message" role="status" aria-live="polite" aria-atomic="true"></p>
    </div>`;
  container.replaceChildren(panel);
  const select = panel.querySelector('select');
  dominoBoards.forEach((board, index) => select.add(new Option(board.name, String(index))));
  select.value = String(mapping[1]);
  const boardArea = panel.querySelector('.dm-board');
  const colours = panel.querySelector('input');
  const counts = panel.querySelector('.dm-count');
  const message = panel.querySelector('.dm-message');
  const undo = panel.querySelector('[data-action="undo"]');
  const reset = panel.querySelector('[data-action="reset"]');
  let board, solutions, pairs, selected;
  let cells = [];
  function update(text) {
    const free = freeCells(board, pairs);
    const darkCount = free.filter(i => dark(board, i)).length;
    cells.forEach((button, cell) => {
      if (!button) return;
      const index = pairs.findIndex(pair => pair.includes(cell));
      const colour = dark(board, cell) ? 'dark' : 'light';
      const mark = index >= 0 ? String(index + 1) : '';
      const name = nameOf(board, cell);
      const isSelected = selected === cell;
      button.dataset.shade = colours.checked ? colour : '';
      button.dataset.domino = mark;
      let placement = 'free';
      if (index >= 0) {
        const mate = pairs[index].find(other => other !== cell);
        const difference = mate - cell;
        button.dataset.mate = ({1: 'right', '-1': 'left', [board.width]: 'below', [-board.width]: 'above'})[difference];
        button.dataset.colour = String(index % 3);
        placement = 'domino ' + mark + ', joined to ' + nameOf(board, mate);
      } else {
        delete button.dataset.mate;
        delete button.dataset.colour;
      }
      button.setAttribute('aria-pressed', String(isSelected));
      button.setAttribute('aria-label', [name, colours.checked ? colour : '', placement].filter(Boolean).join(', '));
      button.textContent = name + (mark ? ' · ' + mark : colours.checked ? ' ' + (colour === 'dark' ? '●' : '○') : '');
    });
    counts.hidden = !colours.checked;
    counts.textContent = 'Free squares: ' + darkCount + ' dark (●) and ' + (free.length - darkCount) + ' light (○). Each domino covers one of each.';
    undo.disabled = pairs.length === 0;
    reset.disabled = pairs.length === 0 && selected == null;
    if (text !== undefined) message.textContent = text;
  }
  function changeBoard() {
    board = dominoBoards[Number(select.value)];
    solutions = countDominoTilings(board);
    pairs = [];
    selected = null;
    colours.checked = false;
    boardArea.style.setProperty('--dm-columns', board.width);
    boardArea.setAttribute('aria-label', board.name + ', ' + board.height + ' rows by ' + board.width + ' columns');
    boardArea.replaceChildren();
    cells = [];
    for (let i = 0; i < board.width * board.height; i++) {
      if (board.holes.includes(i)) {
        const hole = document.createElement('span');
        hole.className = 'dm-hole';
        hole.textContent = '×';
        hole.setAttribute('role','img');
        hole.setAttribute('aria-label', nameOf(board, i) + ', missing square');
        boardArea.append(hole);
      } else {
        const cell = document.createElement('button');
        cell.type = 'button';
        cell.dataset.cell = String(i);
        boardArea.append(cell);
        cells[i] = cell;
      }
    }
    update('');
  }
  boardArea.addEventListener('click', event => {
    const button = event.target.closest('button[data-cell]');
    if (!button) return;
    const next = Number(button.dataset.cell);
    if (pairs.some(pair => pair.includes(next))) {
      update(nameOf(board, next) + ' is covered. Choose a free square or undo the last domino.');
    } else if (next === selected) {
      selected = null;
      update('Selection cleared.');
    } else if (selected == null) {
      selected = next;
      update(nameOf(board, next) + ' selected. Choose a free square sharing an edge.');
    } else if (!neighbours(board, selected, next)) {
      update('These squares do not share an edge. Choose a neighbour of ' + nameOf(board, selected) + ', or choose the selected square again to clear it.');
    } else {
      pairs.push([selected, next]);
      selected = null;
      const remaining = freeCells(board, pairs).length;
      if (remaining === 0) update('Complete! Your ' + pairs.length + ' dominoes cover every square. This arrangement proves the board can be tiled.');
      else if (solutions && !countDominoTilings(board, pairs)) update(remaining + ' free squares remain, but these placements cannot finish the mat. Undo a domino and try another pairing.');
      else update('Domino ' + pairs.length + ' placed. ' + remaining + ' free squares remain.');
    }
  });
  select.addEventListener('change', changeBoard);
  colours.addEventListener('change', () => update(colours.checked ? 'Checkerboard colours shown.' : 'Checkerboard colours hidden.'));
  undo.addEventListener('click', () => {
    pairs.pop();
    selected = null;
    update('Last domino removed.');
  });
  reset.addEventListener('click', () => {
    pairs = [];
    selected = null;
    update('All dominoes removed. Try a different first move.');
  });
  for (const answer of panel.querySelectorAll('fieldset button')) {
    answer.addEventListener('click', () => {
      const agrees = (answer.dataset.action === 'possible') === (solutions > 0);
      update(agrees ? board.proof : board.clue);
    });
  }
  changeBoard();
  return true;
}
