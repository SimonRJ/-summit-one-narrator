import { supabase, usernameToEmail, SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY } from "./supabase-client.js";

const $ = id => document.getElementById(id);
const msg = (text, kind="") => {
  $("message").textContent = text;
  $("message").dataset.kind = kind;
};

async function redirectIfSignedIn(){
  const { data } = await supabase.auth.getSession();
  if(data?.session) location.href="./";
}

async function signIn(){
  const username=$("loginName").value.trim();
  const password=$("password").value;
  if(!username || !password) throw new Error("Enter your login name and password.");
  const email=usernameToEmail(username);
  const { error }=await supabase.auth.signInWithPassword({email,password});
  if(error) throw error;
}

$("signIn").onclick=async()=>{
  try{
    $("signIn").disabled=true;
    msg("Signing in…");
    await signIn();
    location.href="./";
  }catch(e){
    msg(e.message || "Sign in failed.","error");
  }finally{
    $("signIn").disabled=false;
  }
};

$("createAccount").onclick=async()=>{
  try{
    $("createAccount").disabled=true;
    msg("Creating the learner account…");
    const username=$("loginName").value.trim();
    const password=$("password").value;
    if(username.length<3) throw new Error("Use a login name of at least 3 characters.");
    if(password.length<8) throw new Error("Use a password of at least 8 characters.");

    const response=await fetch(`${SUPABASE_URL}/functions/v1/bootstrap-learner`,{
      method:"POST",
      headers:{
        "Content-Type":"application/json",
        "apikey":SUPABASE_PUBLISHABLE_KEY
      },
      body:JSON.stringify({username,password})
    });
    const body=await response.json().catch(()=>({}));
    if(!response.ok) throw new Error(body.error || "Learner account could not be created.");

    msg("Account created. Signing in…");
    await signIn();
    location.href="./";
  }catch(e){
    const text=e.message || "Account setup failed.";
    msg(text,"error");
    if(/already exists/i.test(text)){
      $("createAccount").hidden=true;
      $("subtitle").textContent="The learner account is ready. Sign in to continue.";
    }
  }finally{
    $("createAccount").disabled=false;
  }
};

$("password").addEventListener("keydown",e=>{
  if(e.key==="Enter") $("signIn").click();
});

redirectIfSignedIn();
