// Original ungraded examples on the same three-by-two street grid.
const scenarios = {
  open: {
    name: 'All streets open',
    task: 'Which last steps can bring a route into D3?',
    proof: 'Six routes reach C3 and four reach D2. Every route into D3 ends at exactly one of those neighbours before its last step. Add 6 + 4 to get 10.'
  },
  checkpoint: {
    name: 'Visit B2',
    task: 'Visit the diamond at B2 on the way to D3. How could you split the journey into two parts?',
    proof: 'There are two ways to B2 and three ways from B2 to D3. Each first part works with each second part, giving 2 × 3 = 6 routes.'
  },
  point: {
    name: 'Close the junction B2',
    task: 'The cross at B2 closes the whole junction. Can you get to D3 without touching it?',
    proof: 'Of the 10 routes on the open grid, 6 pass through B2. Closing the junction leaves 10 − 6 = 4 routes.'
  },
  edge: {
    name: 'Close the street A2–B2',
    task: 'The cross closes only the street from A2 to B2. Can you still reach B2 from another direction?',
    proof: 'One route reaches A2. After crossing the closed street into B2 there would be three ways onward. Closing that street removes 1 × 3 routes, leaving 10 − 3 = 7. B2 is still reachable from B1.'
  },
  history: {
    name: 'Separate the up moves',
    task: 'Leave at least one right move between the two up moves. At B2, try arriving with RU and then with UR. Can you make the same next moves?',
    proof: 'Write the three right moves in a row. There are four gaps for the up moves, including the two ends. Pick two different gaps. The six pairs are 1–2, 1–3, 1–4, 2–3, 2–4 and 3–4.'
  }
};

const lessons = new Map([
  [52, ['SEQ-03', 'open']], [93, ['SPATIAL-01', 'open']],
  [227, ['SPATIAL-01', 'checkpoint']], [248, ['SEQ-03', 'history']],
  [318, ['SPATIAL-01', 'point']], [366, ['SPATIAL-01', 'history']]
]);

const start = () => ({x: 0, y: 0, viaB2: false, last: ''});
const atFinish = state => state.x === 3 && state.y === 2;
const qualifies = (rule, state) => rule !== 'checkpoint' || state.viaB2;
const locationName = ({x,y}) => 'ABCD'[x] + (y+1);

function attemptStep(rule, state, move) {
  if (move !== 'R' && move !== 'U') return {error: 'Choose Right or Up.'};
  const x = state.x + Number(move === 'R'), y = state.y + Number(move === 'U');
  if (x > 3 || y > 2) return {error: 'That step would go outside the grid.'};
  const b2 = x === 1 && y === 1;
  if (rule === 'point' && b2) return {error: 'B2 is closed. Choose a route around the junction.'};
  if (rule === 'edge' && b2 && move === 'R') return {error: 'The street from A2 to B2 is closed. You can still reach B2 from B1.'};
  if (rule === 'history' && move === 'U' && state.last === 'U') return {error: 'Two up moves in a row would break the rule. Try Right or undo a move.'};
  return {state: {x, y, viaB2: state.viaB2 || b2, last: move}};
}

export function analyseRoute(rule, word) {
  let state = start();
  for (const move of word) {
    const step = attemptStep(rule, state, move);
    if (step.error) return step;
    state = step.state;
  }
  return {state, accepted: atFinish(state) && qualifies(rule, state)};
}

function finishes(rule, state) {
  if (atFinish(state)) return Number(qualifies(rule, state));
  return ['R', 'U'].reduce((sum, move) => {
    const next = attemptStep(rule, state, move);
    return sum + (next.state ? finishes(rule, next.state) : 0);
  }, 0);
}

export function countRouteFinishes(rule, word = '') {
  const {state} = analyseRoute(rule, word);
  return state ? finishes(rule, state) : 0;
}

const px = x => 37 + 62*x;
const py = y => 145 - 50*y;
function drawRoute(svg, rule, word) {
  let lines = '', junctions = '', labels = '';
  for (let x=0;x<=3;x++) {
    lines += '<line x1="'+px(x)+'" x2="'+px(x)+'" y1="'+py(0)+'" y2="'+py(2)+'"/>';
    labels += '<text x="'+px(x)+'" y="165">'+'ABCD'[x]+'</text>';
    for (let y=0;y<=2;y++) junctions += '<circle cx="'+px(x)+'" cy="'+py(y)+'" r="4"/>';
  }
  for (let y=0;y<=2;y++) {
    lines += '<line x1="'+px(0)+'" x2="'+px(3)+'" y1="'+py(y)+'" y2="'+py(y)+'"/>';
    labels += '<text x="15" y="'+(py(y)+4)+'">'+(y+1)+'</text>';
  }
  let x=0,y=0;
  const points = [[px(0),py(0)]];
  for (const move of word) {
    if (move==='R') x++; else y++;
    points.push([px(x),py(y)]);
  }
  let marker = '';
  if (rule==='checkpoint') marker = '<path class="rm-marker" d="M99 84 l11 11 -11 11 -11 -11 Z"/>';
  if (rule==='point'||rule==='edge') {
    const cx=rule==='point'?px(1):(px(0)+px(1))/2;
    marker = '<g transform="translate('+cx+' '+py(1)+')"><circle class="rm-cross-bg" r="10"/><path class="rm-cross" d="M-5 -5 L5 5 M5 -5 L-5 5"/></g>';
  }
  svg.innerHTML = '<g class="rm-grid">'+lines+'</g><g class="rm-junction">'+junctions+'</g>'+
    '<polyline class="rm-route" points="'+points.map(p=>p.join(',')).join(' ')+'"/>'+marker+
    '<circle class="rm-cursor" cx="'+px(x)+'" cy="'+py(y)+'" r="7"/>'+
    '<g class="rm-label">'+labels+'<text x="55" y="134">Start</text><text x="223" y="29">Finish</text></g>';
  svg.setAttribute('aria-label','Route grid from A1 to D3. '+scenarios[rule].name+'. Current junction '+locationName({x,y})+'. Moves '+(word||'none')+'.');
}

