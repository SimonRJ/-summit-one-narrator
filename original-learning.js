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

export function originalFigure(p){
 const m=p.learning;if(!m)return '';
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
 }else return '';
 return `<figure class="original-figure"><svg viewBox="0 0 360 275" role="img" aria-label="${alt}" xmlns="http://www.w3.org/2000/svg">${body}</svg><figcaption>${alt}. Use the stated conditions, not measurements from the picture.</figcaption></figure>`;
}
