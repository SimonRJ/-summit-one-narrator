
import { createClient } from "npm:@supabase/supabase-js@2.78.0";
const url=Deno.env.get("SUPABASE_URL")!, anon=Deno.env.get("SUPABASE_ANON_KEY")!, service=Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const headers={"Access-Control-Allow-Origin":"https://simonrj.github.io","Access-Control-Allow-Headers":"authorization, x-client-info, apikey, content-type","Access-Control-Allow-Methods":"POST, OPTIONS","Content-Type":"application/json"};
const reply=(b:unknown,s=200)=>new Response(JSON.stringify(b),{status:s,headers});
const norm=(v:unknown)=>String(v??"").trim().toLowerCase().replace(/\s+/g,"").replace(/[×·]/g,"*").replace(/[²]/g,"^2").replace(/[³]/g,"^3").replace(/[.,;:]$/g,"");
export function numberValue(v:unknown){
 const s=String(v??"").trim().replace(/−/g,"-");
 if(/^[+-]?(?:\d+(?:\.\d+)?|\.\d+)$/.test(s))return Number(s);
 const f=s.match(/^([+-]?\d+)\s*\/\s*(\d+)$/);return f&&Number(f[2])!==0?Number(f[1])/Number(f[2]):null;
}
export function grade(expected:any,response:string){
 const e=numberValue(expected);if(e!==null){const r=numberValue(response);return r===null?null:Math.abs(e-r)<1e-10;}
 if(typeof expected==="string"&&expected.length<=12&&/^[a-z .+-]+$/i.test(expected))return norm(response)===norm(expected);
 return null; // Proofs and ambiguous prose need reasoning review, never first-number extraction.
}
Deno.serve(async req=>{
  if(req.method==="OPTIONS")return new Response("ok",{headers});
  if(req.method!=="POST")return reply({error:"Method not allowed"},405);
  try{
    const auth=req.headers.get("Authorization"); if(!auth?.startsWith("Bearer "))return reply({error:"Authentication required"},401);
    const scoped=createClient(url,anon,{global:{headers:{Authorization:auth}},auth:{persistSession:false,autoRefreshToken:false}});
    const {data:u,error:ue}=await scoped.auth.getUser(auth.slice(7)); if(ue||!u.user)return reply({error:"Invalid session"},401);
    const {problem_id,session_number,answer_text}=await req.json();
    if(session_number!=null&&(!Number.isInteger(session_number)||session_number<1||session_number>372))return reply({error:"Invalid session number"},400);
    if(String(answer_text||"").length>3000)return reply({error:"Keep the final answer short; save working separately."},400);
    if(!problem_id||!String(answer_text||"").trim())return reply({error:"Write an answer or reasoning first."},400);
    const admin=createClient(url,service,{auth:{persistSession:false,autoRefreshToken:false}});
    const {data:member}=await admin.from("profiles").select("id").eq("id",u.user.id).maybeSingle(); if(!member)return reply({error:"Learner profile required"},403);
    const {data:p,error:pe}=await admin.from("content_problems").select("id,answer").eq("id",problem_id).single(); if(pe||!p)return reply({error:"Problem not found"},404);
    const {data:history,error:he}=await admin.from("problem_attempts").select("id,answer_text,solution_video_opened").eq("user_id",u.user.id).eq("problem_id",problem_id).limit(1);
    if(he)throw he;
    const fresh=(history||[]).length===0;
    const correct=grade(p.answer,String(answer_text));
    const credit=fresh&&correct===true;
    const {error:ie}=await admin.from("problem_attempts").insert({user_id:u.user.id,problem_id,session_number:session_number||null,answer_text:String(answer_text),is_correct:correct,evidence_level:"independent",solution_video_opened:false,independent_credit:credit});
    if(ie)throw ie;
    return reply({ok:true,correct,independent_credit:credit,first_attempt:fresh});
  }catch(e){console.error(e);return reply({error:e?.message||"Attempt could not be recorded"},500)}
});
