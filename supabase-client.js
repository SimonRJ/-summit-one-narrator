import { createClient } from "https://esm.sh/@supabase/supabase-js@2.78.0";

export const SUPABASE_URL = "https://dyidjdagwdvsczudkryt.supabase.co";
export const SUPABASE_PUBLISHABLE_KEY = "sb_publishable_rz3w3N3QxfgLZjTa6xb-hg_mTv9YM-y";

export const supabase = createClient(SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY, {
  auth: {
    persistSession: true,
    autoRefreshToken: true,
    detectSessionInUrl: true,
    storage: window.localStorage,
  },
});

export function usernameToEmail(username) {
  const clean = String(username || "")
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9._-]/g, "")
    .slice(0, 48);
  if (!clean) throw new Error("Enter your login name.");
  return `${clean}@summit-one.local`;
}

export async function signInWithNamePassword(name, password) {
  const email = usernameToEmail(name);
  const { data, error } = await supabase.auth.signInWithPassword({ email, password });
  if (error) throw error;
  return data;
}

export async function signOut() {
  const { error } = await supabase.auth.signOut();
  if (error) throw error;
}

export async function currentUser() {
  const { data, error } = await supabase.auth.getUser();
  // A signed-out visitor is normal, not a failed page load.
  if (error?.name === "AuthSessionMissingError" || error?.code === "session_not_found") return null;
  if (error) throw error;
  return data?.user ?? null;
}

export async function loadProgress() {
  const user = await currentUser();
  if (!user) return null;
  const { data, error } = await supabase
    .from("progress_state")
    .select("*")
    .eq("user_id", user.id)
    .maybeSingle();
  if (error) throw error;
  return data;
}

export async function saveProgress(patch) {
  const user = await currentUser();
  if (!user) throw new Error("Not signed in.");
  const row = {
    user_id: user.id,
    ...patch,
    updated_at: new Date().toISOString(),
  };
  const { data, error } = await supabase
    .from("progress_state")
    .upsert(row, { onConflict: "user_id" })
    .select()
    .single();
  if (error) throw error;
  return data;
}

let sessionQueue=Promise.resolve();
export function upsertSession(session) {
 const snapshot=structuredClone(session);
 const task=sessionQueue.catch(()=>{}).then(()=>writeSession(snapshot));
 sessionQueue=task;return task;
}
async function writeSession(session) {
 try{
 window.dispatchEvent(new CustomEvent("summit-save",{detail:"Saving…"}));
  const user = await currentUser();
  if (!user) throw new Error("Not signed in.");
  const row = { user_id: user.id, ...session };
  const { data, error } = await supabase
    .from("session_records")
    .upsert(row, { onConflict: "user_id,session_number" })
    .select()
    .single();
  if (error) {window.dispatchEvent(new CustomEvent("summit-save",{detail:"Not saved — reconnect and retry"}));throw error;}
  window.dispatchEvent(new CustomEvent("summit-save",{detail:"Saved to cloud"}));
  return data;
 }catch(error){window.dispatchEvent(new CustomEvent("summit-save",{detail:"Not saved — reconnect and retry"}));throw error;}
}

export async function recordAttempt(attempt) {
  const user = await currentUser();
  if (!user) throw new Error("Not signed in.");
  const { data, error } = await supabase
    .from("problem_attempts")
    .insert({ user_id: user.id, ...attempt })
    .select()
    .single();
  if (error) throw error;
  return data;
}

export async function saveExam(exam) {
  const user = await currentUser();
  if (!user) throw new Error("Not signed in.");
  const row = { user_id: user.id, ...exam };
  if (row.id) {
    const { data, error } = await supabase
      .from("exam_sittings")
      .update(row)
      .eq("id", row.id)
      .select()
      .single();
    if (error) throw error;
    return data;
  }
  const { data, error } = await supabase
    .from("exam_sittings")
    .insert(row)
    .select()
    .single();
  if (error) throw error;
  return data;
}

