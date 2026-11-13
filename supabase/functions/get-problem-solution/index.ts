import { createClient } from "npm:@supabase/supabase-js@2.78.0";
const url=Deno.env.get("SUPABASE_URL")!, anon=Deno.env.get("SUPABASE_ANON_KEY")!, service=Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const headers={"Access-Control-Allow-Origin":"https://simonrj.github.io","Access-Control-Allow-Headers":"authorization, x-client-info, apikey, content-type","Access-Control-Allow-Methods":"POST, OPTIONS","Content-Type":"application/json"};
const reply=(b:unknown,s=200)=>new Response(JSON.stringify(b),{status:s,headers});
const PROTECTED_VIDEO_BUCKET="summit-one-protected-video";
Deno.serve(async req=>{
  if(req.method==="OPTIONS")return new Response("ok",{headers});
  if(req.method!=="POST")return reply({error:"Method not allowed"},405);
  try{
    const auth=req.headers.get("Authorization");
    if(!auth?.startsWith("Bearer "))return reply({error:"Authentication required"},401);
    const scoped=createClient(url,anon,{global:{headers:{Authorization:auth}},auth:{persistSession:false,autoRefreshToken:false}});
    const {data:u,error:ue}=await scoped.auth.getUser(auth.slice(7));
    if(ue||!u.user)return reply({error:"Invalid session"},401);
    const {problem_id,session_number}=await req.json();
    if(!problem_id)return reply({error:"Missing problem_id"},400);
    const admin=createClient(url,service,{auth:{persistSession:false,autoRefreshToken:false}});
    const {data:member}=await admin.from("profiles").select("id").eq("id",u.user.id).maybeSingle();
    if(!member)return reply({error:"Learner profile required"},403);
    const {data:attempt}=await admin.from("problem_attempts")
      .select("id").eq("user_id",u.user.id).eq("problem_id",problem_id)
      .in("evidence_level",["independent","guided"]).not("answer_text","is",null).neq("answer_text","").limit(1).maybeSingle();
    if(!attempt)return reply({error:"Submit a final answer before opening the worked solution. A supported attempt counts."},403);
    const {data:p,error:pe}=await admin.from("content_problems")
      .select("id,title,answer,solution_text,spoken_script,source_type").eq("id",problem_id).single();
    if(pe||!p)return reply({error:"Problem not found"},404);
    await admin.from("problem_attempts").insert({
      user_id:u.user.id,problem_id,session_number:session_number||null,answer_text:null,is_correct:null,
      evidence_level:"viewed",solution_video_opened:true,independent_credit:false
    });
    let video_url:string|null=null;
    let video_expires_in:number|null=null;
    const expires=3600;
    const {data:signed,error:signedError}=await admin.storage.from(PROTECTED_VIDEO_BUCKET)
      .createSignedUrl(`${problem_id}.mp4`,expires);
    if(!signedError&&signed?.signedUrl){video_url=signed.signedUrl;video_expires_in=expires}
    return reply({
      ok:true,title:p.title,answer:p.answer,solution_text:p.solution_text,spoken_script:p.spoken_script,
      video_url,video_expires_in
    });
  }catch(e){
    console.error(e);
    return reply({error:e?.message||"Solution could not be opened"},500);
  }
});