export function mountRouteModel(container, lesson) {
  const mapping = lessons.get(lesson?.slot);
  if (!container || !mapping || (lesson.skill != null && lesson.skill !== mapping[0])) return false;
  const panel = document.createElement('details');
  panel.className = 'lesson-model route-model';
  panel.innerHTML = `<summary>Explore routes on a grid</summary><div class="lesson-model-body">
    <label class="rm-rule-label">Choose a route rule<select></select></label>
    <p>Travel from A1 to D3. Each step goes one street right (R) or up (U).</p>
    <p class="rm-task"></p><svg class="rm-diagram" viewBox="0 0 260 174" role="img"></svg>
    <div class="rm-actions"><button type="button" data-move="R">Right →</button><button type="button" data-move="U">Up ↑</button>
    <button type="button" data-action="undo">Undo step</button><button type="button" data-action="restart">New route</button></div>
    <p class="rm-status" role="status" aria-live="polite"></p>
    <details class="rm-saved"><summary>Routes found (0)</summary><ul></ul></details>
    <details class="rm-proof"><summary>Explain the count</summary><p class="rm-total"></p><p class="rm-working"></p><p class="rm-next"></p></details></div>`;
  container.replaceChildren(panel);
  const select = panel.querySelector('select'), saved = new Map();
  Object.entries(scenarios).forEach(([id, s]) => { select.add(new Option(s.name, id)); saved.set(id,new Set()); });
  select.value = mapping[1];
  const svg=panel.querySelector('svg'), status=panel.querySelector('.rm-status'), list=panel.querySelector('ul');
  const proof=panel.querySelector('.rm-proof'), routeList=panel.querySelector('.rm-saved');
  const right=panel.querySelector('[data-move="R"]'), up=panel.querySelector('[data-move="U"]');
  const undo=panel.querySelector('[data-action="undo"]'), restart=panel.querySelector('[data-action="restart"]');
  let word='';
  function update(note='') {
    const rule=select.value, found=saved.get(rule);
    const {state,accepted}=analyseRoute(rule,word);
    if (accepted && !note) {
      note=found.has(word)?'You already found this route. Try a different order.':'A new route! Try finding another.';
      found.add(word);
    } else if (atFinish(state) && !note) {
      note='This route missed the B2 checkpoint. Undo a step or start a new route.';
    }
    drawRoute(svg,rule,word);
    status.textContent = 'At '+locationName(state)+'. Moves: '+(word||'none')+'. '+note;
    right.disabled=state.x===3; up.disabled=state.y===2;
    undo.disabled=restart.disabled=!word;
    routeList.querySelector('summary').textContent='Routes found ('+found.size+')';
    list.replaceChildren(...Array.from(found,w=>{const li=document.createElement('li');li.textContent=w;return li;}));
    panel.querySelector('.rm-task').textContent=scenarios[rule].task;
    panel.querySelector('.rm-total').textContent=countRouteFinishes(rule)+' routes from A1 to D3.';
    panel.querySelector('.rm-working').textContent=scenarios[rule].proof;
    const r=countRouteFinishes(rule,word+'R'), u=countRouteFinishes(rule,word+'U');
    panel.querySelector('.rm-next').textContent=atFinish(state)?(accepted?'This is one of the counted routes.':'This route is outside the count.'):
      'From here, Right allows '+r+' and Up allows '+u+'. Together they give '+(r+u)+' possible completions.';
  }
  select.addEventListener('change',()=>{word='';proof.open=false;routeList.open=false;update();});
  for(const button of [right,up]) button.addEventListener('click',()=>{
    const next=analyseRoute(select.value,word+button.dataset.move);
    if (next.error) { update(next.error); return; }
    word+=button.dataset.move;
    update();
  });
  undo.addEventListener('click',()=>{word=word.slice(0,-1);update();});
  restart.addEventListener('click',()=>{word='';update();});
  update();
  return true;
}
