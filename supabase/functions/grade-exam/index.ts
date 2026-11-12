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
    const {data:result,error}=await admin.rpc("seal_exam_result",{p_sitting_id:sitting_id,p_user_id:u.user.id,p_auto:Boolean(auto_submitted)});
    if(error)throw error;
    return reply(result);
  }catch(e){
    console.error(e);
    return reply({error:e?.message||"Grading failed"},500);
  }
});
