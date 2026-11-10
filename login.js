import { supabase, usernameToEmail } from "./supabase-client.js";

const $ = id => document.getElementById(id);
const msg = text => $("message").textContent = text;
const FUNCTION_URL = "https://dyidjdagwdvsczudkryt.supabase.co/functions/v1/bootstrap-learner";
const PUBLISHABLE_KEY = "sb_publishable_rz3w3N3QxfgLZjTa6xb-hg_mTv9YM-y";

async function redirectIfSignedIn(){
  const { data } = await supabase.auth.getSession();
  if(data?.session) location.replace("./");
}

async function signIn(username,password){
  const email=usernameToEmail(username);
  const { error }=await supabase.auth.signInWithPassword({email,password});
  if(error) throw error;
}

$("signIn").onclick = async () => {
  try{
    $("signIn").disabled=true;
    msg("Signing in…");
    await signIn($("loginName").value.trim(),$("password").value);
    location.replace("./");
  }catch(e){
    msg(e.message || "Sign in failed.");
  }finally{
    $("signIn").disabled=false;
  }
};

$("createAccount").onclick = async () => {
  try{
    $("createAccount").disabled=true;
    const username=$("loginName").value.trim();
    const password=$("password").value;
    if(username.length<3) throw new Error("Use a login name of at least 3 characters.");
    if(password.length<8) throw new Error("Use a password of at least 8 characters.");
    msg("Creating the learner account…");
    const response=await fetch(FUNCTION_URL,{
      method:"POST",
      headers:{
        "Content-Type":"application/json",
        "apikey":PUBLISHABLE_KEY
      },
      body:JSON.stringify({username,password})
    });
    const body=await response.json().catch(()=>({}));
    if(!response.ok) throw new Error(body.error || "Account setup failed.");
    msg("Account created. Signing in…");
    await signIn(username,password);
    location.replace("./");
  }catch(e){
    msg(e.message || "Account setup failed.");
  }finally{
    $("createAccount").disabled=false;
  }
};

redirectIfSignedIn();
