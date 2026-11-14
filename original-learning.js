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

function spatialFigure(p, diagram) {
 const signature = new TextEncoder().encode(p.prompt).reduce(
  (hash, byte) => Math.imul(hash ^ byte, 16777619) >>> 0, 2166136261);
 // The live question and the static lesson manifest can deploy separately.
 if (signature !== diagram.stemSignature) return '';
 const {cells, description, gap, crease} = diagram;
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
 const columns = widths.map((w, c) => label((x[c]+x[c+1])/2, 20,
  diagram.widths ? w : String.fromCharCode(65+c))).join('');
 const rows = heights.map((h, r) => label(x[0]-16, (y[r]+y[r+1])/2+5,
  diagram.heights ? h : r+1)).join('');
 let markings = '';
 if (gap) {
  const [c, r] = gap;
  markings = `<path d="M${x[c]+1.5} ${y[r]}H${x[c+1]-1.5}" stroke="${fills['.']}" stroke-width="3"/>`;
 }
 if (crease) markings = `<path d="M${x[crease]} ${y[0]-4}V${y.at(-1)+2}" stroke="#4e2910" stroke-width="2.6" stroke-dasharray="5 4"/>`;
 return `<figure class="original-figure" data-spatial-figure><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 276 ${boardHeight}" aria-hidden="true">${rects}${columns}${rows}${markings}</svg><figcaption>${esc(description)}</figcaption></figure>`;
}

