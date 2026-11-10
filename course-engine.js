import { supabase } from "./supabase-client.js";

export const TOTAL_SESSIONS=372;
export const RANK_NAMES=[
"Cadet","Navigator","Pattern Scout","Logic Ranger","Number Pilot",
"Geometry Pathfinder","Counting Specialist","Algebra Explorer","Proof Builder","Strategy Officer",
"Problem Solver","Transfer Specialist","Olympiad Navigator","AMC Pathfinder","MAWA Investigator",
"Rossmoyne Challenger","Competition Analyst","Master Strategist","Summit Elite","Summit One"
];

let cache=null;

async function json(url){
  const r=await fetch(url,{cache:"no-store"});
  if(!r.ok) throw new Error("Could not load "+url);
  return r.json();
}
export async function requireUser(){
  const {data:{session}}=await supabase.auth.getSession();
  if(!session){location.replace("./login.html");throw new Error("Not signed in");}
  return session.user;
}
export async function loadCourse(){
  if(cache)return cache;
  await requireUser();
  const [sessions,teaching,awards,protectedContent]=await Promise.all([
    json("./data/sessions-372.json"),json("./data/teaching-72.json"),json("./data/amc-awards.json"),
    supabase.from("challenge_content").select("*").order("id",{ascending:true})
  ]);
  if(protectedContent.error) throw protectedContent.error;
  const challenges=(protectedContent.data||[]).map(x=>({
    ...x,type:x.kind,
    independent_credit:true,
    solution_video_id:x.id
  }));
  cache={sessions:sessions.sessions,sessionMeta:sessions,teaching:teaching.items,challenges,awards};
  return cache;
}
export async function getProfile(){
  const user=await requireUser();
  const [{data:profile},{data:progress}]=await Promise.all([
    supabase.from("profiles").select("*").eq("id",user.id).maybeSingle(),
    supabase.from("progress_state").select("*").eq("user_id",user.id).maybeSingle()
  ]);
  return {user,profile,progress:progress||{user_id:user.id,completed_sessions:0,current_session:0,xp:0,rank:1,overall_percent:0,state:{}}};
}
export function sessionNumber(progress){
  return Math.min(TOTAL_SESSIONS,Math.max(1,(progress?.completed_sessions||0)+1));
}
export function rankForCompleted(n){
  if(n<=0)return 1;
  return Math.max(1,Math.min(20,Math.ceil(n*20/TOTAL_SESSIONS)));
}
export function rankThreshold(rank){return Math.ceil(TOTAL_SESSIONS*rank/20)}
export function nextSlot(sessions,from,types){
  return sessions.find(s=>s.slot>=from&&types.includes(s.type))?.slot??null;
}
export function countBefore(next,current){return next==null?null:Math.max(0,next-current)}
export function tagClass(type){
  if(type==="MAWA")return "mawa"; if(type==="AMC MOCK")return "exam"; if(type==="ROSSMOYNE MOCK")return "ross"; return "";
}
export function chapterForFocus(focus){
  const s=(focus||"").toLowerCase();
  const rules=[
    ["T03",/(divisib|remainder|clock|last-digit|cycle|multiple|hcf|lcm)/],
    ["T11",/(digit|place-value|palindrome|repunits|cryptarithm)/],
    ["T02",/(working backwards|invariant|difference|fixed|total-sum|eliminating)/],
    ["T13",/(cube|area|perimeter|surface|volume|solid|painted|shaded)/],
    ["T10",/(recurrence|sequence|growth|increment|branching|finite-state|transform)/],
    ["T05",/(enumeration|arrangement|combination|neighbour|partition|case)/],
    ["T06",/(double-count|shared object|counting paths)/],
    ["T16",/(ratio|rate|speed|average|fraction|percentage|weighted|conversion)/],
    ["T12",/(angle|polygon|coordinate|grid line)/],
    ["T15",/(symmetry|tessellation|polyomino|tiling)/],
    ["T14",/(route|adjacency|network|schedule)/],
    ["T08",/(probability|favourable)/],
    ["T09",/(equation|algebra|variable|parts and wholes)/],
    ["T07",/(optimis|proving all cases|unique solution|limit)/],
    ["T17",/(proof|truth-teller|contradiction|logical deduction)/],
    ["T01",/(graph|table|model|reading)/],
    ["T18",/(method combination|evidence-based review|strategy)/]
  ];
  return (rules.find(([,re])=>re.test(s))||["T18"])[0];
}
function seed(slot,salt=0){let x=(slot*1103515245+12345+salt*2654435761)>>>0;return()=>{x=(1664525*x+1013904223)>>>0;return x/4294967296}}
export function challengePair(course,session){
  const pool=course.challenges.filter(x=>x.prompt&&x.answer!==null&&x.answer!==undefined);
  const rnd=seed(session.slot,session.focus.length);
  let a=Math.floor(rnd()*pool.length),b=Math.floor(rnd()*pool.length);
  if(b===a)b=(b+37)%pool.length;
  // Later phases deliberately bias toward harder authentic problems.
  if(session.slot>120){
    const hard=pool.filter(x=>Number(x.difficulty||3)>=4);
    if(hard.length){a=Math.floor(rnd()*hard.length);b=Math.floor(rnd()*hard.length);return [hard[a],hard[b===a?(b+1)%hard.length:b]]}
  }
  return [pool[a],pool[b]];
}
export function teachingSet(course,session){
  const chapter=chapterForFocus(session.focus);
  const items=course.teaching.filter(x=>x.chapter===chapter);
  const concept=items[(session.slot-1)%Math.max(1,items.filter(x=>x.type==="concept").length)]||items[0];
  const example=items.find(x=>x.type==="worked_example")||items.at(-1);
  return {chapter,concept,example};
}
export function normaliseAnswer(v){
  return String(v??"").toLowerCase().replace(/,/g,"").replace(/s+/g,"").replace(/cm²|cm2|cm|km|m²|m2|m|ways?|cubes?|tablets?|years?/g,"").replace(/[×*]/g,"x");
}
export function answerMatches(input,answer){
  const a=normaliseAnswer(input),b=normaliseAnswer(answer);
  if(!a)return false;
  if(a===b)return true;
  const na=Number(a),nb=Number(b); return Number.isFinite(na)&&Number.isFinite(nb)&&Math.abs(na-nb)<1e-9;
}
export async function recordAttempt(problem,slot,input,correct,solutionOpened=false,level="independent"){
  const user=await requireUser();
  const row={user_id:user.id,problem_id:problem.id,session_number:slot,answer_text:String(input||""),is_correct:Boolean(correct),
    evidence_level:level,solution_video_opened:Boolean(solutionOpened),independent_credit:Boolean(correct&&!solutionOpened&&level==="independent")};
  const {error}=await supabase.from("problem_attempts").insert(row); if(error)throw error;
}
export async function saveSessionDraft(slot,key,payload){
  const user=await requireUser();
  const row={user_id:user.id,session_number:slot,session_key:key,...payload};
  const {error}=await supabase.from("session_records").upsert(row,{onConflict:"user_id,session_number"}); if(error)throw error;
}
export async function finishSession(slot,key,payload){
  const user=await requireUser();
  const now=new Date().toISOString();
  const {error:sErr}=await supabase.from("session_records").upsert({
    user_id:user.id,session_number:slot,session_key:key,completed_at:now,immutable:true,...payload
  },{onConflict:"user_id,session_number"}); if(sErr)throw sErr;
  const completed=slot,rank=rankForCompleted(completed),pct=Number((completed/TOTAL_SESSIONS*100).toFixed(2));
  const nextPractice=(await loadCourse()).sessions.find(s=>s.slot>slot&&["AMC MOCK","ROSSMOYNE MOCK"].includes(s.type));
  const {data:old}=await supabase.from("progress_state").select("*").eq("user_id",user.id).maybeSingle();
  const {error:pErr}=await supabase.from("progress_state").upsert({
    ...(old||{}),user_id:user.id,current_session:Math.min(TOTAL_SESSIONS,slot+1),completed_sessions:completed,
    xp:(old?.xp||0)+100,rank,overall_percent:pct,next_practice_exam_in:nextPractice?nextPractice.slot-slot:null,
    updated_at:now
  },{onConflict:"user_id"}); if(pErr)throw pErr;
  return {completed,rank,pct};
}
export async function completedSessionRows(){
 const user=await requireUser();
 const {data,error}=await supabase.from("session_records").select("*").eq("user_id",user.id).not("completed_at","is",null).order("session_number");
 if(error)throw error;return data||[];
}
export async function attemptHistory(){
 const user=await requireUser();
 const {data,error}=await supabase.from("problem_attempts").select("*").eq("user_id",user.id).order("created_at",{ascending:false}).limit(1000);
 if(error)throw error;return data||[];
}
