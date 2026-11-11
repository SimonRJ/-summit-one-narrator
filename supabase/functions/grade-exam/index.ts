import { createClient } from "npm:@supabase/supabase-js@2.78.0";

const url=Deno.env.get("SUPABASE_URL")!;
const anon=Deno.env.get("SUPABASE_ANON_KEY")!;
const service=Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const headers={
  "Access-Control-Allow-Origin":"https://simonrj.github.io",
  "Access-Control-Allow-Headers":"authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods":"POST, OPTIONS",
  "Content-Type":"application/json"
};
const reply=(body:unknown,status=200)=>new Response(JSON.stringify(body),{status,headers});
const norm=(v:unknown)=>String(v??"").trim().toLowerCase().replace(/\s+/g,"").replace(/[.,;:]$/g,"");
function correctFor(q:any,response:any){
  const ans=q.answer;
  if(response===undefined||response===null||response==="") return false;
  if(q.question_type==="multiple_choice"){
    const expected=typeof ans==="string"?ans:(ans?.choice ?? ans?.value ?? "");
    return norm(response)===norm(expected);
  }
  const expected=typeof ans==="object"&&ans!==null?(ans.value ?? ans.answer ?? ""):ans;
  return /^\d{1,3}$/.test(String(response).trim())&&Number(response)===Number(expected);
}
function explicitStars(q:any){
  const raw=q?.metadata?.stars ?? q?.metadata?.star_rating ?? q?.metadata?.difficulty_stars;
  const n=Number(raw);
  return [3,4,5].includes(n)?n:null;
}
function awardFor(score:number,exam:any,sitting:any){
  if(exam.max_score!==135) return {label:null,estimated:false};
  const sittingYear=Number(sitting?.metadata?.student_year||0);
  const studentYear=sittingYear===5||sittingYear===6?sittingYear:(exam.student_year===6?6:5);
  const y=studentYear===6?"year6":"year5";
  const estimates:any={
    year5:{proficiency:32,credit:49,distinction:64,high_distinction:83,prize:106,perfect:135},
    year6:{proficiency:32,credit:58,distinction:73,high_distinction:92,prize:118,perfect:135}
  };
  const c=exam.award_cutoffs || estimates[y];
  const estimated=!exam.award_cutoffs;
  if(score===135) return {label:"Perfect practice score",estimated,student_year:studentYear};
  if(score>=(c.prize??999)) return {label:"Prize range",estimated,student_year:studentYear};
  if(score>=(c.high_distinction??999)) return {label:"High Distinction",estimated,student_year:studentYear};
  if(score>=(c.distinction??999)) return {label:"Distinction",estimated,student_year:studentYear};
  if(score>=(c.credit??999)) return {label:"Credit",estimated,student_year:studentYear};
  if(score>=(c.proficiency??32)) return {label:"Proficiency",estimated,student_year:studentYear};
  return {label:"Participation",estimated,student_year:studentYear};
}
Deno.serve(async(req)=>{
  if(req.method==="OPTIONS") return new Response("ok",{headers});
  if(req.method!=="POST") return reply({error:"Method not allowed"},405);
  try{
    const auth=req.headers.get("Authorization");
    if(!auth?.startsWith("Bearer ")) return reply({error:"Authentication required"},401);
    const token=auth.slice(7);
    const scoped=createClient(url,anon,{global:{headers:{Authorization:auth}},auth:{persistSession:false,autoRefreshToken:false}});
    const {data:u,error:ue}=await scoped.auth.getUser(token);
    if(ue||!u.user) return reply({error:"Invalid session"},401);
    const {sitting_id,auto_submitted=false}=await req.json();
    if(!sitting_id) return reply({error:"Missing sitting_id"},400);
    const admin=createClient(url,service,{auth:{persistSession:false,autoRefreshToken:false}});
    const {data:sitting,error:se}=await admin.from("exam_sittings").select("*").eq("id",sitting_id).eq("user_id",u.user.id).single();
    if(se||!sitting) return reply({error:"Sitting not found"},404);
    const {data:exam,error:ee}=await admin.from("exam_catalog").select("*").eq("id",sitting.exam_id).single();
    if(ee||!exam) throw ee||new Error("Exam missing");
    const {data:questions,error:qe}=await admin.from("exam_questions").select("*").eq("exam_id",sitting.exam_id).order("question_number");
    if(qe) throw qe;
    if((questions||[]).length!==exam.question_count) return reply({error:"Exam question set is incomplete"},409);
    const responses=sitting.responses||{};
    let score=0;
    const rows=(questions||[]).map((q:any)=>{
      const response=responses[String(q.question_number)] ?? responses[q.question_number];
      const ok=correctFor(q,response);
      const earned=ok?q.marks:0; score+=earned;
      const ans=typeof q.answer==="object"&&q.answer!==null?(q.answer.choice??q.answer.value??q.answer.answer??q.answer):q.answer;
      return {
        question_number:q.question_number,question_type:q.question_type,stem:q.stem,choices:q.choices,
        response:response??null,correct:ok,earned,marks:q.marks,correct_answer:ans,
        explanation:q.explanation,image_ref:q.image_ref,metadata:q.metadata,category:q.category,stars:explicitStars(q)
      };
    });
    const award=awardFor(score,exam,sitting);
    const starAdded={3:rows.filter((r:any)=>r.correct&&r.stars===3).length,4:rows.filter((r:any)=>r.correct&&r.stars===4).length,5:rows.filter((r:any)=>r.correct&&r.stars===5).length};
    let starTotals:any=null;
    const now=new Date().toISOString();
    if(!sitting.completed){
      const metadata={...(sitting.metadata||{}),auto_submitted:Boolean(auto_submitted),award:award.label,award_estimated:award.estimated,award_student_year:award.student_year,star_correct_added:starAdded};
      const {data:sealed,error:up}=await admin.from("exam_sittings")
        .update({score,submitted_at:now,completed:true,metadata})
        .eq("id",sitting.id).eq("completed",false).select("id").maybeSingle();
      if(up) throw up;
      if(sealed && (starAdded[3]||starAdded[4]||starAdded[5])){
        const {data:totals,error:te}=await admin.rpc("increment_timed_star_correct",{p_user:u.user.id,p3:starAdded[3],p4:starAdded[4],p5:starAdded[5]});
        if(te) throw te;
        const t=Array.isArray(totals)?totals[0]:totals;
        if(t)starTotals={3:Number(t.star3_correct||0),4:Number(t.star4_correct||0),5:Number(t.star5_correct||0)};
      }
    }
    const finalFive=rows.filter((r:any)=>r.question_number>=26&&r.question_number<=30);
    const finalFiveSummary=exam.max_score===135?{
      correct:finalFive.filter((r:any)=>r.correct).length,
      count:finalFive.length,
      earned:finalFive.reduce((s:number,r:any)=>s+r.earned,0),
      max:finalFive.reduce((s:number,r:any)=>s+r.marks,0)
    }:null;
    return reply({ok:true,exam:{id:exam.id,title:exam.title,year:exam.year,division:exam.division,student_year:award.student_year,max_score:exam.max_score,source_type:exam.source_type},score,max_score:exam.max_score,award,rows,final_five:finalFiveSummary,star_correct_added:starAdded,star_totals:starTotals});
  }catch(e){
    console.error(e);
    return reply({error:e?.message||"Grading failed"},500);
  }
});