export function originalFigure(p){
 const m=p.learning;if(!m)return '';
 if(m.spatialDiagram)return spatialFigure(p,m.spatialDiagram);
 const n=m.visit+2,x=n+4;let body='',alt='';
 if(m.skill==='GEO-04'){
  const N=2*x,points=Array.from({length:N},(_,i)=>[180+105*Math.cos(2*Math.PI*i/N-Math.PI/2),135+105*Math.sin(2*Math.PI*i/N-Math.PI/2)]);
  alt=m.role==='try'?'Regular polygon with alternating blue and gold vertices':'Regular polygon with two adjacent red vertices and all other vertices blue';
  body=`<polygon points="${points.map(v=>v.join(',')).join(' ')}" fill="#102033" stroke="#92cfe5" stroke-width="2"/>`+points.map(([a,b],i)=>`<circle cx="${a}" cy="${b}" r="7" fill="${m.role==='try'?(i%2?'#edc557':'#74baff'):(i<2?'#f0787b':'#74baff')}" stroke="#0a1422" stroke-width="2"/>`).join('');
 }else if(m.skill==='SPATIAL-01'){
  const cap=m.session===366&&m.role==='transfer',a=cap?4:n%4+3,b=cap?3:2,scale=Math.min(46,280/a),left=(360-a*scale)/2,top=50;
  alt='Coordinate grid showing the start, finish and '+(m.role==='try'?'required waypoint':'blocked points');
  const pt=(i,j)=>[left+i*scale,top+(b-j)*scale];
  for(let i=0;i<=a;i++){const [u,v]=pt(i,0),[,w]=pt(i,b);body+=`<path d="M${u},${v}V${w}" stroke="#38566e"/>`;}
  for(let j=0;j<=b;j++){const [u,v]=pt(0,j),[w]=pt(a,j);body+=`<path d="M${u},${v}H${w}" stroke="#38566e"/>`;}
  for(const [i,j,label,color] of [[0,0,'S (0,0)','#91dcbd'],[a,b,`T (${a},${b})`,'#91dcbd'],[1,1,m.role==='try'?'via (1,1)':'blocked','#f3bc7c'],...(cap?[[3,2,'blocked','#f3bc7c']]:[])]){const [u,v]=pt(i,j);body+=`<circle cx="${u}" cy="${v}" r="5" fill="${color}"/><text x="${u}" y="${v+23}" text-anchor="middle" fill="#f0f4fb" font-size="13">${label}</text>`;}
 }else if(m.skill==='SOLID-01' && m.visit>1){
  const long=m.visit+6;
  // Each card labels an actual given dimension or layer count. Neither an
  // inferred result nor an answer value is drawn. The illustration is schematic.
  const options=m.role==='try'?{
    2:[['FULL BLOCK',`${long} × 3 × 4`],['REMOVED PIECE','5 × 2 × 1']],
    3:[['LARGE CUBOID',`${long} × 2 × 5`],['ATTACHED ARM',`${long-5} × 2 × 1`]],
    4:[['COMPLETE SHELVES',`${long-1} shelves of 12`],['FINAL SHELF','2 cubes']],
    5:[['FULL BLOCK',`${long} × 4 × 3`],['REMOVED EDGE','10 cubes']],
    6:[['FULL BLOCK',`${long} × 2 × 6`],['TWO BARS','5 cubes each']],
    7:[['FIRST',`${long} × 1 × 3`],['SECOND',`${long} × 1 × 4`],['THIRD',`${long-2} × 1 × 5`]],
    8:[['FULL ROWS','12 rows'],['EACH ROW',`${long} positions`],['EMPTY','10 positions']]
  }[m.visit]:{
    2:[['COMPLETE BLOCK',`${long} × 11 × 3`],['REMOVE','top layer']],
    3:[['FIRST CUBOID',`${long} × 3 × 4`],['SECOND CUBOID',`${long} × 2 × 5`]],
    4:[['FULL BLOCK',`${long} × 6 × 4`],['GROOVE',`${long} × 1 × 2`]],
    5:[['FULL BLOCK',`${long} × 5 × 5`],['CHANNEL',`${long} × 3 × 1`]],
    6:[['ONE LAYER','4 × 6 grid'],['EMPTY CORNERS','2 per layer'],['LAYERS',`${long}`]],
    7:[['FIRST TOWER','5 × 2 base'],['SECOND TOWER','3 × 4 base'],['HEIGHT',`${long} cubes`]],
    8:[['MAIN SECTION','3 × 6 cubes'],['PATCH','2 × 2 cubes'],['ROWS',`${long}`]]
  }[m.visit];
  if(!options)return '';
  alt='Given unit-cube dimensions in separate schematic cards, not to scale';
  const gap=8,width=(324-gap*(options.length-1))/options.length;
  body=options.map(([name,measure],i)=>{
    const left=18+i*(width+gap),centre=left+width/2;
    const labelSize=options.length===3?10:12;
    return `<g>
      <rect x="${left}" y="46" rx="9" width="${width}" height="178" fill="#122b41" stroke="#41647a" stroke-width="1.5"/>
      <path d="M${centre-40} 108 l20 -18 h60 l-20 18 z" fill="#a7dbe8" stroke="#82b6c6" stroke-width="1"/>
      <path d="M${centre-40} 108 h60 v38 h-60 z" fill="#5aacc1" stroke="#82b6c6" stroke-width="1"/>
      <path d="M${centre+20} 108 l20 -18 v38 l-20 18 z" fill="#37788e" stroke="#82b6c6" stroke-width="1"/>
      <text x="${centre}" y="65" fill="#edf7ff" stroke="none" text-anchor="middle" font-size="${labelSize}" font-weight="600">${name}</text>
      <text x="${centre}" y="185" fill="#f2f8fc" stroke="none" text-anchor="middle" font-size="${options.length===3?13:16}">${measure}</text>
      <text x="${centre}" y="204" fill="#bbd0db" stroke="none" text-anchor="middle" font-size="10">as stated</text>
    </g>`;
  }).join('')+`<text x="180" y="243" font-size="11" fill="#bed5e0" text-anchor="middle" stroke="none">Schematic only · use the problem's given dimensions</text>`;
 }else if(m.skill==='DATA-03'){
  const count=m.visit+6;
  if(m.role==='try'){
    alt=`Pictogram: Monday ${count} full symbols plus one half-symbol; Tuesday ${count+2} full symbols; one full symbol represents six bicycles`;
    const monday=count,tuesday=count+2,space=248/(tuesday+1),radius=Math.min(7,space*.39);
    const icon=(i,y,half=false)=>{
      const cx=76+i*space;
      return `<circle cx="${cx}" cy="${y}" r="${radius}" fill="${half?'#27465a':'#98d7e5'}" stroke="#78afbf" stroke-width="1.5"/>`+
       (half?`<path d="M${cx},${y-radius} A${radius},${radius} 0 0 0 ${cx},${y+radius} Z" fill="#98d7e5"/>`:'');
    };
    body=`<text x="18" y="49" font-size="14" fill="#edf6ff" font-weight="600" stroke="none">Key: one full symbol = 6 bikes</text>
      <text x="18" y="108" font-size="14" fill="#e9f4fa" stroke="none">Mon</text>
      <text x="18" y="170" font-size="14" fill="#e9f4fa" stroke="none">Tue</text>`+
      Array.from({length:monday},(_,i)=>icon(i,102)).join('')+
      icon(monday,102,true)+
      Array.from({length:tuesday},(_,i)=>icon(i,164)).join('')+
      `<text x="180" y="226" font-size="12" text-anchor="middle" fill="#c2dce8" stroke="none">Half-symbol = half of one full symbol</text>`;
  }else{
    const start=5*count,scale=6,left=79,base=221,ya=base-8*scale,yb=base-13*scale;
    alt=`Bar chart with the vertical axis starting at ${start} instead of zero, bar A rising 8 units and bar B rising 13 units above that baseline`;
    const tick=(n)=>`<g><path d="M${left-6} ${base-n*scale} H${left+244}" stroke="#30516a" stroke-width="1"/><text x="${left-9}" y="${base-n*scale+5}" font-size="12" text-anchor="end" fill="#d4e8f0" stroke="none">${start+n}</text></g>`;
    body=tick(0)+tick(5)+tick(10)+tick(15)+
      `<path d="M${left} 48 V${base} H328" fill="none" stroke="#b3d7e4" stroke-width="2"/>
       <rect x="122" y="${ya}" width="64" height="${base-ya}" fill="#82bcd0" stroke="#a3e0f0"/>
       <rect x="230" y="${yb}" width="64" height="${base-yb}" fill="#52a2bd" stroke="#a3e0f0"/>
       <text x="154" y="${ya-11}" font-size="14" text-anchor="middle" fill="#dceff7" stroke="none">+8</text>
       <text x="262" y="${yb-11}" font-size="14" text-anchor="middle" fill="#dceff7" stroke="none">+13</text>
       <text x="154" y="242" font-size="14" text-anchor="middle" fill="#f0f7ff" stroke="none">A</text>
       <text x="262" y="242" font-size="14" text-anchor="middle" fill="#f0f7ff" stroke="none">B</text>
       <text x="180" y="263" font-size="11" text-anchor="middle" fill="#bdd5e1" stroke="none">Notice the axis begins at ${start}, not zero</text>`;
  }
 }else return '';
 return `<figure class="original-figure"><svg viewBox="0 0 360 275" role="img" aria-label="${alt}" xmlns="http://www.w3.org/2000/svg">${body}</svg><figcaption>${alt}. Use the stated conditions, not measurements from the picture.</figcaption></figure>`;
}
