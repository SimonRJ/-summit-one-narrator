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
  const node=get(".lesson-problem-unit");
  if(!node)return [page("Choose the next method",()=>showTop(roots))];
  const nested=[...node.children];
  const reason=node.querySelector(".reasoning-record");
  const rChildren=reason?[...reason.children]:[];
  const rGrid=reason?.querySelector(".check-grid"),rLabels=rGrid?[...rGrid.children]:[];
  const parts={
   intro:[...node.querySelectorAll(":scope > .problem-meta, :scope > .problem-title, :scope > .problem-prompt, :scope > .original-figure, :scope > .problem-figure, :scope > .challenge-bridge")],
   thinking:[reason],
   answer:[...node.querySelectorAll(":scope > .answer-label, :scope > .problem-actions, :scope > .attempt-feedback")],
   review:[...node.querySelectorAll(":scope > .problem-actions, :scope > .attempt-feedback, :scope > .solution-panel")]
  };
  const showProblem=(kind,label=0)=>{
   showTop([node]);
   const setParts=new Set(parts[kind]||[]);
   for(const part of nested)set(part,setParts.has(part));
   if(reason){
    for(const child of rChildren)set(child,kind==="thinking"&&(label===0?child===rGrid||child.tagName==="H3"||child.tagName==="P":child===rGrid||child.classList.contains("support-choice")||child.classList.contains("method-hint")||child.classList.contains("method-hint-text")));
    rLabels.forEach((el,i)=>set(el,kind==="thinking"&&i===label));
   }
  };
  const pages=[],pId=problem?.id;
  if(fade)pages.push(page("Finish a worked example",()=>showTop([fade]),()=>{
   if(!draft?.evidence?.["faded:"+skill]){alert("Complete the partly worked example before moving on.");return false}return true;
  }));
  if(prep)pages.push(page("Independent basics check",()=>showTop([prep]),()=>{
   if(!draft?.evidence?.["retrieval:"+skill]){alert("Record the independent basics check before opening the new problem.");return false}return true;
  }));
  if(mix)pages.push(page("Choose between two methods",()=>showTop([mix])));
  pages.push(page("Read your new problem",()=>showProblem("intro")));
  if(reason){
   pages.push(page("What clue tells you the method?",()=>showProblem("thinking",0)));
   pages.push(page("Explain your plan",()=>showProblem("thinking",1)));
  }
  pages.push(page("Work out and submit your answer",()=>showProblem("answer"),()=>{
   if(!pId||!draft?.answers?.[pId]){alert("Record your first attempt before moving to the solution review. Your draft remains saved.");return false}return true;
  }));
  pages.push(page("Compare your reasoning with the solution",()=>showProblem("review"),null,stage===2?"Transfer":"Check"));
  return pages;
 }
 if(stage===4){
  const grid=get(".check-grid"),checks=get(".transfer-checks"),foot=get(".complete-row");
  const take=get("#takeaway")?.closest("label"),watch=get("#watch")?.closest("label");
  const checkItems=checks?[...checks.querySelectorAll(".check-status")]:[];
  const conf=get("#transferConfidence")?.closest("label");
  const gridChildren=grid?[...grid.children]:[],checkChildren=checks?[...checks.children]:[];
  const showGrid=which=>{
   showTop([grid]);gridChildren.forEach(n=>set(n,n===which));
  };
  const showCheck=which=>{
   showTop([checks]);checkChildren.forEach(n=>set(n,n===which));
  };
  const pages=[];
  if(take)pages.push(page("The key idea you discovered",()=>showGrid(take)));
  if(watch)pages.push(page("What to watch for next time",()=>showGrid(watch)));
  for(let i=0;i<checkItems.length;i++)pages.push(page("Check problem "+(i+1),()=>showCheck(checkItems[i])));
  pages.push(page("Decide your next learning step",()=>{
   showTop([checks,foot]);checkChildren.forEach(n=>set(n,n===conf||n.classList.contains("muted")));
  },null,"Complete and lock session"));
  return pages;
 }
 return [page("Learning",()=>showTop(roots))];
}
