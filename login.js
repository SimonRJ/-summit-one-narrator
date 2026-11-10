import { supabase, usernameToEmail } from "./supabase-client.js";

const $ = id => document.getElementById(id);
const msg = text => $("message").textContent = text;

async function redirectIfSignedIn(){
  const { data } = await supabase.auth.getSession();
  if(data?.session) location.href="./";
}

$("signIn").onclick = async () => {
  try{
    $("signIn").disabled=true;
    msg("Signing in…");
    const username=$("loginName").value.trim();
    const password=$("password").value;
    const email=usernameToEmail(username);
    const { error } = await supabase.auth.signInWithPassword({email,password});
    if(error) throw error;
    location.href="./";
  }catch(e){
    msg(e.message || "Sign in failed.");
  }finally{
    $("signIn").disabled=false;
  }
};

$("createAccount").onclick = async () => {
  try{
    $("createAccount").disabled=true;
    msg("Creating learner account…");
    const username=$("loginName").value.trim();
    const password=$("password").value;
    if(username.length < 3) throw new Error("Use a login name of at least 3 characters.");
    if(password.length < 8) throw new Error("Use a password of at least 8 characters.");
    const email=usernameToEmail(username);
    const { data, error } = await supabase.auth.signUp({
      email,
      password,
      options:{ data:{ learner_name: username } }
    });
    if(error) throw error;
    if(!data.session){
      msg("Account created, but Supabase is waiting for email confirmation. We need to disable email confirmation once in Supabase Auth settings for username-only learner accounts.");
      return;
    }
    const user=data.user;
    if(user){
      await supabase.from("profiles").upsert({
        id:user.id,
        learner_name:username.toLowerCase(),
        display_name:username
      });
      await supabase.from("progress_state").upsert({user_id:user.id});
    }
    location.href="./";
  }catch(e){
    msg(e.message || "Account setup failed.");
  }finally{
    $("createAccount").disabled=false;
  }
};

redirectIfSignedIn();
