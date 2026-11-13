/** Deterministic screen divisions for every ordinary Learning lesson.
 * The original assessment controls, video players, inputs, listeners, evidence and
 * protected problem responses remain mounted in the DOM. We only toggle visibility.
 */
export function learningScreens(host,stage,{draft,skill,problem,flashDone}={}){
 const roots=[...host.children];
 const set=(node,visible)=>{if(node)node.style.display=visible?"":"none"};
 const showTop=(nodes)=>{const allow=new Set(nodes.filter(Boolean));for(const n of roots)set(n,allow.has(n))};
 const page=(title,show,guard=null,finishLabel=null)=>({title,show,guard,finishLabel});
 const get=sel=>host.querySelector(sel);
 if(stage===-1)return [page("Watch the illustrated lesson",()=>showTop(roots),"", "Start practice")];
 if(stage===0){
  const briefing=get(".lesson-recall-brief"),recall=get("#retrievalChecks"),foot=get(".complete-row");
  if(!recall)return [page("Recall",()=>showTop(roots))];
  const checks=[...recall.querySelectorAll('[id^="recall-"]')];
  const introPage=page("Connect to what you know",()=>showTop([briefing]));
  if(!checks.length)return [introPage,page("Recall check",()=>{showTop([recall]);for(const n of recall.children)set(n,true);})];
  const pages=[introPage];
  for(let i=0;i<checks.length;i++)pages.push(page("Recall check "+(i+1),()=>{
   showTop([recall]);
   for(const n of recall.children)set(n,n===checks[i]);
  }));
  return pages;
 }
 if(stage===1){
  const concept=get('[data-lesson-unit="concept"]'),bridge=get('[data-lesson-unit="bridge"]');
  const flash=get('[data-lesson-unit="flash"]'),guided=get('[data-lesson-unit="guided"]');
  const deeper=get('[data-lesson-unit="more"]');
  if(!concept)return [page("Discover",()=>showTop(roots))];
  const worked=[...concept.querySelectorAll(':scope > .worked-example')],method=concept.querySelector(':scope > .method-card');
  const methodElements=method?[...method.children]:[];
  const name=method?.querySelector(':scope > .eyebrow'),methodTitle=method?.querySelector(':scope > h3');
  const intro=method?.querySelector(':scope > p'),second=method?.querySelector(':scope > .worked-example');
  const trap=method?.querySelector(':scope > .trap-note');
  const conceptMode=(kind)=>{
   showTop([concept]);
   for(const child of [...concept.children])set(child,kind==="worked"?worked.includes(child):child===method);
   for(const child of methodElements)set(child,kind==="method"?child===name||child===methodTitle||child===intro:kind==="second"?child===second:kind==="trap"?child===intro||child===trap:false);
  };
  const pages=[];
  worked.forEach((n,i)=>pages.push(page("Watch a small example"+(worked.length>1?" "+(i+1):""),()=>{
   showTop([concept]);for(const child of [...concept.children])set(child,child===n);
  })));
  if(method){
   pages.push(page("Name the method",()=>conceptMode("method")));
   if(second)pages.push(page("Build on the example",()=>conceptMode("second")));
   if(trap)pages.push(page("Avoid a tempting mistake",()=>conceptMode("trap")));
  }
  if(bridge)pages.push(page("Connect the representations",()=>showTop([bridge])));
  if(flash)pages.push(page("Five quick decisions",()=>showTop([flash]),()=>{if(flashDone&&!flashDone()){alert("Finish the five quick decisions and read the recap before continuing.");return false}return true}));
  if(guided)pages.push(page("Solve with support",()=>showTop([guided])));
  if(deeper)pages.push(page("Optional teaching video and notes",()=>showTop([deeper]),null,"Try independently"));
  return pages;
 }
 if(stage===2||stage===3){
  const fade=get(".lesson-fade-unit"),prep=get(".lesson-prep-unit"),mix=get(".lesson-mix-unit");
  const extra=get(".lesson-extra-unit"),node=get(".lesson-problem-unit");
  if(!node)return [page("Choose the next problem",()=>showTop(roots))];
  const nested=[...node.children],problemId=problem?.id;
  const pieces={
   intro:[...node.querySelectorAll(":scope > .problem-meta, :scope > .problem-title, :scope > .problem-prompt, :scope > .original-figure, :scope > .problem-figure, :scope > .challenge-bridge")],
   answer:[...node.querySelectorAll(":scope > .problem-title, :scope > .problem-prompt, :scope > .original-figure, :scope > .problem-figure, :scope > .reasoning-help-only, :scope > .answer-label, :scope > .problem-actions, :scope > .attempt-feedback")],
   review:[...node.querySelectorAll(":scope > .problem-title, :scope > .problem-prompt, :scope > .problem-actions, :scope > .attempt-feedback, :scope > .solution-panel")]
  };
  const showProblem=type=>{
   showTop([node]);
   const showing=new Set(pieces[type]);
   for(const part of nested)set(part,showing.has(part));
  };
  const pages=[];
  if(fade)pages.push(page("Finish the worked example",()=>showTop([fade]),()=>{
   if(!draft?.evidence?.["faded:"+skill]){alert("Answer the partially worked example before moving on.");return false}return true;
  }));
  if(prep)pages.push(page("Independent basics check",()=>showTop([prep]),()=>{
   if(!draft?.evidence?.["retrieval:"+skill]){alert("Check your independent basics answer first.");return false}return true;
  }));
  const mixed=[...mix?.querySelectorAll("[data-mixed]")||[]];
  for(let i=0;i<mixed.length;i++){
    pages.push(page("Mixed-method problem "+(i+1),()=>{
      showTop([mix]);for(const child of [...mix.children])set(child,child===mixed[i]);
    },()=>{if(!draft?.evidence?.["mixed:"+i]){alert("Check your answer before continuing.");return false}return true}));
  }
  const drills=[...extra?.querySelectorAll("[data-extra-question]")||[]];
  const mode=stage===2?"try":"transfer",slot=Number(draft?.summary?.slot)||null;
  for(let i=0;i<drills.length;i++){
   const key="drill:"+mode+":"+(draft?.summary?.session_slot??problem?.learning?.session??slot)+":"+i;
   pages.push(page((mode==="try"?"Practice problem ":"Transfer problem ")+(i+1),()=>{
    showTop([extra]);for(const child of [...extra.children])set(child,child===drills[i]);
   },()=>{if(!draft?.evidence?.[key]){alert("Check this problem's answer before continuing.");return false}return true}));
  }
  pages.push(page("Read the original challenge",()=>showProblem("intro")));
  pages.push(page("Solve and enter your final answer",()=>showProblem("answer"),()=>{
   if(!problemId||!draft?.answers?.[problemId]){alert("Submit a final answer before opening the solution.");return false}return true;
  }));
  pages.push(page("Study the worked solution",()=>showProblem("review"),null,stage===2?"Transfer":"Check"));
  return pages;
 }
 if(stage===4){
   const summary=get(".lesson-check-summary"),foot=get(".complete-row");
   return [page("See your problem-solving results",()=>showTop([summary,foot]),null,"Complete and lock session")];
 }
 return [page("Learning",()=>showTop(roots))];
}
