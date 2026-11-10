import { supabase } from "./supabase-client.js";
import { requireUser,loadCourse,normaliseAnswer } from "./course-engine.js";

export const AMC_MARKS=[...Array(10).fill(3),...Array(10).fill(4),...Array(5).fill(5),6,7,8,9,10];
export function numericAnswer(x){
 const n=Number(normaliseAnswer(x));return Number.isFinite(n)?n:null;
}
function seeded(slot){let x=(slot*2654435761)>>>0;return()=>{x=(x*1664525+1013904223)>>>0;return x/4294967296}}
function choices(answer,index){
 const n=numericAnswer(answer);if(n===null)return null;
 const spread=Math.max(1,Math.round(Math.abs(n)*.08));
 const vals=new Set([n]);
 const offsets=[-2,-1,1,2,3,-3,5];
 for(const o of offsets){if(vals.size>=5)break;let v=n+o*spread;if(Number.isInteger(n))v=Math.round(v);if(v>=0)vals.add(v)}
 let a=[...vals].slice(0,5);
 while(a.length<5)a.push(n+a.length+1);
 const r=seeded(index+Math.round(Math.abs(n)));a=a.sort(()=>r()-.5);
 return a.map((v,i)=>({label:String.fromCharCode(65+i),value:String(v)}));
}
export async function practicePaper(slot,mode="amc"){
 const course=await loadCourse();const rnd=seeded(slot+77);
 const numeric=course.challenges.filter(q=>q.prompt&&numericAnswer(q.answer)!==null);
 const selected=[];let cursor=Math.floor(rnd()*numeric.length);
 const count=mode==="amc"?30:23;
 while(selected.length<count){const q=numeric[cursor%numeric.length];if(!selected.find(x=>x.id===q.id))selected.push(q);cursor+=7+Math.floor(rnd()*17)}
 if(mode==="amc")return {
   id:`practice-amc-${slot}`,title:`Summit One AMC Training Mock · Session ${slot}`,kind:"practice",division:"Upper Primary",duration_minutes:60,max_score:135,
   questions:selected.map((q,i)=>({number:i+1,prompt:q.prompt,answer:String(q.answer),source_id:q.id,type:i<25?"multiple_choice":"integer",choices:i<25?choices(q.answer,i):null,marks:AMC_MARKS[i],category:q.category||"reasoning"}))
 };
 const marks=selected.map((_,i)=>i<8?4:i<18?5:6);const total=marks.reduce((a,b)=>a+b,0);marks[marks.length-1]+=100-total;
 return {id:`practice-ross-${slot}`,title:`Rossmoyne-style Training Paper · Session ${slot}`,kind:"practice",duration_minutes:60,max_score:100,
 questions:selected.map((q,i)=>({number:i+1,prompt:q.prompt,answer:String(q.answer),source_id:q.id,type:"integer",choices:null,marks:marks[i],category:q.category||"reasoning"}))};
}
export function correct(response,answer){return normaliseAnswer(response)===normaliseAnswer(answer)||numericAnswer(response)!==null&&numericAnswer(response)===numericAnswer(answer)}
export function scorePaper(paper,responses){
 let total=0;const rows=paper.questions.map(q=>{const resp=responses[String(q.number)]?.value??"";const ok=correct(resp,q.answer);if(ok)total+=q.marks;return {...q,response:resp,correct:ok,earned:ok?q.marks:0}});
 return {score:total,max:paper.max_score,rows};
}
export function awardFor(score,awards,yearLevel=5,officialCutoffs=null){
 const bands=officialCutoffs||(yearLevel===6?awards.practice_estimate_wa.year6:awards.practice_estimate_wa.year5);
 const list=[["Perfect Score",bands.perfect??135],["Prize",bands.prize],["High Distinction",bands.high_distinction],["Distinction",bands.distinction],["Credit",bands.credit],["Proficiency",bands.proficiency]];
 for(const [name,min] of list)if(min!=null&&score>=min)return {name,min,official:Boolean(officialCutoffs),label:officialCutoffs?"Official paper-year cutoff":"WA practice estimate"};
 return {name:"Participation",min:0,official:Boolean(officialCutoffs),label:officialCutoffs?"Official paper-year cutoff":"WA practice estimate"};
}
export async function createSitting(paper){
 const user=await requireUser();const now=Date.now(),start=new Date(now).toISOString(),expires=new Date(now+paper.duration_minutes*60000).toISOString();
 const {data,error}=await supabase.from("exam_sittings").insert({user_id:user.id,exam_id:paper.id,exam_year:paper.year||null,started_at:start,expires_at:expires,completed:false,max_score:paper.max_score,responses:{},integer_save_times:{},metadata:{title:paper.title,kind:paper.kind}}).select().single();
 if(error)throw error;return data;
}
export async function updateSitting(sitting,responses,saveTimes={}){
 const {data,error}=await supabase.from("exam_sittings").update({responses,integer_save_times:saveTimes}).eq("id",sitting.id).select().single();if(error)throw error;return data;
}
export async function completeSitting(sitting,paper,responses,saveTimes={}){
 const result=scorePaper(paper,responses);const now=new Date().toISOString();
 const {data,error}=await supabase.from("exam_sittings").update({responses,integer_save_times:saveTimes,score:result.score,submitted_at:now,completed:true,metadata:{...(sitting.metadata||{}),result_rows:result.rows.map(r=>({number:r.number,correct:r.correct,earned:r.earned,marks:r.marks,response:r.response,answer:r.answer,source_id:r.source_id,category:r.category}))}}).eq("id",sitting.id).select().single();
 if(error)throw error;return {sitting:data,result};
}
export async function getSitting(id){const {data,error}=await supabase.from("exam_sittings").select("*").eq("id",id).maybeSingle();if(error)throw error;return data}
