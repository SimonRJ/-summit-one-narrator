import { supabase, usernameToEmail, currentUser } from "./supabase-client.js?v=auth-20261112";

const $ = id => document.getElementById(id);
const msg = (text, kind="") => {
  $("message").textContent = text;
  $("message").dataset.kind = kind;
};

// Only allow known local destinations, never arbitrary redirect URLs.
const requestedNext = new URLSearchParams(location.search).get("next") || "";
const destination = /^tests\.html(?:\?[^#]*)?$/.test(requestedNext) ? "./"+requestedNext : "./";
if(destination.startsWith("./tests.html")) $("subtitle").textContent="Sign in to open the Test Centre.";
async function redirectIfSignedIn(){
  try { if(await currentUser()) location.replace(destination); }
  catch(e) { msg(e.message || "Unable to check your sign-in. Please try again.","error"); }
}

async function signIn(){
  const username=$("loginName").value.trim();
  const password=$("password").value;
  if(!username || !password) throw new Error("Enter your login name and PIN / password.");
  const email=usernameToEmail(username);
  const { error }=await supabase.auth.signInWithPassword({email,password});
  if(error) throw error;
}

$("learnerSignIn").addEventListener("submit",async event=>{
  event.preventDefault();
  if($("signIn").disabled)return;
  try{
    $("signIn").disabled=true;
    msg("Signing in…");
    await signIn();
    location.replace(destination === "./" ? "./welcome.html?from=login" : destination);
  }catch(e){
    msg(e.message || "Sign in failed.","error");
  }finally{
    $("signIn").disabled=false;
  }
});
$("signIn").disabled=false;

redirectIfSignedIn().finally(()=>window.SummitLoader?.ready());

if("serviceWorker" in navigator){navigator.serviceWorker.register("./sw.js").catch(()=>{});}

