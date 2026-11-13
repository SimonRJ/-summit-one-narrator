/* Topic navigation from the canonical chronological course. No answer keys or future progress are exposed. */
const SHORT_NAMES={
 DIG:"Numbers & digit puzzles",
 DIV:"Divisibility, factors & remainders",
 FRAC:"Fractions, ratios & percentages",
 RATE:"Rates, speed, time & work",
 ALG:"Algebra & unknowns",
 SEQ:"Sequences & number patterns",
 COUNT:"Counting & combinations",
 LOGIC:"Logic & deduction",
 GEO:"2D geometry & measurement",
 SOLID:"3D shapes & solids",
 SPATIAL:"Grids, routes & spatial reasoning",
 DATA:"Probability, statistics & data"
};
const ordered=(a,b)=>a.slot-b.slot;
function inBatches(items,size,prefix,kind){
 return Array.from({length:Math.ceil(items.length/size)},(_,i)=>{
  const chunk=items.slice(i*size,(i+1)*size);
  return {id:kind+"-"+String(i+1).padStart(2,"0"),
    title:prefix+" "+(i*size+1)+"–"+Math.min(items.length,(i+1)*size),
    kind,items:chunk};
 });
}
export function buildCourseNavigation(course,taxonomy){
 if(!Array.isArray(course)||!Array.isArray(taxonomy?.categories))throw new Error("Course or taxonomy unavailable");
 const skillCategory=new Map(taxonomy.categories.flatMap(c=>(c.subskills||[]).map(sk=>[sk.name,c.id])));
 const groups=taxonomy.categories.map(c=>({
   id:c.id,kind:"LESSON",title:SHORT_NAMES[c.id]||c.name,
   fullTitle:c.name,items:[]
 }));
 const byId=new Map(groups.map(g=>[g.id,g]));
 const capstone={id:"CAPSTONE",kind:"LESSON",title:"Rossmoyne capstone",fullTitle:"Rossmoyne synthesis and final review",items:[]};
 const investigations=[],workshops=[];
 const seen=new Set();
 for(const item of course){
  if(!Number.isInteger(item.slot)||seen.has(item.slot))throw new Error("Repeated or invalid course slot "+item.slot);
  seen.add(item.slot);
  if(item.type==="MAWA"){investigations.push(item);continue}
  if(item.type==="MIXED"){workshops.push(item);continue}
  if(item.type!=="LESSON")throw new Error("Unknown course session type");
  const id=skillCategory.get(item.focus);
  (byId.get(id)||capstone).items.push(item);
 }
 if(course.length!==372||seen.size!==372||Math.min(...seen)!==1||Math.max(...seen)!==372)throw new Error("Course navigation requires all 372 canonical sessions");
 for(const group of groups)group.items.sort(ordered);
 capstone.items.sort(ordered);
 investigations.sort(ordered);workshops.sort(ordered);
 const topics=[...groups.filter(g=>g.items.length),...(capstone.items.length?[capstone]:[])].sort((a,b)=>a.items[0].slot-b.items[0].slot);
 const mawa=inBatches(investigations,18,"Investigations","MAWA");
 const mixed=inBatches(workshops,18,"Workshops","MIXED");
 const every=[...topics,...mawa,...mixed].flatMap(g=>g.items);
 if(every.length!==372||new Set(every.map(x=>x.slot)).size!==372)throw new Error("Every course session must appear exactly once in the menu");
 for(const g of [...topics,...mawa,...mixed])if(g.items.some((s,i)=>i&&s.slot<=g.items[i-1].slot))throw new Error("Chronology error in "+g.title);
 return {topics,mawa,mixed,all:course.slice().sort(ordered),
   totals:{lessons:topics.reduce((n,g)=>n+g.items.length,0),mawa:investigations.length,workshops:workshops.length,total:every.length}};
}
