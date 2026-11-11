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
  if(!username || !password) throw new Error("Enter your login name and PIN / password.");
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

$("password").addEventListener("keydown",e=>{
  if(e.key==="Enter") $("signIn").click();
});

redirectIfSignedIn();

if("serviceWorker" in navigator){navigator.serviceWorker.register("./sw.js").catch(()=>{});}
