// Curriculum mapping is explicit. Never fall back to a real paper or a loose topic match.
export const LEARNING_VERSION='recognition-20261113';
export function selectOriginalProblems(session,bank,manifest){
 if(session.type!=='LESSON')return [];
 const entries=manifest.filter(x=>x.session===session.slot);
 if(entries.length!==2||!entries.some(x=>x.role==='try')||!entries.some(x=>x.role==='transfer'))throw Error('This lesson is missing its original practice pair.');
 return ['try','transfer'].map(role=>{
  const entry=entries.find(x=>x.role===role),p=bank.find(x=>x.id===entry.id);
  if(!p||p.source_type!=='original_authored'||!/^O\d{3}[TX]$/.test(p.id))throw Error('Original lesson content could not be loaded. Please reconnect and reopen the session.');
  return {...p,learning:entry};
 });
}
export function familySeen(records,family){return records.some(r=>Object.values(r.evidence||{}).some(e=>e?.kind==='application'&&e.family===family));}
/** An actual submitted answer, rather than a typed explanation, gates review. */
export function reasoningReady(draft,id){return Boolean(draft?.answers?.[id]?.response)}
export function applicationStatus(e){
 if(!e)return 'Not attempted';
 if(e.correct!==true)return 'Needs another try';
 if(e.used_help)return 'Solved with support';
 return e.familiar_family?'Solved independently · familiar pattern':'Solved independently · first try in this setting';
}
const esc=s=>String(s??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
/** Keep optional help and honest independence recording, with no required typing. */
export function mountReasoning(node,{p,draft,save,showHint}){
 const key='reasoning:'+p.id,e=draft.evidence[key]||{used_help:false};
 draft.evidence[key]=e;
 const panel=document.createElement('section');panel.className='reasoning-record reasoning-help-only';
 panel.innerHTML=`<p class="muted">Solve this problem on paper, then enter only your final answer. Use a hint if you need one.</p><div class="reasoning-help-actions"><button type="button" class="ghost method-hint">Show a starting hint</button><label class="support-choice"><input type="checkbox" class="used-help" ${e.used_help?'checked':''}> I used a hint or help</label></div><p class="method-hint-text" role="status"></p>`;
 node.querySelector('.problem-prompt').after(panel);
 panel.querySelector('.used-help').onchange=async event=>{
  e.used_help=event.target.checked||e.hint_opened===true;
  event.target.checked=e.used_help;
  try{await save()}catch(err){panel.querySelector('.method-hint-text').textContent='Cloud save failed: '+err.message}
 };
 panel.querySelector('.method-hint').onclick=async()=>{
  e.hint_opened=true;e.used_help=true;
  panel.querySelector('.used-help').checked=true;
  panel.querySelector('.method-hint-text').textContent=showHint();
  try{await save()}catch(err){panel.querySelector('.method-hint-text').textContent+=' Hint could not sync: '+err.message}
 };
 return e;
}
export function transferEvidenceHTML(records){
 const ev=records.flatMap(r=>Object.values(r.evidence||{})).filter(e=>e?.kind==='application'&&e.role==='transfer');
 const first=new Set(ev.filter(e=>e.correct===true&&!e.used_help&&!e.familiar_family).map(e=>e.family));
 const support=ev.filter(e=>e.correct===true&&e.used_help).length;
 return `<section class="transfer-evidence"><h2>Applying ideas in other settings</h2><p><b>${first.size}</b> different transfer patterns solved correctly on a first unassisted attempt. <b>${support}</b> transfer attempts solved with support.</p><p class="muted">A new set of numbers in a familiar pattern counts as practice. Worked solutions remain available after attempts; a correct answer alone does not guarantee readiness for unfamiliar problems. Mixed mocks and fresh past papers give additional evidence.</p></section>`;
}

function matchesStem(prompt, diagram) {
 // The live question and the static lesson manifest can deploy separately.
 return new TextEncoder().encode(prompt).reduce(
  (hash, byte) => Math.imul(hash ^ byte, 16777619) >>> 0, 2166136261) === diagram.stemSignature;
}

function spatialFigure(p, diagram) {
 if (!matchesStem(p.prompt, diagram)) return '';
 const {cells, description, gap, crease, hideLabels} = diagram;
 const widths = diagram.widths || Array(cells[0].length).fill(1);
 const heights = diagram.heights || Array(cells.length).fill(1);
 const sum = values => values.reduce((total, value) => total + value, 0);
 const unit = Math.min(34, (diagram.widths ? 205 : 230) / sum(widths), 145 / sum(heights));
 const offsets = (values, start) => values.reduce(
  (positions, value) => [...positions, positions.at(-1) + value * unit], [start]);
 const x = offsets(widths, (276 - unit * sum(widths)) / 2 + 8);
 const y = offsets(heights, 29);
 const boardHeight = y.at(-1) + 5;
 const fills = {'.':'#e4edf4', d:'#6e829a', '#':'#6e829a', X:'#fab958'};
 const label = (a, b, content) => `<text x="${a}" y="${b}" text-anchor="middle" fill="#edf6ff" font-size="16">${content}</text>`;
 const rects = cells.flatMap((row, r) => Array.from(row, (cell, c) => {
  if (cell === ' ') return '';
  const cx = (x[c] + x[c+1]) / 2, cy = (y[r] + y[r+1]) / 2;
  return `<rect x="${x[c]}" y="${y[r]}" width="${widths[c]*unit}" height="${heights[r]*unit}" fill="${fills[cell]}" stroke="#233e56" stroke-width="1.3"/>` +
   (cell === 'X' ? `<circle cx="${cx}" cy="${cy}" r="4" fill="#253748"/>` : '');
 })).join('');
 const columns = hideLabels ? '' : widths.map((w, c) => label((x[c]+x[c+1])/2, 20,
  diagram.widths ? w : String.fromCharCode(65+c))).join('');
 const rows = hideLabels ? '' : heights.map((h, r) => label(x[0]-16, (y[r]+y[r+1])/2+5,
  diagram.heights ? h : r+1)).join('');
 let markings = '';
 if (gap) {
  const [c, r] = gap;
  markings = `<path d="M${x[c]+1.5} ${y[r]}H${x[c+1]-1.5}" stroke="${fills['.']}" stroke-width="3"/>`;
 }
 if (crease) markings = `<path d="M${x[crease]} ${y[0]-4}V${y.at(-1)+2}" stroke="#4e2910" stroke-width="2.6" stroke-dasharray="5 4"/>`;
 return `<figure class="original-figure" data-lesson-figure><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 276 ${boardHeight}" aria-hidden="true">${rects}${columns}${rows}${markings}</svg><figcaption>${esc(description)}</figcaption></figure>`;
}

function dataDisplay(p, display) {
 if (!matchesStem(p.prompt, display)) return '';
 const {kind, caption} = display;
 if (kind === 'table') {
  const heading = display.columns.map(column => `<th scope="col">${esc(column)}</th>`).join('');
  const rows = display.rows.map(([label, ...values]) =>
   `<tr><th scope="row">${esc(label)}</th>${values.map(value => `<td>${esc(value)}</td>`).join('')}</tr>`).join('');
  return `<figure class="original-figure original-data" data-lesson-figure><table><caption>${esc(caption)}</caption><thead><tr>${heading}</tr></thead><tbody>${rows}</tbody></table></figure>`;
 }
 const {labels, values, ticks} = display;
 const low = ticks[0], high = ticks.at(-1);
 const left = 42, right = 262, base = 135, slot = (right - left) / labels.length;
 const height = value => 102 * (value - low) / (high - low);
 const tickMarks = ticks.map(tick => {
  const y = base - height(tick);
  return `<path d="M${left-4} ${y}H${right}" stroke="#59708a"/><text x="${left-9}" y="${y+5}" text-anchor="end">${tick}</text>`;
 }).join('');
 const bars = labels.map((label, index) => {
  const x = left + (index + .5) * slot, h = height(values[index]);
  return `<rect x="${x-16}" y="${base-h}" width="32" height="${h}" fill="#8bd8d8"/><text x="${x}" y="157" text-anchor="middle">${esc(label)}</text>`;
 }).join('');
 return `<figure class="original-figure original-data" data-lesson-figure><svg viewBox="0 0 276 169" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="#edf6ff" font-size="15">${tickMarks}${bars}<path d="M${left} 28V${base}H${right}" fill="none" stroke="#edf6ff" stroke-width="1.4"/></svg><figcaption>${esc(caption)}</figcaption></figure>`;
}

function drawGeometry(diagram) {
 const {lines, labels = [], fills = [], points = [], openPoints = [], closed = [], circles = []} = diagram;
 const coordinates = vertices => vertices.map(point => point.join(',')).join(' ');
 return fills.map(vertices => `<polygon points="${coordinates(vertices)}" fill="#326e82"/>`).join('') +
  circles.map(([x,y,r]) => `<circle cx="${x}" cy="${y}" r="${r}" fill="none" stroke="#9ecddd" stroke-width="1.6"/>`).join('') +
  lines.map(vertices => `<polyline points="${coordinates(vertices)}" fill="none" stroke="#9ecddd" stroke-width="1.6" stroke-linejoin="round"/>`).join('') +
  closed.map(vertices => `<polyline points="${coordinates(vertices)}" fill="none" stroke="#f4b583" stroke-width="2.7" stroke-dasharray="4 3"/>`).join('') +
  points.map(([x,y]) => `<circle cx="${x}" cy="${y}" r="3.1" fill="#a8e4d3"/>`).join('') +
  openPoints.map(([x,y]) => `<circle cx="${x}" cy="${y}" r="3.8" fill="#0b1b2c" stroke="#f4b583" stroke-width="2"/>`).join('') +
  labels.map(([x,y,label]) => `<text x="${x}" y="${y}" text-anchor="middle">${esc(label)}</text>`).join('');
}

function drawCuboid(diagram) {
 const [length, width, height] = diagram.dimensions;
 const [lengthLabel,widthLabel,heightLabel]=diagram.labels;
 const scale = Math.min(22, 166 / (length + width * .65), 117 / (height + width * .4));
 const project = ([x,y,z]) => [46 + scale * (x + .65*y), 145 - scale * (z + .4*y)];
 const path = (vertices, fill = 'none', stroke = '#6b9cb5', strokeWidth = 1) =>
  `<polyline points="${vertices.map(v => project(v).join(',')).join(' ')}" fill="${fill}" stroke="${stroke}" stroke-width="${strokeWidth}" stroke-linejoin="round"/>`;
 const colour = (face, shade) => diagram.faceColours?.[face] ?? (diagram.faces?.includes(face) ? '#4e8998' : shade);
 const front = [[0,0,0],[length,0,0],[length,0,height],[0,0,height],[0,0,0]];
 const right = [[length,0,0],[length,width,0],[length,width,height],[length,0,height],[length,0,0]];
 const top = [[0,0,height],[length,0,height],[length,width,height],[0,width,height],[0,0,height]];
 let body = path(front,colour('front','#1d394e')) + path(right,colour('right','#183146')) + path(top,colour('top',diagram.openTop?'#0d1d2c':'#27475f'));
 const addLine = (start,end) => { body += path([start,end]); };
 for(let x=1;lengthLabel!=='?'&&x<length;x++){
  addLine([x,0,0],[x,0,height]);
  if(!diagram.openTop)addLine([x,0,height],[x,width,height]);
 }
 for(let y=1;widthLabel!=='?'&&y<width;y++){
  addLine([length,y,0],[length,y,height]);
  if(!diagram.openTop)addLine([0,y,height],[length,y,height]);
 }
 for(let z=1;heightLabel!=='?'&&z<height;z++){
  addLine([0,0,z],[length,0,z]);
  addLine([length,0,z],[length,width,z]);
 }
 if(diagram.markTop){
  const [x,y]=project([length/2,width/2,height]);
  body += `<circle cx="${x}" cy="${y}" r="4.2" fill="#fab958" stroke="#203549" stroke-width="1.3"/>`;
 }
 const label = (point,dx,dy,value) => {
  const [x,y]=project(point);
  return `<text x="${x+dx}" y="${y+dy}" text-anchor="middle">${esc(value)}</text>`;
 };
 return body + label([length/2,0,0],0,19,lengthLabel) + label([length,width/2,0],13,14,widthLabel) + label([0,0,height/2],-14,5,heightLabel);
}

function drawPictogram(diagram) {
 return diagram.rows.map(([label,count,half],row) => {
  const y = 39+47*row;
  const symbols = Array.from({length:count+(half?1:0)},(_,i) => {
   const x = 61+21*i;
   if(i<count)return `<circle cx="${x}" cy="${y}" r="7" fill="#96d9df"/>`;
   return `<circle cx="${x}" cy="${y}" r="7" fill="none" stroke="#96d9df"/><path d="M${x} ${y-7}a7 7 0 0 0 0 14z" fill="#96d9df"/>`;
  }).join('');
  return `<text x="12" y="${y+5}">${esc(label)}</text>${symbols}`;
 }).join('');
}

export function originalFigure(p){
 const m=p.learning;
 if(!m)return '';
 if(m.spatialDiagram)return spatialFigure(p,m.spatialDiagram);
 if(m.dataDisplay)return dataDisplay(p,m.dataDisplay);
 const diagram=m.geometryDiagram || m.cuboidDiagram || m.pictogram;
 if(!diagram || !matchesStem(p.prompt,diagram))return '';
 const body=m.geometryDiagram ? drawGeometry(diagram) : m.cuboidDiagram ? drawCuboid(diagram) : drawPictogram(diagram);
 const height=m.pictogram?115:184;
 return `<figure class="original-figure" data-lesson-figure><svg viewBox="0 0 276 ${height}" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="#edf6ff" font-size="15">${body}</svg><figcaption>${esc(diagram.caption)}</figcaption></figure>`;
}
